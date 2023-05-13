"""Admin's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.template import Template

from admin.schemas import AdminSchema
from admin.schemas import AdminUpdate
from admin.models import Admin
from core.database import Database
# from auth.utils import get_password_hash
from auth.exceptions import InvalidCredentials
from admin.exceptions import AdminException



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
async def admin_edit_page(request: Request, id: int, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Admin'

    admin = database.query(Admin).filter(Admin.id == id).first()

    if not admin:
        raise AdminException

    context['user'] = admin

    return template.TemplateResponse('admin/edit.html', context)


@router.post('/create', status_code=201)
async def admin_create_local(request: Request, admin_data: AdminSchema, database: Session = Depends(Database)):
    if not request.state.authenticated:
        raise InvalidCredentials

    admin = Admin(
        tag=admin_data.tag,
        name=admin_data.name,
        birth_date=admin_data.birth_date,
        email=admin_data.email,
        phone=admin_data.phone,
        password=admin_data.password,
    )

    database.add(admin)
    database.commit()

    return {'message': f"Admin '{admin_data.name}' criado com sucesso!"}


@router.post('/edit/{id}', status_code=201)
async def admin_edit_local(request: Request, id: int, admin_data: AdminUpdate, database: Session = Depends(Database)):
    if not request.state.authenticated:
        return InvalidCredentials

    admin = database.query(Admin).filter(Admin.id == id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.name=admin_data.name
    admin.phone=admin_data.phone

    if (admin_data.password):
        admin.password=admin_data.password

    database.commit()

    return {'message': f"Admin '{admin_data.name}' alterado com sucesso!"}

@router.delete('/delete/{id}', status_code=201)
async def admin_delete_local(request: Request, id: int, database: Session = Depends(Database)):
    if not request.state.authenticated:
        return InvalidCredentials

    admin = database.query(Admin).filter(Admin.id == id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    database.delete(admin)
    database.commit()

    return {'message': "Admin deletado com sucesso!"}
