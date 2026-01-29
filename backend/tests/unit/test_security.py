"""
Unit tests for security utilities in Course Companion FTE
Tests password hashing and JWT creation/validation functions
"""
import pytest
import jwt
from datetime import timedelta, datetime
from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from backend.core.config import get_settings


def test_hash_password():
    """
    Test that password hashing works correctly
    """
    password = "test_password_123"
    hashed = hash_password(password)

    # Verify the hash is not the same as the original password
    assert hashed != password
    # Verify the hash contains the expected bcrypt prefix
    assert hashed.startswith("$2b$")


def test_verify_password_correct():
    """
    Test that password verification works with correct password
    """
    password = "test_password_123"
    hashed = hash_password(password)

    result = verify_password(password, hashed)
    assert result is True


def test_verify_password_incorrect():
    """
    Test that password verification fails with incorrect password
    """
    password = "test_password_123"
    wrong_password = "wrong_password_456"
    hashed = hash_password(password)

    result = verify_password(wrong_password, hashed)
    assert result is False


def test_create_access_token():
    """
    Test that access token creation works correctly
    """
    data = {"sub": "123", "username": "testuser"}
    token = create_access_token(data)

    # Verify token is created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Decode and verify contents
    decoded = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
    assert decoded["sub"] == "123"
    assert decoded["username"] == "testuser"
    assert "exp" in decoded
    assert decoded["type"] == "access"


def test_create_access_token_with_custom_expiry():
    """
    Test that access token creation works with custom expiry time
    """
    data = {"sub": "123"}
    custom_expiry = timedelta(minutes=30)
    token = create_access_token(data, expires_delta=custom_expiry)

    decoded = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])

    # Calculate expected expiry time (approximately)
    expected_exp = datetime.utcnow() + custom_expiry
    actual_exp = datetime.utcfromtimestamp(decoded["exp"])

    # Allow for some time difference due to execution time
    time_diff = abs((expected_exp - actual_exp).total_seconds())
    assert time_diff < 5  # Less than 5 seconds difference


def test_create_refresh_token():
    """
    Test that refresh token creation works correctly
    """
    data = {"sub": "123", "username": "testuser"}
    token = create_refresh_token(data)

    # Verify token is created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Decode and verify contents
    decoded = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
    assert decoded["sub"] == "123"
    assert decoded["username"] == "testuser"
    assert "exp" in decoded
    assert decoded["type"] == "refresh"


def test_decode_valid_token():
    """
    Test that decoding a valid token works correctly
    """
    data = {"sub": "123", "test": "value"}
    token = create_access_token(data)

    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "123"
    assert decoded["test"] == "value"
    assert decoded["type"] == "access"


def test_decode_expired_token():
    """
    Test that decoding an expired token returns None
    """
    data = {"sub": "123"}
    # Create a token that expires immediately
    token = jwt.encode(
        {**data, "exp": datetime.utcnow(), "type": "access"},
        get_settings().SECRET_KEY,
        algorithm=get_settings().ALGORITHM
    )

    # Wait a moment for the token to actually expire
    import time
    time.sleep(0.1)

    decoded = decode_token(token)
    assert decoded is None


def test_decode_invalid_token():
    """
    Test that decoding an invalid token returns None
    """
    invalid_token = "this.is.not.a.valid.token"

    decoded = decode_token(invalid_token)
    assert decoded is None


def test_token_expiry_times():
    """
    Test that access and refresh tokens have different expiry times
    """
    data = {"sub": "123"}

    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    access_decoded = jwt.decode(access_token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
    refresh_decoded = jwt.decode(refresh_token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])

    access_exp = datetime.utcfromtimestamp(access_decoded["exp"])
    refresh_exp = datetime.utcfromtimestamp(refresh_decoded["exp"])

    # Refresh token should expire much later than access token
    settings = get_settings()
    expected_difference = timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    ) - timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    actual_difference = refresh_exp - access_exp
    # The actual difference should be approximately equal to expected difference
    # Allow for a small margin of error due to execution time
    assert abs((actual_difference - expected_difference).total_seconds()) < 60


if __name__ == "__main__":
    pytest.main([__file__])