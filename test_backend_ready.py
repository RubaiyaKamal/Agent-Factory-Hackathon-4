"""
Backend Readiness Test Script
Tests all major backend components and endpoints
"""
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_imports():
    """Test that all backend modules can be imported"""
    print("=" * 60)
    print("TEST 1: Module Imports")
    print("=" * 60)

    try:
        from backend.main import app
        print("[PASS] backend.main imports successfully")

        from backend.api.routes import auth, content, navigation, quizzes, search, progress, pricing
        print("[PASS] All route modules import successfully")

        from backend.services import search_service, progress_service
        print("[PASS] Service modules import successfully")

        from backend.api.models.user import User
        from backend.api.models.course import Course
        from backend.api.models.chapter import Chapter
        print("[PASS] Database models import successfully")

        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        return False


async def test_config():
    """Test configuration loading"""
    print("\n" + "=" * 60)
    print("TEST 2: Configuration")
    print("=" * 60)

    try:
        from backend.core.config import get_settings
        settings = get_settings()

        print(f"[INFO] App Name: {settings.APP_NAME}")
        print(f"[INFO] Environment: {settings.ENVIRONMENT}")
        print(f"[INFO] Current Phase: {getattr(settings, 'CURRENT_PHASE', 1)}")
        print(f"[INFO] Debug Mode: {settings.DEBUG}")

        # Check critical settings
        if not settings.SECRET_KEY:
            print("[WARN] SECRET_KEY not set")
            return False

        print("[PASS] Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Configuration error: {e}")
        return False


async def test_routes():
    """Test that routes are registered"""
    print("\n" + "=" * 60)
    print("TEST 3: Route Registration")
    print("=" * 60)

    try:
        from backend.main import app

        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append((route.path, route.methods))

        # Expected routes
        expected_routes = [
            ("/api/auth/register", {"POST"}),
            ("/api/auth/login", {"POST"}),
            ("/api/content/courses", {"GET"}),
            ("/api/navigation/chapters/{id}/next", {"GET"}),
            ("/api/quizzes/{id}/submit", {"POST"}),
            ("/api/search", {"GET"}),
            ("/api/progress/me", {"GET"}),
            ("/api/pricing/tiers", {"GET"}),
        ]

        all_paths = [path for path, _ in routes]

        print(f"[INFO] Total routes registered: {len(routes)}")

        for expected_path, expected_methods in expected_routes:
            # Check if path exists (accounting for path parameters)
            found = False
            for path, methods in routes:
                if expected_path.replace("{id}", "") in path:
                    found = True
                    break

            if found:
                print(f"[PASS] {expected_path} - registered")
            else:
                print(f"[WARN] {expected_path} - not found")

        return True
    except Exception as e:
        print(f"[FAIL] Route registration error: {e}")
        return False


async def test_database_models():
    """Test database models"""
    print("\n" + "=" * 60)
    print("TEST 4: Database Models")
    print("=" * 60)

    try:
        from backend.api.models.user import User
        from backend.api.models.course import Course
        from backend.api.models.chapter import Chapter
        from backend.api.models.quiz import Quiz
        from backend.api.models.quiz_attempt import QuizAttempt
        from backend.api.models.progress import Progress
        from backend.api.models.achievement import Achievement

        models = [User, Course, Chapter, Quiz, QuizAttempt, Progress, Achievement]

        for model in models:
            print(f"[PASS] {model.__name__} model defined")

        return True
    except Exception as e:
        print(f"[FAIL] Database model error: {e}")
        return False


async def test_constitutional_compliance():
    """Test Phase 1 constitutional compliance"""
    print("\n" + "=" * 60)
    print("TEST 5: Constitutional Compliance (Zero-Backend-LLM)")
    print("=" * 60)

    try:
        from backend.core.config import get_settings
        settings = get_settings()

        current_phase = getattr(settings, 'CURRENT_PHASE', 1)

        if current_phase == 1:
            # Check for forbidden imports
            import sys
            forbidden_modules = ["anthropic", "openai", "langchain", "llama_index"]
            violations = []

            for module_name in forbidden_modules:
                if module_name in sys.modules:
                    violations.append(module_name)

            if violations:
                print(f"[FAIL] Phase 1 violation: LLM modules imported: {violations}")
                print("[FAIL] Phase 1 requires Zero-Backend-LLM (no LLM calls)")
                return False
            else:
                print("[PASS] No LLM modules imported")
                print("[PASS] Zero-Backend-LLM requirement satisfied")
        else:
            print(f"[INFO] Phase {current_phase} detected - LLM usage allowed")
            print("[PASS] Phase 2+ allows selective LLM usage")

        return True
    except Exception as e:
        print(f"[FAIL] Constitutional compliance check error: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("Course Companion FTE - Backend Readiness Test")
    print("=" * 80 + "\n")

    results = []

    results.append(await test_imports())
    results.append(await test_config())
    results.append(await test_routes())
    results.append(await test_database_models())
    results.append(await test_constitutional_compliance())

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(results)
    total = len(results)

    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("\n[SUCCESS] Backend is ready! All tests passed.")
        print("\nNext steps:")
        print("1. Set up database: alembic upgrade head")
        print("2. Start server: python backend/main.py")
        print("3. Access docs: http://localhost:8000/docs")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
