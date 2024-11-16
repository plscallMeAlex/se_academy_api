from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

"""SCHEMAS FOR QUIZ"""
# Quiz Schemas


# Base schema for shared logic
class QuizBase(BaseModel):
    course_id: Optional[UUID]
    question: Optional[str]
    choices: Optional[list[str]]
    correct_answer: Optional[int]

    @field_validator("choices")
    def validate_choices(cls, v: list[str]):
        if len(v) < 2:
            raise ValueError("There must be at least 2 choices")
        return v

    @model_validator(mode="after")
    def validate_correct_answer(cls, values):
        correct_answer = values.correct_answer
        choices = values.choices

        if correct_answer is not None and choices is not None:
            if correct_answer < 0:
                raise ValueError("Correct answer index cannot be negative")
            elif correct_answer >= len(choices):
                raise ValueError("Correct answer index out of range")

        return values


# QuizCreate schema for creation
class QuizCreate(QuizBase):
    course_id: UUID
    question: str
    choices: list[str]
    correct_answer: int


# QuizUpdate schema for updates
class QuizUpdate(QuizBase):
    course_id: Optional[UUID] = None
    question: Optional[str] = None
    choices: Optional[list[str]] = None
    correct_answer: Optional[int] = None


# QuizDetail schema for getting details of the quiz
class QuizDetail(QuizBase):
    id: UUID
    course_id: UUID
    question: str
    choices: list[str]
    correct_answer: int

    class Config:
        from_attributes = True


# QuizResponse schema for response
class QuizResponse(BaseModel):
    question: str
    choices: list[str]

    class Config:
        from_attributes = True


# QuizSubmission schema for quiz submission
class QuizSubmission(BaseModel):
    user_id: UUID
    course_id: UUID
    quiz_answers: dict[str, int]
    scores: int


# QuizSubmissionDetail schema for getting details of the quiz submission
class QuizSubmissionDetail(QuizSubmission):
    id: UUID
    user_id: UUID
    course_id: UUID
    submitted_at: datetime

    class Config:
        from_attributes = True


# QuizSubmissionResponse schema for response
class QuizSubmissionResponse(BaseModel):
    quiz_answers: dict[str, int]
    scores: int

    class Config:
        from_attributes = True
