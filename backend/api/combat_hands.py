"""
Najika Combat Hands API Router
Zwei-Hand-Kampfsystem mit Waffen-Anforderungen
Für UE5 Integration
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Combat Hands System
try:
    from najika_combat_hands_system import (
        get_combat_hands_system,
        Hand,
        WeaponType,
        AttackType
    )
    COMBAT_HANDS_AVAILABLE = True
except ImportError as e:
    COMBAT_HANDS_AVAILABLE = False
    print(f"⚠️ Combat Hands System nicht verfügbar: {e}")

router = APIRouter(prefix="/api/combat-hands", tags=["Combat Hands"])


# ============================================================================
# MODELS
# ============================================================================

class EquipRequest(BaseModel):
    weapon_id: str
    hand: str  # "left", "right", "both"


class AttackRequest(BaseModel):
    hand: str  # "left", "right", "both"
    attack_type: str = "light"  # "light", "heavy"
    target_id: Optional[str] = None


class DualCastRequest(BaseModel):
    spell_id: str
    target_id: Optional[str] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/status")
async def get_combat_status():
    """
    Get current combat hands status

    Returns what's equipped in each hand and combat state
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    state = combat.get_state()

    return {
        "left_hand": state["left_hand"],
        "right_hand": state["right_hand"],
        "can_dual_cast": state["can_dual_cast"],
        "combo_counter": state["combo_counter"],
        "exhaustion": state["exhaustion"],
        "stance": state["stance"],
        "available_attacks": {
            "left": state["left_attacks"],
            "right": state["right_attacks"],
            "combined": state["combined_attacks"]
        }
    }


@router.get("/weapons")
async def get_all_weapons():
    """
    Get all available weapons with stats and requirements

    For UE5 inventory/equipment UI
    """
    if not COMBAT_HANDS_AVAILABLE:
        # Return sample weapons
        return {
            "weapons": [
                {
                    "id": "iron_sword",
                    "name": "Eisenschwert",
                    "type": "sword",
                    "damage": 25,
                    "requirements": {"str": 10, "skill_sword": 5},
                    "scaling": {"str": "C", "dex": "C"},
                    "hands": "one"
                },
                {
                    "id": "staff_fire",
                    "name": "Feuerstab",
                    "type": "staff",
                    "damage": 30,
                    "requirements": {"int": 15, "skill_magic": 10},
                    "scaling": {"int": "B"},
                    "hands": "two",
                    "spell_boost": "fire"
                },
                {
                    "id": "explosion_catalyst",
                    "name": "Explosions-Katalysator",
                    "type": "catalyst",
                    "damage": 100,
                    "requirements": {"int": 30, "skill_explosion": 50},
                    "scaling": {"int": "S"},
                    "hands": "two",
                    "spell_boost": "explosion",
                    "note": "Najika's Signatur-Waffe"
                }
            ]
        }

    combat = get_combat_hands_system()
    return {"weapons": combat.get_all_weapons()}


@router.get("/perks")
async def get_combat_perks():
    """
    Get all combat perks (Quick Cast etc.)

    Perks are unlocked through skill milestones
    """
    return {
        "perks": {
            "quick_cast_1": {
                "name": "Quick Cast I",
                "effect": "-10% Cast Time",
                "requirement": "Magic Skill 25"
            },
            "quick_cast_2": {
                "name": "Quick Cast II",
                "effect": "-20% Cast Time",
                "requirement": "Magic Skill 50"
            },
            "quick_cast_3": {
                "name": "Quick Cast III",
                "effect": "-30% Cast Time",
                "requirement": "Magic Skill 75"
            },
            "master_caster": {
                "name": "Master Caster",
                "effect": "-40% Cast Time",
                "requirement": "Magic Skill 100"
            },
            "dual_wield_master": {
                "name": "Dual Wield Master",
                "effect": "+25% Dual Wield Damage",
                "requirement": "Dual Wield Skill 50"
            },
            "combo_expert": {
                "name": "Combo Expert",
                "effect": "+50% Combo Damage",
                "requirement": "Combat Skill 75"
            }
        }
    }


@router.get("/player/{player_id}")
async def get_player_combat_status(player_id: str):
    """
    Get a specific player's combat status

    For multiplayer synchronization
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    state = combat.get_player_state(player_id)

    if not state:
        raise HTTPException(status_code=404, detail=f"Spieler {player_id} nicht gefunden")

    return state


@router.get("/weapon-preview/{player_id}/{weapon_id}")
async def preview_weapon(player_id: str, weapon_id: str):
    """
    Preview how a weapon would perform for a player

    Shows if requirements are met and expected damage
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    preview = combat.preview_weapon(player_id, weapon_id)

    return {
        "weapon_id": weapon_id,
        "player_id": player_id,
        "requirements_met": preview["requirements_met"],
        "requirement_percentage": preview["requirement_percentage"],
        "expected_damage": preview["expected_damage"],
        "warnings": preview.get("warnings", []),
        "effects": preview.get("effects", {})
    }


