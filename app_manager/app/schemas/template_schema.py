from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Template(Base):
    __tablename__ = 'templates'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    initial_survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.uuid'), nullable=False)
    template_text = Column(Text)
