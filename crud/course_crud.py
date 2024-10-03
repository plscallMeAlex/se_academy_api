import os
from fastapi import HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models.course_mdl import Course, Course_Video
from db.schemas.course_sch import (
    CourseCreate,
    CourseUpdate,
)
from moviepy.editor import VideoFileClip


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

    response_data = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "subjectid": course.subjectid,  # Include subjectid
        "course_image": course.course_image,
        "category_list": course.category_list,  # Use the existing field
        "year": course.year,
        "lecturer": course.lecturer,
        "created_at": course.created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Convert datetime to string
        "status": course.status,
        "total_video": course.total_video,
        "total_duration": course.total_duration,
        "enrolled": course.enrolled,
    }

    return response_data


# update the course information
async def update_course(course_id: str, course_update: CourseUpdate, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # handle the q values because some field may be None
    new_course = {k: v for k, v in course_update.model_dump().items() if v is not None}
    course = course.update(new_course)
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
async def get_video(video_id: str, db: Session):
    video = db.query(Course_Video).filter(Course_Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    response_data = {
        "id": video.id,
        "title": video.title,
        "video_path": video.video_path,
        "duration": video.duration,
    }

    return response_data


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
