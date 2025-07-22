from uuid import UUID, uuid4
from typing import List

from fastapi import Depends

from app_manager.app.models.question_model import Types
from app_manager.app.schemas.question_schema import Question
from app_manager.app.repositories.question_repo import QuestionRepo


class QuestionService:
    def __init__(self, question_repo: QuestionRepo = Depends(QuestionRepo)) -> None:
        self.question_repo = question_repo

    def get_all_questions(self) -> List[Question]:
        return self.question_repo.get_all_questions()

    def get_question_by_id(self, question_id: UUID) -> Question:
        return self.question_repo.get_question_by_id(question_id)

    def get_questions_by_survey_id(self, survey_id: UUID) -> List[Question]:
        return self.question_repo.get_questions_by_survey_id(survey_id)

    def create_question(self, survey_id: UUID,category_id:UUID, text: str,type:Types, required:bool) -> Question:
        question = Question(uuid=uuid4(),
                            survey_id=survey_id,
                            category_id=category_id,
                            text=text,
                            type = type,
                            required = required)
        return self.question_repo.create_question(question)

    def update_question(self, uuid: UUID, survey_id: UUID, category_id:UUID, text: str,type:Types, required:bool) -> Question:
        question = Question(uuid=uuid, survey_id=survey_id,
                            category_id=category_id,
                            text=text,
                            type = type,
                            required = required)
        return self.question_repo.update_question(question)

    def delete_question(self, uuid: UUID) -> None:
        return self.question_repo.delete_question(uuid)
