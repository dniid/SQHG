"""Admin's custom exceptions."""

from typing import Any

from fastapi import HTTPException, status


class BaseDetailException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = 'Server error'

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class AdminException(BaseDetailException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Could not find Admin'

    def __init__(self) -> None:
        super().__init__(headers={'WWW-Authenticate': 'Bearer'})
