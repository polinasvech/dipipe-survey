from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app_manager.app.schemas.base_schema import Base

class Client(Base):
    __tablename__ = 'clients'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    tin = Column(String(10), nullable=False)
    preferences = Column(String(50))
    division = Column(String(50))
    ca_type = Column(String(50))
