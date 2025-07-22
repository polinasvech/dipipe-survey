import logging
from uuid import UUID
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from uuid import uuid4
from sqlalchemy.orm import Session
from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.category_schema import Category
from app_manager.app.models.answer_model import Answer,CreateAnswerRequest
from app_manager.app.models.question_model import Question
from app_manager.app.models.dto_models import SurveyDTO
from app_manager.app.schemas.syrvey_schema import Survey
from app_manager.app.models.survey_model import Survey as SurveyModel
from app_manager.app.services.answer_service import AnswerService
from app_manager.app.services.question_service import QuestionService
from app_manager.app.services.survey_service import SurveyService
from app_manager.app.schemas.answer_schema import Answer
from app_manager.app.schemas.question_schema import Question
from app_manager.app.models.dto_models import StatDTO,QuestionBase,AnswerWithQuestion,AnswerBase
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID, uuid4

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)

from sqlalchemy.orm import joinedload
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException




def get_stat_dto_by_survey_id(survey_id: UUID, db: Session) -> StatDTO:
    # Load answers with their questions
    answers_db = db.scalars(
        select(Answer)
        .options(joinedload(Answer.question))
        .where(Answer.survey_id == survey_id)
    ).unique().all()

    if not answers_db:
        raise HTTPException(
            status_code=404,
            detail=f"No answers found for survey with id {survey_id}"
        )

    # Convert SQLAlchemy objects to Pydantic models
    answers = []
    for db_answer in answers_db:
        # Create AnswerWithQuestion instance
        answer = AnswerWithQuestion(
            uuid=db_answer.uuid,
            client_id=db_answer.client_id,
            survey_id=db_answer.survey_id,
            question_id=db_answer.question_id,
            answer_int=db_answer.answer_int,
            answer_text=db_answer.answer_text,
            question=QuestionBase.model_validate(db_answer.question) if db_answer.question else None
        )
        answers.append(answer)

    return StatDTO(
        id=uuid4(),
        survey_id=survey_id,
        count=len(answers),
        answers=answers
    )


@admin_router.get("/get_stat/{survey_id}", response_model=StatDTO)
def get_stat_by_survey(survey_id: UUID, db: Session = Depends(get_db)):
    stat = get_stat_dto_by_survey_id(survey_id, db)
    if stat.count == 0:
        raise HTTPException(status_code=404, detail="Ответы не найдены")
    return stat

@admin_router.get("/get_all_surveys",response_model=List[SurveyModel])
def get_all_surveys(
    survey_service: SurveyService = Depends(SurveyService),
):
    return survey_service.get_all_surveys()

@admin_router.get("/{survey_id}", response_model=SurveyDTO)
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
        response = SurveyDTO(
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





