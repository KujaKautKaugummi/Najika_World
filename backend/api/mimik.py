"""
Najika Mimik-Truhe API Router
Endpoints für Kuja's exklusiven Mimik-Truhe Charakter
Für UE5 Integration
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Mimik System
try:
    from najika_mimik_system import (
        get_mimik_system,
        MimikForm,
        MimikAbility
    )
    MIMIK_AVAILABLE = True
except ImportError as e:
    MIMIK_AVAILABLE = False
    print(f"⚠️ Mimik System nicht verfügbar: {e}")

router = APIRouter(prefix="/api/mimik", tags=["Mimik"])


# ============================================================================
# MODELS
# ============================================================================

class TransformRequest(BaseModel):
    target_form: str  # "chest" oder "human"


class AbilityRequest(BaseModel):
    ability_id: str
    target_id: Optional[str] = None


class EatRequest(BaseModel):
    target_id: str
    target_type: str = "enemy"  # "enemy", "item", "npc"


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/status")
async def get_mimik_status():
    """
    Get Kuja's Mimik-Truhe status

    Returns current form, abilities, stomach contents, Najika bond
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()
    state = mimik.get_state()

    return {
        "player_id": "kuja",
        "current_form": state["current_form"],
        "is_hidden": state["is_hidden"],
        "stomach_contents": state["stomach_contents"],
        "stomach_capacity": state["stomach_capacity"],
        "abilities": {
            "unlocked": state["unlocked_abilities"],
            "locked": state["locked_abilities"],
            "cooldowns": state["ability_cooldowns"]
        },
        "najika_bond": state["najika_bond"],
        "stats": state["stats"]
    }


@router.get("/abilities")
async def get_available_abilities():
    """
    Get all available abilities for current form

    Different abilities available in chest vs human form
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()
    abilities = mimik.get_available_abilities()

    return {
        "current_form": mimik.current_form,
        "abilities": abilities,
        "form_specific": {
            "chest": ["snap_bite", "mimic_hide", "treasure_lure", "stomach_prison", "digest"],
            "human": ["human_transformation", "weapon_use", "magic", "najika_sync", "protect_najika"]
        }
    }


@router.get("/all-abilities")
async def get_all_abilities():
    """
    Get all Mimik abilities with descriptions

    For UE5 skill tree / ability menu
    """
    return {
        "abilities": {
            "snap_bite": {
                "name": "Schnappbiss",
                "description": "Blitzschneller Biss aus der Truhe",
                "damage": 45,
                "form": "chest",
                "cooldown": 3
            },
            "mimic_hide": {
                "name": "Mimik-Tarnung",
                "description": "Verstecke dich als harmlose Truhe",
                "form": "chest",
                "cooldown": 10
            },
            "treasure_lure": {
                "name": "Schatzköder",
                "description": "Locke Feinde mit glitzerndem Inhalt",
                "form": "chest",
                "cooldown": 15
            },
            "stomach_prison": {
                "name": "Magengefängnis",
                "description": "Verschlinge einen Feind",
                "damage": 30,
                "effect": "imprison",
                "form": "chest",
                "cooldown": 20
            },
            "digest": {
                "name": "Verdauen",
                "description": "Verdaue verschlungene Feinde für HP",
                "heal": "20% max HP",
                "form": "chest",
                "cooldown": 30
            },
            "human_transformation": {
                "name": "Menschenform",
                "description": "Verwandle dich in menschliche Gestalt",
                "form": "any",
                "cooldown": 60
            },
            "najika_sync": {
                "name": "Najika-Synchron",
                "description": "Kombiniere Angriff mit Najika für Combo",
                "damage_multiplier": 2.5,
                "form": "human",
                "cooldown": 45,
                "requires": "najika_nearby"
            },
            "protect_najika": {
                "name": "Najika beschützen",
                "description": "Springe vor Najika um Schaden abzufangen",
                "form": "any",
                "cooldown": 5
            }
        }
    }


@router.post("/transform")
async def transform(request: TransformRequest):
    """
    Transform between chest and human form

    Chest: Überraschungsangriffe, Verstecken, Fressen
    Human: Soziale Interaktion, Waffen, normale Kämpfe
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    if request.target_form not in ["chest", "human"]:
        raise HTTPException(status_code=400, detail="Form muss 'chest' oder 'human' sein")

    mimik = get_mimik_system()
    result = mimik.transform(request.target_form)

    return {
        "success": result.get("success", False),
        "previous_form": result.get("previous_form"),
        "new_form": result.get("new_form"),
        "message": result.get("message", "Transformation!"),
        "animation": f"transform_to_{request.target_form}",
        "cooldown": result.get("cooldown", 0)
    }


