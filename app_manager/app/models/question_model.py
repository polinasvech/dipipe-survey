from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    survey_id: UUID
    text: str


class CreateQuestionRequest(BaseModel):
    survey_id: UUID
    text: str
