"""Auth's FastAPI router endpoints for SQHG's backend."""

from datetime import timedelta

from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.models import Admin
from core.database import Database
from core.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from core.template import Template

from auth.schemas import LoginData
from auth.utils import (
    authenticate_user,
    create_access_token,
)
from auth.exceptions import InvalidCredentials


router = APIRouter()


@router.get('/login')
async def login_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    admin: bool = False
):
    if request.state.authenticated:
        return RedirectResponse('/')

    context = {'request': request}
    context['subtitle'] = 'Login'

    if admin:
        context['subtitle'] = 'Admin Login'
        return template.TemplateResponse('auth/login_admin.html', context)

    return template.TemplateResponse('auth/login.html', context)


@router.post('/login')
async def login(credentials: LoginData, database: Session = Depends(Database)):
    form_user = database.query(Admin).filter(Admin.email == credentials.email).first()
    if not form_user:
        raise InvalidCredentials

    user = authenticate_user(form_user, credentials.password)
    if not user:
        raise InvalidCredentials

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires,
    )

    response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key='session_token', value=access_token)
    return response
