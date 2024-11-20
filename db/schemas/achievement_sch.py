from fastapi import Form, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

"""SCHEMAS FOR ACHIEVEMENT"""
# Achievement Schemas


# Create the acheivement for the user
class AchievementCreate(BaseModel):
    title: str = Form(...)
    description: str = Form(...)
    badge: Optional[UploadFile] = File(None)
    course_id: Optional[UUID] = Form(None)


class AchievementUpdate(BaseModel):
    title: Optional[str] = Form(None)
    description: Optional[str] = Form(None)
    badge: Optional[UploadFile] = File(None)
    course_id: Optional[UUID] = Form(None)


class AchievementResponse(BaseModel):
    id: UUID
    title: str
    description: str
    badge: str  # return the api for fetching the badge image

    class Config:
        from_attributes = True
