from uuid import UUID, uuid4
from typing import List, Optional

from fastapi import Depends

from app_manager.app.schemas.template_schema import Template
from app_manager.app.repositories.template_repo import TemplateRepo


class TemplateService:
    def __init__(self, template_repo: TemplateRepo = Depends(TemplateRepo)) -> None:
        self.template_repo = template_repo

    def get_all_templates(self) -> List[Template]:
        return self.template_repo.get_all_templates()

    def get_template_by_id(self, template_id: UUID) -> Template:
        return self.template_repo.get_template_by_id(template_id)

    def create_template(self, initial_survey_id: UUID, template_text: Optional[str]) -> Template:
        template = Template(uuid=uuid4(), initial_survey_id=initial_survey_id, template_text=template_text)
        return self.template_repo.create_template(template)

    def update_manager(self, initial_survey_id: UUID, template_text: Optional[str]) -> Template:
        template = Template(uuid=uuid4(), initial_survey_id=initial_survey_id, template_text=template_text)
        return self.template_repo.update_template(template)

    def delete_template(self, template_id: UUID) -> None:
        return self.template_repo.delete_template(template_id)
