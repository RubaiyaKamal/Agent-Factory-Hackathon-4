"""
Authentication routes for Course Companion FTE
Handles user registration, login, and token refresh
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from backend.api.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from backend.db.session import get_db_session
from backend.api.models.user import User
from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from backend.core.config import get_settings
from backend.api.middleware.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db_session)
) -> Dict:
    """
    Register a new user account and return authentication token

    Args:
        request: Registration request containing email and password
        db: Database session

    Returns:
        Dictionary with token and user information for automatic login

    Raises:
        HTTPException: If email is already taken
    """
    # Check if user already exists
    from sqlalchemy import select
    result = await db.execute(select(User).filter(User.email == request.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(request.password)

    # Create new user
    user = User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password,
        tier="free",  # Default to free tier
        timezone=request.timezone or "UTC"
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Create access token for automatic login
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    # Return token and user info for automatic login after registration
    return {
        "token": access_token,
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "tier": user.tier
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db_session)
) -> TokenResponse:
    """
    Authenticate user and return JWT tokens

    Args:
        request: Login request containing email and password
        db: Database session

    Returns:
        TokenResponse containing access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    from sqlalchemy import select
    result = await db.execute(select(User).filter(User.email == request.email))
    user = result.scalar_one_or_none()

    # Verify credentials
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    # Create refresh token
    refresh_token_expires = timedelta(days=get_settings().REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=refresh_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=access_token_expires.total_seconds()
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: Dict[str, str],
    db: AsyncSession = Depends(get_db_session)
) -> TokenResponse:
    """
    Refresh access token using refresh token

    Args:
        refresh_request: Contains refresh_token
        db: Database session

    Returns:
        TokenResponse with new access token and same refresh token

    Raises:
        HTTPException: If refresh token is invalid
    """
    from backend.core.security import decode_token

    refresh_token_str = refresh_request.get("refresh_token")
    if not refresh_token_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Decode refresh token
    payload = decode_token(refresh_token_str)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify user still exists and is active
    user = await db.get(User, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists or is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    # Return new access token with same refresh token
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,  # Return same refresh token
        token_type="bearer",
        expires_in=access_token_expires.total_seconds()
    )


@router.get("/me", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current user's profile information

    Args:
        current_user: Authenticated user (injected by auth middleware)

    Returns:
        UserResponse with user information
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        tier=current_user.tier,
        timezone=current_user.timezone,
        created_at=current_user.created_at,
        is_active=current_user.is_active
    )