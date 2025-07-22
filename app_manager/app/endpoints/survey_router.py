import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException


from models.question_model import Question
from models.survey_model import Survey as Survey,CreateSurveyRequest
from services.survey_service import SurveyService
from services.question_service import QuestionService
from models.question_model import Question
from models.survey_model import CreateSurveyRequest, GetSurveyRequest
from models.survey_model import Survey as Survey
from services.question_service import QuestionService
from services.survey_service import SurveyService

survey_router = APIRouter(prefix="/surveys", tags=["Surveys"])
logger = logging.getLogger(__name__)


@survey_router.get("/")
def get_all_surveys(
    survey_service: SurveyService = Depends(SurveyService),
) -> list[Survey]:
    return survey_service.get_all_surveys()


@survey_router.get("/{survey_id}", response_model=Survey)
def get_survey_by_id(
        survey_id: UUID,
        survey_service: SurveyService = Depends(SurveyService),
):
    try:
        return survey_service.get_survey_by_id(survey_id)
    except Exception as e:
        raise HTTPException(404, detail=str(e))


@survey_router.post("/create_survey")
def create_survey(
    request: CreateSurveyRequest,
    survey_service: SurveyService = Depends(SurveyService),
) -> Survey:
    try:
        return survey_service.create_survey(request.name, request.start_date, request.end_date, request.manager_id)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@survey_router.put("/{survey_id}")
def update_survey(
    survey_id: UUID,
    name: str,
    start_date: datetime,
    end_date: datetime,
    manager_id: UUID,
    survey_service: SurveyService = Depends(SurveyService),
) -> Survey:
    try:
        return survey_service.update_survey(survey_id, name, start_date, end_date, manager_id)
    except KeyError:
        raise HTTPException(404, detail=f"Survey with id={survey_id} not found")


@survey_router.delete("/{survey_id}")
def delete_survey(
    survey_id: UUID,
    survey_service: SurveyService = Depends(SurveyService),
) -> dict:
    try:
        survey_service.delete_survey(survey_id)
        return {"detail": "Survey deleted successfully"}
    except KeyError:
        raise HTTPException(404, detail=f"Survey with id={survey_id} not found")
