"""
Progress Service for Course Companion FTE
Handles progress tracking, streak calculation, and user statistics
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import pytz

from backend.api.models.progress import Progress
from backend.api.models.chapter import Chapter
from backend.api.models.course import Course
from backend.api.models.quiz_attempt import QuizAttempt
from backend.api.models.achievement import Achievement
from backend.api.models.user import User
from backend.core.config import get_settings


class ProgressService:
    """
    Service for managing user progress and streaks
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()

    async def mark_chapter_complete(
        self,
        user_id: int,
        chapter_id: int,
        time_spent_seconds: Optional[int] = None
    ) -> dict:
        """
        Mark a chapter as complete

        Args:
            user_id: User database ID
            chapter_id: Chapter database ID
            time_spent_seconds: Optional time spent on chapter

        Returns:
            Dictionary with updated progress
        """
        # Get or create progress record
        query = (
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.chapter_id == chapter_id)
        )
        result = await self.db.execute(query)
        progress = result.scalar_one_or_none()

        now = datetime.utcnow()

        if not progress:
            # Create new progress record
            progress = Progress(
                user_id=user_id,
                chapter_id=chapter_id,
                is_completed=True,
                completed_at=now,
                time_spent_seconds=time_spent_seconds or 0,
                last_accessed_at=now
            )
            self.db.add(progress)
        else:
            # Update existing record
            if not progress.is_completed:
                progress.is_completed = True
                progress.completed_at = now

            if time_spent_seconds:
                progress.time_spent_seconds += time_spent_seconds

            progress.last_accessed_at = now

        # Update streak
        await self._update_user_streak(user_id, now)

        await self.db.commit()
        await self.db.refresh(progress)

        # Get chapter info
        chapter = await self.db.get(Chapter, chapter_id)

        return {
            "chapter_id": chapter_id,
            "chapter_title": chapter.title if chapter else "Unknown",
            "is_completed": progress.is_completed,
            "completed_at": progress.completed_at,
            "time_spent_seconds": progress.time_spent_seconds,
            "last_accessed_at": progress.last_accessed_at
        }

    async def get_user_progress(self, user_id: int) -> dict:
        """
        Get overall progress for a user

        Args:
            user_id: User database ID

        Returns:
            Dictionary with overall progress
        """
        # Get user
        user = await self.db.get(User, user_id)

        # Get all courses
        courses_result = await self.db.execute(
            select(Course).where(Course.is_published == True)
        )
        courses = courses_result.scalars().all()

        # Get course progress summaries
        course_summaries = []
        total_chapters_completed = 0
        total_time_spent = 0

        for course in courses:
            summary = await self._get_course_progress_summary(user_id, course)
            course_summaries.append(summary)
            total_chapters_completed += summary["completed_chapters"]
            total_time_spent += summary["time_spent_seconds"]

        # Get streak info
        streak_info = await self.calculate_streak(user_id)

        # Get achievements count
        achievements_result = await self.db.execute(
            select(func.count(Achievement.id))
            .where(Achievement.user_id == user_id)
        )
        achievements_count = achievements_result.scalar() or 0

        return {
            "user_id": user_id,
            "total_chapters_completed": total_chapters_completed,
            "total_time_spent_seconds": total_time_spent,
            "courses": course_summaries,
            "streak": streak_info,
            "achievements_earned": achievements_count
        }

    async def _get_course_progress_summary(
        self,
        user_id: int,
        course: Course
    ) -> dict:
        """
        Get progress summary for a specific course

        Args:
            user_id: User database ID
            course: Course object

        Returns:
            Dictionary with course progress summary
        """
        # Get all chapters for course
        chapters_result = await self.db.execute(
            select(Chapter)
            .where(Chapter.course_id == course.id)
            .where(Chapter.is_published == True)
        )
        chapters = chapters_result.scalars().all()
        total_chapters = len(chapters)

        # Get user's progress on these chapters
        chapter_ids = [ch.id for ch in chapters]

        progress_result = await self.db.execute(
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.chapter_id.in_(chapter_ids))
        )
        progress_records = progress_result.scalars().all()

        # Calculate statistics
        completed_count = sum(1 for p in progress_records if p.is_completed)
        total_time = sum(p.time_spent_seconds for p in progress_records)
        progress_percentage = (
            (completed_count / total_chapters * 100) if total_chapters > 0 else 0
        )

        # Get last accessed time
        last_accessed = max(
            (p.last_accessed_at for p in progress_records),
            default=None
        )

        return {
            "course_id": course.id,
            "course_title": course.title,
            "course_slug": course.slug,
            "completed_chapters": completed_count,
            "total_chapters": total_chapters,
            "progress_percentage": round(progress_percentage, 2),
            "time_spent_seconds": total_time,
            "last_accessed": last_accessed
        }

    async def calculate_streak(self, user_id: int) -> dict:
        """
        Calculate user's learning streak

        Args:
            user_id: User database ID

        Returns:
            Dictionary with streak information
        """
        # Get user for timezone
        user = await self.db.get(User, user_id)
        user_tz = pytz.timezone(user.timezone if user else "UTC")

        # Get all progress records ordered by date
        progress_result = await self.db.execute(
            select(Progress)
            .where(Progress.user_id == user_id)
            .order_by(Progress.last_accessed_at.desc())
        )
        progress_records = progress_result.scalars().all()

        if not progress_records:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "last_activity_date": None,
                "streak_status": "broken",
                "days_until_broken": None
            }

        # Get unique activity dates
        activity_dates = set()
        for record in progress_records:
            # Convert to user's timezone and get date
            local_dt = record.last_accessed_at.replace(tzinfo=pytz.UTC).astimezone(user_tz)
            activity_dates.add(local_dt.date())

        # Sort dates
        sorted_dates = sorted(activity_dates, reverse=True)

        # Calculate current streak
        current_streak = 0
        today = datetime.now(user_tz).date()
        yesterday = today - timedelta(days=1)

        # Check if there's activity today or yesterday (with grace period)
        if sorted_dates[0] >= yesterday:
            current_date = sorted_dates[0]
            current_streak = 1

            # Count consecutive days
            for i in range(1, len(sorted_dates)):
                expected_date = current_date - timedelta(days=1)
                if sorted_dates[i] == expected_date:
                    current_streak += 1
                    current_date = sorted_dates[i]
                elif sorted_dates[i] < expected_date:
                    # Gap found
                    break

        # Calculate longest streak
        longest_streak = 0
        temp_streak = 1

        for i in range(len(sorted_dates) - 1):
            if sorted_dates[i] - sorted_dates[i + 1] == timedelta(days=1):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1

        longest_streak = max(longest_streak, temp_streak, current_streak)

        # Determine streak status
        last_activity = sorted_dates[0]
        days_since_activity = (today - last_activity).days

        if days_since_activity == 0:
            streak_status = "active"
            days_until_broken = 1
        elif days_since_activity == 1:
            streak_status = "at_risk"
            days_until_broken = 0
        else:
            streak_status = "broken"
            days_until_broken = None

        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_activity_date": datetime.combine(last_activity, datetime.min.time()),
            "streak_status": streak_status,
            "days_until_broken": days_until_broken
        }

    async def _update_user_streak(self, user_id: int, activity_time: datetime):
        """
        Update streak information for all user's progress records

        Args:
            user_id: User database ID
            activity_time: Time of activity
        """
        # Calculate streak
        streak_info = await self.calculate_streak(user_id)

        # Update all progress records with current streak info
        progress_result = await self.db.execute(
            select(Progress).where(Progress.user_id == user_id)
        )
        progress_records = progress_result.scalars().all()

        for record in progress_records:
            record.current_streak = streak_info["current_streak"]
            record.longest_streak = streak_info["longest_streak"]
            record.last_activity_date = streak_info["last_activity_date"]

    async def get_user_stats(self, user_id: int) -> dict:
        """
        Get detailed statistics for a user

        Args:
            user_id: User database ID

        Returns:
            Dictionary with detailed statistics
        """
        # Get user
        user = await self.db.get(User, user_id)

        # Total chapters completed
        chapters_result = await self.db.execute(
            select(func.count(Progress.id))
            .where(Progress.user_id == user_id)
            .where(Progress.is_completed == True)
        )
        total_chapters = chapters_result.scalar() or 0

        # Total time spent
        time_result = await self.db.execute(
            select(func.sum(Progress.time_spent_seconds))
            .where(Progress.user_id == user_id)
        )
        total_time = time_result.scalar() or 0

        # Quiz statistics
        quiz_attempts_result = await self.db.execute(
            select(QuizAttempt)
            .where(QuizAttempt.user_id == user_id)
        )
        quiz_attempts = quiz_attempts_result.scalars().all()

        total_quizzes = len(quiz_attempts)
        passed_quizzes = sum(1 for qa in quiz_attempts if qa.passed)
        avg_score = (
            sum(qa.score for qa in quiz_attempts) / total_quizzes
            if total_quizzes > 0 else 0
        )

        # Account age
        days_since_signup = (datetime.utcnow() - user.created_at).days

        # Streak info
        streak_info = await self.calculate_streak(user_id)

        return {
            "total_chapters_completed": total_chapters,
            "total_quizzes_taken": total_quizzes,
            "total_quizzes_passed": passed_quizzes,
            "average_quiz_score": round(avg_score, 2),
            "total_time_spent_seconds": total_time,
            "total_time_spent_hours": round(total_time / 3600, 2),
            "account_created_at": user.created_at,
            "days_since_signup": days_since_signup,
            "streak": streak_info
        }
