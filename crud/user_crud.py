from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.models.user_mdl import User
from db.models.enum_type import RoleEnum, StatusEnum
from db.schemas.user_sch import UserLogin, UserCreate
from security import create_access_token, verify_password, hash_password


def user_login(user:UserLogin, db:Session):
    db_user = db.query(User).filter(User.username == user.username).first()
    if (db_user is None):
        raise HTTPException(status_code=404, detail="User not found"
                            
    )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    token = create_access_token(db_user,db=db)
    response = JSONResponse(content={"success":True}, status_code=200)
    response.headers["Authorization"] = token
    return response

def user_register(user_create:UserCreate, db:Session):
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
            role = RoleEnum.graduate
        case _:
            role = RoleEnum.freshman
    
    db_user = User(**user_create.model_dump(),role=role, status=status)
    db_user.password = hash_password(user_create.password)
    if (db_user.username in db.query(User.username).all()):
        raise HTTPException(status_code=400, detail="Username is already exists")
    if (db_user.email in db.query(User.email).all()):
        raise HTTPException(status_code=400, detail="Email is already exists")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = JSONResponse(content={"success":True}, status_code=200)
    return response