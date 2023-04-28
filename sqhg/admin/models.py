"""Admin's SQLAlchemy database models for SQHG's backend."""

from sqlalchemy import Column, Integer, String, Date

from core.database import BaseModel


class Admin(BaseModel):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(12), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(13), nullable=False)
    password = Column(String(128), nullable=False)
