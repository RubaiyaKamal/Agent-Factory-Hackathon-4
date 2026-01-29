"""
Course Companion FTE - Application Constants
"""

# Application metadata
APP_TITLE = "Course Companion FTE API"
APP_DESCRIPTION = """
**Course Companion FTE (Full-Time Equivalent) - Phase 1: Zero-Backend-LLM Architecture**

A production-ready educational platform that serves as a 24/7 digital tutor.

## Architecture Principles

**Phase 1 (Current): Zero-Backend-LLM**
- Backend performs ZERO LLM inference
- ChatGPT handles ALL intelligent reasoning, explanation, and adaptation
- Backend is purely deterministic: content retrieval, rule-based grading, progress tracking

## Core Features

### 1. Content Delivery
- Serves course content verbatim from Cloudflare R2
- ChatGPT explains at learner's level

### 2. Navigation
- Provides next/previous chapter sequencing
- ChatGPT suggests optimal learning path

### 3. Grounded Q&A
- Returns relevant content sections via search
- ChatGPT answers using ONLY retrieved content (source-grounded)

### 4. Rule-Based Quizzes
- Grades with predefined answer keys (exact match/regex)
- ChatGPT presents, encourages, explains

### 5. Progress Tracking
- Tracks completion, streaks, quiz scores
- ChatGPT motivates and celebrates

### 6. Freemium Gate
- Enforces access control by tier
- ChatGPT explains premium benefits

## Constitutional Compliance

⚠️ **CRITICAL**: This backend follows Zero-Backend-LLM architecture.
NO LLM API calls are permitted in Phase 1. Violations result in immediate disqualification.

## API Documentation

- **OpenAPI Spec**: `/openapi.json`
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Support

For questions or issues, contact the development team.
"""

# HTTP status codes (commonly used)
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_500_INTERNAL_SERVER_ERROR = 500

# User tiers
class UserTier:
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"
    TEAM = "team"

# Quiz question types
class QuestionType:
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_IN_BLANK = "fill_in_blank"

# Quiz difficulty levels
class DifficultyLevel:
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

# Content types
class ContentType:
    MARKDOWN = "text/markdown"
    PLAIN_TEXT = "text/plain"
    JSON = "application/json"

# Achievement types
class AchievementType:
    FIRST_CHAPTER = "first_chapter"
    HALFWAY_HERO = "halfway_hero"
    COURSE_COMPLETE = "course_complete"
    QUIZ_MASTER = "quiz_master"
    WEEK_WARRIOR = "week_warrior"
    MONTH_MASTER = "month_master"
    PERFECTIONIST = "perfectionist"
    COMEBACK_KID = "comeback_kid"

# Error messages
class ErrorMessages:
    # Authentication
    INVALID_CREDENTIALS = "Invalid email or password"
    TOKEN_EXPIRED = "Authentication token has expired"
    INSUFFICIENT_PERMISSIONS = "Insufficient permissions to access this resource"

    # Content
    CHAPTER_NOT_FOUND = "Chapter not found"
    CONTENT_TOO_LARGE = "Content exceeds maximum size limit"
    INVALID_CONTENT_TYPE = "Invalid content type"

    # Quiz
    QUIZ_NOT_FOUND = "Quiz not found"
    MAX_ATTEMPTS_EXCEEDED = "Maximum quiz attempts exceeded"
    QUIZ_ALREADY_COMPLETED = "Quiz has already been completed"

    # Freemium
    TIER_LIMIT_REACHED = "You've reached the limit for free tier. Upgrade to premium for unlimited access."
    PREMIUM_FEATURE_REQUIRED = "This feature requires a premium subscription"

    # Search
    QUERY_TOO_SHORT = "Search query must be at least {min_length} characters"
    NO_RESULTS_FOUND = "No results found for your query"

    # Progress
    INVALID_STREAK_DATA = "Invalid streak calculation data"

    # General
    INTERNAL_ERROR = "An internal server error occurred"
    INVALID_REQUEST = "Invalid request parameters"
    RESOURCE_NOT_FOUND = "Requested resource not found"
    RATE_LIMIT_EXCEEDED = "Rate limit exceeded. Please try again later."

# Success messages
class SuccessMessages:
    CHAPTER_COMPLETED = "Congratulations! Chapter completed successfully"
    QUIZ_PASSED = "Great job! You passed the quiz"
    PROGRESS_UPDATED = "Progress updated successfully"
    CONTENT_RETRIEVED = "Content retrieved successfully"
    STREAK_UPDATED = "Streak updated! Keep up the great work!"

# Regex patterns for validation
class RegexPatterns:
    EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    UUID = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    SLUG = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

# Cache keys
class CacheKeys:
    CHAPTER_CONTENT = "chapter:content:{chapter_id}"
    USER_PROGRESS = "user:progress:{user_id}"
    QUIZ_QUESTIONS = "quiz:questions:{quiz_id}"
    SEARCH_RESULTS = "search:{query}:{filters}"
    USER_TIER = "user:tier:{user_id}"

# Database table names
class TableNames:
    USERS = "users"
    COURSES = "courses"
    CHAPTERS = "chapters"
    QUIZZES = "quizzes"
    QUESTIONS = "questions"
    QUIZ_ATTEMPTS = "quiz_attempts"
    PROGRESS = "progress"
    ACHIEVEMENTS = "achievements"

# API Tags (for OpenAPI grouping)
class APITags:
    AUTH = "Authentication"
    CONTENT = "Content Delivery"
    NAVIGATION = "Navigation"
    QUIZZES = "Quizzes"
    PROGRESS = "Progress Tracking"
    SEARCH = "Search"
    HEALTH = "Health & Monitoring"

# Timezone
DEFAULT_TIMEZONE = "UTC"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Search
MIN_SEARCH_QUERY_LENGTH = 3
MAX_SEARCH_RESULTS = 50

# File upload
MAX_FILE_SIZE_MB = 5
ALLOWED_FILE_EXTENSIONS = [".md", ".txt", ".json"]

# Rate limiting (requests per minute)
RATE_LIMITS = {
    UserTier.FREE: 50,
    UserTier.PREMIUM: 200,
    UserTier.PRO: 500,
    UserTier.TEAM: 1000,
}

# Phase 1 Constitutional Constraints
PHASE_1_FORBIDDEN_IMPORTS = [
    "anthropic",
    "openai",
    "langchain",
    "llama_index",
    "cohere",
    "google.generativeai",
]

PHASE_1_FORBIDDEN_PATTERNS = [
    "llm",
    "language_model",
    "generate_text",
    "complete",
    "chat_completion",
]
