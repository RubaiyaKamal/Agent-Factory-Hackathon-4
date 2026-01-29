"""
Pricing schemas for Course Companion FTE
Request/response models for subscription tiers and upgrades
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SubscriptionTier(BaseModel):
    """
    Information about a subscription tier
    """
    tier: str = Field(description="Tier name (free, premium, enterprise)")
    name: str = Field(description="Display name")
    price_monthly: float = Field(description="Monthly price in USD")
    price_yearly: float = Field(description="Yearly price in USD")
    features: List[str] = Field(description="List of features included")
    chapter_access: str = Field(description="Chapter access description")
    quiz_access: str = Field(description="Quiz access description")
    support_level: str = Field(description="Support level")
    is_popular: bool = Field(default=False, description="Popular tier badge")

    class Config:
        json_schema_extra = {
            "example": {
                "tier": "premium",
                "name": "Premium",
                "price_monthly": 9.99,
                "price_yearly": 99.99,
                "features": [
                    "Access to all chapters",
                    "All quizzes and assessments",
                    "Progress tracking with streaks",
                    "Email support",
                    "Certificate of completion"
                ],
                "chapter_access": "All chapters (unlimited)",
                "quiz_access": "All quizzes",
                "support_level": "Email support (24-48h)",
                "is_popular": True
            }
        }


class PricingResponse(BaseModel):
    """
    Response containing all available tiers
    """
    tiers: List[SubscriptionTier]
    current_tier: Optional[str] = Field(
        default=None,
        description="Current user's tier (if authenticated)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tiers": [],
                "current_tier": "free"
            }
        }


class UpgradeRequest(BaseModel):
    """
    Request to upgrade subscription
    """
    tier: str = Field(description="Target tier (premium or enterprise)")
    billing_cycle: str = Field(
        default="monthly",
        description="Billing cycle (monthly or yearly)"
    )
    payment_method_id: Optional[str] = Field(
        default=None,
        description="Payment method ID (mock in this version)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tier": "premium",
                "billing_cycle": "monthly",
                "payment_method_id": "pm_mock_12345"
            }
        }


class SubscriptionInfo(BaseModel):
    """
    User's current subscription information
    """
    user_id: int
    subscription_tier: str
    is_premium: bool
    subscription_start_date: Optional[datetime]
    subscription_end_date: Optional[datetime]
    billing_cycle: Optional[str]
    auto_renew: bool = Field(default=True)
    chapters_accessible: Optional[int] = Field(
        default=None,
        description="Number of chapters accessible (None = unlimited)"
    )
    features_available: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "subscription_tier": "premium",
                "is_premium": True,
                "subscription_start_date": "2024-01-15T00:00:00Z",
                "subscription_end_date": "2024-02-15T00:00:00Z",
                "billing_cycle": "monthly",
                "auto_renew": True,
                "chapters_accessible": None,
                "features_available": [
                    "Access to all chapters",
                    "All quizzes",
                    "Progress tracking",
                    "Email support"
                ]
            }
        }


class UpgradeResponse(BaseModel):
    """
    Response after successful upgrade
    """
    success: bool
    message: str
    subscription: SubscriptionInfo
    invoice_url: Optional[str] = Field(
        default=None,
        description="URL to view invoice (mock)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully upgraded to Premium tier",
                "subscription": {
                    "user_id": 1,
                    "subscription_tier": "premium",
                    "is_premium": True,
                    "subscription_start_date": "2024-01-15T00:00:00Z",
                    "subscription_end_date": "2024-02-15T00:00:00Z",
                    "billing_cycle": "monthly",
                    "auto_renew": True,
                    "chapters_accessible": None,
                    "features_available": []
                },
                "invoice_url": "/invoices/inv_mock_12345"
            }
        }


class CancelSubscriptionResponse(BaseModel):
    """
    Response after subscription cancellation
    """
    success: bool
    message: str
    subscription: SubscriptionInfo

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Subscription cancelled. Access continues until 2024-02-15",
                "subscription": {
                    "user_id": 1,
                    "subscription_tier": "premium",
                    "is_premium": True,
                    "subscription_start_date": "2024-01-15T00:00:00Z",
                    "subscription_end_date": "2024-02-15T00:00:00Z",
                    "billing_cycle": "monthly",
                    "auto_renew": False,
                    "chapters_accessible": None,
                    "features_available": []
                }
            }
        }
