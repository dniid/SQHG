"""Auth's FastAPI router endpoints for SQHG's backend."""

import requests
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.models import Admin
from admin.schemas import AdminSchema
from core.database import Database
from core.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from core.template import Template

from auth.schemas import JWToken
from auth.utils import (
    authenticate_user,
    create_access_token,
    get_current_user
)
from auth.exceptions import InvalidCredentials


router = APIRouter()


@router.post('/token', response_model=JWToken)
async def login_for_access_token(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    database: Session = Depends(Database)
):
    form_user = database.query(Admin).filter(Admin.email == request.username).first()
    user = authenticate_user(form_user, request.password)
    if not user:
        raise InvalidCredentials
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=AdminSchema)
async def read_users_me(current_user: Annotated[Admin, Depends(get_current_user)]):
    return current_user


@router.get('/login')
async def login_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    admin: bool = False
):
    context = {'request': request}
    context['subtitle'] = 'Login'

    if admin:
        context['subtitle'] = 'Admin Login'
        return template.TemplateResponse('auth/login_admin.html', context)

    return template.TemplateResponse('auth/login.html', context)


@router.post('/login')
async def login(request: Request):
    print(await request.body())
    # token = requests.post(request.url_for('login_for_access_token'),
    #     data={

    #     }
    # )

    return 'test'
