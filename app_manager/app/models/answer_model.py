from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models.question_model import Question

class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    question_id: UUID
    client_id: UUID
    survey_id: UUID
    answer_int: Optional[int] = None
    answer_text: Optional[str] = None

    question: Optional[Question] = None  # Добавляем вложенный объект


class CreateAnswerRequest(BaseModel):
    client_id: UUID
    survey_id: UUID
    question_id: UUID
    answer_int: Optional[int] = None
    answer_text: Optional[str] = None


class AnswerRead(BaseModel):
    uuid: UUID
    client_id: UUID
    survey_id: UUID
    question_id: UUID
    answer_int: Optional[int]
    answer_text: Optional[str]

    class Config:
        orm_mode = True 