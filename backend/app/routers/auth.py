from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models import User, EmailOTP
from app.schemas import SignupRequest, VerifyOtpRequest, LoginRequest, AuthResponse, UserOut
from app.auth import (
    validate_email_domain, hash_password, verify_password, create_token, get_current_user,
    ALLOWED_DOMAINS, generate_otp, hash_otp, verify_otp, OTP_EXPIRY_MINUTES, OTP_RESEND_COOLDOWN_SECONDS,
)
from app.email_utils import send_otp_email, is_email_configured

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup/request-otp")
def request_signup_otp(payload: SignupRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()

    if not validate_email_domain(email):
        raise HTTPException(status_code=400, detail="Only Gmail, Yahoo, and Outlook email addresses are allowed.")

    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    if not is_email_configured():
        raise HTTPException(
            status_code=503,
            detail="Email verification isn't configured on the server yet. Contact the site owner.",
        )

    # Cooldown: don't allow spamming OTP requests for the same email
    recent = (
        db.query(EmailOTP)
        .filter(EmailOTP.email == email, EmailOTP.consumed == 0)
        .order_by(EmailOTP.created_at.desc())
        .first()
    )
    if recent and recent.created_at:
        elapsed = (datetime.now(timezone.utc) - recent.created_at.replace(tzinfo=timezone.utc)).total_seconds()
        if elapsed < OTP_RESEND_COOLDOWN_SECONDS:
            wait = int(OTP_RESEND_COOLDOWN_SECONDS - elapsed)
            raise HTTPException(status_code=429, detail=f"Please wait {wait}s before requesting another code.")

    otp = generate_otp()

    otp_record = EmailOTP(
        email=email,
        otp_hash=hash_otp(otp),
        pending_password_hash=hash_password(payload.password),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES),
        consumed=0,
    )
    db.add(otp_record)
    db.commit()

    try:
        send_otp_email(email, otp)
    except Exception as e:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=502, detail=f"Couldn't send verification email: {e}")

    return {"message": f"A verification code was sent to {email}.", "expires_in_minutes": OTP_EXPIRY_MINUTES}


@router.post("/signup/verify", response_model=AuthResponse)
def verify_signup_otp(payload: VerifyOtpRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()

    otp_record = (
        db.query(EmailOTP)
        .filter(EmailOTP.email == email, EmailOTP.consumed == 0)
        .order_by(EmailOTP.created_at.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(status_code=400, detail="No pending verification for this email. Request a new code.")

    if datetime.now(timezone.utc) > otp_record.expires_at.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="This code has expired. Request a new one.")

    if not verify_otp(payload.otp.strip(), otp_record.otp_hash):
        raise HTTPException(status_code=400, detail="Incorrect verification code.")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    user = User(email=email, password_hash=otp_record.pending_password_hash)
    db.add(user)
    otp_record.consumed = 1
    db.commit()
    db.refresh(user)

    token = create_token(user.id, user.email)
    return AuthResponse(token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = create_token(user.id, user.email)
    return AuthResponse(token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.get("/allowed-domains")
def allowed_domains():
    return sorted(ALLOWED_DOMAINS)