@router.post("/hide")
async def hide():
    """
    Hide as a normal chest (only in chest form)

    Enemies won't notice you until you attack
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()

    if mimik.current_form != "chest":
        raise HTTPException(status_code=400, detail="Kann nur in Truhenform verstecken!")

    result = mimik.hide()

    return {
        "success": True,
        "is_hidden": True,
        "message": "Du siehst jetzt aus wie eine normale Schatztruhe... 🎁",
        "stealth_bonus": result.get("stealth_bonus", 100)
    }


@router.post("/reveal")
async def reveal():
    """
    Stop hiding and reveal yourself
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()
    result = mimik.reveal()

    return {
        "success": True,
        "is_hidden": False,
        "message": "ÜBERRASCHUNG! 👅",
        "surprise_damage_bonus": result.get("surprise_bonus", 1.5) if result.get("was_hidden") else 1.0
    }


@router.post("/ability")
async def use_ability(request: AbilityRequest):
    """
    Use a Mimik ability

    Some abilities require targets, some don't
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()
    result = mimik.use_ability(request.ability_id, request.target_id)

    return {
        "success": result.get("success", False),
        "ability": request.ability_id,
        "target": request.target_id,
        "damage": result.get("damage", 0),
        "effect": result.get("effect"),
        "message": result.get("message", ""),
        "animation": result.get("animation", request.ability_id),
        "cooldown": result.get("cooldown", 0),
        "error": result.get("error")
    }


@router.post("/eat")
async def eat_target(request: EatRequest):
    """
    Eat/swallow a target (only in chest form)

    Can eat enemies, items, even some NPCs
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()

    if mimik.current_form != "chest":
        raise HTTPException(status_code=400, detail="Kann nur in Truhenform fressen!")

    result = mimik.eat(request.target_id, request.target_type)

    return {
        "success": result.get("success", False),
        "target": request.target_id,
        "swallowed": result.get("swallowed", False),
        "stomach_contents": result.get("stomach_contents", []),
        "message": result.get("message", "*SCHNAPP* 👅"),
        "damage": result.get("damage", 0),
        "can_digest": result.get("can_digest", False)
    }


@router.post("/protect-najika")
async def protect_najika():
    """
    Jump in front of Najika to protect her from incoming damage

    Works in both forms, shows Kuja's devotion
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()
    result = mimik.protect_najika()

    return {
        "success": True,
        "damage_absorbed": result.get("damage_absorbed", 0),
        "najika_bond_increase": result.get("bond_increase", 5),
        "message": "Niemand verletzt MEINE Najika! 💜",
        "animation": "protect_jump",
        "najika_reaction": result.get("najika_reaction", "*Kuja!* Danke! 💕")
    }


@router.post("/sync-najika")
async def sync_attack_najika(target_id: str):
    """
    Synchronized combo attack with Najika

    Massive damage bonus, requires both to be nearby
    """
    if not MIMIK_AVAILABLE:
        raise HTTPException(status_code=503, detail="Mimik System nicht verfügbar")

    mimik = get_mimik_system()
    result = mimik.sync_attack(target_id)

    return {
        "success": result.get("success", False),
        "target": target_id,
        "total_damage": result.get("total_damage", 0),
        "kuja_damage": result.get("kuja_damage", 0),
        "najika_damage": result.get("najika_damage", 0),
        "combo_bonus": result.get("combo_bonus", 2.5),
        "animation": "sync_combo_attack",
        "najika_line": result.get("najika_line", "Zusammen, Mr. K! EXPLOSION!!! 💥"),
        "kuja_line": "Für Najika!",
        "cooldown": result.get("cooldown", 45)
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def mimik_health():
    """Check if Mimik System is available"""
    return {
        "available": MIMIK_AVAILABLE,
        "system": "najika_mimik_system",
        "forms": ["chest", "human"],
        "features": ["transform", "hide", "eat", "protect_najika", "sync_attack"],
        "exclusive_to": "kuja"
    }
