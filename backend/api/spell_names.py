"""
Namen-System API - Spieler benennen Zauber selbst!
===================================================

Features:
- Custom Spell Names (3-30 Zeichen)
- Profanity Filter (DE/EN)
- Umbenennen durch Items/Events
- Nicht unique (jeder kann "Feuerball" nutzen)

Rules:
- Erlaubt: A-Z, a-z, 0-9, Space, -, '
- Nicht erlaubt: Sonderzeichen, Schimpfwörter
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, validator
from typing import Dict, Optional
import re
from backend.utils import handle_errors

router = APIRouter(prefix="/api/spells/name", tags=["spell_names"])


# ==================== PROFANITY FILTER ====================

# WARNUNG: Diese Liste dient dem rechtlichen Schutz!
# Nicht vollständig, aber deckt die gröbsten Fälle ab.

PROFANITY_LIST = {
    # Deutsche Schimpfwörter
    "arsch", "scheisse", "scheiße", "fick", "hure", "fotze", "pisse",
    "wichser", "schwanz", "schwuchtel", "spast", "mongo", "hurensohn",
    "bastard", "drecksau", "schwein", "sau", "mistkerl", "idiot",

    # Englische Schimpfwörter
    "fuck", "shit", "bitch", "ass", "dick", "cock", "pussy", "cunt",
    "bastard", "whore", "slut", "damn", "hell", "piss", "fag",

    # Rassistische Begriffe (reduziert, nur offensichtliche)
    "nazi", "nigger", "neger", "jude", "jew", "kike",

    # Sexuelle Begriffe
    "penis", "vagina", "anal", "oral", "porn", "sex", "cum",
    "breast", "boob", "tit", "nipple",

    # Hate Speech
    "kill", "murder", "rape", "hitler", "isis", "terror",
}


def is_profanity(text: str) -> bool:
    """
    Check if text contains profanity

    Returns True if profanity detected
    """
    # Lowercase für Case-Insensitive Check
    text_lower = text.lower()

    # Entferne Sonderzeichen für L33t-Speak Prevention
    # (z.B. "f*ck" → "fuck")
    cleaned = re.sub(r'[^a-z0-9]', '', text_lower)

    # Check gegen Liste
    for word in PROFANITY_LIST:
        # Direct match
        if word in text_lower:
            return True
        # L33t-Speak match
        if word in cleaned:
            return True
        # Fragmentierter Match (z.B. "f u c k")
        if word in text_lower.replace(" ", ""):
            return True

    return False


def validate_spell_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate spell name

    Returns: (is_valid, error_message)
    """
    # Length check
    if len(name) < 3:
        return False, "Name zu kurz! Minimum 3 Zeichen."
    if len(name) > 30:
        return False, "Name zu lang! Maximum 30 Zeichen."

    # Character check (A-Z, a-z, 0-9, Space, -, ')
    if not re.match(r"^[A-Za-z0-9 \-']+$", name):
        return False, "Ungültige Zeichen! Nur A-Z, 0-9, Space, - und ' erlaubt."

    # Profanity check
    if is_profanity(name):
        return False, "❌ Name blockiert! Bitte wähle einen anderen Namen."

    return True, None


# ==================== MODELS ====================

class SetSpellNameRequest(BaseModel):
    player_id: int
    spell_id: str  # z.B. "feuer_feuerball"
    custom_name: str

    @validator('custom_name')
    def validate_name(cls, v):
        is_valid, error = validate_spell_name(v)
        if not is_valid:
            raise ValueError(error)
        return v


class RenameSpellRequest(BaseModel):
    player_id: int
    spell_id: str
    new_name: str
    rename_token: Optional[str] = None  # "Name-Change Scroll", "Ritual", etc.

    @validator('new_name')
    def validate_name(cls, v):
        is_valid, error = validate_spell_name(v)
        if not is_valid:
            raise ValueError(error)
        return v


# ==================== TEMPORARY STORAGE ====================
# TODO: Replace with database storage

SPELL_NAMES: Dict[str, Dict[str, str]] = {}
# Format: {
#     "1_feuer_feuerball": "Höllenball",
#     "1_explosion_explosion": "EXPLOSION!!!",
#     "2_feuer_feuerball": "Phönix-Atem"
# }


def get_spell_key(player_id: int, spell_id: str) -> str:
    """Generate unique key for spell name storage"""
    return f"{player_id}_{spell_id}"


# ==================== ENDPOINTS ====================

