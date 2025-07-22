import logging
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from uuid import uuid4
from sqlalchemy.orm import Session
from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.category_schema import Category
from app_manager.app.models.answer_model import Answer,CreateAnswerRequest
from app_manager.app.models.question_model import Question
from app_manager.app.models.survey_model import GetSurveyRequest
from app_manager.app.services.answer_service import AnswerService
from app_manager.app.services.question_service import QuestionService
from app_manager.app.services.survey_service import SurveyService

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)



@admin_router.get("/{survey_id}", response_model=GetSurveyRequest)
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
        response = GetSurveyRequest(
            id=survey_id,
            title=survey.name,
            questions=questions
        )

        return response

    except HTTPException:
        raise  # Пробрасываем уже обработанные 404 ошибки
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(500, detail="Internal Server Error")

@admin_router.get("/get_stat/{survey_id}")
def get_statistics_by_survey_id(
    survey_id: UUID,
    question_service: QuestionService = Depends(QuestionService),
) -> list[Question]:
    try:
        return question_service.get_questions_by_survey_id(survey_id)
    except KeyError:
        raise HTTPException(404, detail=f"Question with survey_id={survey_id} not found")

@admin_router.post("/categories/import")
async def import_categories(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Файл должен быть Excel (.xlsx или .xls)")

    try:
        contents = await file.read()
        df = pd.read_excel(contents)

        if 'text' not in df.columns:
            raise HTTPException(status_code=400, detail="Ожидается колонка 'text' в файле")

        categories = []
        for _, row in df.iterrows():
            text = str(row['text']).strip()
            if text:
                category = Category(uuid=uuid4(), text=text)
                categories.append(category)

        db.bulk_save_objects(categories)
        db.commit()

        return {"message": f"✅ Загружено {len(categories)} категорий"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка импорта: {str(e)}")