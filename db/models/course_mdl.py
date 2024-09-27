from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Enum as EnumType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from db.models.enum_type import StatusEnum
from db.database import Base

class Course(Base):
    __tablename__ = "course"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    description = Column(String)
    course_image = Column(String)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"))
    year = Column(Integer)
    created_at = Column(DateTime)
    status = Column(EnumType(StatusEnum))
    total_video = Column(Integer)
    total_duration = Column(Time)
    enrolled = Column(Integer)  # number of students enrolled in the course

    course_video = relationship("Course_Video", back_populates="course", cascade="all, delete-orphan")

class Course_Video(Base):
    __tablename__ = "course_video"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"))
    title = Column(String)
    video_path = Column(String)

    course = relationship("Course", back_populates="course_video")