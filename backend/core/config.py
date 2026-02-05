"""
Course Companion FTE - Configuration Management
Loads and validates environment variables using Pydantic Settings
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Course Companion FTE"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = True

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    BCRYPT_ROUNDS: int = 12

    # CORS (stored as comma-separated strings, split on use)
    ALLOWED_ORIGINS: str = "*"
    ALLOWED_METHODS: str = "GET,POST,PUT,DELETE,OPTIONS"
    ALLOWED_HEADERS: str = "*"
    ALLOWED_HOSTS: str = "*"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Split ALLOWED_ORIGINS into list."""
        return [item.strip() for item in self.ALLOWED_ORIGINS.split(",")]

    @property
    def allowed_methods_list(self) -> List[str]:
        """Split ALLOWED_METHODS into list."""
        return [item.strip() for item in self.ALLOWED_METHODS.split(",")]

    @property
    def allowed_headers_list(self) -> List[str]:
        """Split ALLOWED_HEADERS into list."""
        return [item.strip() for item in self.ALLOWED_HEADERS.split(",")]

    @property
    def allowed_hosts_list(self) -> List[str]:
        """Split ALLOWED_HOSTS into list."""
        return [item.strip() for item in self.ALLOWED_HOSTS.split(",")]

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    DB_RETRY_ATTEMPTS: int = 3
    DB_RETRY_DELAY: int = 2

    # Cloudflare R2 Storage
    R2_ENDPOINT_URL: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_REGION: str = "auto"
    R2_SIGNED_URL_EXPIRY: int = 3600

    # Content
    CONTENT_BASE_PATH: str = "/courses"
    MAX_CONTENT_SIZE: int = 5242880  # 5MB
    SUPPORTED_CONTENT_TYPES: str = "text/markdown,text/plain,application/json"

    @property
    def supported_content_types_list(self) -> List[str]:
        """Split SUPPORTED_CONTENT_TYPES into list."""
        return [item.strip() for item in self.SUPPORTED_CONTENT_TYPES.split(",")]

    # Quiz
    QUIZ_PASSING_SCORE: int = 70
    QUIZ_MAX_ATTEMPTS: int = 5
    QUIZ_TRIM_WHITESPACE: bool = True
    QUIZ_CASE_INSENSITIVE: bool = True

    # Progress Tracking
    STREAK_GRACE_PERIOD_HOURS: int = 24
    STREAK_TIMEZONE: str = "UTC"
    PROGRESS_CACHE_TTL: int = 300

    # Freemium
    FREE_TIER_CHAPTER_LIMIT: int = 3
    FREE_TIER_QUIZ_LIMIT: int = 3
    PREMIUM_MONTHLY_PRICE: float = 9.99
    PRO_MONTHLY_PRICE: float = 19.99
    TEAM_MONTHLY_PRICE: float = 49.99

    # Search
    SEARCH_MIN_QUERY_LENGTH: int = 3
    SEARCH_MAX_RESULTS: int = 20
    EMBEDDINGS_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDINGS_CACHE_DIR: str = "./cache/embeddings"
    SEMANTIC_SEARCH_ENABLED: bool = True
    SEMANTIC_SEARCH_THRESHOLD: float = 0.7

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    FREE_TIER_RATE_LIMIT: int = 50
    PREMIUM_TIER_RATE_LIMIT: int = 200
    PRO_TIER_RATE_LIMIT: int = 500

    # Caching
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    CACHE_TTL: int = 300
    CACHE_MAX_SIZE: int = 1000

    # Monitoring
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "./logs/app.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "7 days"

    # Sentry (optional)
    SENTRY_DSN: str = ""
    SENTRY_ENVIRONMENT: str = "development"
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1

    # Testing
    TEST_DATABASE_URL: str = ""
    SEED_TEST_DATA: bool = False

    # ChatGPT App Integration
    BACKEND_URL: str = "http://localhost:8000"
    BACKEND_API_KEY: str = ""

    # API Documentation
    OPENAPI_URL: str = "/openapi.json"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # Development
    DEV_SKIP_AUTH: bool = False
    DEV_MOCK_R2: bool = False

    # Feature Flags
    FEATURE_GROUNDED_QA: bool = True
    FEATURE_PROGRESS_TRACKING: bool = True
    FEATURE_FREEMIUM_GATE: bool = True
    FEATURE_SEMANTIC_SEARCH: bool = True

    # Constitutional Compliance
    CURRENT_PHASE: int = 1  # 1 = Zero-Backend-LLM, 2 = Hybrid Intelligence
    ENFORCE_ZERO_BACKEND_LLM: bool = True  # Only enforce in Phase 1
    BLOCK_LLM_IMPORTS: bool = True
    ALERT_ON_LLM_ATTEMPT: bool = True

    # Phase 2 Settings (Enabled when CURRENT_PHASE >= 2)
    ANTHROPIC_API_KEY: str = ""  # Required for Phase 2
    OPENAI_API_KEY: str = ""     # Optional for Phase 2

    def __init__(self, **kwargs):
        """
        Initialize settings and perform validation.
        """
        super().__init__(**kwargs)
        self._validate_phase_1_compliance()

    def _validate_phase_1_compliance(self) -> None:
        """
        Validate constitutional compliance based on current phase.
        """
        if self.ENVIRONMENT == "production" and self.DEBUG:
            raise ValueError("DEBUG must be False in production")

        if self.SECRET_KEY == "CHANGE_THIS_TO_A_SECURE_RANDOM_STRING_IN_PRODUCTION":
            if self.ENVIRONMENT in ["production", "staging"]:
                raise ValueError("SECRET_KEY must be changed from default in production/staging")

        # Check for LLM configuration based on current phase
        if self.CURRENT_PHASE == 1 and self.ENFORCE_ZERO_BACKEND_LLM:
            # In Phase 1, LLM keys should not be set
            forbidden_keys = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
            for key in forbidden_keys:
                if hasattr(self, key) and getattr(self, key, ""):
                    raise ValueError(
                        f"❌ CONSTITUTIONAL VIOLATION: {key} is set in Phase 1. "
                        f"Phase 1 MUST follow Zero-Backend-LLM architecture. "
                        f"Remove all LLM configuration."
                    )
        elif self.CURRENT_PHASE >= 2:
            # In Phase 2+, we need to ensure required keys are set
            if not getattr(self, 'ANTHROPIC_API_KEY', ""):
                # Only warn for now - can be configured later
                print("WARNING: ANTHROPIC_API_KEY is not set. Phase 2 features will not work without it.")


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure single instance.
    """
    return Settings()


# Global settings instance
settings = get_settings()
