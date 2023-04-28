"""User's SQLAlchemy database models for SQHG's backend."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import BaseModel


class Token(BaseModel):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=False, index=True)
    token = Column(String(128), nullable=False, unique=True)
    status = Column(Integer, nullable=False)

    survey = relationship('Survey', back_populates='tokens')
