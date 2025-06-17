import smtplib
from email.message import EmailMessage
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


async def send_password_reset_email(to_email: str, token: str):
    subject = "Password Reset"
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    body = f"Click the link to reset your password: {reset_url}"

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
        msg["To"] = to_email
        msg.set_content(body)

        if settings.EMAIL_USE_SSL:
            server = smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT)
        else:
            server = smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT)
            if settings.EMAIL_USE_TLS:
                server.starttls()

        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info(f"Password reset email sent to {to_email}")
    except Exception as e:
        logger.exception(f"Failed to send email to {to_email}: {e}")
