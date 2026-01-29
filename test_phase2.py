"""
Test script to verify Phase 2 Hybrid Intelligence features are working correctly.
"""

import asyncio
import os
from dotenv import load_dotenv
from backend.core.config import get_settings
from backend.services.adaptive_learning import AdaptiveLearningPathService
from backend.services.llm_grading import LLMGradingService
from backend.services.premium_access import PremiumFeatureAccess, FeatureType

# Load environment variables
load_dotenv()

def test_services_initialization():
    """Test that Phase 2 services can be initialized."""
    print("Testing Phase 2 service initialization...")

    settings = get_settings()
    print(f"Current phase: {settings.CURRENT_PHASE}")

    if settings.CURRENT_PHASE < 2:
        print("ERROR: Current phase is less than 2. Update CURRENT_PHASE to 2 in your .env file.")
        return False

    try:
        # Test initializing the services
        adaptive_service = AdaptiveLearningPathService(settings.DATABASE_URL)
        grading_service = LLMGradingService(settings.DATABASE_URL)
        premium_service = PremiumFeatureAccess(settings.DATABASE_URL)

        print("✅ All Phase 2 services initialized successfully!")
        return True

    except Exception as e:
        print(f"❌ Error initializing Phase 2 services: {e}")
        return False

def test_premium_access():
    """Test premium access functionality."""
    print("\nTesting premium access functionality...")

    try:
        settings = get_settings()
        premium_service = PremiumFeatureAccess(settings.DATABASE_URL)

        # Grant premium access to a test user
        user_id = "test_user_phase2"
        subscription = premium_service.grant_premium_access(
            user_id=user_id,
            tier="premium",
            duration_days=30
        )

        print(f"✅ Granted premium access to {user_id}")
        print(f"   Tier: {subscription.subscription_tier}")
        print(f"   Ends: {subscription.subscription_end_date}")

        # Check access
        access_result = premium_service.check_feature_access(
            user_id=user_id,
            feature=FeatureType.ADAPTIVE_LEARNING_PATH
        )

        print(f"✅ Access check result: {access_result}")

        # Revoke access
        revoked_subscription = premium_service.revoke_premium_access(user_id=user_id)
        print(f"✅ Revoked premium access from {user_id}")

        return True

    except Exception as e:
        print(f"❌ Error testing premium access: {e}")
        return False

def test_anthropic_integration():
    """Test Anthropic API integration (without making actual API calls)."""
    print("\nTesting Anthropic API integration...")

    try:
        from backend.services.anthropic_client import AnthropicClientService

        # Check if API key is configured
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "sk-ant-...":
            print("⚠️  ANTHROPIC_API_KEY not configured. Please set it in your .env file.")
            print("   Get your API key from: https://console.anthropic.com/")
            return False

        try:
            anthropic_service = AnthropicClientService()
            print("✅ Anthropic service initialized successfully!")

            # Test token counting (doesn't require API call)
            sample_text = "This is a sample text for token counting."
            token_count = anthropic_service.get_token_count(sample_text)
            print(f"✅ Token count for sample text: {token_count}")

            return True

        except Exception as e:
            print(f"❌ Error with Anthropic service: {e}")
            return False

    except Exception as e:
        print(f"❌ Error importing Anthropic service: {e}")
        return False

def main():
    """Run all Phase 2 tests."""
    print("="*60)
    print("Phase 2: Hybrid Intelligence Features Test")
    print("="*60)

    # Check if we're in Phase 2
    settings = get_settings()
    print(f"Current Phase: {settings.CURRENT_PHASE}")

    if settings.CURRENT_PHASE < 2:
        print("\n⚠️  WARNING: You're currently in Phase 1.")
        print("   To enable Phase 2 features, set CURRENT_PHASE=2 in your .env file.")
        print("   Also set ENFORCE_ZERO_BACKEND_LLM=false and BLOCK_LLM_IMPORTS=false")

    all_tests_passed = True

    # Run tests
    all_tests_passed &= test_services_initialization()
    all_tests_passed &= test_premium_access()
    all_tests_passed &= test_anthropic_integration()

    print("\n" + "="*60)
    if all_tests_passed:
        print("🎉 All Phase 2 tests passed! Hybrid Intelligence features are ready.")
        print("\nNext steps:")
        print("- Set up your Anthropic API key in .env")
        print("- Start the backend: uvicorn backend.main:app --reload")
        print("- Test the new API endpoints:")
        print("  - POST /api/v1/adaptive-learning-path")
        print("  - POST /api/v1/llm-grade-assessment")
        print("  - POST /api/v1/premium/grant-access")
    else:
        print("❌ Some tests failed. Please check the output above.")
        print("\nMake sure:")
        print("- CURRENT_PHASE=2 in your .env file")
        print("- ANTHROPIC_API_KEY is set in your .env file")
        print("- All Phase 2 services are properly implemented")

    print("="*60)

if __name__ == "__main__":
    main()