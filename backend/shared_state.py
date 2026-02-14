"""
Shared State fuer alle FastAPI Router
Verhindert zirkulaere Imports - EINE zentrale State-Quelle.

Migriert aus najika_server.py (Zeilen 377-435).
Alle Router importieren von hier statt eigene States zu halten.
"""

import time
import sys
import os
import logging

logger = logging.getLogger("najika.shared_state")

# Backend-Dir in sys.path (fuer najika_* Imports)
_backend_dir = os.path.dirname(os.path.abspath(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# ============================================================================
# LIVING_STATE Import (graceful)
# ============================================================================

try:
    from najika_living_system import LIVING_STATE
    _living_base = LIVING_STATE.copy()
    logger.info("Living System State importiert")
except ImportError:
    _living_base = {
        "mood": "happy",
        "energy": 70,
        "hunger": 80,
        "autonomy_level": 0,
        "current_activity": None,
        "last_proactive": 0,
    }
    logger.warning("najika_living_system nicht verfuegbar, verwende Defaults")


# ============================================================================
# GLOBAL STATE (aus najika_server.py Zeilen 377-435)
# ============================================================================

STATE = {
    "history": [],
    "battle": {"hp": 100, "wave": 0, "enemies": 0},
    "private_mode": False,
    "behavior_mode": "standard",  # standard, explosion, chaos, analyse, kontrolle, private
    "bond_strength": 0,  # 0-100
    "personality_weights": {
        "megumin": 25, "harley": 25, "shiro": 25, "melissa": 25
    },
    "total_interactions": 0,
    "sse_clients": [],
    "user": {
        "level": 1,
        "xp": 0,
        "points": 0,
        "inventory": [],
        "achievements": [],
    },
    "progress": {
        "dungeon_level": 0,
        "quests_completed": [],
    },
    "najika": {
        # NEEDS (0-100, sinken ueber Zeit)
        "hunger": 100,
        "thirst": 100,
        "energy": 100,
        "hygiene": 100,
        "happiness": 100,
        # MANA
        "mana": 100,
        "max_mana": 100,
        # STATS
        "strength": 10,
        "intelligence": 10,
        "dexterity": 10,
        "charisma": 10,
        # CARE TRACKING
        "care_mistakes": 0,
        "fatigue": 0,
        "weight": 50,
        "discipline": 0,
        # GROWTH
        "level": 1,
        "xp": 0,
        "evolution_stage": "base",
        # EQUIPMENT
        "equipment": {
            "weapon": None,
            "armor": None,
            "accessory": None,
        },
        # TIMESTAMPS
        "last_fed": time.time(),
        "last_trained": time.time(),
        "last_sleep": time.time(),
        "last_update": time.time(),
    },
    "living": _living_base,
}

# Rooms (aus najika_server.py)
ROOMS = [
    "Wohnzimmer", "Schlafzimmer", "Kueche", "Badezimmer",
    "Garten", "Musikraum", "Medizin", "Terminal",
    "Studieren & Crafting", "Trainingszimmer", "Kampfarena",
    "Schwarze Muehle - Keller",
]


# ============================================================================
# SHARED SYSTEM INSTANCES (werden in lifespan initialisiert)
# ============================================================================

NAJIKA_MEMORY = None       # NajikaMemoryEnhanced (ChromaDB)
NAJIKA_SEARCH = None       # NajikaSearch (Web Search)
NAJIKA_TOR = None          # NajikaTor (Tor Browser)
NAJIKA_SECURITY = None     # NajikaSecurity (Alcatraz)


# ============================================================================
# FEATURE FLAGS (aus najika_server.py Imports)
# ============================================================================

PERSONALITY_ENGINE_ENABLED = False
RAG_ENABLED = False
NAJIKA_MIND_ENABLED = False
TTS_ENABLED = False
VOICE_CALL_ENABLED = False
SLIME_SYSTEM_ENABLED = False
NEMESIS_ARENA_ENABLED = False
QUEST_SYSTEM_ENABLED = False
COMBAT_BALANCING_ENABLED = False
DUNGEON_GENERATOR_ENABLED = False
HUNTING_SYSTEM_ENABLED = False


# ============================================================================
# HELPER
# ============================================================================

def get_state():
    """Kopie des States (ohne sse_clients)"""
    s = {k: v for k, v in STATE.items() if k != "sse_clients"}
    return s


def update_najika_stat(key, value):
    """Einzelnen Najika-Stat aendern"""
    if key in STATE["najika"]:
        STATE["najika"][key] = value
        STATE["najika"]["last_update"] = time.time()


def add_interaction():
    """Zaehlt Interaktion, erhoeht Bond"""
    STATE["total_interactions"] += 1
    if STATE["bond_strength"] < 100:
        STATE["bond_strength"] = min(100, STATE["bond_strength"] + 0.5)
