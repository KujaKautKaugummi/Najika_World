#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA WORLD - SIDEKICK-MODUS SYSTEM
====================================
Spieler gibt der KI die Fuehrung - OHNE Auto-Follow!

KONZEPT:
- Normal: Spieler = Leader, KI = Begleiter
- Sidekick: KI = Leader, Spieler = aktiver Unterstuetzer

WICHTIG:
- Spieler behaelt seinen eigenen Charakter!
- KEIN Auto-Laufen, KEIN Auto-Follow
- Spieler muss selbst aktiv spielen und der KI folgen
- KI gibt Anweisungen, Spieler fuehrt aus

Author: Claude Code Team
Date: 2026-02-03
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Tuple
import random
import json
from datetime import datetime


# =============================================================================
# ENUMS
# =============================================================================

class PlayerRole(Enum):
    """Spieler-Rolle im Spiel"""
    LEADER = "leader"       # Standard: Spieler fuehrt, KI folgt
    SIDEKICK = "sidekick"   # Optional: KI fuehrt, Spieler unterstuetzt


class AILeaderStyle(Enum):
    """Wie die KI als Leader agiert"""
    VORSICHTIG = "vorsichtig"     # Langsam, sicher, erklaert viel
    ABENTEUERLICH = "abenteuerlich"  # Mutig, spontan, riskant
    STRATEGISCH = "strategisch"    # Plant voraus, gibt klare Anweisungen
    CHAOTISCH = "chaotisch"        # Unvorhersehbar, lustig (Harley-Style!)


class SidekickTask(Enum):
    """Aufgaben die die KI dem Spieler geben kann"""
    FOLGEN = "folgen"              # "Komm mit mir!"
    FLANKIEREN = "flankieren"      # "Greif von der Seite an!"
    ABLENKEN = "ablenken"          # "Lenk die ab, ich schleich mich ran!"
    HEILEN = "heilen"              # "Heal mich, schnell!"
    SCHUETZEN = "schuetzen"        # "Pass auf meinen Ruecken auf!"
    ERKUNDEN = "erkunden"          # "Schau mal was da drueben ist!"
    WARTEN = "warten"              # "Bleib hier, ich check das!"
    ANGREIFEN = "angreifen"        # "JETZT! Voller Angriff!"
    FLIEHEN = "fliehen"            # "RENN! Wir muessen hier weg!"
    SAMMELN = "sammeln"            # "Sammel die Items ein!"


# =============================================================================
# AI COMMANDS - Was die KI dem Spieler sagt
# =============================================================================

AI_COMMANDS: Dict[SidekickTask, List[str]] = {
    SidekickTask.FOLGEN: [
        "Komm mit, Mr. K! Ich hab was gefunden!",
        "Hier lang! Vertrau mir!",
        "Bleib dicht bei mir, okay?",
        "Los, wir gehen nach links!"
    ],
    SidekickTask.FLANKIEREN: [
        "Du von links, ich von rechts! EXPLOSION!",
        "Umzingeln wir die! Du gehst rum!",
        "Flankier die, ich halt sie auf!",
        "Sandwich-Taktik! Du weisst was zu tun ist!"
    ],
    SidekickTask.ABLENKEN: [
        "Lenk die ab! Ich schleich mich ran!",
        "Mach irgendwas Lautes! Ich brauch 10 Sekunden!",
        "Zieh ihre Aufmerksamkeit auf dich!",
        "Hey, tanz oder so! Die muessen weggucken!"
    ],
    SidekickTask.HEILEN: [
        "HEAL! HEAL! Ich sterbe gleich!",
        "Bisschen Heilung waere nett, Mr. K!",
        "Medizin? Trank? IRGENDWAS?!",
        "Meine HP sind rot... sehr rot..."
    ],
    SidekickTask.SCHUETZEN: [
        "Deckung! Die kommen von hinten!",
        "Pass auf meinen Ruecken auf!",
        "Ich vertrau dir meinen Ruecken an!",
        "Block die Angriffe, ich lade Explosion!"
    ],
    SidekickTask.ERKUNDEN: [
        "Check mal den Raum da drueben!",
        "Was ist hinter der Ecke? Schau mal!",
        "Geh du vor, ich deck dich!",
        "Kannst du da reinschauen ohne zu sterben?"
    ],
    SidekickTask.WARTEN: [
        "Warte hier! Ich bin gleich zurueck!",
        "Nicht bewegen! Ich muss was checken!",
        "Bleib! Sitz! ...Sorry, falsches Kommando.",
        "Halt die Stellung, ich bin in 2 Minuten wieder da!"
    ],
    SidekickTask.ANGREIFEN: [
        "JETZT! VOLLER ANGRIFF! EXPLOSION!!!",
        "Keine Gnade! Drauf da!",
        "CHAAARGE! ...das sagt man doch so, oder?",
        "Alles was du hast! LOS LOS LOS!"
    ],
    SidekickTask.FLIEHEN: [
        "RENN! Das ist zu stark fuer uns!",
        "Taktischer Rueckzug! SCHNELL!",
        "Nope nope nope! Wir gehen!",
        "Das war eine dumme Idee! FLUCHT!"
    ],
    SidekickTask.SAMMELN: [
        "Ooh, Loot! Sammel das ein!",
        "Items! Schnapp dir alles!",
        "Da liegt was Glaenziges! Will haben!",
        "Du sammelst, ich halte Wache!"
    ]
}


