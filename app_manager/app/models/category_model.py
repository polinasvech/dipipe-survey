from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    text: str


class CreateCategoryRequest(BaseModel):
    text: str
