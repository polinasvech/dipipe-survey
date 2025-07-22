from enum import Enum
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app_manager.app.models.question_model import Question

class SurveyDTO(BaseModel):
    id: UUID
    title: str
    questions: List[Question]

class QuestionType(str, Enum):
    NUMERIC = "Numeric"
    STRING = "String"

class QuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    survey_id: UUID
    category_id: UUID
    text: str
    type: QuestionType
    required: bool

class AnswerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    client_id: UUID
    survey_id: UUID
    question_id: UUID
    answer_int: Optional[int] = None
    answer_text: Optional[str] = None

class AnswerWithQuestion(AnswerBase):
    question: Optional[QuestionBase] = None

class StatDTO(BaseModel):
    id: UUID
    survey_id: UUID
    count: int
    answers: list[AnswerWithQuestion]