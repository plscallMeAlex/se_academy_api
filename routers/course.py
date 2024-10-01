from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
from crud import course_crud
from db.database import db_dependency
from db.schemas.course_sch import CourseCreate
import json

router = APIRouter()


@router.post("/create_course", response_class=JSONResponse)
async def create_course(
    course: CourseCreate = Depends(CourseCreate.as_form),
    category_name: Optional[list[str]] = Form(None),
    course_image: Optional[UploadFile] = File(None),
    videos: Optional[list[UploadFile]] = File(None),
    db=Depends(db_dependency),
):
    course_obj = course.model_dump()
    return await course_crud.create_course(
        course_obj, category_name, course_image, videos, db
    )
