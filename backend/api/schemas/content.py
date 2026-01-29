"""
Content schemas for Course Companion FTE
Request/response models for course and chapter content delivery
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ChapterResponse(BaseModel):
    """
    Response model for chapter information
    Includes signed R2 URL for content access
    """
    id: int
    course_id: int
    chapter_number: int
    slug: str
    title: str
    description: str
    content_url: str = Field(description="Signed R2 URL for chapter content (60-minute expiry)")
    estimated_minutes: int = Field(description="Estimated reading time in minutes")
    word_count: int
    requires_premium: bool
    previous_chapter_id: Optional[int] = None
    next_chapter_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    is_published: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "course_id": 1,
                "chapter_number": 1,
                "slug": "chapter-1-introduction",
                "title": "Introduction to AI Agents",
                "description": "Learn what AI agents are and how they work",
                "content_url": "https://signed-url.r2.cloudflarestorage.com/...",
                "estimated_minutes": 15,
                "word_count": 1500,
                "requires_premium": False,
                "previous_chapter_id": None,
                "next_chapter_id": 2,
                "created_at": "2024-01-15T14:30:00Z",
                "updated_at": "2024-01-15T14:30:00Z",
                "is_published": True
            }
        }


class ChapterListItem(BaseModel):
    """
    Simplified chapter model for list views
    """
    id: int
    chapter_number: int
    slug: str
    title: str
    estimated_minutes: int
    requires_premium: bool
    is_completed: Optional[bool] = Field(
        default=None,
        description="User's completion status (null if no progress tracking)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "chapter_number": 1,
                "slug": "chapter-1-introduction",
                "title": "Introduction to AI Agents",
                "estimated_minutes": 15,
                "requires_premium": False,
                "is_completed": True
            }
        }


class CourseResponse(BaseModel):
    """
    Response model for course information
    """
    id: int
    slug: str
    title: str
    description: str
    total_chapters: int
    estimated_hours: int
    difficulty_level: str = Field(description="beginner|intermediate|advanced")
    free_chapter_limit: int = Field(description="Number of chapters accessible to free users")
    required_tier: str = Field(description="Minimum tier required for access")
    is_published: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "slug": "ai-agent-development",
                "title": "AI Agent Development with Claude & ChatGPT",
                "description": "Learn to build intelligent agents using modern LLM APIs, MCP servers, and agent skills",
                "total_chapters": 5,
                "estimated_hours": 8,
                "difficulty_level": "intermediate",
                "free_chapter_limit": 3,
                "required_tier": "free",
                "is_published": True,
                "published_at": "2024-01-01T00:00:00Z",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T14:30:00Z"
            }
        }


class CourseDetailResponse(CourseResponse):
    """
    Extended course response with chapter list
    """
    chapters: List[ChapterListItem] = Field(description="List of all chapters in the course")
    user_progress: Optional[dict] = Field(
        default=None,
        description="User's progress summary (null if not authenticated)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "slug": "ai-agent-development",
                "title": "AI Agent Development with Claude & ChatGPT",
                "description": "Learn to build intelligent agents using modern LLM APIs",
                "total_chapters": 5,
                "estimated_hours": 8,
                "difficulty_level": "intermediate",
                "free_chapter_limit": 3,
                "required_tier": "free",
                "is_published": True,
                "chapters": [
                    {
                        "id": 1,
                        "chapter_number": 1,
                        "slug": "chapter-1-introduction",
                        "title": "Introduction to AI Agents",
                        "estimated_minutes": 15,
                        "requires_premium": False,
                        "is_completed": True
                    }
                ],
                "user_progress": {
                    "completed_chapters": 3,
                    "total_chapters": 5,
                    "progress_percentage": 60.0
                }
            }
        }


class CourseListResponse(BaseModel):
    """
    Response model for list of courses
    """
    courses: List[CourseResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "courses": [
                    {
                        "id": 1,
                        "slug": "ai-agent-development",
                        "title": "AI Agent Development",
                        "description": "Build AI agents with modern LLMs",
                        "total_chapters": 5,
                        "estimated_hours": 8,
                        "difficulty_level": "intermediate",
                        "free_chapter_limit": 3,
                        "required_tier": "free",
                        "is_published": True
                    }
                ],
                "total": 1
            }
        }
