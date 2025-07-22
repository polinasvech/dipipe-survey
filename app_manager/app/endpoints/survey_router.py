import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
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


@survey_router.get("/{survey_id}", response_model=GetSurveyRequest)
def get_survey_by_id(
    survey_id: UUID,
    survey_service: SurveyService = Depends(SurveyService),
    question_service: QuestionService = Depends(QuestionService),
):
    try:
        logger.info(f"Fetching survey with ID: {survey_id}")

        # 1. Получаем опрос
        survey = survey_service.get_survey_by_id(survey_id)
        if not survey:
            logger.error(f"Survey not found for ID: {survey_id}")
            raise HTTPException(status_code=404, detail="Survey not found")

        logger.info(f"Found survey: {survey.name}")

        # 2. Получаем вопросы
        questions = question_service.get_questions_by_survey_id(survey_id)
        logger.info(f"Found {len(questions)} questions for survey")

        # 3. Формируем ответ
        response = GetSurveyRequest(id=survey_id, title=survey.name, questions=questions)

        return response

    except HTTPException:
        raise  # Пробрасываем уже обработанные 404 ошибки
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(500, detail="Internal Server Error")


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
