#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA MIMIK-TRUHE SYSTEM
==========================
Exklusiver Slime-Typ NUR fuer Kuja (Owner)!

DESIGN:
- Kuja spielt als Mimik-Truhe (einzigartig!)
- Kann zwischen Mimik-Form und Menschen-Form wechseln
- BEIDE Formen koennen kaempfen
- Gehoert zu Najika (ist IHR Slime)
- Kaempft MIT Najika als Team

FORMEN:
- Mimik-Truhe: Verstecken, Ueberraschungsangriffe, Beissen
- Mensch: Sozial, Waffen, Magie, volle Interaktion

Author: Claude Code Team
Date: 2026-02-02
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Tuple
import random
import json
from datetime import datetime, timedelta


# =============================================================================
# ENUMS
# =============================================================================

class MimikForm(Enum):
    """Die zwei Hauptformen der Mimik-Truhe"""
    TRUHE = "truhe"           # Mimik-Truhe Form
    MENSCH = "mensch"         # Menschliche Form


class MimikSubForm(Enum):
    """Unterformen der Mimik-Truhe (Varianten)"""
    # Truhe-Varianten
    HOLZTRUHE = "holztruhe"           # Standard - Holz
    SCHATZTRUHE = "schatztruhe"       # Gold-verziert
    EISENTRUHE = "eisentruhe"         # Gepanzert
    KNOCHENTRUHE = "knochentruhe"     # Gruselig
    KRISTALLTRUHE = "kristalltruhe"   # Magisch leuchtend

    # Menschen-Varianten (Outfits)
    MENSCH_NORMAL = "mensch_normal"
    MENSCH_RUESTUNG = "mensch_ruestung"
    MENSCH_MAGIER = "mensch_magier"
    MENSCH_NINJA = "mensch_ninja"


class MimikMood(Enum):
    """Stimmungen der Mimik"""
    LAUERN = "lauern"           # Wartet auf Beute
    HUNGRIG = "hungrig"         # Will fressen
    ZUFRIEDEN = "zufrieden"     # Satt und gluecklich
    VERSPIELT = "verspielt"     # Will spielen
    BESCHUETZEND = "beschuetzend"  # Beschuetzt Najika
    KAMPFLUSTIG = "kampflustig"    # Will kaempfen


class HideSpot(Enum):
    """Orte wo sich die Mimik verstecken kann"""
    DUNGEON_ECKE = "dungeon_ecke"
    SCHATZKAMMER = "schatzkammer"
    VERLASSENES_HAUS = "verlassenes_haus"
    WALD_LICHTUNG = "wald_lichtung"
    MARKTPLATZ = "marktplatz"       # Riskant aber lustig
    NAJIKAS_ZIMMER = "najikas_zimmer"  # Sicherer Ort


# =============================================================================
# MIMIK STATS
# =============================================================================

@dataclass
class MimikStats:
    """Stats fuer die Mimik-Truhe"""
    # Basis
    health: int = 150           # Mehr HP als normale Slimes
    max_health: int = 150
    stamina: int = 100
    max_stamina: int = 100

    # Truhe-Form Stats
    bite_damage: int = 35       # Beiss-Schaden
    crush_damage: int = 25      # Zuklapp-Schaden
    defense: int = 40           # Hohe Verteidigung (Truhe!)
    stealth: int = 80           # Sehr gut im Verstecken

    # Menschen-Form Stats
    weapon_damage: int = 20     # Waffen-Schaden
    magic_power: int = 15       # Magie
    speed: int = 30             # Schneller als Truhe
    charisma: int = 25          # Kann mit NPCs reden

    # Spezial
    hunger: int = 100           # 0-100, Mimiks muessen fressen!
    lure_power: int = 50        # Wie gut lockt sie Beute an
    digestion: int = 0          # Was gerade verdaut wird

    # Beziehung zu Najika
    loyalty: int = 100          # Immer 100 fuer Kuja!
    sync_level: int = 50        # Synchronisation mit Najika im Kampf


