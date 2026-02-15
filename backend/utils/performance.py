"""
Performance Monitoring für FastAPI
Misst Response-Times und identifiziert Bottlenecks
"""

import time
import logging
from functools import wraps
from typing import Callable, Dict, List
from collections import defaultdict

logger = logging.getLogger(__name__)


# Performance-Statistiken (in-memory)
_performance_stats: Dict[str, List[float]] = defaultdict(list)
_slow_endpoints: List[Dict] = []


def measure_performance(threshold_ms: float = 1000):
    """
    Decorator zum Messen der Performance von Endpoints.
    Warnt wenn Endpoint langsamer als threshold_ms ist.

    Usage:
        @router.get("/example")
        @measure_performance(threshold_ms=500)  # Warn if > 500ms
        async def example_endpoint():
            return {"status": "ok"}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                # Immer messen, auch bei Exceptions
                elapsed_ms = (time.time() - start_time) * 1000
                endpoint_name = func.__name__

                # Stats speichern
                _performance_stats[endpoint_name].append(elapsed_ms)

                # Keep only last 100 measurements
                if len(_performance_stats[endpoint_name]) > 100:
                    _performance_stats[endpoint_name] = _performance_stats[endpoint_name][-100:]

                # Warnung bei langsamen Endpoints
                if elapsed_ms > threshold_ms:
                    logger.warning(
                        f"SLOW ENDPOINT: {endpoint_name} took {elapsed_ms:.2f}ms "
                        f"(threshold: {threshold_ms}ms)"
                    )

                    _slow_endpoints.append({
                        "endpoint": endpoint_name,
                        "duration_ms": round(elapsed_ms, 2),
                        "threshold_ms": threshold_ms,
                        "timestamp": time.time(),
                    })

                    # Keep only last 50 slow requests
                    if len(_slow_endpoints) > 50:
                        _slow_endpoints.pop(0)
                else:
                    logger.debug(f"{endpoint_name}: {elapsed_ms:.2f}ms")

        return wrapper
    return decorator


def get_performance_stats() -> Dict:
    """
    Gibt Performance-Statistiken für alle gemessenen Endpoints zurück.

    Returns:
        {
            "endpoint_name": {
                "avg_ms": 123.45,
                "min_ms": 50.0,
                "max_ms": 500.0,
                "count": 100,
                "p50": 100.0,  # Median
                "p95": 450.0,  # 95th percentile
                "p99": 490.0   # 99th percentile
            }
        }
    """
    stats = {}

    for endpoint_name, measurements in _performance_stats.items():
        if not measurements:
            continue

        sorted_measurements = sorted(measurements)
        count = len(sorted_measurements)

        stats[endpoint_name] = {
            "avg_ms": round(sum(measurements) / count, 2),
            "min_ms": round(min(measurements), 2),
            "max_ms": round(max(measurements), 2),
            "count": count,
            "p50": round(sorted_measurements[int(count * 0.5)], 2),
            "p95": round(sorted_measurements[int(count * 0.95)] if count >= 20 else sorted_measurements[-1], 2),
            "p99": round(sorted_measurements[int(count * 0.99)] if count >= 100 else sorted_measurements[-1], 2),
        }

    return stats


def get_slow_endpoints(limit: int = 10) -> List[Dict]:
    """
    Gibt die letzten langsamen Endpoint-Calls zurück.

    Args:
        limit: Max Anzahl der Ergebnisse

    Returns:
        List of {"endpoint": "...", "duration_ms": 123.45, ...}
    """
    return _slow_endpoints[-limit:]


def get_slowest_endpoints(top_n: int = 10) -> List[Dict]:
    """
    Gibt die Top N langsamsten Endpoints nach durchschnittlicher Zeit zurück.

    Args:
        top_n: Anzahl der Ergebnisse

    Returns:
        List of {"endpoint": "...", "avg_ms": 123.45, ...}
    """
    stats = get_performance_stats()

    sorted_endpoints = sorted(
        stats.items(),
        key=lambda x: x[1]["avg_ms"],
        reverse=True
    )

    return [
        {"endpoint": name, **data}
        for name, data in sorted_endpoints[:top_n]
    ]


def clear_performance_stats():
    """Löscht alle Performance-Statistiken (für Tests)"""
    _performance_stats.clear()
    _slow_endpoints.clear()
