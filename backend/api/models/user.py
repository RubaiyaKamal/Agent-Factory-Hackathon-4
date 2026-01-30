"""
User model for Course Companion FTE
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User model - stores user authentication and tier information.

    Phase 1 Fields:
    - Basic authentication (email, password)
    - Tier management (free, premium, pro, team)
    - Timezone for progress tracking
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)

    # Tier management
    tier: str = Field(default="free", max_length=20)  # free|premium|pro|team
    tier_expires_at: Optional[datetime] = Field(default=None)

    # User preferences
    timezone: str = Field(default="UTC", max_length=50)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "tier": "free",
                "timezone": "America/New_York"
            }
        }
