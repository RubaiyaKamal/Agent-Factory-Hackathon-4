"""
Search routes for Course Companion FTE
Handles content search (keyword, semantic, and hybrid)
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.search import SearchRequest, SearchResponse, SearchResult
from backend.api.models.user import User
from backend.db.session import get_db_session
from backend.services.search_service import SearchService
from backend.services.r2 import get_r2_client, R2Client
from backend.api.middleware.auth import get_current_user_optional


router = APIRouter(prefix="/search", tags=["search"])


def get_search_service(
    db: AsyncSession = Depends(get_db_session),
    r2_client: R2Client = Depends(get_r2_client)
) -> SearchService:
    """
    Dependency to provide SearchService instance
    """
    return SearchService(db=db, r2_client=r2_client)


@router.get("", response_model=SearchResponse)
async def search_content(
    query: str = Query(..., min_length=3, description="Search query (min 3 characters)"),
    search_type: str = Query(
        default="keyword",
        description="Search type: keyword | semantic | hybrid"
    ),
    limit: int = Query(default=10, ge=1, le=50, description="Max results"),
    course_id: Optional[int] = Query(default=None, description="Filter by course ID"),
    service: SearchService = Depends(get_search_service),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> SearchResponse:
    """
    Search course content

    Supports three search types:
    - **keyword**: Fast text-based search using PostgreSQL ILIKE
    - **semantic**: Similarity-based search using pre-computed embeddings (requires embeddings)
    - **hybrid**: Combination of keyword and semantic (weighted)

    Authentication is optional. Results are filtered based on user's access level.

    ### Search Types

    **Keyword Search** (default):
    - Fast and simple
    - Searches chapter titles and descriptions
    - Uses PostgreSQL pattern matching
    - Good for exact term matches

    **Semantic Search**:
    - Understands meaning and context
    - Uses pre-computed embeddings (no runtime LLM calls)
    - Requires `generate_embeddings.py` to be run first
    - Good for conceptual queries

    **Hybrid Search**:
    - Combines keyword (60%) and semantic (40%)
    - Best of both approaches
    - Recommended for most use cases

    Args:
        query: Search query (minimum 3 characters)
        search_type: Type of search (keyword, semantic, or hybrid)
        limit: Maximum number of results (1-50)
        course_id: Optional filter to specific course
        current_user: Optional authenticated user

    Returns:
        SearchResponse with results ranked by relevance

    Examples:
        ```
        GET /api/search?query=Claude%20SDK&search_type=keyword&limit=10
        GET /api/search?query=MCP%20servers&search_type=semantic
        GET /api/search?query=AI%20agents&search_type=hybrid&course_id=1
        ```
    """
    # Validate search type
    valid_types = ["keyword", "semantic", "hybrid"]
    if search_type not in valid_types:
        search_type = "keyword"

    # Perform search
    result = await service.search(
        query=query,
        search_type=search_type,
        limit=limit,
        course_id=course_id
    )

    # Build response
    search_results = [SearchResult(**item) for item in result["results"]]

    return SearchResponse(
        query=result["query"],
        search_type=result["search_type"],
        results=search_results,
        total_results=result["total_results"],
        execution_time_ms=result["execution_time_ms"]
    )
