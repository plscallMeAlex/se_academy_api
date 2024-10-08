import os
import base64
import mimetypes
from fastapi import HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models.category_mdl import Category
from db.models.course_mdl import Course, Course_Video
from db.schemas.course_sch import (
    CourseCreate,
    CourseUpdate,
)
from moviepy.editor import VideoFileClip


# Course Section


# create the course and add it to the database
async def create_course(
    course: CourseCreate,
    db: Session,
):
    course = Course(**course)
    db.add(course)
    db.commit()
    db.refresh(course)

    return JSONResponse(content={"success": True}, status_code=200)


# get the detail of the course
async def get_course(course_id: str, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


async def get_courses(db: Session):
    courses = db.query(Course).all()
    return courses


async def search_courses(course_name: str, status: str, db: Session):

    if status == "all":
        courses = db.query(Course).filter(Course.title.like(f"%{course_name}%")).all()
    else:
        courses = (
            db.query(Course)
            .filter(Course.title.like(f"%{course_name}%"))
            .filter(Course.status == status)
            .all()
        )
    return courses


async def filter_courses_by_status(status: str, db: Session):
    if status == "all":
        courses = db.query(Course).all()
    else:
        courses = db.query(Course).filter(Course.status == status).all()
    return courses


async def filter_courses_by_category(category: str, db: Session):
    if category == "all":
        courses = db.query(Course).all()
    else:
        courses = db.query(Course).filter(Course.category_list.any(category)).all()

    return courses


async def get_categories(db: Session):
    categories = db.query(Category).all()
    categories = [category.name for category in categories]
    return categories


# Course Section


async def get_course_img(course_id: str, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    with open(course.course_image, "rb") as img:
        base64_img = base64.b64encode(img.read())
    return base64_img


# update the course information
async def update_course(course_id: str, course_update: CourseUpdate, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course_update.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    db.add(course)
    db.commit()
    db.refresh(course)
    return JSONResponse(content={"success": True}, status_code=200)


# update the course image path and then add file to the backend
async def update_course_image(course_id: str, course_image: UploadFile, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_image is None:
        raise HTTPException(status_code=400, detail="No image uploaded")

    image_data = await course_image.read()
    if course_image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only jpeg and png files are allowed",
        )

    saveto = f"images/{course_image.filename}"
    with open(saveto, "wb") as img:
        img.write(image_data)

    course.course_image = saveto
    db.add(course)
    db.commit()
    db.refresh(course)

    return JSONResponse(content={"success": True}, status_code=200)


# delete the course and remove it from the database
async def delete_course(course_id: str, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # delete the video in the course
    db.query(Course_Video).filter(Course_Video.course_id == course_id).delete()
    db.delete(course)
    db.commit()
    return JSONResponse(content={"success": True}, status_code=200)


# Video Section
CHUNK_SIZE = 1024 * 1024


# upload the video the course and add it to the database
async def upload_video(course_id: str, videos: list[UploadFile], db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if videos == []:
        raise HTTPException(status_code=400, detail="No video uploaded")

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

        # check whether the video is already in the directory
        video_in_dir = False
        try:
            with open(f"videos/{video.filename}", "r") as f:
                video_in_dir = True
        except FileNotFoundError:
            video_in_dir = False

        if existname:
            if not video_in_dir:
                with open(f"videos/{video.filename}", "wb") as vid:
                    vid.write(video_data)
            raise HTTPException(
                status_code=400,
                detail=f"Video {video.filename} already exists in the course",
            )

        # save the video to the directory
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

    course.total_video += len(videos)
    course.total_duration += total_time
    db.commit()
    db.refresh(course)

    return JSONResponse(
        content={"success": True, "videos_uploaded": len(videos)}, status_code=200
    )


# get the detail of the video
async def get_video_detail(video_id: str, db: Session):
    video = db.query(Course_Video).filter(Course_Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


# get the detail of the videos in the course
async def get_videos_detail(course_id: str, db: Session):
    videos = db.query(Course_Video).filter(Course_Video.course_id == course_id).all()
    if not videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos


# get the video and return as a stream of video
async def get_video(video_id: str, db: Session):
    video = db.query(Course_Video).filter(Course_Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video_path = video.video_path
    mime_type, _ = mimetypes.guess_type(video_path)

    if not mime_type:
        mime_type = "application/octet-stream"

    def iterfile():
        with open(video.video_path, "rb") as vid:
            while True:
                chunk = vid.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(iterfile(), media_type=mime_type)


# delete the video video id and remove it from the database
async def delete_video(video_id: str, db: Session):
    video = db.query(Course_Video).filter(Course_Video.id == video_id).first()
    course = db.query(Course).filter(Course.id == video.course_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    file_path = video.video_path
    file_name = video.video_path.split("/")[-1]

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    course.total_video -= 1
    course.total_duration -= video.duration
    db.delete(video)
    db.commit()
    db.refresh(course)

    return JSONResponse(
        content={"success": True, "detail": f"Video {file_name} delete successful"},
        status_code=200,
    )
