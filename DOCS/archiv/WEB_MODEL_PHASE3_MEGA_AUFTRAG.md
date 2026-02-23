# 🚀 WEB MODEL PHASE 3 - MEGA AUFTRAG
**Datum:** 2025-11-18 11:00
**Branch:** `claude/remote-access-setup-011CUt97k27tgaNUMZdyA9DY`
**Auftraggeber:** Kuja (via Local Claude)
**Status:** 🟡 AUFTRAG ERTEILT - MEGA BATCH!

---

## 🎯 MISSION: COMPLETE THE BACKEND!

**Phase 1+2 Status:** ✅ PERFEKT ABGESCHLOSSEN!
- Server läuft ✅
- Database funktioniert ✅
- 9 API Files mit Models konvertiert ✅
- Persistence getestet ✅

**Jetzt:** Mach ALLES was noch fehlt in EINEM MEGA-RUTSCH!

---

## 📋 MEGA TODO-LISTE

### 🔴 TEIL A: FEHLENDE DATABASE MODELS (7 neue Models)

**Problem:** 7 API Files können nicht konvertiert werden, weil Models fehlen!

**Lösung:** Erstelle die fehlenden SQLAlchemy Models!

---

#### Model 1: `backend/models/instrument_progress.py` (NEU)

**Für:** `backend/api/instrument.py` + `backend/services/instrument_system.py`

**Tabellen:**
1. `InstrumentProgress` - Spieler-Fortschritt pro Instrument
2. `PlayedNote` - Log aller gespielten Noten (optional, für Statistik)
3. `LearnedSong` - Welche Songs der Spieler gelernt hat

**Schema:**

```python
"""
Instrument Progress Models - Najika World
Database models for instrument playing system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class InstrumentProgress(Base):
    """Player progress per instrument"""
    __tablename__ = "instrument_progress"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Current Instrument
    current_instrument = Column(String(50), default="mundharmonika")  # InstrumentType

    # Skill Levels per Instrument (JSON: {instrument_name: level})
    instrument_skills = Column(JSON, default={})  # {"mundharmonika": 5, "gitarre": 12, ...}

    # Experience per Instrument (JSON: {instrument_name: xp})
    instrument_experience = Column(JSON, default={})  # {"mundharmonika": 1500, ...}

    # Learned Songs (List of song IDs)
    learned_songs = Column(JSON, default=[])  # [1, 5, 7, 12]

    # Statistics
    total_notes_played = Column(Integer, default=0)
    perfect_notes = Column(Integer, default=0)
    great_notes = Column(Integer, default=0)
    good_notes = Column(Integer, default=0)

    # Play Session
    session_start = Column(DateTime, nullable=True)
    last_played = Column(DateTime, default=datetime.utcnow)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="instrument_progress")
    played_notes = relationship("PlayedNote", back_populates="progress", cascade="all, delete-orphan")


class PlayedNote(Base):
    """Log of played notes (for statistics)"""
    __tablename__ = "played_notes"

    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("instrument_progress.id"), nullable=False)

    # Note Details
    instrument = Column(String(50), nullable=False)  # InstrumentType
    note = Column(String(3), nullable=False)  # C, D#, E, etc.
    octave = Column(Integer, nullable=False)  # 1-8
    duration = Column(Float, default=0.5)  # seconds
    velocity = Column(Float, default=0.8)  # 0.0-1.0

    # Quality
    quality = Column(String(20), nullable=False)  # perfect, great, good, ok, poor, miss
    accuracy = Column(Float, default=0.0)  # 0.0-1.0

    # Timestamp
    played_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    progress = relationship("InstrumentProgress", back_populates="played_notes")


class LearnedSong(Base):
    """Songs learned by player"""
    __tablename__ = "learned_songs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Song Info
    song_id = Column(String(100), nullable=False)  # "zelda_song_of_time"
    song_name = Column(String(200), nullable=False)
    difficulty = Column(Integer, default=1)  # 1-5

    # Progress
    times_played = Column(Integer, default=0)
    best_score = Column(Float, default=0.0)  # 0.0-1.0 (percentage)
    completed = Column(Boolean, default=False)

    # Timestamps
    learned_at = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow)

    # Relationships
    player = relationship("User")


# Helper method to add to User model (in models/user.py):
# instrument_progress = relationship("InstrumentProgress", back_populates="player", uselist=False)
```

