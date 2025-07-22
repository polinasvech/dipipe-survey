from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from schemas.base_schema import Base


class Category(Base):
    __tablename__ = "categories"
    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    text = Column(Text, nullable=False)

    questions = relationship("Question", back_populates="category")