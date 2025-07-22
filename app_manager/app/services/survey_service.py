from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import Depends
from repositories.survey_repo import SurveyRepo
from schemas.syrvey_schema import Survey


class SurveyService:
    def __init__(self, survey_repo: SurveyRepo = Depends(SurveyRepo)) -> None:
        self.survey_repo = survey_repo

    def get_all_surveys(self) -> List[Survey]:
        return self.survey_repo.get_all_surveys()

    def get_survey_by_id(self, survey_id: UUID) -> Survey:
        return self.survey_repo.get_survey_by_id(survey_id)

    def create_survey(self, name: str, start_date: datetime, end_date: datetime, manager_id: UUID) -> Survey:
        survey = Survey(uuid=uuid4(), name=name, start_date=start_date, end_date=end_date, manager_id=manager_id)
        return self.survey_repo.create_survey(survey)

    def update_survey(self, uuid: UUID, name: str, start_date: datetime, end_date: datetime, manager_id: UUID) -> Survey:
        survey = Survey(uuid=uuid, name=name, start_date=start_date, end_date=end_date, manager_id=manager_id)
        return self.survey_repo.update_survey(survey)

    def delete_survey(self, uuid: UUID) -> None:
        return self.survey_repo.delete_survey(uuid)
