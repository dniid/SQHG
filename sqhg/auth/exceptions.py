"""Auth's custom exceptions."""

from fastapi import status

from core.exceptions import BaseDetailException


class CredentialsException(BaseDetailException):
    STATUS_CODE = status.HTTP_503_SERVICE_UNAVAILABLE
    DETAIL = 'Não foi possível validar as credenciais'

    def __init__(self) -> None:
        super().__init__(headers={'WWW-Authenticate': 'Bearer'})


class InvalidCredentials(BaseDetailException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Email ou senha inválidos'

    def __init__(self) -> None:
        super().__init__(headers={'WWW-Authenticate': 'Bearer'})
