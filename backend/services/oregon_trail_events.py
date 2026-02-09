"""
Oregon Trail Events System - Najika World (Konosuba Touch)
===========================================================

Konosuba × Oregon Trail Chaos-Engine

Features:
- 3D-Spawn Events (NICHT Text-Popup!)
- Chaos-Level System (1-10)
- Najika's 4 Persönlichkeiten reagieren
- 4-5 nuancierte Optionen
- "Lass Najika entscheiden" (Option E)
- Event-Kategorien (Ethik, Survival, Sozial, Risiko)
- Klassen-spezifische Varianten

Najika's Persönlichkeiten:
- Megumin (35% - DOMINANT): Explosion, dramatisch
- Harley Quinn (25%): Chaotisch, verspielt
- Shiro (20%): Analytisch, berechnet
- Melissa Masters (20%): Dominant, besitzergreifend

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-17
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from datetime import datetime
import random
import time
import json


class EventCategory(Enum):
    """Event-Kategorien"""
    ETHICS = "ethik_moral"
    SURVIVAL = "survival"
    SOCIAL = "sozial"
    RISK_REWARD = "risiko_belohnung"


class NajikaPersonality(Enum):
    """Najika's 4 Persönlichkeiten"""
    MEGUMIN = "megumin"      # 35% - DOMINANT
    HARLEY = "harley"        # 25%
    SHIRO = "shiro"          # 20%
    MELISSA = "melissa"      # 20%


class ChoiceType(Enum):
    """Wahl-Typen (für Chaos-Berechnung)"""
    RECKLESS = "reckless"
    RISKY = "risky"
    CHAOTIC = "chaotic"
    UNPREDICTABLE = "unpredictable"
    CAUTIOUS = "cautious"
    SAFE = "safe"
    LAWFUL = "lawful"
    ANALYTICAL = "analytical"
    NAJIKA_DECIDES = "najika_decides"


