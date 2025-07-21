from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app_manager.app.schemas.syrvey_schema import Survey
from app_manager.app.models.survey_model import Survey as SurveyModel,GetSurveyRequest
from app_manager.app.services.survey_service import SurveyService
from app_manager.app.services.question_service import QuestionService

survey_router = APIRouter(prefix="/surveys", tags=["Surveys"])


@survey_router.get("/")
def get_all_surveys(
    survey_service: SurveyService = Depends(SurveyService),
) -> list[Survey]:
    return survey_service.get_all_surveys()


@survey_router.get("/{survey_id}")
def get_survey_by_id(
    survey_id: UUID,
    survey_service: SurveyService = Depends(SurveyService),
    question_service: QuestionService = Depends(QuestionService)
) -> GetSurveyRequest:
    try:
        survey = survey_service.get_survey_by_id(survey_id)
        questions = question_service.get_question_by_id(survey_id)
        return GetSurveyRequest(id = survey_id, name = survey.name, questions = questions)
    except KeyError:
        raise HTTPException(404, detail=f"Survey with id={survey_id} not found")


@survey_router.post("/create_survey")
def create_survey(
    name: str,
    start_date: datetime,
    end_date: datetime,
    manager_id: UUID,
    survey_service: SurveyService = Depends(SurveyService),
) -> Survey:
    try:
        return survey_service.create_survey(name, start_date, end_date, manager_id)
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

