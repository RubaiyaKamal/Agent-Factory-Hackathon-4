"""
Adaptive Learning Path Service for Phase 2 Hybrid Intelligence Features

This module provides functionality for generating personalized learning paths
based on user performance data using LLM analysis.
"""

from typing import Dict, List, Any, Optional
from .anthropic_client import AnthropicClientService, anthropic_service
from .token_tracker import TokenUsageTracker, TokenUsageCreate
from .premium_access import PremiumFeatureAccess, FeatureType
import json


class AdaptiveLearningPathService:
    """
    Service class for generating adaptive learning paths based on user performance.
    """

    def __init__(self, db_url: str):
        """
        Initialize the adaptive learning path service.

        Args:
            db_url: Database connection URL for token tracking and premium access
        """
        self.anthropic_service = anthropic_service
        self.token_tracker = TokenUsageTracker(db_url)
        self.premium_access = PremiumFeatureAccess(db_url)

    def generate_learning_path(
        self,
        user_id: str,
        user_performance_data: Dict[str, Any],
        content_catalog: Dict[str, Any],
        max_recommendations: int = 5
    ) -> Dict[str, Any]:
        """
        Generate an adaptive learning path for a user based on their performance.

        Args:
            user_id: User ID requesting the learning path
            user_performance_data: User's learning history and performance data
            content_catalog: Available content catalog
            max_recommendations: Maximum number of recommendations to generate

        Returns:
            Dictionary containing personalized learning path recommendations
        """
        # Check if user has access to this premium feature
        access_result = self.premium_access.check_feature_access(user_id, FeatureType.ADAPTIVE_LEARNING_PATH)

        if not access_result["has_access"]:
            return {
                "error": "Access denied",
                "message": access_result["reason"],
                "recommendations": []
            }

        # Generate the learning path using the Anthropic API
        response = self.anthropic_service.generate_adaptive_learning_path(
            user_performance_data,
            content_catalog
        )

        # Record token usage
        usage_record = TokenUsageCreate(
            user_id=user_id,
            feature=FeatureType.ADAPTIVE_LEARNING_PATH.value,
            input_tokens=response["input_tokens"],
            output_tokens=response["output_tokens"],
            total_tokens=response["total_tokens"],
            cost_usd=0,  # Will be calculated by the tracker
            model_used=response["model"]
        )

        self.token_tracker.record_usage(usage_record)

        # Increment user's token usage
        self.premium_access.increment_token_usage(user_id, response["total_tokens"])

        # Parse the response to extract structured recommendations
        try:
            # Attempt to parse the response for structured recommendations
            recommendations_text = response["content"]

            # This is a simplified parsing - in a real implementation,
            # we would have a more robust way to extract structured data
            # from the LLM response
            recommendations = self._parse_recommendations(recommendations_text, max_recommendations)

            return {
                "user_id": user_id,
                "recommendations": recommendations,
                "token_usage": {
                    "input_tokens": response["input_tokens"],
                    "output_tokens": response["output_tokens"],
                    "total_tokens": response["total_tokens"]
                },
                "cost_usd": usage_record.cost_usd
            }
        except Exception as e:
            # If parsing fails, return the raw content with an error
            return {
                "user_id": user_id,
                "recommendations": [],
                "raw_response": response["content"],
                "error": f"Failed to parse recommendations: {str(e)}"
            }

    def _parse_recommendations(self, recommendations_text: str, max_recommendations: int) -> List[Dict[str, Any]]:
        """
        Parse the LLM response to extract structured recommendations.

        Args:
            recommendations_text: Raw text response from the LLM
            max_recommendations: Maximum number of recommendations to extract

        Returns:
            List of structured recommendation dictionaries
        """
        # This is a simplified parsing implementation
        # In a real implementation, we would use more sophisticated parsing
        # or potentially have the LLM return JSON directly

        recommendations = []

        # Split the response into paragraphs/sections
        sections = recommendations_text.split('\n\n')

        for section in sections[:max_recommendations]:
            # Simple heuristic to identify recommendation-like content
            if any(keyword in section.lower() for keyword in ['next', 'recommend', 'suggest', 'path', 'module']):
                # Extract title and description
                lines = section.strip().split('\n')
                title = lines[0].strip(' .#-') if lines else "Learning Module"

                # Remove the title line and join the rest as description
                description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else section

                recommendations.append({
                    "title": title,
                    "description": description,
                    "priority": len(recommendations) + 1  # Higher priority = more recommended
                })

        return recommendations[:max_recommendations]

    def get_user_learning_history(self, user_id: str) -> Dict[str, Any]:
        """
        Get the user's learning history for use in generating recommendations.

        Args:
            user_id: User ID to get learning history for

        Returns:
            Dictionary containing user's learning history
        """
        # In a real implementation, this would fetch from the actual learning database
        # For now, returning a mock structure
        return {
            "user_id": user_id,
            "completed_modules": [],
            "assessment_scores": {},
            "time_spent": {},
            "preferred_topics": [],
            "areas_of_difficulty": [],
            "learning_style_indicators": {}
        }

    def get_content_catalog(self) -> Dict[str, Any]:
        """
        Get the available content catalog for generating recommendations.

        Returns:
            Dictionary containing available learning content
        """
        # In a real implementation, this would fetch from the actual content database
        # For now, returning a mock structure
        return {
            "modules": [],
            "categories": [],
            "difficulty_levels": [],
            "prerequisites": {},
            "learning_paths": []
        }