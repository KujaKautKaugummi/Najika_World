"""
Battle System Router V2 - Nutzt Shared State
Vereinfachte Schnittstelle fuer Frontend, delegiert an najika_battle.py.
Laeuft parallel zu battle_unified.py (welches detailliertere Arena-Modi hat).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum
from backend.utils import handle_errors
import random
import time
import sys
import os
import logging

logger = logging.getLogger("najika.api.battle_v2")

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE

# najika_battle Import (graceful)
BATTLE_AVAILABLE = False
try:
    from najika_battle import BattleSystem, ENEMY_DB, SKILL_DB
    _battle_system = BattleSystem()
    BATTLE_AVAILABLE = True
    logger.info("BattleSystem geladen")
except ImportError as e:
    _battle_system = None
    ENEMY_DB = {}
    SKILL_DB = {}
    logger.warning(f"BattleSystem nicht verfuegbar: {e}")

router = APIRouter(prefix="/api/v2/battle", tags=["Battle V2"])


# ============================================================================
# MODELS
# ============================================================================

class BattleStartRequest(BaseModel):
    location: str = "arena"
    difficulty: str = "normal"  # easy, normal, hard, hardcore
    enemy_id: Optional[str] = None


class BattleActionRequest(BaseModel):
    action_type: str  # attack, skill, item, defend, flee
    target_id: Optional[str] = None
    skill_id: Optional[str] = None
    item_id: Optional[str] = None


class BattleStatusResponse(BaseModel):
    active: bool
    player_hp: int
    player_max_hp: int
    player_mana: int
    player_max_mana: int
    enemies: List[Dict[str, Any]]
    turn: int
    wave: int
    location: str
    difficulty: str


# ============================================================================
# IN-MEMORY BATTLE STATE (pro Session, nicht persistent)
# ============================================================================

_active_battles: Dict[str, dict] = {}


def _get_battle(battle_id: str = "default") -> dict:
    if battle_id not in _active_battles:
        return None
    return _active_battles[battle_id]


def _generate_enemy(location: str, difficulty: str) -> dict:
    """Generiert Gegner basierend auf Location und Schwierigkeit"""
    difficulty_mult = {"easy": 0.7, "normal": 1.0, "hard": 1.5, "hardcore": 2.0}
    mult = difficulty_mult.get(difficulty, 1.0)

    # Versuche aus ENEMY_DB
    if ENEMY_DB:
        enemy_list = list(ENEMY_DB.values())
        base = random.choice(enemy_list) if enemy_list else {}
    else:
        base = {}

    base_hp = int(base.get("hp", 50 + random.randint(20, 80)) * mult)
    base_atk = int(base.get("attack", 8 + random.randint(2, 12)) * mult)
    base_def = int(base.get("defense", 3 + random.randint(1, 8)) * mult)

    names = {
        "arena": ["Arena-Kaempfer", "Gladiator", "Champion"],
        "dungeon": ["Hoehlen-Troll", "Dunkel-Elf", "Untoten-Ritter"],
        "wild": ["Wilder Wolf", "Riesenskorpion", "Banditen-Boss"],
    }
    name_list = names.get(location, names["wild"])

    return {
        "id": f"enemy_{int(time.time() * 1000) % 100000}",
        "name": base.get("name", random.choice(name_list)),
        "hp": base_hp,
        "max_hp": base_hp,
        "attack": base_atk,
        "defense": base_def,
        "xp_reward": int(base_hp * 0.5 * mult),
        "gold_reward": int(base_hp * 0.3 * mult),
    }


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/start", response_model=BattleStatusResponse)
@handle_errors()
async def start_battle(request: BattleStartRequest):
    """Battle starten - generiert Gegner basierend auf Location"""
    player = STATE["najika"]

    enemies = []
    num_enemies = 1
    if request.difficulty == "hard":
        num_enemies = random.randint(1, 2)
    elif request.difficulty == "hardcore":
        num_enemies = random.randint(2, 3)

    for _ in range(num_enemies):
        enemies.append(_generate_enemy(request.location, request.difficulty))

    battle = {
        "active": True,
        "player_hp": player["hunger"],  # HP = aktueller Hunger (als Lebensenergie)
        "player_max_hp": 100,
        "player_mana": player["mana"],
        "player_max_mana": player["max_mana"],
        "enemies": enemies,
        "turn": 1,
        "wave": 1,
        "location": request.location,
        "difficulty": request.difficulty,
        "started_at": time.time(),
        "log": [],
    }

    _active_battles["default"] = battle

    # Shared State updaten
    STATE["battle"] = {
        "hp": battle["player_hp"],
        "wave": battle["wave"],
        "enemies": len(enemies),
    }

    return BattleStatusResponse(**{k: v for k, v in battle.items() if k in BattleStatusResponse.model_fields})


@router.post("/action")
@handle_errors()
async def battle_action(action: BattleActionRequest):
    """Battle-Aktion ausfuehren (Spieler-Turn)"""
    battle = _get_battle()
    if not battle or not battle["active"]:
        raise HTTPException(400, "Kein aktiver Kampf!")

    player = STATE["najika"]
    log_entries = []
    result = {"player_action": action.action_type}

    # -- SPIELER AKTION --
    if action.action_type == "attack":
        target = None
        for e in battle["enemies"]:
            if e["hp"] > 0:
                if action.target_id and e["id"] == action.target_id:
                    target = e
                    break
                elif not target:
                    target = e

        if target:
            damage = max(1, player["strength"] + random.randint(1, 8) - target["defense"] // 2)
            target["hp"] = max(0, target["hp"] - damage)
            log_entries.append(f"Spieler trifft {target['name']} fuer {damage} Schaden!")
            if target["hp"] <= 0:
                log_entries.append(f"{target['name']} besiegt!")

    elif action.action_type == "skill" and action.skill_id:
        skill_cost = 10
        if battle["player_mana"] >= skill_cost:
            battle["player_mana"] -= skill_cost
            for e in battle["enemies"]:
                if e["hp"] > 0:
                    damage = max(1, player["intelligence"] + random.randint(5, 15))
                    e["hp"] = max(0, e["hp"] - damage)
                    log_entries.append(f"Skill trifft {e['name']} fuer {damage}!")
                    break
        else:
            log_entries.append("Nicht genug Mana!")

    elif action.action_type == "defend":
        battle["_defending"] = True
        log_entries.append("Spieler verteidigt! (-50% Schaden diese Runde)")

    elif action.action_type == "flee":
        flee_chance = 0.4 + (player["dexterity"] * 0.02)
        if random.random() < flee_chance:
            battle["active"] = False
            log_entries.append("Flucht erfolgreich!")
            return {"success": True, "fled": True, "log": log_entries}
        else:
            log_entries.append("Flucht fehlgeschlagen!")

    elif action.action_type == "item" and action.item_id:
        battle["player_hp"] = min(battle["player_max_hp"], battle["player_hp"] + 30)
        log_entries.append("Heiltrank benutzt! +30 HP")

    # -- GEGNER AKTION --
    for enemy in battle["enemies"]:
        if enemy["hp"] <= 0:
            continue
        defending = battle.pop("_defending", False)
        e_damage = max(1, enemy["attack"] + random.randint(0, 4) - player["dexterity"] // 3)
        if defending:
            e_damage = e_damage // 2
        battle["player_hp"] = max(0, battle["player_hp"] - e_damage)
        log_entries.append(f"{enemy['name']} trifft fuer {e_damage} Schaden!")

    # -- CHECK ENDE --
    all_dead = all(e["hp"] <= 0 for e in battle["enemies"])
    player_dead = battle["player_hp"] <= 0

    if all_dead:
        battle["active"] = False
        total_xp = sum(e["xp_reward"] for e in battle["enemies"])
        total_gold = sum(e["gold_reward"] for e in battle["enemies"])
        STATE["user"]["xp"] += total_xp
        STATE["user"]["points"] += total_gold
        STATE["najika"]["xp"] += total_xp
        log_entries.append(f"SIEG! +{total_xp} XP, +{total_gold} Gold!")
        result["victory"] = True
        result["rewards"] = {"xp": total_xp, "gold": total_gold}

    elif player_dead:
        battle["active"] = False
        log_entries.append("NIEDERLAGE!")
        result["defeat"] = True

    else:
        battle["turn"] += 1

    # Shared State sync
    STATE["battle"] = {
        "hp": battle["player_hp"],
        "wave": battle["wave"],
        "enemies": len([e for e in battle["enemies"] if e["hp"] > 0]),
    }

    battle["log"].extend(log_entries)
    result["log"] = log_entries
    result["battle"] = {k: v for k, v in battle.items() if k != "log" and k != "_defending"}

    return result


@router.get("/status")
@handle_errors()
async def battle_status():
    """Aktuellen Battle-Status"""
    battle = _get_battle()
    if not battle:
        return {"active": False, "message": "Kein aktiver Kampf"}
    return {k: v for k, v in battle.items() if k != "log"}


@router.get("/log")
@handle_errors()
async def battle_log():
    """Battle-Log (letzte Aktionen)"""
    battle = _get_battle()
    if not battle:
        return {"log": []}
    return {"log": battle.get("log", [])[-20:]}


@router.post("/end")
@handle_errors()
async def end_battle():
    """Battle manuell beenden"""
    if "default" in _active_battles:
        del _active_battles["default"]
    STATE["battle"] = {"hp": 100, "wave": 0, "enemies": 0}
    return {"success": True, "message": "Battle beendet"}


@router.get("/enemies")
@handle_errors()
async def get_enemy_db():
    """Gegner-Datenbank abrufen"""
    if not ENEMY_DB:
        return {"enemies": [], "count": 0}
    return {
        "enemies": [{"id": k, **v} for k, v in list(ENEMY_DB.items())[:50]],
        "count": len(ENEMY_DB),
    }


@router.get("/skills")
@handle_errors()
async def get_skill_db():
    """Skill-Datenbank abrufen"""
    if not SKILL_DB:
        return {"skills": [], "count": 0}
    return {
        "skills": [{"id": k, **v} for k, v in list(SKILL_DB.items())[:50]],
        "count": len(SKILL_DB),
    }
