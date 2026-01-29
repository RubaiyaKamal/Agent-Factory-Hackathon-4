"""
Pricing routes for Course Companion FTE
Handles subscription tiers, upgrades, and billing (mock implementation)
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.api.schemas.pricing import (
    PricingResponse,
    SubscriptionTier,
    UpgradeRequest,
    UpgradeResponse,
    SubscriptionInfo,
    CancelSubscriptionResponse
)
from backend.api.models.user import User
from backend.db.session import get_db_session
from backend.api.middleware.auth import get_current_user, get_current_user_optional
from backend.api.middleware.access import is_premium_user, get_accessible_chapter_count


router = APIRouter(prefix="/pricing", tags=["pricing"])


# Tier definitions
TIER_DEFINITIONS = [
    {
        "tier": "free",
        "name": "Free",
        "price_monthly": 0.0,
        "price_yearly": 0.0,
        "features": [
            "Access to first 3 chapters",
            "Basic quizzes",
            "Progress tracking",
            "Community support"
        ],
        "chapter_access": "First 3 chapters only",
        "quiz_access": "Quizzes for free chapters",
        "support_level": "Community support",
        "is_popular": False
    },
    {
        "tier": "premium",
        "name": "Premium",
        "price_monthly": 9.99,
        "price_yearly": 99.99,
        "features": [
            "Access to all chapters",
            "All quizzes and assessments",
            "Advanced progress tracking",
            "Streak achievements",
            "Email support (24-48h)",
            "Certificate of completion",
            "Downloadable resources"
        ],
        "chapter_access": "All chapters (unlimited)",
        "quiz_access": "All quizzes",
        "support_level": "Email support (24-48h)",
        "is_popular": True
    },
    {
        "tier": "enterprise",
        "name": "Enterprise",
        "price_monthly": 49.99,
        "price_yearly": 499.99,
        "features": [
            "Everything in Premium",
            "Priority support (4h response)",
            "Custom learning paths",
            "Team management (up to 50 users)",
            "Advanced analytics",
            "API access",
            "Custom integrations",
            "Dedicated account manager"
        ],
        "chapter_access": "All chapters (unlimited)",
        "quiz_access": "All quizzes + custom assessments",
        "support_level": "Priority support (4h response)",
        "is_popular": False
    }
]


@router.get("", response_model=PricingResponse)
@router.get("/tiers", response_model=PricingResponse)
async def get_pricing_tiers(
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> PricingResponse:
    """
    Get all available subscription tiers

    Returns pricing information for all tiers including:
    - Free: First 3 chapters
    - Premium: All chapters + advanced features
    - Enterprise: Premium + team features

    Authentication is optional. If authenticated, includes current tier.

    Returns:
        PricingResponse with all tiers and optional current tier
    """
    tiers = [SubscriptionTier(**tier_def) for tier_def in TIER_DEFINITIONS]

    return PricingResponse(
        tiers=tiers,
        current_tier=current_user.subscription_tier if current_user else None
    )


@router.get("/subscription", response_model=SubscriptionInfo)
async def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> SubscriptionInfo:
    """
    Get current user's subscription information

    Returns detailed subscription information including:
    - Current tier and status
    - Billing cycle and renewal date
    - Features available
    - Chapter access limits

    Args:
        current_user: Authenticated user (required)

    Returns:
        SubscriptionInfo with subscription details

    Raises:
        HTTPException 401: If not authenticated
    """
    # Get tier definition for features
    tier_def = next(
        (t for t in TIER_DEFINITIONS if t["tier"] == current_user.subscription_tier),
        TIER_DEFINITIONS[0]  # Default to free
    )

    # Determine accessible chapters
    accessible_chapters = get_accessible_chapter_count(current_user)

    # Build subscription info
    return SubscriptionInfo(
        user_id=current_user.id,
        subscription_tier=current_user.subscription_tier,
        is_premium=is_premium_user(current_user),
        subscription_start_date=current_user.subscription_start_date,
        subscription_end_date=current_user.subscription_end_date,
        billing_cycle="monthly" if current_user.subscription_tier != "free" else None,
        auto_renew=True,
        chapters_accessible=accessible_chapters,
        features_available=tier_def["features"]
    )


@router.post("/upgrade", response_model=UpgradeResponse)
async def upgrade_subscription(
    request: UpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> UpgradeResponse:
    """
    Upgrade user's subscription tier

    **NOTE**: This is a mock implementation for Phase 1.
    In production, this would integrate with a payment processor (Stripe, etc.)

    Args:
        request: Upgrade request with target tier and billing cycle
        current_user: Authenticated user (required)

    Returns:
        UpgradeResponse with new subscription details

    Raises:
        HTTPException 400: Invalid tier or already subscribed
        HTTPException 401: If not authenticated
    """
    # Validate target tier
    valid_tiers = ["premium", "enterprise"]
    if request.tier not in valid_tiers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_tier",
                "message": f"Invalid tier. Must be one of: {', '.join(valid_tiers)}",
                "valid_tiers": valid_tiers
            }
        )

    # Check if already on target tier
    if current_user.subscription_tier == request.tier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "already_subscribed",
                "message": f"You are already subscribed to {request.tier} tier",
                "current_tier": current_user.subscription_tier
            }
        )

    # Validate billing cycle
    if request.billing_cycle not in ["monthly", "yearly"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_billing_cycle",
                "message": "Billing cycle must be 'monthly' or 'yearly'",
                "provided": request.billing_cycle
            }
        )

    # Mock payment processing
    # In production: Integrate with Stripe/PayPal/etc.
    # payment_intent = stripe.PaymentIntent.create(...)

    # Update user subscription
    now = datetime.utcnow()
    duration_days = 30 if request.billing_cycle == "monthly" else 365

    current_user.subscription_tier = request.tier
    current_user.subscription_start_date = now
    current_user.subscription_end_date = now + timedelta(days=duration_days)
    current_user.is_premium = True

    await db.commit()
    await db.refresh(current_user)

    # Get tier features
    tier_def = next(t for t in TIER_DEFINITIONS if t["tier"] == request.tier)

    # Build subscription info
    subscription = SubscriptionInfo(
        user_id=current_user.id,
        subscription_tier=current_user.subscription_tier,
        is_premium=True,
        subscription_start_date=current_user.subscription_start_date,
        subscription_end_date=current_user.subscription_end_date,
        billing_cycle=request.billing_cycle,
        auto_renew=True,
        chapters_accessible=None,  # Unlimited
        features_available=tier_def["features"]
    )

    return UpgradeResponse(
        success=True,
        message=f"Successfully upgraded to {request.tier.title()} tier",
        subscription=subscription,
        invoice_url=f"/invoices/inv_mock_{current_user.id}_{int(now.timestamp())}"
    )


@router.post("/cancel", response_model=CancelSubscriptionResponse)
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> CancelSubscriptionResponse:
    """
    Cancel user's subscription

    Cancels auto-renewal but maintains access until end of billing period.

    **NOTE**: This is a mock implementation for Phase 1.
    In production, this would update payment processor subscription.

    Args:
        current_user: Authenticated user (required)

    Returns:
        CancelSubscriptionResponse with updated subscription

    Raises:
        HTTPException 400: If not subscribed to premium
        HTTPException 401: If not authenticated
    """
    # Check if user has premium subscription
    if current_user.subscription_tier == "free":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "not_subscribed",
                "message": "You do not have an active subscription to cancel",
                "current_tier": "free"
            }
        )

    # Mock cancellation
    # In production: stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)

    # User keeps access until end date, but no renewal
    end_date = current_user.subscription_end_date

    # Get tier features
    tier_def = next(
        t for t in TIER_DEFINITIONS if t["tier"] == current_user.subscription_tier
    )

    # Build subscription info (still active until end date)
    subscription = SubscriptionInfo(
        user_id=current_user.id,
        subscription_tier=current_user.subscription_tier,
        is_premium=True,  # Still premium until end date
        subscription_start_date=current_user.subscription_start_date,
        subscription_end_date=end_date,
        billing_cycle=None,
        auto_renew=False,  # Cancelled
        chapters_accessible=None,
        features_available=tier_def["features"]
    )

    await db.commit()

    return CancelSubscriptionResponse(
        success=True,
        message=f"Subscription cancelled. Access continues until {end_date.strftime('%Y-%m-%d')}",
        subscription=subscription
    )


@router.get("/features/{tier}", response_model=SubscriptionTier)
async def get_tier_features(tier: str) -> SubscriptionTier:
    """
    Get detailed features for a specific tier

    Useful for displaying tier comparison or feature lists.

    Args:
        tier: Tier name (free, premium, or enterprise)

    Returns:
        SubscriptionTier with detailed features

    Raises:
        HTTPException 404: If tier not found
    """
    tier_def = next(
        (t for t in TIER_DEFINITIONS if t["tier"] == tier.lower()),
        None
    )

    if not tier_def:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "tier_not_found",
                "message": f"Tier '{tier}' not found",
                "valid_tiers": ["free", "premium", "enterprise"]
            }
        )

    return SubscriptionTier(**tier_def)
