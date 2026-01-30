"""
Pydantic schemas for authentication in Course Companion FTE
Defines request and response models for auth endpoints
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class RegisterRequest(BaseModel):
    """
    Request schema for user registration
    """
    name: str
    email: EmailStr
    password: str
    timezone: Optional[str] = "UTC"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "student@example.com",
                "password": "securePassword123",
                "timezone": "America/New_York"
            }
        }


class LoginRequest(BaseModel):
    """
    Request schema for user login
    """
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "password": "securePassword123"
            }
        }


class TokenResponse(BaseModel):
    """
    Response schema for authentication tokens
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int  # seconds

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class UserResponse(BaseModel):
    """
    Response schema for user information
    """
    id: int
    name: str
    email: EmailStr
    tier: str
    timezone: str
    created_at: datetime
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "student@example.com",
                "tier": "free",
                "timezone": "UTC",
                "created_at": "2023-01-01T00:00:00Z",
                "is_active": True
            }
        }