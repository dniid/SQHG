"""Admin's Pydantic schemas for SQHG's backend."""

from typing import Optional
from datetime import date

from core.schemas import BaseSchema


class AdminSchema(BaseSchema):
    tag: str
    name: str
    birth_date: date
    email: str
    phone: str
    password: str


class AdminUpdate(BaseSchema):
    name: Optional[str]
    phone: Optional[str]
    password: Optional[str]
