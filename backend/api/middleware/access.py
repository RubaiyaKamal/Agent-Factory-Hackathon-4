"""
Access Control Middleware for Course Companion FTE
Implements freemium gate for content and quiz access
"""
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.api.models.user import User
from backend.api.models.chapter import Chapter
from backend.api.models.quiz import Quiz
from backend.db.session import get_db_session
from backend.api.middleware.auth import get_current_user


# Freemium tier limits
FREE_TIER_CHAPTER_LIMIT = 3  # Free users can access first 3 chapters


async def check_chapter_access(
    chapter_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Check if user has access to a chapter based on subscription tier.

    Free tier: First 3 chapters only
    Premium tier: All chapters

    Args:
        chapter_id: Chapter database ID
        current_user: Authenticated user (required)
        db: Database session

    Raises:
        HTTPException 403: If user lacks access to premium content
        HTTPException 404: If chapter not found
    """
    # Get chapter from database
    chapter = await db.get(Chapter, chapter_id)

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "chapter_not_found",
                "message": f"Chapter with ID {chapter_id} not found"
            }
        )

    # Check if chapter requires premium
    if chapter.requires_premium:
        # Premium chapter - check user tier
        if current_user.subscription_tier == "free":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "premium_required",
                    "message": "This chapter requires a premium subscription",
                    "upgrade_url": "/pricing",
                    "chapter_number": chapter.chapter_number,
                    "chapter_title": chapter.title,
                    "subscription_tier": current_user.subscription_tier
                }
            )

    # Free chapter or premium user - access granted
    return None


async def check_quiz_access(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Check if user has access to a quiz based on subscription tier.

    Quiz access is determined by the associated chapter's requirements.

    Args:
        quiz_id: Quiz database ID
        current_user: Authenticated user (required)
        db: Database session

    Raises:
        HTTPException 403: If user lacks access to premium quiz
        HTTPException 404: If quiz not found
    """
    # Get quiz from database
    quiz = await db.get(Quiz, quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "quiz_not_found",
                "message": f"Quiz with ID {quiz_id} not found"
            }
        )

    # Get associated chapter
    chapter = await db.get(Chapter, quiz.chapter_id)

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "chapter_not_found",
                "message": f"Chapter associated with quiz not found"
            }
        )

    # Check if chapter requires premium
    if chapter.requires_premium:
        # Premium quiz - check user tier
        if current_user.subscription_tier == "free":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "premium_required",
                    "message": "This quiz requires a premium subscription",
                    "upgrade_url": "/pricing",
                    "chapter_number": chapter.chapter_number,
                    "chapter_title": chapter.title,
                    "quiz_title": quiz.title,
                    "subscription_tier": current_user.subscription_tier
                }
            )

    # Free quiz or premium user - access granted
    return None


async def check_chapter_access_by_number(
    chapter_number: int,
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Check if user has access to a chapter by chapter number (alternative check).

    Useful when you have chapter_number instead of chapter_id.

    Args:
        chapter_number: Chapter sequence number (1, 2, 3, ...)
        course_id: Course database ID
        current_user: Authenticated user (required)
        db: Database session

    Raises:
        HTTPException 403: If user lacks access to premium content
    """
    # Free tier: chapters 1-3 only
    if current_user.subscription_tier == "free" and chapter_number > FREE_TIER_CHAPTER_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "premium_required",
                "message": f"Chapters beyond {FREE_TIER_CHAPTER_LIMIT} require a premium subscription",
                "upgrade_url": "/pricing",
                "chapter_number": chapter_number,
                "subscription_tier": current_user.subscription_tier,
                "free_tier_limit": FREE_TIER_CHAPTER_LIMIT
            }
        )

    # Premium user or chapter within free tier - access granted
    return None


def is_premium_user(user: User) -> bool:
    """
    Helper to check if user has premium access.

    Args:
        user: User object

    Returns:
        bool: True if user has premium tier
    """
    return user.subscription_tier in ["premium", "enterprise"]


def get_accessible_chapter_count(user: User) -> Optional[int]:
    """
    Get the number of chapters accessible to user.

    Args:
        user: User object

    Returns:
        int: Number of accessible chapters, or None if unlimited (premium)
    """
    if is_premium_user(user):
        return None  # Unlimited access

    return FREE_TIER_CHAPTER_LIMIT


# Optional: Dependency that returns user with access info
async def get_user_with_access_info(
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Get current user with access information.

    Useful for routes that need to show access status.

    Args:
        current_user: Authenticated user

    Returns:
        dict: User info with access details
    """
    return {
        "user": current_user,
        "is_premium": is_premium_user(current_user),
        "accessible_chapters": get_accessible_chapter_count(current_user),
        "subscription_tier": current_user.subscription_tier
    }
