"""
Quiz Service for Course Companion FTE
Handles quiz retrieval and rule-based grading (NO LLM)
CONSTITUTIONAL REQUIREMENT: All grading must be deterministic and rule-based
"""
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from backend.api.models.quiz import Quiz, Question
from backend.api.models.quiz_attempt import QuizAttempt
from backend.api.models.user import User
from backend.core.config import get_settings


class QuizService:
    """
    Service for quiz retrieval and rule-based grading
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()

    async def get_quiz_by_chapter(self, chapter_id: int) -> Optional[Quiz]:
        """
        Get quiz for a specific chapter

        Args:
            chapter_id: Chapter database ID

        Returns:
            Quiz object or None if no quiz exists
        """
        query = (
            select(Quiz)
            .where(Quiz.chapter_id == chapter_id)
            .where(Quiz.is_published == True)
        )

        result = await self.db.execute(query)
        quiz = result.scalar_one_or_none()

        return quiz

    async def get_quiz_by_id(self, quiz_id: int) -> Quiz:
        """
        Get quiz by ID

        Args:
            quiz_id: Quiz database ID

        Returns:
            Quiz object

        Raises:
            HTTPException: If quiz not found
        """
        quiz = await self.db.get(Quiz, quiz_id)

        if not quiz or not quiz.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz with ID {quiz_id} not found"
            )

        return quiz

    async def get_quiz_questions(self, quiz_id: int) -> List[Question]:
        """
        Get all questions for a quiz

        Args:
            quiz_id: Quiz database ID

        Returns:
            List of Question objects ordered by question_number
        """
        query = (
            select(Question)
            .where(Question.quiz_id == quiz_id)
            .order_by(Question.question_number)
        )

        result = await self.db.execute(query)
        questions = result.scalars().all()

        return list(questions)

    async def submit_quiz(
        self,
        user_id: int,
        quiz_id: int,
        answers: Dict[int, str],
        time_taken_seconds: Optional[int] = None
    ) -> dict:
        """
        Submit quiz and grade answers using rule-based logic (NO LLM)

        Args:
            user_id: User database ID
            quiz_id: Quiz database ID
            answers: Map of question_id to user's answer
            time_taken_seconds: Time taken to complete quiz

        Returns:
            Dictionary with grading results

        Raises:
            HTTPException: If quiz not found or max attempts exceeded
        """
        # Get quiz
        quiz = await self.get_quiz_by_id(quiz_id)

        # Check if user has attempts remaining
        attempt_count = await self.get_user_attempt_count(user_id, quiz_id)

        if attempt_count >= quiz.max_attempts:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Maximum attempts ({quiz.max_attempts}) exceeded for this quiz"
            )

        # Get questions
        questions = await self.get_quiz_questions(quiz_id)

        # Grade each answer
        feedback = []
        correct_count = 0
        points_earned = 0
        total_points = sum(q.points for q in questions)

        for question in questions:
            user_answer = answers.get(question.id, "")

            # Grade using rule-based logic
            is_correct, correct_answer, explanation = self.grade_answer(
                question=question,
                user_answer=user_answer
            )

            points = question.points if is_correct else 0

            if is_correct:
                correct_count += 1
                points_earned += points

            feedback.append({
                "question_id": question.id,
                "question_number": question.question_number,
                "user_answer": user_answer,
                "is_correct": is_correct,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "points_earned": points,
                "points_possible": question.points
            })

        # Calculate score percentage
        score = int((points_earned / total_points * 100)) if total_points > 0 else 0

        # Check if passed
        passed = score >= quiz.passing_score

        # Create quiz attempt record
        quiz_attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            attempt_number=attempt_count + 1,
            answers=json.dumps(answers),
            score=score,
            correct_count=correct_count,
            total_questions=len(questions),
            passed=passed,
            started_at=datetime.utcnow(),
            submitted_at=datetime.utcnow(),
            time_taken_seconds=time_taken_seconds,
            feedback=json.dumps(feedback)
        )

        self.db.add(quiz_attempt)
        await self.db.commit()
        await self.db.refresh(quiz_attempt)

        return {
            "quiz_attempt_id": quiz_attempt.id,
            "quiz_id": quiz_id,
            "attempt_number": quiz_attempt.attempt_number,
            "score": score,
            "points_earned": points_earned,
            "total_points": total_points,
            "correct_count": correct_count,
            "total_questions": len(questions),
            "passed": passed,
            "time_taken_seconds": time_taken_seconds,
            "feedback": feedback,
            "submitted_at": quiz_attempt.submitted_at
        }

    def grade_answer(
        self,
        question: Question,
        user_answer: str
    ) -> Tuple[bool, str, str]:
        """
        Grade a single answer using rule-based logic (NO LLM)

        Args:
            question: Question object
            user_answer: User's answer

        Returns:
            Tuple of (is_correct, correct_answer, explanation)
        """
        # Parse answer configuration
        answer_config = json.loads(question.answer_config)

        if question.question_type == "multiple_choice":
            return self._grade_multiple_choice(
                answer_config, user_answer, question
            )

        elif question.question_type == "true_false":
            return self._grade_true_false(
                answer_config, user_answer, question
            )

        elif question.question_type == "fill_in_blank":
            return self._grade_fill_in_blank(
                answer_config, user_answer, question
            )

        else:
            return False, "", "Unknown question type"

    def _grade_multiple_choice(
        self,
        answer_config: dict,
        user_answer: str,
        question: Question
    ) -> Tuple[bool, str, str]:
        """
        Grade multiple choice question with exact match
        """
        correct_answer = answer_config.get("correct", "")
        explanation = answer_config.get("explanation", "")

        # Normalize for comparison
        user_normalized = user_answer.strip().lower()
        correct_normalized = correct_answer.strip().lower()

        is_correct = user_normalized == correct_normalized

        return is_correct, correct_answer, explanation

    def _grade_true_false(
        self,
        answer_config: dict,
        user_answer: str,
        question: Question
    ) -> Tuple[bool, str, str]:
        """
        Grade true/false question
        """
        correct_answer = answer_config.get("correct", "")
        explanation = answer_config.get("explanation", "")

        # Normalize boolean responses
        user_normalized = self._normalize_boolean(user_answer)
        correct_normalized = self._normalize_boolean(str(correct_answer))

        is_correct = user_normalized == correct_normalized

        return is_correct, str(correct_answer), explanation

    def _grade_fill_in_blank(
        self,
        answer_config: dict,
        user_answer: str,
        question: Question
    ) -> Tuple[bool, str, str]:
        """
        Grade fill-in-blank question with multiple accepted answers
        """
        correct_answers = answer_config.get("correct", [])
        if isinstance(correct_answers, str):
            correct_answers = [correct_answers]

        explanation = answer_config.get("explanation", "")
        regex_pattern = answer_config.get("regex", None)

        # Apply trimming if configured
        if question.trim_whitespace or self.settings.QUIZ_TRIM_WHITESPACE:
            user_answer = user_answer.strip()

        # Apply case insensitivity if configured
        if not question.case_sensitive or self.settings.QUIZ_CASE_INSENSITIVE:
            user_answer_normalized = user_answer.lower()
            correct_answers_normalized = [ans.lower() for ans in correct_answers]
        else:
            user_answer_normalized = user_answer
            correct_answers_normalized = correct_answers

        # Check regex pattern if provided
        if regex_pattern:
            try:
                pattern = re.compile(regex_pattern, re.IGNORECASE if not question.case_sensitive else 0)
                is_correct = bool(pattern.match(user_answer))
            except re.error:
                is_correct = False
        else:
            # Check against list of accepted answers
            is_correct = user_answer_normalized in correct_answers_normalized

        return is_correct, correct_answers[0] if correct_answers else "", explanation

    def _normalize_boolean(self, value: str) -> bool:
        """
        Convert various string representations to boolean
        """
        value = value.strip().lower()

        if value in ["true", "t", "yes", "y", "1"]:
            return True
        elif value in ["false", "f", "no", "n", "0"]:
            return False
        else:
            # Default to False for invalid input
            return False

    async def get_user_attempt_count(self, user_id: int, quiz_id: int) -> int:
        """
        Get number of attempts user has made on a quiz

        Args:
            user_id: User database ID
            quiz_id: Quiz database ID

        Returns:
            Number of attempts
        """
        query = (
            select(func.count(QuizAttempt.id))
            .where(QuizAttempt.user_id == user_id)
            .where(QuizAttempt.quiz_id == quiz_id)
        )

        result = await self.db.execute(query)
        count = result.scalar() or 0

        return count

    async def get_user_quiz_attempts(
        self,
        user_id: int,
        quiz_id: int
    ) -> List[QuizAttempt]:
        """
        Get all user's attempts for a quiz

        Args:
            user_id: User database ID
            quiz_id: Quiz database ID

        Returns:
            List of QuizAttempt objects
        """
        query = (
            select(QuizAttempt)
            .where(QuizAttempt.user_id == user_id)
            .where(QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.created_at.desc())
        )

        result = await self.db.execute(query)
        attempts = result.scalars().all()

        return list(attempts)

    async def get_attempt_by_id(
        self,
        attempt_id: int,
        user_id: int
    ) -> QuizAttempt:
        """
        Get specific quiz attempt

        Args:
            attempt_id: QuizAttempt database ID
            user_id: User database ID (for authorization)

        Returns:
            QuizAttempt object

        Raises:
            HTTPException: If attempt not found or unauthorized
        """
        attempt = await self.db.get(QuizAttempt, attempt_id)

        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz attempt {attempt_id} not found"
            )

        if attempt.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this quiz attempt"
            )

        return attempt
