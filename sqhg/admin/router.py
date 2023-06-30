"""Admin's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.template import Template

from admin.schemas import AdminSchema, AdminUpdate
from admin.models import Admin
from core.database import Database
from auth.utils import get_password_hash
from auth.exceptions import InvalidCredentials


router = APIRouter()


@router.get('/list', response_class=HTMLResponse)
async def admin_list_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database),
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Admin'
    context['users'] = database.query(Admin).all()

    return template.TemplateResponse('admin/list.html', context)


@router.get('/create', response_class=HTMLResponse)
async def admin_create_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Criar Admin'

    return template.TemplateResponse('admin/create.html', context)


@router.get('/edit/{id}', response_class=HTMLResponse)
async def admin_edit_page(
    request: Request,
    id: int,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database),
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Admin'

    admin = database.query(Admin).filter(Admin.id==id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin não encontrado')
    context['user'] = admin.first()

    return template.TemplateResponse('admin/edit.html', context)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
async def admin_create(request: Request, admin_data: AdminSchema, database: Session = Depends(Database)):
    if not request.state.authenticated:
        raise InvalidCredentials

    admin = Admin(
        tag=admin_data.tag,
        name=admin_data.name,
        birth_date=admin_data.birth_date,
        email=admin_data.email,
        phone=admin_data.phone,
        password=get_password_hash(admin_data.password),
    )

    database.add(admin)
    database.commit()

    return {'message': f"Admin '{admin_data.name}' criado com sucesso!"}


@router.post('/edit/{id}', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def admin_edit(request: Request, id: int, admin_data: AdminUpdate, database: Session = Depends(Database)):
    if not request.state.authenticated:
        return InvalidCredentials

    admin = database.query(Admin).filter(Admin.id==id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin não encontrado')
    admin = admin.first()

    for key, value in admin_data.dict(exclude_unset=True).items():
        if key == 'password':
            setattr(admin, key, get_password_hash(value))
            continue
        setattr(admin, key, value)

    database.commit()

    return {'message': f"Admin '{admin_data.name}' alterado com sucesso!"}


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def admin_delete(request: Request, id: int, database: Session = Depends(Database)):
    if not request.state.authenticated:
        return InvalidCredentials

    admin = database.query(Admin).filter(Admin.id==id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin não encontrado')

    database.delete(admin.first())
    database.commit()

    return {'message': 'Admin deletado com sucesso!'}
