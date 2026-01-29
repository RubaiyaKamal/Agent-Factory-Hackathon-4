"""
Script to run Alembic migrations for Course Companion FTE
"""
import os
import sys
from pathlib import Path

# Add the project root to the path so we can import backend modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from alembic import command
from alembic.config import Config
from backend.core.config import get_settings


def run_migrations():
    """
    Run Alembic migrations to create/update database schema
    """
    # Create alembic config
    alembic_cfg = Config(str(project_root / "alembic.ini"))

    # Set the database URL from settings
    settings = get_settings()

    # Replace the async SQLite URL with sync version for migration
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite+aiosqlite://"):
        # Convert to sync SQLite URL
        db_url = db_url.replace("sqlite+aiosqlite://", "sqlite://", 1)

    alembic_cfg.set_main_option("sqlalchemy.url", db_url)

    # Run the upgrade to create all tables
    command.upgrade(alembic_cfg, "head")
    print("✅ Database migrations completed successfully!")


if __name__ == "__main__":
    run_migrations()