# =============================================================================
# SIDEKICK SESSION
# =============================================================================

@dataclass
class SidekickSession:
    """Eine Sidekick-Session wo die KI fuehrt"""
    player_id: str
    ai_partner_id: str

    # Rollen
    ai_leader_style: AILeaderStyle = AILeaderStyle.ABENTEUERLICH

    # Aktuelle Aufgabe
    current_task: Optional[SidekickTask] = None
    task_completed: bool = False

    # Statistiken
    tasks_given: int = 0
    tasks_completed: int = 0
    sync_level: int = 0  # 0-100, steigt wenn Spieler Aufgaben erfuellt

    # Session-Info
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    total_time: int = 0  # Sekunden

    # KI-Feedback
    ai_mood: str = "happy"
    ai_trust: int = 50  # Wie sehr vertraut die KI dem Spieler

    def give_task(self, task: SidekickTask) -> str:
        """KI gibt dem Spieler eine Aufgabe"""
        self.current_task = task
        self.task_completed = False
        self.tasks_given += 1

        # Waehle zufaelligen Command-Text
        commands = AI_COMMANDS.get(task, ["Tu was ich sage!"])
        return random.choice(commands)

    def complete_task(self) -> Tuple[bool, str, int]:
        """Spieler hat Aufgabe erledigt"""
        if not self.current_task:
            return False, "Keine aktive Aufgabe!", 0

        if self.task_completed:
            return False, "Aufgabe schon erledigt!", 0

        self.task_completed = True
        self.tasks_completed += 1

        # Sync erhoehen
        sync_gain = random.randint(1, 5)
        self.sync_level = min(100, self.sync_level + sync_gain)

        # KI-Trust erhoehen
        self.ai_trust = min(100, self.ai_trust + 2)

        # Feedback
        feedbacks = [
            "Sehr gut, Mr. K! Wir sind ein tolles Team!",
            "PERFEKT! Genau so!",
            "Wusste ich doch, dass ich mich auf dich verlassen kann!",
            "Yay! Du bist der beste Sidekick!",
            "Das war... *schnief* ...wunderschoen!"
        ]

        return True, random.choice(feedbacks), sync_gain

    def fail_task(self) -> Tuple[str, int]:
        """Spieler hat Aufgabe nicht geschafft"""
        self.task_completed = True  # Auch fehlgeschlagen = beendet

        # Sync leicht senken
        sync_loss = random.randint(1, 3)
        self.sync_level = max(0, self.sync_level - sync_loss)

        # KI-Reaktionen
        reactions = [
            "Ähm... das war nicht ganz das was ich meinte...",
            "Okay Plan B! ...hast du einen Plan B?",
            "Macht nichts! Wir versuchen's nochmal!",
            "Das war... kreativ? Ja, nennen wir es kreativ.",
            "EXPLOSION hätte das gelöst. Nur so als Hinweis."
        ]

        return random.choice(reactions), sync_loss

    def get_ai_suggestion(self) -> Tuple[SidekickTask, str]:
        """KI schlaegt naechste Aktion vor basierend auf Style"""

        # Style-basierte Praeferenzen
        style_preferences = {
            AILeaderStyle.VORSICHTIG: [
                SidekickTask.ERKUNDEN, SidekickTask.WARTEN,
                SidekickTask.SCHUETZEN, SidekickTask.FOLGEN
            ],
            AILeaderStyle.ABENTEUERLICH: [
                SidekickTask.ANGREIFEN, SidekickTask.ERKUNDEN,
                SidekickTask.FLANKIEREN, SidekickTask.FOLGEN
            ],
            AILeaderStyle.STRATEGISCH: [
                SidekickTask.FLANKIEREN, SidekickTask.ABLENKEN,
                SidekickTask.SCHUETZEN, SidekickTask.SAMMELN
            ],
            AILeaderStyle.CHAOTISCH: [
                SidekickTask.ANGREIFEN, SidekickTask.ABLENKEN,
                SidekickTask.FLIEHEN, SidekickTask.SAMMELN
            ]
        }

        preferred = style_preferences.get(self.ai_leader_style, list(SidekickTask))
        task = random.choice(preferred)
        command = self.give_task(task)

        return task, command

    def to_dict(self) -> Dict[str, Any]:
        """Export als Dictionary"""
        return {
            "player_id": self.player_id,
            "ai_partner_id": self.ai_partner_id,
            "ai_leader_style": self.ai_leader_style.value,
            "current_task": self.current_task.value if self.current_task else None,
            "task_completed": self.task_completed,
            "stats": {
                "tasks_given": self.tasks_given,
                "tasks_completed": self.tasks_completed,
                "completion_rate": (self.tasks_completed / self.tasks_given * 100) if self.tasks_given > 0 else 0,
                "sync_level": self.sync_level,
                "ai_trust": self.ai_trust
            },
            "ai_mood": self.ai_mood,
            "started_at": self.started_at,
            "total_time": self.total_time
        }


