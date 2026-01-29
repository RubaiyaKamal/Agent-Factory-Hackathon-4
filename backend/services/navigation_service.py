"""
Navigation Service for Course Companion FTE
Handles chapter navigation and course structure retrieval
"""
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from backend.api.models.chapter import Chapter
from backend.api.models.course import Course
from backend.api.models.progress import Progress
from backend.api.models.user import User


class NavigationService:
    """
    Service for managing chapter navigation and course structure
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_next_chapter(self, current_chapter_id: int) -> Optional[Chapter]:
        """
        Get the next chapter in sequence

        Args:
            current_chapter_id: Current chapter database ID

        Returns:
            Next Chapter object or None if current is last chapter
        """
        # Get current chapter
        current_chapter = await self.db.get(Chapter, current_chapter_id)
        if not current_chapter:
            return None

        # If next_chapter_id is set, use it
        if current_chapter.next_chapter_id:
            next_chapter = await self.db.get(Chapter, current_chapter.next_chapter_id)
            if next_chapter and next_chapter.is_published:
                return next_chapter

        # Otherwise, find next by chapter_number
        query = (
            select(Chapter)
            .where(Chapter.course_id == current_chapter.course_id)
            .where(Chapter.chapter_number > current_chapter.chapter_number)
            .where(Chapter.is_published == True)
            .order_by(Chapter.chapter_number.asc())
            .limit(1)
        )

        result = await self.db.execute(query)
        next_chapter = result.scalar_one_or_none()

        return next_chapter

    async def get_previous_chapter(self, current_chapter_id: int) -> Optional[Chapter]:
        """
        Get the previous chapter in sequence

        Args:
            current_chapter_id: Current chapter database ID

        Returns:
            Previous Chapter object or None if current is first chapter
        """
        # Get current chapter
        current_chapter = await self.db.get(Chapter, current_chapter_id)
        if not current_chapter:
            return None

        # If previous_chapter_id is set, use it
        if current_chapter.previous_chapter_id:
            prev_chapter = await self.db.get(Chapter, current_chapter.previous_chapter_id)
            if prev_chapter and prev_chapter.is_published:
                return prev_chapter

        # Otherwise, find previous by chapter_number
        query = (
            select(Chapter)
            .where(Chapter.course_id == current_chapter.course_id)
            .where(Chapter.chapter_number < current_chapter.chapter_number)
            .where(Chapter.is_published == True)
            .order_by(Chapter.chapter_number.desc())
            .limit(1)
        )

        result = await self.db.execute(query)
        prev_chapter = result.scalar_one_or_none()

        return prev_chapter

    async def get_chapter_navigation(
        self,
        chapter_id: int,
        user: Optional[User] = None
    ) -> Tuple[Chapter, Optional[Chapter], Optional[Chapter], float]:
        """
        Get navigation info for a chapter (current, next, previous, progress)

        Args:
            chapter_id: Chapter database ID
            user: Optional authenticated user for progress tracking

        Returns:
            Tuple of (current_chapter, next_chapter, previous_chapter, progress_percentage)

        Raises:
            HTTPException: If chapter not found
        """
        # Get current chapter
        current_chapter = await self.db.get(Chapter, chapter_id)
        if not current_chapter or not current_chapter.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter with ID {chapter_id} not found"
            )

        # Get next and previous chapters
        next_chapter = await self.get_next_chapter(chapter_id)
        previous_chapter = await self.get_previous_chapter(chapter_id)

        # Calculate progress percentage
        progress_percentage = 0.0
        if user:
            progress_percentage = await self._calculate_course_progress(
                user_id=user.id,
                course_id=current_chapter.course_id
            )

        return current_chapter, next_chapter, previous_chapter, progress_percentage

    async def get_course_structure(
        self,
        course_id: int,
        user_id: int
    ) -> dict:
        """
        Get complete course structure with user progress

        Args:
            course_id: Course database ID
            user_id: User database ID

        Returns:
            Dictionary with course structure and progress

        Raises:
            HTTPException: If course not found
        """
        # Get course
        course = await self.db.get(Course, course_id)
        if not course or not course.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )

        # Get all chapters for the course
        query = (
            select(Chapter)
            .where(Chapter.course_id == course_id)
            .where(Chapter.is_published == True)
            .order_by(Chapter.chapter_number)
        )
        result = await self.db.execute(query)
        chapters = result.scalars().all()

        # Get user's progress for all chapters
        chapter_ids = [ch.id for ch in chapters]
        progress_query = (
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.chapter_id.in_(chapter_ids))
        )
        progress_result = await self.db.execute(progress_query)
        progress_records = {p.chapter_id: p for p in progress_result.scalars().all()}

        # Build chapter list with progress
        chapters_with_progress = []
        for chapter in chapters:
            progress = progress_records.get(chapter.id)
            chapters_with_progress.append({
                "id": chapter.id,
                "chapter_number": chapter.chapter_number,
                "slug": chapter.slug,
                "title": chapter.title,
                "description": chapter.description,
                "estimated_minutes": chapter.estimated_minutes,
                "requires_premium": chapter.requires_premium,
                "is_completed": progress.is_completed if progress else False,
                "time_spent_seconds": progress.time_spent_seconds if progress else 0,
                "completed_at": progress.completed_at.isoformat() if progress and progress.completed_at else None
            })

        # Calculate overall progress
        progress_percentage = await self._calculate_course_progress(user_id, course_id)

        # Get streak information
        streak_info = await self._get_streak_info(user_id)

        # Calculate total time spent
        total_time_spent = sum(
            p.time_spent_seconds for p in progress_records.values()
        )

        return {
            "course_id": course.id,
            "course_title": course.title,
            "course_slug": course.slug,
            "total_chapters": len(chapters),
            "free_chapter_limit": course.free_chapter_limit,
            "chapters": chapters_with_progress,
            "user_progress": {
                "completed_chapters": sum(1 for ch in chapters_with_progress if ch["is_completed"]),
                "total_chapters": len(chapters),
                "progress_percentage": progress_percentage,
                "current_streak": streak_info["current_streak"],
                "longest_streak": streak_info["longest_streak"],
                "total_time_spent_seconds": total_time_spent
            }
        }

    async def _calculate_course_progress(
        self,
        user_id: int,
        course_id: int
    ) -> float:
        """
        Calculate user's progress percentage for a course

        Args:
            user_id: User database ID
            course_id: Course database ID

        Returns:
            Progress percentage (0-100)
        """
        # Get total chapters
        total_query = (
            select(func.count(Chapter.id))
            .where(Chapter.course_id == course_id)
            .where(Chapter.is_published == True)
        )
        total_result = await self.db.execute(total_query)
        total_chapters = total_result.scalar() or 0

        if total_chapters == 0:
            return 0.0

        # Get completed chapters
        completed_query = (
            select(func.count(Progress.id))
            .join(Chapter, Progress.chapter_id == Chapter.id)
            .where(Chapter.course_id == course_id)
            .where(Progress.user_id == user_id)
            .where(Progress.is_completed == True)
        )
        completed_result = await self.db.execute(completed_query)
        completed_chapters = completed_result.scalar() or 0

        progress_percentage = (completed_chapters / total_chapters) * 100
        return round(progress_percentage, 2)

    async def _get_streak_info(self, user_id: int) -> dict:
        """
        Get user's current and longest streak

        Args:
            user_id: User database ID

        Returns:
            Dictionary with current_streak and longest_streak
        """
        # Get any progress record to check streak info
        # (streak is stored at the user level across all progress records)
        query = (
            select(Progress)
            .where(Progress.user_id == user_id)
            .order_by(Progress.updated_at.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        progress = result.scalar_one_or_none()

        if progress:
            return {
                "current_streak": progress.current_streak,
                "longest_streak": progress.longest_streak
            }
        else:
            return {
                "current_streak": 0,
                "longest_streak": 0
            }
