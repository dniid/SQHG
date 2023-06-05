"""Admin's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.template import Template


router = APIRouter()

@router.get('/')
async def dummy_endpoint():
    return {'message': 'report'}

@router.get('/view', response_class=HTMLResponse)
async def report_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Relatório'

    return template.TemplateResponse('report/report.html', context)
