"""
S.P.E.C.I.A.L. Stats API - Magic/Skill System V3
================================================

Fallout-style stats with balanced bonuses (max +25%)

Stats:
- POW (Power): Melee damage
- INT (Intelligence): Spell power, Mana
- AGI (Agility): Dodge, Speed
- VIT (Vitality): HP
- WIL (Willpower): Mana regen
- LUK (Luck): Crit chance/damage
- PER (Perception): Hit chance

Max +25% bonus at 10 points (sanft, nicht dominant!)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from backend.utils import handle_errors

router = APIRouter(prefix="/api/special", tags=["special"])


class SpecialStats(BaseModel):
    POW: int = 5
    INT: int = 5
    AGI: int = 5
    VIT: int = 5
    WIL: int = 5
    LUK: int = 5
    PER: int = 5


class SetSpecialRequest(BaseModel):
    player_id: int
    stats: SpecialStats


def calculate_bonuses(stats: SpecialStats) -> Dict:
    """
    Calculate bonuses from SPECIAL stats

    Max bonus: +25% at 10 points (2.5% per point)
    """
    return {
        "melee_damage_bonus": (stats.POW - 5) * 0.025,  # ±25% at 10/0
        "spell_power_bonus": (stats.INT - 5) * 0.025,
        "max_mana_bonus": (stats.INT - 5) * 10,  # ±50 mana
        "dodge_chance_bonus": (stats.AGI - 5) * 0.01,  # ±5% at 10/0
        "speed_bonus": (stats.AGI - 5) * 0.01,
        "max_hp_bonus": (stats.VIT - 5) * 15,  # ±75 HP
        "mana_regen_bonus": (stats.WIL - 5) * 0.01,
        "crit_chance_bonus": (stats.LUK - 5) * 0.01,
        "crit_damage_bonus": (stats.LUK - 5) * 0.05,  # ±25% crit dmg
        "hit_chance_bonus": (stats.PER - 5) * 0.02  # ±10% hit
    }


@router.post("/set")
@handle_errors()
async def set_special(request: SetSpecialRequest):
    """
    Set S.P.E.C.I.A.L. stats for player

    Start pool: 40 points (5 in each stat + 5 to distribute)

    Body:
    {
        "player_id": 1,
        "stats": {
            "POW": 5,
            "INT": 8,
            "AGI": 6,
            "VIT": 5,
            "WIL": 5,
            "LUK": 5,
            "PER": 6
        }
    }
    """
    # Validate total points
    total = sum([
        request.stats.POW,
        request.stats.INT,
        request.stats.AGI,
        request.stats.VIT,
        request.stats.WIL,
        request.stats.LUK,
        request.stats.PER
    ])

    if total != 40:
        raise HTTPException(
            status_code=400,
            detail=f"Total must be 40 points! (got {total})"
        )

    # Validate individual stats (min 1, max 10)
    for stat_name in ["POW", "INT", "AGI", "VIT", "WIL", "LUK", "PER"]:
        value = getattr(request.stats, stat_name)
        if value < 1 or value > 10:
            raise HTTPException(
                status_code=400,
                detail=f"{stat_name} must be between 1 and 10! (got {value})"
            )

    # Calculate bonuses
    bonuses = calculate_bonuses(request.stats)

    # TODO: Save to database
    # For now, return calculated bonuses

    return {
        "success": True,
        "player_id": request.player_id,
        "stats": request.stats.dict(),
        "bonuses": bonuses,
        "message": "✅ S.P.E.C.I.A.L. Stats gesetzt!"
    }


@router.get("/bonuses")
@handle_errors()
async def get_bonuses(player_id: int):
    """
    Get calculated bonuses for player's S.P.E.C.I.A.L. stats
    """
    # TODO: Load from database
    # For now, return example
    default_stats = SpecialStats()
    bonuses = calculate_bonuses(default_stats)

    return {
        "player_id": player_id,
        "stats": default_stats.dict(),
        "bonuses": bonuses
    }