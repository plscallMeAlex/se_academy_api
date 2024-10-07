from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.models.user_mdl import User
from db.models.enrolled_mdl import Enrolled_Course, Enrolled_Course_Video
from db.schemas.enrolled_sch import (
    EnrolledCourseCreate,
    EnrolledCourseUpdate,
    EnrolledCourseVideoCreate,
    EnrolledCourseVideoUpdate,
)
from datetime import datetime, timezone


# Enrolled course Section


# for the user when they enroll the course
async def create_enrolled_course(enrolled_course: EnrolledCourseCreate, db: Session):
    enrolled_course = enrolled_course.model_dump()
    enrolled_course.enrolled_at = datetime.now(timezone.utc)
    db.add(enrolled_course)
    db.commit()
    db.refresh(enrolled_course)

    return JSONResponse(content={"success": True}, status_code=200)


# get the detail of the enrolled course
async def get_enrolled_course(user_id: str, db: Session):
    if db.query(User).filter(User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    enrolled_course = (
        db.query(Enrolled_Course).filter(Enrolled_Course.user_id == user_id).all()
    )

    if not enrolled_course:
        raise HTTPException(status_code=404, detail="Course not found")

    return enrolled_course


# update the enrolled course end date
async def update_enrolled_course(
    enrolled_course_id: str, update_enrolled_course: EnrolledCourseUpdate, db: Session
):
    if update_enrolled_course.ended_at is None:
        return JSONResponse(
            content={"success": True, "detail": "course is nothing updated"},
            status_code=200,
        )

    if (
        db.query(Enrolled_Course)
        .filter(Enrolled_Course.id == enrolled_course_id)
        .first()
        is None
    ):
        raise HTTPException(status_code=404, detail="Course not found")

    db.query(Enrolled_Course).filter(Enrolled_Course.id == enrolled_course_id).update(
        update_enrolled_course.model_dump(), synchronize_session=False
    )
    db.commit()

    return JSONResponse(content={"success": True}, status_code=200)


# for the user who want to remove the enrolled course
async def delete_enrolled_course(enrolled_course_id: str, db: Session):
    if (
        db.query(Enrolled_Course)
        .filter(Enrolled_Course.id == enrolled_course_id)
        .first()
        is None
    ):
        raise HTTPException(status_code=404, detail="Course not found")

    db.query(Enrolled_Course).filter(Enrolled_Course.id == enrolled_course_id).delete()
    db.commit()

    return JSONResponse(
        content={"success": True, "detail": "Remove the course success"},
        status_code=200,
    )


# Enrolled course video Section


# for the user when play the video first time
async def create_enrolled_course_video(
    enrolled_course_video: EnrolledCourseVideoCreate, db: Session
):
    enrolled_course_video = enrolled_course_video.model_dump()

    db.add(enrolled_course_video)
    db.commit()
    db.refresh(enrolled_course_video)

    return JSONResponse(content={"success": True}, status_code=200)


# get the detail of the video timestamp
async def get_enrolled_course_video_detail(enrolled_course_video_id: str, db: Session):
    enrolled_course_video = (
        db.query(Enrolled_Course_Video)
        .filter(Enrolled_Course_Video.id == enrolled_course_video_id)
        .first()
    )

    if not enrolled_course_video:
        raise HTTPException(status_code=404, detail="Video not found")

    return enrolled_course_video


# update the video status or timestamp
async def update_enrolled_course_video(
    enrolled_course_video_id: str,
    enrolled_course_video: EnrolledCourseVideoUpdate,
    db: Session,
):
    enrolled_course_video = (
        db.query(Enrolled_Course_Video)
        .filter(Enrolled_Course_Video.id == enrolled_course_video_id)
        .first()
    )

    if not enrolled_course_video:
        raise HTTPException(status_code=404, detail="Video not found")

    if enrolled_course_video.status is not None:
        enrolled_course_video.status = enrolled_course_video.status

    if enrolled_course_video.timestamp is not None:
        enrolled_course_video.timestamp = enrolled_course_video.timestamp

    db.commit()
    db.refresh(enrolled_course_video)
    return JSONResponse(
        content={"success": True, "detail": "Update the video detail success"},
        status_code=200,
    )
