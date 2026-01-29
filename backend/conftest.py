"""
Pytest configuration and fixtures for Course Companion FTE
Defines reusable fixtures for unit and integration tests
"""
import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import tempfile
import os

from backend.main import app
from backend.core.config import get_settings
from backend.db.base import Base
from backend.db.session import get_db_session, db_manager


# Override the database URL for testing
@pytest.fixture(scope="session")
def db_url():
    # Use an in-memory SQLite database for testing
    return "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(db_url):
    # Temporarily override the database URL for testing
    original_url = get_settings().DATABASE_URL
    get_settings().DATABASE_URL = db_url

    yield

    # Restore original URL after tests
    get_settings().DATABASE_URL = original_url


@pytest.fixture(scope="session")
async def async_engine(db_url):
    engine = create_async_engine(db_url, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def tables(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session(async_engine, tables):
    async_session_local = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_local() as session:
        yield session


@pytest.fixture
async def client(async_session):
    """
    Test client fixture that overrides the database session dependency
    """
    async def override_get_db_session():
        yield async_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

    # Clean up the override after the test
    app.dependency_overrides.clear()


@pytest.fixture
def test_client(async_session):
    """
    Synchronous test client using TestClient (for FastAPI's default test client)
    """
    def override_get_db_session():
        yield async_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    with TestClient(app) as test_client:
        yield test_client

    # Clean up the override after the test
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(client, test_user_data):
    """
    Fixture that provides authenticated headers for API requests
    """
    # Register a test user
    register_response = await client.post("/auth/register", json=test_user_data)

    # Login to get tokens
    login_response = await client.post("/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })

    assert login_response.status_code == 200
    tokens = login_response.json()

    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
def test_user_data():
    """
    Sample user data for testing
    """
    return {
        "email": "test@example.com",
        "password": "securepassword123",
        "timezone": "UTC"
    }


@pytest.fixture
def sample_course():
    """
    Sample course data for testing
    """
    return {
        "title": "Introduction to AI Agents",
        "description": "Learn the fundamentals of AI agent development",
        "difficulty": "beginner",
        "total_chapters": 5
    }


@pytest.fixture
def sample_chapter():
    """
    Sample chapter data for testing
    """
    return {
        "chapter_number": 1,
        "title": "Getting Started with AI Agents",
        "content_key": "courses/ai-agents/chapter-1.md",
        "duration": 30  # minutes
    }


@pytest.fixture
async def sample_authenticated_user(async_session):
    """
    Creates a sample authenticated user in the database
    """
    from backend.api.models.user import User
    from backend.core.security import hash_password

    user = User(
        email="sample@test.com",
        hashed_password=hash_password("password123"),
        tier="free",
        timezone="UTC"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    return user