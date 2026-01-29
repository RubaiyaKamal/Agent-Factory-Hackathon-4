"""
Content routes for Course Companion FTE
Handles course and chapter content delivery
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.content import (
    CourseResponse,
    CourseDetailResponse,
    CourseListResponse,
    ChapterResponse,
    ChapterListItem
)
from backend.api.models.user import User
from backend.db.session import get_db_session
from backend.services.r2 import get_r2_client, R2Client
from backend.services.content_service import ContentService
from backend.api.middleware.auth import get_current_user, get_current_user_optional


router = APIRouter(prefix="/content", tags=["content"])


def get_content_service(
    db: AsyncSession = Depends(get_db_session),
    r2_client: R2Client = Depends(get_r2_client)
) -> ContentService:
    """
    Dependency to provide ContentService instance
    """
    return ContentService(db=db, r2_client=r2_client)


@router.get("/courses", response_model=CourseListResponse)
async def list_courses(
    service: ContentService = Depends(get_content_service),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> CourseListResponse:
    """
    List all available courses

    Returns a list of published courses with metadata.
    Authentication is optional - authenticated users may see additional information.

    Returns:
        CourseListResponse with list of courses and total count
    """
    courses = await service.list_courses(user=current_user, published_only=True)

    course_responses = [
        CourseResponse(
            id=course.id,
            slug=course.slug,
            title=course.title,
            description=course.description,
            total_chapters=course.total_chapters,
            estimated_hours=course.estimated_hours,
            difficulty_level=course.difficulty_level,
            free_chapter_limit=course.free_chapter_limit,
            required_tier=course.required_tier,
            is_published=course.is_published,
            published_at=course.published_at,
            created_at=course.created_at,
            updated_at=course.updated_at
        )
        for course in courses
    ]

    return CourseListResponse(
        courses=course_responses,
        total=len(course_responses)
    )


@router.get("/courses/{slug}", response_model=CourseDetailResponse)
async def get_course_by_slug(
    slug: str,
    service: ContentService = Depends(get_content_service),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> CourseDetailResponse:
    """
    Get course details by slug

    Includes course metadata and list of all chapters.
    If authenticated, includes user's progress information.

    Args:
        slug: Course slug (e.g., 'ai-agent-development')
        current_user: Optional authenticated user

    Returns:
        CourseDetailResponse with course details and chapters

    Raises:
        HTTPException 404: If course not found
    """
    course = await service.get_course_by_slug(slug)
    chapters = await service.get_course_chapters(course.id, user=current_user)

    # Build chapter list items
    chapter_list_items = []
    for chapter in chapters:
        # Check if user has completed this chapter
        is_completed = None
        if current_user:
            progress = await service.check_chapter_progress(
                user_id=current_user.id,
                chapter_id=chapter.id
            )
            is_completed = progress.is_completed if progress else False

        chapter_list_items.append(
            ChapterListItem(
                id=chapter.id,
                chapter_number=chapter.chapter_number,
                slug=chapter.slug,
                title=chapter.title,
                estimated_minutes=chapter.estimated_minutes,
                requires_premium=chapter.requires_premium,
                is_completed=is_completed
            )
        )

    # Get user progress if authenticated
    user_progress = None
    if current_user:
        user_progress = await service.get_user_course_progress(
            user_id=current_user.id,
            course_id=course.id
        )

    return CourseDetailResponse(
        id=course.id,
        slug=course.slug,
        title=course.title,
        description=course.description,
        total_chapters=course.total_chapters,
        estimated_hours=course.estimated_hours,
        difficulty_level=course.difficulty_level,
        free_chapter_limit=course.free_chapter_limit,
        required_tier=course.required_tier,
        is_published=course.is_published,
        published_at=course.published_at,
        created_at=course.created_at,
        updated_at=course.updated_at,
        chapters=chapter_list_items,
        user_progress=user_progress
    )


@router.get("/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    chapter_id: int,
    service: ContentService = Depends(get_content_service),
    current_user: User = Depends(get_current_user)
) -> ChapterResponse:
    """
    Get chapter by ID with signed content URL

    Returns chapter metadata and a signed R2 URL for accessing the content.
    The signed URL expires after 60 minutes.

    **Authentication required.** Free users can access first 3 chapters only.
    Premium users can access all chapters.

    Args:
        chapter_id: Chapter database ID
        current_user: Authenticated user (required)

    Returns:
        ChapterResponse with chapter details and signed content URL

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 403: If free user tries to access premium chapter
        HTTPException 404: If chapter not found
        HTTPException 500: If URL generation fails
    """
    chapter = await service.get_chapter_by_id(chapter_id)

    # Check if user has access to this chapter (freemium gate)
    if chapter.requires_premium and current_user.subscription_tier == "free":
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

    # Generate signed URL for content access
    content_url = await service.generate_content_url(chapter)

    return ChapterResponse(
        id=chapter.id,
        course_id=chapter.course_id,
        chapter_number=chapter.chapter_number,
        slug=chapter.slug,
        title=chapter.title,
        description=chapter.description,
        content_url=content_url,
        estimated_minutes=chapter.estimated_minutes,
        word_count=chapter.word_count,
        requires_premium=chapter.requires_premium,
        previous_chapter_id=chapter.previous_chapter_id,
        next_chapter_id=chapter.next_chapter_id,
        created_at=chapter.created_at,
        updated_at=chapter.updated_at,
        is_published=chapter.is_published
    )
