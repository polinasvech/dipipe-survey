from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Manager(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    full_name: str


class CreateManagerRequest(BaseModel):
    full_name: str
