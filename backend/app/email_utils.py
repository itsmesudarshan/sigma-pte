"""
Sends OTP verification emails using Gmail's free SMTP relay via Python's
built-in smtplib — no paid email API, no third-party service.

Requires two environment variables set on the backend:
  SMTP_EMAIL          — a Gmail address you control (e.g. yourapp@gmail.com)
  SMTP_APP_PASSWORD    — a free Google "App Password" for that account
                          (Google Account -> Security -> 2-Step Verification
                          must be ON -> App Passwords -> generate one for
                          "Mail". This is NOT your normal Gmail password.)

If these aren't set, OTP sending fails loudly rather than silently — signup
can't proceed without a working mail path, so this is surfaced as a clear
error rather than pretending to send.
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_EMAIL = os.getenv("SMTP_EMAIL", "").strip()
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD", "").strip()
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def is_email_configured() -> bool:
    return bool(SMTP_EMAIL and SMTP_APP_PASSWORD)


def send_otp_email(to_email: str, otp_code: str) -> None:
    if not is_email_configured():
        raise RuntimeError(
            "Email sending isn't configured on the server yet (SMTP_EMAIL / "
            "SMTP_APP_PASSWORD environment variables are missing)."
        )

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your Prepwise verification code: {otp_code}"
    message["From"] = SMTP_EMAIL
    message["To"] = to_email

    text_body = f"Your Prepwise verification code is: {otp_code}\n\nThis code expires in 10 minutes."
    html_body = f"""
    <div style="font-family: sans-serif; max-width: 420px; margin: 0 auto;">
      <h2 style="color: #14213D;">Prepwise</h2>
      <p>Your verification code is:</p>
      <p style="font-size: 32px; font-weight: 700; letter-spacing: 6px; color: #2A5CDB;">{otp_code}</p>
      <p style="color: #5B6472; font-size: 13px;">This code expires in 10 minutes. If you didn't request this, you can ignore this email.</p>
    </div>
    """

    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, message.as_string())
