"""
Quiz Attempt model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class QuizAttempt(SQLModel, table=True):
    """
    Quiz Attempt model - tracks user attempts at quizzes.

    Phase 1: All grading is rule-based (NO LLM).
    """
    __tablename__ = "quiz_attempts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)

    # Attempt tracking
    attempt_number: int = Field(ge=1)  # 1st attempt, 2nd attempt, etc.

    # Answers (JSON serialized)
    # Format: {"1": "A", "2": "true", "3": "machine learning"}
    # Keys are question_numbers, values are user answers
    answers: str = Field()  # JSON string

    # Grading results (computed by backend using answer keys)
    score: int = Field(ge=0, le=100)  # Percentage
    correct_count: int = Field(ge=0)
    total_questions: int = Field(ge=1)
    passed: bool = Field(default=False)

    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    submitted_at: Optional[datetime] = Field(default=None)
    time_taken_seconds: Optional[int] = Field(default=None, ge=0)

    # Detailed feedback (JSON serialized)
    # Format: {"1": {"correct": true, "explanation": "..."}, ...}
    feedback: Optional[str] = Field(default=None)  # JSON string

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "quiz_id": 1,
                "attempt_number": 1,
                "answers": '{"1": "A program that uses AI", "2": "true", "3": "machine learning"}',
                "score": 85,
                "correct_count": 17,
                "total_questions": 20,
                "passed": True,
                "time_taken_seconds": 1200
            }
        }
