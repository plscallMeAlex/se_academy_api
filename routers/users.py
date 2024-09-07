from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import db_dependency  # Adjust the import path as needed
from db.models.users_mdl import User
from db.schemas.users_sch import UserCreate, UserResponse

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user(user_create: UserCreate, db: Session = Depends(db_dependency)):
    # Use `db` to interact with the database
    db_user = User(**user_create.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(db_dependency)):
    # Use `db` to interact with the database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
