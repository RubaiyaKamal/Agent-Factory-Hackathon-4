"""
Achievement model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Achievement(SQLModel, table=True):
    """
    Achievement model - tracks user achievements and milestones.

    Achievements are awarded based on deterministic rules (NO LLM):
    - First chapter completion
    - Course 50% completion
    - Course 100% completion
    - Quiz perfect score
    - Streak milestones (7 days, 30 days)
    """
    __tablename__ = "achievements"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Achievement details
    achievement_type: str = Field(max_length=50, index=True)  # first_chapter, halfway_hero, etc.
    achievement_name: str = Field(max_length=100)
    achievement_description: str = Field(max_length=255)

    # Context (optional - what triggered the achievement)
    context_course_id: Optional[int] = Field(default=None, foreign_key="courses.id")
    context_chapter_id: Optional[int] = Field(default=None, foreign_key="chapters.id")
    context_quiz_id: Optional[int] = Field(default=None, foreign_key="quizzes.id")

    # Metadata
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    is_notified: bool = Field(default=False)  # Whether user has been notified

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "achievement_type": "first_chapter",
                "achievement_name": "First Steps",
                "achievement_description": "Completed your first chapter!",
                "context_course_id": 1,
                "context_chapter_id": 1,
                "earned_at": "2024-01-15T14:30:00Z"
            }
        }
