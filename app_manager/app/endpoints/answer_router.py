from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models.answer_model import Answer, CreateAnswerRequest
from services.answer_service import AnswerService

answer_router = APIRouter(prefix="/answers", tags=["Answers"])


@answer_router.post("/")
def create_answer(
    request: CreateAnswerRequest,
    answer_service: AnswerService = Depends(AnswerService),
) -> Answer:
    try:
        return answer_service.create_answer(request.client_id, request.survey_id,request.question_id, request.answer_int, request.answer_text)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@answer_router.get("/survey/{survey_id}")
def get_answers_by_survey(
    survey_id: UUID,
    answer_service: AnswerService = Depends(AnswerService),
) -> list[Answer]:
    try:
        return answer_service.get_answers_by_survey(survey_id)
    except Exception as e:
        raise HTTPException(404, detail=str(e))


@answer_router.get("/client/{client_id}")
def get_answers_by_client(
    client_id: UUID,
    answer_service: AnswerService = Depends(AnswerService),
) -> list[Answer]:
    try:
        return answer_service.get_answers_by_client(client_id)
    except Exception as e:
        raise HTTPException(404, detail=str(e))


@answer_router.put("/")
def update_answer(
    client_id: UUID,
    survey_id: UUID,
    answer_int: Optional[int] = None,
    answer_text: Optional[str] = None,
    answer_service: AnswerService = Depends(AnswerService),
) -> Answer:
    try:
        return answer_service.update_answer(client_id, survey_id, answer_int, answer_text)
    except KeyError:
        raise HTTPException(404, detail=f"Answer for client_id={client_id} and survey_id={survey_id} not found")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@answer_router.delete("/")
def delete_answer(
    client_id: UUID,
    survey_id: UUID,
    answer_service: AnswerService = Depends(AnswerService),
) -> dict:
    try:
        answer_service.delete_answer(client_id, survey_id)
        return {"detail": "Answer deleted successfully"}
    except KeyError:
        raise HTTPException(404, detail=f"Answer for client_id={client_id} and survey_id={survey_id} not found")
    except Exception as e:
        raise HTTPException(400, detail=str(e))
