from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Survey(Base):
    __tablename__ = 'surveys'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    manager_id = Column(UUID(as_uuid=True), ForeignKey('managers.uuid'), nullable=True)
