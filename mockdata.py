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
from db.models.quiz_mdl import Quiz

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

user_student6 = User(
    username="student6",
    password=hash_password("student6"),
    firstname="Student6",
    lastname="Student6",
    year=1,
    email="student6@student6.com",
    role="freshman",
)

user_student7 = User(
    username="student7",
    password=hash_password("student7"),
    firstname="Student7",
    lastname="Student7",
    year=2,
    email="student7@student7.com",
    role="sophomore",
)

user_student8 = User(
    username="student8",
    password=hash_password("student8"),
    firstname="student8",
    lastname="student8",
    year=2,
    email="student8@student8.com",
    role="sophomore",
)

user_student9 = User(
    username="student9",
    password=hash_password("student9"),
    firstname="student9",
    lastname="student9",
    year=2,
    email="student9@student9.com",
    role="sophomore",
)

user_student10 = User(
    username="student10",
    password=hash_password("student10"),
    firstname="student10",
    lastname="student10",
    year=3,
    email="student10@student10.com",
    role="junior",
)

user_student11 = User(
    username="student11",
    password=hash_password("student11"),
    firstname="student11",
    lastname="student11",
    year=3,
    email="student11@student11.com",
    role="junior",
)

user_student12 = User(
    username="student12",
    password=hash_password("student12"),
    firstname="student12",
    lastname="student12",
    year=1,
    email="student12@student12.com",
    role="freshman",
)

data_list.append(user_admin)
data_list.append(user_student1)
data_list.append(user_student2)
data_list.append(user_student3)
data_list.append(user_student4)
data_list.append(user_student5)
data_list.append(user_student6)
data_list.append(user_student7)
data_list.append(user_student8)
data_list.append(user_student9)
data_list.append(user_student10)
data_list.append(user_student11)
data_list.append(user_student12)


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


# SECTION - Quiz Creating
quiz1_1 = Quiz(
    title="DSA Quiz 1",
    course_id=course1.id,
    question="What is the time complexity of the Bubble Sort algorithm?",
    choices=["O(n)", "O(n^2)", "O(n log n)", "O(1)"],
    correct_answer=1,
)

quiz1_2 = Quiz(
    title="DSA Quiz 2",
    course_id=course1.id,
    question="What is the time complexity of the Quick Sort algorithm?",
    choices=["O(n)", "O(n^2)", "O(n log n)", "O(1)"],
    correct_answer=2,
)

quiz1_3 = Quiz(
    title="DSA Quiz 3",
    course_id=course1.id,
    question="What is the time complexity of the Merge Sort algorithm?",
    choices=["O(n)", "O(n^2)", "O(n log n)", "O(1)"],
    correct_answer=2,
)

quiz2_1 = Quiz(
    title="Web Development Quiz 1",
    course_id=course2.id,
    question="What is the full form of HTML?",
    choices=[
        "Hyper Text Markup Language",
        "Hyperlinks and Text Markup Language",
        "Home Tool Markup Language",
        "None of the above",
    ],
    correct_answer=0,
)

quiz2_2 = Quiz(
    title="Web Development Quiz 2",
    course_id=course2.id,
    question="What is the full form of CSS?",
    choices=[
        "Computer Style Sheets",
        "Cascading Style Sheets",
        "Creative Style Sheets",
        "Colorful Style Sheets",
    ],
    correct_answer=1,
)

quiz2_3 = Quiz(
    title="Web Development Quiz 3",
    course_id=course2.id,
    question="What is the full form of HTTP?",
    choices=[
        "Hyper Text Transfer Protocol",
        "Hyper Text Test Protocol",
        "Hyper Tool Transfer Protocol",
        "Hyper Transfer Protocol",
    ],
    correct_answer=0,
)

quiz3_1 = Quiz(
    title="Calculus Quiz 1",
    course_id=course3.id,
    question="What is the derivative of x^2?",
    choices=["1", "2x", "x", "0"],
    correct_answer=1,
)

quiz3_2 = Quiz(
    title="Calculus Quiz 2",
    course_id=course3.id,
    question="What is the integral of x?",
    choices=["1", "2x", "x^2", "0"],
    correct_answer=2,
)

quiz3_3 = Quiz(
    title="Calculus Quiz 3",
    course_id=course3.id,
    question="What is the derivative of sin(x)?",
    choices=["cos(x)", "sin(x)", "tan(x)", "cot(x)"],
    correct_answer=0,
)

quiz4_1 = Quiz(
    title="Embedded Systems Quiz 1",
    course_id=course4.id,
    question="What is the full form of ARM?",
    choices=[
        "Advanced RISC Machine",
        "Advanced Reduced Instruction Set Computer",
        "Advanced Reduced Instruction Set Machine",
        "Advanced RISC Microcontroller",
    ],
    correct_answer=1,
)

quiz4_2 = Quiz(
    title="Embedded Systems Quiz 2",
    course_id=course4.id,
    question="What is the full form of FPGA?",
    choices=[
        "Fast Programming Gate Array",
        "Field Programming Gate Array",
        "Field Programmable Gate Array",
        "Fast Programmable Gate Array",
    ],
    correct_answer=2,
)

quiz4_3 = Quiz(
    title="Embedded Systems Quiz 3",
    course_id=course4.id,
    question="What is the full form of RTOS?",
    choices=[
        "Real Time Operating System",
        "Real Time Operating Software",
        "Real Time Operating Service",
        "Real Time Operating Software",
    ],
    correct_answer=0,
)

quiz5_1 = Quiz(
    title="Computer Programming Quiz 1",
    course_id=course5.id,
    question="What is the full form of CPU?",
    choices=[
        "Central Processing Unit",
        "Central Process Unit",
        "Computer Personal Unit",
        "Central Processor Unit",
    ],
    correct_answer=0,
)

quiz5_2 = Quiz(
    title="Computer Programming Quiz 2",
    course_id=course5.id,
    question="What is the full form of RAM?",
    choices=[
        "Random Access Memory",
        "Randomly Access Memory",
        "Run Access Memory",
        "Random Accessible Memory",
    ],
    correct_answer=0,
)

quiz5_3 = Quiz(
    title="Computer Programming Quiz 3",
    course_id=course5.id,
    question="What is the full form of ROM?",
    choices=[
        "Read Only Memory",
        "Read On Memory",
        "Random Only Memory",
        "Read Only Memory",
    ],
    correct_answer=0,
)

data_list.append(quiz1_1)
data_list.append(quiz1_2)
data_list.append(quiz1_3)
data_list.append(quiz2_1)
data_list.append(quiz2_2)
data_list.append(quiz2_3)
data_list.append(quiz3_1)
data_list.append(quiz3_2)
data_list.append(quiz3_3)
data_list.append(quiz4_1)
data_list.append(quiz4_2)
data_list.append(quiz4_3)
data_list.append(quiz5_1)
data_list.append(quiz5_2)
data_list.append(quiz5_3)


if __name__ == "__main__":
    create_mock_data(data_list)
