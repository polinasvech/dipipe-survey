from schemas.base_schema import Base
from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from schemas.base_schema import Base


class Answer(Base):
    __tablename__ = "answers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.uuid", ondelete="CASCADE"), nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.uuid", ondelete="CASCADE"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.uuid", ondelete="CASCADE"), nullable=False)
    answer_int = Column(Integer)
    answer_text = Column(Text)

    question = relationship(
        "Question",
        primaryjoin="Answer.question_id == Question.uuid",
        back_populates="answers"
    )
