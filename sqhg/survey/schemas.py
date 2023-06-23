"""Survey's Pydantic schemas for SQHG's backend."""

from typing import Optional, Dict, List, Union

from core.schemas import BaseSchema

class SurveyModelSchema(BaseSchema):
    name: str
    description: str
    questions: Optional[List[Dict[str,Union[str, int, List[Dict[str, str]]]]]]


class SurveySchema(BaseSchema):
    survey_model: int
    superiors: List[int]
