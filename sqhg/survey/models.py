"""Survey's SQLAlchemy database models for SQHG's backend."""

import enum

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from core.database import BaseModel


class SurveyStatus(enum.Enum):
    scheduled = 1
    active = 2
    done = 3


class QuestionType(enum.Enum):
    likert = 1
    alternatives = 2
    multiple = 3
    open_ended = 4


class Survey(BaseModel):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Enum(SurveyStatus), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey('admin.id'), nullable=False, index=True)
    superior_id = Column(Integer, ForeignKey('superior.id'), nullable=False, index=True)
    survey_model_id = Column(Integer, ForeignKey('survey_model.id'), nullable=False, index=True)

    superior = relationship('Superior', back_populates='surveys')
    survey_model = relationship('SurveyModel', back_populates='surveys')
    questions = relationship('Question', back_populates='survey')
    tokens = relationship('Token', back_populates='survey')


class Question(BaseModel):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=False, index=True)

    survey = relationship('Survey', back_populates='questions')
    options = relationship('Option', back_populates='question')
    answers = relationship('Answer', back_populates='question')


class Option(BaseModel):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False, index=True)

    question = relationship('Question', back_populates='options')


class SurveyModel(BaseModel):
    __tablename__ = 'survey_model'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    is_archived = Column(Boolean, nullable=False, default=False)

    surveys = relationship('Survey', back_populates='survey_model')
    questions_model = relationship('QuestionModel', back_populates='survey_model')


class QuestionModel(BaseModel):
    __tablename__ = 'question_model'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    survey_model_id = Column(Integer, ForeignKey('survey_model.id'), nullable=False, index=True)

    survey_model = relationship('SurveyModel', back_populates='questions_model')
    options_model = relationship('OptionModel', back_populates='question_model')


class OptionModel(BaseModel):
    __tablename__ = 'option_model'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    question_model_id = Column(Integer, ForeignKey('question_model.id'), nullable=False, index=True)

    question_model = relationship('QuestionModel', back_populates='options_model')


class Answer(BaseModel):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String(255), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False, index=True)

    question = relationship('Question', back_populates='answers')
