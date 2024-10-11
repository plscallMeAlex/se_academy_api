from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from db.models.enum_type import StatusEnum
from uuid import UUID
from datetime import datetime

"""SCHEMAS FOR COURSE VIDEO"""
# Course Video Schemas


# the detail that will be shown when the video is requested
class CourseVideoDetail(BaseModel):
    id: UUID
    chapter: Optional[int] = None
    title: str
    video_description: Optional[str] = None
    video_path: str
    duration: float

    class Config:
        from_attributes = True


class CourseVideoUpdate(BaseModel):
    chapter: Optional[int] = None
    title: Optional[str] = None
    video_description: Optional[str] = None
    video_path: Optional[str] = None


"""SCHEMAS FOR COURSE"""
# Course Schemas


# create the course as same as the video but
# you can add video now or later by updating the course
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    subjectid: Optional[str] = ""
    year: Optional[int] = 1
    lecturer: Optional[str] = ""
    created_at: Optional[datetime] = datetime.now()
    status: Optional[StatusEnum] = StatusEnum.active
    category_list: Optional[list] = []


# for updating the course when some detail want to
# be up to date
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subjectid: Optional[str] = None
    category_list: Optional[list] = None
    year: Optional[int] = None
    lecturer: Optional[str] = None
    total_video: Optional[int] = None
    total_duration: Optional[float] = None
    enrolled: Optional[int] = None
    status: Optional[StatusEnum] = StatusEnum.active


# the response model that will be received when you want
# the detail of the course
class CourseDetail(BaseModel):
    id: UUID
    title: str
    description: str
    subjectid: str
    course_image: str
    category_list: List[str]
    year: int
    lecturer: str
    created_at: datetime
    status: StatusEnum
    total_video: int
    total_duration: float
    enrolled: int

    class Config:
        from_attributes = True
