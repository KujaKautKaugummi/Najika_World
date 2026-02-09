"""
NAJIKA SLIME SPEZIALISIERUNGS-SYSTEM
=====================================

Dein Slime kann sich spezialisieren:
- KAMPF: Kämpft aktiv an deiner Seite, braucht eigene Skill-Punkte
- UTILITY: Hilft bei Lifeskills (Farming, Crafting, Mining, etc.)

WICHTIG:
- KEINE Spezialisierung = beides auf Basis-Level
- Spezialisierung = FOKUS auf einen Bereich (der andere wird schwächer)
- Kann später gewechselt werden (kostet Zeit + Items)

"Dein Schleim, deine Wahl - Kämpfer oder Helfer?"

Author: Claude Code (OPUS-1)
Date: 2026-02-01
"""

import time
import json
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

# ============================================================
# ENUMS & KONSTANTEN
# ============================================================

class Spezialisierung(Enum):
    """Slime Spezialisierung"""
    KEINE = "keine"              # Kein Fokus - beides auf 50%
    KAMPF = "kampf"              # Kampf-Fokus - 100% Kampf, 25% Utility
    UTILITY = "utility"          # Utility-Fokus - 25% Kampf, 100% Utility

class UtilityZweig(Enum):
    """Utility Sub-Spezialisierungen"""
    KEINE = "keine"
    FARMING = "farming"          # Gärtnern, Ernten, Pflanzen
    CRAFTING = "crafting"        # Handwerk, Alchemie, Kochen
    MINING = "mining"            # Bergbau, Steinbruch, Graben
    FISHING = "fishing"          # Angeln, Wassersammeln
    GATHERING = "gathering"      # Sammeln, Kräuter, Pilze
    TAMING = "taming"            # Monster zähmen helfen

class KampfZweig(Enum):
    """Kampf Sub-Spezialisierungen"""
    KEINE = "keine"
    TANK = "tank"                # Hohes HP, zieht Aggro
    DAMAGE = "damage"            # Hoher Schaden
    SUPPORT = "support"          # Heilt/Bufft den Spieler
    DEBUFF = "debuff"            # Schwächt Gegner

# Spezialisierungs-Effizienz
EFFIZIENZ = {
    Spezialisierung.KEINE: {"kampf": 0.5, "utility": 0.5},
    Spezialisierung.KAMPF: {"kampf": 1.0, "utility": 0.25},
    Spezialisierung.UTILITY: {"kampf": 0.25, "utility": 1.0},
}

# Kosten für Spezialisierungs-Wechsel
WECHSEL_KOSTEN = {
    "gold": 5000,
    "zeit_stunden": 24,           # 24h Trainingszeit
    "item": "spezialisierungs_kristall",  # Seltenes Item
}

# Utility-Zweig Boni (multipliziert mit Slime-Level)
UTILITY_ZWEIG_BONI = {
    UtilityZweig.FARMING: {
        "ernte_menge": 0.02,       # +2% pro Level
        "wachstum_speed": 0.01,    # +1% pro Level
        "seltene_samen": 0.005,    # +0.5% pro Level
        "beschreibung": "Hilft Pflanzen schneller wachsen und erntet mehr"
    },
    UtilityZweig.CRAFTING: {
        "craft_qualitaet": 0.02,   # +2% bessere Qualität
        "craft_speed": 0.015,      # +1.5% schneller
        "bonus_items": 0.01,       # +1% Chance auf Bonus-Items
        "beschreibung": "Verbessert Crafting-Qualität und Geschwindigkeit"
    },
    UtilityZweig.MINING: {
        "erz_menge": 0.02,         # +2% mehr Erz
        "seltene_erze": 0.01,      # +1% Chance auf seltene Erze
        "stamina_kosten": -0.01,   # -1% Stamina-Kosten
        "beschreibung": "Findet mehr und bessere Erze"
    },
    UtilityZweig.FISHING: {
        "fisch_qualitaet": 0.02,
        "seltene_fische": 0.015,
        "köder_sparen": 0.01,
        "beschreibung": "Bessere Fänge und seltene Fische"
    },
    UtilityZweig.GATHERING: {
        "sammel_menge": 0.02,
        "seltene_items": 0.01,
        "respawn_speed": 0.005,
        "beschreibung": "Sammelt mehr und findet seltene Materialien"
    },
    UtilityZweig.TAMING: {
        "zaehm_chance": 0.02,      # +2% Zähm-Chance
        "zaehm_speed": 0.01,       # +1% schneller
        "zaehm_kosten": -0.015,    # -1.5% Item-Kosten
        "beschreibung": "Hilft beim Zähmen von Monstern"
    },
}

# Kampf-Zweig Boni
KAMPF_ZWEIG_BONI = {
    KampfZweig.TANK: {
        "hp_bonus": 0.05,          # +5% HP pro Level
        "defense_bonus": 0.03,     # +3% Verteidigung
        "aggro_radius": 0.02,      # +2% Aggro-Radius
        "skills": ["Provokation", "Schutzschild", "Harte Haut"],
        "beschreibung": "Zieht Feinde an und hält viel aus"
    },
    KampfZweig.DAMAGE: {
        "attack_bonus": 0.05,      # +5% Angriff pro Level
        "crit_chance": 0.02,       # +2% Crit
        "crit_damage": 0.03,       # +3% Crit-Schaden
        "skills": ["Schleim-Schlag", "Gift-Spucke", "Explosion"],
        "beschreibung": "Teilt massiven Schaden aus"
    },
    KampfZweig.SUPPORT: {
        "heal_power": 0.03,        # +3% Heilung
        "buff_duration": 0.02,     # +2% Buff-Dauer
        "mana_regen": 0.02,        # +2% Mana-Regen (für dich!)
        "skills": ["Heilschleim", "Energie-Infusion", "Schutzhülle"],
        "beschreibung": "Heilt und stärkt dich im Kampf"
    },
    KampfZweig.DEBUFF: {
        "debuff_chance": 0.03,     # +3% Debuff-Chance
        "debuff_duration": 0.02,   # +2% Debuff-Dauer
        "enemy_resist_reduction": 0.02,  # -2% Feind-Resistenz
        "skills": ["Gift-Wolke", "Lähmung", "Schwächung"],
        "beschreibung": "Schwächt und verlangsamt Feinde"
    },
}

# Skill-Punkte pro Level (Slime braucht eigene SP!)
SKILL_PUNKTE_PRO_LEVEL = {
    "kampf": 2,     # 2 SP pro Level für Kampf-Skills
    "utility": 2,   # 2 SP pro Level für Utility-Skills
}

# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class SlimeSpezialisierungsState:
    """Spezialisierungs-Zustand eines Slimes"""
    slime_id: str

    # Haupt-Spezialisierung
    spezialisierung: str = Spezialisierung.KEINE.value

    # Sub-Spezialisierungen
    utility_zweig: str = UtilityZweig.KEINE.value
    kampf_zweig: str = KampfZweig.KEINE.value

    # Skill-Punkte
    kampf_sp_gesamt: int = 0
    kampf_sp_verfuegbar: int = 0
    utility_sp_gesamt: int = 0
    utility_sp_verfuegbar: int = 0

    # Gelernte Skills
    kampf_skills: Dict[str, int] = field(default_factory=dict)  # skill_id -> level
    utility_skills: Dict[str, int] = field(default_factory=dict)

    # Spezialisierungs-Level (wie lange in dieser Spec)
    spec_level: int = 1
    spec_exp: int = 0
    spec_exp_next: int = 100

    # Training
    training_aktiv: bool = False
    training_start: float = 0
    training_ende: float = 0
    training_typ: str = ""  # "kampf" oder "utility"

    # Wechsel-Cooldown
    letzter_wechsel: float = 0
    wechsel_cooldown: float = 86400  # 24h

    def to_dict(self) -> dict:
        return {
            "slime_id": self.slime_id,
            "spezialisierung": self.spezialisierung,
            "utility_zweig": self.utility_zweig,
            "kampf_zweig": self.kampf_zweig,
            "kampf_sp_gesamt": self.kampf_sp_gesamt,
            "kampf_sp_verfuegbar": self.kampf_sp_verfuegbar,
            "utility_sp_gesamt": self.utility_sp_gesamt,
            "utility_sp_verfuegbar": self.utility_sp_verfuegbar,
            "kampf_skills": self.kampf_skills,
            "utility_skills": self.utility_skills,
            "spec_level": self.spec_level,
            "spec_exp": self.spec_exp,
            "spec_exp_next": self.spec_exp_next,
            "training_aktiv": self.training_aktiv,
            "training_start": self.training_start,
            "training_ende": self.training_ende,
            "training_typ": self.training_typ,
            "letzter_wechsel": self.letzter_wechsel
        }

@dataclass
class SlimeKampfSkill:
    """Ein Kampf-Skill des Slimes"""
    skill_id: str
    name: str
    beschreibung: str
    zweig: str  # KampfZweig

    # Kosten
    sp_kosten: int = 1           # Skill-Punkte zum Lernen
    mana_kosten: int = 10        # Mana pro Nutzung
    cooldown: float = 5.0        # Sekunden

    # Effekte
    schaden_basis: int = 10
    schaden_skalierung: float = 0.5  # pro Skill-Level
    effekt_typ: str = "damage"   # damage, heal, buff, debuff
    effekt_wert: float = 0

    # Level-Up
    max_level: int = 5

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "beschreibung": self.beschreibung,
            "zweig": self.zweig,
            "sp_kosten": self.sp_kosten,
            "mana_kosten": self.mana_kosten,
            "cooldown": self.cooldown,
            "schaden_basis": self.schaden_basis,
            "schaden_skalierung": self.schaden_skalierung,
            "effekt_typ": self.effekt_typ,
            "effekt_wert": self.effekt_wert,
            "max_level": self.max_level
        }

@dataclass
class SlimeUtilitySkill:
    """Ein Utility-Skill des Slimes"""
    skill_id: str
    name: str
    beschreibung: str
    zweig: str  # UtilityZweig

    # Kosten
    sp_kosten: int = 1
    aktivierungs_kosten: int = 0  # Gold/Items pro Nutzung

    # Effekte (Boni werden addiert)
    bonus_typ: str = ""          # z.B. "ernte_menge", "craft_qualitaet"
    bonus_wert: float = 0.05     # +5% pro Level
    passive: bool = True         # Passive oder aktive Fähigkeit

    # Level-Up
    max_level: int = 5

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "beschreibung": self.beschreibung,
            "zweig": self.zweig,
            "sp_kosten": self.sp_kosten,
            "aktivierungs_kosten": self.aktivierungs_kosten,
            "bonus_typ": self.bonus_typ,
            "bonus_wert": self.bonus_wert,
            "passive": self.passive,
            "max_level": self.max_level
        }

# ============================================================
# SKILL-DATENBANK
# ============================================================

KAMPF_SKILL_DB: Dict[str, SlimeKampfSkill] = {
    # Tank Skills
    "provokation": SlimeKampfSkill(
        skill_id="provokation",
        name="Provokation",
        beschreibung="Zieht Feinde auf den Slime",
        zweig=KampfZweig.TANK.value,
        sp_kosten=1,
        mana_kosten=15,
        cooldown=10,
        effekt_typ="taunt",
        effekt_wert=5  # Sekunden
    ),
    "schutzschild": SlimeKampfSkill(
        skill_id="schutzschild",
        name="Schutzschild",
        beschreibung="Absorbiert Schaden für dich",
        zweig=KampfZweig.TANK.value,
        sp_kosten=2,
        mana_kosten=25,
        cooldown=20,
        effekt_typ="shield",
        effekt_wert=100  # Basis-Schild HP
    ),
    "harte_haut": SlimeKampfSkill(
        skill_id="harte_haut",
        name="Harte Haut",
        beschreibung="Passiv: Erhöhte Verteidigung",
        zweig=KampfZweig.TANK.value,
        sp_kosten=1,
        effekt_typ="passive_defense",
        effekt_wert=0.1  # +10% pro Level
    ),

    # Damage Skills
    "schleim_schlag": SlimeKampfSkill(
        skill_id="schleim_schlag",
        name="Schleim-Schlag",
        beschreibung="Basis-Angriff",
        zweig=KampfZweig.DAMAGE.value,
        sp_kosten=1,
        mana_kosten=5,
        cooldown=2,
        schaden_basis=15,
        schaden_skalierung=0.6
    ),
    "gift_spucke": SlimeKampfSkill(
        skill_id="gift_spucke",
        name="Gift-Spucke",
        beschreibung="Vergiftet Feinde über Zeit",
        zweig=KampfZweig.DAMAGE.value,
        sp_kosten=2,
        mana_kosten=20,
        cooldown=8,
        schaden_basis=5,
        schaden_skalierung=0.3,
        effekt_typ="poison",
        effekt_wert=5  # Ticks
    ),
    "explosion_mini": SlimeKampfSkill(
        skill_id="explosion_mini",
        name="Mini-Explosion",
        beschreibung="AoE-Schaden (Slime überlebt!)",
        zweig=KampfZweig.DAMAGE.value,
        sp_kosten=3,
        mana_kosten=40,
        cooldown=30,
        schaden_basis=50,
        schaden_skalierung=1.0,
        effekt_typ="aoe"
    ),

    # Support Skills
    "heilschleim": SlimeKampfSkill(
        skill_id="heilschleim",
        name="Heilschleim",
        beschreibung="Heilt dich langsam",
        zweig=KampfZweig.SUPPORT.value,
        sp_kosten=1,
        mana_kosten=15,
        cooldown=5,
        effekt_typ="heal",
        effekt_wert=20  # Basis-Heilung
    ),
    "energie_infusion": SlimeKampfSkill(
        skill_id="energie_infusion",
        name="Energie-Infusion",
        beschreibung="Regeneriert dein Mana",
        zweig=KampfZweig.SUPPORT.value,
        sp_kosten=2,
        mana_kosten=10,
        cooldown=15,
        effekt_typ="mana_restore",
        effekt_wert=30
    ),
    "schutzhulle": SlimeKampfSkill(
        skill_id="schutzhulle",
        name="Schutzhülle",
        beschreibung="Kurze Unverwundbarkeit",
        zweig=KampfZweig.SUPPORT.value,
        sp_kosten=3,
        mana_kosten=50,
        cooldown=60,
        effekt_typ="invuln",
        effekt_wert=2  # Sekunden
    ),

    # Debuff Skills
    "gift_wolke": SlimeKampfSkill(
        skill_id="gift_wolke",
        name="Gift-Wolke",
        beschreibung="Vergiftet alle Feinde im Bereich",
        zweig=KampfZweig.DEBUFF.value,
        sp_kosten=2,
        mana_kosten=25,
        cooldown=12,
        effekt_typ="aoe_poison",
        effekt_wert=3
    ),
    "laehmung": SlimeKampfSkill(
        skill_id="laehmung",
        name="Lähmung",
        beschreibung="Verlangsamt einen Feind stark",
        zweig=KampfZweig.DEBUFF.value,
        sp_kosten=2,
        mana_kosten=20,
        cooldown=10,
        effekt_typ="slow",
        effekt_wert=0.5  # 50% langsamer
    ),
    "schwaechung": SlimeKampfSkill(
        skill_id="schwaechung",
        name="Schwächung",
        beschreibung="Reduziert Feind-Verteidigung",
        zweig=KampfZweig.DEBUFF.value,
        sp_kosten=1,
        mana_kosten=15,
        cooldown=8,
        effekt_typ="defense_down",
        effekt_wert=0.2  # -20%
    ),
}

UTILITY_SKILL_DB: Dict[str, SlimeUtilitySkill] = {
    # Farming Skills
    "schnelles_wachstum": SlimeUtilitySkill(
        skill_id="schnelles_wachstum",
        name="Schnelles Wachstum",
        beschreibung="Pflanzen wachsen schneller",
        zweig=UtilityZweig.FARMING.value,
        sp_kosten=1,
        bonus_typ="wachstum_speed",
        bonus_wert=0.05
    ),
    "reiche_ernte": SlimeUtilitySkill(
        skill_id="reiche_ernte",
        name="Reiche Ernte",
        beschreibung="Mehr Ertrag beim Ernten",
        zweig=UtilityZweig.FARMING.value,
        sp_kosten=2,
        bonus_typ="ernte_menge",
        bonus_wert=0.08
    ),
    "samen_finder": SlimeUtilitySkill(
        skill_id="samen_finder",
        name="Samen-Finder",
        beschreibung="Findet seltene Samen",
        zweig=UtilityZweig.FARMING.value,
        sp_kosten=2,
        bonus_typ="seltene_samen",
        bonus_wert=0.02
    ),

    # Crafting Skills
    "meisterhand": SlimeUtilitySkill(
        skill_id="meisterhand",
        name="Meisterhand",
        beschreibung="Bessere Craft-Qualität",
        zweig=UtilityZweig.CRAFTING.value,
        sp_kosten=1,
        bonus_typ="craft_qualitaet",
        bonus_wert=0.05
    ),
    "effizienz": SlimeUtilitySkill(
        skill_id="effizienz",
        name="Effizienz",
        beschreibung="Weniger Material verbraucht",
        zweig=UtilityZweig.CRAFTING.value,
        sp_kosten=2,
        bonus_typ="material_sparen",
        bonus_wert=0.05
    ),
    "inspiration": SlimeUtilitySkill(
        skill_id="inspiration",
        name="Inspiration",
        beschreibung="Chance auf Bonus-Items",
        zweig=UtilityZweig.CRAFTING.value,
        sp_kosten=2,
        bonus_typ="bonus_items",
        bonus_wert=0.03
    ),

    # Mining Skills
    "erz_spuerer": SlimeUtilitySkill(
        skill_id="erz_spuerer",
        name="Erz-Spürer",
        beschreibung="Findet versteckte Erz-Adern",
        zweig=UtilityZweig.MINING.value,
        sp_kosten=1,
        bonus_typ="erz_sichtbar",
        bonus_wert=0.10
    ),
    "hartes_graben": SlimeUtilitySkill(
        skill_id="hartes_graben",
        name="Hartes Graben",
        beschreibung="Schneller abbauen",
        zweig=UtilityZweig.MINING.value,
        sp_kosten=2,
        bonus_typ="mining_speed",
        bonus_wert=0.08
    ),
    "gluecksschuerfer": SlimeUtilitySkill(
        skill_id="gluecksschuerfer",
        name="Glücksschürfer",
        beschreibung="Mehr seltene Erze",
        zweig=UtilityZweig.MINING.value,
        sp_kosten=2,
        bonus_typ="seltene_erze",
        bonus_wert=0.03
    ),

    # Fishing Skills
    "geduldiger_angler": SlimeUtilitySkill(
        skill_id="geduldiger_angler",
        name="Geduldiger Angler",
        beschreibung="Fische beißen schneller an",
        zweig=UtilityZweig.FISHING.value,
        sp_kosten=1,
        bonus_typ="biss_chance",
        bonus_wert=0.10
    ),
    "fischkenner": SlimeUtilitySkill(
        skill_id="fischkenner",
        name="Fischkenner",
        beschreibung="Bessere Fisch-Qualität",
        zweig=UtilityZweig.FISHING.value,
        sp_kosten=2,
        bonus_typ="fisch_qualitaet",
        bonus_wert=0.08
    ),
    "legendaerer_fang": SlimeUtilitySkill(
        skill_id="legendaerer_fang",
        name="Legendärer Fang",
        beschreibung="Chance auf legendäre Fische",
        zweig=UtilityZweig.FISHING.value,
        sp_kosten=3,
        bonus_typ="legendaere_fische",
        bonus_wert=0.01
    ),

    # Gathering Skills
    "kraeuterkenner": SlimeUtilitySkill(
        skill_id="kraeuterkenner",
        name="Kräuterkenner",
        beschreibung="Findet mehr Kräuter",
        zweig=UtilityZweig.GATHERING.value,
        sp_kosten=1,
        bonus_typ="kraeuter_menge",
        bonus_wert=0.10
    ),
    "pilzfreund": SlimeUtilitySkill(
        skill_id="pilzfreund",
        name="Pilzfreund",
        beschreibung="Erkennt essbare Pilze",
        zweig=UtilityZweig.GATHERING.value,
        sp_kosten=1,
        bonus_typ="pilz_sicherheit",
        bonus_wert=1.0  # 100% sichere Pilze
    ),
    "naturverbunden": SlimeUtilitySkill(
        skill_id="naturverbunden",
        name="Naturverbunden",
        beschreibung="Ressourcen spawnen schneller",
        zweig=UtilityZweig.GATHERING.value,
        sp_kosten=2,
        bonus_typ="respawn_speed",
        bonus_wert=0.05
    ),

    # Taming Skills
    "tierfluesterer": SlimeUtilitySkill(
        skill_id="tierfluesterer",
        name="Tierflüsterer",
        beschreibung="Höhere Zähm-Chance",
        zweig=UtilityZweig.TAMING.value,
        sp_kosten=2,
        bonus_typ="zaehm_chance",
        bonus_wert=0.05
    ),
    "beruhigung": SlimeUtilitySkill(
        skill_id="beruhigung",
        name="Beruhigung",
        beschreibung="Wildes Monster beruhigen",
        zweig=UtilityZweig.TAMING.value,
        sp_kosten=1,
        bonus_typ="aggro_reduktion",
        bonus_wert=0.20,
        passive=False
    ),
    "futtermeister": SlimeUtilitySkill(
        skill_id="futtermeister",
        name="Futtermeister",
        beschreibung="Weniger Futter zum Zähmen",
        zweig=UtilityZweig.TAMING.value,
        sp_kosten=2,
        bonus_typ="zaehm_kosten",
        bonus_wert=-0.10
    ),
}

