"""
Najika Combat Magic API Router
==============================
Vereintes Combat + Magic + Infuse System

FEATURES:
1. Weapon Infuse (Zauber auf Waffe = temporaerer Buff)
2. Spell Casting (Skyrim-Style, Zauber in Hand)
3. Combo Attacks (Feuerball + Schwerthieb gleichzeitig, wenn trainiert!)
4. Learning by Doing (XP beim Benutzen)

WICHTIG:
- Explosion kann NIEMALS auf Waffen angewendet werden!
- Explosion kann NIEMALS mit anderen Elementen kombiniert werden!

Author: Claude Code Team
Date: 2026-02-06
"""

from fastapi import APIRouter, HTTPException, Query
from backend.utils import handle_errors
from pydantic import BaseModel
from typing import Optional, Dict, List
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Systems
try:
    from najika_combat_hands_system import (
        get_combat_system,
        get_infuse_system,
        get_grab_system,
        get_tids_system,
        HandSlot,
        AttackType,
        SPELLS_DB,
        WEAPONS_DB,
        MagicElement,
        PlayerCombatStats,
        GrabMoveType
    )
    COMBAT_MAGIC_AVAILABLE = True
except ImportError as e:
    COMBAT_MAGIC_AVAILABLE = False
    print(f"Combat Magic System nicht verfuegbar: {e}")

router = APIRouter(prefix="/api/combat-magic", tags=["Combat Magic"])


# ============================================================================
# REQUEST MODELS
# ============================================================================

class EquipSpellRequest(BaseModel):
    player_id: str
    spell_id: str
    hand: str  # "left", "right", "both"


class InfuseWeaponRequest(BaseModel):
    player_id: str
    spell_hand: str  # "left" oder "right" - wo der Zauber ist
    weapon_hand: str  # "left" oder "right" - wo die Waffe ist


class CastSpellRequest(BaseModel):
    player_id: str
    hand: str  # "left", "right"
    target_id: Optional[str] = None


class ComboAttackRequest(BaseModel):
    """
    Echter Combo: Zauber + Waffenangriff gleichzeitig
    NICHT das Gleiche wie Infuse (temporaerer Buff)!

    Beispiel: Feuerball werfen UND mit Schwert zuschlagen
    Braucht Training in beiden Skills!
    """
    player_id: str
    spell_hand: str  # "left" oder "right" - Zauber wirken
    weapon_hand: str  # "left" oder "right" - Waffe schwingen
    target_id: Optional[str] = None


class RegisterPlayerRequest(BaseModel):
    player_id: str
    stats: Optional[Dict[str, int]] = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def hand_from_string(hand_str: str) -> HandSlot:
    """Konvertiert String zu HandSlot Enum"""
    if hand_str == "left":
        return HandSlot.LEFT
    elif hand_str == "right":
        return HandSlot.RIGHT
    else:
        return HandSlot.BOTH


def check_system():
    """Prueft ob System verfuegbar"""
    if not COMBAT_MAGIC_AVAILABLE:
        raise HTTPException(status_code=503, detail="Combat Magic System nicht verfuegbar")


# ============================================================================
# SPELL ENDPOINTS
# ============================================================================

@router.get("/spells")
@handle_errors()
async def get_all_spells():
    """
    Alle verfuegbaren Zauber

    Zauber koennen in Haende ausgeruestet werden (Skyrim-Style)
    Manche Zauber koennen auf Waffen angewendet werden (Infuse)
    """
    check_system()

    spells = []
    for spell_id, spell in SPELLS_DB.items():
        spells.append({
            "spell_id": spell.spell_id,
            "name": spell.name,
            "name_de": spell.name_de,
            "element": spell.element.value,
            "mana_cost": spell.mana_cost,
            "stamina_cost": spell.stamina_cost,
            "base_damage": spell.base_damage,
            "base_heal": spell.base_heal,
            "cast_time": spell.cast_time,
            "can_infuse": spell.infuse_duration > 0,
            "infuse_bonus": f"+{int(spell.infuse_damage_bonus * 100)}%" if spell.infuse_duration > 0 else None,
            "infuse_duration": spell.infuse_duration if spell.infuse_duration > 0 else None
        })

    return {
        "spells": spells,
        "total": len(spells)
    }


