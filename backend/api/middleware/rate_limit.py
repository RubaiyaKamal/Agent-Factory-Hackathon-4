"""
Rate limiting middleware for Course Companion FTE
Implements tier-based rate limiting using Redis
"""
from fastapi import Request, HTTPException, status, Depends
from typing import Callable, Optional
import time
import json
from redis.asyncio import Redis
from backend.core.config import get_settings
from backend.api.models.user import User
from backend.api.middleware.auth import get_current_user
from backend.core.exceptions import RateLimitError


class RateLimiter:
    """
    Rate limiter implementation using Redis
    """
    def __init__(self):
        self.settings = get_settings()
        self.redis_client: Optional[Redis] = None

    async def get_redis_client(self) -> Redis:
        """
        Get Redis client instance (lazy initialization)
        """
        if self.redis_client is None:
            self.redis_client = Redis.from_url(self.settings.REDIS_URL)
        return self.redis_client

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int  # in seconds
    ) -> tuple[bool, dict]:  # (is_allowed, rate_info)
        """
        Check if the request is within rate limit

        Args:
            key: Unique identifier for the rate limit (e.g., user_id, IP address)
            limit: Maximum number of requests allowed
            window: Time window in seconds

        Returns:
            Tuple of (is_allowed, rate_info_dict)
        """
        redis = await self.get_redis_client()

        # Use a timestamp-based sliding window approach
        current_time = int(time.time())
        pipe = redis.pipeline()

        # Remove old entries outside the current window
        pipe.zremrangebyscore(key, 0, current_time - window)

        # Count current requests in window
        pipe.zcard(key)

        # Add current request
        pipe.zadd(key, {str(current_time): current_time})

        # Set expiration for the key
        pipe.expire(key, window)

        results = await pipe.execute()
        current_requests = results[1]

        remaining = max(0, limit - current_requests)
        reset_time = current_time + window

        rate_info = {
            "limit": limit,
            "remaining": remaining,
            "reset": reset_time
        }

        is_allowed = current_requests < limit
        return is_allowed, rate_info


# Global rate limiter instance
rate_limiter = RateLimiter()


def get_rate_limit_for_tier(tier: str) -> tuple[int, int]:
    """
    Get rate limit based on user tier

    Args:
        tier: User's subscription tier ('free', 'premium', 'pro', 'team')

    Returns:
        Tuple of (limit, window_in_seconds)
    """
    settings = get_settings()

    if tier == "premium":
        return settings.PREMIUM_TIER_RATE_LIMIT, settings.RATE_LIMIT_WINDOW
    elif tier == "pro":
        return settings.PRO_TIER_RATE_LIMIT, settings.RATE_LIMIT_WINDOW
    elif tier == "team":
        return settings.PRO_TIER_RATE_LIMIT * 2, settings.RATE_LIMIT_WINDOW  # Assuming team gets higher limits
    else:  # free tier
        return settings.FREE_TIER_RATE_LIMIT, settings.RATE_LIMIT_WINDOW


async def rate_limit_by_user(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Rate limit based on authenticated user ID

    Args:
        request: FastAPI request object
        current_user: Authenticated user

    Returns:
        Rate limit info dictionary

    Raises:
        HTTPException: If rate limit is exceeded
    """
    settings = get_settings()

    if not settings.RATE_LIMIT_ENABLED:
        return {"limit": 9999, "remaining": 9999, "reset": int(time.time()) + 60}

    limit, window = get_rate_limit_for_tier(current_user.tier)
    key = f"rate_limit:user:{current_user.id}"

    is_allowed, rate_info = await rate_limiter.check_rate_limit(key, limit, window)

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "limit": rate_info["limit"],
                "reset": rate_info["reset"]
            }
        )

    return rate_info


async def rate_limit_by_ip(
    request: Request
) -> dict:
    """
    Rate limit based on IP address

    Args:
        request: FastAPI request object

    Returns:
        Rate limit info dictionary

    Raises:
        HTTPException: If rate limit is exceeded
    """
    settings = get_settings()

    if not settings.RATE_LIMIT_ENABLED:
        return {"limit": 9999, "remaining": 9999, "reset": int(time.time()) + 60}

    # Get client IP (considering proxy headers)
    client_ip = request.client.host if request.client else "unknown"

    # Use default rate limit for IP-based limiting
    limit = settings.RATE_LIMIT_REQUESTS
    window = settings.RATE_LIMIT_WINDOW
    key = f"rate_limit:ip:{client_ip}"

    is_allowed, rate_info = await rate_limiter.check_rate_limit(key, limit, window)

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "limit": rate_info["limit"],
                "reset": rate_info["reset"]
            }
        )

    return rate_info


def get_rate_limit_dependency(
    limit_type: str = "user"
) -> Callable:
    """
    Factory function to create rate limit dependencies

    Args:
        limit_type: Type of rate limiting ('user' or 'ip')

    Returns:
        Dependency function for FastAPI
    """
    if limit_type == "user":
        return rate_limit_by_user
    elif limit_type == "ip":
        return rate_limit_by_ip
    else:
        raise ValueError(f"Invalid rate limit type: {limit_type}")


# Utility function to add rate limit headers to responses
async def add_rate_limit_headers(response, rate_info: dict):
    """
    Add rate limit information to response headers

    Args:
        response: FastAPI response object
        rate_info: Rate limit information from rate limiter
    """
    if response:
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset"])