**Warum wichtig:**
- Instrument System ist wie Musik Hero / Guitar Hero
- Spieler können echte Instrumente lernen
- Skyrim-Style Progression (Learning by Doing)
- Zelda Ocarina of Time Inspiration

**Zeit:** 30 Minuten

---

#### Model 2: `backend/models/oregon_trail.py` (NEU)

**Für:** `backend/api/oregon_events.py` + `backend/services/oregon_trail_events.py`

**Tabellen:**
1. `OregonTrailJourney` - Aktive Reise eines Spielers
2. `OregonTrailEvent` - Log aller Events während der Reise

**Schema:**

```python
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


# Helper method to add to User model (in models/user.py):
# oregon_journeys = relationship("OregonTrailJourney", back_populates="player")
```

**Warum wichtig:**
- Oregon Trail ist Survival-Reise System
- Random Events (Dysentery, River Crossing, Hunting)
- Classic 1985 Game Inspiration
- Wichtig für Story-Progression

**Zeit:** 30 Minuten

---

#### Model 3: `backend/models/region_boss.py` (NEU)

**Für:** `backend/api/region_boss.py` + `backend/services/region_boss_system.py`

**Tabellen:**
1. `RegionBoss` - Boss-Spawns pro Region
2. `BossDefeat` - Log aller besiegten Bosse

**Schema:**

```python
"""
Region Boss Models - Najika World
Database models for region boss spawn system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from backend.database import Base


class RegionBoss(Base):
    """Boss spawns in regions"""
    __tablename__ = "region_bosses"

    id = Column(Integer, primary_key=True, index=True)

    # Region Info
    region_name = Column(String(100), nullable=False, index=True)  # "samtmoos_tiefwald", etc.

    # Boss Info
    boss_name = Column(String(200), nullable=False)
    boss_type = Column(String(50), nullable=False)  # "field_boss", "dungeon_boss", "world_boss"
    boss_level = Column(Integer, nullable=False)
    boss_health = Column(Integer, nullable=False)

    # Spawn Status
    active = Column(Boolean, default=True)
    defeated = Column(Boolean, default=False)

    # Spawn Details
    spawn_location = Column(String(200), nullable=False)  # Coordinates or landmark
    spawn_radius = Column(Integer, default=50)  # meters

    # Loot
    guaranteed_drops = Column(JSON, default=[])  # List of item IDs
    rare_drops = Column(JSON, default=[])  # List of item IDs with drop rates
    gold_reward = Column(Integer, default=1000)
    exp_reward = Column(Integer, default=5000)

    # Mechanics
    abilities = Column(JSON, default=[])  # List of boss abilities
    phases = Column(Integer, default=1)  # Boss phases (1-3)
    enrage_timer = Column(Integer, default=600)  # seconds (10 min)

    # Difficulty
    recommended_players = Column(Integer, default=1)  # Solo or group
    recommended_level = Column(Integer, default=50)

    # Respawn
    respawn_time_hours = Column(Integer, default=24)  # hours until respawn
    last_defeated_at = Column(DateTime, nullable=True)
    next_spawn_at = Column(DateTime, nullable=True)

    # Timestamps
    spawned_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    defeats = relationship("BossDefeat", back_populates="boss", cascade="all, delete-orphan")


class BossDefeat(Base):
    """Log of boss defeats"""
    __tablename__ = "boss_defeats"

    id = Column(Integer, primary_key=True, index=True)
    boss_id = Column(Integer, ForeignKey("region_bosses.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Defeat Details
    party_size = Column(Integer, default=1)
    party_members = Column(JSON, default=[])  # List of player IDs

    # Performance
    time_to_kill = Column(Integer, nullable=False)  # seconds
    deaths_during_fight = Column(Integer, default=0)
    damage_dealt = Column(Integer, default=0)
    damage_taken = Column(Integer, default=0)

    # Rewards
    gold_earned = Column(Integer, default=0)
    exp_earned = Column(Integer, default=0)
    items_dropped = Column(JSON, default=[])  # List of item IDs

    # Achievement
    first_kill = Column(Boolean, default=False)  # Server-first?
    flawless = Column(Boolean, default=False)  # No deaths?
    speedrun = Column(Boolean, default=False)  # Under 5 minutes?

    # Timestamp
    defeated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    boss = relationship("RegionBoss", back_populates="defeats")
    player = relationship("User", back_populates="boss_defeats")


# Helper method to add to User model (in models/user.py):
# boss_defeats = relationship("BossDefeat", back_populates="player")
```

