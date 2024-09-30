from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

'''SCHEMAS FOR ENROLLED COURSE'''
# Enrolled Course Schemas

# the schema for enrolling the course
class EnrolledCourseCreate(BaseModel):
    user_id: UUID
    course_id: UUID

# to get the course detail
class EnrolledCourseDetail(BaseModel):
    id: UUID
    user_id: UUID
    course_id: UUID
    enrolled_at: datetime
    ended_at: datetime

# to update the course ended
class EnrolledCourseUpdate(BaseModel):
    ended_at: Optional[datetime]

# to change the state or update the enrolled course
class EnrolledCourseDelete(BaseModel):
    user_id: UUID
    course_id: UUID


'''SCHEMAS FOR ENROLLED COURSE VIDEO'''

# Enrolled Course Video Schemas

# to enroll the course video when user play the video that video will be
# add to the enrolled course video to save the progress and make the
# timestamp for user for making a good experience
class EnrolledCourseVideoCreate(BaseModel):
    user_id: UUID
    course_video_id: UUID

# getting the timestamp of the video or get that user has already finished
# the video or not by using the user id or course_video_id
class EnrolledCourseVideoDetail(BaseModel):
    status: bool
    timestamp: float

# to update the video status or timestamp
class EnrolledCourseVideoUpdate(BaseModel):
    status: Optional[bool]
    timestamp: Optional[float]

# to delete the video from the enrolled course video
class EnrolledCourseVideoDelete(BaseModel):
    user_id: UUID
    course_video_id: UUID