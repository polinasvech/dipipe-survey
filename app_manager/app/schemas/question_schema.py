from sqlalchemy import Column, Text, Boolean, Enum as SQLAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app_manager.app.schemas.base_schema import Base
from app_manager.app.models.question_model import Types  # если Enum Types объявлен в question_schema.py

class Question(Base):
    __tablename__ = 'questions'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.uuid', ondelete='CASCADE'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.uuid', ondelete='CASCADE'), nullable=False)
    text = Column(Text, nullable=False)
    type = Column(SQLAEnum(Types), nullable=False)
    required = Column(Boolean, nullable=False, default=False)

    # Add relationship to Answer
    answers = relationship("Answer", back_populates="question")
    # Add relationship to Survey and Category if needed
    survey = relationship("Survey")
    category = relationship("Category")