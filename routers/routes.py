# Description: This file is used to include all the routers in the application.
from fastapi import APIRouter
from .user import router as users

router = APIRouter()
router.include_router(users, prefix="/user", tags=["user"])  