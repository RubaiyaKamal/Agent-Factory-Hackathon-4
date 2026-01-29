"""
Test script to verify Zero-Backend-LLM compliance checks.

Test 1: Should PASS when no LLM libraries are imported
Test 2: Should FAIL when LLM library is detected
"""
import sys

print("=" * 80)
print("Test 1: Verify compliance check passes with no LLM imports")
print("=" * 80)

# First, import backend.main normally (should succeed)
try:
    from backend.main import _verify_zero_llm_compliance

    # Call the verification function directly
    _verify_zero_llm_compliance()
    print("[PASS] Test 1 PASSED: No LLM imports detected correctly\n")
except Exception as e:
    print(f"[FAIL] Test 1 FAILED: Unexpected error: {e}\n")
    sys.exit(1)

print("=" * 80)
print("Test 2: Verify compliance check fails with LLM imports")
print("=" * 80)

# Now simulate a violation
sys.modules['openai'] = type(sys)('openai')
sys.modules['anthropic'] = type(sys)('anthropic')

try:
    _verify_zero_llm_compliance()
    print("[FAIL] Test 2 FAILED: Forbidden imports were not detected!\n")
    sys.exit(1)
except RuntimeError as e:
    if "CONSTITUTIONAL VIOLATION" in str(e):
        print("[PASS] Test 2 PASSED: Forbidden imports detected correctly!")
        print(f"  Error message: {e}\n")
    else:
        print(f"[FAIL] Test 2 FAILED: Wrong error: {e}\n")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Test 2 FAILED: Unexpected exception: {type(e).__name__}: {e}\n")
    sys.exit(1)

print("=" * 80)
print("All compliance tests PASSED!")
print("=" * 80)
