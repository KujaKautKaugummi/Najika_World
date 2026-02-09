#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - Slime Companion System
=====================================
Basiert auf: Dragon Quest Monsters + Digimon V-Pet + Fortnite Begleiter
WICHTIG: Monster-Kaempfe sind OPTIONAL! Skyrim-Freiheit!

Erstellt: 2026-01-28
"""

import json
import time
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# =============================================================================
# ENUMS & CONSTANTS
# =============================================================================

class SlimeType(Enum):
    """9 Slime-Typen basierend auf den 9 Regionen"""
    MOOS = "moos_schleim"           # Samtmoos-Tiefwald
    FROST = "frost_schleim"         # Reich der Drei
    WASSER = "wasser_schleim"       # Salzwind-Kueste
    BLITZ = "blitz_schleim"         # Blitzebene
    GIFT = "gift_schleim"           # Gruenschlamm-Sumpf
    MAGMA = "magma_schleim"         # Magmastroeme
    SAND = "sand_schleim"           # Heisse Duenen
    KRISTALL = "kristall_schleim"   # Tiefenhoehlen
    GOETTER = "goetter_schleim"     # Goetterfels (SELTEN!)

class EvolutionStage(Enum):
    """6 Evolution-Stufen (Digimon V-Pet Style)"""
    EGG = 1         # Schleim-Ei
    BABY = 2        # Baby-Schleim (nach 1h)
    KIND = 3        # Kind-Schleim (nach 24h)
    REIF = 4        # Reifer Schleim (nach 3 Tage)
    CHAMPION = 5    # Champion-Schleim (nach 7 Tage)
    ULTIMATIV = 6   # Ultimativ (nach 14 Tage)

# Evolution Zeit in Sekunden
EVOLUTION_TIMES = {
    EvolutionStage.EGG: 0,
    EvolutionStage.BABY: 3600,          # 1 Stunde
    EvolutionStage.KIND: 86400,         # 24 Stunden
    EvolutionStage.REIF: 259200,        # 3 Tage
    EvolutionStage.CHAMPION: 604800,    # 7 Tage
    EvolutionStage.ULTIMATIV: 1209600,  # 14 Tage
}

# Passive Boni pro Slime-Typ (fuer Nicht-Kaempfer!)
PASSIVE_BONUSES = {
    SlimeType.MOOS: {
        "farming_speed": 0.20,
        "herb_quality": 0.10,
        "description": "Hilft beim Gaertnern, verbessert Kraeuter-Qualitaet"
    },
    SlimeType.FROST: {
        "food_preservation": 0.30,
        "cold_resistance": 0.20,
        "description": "Haelt Essen frisch, schuetzt vor Kaelte"
    },
    SlimeType.WASSER: {
        "fishing_luck": 0.30,
        "swimming_speed": 0.15,
        "description": "Mehr Glueck beim Angeln, schneller schwimmen"
    },
    SlimeType.BLITZ: {
        "movement_speed": 0.15,
        "crafting_speed": 0.10,
        "description": "Schnellere Bewegung und Crafting"
    },
    SlimeType.GIFT: {
        "poison_immunity": 0.50,
        "stealth": 0.20,
        "description": "Gift-Resistenz, besser verstecken"
    },
    SlimeType.MAGMA: {
        "smithing_bonus": 0.25,
        "fire_resistance": 0.20,
        "description": "Besseres Schmieden, Feuer-Schutz"
    },
    SlimeType.SAND: {
        "treasure_find": 0.25,
        "trade_discount": 0.05,
        "description": "Findet versteckte Schaetze, Handelsrabatt"
    },
    SlimeType.KRISTALL: {
        "mining_speed": 0.20,
        "light_radius": 0.50,
        "description": "Schnelleres Mining, leuchtet im Dunkeln"
    },
    SlimeType.GOETTER: {
        "all_bonus": 0.10,
        "luck": 0.20,
        "description": "Kleiner Bonus auf ALLES! (Sehr selten)"
    },
}

# Slime Farben
SLIME_COLORS = {
    SlimeType.MOOS: "#4CAF50",      # Gruen
    SlimeType.FROST: "#81D4FA",     # Hellblau
    SlimeType.WASSER: "#2196F3",    # Blau
    SlimeType.BLITZ: "#9C27B0",     # Lila
    SlimeType.GIFT: "#1B5E20",      # Dunkelgruen
    SlimeType.MAGMA: "#FF5722",     # Orange-Rot
    SlimeType.SAND: "#FFD54F",      # Gold
    SlimeType.KRISTALL: "#E0E0E0",  # Transparent/Weiss
    SlimeType.GOETTER: "rainbow",   # Regenbogen!
}

# Region zu Slime-Typ Mapping
REGION_TO_SLIME = {
    "samtmoos_tiefwald": SlimeType.MOOS,
    "reich_der_drei": SlimeType.FROST,
    "salzwind_kueste": SlimeType.WASSER,
    "blitzebene": SlimeType.BLITZ,
    "gruenschlamm_sumpf": SlimeType.GIFT,
    "magmastroeme": SlimeType.MAGMA,
    "heisse_duenen": SlimeType.SAND,
    "tiefenhoehlen": SlimeType.KRISTALL,
    "goetterfels": SlimeType.GOETTER,
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SlimeState:
    """Vollstaendiger Zustand eines Slimes (V-Pet Style)"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Schleim"
    slime_type: str = SlimeType.MOOS.value
    stage: int = EvolutionStage.EGG.value
    level: int = 1
    plus_value: int = 0  # Synthese-Generationen (+N)

    # V-Pet Herzen (Max 4)
    hunger_hearts: int = 4
    strength_hearts: int = 4

    # Care Stats
    care_mistakes: int = 0
    effort_hearts: int = 0  # Alle 4 Trainings = 1 Effort Heart
    training_count: int = 0

    # Battle Stats (OPTIONAL!)
    battles: int = 0
    wins: int = 0

    # Zeitstempel
    birth_time: float = field(default_factory=time.time)
    last_fed: float = field(default_factory=time.time)
    last_trained: float = field(default_factory=time.time)
    last_played: float = field(default_factory=time.time)
    evolution_time: float = 0  # Wann naechste Evolution moeglich

    # Vererbte Skills (von Synthese)
    skills: List[str] = field(default_factory=list)
    inherited_from: List[str] = field(default_factory=list)

    # Zustand
    is_sleeping: bool = False
    injuries: int = 0
    is_alive: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary fuer JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "slime_type": self.slime_type,
            "stage": self.stage,
            "stage_name": EvolutionStage(self.stage).name,
            "level": self.level,
            "plus_value": self.plus_value,
            "hunger_hearts": self.hunger_hearts,
            "strength_hearts": self.strength_hearts,
            "care_mistakes": self.care_mistakes,
            "effort_hearts": self.effort_hearts,
            "training_count": self.training_count,
            "battles": self.battles,
            "wins": self.wins,
            "win_rate": self.wins / max(self.battles, 1),
            "birth_time": self.birth_time,
            "age_hours": (time.time() - self.birth_time) / 3600,
            "last_fed": self.last_fed,
            "last_trained": self.last_trained,
            "last_played": self.last_played,
            "evolution_time": self.evolution_time,
            "can_evolve": time.time() >= self.evolution_time and self.stage < 6,
            "skills": self.skills,
            "inherited_from": self.inherited_from,
            "is_sleeping": self.is_sleeping,
            "injuries": self.injuries,
            "is_alive": self.is_alive,
            "passive_bonuses": self._get_passive_bonuses(),
            "color": SLIME_COLORS.get(SlimeType(self.slime_type), "#888888"),
        }

    def _get_passive_bonuses(self) -> Dict[str, Any]:
        """Berechnet aktuelle passive Boni basierend auf Stage und Plus"""
        try:
            base_bonus = PASSIVE_BONUSES.get(SlimeType(self.slime_type), {}).copy()
            # Boni skalieren mit Stage und Plus-Wert
            multiplier = 1.0 + (self.stage * 0.1) + (self.plus_value * 0.05)
            for key in base_bonus:
                if isinstance(base_bonus[key], (int, float)):
                    base_bonus[key] = round(base_bonus[key] * multiplier, 3)
            return base_bonus
        except:
            return {}


