"""
Content Service for Course Companion FTE
Handles course and chapter retrieval with R2 integration
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from backend.api.models.course import Course
from backend.api.models.chapter import Chapter
from backend.api.models.progress import Progress
from backend.api.models.user import User
from backend.services.r2 import R2Client
from backend.core.config import get_settings


class ContentService:
    """
    Service for managing course and chapter content delivery
    """

    def __init__(self, db: AsyncSession, r2_client: R2Client):
        self.db = db
        self.r2_client = r2_client
        self.settings = get_settings()

    async def list_courses(
        self,
        user: Optional[User] = None,
        published_only: bool = True
    ) -> List[Course]:
        """
        List all available courses

        Args:
            user: Optional authenticated user for filtering
            published_only: Only return published courses

        Returns:
            List of Course objects
        """
        query = select(Course)

        if published_only:
            query = query.where(Course.is_published == True)

        result = await self.db.execute(query)
        courses = result.scalars().all()

        return list(courses)

    async def get_course_by_id(self, course_id: int) -> Course:
        """
        Get course by ID

        Args:
            course_id: Course database ID

        Returns:
            Course object

        Raises:
            HTTPException: If course not found
        """
        course = await self.db.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )

        if not course.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} is not published"
            )

        return course

    async def get_course_by_slug(self, slug: str) -> Course:
        """
        Get course by slug

        Args:
            slug: Course slug (e.g., 'ai-agent-development')

        Returns:
            Course object

        Raises:
            HTTPException: If course not found
        """
        query = select(Course).where(Course.slug == slug)
        result = await self.db.execute(query)
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course '{slug}' not found"
            )

        if not course.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course '{slug}' is not published"
            )

        return course

    async def get_course_chapters(
        self,
        course_id: int,
        user: Optional[User] = None
    ) -> List[Chapter]:
        """
        Get all chapters for a course

        Args:
            course_id: Course database ID
            user: Optional authenticated user for progress tracking

        Returns:
            List of Chapter objects ordered by chapter_number
        """
        query = (
            select(Chapter)
            .where(Chapter.course_id == course_id)
            .where(Chapter.is_published == True)
            .order_by(Chapter.chapter_number)
        )

        result = await self.db.execute(query)
        chapters = result.scalars().all()

        return list(chapters)

    async def get_chapter_by_id(self, chapter_id: int) -> Chapter:
        """
        Get chapter by ID

        Args:
            chapter_id: Chapter database ID

        Returns:
            Chapter object

        Raises:
            HTTPException: If chapter not found
        """
        chapter = await self.db.get(Chapter, chapter_id)

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter with ID {chapter_id} not found"
            )

        if not chapter.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter with ID {chapter_id} is not published"
            )

        return chapter

    async def generate_content_url(
        self,
        chapter: Chapter,
        expiry_minutes: Optional[int] = None
    ) -> str:
        """
        Generate signed R2 URL for chapter content

        Args:
            chapter: Chapter object
            expiry_minutes: URL expiration time (default: from settings)

        Returns:
            Signed URL for accessing chapter content

        Raises:
            HTTPException: If URL generation fails
        """
        if not expiry_minutes:
            expiry_minutes = self.settings.R2_SIGNED_URL_EXPIRY // 60

        try:
            signed_url = await self.r2_client.generate_signed_url(
                key=chapter.content_key,
                expiry_minutes=expiry_minutes
            )

            return signed_url

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate content URL: {str(e)}"
            )

    async def check_chapter_progress(
        self,
        user_id: int,
        chapter_id: int
    ) -> Optional[Progress]:
        """
        Check user's progress for a chapter

        Args:
            user_id: User database ID
            chapter_id: Chapter database ID

        Returns:
            Progress object if exists, None otherwise
        """
        query = (
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.chapter_id == chapter_id)
        )

        result = await self.db.execute(query)
        progress = result.scalar_one_or_none()

        return progress

    async def get_user_course_progress(
        self,
        user_id: int,
        course_id: int
    ) -> dict:
        """
        Calculate user's progress for a course

        Args:
            user_id: User database ID
            course_id: Course database ID

        Returns:
            Dictionary with progress statistics
        """
        # Get all chapters for the course
        chapters = await self.get_course_chapters(course_id)
        total_chapters = len(chapters)

        # Get user's completed chapters
        chapter_ids = [ch.id for ch in chapters]
        query = (
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.chapter_id.in_(chapter_ids))
            .where(Progress.is_completed == True)
        )

        result = await self.db.execute(query)
        completed_progress = result.scalars().all()
        completed_chapters = len(completed_progress)

        progress_percentage = (
            (completed_chapters / total_chapters * 100)
            if total_chapters > 0 else 0
        )

        return {
            "completed_chapters": completed_chapters,
            "total_chapters": total_chapters,
            "progress_percentage": round(progress_percentage, 2)
        }
