"""Survey's Pydantic schemas for SQHG's backend."""

from typing import Optional, Dict, List, Union
# from datetime import date

from core.schemas import BaseSchema

class SurveyModelSchema(BaseSchema):
    name: str
    description: str
    questions: Optional[List[Dict[str,Union[str, int, List[Dict[str, str]]]]]]
