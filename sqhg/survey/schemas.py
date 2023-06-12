"""Survey's Pydantic schemas for SQHG's backend."""

from typing import List
# from datetime import date

from core.schemas import BaseSchema

class SurveyModelSchema(BaseSchema):
    name: str
    description: str


class QuestionSchema(BaseSchema):
    description: str
    type: int
    survey_model_id: int


class OptionSchema(BaseSchema):
    description: str
    type: int
    question_id: int


class SurveySchema(BaseSchema):
    survey_model: int
    superiors: List[int]
