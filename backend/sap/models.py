"""SAP's SQLAlchemy database models for SQHG's backend."""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.database import BaseModel


class Superior(BaseModel):
    __tablename__ = 'superior'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cargo = Column(String(45), nullable=False)
    area_id = Column(Integer, ForeignKey('area.id'), nullable=False, index=True)

    area = relationship('Area', back_populates='superiors')


class Area(BaseModel):
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    data_cadastro = Column(Date, nullable=False)
    data_inativacao = Column(Date, nullable=True)
    status = Column(Integer, nullable=False)
    tipo = Column(Integer, nullable=False)

    superiors = relationship('Superior', back_populates='area')
