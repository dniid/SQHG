"""Jinja2 configuration for SQHG's backend."""

from fastapi.templating import Jinja2Templates

from core.extensions import StaticFilesExtension

from utils.settings import find_dirs


async def Template():
    templates = Jinja2Templates(directory=find_dirs('.', 'templates'))
    templates.env.static_dirs = find_dirs('.', 'static')
    templates.env.add_extension(StaticFilesExtension)

    yield templates
