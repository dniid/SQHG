"""Admin's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.template import Template


router = APIRouter()


@router.get('/')
async def dummy_endpoint():
    return {'message': 'admin'}


@router.get('/list', response_class=HTMLResponse)
async def admin_list_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}

    return template.TemplateResponse('admin/list.html', context)


@router.get('/create', response_class=HTMLResponse)
async def admin_create_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}

    return template.TemplateResponse('admin/create.html', context)
