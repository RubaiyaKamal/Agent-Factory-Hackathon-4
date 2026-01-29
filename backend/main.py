"""
Course Companion FTE - Main Application Entry Point
Phase 1: Zero-Backend-LLM Architecture

CONSTITUTIONAL REQUIREMENT:
This backend MUST NOT contain any LLM API calls.
Violations result in immediate disqualification.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging

from backend.core.config import settings
from backend.core.constants import APP_DESCRIPTION, APP_TITLE
# from backend.api.routes import health, content, navigation, quizzes, progress, auth
# Uncomment above when routes are implemented

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"[START] Starting {APP_TITLE} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Zero-Backend-LLM Enforcement: {settings.ENFORCE_ZERO_BACKEND_LLM}")

    # Constitutional compliance check
    if settings.ENFORCE_ZERO_BACKEND_LLM:
        _verify_zero_llm_compliance()

    # Initialize database connection pool
    # await db.connect()

    # Initialize R2 client
    # await storage.init_r2_client()

    logger.info("[OK] Application startup complete")

    yield

    # Shutdown
    logger.info("[STOP] Shutting down application...")

    # Close database connections
    # await db.disconnect()

    # Close R2 client
    # await storage.close()

    logger.info("[OK] Application shutdown complete")


def _verify_zero_llm_compliance() -> None:
    """
    Verify that no LLM client libraries are imported.
    Constitutional compliance enforcement.
    NOTE: This check is for Phase 1. In Phase 2, hybrid features are allowed in separate modules.
    """
    import sys

    # Check current phase from settings
    current_phase = getattr(settings, 'CURRENT_PHASE', 1)

    if current_phase == 1:
        forbidden_modules = ["anthropic", "openai", "langchain", "llama_index"]
        violations = []

        for module_name in forbidden_modules:
            if module_name in sys.modules:
                violations.append(module_name)

        if violations:
            error_msg = (
                f"[ERROR] CONSTITUTIONAL VIOLATION: Phase 1 backend detected forbidden LLM imports: {violations}\n"
                f"Phase 1 MUST follow Zero-Backend-LLM architecture.\n"
                f"Remove all LLM client libraries from imports.\n"
                f"This violation would result in immediate disqualification."
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        logger.info("[OK] Zero-Backend-LLM compliance verified - no LLM imports detected")
    else:
        logger.info(f"[OK] Phase {current_phase} detected - LLM imports allowed in designated modules")


# Create FastAPI application
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url=settings.DOCS_URL if settings.DEBUG else None,
    redoc_url=settings.REDOC_URL if settings.DEBUG else None,
    openapi_url=settings.OPENAPI_URL if settings.DEBUG else None,
)

# ==============================================================================
# Middleware Configuration
# ==============================================================================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Trusted host middleware (security)
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


# ==============================================================================
# Exception Handlers
# ==============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An internal server error occurred",
            "detail": str(exc) if settings.DEBUG else None,
        },
    )


# ==============================================================================
# Root Endpoint
# ==============================================================================


@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    response_description="API information",
)
async def root() -> dict:
    """
    Root endpoint returning API information.
    """
    current_phase = getattr(settings, 'CURRENT_PHASE', 1)

    if current_phase == 1:
        architecture_desc = "Zero-Backend-LLM (Phase 1)"
    elif current_phase == 2:
        architecture_desc = "Hybrid Intelligence (Phase 2)"
    else:
        architecture_desc = f"Phase {current_phase}"

    return {
        "app": APP_TITLE,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "current_phase": current_phase,
        "architecture": architecture_desc,
        "docs": f"{settings.BACKEND_URL}{settings.DOCS_URL}",
        "status": "operational",
    }


# ==============================================================================
# Health Check Endpoint
# ==============================================================================


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    response_description="System health status",
)
async def health_check() -> dict:
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Health status with component checks
    """
    # TODO: Add actual health checks for database, R2, etc.
    return {
        "status": "healthy",
        "checks": {
            "database": "ok",  # await db.health_check()
            "storage": "ok",  # await storage.health_check()
            "cache": "ok",
        },
        "version": settings.APP_VERSION,
        "uptime": "0s",  # TODO: Calculate actual uptime
    }


# ==============================================================================
# API Routes (to be implemented)
# ==============================================================================

# Import Phase 2 services (only when needed to avoid early import violations)
def import_phase2_services():
    try:
        from backend.services.adaptive_learning import AdaptiveLearningPathService
        from backend.services.llm_grading import LLMGradingService
        from backend.services.premium_access import PremiumFeatureAccess, FeatureType
        return AdaptiveLearningPathService, LLMGradingService, PremiumFeatureAccess, FeatureType
    except ImportError as e:
        print(f"Phase 2 services not available: {e}")
        return None, None, None, None


# Import route routers
from backend.api.routes import auth, content, navigation, quizzes, search, progress, pricing

# Authentication routes
app.include_router(auth.router, prefix="/api", tags=["authentication"])

