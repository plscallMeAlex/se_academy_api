from sqlalchemy import Column, ForeignKey, Integer, String, Time, Date, Enum as EnumType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mysql import INTEGER as MySQLInteger
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import time
from db.database import Base
from db.models.models import RoleEnum, StatusEnum

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
    role = Column(EnumType(RoleEnum), default=RoleEnum.freshman) 
    level = Column(MySQLInteger(unsigned=True), default=1)
    score = Column(MySQLInteger(unsigned=True), default=0)
    study_hours = Column(Time, default=time())
    status = Column(EnumType(StatusEnum), default=StatusEnum.active)

    # link to user_history & achievement table via user_id
    history = relationship("User_History", back_populates="user", cascade="all, delete-orphan")
    achievement = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")

    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")

class User_History(Base):
    __tablename__ = "user_history"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    # course_id = Column(Integer, ForeignKey("course.id"))
    # course_video_id = Column(Integer, ForeignKey("course_video.id"))
    started_at = Column(Date)
    ended_at = Column(Date)
    started_time = Column(Time)
    stoped_time = Column(Time)
    duration = Column(Time)

    user = relationship("User", back_populates="history")

class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))        # link to user table via user_id
    title = Column(String)
    detail = Column(String)
    image = Column(String)
    type = Column(String)
    received_at = Column(Date)

    user = relationship("User", back_populates="achievement")