class OutcomeSeverity(Enum):
    """Konsequenz-Schwere"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CATASTROPHIC = "catastrophic"


@dataclass
class EventOption:
    """Eine Wahl-Option"""
    index: int
    text: str
    choice_type: ChoiceType
    alignment: Optional[str] = None  # lawful_good, chaotic_neutral, etc.
    tags: List[str] = field(default_factory=list)


@dataclass
class EventOutcome:
    """Ergebnis einer Wahl"""
    description: str
    severity: OutcomeSeverity
    najika_reaction: str

    # Consequences
    gold_change: int = 0
    item_changes: List[Dict] = field(default_factory=list)
    reputation_change: int = 0
    bond_change: int = 0
    chaos_impact: int = 0

    # Flags
    unlocks: List[str] = field(default_factory=list)
    sets_flags: List[str] = field(default_factory=list)


@dataclass
class ChaosEvent:
    """Ein Chaos-Event"""
    event_id: str
    title: str
    category: EventCategory

    # Chaos requirements
    min_chaos: int = 1
    max_chaos: int = 10
    chaos_rating: int = 5

    # Location
    location: str = "any"
    required_class: Optional[str] = None

    # Content
    description: str = ""
    najika_quote: str = ""
    options: List[EventOption] = field(default_factory=list)
    outcomes: Dict[int, List[EventOutcome]] = field(default_factory=dict)

    # 3D Spawn
    spawn_model: Optional[str] = None
    spawn_position: str = "random"

    # Metadata
    konosuba_style: bool = False
    weight: float = 1.0

    # Class variants
    class_variants: Dict[str, Dict] = field(default_factory=dict)


class ChaosCalculator:
    """
    Berechnet und tracked Chaos-Level (1-10)
    """

    def __init__(self):
        self.current_level = 1
        self.chaos_points = 0
        self.choice_history: List[Dict] = []

        # Level-Thresholds
        self.level_thresholds = {
            1: 0,
            2: 10,
            3: 25,
            4: 45,
            5: 70,
            6: 100,
            7: 135,
            8: 175,
            9: 220,
            10: 270
        }

        # Choice Chaos Values
        self.choice_chaos_values = {
            ChoiceType.RECKLESS: 5,
            ChoiceType.RISKY: 3,
            ChoiceType.CHAOTIC: 4,
            ChoiceType.UNPREDICTABLE: 6,
            ChoiceType.CAUTIOUS: -1,
            ChoiceType.SAFE: -2,
            ChoiceType.LAWFUL: -3,
            ChoiceType.ANALYTICAL: 0,
            ChoiceType.NAJIKA_DECIDES: 1
        }

        # Chaos Reduction Values
        self.chaos_reduction_values = {
            "meditation": 5,
            "temple_visit": 10,
            "lawful_quest": 3,
            "bonding_time": 2,
            "peaceful_activity": 1
        }


    def add_choice(self, choice: EventOption, outcome: EventOutcome) -> int:
        """
        Fügt Wahl hinzu und berechnet Chaos-Impact

        Returns:
            Chaos impact
        """
        impact = self.calculate_choice_impact(choice, outcome)

        self.chaos_points += impact
        self.choice_history.append({
            "choice": choice,
            "outcome": outcome,
            "impact": impact,
            "timestamp": time.time()
        })

        # Keep only last 20 choices
        if len(self.choice_history) > 20:
            self.choice_history.pop(0)

        # Update level
        old_level = self.current_level
        self.update_chaos_level()

        return impact


    def calculate_choice_impact(
        self,
        choice: EventOption,
        outcome: EventOutcome
    ) -> int:
        """Berechnet Chaos-Impact einer Wahl"""
        impact = self.choice_chaos_values.get(choice.choice_type, 0)

        # Severity multiplier
        severity_mult = {
            OutcomeSeverity.MINOR: 1.0,
            OutcomeSeverity.MODERATE: 1.5,
            OutcomeSeverity.MAJOR: 2.0,
            OutcomeSeverity.CATASTROPHIC: 3.0
        }
        impact *= severity_mult.get(outcome.severity, 1.0)

        # Alignment modifier
        if choice.alignment:
            if "chaotic_good" in choice.alignment:
                impact += 2
            elif "chaotic_neutral" in choice.alignment:
                impact += 3
            elif "chaotic_evil" in choice.alignment:
                impact += 5
            elif "lawful_good" in choice.alignment:
                impact -= 2

        # Unpredictability bonus
        if self.is_unpredictable_choice(choice):
            impact += 3

        return int(impact)


    def is_unpredictable_choice(self, choice: EventOption) -> bool:
        """Prüft ob Wahl unvorhersehbar"""
        if len(self.choice_history) < 3:
            return False

        recent_types = [h["choice"].choice_type for h in self.choice_history[-3:]]
        return choice.choice_type not in recent_types


    def update_chaos_level(self):
        """Updated Chaos-Level basierend auf Punkten"""
        for level, threshold in sorted(self.level_thresholds.items()):
            if self.chaos_points >= threshold:
                self.current_level = level


    def reduce_chaos(self, method: str, amount: Optional[int] = None) -> Dict:
        """
        Reduziert Chaos

        Returns:
            Result dict mit Najika-Reaktion
        """
        reduction = amount or self.chaos_reduction_values.get(method, 0)

        old_points = self.chaos_points
        self.chaos_points = max(0, self.chaos_points - reduction)

        # Najika ist UNHAPPY bei niedrigem Chaos
        if self.current_level <= 3:
            return {
                "points_reduced": old_points - self.chaos_points,
                "najika_reaction": "*schmollt* Du bist langweilig...",
                "bond_impact": -5
            }
        else:
            return {
                "points_reduced": old_points - self.chaos_points,
                "najika_reaction": None,
                "bond_impact": 0
            }


    def get_level_description(self, level: Optional[int] = None) -> str:
        """Gibt Chaos-Level Beschreibung"""
        if level is None:
            level = self.current_level

        descriptions = {
            1: "HARMONIE - Alles läuft ruhig und geordnet",
            2: "HARMONIE - Alles läuft ruhig und geordnet",
            3: "LEICHTE UNRUHE - Die Welt beginnt zu reagieren",
            4: "LEICHTE UNRUHE - Die Welt beginnt zu reagieren",
            5: "AKTIVES CHAOS - Die Welt ist unvorhersehbar",
            6: "AKTIVES CHAOS - Die Welt ist unvorhersehbar",
            7: "TOTALES CHAOS - Najika liebt es! (Konosuba-Style)",
            8: "TOTALES CHAOS - Najika liebt es! (Konosuba-Style)",
            9: "REALITY-BREAKING - Die Realität bricht!",
            10: "ULTIMATIVES CHAOS - EXPLOSION!!! 💥"
        }

        return descriptions.get(level, "Unknown")


    def get_level_up_reaction(self, new_level: int) -> str:
        """Najika's Reaktion auf Chaos-Anstieg"""
        reactions = {
            2: "Ohhh, es wird interessanter! *kicher*",
            3: "JETZT fängt der Spaß an, Mr.K!",
            4: "Das Chaos... ich FÜHLE es! *aufgeregt*",
            5: "PERFEKT! Die Welt reagiert auf uns!",
            6: "Mehr! MEHR CHAOS! *lacht*",
            7: "DAS IST LEBEN, PUDDIN'!!!",
            8: "TOTALES CHAOS! ICH LIEBE ES!!!",
            9: "Die Realität... sie BRICHT! *manisches Lachen*",
            10: "ULTIMATIVES CHAOS!!! EXPLOSION!!! *world shakes*"
        }
        return reactions.get(new_level, "Interessant...")