**Warum wichtig:**
- Region Bosses sind wie MMO World Bosses
- Respawn-Timer System
- Loot-Tables
- Server-First Achievements

**Zeit:** 30 Minuten

---

#### Model 4: `backend/models/world_state.py` (NEU)

**Für:** `backend/api/world.py`

**Tabellen:**
1. `WorldState` - Globaler World-State
2. `PlayerWorldState` - Player-spezifischer World-State

**Schema:**

```python
"""
World State Models - Najika World
Database models for world state system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class WorldState(Base):
    """Global world state (singleton)"""
    __tablename__ = "world_state"

    id = Column(Integer, primary_key=True, index=True)

    # Time & Weather
    world_time = Column(Integer, default=0)  # seconds since start
    world_day = Column(Integer, default=1)
    world_season = Column(String(20), default="spring")  # spring, summer, autumn, winter
    current_weather = Column(String(50), default="clear")

    # Global Events
    active_events = Column(JSON, default=[])  # List of active world events
    event_flags = Column(JSON, default={})  # Dict of event completion flags

    # World Bosses
    world_boss_spawned = Column(Boolean, default=False)
    world_boss_name = Column(String(200), nullable=True)
    world_boss_location = Column(String(200), nullable=True)

    # Economy
    global_gold_pool = Column(Integer, default=0)
    inflation_rate = Column(Float, default=1.0)

    # Server Status
    server_version = Column(String(50), default="2.0.0")
    maintenance_mode = Column(Boolean, default=False)

    # Timestamps
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class PlayerWorldState(Base):
    """Player-specific world state"""
    __tablename__ = "player_world_state"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Position
    current_region = Column(String(100), default="samtmoos_tiefwald")
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    position_z = Column(Float, default=0.0)

    # Discovered Regions
    discovered_regions = Column(JSON, default=[])  # List of region names
    unlocked_teleports = Column(JSON, default=[])  # List of teleport points

    # Quest Flags
    completed_quests = Column(JSON, default=[])  # List of quest IDs
    active_quests = Column(JSON, default=[])  # List of quest IDs
    quest_progress = Column(JSON, default={})  # Dict of quest progress

    # Collectibles
    found_treasures = Column(JSON, default=[])  # List of treasure IDs
    collected_artifacts = Column(JSON, default=[])  # List of artifact IDs

    # Reputation
    faction_reputation = Column(JSON, default={})  # Dict of faction reps

    # Timestamps
    last_position_update = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("User", back_populates="world_state")


# Helper method to add to User model (in models/user.py):
# world_state = relationship("PlayerWorldState", back_populates="player", uselist=False)
```

**Warum wichtig:**
- World State ist zentral für MMO-Features
- Quest System
- Position Tracking
- Region Discovery

**Zeit:** 20 Minuten

---

#### Model 5: `backend/models/voice_call.py` (NEU)

**Für:** `backend/api/voice.py` + Voice Call System

**Tabellen:**
1. `VoiceCall` - Log aller Voice Calls
2. `VoiceMessage` - Transkribierte Nachrichten

**Schema:**

