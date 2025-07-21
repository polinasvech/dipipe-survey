from uuid import UUID
from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Survey(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    name: str
    start_date: datetime
    end_date: datetime
    manager_id: UUID | None = None

class CreateSurveyRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    manager_id: UUID | None = None


class GetSurveyRequest(BaseModel):
    id: UUID
    title: str
    questions: List[dict]
