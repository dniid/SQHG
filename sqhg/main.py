#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.database import BaseModel, engine
from core.logger import LogConfig
from core.middlewares import AuthMiddleware
from core.template import Template

from utils.settings import find_dirs

# Import models for SQLAlchemy's database base metadata
from admin.models import Admin  # noqa: F401
from sap.models import Area, Superior  # noqa: F401
from survey.models import Survey, SurveyModel, Question, Option, Answer  # noqa: F401
from user.models import Token  # noqa: F401

import admin.router
import auth.router
import survey.router
import user.router


logging.config.dictConfig(LogConfig().dict())
logger = logging.getLogger('sqhg')

BaseModel.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.add_middleware(AuthMiddleware)

app.include_router(admin.router.router, prefix='/admin', tags=['Admin'])
app.include_router(survey.router.router, prefix='/survey', tags=['Survey'])
app.include_router(user.router.router, prefix='/user', tags=['User'])
app.include_router(auth.router.router, tags=['Auth'])


# Searches for directories named 'static' and then mount them dynamically
for static in find_dirs('.', 'static'):
    app.mount('/static', StaticFiles(directory=static), name=static)


@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}

    return template.TemplateResponse('homepage.html', context)
