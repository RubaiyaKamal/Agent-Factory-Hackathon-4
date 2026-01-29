"""
Quiz routes for Course Companion FTE
Handles quiz delivery, submission, and attempt history
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.quiz import (
    QuizResponse,
    QuestionResponse,
    SubmitQuizRequest,
    QuizResultResponse,
    QuestionFeedback,
    QuizHistoryResponse,
    QuizAttemptSummary
)
from backend.api.models.user import User
from backend.api.models.chapter import Chapter
from backend.db.session import get_db_session
from backend.services.quiz_service import QuizService
from backend.api.middleware.auth import get_current_user
import json


router = APIRouter(prefix="/quizzes", tags=["quizzes"])


def get_quiz_service(
    db: AsyncSession = Depends(get_db_session)
) -> QuizService:
    """
    Dependency to provide QuizService instance
    """
    return QuizService(db=db)


@router.get("/chapters/{chapter_id}/quiz", response_model=QuizResponse)
async def get_chapter_quiz(
    chapter_id: int,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> QuizResponse:
    """
    Get quiz for a chapter

    Returns the quiz with all questions but WITHOUT correct answers.
    The correct answers are only revealed after submission.

    **Authentication required.** Quizzes for premium chapters require premium subscription.

    Args:
        chapter_id: Chapter database ID
        current_user: Authenticated user (required)

    Returns:
        QuizResponse with questions (no answers included)

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 403: If free user tries to access premium quiz
        HTTPException 404: If no quiz exists for this chapter
    """
    # Get chapter to check premium requirements
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter {chapter_id} not found"
        )

    # Check if user has access (freemium gate)
    if chapter.requires_premium and current_user.subscription_tier == "free":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "premium_required",
                "message": "This quiz requires a premium subscription",
                "upgrade_url": "/pricing",
                "chapter_number": chapter.chapter_number,
                "chapter_title": chapter.title,
                "subscription_tier": current_user.subscription_tier
            }
        )

    # Get quiz for chapter
    quiz = await service.get_quiz_by_chapter(chapter_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No quiz found for chapter {chapter_id}"
        )

    # Get questions
    questions = await service.get_quiz_questions(quiz.id)

    # Build question responses (WITHOUT correct answers)
    question_responses = []
    total_points = 0

    for question in questions:
        # Parse answer config to get options for multiple choice
        answer_config = json.loads(question.answer_config)
        options = answer_config.get("options", None)

        question_responses.append(
            QuestionResponse(
                id=question.id,
                question_number=question.question_number,
                question_text=question.question_text,
                question_type=question.question_type,
                options=options,
                points=question.points
            )
        )
        total_points += question.points

    return QuizResponse(
        id=quiz.id,
        chapter_id=quiz.chapter_id,
        title=quiz.title,
        description=quiz.description,
        difficulty=quiz.difficulty,
        passing_score=quiz.passing_score,
        max_attempts=quiz.max_attempts,
        time_limit_minutes=quiz.time_limit_minutes,
        requires_premium=quiz.requires_premium,
        questions=question_responses,
        total_points=total_points,
        created_at=quiz.created_at
    )


@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
async def submit_quiz(
    quiz_id: int,
    submission: SubmitQuizRequest,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user)
) -> QuizResultResponse:
    """
    Submit quiz answers and get results

    Grades the quiz using rule-based logic (no LLM) and returns:
    - Overall score and pass/fail status
    - Detailed feedback for each question
    - Correct answers and explanations

    Args:
        quiz_id: Quiz database ID
        submission: User's answers
        current_user: Authenticated user (required)

    Returns:
        QuizResultResponse with grading results and feedback

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 403: If max attempts exceeded
        HTTPException 404: If quiz not found
    """
    # Submit and grade
    result = await service.submit_quiz(
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=submission.answers,
        time_taken_seconds=submission.time_taken_seconds
    )

    # Get quiz title
    quiz = await service.get_quiz_by_id(quiz_id)

    # Build feedback list
    feedback_list = [
        QuestionFeedback(**item) for item in result["feedback"]
    ]

    return QuizResultResponse(
        quiz_attempt_id=result["quiz_attempt_id"],
        quiz_id=quiz_id,
        quiz_title=quiz.title,
        attempt_number=result["attempt_number"],
        score=result["score"],
        points_earned=result["points_earned"],
        total_points=result["total_points"],
        correct_count=result["correct_count"],
        total_questions=result["total_questions"],
        passed=result["passed"],
        time_taken_seconds=result["time_taken_seconds"],
        feedback=feedback_list,
        submitted_at=result["submitted_at"]
    )


@router.get("/{quiz_id}/attempts", response_model=QuizHistoryResponse)
async def get_quiz_attempts(
    quiz_id: int,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user)
) -> QuizHistoryResponse:
    """
    Get user's quiz attempt history

    Returns all attempts the user has made on this quiz,
    along with their best score and remaining attempts.

    Args:
        quiz_id: Quiz database ID
        current_user: Authenticated user (required)

    Returns:
        QuizHistoryResponse with attempt history

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 404: If quiz not found
    """
    # Get quiz
    quiz = await service.get_quiz_by_id(quiz_id)

    # Get user's attempts
    attempts = await service.get_user_quiz_attempts(
        user_id=current_user.id,
        quiz_id=quiz_id
    )

    # Build attempt summaries
    attempt_summaries = [
        QuizAttemptSummary(
            attempt_id=attempt.id,
            attempt_number=attempt.attempt_number,
            score=attempt.score,
            passed=attempt.passed,
            submitted_at=attempt.submitted_at,
            time_taken_seconds=attempt.time_taken_seconds
        )
        for attempt in attempts
    ]

    # Calculate best score
    best_score = max((a.score for a in attempts), default=0)

    # Calculate remaining attempts
    attempts_remaining = quiz.max_attempts - len(attempts)

    return QuizHistoryResponse(
        quiz_id=quiz_id,
        quiz_title=quiz.title,
        attempts=attempt_summaries,
        best_score=best_score,
        attempts_remaining=max(0, attempts_remaining),
        max_attempts=quiz.max_attempts
    )


@router.get("/{quiz_id}/attempts/{attempt_id}", response_model=QuizResultResponse)
async def get_quiz_attempt_details(
    quiz_id: int,
    attempt_id: int,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user)
) -> QuizResultResponse:
    """
    Get detailed results for a specific quiz attempt

    Allows users to review their past quiz attempts with
    full feedback and correct answers.

    Args:
        quiz_id: Quiz database ID
        attempt_id: QuizAttempt database ID
        current_user: Authenticated user (required)

    Returns:
        QuizResultResponse with full attempt details

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 403: If not authorized to view this attempt
        HTTPException 404: If attempt not found
    """
    # Get attempt
    attempt = await service.get_attempt_by_id(attempt_id, current_user.id)

    # Verify attempt belongs to this quiz
    if attempt.quiz_id != quiz_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attempt {attempt_id} does not belong to quiz {quiz_id}"
        )

    # Get quiz
    quiz = await service.get_quiz_by_id(quiz_id)

    # Parse feedback
    feedback_data = json.loads(attempt.feedback) if attempt.feedback else []
    feedback_list = [QuestionFeedback(**item) for item in feedback_data]

    return QuizResultResponse(
        quiz_attempt_id=attempt.id,
        quiz_id=quiz_id,
        quiz_title=quiz.title,
        attempt_number=attempt.attempt_number,
        score=attempt.score,
        points_earned=sum(f.points_earned for f in feedback_list),
        total_points=sum(f.points_possible for f in feedback_list),
        correct_count=attempt.correct_count,
        total_questions=attempt.total_questions,
        passed=attempt.passed,
        time_taken_seconds=attempt.time_taken_seconds,
        feedback=feedback_list,
        submitted_at=attempt.submitted_at
    )
