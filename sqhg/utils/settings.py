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


def find_dirs(root_dir, dir_name):
    """
    Searches for all directories 'dir_name'
    within the specified root directory and
    returns their absolute paths.
    """
    dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dir_name in dirnames:
            dir = os.path.join(dirpath, dir_name)
            dirs.append(dir)

    return dirs
