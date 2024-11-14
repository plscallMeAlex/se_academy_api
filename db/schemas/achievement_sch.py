from fastapi import Form, UploadFile, File
from pydantic import BaseModel
from typing import Optional

"""SCHEMAS FOR ACHIEVEMENT"""
# Achievement Schemas


# Create the acheivement for the user
class AchievementCreate(BaseModel):
    title: str = Form(...)
    description: str = Form(...)
    badge: Optional[UploadFile] = File(None)


class AchievementUpdate(BaseModel):
    title: Optional[str] = Form(None)
    description: Optional[str] = Form(None)
    badge: Optional[UploadFile] = File(None)


class AchievementResponse(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True
