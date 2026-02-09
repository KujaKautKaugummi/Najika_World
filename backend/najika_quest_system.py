"""
NAJIKA QUEST SYSTEM - Backend
=============================

Skyrim-Style Quest System mit:
- Main Quests, Side Quests, Legendary Quests
- Quest Chains (verbundene Quest-Reihen)
- Entscheidungen mit Konsequenzen
- Najika-Reaktionen pro Quest-Phase
- Persistentes Tracking (aktiv, abgeschlossen, Fortschritt)

Erstellt: 2026-01-29
"""

import json
import os
import time
from typing import Dict, List, Optional, Any

# Quest Status Enum
class QuestStatus:
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    LOCKED = "locked"  # Noch nicht freigeschaltet

# Quest Types
class QuestType:
    MAIN = "main_quest"
    SIDE = "side_quest"
    LEGENDARY = "legendary_quest"
    STORY = "story_quest"
    CRAFTING = "crafting_quest"
    EXPLORATION = "exploration_quest"
    MYSTERY = "mystery_quest"
    DAILY = "daily_quest"
    REPEATABLE = "repeatable_quest"


class QuestSystem:
    """
    Zentrale Quest-Verwaltung für Najika World
    """

    def __init__(self, data_path: str = None):
        self.data_path = data_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "digivice", "data"
        )

        # Quest-Datenbank (aus JSON geladen)
        self.quests: Dict[str, Dict] = {}
        self.quest_chains: Dict[str, List[str]] = {}

        # Spieler Quest-Status (wird persistent gespeichert)
        self.player_quests = {
            "active": [],           # Aktive Quest IDs
            "completed": [],        # Abgeschlossene Quest IDs
            "failed": [],           # Fehlgeschlagene Quest IDs
            "progress": {},         # Quest-Fortschritt {quest_id: {objective_idx: done, ...}}
            "choices_made": {},     # Getroffene Entscheidungen {quest_id: choice_id}
            "timestamps": {}        # Wann Quest gestartet/beendet
        }

        # Lade Quest-Daten
        self.load_all_quests()

        print(f"[QUEST SYSTEM] ✅ {len(self.quests)} Quests geladen")

    def load_all_quests(self):
        """Lädt alle Quest-JSON-Dateien aus dem data-Ordner"""
        if not os.path.exists(self.data_path):
            print(f"[QUEST SYSTEM] ⚠️ Data path nicht gefunden: {self.data_path}")
            return

        for filename in os.listdir(self.data_path):
            if filename.startswith("quests_") and filename.endswith(".json"):
                filepath = os.path.join(self.data_path, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    region = data.get("region", "unknown")
                    quests = data.get("quests", [])
                    chains = data.get("quest_chains", {})

                    # Quests hinzufügen
                    for quest in quests:
                        quest_id = quest.get("id")
                        if quest_id:
                            quest["region"] = region
                            self.quests[quest_id] = quest

                    # Quest Chains hinzufügen
                    for chain_name, chain_quests in chains.items():
                        self.quest_chains[chain_name] = chain_quests

                    print(f"[QUEST SYSTEM] 📜 {filename}: {len(quests)} Quests geladen")
                except Exception as e:
                    print(f"[QUEST SYSTEM] ❌ Fehler beim Laden von {filename}: {e}")

    def get_quest(self, quest_id: str) -> Optional[Dict]:
        """Holt Quest-Details"""
        return self.quests.get(quest_id)

    def get_quest_status(self, quest_id: str) -> str:
        """Gibt den Status einer Quest zurück"""
        if quest_id in self.player_quests["completed"]:
            return QuestStatus.COMPLETED
        if quest_id in self.player_quests["failed"]:
            return QuestStatus.FAILED
        if quest_id in self.player_quests["active"]:
            return QuestStatus.ACTIVE

        # Check ob Quest locked ist (Level-Requirement nicht erfüllt)
        quest = self.get_quest(quest_id)
        if quest:
            # TODO: Player Level Check
            pass

        return QuestStatus.NOT_STARTED

    def start_quest(self, quest_id: str, player_level: int = 1) -> Dict:
        """Startet eine Quest"""
        quest = self.get_quest(quest_id)
        if not quest:
            return {"success": False, "error": "Quest nicht gefunden"}

        # Check Level Requirement
        level_req = quest.get("level_required", 0)
        if player_level < level_req:
            return {
                "success": False,
                "error": f"Level {level_req} benötigt (du hast {player_level})"
            }

        # Check ob bereits aktiv/abgeschlossen
        status = self.get_quest_status(quest_id)
        if status == QuestStatus.COMPLETED:
            return {"success": False, "error": "Quest bereits abgeschlossen"}
        if status == QuestStatus.ACTIVE:
            return {"success": False, "error": "Quest bereits aktiv"}

        # Quest starten
        self.player_quests["active"].append(quest_id)
        self.player_quests["progress"][quest_id] = {}
        self.player_quests["timestamps"][quest_id] = {
            "started": time.time()
        }

        # Initialisiere Objectives
        for idx, obj in enumerate(quest.get("objectives", [])):
            self.player_quests["progress"][quest_id][idx] = {
                "done": False,
                "current": 0,
                "required": obj.get("amount", 1)
            }

        # Najika Reaktion
        najika_reaction = None
        reactions = quest.get("najika_reactions", {})
        if "initial" in reactions:
            najika_reaction = reactions["initial"]

        return {
            "success": True,
            "quest": quest,
            "najika_reaction": najika_reaction,
            "message": f"Quest '{quest['name']}' gestartet!"
        }

    def update_objective(self, quest_id: str, objective_idx: int, amount: int = 1) -> Dict:
        """Aktualisiert den Fortschritt eines Quest-Objectives"""
        if quest_id not in self.player_quests["active"]:
            return {"success": False, "error": "Quest nicht aktiv"}

        quest = self.get_quest(quest_id)
        if not quest:
            return {"success": False, "error": "Quest nicht gefunden"}

        progress = self.player_quests["progress"].get(quest_id, {})
        obj_progress = progress.get(objective_idx, {})

        if obj_progress.get("done", False):
            return {"success": False, "error": "Objective bereits abgeschlossen"}

        # Update Progress
        current = obj_progress.get("current", 0) + amount
        required = obj_progress.get("required", 1)

        obj_progress["current"] = current

        # Check ob Objective fertig
        objective_done = current >= required
        if objective_done:
            obj_progress["done"] = True

        self.player_quests["progress"][quest_id][objective_idx] = obj_progress

        # Check ob alle Objectives fertig
        all_done = all(
            self.player_quests["progress"][quest_id].get(i, {}).get("done", False)
            for i in range(len(quest.get("objectives", [])))
        )

        return {
            "success": True,
            "objective_done": objective_done,
            "quest_completable": all_done,
            "progress": f"{current}/{required}"
        }

    def complete_quest(self, quest_id: str, choice_id: str = None) -> Dict:
        """Schließt eine Quest ab"""
        if quest_id not in self.player_quests["active"]:
            return {"success": False, "error": "Quest nicht aktiv"}

        quest = self.get_quest(quest_id)
        if not quest:
            return {"success": False, "error": "Quest nicht gefunden"}

        # Check ob alle Objectives fertig
        progress = self.player_quests["progress"].get(quest_id, {})
        objectives = quest.get("objectives", [])

        for idx in range(len(objectives)):
            if not progress.get(idx, {}).get("done", False):
                return {"success": False, "error": f"Objective {idx+1} nicht abgeschlossen"}

        # Verarbeite Choice wenn vorhanden
        choice_outcome = None
        if choice_id and quest.get("choices"):
            for choice_event in quest["choices"]:
                for option in choice_event.get("options", []):
                    if option["id"] == choice_id:
                        choice_outcome = option.get("outcome", {})
                        self.player_quests["choices_made"][quest_id] = choice_id
                        break

        # Quest abschließen
        self.player_quests["active"].remove(quest_id)
        self.player_quests["completed"].append(quest_id)
        self.player_quests["timestamps"][quest_id]["completed"] = time.time()

        # Rewards berechnen
        rewards = quest.get("rewards", {})
        if choice_outcome and "rewards" in choice_outcome:
            # Merge Choice Rewards
            rewards = {**rewards, **choice_outcome.get("rewards", {})}

        # Najika Reaktion
        najika_reaction = None
        reactions = quest.get("najika_reactions", {})
        if choice_id and choice_outcome and "najika_aftermath" in choice_outcome:
            najika_reaction = choice_outcome["najika_aftermath"]
        elif "completion" in reactions:
            najika_reaction = reactions["completion"]

        return {
            "success": True,
            "quest_name": quest["name"],
            "rewards": rewards,
            "choice_outcome": choice_outcome,
            "najika_reaction": najika_reaction,
            "unlocks": quest.get("unlocks")
        }

    def get_active_quests(self) -> List[Dict]:
        """Gibt alle aktiven Quests zurück"""
        return [
            {
                **self.get_quest(qid),
                "status": QuestStatus.ACTIVE,
                "progress": self.player_quests["progress"].get(qid, {})
            }
            for qid in self.player_quests["active"]
            if self.get_quest(qid)
        ]

    def get_available_quests(self, player_level: int = 1, region: str = None) -> List[Dict]:
        """Gibt alle verfügbaren (nicht gestarteten) Quests zurück"""
        available = []
        for quest_id, quest in self.quests.items():
            status = self.get_quest_status(quest_id)
            if status != QuestStatus.NOT_STARTED:
                continue

            # Level Check
            if player_level < quest.get("level_required", 0):
                continue

            # Region Filter
            if region and quest.get("region") != region:
                continue

            available.append({
                **quest,
                "status": QuestStatus.NOT_STARTED
            })

        return available

    def get_completed_quests(self) -> List[Dict]:
        """Gibt alle abgeschlossenen Quests zurück"""
        return [
            {
                **self.get_quest(qid),
                "status": QuestStatus.COMPLETED,
                "choice_made": self.player_quests["choices_made"].get(qid),
                "completed_at": self.player_quests["timestamps"].get(qid, {}).get("completed")
            }
            for qid in self.player_quests["completed"]
            if self.get_quest(qid)
        ]

    def get_quest_chain(self, chain_name: str) -> List[Dict]:
        """Gibt alle Quests einer Chain zurück"""
        chain_ids = self.quest_chains.get(chain_name, [])
        return [
            {
                **self.get_quest(qid),
                "status": self.get_quest_status(qid)
            }
            for qid in chain_ids
            if self.get_quest(qid)
        ]

    def export_state(self) -> Dict:
        """Exportiert den Quest-Status für Save/Load"""
        return self.player_quests.copy()

    def import_state(self, state: Dict):
        """Importiert den Quest-Status"""
        if state:
            self.player_quests = state

    def get_stats(self) -> Dict:
        """Gibt Quest-Statistiken zurück"""
        return {
            "total_quests": len(self.quests),
            "active": len(self.player_quests["active"]),
            "completed": len(self.player_quests["completed"]),
            "failed": len(self.player_quests["failed"]),
            "completion_rate": (
                len(self.player_quests["completed"]) / len(self.quests) * 100
                if self.quests else 0
            ),
            "quest_chains": len(self.quest_chains)
        }


# Singleton Instance
_quest_system = None

def get_quest_system() -> QuestSystem:
    """Gibt die Quest System Instanz zurück (Singleton)"""
    global _quest_system
    if _quest_system is None:
        _quest_system = QuestSystem()
    return _quest_system


# Test
if __name__ == "__main__":
    qs = get_quest_system()
    print("\n=== QUEST SYSTEM TEST ===")
    print(f"Stats: {qs.get_stats()}")

    # Test Quest starten
    result = qs.start_quest("die_botschaft_der_goetter", player_level=20)
    print(f"\nQuest Start: {result}")

    # Active Quests
    print(f"\nAktive Quests: {len(qs.get_active_quests())}")
