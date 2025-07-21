from sqlalchemy import Column, Text, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Answer(Base):
    __tablename__ = 'answers'

    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.uuid', ondelete='CASCADE'), nullable=False)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.uuid', ondelete='CASCADE'), nullable=False)
    answer_int = Column(Integer)
    answer_text = Column(Text)

    __table_args__ = (
        PrimaryKeyConstraint('client_id', 'survey_id'),
    )
