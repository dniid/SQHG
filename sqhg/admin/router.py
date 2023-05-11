"""Admin's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.template import Template

from admin.models import Admin
from core.database import Database

import re



router = APIRouter()


@router.get('/')
async def dummy_endpoint():
    return {'message': 'admin'}


@router.get('/list', response_class=HTMLResponse)
async def admin_list_page(request: Request, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Admin'

    users = database.query(Admin).all()

    context['users'] = users

    return template.TemplateResponse('admin/list.html', context)


@router.get('/create', response_class=HTMLResponse)
async def admin_create_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Criar Admin'

    return template.TemplateResponse('admin/create.html', context)

@router.get('/edit/{id}', response_class=HTMLResponse)
async def admin_list_page(request: Request, id: int, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Admin'

    admin = database.query(Admin).filter(Admin.id == id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    context['user'] = admin

    return template.TemplateResponse('admin/edit.html', context)


@router.post('/create', response_class=HTMLResponse)
async def admin_create_page(request: Request, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    form_data = await request.form()

    regex = r"\d+"
    valid_phone = "".join(re.findall(regex, form_data['phone']))

    admin = Admin()
    admin.tag = form_data['tag']
    admin.name = form_data['name']
    admin.birth_date = form_data['birthDate']
    admin.email = form_data['email']
    admin.phone = valid_phone
    admin.password = form_data['password']

    database.add(admin)
    database.commit()

    raise HTTPException(status_code=303, headers={"Location": "/admin/list"})


@router.post('/edit/{id}', response_class=HTMLResponse)
async def admin_create_page(request: Request, id: int, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    admin = database.query(Admin).filter(Admin.id == id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    form_data = await request.form()

    regex = r"\d+"
    valid_phone = "".join(re.findall(regex, form_data['phone']))
    
    admin.tag = form_data['tag']
    admin.name = form_data['name']
    admin.birth_date = form_data['birthDate']
    admin.email = form_data['email']
    admin.phone = valid_phone

    if not (form_data['password'] == ''):
        admin.password = form_data['password']

    database.commit()

    raise HTTPException(status_code=303, headers={"Location": "/admin/list"})