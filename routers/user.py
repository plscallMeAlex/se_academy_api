from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse 
from sqlalchemy.orm import Session
from crud import user_crud
from db.database import db_dependency  # Adjust the import path as needed
from db.models.user_mdl import User
from db.models.enum_type import RoleEnum, StatusEnum
from db.schemas.user_sch import UserCreate, UserResponse, UserLogin
from security import hash_password, create_access_token, verify_password


router = APIRouter()

@router.post("/login",response_class=JSONResponse)
async def login(user:UserLogin, db:Session=Depends(db_dependency)):
    return user_crud.user_login(user, db)

@router.post("/register")
async def register(user_create: UserCreate, db: Session = Depends(db_dependency)):
    return user_crud.user_register(user_create, db)
                                                                       
@router.get("/get_user", response_model=UserResponse)
async def read_user(
    id: str = None,
    username: str = None,
    firstname: str = None,
    db: Session = Depends(db_dependency)
):
    # Use `db` to interact with the database
    if id is not None:
        db_user = db.query(User).filter(User.id == id).first()
    elif username is not None:
        db_user = db.query(User).filter(User.username == username).first()
    elif firstname is not None:
        db_user = db.query(User).filter(User.firstname == firstname).first()
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user