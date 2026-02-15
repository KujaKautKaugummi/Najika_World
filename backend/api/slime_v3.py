"""
Slime System Router V3 - Formwandler + Aura
Direkt V3 implementiert (NICHT V2 migriert!).

Basierend auf SLIME_SYSTEM_V3_DOKUMENTATION.md:
- Formwandler (keine Evolution!)
- 8 Regional Start-Formen
- Form-Lernen (0.5-2% Chance)
- Aura-System (13 Elemente, 6 Stufen)
- Zwei Modi: Koerperlich / Aura
- Vertrauen (6 Level)
- Erinnerungs-System
- Skill-Copy (getrennt von Form-Lernen)
"""

from fastapi import APIRouter, HTTPException
from backend.utils import handle_errors
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum
import random
import time
import json
import sys
import os
import logging

logger = logging.getLogger("najika.api.slime_v3")

_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE

router = APIRouter(prefix="/api/slime-v3", tags=["Slime V3"])


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class RegionalForm(str, Enum):
    """8 Start-Formen (eine pro Region)"""
    WUESTEN_ECHSE = "wuesten_echse"              # Heisse Duenen
    WALD_WOLF = "wald_wolf"                       # Samtmoos-Tiefwald
    SUMPF_MOLCH = "sumpf_molch"                   # Gruenschlamm-Sumpf
    VULKAN_SALAMANDER = "vulkan_salamander"        # Magmastroeme
    EIS_HASE = "eis_hase"                         # Reich der Drei
    BLITZ_VOGEL = "blitz_vogel"                   # Blitzebene
    WELLEN_QUALLE = "wellen_qualle"               # Salzwind-Kueste
    KRISTALL_SPINNE = "kristall_spinne"            # Tiefenhoehlen


class SpecialForm(str, Enum):
    """Spezial-Formen (Freischaltung)"""
    REGENBOGEN_BLOB = "regenbogen_blob"    # Alle 8 Regional-Formen
    KOENIG_SCHLEIM = "koenig_schleim"      # 1000 Kaempfe gewonnen
    SKELETT_FORM = "skelett_form"          # Halloween Event
    MINI_DRACHE = "mini_drache"            # Drachen-Boss besiegt
    MENSCH_FORM = "mensch_form"            # Trust Level 5 (Seelenbund)


class AuraElement(str, Enum):
    """13 Aura-Elemente"""
    FEUER = "feuer"
    FROST = "frost"
    SCHATTEN = "schatten"
    HEILIG = "heilig"
    EXPLOSION = "explosion"
    METALL = "metall"
    NATUR = "natur"
    BLITZ = "blitz"
    WASSER = "wasser"
    GIFT = "gift"
    KRISTALL = "kristall"
    SAND = "sand"
    GOETTLICH = "goettlich"


class CompanionMode(str, Enum):
    KOERPERLICH = "koerperlich"  # Slime kaempft physisch mit
    AURA = "aura"                # Slime wird zur Aura (Buffs)


# Trust Levels
TRUST_LEVELS = {
    0: {"name": "Fremd",     "min_points": 0,   "max_points": 49},
    1: {"name": "Bekannt",   "min_points": 50,  "max_points": 149},
    2: {"name": "Freund",    "min_points": 150, "max_points": 299},
    3: {"name": "Vertraut",  "min_points": 300, "max_points": 499},
    4: {"name": "Familie",   "min_points": 500, "max_points": 800},
    5: {"name": "Seelenbund","min_points": 801, "max_points": 99999},
}

# Aura-Level Boni
AURA_LEVEL_BONUS = {
    0: 0.0,    # Keine Aura
    1: 0.05,   # +5%
    2: 0.15,   # +15%
    3: 0.25,   # +25%
    4: 0.35,   # +35%
    5: 0.50,   # +50%
}

# Form-Lern-Chancen (nach Gegner-Typ)
FORM_LEARN_CHANCES = {
    "voelker": 0.02,     # 2% - Voelker-Monster
    "wild": 0.008,       # 0.8% - Wilde Monster
    "nutztiere": 0.001,  # 0.1% - Nutztiere / Farm
}

