from uuid import UUID

from pydantic import BaseModel, ConfigDict
from enum import StrEnum


class QuestionType(StrEnum):
    NUMERIC = "numeric"
    STRING = "string"


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    survey_id: UUID
    text: str


class CreateQuestionRequest(BaseModel):
    survey_id: UUID
    text: str
