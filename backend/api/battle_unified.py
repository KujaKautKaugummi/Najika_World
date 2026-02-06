"""
UNIFIED BATTLE API V2 - Najika World
=====================================
Vereinigt alle Battle-Systeme unter einer API.

WICHTIG - UNTERSCHIED ZWISCHEN ARENEN:
=====================================

SPIELER-ARENA / GAME WORLD:
- Spieler ist IMMER MANUAL (direkte Steuerung)
- Companion (Najika/Slime) hat: AUTO oder CHEER
- Companion kann KÖRPERLICH (physisch) oder AURA (fusioniert) sein
- Modi: HARDCORE, NORMAL, SOFTY (Training), WELLE

SCHLEIM-ARENA:
- Alle 3 Modi anwendbar: AUTO, MANUAL, CHEER
- MANUAL = Spieler übernimmt DIREKTE Kontrolle über seinen Slime
- Modi: NORMAL, WELLE

EXTENDED AUTO MODE:
- "Companion führt" Toggle
- KI gibt taktische Befehle in ihrer Persönlichkeit
- Spieler kann folgen oder ignorieren
- Vertrauen steigt wenn Spieler folgt → KI wird mutiger

LEARNING TRANSFER:
- Was Spieler in MANUAL macht → KI lernt für AUTO
- KI kann später fragen "warum haben wir das nicht benutzt?"
- Spieler kann Kontext erklären (z.B. "das Dorf hätte gebrannt")

Port: 8000 (NIEMALS 5000!)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum
import random
import sys
import os
from datetime import datetime

# Import des Haupt-Battle-Systems
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from najika_battle import BattleSystem, ENEMY_DB, SKILL_DB

router = APIRouter(prefix="/api/battle", tags=["Battle Unified"])

# ===== ENUMS =====

class CombatMode(str, Enum):
    """Kampfmodus für den Companion (nicht den Spieler!)"""
    AUTO = "auto"      # KI-Kontrolle (Companion kämpft selbstständig)
    MANUAL = "manual"  # Direkte Befehle (Spieler gibt Befehle an Companion)
    CHEER = "cheer"    # Digimon-Anfeuern (Buffs durch Anfeuern)

class CompanionForm(str, Enum):
    """Form des Companions im Kampf"""
    KOERPERLICH = "koerperlich"  # Physische Form - kämpft neben Spieler
    AURA = "aura"                 # Aura-Form - fusioniert mit Spieler, gibt Buffs

class ArenaType(str, Enum):
    """Art der Arena"""
    PLAYER_ARENA = "player_arena"    # Spieler-Arena (Spieler + Companion)
    SLIME_ARENA = "slime_arena"      # Schleim-Arena (nur Slimes)
    GAME_WORLD = "game_world"        # Open World Kämpfe

class ArenaMode(str, Enum):
    """Modus innerhalb der Arena"""
    # Spieler-Arena Modi
    HARDCORE = "hardcore"    # Echter Tod möglich
    NORMAL = "normal"        # Standard PvP/PvE
    SOFTY = "softy"          # Training (kein echter Tod)
    WELLE = "welle"          # Wellen-System

class CheerType(str, Enum):
    ATTACK = "attack"      # +10% DMG für 3 Runden
    DEFEND = "defend"      # +20% DEF für 3 Runden
    COMBO = "combo"        # Nächster Angriff = Combo
    FOCUS = "focus"        # +15% ACC für 3 Runden
    HEAL = "heal"          # Kleine Heilung
    EXPLOSIVE = "explosive"  # EXPLOSION Buff (nur Najika!)

# ===== REQUEST MODELS =====

class StartBattleRequest(BaseModel):
    player_id: str
    arena_type: ArenaType = ArenaType.GAME_WORLD
    arena_mode: ArenaMode = ArenaMode.NORMAL
    companion_form: CompanionForm = CompanionForm.KOERPERLICH
    companion_combat_mode: CombatMode = CombatMode.AUTO
    companion_leads: bool = False  # "Companion führt" Toggle
    dungeon_level: int = 1
    boss_wave: int = 10

class PlayerActionRequest(BaseModel):
    """Spieler-Aktion (Spieler ist IMMER manual)"""
    player_id: str
    action: str  # attack, defend, skill, item, flee
    target_index: int = 0
    skill_name: Optional[str] = None
    item_name: Optional[str] = None

class CompanionActionRequest(BaseModel):
    """Manuelle Companion-Aktion (wenn MANUAL mode)"""
    player_id: str
    action: str
    target_index: int = 0
    skill_name: Optional[str] = None

class SlimeControlRequest(BaseModel):
    """Slime-Arena: Spieler kontrolliert Slime direkt"""
    player_id: str
    slime_id: str
    action: str
    target_index: int = 0
    skill_name: Optional[str] = None

class CheerRequest(BaseModel):
    player_id: str
    cheer_type: CheerType

class SetModeRequest(BaseModel):
    player_id: str
    companion_combat_mode: CombatMode
    companion_leads: bool = False

class SetCompanionFormRequest(BaseModel):
    player_id: str
    companion_form: CompanionForm

class ExplainDecisionRequest(BaseModel):
    """Spieler erklärt der KI warum er nicht gefolgt ist"""
    player_id: str
    explanation: str
    context_tags: List[str] = []  # z.B. ["village_nearby", "fire_danger"]


class FinisherRequest(BaseModel):
    """Finisher-Anfrage (wenn Gegner HP = 0)"""
    player_id: str
    words: List[str] = []  # Wörter die der Spieler vorgibt
    category: str = "ehrenvoll"  # ehrenvoll, lustig, grausam, episch
    target_index: int = 0


class BrutalityCategory(str, Enum):
    """Finisher-Kategorien"""
    EHRENVOLL = "ehrenvoll"   # Ehrenvoller Tod - respektvoll
    LUSTIG = "lustig"         # Lustiger Tod - komödiantisch
    GRAUSAM = "grausam"       # Grausamer Tod - brutal
    EPISCH = "episch"         # Epischer Tod - dramatisch
    NIEDLICH = "niedlich"     # Niedlicher Tod - cute (für Slime Arena)

# ===== BATTLE STATE MANAGER =====

class CompanionAI:
    """KI für den Companion mit Lernfähigkeit"""

    def __init__(self, personality: str = "neutral"):
        self.personality = personality  # megumin, harley, shiro, melissa
        self.trust_level = 50  # 0-100
        self.learned_combos: List[Dict] = []
        self.player_patterns: List[Dict] = []
        self.ignored_suggestions: List[Dict] = []
        self.context_memory: List[Dict] = []

    def get_suggestion(self, battle_state: Dict) -> Dict:
        """Gibt taktische Empfehlung in Persönlichkeit"""
        enemies = battle_state.get("enemies", [])
        player = battle_state.get("player", {})

        # Basis-Entscheidung
        suggestion = self._analyze_situation(enemies, player)

        # Persönlichkeits-Flavor
        suggestion["message"] = self._personality_message(suggestion)
        suggestion["confidence"] = min(100, self.trust_level + random.randint(-10, 20))

        return suggestion

    def _analyze_situation(self, enemies: List, player: Dict) -> Dict:
        """Analysiert Kampfsituation"""
        if not enemies:
            return {"action": "wait", "reason": "Keine Gegner"}

        # Kritische HP?
        if player.get("hp", 100) < player.get("max_hp", 100) * 0.3:
            return {
                "action": "defend_or_heal",
                "priority": "high",
                "reason": "HP kritisch!"
            }

        # Mehrere Gegner?
        if len(enemies) > 2:
            return {
                "action": "aoe_attack",
                "priority": "medium",
                "reason": f"{len(enemies)} Gegner - AoE empfohlen"
            }

        # Schwächsten Gegner fokussieren
        weakest = min(enemies, key=lambda e: e.get("hp", 100))
        return {
            "action": "focus_weak",
            "target": weakest.get("name", "Gegner"),
            "priority": "normal",
            "reason": "Schwächsten eliminieren"
        }

    def _personality_message(self, suggestion: Dict) -> str:
        """Formuliert Nachricht in Persönlichkeit"""
        action = suggestion.get("action", "")

        if self.personality == "megumin":
            messages = {
                "defend_or_heal": "Mr. K! Wir sollten uns heilen... DANACH EXPLOSION! 💥",
                "aoe_attack": "PERFEKT! Mehrere Ziele! EXPLOSIOOON!!! 💥💥💥",
                "focus_weak": "Der Schwächling zuerst... dann EXPLOSION für alle! 💥",
                "wait": "...wo sind die Explosionsziele? 🤔"
            }
        elif self.personality == "harley":
            messages = {
                "defend_or_heal": "Hey Mr. K! Zeit für'n Pflaster, Süßer! 🃏",
                "aoe_attack": "Oooh, Party-Time! Alle auf einmal! Hahaha! 🎭",
                "focus_weak": "Der Kleine zuerst, dann der Rest! Trust me, Mr. K! 💋",
                "wait": "Booooring! Wo bleiben die Bad Guys? 🃏"
            }
        elif self.personality == "shiro":
            messages = {
                "defend_or_heal": "...Heilung. 78% Überlebenschance. ...logisch.",
                "aoe_attack": "...Flächenangriff. Effizienz: 94%. ...optimal.",
                "focus_weak": "...Schwaches Ziel eliminieren. ...strategisch korrekt.",
                "wait": "...keine Daten. ...warte auf Input."
            }
        elif self.personality == "melissa":
            messages = {
                "defend_or_heal": "Kuja-sama, bitte pass auf dich auf! Ich heile dich! 💚",
                "aoe_attack": "I-Ich versuche alle zu treffen! Für Kuja-sama! 🌟",
                "focus_weak": "D-Der Kleine da... soll ich? Wenn du es sagst... 👉👈",
                "wait": "Äh... was soll ich tun, Kuja-sama? 🥺"
            }
        else:
            messages = {
                "defend_or_heal": "Empfehlung: Heilen oder Verteidigen",
                "aoe_attack": "Empfehlung: Flächenangriff",
                "focus_weak": "Empfehlung: Schwächsten Gegner fokussieren",
                "wait": "Warte auf Gegner..."
            }

        return messages.get(action, "...")

    def record_player_action(self, action: Dict, was_suggestion_followed: bool):
        """Speichert Spieler-Aktion für Lern-System"""
        self.player_patterns.append({
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "followed_suggestion": was_suggestion_followed
        })

        # Trust anpassen
        if was_suggestion_followed:
            self.trust_level = min(100, self.trust_level + 2)
        else:
            self.trust_level = max(0, self.trust_level - 1)

    def record_ignored_suggestion(self, suggestion: Dict, explanation: str = None):
        """Speichert ignorierte Vorschläge für spätere Fragen"""
        self.ignored_suggestions.append({
            "suggestion": suggestion,
            "explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        })

    def ask_about_decision(self) -> Optional[Dict]:
        """KI fragt nach ignorierter Entscheidung"""
        if not self.ignored_suggestions:
            return None

        # Wähle zufällig eine unbeantwortete
        unanswered = [s for s in self.ignored_suggestions if not s.get("explanation")]
        if not unanswered:
            return None

        question_target = random.choice(unanswered)

        if self.personality == "megumin":
            return {
                "question": f"Mr. K! Warum haben wir nicht {question_target['suggestion'].get('action')} benutzt?! Das wäre EXPLOSIV gewesen! 💥",
                "suggestion_ref": question_target
            }
        elif self.personality == "harley":
            return {
                "question": f"Hey Mr. K~ Warum hast du meinen genialen Plan ignoriert? Ich bin neugierig! 🃏",
                "suggestion_ref": question_target
            }
        elif self.personality == "shiro":
            return {
                "question": f"...warum wurde optimale Strategie nicht ausgeführt? ...Datensammlung.",
                "suggestion_ref": question_target
            }
        else:
            return {
                "question": f"K-Kuja-sama... war mein Vorschlag nicht gut genug? 🥺",
                "suggestion_ref": question_target
            }

    def learn_context(self, explanation: str, tags: List[str]):
        """Lernt aus Spieler-Erklärung"""
        self.context_memory.append({
            "explanation": explanation,
            "tags": tags,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Trust steigt wenn Spieler erklärt
        self.trust_level = min(100, self.trust_level + 5)


class UnifiedBattleManager:
    """Verwaltet alle aktiven Kämpfe"""

    def __init__(self):
        self.battles: Dict[str, Dict] = {}

    def get_or_create_battle(self, player_id: str) -> Dict:
        """Holt oder erstellt Battle für Spieler"""
        if player_id not in self.battles:
            self.battles[player_id] = {
                "system": BattleSystem(),
                "arena_type": ArenaType.GAME_WORLD,
                "arena_mode": ArenaMode.NORMAL,
                "companion_form": CompanionForm.KOERPERLICH,
                "companion_combat_mode": CombatMode.AUTO,
                "companion_leads": False,
                "companion_ai": CompanionAI(personality="megumin"),
                "pending_suggestion": None,
                "cheer_buffs": {
                    "attack": 0,
                    "defend": 0,
                    "combo": 0,
                    "focus": 0
                },
                "turn_count": 0,
                "player_actions_log": [],
                "companion_actions_log": []
            }
        return self.battles[player_id]

    def remove_battle(self, player_id: str):
        """Entfernt Battle nach Abschluss"""
        if player_id in self.battles:
            del self.battles[player_id]

# Global Manager Instance
battle_manager = UnifiedBattleManager()

# ===== CHEER EFFECTS =====

CHEER_EFFECTS = {
    CheerType.ATTACK: {"buff": "attack", "value": 1.1, "rounds": 3, "message": "💪 LOS! Angriff verstärkt!"},
    CheerType.DEFEND: {"buff": "defend", "value": 1.2, "rounds": 3, "message": "🛡️ DEFEND! Verteidigung erhöht!"},
    CheerType.COMBO: {"buff": "combo", "value": 2.0, "rounds": 1, "message": "💥 COMBO! Nächster Angriff x2!"},
    CheerType.FOCUS: {"buff": "focus", "value": 1.15, "rounds": 3, "message": "🎯 FOCUS! Genauigkeit erhöht!"},
    CheerType.HEAL: {"buff": "heal", "value": 15, "rounds": 0, "message": "💚 Kleine Heilung!"},
    CheerType.EXPLOSIVE: {"buff": "explosive", "value": 5.0, "rounds": 1, "message": "💥 EXPLOSION!!! (Najika Mode!)"}
}

# ===== AURA FORM BUFFS =====

AURA_BUFFS = {
    "bubble": {"defense": 1.2, "water_resist": 0.5, "passive": "Seifenblasenschild"},
    "molten": {"attack": 1.3, "fire_damage": 1.5, "passive": "Vulkanische Wut"},
    "crystal": {"defense": 1.4, "reflect": 0.1, "passive": "Kristallpanzer"},
    "shadow": {"evasion": 1.3, "crit": 1.2, "passive": "Schattenschritt"},
    "nature": {"regen": 5, "poison_resist": 0.8, "passive": "Naturheilung"},
    "storm": {"speed": 1.3, "lightning_damage": 1.4, "passive": "Blitzreflexe"}
}


def apply_cheer_buffs_to_action(battle_data: Dict, action_result: Dict) -> Dict:
    """Wendet Cheer-Buffs auf Aktionsergebnis an"""
    cheer_buffs = battle_data["cheer_buffs"]

    # Attack Boost
    if cheer_buffs.get("attack", 0) > 0 and "damage" in action_result:
        original = action_result["damage"]
        action_result["damage"] = int(original * CHEER_EFFECTS[CheerType.ATTACK]["value"])
        action_result["cheer_bonus"] = f"💪 Attack Boost: {original} → {action_result['damage']}"
        cheer_buffs["attack"] -= 1

    # Combo
    if cheer_buffs.get("combo", 0) > 0 and "damage" in action_result:
        original = action_result["damage"]
        action_result["damage"] = int(original * CHEER_EFFECTS[CheerType.COMBO]["value"])
        action_result["combo_bonus"] = f"💥 COMBO! {original} → {action_result['damage']}"
        cheer_buffs["combo"] = 0

    # Defense Boost
    if cheer_buffs.get("defend", 0) > 0 and "damage_taken" in action_result:
        original = action_result["damage_taken"]
        action_result["damage_taken"] = int(original / CHEER_EFFECTS[CheerType.DEFEND]["value"])
        action_result["defend_bonus"] = f"🛡️ Defense Boost: {original} → {action_result['damage_taken']}"
        cheer_buffs["defend"] -= 1

    # Focus (Crit)
    if cheer_buffs.get("focus", 0) > 0:
        if random.random() < 0.15:
            if "damage" in action_result:
                action_result["damage"] = int(action_result["damage"] * 1.5)
                action_result["focus_crit"] = "🎯 CRITICAL HIT!"
        cheer_buffs["focus"] -= 1

    return action_result


def apply_aura_buffs(battle_data: Dict, slime_type: str) -> Dict:
    """Wendet Aura-Buffs an wenn Companion in AURA-Form"""
    if battle_data["companion_form"] != CompanionForm.AURA:
        return {}

    buffs = AURA_BUFFS.get(slime_type, {})
    return {
        "active_aura": slime_type,
        "buffs": buffs,
        "passive_effect": buffs.get("passive", "Keine")
    }


# ===== API ENDPOINTS =====

@router.post("/start")
async def start_battle(request: StartBattleRequest):
    """Startet einen neuen Kampf"""
    battle_data = battle_manager.get_or_create_battle(request.player_id)

    battle_data["arena_type"] = request.arena_type
    battle_data["arena_mode"] = request.arena_mode
    battle_data["companion_form"] = request.companion_form
    battle_data["companion_combat_mode"] = request.companion_combat_mode
    battle_data["companion_leads"] = request.companion_leads
    battle_data["turn_count"] = 0

    result = battle_data["system"].start_battle(
        dungeon_level=request.dungeon_level,
        boss_wave=request.boss_wave
    )

    # Erste KI-Empfehlung wenn "Companion führt"
    initial_suggestion = None
    if request.companion_leads:
        initial_suggestion = battle_data["companion_ai"].get_suggestion(
            battle_data["system"].battle_state
        )
        battle_data["pending_suggestion"] = initial_suggestion

    return {
        "success": True,
        "arena_type": request.arena_type,
        "arena_mode": request.arena_mode,
        "companion_setup": {
            "form": request.companion_form,
            "combat_mode": request.companion_combat_mode,
            "leads": request.companion_leads,
            "form_description": {
                CompanionForm.KOERPERLICH: "🐾 Körperlich: Companion kämpft physisch neben dir!",
                CompanionForm.AURA: "✨ Aura: Companion fusioniert mit dir, gibt passive Buffs!"
            }[request.companion_form]
        },
        "mode_description": {
            ArenaMode.HARDCORE: "☠️ HARDCORE: Echter Tod möglich!",
            ArenaMode.NORMAL: "⚔️ NORMAL: Standard Kampf",
            ArenaMode.SOFTY: "🎓 TRAINING: Kein echter Tod, lernen erlaubt!",
            ArenaMode.WELLE: "🌊 WELLE: Überlebe die Wellen!"
        }[request.arena_mode],
        "companion_suggestion": initial_suggestion,
        "battle_status": result,
        "message": f"Kampf gestartet! Arena: {request.arena_type}, Modus: {request.arena_mode}"
    }


@router.post("/player-action")
async def player_action(request: PlayerActionRequest):
    """
    Spieler-Aktion (Spieler ist IMMER manual in Game World / Player Arena)
    """
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]
    system = battle_data["system"]
    companion_ai = battle_data["companion_ai"]

    # Prüfe ob Vorschlag befolgt wurde
    was_suggestion_followed = False
    if battle_data["pending_suggestion"]:
        suggested_action = battle_data["pending_suggestion"].get("action", "")
        if request.action in suggested_action or suggested_action in request.action:
            was_suggestion_followed = True
        else:
            # Ignorierter Vorschlag speichern
            companion_ai.record_ignored_suggestion(battle_data["pending_suggestion"])

    # Aktion speichern für Lern-System
    companion_ai.record_player_action(
        {"action": request.action, "target": request.target_index},
        was_suggestion_followed
    )

    # Aktion ausführen
    kwargs = {}
    if request.skill_name:
        kwargs["skill_name"] = request.skill_name
    if request.item_name:
        kwargs["item_name"] = request.item_name

    result = system.player_action(
        action=request.action,
        target_index=request.target_index,
        **kwargs
    )

    # Log
    battle_data["player_actions_log"].append({
        "turn": battle_data["turn_count"],
        "action": request.action,
        "result": result
    })

    # Aura-Buffs anwenden wenn aktiv
    aura_info = apply_aura_buffs(battle_data, "bubble")  # TODO: echten Slime-Typ

    # Nächste KI-Empfehlung
    next_suggestion = None
    if battle_data["companion_leads"]:
        next_suggestion = companion_ai.get_suggestion(system.battle_state)
        battle_data["pending_suggestion"] = next_suggestion

    # KI fragt vielleicht nach ignorierter Entscheidung
    ai_question = None
    if random.random() < 0.1:  # 10% Chance
        ai_question = companion_ai.ask_about_decision()

    battle_data["turn_count"] += 1

    return {
        "success": True,
        "action_result": result,
        "followed_suggestion": was_suggestion_followed,
        "trust_level": companion_ai.trust_level,
        "aura_buffs": aura_info,
        "next_suggestion": next_suggestion,
        "ai_question": ai_question,
        "battle_status": system.get_battle_status()
    }


@router.post("/companion-action")
async def companion_action(request: CompanionActionRequest):
    """
    Companion-Aktion (nur wenn Companion MANUAL mode)
    Im AUTO mode handelt Companion selbstständig
    """
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]

    if battle_data["companion_form"] != CompanionForm.KOERPERLICH:
        raise HTTPException(
            status_code=400,
            detail="Companion ist in AURA-Form und kann keine eigenen Aktionen ausführen!"
        )

    if battle_data["companion_combat_mode"] != CombatMode.MANUAL:
        raise HTTPException(
            status_code=400,
            detail="Companion ist nicht im MANUAL-Modus! Wechsle den Modus oder nutze AUTO/CHEER."
        )

    system = battle_data["system"]

    # Companion-Aktion ausführen
    result = system.player_action(
        action=request.action,
        target_index=request.target_index,
        skill_name=request.skill_name
    )

    # Log
    battle_data["companion_actions_log"].append({
        "turn": battle_data["turn_count"],
        "action": request.action,
        "result": result
    })

    return {
        "success": True,
        "companion_action_result": result,
        "battle_status": system.get_battle_status()
    }


@router.post("/companion-auto-turn")
async def companion_auto_turn(player_id: str):
    """
    Companion führt AUTO-Zug aus (nur wenn AUTO oder CHEER mode)
    """
    if player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[player_id]

    if battle_data["companion_form"] != CompanionForm.KOERPERLICH:
        return {
            "success": True,
            "message": "Companion ist in AURA-Form - gibt passive Buffs statt zu kämpfen",
            "aura_buffs": apply_aura_buffs(battle_data, "bubble")
        }

    if battle_data["companion_combat_mode"] == CombatMode.MANUAL:
        raise HTTPException(
            status_code=400,
            detail="Companion ist im MANUAL-Modus! Nutze /companion-action für manuelle Befehle."
        )

    # KI entscheidet
    companion_ai = battle_data["companion_ai"]
    suggestion = companion_ai.get_suggestion(battle_data["system"].battle_state)

    # Vereinfache zu tatsächlicher Aktion
    action_map = {
        "defend_or_heal": "defend",
        "aoe_attack": "skill",
        "focus_weak": "attack",
        "wait": "defend"
    }
    actual_action = action_map.get(suggestion["action"], "attack")

    system = battle_data["system"]
    result = system.player_action(action=actual_action, target_index=0)

    # Cheer-Buffs anwenden
    result = apply_cheer_buffs_to_action(battle_data, result)

    return {
        "success": True,
        "ai_thought": suggestion["message"],
        "action_taken": actual_action,
        "action_result": result,
        "battle_status": system.get_battle_status()
    }


@router.post("/slime-arena/control")
async def slime_arena_control(request: SlimeControlRequest):
    """
    SCHLEIM-ARENA: Spieler kontrolliert Slime DIREKT (MANUAL mode)
    In der Schleim-Arena kann der Spieler seinen Slime selbst steuern!
    """
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]

    if battle_data["arena_type"] != ArenaType.SLIME_ARENA:
        raise HTTPException(
            status_code=400,
            detail="Direkte Slime-Kontrolle nur in der Schleim-Arena!"
        )

    system = battle_data["system"]

    result = system.player_action(
        action=request.action,
        target_index=request.target_index,
        skill_name=request.skill_name
    )

    return {
        "success": True,
        "slime_id": request.slime_id,
        "action_result": result,
        "message": f"Du steuerst deinen Slime direkt! Aktion: {request.action}",
        "battle_status": system.get_battle_status()
    }


@router.post("/cheer")
async def cheer_action(request: CheerRequest):
    """Führt einen Cheer aus (CHEER-Modus)"""
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]

    if battle_data["companion_combat_mode"] != CombatMode.CHEER:
        raise HTTPException(status_code=400, detail="Nicht im CHEER-Modus!")

    cheer_buffs = battle_data["cheer_buffs"]
    cheer_effect = CHEER_EFFECTS[request.cheer_type]
    buff_key = cheer_effect["buff"]

    if cheer_buffs.get(buff_key, 0) > 0:
        return {
            "success": False,
            "message": f"Dieser Buff ist noch aktiv ({cheer_buffs[buff_key]} Runden)!"
        }

    system = battle_data["system"]

    # Heal ist sofort
    if request.cheer_type == CheerType.HEAL:
        player = system.battle_state["player"]
        heal_amount = min(cheer_effect["value"], player["max_hp"] - player["hp"])
        player["hp"] += heal_amount

        return {
            "success": True,
            "cheer_type": request.cheer_type,
            "message": cheer_effect["message"],
            "effect": f"Geheilt um {heal_amount} HP!",
            "battle_status": system.get_battle_status()
        }

    # Andere Buffs für Runden
    cheer_buffs[buff_key] = cheer_effect["rounds"]

    # Nach Cheer: Companion greift automatisch an
    auto_result = None
    if battle_data["companion_form"] == CompanionForm.KOERPERLICH:
        if system.battle_state["enemies"]:
            auto_result = system.player_action("attack", target_index=0)
            auto_result = apply_cheer_buffs_to_action(battle_data, auto_result)

    return {
        "success": True,
        "cheer_type": request.cheer_type,
        "message": cheer_effect["message"],
        "buff_rounds": cheer_effect["rounds"],
        "companion_attack_result": auto_result,
        "battle_status": system.get_battle_status(),
        "active_buffs": cheer_buffs
    }


@router.post("/set-companion-mode")
async def set_companion_mode(request: SetModeRequest):
    """Wechselt den Companion-Kampfmodus"""
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]
    old_mode = battle_data["companion_combat_mode"]

    battle_data["companion_combat_mode"] = request.companion_combat_mode
    battle_data["companion_leads"] = request.companion_leads

    return {
        "success": True,
        "old_mode": old_mode,
        "new_mode": request.companion_combat_mode,
        "companion_leads": request.companion_leads,
        "message": f"Companion-Modus: {old_mode} → {request.companion_combat_mode}",
        "description": {
            CombatMode.AUTO: "🤖 Companion kämpft selbstständig!",
            CombatMode.MANUAL: "🎮 Du gibst Companion direkte Befehle!",
            CombatMode.CHEER: "📣 Feuere Companion an für Buffs!"
        }[request.companion_combat_mode]
    }


@router.post("/set-companion-form")
async def set_companion_form(request: SetCompanionFormRequest):
    """
    Wechselt die Companion-Form (KÖRPERLICH ↔ AURA)
    WICHTIG: Form-Wechsel nur 1x pro Saison oder bei seltenen Events!
    """
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]
    old_form = battle_data["companion_form"]

    # TODO: Check ob Form-Wechsel erlaubt (1x/Saison)

    battle_data["companion_form"] = request.companion_form

    return {
        "success": True,
        "old_form": old_form,
        "new_form": request.companion_form,
        "message": f"Companion-Form gewechselt: {old_form} → {request.companion_form}",
        "description": {
            CompanionForm.KOERPERLICH: "🐾 KÖRPERLICH: Companion kämpft physisch neben dir!",
            CompanionForm.AURA: "✨ AURA: Companion fusioniert mit dir, gibt passive Buffs!"
        }[request.companion_form],
        "warning": "⚠️ Form-Wechsel ist begrenzt! (1x pro Saison)"
    }


@router.post("/explain-decision")
async def explain_decision(request: ExplainDecisionRequest):
    """
    Spieler erklärt der KI warum er einen Vorschlag ignoriert hat.
    KI lernt daraus für zukünftige Situationen.
    """
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]
    companion_ai = battle_data["companion_ai"]

    companion_ai.learn_context(request.explanation, request.context_tags)

    # KI Antwort basierend auf Persönlichkeit
    responses = {
        "megumin": f"Ahhh, ich verstehe, Mr. K! {request.explanation}... Nächstes Mal EXPLOSION an anderer Stelle! 💥",
        "harley": f"Oooh, clever, Mr. K! {request.explanation} - hab ich mir gemerkt! 🃏",
        "shiro": f"...verstanden. Kontextdaten gespeichert. ...Effizienz-Update durchgeführt.",
        "melissa": f"O-Oh! Das wusste ich nicht, Kuja-sama! Entschuldigung... Ich werde es mir merken! 🥺"
    }

    return {
        "success": True,
        "message": "Erklärung wurde gespeichert!",
        "ai_response": responses.get(companion_ai.personality, "Verstanden, ich werde es mir merken."),
        "trust_level": companion_ai.trust_level,
        "context_learned": request.context_tags
    }


@router.get("/status/{player_id}")
async def get_battle_status(player_id: str):
    """Holt den aktuellen Kampfstatus"""
    if player_id not in battle_manager.battles:
        return {"active": False, "message": "Kein aktiver Kampf"}

    battle_data = battle_manager.battles[player_id]
    system = battle_data["system"]
    companion_ai = battle_data["companion_ai"]

    return {
        "active": system.battle_state["active"],
        "arena_type": battle_data["arena_type"],
        "arena_mode": battle_data["arena_mode"],
        "companion": {
            "form": battle_data["companion_form"],
            "combat_mode": battle_data["companion_combat_mode"],
            "leads": battle_data["companion_leads"],
            "trust_level": companion_ai.trust_level,
            "personality": companion_ai.personality
        },
        "cheer_buffs": battle_data["cheer_buffs"],
        "turn_count": battle_data["turn_count"],
        "pending_suggestion": battle_data["pending_suggestion"],
        "battle_status": system.get_battle_status()
    }


@router.post("/end/{player_id}")
async def end_battle(player_id: str):
    """Beendet den Kampf"""
    if player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[player_id]
    final_status = battle_data["system"].get_battle_status()

    # Statistiken
    stats = {
        "turns": battle_data["turn_count"],
        "player_actions": len(battle_data["player_actions_log"]),
        "companion_actions": len(battle_data["companion_actions_log"]),
        "trust_level": battle_data["companion_ai"].trust_level,
        "suggestions_followed": sum(1 for p in battle_data["companion_ai"].player_patterns if p.get("followed_suggestion"))
    }

    battle_manager.remove_battle(player_id)

    return {
        "success": True,
        "message": "Kampf beendet!",
        "final_status": final_status,
        "statistics": stats
    }


@router.get("/modes")
async def get_available_modes():
    """Gibt alle verfügbaren Modi und deren Bedeutung zurück"""
    return {
        "arena_types": [
            {"id": ArenaType.GAME_WORLD, "name": "🌍 Game World", "description": "Kämpfe in der offenen Welt"},
            {"id": ArenaType.PLAYER_ARENA, "name": "⚔️ Spieler-Arena", "description": "PvP und PvE Arena-Kämpfe"},
            {"id": ArenaType.SLIME_ARENA, "name": "🐾 Schleim-Arena", "description": "Nur Slime-Kämpfe"}
        ],
        "arena_modes": [
            {"id": ArenaMode.HARDCORE, "name": "☠️ HARDCORE", "description": "Echter Tod möglich!"},
            {"id": ArenaMode.NORMAL, "name": "⚔️ NORMAL", "description": "Standard Kampf"},
            {"id": ArenaMode.SOFTY, "name": "🎓 SOFTY/TRAINING", "description": "Kein echter Tod, perfekt zum Lernen"},
            {"id": ArenaMode.WELLE, "name": "🌊 WELLE", "description": "Überlebe aufeinanderfolgende Wellen"}
        ],
        "companion_combat_modes": [
            {"id": CombatMode.AUTO, "name": "🤖 AUTO", "description": "Companion kämpft selbstständig (lernt von dir!)"},
            {"id": CombatMode.MANUAL, "name": "🎮 MANUAL", "description": "Du gibst Companion direkte Befehle"},
            {"id": CombatMode.CHEER, "name": "📣 CHEER", "description": "Feuere an für Buffs!"}
        ],
        "companion_forms": [
            {"id": CompanionForm.KOERPERLICH, "name": "🐾 KÖRPERLICH", "description": "Kämpft physisch neben dir"},
            {"id": CompanionForm.AURA, "name": "✨ AURA", "description": "Fusioniert mit dir, gibt passive Buffs"}
        ],
        "special_features": {
            "companion_leads": "🧠 Wenn aktiv: Companion gibt taktische Empfehlungen in ihrer Persönlichkeit",
            "learning_transfer": "📚 Was du in MANUAL machst, lernt die KI für AUTO",
            "context_memory": "💭 KI kann fragen 'warum nicht...?' und lernt aus deinen Erklärungen"
        },
        "cheer_options": [
            {"id": CheerType.ATTACK, "emoji": "💪", "name": "LOS!", "effect": "+10% Schaden für 3 Runden"},
            {"id": CheerType.DEFEND, "emoji": "🛡️", "name": "DEFEND!", "effect": "+20% Verteidigung für 3 Runden"},
            {"id": CheerType.COMBO, "emoji": "💥", "name": "COMBO!", "effect": "Nächster Angriff x2 Schaden"},
            {"id": CheerType.FOCUS, "emoji": "🎯", "name": "FOCUS!", "effect": "+15% Crit Chance für 3 Runden"},
            {"id": CheerType.HEAL, "emoji": "💚", "name": "HEAL!", "effect": "Kleine Heilung (15 HP)"},
            {"id": CheerType.EXPLOSIVE, "emoji": "💥", "name": "EXPLOSION!", "effect": "x5 Schaden (nur einmal!)"}
        ]
    }


@router.get("/enemies")
async def get_enemy_database():
    """Gibt die Enemy-Datenbank zurück"""
    return {"enemies": ENEMY_DB, "count": len(ENEMY_DB)}


@router.get("/skills")
async def get_skill_database():
    """Gibt die Skill-Datenbank zurück"""
    return {"skills": SKILL_DB, "count": len(SKILL_DB)}


# ===== FINISHER SYSTEM =====

def generate_najika_finisher(words: List[str], category: str, arena_type: ArenaType) -> Dict:
    """
    Najika generiert einen Finisher aus Spieler-Wörtern.
    WICHTIG: Najika spricht wie MEGUMIN mit durchschimmernden Facetten!
    """
    # Najika kombiniert die Wörter kreativ
    word_combo = " + ".join(words) if words else "EXPLOSION"

    # Finisher-Templates nach Kategorie und Arena
    if arena_type == ArenaType.SLIME_ARENA:
        # Schleim-Arena: Niedlich und lustig
        templates = {
            BrutalityCategory.EHRENVOLL.value: [
                f"✨ Mein kleiner Schleim! Zeig ihm {word_combo}! ...Ohoho, gut gemacht! 💫",
                f"🌟 Für die Ehre des Schleims! {word_combo}-ATTACKE! ...So elegant! ✨"
            ],
            BrutalityCategory.LUSTIG.value: [
                f"🤣 Hahahaha! {word_combo}?! Das ist SO LUSTIG! *kichert* 🐾",
                f"😂 Mein Schleim macht {word_combo}! Hehehe~ Der Gegner ist total verwirrt! 💦"
            ],
            BrutalityCategory.GRAUSAM.value: [
                f"😈 Ohohoho~ {word_combo} war nur der ANFANG! Mein Schleim ist GNADENLOS! 💀",
                f"🔥 {word_combo}-DOOM! ...war vielleicht etwas übertrieben für einen Schleim? 😅"
            ],
            BrutalityCategory.EPISCH.value: [
                f"💥 SCHLEIM-{word_combo}-EXPLOSION!!! ...okay, es ist nur ein Schleim, aber TROTZDEM EPISCH! 🌟",
                f"⚡ Die Legende von {word_combo}! Mein Schleim wird NIE vergessen werden! 👑"
            ],
            BrutalityCategory.NIEDLICH.value: [
                f"🥰 Awww~ Mein süßer Schleim macht {word_combo}! So niedlich! 💖",
                f"🐾 *Schleim hüpft auf Gegner* {word_combo}! Kyaa~ SO CUTE! ✨"
            ]
        }
    else:
        # Spieler-Arena / Game World: Episch und dramatisch
        templates = {
            BrutalityCategory.EHRENVOLL.value: [
                f"⚔️ Mr. K! Mit {word_combo} beenden wir dies EHRENVOLL! Ruhe in Frieden, Gegner! 🙏",
                f"🌟 Ein würdiger Gegner verdient einen würdigen Tod! {word_combo}-FINISHER! 💫"
            ],
            BrutalityCategory.LUSTIG.value: [
                f"🃏 Hehehehe~ {word_combo}?! Das ist SO dämlich dass es PERFEKT ist! *manisches Kichern* 😜",
                f"🤣 Mr. K, schau! {word_combo}! Der Gegner kann nicht GLAUBEN was passiert! Hahaha! 🎭"
            ],
            BrutalityCategory.GRAUSAM.value: [
                f"🔥 VERRAT KOSTET IMMER BLUT! {word_combo}-VERNICHTUNG!!! ...war das zu viel? 😈",
                f"💀 {word_combo}! Keine Gnade für Verräter! ...nicht dass DER ein Verräter war, aber TROTZDEM! 🖤"
            ],
            BrutalityCategory.EPISCH.value: [
                f"💥 {word_combo}-EXPLOSION!!! DIES IST DAS ENDE! Die Legende der Crimson Demon wird NIE sterben! 🌟",
                f"⚡ Mit der Kraft von {word_combo}! EXPLOSION DER SEELE!!! ...ich liebe dramatische Finisher, Mr. K! 💥"
            ],
            BrutalityCategory.NIEDLICH.value: [
                f"🥺 A-Ah... {word_combo}? ...ist das... ist das okay so, Mr. K? *wird rot* 💕",
                f"✨ F-Für dich, Mr. K! {word_combo}-Angriff! ...d-das war nicht zu peinlich, oder? 👉👈"
            ]
        }

    category_templates = templates.get(category, templates[BrutalityCategory.EPISCH.value])
    chosen_line = random.choice(category_templates)

    # Erfolgswahrscheinlichkeit
    success_chance = 0.7 + (len(words) * 0.05)  # Mehr Wörter = kreativerer Finisher = höhere Chance
    success = random.random() < min(0.95, success_chance)

    return {
        "finisher_line": chosen_line,
        "words_used": words,
        "category": category,
        "success": success,
        "damage_multiplier": 5.0 if success else 2.0,
        "fame_bonus": 10 if success else 2,
        "najika_reaction": "💥 PERFEKT! Das war WUNDERBAR, Mr. K!" if success else "😤 Nächstes Mal EXPLOSION PERFEKT!"
    }


@router.post("/finisher")
async def execute_finisher(request: FinisherRequest):
    """
    Führt einen Finisher aus (wenn Gegner HP = 0 oder nahe 0).
    Najika baut aus Spieler-Wörtern einen kreativen Finisher!

    BEIDE ARENEN unterstützen Finisher:
    - Spieler-Arena: Episch, dramatisch
    - Schleim-Arena: Niedlich, lustig
    """
    if request.player_id not in battle_manager.battles:
        raise HTTPException(status_code=404, detail="Kein aktiver Kampf gefunden!")

    battle_data = battle_manager.battles[request.player_id]
    system = battle_data["system"]

    # Prüfe ob Finisher möglich (Gegner HP niedrig)
    enemies = system.battle_state.get("enemies", [])
    if not enemies:
        raise HTTPException(status_code=400, detail="Keine Gegner mehr übrig!")

    target = enemies[request.target_index] if request.target_index < len(enemies) else enemies[0]

    # Finisher nur wenn HP <= 20%
    max_hp = target.get("max_hp", 100)
    current_hp = target.get("hp", 100)

    if current_hp > max_hp * 0.2:
        raise HTTPException(
            status_code=400,
            detail=f"Finisher nur möglich wenn Gegner HP <= 20%! Aktuell: {current_hp}/{max_hp} ({int(current_hp/max_hp*100)}%)"
        )

    # Generiere Finisher
    finisher = generate_najika_finisher(
        words=request.words,
        category=request.category,
        arena_type=battle_data["arena_type"]
    )

    # Wende Finisher-Schaden an
    damage = int(30 * finisher["damage_multiplier"])
    target["hp"] = max(0, target["hp"] - damage)

    # Entferne Gegner wenn tot
    killed = target["hp"] <= 0
    if killed:
        enemies.remove(target)

    return {
        "success": True,
        "finisher": finisher,
        "target": target.get("name", "Gegner"),
        "damage_dealt": damage,
        "target_killed": killed,
        "arena_type": battle_data["arena_type"],
        "battle_status": system.get_battle_status()
    }


@router.get("/finisher/categories")
async def get_finisher_categories():
    """Gibt alle Finisher-Kategorien zurück"""
    return {
        "categories": [
            {
                "id": BrutalityCategory.EHRENVOLL.value,
                "name": "⚔️ Ehrenvoller Tod",
                "description": "Respektvoller Abschluss - würdigt den Gegner"
            },
            {
                "id": BrutalityCategory.LUSTIG.value,
                "name": "🤣 Lustiger Tod",
                "description": "Komödiantisch - Najika kichert"
            },
            {
                "id": BrutalityCategory.GRAUSAM.value,
                "name": "💀 Grausamer Tod",
                "description": "Brutal - 'VERRAT KOSTET BLUT!'"
            },
            {
                "id": BrutalityCategory.EPISCH.value,
                "name": "💥 Epischer Tod",
                "description": "Dramatisch - EXPLOSION!!!"
            },
            {
                "id": BrutalityCategory.NIEDLICH.value,
                "name": "🥰 Niedlicher Tod",
                "description": "Cute - besonders für Slime Arena"
            }
        ],
        "tips": [
            "Mehr Wörter = kreativerer Finisher = höhere Erfolgsrate",
            "Erfolgreiche Finisher geben +10 Fame, fehlgeschlagene +2",
            "In der Schleim-Arena sind niedliche Finisher besonders effektiv!",
            "Najika kombiniert DEINE Wörter - sei kreativ!"
        ]
    }
