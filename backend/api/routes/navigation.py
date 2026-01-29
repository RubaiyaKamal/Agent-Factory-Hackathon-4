"""
Navigation routes for Course Companion FTE
Handles chapter navigation and course structure retrieval
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.navigation import (
    ChapterNavigation,
    CourseStructure,
    ChapterWithProgress,
    ProgressSummary
)
from backend.api.schemas.content import ChapterResponse
from backend.api.models.user import User
from backend.db.session import get_db_session
from backend.services.navigation_service import NavigationService
from backend.services.content_service import ContentService
from backend.services.r2 import get_r2_client, R2Client
from backend.api.middleware.auth import get_current_user, get_current_user_optional


router = APIRouter(prefix="/navigation", tags=["navigation"])


def get_navigation_service(
    db: AsyncSession = Depends(get_db_session)
) -> NavigationService:
    """
    Dependency to provide NavigationService instance
    """
    return NavigationService(db=db)


def get_content_service_for_nav(
    db: AsyncSession = Depends(get_db_session),
    r2_client: R2Client = Depends(get_r2_client)
) -> ContentService:
    """
    Dependency to provide ContentService instance for navigation
    """
    return ContentService(db=db, r2_client=r2_client)


@router.get("/chapters/{chapter_id}/next", response_model=Optional[ChapterResponse])
async def get_next_chapter(
    chapter_id: int,
    nav_service: NavigationService = Depends(get_navigation_service),
    content_service: ContentService = Depends(get_content_service_for_nav),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> Optional[ChapterResponse]:
    """
    Get the next chapter in sequence

    Returns the next chapter after the specified chapter_id.
    Returns null if the current chapter is the last in the course.

    Args:
        chapter_id: Current chapter database ID
        current_user: Optional authenticated user

    Returns:
        ChapterResponse with next chapter details and signed content URL, or null

    Raises:
        HTTPException 404: If current chapter not found
    """
    # Verify current chapter exists
    await content_service.get_chapter_by_id(chapter_id)

    # Get next chapter
    next_chapter = await nav_service.get_next_chapter(chapter_id)

    if not next_chapter:
        return None

    # Generate signed URL for content
    content_url = await content_service.generate_content_url(next_chapter)

    return ChapterResponse(
        id=next_chapter.id,
        course_id=next_chapter.course_id,
        chapter_number=next_chapter.chapter_number,
        slug=next_chapter.slug,
        title=next_chapter.title,
        description=next_chapter.description,
        content_url=content_url,
        estimated_minutes=next_chapter.estimated_minutes,
        word_count=next_chapter.word_count,
        requires_premium=next_chapter.requires_premium,
        previous_chapter_id=next_chapter.previous_chapter_id,
        next_chapter_id=next_chapter.next_chapter_id,
        created_at=next_chapter.created_at,
        updated_at=next_chapter.updated_at,
        is_published=next_chapter.is_published
    )


@router.get("/chapters/{chapter_id}/previous", response_model=Optional[ChapterResponse])
async def get_previous_chapter(
    chapter_id: int,
    nav_service: NavigationService = Depends(get_navigation_service),
    content_service: ContentService = Depends(get_content_service_for_nav),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> Optional[ChapterResponse]:
    """
    Get the previous chapter in sequence

    Returns the previous chapter before the specified chapter_id.
    Returns null if the current chapter is the first in the course.

    Args:
        chapter_id: Current chapter database ID
        current_user: Optional authenticated user

    Returns:
        ChapterResponse with previous chapter details and signed content URL, or null

    Raises:
        HTTPException 404: If current chapter not found
    """
    # Verify current chapter exists
    await content_service.get_chapter_by_id(chapter_id)

    # Get previous chapter
    prev_chapter = await nav_service.get_previous_chapter(chapter_id)

    if not prev_chapter:
        return None

    # Generate signed URL for content
    content_url = await content_service.generate_content_url(prev_chapter)

    return ChapterResponse(
        id=prev_chapter.id,
        course_id=prev_chapter.course_id,
        chapter_number=prev_chapter.chapter_number,
        slug=prev_chapter.slug,
        title=prev_chapter.title,
        description=prev_chapter.description,
        content_url=content_url,
        estimated_minutes=prev_chapter.estimated_minutes,
        word_count=prev_chapter.word_count,
        requires_premium=prev_chapter.requires_premium,
        previous_chapter_id=prev_chapter.previous_chapter_id,
        next_chapter_id=prev_chapter.next_chapter_id,
        created_at=prev_chapter.created_at,
        updated_at=prev_chapter.updated_at,
        is_published=prev_chapter.is_published
    )


@router.get("/chapters/{chapter_id}/context", response_model=ChapterNavigation)
async def get_chapter_navigation_context(
    chapter_id: int,
    nav_service: NavigationService = Depends(get_navigation_service),
    content_service: ContentService = Depends(get_content_service_for_nav),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> ChapterNavigation:
    """
    Get complete navigation context for a chapter

    Returns the current chapter along with next and previous chapters,
    and the user's overall course progress percentage.

    Args:
        chapter_id: Current chapter database ID
        current_user: Optional authenticated user

    Returns:
        ChapterNavigation with current, next, previous chapters and progress

    Raises:
        HTTPException 404: If chapter not found
    """
    # Get navigation info
    current, next_ch, prev_ch, progress_pct = await nav_service.get_chapter_navigation(
        chapter_id=chapter_id,
        user=current_user
    )

    # Generate signed URLs
    current_url = await content_service.generate_content_url(current)

    current_response = ChapterResponse(
        id=current.id,
        course_id=current.course_id,
        chapter_number=current.chapter_number,
        slug=current.slug,
        title=current.title,
        description=current.description,
        content_url=current_url,
        estimated_minutes=current.estimated_minutes,
        word_count=current.word_count,
        requires_premium=current.requires_premium,
        previous_chapter_id=current.previous_chapter_id,
        next_chapter_id=current.next_chapter_id,
        created_at=current.created_at,
        updated_at=current.updated_at,
        is_published=current.is_published
    )

    next_response = None
    if next_ch:
        next_url = await content_service.generate_content_url(next_ch)
        next_response = ChapterResponse(
            id=next_ch.id,
            course_id=next_ch.course_id,
            chapter_number=next_ch.chapter_number,
            slug=next_ch.slug,
            title=next_ch.title,
            description=next_ch.description,
            content_url=next_url,
            estimated_minutes=next_ch.estimated_minutes,
            word_count=next_ch.word_count,
            requires_premium=next_ch.requires_premium,
            previous_chapter_id=next_ch.previous_chapter_id,
            next_chapter_id=next_ch.next_chapter_id,
            created_at=next_ch.created_at,
            updated_at=next_ch.updated_at,
            is_published=next_ch.is_published
        )

    prev_response = None
    if prev_ch:
        prev_url = await content_service.generate_content_url(prev_ch)
        prev_response = ChapterResponse(
            id=prev_ch.id,
            course_id=prev_ch.course_id,
            chapter_number=prev_ch.chapter_number,
            slug=prev_ch.slug,
            title=prev_ch.title,
            description=prev_ch.description,
            content_url=prev_url,
            estimated_minutes=prev_ch.estimated_minutes,
            word_count=prev_ch.word_count,
            requires_premium=prev_ch.requires_premium,
            previous_chapter_id=prev_ch.previous_chapter_id,
            next_chapter_id=prev_ch.next_chapter_id,
            created_at=prev_ch.created_at,
            updated_at=prev_ch.updated_at,
            is_published=prev_ch.is_published
        )

    return ChapterNavigation(
        current=current_response,
        next=next_response,
        previous=prev_response,
        course_progress_percentage=progress_pct
    )


@router.get("/courses/{course_id}/structure", response_model=CourseStructure)
async def get_course_structure(
    course_id: int,
    nav_service: NavigationService = Depends(get_navigation_service),
    current_user: User = Depends(get_current_user)
) -> CourseStructure:
    """
    Get complete course structure with user progress

    Returns the full course structure including all chapters and detailed
    progress information. Requires authentication.

    Args:
        course_id: Course database ID
        current_user: Authenticated user (required)

    Returns:
        CourseStructure with all chapters and progress details

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 404: If course not found
    """
    structure = await nav_service.get_course_structure(
        course_id=course_id,
        user_id=current_user.id
    )

    return CourseStructure(**structure)
