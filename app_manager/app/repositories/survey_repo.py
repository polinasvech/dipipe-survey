import traceback
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.syrvey_schema import Survey as DBSurvey
from app_manager.app.models.survey_model import Survey as SurveySchema, CreateSurveyRequest


class SurveyRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, survey: DBSurvey) -> SurveySchema:
        return SurveySchema(**dict(survey))

    def _map_to_schema(self, survey: SurveySchema | CreateSurveyRequest) -> DBSurvey:
        return DBSurvey(**survey.model_dump())

    def create_survey(self, survey: CreateSurveyRequest) -> SurveySchema:
        try:
            db_survey = self._map_to_schema(survey)
            self.db.add(db_survey)
            self.db.commit()
            self.db.refresh(db_survey)
            return self._map_to_model(db_survey)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def get_all_surveys(self) -> List[SurveySchema]:
        return [self._map_to_model(s) for s in self.db.query(DBSurvey).all()]

    def get_survey_by_id(self, survey_id: UUID) -> SurveySchema:
        survey = self.db.query(DBSurvey).filter(DBSurvey.uuid == survey_id).first()
        if not survey:
            raise KeyError(f"Survey with id {survey_id} not found.")
        return self._map_to_model(survey)

    def update_survey(self, survey: SurveySchema) -> SurveySchema:
        try:
            db_survey = self.db.query(DBSurvey).filter(DBSurvey.uuid == survey.uuid).first()
            for field, value in survey.model_dump().items():
                setattr(db_survey, field, value)
            self.db.commit()
            return self._map_to_model(db_survey)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def delete_survey(self, survey_id: UUID) -> None:
        try:
            self.db.query(DBSurvey).filter(DBSurvey.uuid == survey_id).delete()
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise
