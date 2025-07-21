import traceback
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.question_schema import Question as DBQuestion
from app_manager.app.models.question_model import Question as QuestionSchema, CreateQuestionRequest


class QuestionRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, question: DBQuestion) -> QuestionSchema:
        return QuestionSchema(**dict(question))

    def _map_to_schema(self, question: QuestionSchema | CreateQuestionRequest) -> DBQuestion:
        return DBQuestion(**question.model_dump())

    def create_question(self, question: CreateQuestionRequest) -> QuestionSchema:
        try:
            db_question = self._map_to_schema(question)
            self.db.add(db_question)
            self.db.commit()
            self.db.refresh(db_question)
            return self._map_to_model(db_question)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def get_all_questions(self) -> List[QuestionSchema]:
        return [self._map_to_model(q) for q in self.db.query(DBQuestion).all()]

    def get_question_by_id(self, question_id: UUID) -> QuestionSchema:
        question = self.db.query(DBQuestion).filter(DBQuestion.uuid == question_id).first()
        if not question:
            raise KeyError(f"Question with id {question_id} not found.")
        return self._map_to_model(question)

    def get_questions_by_survey_id(self, survey_id: UUID) -> List[QuestionSchema]:
        return [self._map_to_model(s) for s in self.db.query(DBQuestion).filter(DBQuestion.survey_id == survey_id).all()]


    def update_question(self, question: QuestionSchema) -> QuestionSchema:
        try:
            db_question = self.db.query(DBQuestion).filter(DBQuestion.uuid == question.uuid).first()
            for field, value in question.model_dump().items():
                setattr(db_question, field, value)
            self.db.commit()
            return self._map_to_model(db_question)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def delete_question(self, question_id: UUID) -> None:
        try:
            self.db.query(DBQuestion).filter(DBQuestion.uuid == question_id).delete()
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise
