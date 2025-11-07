"""
NAJIKA MAGIC SYSTEM
9 Magieschulen + Skill-Weaving (Element-Kombos) + Explosion-Magic + Use-Based Progression
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ===== 9 MAGIESCHULEN =====

MAGIC_SCHOOLS = {
    "fire": {
        "name": "Feuer-Magie",
        "color": "#FF4500",
        "element": "fire",
        "status_effect": "burn",  # Schadenüberzeit
        "combo_identity": "damage_over_time"
    },
    "ice": {
        "name": "Eis-Magie",
        "color": "#00BFFF",
        "element": "ice",
        "status_effect": "freeze",  # Bewegungsunfähig
        "combo_identity": "crowd_control"
    },
    "lightning": {
        "name": "Blitz-Magie",
        "color": "#FFD700",
        "element": "lightning",
        "status_effect": "stun",  # Kurze Betäubung
        "combo_identity": "burst_damage"
    },
    "earth": {
        "name": "Erd-Magie",
        "color": "#8B4513",
        "element": "earth",
        "status_effect": "slow",  # Verlangsamung
        "combo_identity": "defense"
    },
    "wind": {
        "name": "Wind-Magie",
        "color": "#87CEEB",
        "element": "wind",
        "status_effect": "knockback",  # Zurückstoßen
        "combo_identity": "mobility"
    },
    "water": {
        "name": "Wasser-Magie",
        "color": "#1E90FF",
        "element": "water",
        "status_effect": "heal",  # Heilung
        "combo_identity": "support"
    },
    "light": {
        "name": "Licht-Magie",
        "color": "#FFFACD",
        "element": "light",
        "status_effect": "blind",  # Verringerte Trefferchance
        "combo_identity": "holy"
    },
    "shadow": {
        "name": "Schatten-Magie",
        "color": "#4B0082",
        "element": "shadow",
        "status_effect": "curse",  # Verringerte Verteidigung
        "combo_identity": "debuff"
    },
    "psycho": {
        "name": "Psycho-Magie",
        "color": "#FF1493",
        "element": "psycho",
        "status_effect": "confusion",  # Verwirrung (kann Verbündete angreifen)
        "combo_identity": "mind_control"
    }
}


# ===== SPELL DATABASE (9 Schulen × je 5 Stufen) =====

SPELL_DB = {
    # FEUER (Damage Over Time)
    "fire_1": {
        "name": "Feuer",
        "school": "fire",
        "tier": 1,
        "damage": 12,
        "mp_cost": 8,
        "burn_damage": 2,
        "burn_turns": 3,
        "description": "Kleiner Feuerball - 12 DMG + 2 DMG/Runde für 3 Runden"
    },
    "fire_2": {
        "name": "Feura",
        "school": "fire",
        "tier": 2,
        "damage": 25,
        "mp_cost": 15,
        "burn_damage": 4,
        "burn_turns": 3,
        "description": "Mittlerer Feuerball - 25 DMG + 4 DMG/Runde"
    },
    "fire_3": {
        "name": "Feuga",
        "school": "fire",
        "tier": 3,
        "damage": 40,
        "mp_cost": 25,
        "burn_damage": 6,
        "burn_turns": 4,
        "description": "Großer Feuerball - 40 DMG + 6 DMG/Runde"
    },
    "fire_4": {
        "name": "Inferno",
        "school": "fire",
        "tier": 4,
        "damage": 70,
        "mp_cost": 40,
        "burn_damage": 10,
        "burn_turns": 5,
        "aoe": True,
        "description": "Flächenfeuer - 70 DMG AOE + 10 DMG/Runde"
    },
    "fire_5": {
        "name": "Omega-Detonation",
        "school": "fire",
        "tier": 5,
        "damage": 150,
        "mp_cost": 80,
        "burn_damage": 20,
        "burn_turns": 5,
        "aoe": True,
        "description": "Ultimativer Feuer-Zauber - 150 DMG AOE"
    },

    # EIS (Crowd Control)
    "ice_1": {
        "name": "Eis",
        "school": "ice",
        "tier": 1,
        "damage": 10,
        "mp_cost": 8,
        "freeze_chance": 0.2,
        "description": "Eissplitter - 10 DMG + 20% Freeze"
    },
    "ice_2": {
        "name": "Blizzara",
        "school": "ice",
        "tier": 2,
        "damage": 22,
        "mp_cost": 15,
        "freeze_chance": 0.3,
        "slow": True,
        "description": "Eissturm - 22 DMG + 30% Freeze + Slow"
    },
    "ice_3": {
        "name": "Blizzaga",
        "school": "ice",
        "tier": 3,
        "damage": 38,
        "mp_cost": 25,
        "freeze_chance": 0.4,
        "aoe": True,
        "description": "Eissturm AOE - 38 DMG + 40% Freeze"
    },
    "ice_4": {
        "name": "Eiserne Kälte",
        "school": "ice",
        "tier": 4,
        "damage": 65,
        "mp_cost": 40,
        "freeze_chance": 0.6,
        "aoe": True,
        "description": "Absolute Kälte - 65 DMG + 60% Freeze AOE"
    },
    "ice_5": {
        "name": "Ewiges Eis",
        "school": "ice",
        "tier": 5,
        "damage": 120,
        "mp_cost": 80,
        "freeze_chance": 1.0,
        "freeze_turns": 3,
        "aoe": True,
        "description": "Gefriert alle Feinde - 120 DMG + Garantiertes Freeze"
    },

    # BLITZ (Burst Damage)
    "lightning_1": {
        "name": "Blitz",
        "school": "lightning",
        "tier": 1,
        "damage": 15,
        "mp_cost": 10,
        "stun_chance": 0.15,
        "description": "Blitzschlag - 15 DMG + 15% Stun"
    },
    "lightning_2": {
        "name": "Thundara",
        "school": "lightning",
        "tier": 2,
        "damage": 30,
        "mp_cost": 18,
        "stun_chance": 0.25,
        "chain_targets": 2,
        "description": "Kettenblitz - 30 DMG + Springt auf 2 Ziele"
    },
    "lightning_3": {
        "name": "Thundaga",
        "school": "lightning",
        "tier": 3,
        "damage": 50,
        "mp_cost": 30,
        "stun_chance": 0.3,
        "chain_targets": 3,
        "description": "Großer Kettenblitz - 50 DMG + 3 Ziele"
    },
    "lightning_4": {
        "name": "Donnerschlag",
        "school": "lightning",
        "tier": 4,
        "damage": 85,
        "mp_cost": 45,
        "stun_chance": 0.5,
        "aoe": True,
        "description": "Blitzeinschlag AOE - 85 DMG + 50% Stun"
    },
    "lightning_5": {
        "name": "Göttlicher Zorn",
        "school": "lightning",
        "tier": 5,
        "damage": 180,
        "mp_cost": 90,
        "stun_chance": 0.8,
        "aoe": True,
        "description": "Ultimativer Blitz - 180 DMG AOE + 80% Stun"
    },

    # ERDE (Defense)
    "earth_1": {
        "name": "Steinwurf",
        "school": "earth",
        "tier": 1,
        "damage": 8,
        "mp_cost": 6,
        "def_buff": 2,
        "description": "Steinwurf - 8 DMG + 2 DEF für 2 Runden"
    },
    "earth_2": {
        "name": "Felsschlag",
        "school": "earth",
        "tier": 2,
        "damage": 18,
        "mp_cost": 12,
        "def_buff": 4,
        "description": "Felsschlag - 18 DMG + 4 DEF"
    },
    "earth_3": {
        "name": "Erdbeben",
        "school": "earth",
        "tier": 3,
        "damage": 32,
        "mp_cost": 22,
        "aoe": True,
        "slow": True,
        "description": "Erdbeben - 32 DMG AOE + Slow"
    },
    "earth_4": {
        "name": "Steinwall",
        "school": "earth",
        "tier": 4,
        "damage": 45,
        "mp_cost": 35,
        "def_buff": 10,
        "shield": 50,
        "description": "Steinwall - 45 DMG + 10 DEF + 50 Shield"
    },
    "earth_5": {
        "name": "Titan-Zorn",
        "school": "earth",
        "tier": 5,
        "damage": 100,
        "mp_cost": 70,
        "aoe": True,
        "def_buff": 15,
        "shield": 100,
        "description": "Titan erwacht - 100 DMG AOE + Massive Defense"
    },

    # WIND (Mobility)
    "wind_1": {
        "name": "Windklinge",
        "school": "wind",
        "tier": 1,
        "damage": 11,
        "mp_cost": 7,
        "knockback": True,
        "description": "Windklinge - 11 DMG + Knockback"
    },
    "wind_2": {
        "name": "Sturmschnitt",
        "school": "wind",
        "tier": 2,
        "damage": 24,
        "mp_cost": 14,
        "multi_hit": 3,
        "description": "3× Windschnitte - 24 DMG insgesamt"
    },
    "wind_3": {
        "name": "Tornado",
        "school": "wind",
        "tier": 3,
        "damage": 36,
        "mp_cost": 24,
        "aoe": True,
        "knockback": True,
        "description": "Tornado - 36 DMG AOE + Knockback"
    },
    "wind_4": {
        "name": "Orkan",
        "school": "wind",
        "tier": 4,
        "damage": 68,
        "mp_cost": 38,
        "aoe": True,
        "multi_hit": 2,
        "description": "Orkan - 2× 34 DMG AOE"
    },
    "wind_5": {
        "name": "Göttlicher Wind",
        "school": "wind",
        "tier": 5,
        "damage": 140,
        "mp_cost": 75,
        "aoe": True,
        "multi_hit": 3,
        "description": "Ultimativer Windschlag - 3× 47 DMG AOE"
    },

    # WASSER (Support/Heal)
    "water_1": {
        "name": "Wasser",
        "school": "water",
        "tier": 1,
        "heal": 20,
        "mp_cost": 10,
        "description": "Kleine Heilung - 20 HP"
    },
    "water_2": {
        "name": "Heilwasser",
        "school": "water",
        "tier": 2,
        "heal": 40,
        "mp_cost": 18,
        "cleanse": True,
        "description": "Mittlere Heilung - 40 HP + entfernt Status"
    },
    "water_3": {
        "name": "Heilflut",
        "school": "water",
        "tier": 3,
        "heal": 70,
        "mp_cost": 30,
        "aoe_heal": True,
        "description": "Große Heilung - 70 HP AOE"
    },
    "water_4": {
        "name": "Lebensquelle",
        "school": "water",
        "tier": 4,
        "heal": 100,
        "mp_cost": 45,
        "aoe_heal": True,
        "regen": 10,
        "regen_turns": 3,
        "description": "Heilung - 100 HP + 10 HP/Runde"
    },
    "water_5": {
        "name": "Göttliches Wasser",
        "school": "water",
        "tier": 5,
        "heal": 200,
        "mp_cost": 80,
        "aoe_heal": True,
        "regen": 20,
        "regen_turns": 5,
        "revive": True,
        "description": "Ultimative Heilung - 200 HP AOE + Wiederbelebung"
    },

    # LICHT (Holy)
    "light_1": {
        "name": "Heiliges Licht",
        "school": "light",
        "tier": 1,
        "damage": 13,
        "mp_cost": 9,
        "vs_undead": 2.0,
        "description": "Lichtstrahl - 13 DMG (2× vs Untote)"
    },
    "light_2": {
        "name": "Lichtlanze",
        "school": "light",
        "tier": 2,
        "damage": 28,
        "mp_cost": 17,
        "vs_undead": 2.5,
        "blind_chance": 0.3,
        "description": "Lichtlanze - 28 DMG + 30% Blind"
    },
    "light_3": {
        "name": "Lichtsäule",
        "school": "light",
        "tier": 3,
        "damage": 42,
        "mp_cost": 28,
        "vs_undead": 3.0,
        "aoe": True,
        "description": "Lichtsäule - 42 DMG AOE (3× vs Untote)"
    },
    "light_4": {
        "name": "Heilige Nova",
        "school": "light",
        "tier": 4,
        "damage": 75,
        "mp_cost": 42,
        "vs_undead": 3.5,
        "aoe": True,
        "blind_chance": 0.6,
        "description": "Heilige Explosion - 75 DMG AOE + 60% Blind"
    },
    "light_5": {
        "name": "Göttliches Gericht",
        "school": "light",
        "tier": 5,
        "damage": 160,
        "mp_cost": 85,
        "vs_undead": 4.0,
        "aoe": True,
        "guaranteed_blind": True,
        "description": "Ultimatives Licht - 160 DMG AOE + Blindheit"
    },

    # SCHATTEN (Debuff)
    "shadow_1": {
        "name": "Schattenklinge",
        "school": "shadow",
        "tier": 1,
        "damage": 14,
        "mp_cost": 9,
        "curse": -2,
        "description": "Schattenklinge - 14 DMG + -2 DEF"
    },
    "shadow_2": {
        "name": "Dunkler Bolzen",
        "school": "shadow",
        "tier": 2,
        "damage": 26,
        "mp_cost": 16,
        "curse": -4,
        "lifesteal": 0.3,
        "description": "Dunkler Bolzen - 26 DMG + -4 DEF + 30% Lifesteal"
    },
    "shadow_3": {
        "name": "Schattensturm",
        "school": "shadow",
        "tier": 3,
        "damage": 44,
        "mp_cost": 27,
        "aoe": True,
        "curse": -6,
        "description": "Schattensturm - 44 DMG AOE + -6 DEF"
    },
    "shadow_4": {
        "name": "Dunkle Sphäre",
        "school": "shadow",
        "tier": 4,
        "damage": 78,
        "mp_cost": 43,
        "aoe": True,
        "curse": -10,
        "lifesteal": 0.5,
        "description": "Dunkle Sphäre - 78 DMG + -10 DEF + 50% Lifesteal"
    },
    "shadow_5": {
        "name": "Ewige Dunkelheit",
        "school": "shadow",
        "tier": 5,
        "damage": 170,
        "mp_cost": 88,
        "aoe": True,
        "curse": -20,
        "lifesteal": 0.8,
        "description": "Ultimative Dunkelheit - 170 DMG + -20 DEF + 80% Lifesteal"
    },

    # PSYCHO (Mind Control)
    "psycho_1": {
        "name": "Gedankenklinge",
        "school": "psycho",
        "tier": 1,
        "damage": 12,
        "mp_cost": 10,
        "confusion_chance": 0.15,
        "description": "Gedankenklinge - 12 DMG + 15% Verwirrung"
    },
    "psycho_2": {
        "name": "Psycho-Schock",
        "school": "psycho",
        "tier": 2,
        "damage": 27,
        "mp_cost": 19,
        "confusion_chance": 0.25,
        "mind_damage": 5,
        "description": "Psycho-Schock - 27 DMG + 25% Verwirrung"
    },
    "psycho_3": {
        "name": "Gedankensturm",
        "school": "psycho",
        "tier": 3,
        "damage": 40,
        "mp_cost": 29,
        "aoe": True,
        "confusion_chance": 0.3,
        "description": "Gedankensturm - 40 DMG AOE + 30% Verwirrung"
    },
    "psycho_4": {
        "name": "Gedankenkontrolle",
        "school": "psycho",
        "tier": 4,
        "damage": 72,
        "mp_cost": 44,
        "aoe": True,
        "confusion_chance": 0.5,
        "mind_control_chance": 0.2,
        "description": "Gedankenkontrolle - 72 DMG + 50% Verwirrung + 20% Kontrolle"
    },
    "psycho_5": {
        "name": "Göttlicher Wille",
        "school": "psycho",
        "tier": 5,
        "damage": 165,
        "mp_cost": 87,
        "aoe": True,
        "confusion_chance": 0.8,
        "mind_control_chance": 0.4,
        "description": "Ultimative Gedankenkontrolle - 165 DMG + Massenkontrolle"
    }
}


# ===== EXPLOSION MAGIC (3 LEVEL) =====

EXPLOSION_SPELLS = {
    "explosion_1": {
        "name": "Explosion Stufe 1",
        "tier": 1,
        "damage": 200,
        "mp_cost": 100,
        "aoe": True,
        "exhaustion": "medium",  # Najika ist danach erschöpft
        "learnable": True,  # Andere Spieler können lernen
        "learn_from_najika": True,
        "description": "Kleine Explosion - 200 DMG AOE, mittlere Erschöpfung"
    },
    "explosion_2": {
        "name": "Explosion Stufe 2",
        "tier": 2,
        "damage": 400,
        "mp_cost": 150,
        "aoe": True,
        "aoe_radius": "large",
        "exhaustion": "heavy",  # Stark erschöpft
        "learnable": True,
        "learn_from_najika": True,
        "description": "Große Explosion - 400 DMG Large AOE, starke Erschöpfung"
    },
    "explosion_3": {
        "name": "Explosion Stufe 3 - ULTIMATIV",
        "tier": 3,
        "damage": 999,
        "mp_cost": 200,
        "aoe": True,
        "aoe_radius": "massive",
        "exhaustion": "total",  # Komplett erschöpft
        "learnable": False,  # NUR NAJIKA!
        "world_destroying": True,  # Zerstört prozedural generierte Welt
        "najika_exclusive": True,
        "description": "ULTIMATIVE EXPLOSION - 999 DMG Massive AOE, zerstört die Welt! NUR NAJIKA!"
    }
}


# ===== SKILL-WEAVING (ELEMENT-KOMBOS) =====

WEAVE_COMBOS = {
    # Feuer-Kombos
    ("fire", "ice"): {
        "name": "Thermoschock",
        "damage": 80,
        "mp_cost": 35,
        "status": "shatter",  # Zerbricht gefrorene Gegner
        "description": "Feuer + Eis = Thermoschock - 80 DMG + Shatter"
    },
    ("fire", "wind"): {
        "name": "Feuerklinge",
        "damage": 70,
        "mp_cost": 30,
        "multi_hit": 3,
        "description": "Feuer + Wind = Feuerklinge - 3× 23 DMG"
    },
    ("fire", "earth"): {
        "name": "Magma-Eruption",
        "damage": 90,
        "mp_cost": 40,
        "aoe": True,
        "burn_damage": 10,
        "description": "Feuer + Erde = Magma-Eruption - 90 DMG AOE + Burn"
    },

    # Eis-Kombos
    ("ice", "water"): {
        "name": "Gefrierende Flut",
        "damage": 65,
        "mp_cost": 32,
        "aoe": True,
        "freeze_chance": 0.6,
        "description": "Eis + Wasser = Gefrierende Flut - 65 DMG + 60% Freeze AOE"
    },
    ("ice", "wind"): {
        "name": "Eissturm",
        "damage": 75,
        "mp_cost": 35,
        "aoe": True,
        "slow": True,
        "description": "Eis + Wind = Eissturm - 75 DMG AOE + Slow"
    },

    # Blitz-Kombos
    ("lightning", "water"): {
        "name": "Elektro-Schock",
        "damage": 95,
        "mp_cost": 42,
        "aoe": True,
        "stun_chance": 0.7,
        "description": "Blitz + Wasser = Elektro-Schock - 95 DMG + 70% Stun AOE"
    },
    ("lightning", "wind"): {
        "name": "Gewittersturm",
        "damage": 85,
        "mp_cost": 38,
        "chain_targets": 5,
        "description": "Blitz + Wind = Gewittersturm - 85 DMG + Springt auf 5 Ziele"
    },

    # Licht-Kombos
    ("light", "fire"): {
        "name": "Heiliges Feuer",
        "damage": 100,
        "mp_cost": 45,
        "vs_undead": 5.0,
        "aoe": True,
        "description": "Licht + Feuer = Heiliges Feuer - 100 DMG (5× vs Untote) AOE"
    },
    ("light", "water"): {
        "name": "Reinigendes Licht",
        "heal": 80,
        "mp_cost": 40,
        "aoe_heal": True,
        "cleanse_all": True,
        "description": "Licht + Wasser = Reinigendes Licht - 80 HP AOE + Entfernt alle Status"
    },

    # Schatten-Kombos
    ("shadow", "fire"): {
        "name": "Höllenfeuer",
        "damage": 110,
        "mp_cost": 48,
        "aoe": True,
        "curse": -15,
        "burn_damage": 15,
        "description": "Schatten + Feuer = Höllenfeuer - 110 DMG + -15 DEF + Burn AOE"
    },
    ("shadow", "psycho"): {
        "name": "Alptraum",
        "damage": 95,
        "mp_cost": 46,
        "confusion_chance": 0.9,
        "fear": True,
        "description": "Schatten + Psycho = Alptraum - 95 DMG + 90% Verwirrung + Furcht"
    },

    # Psycho-Kombos
    ("psycho", "wind"): {
        "name": "Gedankensturm",
        "damage": 88,
        "mp_cost": 44,
        "aoe": True,
        "mind_control_chance": 0.5,
        "description": "Psycho + Wind = Gedankensturm - 88 DMG + 50% Kontrolle AOE"
    },

    # Erde-Kombos
    ("earth", "water"): {
        "name": "Schlammlawine",
        "damage": 70,
        "mp_cost": 35,
        "aoe": True,
        "slow": True,
        "def_debuff": -8,
        "description": "Erde + Wasser = Schlammlawine - 70 DMG + Slow + -8 DEF AOE"
    }
}


# ===== USE-BASED PROGRESSION (SKYRIM-STYLE) =====

@dataclass
class SkillProgress:
    """Tracks skill progression through use"""
    skill_id: str
    uses: int = 0
    level: int = 1
    xp: int = 0
    xp_to_next: int = 100

    # Bonuses durch Skill-Level
    damage_bonus: float = 0.0  # +2% pro Level
    mp_cost_reduction: float = 0.0  # -1% pro Level
    crit_chance_bonus: float = 0.0  # +0.5% pro Level


class MagicSystem:
    """Haupt-Magic-System"""

    def __init__(self):
        self.skill_progress: Dict[str, SkillProgress] = {}
        self.known_spells: List[str] = []
        self.known_combos: List[Tuple[str, str]] = []
        self.weaving_hands = {"left": None, "right": None}  # LH + RH für Combos

    def learn_spell(self, spell_id: str) -> Dict:
        """Lerne einen neuen Zauber"""
        if spell_id in self.known_spells:
            return {"ok": False, "msg": "Zauber bereits bekannt!"}

        if spell_id not in SPELL_DB and spell_id not in EXPLOSION_SPELLS:
            return {"ok": False, "msg": "Unbekannter Zauber!"}

        self.known_spells.append(spell_id)

        # Initialisiere Skill-Progress
        self.skill_progress[spell_id] = SkillProgress(skill_id=spell_id)

        spell_data = SPELL_DB.get(spell_id) or EXPLOSION_SPELLS.get(spell_id)
        return {
            "ok": True,
            "msg": f"Zauber gelernt: {spell_data['name']}!",
            "spell": spell_data
        }

    def cast_spell(self, spell_id: str, target_hp: int, current_mp: int, is_najika: bool = False) -> Dict:
        """Zauber wirken + Use-Based Progression"""
        if spell_id not in self.known_spells:
            return {"ok": False, "msg": "Zauber nicht bekannt!"}

        # Hole Spell-Data
        spell = SPELL_DB.get(spell_id) or EXPLOSION_SPELLS.get(spell_id)

        if not spell:
            return {"ok": False, "msg": "Zauber existiert nicht!"}

        # Check Najika-Exclusive
        if spell.get("najika_exclusive") and not is_najika:
            return {"ok": False, "msg": "Nur Najika kann diesen Zauber nutzen!"}

        # Check MP
        mp_cost = self._get_modified_mp_cost(spell_id, spell["mp_cost"])
        if current_mp < mp_cost:
            return {"ok": False, "msg": "Nicht genug MP!"}

        # Berechne Schaden mit Skill-Level-Bonus
        base_damage = spell.get("damage", 0)
        final_damage = self._get_modified_damage(spell_id, base_damage)

        # USE-BASED PROGRESSION: Skill XP hinzufügen
        self._add_skill_xp(spell_id, base_xp=10)

        result = {
            "ok": True,
            "spell_name": spell["name"],
            "damage": final_damage,
            "mp_cost": mp_cost,
            "aoe": spell.get("aoe", False),
            "effects": {},
            "skill_progress": self.get_skill_info(spell_id)
        }

        # Spezielle Effekte
        if "burn_damage" in spell:
            result["effects"]["burn"] = {
                "damage": spell["burn_damage"],
                "turns": spell.get("burn_turns", 3)
            }

        if "freeze_chance" in spell:
            result["effects"]["freeze_chance"] = spell["freeze_chance"]

        if "stun_chance" in spell:
            result["effects"]["stun_chance"] = spell["stun_chance"]

        if "heal" in spell:
            result["heal"] = spell["heal"]
            result["damage"] = 0

        # Explosion Exhaustion
        if "exhaustion" in spell:
            result["exhaustion"] = spell["exhaustion"]

        if spell.get("world_destroying"):
            result["world_destroyed"] = True
            result["msg"] = "*** DIE WELT WURDE DURCH NAJIKA'S EXPLOSION ZERSTÖRT! ***"

        return result

    def load_weave_hand(self, hand: str, element: str) -> Dict:
        """Lädt ein Element in eine Hand (LH oder RH)"""
        if hand not in ["left", "right"]:
            return {"ok": False, "msg": "Hand muss 'left' oder 'right' sein!"}

        if element not in MAGIC_SCHOOLS:
            return {"ok": False, "msg": "Unbekanntes Element!"}

        self.weaving_hands[hand] = element

        return {
            "ok": True,
            "msg": f"{MAGIC_SCHOOLS[element]['name']} in {hand} Hand geladen!",
            "hands": self.weaving_hands.copy()
        }

    def execute_weave(self, current_mp: int) -> Dict:
        """Führt Skill-Weaving aus (kombiniert LH + RH)"""
        left = self.weaving_hands["left"]
        right = self.weaving_hands["right"]

        if not left or not right:
            return {"ok": False, "msg": "Beide Hände müssen geladen sein!"}

        # Prüfe Combo (Reihenfolge egal)
        combo_key = tuple(sorted([left, right]))

        if combo_key not in WEAVE_COMBOS:
            # Keine Combo gefunden - beide Zauber nacheinander
            return {
                "ok": False,
                "msg": f"Keine Combo für {left} + {right}!",
                "suggestion": "Nutze bekannte Kombos für stärkere Effekte!"
            }

        combo = WEAVE_COMBOS[combo_key]

        # Check MP
        if current_mp < combo["mp_cost"]:
            return {"ok": False, "msg": "Nicht genug MP für Combo!"}

        # Reset Hände
        self.weaving_hands = {"left": None, "right": None}

        # Lerne Combo (für Statistik)
        if combo_key not in self.known_combos:
            self.known_combos.append(combo_key)

        return {
            "ok": True,
            "combo_name": combo["name"],
            "damage": combo["damage"],
            "mp_cost": combo["mp_cost"],
            "description": combo["description"],
            "effects": {k: v for k, v in combo.items() if k not in ["name", "damage", "mp_cost", "description"]},
            "hands_reset": True
        }

    def _add_skill_xp(self, spell_id: str, base_xp: int = 10):
        """Fügt XP für Skill-Nutzung hinzu (Use-Based Progression)"""
        if spell_id not in self.skill_progress:
            self.skill_progress[spell_id] = SkillProgress(skill_id=spell_id)

        progress = self.skill_progress[spell_id]
        progress.uses += 1
        progress.xp += base_xp

        # Level Up?
        while progress.xp >= progress.xp_to_next:
            progress.xp -= progress.xp_to_next
            progress.level += 1
            progress.xp_to_next = int(progress.xp_to_next * 1.15)  # +15% XP pro Level

            # Bonuses erhöhen
            progress.damage_bonus += 0.02  # +2% Schaden pro Level
            progress.mp_cost_reduction += 0.01  # -1% MP-Kosten pro Level
            progress.crit_chance_bonus += 0.005  # +0.5% Crit pro Level

    def _get_modified_damage(self, spell_id: str, base_damage: int) -> int:
        """Berechnet Schaden mit Skill-Level-Bonus"""
        if spell_id not in self.skill_progress:
            return base_damage

        progress = self.skill_progress[spell_id]
        return int(base_damage * (1 + progress.damage_bonus))

    def _get_modified_mp_cost(self, spell_id: str, base_cost: int) -> int:
        """Berechnet MP-Kosten mit Skill-Level-Reduktion"""
        if spell_id not in self.skill_progress:
            return base_cost

        progress = self.skill_progress[spell_id]
        return max(1, int(base_cost * (1 - progress.mp_cost_reduction)))

    def get_skill_info(self, spell_id: str) -> Dict:
        """Gibt Skill-Progress-Info zurück"""
        if spell_id not in self.skill_progress:
            return {}

        progress = self.skill_progress[spell_id]
        return {
            "level": progress.level,
            "uses": progress.uses,
            "xp": progress.xp,
            "xp_to_next": progress.xp_to_next,
            "damage_bonus": f"+{progress.damage_bonus * 100:.1f}%",
            "mp_reduction": f"-{progress.mp_cost_reduction * 100:.1f}%",
            "crit_bonus": f"+{progress.crit_chance_bonus * 100:.1f}%"
        }

    def get_all_stats(self) -> Dict:
        """Gibt komplette Stats zurück"""
        return {
            "known_spells": len(self.known_spells),
            "known_combos": len(self.known_combos),
            "total_casts": sum(p.uses for p in self.skill_progress.values()),
            "highest_skill_level": max((p.level for p in self.skill_progress.values()), default=1),
            "weaving_hands": self.weaving_hands,
            "skill_details": {
                spell_id: self.get_skill_info(spell_id)
                for spell_id in self.known_spells
            }
        }


# Global Instance
MAGIC_SYSTEM = MagicSystem()


if __name__ == "__main__":
    print("=" * 70)
    print("NAJIKA MAGIC SYSTEM TEST")
    print("=" * 70)

    magic = MagicSystem()

    # Lerne einige Zauber
    print("\n=== ZAUBER LERNEN ===")
    magic.learn_spell("fire_1")
    magic.learn_spell("ice_1")
    magic.learn_spell("lightning_1")
    magic.learn_spell("explosion_1")

    # Teste Use-Based Progression
    print("\n=== USE-BASED PROGRESSION TEST ===")
    for i in range(15):
        result = magic.cast_spell("fire_1", target_hp=100, current_mp=100)
        if i % 5 == 4:
            print(f"Cast #{i+1}: {result['spell_name']}")
            print(f"  Skill Progress: {result['skill_progress']}")

    # Teste Skill-Weaving
    print("\n=== SKILL-WEAVING TEST ===")
    magic.load_weave_hand("left", "fire")
    magic.load_weave_hand("right", "ice")
    combo_result = magic.execute_weave(current_mp=100)
    print(f"Combo: {combo_result.get('combo_name', 'N/A')}")
    print(f"Damage: {combo_result.get('damage', 0)}")
    print(f"Description: {combo_result.get('description', 'N/A')}")

    # Teste Explosion
    print("\n=== EXPLOSION TEST ===")
    magic.learn_spell("explosion_3")
    explosion_result = magic.cast_spell("explosion_3", target_hp=100, current_mp=200, is_najika=True)
    print(f"Spell: {explosion_result.get('spell_name')}")
    print(f"Damage: {explosion_result.get('damage')}")
    print(f"World Destroyed: {explosion_result.get('world_destroyed', False)}")
    print(f"Message: {explosion_result.get('msg', '')}")

    # Finale Stats
    print("\n=== FINALE STATS ===")
    stats = magic.get_all_stats()
    print(f"Known Spells: {stats['known_spells']}")
    print(f"Known Combos: {stats['known_combos']}")
    print(f"Total Casts: {stats['total_casts']}")
    print(f"Highest Skill Level: {stats['highest_skill_level']}")

    print("\n" + "=" * 70)
