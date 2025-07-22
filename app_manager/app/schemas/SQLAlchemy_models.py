from models.question_model import Types
from schemas.base_schema import Base  # Assuming you have a Base class for SQLAlchemy
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class DBAnswer(Base):
    __tablename__ = "answers"

    uuid = Column(SQLUUID, primary_key=True, index=True)
    question_id = Column(SQLUUID, ForeignKey("questions.uuid"))
    client_id = Column(SQLUUID)
    survey_id = Column(SQLUUID)
    answer_int = Column(Integer, nullable=True)
    answer_text = Column(String, nullable=True)

    question = relationship("DBQuestion", back_populates="answers")


class DBQuestion(Base):
    __tablename__ = "questions"

    uuid = Column(SQLUUID, primary_key=True, index=True)
    survey_id = Column(SQLUUID)
    category_id = Column(SQLUUID)
    text = Column(String)
    type = Column(SQLEnum(Types))
    required = Column(Boolean)

    answers = relationship("DBAnswer", back_populates="question")
