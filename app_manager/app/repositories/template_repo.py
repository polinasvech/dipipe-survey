import traceback
from typing import List
from uuid import UUID

from models.template_model import Template as Template
from schemas.base_schema import get_db
from schemas.template_schema import Template as DBTemplate
from sqlalchemy.orm import Session


class TemplateRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, template: DBTemplate) -> Template:
        result = Template.from_orm(template)
        return result

    def _map_to_schema(self, template: Template) -> DBTemplate:
        return DBTemplate(
            uuid=template.uuid, initial_survey_id=template.initial_survey_id, template_text=template.template_text
        )

    def create_template(self, template: Template) -> Template:
        try:
            db_template = self._map_to_schema(template)
            self.db.add(db_template)
            self.db.commit()
            self.db.refresh(db_template)
            return self._map_to_model(db_template)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def get_all_templates(self) -> List[Template]:
        return [self._map_to_model(t) for t in self.db.query(DBTemplate).all()]

    def get_template_by_id(self, template_id: UUID) -> Template:
        template = self.db.query(DBTemplate).filter(DBTemplate.uuid == template_id).first()
        if not template:
            raise KeyError(f"Template with id {template_id} not found.")
        return self._map_to_model(template)

    def delete_template(self, template_id: UUID) -> None:
        try:
            self.db.query(DBTemplate).filter(DBTemplate.uuid == template_id).delete()
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def update_template(self, template: Template) -> Template:
        try:
            db_template = self.db.query(DBTemplate).filter(DBTemplate.uuid == template.uuid).first()
            for field, value in template.model_dump().items():
                setattr(db_template, field, value)
            self.db.commit()
            return self._map_to_model(db_template)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise
