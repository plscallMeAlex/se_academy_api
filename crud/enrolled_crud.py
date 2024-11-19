import os
import mimetypes
from fastapi import HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session, joinedload
from db.models.user_mdl import User, User_Progress
from db.models.course_mdl import Course
from db.models.enrolled_mdl import Enrolled_Course, Enrolled_Course_Video
from db.models.achievement_mdl import Achievement
from db.schemas.enrolled_sch import (
    EnrolledCourseCreate,
    EnrolledCourseUpdate,
    EnrollmentDetail,
    EnrolledCourseVideoUpdate,
)
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

CHUNK_SIZE = 1024 * 1024

# Enrolled course Section


# for the user when they enroll the course
async def create_enrolled_course(enrolled_course: EnrolledCourseCreate, db: Session):
    if (
        db.query(Enrolled_Course)
        .filter(Enrolled_Course.user_id == enrolled_course.user_id)
        .filter(Enrolled_Course.course_id == enrolled_course.course_id)
        .first()
        is not None
    ):
        raise HTTPException(status_code=400, detail="User already enrolled the course")

    enrolled_course = Enrolled_Course(**enrolled_course.model_dump())
    db.add(enrolled_course)
    db.commit()
    db.refresh(enrolled_course)

    enrolled_course.course.enrolled += 1
    db.commit()

    # creating the enrolled course video via relationship
    for course_video in enrolled_course.course.course_video:
        enrolled_course_video = Enrolled_Course_Video(
            user_id=enrolled_course.user_id,
            enrolled_course_id=enrolled_course.id,
            course_video_id=course_video.id,
        )
        db.add(enrolled_course_video)
        db.commit()

    return JSONResponse(content={"success": True}, status_code=200)


# get all the enrollment
async def get_all_enrolled_course(db: Session):
    print("get_all_enrolled_course")
    enrolled_course = (
        db.query(Enrolled_Course)
        .options(joinedload(Enrolled_Course.course))
        .order_by(Enrolled_Course.enrolled_at.desc())
        .limit(12)
        .all()
    )

    # Sort the enrolled course by the enrolled time recently
    # enrolled_course = sorted(enrolled_course, key=lambda x: x.enrolled_at, reverse=True)

    result = [
        EnrollmentDetail(
            id=enrolled.id,
            username=db.query(User)
            .filter(User.id == enrolled.user_id)
            .first()
            .username,
            course_id=enrolled.course.subjectid,
            course_title=enrolled.course.title,
            enrolled_at=enrolled.enrolled_at,
        )
        for enrolled in enrolled_course
    ]

    return result


# get all the summary of the enrollment by month
async def get_enrollment_summary(db: Session):
    enrolled_courses = (
        db.query(Enrolled_Course)
        .options(joinedload(Enrolled_Course.course))
        .order_by(Enrolled_Course.enrolled_at)
        .all()
    )

    month_counts = Counter(enrolled.enrolled_at.month for enrolled in enrolled_courses)
    month_summary = [month_counts.get(month, 0) for month in range(1, 13)]
    return month_summary


# get all enrolled course that already ended by month
async def get_ended_enrollment_summary(db: Session):
    ended_enrolled_courses = (
        db.query(Enrolled_Course)
        .filter(Enrolled_Course.ended_at.isnot(None))
        .options(joinedload(Enrolled_Course.course))
        .order_by(Enrolled_Course.ended_at.desc())
        .all()
    )

    month_counts = Counter(
        enrolled.ended_at.month for enrolled in ended_enrolled_courses
    )
    month_summary = [month_counts.get(month, 0) for month in range(1, 13)]
    return month_summary


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