@router.post("/register")
async def register_player(player_id: str, stats: Dict[str, int]):
    """
    Register a player with the combat system

    Required before combat actions
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    result = combat.register_player(player_id, stats)

    return {
        "success": True,
        "player_id": player_id,
        "registered": True,
        "initial_state": result
    }


@router.post("/equip")
async def equip_weapon(request: EquipRequest):
    """
    Equip a weapon in a hand

    Checks requirements - may fail or reduce effectiveness
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    if request.hand not in ["left", "right", "both"]:
        raise HTTPException(status_code=400, detail="Hand muss 'left', 'right' oder 'both' sein")

    combat = get_combat_hands_system()
    result = combat.equip_weapon(request.weapon_id, request.hand)

    return {
        "success": result.get("success", False),
        "weapon": request.weapon_id,
        "hand": request.hand,
        "requirements_met": result.get("requirements_met", False),
        "effectiveness": result.get("effectiveness", 100),
        "warnings": result.get("warnings", []),
        "message": result.get("message", "Waffe ausgerüstet!")
    }


@router.post("/attack")
async def attack(request: AttackRequest):
    """
    Perform an attack

    Q = Left Light, Shift+Q = Left Heavy
    E = Right Light, Shift+E = Right Heavy
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    result = combat.attack(request.hand, request.attack_type, request.target_id)

    return {
        "success": result.get("success", False),
        "hand": request.hand,
        "attack_type": request.attack_type,
        "damage": result.get("damage", 0),
        "damage_type": result.get("damage_type", "physical"),
        "critical": result.get("critical", False),
        "combo_count": result.get("combo_count", 0),
        "stamina_cost": result.get("stamina_cost", 0),
        "animation": result.get("animation", f"attack_{request.hand}_{request.attack_type}"),
        "hit": result.get("hit", True),
        "self_damage": result.get("self_damage", 0),  # Bei unerfüllten Requirements!
        "message": result.get("message", "")
    }


@router.post("/dual-cast")
async def dual_cast(request: DualCastRequest):
    """
    Dual-cast a spell (both hands)

    Stronger but slower, requires appropriate items in both hands
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    result = combat.dual_cast(request.spell_id, request.target_id)

    return {
        "success": result.get("success", False),
        "spell": request.spell_id,
        "damage": result.get("damage", 0),
        "damage_multiplier": result.get("multiplier", 2.0),
        "mana_cost": result.get("mana_cost", 0),
        "cast_time": result.get("cast_time", 0),
        "animation": result.get("animation", "dual_cast"),
        "message": result.get("message", "Dual Cast!")
    }


@router.post("/perk/unlock")
async def unlock_perk(perk_id: str, player_id: str):
    """
    Unlock a combat perk

    Perks are earned through skill milestones
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    result = combat.unlock_perk(player_id, perk_id)

    return {
        "success": result.get("success", False),
        "perk": perk_id,
        "message": result.get("message", "Perk freigeschaltet!"),
        "effect": result.get("effect")
    }


@router.post("/train")
async def train_skill(skill_id: str, player_id: str, xp: int):
    """
    Train a combat skill

    Learning by Doing - skills improve through use
    """
    if not COMBAT_HANDS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Hands System nicht verfügbar")

    combat = get_combat_hands_system()
    result = combat.train_skill(player_id, skill_id, xp)

    return {
        "success": True,
        "skill": skill_id,
        "xp_gained": xp,
        "new_level": result.get("new_level"),
        "level_up": result.get("level_up", False),
        "perk_unlocked": result.get("perk_unlocked"),
        "message": result.get("message", f"+{xp} XP für {skill_id}")
    }


# ============================================================================
# KEYBIND INFO (für UE5 Input Mapping)
# ============================================================================

@router.get("/keybinds")
async def get_keybinds():
    """
    Get recommended keybinds for combat

    For UE5 Enhanced Input setup
    """
    return {
        "keybinds": {
            "Q": "Left Hand Light Attack",
            "Shift+Q": "Left Hand Heavy Attack",
            "E": "Right Hand Light Attack",
            "Shift+E": "Right Hand Heavy Attack",
            "Q+E": "Dual Attack / Dual Cast",
            "F": "Interact / Grab",
            "R": "Reload / Sheathe",
            "Space": "Dodge / Jump",
            "Ctrl": "Block (if shield equipped)",
            "Tab": "Switch Weapon Set"
        },
        "combos": {
            "Q-Q-E": "Basic Combo",
            "Q-E-Q-E": "Alternating Combo",
            "Shift+Q-Shift+E": "Power Combo",
            "Hold Q+E": "Charged Dual Attack"
        }
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def combat_hands_health():
    """Check if Combat Hands System is available"""
    return {
        "available": COMBAT_HANDS_AVAILABLE,
        "system": "najika_combat_hands_system",
        "features": ["two_hand_combat", "weapon_requirements", "dual_cast", "perks", "combos"]
    }
