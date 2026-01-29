"""
Progress routes for Course Companion FTE
Handles progress tracking, streaks, and user statistics
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.progress import (
    MarkChapterCompleteRequest,
    ChapterProgressResponse,
    OverallProgressResponse,
    StreakInfo,
    StatsResponse,
    CourseProgressSummary
)
from backend.api.models.user import User
from backend.db.session import get_db_session
from backend.services.progress_service import ProgressService
from backend.api.middleware.auth import get_current_user


router = APIRouter(prefix="/progress", tags=["progress"])


def get_progress_service(
    db: AsyncSession = Depends(get_db_session)
) -> ProgressService:
    """
    Dependency to provide ProgressService instance
    """
    return ProgressService(db=db)


@router.post("/chapters/{chapter_id}/complete", response_model=ChapterProgressResponse)
async def mark_chapter_complete(
    chapter_id: int,
    request: MarkChapterCompleteRequest,
    service: ProgressService = Depends(get_progress_service),
    current_user: User = Depends(get_current_user)
) -> ChapterProgressResponse:
    """
    Mark a chapter as complete

    Records chapter completion and updates user's learning streak.
    Can be called multiple times - will update time spent if already completed.

    Args:
        chapter_id: Chapter database ID
        request: Contains optional time spent
        current_user: Authenticated user (required)

    Returns:
        ChapterProgressResponse with updated progress

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 404: If chapter not found
    """
    result = await service.mark_chapter_complete(
        user_id=current_user.id,
        chapter_id=chapter_id,
        time_spent_seconds=request.time_spent_seconds
    )

    return ChapterProgressResponse(**result)


@router.get("/me", response_model=OverallProgressResponse)
async def get_my_progress(
    service: ProgressService = Depends(get_progress_service),
    current_user: User = Depends(get_current_user)
) -> OverallProgressResponse:
    """
    Get current user's overall progress

    Returns comprehensive progress information including:
    - Progress across all courses
    - Current learning streak
    - Total time spent
    - Achievements earned

    Args:
        current_user: Authenticated user (required)

    Returns:
        OverallProgressResponse with complete progress data

    Raises:
        HTTPException 401: If not authenticated
    """
    result = await service.get_user_progress(current_user.id)

    # Build response
    courses = [CourseProgressSummary(**course) for course in result["courses"]]
    streak = StreakInfo(**result["streak"])

    return OverallProgressResponse(
        user_id=result["user_id"],
        total_chapters_completed=result["total_chapters_completed"],
        total_time_spent_seconds=result["total_time_spent_seconds"],
        courses=courses,
        streak=streak,
        achievements_earned=result["achievements_earned"]
    )


@router.get("/streak", response_model=StreakInfo)
async def get_my_streak(
    service: ProgressService = Depends(get_progress_service),
    current_user: User = Depends(get_current_user)
) -> StreakInfo:
    """
    Get current user's learning streak

    Returns detailed streak information including:
    - Current consecutive days of activity
    - Longest streak ever achieved
    - Streak status (active, at_risk, or broken)
    - Days until streak breaks (with 24-hour grace period)

    Args:
        current_user: Authenticated user (required)

    Returns:
        StreakInfo with streak details

    Raises:
        HTTPException 401: If not authenticated
    """
    streak_data = await service.calculate_streak(current_user.id)

    return StreakInfo(**streak_data)


@router.get("/stats", response_model=StatsResponse)
async def get_my_stats(
    service: ProgressService = Depends(get_progress_service),
    current_user: User = Depends(get_current_user)
) -> StatsResponse:
    """
    Get detailed user statistics

    Returns comprehensive statistics including:
    - Total chapters completed
    - Quiz performance (attempts, passes, average score)
    - Total time spent learning
    - Account age
    - Current streak

    Useful for:
    - Progress dashboards
    - Achievement tracking
    - Motivational features

    Args:
        current_user: Authenticated user (required)

    Returns:
        StatsResponse with detailed statistics

    Raises:
        HTTPException 401: If not authenticated
    """
    stats_data = await service.get_user_stats(current_user.id)

    # Convert streak dict to StreakInfo
    stats_data["streak"] = StreakInfo(**stats_data["streak"])

    return StatsResponse(**stats_data)