# Erinnerungs-Meilensteine
MEMORY_MILESTONES = {
    1: "Ich bin... anders als die anderen?",
    2: "Warum kann ich Formen annehmen? Normale Monster koennen das nicht...",
    3: "Es gibt Erinnerungen... verschwommen... jemand hat mich erschaffen?",
    4: "Ich sehe ein Gesicht... freundlich... wer war das?",
    5: "Ich erinnere mich an eine Stimme: 'Du bist etwas Besonderes.'",
    6: "Die Welt... ich war schon einmal hier. Vor langer, langer Zeit.",
    7: "Mein Name... ich hatte einen Namen. Aber ich habe ihn vergessen.",
    8: "ICH ERINNERE MICH! Ich bin kein Monster. Ich bin... ICH!",
}

REGION_FORMS = {
    "heisse_duenen": RegionalForm.WUESTEN_ECHSE,
    "samtmoos_tiefwald": RegionalForm.WALD_WOLF,
    "gruenschlamm_sumpf": RegionalForm.SUMPF_MOLCH,
    "magmastroeme": RegionalForm.VULKAN_SALAMANDER,
    "reich_der_drei": RegionalForm.EIS_HASE,
    "blitzebene": RegionalForm.BLITZ_VOGEL,
    "salzwind_kueste": RegionalForm.WELLEN_QUALLE,
    "tiefenhoehlen": RegionalForm.KRISTALL_SPINNE,
}


# ============================================================================
# SLIME STATE (in-memory, mit Save/Load)
# ============================================================================

def _default_slime_state():
    return {
        "name": "Slime",
        "current_form": RegionalForm.WALD_WOLF.value,
        "learned_forms": [RegionalForm.WALD_WOLF.value],
        "aura_element": None,
        "aura_stufe": 0,
        "mode": CompanionMode.KOERPERLICH.value,
        "trust_points": 0,
        "trust_level": 0,
        "memory_fragments": 1,
        "memories_unlocked": [],
        "skills": [],
        "max_skills": 20,
        "battles_won": 0,
        "battles_total": 0,
        "hunger_hearts": 4,
        "max_hunger_hearts": 4,
        "last_fed": time.time(),
        "last_rescue": 0,
        "human_form_unlocked": False,
        "is_human_form": False,
        "created_at": time.time(),
    }


# Load from localStorage-equivalent (file-based)
_SAVE_PATH = os.path.join(_backend_dir, "saves", "slime_v3_state.json")

