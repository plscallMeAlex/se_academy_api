from sqlalchemy import Column, Boolean, ForeignKey, DateTime, Time, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from db.database import Base
from db.models.course_mdl import Course, Course_Video
from datetime import datetime, timezone


class Enrolled_Course(Base):
    __tablename__ = "enrolled_course"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"))
    enrolled_at = Column(DateTime, default=datetime.now(timezone.utc))
    ended_at = Column(DateTime)

    course = relationship("Course")


class Enrolled_Course_Video(Base):
    __tablename__ = "enrolled_course_video"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    enrolled_course_id = Column(UUID(as_uuid=True), ForeignKey("enrolled_course.id"))
    course_video_id = Column(UUID(as_uuid=True), ForeignKey("course_video.id"))
    status = Column(Boolean, default=False)
    timestamp = Column(Float, default=0.0)

    course_video = relationship("Course_Video")
