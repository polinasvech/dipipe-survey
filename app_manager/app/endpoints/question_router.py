from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models.question_model import CreateQuestionRequest, Question
from services.question_service import QuestionService

question_router = APIRouter(prefix="/questions", tags=["Questions"])


@question_router.get("/")
def get_all_questions(
    question_service: QuestionService = Depends(QuestionService),
) -> list[Question]:
    return question_service.get_all_questions()


@question_router.get("/{question_id}")
def get_question_by_id(
    question_id: UUID,
    question_service: QuestionService = Depends(QuestionService),
) -> Question:
    try:
        return question_service.get_question_by_id(question_id)
    except KeyError:
        raise HTTPException(404, detail=f"Question with id={question_id} not found")


@question_router.get("/get_question_by_survey/{survey_id}")
def get_question_by_survey_id(
    survey_id: UUID,
    question_service: QuestionService = Depends(QuestionService),
) -> list[Question]:
    try:
        return question_service.get_questions_by_survey_id(survey_id)
    except KeyError:
        raise HTTPException(404, detail=f"Question with survey_id={survey_id} not found")


@question_router.post("/")
def create_question(
    request: CreateQuestionRequest,
    question_service: QuestionService = Depends(QuestionService),
) -> Question:
    try:
        return question_service.create_question(request.survey_id,
                                                request.category_id,
                                                request.text,
                                                request.type,
                                                request.required
                                                )
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@question_router.put("/{question_id}")
def update_question(
    question_id: UUID,
    survey_id: UUID,
    text: str,
    question_service: QuestionService = Depends(QuestionService),
) -> Question:
    try:
        return question_service.update_question(question_id, survey_id, text)
    except KeyError:
        raise HTTPException(404, detail=f"Question with id={question_id} not found")


@question_router.delete("/{question_id}")
def delete_question(
    question_id: UUID,
    question_service: QuestionService = Depends(QuestionService),
) -> dict:
    try:
        question_service.delete_question(question_id)
        return {"detail": "Question deleted successfully"}
    except KeyError:
        raise HTTPException(404, detail=f"Question with id={question_id} not found")
