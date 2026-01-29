"""
Custom exception classes for Course Companion FTE
Defines application-specific exceptions for consistent error handling
"""


class BaseAppException(Exception):
    """
    Base exception class for all application-specific exceptions
    """
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(BaseAppException):
    """
    Raised when authentication fails
    """
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class NotFoundError(BaseAppException):
    """
    Raised when a requested resource is not found
    """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ForbiddenError(BaseAppException):
    """
    Raised when access to a resource is forbidden
    """
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, 403)


class ValidationError(BaseAppException):
    """
    Raised when input validation fails
    """
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400)


class DatabaseError(BaseAppException):
    """
    Raised when database operations fail
    """
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, 500)


class StorageError(BaseAppException):
    """
    Raised when storage operations (R2) fail
    """
    def __init__(self, message: str = "Storage operation failed"):
        super().__init__(message, 500)


class RateLimitError(BaseAppException):
    """
    Raised when rate limit is exceeded
    """
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 429)


class BusinessLogicError(BaseAppException):
    """
    Raised when business logic validation fails
    """
    def __init__(self, message: str = "Business logic validation failed"):
        super().__init__(message, 400)


class ConfigurationError(BaseAppException):
    """
    Raised when configuration is invalid or missing
    """
    def __init__(self, message: str = "Configuration error"):
        super().__init__(message, 500)