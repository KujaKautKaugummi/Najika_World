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

from .performance import (
    measure_performance,
    get_performance_stats,
    get_slow_endpoints,
    get_slowest_endpoints,
    clear_performance_stats,
)

__all__ = [
    # Error Handling
    "handle_errors",
    "safe_execute",
    "APIError",
    "ValidationError",
    "NotFoundError",
    "UnauthorizedError",
    "ConflictError",
    "convert_to_http_exception",
    # Performance
    "measure_performance",
    "get_performance_stats",
    "get_slow_endpoints",
    "get_slowest_endpoints",
    "clear_performance_stats",
]