@router.get("/spells/{element}")
@handle_errors()
async def get_spells_by_element(element: str):
    """Zauber nach Element filtern"""
    check_system()

    try:
        target_element = MagicElement(element)
    except ValueError:
        valid_elements = [e.value for e in MagicElement]
        raise HTTPException(
            status_code=400,
            detail=f"Ungueltiges Element: {element}. Verfuegbar: {valid_elements}"
        )

    spells = []
    for spell_id, spell in SPELLS_DB.items():
        if spell.element == target_element:
            spells.append({
                "spell_id": spell.spell_id,
                "name": spell.name,
                "name_de": spell.name_de,
                "mana_cost": spell.mana_cost,
                "base_damage": spell.base_damage,
                "can_infuse": spell.infuse_duration > 0
            })

    return {
        "element": element,
        "spells": spells,
        "total": len(spells)
    }


@router.post("/spell/learn")
@handle_errors()
async def learn_spell(player_id: str, spell_id: str):
    """
    Zauber lernen

    Zauber muessen gelernt werden bevor sie ausgeruestet werden koennen.
    Learning by Doing = mehr XP wenn du sie benutzt!
    """
    check_system()

    infuse_sys = get_infuse_system()
    result = infuse_sys.learn_spell(player_id, spell_id)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@router.post("/spell/equip")
@handle_errors()
async def equip_spell(request: EquipSpellRequest):
    """
    Zauber in Hand ausruesten (Skyrim-Style)

    Beispiel: Linke Hand = Feuerball, Rechte Hand = Schwert
    """
    check_system()

    infuse_sys = get_infuse_system()
    hand = hand_from_string(request.hand)

    result = infuse_sys.equip_spell(request.player_id, request.spell_id, hand)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@router.get("/spell/learned/{player_id}")
@handle_errors()
async def get_learned_spells(player_id: str):
    """Alle gelernten Zauber eines Spielers"""
    check_system()

    infuse_sys = get_infuse_system()
    learned = infuse_sys.learned_spells.get(player_id, [])

    spells_info = []
    for spell_id in learned:
        spell = SPELLS_DB.get(spell_id)
        if spell:
            spells_info.append({
                "spell_id": spell_id,
                "name_de": spell.name_de,
                "element": spell.element.value
            })

    return {
        "player_id": player_id,
        "learned_spells": spells_info,
        "total": len(spells_info)
    }


# ============================================================================
# INFUSE ENDPOINTS (Zauber auf Waffe = temporaerer Buff)
# ============================================================================

@router.post("/infuse")
@handle_errors()
async def infuse_weapon(request: InfuseWeaponRequest):
    """
    WEAPON INFUSE - Zauber auf Waffe = temporaerer Buff

    Beispiel:
    - Linke Hand: Feuerball
    - Rechte Hand: Schwert
    - Aktion: Feuer auf Schwert wirken
    - Ergebnis: Flammenschwert fuer 30 Sekunden (+30% Feuerschaden)

    WICHTIG:
    - EXPLOSION kann NIEMALS auf Waffen angewendet werden!
    - Dies ist NICHT ein Combo-Angriff, sondern ein BUFF!
    """
    check_system()

    infuse_sys = get_infuse_system()
    spell_hand = hand_from_string(request.spell_hand)
    weapon_hand = hand_from_string(request.weapon_hand)

    result = infuse_sys.infuse_weapon(request.player_id, spell_hand, weapon_hand)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@router.get("/infuse/active/{player_id}")
@handle_errors()
async def get_active_infuses(player_id: str):
    """
    Alle aktiven Weapon Infuses fuer einen Spieler

    Zeigt welche Waffen gerade verzaubert sind und wie lange noch
    """
    check_system()

    infuse_sys = get_infuse_system()
    active = infuse_sys.get_active_infuses(player_id)

    return {
        "player_id": player_id,
        "active_infuses": active,
        "total": len(active)
    }


# ============================================================================
# COMBO ATTACK ENDPOINTS (Zauber + Waffe gleichzeitig)
# ============================================================================

