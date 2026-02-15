"""
Error Handling Utilities für FastAPI
Zentralisiertes Exception-Handling für alle API-Endpoints
"""

import logging
import traceback
from functools import wraps
from typing import Callable
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def handle_errors(fallback_value=None, status_code: int = 500):
    """
    Decorator für FastAPI Endpoints mit automatischem Error-Handling.

    Usage:
        @router.get("/example")
        @handle_errors()
        async def example_endpoint():
            # Your code here - exceptions werden automatisch gefangen
            return {"status": "ok"}

    Args:
        fallback_value: Wert der zurückgegeben wird bei Fehler (default: HTTPException)
        status_code: HTTP Status Code für Fehler (default: 500)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                # HTTPException wird nicht gefangen (FastAPI soll es handlen)
                raise
            except Exception as e:
                # Alle anderen Exceptions loggen
                logger.error(f"Error in {func.__name__}: {str(e)}")
                logger.error(traceback.format_exc())

                if fallback_value is not None:
                    return fallback_value

                # Default: HTTPException werfen
                raise HTTPException(
                    status_code=status_code,
                    detail=f"Internal server error in {func.__name__}: {str(e)}"
                )

        return wrapper
    return decorator


def safe_execute(func: Callable, *args, **kwargs):
    """
    Führt eine Funktion sicher aus und gibt None zurück bei Fehler.

    Usage:
        result = safe_execute(dangerous_function, arg1, arg2)
        if result is None:
            # Handle error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {str(e)}")
        return None


class APIError(Exception):
    """Base Exception für API-Fehler"""
    pass


class ValidationError(APIError):
    """Validation-Fehler (400 Bad Request)"""
    pass


class NotFoundError(APIError):
    """Resource nicht gefunden (404)"""
    pass


class UnauthorizedError(APIError):
    """Nicht autorisiert (401)"""
    pass


class ConflictError(APIError):
    """Konflikt (409)"""
    pass


def convert_to_http_exception(error: APIError, default_status: int = 500) -> HTTPException:
    """
    Konvertiert APIError zu HTTPException.

    Usage:
        try:
            if not user:
                raise NotFoundError("User not found")
        except APIError as e:
            raise convert_to_http_exception(e)
    """
    status_map = {
        ValidationError: 400,
        NotFoundError: 404,
        UnauthorizedError: 401,
        ConflictError: 409,
    }

    status_code = status_map.get(type(error), default_status)

    return HTTPException(
        status_code=status_code,
        detail=str(error)
    )