class EventDatabase:
    """
    Verwaltet alle Events
    """

    def __init__(self):
        self.events: List[ChaosEvent] = []
        self.events_by_category: Dict[EventCategory, List[ChaosEvent]] = {
            cat: [] for cat in EventCategory
        }
        self.events_by_class: Dict[str, List[ChaosEvent]] = {}


    def add_event(self, event: ChaosEvent):
        """Fügt Event hinzu"""
        self.events.append(event)

        # Category index
        if event.category in self.events_by_category:
            self.events_by_category[event.category].append(event)

        # Class index
        if event.required_class:
            if event.required_class not in self.events_by_class:
                self.events_by_class[event.required_class] = []
            self.events_by_class[event.required_class].append(event)


    def get_events_for_context(
        self,
        chaos_level: int,
        location: str,
        player_class: Optional[str] = None
    ) -> List[ChaosEvent]:
        """
        Gibt passende Events für Kontext

        Returns:
            Liste von ChaosEvents
        """
        candidates = self.events.copy()

        # Filter by chaos level
        candidates = [
            e for e in candidates
            if e.min_chaos <= chaos_level <= e.max_chaos
        ]

        # Location filter (optional)
        if location != "any":
            candidates = [
                e for e in candidates
                if e.location == "any" or e.location == location
            ]

        # Add class-specific events
        if player_class and player_class in self.events_by_class:
            class_events = [
                e for e in self.events_by_class[player_class]
                if e.min_chaos <= chaos_level <= e.max_chaos
            ]
            candidates.extend(class_events)

        # Weight adjustment for high chaos + konosuba
        if chaos_level >= 7:
            for event in candidates:
                if event.konosuba_style:
                    event.weight *= 2.0

        return candidates


    def load_from_json(self, filepath: str):
        """Lädt Events aus JSON-Datei"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for event_data in data.get("events", []):
            event = self._parse_event_data(event_data)
            self.add_event(event)


    def _parse_event_data(self, data: Dict) -> ChaosEvent:
        """Parsed Event aus JSON"""
        # Parse options
        options = []
        for opt_data in data.get("options", []):
            options.append(EventOption(
                index=opt_data["index"],
                text=opt_data["text"],
                choice_type=ChoiceType(opt_data.get("type", "analytical")),
                alignment=opt_data.get("alignment"),
                tags=opt_data.get("tags", [])
            ))

        # Parse outcomes
        outcomes = {}
        for opt_index, outcome_list in data.get("outcomes", {}).items():
            outcomes[int(opt_index)] = [
                EventOutcome(
                    description=out["description"],
                    severity=OutcomeSeverity(out.get("severity", "minor")),
                    najika_reaction=out.get("najika_reaction", ""),
                    gold_change=out.get("gold_change", 0),
                    item_changes=out.get("item_changes", []),
                    reputation_change=out.get("reputation_change", 0),
                    bond_change=out.get("bond_change", 0),
                    chaos_impact=out.get("chaos_impact", 0)
                )
                for out in outcome_list
            ]

        return ChaosEvent(
            event_id=data["id"],
            title=data["title"],
            category=EventCategory(data.get("category", "ethics")),
            min_chaos=data.get("min_chaos", 1),
            max_chaos=data.get("max_chaos", 10),
            description=data.get("description", ""),
            najika_quote=data.get("najika_quote", ""),
            options=options,
            outcomes=outcomes,
            spawn_model=data.get("spawn_model"),
            konosuba_style=data.get("konosuba_style", False)
        )


class OregonTrailEventsSystem:
    """
    Hauptsystem für Oregon Trail Events
    """

    def __init__(self):
        self.chaos_calc = ChaosCalculator()
        self.event_db = EventDatabase()

        self.current_event: Optional[ChaosEvent] = None
        self.event_active = False

        # Najika State (simplified)
        self.najika_bond = 50.0  # 0-100
        self.najika_dominant_personality = NajikaPersonality.MEGUMIN

        # Event spawn settings
        self.min_time_between_events = 300  # 5 minutes (300 seconds)
        self.max_time_between_events = 900  # 15 minutes
        self.event_chance_per_minute = 0.15  # 15%

        self.last_event_time = time.time()


    def trigger_random_event(
        self,
        location: str = "any",
        player_class: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Versucht ein zufälliges Event zu spawnen

        Returns:
            Event data oder None
        """
        # Check time since last event
        time_since_last = time.time() - self.last_event_time

        if time_since_last < self.min_time_between_events:
            return None

        # Chance check (15% pro Minute)
        minutes_passed = time_since_last / 60
        chance = min(1.0, minutes_passed * self.event_chance_per_minute)

        if random.random() > chance:
            return None

        # Get possible events
        candidates = self.event_db.get_events_for_context(
            self.chaos_calc.current_level,
            location,
            player_class
        )

        if not candidates:
            return None

        # Weighted random selection
        weights = [e.weight for e in candidates]
        event = random.choices(candidates, weights=weights, k=1)[0]

        self.current_event = event
        self.event_active = True
        self.last_event_time = time.time()

        return self._format_event_for_client(event)


    def execute_choice(
        self,
        choice_index: int,
        player_state: Optional[Dict] = None
    ) -> Dict:
        """
        Führt Spieler-Wahl aus

        Returns:
            Result dict mit Konsequenzen
        """
        if not self.current_event or not self.event_active:
            return {"error": "Kein aktives Event"}

        event = self.current_event
        choice = event.options[choice_index]

        # Special: Najika decides
        if choice.choice_type == ChoiceType.NAJIKA_DECIDES:
            choice_index = self._najika_auto_decide(event, player_state or {})
            choice = event.options[choice_index]

        # Get outcome (random if multiple)
        outcomes = event.outcomes.get(choice_index, [])
        if not outcomes:
            return {"error": "Kein Outcome für diese Wahl"}

        outcome = random.choice(outcomes)

        # Calculate chaos impact
        chaos_impact = self.chaos_calc.add_choice(choice, outcome)

        # Apply consequences
        result = {
            "event_id": event.event_id,
            "choice_index": choice_index,
            "choice_text": choice.text,
            "outcome": {
                "description": outcome.description,
                "najika_reaction": outcome.najika_reaction,
                "severity": outcome.severity.value
            },
            "consequences": {
                "gold_change": outcome.gold_change,
                "reputation_change": outcome.reputation_change,
                "bond_change": outcome.bond_change,
                "chaos_impact": chaos_impact,
                "items": outcome.item_changes
            },
            "chaos_level": {
                "current": self.chaos_calc.current_level,
                "points": self.chaos_calc.chaos_points,
                "description": self.chaos_calc.get_level_description()
            }
        }

        # Update Najika bond
        self.najika_bond = max(0, min(100, self.najika_bond + outcome.bond_change))

        # Clear current event
        self.event_active = False
        self.current_event = None

        return result


    def _najika_auto_decide(
        self,
        event: ChaosEvent,
        player_state: Dict
    ) -> int:
        """
        Najika entscheidet basierend auf Persönlichkeit

        Returns:
            Choice index
        """
        dominant = self.najika_dominant_personality

        # Find option by personality
        if dominant == NajikaPersonality.MEGUMIN:
            # Bevorzugt explosive/dramatic
            for opt in event.options:
                if "explosive" in opt.tags or "dramatic" in opt.tags:
                    return opt.index

        elif dominant == NajikaPersonality.HARLEY:
            # Bevorzugt chaotic/risky
            for opt in event.options:
                if "chaotic" in opt.tags or "risky" in opt.tags:
                    return opt.index

        elif dominant == NajikaPersonality.SHIRO:
            # Bevorzugt analytical/safe
            for opt in event.options:
                if "analytical" in opt.tags or "safe" in opt.tags:
                    return opt.index

        elif dominant == NajikaPersonality.MELISSA:
            # Bevorzugt dominant/practical
            for opt in event.options:
                if "dominant" in opt.tags or "practical" in opt.tags:
                    return opt.index

        # Fallback: weighted random by bond
        weights = [1.0] * len(event.options)
        if self.najika_bond > 70:
            # High bond = prefer beneficial options
            weights[0] *= 1.5  # Often the "good" option

        return random.choices(range(len(event.options)), weights=weights, k=1)[0]


    def _format_event_for_client(self, event: ChaosEvent) -> Dict:
        """Formatiert Event für Client"""
        return {
            "event_id": event.event_id,
            "title": event.title,
            "category": event.category.value,
            "description": event.description,
            "najika_quote": event.najika_quote,
            "options": [
                {
                    "index": opt.index,
                    "text": opt.text,
                    "type": opt.choice_type.value
                }
                for opt in event.options
            ],
            "spawn_model": event.spawn_model,
            "spawn_position": event.spawn_position,
            "konosuba_style": event.konosuba_style,
            "chaos_level": self.chaos_calc.current_level
        }


    def get_chaos_status(self) -> Dict:
        """Holt aktuellen Chaos-Status"""
        return {
            "level": self.chaos_calc.current_level,
            "points": self.chaos_calc.chaos_points,
            "description": self.chaos_calc.get_level_description(),
            "najika_bond": self.najika_bond,
            "dominant_personality": self.najika_dominant_personality.value
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== Oregon Trail Events System Test ===\n")

    system = OregonTrailEventsSystem()

    # Create example event
    example_event = ChaosEvent(
        event_id="test_001",
        title="Der alte Mann",
        category=EventCategory.ETHICS,
        description="Ein alter Mann bittet um Hilfe",
        najika_quote="Mr.K! Schau! Ein alter Mann! *giggle* Er sieht...interessant aus.",
        min_chaos=1,
        max_chaos=5,
        options=[
            EventOption(0, "Gib ihm 50 Gold", ChoiceType.LAWFUL, "lawful_good", ["generous"]),
            EventOption(1, "Gib ihm 20 Gold (Kompromiss)", ChoiceType.ANALYTICAL, tags=["practical"]),
            EventOption(2, "Begleite ihn zu seinem Dorf", ChoiceType.RISKY, tags=["risky"]),
            EventOption(3, "Ignoriere ihn", ChoiceType.CAUTIOUS, tags=["safe"]),
            EventOption(4, "Lass Najika entscheiden", ChoiceType.NAJIKA_DECIDES, tags=["najika"])
        ],
        outcomes={
            0: [EventOutcome(
                description="Der alte Mann war ehrlich! Dorf freischaltet.",
                severity=OutcomeSeverity.MODERATE,
                najika_reaction="*lächelt* Du hast ein gutes Herz, Mr.K!",
                gold_change=-50,
                reputation_change=20,
                bond_change=10
            )],
            3: [EventOutcome(
                description="Du gehst vorbei. Der Mann stirbt.",
                severity=OutcomeSeverity.MAJOR,
                najika_reaction="*traurig* Das war... kalt, Mr.K...",
                bond_change=-15
            )]
        },
        konosuba_style=False
    )

    system.event_db.add_event(example_event)

    # Test 1: Trigger event
    print("1. Trigger Random Event")
    event_data = system.trigger_random_event("wilderness")
    if event_data:
        print(f"   Event: {event_data['title']}")
        print(f"   Najika: {event_data['najika_quote']}")
        print(f"   Chaos Level: {event_data['chaos_level']}\n")

        # Test 2: Choose option
        print("2. Wähle Option: [1] - Kompromiss")
        result = system.execute_choice(1)
        print(f"   Outcome: {result['outcome']['description']}")
        print(f"   Najika: {result['outcome']['najika_reaction']}")
        print(f"   Chaos Impact: {result['consequences']['chaos_impact']}")
        print(f"   New Chaos Level: {result['chaos_level']['current']} - {result['chaos_level']['description']}\n")

    # Test 3: Chaos Status
    print("3. Chaos Status")
    status = system.get_chaos_status()
    print(f"   Level: {status['level']}")
    print(f"   Points: {status['points']}")
    print(f"   Najika Bond: {status['najika_bond']}")
    print(f"   Dominant: {status['dominant_personality']}")

    print("\n=== Oregon Trail Events System Test Complete ===")