# ============================================================
# HAUPT-MANAGER
# ============================================================

class SlimeSpezialisierungsManager:
    """
    Verwaltet Slime-Spezialisierungen.

    Ablauf:
    1. Slime startet ohne Spezialisierung (50% Kampf, 50% Utility)
    2. Spieler wählt Spezialisierung (ab Slime Level 10)
    3. Sub-Zweig wählen (ab Spec-Level 5)
    4. Skills mit SP lernen
    5. Wechsel möglich (mit Kosten/Cooldown)
    """

    def __init__(self):
        # Spezialisierungs-States
        self.slime_specs: Dict[str, SlimeSpezialisierungsState] = {}

        # Skill-Datenbank
        self.kampf_skills = KAMPF_SKILL_DB
        self.utility_skills = UTILITY_SKILL_DB

        # State laden
        self._load_state()

    # --- Spezialisierung wählen ---

    def waehle_spezialisierung(self, slime_id: str, slime_level: int,
                                spezialisierung: str) -> dict:
        """
        Wählt Haupt-Spezialisierung für einen Slime.
        Voraussetzung: Slime Level >= 10
        """
        if slime_level < 10:
            return {
                "erfolg": False,
                "grund": "Slime muss mindestens Level 10 sein",
                "aktuelles_level": slime_level
            }

        try:
            spec_enum = Spezialisierung(spezialisierung)
        except ValueError:
            return {
                "erfolg": False,
                "grund": f"Ungültige Spezialisierung: {spezialisierung}",
                "optionen": [s.value for s in Spezialisierung]
            }

        # State holen oder erstellen
        state = self._get_oder_erstelle_state(slime_id)

        # Prüfen ob Wechsel-Cooldown aktiv
        if state.spezialisierung != Spezialisierung.KEINE.value:
            if time.time() - state.letzter_wechsel < state.wechsel_cooldown:
                verbleibend = state.wechsel_cooldown - (time.time() - state.letzter_wechsel)
                return {
                    "erfolg": False,
                    "grund": "Wechsel-Cooldown aktiv",
                    "verbleibend_sekunden": verbleibend,
                    "verbleibend_stunden": verbleibend / 3600
                }

        # Spezialisierung setzen
        alte_spec = state.spezialisierung
        state.spezialisierung = spec_enum.value
        state.letzter_wechsel = time.time()

        # Initiale SP vergeben basierend auf Slime-Level
        sp_bonus = (slime_level - 10) * SKILL_PUNKTE_PRO_LEVEL["kampf" if spec_enum == Spezialisierung.KAMPF else "utility"]

        if spec_enum == Spezialisierung.KAMPF:
            state.kampf_sp_gesamt += sp_bonus
            state.kampf_sp_verfuegbar += sp_bonus
        elif spec_enum == Spezialisierung.UTILITY:
            state.utility_sp_gesamt += sp_bonus
            state.utility_sp_verfuegbar += sp_bonus

        self._save_state()

        return {
            "erfolg": True,
            "alte_spezialisierung": alte_spec,
            "neue_spezialisierung": spec_enum.value,
            "effizienz": EFFIZIENZ[spec_enum],
            "sp_erhalten": sp_bonus,
            "nachricht": f"Dein Slime ist jetzt auf {spec_enum.value.upper()} spezialisiert!"
        }

    def waehle_sub_zweig(self, slime_id: str, zweig_typ: str, zweig: str) -> dict:
        """
        Wählt Sub-Zweig (Kampf oder Utility).
        Voraussetzung: Spec-Level >= 5
        """
        state = self.slime_specs.get(slime_id)
        if not state:
            return {"erfolg": False, "grund": "Slime hat noch keine Spezialisierung"}

        if state.spec_level < 5:
            return {
                "erfolg": False,
                "grund": "Spec-Level muss mindestens 5 sein",
                "aktuelles_level": state.spec_level
            }

        if zweig_typ == "kampf":
            if state.spezialisierung != Spezialisierung.KAMPF.value:
                return {"erfolg": False, "grund": "Slime ist nicht auf Kampf spezialisiert"}
            try:
                zweig_enum = KampfZweig(zweig)
                state.kampf_zweig = zweig_enum.value
                boni = KAMPF_ZWEIG_BONI.get(zweig_enum, {})
            except ValueError:
                return {"erfolg": False, "grund": f"Ungültiger Kampf-Zweig: {zweig}"}

        elif zweig_typ == "utility":
            if state.spezialisierung != Spezialisierung.UTILITY.value:
                return {"erfolg": False, "grund": "Slime ist nicht auf Utility spezialisiert"}
            try:
                zweig_enum = UtilityZweig(zweig)
                state.utility_zweig = zweig_enum.value
                boni = UTILITY_ZWEIG_BONI.get(zweig_enum, {})
            except ValueError:
                return {"erfolg": False, "grund": f"Ungültiger Utility-Zweig: {zweig}"}

        else:
            return {"erfolg": False, "grund": "zweig_typ muss 'kampf' oder 'utility' sein"}

        self._save_state()

        return {
            "erfolg": True,
            "zweig": zweig,
            "boni": boni,
            "nachricht": f"Sub-Zweig {zweig.upper()} gewählt!"
        }

    # --- Skills lernen ---

    def lerne_skill(self, slime_id: str, skill_id: str) -> dict:
        """Lernt oder upgraded einen Skill"""
        state = self.slime_specs.get(slime_id)
        if not state:
            return {"erfolg": False, "grund": "Slime hat noch keine Spezialisierung"}

        # Skill finden
        if skill_id in self.kampf_skills:
            skill = self.kampf_skills[skill_id]
            skill_typ = "kampf"
            sp_verfuegbar = state.kampf_sp_verfuegbar
            gelernter_level = state.kampf_skills.get(skill_id, 0)

        elif skill_id in self.utility_skills:
            skill = self.utility_skills[skill_id]
            skill_typ = "utility"
            sp_verfuegbar = state.utility_sp_verfuegbar
            gelernter_level = state.utility_skills.get(skill_id, 0)

        else:
            return {"erfolg": False, "grund": f"Skill nicht gefunden: {skill_id}"}

        # Max-Level prüfen
        if gelernter_level >= skill.max_level:
            return {"erfolg": False, "grund": "Skill bereits auf Max-Level"}

        # SP prüfen
        if sp_verfuegbar < skill.sp_kosten:
            return {
                "erfolg": False,
                "grund": "Nicht genug Skill-Punkte",
                "verfuegbar": sp_verfuegbar,
                "benoetigt": skill.sp_kosten
            }

        # Skill lernen/upgraden
        neues_level = gelernter_level + 1

        if skill_typ == "kampf":
            state.kampf_skills[skill_id] = neues_level
            state.kampf_sp_verfuegbar -= skill.sp_kosten
        else:
            state.utility_skills[skill_id] = neues_level
            state.utility_sp_verfuegbar -= skill.sp_kosten

        self._save_state()

        return {
            "erfolg": True,
            "skill_id": skill_id,
            "skill_name": skill.name,
            "neues_level": neues_level,
            "max_level": skill.max_level,
            "sp_verbleibend": state.kampf_sp_verfuegbar if skill_typ == "kampf" else state.utility_sp_verfuegbar,
            "nachricht": f"{skill.name} auf Level {neues_level} gelernt!"
        }

    # --- Training ---

    def starte_training(self, slime_id: str, training_typ: str,
                         dauer_minuten: int = 60) -> dict:
        """
        Startet Training für Spezialisierung.
        Training gibt EXP für Spec-Level und SP.
        """
        state = self._get_oder_erstelle_state(slime_id)

        if state.training_aktiv:
            return {
                "erfolg": False,
                "grund": "Slime trainiert bereits",
                "training_ende": state.training_ende
            }

        state.training_aktiv = True
        state.training_start = time.time()
        state.training_ende = time.time() + (dauer_minuten * 60)
        state.training_typ = training_typ

        self._save_state()

        return {
            "erfolg": True,
            "training_typ": training_typ,
            "dauer_minuten": dauer_minuten,
            "training_ende": state.training_ende,
            "nachricht": f"Training gestartet! Fertig in {dauer_minuten} Minuten."
        }

    def beende_training(self, slime_id: str) -> dict:
        """Beendet Training und gibt Belohnungen"""
        state = self.slime_specs.get(slime_id)
        if not state or not state.training_aktiv:
            return {"erfolg": False, "grund": "Kein aktives Training"}

        jetzt = time.time()
        if jetzt < state.training_ende:
            return {
                "erfolg": False,
                "grund": "Training noch nicht fertig",
                "verbleibend_sekunden": state.training_ende - jetzt
            }

        # Belohnungen berechnen
        dauer_minuten = (state.training_ende - state.training_start) / 60
        exp_gewinn = int(dauer_minuten * 2)  # 2 EXP pro Minute
        sp_gewinn = max(1, int(dauer_minuten / 30))  # 1 SP pro 30 Min

        # EXP hinzufügen
        state.spec_exp += exp_gewinn
        while state.spec_exp >= state.spec_exp_next:
            state.spec_exp -= state.spec_exp_next
            state.spec_level += 1
            state.spec_exp_next = int(state.spec_exp_next * 1.2)  # +20% pro Level

        # SP hinzufügen
        if state.training_typ == "kampf":
            state.kampf_sp_gesamt += sp_gewinn
            state.kampf_sp_verfuegbar += sp_gewinn
        else:
            state.utility_sp_gesamt += sp_gewinn
            state.utility_sp_verfuegbar += sp_gewinn

        # Training zurücksetzen
        state.training_aktiv = False
        state.training_typ = ""

        self._save_state()

        return {
            "erfolg": True,
            "exp_gewinn": exp_gewinn,
            "sp_gewinn": sp_gewinn,
            "neues_spec_level": state.spec_level,
            "spec_exp": state.spec_exp,
            "spec_exp_next": state.spec_exp_next,
            "nachricht": f"Training abgeschlossen! +{exp_gewinn} EXP, +{sp_gewinn} SP"
        }

    # --- Boni berechnen ---

    def berechne_kampf_boni(self, slime_id: str, slime_level: int) -> dict:
        """Berechnet alle aktiven Kampf-Boni"""
        state = self.slime_specs.get(slime_id)
        if not state:
            return {"effizienz": 0.5, "boni": {}}

        # Basis-Effizienz
        try:
            spec = Spezialisierung(state.spezialisierung)
            effizienz = EFFIZIENZ[spec]["kampf"]
        except:
            effizienz = 0.5

        boni = {}

        # Zweig-Boni
        if state.kampf_zweig != KampfZweig.KEINE.value:
            try:
                zweig = KampfZweig(state.kampf_zweig)
                zweig_boni = KAMPF_ZWEIG_BONI.get(zweig, {})
                for key, value in zweig_boni.items():
                    if isinstance(value, (int, float)):
                        boni[key] = value * slime_level * effizienz
            except:
                pass

        # Skill-Boni
        for skill_id, skill_level in state.kampf_skills.items():
            skill = self.kampf_skills.get(skill_id)
            if skill and skill.effekt_typ.startswith("passive"):
                boni[skill.effekt_typ] = skill.effekt_wert * skill_level * effizienz

        return {
            "effizienz": effizienz,
            "zweig": state.kampf_zweig,
            "boni": boni,
            "skills": list(state.kampf_skills.keys())
        }

    def berechne_utility_boni(self, slime_id: str, slime_level: int) -> dict:
        """Berechnet alle aktiven Utility-Boni"""
        state = self.slime_specs.get(slime_id)
        if not state:
            return {"effizienz": 0.5, "boni": {}}

        # Basis-Effizienz
        try:
            spec = Spezialisierung(state.spezialisierung)
            effizienz = EFFIZIENZ[spec]["utility"]
        except:
            effizienz = 0.5

        boni = {}

        # Zweig-Boni
        if state.utility_zweig != UtilityZweig.KEINE.value:
            try:
                zweig = UtilityZweig(state.utility_zweig)
                zweig_boni = UTILITY_ZWEIG_BONI.get(zweig, {})
                for key, value in zweig_boni.items():
                    if isinstance(value, (int, float)):
                        boni[key] = value * slime_level * effizienz
            except:
                pass

        # Skill-Boni (nur passive)
        for skill_id, skill_level in state.utility_skills.items():
            skill = self.utility_skills.get(skill_id)
            if skill and skill.passive:
                boni[skill.bonus_typ] = boni.get(skill.bonus_typ, 0) + (skill.bonus_wert * skill_level * effizienz)

        return {
            "effizienz": effizienz,
            "zweig": state.utility_zweig,
            "boni": boni,
            "skills": list(state.utility_skills.keys())
        }

    # --- Abfragen ---

    def get_status(self, slime_id: str) -> dict:
        """Gibt vollständigen Spezialisierungs-Status zurück"""
        state = self.slime_specs.get(slime_id)
        if not state:
            return {
                "hat_spezialisierung": False,
                "hinweis": "Slime hat noch keine Spezialisierung (ab Level 10 möglich)"
            }

        return {
            "hat_spezialisierung": True,
            "state": state.to_dict(),
            "verfuegbare_kampf_skills": [s.to_dict() for s in self.kampf_skills.values()
                                          if state.kampf_zweig == KampfZweig.KEINE.value or s.zweig == state.kampf_zweig],
            "verfuegbare_utility_skills": [s.to_dict() for s in self.utility_skills.values()
                                            if state.utility_zweig == UtilityZweig.KEINE.value or s.zweig == state.utility_zweig]
        }

    def get_stats(self) -> dict:
        """Gibt System-Statistiken zurück"""
        kampf_count = sum(1 for s in self.slime_specs.values() if s.spezialisierung == Spezialisierung.KAMPF.value)
        utility_count = sum(1 for s in self.slime_specs.values() if s.spezialisierung == Spezialisierung.UTILITY.value)

        return {
            "slimes_mit_spec": len(self.slime_specs),
            "kampf_spezialisiert": kampf_count,
            "utility_spezialisiert": utility_count,
            "kampf_skills_gesamt": len(self.kampf_skills),
            "utility_skills_gesamt": len(self.utility_skills)
        }

    # --- Hilfsfunktionen ---

    def _get_oder_erstelle_state(self, slime_id: str) -> SlimeSpezialisierungsState:
        """Holt oder erstellt Spezialisierungs-State"""
        if slime_id not in self.slime_specs:
            self.slime_specs[slime_id] = SlimeSpezialisierungsState(slime_id=slime_id)
        return self.slime_specs[slime_id]

    def _save_state(self):
        """Speichert State"""
        state = {
            "slime_specs": {k: v.to_dict() for k, v in self.slime_specs.items()}
        }

        path = Path(__file__).parent / "slime_spec_state.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        """Lädt State"""
        path = Path(__file__).parent / "slime_spec_state.json"
        if not path.exists():
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)

            for k, v in state.get("slime_specs", {}).items():
                self.slime_specs[k] = SlimeSpezialisierungsState(
                    slime_id=v["slime_id"],
                    spezialisierung=v.get("spezialisierung", Spezialisierung.KEINE.value),
                    utility_zweig=v.get("utility_zweig", UtilityZweig.KEINE.value),
                    kampf_zweig=v.get("kampf_zweig", KampfZweig.KEINE.value),
                    kampf_sp_gesamt=v.get("kampf_sp_gesamt", 0),
                    kampf_sp_verfuegbar=v.get("kampf_sp_verfuegbar", 0),
                    utility_sp_gesamt=v.get("utility_sp_gesamt", 0),
                    utility_sp_verfuegbar=v.get("utility_sp_verfuegbar", 0),
                    kampf_skills=v.get("kampf_skills", {}),
                    utility_skills=v.get("utility_skills", {}),
                    spec_level=v.get("spec_level", 1),
                    spec_exp=v.get("spec_exp", 0),
                    spec_exp_next=v.get("spec_exp_next", 100),
                    training_aktiv=v.get("training_aktiv", False),
                    training_start=v.get("training_start", 0),
                    training_ende=v.get("training_ende", 0),
                    training_typ=v.get("training_typ", ""),
                    letzter_wechsel=v.get("letzter_wechsel", 0)
                )

        except Exception as e:
            print(f"[SLIME SPEC] Fehler beim Laden: {e}")


# ============================================================
# SINGLETON
# ============================================================

_manager: Optional[SlimeSpezialisierungsManager] = None

def get_slime_spec_manager() -> SlimeSpezialisierungsManager:
    """Gibt Singleton-Instanz zurück"""
    global _manager
    if _manager is None:
        _manager = SlimeSpezialisierungsManager()
    return _manager


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("🟢 Slime Spezialisierungs-System Test")
    print("=" * 50)

    manager = get_slime_spec_manager()

    # Test: Spezialisierung wählen
    print("\n1. Wähle Kampf-Spezialisierung...")
    result = manager.waehle_spezialisierung("test_slime_1", 15, "kampf")
    print(f"   Erfolg: {result.get('erfolg')}")
    print(f"   Nachricht: {result.get('nachricht', result.get('grund'))}")

    # Test: Sub-Zweig wählen
    print("\n2. Wähle Damage-Zweig...")
    # Erst Spec-Level erhöhen
    state = manager.slime_specs.get("test_slime_1")
    if state:
        state.spec_level = 5
        result = manager.waehle_sub_zweig("test_slime_1", "kampf", "damage")
        print(f"   Erfolg: {result.get('erfolg')}")
        print(f"   Boni: {result.get('boni', {}).get('beschreibung')}")

    # Test: Skill lernen
    print("\n3. Lerne Schleim-Schlag...")
    result = manager.lerne_skill("test_slime_1", "schleim_schlag")
    print(f"   Erfolg: {result.get('erfolg')}")
    print(f"   Nachricht: {result.get('nachricht', result.get('grund'))}")

    # Test: Boni berechnen
    print("\n4. Berechne Kampf-Boni (Level 20 Slime)...")
    boni = manager.berechne_kampf_boni("test_slime_1", 20)
    print(f"   Effizienz: {boni['effizienz']}")
    print(f"   Boni: {boni['boni']}")

    # Test: Utility-Slime
    print("\n5. Erstelle Utility-Slime...")
    result = manager.waehle_spezialisierung("test_slime_2", 10, "utility")
    print(f"   Erfolg: {result.get('erfolg')}")

    # Stats
    print("\n6. System Stats:")
    stats = manager.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")

    print("\n✅ Test abgeschlossen!")
