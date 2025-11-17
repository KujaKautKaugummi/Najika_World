"""
Najika World Analytics & Monitoring Module
Comprehensive analytics and performance monitoring
"""

from backend.analytics.user_tracking import (
    UserTracker,
    UserEvent,
    UserSession,
    EventType,
    get_user_tracker,
    track_event
)

from backend.analytics.game_analytics import (
    GameAnalytics,
    CombatMetrics,
    ProgressionMetrics,
    EconomyMetrics,
    SocialMetrics,
    get_game_analytics
)

from backend.analytics.performance_monitoring import (
    PerformanceMonitor,
    APIMetrics,
    SystemMetrics,
    PerformanceAlert,
    get_performance_monitor,
    monitor_performance
)


__all__ = [
    # User Tracking
    'UserTracker',
    'UserEvent',
    'UserSession',
    'EventType',
    'get_user_tracker',
    'track_event',

    # Game Analytics
    'GameAnalytics',
    'CombatMetrics',
    'ProgressionMetrics',
    'EconomyMetrics',
    'SocialMetrics',
    'get_game_analytics',

    # Performance Monitoring
    'PerformanceMonitor',
    'APIMetrics',
    'SystemMetrics',
    'PerformanceAlert',
    'get_performance_monitor',
    'monitor_performance'
]

__version__ = '1.0.0'
