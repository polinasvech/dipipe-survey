from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Template(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    initial_survey_id: UUID
    template_text: str


class CreateTemplateRequest(BaseModel):
    initial_survey_id: UUID
    template_text: str
