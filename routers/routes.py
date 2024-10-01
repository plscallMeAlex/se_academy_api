# Description: This file is used to include all the routers in the application.
from fastapi import APIRouter
from .user import router as users
from .course import router as course

router = APIRouter()
router.include_router(users, prefix="/user", tags=["user"])
router.include_router(course, prefix="/course", tags=["course"])
