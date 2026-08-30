"""
Sends OTP verification emails using Brevo's (formerly Sendinblue) free
transactional email API over HTTPS — not SMTP.

This matters specifically because Render's free tier blocks all outbound
SMTP traffic (ports 25, 465, 587) as of September 2025, which silently
hangs any smtplib-based approach (including Gmail SMTP) forever with no
error. Brevo's API runs over plain HTTPS (port 443), so it isn't affected.

Requires two environment variables on the backend:
  BREVO_API_KEY       — from Brevo dashboard: Settings -> SMTP & API -> API Keys
  BREVO_SENDER_EMAIL   — an email address you've verified in Brevo under
                          Senders, Domains & Dedicated IPs -> Senders
                          (Single Sender Verification — no domain needed,
                          just click the confirmation link Brevo emails you)

Free tier: 300 emails/day, no credit card required. Once your sender email
is verified, you can send to any recipient (unlike Resend's sandbox mode,
which restricts unverified-domain accounts to only your own signup email).

If these variables aren't set, sending fails loudly rather than silently —
signup can't proceed without a working mail path, so this is surfaced as a
clear error rather than pretending to send.
"""

import os
import json
from urllib import request as urlrequest, error as urlerror

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL", "").strip()
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def is_email_configured() -> bool:
    return bool(BREVO_API_KEY and BREVO_SENDER_EMAIL)


def send_otp_email(to_email: str, otp_code: str) -> None:
    if not is_email_configured():
        raise RuntimeError(
            "Email sending isn't configured on the server yet (BREVO_API_KEY / "
            "BREVO_SENDER_EMAIL environment variables are missing)."
        )

    html_body = f"""
    <div style="font-family: sans-serif; max-width: 420px; margin: 0 auto;">
      <h2 style="color: #14213D;">Prepwise</h2>
      <p>Your verification code is:</p>
      <p style="font-size: 32px; font-weight: 700; letter-spacing: 6px; color: #2A5CDB;">{otp_code}</p>
      <p style="color: #5B6472; font-size: 13px;">This code expires in 10 minutes. If you didn't request this, you can ignore this email.</p>
    </div>
    """
    text_body = f"Your Prepwise verification code is: {otp_code}\n\nThis code expires in 10 minutes."

    payload = json.dumps({
        "sender": {"email": BREVO_SENDER_EMAIL, "name": "Prepwise"},
        "to": [{"email": to_email}],
        "subject": f"Your Prepwise verification code: {otp_code}",
        "htmlContent": html_body,
        "textContent": text_body,
    }).encode("utf-8")

    req = urlrequest.Request(
        BREVO_API_URL,
        data=payload,
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urlrequest.urlopen(req, timeout=15) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"Brevo returned unexpected status {resp.status}")
    except urlerror.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Brevo API error ({e.code}): {error_body}")
    except urlerror.URLError as e:
        raise RuntimeError(f"Couldn't reach Brevo API: {e.reason}")
