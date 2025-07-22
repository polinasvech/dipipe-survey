import traceback
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app_manager.app.schemas.base_schema import get_db
from app_manager.app.schemas.answer_schema import Answer as DBAnswer
from app_manager.app.models.answer_model import Answer as Answer, CreateAnswerRequest


class AnswerRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, answer: DBAnswer) -> Answer:
        result = Answer.from_orm(answer)
        return result

    def _map_to_schema(self, answer: Answer) -> DBAnswer:
        return DBAnswer(
            uuid = answer.uuid,
            client_id=answer.client_id,
            survey_id=answer.survey_id,
            question_id=answer.question_id,
            answer_int=answer.answer_int,
            answer_text=answer.answer_text
        )

    def create_answer(self, answer: Answer) -> Answer:
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

    def get_answers_by_survey(self, survey_id: UUID) -> List[Answer]:
        return [self._map_to_model(a) for a in self.db.query(DBAnswer).filter(DBAnswer.survey_id == survey_id).all()]

    def get_answers_by_client(self, client_id: UUID) -> List[Answer]:
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

    def update_answer(self, answer: Answer) -> Answer:
        try:
            db_answer = self.db.query(DBAnswer).filter(DBAnswer.uuid == answer.uuid).first()
            db_answer.client_id = answer.client_id,
            db_answer.survey_id = answer.survey_id,
            db_answer.question_id = answer.question_id,
            db_answer.answer_int = answer.answer_int,
            db_answer.answer_text = answer.answer_text
            self.db.commit()
            return self._map_to_model(db_answer)
        except Exception:
            traceback.print_exc()
            self.db.rollback()
            raise