@router.post("/combo")
@handle_errors()
async def combo_attack(request: ComboAttackRequest):
    """
    ECHTER COMBO ANGRIFF - Zauber UND Waffe gleichzeitig

    Dies ist NICHT das Gleiche wie Infuse!

    Beispiel:
    - Linke Hand: Feuerball (wirft den Zauber)
    - Rechte Hand: Schwert (schwingt gleichzeitig)
    - Effekt: Beides passiert, aber keine magische Kombination

    ANFORDERUNGEN:
    - Braucht Training in BEIDEN Skills
    - Schnellzauber-Perk hilft (weniger Cast-Zeit)
    - Waffen-Skill hilft (weniger Fumble)

    REALISTISCH:
    - Ein trainierter Kaempfer kann beides - wie in echten Kaempfen!
    """
    check_system()

    combat_sys = get_combat_system()
    infuse_sys = get_infuse_system()

    # Spieler pruefen
    if request.player_id not in combat_sys.players:
        raise HTTPException(status_code=404, detail="Spieler nicht registriert")

    player = combat_sys.players[request.player_id]
    loadout = infuse_sys.get_or_create_loadout(request.player_id)

    # Was ist in welcher Hand?
    spell_slot = hand_from_string(request.spell_hand)
    weapon_slot = hand_from_string(request.weapon_hand)

    spell_id = loadout.left_spell if spell_slot == HandSlot.LEFT else loadout.right_spell
    weapon_id = loadout.right_hand if weapon_slot == HandSlot.RIGHT else loadout.left_hand

    if not spell_id:
        raise HTTPException(status_code=400, detail=f"Kein Zauber in {request.spell_hand} Hand!")

    if not weapon_id:
        raise HTTPException(status_code=400, detail=f"Keine Waffe in {request.weapon_hand} Hand!")

    spell = SPELLS_DB.get(spell_id)
    weapon = WEAPONS_DB.get(weapon_id)

    if not spell or not weapon:
        raise HTTPException(status_code=400, detail="Zauber oder Waffe nicht gefunden!")

    # Ressourcen pruefen
    total_mana = spell.mana_cost
    total_stamina = spell.stamina_cost + weapon.stamina_light  # Light attack fuer Combo

    if player.mana < total_mana:
        raise HTTPException(status_code=400, detail=f"Nicht genug Mana! ({player.mana}/{total_mana})")

    if player.stamina < total_stamina:
        raise HTTPException(status_code=400, detail=f"Nicht genug Stamina! ({player.stamina}/{total_stamina})")

    # Ressourcen abziehen
    player.mana -= total_mana
    player.stamina -= total_stamina

    # Zauber-Schaden
    spell_damage = spell.base_damage

    # Waffen-Schaden (mit Effektivitaet)
    weapon_attack = combat_sys.attack(request.player_id, weapon_slot, AttackType.LIGHT)
    weapon_damage = weapon_attack.damage

    # Timing: Laengste Cast-Zeit + Waffen-Zeit
    total_time = spell.cast_time + weapon_attack.attack_time

    # Mit Schnellzauber-Perks reduzieren
    cast_reduction = combat_sys._get_cast_time_reduction(
        request.player_id,
        spell.element.value,
        player.intelligence
    )
    total_time = total_time * (1 - cast_reduction * 0.5)  # Nur halbe Reduktion fuer Combo

    # XP fuer beide (Learning by Doing!)
    magic_xp = combat_sys._gain_magic_xp(request.player_id, spell.element.value, 15)
    weapon_xp = weapon_attack.xp_gained.get("weapon", 0)

    return {
        "success": True,
        "combo_type": "spell_weapon",
        "spell": {
            "id": spell_id,
            "name": spell.name_de,
            "element": spell.element.value,
            "damage": spell_damage
        },
        "weapon": {
            "id": weapon_id,
            "name": weapon.name_de,
            "damage": weapon_damage,
            "fumbled": weapon_attack.fumbled
        },
        "total_damage": spell_damage + weapon_damage,
        "total_time": round(total_time, 2),
        "mana_cost": total_mana,
        "stamina_cost": total_stamina,
        "xp_gained": {
            "magic": magic_xp,
            "weapon": weapon_xp
        },
        "message": f"⚔️ {spell.name_de} + {weapon.name_de}: {spell_damage + weapon_damage} Schaden!"
    }


# ============================================================================
# PLAYER & STATUS ENDPOINTS
# ============================================================================

@router.post("/player/register")
@handle_errors()
async def register_player(request: RegisterPlayerRequest):
    """Spieler beim Combat System registrieren"""
    check_system()

    combat_sys = get_combat_system()

    # Stats setzen falls uebergeben
    stats = None
    if request.stats:
        stats = PlayerCombatStats(
            strength=request.stats.get("strength", 5),
            perception=request.stats.get("perception", 5),
            endurance=request.stats.get("endurance", 5),
            charisma=request.stats.get("charisma", 5),
            intelligence=request.stats.get("intelligence", 5),
            agility=request.stats.get("agility", 5),
            luck=request.stats.get("luck", 5)
        )

    combat_sys.register_player(request.player_id, stats)

    return {
        "success": True,
        "player_id": request.player_id,
        "message": "Spieler registriert!"
    }


@router.get("/player/{player_id}/status")
@handle_errors()
async def get_player_status(player_id: str):
    """Kompletter Spieler-Status (Combat + Magic)"""
    check_system()

    combat_sys = get_combat_system()
    infuse_sys = get_infuse_system()

    if player_id not in combat_sys.players:
        raise HTTPException(status_code=404, detail="Spieler nicht registriert")

    # Combat Status
    combat_status = combat_sys.get_player_status(player_id)

    # Magic Status
    loadout = infuse_sys.get_or_create_loadout(player_id)
    learned_spells = infuse_sys.learned_spells.get(player_id, [])
    active_infuses = infuse_sys.get_active_infuses(player_id)

    return {
        **combat_status,
        "magic": {
            "left_spell": loadout.left_spell,
            "right_spell": loadout.right_spell,
            "learned_spells": learned_spells,
            "active_infuses": active_infuses
        }
    }


@router.get("/player/{player_id}/loadout")
@handle_errors()
async def get_player_loadout(player_id: str):
    """Was hat der Spieler in welcher Hand?"""
    check_system()

    combat_sys = get_combat_system()
    infuse_sys = get_infuse_system()

    if player_id not in combat_sys.players:
        raise HTTPException(status_code=404, detail="Spieler nicht registriert")

    loadout = infuse_sys.get_or_create_loadout(player_id)

    left_weapon = WEAPONS_DB.get(loadout.left_hand) if loadout.left_hand else None
    right_weapon = WEAPONS_DB.get(loadout.right_hand) if loadout.right_hand else None
    left_spell = SPELLS_DB.get(loadout.left_spell) if loadout.left_spell else None
    right_spell = SPELLS_DB.get(loadout.right_spell) if loadout.right_spell else None

    return {
        "player_id": player_id,
        "left_hand": {
            "type": "weapon" if loadout.left_hand else ("spell" if loadout.left_spell else "empty"),
            "weapon": {
                "id": loadout.left_hand,
                "name": left_weapon.name_de if left_weapon else None
            } if loadout.left_hand else None,
            "spell": {
                "id": loadout.left_spell,
                "name": left_spell.name_de if left_spell else None,
                "element": left_spell.element.value if left_spell else None
            } if loadout.left_spell else None
        },
        "right_hand": {
            "type": "weapon" if loadout.right_hand else ("spell" if loadout.right_spell else "empty"),
            "weapon": {
                "id": loadout.right_hand,
                "name": right_weapon.name_de if right_weapon else None
            } if loadout.right_hand else None,
            "spell": {
                "id": loadout.right_spell,
                "name": right_spell.name_de if right_spell else None,
                "element": right_spell.element.value if right_spell else None
            } if loadout.right_spell else None
        },
        "two_handed": loadout.using_two_handed,
        "two_handed_weapon": loadout.two_handed_weapon
    }


# ============================================================================
# GRAB & THROW ENDPOINTS (Wrestling-Style!)
# ============================================================================

class GrabRequest(BaseModel):
    player_id: str
    target_id: str


class GrabMoveRequest(BaseModel):
    player_id: str
    move: str  # "suplex", "chokeslam", "throw_object", "throw_enemy", "release"


class TIDSRequest(BaseModel):
    player_id: str
    target_type: str = "humanoid"  # humanoid, slime, skeleton, ghost, golem, dragon, etc.
    target_name: str = ""  # Optional: Name des Gegners fuer lustigere Nachrichten
    is_boss: bool = False


@router.post("/grab")
@handle_errors()
async def grab_enemy(request: GrabRequest):
    """
    GEGNER GREIFEN (Wrestling-Style!)

    Erfolg basiert auf:
    - Staerke des Spielers
    - Grab-Skill Level
    - 20 Stamina Kosten

    Nach erfolgreichem Griff: Waehle Follow-Up Move!
    """
    check_system()

    grab_sys = get_grab_system()
    result = grab_sys.grab(request.player_id, request.target_id)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


