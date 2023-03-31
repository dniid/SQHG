"""Auth's Pydantic schemas for SQHG's backend."""

from core.schemas import BaseSchema


class JWToken(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    email: str | None = None
