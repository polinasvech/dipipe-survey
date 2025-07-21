import traceback
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.answer_schema import Answer as DBAnswer
from app_manager.app.models.answer_model import Answer as AnswerSchema, CreateAnswerRequest


class AnswerRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, answer: DBAnswer) -> AnswerSchema:
        return AnswerSchema(**dict(answer))

    def _map_to_schema(self, answer: AnswerSchema | CreateAnswerRequest) -> DBAnswer:
        return DBAnswer(**answer.model_dump())

    def create_answer(self, answer: CreateAnswerRequest) -> AnswerSchema:
        try:
            db_answer = self._map_to_schema(answer)
            self.db.add(db_answer)
            self.db.commit()
            self.db.refresh(db_answer)
            return self._map_to_model(db_answer)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def get_answers_by_survey(self, survey_id: UUID) -> List[AnswerSchema]:
        return [self._map_to_model(a) for a in self.db.query(DBAnswer).filter(DBAnswer.survey_id == survey_id).all()]

    def get_answers_by_client(self, client_id: UUID) -> List[AnswerSchema]:
        return [self._map_to_model(a) for a in self.db.query(DBAnswer).filter(DBAnswer.client_id == client_id).all()]

    def delete_answer(self, client_id: UUID, survey_id: UUID) -> None:
        try:
            self.db.query(DBAnswer).filter(
                DBAnswer.client_id == client_id,
                DBAnswer.survey_id == survey_id
            ).delete()
            self.db.commit()
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise

    def update_answer(self, answer: AnswerSchema) -> AnswerSchema:
        try:
            db_answer = self.db.query(DBAnswer).filter(DBAnswer.uuid == answer.uuid).first()
            for field, value in answer.model_dump().items():
                setattr(db_answer, field, value)
            self.db.commit()
            return self._map_to_model(db_answer)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise