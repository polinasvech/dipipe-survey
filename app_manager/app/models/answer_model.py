from uuid import UUID
from pydantic import BaseModel, ConfigDict

class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    client_id: UUID
    survey_id: UUID
    answer_int: int | None = None
    answer_text: str | None = None

class CreateAnswerRequest(BaseModel):
    client_id: UUID
    survey_id: UUID
    answer_int: int | None = None
    answer_text: str | None = None