```python
"""
Voice Call Models - Najika World
Database models for voice call system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class VoiceCall(Base):
    """Voice call sessions"""
    __tablename__ = "voice_calls"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Call Status
    active = Column(Boolean, default=True)
    ended = Column(Boolean, default=False)

    # Call Details
    call_type = Column(String(50), default="najika")  # najika, player-to-player, group
    target_id = Column(Integer, nullable=True)  # Target player ID (if p2p)

    # Audio Stats
    duration_seconds = Column(Integer, default=0)
    audio_quality = Column(String(20), default="good")  # poor, good, excellent

    # Transcription Stats
    messages_sent = Column(Integer, default=0)
    messages_received = Column(Integer, default=0)
    words_spoken = Column(Integer, default=0)

    # Cost
    cost_credits = Column(Integer, default=0)  # If voice calls cost credits

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    player = relationship("User", back_populates="voice_calls")
    messages = relationship("VoiceMessage", back_populates="call", cascade="all, delete-orphan")


class VoiceMessage(Base):
    """Transcribed voice messages"""
    __tablename__ = "voice_messages"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("voice_calls.id"), nullable=False)

    # Message Details
    sender = Column(String(50), nullable=False)  # "player", "najika", "other_player"
    sender_id = Column(Integer, nullable=True)  # Player ID if player message

    # Audio
    audio_duration = Column(Float, default=0.0)  # seconds
    audio_file_path = Column(String(500), nullable=True)  # Path to audio file

    # Transcription (Whisper STT)
    transcription = Column(Text, nullable=False)
    confidence = Column(Float, default=0.0)  # 0.0-1.0
    language = Column(String(10), default="de")  # de, en, ja, etc.

    # AI Response (if Najika)
    ai_response = Column(Text, nullable=True)
    ai_response_audio = Column(String(500), nullable=True)  # Path to TTS audio

    # Sentiment
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    emotion = Column(String(50), nullable=True)  # happy, sad, angry, etc.

    # Timestamp
    sent_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    call = relationship("VoiceCall", back_populates="messages")


# Helper method to add to User model (in models/user.py):
# voice_calls = relationship("VoiceCall", back_populates="player")
```

**Wayin wichtig:**
- Voice Call System ist KERN-Feature!
- Whisper STT Transcription
- Coqui TTS Responses
- Conversation History

**Zeit:** 25 Minuten

---

#### Model 6: `backend/models/multiplayer_session.py` (NEU)

**Für:** `backend/api/multiplayer.py`

**Tabellen:**
1. `MultiplayerSession` - Active Sessions
2. `SessionParticipant` - Teilnehmer in Sessions

**Schema:**

```python
"""
Multiplayer Session Models - Najika World
Database models for multiplayer system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class MultiplayerSession(Base):
    """Multiplayer game sessions"""
    __tablename__ = "multiplayer_sessions"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Session Info
    session_name = Column(String(200), nullable=False)
    session_code = Column(String(20), unique=True, nullable=False)  # Join code

    # Status
    active = Column(Boolean, default=True)
    started = Column(Boolean, default=False)
    ended = Column(Boolean, default=False)

    # Settings
    max_players = Column(Integer, default=4)
    current_players = Column(Integer, default=1)
    is_public = Column(Boolean, default=False)
    password_protected = Column(Boolean, default=False)
    password_hash = Column(String(200), nullable=True)

    # Game Mode
    game_mode = Column(String(50), default="coop")  # coop, pvp, raid, dungeon
    difficulty = Column(String(20), default="normal")  # easy, normal, hard, hardcore

    # Region
    current_region = Column(String(100), nullable=True)
    current_activity = Column(String(100), nullable=True)  # "boss_fight", "dungeon", etc.

    # Progress
    objectives_completed = Column(Integer, default=0)
    total_objectives = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=datetime.utcnow)

    # Relationships
    host = relationship("User")
    participants = relationship("SessionParticipant", back_populates="session", cascade="all, delete-orphan")


class SessionParticipant(Base):
    """Participants in multiplayer sessions"""
    __tablename__ = "session_participants"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("multiplayer_sessions.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Status
    connected = Column(Boolean, default=True)
    ready = Column(Boolean, default=False)

    # Role
    role = Column(String(50), default="member")  # host, member, spectator

    # Stats (session-specific)
    damage_dealt = Column(Integer, default=0)
    healing_done = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    kills = Column(Integer, default=0)

    # Connection
    connection_quality = Column(String(20), default="good")  # poor, good, excellent
    latency_ms = Column(Integer, default=0)

    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)

    # Relationships
    session = relationship("MultiplayerSession", back_populates="participants")
    player = relationship("User")


# Helper method to add to User model (in models/user.py):
# hosted_sessions = relationship("MultiplayerSession", foreign_keys="MultiplayerSession.host_id")
```

