"""
Base classes for Course Companion FTE database models
Includes SQLModel base and imports for all models
"""
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models with async support
    """
    pass


# Import all models here to ensure they're registered with SQLAlchemy
# This is needed for Alembic migrations to detect all models
from backend.api.models.user import User  # noqa: F401
from backend.api.models.course import Course  # noqa: F401
from backend.api.models.chapter import Chapter  # noqa: F401
from backend.api.models.quiz import Quiz, Question  # noqa: F401
from backend.api.models.quiz_attempt import QuizAttempt  # noqa: F401
from backend.api.models.progress import Progress  # noqa: F401
from backend.api.models.achievement import Achievement  # noqa: F401


def get_base():
    """
    Return the base class for SQLAlchemy models
    """
    return Base