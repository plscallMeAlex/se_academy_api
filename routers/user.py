from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse 
from sqlalchemy.orm import Session
from db.database import db_dependency  # Adjust the import path as needed
from db.models.user_mdl import User
from db.schemas.user_sch import UserCreate, UserResponse, UserLogin
from security import hash_password, create_access_token, verify_password


router = APIRouter()

@router.post("/login",response_class=JSONResponse)
async def login(user:UserLogin, db:Session=Depends(db_dependency)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if (db_user is None):
        raise HTTPException(status_code=404, detail="User not found"
                            
    )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    token = create_access_token(db_user,db=db)
    response = JSONResponse(content={"login":"success"}, status_code=200)
    response.headers["Authorization"] = token
    return response

@router.post("/register")
async def register(user_create: UserCreate, db: Session = Depends(db_dependency)):
    db_user = User(**user_create.model_dump())
    db_user.password = hash_password(user_create.password)
    if (db_user.username in db.query(User.username).all() or db_user.email in db.query(User.email).all()):
        raise HTTPException(status_code=400, detail="Username or Email is already exists")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = JSONResponse(content={"register":"success"}, status_code=200)
    return response
                                                                       
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