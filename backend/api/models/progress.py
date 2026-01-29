"""
Progress model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Progress(SQLModel, table=True):
    """
    Progress model - tracks user progress through course chapters.

    Tracks completion, reading time, and streaks.
    All calculations are deterministic (NO LLM).
    """
    __tablename__ = "progress"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    chapter_id: int = Field(foreign_key="chapters.id", index=True)

    # Completion tracking
    is_completed: bool = Field(default=False)
    completed_at: Optional[datetime] = Field(default=None)

    # Reading engagement
    time_spent_seconds: int = Field(default=0, ge=0)
    last_position: int = Field(default=0, ge=0)  # Character position for resume
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow)

    # Streak tracking (calculated server-side)
    current_streak: int = Field(default=0, ge=0)  # Days with activity
    longest_streak: int = Field(default=0, ge=0)
    last_activity_date: Optional[datetime] = Field(default=None)  # Date component only

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "chapter_id": 1,
                "is_completed": True,
                "completed_at": "2024-01-15T14:30:00Z",
                "time_spent_seconds": 1200,
                "last_position": 15000,
                "current_streak": 7,
                "longest_streak": 14
            }
        }
