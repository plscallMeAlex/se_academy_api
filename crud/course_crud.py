import string
from typing import Optional
from fastapi import HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models.course_mdl import Course, Course_Video
from db.models.category_mdl import Category
from db.schemas.course_sch import (
    CourseCreate,
    CourseDetail,
    CourseUpdate,
    CourseDelete,
    CourseVideoCreate,
    CourseVideoDetail,
    CourseVideoUpdate,
    CourseVideoDelete,
)
from uuid import UUID, uuid4
from moviepy.editor import VideoFileClip
from datetime import time


async def create_course(
    course: CourseCreate,
    category_name: Optional[list[str]],
    course_image: Optional[UploadFile],
    videos: Optional[list[UploadFile]],
    db: Session,
):
    course = Course(**course)

    # handle optional values
    if course_image is None:
        course_image = None
    if videos is None:
        videos = []

    if category_name:
        list_category = []
        # create a new category if it does not exist
        for category in category_name:
            existing_category = (
                db.query(Category)
                .filter(func.lower(Category.name) == category.lower())
                .first()
            )
            if not existing_category:
                new_category = Category(name=string.capwords(category))
                list_category.append(
                    new_category
                )  # store the category name for the course
                db.add(new_category)
            else:
                list_category.append(existing_category)

        db.commit()

        # refresh session obj state
        for category in list_category:
            db.refresh(category)

        course.category_list = [category.name for category in list_category]
    else:
        course.category_list = ["Uncategorized"]

    if course_image:
        img_data = await course_image.read()
        if course_image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only jpeg and png files are allowed",
            )
        saveto = f"images/{course_image.filename}"
        with open(saveto, "wb") as img:
            img.write(img_data)

        course.course_image = saveto
    db.add(course)
    db.commit()
    db.refresh(course)

    if videos != []:
        total_time = 0
        for video in videos:
            video_data = await video.read()
            if video.content_type not in ["video/mp4", "video/mov", "video/webm"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {video.filename} type {video.content_type} is not supported for video",
                )
            existname = (
                db.query(Course_Video)
                .filter(func.lower(Course_Video.title) == video.filename.lower())
                .first()
            )
            if video.filename in [video.title for video in course.videos]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Video {video.filename} already exists in the course",
                )

            saveto = f"videos/{video.filename}"
            with open(saveto, "wb") as vid:
                vid.write(video_data)
            clip = VideoFileClip(saveto)
            total_time += clip.duration

            course_video = Course_Video(
                title=video.filename,
                video_path=saveto,
                course_id=course.id,
                duration=clip.duration,
            )
            db.add(course_video)

        course.total_video = len(videos)
        course.total_duration = total_time
    else:
        course.total_video = 0
        course.total_duration = 0.0

    db.commit()
    db.refresh(course)
    return JSONResponse(
        content={"success": True, "videos_uploaded": len(videos)}, status_code=200
    )
