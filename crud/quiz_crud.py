from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.models.quiz_mdl import Quiz, Course_Quiz_Submission
from db.schemas.quiz_sch import QuizCreate, QuizUpdate, QuizSubmissionCreate

# Section for the quiz


# Create the quiz
async def quiz_create(quiz: QuizCreate, db: Session):
    quiz = Quiz(**quiz.model_dump())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return JSONResponse(
        content={"success": True, "quiz_id": f"{quiz.id}"}, status_code=200
    )


# When want to update the quiz (It's creating the new one)
async def quiz_update(quiz_id: str, quiz: QuizUpdate, db: Session):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz.course_id != None:
        db_quiz.course_id = quiz.course_id
    if quiz.question != None:
        db_quiz.question = quiz.question
    if quiz.choices != None:
        db_quiz.choices = quiz.choices
    if quiz.correct_answer != None:
        db_quiz.correct_answer = quiz.correct_answer

    db.commit()
    return JSONResponse(
        content={"success": True, "detail": "update the detail successfully"},
        status_code=200,
    )


# Get all the quiz from the specific course
async def quiz_get_all(course_id: str, db: Session):
    if db.query(Quiz).filter(Quiz.course_id == course_id).first() is None:
        raise HTTPException(status_code=404, detail="Quiz not found in this course")
    quiz = db.query(Quiz).filter(Quiz.course_id == course_id).all()
    return quiz


# Get the specific quiz via quiz id can be quiz detail or quiz response from the pydantic model
# (Having 2 responses possible 1: QuizDetail, 2: QuizResponse)
async def quiz_get(quiz_id: str, db: Session):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


# Delete the quiz via quiz id
async def quiz_delete(quiz_id: str, db: Session):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db.delete(db_quiz)
    db.commit()
    return JSONResponse(
        content={
            "success": True,
            "detail": f"delete the quiz id {quiz_id} successfully",
        },
        status_code=200,
    )


# Section for the quiz submission


# Create the quiz submission (When the user submit the quiz)
async def quiz_submission_create(quiz_submission: QuizSubmissionCreate, db: Session):
    # Trying to calculate the scores
    scores = 0
    quiz_list = db.query(Quiz).filter(Quiz.course_id == quiz_submission.course_id).all()

    # Create a mapping of quiz_id to Quiz object for easy lookup
    quiz_map = {}
    for item in quiz_list:
        quiz_map[str(item.id)] = item.correct_answer

    # Iterate over the submitted answers
    for k, v in quiz_submission.quiz_answers.items():
        if quiz_map.get(k) == v:
            scores += 1

    quiz_submission = Course_Quiz_Submission(
        user_id=quiz_submission.user_id,
        course_id=quiz_submission.course_id,
        quiz_answers=quiz_submission.quiz_answers,
        scores=scores,
    )

    db.add(quiz_submission)
    db.commit()
    db.refresh(quiz_submission)

    return JSONResponse(
        content={"success": True, "quiz_submission_id": f"{quiz_submission.id}"},
        status_code=200,
    )


# get all of the quiz submission from the specific user id and will reponse as list of the quiz submission response
async def quiz_submission_get_all(user_id: str, db: Session):
    quiz_submission = (
        db.query(Course_Quiz_Submission)
        .filter(Course_Quiz_Submission.user_id == user_id)
        .all()
    )
    if quiz_submission is None:
        raise HTTPException(status_code=404, detail="Quiz submission not found")

    return quiz_submission


# Get the quiz submission detail via quiz user and course id will return the quiz submission response
async def quiz_submission_get(user_id: str, course_id: str, db: Session):
    quiz_submission = (
        db.query(Course_Quiz_Submission)
        .filter(Course_Quiz_Submission.user_id == user_id)
        .filter(Course_Quiz_Submission.course_id == course_id)
        .first()
    )
    if quiz_submission is None:
        raise HTTPException(status_code=404, detail="Quiz submission not found")
    return quiz_submission


# get the quiz submission detail via quiz submission id will return the quiz submission response or detail as you want
async def quiz_submission_get_detail(quiz_submission_id: str, db: Session):
    quiz_submission = (
        db.query(Course_Quiz_Submission)
        .filter(Course_Quiz_Submission.id == quiz_submission_id)
        .first()
    )
    if quiz_submission is None:
        raise HTTPException(status_code=404, detail="Quiz submission not found")
    return quiz_submission


# Delete the quiz submission via quiz submission id
async def quiz_submission_delete(quiz_submission_id: str, db: Session):
    quiz_submission = (
        db.query(Course_Quiz_Submission)
        .filter(Course_Quiz_Submission.id == quiz_submission_id)
        .first()
    )
    if quiz_submission is None:
        raise HTTPException(status_code=404, detail="Quiz submission not found")
    db.delete(quiz_submission)
    db.commit()
    return JSONResponse(
        content={
            "success": True,
            "detail": f"delete the quiz submission id {quiz_submission_id} successfully",
        },
        status_code=200,
    )
