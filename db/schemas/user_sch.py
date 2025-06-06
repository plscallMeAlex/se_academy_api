from fastapi import UploadFile, Form, File
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    year: int
    email: EmailStr

    @field_validator("year")
    def validate_year(cls, year):
        if year >= 5:
            return 5
        elif year <= 1:
            return 1
        return year

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


# response that will shown when u want the detail of the user
class UserDetail(BaseModel):
    id: UUID
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    year: int
    avatar: str  # return the api for fetching the avatar image
    level: int
    score: int
    study_hours: float
    status: str
    role: str
    achievements: Optional[list[UUID]]

    class Config:
        from_attributes = True


# simple response if it work u can use it if not u can adjust it
# updating the data for the user
class UserUpdate(BaseModel):
    firstname: Optional[str] = Form(None)
    lastname: Optional[str] = Form(None)
    email: Optional[EmailStr] = Form(None)
    year: Optional[int] = Form(None)


class UserDelete(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: UUID
    username: str
    firstname: str
    lastname: str

    class Config:
        from_attributes = True