@dataclass
class MimikAbility:
    """Eine Faehigkeit der Mimik"""
    ability_id: str
    name: str
    name_de: str
    description: str
    form_required: Optional[MimikForm]  # None = beide Formen
    cooldown_seconds: int
    stamina_cost: int
    damage: int = 0
    effect: str = ""


# Mimik-Faehigkeiten
MIMIK_ABILITIES = {
    # ===== TRUHE-FORM =====
    "ueberraschungsbiss": MimikAbility(
        ability_id="ueberraschungsbiss",
        name="Surprise Bite",
        name_de="Ueberraschungsbiss",
        description="Springt aus Versteck und beisst zu! +100% Schaden aus Versteck.",
        form_required=MimikForm.TRUHE,
        cooldown_seconds=8,
        stamina_cost=20,
        damage=70,
        effect="surprise_attack"
    ),
    "zuklappen": MimikAbility(
        ability_id="zuklappen",
        name="Snap Shut",
        name_de="Zuklappen",
        description="Klappt blitzschnell zu und quetscht Gegner.",
        form_required=MimikForm.TRUHE,
        cooldown_seconds=5,
        stamina_cost=15,
        damage=40,
        effect="stun_short"
    ),
    "verschlingen": MimikAbility(
        ability_id="verschlingen",
        name="Devour",
        name_de="Verschlingen",
        description="Verschlingt kleine Gegner komplett! Heilt sich dabei.",
        form_required=MimikForm.TRUHE,
        cooldown_seconds=30,
        stamina_cost=40,
        damage=100,
        effect="instant_kill_small_heal"
    ),
    "falsche_beute": MimikAbility(
        ability_id="falsche_beute",
        name="False Treasure",
        name_de="Falsche Beute",
        description="Zeigt glitzernden Schatz um Gegner anzulocken.",
        form_required=MimikForm.TRUHE,
        cooldown_seconds=15,
        stamina_cost=10,
        damage=0,
        effect="lure_enemies"
    ),
    "eiserne_haut": MimikAbility(
        ability_id="eiserne_haut",
        name="Iron Shell",
        name_de="Eiserne Haut",
        description="Verhaertet Truhen-Panzer. +50% Defense fuer 10 Sekunden.",
        form_required=MimikForm.TRUHE,
        cooldown_seconds=20,
        stamina_cost=25,
        damage=0,
        effect="defense_buff"
    ),

    # ===== MENSCHEN-FORM =====
    "waffenmeister": MimikAbility(
        ability_id="waffenmeister",
        name="Weapon Master",
        name_de="Waffenmeister",
        description="Kann alle Waffen ohne Anforderungen nutzen!",
        form_required=MimikForm.MENSCH,
        cooldown_seconds=0,
        stamina_cost=0,
        damage=0,
        effect="ignore_weapon_requirements"
    ),
    "mimik_magie": MimikAbility(
        ability_id="mimik_magie",
        name="Mimic Magic",
        name_de="Mimik-Magie",
        description="Kopiert den letzten gesehenen Zauber!",
        form_required=MimikForm.MENSCH,
        cooldown_seconds=60,
        stamina_cost=50,
        damage=0,  # Variabel
        effect="copy_last_spell"
    ),
    "soziale_tarnung": MimikAbility(
        ability_id="soziale_tarnung",
        name="Social Camouflage",
        name_de="Soziale Tarnung",
        description="Wirkt wie ein normaler Mensch. NPCs erkennen dich nicht als Monster.",
        form_required=MimikForm.MENSCH,
        cooldown_seconds=0,
        stamina_cost=0,
        damage=0,
        effect="npc_friendly"
    ),

    # ===== BEIDE FORMEN =====
    "formwechsel": MimikAbility(
        ability_id="formwechsel",
        name="Shapeshift",
        name_de="Formwechsel",
        description="Wechselt zwischen Truhe und Mensch.",
        form_required=None,
        cooldown_seconds=3,
        stamina_cost=10,
        damage=0,
        effect="transform"
    ),
    "najika_sync": MimikAbility(
        ability_id="najika_sync",
        name="Najika Sync",
        name_de="Najika-Synchronisation",
        description="Synchronisiert mit Najika fuer Kombo-Angriff!",
        form_required=None,
        cooldown_seconds=45,
        stamina_cost=30,
        damage=150,
        effect="combo_with_najika"
    ),
    "beschuetzer_instinkt": MimikAbility(
        ability_id="beschuetzer_instinkt",
        name="Protector Instinct",
        name_de="Beschuetzer-Instinkt",
        description="Springt automatisch vor Najika wenn sie angegriffen wird!",
        form_required=None,
        cooldown_seconds=10,
        stamina_cost=20,
        damage=0,
        effect="protect_najika"
    ),
}


