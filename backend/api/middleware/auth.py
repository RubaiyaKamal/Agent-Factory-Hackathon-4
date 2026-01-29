"""
Authentication middleware for Course Companion FTE
Provides JWT-based authentication and user retrieval
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import decode_token
from backend.db.session import get_db_session
from backend.api.models.user import User
from backend.core.exceptions import AuthenticationError


# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db_session)
) -> User:
    """
    Get the current authenticated user from the JWT token

    Args:
        credentials: HTTP Authorization header containing the JWT token
        db: Database session

    Returns:
        User object if token is valid and user exists

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    # Decode the token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # Extract user ID from token
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Query user from database
    try:
        user = await db.get(User, int(user_id))
        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise credentials_exception

        return user
    except ValueError:
        # Invalid user ID in token
        raise credentials_exception
    except Exception:
        # Database error
        raise credentials_exception


async def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token without retrieving user (for public endpoints that need token validation)

    Args:
        credentials: HTTP Authorization header containing the JWT token

    Returns:
        Decoded token payload if valid

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# Optional security scheme (doesn't require authentication)
from fastapi.security import HTTPBearer as HTTPBearerOptional


security_optional = HTTPBearerOptional(auto_error=False)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: AsyncSession = Depends(get_db_session)
) -> Optional[User]:
    """
    Get the current authenticated user from JWT token (optional)

    This function is similar to get_current_user but returns None instead of
    raising an exception when no token is provided. Useful for endpoints that
    work differently for authenticated vs unauthenticated users.

    Args:
        credentials: Optional HTTP Authorization header containing the JWT token
        db: Database session

    Returns:
        User object if token is valid and user exists, None if no token provided

    Raises:
        HTTPException: If token is provided but invalid/expired
    """
    # If no credentials provided, return None (unauthenticated)
    if credentials is None:
        return None

    token = credentials.credentials

    # Decode the token
    payload = decode_token(token)
    if payload is None:
        # Token is provided but invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user ID from token
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Query user from database
    try:
        user = await db.get(User, int(user_id))
        if user is None:
            return None

        if not user.is_active:
            return None

        return user
    except ValueError:
        # Invalid user ID in token
        return None
    except Exception:
        # Database error
        return None