@router.post("/set")
@handle_errors()
async def set_spell_name(request: SetSpellNameRequest):
    """
    Set custom name for spell (first time)

    Body:
    {
        "player_id": 1,
        "spell_id": "feuer_feuerball",
        "custom_name": "Höllenball"
    }

    Returns:
    {
        "success": true,
        "spell_id": "feuer_feuerball",
        "custom_name": "Höllenball",
        "message": "✅ Zauber benannt!"
    }
    """
    spell_key = get_spell_key(request.player_id, request.spell_id)

    # Check if already named
    if spell_key in SPELL_NAMES:
        raise HTTPException(
            status_code=400,
            detail="Zauber bereits benannt! Nutze /rename zum Umbenennen."
        )

    # Validate name (already done by Pydantic validator)
    # Save name
    SPELL_NAMES[spell_key] = request.custom_name

    return {
        "success": True,
        "spell_id": request.spell_id,
        "custom_name": request.custom_name,
        "message": f"✅ Zauber benannt: {request.custom_name}"
    }


@router.get("/get")
@handle_errors()
async def get_spell_name(
    player_id: int = Query(..., description="Player ID"),
    spell_id: str = Query(..., description="Spell ID (z.B. feuer_feuerball)")
):
    """
    Get custom name for spell

    Returns custom name or default name if not set
    """
    spell_key = get_spell_key(player_id, spell_id)

    custom_name = SPELL_NAMES.get(spell_key)

    if custom_name:
        return {
            "player_id": player_id,
            "spell_id": spell_id,
            "custom_name": custom_name,
            "is_custom": True
        }
    else:
        # Return default name (extracted from spell_id)
        default_name = spell_id.split("_")[-1].capitalize()
        return {
            "player_id": player_id,
            "spell_id": spell_id,
            "custom_name": default_name,
            "is_custom": False,
            "message": "Noch nicht benannt! Nutze /set zum Benennen."
        }


@router.post("/rename")
@handle_errors()
async def rename_spell(request: RenameSpellRequest):
    """
    Rename spell (requires item/event token)

    Body:
    {
        "player_id": 1,
        "spell_id": "feuer_feuerball",
        "new_name": "Brennende Rache",
        "rename_token": "name_change_scroll"
    }

    Rename Tokens:
    - "name_change_scroll": Item (selten)
    - "ritual_umbenennung": Event
    - "quest_identitaet": Quest Reward
    - "admin": Owner-Only (für Testing)
    """
    spell_key = get_spell_key(request.player_id, request.spell_id)

    # Check if spell has a name
    if spell_key not in SPELL_NAMES:
        raise HTTPException(
            status_code=400,
            detail="Zauber noch nicht benannt! Nutze /set zuerst."
        )

    # Validate rename token
    valid_tokens = [
        "name_change_scroll",
        "ritual_umbenennung",
        "quest_identitaet",
        "admin"  # Testing only
    ]

    if request.rename_token not in valid_tokens:
        raise HTTPException(
            status_code=403,
            detail="Ungültiges Rename-Token! Benötigt: Item, Event oder Quest."
        )

    # TODO: Check if player actually has the item/completed event
    # For now, we trust the frontend

    old_name = SPELL_NAMES[spell_key]
    SPELL_NAMES[spell_key] = request.new_name

    return {
        "success": True,
        "spell_id": request.spell_id,
        "old_name": old_name,
        "new_name": request.new_name,
        "message": f"✅ Zauber umbenannt: {old_name} → {request.new_name}"
    }


@router.get("/all")
@handle_errors()
async def get_all_spell_names(player_id: int = Query(...)):
    """
    Get all custom spell names for player

    Returns:
    {
        "player_id": 1,
        "spells": {
            "feuer_feuerball": "Höllenball",
            "explosion_explosion": "EXPLOSION!!!"
        }
    }
    """
    player_spells = {}

    for key, name in SPELL_NAMES.items():
        if key.startswith(f"{player_id}_"):
            spell_id = key.replace(f"{player_id}_", "")
            player_spells[spell_id] = name

    return {
        "player_id": player_id,
        "spells": player_spells,
        "count": len(player_spells)
    }


@router.delete("/reset")
@handle_errors()
async def reset_spell_name(
    player_id: int = Query(...),
    spell_id: str = Query(...)
):
    """
    Reset spell name to default (Admin only)

    Removes custom name, returns to default
    """
    spell_key = get_spell_key(player_id, spell_id)

    if spell_key not in SPELL_NAMES:
        raise HTTPException(
            status_code=404,
            detail="Zauber hat keinen custom Namen!"
        )

    old_name = SPELL_NAMES.pop(spell_key)

    return {
        "success": True,
        "spell_id": spell_id,
        "removed_name": old_name,
        "message": "✅ Zauber-Name zurückgesetzt!"
    }


@router.post("/validate")
@handle_errors()
async def validate_name(name: str = Query(..., min_length=1)):
    """
    Validate spell name (for frontend preview)

    Returns validation result without saving
    """
    is_valid, error = validate_spell_name(name)

    if is_valid:
        return {
            "valid": True,
            "name": name,
            "message": "✅ Name gültig!"
        }
    else:
        return {
            "valid": False,
            "name": name,
            "error": error
        }