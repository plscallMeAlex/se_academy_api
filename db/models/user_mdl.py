from sqlalchemy import Column, ForeignKey, Integer, String, Time, Date, DateTime, Enum as EnumType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mysql import INTEGER as MySQLInteger
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import time
from db.database import Base
from db.models.enum_type import RoleEnum, StatusEnum

# This make the tables that interact with the user table become the child of the User class to make easy
# to maintain by using relationship with cascad to delete the child table when the parent table is deleted

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    year = Column(Integer)
    email = Column(String, unique=True, index=True)
    avatar = Column(String)
    role = Column(EnumType(RoleEnum, name="roleenum"), default=RoleEnum.freshman) 
    level = Column(MySQLInteger(unsigned=True), default=1)
    score = Column(MySQLInteger(unsigned=True), default=0)
    study_hours = Column(Time, default=time())
    status = Column(EnumType(StatusEnum), default=StatusEnum.active)

    # relationship between user and other tables
    progress = relationship("User_Progress", back_populates="user", cascade="all, delete-orphan")
    achievement = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")

class User_Progress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    enrolled_course_id = Column(UUID(as_uuid=True), ForeignKey("enrolled_course.id"))
    enrolled_course_video_id = Column(UUID(as_uuid=True), ForeignKey("enrolled_course_video.id"))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration = Column(Time)

    # relationship between user_progress and other tables
    user = relationship("User", back_populates="progress")
    enrolled_course = relationship("Enrolled_Course", cascade="all, delete-orphan")
    enrolled_course_video = relationship("Enrolled_Course_Video", cascade="all, delete-orphan")

class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))        # link to user table via user_id
    title = Column(String)
    description = Column(String)
    badge = Column(String)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"))
    received_at = Column(Date)

    user = relationship("User", back_populates="achievement")