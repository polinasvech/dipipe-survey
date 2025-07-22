from schemas.base_schema import Base
from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from schemas.base_schema import Base


class Answer(Base):
    __tablename__ = "answers"

    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.uuid", ondelete="CASCADE"), nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.uuid", ondelete="CASCADE"), nullable=False)
    answer_int = Column(Integer)
    answer_text = Column(Text)

    question = relationship("Question", back_populates="answers")
