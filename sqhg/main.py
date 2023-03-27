#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.database import BaseModel, engine
from core.extensions import StaticFilesExtension

from utils.settings import find_dirs

import admin.router
import survey.router
import user.router


BaseModel.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router.router, prefix='/admin', tags=['Admin'])
app.include_router(survey.router.router, prefix='/survey', tags=['Survey'])
app.include_router(user.router.router, prefix='/user', tags=['User'])


static_dirs = find_dirs('.', 'static')
for dir in static_dirs:
    app.mount(f"/static/{dir}", StaticFiles(directory=dir), name=dir)

templates = Jinja2Templates(directory=find_dirs('.', 'templates'))
templates.env.add_extension(StaticFilesExtension)


@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('components/navbar.html', context)