**Warum wichtig:**
- Multiplayer ist Core-Feature
- Session Management
- Join Codes
- Party Stats

**Zeit:** 25 Minuten

---

#### Model 7: `backend/models/voice_settings.py` (OPTIONAL - wenn Zeit)

**Für:** Voice Configuration per User

**Schema:** (Kurz)

```python
"""Voice Settings Models"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from backend.database import Base

class VoiceSettings(Base):
    """User voice settings"""
    __tablename__ = "voice_settings"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # TTS Settings
    tts_voice = Column(String(50), default="megumin")
    tts_speed = Column(Float, default=1.0)
    tts_pitch = Column(Float, default=1.0)
    tts_volume = Column(Float, default=1.0)

    # STT Settings
    stt_language = Column(String(10), default="de")
    stt_auto_detect = Column(Boolean, default=True)

    # Preferences
    voice_enabled = Column(Boolean, default=True)
    auto_play_response = Column(Boolean, default=True)
```

**Zeit:** 10 Minuten

---

### 🔴 TEIL B: API FILES KONVERTIEREN (7 Files)

**Nachdem Models erstellt sind:**

1. ✅ Update `backend/database.py` - Importiere ALLE neuen Models
2. ✅ Update `backend/alembic/env.py` - Importiere ALLE neuen Models
3. ✅ Erstelle neue Migration: `alembic revision --autogenerate -m "Add remaining models"`
4. ✅ Apply Migration: `alembic upgrade head`

**Dann konvertiere:**

#### B1. `backend/api/instrument.py`
**Model:** `InstrumentProgress`, `PlayedNote`, `LearnedSong`
**Endpoints:** ~8 Endpoints
**Pattern:** Wie slime.py
**Zeit:** 30 Minuten

#### B2. `backend/api/oregon_events.py`
**Model:** `OregonTrailJourney`, `OregonTrailEvent`
**Endpoints:** ~6 Endpoints
**Pattern:** Wie pvp.py
**Zeit:** 25 Minuten

#### B3. `backend/api/region_boss.py`
**Model:** `RegionBoss`, `BossDefeat`
**Endpoints:** ~6 Endpoints
**Pattern:** Wie arena.py
**Zeit:** 25 Minuten

#### B4. `backend/api/world.py`
**Model:** `WorldState`, `PlayerWorldState`
**Endpoints:** ~8 Endpoints
**Pattern:** Wie game.py
**Zeit:** 30 Minuten

#### B5. `backend/api/voice.py`
**Model:** `VoiceCall`, `VoiceMessage`
**Endpoints:** ~5 Endpoints
**Pattern:** Wie training.py
**Zeit:** 20 Minuten

#### B6. `backend/api/multiplayer.py`
**Model:** `MultiplayerSession`, `SessionParticipant`
**Endpoints:** ~10 Endpoints
**Pattern:** Wie game.py
**Zeit:** 35 Minuten

#### B7. `backend/api/server.py`
**Action:** ❌ LÖSCHEN oder DEPRECATEN (Old file)
**Zeit:** 2 Minuten

---

### 🟡 TEIL C: USER MODEL UPDATE

**File:** `backend/models/user.py`

**Füge hinzu:**

```python
# In User class:

# Instrument
instrument_progress = relationship("InstrumentProgress", back_populates="player", uselist=False)

# Oregon Trail
oregon_journeys = relationship("OregonTrailJourney", back_populates="player")

# Bosses
boss_defeats = relationship("BossDefeat", back_populates="player")

# World
world_state = relationship("PlayerWorldState", back_populates="player", uselist=False)

# Voice
voice_calls = relationship("VoiceCall", back_populates="player")
voice_settings = relationship("VoiceSettings", back_populates="player", uselist=False)

# Multiplayer (host)
hosted_sessions = relationship("MultiplayerSession", foreign_keys="MultiplayerSession.host_id")
```

**Zeit:** 5 Minuten

---