# =============================================================================
# SLIME COMPANION SYSTEM
# =============================================================================

class SlimeCompanionSystem:
    """
    Haupt-System fuer Slime Companions

    Kombiniert:
    - Digimon V-Pet: Pflege, Care Mistakes, Evolution
    - Dragon Quest Monsters: Synthese, +N System
    - Fortnite Begleiter: Folgt Spieler, hilft
    - Skyrim: ALLES OPTIONAL!
    """

    def __init__(self, save_path: str = "saves/slimes.json"):
        self.save_path = save_path
        self.slimes: Dict[str, SlimeState] = {}
        self.active_slime_id: Optional[str] = None
        self.load()

    # =========================================================================
    # SAVE/LOAD
    # =========================================================================

    def save(self):
        """Speichert alle Slimes"""
        data = {
            "slimes": {sid: s.to_dict() for sid, s in self.slimes.items()},
            "active_slime_id": self.active_slime_id,
            "saved_at": time.time()
        }
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[SlimeSystem] Save Error: {e}")

    def load(self):
        """Laedt alle Slimes"""
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for sid, sdata in data.get("slimes", {}).items():
                slime = SlimeState(
                    id=sdata.get("id", sid),
                    name=sdata.get("name", "Schleim"),
                    slime_type=sdata.get("slime_type", SlimeType.MOOS.value),
                    stage=sdata.get("stage", 1),
                    level=sdata.get("level", 1),
                    plus_value=sdata.get("plus_value", 0),
                    hunger_hearts=sdata.get("hunger_hearts", 4),
                    strength_hearts=sdata.get("strength_hearts", 4),
                    care_mistakes=sdata.get("care_mistakes", 0),
                    effort_hearts=sdata.get("effort_hearts", 0),
                    training_count=sdata.get("training_count", 0),
                    battles=sdata.get("battles", 0),
                    wins=sdata.get("wins", 0),
                    birth_time=sdata.get("birth_time", time.time()),
                    last_fed=sdata.get("last_fed", time.time()),
                    last_trained=sdata.get("last_trained", time.time()),
                    last_played=sdata.get("last_played", time.time()),
                    evolution_time=sdata.get("evolution_time", 0),
                    skills=sdata.get("skills", []),
                    inherited_from=sdata.get("inherited_from", []),
                    is_sleeping=sdata.get("is_sleeping", False),
                    injuries=sdata.get("injuries", 0),
                    is_alive=sdata.get("is_alive", True),
                )
                self.slimes[sid] = slime

            self.active_slime_id = data.get("active_slime_id")
            print(f"[SlimeSystem] Loaded {len(self.slimes)} slimes")
        except FileNotFoundError:
            print("[SlimeSystem] No save file, starting fresh")
        except Exception as e:
            print(f"[SlimeSystem] Load Error: {e}")

    # =========================================================================
    # SLIME CREATION
    # =========================================================================

    def create_egg(self, slime_type: SlimeType, name: str = None) -> SlimeState:
        """
        Erstellt ein neues Schleim-Ei

        Args:
            slime_type: Typ des Schleims (basierend auf Region)
            name: Optionaler Name

        Returns:
            Neuer SlimeState
        """
        slime = SlimeState(
            name=name or f"{slime_type.name.capitalize()}-Ei",
            slime_type=slime_type.value,
            stage=EvolutionStage.EGG.value,
            evolution_time=time.time() + EVOLUTION_TIMES[EvolutionStage.BABY],
        )

        # Basis-Skills je nach Typ
        slime.skills = self._get_base_skills(slime_type)

        self.slimes[slime.id] = slime
        self.save()

        return slime

    def create_from_region(self, region_id: str, name: str = None) -> Optional[SlimeState]:
        """Erstellt Slime basierend auf Region wo gefunden"""
        slime_type = REGION_TO_SLIME.get(region_id)
        if slime_type:
            return self.create_egg(slime_type, name)
        return None

    def _get_base_skills(self, slime_type: SlimeType) -> List[str]:
        """Gibt Basis-Skills fuer einen Slime-Typ zurueck"""
        base_skills = {
            SlimeType.MOOS: ["heal_small", "nature_shield"],
            SlimeType.FROST: ["ice_touch", "freeze"],
            SlimeType.WASSER: ["water_jet", "bubble_shield"],
            SlimeType.BLITZ: ["shock", "speed_boost"],
            SlimeType.GIFT: ["poison_spit", "camouflage"],
            SlimeType.MAGMA: ["fire_ball", "heat_aura"],
            SlimeType.SAND: ["sand_blast", "burrow"],
            SlimeType.KRISTALL: ["light_beam", "crystal_armor"],
            SlimeType.GOETTER: ["divine_light", "miracle"],
        }
        return base_skills.get(slime_type, ["tackle"])

    # =========================================================================
    # CARE SYSTEM (V-Pet Style)
    # =========================================================================

    def feed(self, slime_id: str) -> Dict[str, Any]:
        """
        Fuettert einen Slime

        Returns:
            Status-Dict mit Ergebnis
        """
        slime = self.slimes.get(slime_id)
        if not slime or not slime.is_alive:
            return {"success": False, "message": "Slime nicht gefunden oder tot"}

        if slime.is_sleeping:
            return {"success": False, "message": "Slime schlaeft!"}

        if slime.hunger_hearts >= 4:
            return {"success": False, "message": "Slime ist nicht hungrig"}

        slime.hunger_hearts = min(4, slime.hunger_hearts + 1)
        slime.last_fed = time.time()
        self.save()

        return {
            "success": True,
            "message": f"{slime.name} wurde gefuettert!",
            "hunger_hearts": slime.hunger_hearts
        }

    def train(self, slime_id: str) -> Dict[str, Any]:
        """
        Trainiert einen Slime (erhoet Effort Hearts)

        Alle 4 Trainings = 1 Effort Heart (Digimon-Style)
        """
        slime = self.slimes.get(slime_id)
        if not slime or not slime.is_alive:
            return {"success": False, "message": "Slime nicht gefunden oder tot"}

        if slime.is_sleeping:
            return {"success": False, "message": "Slime schlaeft!"}

        # Training kostet 1 Strength Heart
        if slime.strength_hearts < 1:
            return {"success": False, "message": "Slime ist zu muede zum trainieren!"}

        slime.strength_hearts -= 1
        slime.training_count += 1
        slime.last_trained = time.time()

        # Alle 4 Trainings = 1 Effort Heart
        if slime.training_count % 4 == 0:
            slime.effort_hearts += 1

        # Level-Up Chance bei Training
        if random.random() < 0.1:  # 10% Chance
            slime.level += 1

        self.save()

        return {
            "success": True,
            "message": f"{slime.name} hat trainiert!",
            "strength_hearts": slime.strength_hearts,
            "training_count": slime.training_count,
            "effort_hearts": slime.effort_hearts
        }

    def play(self, slime_id: str) -> Dict[str, Any]:
        """Spielen mit Slime (erhoet Strength Hearts)"""
        slime = self.slimes.get(slime_id)
        if not slime or not slime.is_alive:
            return {"success": False, "message": "Slime nicht gefunden oder tot"}

        if slime.is_sleeping:
            return {"success": False, "message": "Slime schlaeft!"}

        if slime.strength_hearts >= 4:
            return {"success": False, "message": "Slime ist schon fit genug!"}

        slime.strength_hearts = min(4, slime.strength_hearts + 1)
        slime.last_played = time.time()
        self.save()

        return {
            "success": True,
            "message": f"{slime.name} hat gespielt!",
            "strength_hearts": slime.strength_hearts
        }

    def sleep(self, slime_id: str, wake: bool = False) -> Dict[str, Any]:
        """Slime schlafen legen oder aufwecken"""
        slime = self.slimes.get(slime_id)
        if not slime or not slime.is_alive:
            return {"success": False, "message": "Slime nicht gefunden oder tot"}

        if wake:
            if not slime.is_sleeping:
                return {"success": False, "message": "Slime schlaeft nicht"}
            slime.is_sleeping = False
            # Aufwachen regeneriert
            slime.hunger_hearts = min(4, slime.hunger_hearts + 2)
            slime.strength_hearts = 4
        else:
            if slime.is_sleeping:
                return {"success": False, "message": "Slime schlaeft bereits"}
            slime.is_sleeping = True

        self.save()
        return {
            "success": True,
            "message": f"{slime.name} {'ist aufgewacht' if wake else 'schlaeft jetzt'}!",
            "is_sleeping": slime.is_sleeping
        }

    def heal(self, slime_id: str) -> Dict[str, Any]:
        """Heilt Verletzungen"""
        slime = self.slimes.get(slime_id)
        if not slime or not slime.is_alive:
            return {"success": False, "message": "Slime nicht gefunden oder tot"}

        if slime.injuries == 0:
            return {"success": False, "message": "Slime ist nicht verletzt"}

        slime.injuries = 0
        self.save()

        return {
            "success": True,
            "message": f"{slime.name} wurde geheilt!",
            "injuries": 0
        }

    # =========================================================================
    # UPDATE LOOP (Called periodically)
    # =========================================================================

    def update(self) -> List[Dict[str, Any]]:
        """
        Periodischer Update fuer alle Slimes

        Returns:
            Liste von Events (Care Mistakes, Hungrig, etc.)
        """
        events = []
        current_time = time.time()

        for slime_id, slime in self.slimes.items():
            if not slime.is_alive:
                continue

            # Hunger-Check (alle 30 Min verliert 1 Herz wenn wach)
            if not slime.is_sleeping:
                time_since_fed = current_time - slime.last_fed
                hearts_to_lose = int(time_since_fed / 1800)  # 30 Min = 1 Herz

                if hearts_to_lose > 0 and slime.hunger_hearts > 0:
                    old_hearts = slime.hunger_hearts
                    slime.hunger_hearts = max(0, slime.hunger_hearts - hearts_to_lose)
                    slime.last_fed = current_time  # Reset timer

                    if slime.hunger_hearts == 0:
                        # Care Mistake wenn Hunger auf 0!
                        slime.care_mistakes += 1
                        events.append({
                            "type": "care_mistake",
                            "slime_id": slime_id,
                            "slime_name": slime.name,
                            "reason": "hunger",
                            "care_mistakes": slime.care_mistakes
                        })
                    elif slime.hunger_hearts <= 1:
                        events.append({
                            "type": "hungry",
                            "slime_id": slime_id,
                            "slime_name": slime.name,
                            "hunger_hearts": slime.hunger_hearts
                        })

            # Tod-Check
            if slime.injuries >= 20:
                slime.is_alive = False
                events.append({
                    "type": "death",
                    "slime_id": slime_id,
                    "slime_name": slime.name,
                    "reason": "injuries"
                })
            elif slime.care_mistakes >= 10:
                slime.is_alive = False
                events.append({
                    "type": "death",
                    "slime_id": slime_id,
                    "slime_name": slime.name,
                    "reason": "neglect"
                })

            # Evolution-Check
            if slime.stage < 6 and current_time >= slime.evolution_time:
                events.append({
                    "type": "evolution_ready",
                    "slime_id": slime_id,
                    "slime_name": slime.name,
                    "current_stage": slime.stage,
                    "next_stage": slime.stage + 1
                })

        self.save()
        return events

    # =========================================================================
    # GETTERS
    # =========================================================================

    def get_slime(self, slime_id: str) -> Optional[Dict[str, Any]]:
        """Gibt Slime-Status als Dict zurueck"""
        slime = self.slimes.get(slime_id)
        if slime:
            return slime.to_dict()
        return None

    def get_active_slime(self) -> Optional[Dict[str, Any]]:
        """Gibt aktiven Slime zurueck"""
        if self.active_slime_id:
            return self.get_slime(self.active_slime_id)
        return None

    def get_all_slimes(self) -> List[Dict[str, Any]]:
        """Gibt alle Slimes zurueck"""
        return [s.to_dict() for s in self.slimes.values()]

    def set_active_slime(self, slime_id: str) -> bool:
        """Setzt aktiven Begleiter-Slime"""
        if slime_id in self.slimes:
            self.active_slime_id = slime_id
            self.save()
            return True
        return False

    def get_passive_bonuses(self) -> Dict[str, float]:
        """Gibt kombinierte passive Boni aller aktiven Slimes zurueck"""
        bonuses = {}
        if self.active_slime_id:
            slime = self.slimes.get(self.active_slime_id)
            if slime and slime.is_alive:
                bonuses = slime._get_passive_bonuses()
        return bonuses

    # =========================================================================
    # RENAME
    # =========================================================================

    def rename(self, slime_id: str, new_name: str) -> Dict[str, Any]:
        """Benennt einen Slime um"""
        slime = self.slimes.get(slime_id)
        if not slime:
            return {"success": False, "message": "Slime nicht gefunden"}

        old_name = slime.name
        slime.name = new_name
        self.save()

        return {
            "success": True,
            "message": f"{old_name} heisst jetzt {new_name}!",
            "old_name": old_name,
            "new_name": new_name
        }

    # =========================================================================
    # BATTLE (OPTIONAL!)
    # =========================================================================

    def record_battle(self, slime_id: str, won: bool) -> Dict[str, Any]:
        """
        Zeichnet einen Kampf auf (NUR wenn Spieler kaempfen WILL!)

        WICHTIG: Kaempfe sind OPTIONAL! Diese Funktion wird nur aufgerufen
        wenn der Spieler aktiv Monster-Kaempfe waehlt!
        """
        slime = self.slimes.get(slime_id)
        if not slime or not slime.is_alive:
            return {"success": False, "message": "Slime nicht gefunden oder tot"}

        slime.battles += 1
        if won:
            slime.wins += 1
            # Level-Up Chance bei Sieg
            if random.random() < 0.2:  # 20% Chance
                slime.level += 1
        else:
            # Verletzung bei Niederlage
            slime.injuries += 1

        self.save()

        return {
            "success": True,
            "message": f"{slime.name} hat {'gewonnen' if won else 'verloren'}!",
            "battles": slime.battles,
            "wins": slime.wins,
            "win_rate": slime.wins / slime.battles,
            "injuries": slime.injuries
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_slime_system: Optional[SlimeCompanionSystem] = None

def get_slime_system() -> SlimeCompanionSystem:
    """Gibt Singleton-Instanz zurueck"""
    global _slime_system
    if _slime_system is None:
        _slime_system = SlimeCompanionSystem()
    return _slime_system


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA SLIME COMPANION SYSTEM - TEST")
    print("=" * 60)

    system = get_slime_system()

    # Test: Neues Ei erstellen
    print("\n[TEST] Erstelle Moos-Schleim Ei...")
    slime = system.create_egg(SlimeType.MOOS, "Moosy")
    print(f"  Erstellt: {slime.name} (ID: {slime.id[:8]}...)")
    print(f"  Typ: {slime.slime_type}")
    print(f"  Skills: {slime.skills}")

    # Test: Fuettern
    print("\n[TEST] Fuettern...")
    result = system.feed(slime.id)
    print(f"  {result['message']}")

    # Test: Trainieren
    print("\n[TEST] Trainieren...")
    for i in range(5):
        result = system.train(slime.id)
        print(f"  Training {i+1}: Effort Hearts = {result.get('effort_hearts', 0)}")

    # Test: Status
    print("\n[TEST] Status...")
    status = system.get_slime(slime.id)
    print(f"  Name: {status['name']}")
    print(f"  Stage: {status['stage_name']}")
    print(f"  Level: {status['level']}")
    print(f"  Hunger: {status['hunger_hearts']}/4")
    print(f"  Strength: {status['strength_hearts']}/4")
    print(f"  Care Mistakes: {status['care_mistakes']}")
    print(f"  Effort Hearts: {status['effort_hearts']}")
    print(f"  Passive Boni: {status['passive_bonuses']}")

    print("\n" + "=" * 60)
    print("TEST ABGESCHLOSSEN")
    print("=" * 60)
