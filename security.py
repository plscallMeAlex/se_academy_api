# This file contains the function for jwt and hashing
import string
import secrets
from functools import lru_cache
from datetime import datetime, timedelta, timezone 
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.models import token_mdl, user_mdl
from settings import get_settings
from db.database import db_dependency


settings = get_settings()
# Create an engine for encrypting the password.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A function to hash the password
def hash_password(password:str)->str:
    return pwd_context.hash(str(password)+settings.SECRET_KEY)

# A function to verify the password with the hashed password in the database
def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password + settings.SECRET_KEY, hashed_password)

# # A token part to generate the token return the token as a string
def create_access_token(user:user_mdl.User, db:Session, expire_hours:int = 24)->str:
    token_str = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))

    new_token = token_mdl.Token(token=token_str, user_id=user.id, state=True,created_at=datetime.now(timezone.utc),expired_at=datetime.now(timezone.utc)+timedelta(hours=expire_hours), updated_at=datetime.now(timezone.utc))

    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    return token_str

@lru_cache()
def check_token_valid(token:str, db:Session=Depends(db_dependency)):
    token = db.query(token_mdl.Token).filter(token_mdl.Token.token == token).first()

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have a permission to access")
    if token.expired_at < datetime.now(timezone.utc):
        token.state = False
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    return token

# A function to update the expired time of the token
def update_token(token:str, extend_hours:int,db:Session=Depends(db_dependency)):
    token = db.query(token_mdl.Token).filter(token_mdl.Token.token == token).first()
    token.updated_at = datetime.now(timezone.utc)
    token.expired_at = token.expired_at + timedelta(hours=extend_hours)
    if token.expired_at < datetime.now(timezone.utc):
        token.state = False
    else:
        token.state = True
    db.commit()
    return token
