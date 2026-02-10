"""
Najika Compatibility API
Endpoints for compatibility with old najika_server.py + missing frontend stubs
Prevents 404 errors from frontend JS that calls legacy endpoints.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import random
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Najika Compatibility"])


# ============================================================================
# CORE STATUS (used by system_monitor.js, command_system.js)
# ============================================================================

@router.get("/status")
async def status():
    """Legacy status endpoint (command_system.js, system_monitor.js)"""
    return {
        "status": "online",
        "personality": "megumin",
        "mood": "happy",
        "energy": 85,
        "timestamp": datetime.now().isoformat(),
        "backend": "fastapi",
        "version": "2.0.0"
    }


@router.get("/najika/status")
async def najika_status():
    """Najika status (system_monitor.js, najika_fullscreen.js)"""
    return {
        "status": "online",
        "personality": "megumin",
        "mood": "happy",
        "energy": 85,
        "hunger": 80,
        "happiness": 75,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "backend": "fastapi", "version": "2.0.0"}


@router.get("/cloud/status")
async def cloud_status():
    """Cloud provider status"""
    return {"cloud_enabled": False, "provider": "local", "status": "offline"}


# ============================================================================
# NAJIKA CARE (command_system.js, najika_fullscreen.js)
# ============================================================================

@router.post("/najika/praise")
async def praise_najika():
    """Praise Najika (command_system.js)"""
    return {
        "status": "ok",
        "action": "praise",
        "response": "Hehe~ Danke, Mr. K! *strahlt*",
        "mood_change": +5,
        "mood": "happy"
    }


@router.post("/najika/scold")
async def scold_najika():
    """Scold Najika (command_system.js)"""
    return {
        "status": "ok",
        "action": "scold",
        "response": "H-Hmph! Das war nicht nett...",
        "mood_change": -10,
        "mood": "tsundere"
    }


@router.post("/najika/equipment")
async def najika_equipment():
    """Equipment endpoint"""
    return {
        "weapon": "staff",
        "armor": "mage_robe",
        "accessory": "explosion_ring",
        "stats": {"attack": 50, "defense": 30, "magic": 100}
    }


@router.post("/room/actions")
async def room_actions(request: Request):
    """Room actions (safe_functions.js)"""
    try:
        body = await request.json()
        room = body.get("room", "Wohnzimmer")
    except Exception:
        room = "Wohnzimmer"

    actions_map = {
        "Wohnzimmer": ["Chat", "Minigame", "Stats"],
        "Schlafzimmer": ["Sleep", "Save", "Stats"],
        "Kueche": ["Cook", "Eat", "Stats"],
        "Garten": ["Garden", "Plant", "Stats"],
        "Musikraum": ["Play", "Listen", "Stats"],
        "Trainingszimmer": ["Train", "Battle", "Stats"],
        "Kampfarena": ["Fight", "Tournament", "Stats"],
    }
    return {"room": room, "actions": actions_map.get(room, ["Chat", "Stats"])}


# ============================================================================
# PLAYER (npc_interaction.js, world_map_api.js)
# ============================================================================

@router.get("/player/gold")
async def get_player_gold():
    """Player gold (npc_interaction.js)"""
    return {"gold": 500, "player_id": "player1"}


@router.get("/player/session")
async def get_player_session():
    """Player session (world_map_api.js)"""
    return {
        "player_id": "player1",
        "session_id": "default",
        "position": {"x": 4800, "y": 4800},
        "region": "Samtmoos-Tiefwald",
        "level": 1
    }


@router.post("/shop/buy")
async def shop_buy(request: Request):
    """Buy from shop (npc_interaction.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    return {
        "status": "ok",
        "item": body.get("item", "unknown"),
        "gold_remaining": 450,
        "message": "Einkauf erfolgreich!"
    }


@router.post("/service/use")
async def service_use(request: Request):
    """Use NPC service (npc_interaction.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    return {
        "status": "ok",
        "service": body.get("service", "unknown"),
        "message": "Service genutzt!"
    }


# ============================================================================
# ARENA COMPAT (nemesis_arena_frontend.js uses /api/arena/*)
# Backend has routes at /api/v1/game/arena/* - these are stubs
# ============================================================================

@router.get("/arena/status")
async def arena_status():
    """Arena status (nemesis_arena_frontend.js)"""
    return {
        "player_rank": "Neuling",
        "total_monsters": 12,
        "events": [],
        "wave_available": True
    }


@router.get("/arena/monsters")
async def arena_monsters():
    """Arena monsters list (nemesis_arena_frontend.js)"""
    return {
        "success": True,
        "monsters": [
            {"id": 1, "name": "Schattenlaurer", "rank": "NOBODY", "level": 3,
             "type": "SCHATTENLAURER", "hp": 45, "max_hp": 45, "region": "Samtmoos-Tiefwald"},
            {"id": 2, "name": "Pilzterror", "rank": "GLADIATOR", "level": 5,
             "type": "PILZTERROR", "hp": 70, "max_hp": 70, "region": "Kristallhoehlen"},
            {"id": 3, "name": "Nebelwandler", "rank": "NOBODY", "level": 2,
             "type": "NEBELWANDLER", "hp": 30, "max_hp": 30, "region": "Nebelwald"},
        ],
        "count": 3
    }


@router.post("/arena/challenge")
async def arena_challenge(request: Request):
    """Start arena challenge (nemesis_arena_frontend.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    return {
        "success": True,
        "battle_id": f"battle_{random.randint(1000, 9999)}",
        "monster_id": body.get("monster_id", 1),
        "message": "Kampf beginnt!",
        "player": {"hp": 100, "max_hp": 100, "mp": 50, "max_mp": 50},
        "enemy": {"name": "Arena Monster", "hp": 60, "max_hp": 60, "level": 3}
    }


@router.post("/arena/battle/action")
async def arena_battle_action(request: Request):
    """Arena battle action (nemesis_arena_frontend.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}

    action = body.get("action", "attack")
    damage = random.randint(8, 25)
    enemy_damage = random.randint(5, 15)

    return {
        "success": True,
        "action": action,
        "damage_dealt": damage,
        "damage_taken": enemy_damage,
        "player": {"hp": 85, "max_hp": 100},
        "enemy": {"hp": 35, "max_hp": 60},
        "message": f"{action} trifft! {damage} Schaden!",
        "battle_over": False
    }


@router.get("/arena/monster/{monster_id}")
async def arena_monster_detail(monster_id: int):
    """Arena monster detail (nemesis_arena_frontend.js)"""
    return {
        "id": monster_id,
        "name": f"Monster #{monster_id}",
        "rank": "NOBODY",
        "level": 3,
        "type": "SCHATTENLAURER",
        "hp": 45, "max_hp": 45,
        "strengths": ["Schattenschlag"],
        "weaknesses": ["Licht"],
        "region": "Samtmoos-Tiefwald",
        "kills": 0,
        "deaths": 0
    }


@router.post("/arena/wave-battle")
async def arena_wave_battle(request: Request):
    """Arena wave battle (nemesis_arena_frontend.js)"""
    return {
        "success": True,
        "wave": 1,
        "enemies": [
            {"name": "Wellenmonster A", "hp": 30, "max_hp": 30, "level": 2},
            {"name": "Wellenmonster B", "hp": 25, "max_hp": 25, "level": 1},
        ],
        "player": {"hp": 100, "max_hp": 100},
        "message": "Welle 1 beginnt!"
    }


@router.get("/arena/hierarchy")
async def arena_hierarchy():
    """Arena hierarchy (nemesis_arena_frontend.js)"""
    return {
        "hierarchy": {
            "overlord": None,
            "warlords": [],
            "captains": [
                {"id": 2, "name": "Pilzterror", "rank": "CAPTAIN", "level": 5}
            ],
            "gladiators": [
                {"id": 1, "name": "Schattenlaurer", "rank": "GLADIATOR", "level": 3},
                {"id": 3, "name": "Nebelwandler", "rank": "GLADIATOR", "level": 2},
            ]
        }
    }


# ============================================================================
# QUESTS (quest_ui.js)
# ============================================================================

@router.get("/quests/stats")
async def quest_stats():
    """Quest stats (quest_ui.js)"""
    return {
        "total_completed": 0,
        "active_count": 0,
        "available_count": 3,
        "level": 1
    }


@router.get("/quests/active")
async def quests_active():
    """Active quests (quest_ui.js)"""
    return {"quests": [], "count": 0}


@router.get("/quests/available")
async def quests_available(level: int = 1):
    """Available quests (quest_ui.js)"""
    return {
        "quests": [
            {"id": 1, "name": "Erste Schritte", "description": "Erkunde die Welt",
             "reward_gold": 50, "reward_xp": 100, "level_req": 1},
            {"id": 2, "name": "Pilze sammeln", "description": "Sammle 5 Pilze im Wald",
             "reward_gold": 30, "reward_xp": 60, "level_req": 1},
            {"id": 3, "name": "Arena-Debut", "description": "Gewinne deinen ersten Arena-Kampf",
             "reward_gold": 100, "reward_xp": 200, "level_req": 1},
        ],
        "count": 3
    }


@router.post("/quests/start")
async def quest_start(request: Request):
    """Start quest (quest_ui.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    return {
        "status": "ok",
        "quest_id": body.get("quest_id", 1),
        "message": "Quest gestartet!"
    }


@router.post("/quests/complete")
async def quest_complete(request: Request):
    """Complete quest (quest_ui.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    return {
        "status": "ok",
        "quest_id": body.get("quest_id", 1),
        "rewards": {"gold": 50, "xp": 100},
        "message": "Quest abgeschlossen!"
    }


# ============================================================================
# MINIGAMES (safe_functions.js)
# ============================================================================

@router.post("/minigame/garden")
async def minigame_garden(request: Request):
    """Garden minigame (safe_functions.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    mode = body.get("mode", "check")
    return {
        "status": "ok",
        "mode": mode,
        "plants": [
            {"name": "Sonnenlilie", "growth": 45, "water_needed": True},
            {"name": "Kristallmoos", "growth": 80, "water_needed": False},
        ],
        "message": "Garten-Update!"
    }


@router.post("/minigame/rhythm")
async def minigame_rhythm():
    """Rhythm minigame (safe_functions.js)"""
    return {
        "status": "ok",
        "song": "Explosion March",
        "bpm": 120,
        "notes": ["C", "D", "E", "G", "A"],
        "message": "Rhythmus-Spiel gestartet!"
    }


@router.post("/minigame/reflex")
async def minigame_reflex():
    """Reflex minigame (safe_functions.js)"""
    return {
        "status": "ok",
        "target_time_ms": random.randint(500, 2000),
        "message": "Reflex-Test bereit!"
    }


@router.post("/heal")
async def heal():
    """Heal action (safe_functions.js)"""
    return {
        "status": "ok",
        "healed": 30,
        "hp": 100,
        "max_hp": 100,
        "message": "Heilung erfolgreich!"
    }


@router.post("/crafting")
async def crafting(request: Request):
    """Crafting action (safe_functions.js)"""
    return {
        "status": "ok",
        "crafted": None,
        "message": "Kein Rezept ausgewaehlt",
        "recipes_available": 5
    }


# ============================================================================
# EVENTS (oregon.js, safe_functions.js)
# ============================================================================

@router.post("/event/next")
async def event_next():
    """Next event (oregon.js, safe_functions.js)"""
    events = [
        {"type": "encounter", "text": "Ein Reisender erscheint am Wegesrand.", "choices": ["Grüßen", "Ignorieren"]},
        {"type": "treasure", "text": "Du findest eine alte Truhe!", "choices": ["Öffnen", "Weitergehen"]},
        {"type": "weather", "text": "Dunkle Wolken ziehen auf.", "choices": ["Unterschlupf suchen", "Weitergehen"]},
    ]
    return random.choice(events)


# ============================================================================
# CHAOS EVENTS (chaos_event_ui.js)
# ============================================================================

@router.get("/chaos/check_event")
async def chaos_check_event():
    """Check for chaos event (chaos_event_ui.js)"""
    return {"event_active": False, "event": None}


@router.post("/chaos/execute_choice")
async def chaos_execute_choice(request: Request):
    """Execute chaos event choice (chaos_event_ui.js)"""
    return {"status": "ok", "result": "no_event", "message": "Kein aktives Chaos-Event"}


# ============================================================================
# DUNGEON (dungeon_ui.js)
# ============================================================================

@router.get("/dungeon/biomes")
async def dungeon_biomes():
    """Dungeon biomes (dungeon_ui.js)"""
    return {
        "biomes": [
            {"id": "forest", "name": "Samtmoos-Tiefwald", "difficulty_range": [1, 5]},
            {"id": "crystal", "name": "Kristallhoehlen", "difficulty_range": [3, 8]},
            {"id": "shadow", "name": "Schattenreich", "difficulty_range": [5, 10]},
        ]
    }


@router.get("/dungeon/difficulties")
async def dungeon_difficulties():
    """Dungeon difficulties (dungeon_ui.js)"""
    return {
        "difficulties": [
            {"id": 1, "name": "Leicht", "enemy_mult": 0.8},
            {"id": 2, "name": "Normal", "enemy_mult": 1.0},
            {"id": 3, "name": "Schwer", "enemy_mult": 1.5},
        ]
    }


@router.get("/dungeon/generate/{biome}/{difficulty}/{floor}")
async def dungeon_generate(biome: str, difficulty: int, floor: int):
    """Generate dungeon floor (dungeon_ui.js)"""
    return {
        "biome": biome,
        "difficulty": difficulty,
        "floor": floor,
        "rooms": random.randint(3, 7),
        "enemies": random.randint(2, 5),
        "treasure_chests": random.randint(0, 2),
        "boss": floor % 5 == 0,
        "message": f"Dungeon {biome} Floor {floor} generiert!"
    }


# ============================================================================
# ECHOHARP / BARD (echoharp_ui.js)
# ============================================================================

@router.get("/echoharp/status")
async def echoharp_status():
    return {"status": "available", "active_song": None}

@router.get("/bard/status")
async def bard_status():
    return {"status": "available", "active_performance": None}

@router.get("/echoharp/witness-item")
async def echoharp_witness_item(spieler_id: str = "player1"):
    return {"has_item": False, "item": None}

@router.get("/bard/item/status")
async def bard_item_status(spieler_id: str = "player1"):
    return {"has_item": False, "item": None}

@router.get("/echoharp/stories")
async def echoharp_stories(limit: int = 10):
    return {"stories": [], "count": 0}

@router.get("/bard/stories")
async def bard_stories(limit: int = 10):
    return {"stories": [], "count": 0}

@router.get("/echoharp/deeds")
async def echoharp_deeds(spieler_id: str = "player1"):
    return {"deeds": [], "count": 0}

@router.get("/bard/player/deeds")
async def bard_player_deeds(spieler_id: str = "player1"):
    return {"deeds": [], "count": 0}

@router.get("/echoharp/quests")
async def echoharp_quests(spieler_id: str = "player1"):
    return {"quests": [], "count": 0}

@router.get("/bard/quest")
async def bard_quest(spieler_id: str = "player1"):
    return {"quest": None, "active": False}

@router.post("/echoharp/quest/accept")
async def echoharp_quest_accept():
    return {"status": "ok", "message": "Keine Quest verfuegbar"}

@router.post("/echoharp/witness/activate")
async def echoharp_witness_activate():
    return {"status": "ok", "activated": False}

@router.post("/bard/item/activate/before")
async def bard_item_activate_before():
    return {"status": "ok", "activated": False}

@router.post("/bard/item/activate/after")
async def bard_item_activate_after():
    return {"status": "ok", "activated": False}


# ============================================================================
# VOICE CALL (voice_call.js)
# ============================================================================

@router.post("/voice_call/start")
async def voice_call_start():
    """Start voice call (voice_call.js)"""
    return {"status": "ok", "call_id": "vc_001", "message": "Voice-Call gestartet"}

@router.post("/voice_call/audio")
async def voice_call_audio():
    """Send audio in voice call (voice_call.js)"""
    return {"status": "ok", "transcription": "", "response": ""}

@router.post("/voice_call/end")
async def voice_call_end():
    """End voice call (voice_call.js)"""
    return {"status": "ok", "message": "Voice-Call beendet"}


# ============================================================================
# LOGGING (najika_logger.js)
# ============================================================================

@router.post("/log/claude")
async def log_claude(request: Request):
    """Log from frontend (najika_logger.js)"""
    try:
        body = await request.json()
        print(f"[FRONTEND LOG] {body.get('level', 'INFO')}: {body.get('message', '')}")
    except Exception:
        pass
    return {"status": "ok"}


# ============================================================================
# MONITORING (system_monitor.js)
# ============================================================================

@router.get("/training/status")
async def training_status():
    """Training status (system_monitor.js)"""
    return {
        "status": "idle",
        "current_job": None,
        "queue": [],
        "total_completed": 0
    }


@router.get("/security/status")
async def security_status():
    """Security status (system_monitor.js)"""
    return {
        "status": "secure",
        "threats": 0,
        "last_scan": datetime.now().isoformat(),
        "firewall": "active"
    }


@router.get("/memory/export")
async def memory_export():
    """Memory export (system_monitor.js)"""
    return {
        "status": "ok",
        "collections": 6,
        "total_entries": 2556,
        "exported": False,
        "message": "Use /api/memory/stats for details"
    }


# ============================================================================
# SLIME COMPAT (slime_companion_ui.js uses different endpoint names)
# ============================================================================

@router.get("/slime/types")
async def slime_types():
    """Slime types (slime_companion_ui.js)"""
    return {
        "types": [
            {"id": "water", "name": "Wasserschleim", "element": "water", "color": "#4488ff"},
            {"id": "fire", "name": "Feuerschleim", "element": "fire", "color": "#ff4444"},
            {"id": "earth", "name": "Erdschleim", "element": "earth", "color": "#88aa44"},
            {"id": "shadow", "name": "Schattenschleim", "element": "shadow", "color": "#664488"},
        ]
    }


@router.get("/slime/all")
async def slime_all():
    """All player slimes (slime_companion_ui.js)"""
    return {"slimes": [], "count": 0}


@router.post("/slime/update")
async def slime_update():
    """Update slime tick (slime_companion_ui.js)"""
    return {"status": "ok", "updated": True}


@router.post("/slime/play")
async def slime_play(request: Request):
    """Play with slime (slime_companion_ui.js)"""
    return {"status": "ok", "happiness_gained": 10, "message": "Schleim ist gluecklich!"}


@router.post("/slime/heal")
async def slime_heal(request: Request):
    """Heal slime (slime_companion_ui.js)"""
    return {"status": "ok", "healed": True, "message": "Schleim geheilt!"}


@router.post("/slime/evolve")
async def slime_evolve(request: Request):
    """Evolve slime (slime_companion_ui.js)"""
    return {"status": "ok", "evolved": False, "message": "Nicht genug XP fuer Evolution"}


@router.post("/slime/rename")
async def slime_rename(request: Request):
    """Rename slime (slime_companion_ui.js)"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    return {"status": "ok", "new_name": body.get("name", "Schleim"), "message": "Umbenannt!"}


@router.post("/slime/activate")
async def slime_activate(request: Request):
    """Activate slime as companion (slime_companion_ui.js)"""
    return {"status": "ok", "active": True, "message": "Schleim aktiviert!"}


@router.post("/slime/train")
async def slime_train(request: Request):
    """Train slime (slime_companion_ui.js)"""
    return {"status": "ok", "xp_gained": 15, "message": "Training abgeschlossen!"}


@router.post("/slime/status")
async def slime_status_post():
    """Slime status via POST (slime_companion.js)"""
    return {"status": "ok", "slime": None, "has_slime": False}


# ============================================================================
# FILE MANAGER / CODE EDITOR (file_manager.js, code_editor.js)
# These are dev tools - return safe defaults
# ============================================================================

@router.get("/file/list")
async def file_list():
    return {"files": [], "message": "File Manager deaktiviert im FastAPI-Modus"}

@router.get("/file/read")
async def file_read():
    return {"content": "", "message": "File Manager deaktiviert"}

@router.post("/file/write")
async def file_write():
    return {"status": "error", "message": "File Manager deaktiviert im FastAPI-Modus"}

@router.post("/file/delete")
async def file_delete():
    return {"status": "error", "message": "File Manager deaktiviert"}

@router.post("/file/rename")
async def file_rename():
    return {"status": "error", "message": "File Manager deaktiviert"}

@router.post("/code/execute")
async def code_execute():
    return {"status": "error", "output": "", "message": "Code-Ausfuehrung deaktiviert im FastAPI-Modus"}