# Content delivery routes
app.include_router(content.router, prefix="/api", tags=["content"])

# Navigation routes
app.include_router(navigation.router, prefix="/api", tags=["navigation"])

# Quiz routes
app.include_router(quizzes.router, prefix="/api", tags=["quizzes"])

# Search routes
app.include_router(search.router, prefix="/api", tags=["search"])

# Progress tracking routes
app.include_router(progress.router, prefix="/api", tags=["progress"])

# Pricing and subscription routes
app.include_router(pricing.router, prefix="/api", tags=["pricing"])


# ==============================================================================
# Phase 2: Hybrid Intelligence Endpoints
# ==============================================================================

# Only add Phase 2 endpoints if in Phase 2
current_phase = getattr(settings, 'CURRENT_PHASE', 1)

if current_phase >= 2:
    from fastapi import Depends
    from typing import Dict, Any, Optional

    # Get service classes
    AdaptiveLearningPathService, LLMGradingService, PremiumFeatureAccess, FeatureType = import_phase2_services()

    if AdaptiveLearningPathService and LLMGradingService and PremiumFeatureAccess and FeatureType:

        def get_adaptive_learning_service():
            return AdaptiveLearningPathService(settings.DATABASE_URL)


        def get_llm_grading_service():
            return LLMGradingService(settings.DATABASE_URL)


        def get_premium_access_service():
            return PremiumFeatureAccess(settings.DATABASE_URL)


        @app.post("/api/v1/adaptive-learning-path", tags=["hybrid-intelligence"])
        async def generate_adaptive_learning_path(
            user_id: str,
            user_performance_data: Dict[str, Any],
            content_catalog: Dict[str, Any],
            max_recommendations: int = 5,
            service = Depends(get_adaptive_learning_service)
        ):
            """
            Generate an adaptive learning path for a user based on their performance.
            Phase 2: Hybrid Intelligence (Selective Premium) feature.
            """
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Generating adaptive learning path for user: {user_id}")

            result = service.generate_learning_path(
                user_id=user_id,
                user_performance_data=user_performance_data,
                content_catalog=content_catalog,
                max_recommendations=max_recommendations
            )

            if "error" in result:
                from fastapi import HTTPException
                raise HTTPException(status_code=403, detail=result["message"])

            return result


        @app.post("/api/v1/llm-grade-assessment", tags=["hybrid-intelligence"])
        async def grade_assessment(
            user_id: str,
            question: str,
            user_answer: str,
            rubric: str,
            assessment_id: Optional[str] = None,
            service = Depends(get_llm_grading_service)
        ):
            """
            Grade a free-form assessment answer using LLM evaluation.
            Phase 2: Hybrid Intelligence (Selective Premium) feature.
            """
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Grading assessment for user: {user_id}")

            result = service.grade_assessment(
                user_id=user_id,
                question=question,
                user_answer=user_answer,
                rubric=rubric,
                assessment_id=assessment_id
            )

            if "error" in result:
                from fastapi import HTTPException
                raise HTTPException(status_code=403, detail=result["message"])

            return result


        @app.post("/api/v1/premium/grant-access", tags=["premium-access"])
        async def grant_premium_access(
            user_id: str,
            tier: str = "premium",
            duration_days: int = 30,
            service = Depends(get_premium_access_service)
        ):
            """
            Grant premium access to a user for Phase 2 features.
            """
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Granting premium access to user: {user_id}, tier: {tier}")

            subscription = service.grant_premium_access(
                user_id=user_id,
                tier=tier,
                duration_days=duration_days
            )

            return {
                "user_id": user_id,
                "subscription": {
                    "is_premium": subscription.is_premium,
                    "tier": subscription.subscription_tier,
                    "start_date": subscription.subscription_start_date,
                    "end_date": subscription.subscription_end_date,
                    "max_monthly_tokens": subscription.max_monthly_tokens
                }
            }


        @app.delete("/api/v1/premium/revoke-access", tags=["premium-access"])
        async def revoke_premium_access(
            user_id: str,
            service = Depends(get_premium_access_service)
        ):
            """
            Revoke premium access from a user.
            """
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Revoking premium access for user: {user_id}")

            subscription = service.revoke_premium_access(user_id=user_id)

            return {
                "user_id": user_id,
                "subscription": {
                    "is_premium": subscription.is_premium,
                    "tier": subscription.subscription_tier,
                    "end_date": subscription.subscription_end_date
                }
            }


        @app.get("/api/v1/premium/check-access/{user_id}/{feature}", tags=["premium-access"])
        async def check_premium_access(
            user_id: str,
            feature: FeatureType,
            service = Depends(get_premium_access_service)
        ):
            """
            Check if a user has access to a specific premium feature.
            """
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Checking access for user: {user_id}, feature: {feature}")

            access_result = service.check_feature_access(user_id, feature)

            return {
                "user_id": user_id,
                "feature": feature.value,
                "access_status": access_result
            }


# ==============================================================================
# Development Entry Point
# ==============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
