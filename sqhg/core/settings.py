"""Settings for SQHG's backend."""

from utils.settings import getstr, getint


# Postgres settings

POSTGRES_USERNAME = getstr('POSTGRES_USERNAME', 'sqhg')
POSTGRES_PASSWORD = getstr('POSTGRES_PASSWORD', 'sqhg')

POSTGRES_HOST = getstr('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = getint('POSTGRES_PORT', 5432)

POSTGRES_DATABASE = getstr('POSTGRES_DATABASE', 'sqhg')
