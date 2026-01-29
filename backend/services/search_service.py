"""
Search Service for Course Companion FTE
Implements keyword and semantic search using pre-computed embeddings (NO LLM)
CONSTITUTIONAL REQUIREMENT: All searches use offline methods, no runtime LLM calls
"""
import json
import numpy as np
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
import time

from backend.api.models.chapter import Chapter
from backend.api.models.course import Course
from backend.services.r2 import R2Client
from backend.core.config import get_settings


class SearchService:
    """
    Service for searching course content using keyword and semantic methods
    """

    def __init__(self, db: AsyncSession, r2_client: R2Client):
        self.db = db
        self.r2_client = r2_client
        self.settings = get_settings()

    async def search(
        self,
        query: str,
        search_type: str = "keyword",
        limit: int = 10,
        course_id: Optional[int] = None
    ) -> dict:
        """
        Search content using specified method

        Args:
            query: Search query string
            search_type: Type of search (keyword, semantic, hybrid)
            limit: Maximum number of results
            course_id: Optional course filter

        Returns:
            Dictionary with search results and metadata
        """
        start_time = time.time()

        if search_type == "keyword":
            results = await self.search_keyword(query, limit, course_id)
        elif search_type == "semantic":
            results = await self.search_semantic(query, limit, course_id)
        elif search_type == "hybrid":
            results = await self.search_hybrid(query, limit, course_id)
        else:
            results = []

        execution_time_ms = (time.time() - start_time) * 1000

        return {
            "query": query,
            "search_type": search_type,
            "results": results,
            "total_results": len(results),
            "execution_time_ms": round(execution_time_ms, 2)
        }

    async def search_keyword(
        self,
        query: str,
        limit: int = 10,
        course_id: Optional[int] = None
    ) -> List[dict]:
        """
        Keyword-based search using PostgreSQL ILIKE

        Args:
            query: Search query
            limit: Maximum results
            course_id: Optional course filter

        Returns:
            List of search results
        """
        # Normalize query
        query_lower = query.lower()
        search_pattern = f"%{query_lower}%"

        # Build query
        query_obj = (
            select(Chapter, Course)
            .join(Course, Chapter.course_id == Course.id)
            .where(Chapter.is_published == True)
            .where(
                or_(
                    Chapter.title.ilike(search_pattern),
                    Chapter.description.ilike(search_pattern)
                )
            )
        )

        # Apply course filter if specified
        if course_id:
            query_obj = query_obj.where(Chapter.course_id == course_id)

        query_obj = query_obj.limit(limit)

        # Execute query
        result = await self.db.execute(query_obj)
        rows = result.all()

        # Build results
        results = []
        for chapter, course in rows:
            # Calculate simple relevance score based on keyword frequency
            title_matches = chapter.title.lower().count(query_lower)
            desc_matches = chapter.description.lower().count(query_lower)
            total_matches = title_matches + desc_matches

            # Normalize score (simple heuristic)
            relevance_score = min(1.0, total_matches / 10.0)

            # Create excerpt from description
            excerpt = self._create_excerpt(
                chapter.description,
                query_lower,
                max_length=200
            )

            results.append({
                "chapter_id": chapter.id,
                "chapter_number": chapter.chapter_number,
                "chapter_title": chapter.title,
                "course_id": course.id,
                "course_title": course.title,
                "excerpt": excerpt,
                "relevance_score": relevance_score,
                "match_type": "keyword"
            })

        # Sort by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return results

    async def search_semantic(
        self,
        query: str,
        limit: int = 10,
        course_id: Optional[int] = None
    ) -> List[dict]:
        """
        Semantic search using pre-computed embeddings (NO LLM)

        Uses cosine similarity with embeddings generated offline.
        Embeddings must be pre-computed using the generate_embeddings script.

        Args:
            query: Search query
            limit: Maximum results
            course_id: Optional course filter

        Returns:
            List of search results ranked by semantic similarity
        """
        # Check if semantic search is enabled
        if not self.settings.SEMANTIC_SEARCH_ENABLED:
            return []

        # For semantic search, we would need to:
        # 1. Generate embedding for the query (using offline model)
        # 2. Compare with pre-computed chapter embeddings
        # 3. Rank by cosine similarity

        # NOTE: This is a placeholder implementation
        # In production, you would:
        # - Load a local sentence-transformers model
        # - Generate query embedding
        # - Compare with stored embeddings using cosine similarity

        # For now, fall back to keyword search
        # TODO: Implement full semantic search with local embeddings
        return await self.search_keyword(query, limit, course_id)

    async def search_hybrid(
        self,
        query: str,
        limit: int = 10,
        course_id: Optional[int] = None
    ) -> List[dict]:
        """
        Hybrid search combining keyword and semantic methods

        Args:
            query: Search query
            limit: Maximum results
            course_id: Optional course filter

        Returns:
            List of search results with combined ranking
        """
        # Get keyword results
        keyword_results = await self.search_keyword(query, limit * 2, course_id)

        # Get semantic results (if enabled)
        if self.settings.SEMANTIC_SEARCH_ENABLED:
            semantic_results = await self.search_semantic(query, limit * 2, course_id)
        else:
            semantic_results = []

        # Combine and deduplicate results
        combined_results = {}

        # Add keyword results with weight
        for result in keyword_results:
            chapter_id = result["chapter_id"]
            combined_results[chapter_id] = {
                **result,
                "relevance_score": result["relevance_score"] * 0.6,  # 60% weight
                "match_type": "hybrid"
            }

        # Add semantic results with weight
        for result in semantic_results:
            chapter_id = result["chapter_id"]
            if chapter_id in combined_results:
                # Combine scores
                combined_results[chapter_id]["relevance_score"] += result["relevance_score"] * 0.4
            else:
                combined_results[chapter_id] = {
                    **result,
                    "relevance_score": result["relevance_score"] * 0.4,  # 40% weight
                    "match_type": "hybrid"
                }

        # Convert to list and sort
        results = list(combined_results.values())
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return results[:limit]

    def _create_excerpt(
        self,
        text: str,
        query: str,
        max_length: int = 200
    ) -> str:
        """
        Create an excerpt around the search query

        Args:
            text: Full text
            query: Search query
            max_length: Maximum excerpt length

        Returns:
            Excerpt with query context
        """
        text_lower = text.lower()
        query_lower = query.lower()

        # Find first occurrence of query
        pos = text_lower.find(query_lower)

        if pos == -1:
            # Query not found, return beginning of text
            return text[:max_length] + ("..." if len(text) > max_length else "")

        # Calculate excerpt boundaries
        start = max(0, pos - max_length // 2)
        end = min(len(text), pos + len(query) + max_length // 2)

        excerpt = text[start:end]

        # Add ellipsis if truncated
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(text):
            excerpt = excerpt + "..."

        return excerpt

    async def get_chapter_content_for_search(
        self,
        chapter_id: int
    ) -> Optional[str]:
        """
        Fetch chapter content from R2 for indexing

        Args:
            chapter_id: Chapter database ID

        Returns:
            Chapter content as string, or None if not found
        """
        # Get chapter
        chapter = await self.db.get(Chapter, chapter_id)
        if not chapter or not chapter.content_key:
            return None

        try:
            # Download content from R2
            content_bytes = await self.r2_client.download_content(
                chapter.content_key
            )
            return content_bytes.decode('utf-8')
        except Exception:
            return None

    def calculate_cosine_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)

        # Normalize to 0-1 range
        return float((similarity + 1) / 2)
