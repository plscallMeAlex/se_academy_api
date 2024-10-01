from fastapi import APIRouter, HTTPException, Depends, Header, Form, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import db_dependency  # Adjust the import path as needed
from db.models.user_mdl import User
from db.schemas.user_sch import UserCreate, UserLogin, UserUpdate
from typing import Annotated
from crud import user_crud

router = APIRouter()


@router.post("/login", response_class=JSONResponse)
async def login(user: UserLogin, db: Session = Depends(db_dependency)):
    return user_crud.user_login(user, db)


@router.post("/register")
async def register(user_create: UserCreate, db: Session = Depends(db_dependency)):
    return user_crud.user_register(user_create, db)


@router.put("/update_user/{user_id}", response_class=JSONResponse)
async def update_user(
    user_id: str,
    user: Annotated[UserUpdate, Form()],
    db: Session = Depends(db_dependency),
):
    return user_crud.user_update(user_id, user, db)


@router.put("/update_avatar/{user_id}", response_class=JSONResponse)
async def update_avatar(
    user_id: str,
    avatar: UploadFile = File(...),
    db: Session = Depends(db_dependency),
):
    return await user_crud.user_update_avatar(user_id, avatar, db)
