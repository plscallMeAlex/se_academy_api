from fastapi import APIRouter, Depends, UploadFile, File, Query, Form
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from crud import course_crud
from db.database import db_dependency
from db.schemas.course_sch import (
    CourseCreate,
    CourseUpdate,
    CourseDetail,
    CourseVideoCreate,
    CourseVideoDetail,
    CourseVideoUpdate,
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


@router.get("/get_categories", response_model=list[str])
async def get_categorys(db: Session = Depends(db_dependency)):
    return await course_crud.get_categories(db)


@router.get("/category")
async def get_categories_detail(db: Session = Depends(db_dependency)):
    return await course_crud.get_categories_detail(db)


@router.get("/category/{category_id}")
async def get_category_detail(category_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_category_detail(category_id, db)


@router.get("/get_course_img/{course_id}", response_class=JSONResponse)
async def get_course_img(course_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_course_img(course_id, db)


@router.get("/search_courses", response_model=list[CourseDetail])
async def filter_courses(
    course_name: str = Query(...),
    status: str = Query(...),
    db: Session = Depends(db_dependency),
):
    return await course_crud.search_courses(course_name, status, db)


@router.get("/filter_courses_by_status", response_model=list[CourseDetail])
async def filter_courses_by_status(
    status: str = Query(...),
    db: Session = Depends(db_dependency),
):
    return await course_crud.filter_courses_by_status(status, db)


@router.get("/top_courses", response_model=list[CourseDetail])
async def top_courses(
    db: Session = Depends(db_dependency),
):
    return await course_crud.get_top_three_courses(db)


@router.get("/filter_courses_by_category", response_model=list[CourseDetail])
async def filter_courses_by_category(
    category: str = Query(...),
    db: Session = Depends(db_dependency),
):
    return await course_crud.filter_courses_by_category(category, db)


@router.get("/get_courses_by_category/{category_id}", response_model=list[CourseDetail])
async def get_courses_by_category(
    category_id: str, db: Session = Depends(db_dependency)
):
    return await course_crud.get_course_by_category_id(category_id, db)


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
    title: str = Form(...),
    description: str = Form(...),
    chapter: int = Form(...),
    video: UploadFile = File(...),
    db: Session = Depends(db_dependency),
):
    course_video_data = CourseVideoCreate(
        title=title, description=description, chapter=chapter, video=video
    )
    return await course_crud.upload_video(course_id, course_video_data, db)


@router.get("/get_video_detail/{video_id}", response_model=CourseVideoDetail)
async def get_video_detail(video_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_video_detail(video_id, db)


@router.get("/get_videos_detail/{course_id}", response_model=list[CourseVideoDetail])
async def get_videos_detail(course_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_videos_detail(course_id, db)


@router.get("/get_video/{video_id}")
async def get_video(video_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.get_video(video_id, db)


@router.patch("/update_video/{video_id}", response_class=JSONResponse)
async def update_video(
    video_id: str,
    video: CourseVideoUpdate,
    db: Session = Depends(db_dependency),
):
    return await course_crud.update_video(video_id, video, db)


@router.delete("/delete_video/{video_id}", response_class=JSONResponse)
async def delete_video(video_id: str, db: Session = Depends(db_dependency)):
    return await course_crud.delete_video(video_id, db)
