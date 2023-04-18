#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.database import BaseModel, engine
from core.logger import LogConfig
from core.template import Template

from utils.settings import find_dirs

# Import models for SQLAlchemy's database base metadata
# pylint: disable=unused-import
from admin.models import Admin
from sap.models import Area, Superior
from survey.models import Survey, SurveyModel, Question, Option, Answer
from user.models import Token

import admin.router
import auth.router
import survey.router
import user.router


logging.config.dictConfig(LogConfig().dict())
logger = logging.getLogger('sqhg')

BaseModel.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

app.include_router(admin.router.router, prefix='/admin', tags=['Admin'])
app.include_router(survey.router.router, prefix='/survey', tags=['Survey'])
app.include_router(user.router.router, prefix='/user', tags=['User'])
app.include_router(auth.router.router, tags=['Auth'])


# Searches for directories named 'static' and then mount them dynamically
for static in find_dirs('.', 'static'):
    app.mount(static[1:], StaticFiles(directory=static), name=static)


@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request, templates: Jinja2Templates = Depends(Template)):
    context = {'request': request}
    return templates.TemplateResponse('homepage.html', context)
