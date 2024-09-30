from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from db.models.enum_type import StatusEnum
from uuid import UUID

'''SCHEMAS FOR COURSE VIDEO'''
# Course Video Schemas

# create the each video by adding it title and the path of the video
class CourseVideoCreate(BaseModel):
    title: str
    video_path: str

# the detail that will be shown when the video is requested
class CourseVideoDetail(BaseModel):
    id: UUID
    title: str  
    video_path: str
    duration: float

# for updating the video in the situation that you want to update the path or
# the title of the video
class CourseVideoUpdate(BaseModel):
    title: Optional[str]
    video_path: Optional[str]

# for deleting the video or suspending the video
class CourseVideoDelete(BaseModel):
    video_id: UUID


'''SCHEMAS FOR COURSE'''
# Course Schemas

# create the course as same as the video but
# you can add video now or later by updating the course
class CourseCreate(BaseModel):
    title: str
    description: str
    year: int

    @classmethod
    def as_form(cls, title:str, description:str, year:int)-> 'CourseCreate':
        return cls(title=title, description=description, year=year)

# for updating the course when some detail want to
# be up to date
class CourseUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    course_image: Optional[str]
    category_id: Optional[UUID]
    year: Optional[int]
    status: Optional[StatusEnum]
    videos: Optional[list[CourseVideoCreate]]

# the response model that will be received when you want
# the detail of the course  
class CourseDetail(BaseModel):
    id: UUID
    title: str
    description: str
    course_image: str
    category_id: UUID
    year: int
    created_at: str
    status: StatusEnum
    total_video: int
    total_duration: float
    enrolled: int

# for suspending the course
class CourseDelete(BaseModel):
    course_id: UUID