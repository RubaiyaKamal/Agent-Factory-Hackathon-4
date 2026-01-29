"""
Progress schemas for Course Companion FTE
Request/response models for progress tracking and streaks
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MarkChapterCompleteRequest(BaseModel):
    """
    Request to mark a chapter as complete
    """
    time_spent_seconds: Optional[int] = Field(
        default=None,
        ge=0,
        description="Time spent on chapter in seconds"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "time_spent_seconds": 1200
            }
        }


class ChapterProgressResponse(BaseModel):
    """
    Response for chapter progress
    """
    chapter_id: int
    chapter_title: str
    is_completed: bool
    completed_at: Optional[datetime]
    time_spent_seconds: int
    last_accessed_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "chapter_id": 1,
                "chapter_title": "Introduction to AI Agents",
                "is_completed": True,
                "completed_at": "2024-01-15T14:30:00Z",
                "time_spent_seconds": 1200,
                "last_accessed_at": "2024-01-15T14:30:00Z"
            }
        }


class StreakInfo(BaseModel):
    """
    Information about user's learning streak
    """
    current_streak: int = Field(description="Current consecutive days with activity")
    longest_streak: int = Field(description="Longest streak ever achieved")
    last_activity_date: Optional[datetime]
    streak_status: str = Field(description="active | at_risk | broken")
    days_until_broken: Optional[int] = Field(
        default=None,
        description="Days remaining before streak breaks (with grace period)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "current_streak": 7,
                "longest_streak": 14,
                "last_activity_date": "2024-01-15T14:30:00Z",
                "streak_status": "active",
                "days_until_broken": 1
            }
        }


class CourseProgressSummary(BaseModel):
    """
    Summary of progress for a single course
    """
    course_id: int
    course_title: str
    course_slug: str
    completed_chapters: int
    total_chapters: int
    progress_percentage: float
    time_spent_seconds: int
    last_accessed: Optional[datetime]

    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 1,
                "course_title": "AI Agent Development",
                "course_slug": "ai-agent-development",
                "completed_chapters": 3,
                "total_chapters": 5,
                "progress_percentage": 60.0,
                "time_spent_seconds": 3600,
                "last_accessed": "2024-01-15T14:30:00Z"
            }
        }


class OverallProgressResponse(BaseModel):
    """
    Overall progress across all courses
    """
    user_id: int
    total_chapters_completed: int
    total_time_spent_seconds: int
    courses: List[CourseProgressSummary]
    streak: StreakInfo
    achievements_earned: int

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "total_chapters_completed": 3,
                "total_time_spent_seconds": 3600,
                "courses": [],
                "streak": {
                    "current_streak": 7,
                    "longest_streak": 14,
                    "streak_status": "active"
                },
                "achievements_earned": 2
            }
        }


class StatsResponse(BaseModel):
    """
    Detailed user statistics
    """
    total_chapters_completed: int
    total_quizzes_taken: int
    total_quizzes_passed: int
    average_quiz_score: float
    total_time_spent_seconds: int
    total_time_spent_hours: float
    account_created_at: datetime
    days_since_signup: int
    streak: StreakInfo

    class Config:
        json_schema_extra = {
            "example": {
                "total_chapters_completed": 3,
                "total_quizzes_taken": 5,
                "total_quizzes_passed": 4,
                "average_quiz_score": 85.5,
                "total_time_spent_seconds": 7200,
                "total_time_spent_hours": 2.0,
                "account_created_at": "2024-01-01T00:00:00Z",
                "days_since_signup": 15,
                "streak": {
                    "current_streak": 7,
                    "longest_streak": 14,
                    "streak_status": "active"
                }
            }
        }