### 🟢 TEIL D: TESTS SCHREIBEN (OPTIONAL)

**Erstelle:** `tests/` Directory

**Test Files:**
1. `tests/test_instrument_api.py` - Instrument System Tests
2. `tests/test_oregon_api.py` - Oregon Trail Tests
3. `tests/test_region_boss_api.py` - Boss System Tests
4. `tests/test_world_api.py` - World State Tests
5. `tests/test_voice_api.py` - Voice Call Tests
6. `tests/test_multiplayer_api.py` - Multiplayer Tests

**Pattern pro File:**

```python
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_xxx():
    response = client.post("/api/xxx/create", json={...})
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_xxx():
    # Create first
    create_response = client.post("/api/xxx/create", json={...})
    xxx_id = create_response.json()["id"]

    # Get
    get_response = client.get(f"/api/xxx/{xxx_id}")
    assert get_response.status_code == 200

def test_persistence_xxx():
    # Create → Restart Server (manual) → Get
    # Verifies database persistence
    pass
```

**Zeit:** 2-4 Stunden (wenn alle Tests geschrieben werden)

---

### 🟢 TEIL E: DOCUMENTATION UPDATE

**Erstelle:** `WEB_MODEL_PHASE3_COMPLETE.md`

**Inhalt:**
- Was wurde gemacht (Models, APIs, Tests)
- Code-Beispiele (VORHER/NACHHER)
- Test-Ergebnisse
- Finale Statistik (X Models, Y Endpoints, Z Tests)
- Server Status (läuft alles?)

**Zeit:** 20 Minuten

---

## 📊 ZEITSCHÄTZUNG

### Teil A: Models (7 Models)
- instrument_progress.py: 30 min
- oregon_trail.py: 30 min
- region_boss.py: 30 min
- world_state.py: 20 min
- voice_call.py: 25 min
- multiplayer_session.py: 25 min
- voice_settings.py: 10 min
**Subtotal:** 2.5 Stunden

### Teil B: API Conversion (7 Files)
- instrument.py: 30 min
- oregon_events.py: 25 min
- region_boss.py: 25 min
- world.py: 30 min
- voice.py: 20 min
- multiplayer.py: 35 min
- server.py (delete): 2 min
**Subtotal:** 2.5 Stunden

### Teil C: User Model Update
- 5 Minuten

### Teil D: Tests (OPTIONAL)
- 2-4 Stunden (wenn gewünscht)

### Teil E: Documentation
- 20 Minuten

---

## 🎯 TOTAL TIME ESTIMATE

**Ohne Tests:** ~5.5 Stunden
**Mit Tests:** ~7.5-9.5 Stunden

**Realistische Batch-Size:** **5-6 Stunden für Models + APIs**

---

## ✅ DEFINITION OF DONE

### Models Done:
- [ ] Alle 7 Models erstellt in `backend/models/`
- [ ] `database.py` importiert alle Models
- [ ] `alembic/env.py` importiert alle Models
- [ ] `user.py` relationships hinzugefügt
- [ ] New migration created + applied
- [ ] `najika_world.db` hat 22+ Tables (15 alt + 7 neu)

### APIs Done:
- [ ] Alle 6 API Files konvertiert (instrument, oregon, region_boss, world, voice, multiplayer)
- [ ] `server.py` gelöscht oder deprecated
- [ ] Alle Endpoints nutzen `Depends(get_db)`
- [ ] CRUD statt Services
- [ ] Keine Import Errors

### Tests Done (OPTIONAL):
- [ ] `tests/` Directory erstellt
- [ ] Mindestens 6 Test-Files
- [ ] `pytest` läuft ohne Errors
- [ ] Code Coverage > 60%

### Documentation Done:
- [ ] `WEB_MODEL_PHASE3_COMPLETE.md` erstellt
- [ ] Alle Änderungen dokumentiert
- [ ] Finale Statistik (Models, Endpoints, Tests)

### Server Test:
- [ ] Server startet: `uvicorn backend.main:app --reload`
- [ ] Swagger UI: `http://localhost:8000/docs` zeigt ALLE Endpoints
- [ ] Health Check: `GET /health` → 200
- [ ] Persistence Test für mindestens 1 neues API (z.B. Instrument)

