"""
Oregon Trail Models - Najika World
Database models for Oregon Trail events system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class OregonTrailJourney(Base):
    """Player's Oregon Trail journey"""
    __tablename__ = "oregon_trail_journeys"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Journey Status
    active = Column(Boolean, default=True)
    completed = Column(Boolean, default=False)

    # Progress
    distance_traveled = Column(Integer, default=0)  # miles
    days_elapsed = Column(Integer, default=0)
    current_location = Column(String(100), default="Independence, Missouri")

    # Party Stats
    party_health = Column(Float, default=100.0)  # Average health
    party_morale = Column(Float, default=100.0)
    party_members = Column(JSON, default=[])  # List of party member names
    alive_members = Column(Integer, default=4)

    # Resources
    food = Column(Integer, default=200)  # pounds
    water = Column(Integer, default=50)  # gallons
    money = Column(Integer, default=100)  # dollars
    ammunition = Column(Integer, default=50)  # bullets

    # Inventory
    oxen = Column(Integer, default=2)
    wagon_wheels = Column(Integer, default=2)
    wagon_axles = Column(Integer, default=1)
    wagon_tongues = Column(Integer, default=1)

    # Weather
    current_weather = Column(String(50), default="clear")  # clear, rain, storm, snow
    temperature = Column(Integer, default=70)  # Fahrenheit

    # Pace & Rations
    pace = Column(String(20), default="steady")  # slow, steady, fast, grueling
    rations = Column(String(20), default="normal")  # meager, normal, well-fed

    # Events Counter
    total_events = Column(Integer, default=0)
    deaths = Column(Integer, default=0)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    last_event_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="oregon_journeys")
    events = relationship("OregonTrailEvent", back_populates="journey", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "player_id": self.player_id,
            "active": self.active,
            "completed": self.completed,
            "distance_traveled": self.distance_traveled,
            "days_elapsed": self.days_elapsed,
            "current_location": self.current_location,
            "party_health": self.party_health,
            "party_morale": self.party_morale,
            "party_members": self.party_members or [],
            "alive_members": self.alive_members,
            "food": self.food,
            "water": self.water,
            "money": self.money,
            "ammunition": self.ammunition,
            "oxen": self.oxen,
            "wagon_wheels": self.wagon_wheels,
            "wagon_axles": self.wagon_axles,
            "wagon_tongues": self.wagon_tongues,
            "current_weather": self.current_weather,
            "temperature": self.temperature,
            "pace": self.pace,
            "rations": self.rations,
            "total_events": self.total_events,
            "deaths": self.deaths,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "last_event_at": self.last_event_at.isoformat() if self.last_event_at else None,
        }


class OregonTrailEvent(Base):
    """Log of events during journey"""
    __tablename__ = "oregon_trail_events"

    id = Column(Integer, primary_key=True, index=True)
    journey_id = Column(Integer, ForeignKey("oregon_trail_journeys.id"), nullable=False)

    # Event Details
    event_type = Column(String(50), nullable=False)  # random, weather, hunt, river, illness, etc.
    event_name = Column(String(200), nullable=False)
    event_description = Column(Text, nullable=False)

    # Choices
    choices = Column(JSON, default=[])  # List of available choices
    player_choice = Column(String(200), nullable=True)

    # Outcome
    outcome = Column(Text, nullable=True)
    success = Column(Boolean, default=True)

    # Impact (JSON: what changed)
    impact = Column(JSON, default={})  # {"food": -10, "health": -5, "morale": +10}

    # Location
    location_at_event = Column(String(100), nullable=False)
    distance_at_event = Column(Integer, default=0)

    # Timestamp
    occurred_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    journey = relationship("OregonTrailJourney", back_populates="events")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "journey_id": self.journey_id,
            "event_type": self.event_type,
            "event_name": self.event_name,
            "event_description": self.event_description,
            "choices": self.choices or [],
            "player_choice": self.player_choice,
            "outcome": self.outcome,
            "success": self.success,
            "impact": self.impact or {},
            "location_at_event": self.location_at_event,
            "distance_at_event": self.distance_at_event,
            "occurred_at": self.occurred_at.isoformat() if self.occurred_at else None,
        }