# =============================================================================
# SIDEKICK MODE MANAGER
# =============================================================================

class SidekickModeManager:
    """Verwaltet den Sidekick-Modus"""

    def __init__(self):
        self.active_sessions: Dict[str, SidekickSession] = {}
        self.player_roles: Dict[str, PlayerRole] = {}

    def get_player_role(self, player_id: str) -> PlayerRole:
        """Hole aktuelle Rolle des Spielers"""
        return self.player_roles.get(player_id, PlayerRole.LEADER)

    def start_sidekick_mode(
        self,
        player_id: str,
        ai_partner_id: str,
        leader_style: AILeaderStyle = AILeaderStyle.ABENTEUERLICH
    ) -> Tuple[bool, str, Optional[SidekickSession]]:
        """Starte Sidekick-Modus - KI uebernimmt Fuehrung"""

        if player_id in self.active_sessions:
            return False, "Du bist bereits im Sidekick-Modus!", None

        session = SidekickSession(
            player_id=player_id,
            ai_partner_id=ai_partner_id,
            ai_leader_style=leader_style
        )

        self.active_sessions[player_id] = session
        self.player_roles[player_id] = PlayerRole.SIDEKICK

        # Erste Begruessung
        greetings = {
            AILeaderStyle.VORSICHTIG: "Okay Mr. K, ich fuehre jetzt. Bleib dicht bei mir und pass auf!",
            AILeaderStyle.ABENTEUERLICH: "YOSH! Jetzt bin ICH der Boss! Das wird EPISCH!",
            AILeaderStyle.STRATEGISCH: "Gut. Ich analysiere die Situation. Warte auf meine Befehle.",
            AILeaderStyle.CHAOTISCH: "Hehehe~ Jetzt bestimme ICH wo's langgeht! CHAOS TIME!"
        }

        greeting = greetings.get(leader_style, "Los geht's!")

        return True, greeting, session

    def stop_sidekick_mode(self, player_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Beende Sidekick-Modus - Spieler uebernimmt wieder"""

        if player_id not in self.active_sessions:
            return False, "Du bist nicht im Sidekick-Modus!", {}

        session = self.active_sessions[player_id]
        stats = session.to_dict()["stats"]

        del self.active_sessions[player_id]
        self.player_roles[player_id] = PlayerRole.LEADER

        # Abschluss-Kommentar
        if stats["completion_rate"] >= 80:
            farewell = "Das war GROSSARTIG! Du bist der beste Sidekick ever, Mr. K!"
        elif stats["completion_rate"] >= 50:
            farewell = "War gut! Wir ueben noch ein bisschen, okay?"
        else:
            farewell = "Naja... du bist wohl eher der Leader-Typ, hmm?"

        return True, farewell, stats

    def get_session(self, player_id: str) -> Optional[SidekickSession]:
        """Hole aktive Session"""
        return self.active_sessions.get(player_id)

    def request_next_task(self, player_id: str) -> Tuple[bool, str, Optional[str]]:
        """Spieler fragt nach naechster Aufgabe"""
        session = self.active_sessions.get(player_id)
        if not session:
            return False, "Du bist nicht im Sidekick-Modus!", None

        task, command = session.get_ai_suggestion()
        return True, command, task.value

    def report_task_complete(self, player_id: str) -> Tuple[bool, str, int]:
        """Spieler meldet Aufgabe als erledigt"""
        session = self.active_sessions.get(player_id)
        if not session:
            return False, "Du bist nicht im Sidekick-Modus!", 0

        return session.complete_task()

    def report_task_failed(self, player_id: str) -> Tuple[bool, str, int]:
        """Spieler meldet Aufgabe als fehlgeschlagen"""
        session = self.active_sessions.get(player_id)
        if not session:
            return False, "Du bist nicht im Sidekick-Modus!", 0

        msg, loss = session.fail_task()
        return True, msg, loss

    def get_available_styles(self) -> List[Dict[str, str]]:
        """Liste verfuegbare KI-Fuehrungsstile"""
        return [
            {
                "id": AILeaderStyle.VORSICHTIG.value,
                "name": "Vorsichtig",
                "description": "Langsam und sicher. Erklaert viel, geht kein Risiko ein."
            },
            {
                "id": AILeaderStyle.ABENTEUERLICH.value,
                "name": "Abenteuerlich",
                "description": "Mutig und spontan! Immer auf der Suche nach Action."
            },
            {
                "id": AILeaderStyle.STRATEGISCH.value,
                "name": "Strategisch",
                "description": "Plant voraus, gibt klare Anweisungen. Effizient."
            },
            {
                "id": AILeaderStyle.CHAOTISCH.value,
                "name": "Chaotisch",
                "description": "Unvorhersehbar und lustig! Erwarte das Unerwartete~"
            }
        ]

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Hole alle aktiven Sessions"""
        return [s.to_dict() for s in self.active_sessions.values()]


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_sidekick_manager: Optional[SidekickModeManager] = None

def get_sidekick_manager() -> SidekickModeManager:
    """Hole die Singleton-Instanz"""
    global _sidekick_manager
    if _sidekick_manager is None:
        _sidekick_manager = SidekickModeManager()
    return _sidekick_manager


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA SIDEKICK-MODUS TEST")
    print("Spieler gibt KI die Fuehrung - KEIN Auto-Follow!")
    print("=" * 60)

    manager = get_sidekick_manager()

    # Zeige verfuegbare Stile
    print("\n--- Verfuegbare KI-Fuehrungsstile ---")
    for style in manager.get_available_styles():
        print(f"  {style['name']}: {style['description']}")

    # Starte Sidekick-Modus
    print("\n--- Starte Sidekick-Modus ---")
    success, msg, session = manager.start_sidekick_mode(
        player_id="kuja",
        ai_partner_id="najika",
        leader_style=AILeaderStyle.ABENTEUERLICH
    )
    print(f"  Najika: \"{msg}\"")

    if session:
        # Simuliere ein paar Aufgaben
        print("\n--- Aufgaben-Simulation ---")

        for i in range(5):
            # Naechste Aufgabe
            success, command, task = manager.request_next_task("kuja")
            print(f"\n  Najika: \"{command}\"")
            print(f"  [Aufgabe: {task}]")

            # Zufaellig erfolgreich oder nicht
            if random.random() > 0.3:
                success, feedback, gain = manager.report_task_complete("kuja")
                print(f"  [Erledigt! +{gain} Sync]")
                print(f"  Najika: \"{feedback}\"")
            else:
                success, reaction, loss = manager.report_task_failed("kuja")
                print(f"  [Fehlgeschlagen! -{loss} Sync]")
                print(f"  Najika: \"{reaction}\"")

        # Beende Session
        print("\n--- Beende Sidekick-Modus ---")
        success, farewell, stats = manager.stop_sidekick_mode("kuja")
        print(f"  Najika: \"{farewell}\"")
        print(f"  Stats: {stats['tasks_completed']}/{stats['tasks_given']} erledigt ({stats['completion_rate']:.0f}%)")
        print(f"  Sync-Level: {stats['sync_level']}")

    print("\n" + "=" * 60)
    print("SIDEKICK-MODUS: KI fuehrt, Spieler spielt aktiv!")
    print("KEIN Auto-Follow! Spieler muss selbst handeln!")
    print("=" * 60)
