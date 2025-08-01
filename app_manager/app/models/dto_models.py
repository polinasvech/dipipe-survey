from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from models.question_model import Question
from pydantic import BaseModel, ConfigDict


class SurveyDTO(BaseModel):
    id: UUID
    title: str
    questions: List[Question]


class QuestionType(str, Enum):
    NUMERIC = "NUMERIC"
    STRING = "STRING"


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
