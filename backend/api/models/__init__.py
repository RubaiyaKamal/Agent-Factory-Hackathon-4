"""
Database models for Course Companion FTE

All models follow Phase 1 Zero-Backend-LLM architecture:
- NO LLM API calls
- Deterministic data structures only
- Pre-computed embeddings (no runtime inference)
"""
from .achievement import Achievement
from .chapter import Chapter
from .course import Course
from .progress import Progress
from .quiz import Question, Quiz
from .quiz_attempt import QuizAttempt
from .user import User

__all__ = [
    "User",
    "Course",
    "Chapter",
    "Quiz",
    "Question",
    "QuizAttempt",
    "Progress",
    "Achievement",
]