def _load_slime_state():
    try:
        if os.path.exists(_SAVE_PATH):
            with open(_SAVE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Slime State laden fehlgeschlagen: {e}")
    return _default_slime_state()


def _save_slime_state():
    try:
        os.makedirs(os.path.dirname(_SAVE_PATH), exist_ok=True)
        with open(_SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(_slime, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Slime State speichern fehlgeschlagen: {e}")


_slime = _load_slime_state()


def _get_trust_level(points):
    for lvl in sorted(TRUST_LEVELS.keys(), reverse=True):
        if points >= TRUST_LEVELS[lvl]["min_points"]:
            return lvl
    return 0


# ============================================================================
# ENDPOINTS - STATUS
# ============================================================================

@router.get("/status")
@handle_errors()
async def get_slime_status():
    """Kompletter Slime V3 Status"""
    _update_hunger()
    trust_lvl = _get_trust_level(_slime["trust_points"])
    trust_info = TRUST_LEVELS.get(trust_lvl, TRUST_LEVELS[0])

    return {
        "name": _slime["name"],
        "current_form": _slime["current_form"],
        "learned_forms": _slime["learned_forms"],
        "total_forms": len(_slime["learned_forms"]),
        "aura_element": _slime["aura_element"],
        "aura_stufe": _slime["aura_stufe"],
        "aura_bonus": AURA_LEVEL_BONUS.get(_slime["aura_stufe"], 0),
        "mode": _slime["mode"],
        "trust_points": _slime["trust_points"],
        "trust_level": trust_lvl,
        "trust_name": trust_info["name"],
        "memory_fragments": _slime["memory_fragments"],
        "memories_unlocked": _slime["memories_unlocked"],
        "skills": _slime["skills"],
        "skill_count": len(_slime["skills"]),
        "max_skills": _slime["max_skills"],
        "battles_won": _slime["battles_won"],
        "battles_total": _slime["battles_total"],
        "hunger_hearts": _slime["hunger_hearts"],
        "max_hunger_hearts": _slime["max_hunger_hearts"],
        "human_form_unlocked": _slime["human_form_unlocked"],
        "is_human_form": _slime["is_human_form"],
    }


# ============================================================================
# ENDPOINTS - FORMS
# ============================================================================

@router.post("/form/learn")
@handle_errors()
async def try_learn_form(enemy_type: str = "wild", enemy_form: Optional[str] = None, slime_had_kill: bool = False):
    """
    Versuche eine Form zu lernen (nach besiegtem Gegner).

    - enemy_type: voelker / wild / nutztiere
    - enemy_form: Die Form des besiegten Gegners (z.B. "wald_wolf")
    - slime_had_kill: Ob der Slime den Kill hatte (+0.5%)
    """
    if not enemy_form:
        raise HTTPException(400, "enemy_form ist erforderlich")

    if enemy_form in _slime["learned_forms"]:
        return {"success": False, "message": "Form bereits gelernt", "already_known": True}

    # Chance berechnen
    base_chance = FORM_LEARN_CHANCES.get(enemy_type, 0.008)
    trust_bonus = _get_trust_level(_slime["trust_points"]) * 0.001
    kill_bonus = 0.005 if slime_had_kill else 0

    total_chance = base_chance + trust_bonus + kill_bonus

    if random.random() < total_chance:
        _slime["learned_forms"].append(enemy_form)
        _slime["memory_fragments"] = len(_slime["learned_forms"])

        # Memory-Meilenstein pruefen
        memory_msg = None
        frag_count = _slime["memory_fragments"]
        if frag_count in MEMORY_MILESTONES and frag_count not in _slime["memories_unlocked"]:
            _slime["memories_unlocked"].append(frag_count)
            memory_msg = MEMORY_MILESTONES[frag_count]

        # Alle 8 Regional-Formen? → Regenbogen-Blob!
        regional_values = [f.value for f in RegionalForm]
        has_all_regional = all(f in _slime["learned_forms"] for f in regional_values)
        rainbow_unlocked = False
        if has_all_regional and SpecialForm.REGENBOGEN_BLOB.value not in _slime["learned_forms"]:
            _slime["learned_forms"].append(SpecialForm.REGENBOGEN_BLOB.value)
            rainbow_unlocked = True

        _save_slime_state()

        return {
            "success": True,
            "form_learned": enemy_form,
            "chance_was": round(total_chance * 100, 2),
            "memory_milestone": memory_msg,
            "rainbow_unlocked": rainbow_unlocked,
            "total_forms": len(_slime["learned_forms"]),
        }

    return {
        "success": False,
        "message": "Form nicht gelernt (Chance nicht getroffen)",
        "chance_was": round(total_chance * 100, 2),
    }


@router.post("/form/change")
@handle_errors()
async def change_form(form: str):
    """Form wechseln (nur gelernte Formen)"""
    if form not in _slime["learned_forms"]:
        raise HTTPException(400, f"Form '{form}' nicht gelernt!")

    _slime["current_form"] = form
    _slime["is_human_form"] = False
    _save_slime_state()

    return {"success": True, "current_form": form}


@router.get("/forms")
@handle_errors()
async def get_all_forms():
    """Alle gelernten Formen + verfuegbare"""
    regional = [{"id": f.value, "name": f.value.replace("_", " ").title(), "learned": f.value in _slime["learned_forms"]}
                for f in RegionalForm]
    special = [{"id": f.value, "name": f.value.replace("_", " ").title(), "learned": f.value in _slime["learned_forms"]}
               for f in SpecialForm]

    return {
        "current": _slime["current_form"],
        "learned": _slime["learned_forms"],
        "regional": regional,
        "special": special,
        "total_learned": len(_slime["learned_forms"]),
    }


# ============================================================================
# ENDPOINTS - AURA
# ============================================================================

@router.post("/aura/set")
@handle_errors()
async def set_aura_element(element: str):
    """Aura-Element setzen (kann gewechselt werden durch Training)"""
    try:
        aura = AuraElement(element)
    except ValueError:
        valid = [e.value for e in AuraElement]
        raise HTTPException(400, f"Ungueltiges Element. Erlaubt: {valid}")

    _slime["aura_element"] = aura.value
    if _slime["aura_stufe"] == 0:
        _slime["aura_stufe"] = 1
    _save_slime_state()

    return {
        "success": True,
        "aura_element": aura.value,
        "aura_stufe": _slime["aura_stufe"],
        "bonus": AURA_LEVEL_BONUS.get(_slime["aura_stufe"], 0),
    }


@router.post("/aura/upgrade")
@handle_errors()
async def upgrade_aura():
    """Aura-Stufe erhoehen (0 bis 5)"""
    if not _slime["aura_element"]:
        raise HTTPException(400, "Keine Aura gewaehlt!")
    if _slime["aura_stufe"] >= 5:
        raise HTTPException(400, "Aura bereits maximal (Stufe 5)!")

    _slime["aura_stufe"] += 1
    _save_slime_state()

    return {
        "success": True,
        "aura_stufe": _slime["aura_stufe"],
        "bonus": AURA_LEVEL_BONUS[_slime["aura_stufe"]],
        "element": _slime["aura_element"],
    }


@router.get("/aura")
@handle_errors()
async def get_aura_status():
    """Aura-Status"""
    return {
        "element": _slime["aura_element"],
        "stufe": _slime["aura_stufe"],
        "bonus": AURA_LEVEL_BONUS.get(_slime["aura_stufe"], 0),
        "available_elements": [e.value for e in AuraElement],
    }


# ============================================================================
# ENDPOINTS - MODE
# ============================================================================

@router.post("/mode/switch")
@handle_errors()
async def switch_mode():
    """Zwischen Koerperlich und Aura wechseln"""
    if _slime["mode"] == CompanionMode.KOERPERLICH.value:
        if not _slime["aura_element"]:
            raise HTTPException(400, "Keine Aura verfuegbar! Erst ein Element waehlen.")
        _slime["mode"] = CompanionMode.AURA.value
    else:
        _slime["mode"] = CompanionMode.KOERPERLICH.value

    _save_slime_state()
    return {"success": True, "mode": _slime["mode"]}


@router.post("/mode/set")
@handle_errors()
async def set_mode(mode: str):
    """Modus direkt setzen"""
    if mode not in [m.value for m in CompanionMode]:
        raise HTTPException(400, f"Ungueltig. Erlaubt: koerperlich, aura")
    if mode == CompanionMode.AURA.value and not _slime["aura_element"]:
        raise HTTPException(400, "Keine Aura verfuegbar!")

    _slime["mode"] = mode
    _save_slime_state()
    return {"success": True, "mode": mode}


# ============================================================================
# ENDPOINTS - TRUST
# ============================================================================

@router.get("/trust")
@handle_errors()
async def get_trust():
    """Vertrauens-Status"""
    lvl = _get_trust_level(_slime["trust_points"])
    info = TRUST_LEVELS.get(lvl, TRUST_LEVELS[0])
    next_lvl = TRUST_LEVELS.get(lvl + 1)

    return {
        "points": _slime["trust_points"],
        "level": lvl,
        "name": info["name"],
        "next_level": {
            "name": next_lvl["name"],
            "points_needed": next_lvl["min_points"] - _slime["trust_points"],
        } if next_lvl else None,
    }


@router.post("/trust/add")
@handle_errors()
async def add_trust(amount: int = 1):
    """Trust-Punkte hinzufuegen (DARF NIEMALS sinken!)"""
    if amount < 0:
        raise HTTPException(400, "Trust darf NIEMALS sinken! (Regel aus V3-Doku)")

    old_level = _get_trust_level(_slime["trust_points"])
    _slime["trust_points"] += amount
    new_level = _get_trust_level(_slime["trust_points"])

    # Human Form bei Level 5
    if new_level >= 5 and not _slime["human_form_unlocked"]:
        _slime["human_form_unlocked"] = True

    _save_slime_state()

    level_up = new_level > old_level
    return {
        "success": True,
        "trust_points": _slime["trust_points"],
        "trust_level": new_level,
        "trust_name": TRUST_LEVELS[new_level]["name"],
        "level_up": level_up,
        "human_form_unlocked": _slime["human_form_unlocked"],
    }


# ============================================================================
# ENDPOINTS - SKILLS
# ============================================================================

@router.post("/skill/learn")
@handle_errors()
async def try_learn_skill(skill_name: str, enemy_type: str = "wild"):
    """Skill-Copy nach besiegtem Gegner (1-5% Chance, GETRENNT von Form-Lernen)"""
    if len(_slime["skills"]) >= _slime["max_skills"]:
        return {"success": False, "message": f"Max Skills ({_slime['max_skills']}) erreicht! Erst einen vergessen."}

    if skill_name in _slime["skills"]:
        return {"success": False, "message": "Skill bereits gelernt", "already_known": True}

    chance = random.uniform(0.01, 0.05)  # 1-5%
    if random.random() < chance:
        _slime["skills"].append(skill_name)
        _save_slime_state()
        return {"success": True, "skill_learned": skill_name, "total_skills": len(_slime["skills"])}

    return {"success": False, "message": "Skill nicht gelernt"}


@router.post("/skill/forget")
@handle_errors()
async def forget_skill(skill_name: str):
    """Skill vergessen (Spieler-Wahl)"""
    if skill_name not in _slime["skills"]:
        raise HTTPException(404, f"Skill '{skill_name}' nicht gelernt")

    _slime["skills"].remove(skill_name)
    _save_slime_state()
    return {"success": True, "forgotten": skill_name, "remaining_skills": len(_slime["skills"])}


# ============================================================================
# ENDPOINTS - CARE (V-Pet)
# ============================================================================

def _update_hunger():
    """Hunger Hearts Decay (1 pro 60 Min)"""
    now = time.time()
    elapsed = now - _slime.get("last_fed", now)
    hearts_lost = int(elapsed / 3600)
    if hearts_lost > 0:
        _slime["hunger_hearts"] = max(0, _slime["hunger_hearts"] - hearts_lost)
        _slime["last_fed"] = now


@router.post("/care/feed")
@handle_errors()
async def feed_slime():
    """Slime fuettern (Hunger Hearts auffuellen)"""
    _slime["hunger_hearts"] = min(_slime["max_hunger_hearts"], _slime["hunger_hearts"] + 1)
    _slime["last_fed"] = time.time()
    _slime["trust_points"] += 1
    _save_slime_state()
    return {"success": True, "hunger_hearts": _slime["hunger_hearts"], "trust_points": _slime["trust_points"]}


@router.post("/care/play")
@handle_errors()
async def play_with_slime():
    """Mit Slime spielen"""
    _slime["trust_points"] += 2
    _save_slime_state()
    return {"success": True, "trust_points": _slime["trust_points"]}


@router.post("/care/heal")
@handle_errors()
async def heal_slime():
    """Slime heilen"""
    _slime["hunger_hearts"] = _slime["max_hunger_hearts"]
    _slime["trust_points"] += 1
    _save_slime_state()
    return {"success": True, "hunger_hearts": _slime["hunger_hearts"]}


# ============================================================================
# ENDPOINTS - BATTLE TRACKING
# ============================================================================

@router.post("/battle/won")
@handle_errors()
async def record_battle_won():
    """Battle gewonnen tracken"""
    _slime["battles_won"] += 1
    _slime["battles_total"] += 1
    _slime["trust_points"] += 3

    # Koenig-Schleim bei 1000 Siegen
    if _slime["battles_won"] >= 1000 and SpecialForm.KOENIG_SCHLEIM.value not in _slime["learned_forms"]:
        _slime["learned_forms"].append(SpecialForm.KOENIG_SCHLEIM.value)
        _save_slime_state()
        return {"success": True, "special_unlock": "koenig_schleim", "battles_won": _slime["battles_won"]}

    _save_slime_state()
    return {"success": True, "battles_won": _slime["battles_won"]}


@router.post("/battle/lost")
@handle_errors()
async def record_battle_lost():
    """Battle verloren tracken"""
    _slime["battles_total"] += 1
    _save_slime_state()
    return {"success": True, "battles_total": _slime["battles_total"]}


# ============================================================================
# ENDPOINTS - RESCUE
# ============================================================================

@router.post("/rescue")
@handle_errors()
async def rescue_check():
    """Rescue System: 1x pro 24h (oder kein Cooldown bei Trust 4+)"""
    now = time.time()
    cooldown = 86400  # 24h

    trust_lvl = _get_trust_level(_slime["trust_points"])
    if trust_lvl >= 4:
        cooldown = 0  # Kein Cooldown bei Familie/Seelenbund

    elapsed = now - _slime.get("last_rescue", 0)
    if elapsed < cooldown:
        remaining = cooldown - elapsed
        return {"available": False, "cooldown_remaining": int(remaining), "trust_bypass": False}

    _slime["last_rescue"] = now
    _save_slime_state()
    return {"available": True, "rescued": True, "trust_level": trust_lvl}


# ============================================================================
# ENDPOINTS - MEMORY / ERINNERUNGEN
# ============================================================================

@router.get("/memories")
@handle_errors()
async def get_memories():
    """Alle freigeschalteten Erinnerungen"""
    memories = []
    for frag_num in sorted(_slime["memories_unlocked"]):
        if frag_num in MEMORY_MILESTONES:
            memories.append({
                "fragment": frag_num,
                "text": MEMORY_MILESTONES[frag_num],
            })

    all_unlocked = len(_slime["memories_unlocked"]) >= 8
    return {
        "memories": memories,
        "fragments_total": _slime["memory_fragments"],
        "all_unlocked": all_unlocked,
    }


# ============================================================================
# ENDPOINTS - HUMAN FORM
# ============================================================================

@router.post("/human-form/toggle")
@handle_errors()
async def toggle_human_form():
    """Menschen-Form an/aus (nur bei Trust Level 5)"""
    if not _slime["human_form_unlocked"]:
        raise HTTPException(400, "Menschen-Form nicht freigeschaltet! Braucht Trust Level 5 (Seelenbund)")

    _slime["is_human_form"] = not _slime["is_human_form"]
    _save_slime_state()
    return {"success": True, "is_human_form": _slime["is_human_form"]}


# ============================================================================
# ENDPOINTS - SAVE/LOAD/RESET
# ============================================================================

@router.post("/save")
@handle_errors()
async def save_state():
    """State manuell speichern"""
    _save_slime_state()
    return {"success": True}


@router.post("/reset")
@handle_errors()
async def reset_state():
    """State zuruecksetzen (Vorsicht!)"""
    global _slime
    _slime = _default_slime_state()
    _save_slime_state()
    return {"success": True, "message": "Slime State zurueckgesetzt"}


@router.post("/name")
@handle_errors()
async def set_slime_name(name: str):
    """Slime umbenennen"""
    if not name or len(name) > 30:
        raise HTTPException(400, "Name muss 1-30 Zeichen lang sein")
    _slime["name"] = name
    _save_slime_state()
    return {"success": True, "name": name}
