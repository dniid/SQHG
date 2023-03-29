""""LogConfig pydantic-based."""

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "sqhg"
    LOG_FORMAT: str = "[%(asctime)s] [%(levelname)s] %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/sqhg/sqhg.log",
            "level": "INFO",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["file"], "level": LOG_LEVEL},
    }
