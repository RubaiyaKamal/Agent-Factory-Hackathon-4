"""
Chapter model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Chapter(SQLModel, table=True):
    """
    Chapter model - represents a chapter within a course.

    Chapter content is stored in R2, this model stores metadata and navigation.
    Embeddings are pre-computed for semantic search (no runtime LLM).
    """
    __tablename__ = "chapters"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    chapter_number: int = Field(ge=1)  # 1-indexed chapter number
    slug: str = Field(max_length=100, index=True)  # chapter-1-introduction

    # Content metadata
    title: str = Field(max_length=255)
    description: str = Field(max_length=500)
    content_key: str = Field(max_length=255)  # R2 object key (e.g., "ai-agent-dev/chapter-1.md")

    # Navigation
    previous_chapter_id: Optional[int] = Field(default=None, foreign_key="chapters.id")
    next_chapter_id: Optional[int] = Field(default=None, foreign_key="chapters.id")

    # Content details
    estimated_minutes: int = Field(default=0)  # Reading time estimate
    word_count: int = Field(default=0)

    # Freemium gate
    requires_premium: bool = Field(default=False)  # True if beyond free tier limit

    # Semantic search support (Phase 1: Pre-computed embeddings, NO LLM)
    # Embeddings stored as JSON array of floats
    embedding: Optional[str] = Field(default=None)  # JSON serialized numpy array

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = Field(default=True)

    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 1,
                "chapter_number": 1,
                "slug": "chapter-1-introduction",
                "title": "Introduction to AI Agents",
                "description": "Learn what AI agents are and how they work",
                "content_key": "ai-agent-dev/chapter-1-introduction.md",
                "estimated_minutes": 15,
                "word_count": 1500,
                "requires_premium": False
            }
        }
