"""
Token Usage Tracker for Phase 2 Hybrid Intelligence Features

This module provides functionality for tracking token usage per user
and per feature, enabling cost calculation and monitoring.
"""

import datetime
from typing import Dict, List, Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import Column, DateTime
from pydantic import BaseModel


class TokenUsageRecord(SQLModel, table=True):
    """
    Database model for storing token usage records.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    feature: str  # adaptive_learning_path, llm_grading, etc.
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float  # Calculated cost based on token usage
    timestamp: datetime.datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    model_used: str


class TokenUsageCreate(BaseModel):
    """
    Pydantic model for creating token usage records.
    """
    user_id: str
    feature: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    model_used: str


class TokenUsageTracker:
    """
    Service class for tracking and managing token usage for cost calculation.
    """

    def __init__(self, db_url: str):
        """
        Initialize the token usage tracker with database connection.

        Args:
            db_url: Database connection URL
        """
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)  # Create tables if they don't exist

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "claude-3-sonnet-20240229") -> float:
        """
        Calculate cost based on token usage and model.

        According to Anthropic pricing (as of 2024):
        - Claude 3 Sonnet: $3.00 per 1M input tokens, $15.00 per 1M output tokens

        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
            model: Model used for the API call

        Returns:
            Cost in USD
        """
        if model == "claude-3-sonnet-20240229":
            input_cost_per_million = 3.00
            output_cost_per_million = 15.00
        else:
            # Default to sonnet pricing if unknown model
            input_cost_per_million = 3.00
            output_cost_per_million = 15.00

        input_cost = (input_tokens / 1_000_000) * input_cost_per_million
        output_cost = (output_tokens / 1_000_000) * output_cost_per_million

        return input_cost + output_cost

    def record_usage(self, usage_create: TokenUsageCreate) -> TokenUsageRecord:
        """
        Record token usage in the database.

        Args:
            usage_create: Token usage data to record

        Returns:
            Created TokenUsageRecord
        """
        with Session(self.engine) as session:
            # Calculate cost if not provided
            if usage_create.cost_usd == 0:
                usage_create.cost_usd = self.calculate_cost(
                    usage_create.input_tokens,
                    usage_create.output_tokens,
                    usage_create.model_used
                )

            record = TokenUsageRecord(
                user_id=usage_create.user_id,
                feature=usage_create.feature,
                input_tokens=usage_create.input_tokens,
                output_tokens=usage_create.output_tokens,
                total_tokens=usage_create.total_tokens,
                cost_usd=usage_create.cost_usd,
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                model_used=usage_create.model_used
            )

            session.add(record)
            session.commit()
            session.refresh(record)

            return record

    def get_user_usage(self, user_id: str, days_back: int = 30) -> List[TokenUsageRecord]:
        """
        Get token usage for a specific user within a time range.

        Args:
            user_id: User ID to get usage for
            days_back: Number of days back to query (default 30)

        Returns:
            List of token usage records
        """
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)

        with Session(self.engine) as session:
            statement = select(TokenUsageRecord).where(
                TokenUsageRecord.user_id == user_id,
                TokenUsageRecord.timestamp >= cutoff_date
            ).order_by(TokenUsageRecord.timestamp.desc())

            results = session.exec(statement).all()
            return results

    def get_feature_usage(self, feature: str, days_back: int = 30) -> List[TokenUsageRecord]:
        """
        Get token usage for a specific feature within a time range.

        Args:
            feature: Feature name to get usage for
            days_back: Number of days back to query (default 30)

        Returns:
            List of token usage records
        """
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_back)

        with Session(self.engine) as session:
            statement = select(TokenUsageRecord).where(
                TokenUsageRecord.feature == feature,
                TokenUsageRecord.timestamp >= cutoff_date
            ).order_by(TokenUsageRecord.timestamp.desc())

            results = session.exec(statement).all()
            return results

    def get_total_cost_for_user(self, user_id: str, days_back: int = 30) -> float:
        """
        Get total cost for a user within a time range.

        Args:
            user_id: User ID to get cost for
            days_back: Number of days back to query (default 30)

        Returns:
            Total cost in USD
        """
        usage_records = self.get_user_usage(user_id, days_back)
        return sum(record.cost_usd for record in usage_records)

    def get_total_cost_for_feature(self, feature: str, days_back: int = 30) -> float:
        """
        Get total cost for a feature within a time range.

        Args:
            feature: Feature name to get cost for
            days_back: Number of days back to query (default 30)

        Returns:
            Total cost in USD
        """
        usage_records = self.get_feature_usage(feature, days_back)
        return sum(record.cost_usd for record in usage_records)