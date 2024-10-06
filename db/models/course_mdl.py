from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    ARRAY,
    Enum as EnumType,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime, timezone
from db.models.enum_type import StatusEnum
from db.models.category_mdl import Category
from db.database import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    description = Column(String)
    subjectid = Column(String, default="DEV101")
    course_image = Column(String, default="images/default.jpg")
    category_list = Column(ARRAY(String), default=[])
    year = Column(Integer)
    lecturer = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(EnumType(StatusEnum), default=StatusEnum.active)
    total_video = Column(Integer, default=0)
    total_duration = Column(Float, default=0.0)
    enrolled = Column(Integer, default=0)  # number of students enrolled in the course

    course_video = relationship(
        "Course_Video", back_populates="course", cascade="all, delete-orphan"
    )


class Course_Video(Base):
    __tablename__ = "course_video"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"))
    title = Column(String)
    video_path = Column(String)
    duration = Column(Float, default=0.0)

    course = relationship("Course", back_populates="course_video")
