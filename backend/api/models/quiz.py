"""
Quiz model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Quiz(SQLModel, table=True):
    """
    Quiz model - represents a quiz associated with a chapter.

    Phase 1: Rule-based grading only (NO LLM).
    All questions have predefined answer keys.
    """
    __tablename__ = "quizzes"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: int = Field(foreign_key="chapters.id", index=True)

    # Quiz metadata
    title: str = Field(max_length=255)
    description: str = Field(max_length=500)
    difficulty: str = Field(default="medium", max_length=20)  # easy|medium|hard

    # Grading configuration
    passing_score: int = Field(default=70, ge=0, le=100)  # Percentage
    max_attempts: int = Field(default=5, ge=1)
    time_limit_minutes: Optional[int] = Field(default=None, ge=1)  # None = unlimited

    # Freemium gate
    requires_premium: bool = Field(default=False)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = Field(default=True)

    class Config:
        json_schema_extra = {
            "example": {
                "chapter_id": 1,
                "title": "Chapter 1 Quiz: Introduction to AI Agents",
                "description": "Test your understanding of AI agent basics",
                "difficulty": "medium",
                "passing_score": 70,
                "max_attempts": 5,
                "time_limit_minutes": 30,
                "requires_premium": False
            }
        }


class Question(SQLModel, table=True):
    """
    Question model - represents a quiz question.

    Phase 1: Supports multiple choice, true/false, fill-in-blank.
    All answers are graded using predefined rules (NO LLM).
    """
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)

    # Question details
    question_number: int = Field(ge=1)  # Order within quiz
    question_text: str = Field(max_length=1000)
    question_type: str = Field(max_length=20)  # multiple_choice|true_false|fill_in_blank

    # Answer configuration (JSON serialized)
    # For multiple_choice: {"options": ["A", "B", "C", "D"], "correct": "A"}
    # For true_false: {"correct": true}
    # For fill_in_blank: {"correct": ["answer1", "answer2"], "case_sensitive": false}
    answer_config: str = Field()  # JSON string

    # Grading rules for fill-in-blank
    case_sensitive: bool = Field(default=False)
    trim_whitespace: bool = Field(default=True)
    allow_partial: bool = Field(default=False)  # Accept any of multiple correct answers

    # Points
    points: int = Field(default=1, ge=1)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_number": 1,
                "question_text": "What is an AI agent?",
                "question_type": "multiple_choice",
                "answer_config": '{"options": ["A program that uses AI", "A human operator", "A database"], "correct": "A program that uses AI"}',
                "points": 1
            }
        }
