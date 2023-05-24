"""FastAPI Mail configuration for SQHG's backend."""

import logging

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema

from utils.settings import find_dirs
from core.settings import (
    ENVIRONMENT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_MAIL_FROM,
)


logger = logging.getLogger('sqhg')


class FastMailConfig(FastMail):
    """FastAPI Mail configuration for SQHG's backend."""

    def __init__(self) -> None:
        self.config = ConnectionConfig(
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

    async def send_message(
        self, message: MessageSchema, template_name: str = None
    ) -> None:
        if ENVIRONMENT == 'development':
            with self.record_messages() as outbox:
                await super().send_message(message, template_name)
                logger.debug(outbox[0])
        else:
            await super().send_message(message, template_name)


async def Email():  # noqa: N802
    yield FastMailConfig()
