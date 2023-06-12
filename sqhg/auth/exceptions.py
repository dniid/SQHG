"""Auth's custom exceptions."""

from fastapi import status

from core.exceptions import BaseDetailException


class CredentialsException(BaseDetailException):
    STATUS_CODE = status.HTTP_503_SERVICE_UNAVAILABLE
    DETAIL = 'Não foi possível validar as credenciais'


class InvalidCredentials(BaseDetailException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Email ou senha inválidos'


class InvalidToken(BaseDetailException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = 'Token inválido'


class ExpiredToken(BaseDetailException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Token já utilizado'
