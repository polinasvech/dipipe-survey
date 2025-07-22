from schemas.base_schema import Base
from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID


class Template(Base):
    __tablename__ = "templates"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    initial_survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.uuid"), nullable=False)
    template_text = Column(Text)
