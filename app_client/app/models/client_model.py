from uuid import UUID
from pydantic import BaseModel, ConfigDict

class Client(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    tin: str
    preferences: str | None = None
    division: str | None = None
    ca_type: str | None = None

class CreateClientRequest(BaseModel):
    tin: str
    preferences: str | None = None
    division: str | None = None
    ca_type: str | None = None
