"""SAP's Pydantic schemas for SQHG's backend."""

from typing import Optional
from datetime import date

from core.schemas import BaseSchema


class AreaBase(BaseSchema):
    nome: str
    data_cadastro: date
    data_inativacao: Optional[date] = None
    status: int
    tipo: int


class AreaSchema(AreaBase):
    id: int


class AreaCreate(AreaBase):
    pass


class AreaUpdate(BaseSchema):
    nome: Optional[str]
    data_cadastro: Optional[date]
    data_inativacao: Optional[date]
    status: Optional[int]
    tipo: Optional[int]


class SuperiorBase(BaseSchema):
    nome: str
    cargo: str
    area_id: int


class SuperiorCreate(SuperiorBase):
    pass


class Superior(SuperiorBase):
    id: int
