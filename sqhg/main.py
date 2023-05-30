#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

import os
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
static_directories = [(os.path.dirname(static)[2:], 'static') for static in find_dirs('static')]
app.mount('/static', StaticFiles(packages=static_directories), name='static')


@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}

    return template.TemplateResponse('homepage.html', context)


@app.on_event('startup')
def start_population():
    import multiprocessing

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.sql import text

    from core.database import engine
    from utils import fake_data

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    session.execute(text('SET FOREIGN_KEY_CHECKS=0'))

    for _ in range(100):
        pool = multiprocessing.Pool(processes=6)

        area_data = pool.map(fake_data.generate_area_data, range(6))
        admin_data = pool.map(fake_data.generate_admin_data, range(6))
        answer_data = pool.map(fake_data.generate_answer_data, range(6))
        survey_data = pool.map(fake_data.generate_survey_model_data, range(6))
        model_data = pool.map(fake_data.generate_survey_data, range(6))
        question_data = pool.map(fake_data.generate_question_data, range(6))
        superior_data = pool.map(fake_data.generate_superior_data, range(6))
        token_data = pool.map(fake_data.generate_token_data, range(6))
        option_data = pool.map(fake_data.generate_option_data, range(6))

        db_data = []
        db_data.extend(area_data[0])
        db_data.extend(admin_data[0])
        db_data.extend(answer_data[0])
        db_data.extend(survey_data[0])
        db_data.extend(model_data[0])
        db_data.extend(question_data[0])
        db_data.extend(superior_data[0])
        db_data.extend(token_data[0])
        db_data.extend(option_data[0])

        pool.close()

        for index in range(0, len(db_data), 1000):
            chunk = db_data[index:index+1000]
            print(f'Bulk saving... current index: {index}', flush=True)
            session.bulk_save_objects(chunk)

    session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
    logger.info('Commiting changes')
    session.commit()

    session.close()
