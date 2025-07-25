from schemas.base_schema import Base
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Answer(Base):
    __tablename__ = "answers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.uuid", ondelete="CASCADE"), nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.uuid", ondelete="CASCADE"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.uuid", ondelete="CASCADE"), nullable=False)
    answer_int = Column(Integer)
    answer_text = Column(Text)

    # Add relationship to Question
    question = relationship("Question", back_populates="answers")
