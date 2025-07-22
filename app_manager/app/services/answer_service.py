from uuid import UUID, uuid4
from typing import List, Optional

from fastapi import Depends

from app_manager.app.schemas.answer_schema import Answer
from app_manager.app.repositories.answer_repo import AnswerRepo


class AnswerService:
    def __init__(self, answer_repo: AnswerRepo = Depends(AnswerRepo)) -> None:
        self.answer_repo = answer_repo

    def create_answer(self, client_id: UUID, survey_id: UUID,question_id: UUID, answer_int: Optional[int], answer_text: Optional[str]) -> Answer:
        answer = Answer(uuid = uuid4(),client_id=client_id, survey_id=survey_id, question_id =question_id, answer_int=answer_int, answer_text=answer_text)
        return self.answer_repo.create_answer(answer)

    def get_answers_by_survey(self, survey_id: UUID) -> List[Answer]:
        return self.answer_repo.get_answers_by_survey(survey_id)

    def get_answers_by_client(self, client_id: UUID) -> List[Answer]:
        return self.answer_repo.get_answers_by_client(client_id)

    def delete_answer(self, client_id: UUID, survey_id: UUID) -> None:
        return self.answer_repo.delete_answer(client_id, survey_id)

    def update_answer(self, client_id: UUID, survey_id: UUID, answer_int: Optional[int], answer_text: Optional[str]) -> Answer:
        answer = Answer(client_id=client_id, survey_id=survey_id, answer_int=answer_int, answer_text=answer_text)
        return self.answer_repo.update_answer(answer)