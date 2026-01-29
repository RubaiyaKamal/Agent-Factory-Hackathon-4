"""
Quiz schemas for Course Companion FTE
Request/response models for quiz delivery and grading
"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class QuestionResponse(BaseModel):
    """
    Response model for a quiz question (without correct answer)
    """
    id: int
    question_number: int
    question_text: str
    question_type: str = Field(description="multiple_choice | true_false | fill_in_blank")
    options: Optional[List[str]] = Field(
        default=None,
        description="Available options for multiple choice questions"
    )
    points: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "question_number": 1,
                "question_text": "What is the primary purpose of the Claude Agent SDK?",
                "question_type": "multiple_choice",
                "options": [
                    "To generate images",
                    "To build AI agents with natural language capabilities",
                    "To manage databases",
                    "To create web applications"
                ],
                "points": 10
            }
        }


class QuizResponse(BaseModel):
    """
    Response model for a complete quiz (without answers)
    """
    id: int
    chapter_id: int
    title: str
    description: str
    difficulty: str
    passing_score: int
    max_attempts: int
    time_limit_minutes: Optional[int]
    requires_premium: bool
    questions: List[QuestionResponse]
    total_points: int
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "chapter_id": 1,
                "title": "Introduction to AI Agents - Quiz",
                "description": "Test your understanding of AI agent basics",
                "difficulty": "medium",
                "passing_score": 70,
                "max_attempts": 5,
                "time_limit_minutes": 30,
                "requires_premium": False,
                "questions": [],
                "total_points": 100,
                "created_at": "2024-01-15T14:30:00Z"
            }
        }


class SubmitQuizRequest(BaseModel):
    """
    Request model for submitting quiz answers
    """
    answers: Dict[int, str] = Field(
        description="Map of question_id to user's answer"
    )
    time_taken_seconds: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "answers": {
                    "1": "To build AI agents with natural language capabilities",
                    "2": "true",
                    "3": "Model Context Protocol"
                },
                "time_taken_seconds": 1200
            }
        }


class QuestionFeedback(BaseModel):
    """
    Feedback for a single question
    """
    question_id: int
    question_number: int
    user_answer: str
    is_correct: bool
    correct_answer: Optional[str] = Field(
        default=None,
        description="Correct answer (only shown after submission)"
    )
    explanation: Optional[str] = None
    points_earned: int
    points_possible: int

    class Config:
        json_schema_extra = {
            "example": {
                "question_id": 1,
                "question_number": 1,
                "user_answer": "To build AI agents with natural language capabilities",
                "is_correct": True,
                "correct_answer": "To build AI agents with natural language capabilities",
                "explanation": "Correct! The Claude SDK is designed specifically for building AI agents.",
                "points_earned": 10,
                "points_possible": 10
            }
        }


class QuizResultResponse(BaseModel):
    """
    Response model for quiz results
    """
    quiz_attempt_id: int
    quiz_id: int
    quiz_title: str
    attempt_number: int
    score: int = Field(description="Score as percentage (0-100)")
    points_earned: int
    total_points: int
    correct_count: int
    total_questions: int
    passed: bool
    time_taken_seconds: Optional[int]
    feedback: List[QuestionFeedback]
    submitted_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_attempt_id": 1,
                "quiz_id": 1,
                "quiz_title": "Introduction to AI Agents - Quiz",
                "attempt_number": 1,
                "score": 85,
                "points_earned": 85,
                "total_points": 100,
                "correct_count": 17,
                "total_questions": 20,
                "passed": True,
                "time_taken_seconds": 1200,
                "feedback": [],
                "submitted_at": "2024-01-15T15:00:00Z"
            }
        }


class QuizAttemptSummary(BaseModel):
    """
    Summary of a quiz attempt (for history view)
    """
    attempt_id: int
    attempt_number: int
    score: int
    passed: bool
    submitted_at: datetime
    time_taken_seconds: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "attempt_id": 1,
                "attempt_number": 1,
                "score": 85,
                "passed": True,
                "submitted_at": "2024-01-15T15:00:00Z",
                "time_taken_seconds": 1200
            }
        }


class QuizHistoryResponse(BaseModel):
    """
    Response model for user's quiz history
    """
    quiz_id: int
    quiz_title: str
    attempts: List[QuizAttemptSummary]
    best_score: int
    attempts_remaining: int
    max_attempts: int

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "quiz_title": "Introduction to AI Agents - Quiz",
                "attempts": [],
                "best_score": 85,
                "attempts_remaining": 4,
                "max_attempts": 5
            }
        }
