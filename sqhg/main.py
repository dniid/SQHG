#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.database import BaseModel, engine, SessionLocal
from core.logger import LogConfig
from core.middlewares import AuthMiddleware
from core.template import Template
from core.settings import (
    SUPERUSER_EMAIL,
    SUPERUSER_USERNAME,
    SUPERUSER_PASSWORD,
)

from auth.utils import get_password_hash
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
import report.router


logging.config.dictConfig(LogConfig().dict())
logger = logging.getLogger('sqhg')

BaseModel.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.add_middleware(AuthMiddleware)

app.include_router(admin.router.router, prefix='/admin', tags=['Admin'])
app.include_router(survey.router.router, prefix='/survey', tags=['Survey'])
app.include_router(user.router.router, prefix='/user', tags=['User'])
app.include_router(report.router.router, prefix='/report', tags=['Report'])
app.include_router(auth.router.router, tags=['Auth'])

# Searches for directories named 'static' and then mount them dynamically
for static in find_dirs('.', 'static'):
    app.mount(static[1:], StaticFiles(directory=static), name=static)


@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}

    return template.TemplateResponse('homepage.html', context)


@app.on_event("startup")
async def check_superuser():
    database = SessionLocal()

    logger.info('Verifying superuser...')
    admin = database.query(Admin).filter(Admin.email == SUPERUSER_EMAIL).first()
    if not admin:
        logger.info('Creating superuser...')
        password = get_password_hash(SUPERUSER_PASSWORD)
        admin = Admin(
            tag='000000000000',
            name=SUPERUSER_USERNAME,
            birth_date='2000-01-01',
            email=SUPERUSER_EMAIL,
            phone='00000000000',
            password=password
        )
        database.add(admin)
        database.commit()

    database.close()