@router.post("/grab/execute")
@handle_errors()
async def execute_grab_move(request: GrabMoveRequest):
    """
    GRIFF-MOVE AUSFUEHREN

    Verfuegbare Moves:
    - suplex: Hoher Schaden + 2s Stun (Skill 15 noetig!)
    - chokeslam: Mittlerer Schaden + 3s am Boden (Skill 10 noetig!)
    - throw_object: In Umgebungsobjekt werfen
    - throw_enemy: Auf anderen Gegner werfen (Skill 5 noetig!)
    - release: Loslassen
    """
    check_system()

    grab_sys = get_grab_system()
    result = grab_sys.execute_grab_move(request.player_id, request.move)

    return {
        "success": result.success,
        "move": result.move_type.value,
        "damage": result.damage,
        "stun_duration": result.stun_duration,
        "grounded_duration": result.grounded_duration,
        "environment_bonus": result.environment_bonus,
        "xp_gained": result.xp_gained,
        "message": result.message
    }


@router.get("/grab/skill/{player_id}")
@handle_errors()
async def get_throw_skill(player_id: str):
    """Wurf-Skill Status und freigeschaltete Moves"""
    check_system()

    grab_sys = get_grab_system()
    return grab_sys.get_throw_skill(player_id)


# ============================================================================
# TIDS - TRITT IN DEN SCHRITT (Gag Move!)
# ============================================================================

@router.post("/tids")
@handle_errors()
async def use_tids(request: TIDSRequest):
    """
    TIDS - TRITT IN DEN SCHRITT!

    Der ultimative Gag-Move - jetzt mit MONSTER-REAKTIONEN!

    EFFEKTE JE NACH GEGNER-TYP:
    - humanoid: Voller Effekt (3s Stun, +90% Flucht)
    - slime/blob/ghost: Kein Effekt, aber lustige Reaktion
    - golem/robot: DU nimmst Schaden! (Metall/Stein tut weh!)
    - skeleton: Kurze Verwirrung (0.5s)
    - wolf/dragon: Konter-Angriff! (-10 HP, -20% Flucht)
    - plant/fish: Einfach nur absurd

    Einschraenkungen:
    - 24 STUNDEN Cooldown (auch bei Fehlschlag!)
    - Funktioniert NICHT gegen Bosse!
    """
    check_system()

    tids_sys = get_tids_system()
    result = tids_sys.use_tids(
        request.player_id,
        request.target_type,
        request.is_boss,
        request.target_name
    )

    return {
        "success": result.success,
        "damage": result.damage,  # Kann NEGATIV sein (Spieler nimmt Schaden!)
        "stun_duration": result.stun_duration,
        "flee_bonus": result.flee_bonus,  # Kann NEGATIV sein!
        "flee_duration": result.flee_duration,
        "cooldown_remaining": result.cooldown_remaining,
        "message": result.message,
        "gag_message": result.gag_message,  # Die lustige Reaktion!
        "is_gag": result.is_gag
    }


@router.get("/tids/cooldown/{player_id}")
@handle_errors()
async def get_tids_cooldown(player_id: str):
    """TIDS Cooldown Status"""
    check_system()

    tids_sys = get_tids_system()
    remaining = tids_sys.get_cooldown(player_id)

    return {
        "player_id": player_id,
        "on_cooldown": remaining is not None,
        "remaining_hours": remaining,
        "ready": remaining is None
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
@handle_errors()
async def combat_magic_health():
    """System Health Check"""
    return {
        "available": COMBAT_MAGIC_AVAILABLE,
        "system": "najika_combat_magic",
        "features": [
            "spell_learning",
            "spell_equipping",
            "weapon_infuse",
            "combo_attacks",
            "grab_throw",
            "suplex",
            "chokeslam",
            "tids",
            "learning_by_doing"
        ],
        "rules": [
            "EXPLOSION kann NIEMALS auf Waffen angewendet werden!",
            "EXPLOSION kann NIEMALS mit anderen Elementen kombiniert werden!",
            "TIDS funktioniert NUR bei Humanoiden!",
            "TIDS hat 24h Cooldown!"
        ]
    }
