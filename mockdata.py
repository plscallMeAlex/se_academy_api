from __future__ import annotations
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from settings import get_settings
from security import hash_password
from db.database import SessionLocal
from db.models.user_mdl import User
from db.models.token_mdl import Token

# This file is for creating the mock data prepared for demonstration purposes.
session: Session = SessionLocal()
data_list = []


def create_mock_data(data_list: list):
    print("Creating mock data...")
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


# User Section
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

user_student1 = User(
    username="student1",
    password=hash_password("student1"),
    firstname="Student1",
    lastname="Student1",
    year=1,
    email="student1@student1.com",
    role="freshman",
)

user_student2 = User(
    username="student2",
    password=hash_password("student2"),
    firstname="Student2",
    lastname="Student2",
    year=2,
    email="student2@student2.com",
    role="sophomore",
)

user_student3 = User(
    username="student3",
    password=hash_password("student3"),
    firstname="Student3",
    lastname="Student3",
    year=3,
    email="student3@student3.com",
    role="junior",
)

user_student4 = User(
    username="student4",
    password=hash_password("student4"),
    firstname="Student4",
    lastname="Student4",
    year=4,
    email="student4@student4.com",
    role="senior",
)

user_student5 = User(
    username="student5",
    password=hash_password("student5"),
    firstname="Student5",
    lastname="Student5",
    year=5,
    email="student5@student5.com",
    role="graduated",
)


data_list.append(user_admin)
data_list.append(user_student1)
data_list.append(user_student2)
data_list.append(user_student3)
data_list.append(user_student4)
data_list.append(user_student5)

if __name__ == "__main__":
    create_mock_data(data_list)
