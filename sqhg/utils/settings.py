"""Settings utils for SQHG's backend."""

import os


def getstr(key, default=''):
    value = os.getenv(key, '')
    return value if value else default


def getint(key, default=0, base=10):
    value = os.getenv(key, '').strip()
    return int(value, base) if value else default


def getbool(key, default=False):
    value = os.getenv(key, '').strip()
    return value.lower()[:1] not in ['0', 'f', 'n'] if value else default


def getlist(key, default=None, separator=','):
    default = [] if default is None else default
    value = os.getenv(key, '').strip()
    return value.split(separator) if value else default
