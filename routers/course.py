from fastapi import APIRouter, Depends, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from crud import course_crud
from db.database import db_dependency
from db.schemas.course_sch import (
    CourseCreate,
    CourseUpdate,
    CourseDetail,
    CourseVideoDetail,
)

router = APIRouter()


# Course Section
@router.post("/create_course", response_class=JSONResponse)
async def create_course(
    course: CourseCreate,
    db=Depends(db_dependency),
):
    course = course.model_dump()
    return await course_crud.create_course(course, db)


@router.get("/get_course/{course_id}", response_model=CourseDetail)
async def get_course(course_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_course(course_id, db)


@router.get("/get_courses", response_model=list[CourseDetail])
async def get_courses(db: Session = Depends(db_dependency)):
    return await course_crud.get_courses(db)


@router.get("/get_course_img/{course_id}", response_class=JSONResponse)
async def get_course_img(course_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_course_img(course_id, db)


@router.patch("/update_course/{course_id}", response_class=JSONResponse)
async def update_course(
    course_id: str,
    course: CourseUpdate,
    db: Session = Depends(db_dependency),
):
    return await course_crud.update_course(course_id, course, db)


@router.put("/update_course_image/{course_id}", response_class=JSONResponse)
async def update_course_image(
    course_id: str, image: UploadFile = File(...), db: Session = Depends(db_dependency)
):
    return await course_crud.update_course_image(course_id, image, db)


@router.delete("/delete_course/{course_id}", response_class=JSONResponse)
async def delete_course(course_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.delete_course(course_id, db)


# Video Section
@router.post("/upload_video/{course_id}", response_class=JSONResponse)
async def upload_video(
    course_id: str,
    videos: list[UploadFile] = File(None),
    db: Session = Depends(db_dependency),
):
    return await course_crud.upload_video(course_id, videos, db)


@router.get("/get_video_detail/{video_id}", response_model=CourseVideoDetail)
async def get_video_detail(video_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_video(video_id, db)


@router.get("/get_videos_detail/{course_id}", response_model=list[CourseVideoDetail])
async def get_videos_detail(course_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_videos_detail(course_id, db)


@router.get("/get_video/{video_id}")
async def get_video(video_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_video(video_id, db)


@router.delete("/delete_video/{video_id}", response_class=JSONResponse)
async def delete_video(video_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.delete_video(video_id, db)
