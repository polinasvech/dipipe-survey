from uuid import uuid4

from sqlalchemy import Column, Text, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Answer(Base):
    __tablename__ = 'answers'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.uuid',ondelete='CASCADE'), nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.uuid',ondelete='CASCADE'), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.uuid', ondelete='CASCADE'), nullable=False)
    answer_int = Column(Integer)
    answer_text = Column(Text)

