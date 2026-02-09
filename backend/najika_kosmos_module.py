#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA KOSMOS - MODUL-SYSTEM
=============================
Das zentrale Framework fuer alle Najika-Module.

VISION:
"Schaffe dir was auch immer du willst.
 Dein Leben. Dein Begleiter. Dein Spiel.
 Von Kleinkind bis Senior - wann du willst, wie du willst."

ARCHITEKTUR:
┌─────────────────────────────────────────────────────────────┐
│                    NAJIKA KOSMOS                            │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              KERN: SLIME-KI (LLM)                     │  │
│  │      Begleitet dich dein GANZES Leben                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                  │
│     ┌────────────────────┼────────────────────┐            │
│     ▼                    ▼                    ▼            │
│  MODULE           MODULE           MODULE                  │
│  (beliebig erweiterbar)                                    │
└─────────────────────────────────────────────────────────────┘

Author: Claude Code Team
Date: 2026-02-02
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Type
from datetime import datetime
import json
import importlib


# =============================================================================
# ENUMS
# =============================================================================

class ModuleCategory(Enum):
    """Kategorien von Modulen"""
    CORE = "core"               # Kern-Module (immer aktiv)
    SECURITY = "security"       # Sicherheitsmodule
    GAME = "game"               # Spiel-Module
    PRODUCTIVITY = "productivity"  # Produktivitaet
    LEARNING = "learning"       # Lern-Module
    FITNESS = "fitness"         # Fitness & Gesundheit
    SOCIAL = "social"           # Soziale Module
    LIFESTYLE = "lifestyle"     # Lifestyle (Senior, etc.)
    INTEGRATION = "integration" # Externe Integrationen (Fortnite, etc.)


class ModuleStatus(Enum):
    """Status eines Moduls"""
    ACTIVE = "active"           # Aktiv und laufend
    INACTIVE = "inactive"       # Installiert aber inaktiv
    NOT_INSTALLED = "not_installed"  # Nicht installiert
    ERROR = "error"             # Fehler beim Laden
    UPDATING = "updating"       # Wird aktualisiert


class LifePhase(Enum):
    """Lebensphasen des Nutzers"""
    CHILD = "child"             # 0-12 Jahre
    TEENAGER = "teenager"       # 13-19 Jahre
    ADULT = "adult"             # 20-60 Jahre
    SENIOR = "senior"           # 60+ Jahre


# =============================================================================
# MODULE DEFINITION
# =============================================================================

@dataclass
class ModuleInfo:
    """Informationen ueber ein Modul"""
    module_id: str
    name: str
    name_de: str
    description: str
    description_de: str
    category: ModuleCategory
    version: str = "1.0.0"

    # Anforderungen
    requires_modules: List[str] = field(default_factory=list)
    compatible_phases: List[LifePhase] = field(default_factory=lambda: list(LifePhase))

    # Technisch
    entry_point: str = ""  # Python module path
    api_prefix: str = ""   # API Prefix (z.B. "/api/messenger")
    config_schema: Dict[str, Any] = field(default_factory=dict)

    # Status
    status: ModuleStatus = ModuleStatus.NOT_INSTALLED
    installed_at: Optional[datetime] = None
    last_used: Optional[datetime] = None

    # Statistiken
    usage_count: int = 0
    total_time_used: float = 0.0  # In Stunden


# =============================================================================
# BESTEHENDE MODULE (Bereits implementiert!)
# =============================================================================

