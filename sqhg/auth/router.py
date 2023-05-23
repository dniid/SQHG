"""Auth's FastAPI router endpoints for SQHG's backend."""

from datetime import timedelta

from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy.orm import Session

from admin.models import Admin
from core.database import Database
from core.email import Email
from core.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
)
from core.template import Template

from auth.schemas import LoginData, ForgotPasswordData
from auth.utils import (
    authenticate_user,
    create_access_token,
)
from auth.exceptions import InvalidCredentials


router = APIRouter()


@router.get('/login', response_class=HTMLResponse)
async def login_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    admin: bool = False,
):
    if request.state.authenticated:
        return RedirectResponse('/')

    context = {'request': request}
    context['subtitle'] = 'Login'

    if admin:
        context['subtitle'] = 'Admin Login'
        return template.TemplateResponse('auth/login_admin.html', context)

    return template.TemplateResponse('auth/login.html', context)


@router.get('/forgot_password', response_class=HTMLResponse)
async def forgot_password_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
):
    context = {'request': request}
    context['subtitle'] = 'Esqueci a senha'

    return template.TemplateResponse('auth/forgot_password.html', context)


@router.get('/reset_password/{token}', response_class=HTMLResponse)
async def reset_password_page(
    request: Request,
    token: str,
    template: Jinja2Templates = Depends(Template),
):
    context = {'request': request}
    context['subtitle'] = 'Redefinir Senha'

    return template.TemplateResponse('auth/reset_password.html', context)


@router.post('/login', response_class=JSONResponse)
async def login(credentials: LoginData, database: Session = Depends(Database)):
    user = database.query(Admin).filter(Admin.email == credentials.email).first()
    if not user:
        raise InvalidCredentials

    user = authenticate_user(user, credentials.password)
    if not user:
        raise InvalidCredentials

    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Logado com sucesso!'})
    response.set_cookie(key='session_token', value=access_token)
    return response


@router.post('/logout', response_class=JSONResponse)
async def logout(request: Request):
    if not request.state.authenticated:
        raise InvalidCredentials

    response = JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Deslogado com sucesso!'})
    response.delete_cookie(key='session_token')
    return response


@router.post('/forgot_password', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def forgot_password(
    request: Request,
    credentials: ForgotPasswordData,
    database: Session = Depends(Database),
    email: FastMail = Depends(Email)
):
    user = database.query(Admin).filter(Admin.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    token = create_access_token(
        data={'email': user.email},
        expires_delta=timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
    )

    email_context = {}
    email_context['user'] = user
    email_context['link'] = request.url_for('reset_password_page', token=token)

    email_body = MessageSchema(
        subject='SQHG - Recuperação de senha',
        recipients=[user.email],
        template_body=email_context,
        subtype=MessageType.html,
    )
    await email.send_message(email_body, template_name='email_template.html')

    return {'detail': 'Email enviado com sucesso! Verifique sua caixa de entrada.'}
