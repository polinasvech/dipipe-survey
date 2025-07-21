from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app_manager.app.models.question_model import Question


class Survey(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    name: str
    start_date: datetime
    end_date: datetime
    manager_id: Optional[UUID] = None

class CreateSurveyRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    manager_id: Optional[UUID] = None


class GetSurveyRequest(BaseModel):
    id: UUID
    title: str
    questions: List[Question]