EXISTING_MODULES = {
    # ===== KERN-MODULE =====
    "slime_core": ModuleInfo(
        module_id="slime_core",
        name="Slime Core",
        name_de="Slime-Kern",
        description="The core Slime AI companion system",
        description_de="Das zentrale Slime-KI Begleiter-System",
        category=ModuleCategory.CORE,
        version="2.0.0",
        entry_point="najika_slime_system",
        api_prefix="/api/slime",
        status=ModuleStatus.ACTIVE
    ),
    "companion_system": ModuleInfo(
        module_id="companion_system",
        name="Companion System",
        name_de="Begleiter-System",
        description="Najika as AI companion for Kuja",
        description_de="Najika als KI-Partnerin fuer Kuja",
        category=ModuleCategory.CORE,
        version="1.0.0",
        entry_point="najika_companion_system",
        api_prefix="/api/companion",
        status=ModuleStatus.ACTIVE
    ),
    "memory_system": ModuleInfo(
        module_id="memory_system",
        name="Memory System",
        name_de="Gedaechtnis-System",
        description="ChromaDB-based persistent memory",
        description_de="ChromaDB-basiertes persistentes Gedaechtnis",
        category=ModuleCategory.CORE,
        version="1.5.0",
        entry_point="najika_memory_enhanced",
        api_prefix="/api/memory",
        status=ModuleStatus.ACTIVE
    ),

    # ===== SICHERHEITS-MODULE =====
    "secure_messenger": ModuleInfo(
        module_id="secure_messenger",
        name="Secure Messenger",
        name_de="Sicherer Messenger",
        description="E2E encrypted messaging with Signal Protocol + Post-Quantum",
        description_de="E2E verschluesselte Nachrichten mit Signal Protocol + Post-Quantum",
        category=ModuleCategory.SECURITY,
        version="1.0.0",
        entry_point="sicherheitsmodule.backend.najika_messenger_server",
        api_prefix="/api/messenger",
        status=ModuleStatus.ACTIVE
    ),
    "secure_browser": ModuleInfo(
        module_id="secure_browser",
        name="Secure Browser",
        name_de="Sicherer Browser",
        description="Firefox remote control with Tor/VPN profiles",
        description_de="Firefox Fernsteuerung mit Tor/VPN Profilen",
        category=ModuleCategory.SECURITY,
        version="1.0.0",
        entry_point="sicherheitsmodule.backend.najika_browser_api",
        api_prefix="/api/browser",
        status=ModuleStatus.ACTIVE
    ),
    "tor_integration": ModuleInfo(
        module_id="tor_integration",
        name="Tor Integration",
        name_de="Tor-Integration",
        description="Darknet access and anonymity",
        description_de="Darknet-Zugriff und Anonymitaet",
        category=ModuleCategory.SECURITY,
        version="1.0.0",
        entry_point="najika_tor",
        api_prefix="/api/tor",
        status=ModuleStatus.ACTIVE
    ),
    "alcatraz_security": ModuleInfo(
        module_id="alcatraz_security",
        name="Alcatraz Security",
        name_de="Alcatraz-Sicherheit",
        description="Owner-Token, Zero-Trust architecture",
        description_de="Owner-Token, Zero-Trust Architektur",
        category=ModuleCategory.SECURITY,
        version="1.0.0",
        entry_point="najika_security",
        api_prefix="/api/security",
        status=ModuleStatus.ACTIVE
    ),

    # ===== HAUPTSPIEL (Najika World) =====
    # ALLE Spiel-Features sind TEIL von Najika World, keine separaten Module!
    "najika_world": ModuleInfo(
        module_id="najika_world",
        name="Najika World",
        name_de="Najika World (HAUPTSPIEL)",
        description="3D Action-RPG with Open World, Combat, V-Pet, Minigames, Crafting - ALL IN ONE!",
        description_de="3D Action-RPG mit Open World, Kampf, V-Pet, Minispiele, Crafting - ALLES IN EINEM!",
        category=ModuleCategory.GAME,
        version="0.9.0",
        entry_point="najika_server",
        api_prefix="/api",
        status=ModuleStatus.ACTIVE
        # HINWEIS: Najika World ENTHAELT alle Spiel-Features:
        # - V-Pet/Slime System
        # - Minigames (Triple Triad, DDM, Ocarina)
        # - Combat System (Zwei-Hand, Magie)
        # - Mimik-Truhe (Kuja's Charakter)
        # - Oregon Trail Events
        # - Housing, Crafting, Quests, etc.
        # Diese sind KEINE separaten Module!
    ),

    # ===== DIGIVICE APP =====
    "digivice_app": ModuleInfo(
        module_id="digivice_app",
        name="Digivice App",
        name_de="Digivice App",
        description="Mobile companion app with Chat, V-Pet care, Minigames",
        description_de="Mobile Begleiter-App mit Chat, V-Pet Pflege, Minispielen",
        category=ModuleCategory.CORE,
        version="1.0.0",
        entry_point="najika_server",
        api_prefix="/api",
        status=ModuleStatus.ACTIVE
        # HINWEIS: Digivice App synct mit Najika World!
    ),

    # ===== GEPLANTE MODULE =====
    "fortnite_integration": ModuleInfo(
        module_id="fortnite_integration",
        name="Fortnite Integration",
        name_de="Fortnite-Integration",
        description="Gaming companion for Fortnite",
        description_de="Gaming-Begleiter fuer Fortnite",
        category=ModuleCategory.INTEGRATION,
        version="0.1.0",
        compatible_phases=[LifePhase.TEENAGER, LifePhase.ADULT],
        status=ModuleStatus.NOT_INSTALLED
    ),
    "learning_module": ModuleInfo(
        module_id="learning_module",
        name="Learning Module",
        name_de="Lern-Modul",
        description="Language learning, skills training",
        description_de="Sprachen lernen, Skills trainieren",
        category=ModuleCategory.LEARNING,
        version="0.1.0",
        compatible_phases=[LifePhase.CHILD, LifePhase.TEENAGER, LifePhase.ADULT],
        status=ModuleStatus.NOT_INSTALLED
    ),
    "fitness_module": ModuleInfo(
        module_id="fitness_module",
        name="Fitness Module",
        name_de="Fitness-Modul",
        description="Training, health tracking, challenges",
        description_de="Training, Gesundheits-Tracking, Challenges",
        category=ModuleCategory.FITNESS,
        version="0.1.0",
        compatible_phases=[LifePhase.TEENAGER, LifePhase.ADULT, LifePhase.SENIOR],
        status=ModuleStatus.NOT_INSTALLED
    ),
    "productivity_module": ModuleInfo(
        module_id="productivity_module",
        name="Productivity Module",
        name_de="Produktiv-Modul",
        description="ToDo, Calendar, Notes, Finance",
        description_de="ToDo, Kalender, Notizen, Finanzen",
        category=ModuleCategory.PRODUCTIVITY,
        version="0.1.0",
        compatible_phases=[LifePhase.TEENAGER, LifePhase.ADULT],
        status=ModuleStatus.NOT_INSTALLED
    ),
    "senior_module": ModuleInfo(
        module_id="senior_module",
        name="Senior Module",
        name_de="Senior-Modul",
        description="Memories, Family Chronicle, Life Story",
        description_de="Erinnerungen, Familienchronik, Lebensgeschichte",
        category=ModuleCategory.LIFESTYLE,
        version="0.1.0",
        compatible_phases=[LifePhase.SENIOR],
        status=ModuleStatus.NOT_INSTALLED
    ),
}


