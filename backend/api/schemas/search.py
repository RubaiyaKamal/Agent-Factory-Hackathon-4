"""
Search schemas for Course Companion FTE
Request/response models for content search (keyword and semantic)
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """
    Request model for content search
    """
    query: str = Field(min_length=3, description="Search query (minimum 3 characters)")
    search_type: str = Field(
        default="keyword",
        description="Type of search: keyword | semantic | hybrid"
    )
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of results")
    course_id: Optional[int] = Field(
        default=None,
        description="Filter results to specific course"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Claude SDK",
                "search_type": "keyword",
                "limit": 10,
                "course_id": 1
            }
        }


class SearchResult(BaseModel):
    """
    Single search result
    """
    chapter_id: int
    chapter_number: int
    chapter_title: str
    course_id: int
    course_title: str
    excerpt: str = Field(description="Relevant excerpt from content")
    relevance_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Relevance score (0.0 to 1.0)"
    )
    match_type: str = Field(description="keyword | semantic | hybrid")

    class Config:
        json_schema_extra = {
            "example": {
                "chapter_id": 2,
                "chapter_number": 2,
                "chapter_title": "Claude SDK Basics",
                "course_id": 1,
                "course_title": "AI Agent Development",
                "excerpt": "The Claude SDK by Anthropic provides a powerful foundation for building AI agents...",
                "relevance_score": 0.95,
                "match_type": "keyword"
            }
        }


class SearchResponse(BaseModel):
    """
    Response model for search results
    """
    query: str
    search_type: str
    results: List[SearchResult]
    total_results: int
    execution_time_ms: float

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Claude SDK",
                "search_type": "keyword",
                "results": [],
                "total_results": 5,
                "execution_time_ms": 42.5
            }
        }
