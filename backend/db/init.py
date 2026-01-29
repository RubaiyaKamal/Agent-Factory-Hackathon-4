"""
Database initialization for Course Companion FTE

Creates all tables based on SQLModel models.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from backend.core.config import get_settings
from backend.api.models import (
    Achievement,
    Chapter,
    Course,
    Progress,
    Question,
    Quiz,
    QuizAttempt,
    User,
)


async def init_db() -> None:
    """
    Initialize database - create all tables.

    This is idempotent - safe to run multiple times.
    Only creates tables that don't exist.
    """
    settings = get_settings()

    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        future=True
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    await engine.dispose()

    print("[OK] Database initialized successfully")
    print(f"   Tables created: {len(SQLModel.metadata.tables)}")
    print(f"   Database URL: {settings.DATABASE_URL}")


async def drop_db() -> None:
    """
    Drop all tables - USE WITH CAUTION!

    Only for development/testing.
    """
    settings = get_settings()

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()

    print("[WARN] Database dropped successfully")


if __name__ == "__main__":
    # Run from command line: python -m backend.db.init
    asyncio.run(init_db())
