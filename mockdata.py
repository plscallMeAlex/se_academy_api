from __future__ import annotations
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from settings import get_settings
from db.database import SessionLocal
from db.models.user_mdl import User
from db.models.token_mdl import Token

# This file is for creating the mock data prepared for demonstration purposes.
session: Session = SessionLocal()
data_list = []


def create_mock_data(data_list: list):
    try:
        for data in data_list:
            session.add(data)
            session.commit()
            session.refresh(data)
            print(f"Data {data} has been created.")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()


# User Create Section
settins = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(str(password) + settins.SECRET_KEY)


user_admin = User(
    username="admin",
    password=hash_password("admin"),
    firstname="Admin",
    lastname="Admin",
    year=5,
    email="Admin@admin.com",
    role="admin",
    level=9999,
    score=9999,
    study_hours=9999.99,
    status="active",
)

data_list.append(user_admin)
