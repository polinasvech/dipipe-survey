from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Question(Base):
    __tablename__ = 'questions'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.uuid', ondelete='CASCADE'), nullable=False)
    text = Column(Text, nullable=False)
