import traceback
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.template_schema import Template as DBTemplate
from app_manager.app.models.template_model import Template as TemplateSchema, CreateTemplateRequest


class TemplateRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, template: DBTemplate) -> TemplateSchema:
        return TemplateSchema(**dict(template))

    def _map_to_schema(self, template: TemplateSchema | CreateTemplateRequest) -> DBTemplate:
        return DBTemplate(**template.model_dump())

    def create_template(self, template: CreateTemplateRequest) -> TemplateSchema:
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

    def get_all_templates(self) -> List[TemplateSchema]:
        return [self._map_to_model(t) for t in self.db.query(DBTemplate).all()]

    def get_template_by_id(self, template_id: UUID) -> TemplateSchema:
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
