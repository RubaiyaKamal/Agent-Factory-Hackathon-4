"""
Premium Feature Access Controller for Phase 2 Hybrid Intelligence Features

This module provides functionality for controlling access to premium features
based on user subscription status and feature availability.
"""

from typing import Dict, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, create_engine, Session, select
import datetime


class FeatureType(str, Enum):
    """Enumeration of available premium features."""
    ADAPTIVE_LEARNING_PATH = "adaptive_learning_path"
    LLM_GRADED_ASSESSMENTS = "llm_graded_assessments"


class UserSubscription(SQLModel, table=True):
    """
    Database model for storing user subscription information.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True)
    is_premium: bool = False
    subscription_tier: str = "free"  # free, premium, enterprise
    subscription_start_date: Optional[datetime.datetime] = None
    subscription_end_date: Optional[datetime.datetime] = None
    max_monthly_tokens: Optional[int] = 100000  # Default for premium users
    used_monthly_tokens: int = 0


class PremiumFeatureAccess:
    """
    Service class for managing access to premium features.
    """

    def __init__(self, db_url: str):
        """
        Initialize the premium feature access controller with database connection.

        Args:
            db_url: Database connection URL
        """
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)  # Create tables if they don't exist

    def check_feature_access(self, user_id: str, feature: FeatureType) -> Dict[str, bool]:
        """
        Check if a user has access to a specific premium feature.

        Args:
            user_id: User ID to check access for
            feature: Feature to check access for

        Returns:
            Dictionary with access status and reason
        """
        with Session(self.engine) as session:
            # Get user subscription info
            statement = select(UserSubscription).where(UserSubscription.user_id == user_id)
            user_subscription = session.exec(statement).first()

            if not user_subscription:
                # User doesn't exist in subscription table, default to no premium access
                return {
                    "has_access": False,
                    "is_subscribed": False,
                    "reason": "User not found in subscription system"
                }

            if not user_subscription.is_premium:
                return {
                    "has_access": False,
                    "is_subscribed": False,
                    "reason": "User does not have premium subscription"
                }

            # Check if user has exceeded their monthly token limit
            if (user_subscription.max_monthly_tokens and
                user_subscription.used_monthly_tokens >= user_subscription.max_monthly_tokens):
                return {
                    "has_access": False,
                    "is_subscribed": True,
                    "reason": "Monthly token limit exceeded"
                }

            # All checks passed, user has access
            return {
                "has_access": True,
                "is_subscribed": True,
                "reason": "Access granted"
            }

    def grant_premium_access(self, user_id: str, tier: str = "premium", duration_days: int = 30) -> UserSubscription:
        """
        Grant premium access to a user.

        Args:
            user_id: User ID to grant access to
            tier: Subscription tier (default: premium)
            duration_days: Duration of subscription in days (default: 30)

        Returns:
            Updated UserSubscription object
        """
        with Session(self.engine) as session:
            # Check if user already exists in subscription table
            statement = select(UserSubscription).where(UserSubscription.user_id == user_id)
            existing_subscription = session.exec(statement).first()

            start_date = datetime.datetime.now(datetime.timezone.utc)
            end_date = start_date + datetime.timedelta(days=duration_days)

            if existing_subscription:
                # Update existing subscription
                existing_subscription.is_premium = True
                existing_subscription.subscription_tier = tier
                existing_subscription.subscription_start_date = start_date
                existing_subscription.subscription_end_date = end_date
                existing_subscription.used_monthly_tokens = 0

                # Set token limit based on tier
                if tier == "premium":
                    existing_subscription.max_monthly_tokens = 100000
                elif tier == "enterprise":
                    existing_subscription.max_monthly_tokens = 1000000
                else:
                    existing_subscription.max_monthly_tokens = 10000  # Free tier limit

                session.add(existing_subscription)
            else:
                # Create new subscription
                token_limit = 100000 if tier == "premium" else 1000000 if tier == "enterprise" else 10000
                new_subscription = UserSubscription(
                    user_id=user_id,
                    is_premium=True,
                    subscription_tier=tier,
                    subscription_start_date=start_date,
                    subscription_end_date=end_date,
                    max_monthly_tokens=token_limit,
                    used_monthly_tokens=0
                )
                session.add(new_subscription)

            session.commit()

            # Return the updated/created subscription
            if existing_subscription:
                session.refresh(existing_subscription)
                return existing_subscription
            else:
                session.refresh(new_subscription)
                return new_subscription

    def revoke_premium_access(self, user_id: str) -> UserSubscription:
        """
        Revoke premium access from a user.

        Args:
            user_id: User ID to revoke access from

        Returns:
            Updated UserSubscription object
        """
        with Session(self.engine) as session:
            statement = select(UserSubscription).where(UserSubscription.user_id == user_id)
            user_subscription = session.exec(statement).first()

            if not user_subscription:
                # Create a subscription record if it doesn't exist
                user_subscription = UserSubscription(
                    user_id=user_id,
                    is_premium=False,
                    subscription_tier="free",
                    max_monthly_tokens=10000,  # Default free tier limit
                    used_monthly_tokens=0
                )
                session.add(user_subscription)
            else:
                # Update existing subscription
                user_subscription.is_premium = False
                user_subscription.subscription_tier = "free"
                user_subscription.subscription_end_date = datetime.datetime.now(datetime.timezone.utc)

                # Reset token usage but keep the historical data
                user_subscription.used_monthly_tokens = 0
                user_subscription.max_monthly_tokens = 10000  # Free tier limit

            session.commit()
            session.refresh(user_subscription)

            return user_subscription

    def increment_token_usage(self, user_id: str, tokens_used: int) -> bool:
        """
        Increment the token usage for a user.

        Args:
            user_id: User ID to increment token usage for
            tokens_used: Number of tokens to add to usage

        Returns:
            True if successful, False if user exceeded limit
        """
        with Session(self.engine) as session:
            statement = select(UserSubscription).where(UserSubscription.user_id == user_id)
            user_subscription = session.exec(statement).first()

            if not user_subscription:
                return False  # User not found

            # Check if adding tokens would exceed the limit
            new_usage = user_subscription.used_monthly_tokens + tokens_used
            if (user_subscription.max_monthly_tokens and
                new_usage > user_subscription.max_monthly_tokens):
                return False  # Would exceed limit

            # Increment token usage
            user_subscription.used_monthly_tokens = new_usage
            session.add(user_subscription)
            session.commit()

            return True

    def reset_monthly_usage(self, user_id: str) -> bool:
        """
        Reset the monthly token usage for a user (typically done at subscription renewal).

        Args:
            user_id: User ID to reset token usage for

        Returns:
            True if successful, False otherwise
        """
        with Session(self.engine) as session:
            statement = select(UserSubscription).where(UserSubscription.user_id == user_id)
            user_subscription = session.exec(statement).first()

            if not user_subscription:
                return False  # User not found

            user_subscription.used_monthly_tokens = 0
            session.add(user_subscription)
            session.commit()

            return True