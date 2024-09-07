from fastapi import APIRouter
from .users import router as users

router = APIRouter()
router.include_router(users, prefix="/users", tags=["users"])  