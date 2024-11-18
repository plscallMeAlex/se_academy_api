from sqlalchemy import Column, String, Integer, ARRAY, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from db.database import Base
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True))
    question = Column(String)  # Question for the quiz
    choices = Column(ARRAY(String))  # Choices for the question
    correct_answer = Column(Integer)  # Index of the correct answer


class Course_Quiz_Submission(Base):
    __tablename__ = "quiz_submission"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True))
    course_id = Column(UUID(as_uuid=True))
    quiz_answers = Column(JSON)  # Answers submitted by the user
    scores = Column(Integer, default=0)  # Scores obtained
    submitted_at = Column(
        DateTime, default=datetime.now(ZoneInfo("Asia/Bangkok"))
    )  # Time when user submitted their quiz