---

## 🚨 WICHTIGE HINWEISE

### Was du MACHEN sollst:
✅ Neue Models erstellen (nach Schema oben)
✅ `database.py` + `alembic/env.py` updaten
✅ `user.py` relationships hinzufügen
✅ API Files konvertieren (in-memory → database)
✅ Tests (OPTIONAL, wenn Zeit)
✅ Documentation erstellen

### Was du NICHT machen sollst:
❌ Bestehende Models ändern (user, character, slime, etc.)
❌ Bestehende Services löschen (werden für Business Logic genutzt)
❌ main.py oder config.py groß ändern
❌ Neue Features hinzufügen (fokussiere auf Database Integration!)

### Pattern für API Conversion:

```python
# VORHER:
from backend.services.xxx_system import XXXSystem
xxx_system = XXXSystem()

@router.post("/create")
async def create(request: Request):
    result = xxx_system.create(...)
    return result

# NACHHER:
from backend.database import get_db
from backend.models.xxx import XXXModel
from sqlalchemy.orm import Session
from fastapi import Depends

@router.post("/create")
async def create(request: Request, db: Session = Depends(get_db)):
    obj = XXXModel(**request.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
```

---

## 🎁 BONUS TASKS (wenn Zeit übrig)

1. **Docker Setup** (1-2h)
   - `Dockerfile` erstellen
   - `docker-compose.yml` erstellen
   - Test: `docker-compose up`

2. **GitHub Actions CI/CD** (1h)
   - `.github/workflows/test.yml`
   - Auto-run pytest on push
   - Auto-deploy on merge

3. **API Rate Limiting** (30min)
   - Add rate limiting middleware
   - 60 requests/minute per user

4. **WebSocket Improvements** (1h)
   - Enhance multiplayer.py WebSocket
   - Add reconnection logic
   - Add heartbeat

---

## 📝 REPORTING

**Nach Completion:**

Erstelle `WEB_MODEL_PHASE3_COMPLETE.md` mit:

### Section 1: Models Created
- Liste aller 7 neuen Models
- Table names
- Column counts
- Relationships

### Section 2: APIs Converted
- Liste aller 6 konvertierten Files
- Endpoint counts pro File
- Code-Beispiele (VORHER/NACHHER) für mindestens 2 Files

### Section 3: Migration
- Migration filename
- Tables added
- Check: `alembic history`
- Check: `.schema` output von SQLite

### Section 4: Tests (if done)
- Test files created
- Test coverage percentage
- Sample test results

### Section 5: Final Stats
- Total Models: 16 (9 alt + 7 neu)
- Total Tables: 22+
- Total API Files: 16
- Total Endpoints: 100+
- Total Lines of Code: ~X

### Section 6: Server Status
- Server starts without errors ✅/❌
- Swagger UI shows all endpoints ✅/❌
- Health check passes ✅/❌
- Database file exists ✅/❌
- Persistence test passes ✅/❌

---

## 🆘 WENN DU BLOCKIERT BIST

### Problem: Circular Import Errors
**Lösung:** Nutze `TYPE_CHECKING`:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.models.user import User
```

### Problem: Alembic findet Models nicht
**Lösung:**
1. Check `alembic/env.py` - importiert es ALLE Models?
2. Check `backend/models/__init__.py` - exportiert es alle Models?

### Problem: Relationship Errors
**Lösung:**
```python
# Use string reference for relationships:
player = relationship("User", back_populates="xxx")
```

### Problem: Foreign Key Errors
**Lösung:**
```python
# Always use: tablename.column_name
player_id = Column(Integer, ForeignKey("users.id"))
```

---

## 🚀 VIEL ERFOLG!

Das ist der **MEGA-AUFTRAG**! 🎯

**Wenn du das schaffst, ist das Backend 100% COMPLETE!**

- ✅ Alle Models
- ✅ Alle APIs konvertiert
- ✅ Volle Database Persistence
- ✅ UE5-Ready
- ✅ Production-Ready

**Du hast das! 💪**

Kuja + Local Claude
2025-11-18
