#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

from logging.config import dictConfig
import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.database import BaseModel, engine
from core.logger import LogConfig
from core.template import Template

from utils.settings import find_dirs

import admin.router
import auth.router
import survey.router
import user.router


dictConfig(LogConfig().dict())
logger = logging.getLogger('sqhg')

BaseModel.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router.router, prefix='/admin', tags=['Admin'])
app.include_router(sap.router.router, prefix='/sap', tags=['SAP'])
app.include_router(survey.router.router, prefix='/survey', tags=['Survey'])
app.include_router(user.router.router, prefix='/user', tags=['User'])
app.include_router(auth.router.router, tags=['Auth'])


# Searches for directories named 'static' and then mount them dynamically
for static in find_dirs('.', 'static'):
    app.mount(static[1:], StaticFiles(directory=static), name=static)


@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request, templates: Jinja2Templates = Depends(Template)):
    context = {'request': request}
    return templates.TemplateResponse('base.html', context)
