"""
Course model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Course(SQLModel, table=True):
    """
    Course model - represents an educational course with multiple chapters.

    Courses are stored in R2, this model stores metadata and configuration.
    """
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True, max_length=100)  # ai-agent-dev, python-basics
    title: str = Field(max_length=255)
    description: str = Field(max_length=1000)

    # Freemium configuration
    free_chapter_limit: int = Field(default=3)  # First N chapters free
    required_tier: str = Field(default="free", max_length=20)  # Minimum tier required

    # Content metadata
    total_chapters: int = Field(default=0)
    estimated_hours: int = Field(default=0)  # Total course duration estimate
    difficulty_level: str = Field(default="intermediate", max_length=20)  # beginner|intermediate|advanced

    # Course status
    is_published: bool = Field(default=False)
    published_at: Optional[datetime] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "slug": "ai-agent-development",
                "title": "AI Agent Development with Claude & ChatGPT",
                "description": "Learn to build intelligent agents using modern LLM APIs",
                "free_chapter_limit": 3,
                "required_tier": "free",
                "total_chapters": 12,
                "estimated_hours": 24,
                "difficulty_level": "intermediate"
            }
        }
