"""Auth's Pydantic schemas for SQHG's backend."""

from core.schemas import BaseSchema


class LoginData(BaseSchema):
    email: str
    password: str


class ForgotPasswordData(BaseSchema):
    email: str


class PasswordResetData(BaseSchema):
    password: str