# =============================================================================
# KOSMOS MANAGER
# =============================================================================

class NajikaKosmos:
    """
    Der zentrale Manager fuer alle Najika-Module.
    Verwaltet das gesamte Oekosystem.
    """

    def __init__(self):
        self.modules: Dict[str, ModuleInfo] = EXISTING_MODULES.copy()
        self.loaded_modules: Dict[str, Any] = {}
        self.user_life_phase: LifePhase = LifePhase.ADULT
        self.user_id: str = "kuja"  # Owner

    # =========================================================================
    # MODUL-VERWALTUNG
    # =========================================================================

    def get_module(self, module_id: str) -> Optional[ModuleInfo]:
        """Holt Modul-Info"""
        return self.modules.get(module_id)

    def get_all_modules(self) -> List[ModuleInfo]:
        """Holt alle Module"""
        return list(self.modules.values())

    def get_modules_by_category(self, category: ModuleCategory) -> List[ModuleInfo]:
        """Holt Module einer Kategorie"""
        return [m for m in self.modules.values() if m.category == category]

    def get_active_modules(self) -> List[ModuleInfo]:
        """Holt alle aktiven Module"""
        return [m for m in self.modules.values() if m.status == ModuleStatus.ACTIVE]

    def get_compatible_modules(self, phase: LifePhase) -> List[ModuleInfo]:
        """Holt Module die zur Lebensphase passen"""
        return [m for m in self.modules.values() if phase in m.compatible_phases]

    # =========================================================================
    # MODUL-AKTIVIERUNG
    # =========================================================================

    def activate_module(self, module_id: str) -> Dict[str, Any]:
        """Aktiviert ein Modul"""
        module = self.modules.get(module_id)
        if not module:
            return {"success": False, "error": "Modul nicht gefunden"}

        if module.status == ModuleStatus.ACTIVE:
            return {"success": True, "message": "Modul bereits aktiv"}

        # Abhaengigkeiten pruefen
        for req in module.requires_modules:
            req_module = self.modules.get(req)
            if not req_module or req_module.status != ModuleStatus.ACTIVE:
                return {
                    "success": False,
                    "error": f"Benoetigt Modul: {req}"
                }

        # Aktivieren
        module.status = ModuleStatus.ACTIVE
        module.installed_at = datetime.now()

        return {
            "success": True,
            "module_id": module_id,
            "name": module.name_de,
            "status": "active"
        }

    def deactivate_module(self, module_id: str) -> Dict[str, Any]:
        """Deaktiviert ein Modul"""
        module = self.modules.get(module_id)
        if not module:
            return {"success": False, "error": "Modul nicht gefunden"}

        # Kern-Module koennen nicht deaktiviert werden
        if module.category == ModuleCategory.CORE:
            return {"success": False, "error": "Kern-Module koennen nicht deaktiviert werden"}

        module.status = ModuleStatus.INACTIVE

        return {
            "success": True,
            "module_id": module_id,
            "status": "inactive"
        }

    # =========================================================================
    # LEBENSPHASE
    # =========================================================================

    def set_life_phase(self, phase: LifePhase) -> Dict[str, Any]:
        """Setzt die Lebensphase des Nutzers"""
        old_phase = self.user_life_phase
        self.user_life_phase = phase

        # Empfohlene Module fuer diese Phase
        recommended = self.get_compatible_modules(phase)

        return {
            "success": True,
            "old_phase": old_phase.value,
            "new_phase": phase.value,
            "recommended_modules": [m.module_id for m in recommended if m.status == ModuleStatus.NOT_INSTALLED]
        }

    # =========================================================================
    # STATISTIKEN
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Holt Kosmos-Statistiken"""
        modules_by_status = {}
        for status in ModuleStatus:
            modules_by_status[status.value] = len([m for m in self.modules.values() if m.status == status])

        modules_by_category = {}
        for category in ModuleCategory:
            modules_by_category[category.value] = len([m for m in self.modules.values() if m.category == category])

        return {
            "total_modules": len(self.modules),
            "by_status": modules_by_status,
            "by_category": modules_by_category,
            "user_life_phase": self.user_life_phase.value,
            "active_count": modules_by_status.get("active", 0)
        }

    def get_module_summary(self) -> Dict[str, Any]:
        """Kurzuebersicht aller Module"""
        summary = {
            "core": [],
            "security": [],
            "game": [],
            "planned": []
        }

        for module in self.modules.values():
            entry = {
                "id": module.module_id,
                "name": module.name_de,
                "status": module.status.value,
                "version": module.version
            }

            if module.category == ModuleCategory.CORE:
                summary["core"].append(entry)
            elif module.category == ModuleCategory.SECURITY:
                summary["security"].append(entry)
            elif module.category == ModuleCategory.GAME:
                summary["game"].append(entry)
            elif module.status == ModuleStatus.NOT_INSTALLED:
                summary["planned"].append(entry)

        return summary


# =============================================================================
# SINGLETON
# =============================================================================

_kosmos: Optional[NajikaKosmos] = None

def get_kosmos() -> NajikaKosmos:
    """Singleton fuer den Najika Kosmos"""
    global _kosmos
    if _kosmos is None:
        _kosmos = NajikaKosmos()
    return _kosmos


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA KOSMOS - MODUL-SYSTEM TEST")
    print("=" * 60)

    kosmos = get_kosmos()

    # Statistiken
    print("\n--- Kosmos Statistiken ---")
    stats = kosmos.get_stats()
    print(f"Total Module: {stats['total_modules']}")
    print(f"Aktive Module: {stats['active_count']}")
    print(f"Lebensphase: {stats['user_life_phase']}")

    # Module nach Kategorie
    print("\n--- Module nach Kategorie ---")
    for cat in ModuleCategory:
        modules = kosmos.get_modules_by_category(cat)
        if modules:
            print(f"\n{cat.value.upper()}:")
            for m in modules:
                status_icon = "aktiv" if m.status == ModuleStatus.ACTIVE else "geplant"
                print(f"  - {m.name_de} ({status_icon})")

    # Aktive Module
    print("\n--- Aktive Module ---")
    active = kosmos.get_active_modules()
    for m in active:
        print(f"  [{m.category.value}] {m.name_de} v{m.version}")

    # Modul-Zusammenfassung
    print("\n--- Modul-Zusammenfassung ---")
    summary = kosmos.get_module_summary()
    print(f"Kern: {len(summary['core'])} Module")
    print(f"Sicherheit: {len(summary['security'])} Module")
    print(f"Spiele: {len(summary['game'])} Module")
    print(f"Geplant: {len(summary['planned'])} Module")

    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
