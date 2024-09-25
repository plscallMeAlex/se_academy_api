from db.models.user_mdl import RoleEnum, StatusEnum
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
    
class UserDelete(BaseModel):
    id: UUID
    class Config:
        from_attributes = True

class UserDetail(BaseModel):
    id: Optional[UUID]  = None
    username: Optional[str] = None
    firstname: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: UUID
    username: str
    firstname: str
    lastname: str

    class Config:
        from_attributes = True

