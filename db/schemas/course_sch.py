from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from db.models.enum_type import StatusEnum
from uuid import UUID

"""SCHEMAS FOR COURSE VIDEO"""
# Course Video Schemas


# the detail that will be shown when the video is requested
class CourseVideoDetail(BaseModel):
    id: UUID
    title: str
    video_path: str
    duration: float


"""SCHEMAS FOR COURSE"""
# Course Schemas


# create the course as same as the video but
# you can add video now or later by updating the course
class CourseCreate(BaseModel):
    title: str
    description: str
    subjectid: str
    year: int
    lecturer: str


# for updating the course when some detail want to
# be up to date
class CourseUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    subjectid: Optional[str]
    category_list: Optional[list]
    year: Optional[int]
    lecturer: Optional[str]
    status: Optional[StatusEnum]


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
    created_at: str
    status: StatusEnum
    total_video: int
    total_duration: float
    enrolled: int

    class Config:
        from_attributes = True
