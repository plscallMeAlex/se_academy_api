from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import enrolled_crud
from db.database import db_dependency
from db.schemas.enrolled_sch import (
    EnrolledCourseCreate,
    EnrolledCourseDetail,
    EnrolledCourseUpdate,
    EnrolledCourseVideoCreate,
    EnrolledCourseVideoDetail,
    EnrolledCourseVideoUpdate,
)


router = APIRouter()


@router.post("/create_enrolled_course", response_class=JSONResponse)
async def create_enrolled_course(
    enrolled_course: EnrolledCourseCreate, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.create_enrolled_course(enrolled_course, db)


@router.get("/get_enrolled_course/{user_id}", response_model=list[EnrolledCourseDetail])
async def get_enrolled_course(user_id: str, db: Session = Depends(db_dependency)):
    return await enrolled_crud.get_enrolled_course(user_id, db)


@router.put("/update_enrolled_course/{enrolled_course_id}")
async def update_enrolled_course(
    enrolled_course_id: str,
    update_enrolled_course: EnrolledCourseUpdate,
    db: Session = Depends(db_dependency),
):
    return await enrolled_crud.update_enrolled_course(
        enrolled_course_id, update_enrolled_course, db
    )


@router.delete("/delete_enrolled_course/{enrolled_course_id}")
async def delete_enrolled_course(
    enrolled_course_id: str, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.delete_enrolled_course(enrolled_course_id, db)


@router.post("/create_enrolled_course_video")
async def create_enrolled_course_video(
    enrolled_course_video: EnrolledCourseVideoCreate,
    db: Session = Depends(db_dependency),
):
    return await enrolled_crud.create_enrolled_course_video(enrolled_course_video, db)


@router.get(
    "/get_enrolled_course_video/{enrolled_course_video_id}",
    response_model=EnrolledCourseVideoDetail,
)
async def get_enrolled_course_video(
    enrolled_course_video_id: str, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.get_enrolled_course_video(enrolled_course_video_id, db)


@router.put("/update_enrolled_course_video/{enrolled_course_video_id}")
async def update_enrolled_course_video(
    enrolled_course_video_id: str,
    enrolled_course_video: EnrolledCourseVideoUpdate,
    db: Session = Depends(db_dependency),
):
    return await enrolled_crud.update_enrolled_course_video(
        enrolled_course_video_id, enrolled_course_video, db
    )