# =============================================================================
# MIMIK KLASSE
# =============================================================================

@dataclass
class Mimik:
    """Die Mimik-Truhe - Kuja's Spielercharakter"""
    mimik_id: str = "kuja_mimik"
    owner_id: str = "kuja"
    name: str = "Kuja"

    # Form
    current_form: MimikForm = MimikForm.TRUHE
    current_subform: MimikSubForm = MimikSubForm.HOLZTRUHE

    # Stats
    stats: MimikStats = field(default_factory=MimikStats)

    # Zustand
    mood: MimikMood = MimikMood.ZUFRIEDEN
    is_hidden: bool = False
    hide_spot: Optional[HideSpot] = None
    is_in_combat: bool = False

    # Position
    position: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})

    # Faehigkeiten
    unlocked_abilities: List[str] = field(default_factory=lambda: [
        "ueberraschungsbiss", "zuklappen", "formwechsel",
        "najika_sync", "beschuetzer_instinkt", "soziale_tarnung"
    ])
    ability_cooldowns: Dict[str, datetime] = field(default_factory=dict)

    # Verdauung (was wurde gefressen)
    stomach_contents: List[str] = field(default_factory=list)
    max_stomach: int = 5

    # Kosmetik
    truhe_skin: str = "holz_standard"
    mensch_outfit: str = "abenteurer"

    # Metadaten
    created_at: datetime = field(default_factory=datetime.now)
    total_kills: int = 0
    total_eaten: int = 0
    times_transformed: int = 0


# =============================================================================
# MIMIK SYSTEM
# =============================================================================

