"""FastAPI Mail configuration for SQHG's backend."""

from fastapi_mail import FastMail, ConnectionConfig

from utils.settings import find_dirs
from core.settings import (
    ENVIRONMENT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_MAIL_FROM,
)


async def Email():  # noqa: N802
    config = ConnectionConfig(
        MAIL_USERNAME=SMTP_USERNAME,
        MAIL_PASSWORD=SMTP_PASSWORD,
        MAIL_SERVER=SMTP_HOST,
        MAIL_PORT=SMTP_PORT,
        MAIL_FROM=SMTP_MAIL_FROM,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        TEMPLATE_FOLDER=find_dirs('auth', 'email')[0],
        SUPPRESS_SEND=1 if ENVIRONMENT == 'development' else 0,
        MAIL_DEBUG=1 if ENVIRONMENT == 'development' else 0,
    )

    yield FastMail(config)
