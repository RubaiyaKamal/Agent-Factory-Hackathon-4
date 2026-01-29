"""
Anthropic API Client Service for Phase 2 Hybrid Intelligence Features

This module provides a service for interacting with the Anthropic API,
including token usage tracking and error handling for premium features.
"""

import os
import logging
from typing import Dict, Optional, Any
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class AnthropicClientService:
    """
    Service class for interacting with the Anthropic API.

    Handles API communication, token usage tracking, and error management
    for premium LLM-powered features.
    """

    def __init__(self):
        """Initialize the Anthropic client with API key from environment."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-sonnet-20240229"  # Using Sonnet as per constitutional requirements

    def get_token_count(self, text: str) -> int:
        """
        Get approximate token count for a given text.

        Args:
            text: Input text to count tokens for

        Returns:
            Number of tokens in the text
        """
        return self.client.count_tokens(text)

    def generate_content(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate content using the Anthropic API.

        Args:
            prompt: Input prompt for content generation
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature for generation

        Returns:
            Dictionary containing response and token usage information
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            # Calculate token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens

            return {
                "content": response.content[0].text if response.content else "",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "model": self.model
            }

        except Exception as e:
            logger.error(f"Error calling Anthropic API: {str(e)}")
            raise

    def generate_adaptive_learning_path(
        self,
        user_performance_data: Dict[str, Any],
        content_catalog: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate adaptive learning path based on user performance.

        Args:
            user_performance_data: User's learning history and performance
            content_catalog: Available content catalog

        Returns:
            Personalized learning path recommendations
        """
        prompt = f"""
        Based on the following user performance data and content catalog,
        recommend a personalized learning path:

        User Performance Data:
        {user_performance_data}

        Content Catalog:
        {content_catalog}

        Please provide specific recommendations for the next learning modules
        that would best suit this user's needs, considering their strengths
        and areas for improvement.
        """

        return self.generate_content(prompt, max_tokens=500)

    def grade_assessment(
        self,
        question: str,
        user_answer: str,
        rubric: str
    ) -> Dict[str, Any]:
        """
        Grade a free-form assessment answer using LLM evaluation.

        Args:
            question: The original assessment question
            user_answer: The user's answer to the question
            rubric: Grading rubric to evaluate the answer against

        Returns:
            Grading results with score and feedback
        """
        prompt = f"""
        Please grade the following answer according to the provided rubric:

        Question: {question}

        User Answer: {user_answer}

        Rubric: {rubric}

        Provide a score (out of 100) and detailed feedback explaining the score
        and suggestions for improvement.
        """

        return self.generate_content(prompt, max_tokens=800)


# Singleton instance
anthropic_service = AnthropicClientService()