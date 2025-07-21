from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Manager(Base):
    __tablename__ = 'managers'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    full_name = Column(Text, nullable=False)
