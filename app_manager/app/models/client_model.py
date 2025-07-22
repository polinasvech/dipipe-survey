from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Client(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    tin: str
    preferences: Optional[str] = None
    division: Optional[str] = None
    ca_type: Optional[str] = None


class CreateClientRequest(BaseModel):
    tin: str
    preferences: Optional[str] = None
    division: Optional[str] = None
    ca_type: Optional[str] = None
