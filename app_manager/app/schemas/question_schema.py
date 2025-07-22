from schemas.base_schema import Base
from sqlalchemy import Boolean, Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "questions"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.uuid", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)

    type = Column(Text, nullable=False)
    required = Column(Boolean, nullable=False, default=False)

    # Add relationship to Answer
    answers = relationship("Answer", back_populates="question")
    # Add relationship to Survey and Category if needed
    # survey = relationship("Survey", back_populates="question")  # TODO
    # category = relationship("Category", back_populates="question")  # TODO
