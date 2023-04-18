"""Auth's custom exceptions."""

from typing import Any

from fastapi import HTTPException, status


class BaseDetailException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class CredentialsException(BaseDetailException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Could not validate credentials"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class InvalidCredentials(BaseDetailException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Invalid email or password"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})