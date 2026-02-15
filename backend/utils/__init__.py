"""
Backend Utilities Package
"""

from .error_handling import (
    handle_errors,
    safe_execute,
    APIError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ConflictError,
    convert_to_http_exception,
)

__all__ = [
    "handle_errors",
    "safe_execute",
    "APIError",
    "ValidationError",
    "NotFoundError",
    "UnauthorizedError",
    "ConflictError",
    "convert_to_http_exception",
]
