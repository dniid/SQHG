"""SAP's Pydantic schemas for SQHG's backend."""

from typing import Optional
from datetime import date

from core.schemas import BaseSchema


class AreaBase(BaseSchema):
    name: str
    activatino_date: date
    deactivation_date: Optional[date] = None
    status: int


class AreaSchema(AreaBase):
    id: int


class AreaCreate(AreaBase):
    pass


class AreaUpdate(BaseSchema):
    name: Optional[str]
    register_date: Optional[date]
    deactivation_date: Optional[date]
    status: Optional[int]


class SuperiorBase(BaseSchema):
    name: str
    position: str
    area_id: int


class SuperiorSchema(SuperiorBase):
    id: int


class SuperiorCreate(SuperiorBase):
    pass
