"""
LLM Grading Service for Phase 2 Hybrid Intelligence Features

This module provides functionality for grading free-form assessment answers
using LLM analysis with detailed feedback.
"""

from typing import Dict, Any, Optional, List
from .anthropic_client import AnthropicClientService, anthropic_service
from .token_tracker import TokenUsageTracker, TokenUsageCreate
from .premium_access import PremiumFeatureAccess, FeatureType
import re


class LLMGradingService:
    """
    Service class for grading free-form assessment answers using LLM analysis.
    """

    def __init__(self, db_url: str):
        """
        Initialize the LLM grading service.

        Args:
            db_url: Database connection URL for token tracking and premium access
        """
        self.anthropic_service = anthropic_service
        self.token_tracker = TokenUsageTracker(db_url)
        self.premium_access = PremiumFeatureAccess(db_url)

    def grade_assessment(
        self,
        user_id: str,
        question: str,
        user_answer: str,
        rubric: str,
        assessment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Grade a free-form assessment answer using LLM evaluation.

        Args:
            user_id: User ID submitting the answer
            question: The original assessment question
            user_answer: The user's answer to the question
            rubric: Grading rubric to evaluate the answer against
            assessment_id: Optional assessment ID for tracking

        Returns:
            Dictionary containing grading results with score and feedback
        """
        # Check if user has access to this premium feature
        access_result = self.premium_access.check_feature_access(user_id, FeatureType.LLM_GRADED_ASSESSMENTS)

        if not access_result["has_access"]:
            return {
                "error": "Access denied",
                "message": access_result["reason"],
                "grade": None
            }

        # Grade the assessment using the Anthropic API
        response = self.anthropic_service.grade_assessment(question, user_answer, rubric)

        # Record token usage
        usage_record = TokenUsageCreate(
            user_id=user_id,
            feature=FeatureType.LLM_GRADED_ASSESSMENTS.value,
            input_tokens=response["input_tokens"],
            output_tokens=response["output_tokens"],
            total_tokens=response["total_tokens"],
            cost_usd=0,  # Will be calculated by the tracker
            model_used=response["model"]
        )

        self.token_tracker.record_usage(usage_record)

        # Increment user's token usage
        self.premium_access.increment_token_usage(user_id, response["total_tokens"])

        # Parse the response to extract structured grading information
        try:
            grading_result = self._parse_grading_response(response["content"])

            return {
                "user_id": user_id,
                "assessment_id": assessment_id,
                "grade": grading_result,
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
                "assessment_id": assessment_id,
                "grade": None,
                "raw_response": response["content"],
                "error": f"Failed to parse grading response: {str(e)}"
            }

    def _parse_grading_response(self, grading_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract structured grading information.

        Args:
            grading_text: Raw text response from the LLM

        Returns:
            Dictionary containing structured grading information
        """
        # Extract score using regex patterns
        score_patterns = [
            r'score[:\s]+(\d+)',
            r'grade[:\s]+(\d+)',
            r'(\d+)\s*/\s*100',
            r'overall:\s*(\d+)'
        ]

        score = 0
        for pattern in score_patterns:
            match = re.search(pattern, grading_text, re.IGNORECASE)
            if match:
                try:
                    score = int(match.group(1))
                    break
                except (ValueError, IndexError):
                    continue

        # If no score found in the text, default to 0
        if score == 0:
            # Try to infer from common rating scales
            if 'excellent' in grading_text.lower():
                score = 90
            elif 'very good' in grading_text.lower():
                score = 80
            elif 'good' in grading_text.lower():
                score = 75
            elif 'satisfactory' in grading_text.lower():
                score = 70
            elif 'needs improvement' in grading_text.lower():
                score = 60
            elif 'poor' in grading_text.lower():
                score = 50

        # Extract feedback sections
        feedback_sections = []
        lines = grading_text.split('\n')

        current_section = ""
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('score', 'grade', 'overall')) and len(line) > 10:
                current_section += line + "\n"

        if current_section:
            feedback_sections.append(current_section.strip())

        # If no feedback sections found, use the entire response as feedback
        if not feedback_sections:
            feedback_sections = [grading_text]

        return {
            "score": min(max(score, 0), 100),  # Ensure score is between 0 and 100
            "feedback": feedback_sections[0] if feedback_sections else "No detailed feedback provided",
            "improvement_suggestions": self._extract_improvement_suggestions(grading_text),
            "strengths_identified": self._extract_strengths(grading_text)
        }

    def _extract_improvement_suggestions(self, grading_text: str) -> List[str]:
        """
        Extract improvement suggestions from the grading response.

        Args:
            grading_text: Raw grading response text

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Look for common improvement suggestion indicators
        improvement_indicators = [
            r'(?:to improve|improvement|suggestion).*?(?:\n|$)',
            r'(?:needs work|could be better|lacks).*?(?:\n|$)',
            r'(?:consider|try|focus on).*?(?:\n|$)'
        ]

        for indicator in improvement_indicators:
            matches = re.findall(indicator, grading_text, re.IGNORECASE)
            suggestions.extend([match.strip(': ') for match in matches if len(match.strip()) > 10])

        # Remove duplicates while preserving order
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion not in unique_suggestions:
                unique_suggestions.append(suggestion)

        return unique_suggestions

    def _extract_strengths(self, grading_text: str) -> List[str]:
        """
        Extract strengths identified in the grading response.

        Args:
            grading_text: Raw grading response text

        Returns:
            List of strengths identified
        """
        strengths = []

        # Look for common strength indicators
        strength_indicators = [
            r'(?:good|excellent|well done|strong|great|nice).*?(?:\n|$)',
            r'(?:correct|accurate|precise|valid|appropriate).*?(?:\n|$)',
            r'(?:understanding|comprehension|knowledge).*?(?:\n|$)'
        ]

        for indicator in strength_indicators:
            matches = re.findall(indicator, grading_text, re.IGNORECASE)
            strengths.extend([match.strip(': ') for match in matches if len(match.strip()) > 10])

        # Remove duplicates while preserving order
        unique_strengths = []
        for strength in strengths:
            if strength not in unique_strengths:
                unique_strengths.append(strength)

        return unique_strengths

    def create_rubric_template(self, question_type: str) -> str:
        """
        Create a standard rubric template for different question types.

        Args:
            question_type: Type of question (e.g., 'essay', 'short_answer', 'problem_solving')

        Returns:
            Standard rubric template
        """
        rubrics = {
            "essay": """
            Evaluate the essay based on the following criteria:
            1. Content and Understanding (40%): Does the answer demonstrate understanding of the topic?
            2. Organization and Structure (25%): Is the essay well-organized with clear introduction, body, and conclusion?
            3. Language and Clarity (20%): Is the writing clear and free of grammatical errors?
            4. Critical Thinking (15%): Does the answer show analytical thinking and insight?
            """,
            "short_answer": """
            Evaluate the short answer based on the following criteria:
            1. Accuracy (50%): Is the information provided factually correct?
            2. Completeness (30%): Does the answer address all parts of the question?
            3. Clarity (20%): Is the answer clear and concise?
            """,
            "problem_solving": """
            Evaluate the problem-solving response based on the following criteria:
            1. Methodology (40%): Is the approach to solving the problem logical and appropriate?
            2. Correctness (40%): Is the final answer correct?
            3. Explanation (20%): Are the steps clearly explained?
            """,
            "default": """
            Evaluate the response based on the following criteria:
            1. Accuracy (40%): Is the information provided factually correct?
            2. Completeness (30%): Does the answer address all aspects of the question?
            3. Clarity (30%): Is the answer clear and well-articulated?
            """
        }

        return rubrics.get(question_type, rubrics["default"])