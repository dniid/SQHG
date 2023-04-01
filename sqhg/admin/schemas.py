"""Admin's Pydantic schemas for SQHG's backend."""

from datetime import date

from core.schemas import BaseSchema


class AdminSchema(BaseSchema):
    tag: str
    name: str
    birth_date: date
    email: str
    phone: str
