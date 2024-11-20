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
    CourseVideoCreate,
    CourseVideoUpdate,
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


async def get_course_by_category_id(category_id: str, db: Session):
    category_name = db.query(Category).filter(Category.id == category_id).first()
    if not category_name:
        raise HTTPException(status_code=404, detail="Category not found")

    courses = (
        db.query(Course).filter(Course.category_list.any(category_name.name)).all()
    )
    return courses


async def get_categories(db: Session):
    categories = db.query(Category).all()
    categories = [category.name for category in categories]
    return categories


async def get_categories_detail(db: Session):
    categories = db.query(Category).all()
    return categories


async def get_category_detail(category_id: str, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def get_top_three_courses(db: Session):
    courses = db.query(Course).order_by(Course.enrolled.desc()).limit(3).all()
    return courses


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
        if key == "category_list":
            for category in value:
                category_lower = category.lower()

                exist_category = db.query(Category).all()

                if not any(
                    category_lower in cat.name.lower() for cat in exist_category
                ):
                    new_category = Category(name=category_lower)
                    db.add(new_category)
                    db.commit()
                    db.refresh(new_category)

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
async def upload_video(course_id: str, course_video: CourseVideoCreate, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    video = course_video.video
    total_time = 0
    video_data = await video.read()
    if video.content_type not in ["video/mp4", "video/mov", "video/webm"]:
        raise HTTPException(
            status_code=400,
            detail=f"File {video.filename} type {video.content_type} is not supported for video",
        )

    # Trim and clean up course title for directory naming
    course_title_trimmed = course.title.strip()  # Remove leading and trailing spaces
    course_dir_name = course_title_trimmed.replace(
        " ", "_"
    )  # Replace spaces with underscores

    # Create the course-specific directory if it doesn't exist
    course_dir = f"videos/{course_dir_name}"
    if not os.path.exists(course_dir):
        os.makedirs(course_dir)

    # save the video to the directory
    saveto = f"{course_dir}/{video.filename}"

    # Check if the video already exists in the directory
    if os.path.exists(saveto):
        raise HTTPException(
            status_code=400,
            detail=f"Video {video.filename} already exists in the course directory",
        )

    with open(saveto, "wb") as vid:
        vid.write(video_data)
    clip = VideoFileClip(saveto)
    total_time += clip.duration
    course_video = Course_Video(
        title=course_video.title,
        video_description=course_video.description,
        chapter=course_video.chapter,
        video_path=saveto,
        course_id=course.id,
        duration=clip.duration,
    )
    db.add(course_video)

    course.total_video += 1
    course.total_duration += total_time
    db.commit()
    db.refresh(course)

    return JSONResponse(content={"success": True}, status_code=200)


# get the detail of the video
async def get_video_detail(video_id: str, db: Session):
    video = db.query(Course_Video).filter(Course_Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


# get the detail of the videos in the course
async def get_videos_detail(course_id: str, db: Session):
    videos = (
        db.query(Course_Video)
        .filter(Course_Video.course_id == course_id)
        .order_by(Course_Video.chapter)
        .all()
    )
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


async def update_video(video_id: str, video: CourseVideoUpdate, db: Session):
    course_video = db.query(Course_Video).filter(Course_Video.id == video_id).first()
    if not course_video:
        raise HTTPException(status_code=404, detail="Video not found")

    for key, value in video.model_dump(exclude_unset=True).items():
        if value == None:
            continue
        setattr(course_video, key, value)

    db.add(course_video)
    db.commit()
    db.refresh(course_video)
    return JSONResponse(
        content={"success": True, "detail": f"Update video {video_id} detail success"},
        status_code=200,
    )


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
