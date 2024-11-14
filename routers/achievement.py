from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
from sqlalchemy.orm import Session
from db.database import db_dependency
from db.schemas.achievement_sch import (
    AchievementCreate,
    AchievementUpdate,
    AchievementResponse,
)
from uuid import UUID
from crud import achievement_crud

router = APIRouter()


@router.post("/create_achievement", response_class=JSONResponse)
async def create_achievement(
    title: str = Form(...),
    description: str = Form(...),
    badge: UploadFile = File(None),
    course_id: Optional[UUID] = Form(None),
    db: Session = Depends(db_dependency),
):
    achievement_data = AchievementCreate(
        title=title, description=description, badge=badge, course_id=course_id
    )
    return await achievement_crud.achievement_create(achievement_data, db)


@router.put("/update_achievement/{achievement_id}", response_class=JSONResponse)
async def update_achievement(
    achievement_id: str,
    title: str = Form(None),
    description: str = Form(None),
    badge: UploadFile = File(None),
    course_id: Optional[UUID] = Form(None),
    db: Session = Depends(db_dependency),
):
    achievement_data = AchievementUpdate(
        title=title, description=description, badge=badge, course_id=course_id
    )
    return await achievement_crud.achievement_update(
        achievement_id, achievement_data, db
    )


@router.get("/get_achievement/{achievement_id}", response_model=AchievementResponse)
async def get_achievement(achievement_id: str, db: Session = Depends(db_dependency)):
    return await achievement_crud.achievement_get(achievement_id, db)


@router.get("/get_achievement_badge/{achievement_id}", response_class=FileResponse)
async def get_achievement_badge(
    achievement_id: str, db: Session = Depends(db_dependency)
):
    return await achievement_crud.achievement_badge_get(achievement_id, db)


@router.delete("/delete_achievement/{achievement_id}", response_class=JSONResponse)
async def delete_achievement(achievement_id: str, db: Session = Depends(db_dependency)):
    return await achievement_crud.achievement_delete(achievement_id, db)