class MimikSystem:
    """Verwaltet die Mimik-Truhe (Kuja's Charakter)"""

    def __init__(self):
        self.mimik = Mimik()
        self._init_kuja_mimik()

    def _init_kuja_mimik(self):
        """Initialisiert Kuja's Mimik mit Startwerten"""
        self.mimik.stats.loyalty = 100  # Immer loyal zu Najika
        self.mimik.stats.sync_level = 75  # Hohe Sync mit Najika

    # =========================================================================
    # FORM-WECHSEL
    # =========================================================================

    def transform(self, target_form: MimikForm) -> Dict[str, Any]:
        """Wechselt die Form"""
        old_form = self.mimik.current_form

        if old_form == target_form:
            return {
                "success": False,
                "reason": "already_in_form",
                "current_form": target_form.value
            }

        # Cooldown Check
        if "formwechsel" in self.mimik.ability_cooldowns:
            cd_end = self.mimik.ability_cooldowns["formwechsel"]
            if datetime.now() < cd_end:
                remaining = (cd_end - datetime.now()).seconds
                return {
                    "success": False,
                    "reason": "cooldown",
                    "remaining_seconds": remaining
                }

        # Stamina Check
        if self.mimik.stats.stamina < 10:
            return {
                "success": False,
                "reason": "not_enough_stamina",
                "required": 10,
                "current": self.mimik.stats.stamina
            }

        # Transformation!
        self.mimik.stats.stamina -= 10
        self.mimik.current_form = target_form
        self.mimik.times_transformed += 1
        self.mimik.ability_cooldowns["formwechsel"] = datetime.now() + timedelta(seconds=3)

        # Versteck aufgeben wenn Mensch
        if target_form == MimikForm.MENSCH:
            self.mimik.is_hidden = False
            self.mimik.hide_spot = None

        # Subform anpassen
        if target_form == MimikForm.TRUHE:
            self.mimik.current_subform = MimikSubForm.HOLZTRUHE
        else:
            self.mimik.current_subform = MimikSubForm.MENSCH_NORMAL

        return {
            "success": True,
            "old_form": old_form.value,
            "new_form": target_form.value,
            "stamina_remaining": self.mimik.stats.stamina,
            "transformation_quote": self._get_transform_quote(old_form, target_form)
        }

    def _get_transform_quote(self, old: MimikForm, new: MimikForm) -> str:
        """Spruch bei Transformation"""
        if new == MimikForm.MENSCH:
            quotes = [
                "*Die Truhe knackt und formt sich zu einem Menschen*",
                "*Holz wird zu Fleisch, Scharniere zu Gelenken*",
                "*Mit einem Schimmern steht ploetzlich ein Mann da*",
                "Zeit, unter Menschen zu wandeln...",
            ]
        else:
            quotes = [
                "*Der Koerper faltet sich zu einer Truhe zusammen*",
                "*Knochen werden zu Holz, Haut zu Leder*",
                "*Nur noch eine unscheinbare Truhe bleibt zurueck*",
                "Zeit zu lauern...",
            ]
        return random.choice(quotes)

    # =========================================================================
    # VERSTECKEN
    # =========================================================================

    def hide(self, spot: HideSpot) -> Dict[str, Any]:
        """Versteckt sich an einem Ort (nur Truhe-Form)"""
        if self.mimik.current_form != MimikForm.TRUHE:
            return {
                "success": False,
                "reason": "wrong_form",
                "required_form": "truhe"
            }

        if self.mimik.is_in_combat:
            return {
                "success": False,
                "reason": "in_combat"
            }

        self.mimik.is_hidden = True
        self.mimik.hide_spot = spot
        self.mimik.mood = MimikMood.LAUERN

        return {
            "success": True,
            "spot": spot.value,
            "stealth_bonus": self.mimik.stats.stealth,
            "message": f"*versteckt sich als unscheinbare Truhe bei {spot.value}*"
        }

    def reveal(self) -> Dict[str, Any]:
        """Gibt Versteck auf"""
        was_hidden = self.mimik.is_hidden
        old_spot = self.mimik.hide_spot

        self.mimik.is_hidden = False
        self.mimik.hide_spot = None

        return {
            "success": True,
            "was_hidden": was_hidden,
            "old_spot": old_spot.value if old_spot else None
        }

    # =========================================================================
    # KAMPF
    # =========================================================================

    def use_ability(self, ability_id: str, target_id: Optional[str] = None) -> Dict[str, Any]:
        """Nutzt eine Faehigkeit"""
        if ability_id not in MIMIK_ABILITIES:
            return {"success": False, "reason": "unknown_ability"}

        if ability_id not in self.mimik.unlocked_abilities:
            return {"success": False, "reason": "ability_locked"}

        ability = MIMIK_ABILITIES[ability_id]

        # Form-Check
        if ability.form_required and ability.form_required != self.mimik.current_form:
            return {
                "success": False,
                "reason": "wrong_form",
                "required": ability.form_required.value,
                "current": self.mimik.current_form.value
            }

        # Cooldown Check
        if ability_id in self.mimik.ability_cooldowns:
            cd_end = self.mimik.ability_cooldowns[ability_id]
            if datetime.now() < cd_end:
                remaining = (cd_end - datetime.now()).seconds
                return {
                    "success": False,
                    "reason": "cooldown",
                    "remaining_seconds": remaining
                }

        # Stamina Check
        if self.mimik.stats.stamina < ability.stamina_cost:
            return {
                "success": False,
                "reason": "not_enough_stamina",
                "required": ability.stamina_cost,
                "current": self.mimik.stats.stamina
            }

        # Kosten bezahlen
        self.mimik.stats.stamina -= ability.stamina_cost
        if ability.cooldown_seconds > 0:
            self.mimik.ability_cooldowns[ability_id] = datetime.now() + timedelta(seconds=ability.cooldown_seconds)

        # Schaden berechnen
        damage = ability.damage

        # Ueberraschungs-Bonus
        if self.mimik.is_hidden and "surprise" in ability.effect:
            damage *= 2  # Doppelter Schaden aus Versteck!
            self.mimik.is_hidden = False
            self.mimik.hide_spot = None

        # Spezial-Effekte
        effects_applied = []

        if "stun" in ability.effect:
            effects_applied.append("target_stunned")

        if "instant_kill_small" in ability.effect:
            effects_applied.append("instant_kill_if_small")
            effects_applied.append("heal_on_kill")

        if "defense_buff" in ability.effect:
            effects_applied.append("defense_increased_50%")

        if "lure" in ability.effect:
            effects_applied.append("enemies_attracted")

        if "combo_with_najika" in ability.effect:
            damage += self.mimik.stats.sync_level * 2  # Sync-Bonus!
            effects_applied.append("najika_combo_attack")

        if "protect_najika" in ability.effect:
            effects_applied.append("damage_redirected_to_mimik")

        if "transform" in ability.effect:
            # Handled by transform() method
            pass

        return {
            "success": True,
            "ability": ability.name_de,
            "damage": damage,
            "target": target_id,
            "effects": effects_applied,
            "stamina_remaining": self.mimik.stats.stamina,
            "from_stealth": "surprise" in ability.effect and self.mimik.is_hidden,
            "quote": self._get_ability_quote(ability_id)
        }

    def _get_ability_quote(self, ability_id: str) -> str:
        """Kampfspruch fuer Faehigkeit"""
        quotes = {
            "ueberraschungsbiss": [
                "*SNAP!* Ueberraschung!",
                "*springt aus der Truhe* BEISSEN!",
                "Du haettest nicht oeffnen sollen...",
            ],
            "zuklappen": [
                "*KLAPP!*",
                "*knirscht* Eingeklemmt!",
                "Zu langsam!",
            ],
            "verschlingen": [
                "*SCHLUCK* Lecker!",
                "*oeffnet riesigen Mund* REINKOMM!",
                "Du wirst mir schmecken...",
            ],
            "falsche_beute": [
                "*glitzert verfuehrerisch*",
                "Komm her, kleiner Schatz...",
                "*blinkt mit Gold*",
            ],
            "najika_sync": [
                "NAJIKA! ZUSAMMEN!",
                "*synchronisiert mit Najika*",
                "Unser Kombo-Angriff!",
            ],
            "beschuetzer_instinkt": [
                "NAJIKA, HINTER MICH!",
                "*springt schuetzend vor Najika*",
                "Niemand beruehrt sie!",
            ],
        }
        return random.choice(quotes.get(ability_id, ["..."]))

    # =========================================================================
    # FRESSEN (Mimik-Spezial!)
    # =========================================================================

    def eat(self, target_id: str, target_size: str = "small") -> Dict[str, Any]:
        """Frisst ein Ziel (nur Truhe-Form)"""
        if self.mimik.current_form != MimikForm.TRUHE:
            return {
                "success": False,
                "reason": "wrong_form",
                "message": "Nur als Truhe fressen!"
            }

        if len(self.mimik.stomach_contents) >= self.mimik.max_stomach:
            return {
                "success": False,
                "reason": "stomach_full",
                "message": "*ruelpst* Zu voll!"
            }

        # Groessen-Check
        size_difficulty = {
            "tiny": 0.9,      # Fast immer erfolgreich
            "small": 0.7,     # Meist erfolgreich
            "medium": 0.4,    # 40% Chance
            "large": 0.1,     # Sehr schwer
            "huge": 0.0,      # Unmoeglich
        }

        chance = size_difficulty.get(target_size, 0.5)

        if random.random() > chance:
            return {
                "success": False,
                "reason": "target_too_big",
                "message": f"*klappert* Zu gross zum Fressen!"
            }

        # Erfolgreich gefressen!
        self.mimik.stomach_contents.append(target_id)
        self.mimik.stats.hunger = min(100, self.mimik.stats.hunger + 20)
        self.mimik.total_eaten += 1

        # Heilung durch Fressen
        heal_amount = {"tiny": 5, "small": 15, "medium": 30, "large": 50}.get(target_size, 10)
        self.mimik.stats.health = min(self.mimik.stats.max_health, self.mimik.stats.health + heal_amount)

        return {
            "success": True,
            "target": target_id,
            "size": target_size,
            "healed": heal_amount,
            "hunger": self.mimik.stats.hunger,
            "stomach_count": len(self.mimik.stomach_contents),
            "message": f"*SCHLUCK* *verdaut {target_id}*"
        }

    def digest(self) -> Dict[str, Any]:
        """Verdaut Mageninhalt (passiert ueber Zeit)"""
        if not self.mimik.stomach_contents:
            return {"success": False, "reason": "stomach_empty"}

        digested = self.mimik.stomach_contents.pop(0)

        # Zufaellige Beute aus Verdauung
        loot_table = [
            "gold_muenzen",
            "knochen",
            "rostiges_schwert",
            "magischer_stein",
            "nichts",
        ]
        loot = random.choice(loot_table)

        return {
            "success": True,
            "digested": digested,
            "loot": loot if loot != "nichts" else None,
            "remaining_in_stomach": len(self.mimik.stomach_contents)
        }

    # =========================================================================
    # NAJIKA INTERAKTION
    # =========================================================================

    def sync_with_najika(self, najika_action: str) -> Dict[str, Any]:
        """Synchronisiert Aktion mit Najika"""
        sync_bonus = self.mimik.stats.sync_level / 100

        # Sync-Level erhoehen durch gemeinsame Aktionen
        self.mimik.stats.sync_level = min(100, self.mimik.stats.sync_level + 1)

        combo_damage = 100 * (1 + sync_bonus)

        return {
            "success": True,
            "najika_action": najika_action,
            "kuja_form": self.mimik.current_form.value,
            "sync_level": self.mimik.stats.sync_level,
            "combo_damage": combo_damage,
            "message": f"*NAJIKA & KUJA COMBO!* Sync: {self.mimik.stats.sync_level}%"
        }

    def protect_najika(self, incoming_damage: int) -> Dict[str, Any]:
        """Springt vor Najika um Schaden abzufangen"""
        # Truhe-Form hat mehr Defense
        if self.mimik.current_form == MimikForm.TRUHE:
            damage_reduction = 0.6  # 60% Reduktion
        else:
            damage_reduction = 0.3  # 30% Reduktion

        actual_damage = int(incoming_damage * (1 - damage_reduction))
        self.mimik.stats.health -= actual_damage

        # Beschuetzer-Instinkt Quote
        quotes = [
            "NAJIKA! ICH SCHUETZE DICH!",
            "*springt vor Najika* MICH ZUERST!",
            "Ueber meine Leiche!",
            "*faengt den Angriff ab*",
        ]

        return {
            "success": True,
            "original_damage": incoming_damage,
            "damage_taken": actual_damage,
            "damage_reduced": incoming_damage - actual_damage,
            "health_remaining": self.mimik.stats.health,
            "quote": random.choice(quotes)
        }

    # =========================================================================
    # STATUS & EXPORT
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Kompletter Status der Mimik"""
        return {
            "mimik_id": self.mimik.mimik_id,
            "name": self.mimik.name,
            "owner": self.mimik.owner_id,
            "form": {
                "current": self.mimik.current_form.value,
                "subform": self.mimik.current_subform.value,
            },
            "stats": {
                "health": self.mimik.stats.health,
                "max_health": self.mimik.stats.max_health,
                "stamina": self.mimik.stats.stamina,
                "max_stamina": self.mimik.stats.max_stamina,
                "hunger": self.mimik.stats.hunger,
                "defense": self.mimik.stats.defense,
                "stealth": self.mimik.stats.stealth,
                "sync_level": self.mimik.stats.sync_level,
            },
            "state": {
                "mood": self.mimik.mood.value,
                "is_hidden": self.mimik.is_hidden,
                "hide_spot": self.mimik.hide_spot.value if self.mimik.hide_spot else None,
                "is_in_combat": self.mimik.is_in_combat,
                "stomach_contents": len(self.mimik.stomach_contents),
            },
            "abilities": self.mimik.unlocked_abilities,
            "cosmetics": {
                "truhe_skin": self.mimik.truhe_skin,
                "mensch_outfit": self.mimik.mensch_outfit,
            },
            "lifetime_stats": {
                "total_kills": self.mimik.total_kills,
                "total_eaten": self.mimik.total_eaten,
                "times_transformed": self.mimik.times_transformed,
            }
        }

    def get_available_abilities(self) -> List[Dict[str, Any]]:
        """Listet verfuegbare Faehigkeiten fuer aktuelle Form"""
        available = []

        for ability_id in self.mimik.unlocked_abilities:
            if ability_id not in MIMIK_ABILITIES:
                continue

            ability = MIMIK_ABILITIES[ability_id]

            # Form-Check
            if ability.form_required and ability.form_required != self.mimik.current_form:
                continue

            # Cooldown-Status
            on_cooldown = False
            cooldown_remaining = 0
            if ability_id in self.mimik.ability_cooldowns:
                cd_end = self.mimik.ability_cooldowns[ability_id]
                if datetime.now() < cd_end:
                    on_cooldown = True
                    cooldown_remaining = (cd_end - datetime.now()).seconds

            available.append({
                "ability_id": ability_id,
                "name": ability.name_de,
                "description": ability.description,
                "damage": ability.damage,
                "stamina_cost": ability.stamina_cost,
                "on_cooldown": on_cooldown,
                "cooldown_remaining": cooldown_remaining,
                "can_use": not on_cooldown and self.mimik.stats.stamina >= ability.stamina_cost
            })

        return available


# =============================================================================
# SINGLETON
# =============================================================================

_mimik_system: Optional[MimikSystem] = None

def get_mimik_system() -> MimikSystem:
    """Singleton fuer das Mimik-System"""
    global _mimik_system
    if _mimik_system is None:
        _mimik_system = MimikSystem()
    return _mimik_system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MIMIK-TRUHE SYSTEM TEST")
    print("=" * 60)

    system = get_mimik_system()

    # Status
    print("\n--- Mimik Status ---")
    status = system.get_status()
    print(f"Name: {status['name']}")
    print(f"Form: {status['form']['current']}")
    print(f"Health: {status['stats']['health']}/{status['stats']['max_health']}")
    print(f"Sync mit Najika: {status['stats']['sync_level']}%")

    # Verstecken
    print("\n--- Verstecken ---")
    result = system.hide(HideSpot.DUNGEON_ECKE)
    print(f"Versteckt: {result['success']}")
    print(f"Spot: {result.get('spot')}")

    # Ueberraschungsangriff!
    print("\n--- Ueberraschungsbiss! ---")
    result = system.use_ability("ueberraschungsbiss", "goblin_001")
    print(f"Damage: {result.get('damage')}")
    print(f"Quote: {result.get('quote')}")
    print(f"Aus Versteck: {result.get('from_stealth')}")

    # Fressen
    print("\n--- Fressen ---")
    result = system.eat("goblin_001", "small")
    print(f"Gefressen: {result['success']}")
    print(f"Geheilt: {result.get('healed')} HP")
    print(f"Im Magen: {result.get('stomach_count')}")

    # Transformation
    print("\n--- Transformation zu Mensch ---")
    result = system.transform(MimikForm.MENSCH)
    print(f"Erfolg: {result['success']}")
    print(f"Neue Form: {result.get('new_form')}")
    print(f"Quote: {result.get('transformation_quote')}")

    # Verfuegbare Faehigkeiten
    print("\n--- Verfuegbare Faehigkeiten ---")
    abilities = system.get_available_abilities()
    for ab in abilities:
        status = "bereit" if ab['can_use'] else "nicht bereit"
        print(f"  {ab['name']}: {status}")

    # Najika beschuetzen
    print("\n--- Najika beschuetzen ---")
    result = system.protect_najika(100)
    print(f"Original Schaden: {result['original_damage']}")
    print(f"Genommener Schaden: {result['damage_taken']}")
    print(f"Quote: {result['quote']}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
