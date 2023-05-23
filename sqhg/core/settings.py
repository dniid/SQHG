"""Settings for SQHG's backend."""

from utils.settings import getstr, getint


# Environment settings

ENVIRONMENT = getstr('MODE', 'development')

# Postgres settings

POSTGRES_USERNAME = getstr('POSTGRES_USERNAME', 'sqhg')
POSTGRES_PASSWORD = getstr('POSTGRES_PASSWORD', 'sqhg')

POSTGRES_HOST = getstr('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = getint('POSTGRES_PORT', 5432)

POSTGRES_DATABASE = getstr('POSTGRES_DATABASE', 'sqhg')

# Security settings

SECRET_KEY = getstr('SECRET_KEY', '')
ALGORITHM = getstr('ALGORITHM', '')

ACCESS_TOKEN_EXPIRE_MINUTES = getint('ACCESS_TOKEN_EXPIRE_MINUTES', 60 * 24 * 30)
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = getint('PASSWORD_RESET_TOKEN_EXPIRE_MINUTES', 15)

# SMTP settings

SMTP_USERNAME = getstr('SMTP_USERNAME', '')
SMTP_PASSWORD = getstr('SMTP_PASSWORD', '')
SMTP_HOST = getstr('SMTP_HOST', 'localhost')
SMTP_PORT = getint('SMTP_PORT', 587)
SMTP_MAIL_FROM = getstr('SMTP_MAIL_FROM', 'suporte@sqhg.com')
