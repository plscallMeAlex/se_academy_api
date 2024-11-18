from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from crud import enrolled_crud
from db.database import db_dependency
from db.schemas.enrolled_sch import (
    EnrolledCourseCreate,
    EnrolledCourseDetail,
    EnrollmentDetail,
    EnrolledCourseUpdate,
    EnrolledCourseVideoDetail,
    EnrolledCourseVideoUpdate,
)


router = APIRouter()


@router.post("/create_enrolled_course", response_class=JSONResponse)
async def create_enrolled_course(
    enrolled_course: EnrolledCourseCreate, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.create_enrolled_course(enrolled_course, db)


@router.get("/get_all", response_model=list[EnrollmentDetail])
async def get_all_enrolled_course(db: Session = Depends(db_dependency)):
    return await enrolled_crud.get_all_enrolled_course(db)


@router.get("/get_enrolled_course/{user_id}", response_model=list[EnrolledCourseDetail])
async def get_enrolled_course(user_id: str, db: Session = Depends(db_dependency)):
    return await enrolled_crud.get_enrolled_course(user_id, db)


@router.get("/check_enrolled/{user_id}/{course_id}", response_class=JSONResponse)
async def check_enrolled_course(
    user_id: str, course_id: str, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.check_enrolled_course(user_id, course_id, db)


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


@router.get(
    "/get_enrolled_course_video_detail/{user_id}/{course_video_id}",
    response_model=EnrolledCourseVideoDetail,
)
async def get_enrolled_course_video_detail(
    user_id: str, course_video_id, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.get_enrolled_course_video_detail(
        user_id, course_video_id, db
    )


@router.get(
    "/get_enrolled_course_video/{user_id}/{course_video_id}",
    response_class=StreamingResponse,
)
async def get_enrolled_course_video(
    user_id: str, course_video_id: str, db: Session = Depends(db_dependency)
):
    return await enrolled_crud.get_enrolled_course_video(user_id, course_video_id, db)


@router.put("/update_enrolled_course_video/{user_id}/{course_video_id}")
async def update_enrolled_course_video(
    user_id: str,
    course_video_id: str,
    enrolled_course_video: EnrolledCourseVideoUpdate,
    db: Session = Depends(db_dependency),
):
    return await enrolled_crud.update_enrolled_course_video(
        user_id, course_video_id, enrolled_course_video, db
    )