# check if the user has enrolled the course
async def check_enrolled_course(user_id: str, course_id: str, db: Session):
    if db.query(User).filter(User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    if db.query(Course).filter(Course.id == course_id).first() is None:
        raise HTTPException(status_code=404, detail="Course not found")

    enrolled_course = (
        db.query(Enrolled_Course)
        .filter(Enrolled_Course.user_id == user_id)
        .filter(Enrolled_Course.course_id == course_id)
        .first()
    )

    if not enrolled_course:
        return JSONResponse(
            content={"success": False, "detail": "User not enrolled the course"},
            status_code=200,
        )

    return JSONResponse(
        content={"success": True, "detail": "User already enrolled the course"},
        status_code=200,
    )


async def check_enrolled_course_ended(enrolled_course_id: str, db: Session):
    # query the enrolled course video to check if the course is already ended
    enrolled_course_videos = (
        db.query(Enrolled_Course_Video)
        .filter(Enrolled_Course_Video.enrolled_course_id == enrolled_course_id)
        .all()
    )

    # Check if the course is already ended
    if all(video.status for video in enrolled_course_videos):
        return JSONResponse(
            content={
                "success": True,
                "detail": "Course is already ended",
                "ended": True,
            },
            status_code=200,
        )

    return JSONResponse(
        content={
            "success": True,
            "detail": "Course is not ended yet",
            "ended": False,
        },
        status_code=200,
    )


# update the enrolled course end date
async def update_enrolled_course(
    enrolled_course_id: str, update_enrolled_course: EnrolledCourseUpdate, db: Session
):
    # Check if it None data
    if update_enrolled_course.ended is None:
        return JSONResponse(
            content={"success": True, "detail": "course is nothing updated"},
            status_code=200,
        )

    db_enrolled_course = (
        db.query(Enrolled_Course)
        .filter(Enrolled_Course.id == enrolled_course_id)
        .first()
    )

    # Check if the course is not found
    if not db_enrolled_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check the boolean value of the ended
    if update_enrolled_course.ended:
        # ended the course at the current time
        current_time = datetime.now(ZoneInfo("Asia/Bangkok"))
        db_enrolled_course.ended_at = current_time
        db.commit()
        db.refresh(db_enrolled_course)

        achievement = (
            db.query(Achievement)
            .filter(Achievement.course_id == db_enrolled_course.course_id)
            .first()
        )
        # If the course has an achievement, then add the achievement to the user
        if achievement:
            user = db.query(User).filter(User.id == db_enrolled_course.user_id).first()
            user.achievements.append(achievement.id)

            user.score += 100
            user.level += 1

            db.commit()
            db.refresh(user)

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


# get the detail of the video timestamp
async def get_enrolled_course_video_detail(
    user_id: str, course_video_id: str, db: Session
):
    enrolled_course_video = (
        db.query(Enrolled_Course_Video)
        .filter(Enrolled_Course_Video.user_id == user_id)
        .filter(Enrolled_Course_Video.course_video_id == course_video_id)
        .first()
    )

    if not enrolled_course_video:
        raise HTTPException(status_code=404, detail="Video not found")

    return enrolled_course_video


# get the enrolled video
async def get_enrolled_course_video(user_id: str, course_video_id: str, db: Session):
    enrolled_video = (
        db.query(Enrolled_Course_Video)
        .filter(Enrolled_Course_Video.user_id == user_id)
        .filter(Enrolled_Course_Video.course_video_id == course_video_id)
        .first()
    )
    if enrolled_video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    # check if the video has started yet
    if enrolled_video.started_at is None:
        enrolled_video.started_at = datetime.now(ZoneInfo("Asia/Bangkok"))
        db.commit()

    video = enrolled_video.course_video
    video_path = video.video_path
    mime_type, _ = mimetypes.guess_type(video_path)

    if not mime_type:
        mime_type = "application/octet-stream"

    def iterfile():
        with open(video_path, "rb") as file:
            while True:
                data = file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    return StreamingResponse(iterfile(), media_type=mime_type)


# update the video status or timestamp
async def update_enrolled_course_video(
    user_id: str,
    course_video_id: str,
    enrolled_course_video: EnrolledCourseVideoUpdate,
    db: Session,
):
    db_enrolled_course_video = (
        db.query(Enrolled_Course_Video)
        .filter(Enrolled_Course_Video.user_id == user_id)
        .filter(Enrolled_Course_Video.course_video_id == course_video_id)
        .first()
    )

    if not enrolled_course_video:
        raise HTTPException(status_code=404, detail="Video not found")

    if enrolled_course_video.timestamp is not None:
        db_enrolled_course_video.timestamp = enrolled_course_video.timestamp

    if enrolled_course_video.status is not None:
        # update the status of the video
        if enrolled_course_video.status:
            # Check if the User progress is already have this enrolled video
            user_progress = (
                db.query(User_Progress)
                .filter(
                    User_Progress.enrolled_course_video_id
                    == db_enrolled_course_video.id
                )
                .first()
            )
            if user_progress:
                raise HTTPException(
                    status_code=400, detail="User already finished this video"
                )

            current_time = datetime.now(ZoneInfo("Asia/Bangkok"))

            db_enrolled_course_video.status = enrolled_course_video.status

            # Check whether the video has started or not
            if db_enrolled_course_video.started_at is None:
                raise HTTPException(status_code=400, detail="Video has not started yet")

            # Handle the ended time of the video
            if db_enrolled_course_video.ended_at is None:
                db_enrolled_course_video.ended_at = current_time

            # adjust time zone
            start_time = db_enrolled_course_video.started_at.astimezone(
                ZoneInfo("Asia/Bangkok")
            )
            end_time = db_enrolled_course_video.ended_at.astimezone(
                ZoneInfo("Asia/Bangkok")
            )

            # Calculate duration
            duration = (end_time - start_time).total_seconds()

            # add the user progress also to track the user is already finished the video
            user_progress = User_Progress(
                user_id=user_id,
                enrolled_course_id=db_enrolled_course_video.enrolled_course_id,
                enrolled_course_video_id=db_enrolled_course_video.id,
                started_at=db_enrolled_course_video.started_at,
                ended_at=db_enrolled_course_video.ended_at,
                duration=duration,
            )
            db.add(user_progress)

            # update the user study hours
            await update_user_study_hours(user_id, duration, db)

    db.commit()
    db.refresh(db_enrolled_course_video)
    return JSONResponse(
        content={"success": True, "detail": "Update the video detail success"},
        status_code=200,
    )


# duration will be unit of second
async def update_user_study_hours(user_id: str, duration: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return
    # Convert the duration to hours
    user.study_hours += duration / 3600
    db.commit()
    db.refresh(user)
    return
