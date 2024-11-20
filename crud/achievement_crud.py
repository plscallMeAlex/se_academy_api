import os
from fastapi import HTTPException
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from db.models.achievement_mdl import Achievement
from db.schemas.achievement_sch import AchievementCreate, AchievementUpdate
import base64

DEFAULT_NAME = "default_badge.png"
BADGE_PATH = "images/badge"


# create the achievement
async def achievement_create(achievement: AchievementCreate, db: Session):
    # First check the title of the achievement is already exists
    if db.query(Achievement).filter(Achievement.title == achievement.title).first():
        raise HTTPException(status_code=400, detail="Achievement is already exists")

    # If the badge is not uploaded, then set the default badge
    badgePath = DEFAULT_NAME

    if achievement.badge != None:
        # Check the file type is png or jpg or not
        if achievement.badge.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(
                status_code=400, detail="Badge must be in png or jpg format"
            )
        badgePath = achievement.title + ".png"
        with open(f"{BADGE_PATH}/{badgePath}", "wb") as buffer:
            content = await achievement.badge.read()
            buffer.write(content)
    # Change the badge from UploadFile to the path of the badge
    achievement_data = achievement.model_dump()
    achievement_data["badge"] = badgePath

    # De serialize the data and save to the database
    db_achievement = Achievement(**achievement_data)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return JSONResponse(
        content={"success": True, "achievement_id": f"{db_achievement.id}"},
        status_code=200,
    )


# update the achievement via achievement id
async def achievement_update(
    achievement_id: str, achievement: AchievementUpdate, db: Session
):
    # Check the achievement is exists or not
    db_achievement = (
        db.query(Achievement).filter(Achievement.id == achievement_id).first()
    )
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")

    # Check the title of the achievement is already exists
    if (
        db.query(Achievement)
        .filter(Achievement.title == achievement.title)
        .filter(Achievement.id != achievement_id)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Achievement is already exists")

    # If the badge is uploaded, then save the badge
    if achievement.badge:
        badgePath = achievement.title + ".png"
        badge_file_Path = os.path.join(BADGE_PATH, badgePath)

        with open(badge_file_Path, "wb") as buffer:
            content = await achievement.badge.read()
            buffer.write(content)

        # Check if the old badge path is not the default badge path it will be deleted
        if db_achievement.badge != DEFAULT_NAME:
            old_path = os.path.join(BADGE_PATH, db_achievement.badge)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    print(f"Error deleting the file {old_path}: {e}")
        # Update the badge path
        db_achievement.badge = badgePath

    if achievement.title:
        db_achievement.title = achievement.title
    if achievement.description:
        db_achievement.description = achievement.description
    if achievement.course_id:
        db_achievement.course_id = achievement.course_id

    db.commit()
    db.refresh(db_achievement)

    return JSONResponse(
        content={
            "success": True,
            "detail": f"Update achievement id {str(db_achievement.id)} successfully",
        },
        status_code=200,
    )


# Get all the achievement
async def achievement_get_all(db: Session):
    db_achievement = db.query(Achievement).all()
    return db_achievement


# Response when trying to get the achievement detail
async def achievement_get(achievement_id: str, db: Session):
    db_achievement = (
        db.query(Achievement).filter(Achievement.id == achievement_id).first()
    )
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return db_achievement


async def achievement_get_by_course(course_id: str, db: Session):
    db_achievement = (
        db.query(Achievement).filter(Achievement.course_id == course_id).all()
    )
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return db_achievement


# Response the badge image as file response
async def achievement_badge_get(achievement_id: str, db: Session):
    db_achievement = (
        db.query(Achievement).filter(Achievement.id == achievement_id).first()
    )
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")

    with open(f"{BADGE_PATH}/{db_achievement.badge}", "rb") as img:
        base64_img = base64.b64encode(img.read())
    return base64_img


# Delete the achievement
async def achievement_delete(achievement_id: str, db: Session):
    db_achievement = (
        db.query(Achievement).filter(Achievement.id == achievement_id).first()
    )
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")

    # Check if the badge is not the default one
    if db_achievement.badge != DEFAULT_NAME:
        old_path = os.path.join(BADGE_PATH, db_achievement.badge)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception as e:
                print(f"Error deleting the file {old_path}: {e}")

    db.delete(db_achievement)
    db.commit()
    return JSONResponse(content={"success": True}, status_code=200)
