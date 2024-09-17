from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    avatar: Optional[str]

class UserCreate(UserBase):
    username: str
    password: str
    firstname: str
    lastname: str
    year: int
    email: EmailStr
    role:str
    status:str 

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
    
class UserDelete(UserBase):
    id: UUID
    class Config:
        from_attributes = True

class UserDetail(UserBase):
    id: Optional[UUID]  = None
    username: Optional[str] = None
    firstname: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: UUID
    username: str
    firstname: str
    lastname: str

    class Config:
        from_attributes = True

