from fastapi import HTTPException, Form, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from typing import Annotated
from sqlalchemy.orm import Session
from db.models.user_mdl import User, User_Progress
from db.models.enrolled_mdl import Enrolled_Course, Enrolled_Course_Video
from db.models.course_mdl import Course, Course_Video
from db.models.enum_type import RoleEnum, StatusEnum
from db.schemas.user_sch import UserLogin, UserCreate, UserUpdate
from settings import get_settings
from security import create_access_token, verify_password, hash_password
import base64

SETTINGS = get_settings()


# login user and assign the token to the user
def user_login(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    token = create_access_token(db_user, db=db)
    response = JSONResponse(
        content={"success": True, "id": str(db_user.id), "role": db_user.role},
        status_code=200,
    )
    response.headers["Authorization"] = token
    return response


# register user
def user_register(user_create: UserCreate, db: Session):
    role = None
    status = StatusEnum.active
    match user_create.year:
        case 1:
            role = RoleEnum.freshman
        case 2:
            role = RoleEnum.sophomore
        case 3:
            role = RoleEnum.junior
        case 4:
            role = RoleEnum.senior
        case 5:
            role = RoleEnum.graduated
        case _:
            role = RoleEnum.freshman

    db_user = User(**user_create.model_dump(), role=role, status=status)
    db_user.password = hash_password(user_create.password)
    if db_user.username in db.query(User.username).all():
        raise HTTPException(status_code=400, detail="Username is already exists")
    if db_user.email in db.query(User.email).all():
        raise HTTPException(status_code=400, detail="Email is already exists")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = JSONResponse(content={"success": True}, status_code=200)
    return response


# get user detail
async def get_user(user_id: str, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.avatar = f"{SETTINGS.BACKEND_URL}/user/avatar/{user_id}"
    return db_user


# get all users
async def get_users(db: Session):
    db_users = db.query(User).filter(User.role != "admin").all()
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    # assign the avatar api for each user
    for user in db_users:
        user.avatar = f"{SETTINGS.BACKEND_URL}/user/avatar/{user.id}"
    return db_users


# get user avatar
async def get_avatar(user_id: str, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.avatar is None:
        raise HTTPException(status_code=404, detail="User avatar not found")

    with open(db_user.avatar, "rb") as img:
        base64_img = base64.b64encode(img.read())
    return base64_img


# get the top 3 users to display on the leaderboard
async def get_leaderboard(db: Session):
    db_users = (
        db.query(User)
        .order_by(User.level.desc())
        .order_by(User.score.desc())
        .filter(User.role != RoleEnum.admin)
        .limit(3)
        .all()
    )
    if db_users is None:
        raise HTTPException(status_code=404, detail="Leaderboard not found")
    return db_users


# get user progress
async def get_user_progress(user_id: str, db: Session):
    user_progress = (
        db.query(User_Progress)
        .filter(User_Progress.user_id == user_id)
        .order_by(User_Progress.started_at.desc())
        .limit(10)
        .all()
    )

    if user_progress is None:
        raise HTTPException(status_code=404, detail="User progress not found")

    result = []

    for progress in user_progress:

        enrollment = (
            db.query(Enrolled_Course)
            .filter(Enrolled_Course.id == progress.enrolled_course_id)
            .first()
        )

        video_enrollment = (
            db.query(Enrolled_Course_Video)
            .filter(Enrolled_Course_Video.id == progress.enrolled_course_video_id)
            .first()
        )

        course_name = db.query(Course).filter(Course.id == enrollment.course_id).first()

        video_name = (
            db.query(Course_Video)
            .filter(Course_Video.id == video_enrollment.course_video_id)
            .first()
        )

        result.append(
            {
                "course_name": course_name.title,
                "video_name": video_name.title,
                "started_at": progress.started_at,
                "ended_at": progress.ended_at,
                "duration": progress.duration,
            }
        )

    return result


# for update information of the user
def user_update(user_id: str, user: Annotated[UserUpdate, Form()], db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump().items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = JSONResponse(content={"success": True}, status_code=200)
    return response


# for update avatar of the user
async def user_update_avatar(user_id: str, avatar: UploadFile, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if avatar.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only jpeg and png files are allowed",
        )

    img_data = await avatar.read()
    saveto = f"images/{avatar.filename}"
    with open(saveto, "wb") as img:
        img.write(img_data)

    db_user.avatar = saveto
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = JSONResponse(content={"success": True}, status_code=200)
    return response


# for delete the user
async def user_delete(user_id: str, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return JSONResponse(content={"success": True}, status_code=200)
