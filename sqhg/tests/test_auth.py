"""Auth's tests for SQHG's backend."""

from datetime import timedelta

import pytest
import pytest_asyncio
from fastapi import status
from sqlalchemy.orm import Session

from async_asgi_testclient import TestClient

from admin.models import Admin
from auth.utils import get_password_hash, create_access_token, verify_password
from core.email import FastMailConfig
from core.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
)


@pytest_asyncio.fixture
async def admin(database: Session) -> Admin:
    admin = Admin(
        tag='000000000000',
        name='mockadmin',
        birth_date='2001-01-01',
        email='mock@admin.com',
        phone='0000000000000',
        password=get_password_hash('mock'),
    )
    database.add(admin)
    database.commit()
    return admin


@pytest.mark.asyncio
async def test_auth_admin_login_page(client: TestClient) -> None:
    response = await client.get('/login?admin=True')

    assert response.status_code == status.HTTP_200_OK
    assert 'Admin Login' in response.content.decode('utf-8')


@pytest.mark.asyncio
async def test_auth_admin_login_page_redirect(client: TestClient, admin: Admin) -> None:
    access_token = create_access_token(
        data={'sub': admin.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    client.cookie_jar.load({'session_token': access_token})

    response = await client.get('/login?admin=True')

    assert response.status_code == status.HTTP_200_OK
    assert 'Login' not in response.content.decode('utf-8')


@pytest.mark.asyncio
async def test_auth_admin_login_succeeds(client: TestClient, admin: Admin) -> None:
    response = await client.post('/login', json={
        'email': 'mock@admin.com',
        'password': 'mock',
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == 'Logado com sucesso!'
    assert client.cookie_jar.get('session_token')


@pytest.mark.asyncio
async def test_auth_admin_login_fails(client: TestClient) -> None:
    response = await client.post('/login', json={
        'email': 'mock@admin.com',
        'password': 'wrongpass',
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Email ou senha inválidos'


@pytest.mark.asyncio
async def test_auth_admin_logout_succeeds(client: TestClient, admin: Admin) -> None:
    access_token = create_access_token(
        data={'sub': admin.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    client.cookie_jar.load({'session_token': access_token})

    response = await client.post('/logout')

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == 'Deslogado com sucesso!'


@pytest.mark.asyncio
async def test_auth_admin_logout_fails(client: TestClient) -> None:
    response = await client.post('/logout')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Email ou senha inválidos'


@pytest.mark.asyncio
async def test_auth_admin_forgot_password_page(client: TestClient) -> None:
    response = await client.get('/forgot-password')

    assert response.status_code == status.HTTP_200_OK
    assert 'Esqueci a senha' in response.content.decode('utf-8')


@pytest.mark.asyncio
async def test_auth_admin_forgot_password_valid(client: TestClient, admin: Admin) -> None:
    email = FastMailConfig()
    with email.record_messages() as outbox:
        response = await client.post('/forgot-password', json={
            'email': admin.email,
        })

        assert response.status_code == status.HTTP_200_OK
        assert len(outbox) == 1
        assert outbox[0]['Subject'] == 'SQHG - Recuperação de senha'
        assert outbox[0]['To'] == admin.email


@pytest.mark.asyncio
async def test_auth_admin_forgot_password_invalid(client: TestClient) -> None:
    response = await client.post('/forgot-password', json={
        'email': 'wrong@email.com',
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'Usuário não encontrado'


@pytest.mark.asyncio
async def test_auth_admin_reset_password_page_valid(client: TestClient, admin: Admin) -> None:
    token = create_access_token(
        data={'email': admin.email},
        expires_delta=timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
    )

    response = await client.get(f'/reset-password/{token}')

    assert response.status_code == status.HTTP_200_OK
    assert 'Redefinir Senha' in response.content.decode('utf-8')
    assert 'Confirmar senha' in response.content.decode('utf-8')


@pytest.mark.asyncio
async def test_auth_admin_reset_password_page_invalid(client: TestClient) -> None:
    response = await client.get('/reset-password/invalid-token')

    assert response.status_code == status.HTTP_200_OK
    assert 'O link que você está tentando acessar já expirou' in response.content.decode('utf-8')


@pytest.mark.asyncio
async def test_auth_admin_reset_password_valid(client: TestClient, admin: Admin) -> None:
    token = create_access_token(
        data={'email': admin.email},
        expires_delta=timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
    )

    response = await client.post(f'/reset-password/{token}', json={
        'password': 'newpass',
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == 'Senha atualizada com sucesso!'
    assert verify_password('newpass', admin.password)


@pytest.mark.asyncio
async def test_auth_admin_reset_password_invalid(client: TestClient, admin: Admin) -> None:
    response = await client.post('/reset-password/invalid-token', json={
        'password': 'newpass',
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'Usuário não encontrado'
    assert not verify_password('newpass', admin.password)
