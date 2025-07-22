from datetime import datetime
from typing import List, Optional
from uuid import UUID

from models.question_model import Question
from pydantic import BaseModel, ConfigDict


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
