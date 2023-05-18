"""Settings for SQHG's backend."""

from utils.settings import getstr, getint


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

# Superuser constants

SUPERUSER_EMAIL = getstr('SUPERUSER_EMAIL', 'admin@admin.com')
SUPERUSER_USERNAME = getstr('SUPERUSER_USERNAME', 'admin')
SUPERUSER_PASSWORD = getstr('SUPERUSER_PASSWORD', 'admin')
