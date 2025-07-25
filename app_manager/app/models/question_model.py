from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class QuestionType(str, Enum):
    NUMERIC = "NUMERIC"
    STRING = "STRING"


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    survey_id: UUID
    category_id: UUID
    text: str
    type: QuestionType
    required: bool


class CreateQuestionRequest(BaseModel):
    survey_id: UUID
    category_id: UUID
    text: str
    type: QuestionType
    required: bool
