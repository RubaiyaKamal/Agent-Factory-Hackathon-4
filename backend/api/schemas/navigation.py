"""
Navigation schemas for Course Companion FTE
Request/response models for chapter navigation and course structure
"""
from typing import Optional, List
from pydantic import BaseModel, Field

from backend.api.schemas.content import ChapterListItem, ChapterResponse


class ChapterNavigation(BaseModel):
    """
    Response model for chapter navigation
    Includes current chapter with previous/next chapter information
    """
    current: ChapterResponse
    next: Optional[ChapterResponse] = Field(
        default=None,
        description="Next chapter in sequence (null if current is last chapter)"
    )
    previous: Optional[ChapterResponse] = Field(
        default=None,
        description="Previous chapter in sequence (null if current is first chapter)"
    )
    course_progress_percentage: float = Field(
        description="User's progress through the course as percentage"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "current": {
                    "id": 2,
                    "course_id": 1,
                    "chapter_number": 2,
                    "title": "Claude SDK Basics",
                    "content_url": "https://...",
                    "estimated_minutes": 20,
                    "requires_premium": False
                },
                "next": {
                    "id": 3,
                    "chapter_number": 3,
                    "title": "MCP Servers",
                    "estimated_minutes": 25
                },
                "previous": {
                    "id": 1,
                    "chapter_number": 1,
                    "title": "Introduction to AI Agents",
                    "estimated_minutes": 15
                },
                "course_progress_percentage": 40.0
            }
        }


class ChapterWithProgress(ChapterListItem):
    """
    Extended chapter list item with detailed progress information
    """
    description: str
    time_spent_seconds: Optional[int] = Field(
        default=None,
        description="Time user has spent on this chapter"
    )
    completed_at: Optional[str] = Field(
        default=None,
        description="ISO timestamp when chapter was completed"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "chapter_number": 1,
                "slug": "chapter-1-introduction",
                "title": "Introduction to AI Agents",
                "description": "Learn what AI agents are and how they work",
                "estimated_minutes": 15,
                "requires_premium": False,
                "is_completed": True,
                "time_spent_seconds": 1200,
                "completed_at": "2024-01-15T14:30:00Z"
            }
        }


class ProgressSummary(BaseModel):
    """
    Summary of user's progress through a course
    """
    completed_chapters: int
    total_chapters: int
    progress_percentage: float
    current_streak: int = Field(description="Days of consecutive activity")
    longest_streak: int = Field(description="Longest streak achieved")
    total_time_spent_seconds: int = Field(description="Total time spent in course")

    class Config:
        json_schema_extra = {
            "example": {
                "completed_chapters": 3,
                "total_chapters": 5,
                "progress_percentage": 60.0,
                "current_streak": 7,
                "longest_streak": 14,
                "total_time_spent_seconds": 5400
            }
        }


class CourseStructure(BaseModel):
    """
    Complete course structure with chapters and user progress
    """
    course_id: int
    course_title: str
    course_slug: str
    total_chapters: int
    free_chapter_limit: int
    chapters: List[ChapterWithProgress] = Field(
        description="All chapters with progress information"
    )
    user_progress: ProgressSummary

    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 1,
                "course_title": "AI Agent Development",
                "course_slug": "ai-agent-development",
                "total_chapters": 5,
                "free_chapter_limit": 3,
                "chapters": [
                    {
                        "id": 1,
                        "chapter_number": 1,
                        "slug": "chapter-1-introduction",
                        "title": "Introduction",
                        "description": "Learn about AI agents",
                        "estimated_minutes": 15,
                        "requires_premium": False,
                        "is_completed": True,
                        "time_spent_seconds": 1200
                    }
                ],
                "user_progress": {
                    "completed_chapters": 3,
                    "total_chapters": 5,
                    "progress_percentage": 60.0,
                    "current_streak": 7,
                    "longest_streak": 14,
                    "total_time_spent_seconds": 5400
                }
            }
        }
