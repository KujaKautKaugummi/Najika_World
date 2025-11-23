"""
User Analytics and Event Tracking Module
Tracks user behavior, events, and sessions for analytics
"""

import time
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass, asdict
from enum import Enum


logger = logging.getLogger(__name__)


class EventType(Enum):
    """Standard event types"""
    PAGE_VIEW = "page_view"
    BUTTON_CLICK = "button_click"
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTRATION = "registration"
    CHARACTER_CREATED = "character_created"
    COMBAT_START = "combat_start"
    COMBAT_END = "combat_end"
    QUEST_STARTED = "quest_started"
    QUEST_COMPLETED = "quest_completed"
    ITEM_ACQUIRED = "item_acquired"
    ITEM_USED = "item_used"
    TRAINING_JOB_STARTED = "training_job_started"
    TRAINING_JOB_COMPLETED = "training_job_completed"
    ERROR = "error"
    CUSTOM = "custom"


@dataclass
class UserEvent:
    """
    User event data structure
    """
    event_id: str
    user_id: int
    event_type: str
    timestamp: float
    session_id: str
    event_data: Dict[str, Any]
    metadata: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


@dataclass
class UserSession:
    """
    User session data structure
    """
    session_id: str
    user_id: int
    start_time: float
    end_time: Optional[float]
    duration: float
    event_count: int
    page_views: int
    ip_address: str
    user_agent: str
    device_type: str
    browser: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class UserTracker:
    """
    User analytics tracker
    """

    def __init__(self):
        """Initialize user tracker"""
        self.events: List[UserEvent] = []
        self.sessions: Dict[str, UserSession] = {}
        self.user_data: Dict[int, Dict[str, Any]] = defaultdict(lambda: {
            'total_events': 0,
            'total_sessions': 0,
            'total_time': 0,
            'first_seen': None,
            'last_seen': None,
            'events_by_type': defaultdict(int)
        })

        # Session configuration
        self.session_timeout = 1800  # 30 minutes

    def track_event(
        self,
        user_id: int,
        event_type: str,
        event_data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserEvent:
        """
        Track a user event

        Args:
            user_id: User identifier
            event_type: Type of event
            event_data: Event-specific data
            metadata: Additional metadata
            session_id: Session identifier
            ip_address: User's IP address
            user_agent: User's user agent string

        Returns:
            Created user event
        """
        import uuid

        # Generate event ID
        event_id = str(uuid.uuid4())

        # Get or create session
        if session_id is None:
            session_id = self.get_or_create_session(
                user_id,
                ip_address,
                user_agent
            )

        # Create event
        event = UserEvent(
            event_id=event_id,
            user_id=user_id,
            event_type=event_type,
            timestamp=time.time(),
            session_id=session_id,
            event_data=event_data or {},
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Store event
        self.events.append(event)

        # Update user data
        user_data = self.user_data[user_id]
        user_data['total_events'] += 1
        user_data['events_by_type'][event_type] += 1
        user_data['last_seen'] = event.timestamp

        if user_data['first_seen'] is None:
            user_data['first_seen'] = event.timestamp

        # Update session
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.event_count += 1
            session.end_time = event.timestamp
            session.duration = session.end_time - session.start_time

            if event_type == EventType.PAGE_VIEW.value:
                session.page_views += 1

        logger.info(f"Tracked event: {event_type} for user {user_id}")
        return event

    def get_or_create_session(
        self,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> str:
        """
        Get or create user session

        Args:
            user_id: User identifier
            ip_address: User's IP address
            user_agent: User's user agent string

        Returns:
            Session ID
        """
        import uuid

        # Check for active session
        active_session = self.get_active_session(user_id)

        if active_session:
            return active_session.session_id

        # Create new session
        session_id = str(uuid.uuid4())

        device_type, browser = self.parse_user_agent(user_agent or "")

        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            start_time=time.time(),
            end_time=None,
            duration=0,
            event_count=0,
            page_views=0,
            ip_address=ip_address or "unknown",
            user_agent=user_agent or "unknown",
            device_type=device_type,
            browser=browser
        )

        self.sessions[session_id] = session
        self.user_data[user_id]['total_sessions'] += 1

        logger.info(f"Created new session {session_id} for user {user_id}")
        return session_id

    def get_active_session(self, user_id: int) -> Optional[UserSession]:
        """
        Get active session for user

        Args:
            user_id: User identifier

        Returns:
            Active session or None
        """
        current_time = time.time()

        for session in self.sessions.values():
            if session.user_id != user_id:
                continue

            # Check if session is still active
            last_activity = session.end_time or session.start_time
            if current_time - last_activity < self.session_timeout:
                return session

        return None

    def end_session(self, session_id: str):
        """
        End a session

        Args:
            session_id: Session identifier
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.end_time = time.time()
            session.duration = session.end_time - session.start_time

            # Update user total time
            self.user_data[session.user_id]['total_time'] += session.duration

            logger.info(f"Ended session {session_id} (duration: {session.duration:.2f}s)")

    def get_user_events(
        self,
        user_id: int,
        event_type: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: int = 100
    ) -> List[UserEvent]:
        """
        Get events for a user

        Args:
            user_id: User identifier
            event_type: Filter by event type
            start_time: Start timestamp
            end_time: End timestamp
            limit: Maximum number of events

        Returns:
            List of user events
        """
        events = [
            event for event in self.events
            if event.user_id == user_id
        ]

        # Filter by event type
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        # Filter by time range
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]

        # Sort by timestamp (newest first)
        events.sort(key=lambda e: e.timestamp, reverse=True)

        return events[:limit]

    def get_user_analytics(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get analytics for a user

        Args:
            user_id: User identifier
            start_date: Start date
            end_date: End date

        Returns:
            User analytics data
        """
        user_data = self.user_data[user_id]

        # Get events in date range
        start_time = start_date.timestamp() if start_date else None
        end_time = end_date.timestamp() if end_date else None

        events = self.get_user_events(
            user_id,
            start_time=start_time,
            end_time=end_time,
            limit=10000
        )

        # Get sessions
        sessions = [
            session for session in self.sessions.values()
            if session.user_id == user_id
        ]

        # Calculate metrics
        total_sessions = len(sessions)
        avg_session_duration = (
            sum(s.duration for s in sessions) / total_sessions
            if total_sessions > 0 else 0
        )

        avg_events_per_session = (
            len(events) / total_sessions
            if total_sessions > 0 else 0
        )

        # Event type distribution
        event_type_dist = defaultdict(int)
        for event in events:
            event_type_dist[event.event_type] += 1

        return {
            'user_id': user_id,
            'total_events': len(events),
            'total_sessions': total_sessions,
            'avg_session_duration': avg_session_duration,
            'avg_events_per_session': avg_events_per_session,
            'first_seen': user_data['first_seen'],
            'last_seen': user_data['last_seen'],
            'event_type_distribution': dict(event_type_dist),
            'recent_events': [e.to_dict() for e in events[:10]]
        }

    def get_overall_analytics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get overall analytics

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Overall analytics data
        """
        start_time = start_date.timestamp() if start_date else None
        end_time = end_date.timestamp() if end_date else None

        # Filter events
        events = self.events
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]

        # Unique users
        unique_users = len(set(e.user_id for e in events))

        # Event type distribution
        event_type_dist = defaultdict(int)
        for event in events:
            event_type_dist[event.event_type] += 1

        # Daily active users
        daily_active_users = self.calculate_daily_active_users(start_date, end_date)

        return {
            'total_events': len(events),
            'unique_users': unique_users,
            'total_sessions': len(self.sessions),
            'avg_events_per_user': len(events) / unique_users if unique_users > 0 else 0,
            'event_type_distribution': dict(event_type_dist),
            'daily_active_users': daily_active_users
        }

    def calculate_daily_active_users(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, int]:
        """
        Calculate daily active users

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary of date -> active user count
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()

        daily_users = defaultdict(set)

        for event in self.events:
            event_date = datetime.fromtimestamp(event.timestamp).date()

            if start_date.date() <= event_date <= end_date.date():
                daily_users[event_date.isoformat()].add(event.user_id)

        return {
            date: len(users)
            for date, users in sorted(daily_users.items())
        }

    @staticmethod
    def parse_user_agent(user_agent: str) -> tuple[str, str]:
        """
        Parse user agent string

        Args:
            user_agent: User agent string

        Returns:
            Tuple of (device_type, browser)
        """
        ua_lower = user_agent.lower()

        # Detect device type
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            device_type = 'mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            device_type = 'tablet'
        else:
            device_type = 'desktop'

        # Detect browser
        if 'chrome' in ua_lower and 'edg' not in ua_lower:
            browser = 'Chrome'
        elif 'firefox' in ua_lower:
            browser = 'Firefox'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            browser = 'Safari'
        elif 'edg' in ua_lower:
            browser = 'Edge'
        elif 'opera' in ua_lower or 'opr' in ua_lower:
            browser = 'Opera'
        else:
            browser = 'Unknown'

        return device_type, browser

    def cleanup_old_events(self, max_age_days: int = 90):
        """
        Remove events older than max_age_days

        Args:
            max_age_days: Maximum age in days
        """
        cutoff_time = time.time() - (max_age_days * 86400)

        original_count = len(self.events)
        self.events = [e for e in self.events if e.timestamp >= cutoff_time]
        removed = original_count - len(self.events)

        if removed > 0:
            logger.info(f"Cleaned up {removed} old events")

    def export_events(
        self,
        format: str = 'json',
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> str:
        """
        Export events to string format

        Args:
            format: Export format ('json' or 'csv')
            start_time: Start timestamp
            end_time: End timestamp

        Returns:
            Exported events as string
        """
        events = self.events

        # Filter by time
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]

        if format == 'json':
            return json.dumps([e.to_dict() for e in events], indent=2)
        elif format == 'csv':
            import csv
            import io

            output = io.StringIO()
            if events:
                writer = csv.DictWriter(output, fieldnames=events[0].to_dict().keys())
                writer.writeheader()
                for event in events:
                    writer.writerow(event.to_dict())

            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")


# Global tracker instance
_user_tracker = None


def get_user_tracker() -> UserTracker:
    """
    Get global user tracker instance

    Returns:
        User tracker instance
    """
    global _user_tracker
    if _user_tracker is None:
        _user_tracker = UserTracker()
    return _user_tracker


def track_event(
    user_id: int,
    event_type: str,
    event_data: Optional[Dict[str, Any]] = None,
    **kwargs
) -> UserEvent:
    """
    Track a user event (convenience function)

    Args:
        user_id: User identifier
        event_type: Type of event
        event_data: Event-specific data
        **kwargs: Additional arguments

    Returns:
        Created user event
    """
    tracker = get_user_tracker()
    return tracker.track_event(user_id, event_type, event_data, **kwargs)
