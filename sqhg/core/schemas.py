"""Base Pydantic schemas for SQHG's backend."""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        smart_union = True
        orm_mode = True


class RequestSchema(BaseSchema):
    pass


class ResponseSchema(BaseSchema):
    pass
