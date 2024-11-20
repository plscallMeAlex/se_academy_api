from __future__ import annotations
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from settings import get_settings
from security import hash_password
from db.database import SessionLocal
from db.models.user_mdl import User
from db.models.token_mdl import Token
from db.models.category_mdl import Category
from db.models.course_mdl import Course
from db.models.achievement_mdl import Achievement

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


# SECTION - User Creating
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


# SECTION - Category Creating
category1 = Category(name="Programming")
category2 = Category(name="Analysis")
category3 = Category(name="Design")
category4 = Category(name="Mathematics")
category5 = Category(name="Science")
category6 = Category(name="Language")

data_list.append(category1)
data_list.append(category2)
data_list.append(category3)
data_list.append(category4)
data_list.append(category5)
data_list.append(category6)


# SECTION - Course Creating
course1 = Course(
    title="DSA",
    description="Data Structures and Algorithms course for beginners.",
    subjectid="COM201",
    course_image="images/dsa.png",
    category_list=["Programming", "Analysis"],
    year=2,
    lecturer="Doctor Sunthana",
)

course2 = Course(
    title="Web Development",
    description="Web Development course for beginners.",
    subjectid="COM202",
    course_image="images/webdev.jpg",
    category_list=["Programming", "Design"],
    year=2,
    lecturer="Doctor Visit",
)

course3 = Course(
    title="Calculus",
    description="Calculus course for beginners.",
    subjectid="MATH101",
    course_image="images/calculus.png",
    category_list=["Mathematics"],
    year=1,
    lecturer="Doctor Tui",
)

course4 = Course(
    title="Embedded Systems",
    description="Embedded Systems course for beginners.",
    subjectid="COM301",
    course_image="images/embedded.jpg",
    category_list=["Programming", "Analysis"],
    year=3,
    lecturer="Doctor Phairoj",
)

course5 = Course(
    title="Computer Programming",
    description="Computer Programming course for beginners.",
    subjectid="COM101",
    course_image="images/computerprogramming.jpg",
    category_list=["Programming"],
    year=1,
    lecturer="Doctor Visit",
)

data_list.append(course1)
data_list.append(course2)
data_list.append(course3)
data_list.append(course4)
data_list.append(course5)


# SECTION - Achievement Creating
achievement1 = Achievement(
    title="Ur Logic is Good",
    description="You have completed the DSA course.",
    course_id=course1.id,
)

achievement2 = Achievement(
    title="DEV Master",
    description="You have completed the Web Development course.",
    course_id=course2.id,
)

achievement3 = Achievement(
    title="Math Genius",
    description="You have completed the Calculus course.",
    course_id=course3.id,
)

achievement4 = Achievement(
    title="Embedded Systems Expert",
    description="You have completed the Embedded Systems course.",
    course_id=course4.id,
)

achievement5 = Achievement(
    title="Programming Prodigy",
    description="You have completed the Computer Programming course.",
    course_id=course5.id,
)

data_list.append(achievement1)
data_list.append(achievement2)
data_list.append(achievement3)
data_list.append(achievement4)
data_list.append(achievement5)


if __name__ == "__main__":
    create_mock_data(data_list)
