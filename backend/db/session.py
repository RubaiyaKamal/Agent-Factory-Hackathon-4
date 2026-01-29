"""
Database session management for Course Companion FTE
Creates async SQLModel engine and session factory
"""
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from backend.core.config import get_settings


class DatabaseSessionManager:
    """
    Manages database sessions and engine lifecycle
    """
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.SessionLocal: async_sessionmaker | None = None
        self._initialized = False

    def init_db(self) -> None:
        """
        Initialize database engine and session factory
        """
        if self._initialized:
            return

        settings = get_settings()

        # Create async engine
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DB_ECHO,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections every 5 minutes
        )

        # Create async session factory
        self.SessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False,
        )

        self._initialized = True

    async def close(self) -> None:
        """
        Close database engine connection
        """
        if self.engine:
            await self.engine.dispose()


# Global session manager instance
db_manager = DatabaseSessionManager()


async def get_db_session():
    """
    Dependency to provide database session to FastAPI endpoints
    """
    if not db_manager._initialized:
        db_manager.init_db()

    async with db_manager.SessionLocal() as session:
        yield session


# Convenience functions for direct access
def get_engine():
    """
    Get the database engine directly
    """
    if not db_manager._initialized:
        db_manager.init_db()
    return db_manager.engine


def get_sessionmaker():
    """
    Get the session maker directly
    """
    if not db_manager._initialized:
        db_manager.init_db()
    return db_manager.SessionLocal