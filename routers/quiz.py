from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import db_dependency
from db.schemas.quiz_sch import (
    QuizCreate,
    QuizUpdate,
    QuizDetail,
    QuizResponse,
    QuizSubmissionCreate,
    QuizSubmissionDetail,
    QuizSubmissionResponse,
)
from crud import quiz_crud

router = APIRouter()

# Section for the quiz


@router.post("/create_quiz", response_class=JSONResponse)
async def create_quiz(
    quiz: QuizCreate,
    db=Depends(db_dependency),
):
    quiz = quiz.model_dump()
    return await quiz_crud.quiz_create(quiz, db)


@router.put("/update_quiz/{quiz_id}", response_class=JSONResponse)
async def update_quiz(
    quiz_id: str,
    quiz: QuizUpdate,
    db=Depends(db_dependency),
):
    return await quiz_crud.quiz_update(quiz_id, quiz, db)


@router.get("/get_quiz_all/{course_id}", response_model=list[QuizResponse])
async def get_quiz_all(course_id: str, db: Session = Depends(db_dependency)):
    return await quiz_crud.quiz_get_all(course_id, db)


@router.get("/get_quiz/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: str, db: Session = Depends(db_dependency)):
    return await quiz_crud.quiz_get(quiz_id, db)


@router.get("/get_quiz_detail/{quiz_id}", response_model=QuizDetail)
async def get_quiz_detail(quiz_id: str, db: Session = Depends(db_dependency)):
    return await quiz_crud.quiz_get(quiz_id, db)


@router.delete("/delete_quiz/{quiz_id}", response_class=JSONResponse)
async def delete_quiz(quiz_id: str, db=Depends(db_dependency)):
    return await quiz_crud.quiz_delete(quiz_id, db)


# Section for the quiz submission


@router.post("/submit_quiz", response_class=JSONResponse)
async def submit_quiz(
    quiz_submission: QuizSubmissionCreate,
    db=Depends(db_dependency),
):
    return await quiz_crud.quiz_submission_create(quiz_submission, db)


# Get all the submission response via user_id
@router.get(
    "/get_quiz_submission_all/{user_id}", response_model=list[QuizSubmissionResponse]
)
async def get_quiz_submission_all(user_id: str, db=Depends(db_dependency)):
    return await quiz_crud.quiz_submission_get_all(user_id, db)


# Get the submission response via user_id and course_id
@router.get(
    "/get_quiz_submission_course/{user_id}/{course_id}",
    response_model=QuizSubmissionResponse,
)
async def get_quiz_submission_course(
    user_id: str, course_id: str, db=Depends(db_dependency)
):
    return await quiz_crud.quiz_submission_get(user_id, course_id, db)


# Get the submission response via quiz_submission_id
@router.get(
    "/get_quiz_submission/{quiz_submission_id}", response_model=QuizSubmissionResponse
)
async def get_quiz_submission(quiz_submission_id: str, db=Depends(db_dependency)):
    return await quiz_crud.quiz_submission_get_detail(quiz_submission_id, db)


# Get the submission detail via quiz_submission_id
@router.get(
    "/get_quiz_submission_detail/{quiz_submission_id}",
    response_model=QuizSubmissionDetail,
)
async def get_quiz_submission_detail(
    quiz_submission_id: str, db=Depends(db_dependency)
):
    return await quiz_crud.quiz_submission_get_detail(quiz_submission_id, db)


@router.delete(
    "/delete_quiz_submission/{quiz_submission_id}", response_class=JSONResponse
)
async def delete_quiz_submission(quiz_submission_id: str, db=Depends(db_dependency)):
    return await quiz_crud.quiz_submission_delete(quiz_submission_id, db)
