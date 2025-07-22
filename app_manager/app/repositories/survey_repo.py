import traceback
from typing import List
from uuid import UUID

from models.survey_model import CreateSurveyRequest
from models.survey_model import Survey as Survey
from schemas.base_schema import get_db
from schemas.syrvey_schema import Survey as DBSurvey
from sqlalchemy.orm import Session


class SurveyRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, survey: DBSurvey) -> Survey:
        return Survey.from_orm(survey)

    def _map_to_schema(self, survey: Survey) -> DBSurvey:
        return DBSurvey(
            uuid=survey.uuid,
            name=survey.name,
            start_date=survey.start_date,
            end_date=survey.end_date,
            manager_id=survey.manager_id,
        )

    def create_survey(self, survey: Survey) -> Survey:
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

    def get_all_surveys(self) -> List[Survey]:
        return [self._map_to_model(s) for s in self.db.query(DBSurvey).all()]

    def get_survey_by_id(self, survey_id: UUID) -> Survey:
        survey = self.db.query(DBSurvey).filter(DBSurvey.uuid == survey_id).first()
        if not survey:
            raise KeyError(f"Survey with id {survey_id} not found.")
        return self._map_to_model(survey)

    def update_survey(self, survey: Survey) -> Survey:
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
