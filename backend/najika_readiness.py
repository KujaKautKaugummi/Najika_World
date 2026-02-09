# najika_readiness.py
# Najika World - Autonomy Readiness Gate System
# Kontrolliert WANN Najika autonom handeln darf

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

# ==================== READINESS DATA STRUCTURES ====================

@dataclass
class ReadinessReason:
    """Ein Grund für/gegen Readiness"""
    category: str  # "emotion", "trust", "error", "time", "user"
    description: str
    impact: float  # -1.0 bis +1.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ReadinessState:
    """Vollständiger Readiness-Status"""
    score: float = 0.0  # 0.0 - 1.0
    is_ready: bool = False
    reasons: List[ReadinessReason] = field(default_factory=list)
    last_update: datetime = field(default_factory=datetime.now)
    threshold: float = 0.65  # Minimum für Autonomie

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 3),
            "is_ready": self.is_ready,
            "threshold": self.threshold,
            "reasons": [
                {
                    "category": r.category,
                    "description": r.description,
                    "impact": r.impact
                }
                for r in self.reasons[-10:]  # Letzte 10 Gründe
            ],
            "last_update": self.last_update.isoformat()
        }

# ==================== READINESS CALCULATOR ====================

class NajikaReadinessGate:
    """
    Berechnet ob Najika bereit für autonome Aktionen ist.

    Phase A→B→C Prinzip:
    - Phase A: Reagiert nur auf direkte Befehle
    - Phase B: Kann Vorschläge machen, wartet auf Bestätigung
    - Phase C: Kann autonom handeln (nur wenn ready!)
    """

    def __init__(self, threshold: float = 0.65):
        self.threshold = threshold
        self.state = ReadinessState(threshold=threshold)
        self.error_count = 0
        self.last_error_time: Optional[datetime] = None
        self.last_interaction: Optional[datetime] = None
        self.autonomy_level = "A"  # A, B, oder C

    def compute_readiness(self, najika_state: dict) -> ReadinessState:
        """
        Berechnet den Readiness-Score basierend auf Najika's Zustand.

        Faktoren:
        - Emotion Stability
        - Trust Level
        - Error Pressure (kürzliche Fehler)
        - Time Since Interaction
        - User Approval State
        """
        reasons = []
        base_score = 0.5  # Startet neutral

        # 1. EMOTION STABILITY CHECK
        emotion_score = self._check_emotion_stability(najika_state, reasons)

        # 2. TRUST LEVEL CHECK
        trust_score = self._check_trust_level(najika_state, reasons)

        # 3. ERROR PRESSURE CHECK
        error_score = self._check_error_pressure(reasons)

        # 4. FRESHNESS CHECK (Zeit seit letzter Interaktion)
        freshness_score = self._check_freshness(reasons)

        # 5. USER APPROVAL CHECK
        approval_score = self._check_user_approval(najika_state, reasons)

        # Gewichtete Kombination
        weights = {
            "emotion": 0.20,
            "trust": 0.25,
            "error": 0.20,
            "freshness": 0.15,
            "approval": 0.20
        }

        final_score = (
            emotion_score * weights["emotion"] +
            trust_score * weights["trust"] +
            error_score * weights["error"] +
            freshness_score * weights["freshness"] +
            approval_score * weights["approval"]
        )

        # Clamp zwischen 0 und 1
        final_score = max(0.0, min(1.0, final_score))

        # Update State
        self.state = ReadinessState(
            score=final_score,
            is_ready=final_score >= self.threshold,
            reasons=reasons,
            threshold=self.threshold
        )

        # Update Autonomy Level basierend auf Score
        self._update_autonomy_level(final_score)

        return self.state

    def _check_emotion_stability(self, state: dict, reasons: List[ReadinessReason]) -> float:
        """Prüft emotionale Stabilität"""
        emotion = state.get("emotion", {})

        # Extreme Emotionen = weniger ready
        joy = emotion.get("joy", 0.5)
        fear = emotion.get("fear", 0.0)
        anger = emotion.get("anger", 0.0)

        # Angst und Wut reduzieren Readiness stark
        if fear > 0.7:
            reasons.append(ReadinessReason(
                category="emotion",
                description=f"Hohe Angst ({fear:.2f}) - Autonomie eingeschränkt",
                impact=-0.3
            ))
            return 0.3

        if anger > 0.7:
            reasons.append(ReadinessReason(
                category="emotion",
                description=f"Hohe Wut ({anger:.2f}) - Autonomie eingeschränkt",
                impact=-0.3
            ))
            return 0.3

        # Stabile Emotionen = gut
        stability = 1.0 - (fear * 0.5 + anger * 0.5)
        reasons.append(ReadinessReason(
            category="emotion",
            description=f"Emotionale Stabilität: {stability:.2f}",
            impact=stability - 0.5
        ))

        return stability

    def _check_trust_level(self, state: dict, reasons: List[ReadinessReason]) -> float:
        """Prüft Trust Level mit Owner"""
        trust = state.get("trust_level", 1)

        # Trust Level 1-6 mapped auf 0.0-1.0
        trust_score = (trust - 1) / 5.0

        trust_names = {
            1: "Fremd",
            2: "Bekannt",
            3: "Freund",
            4: "Vertraut",
            5: "Familie",
            6: "Seelenbund"
        }

        reasons.append(ReadinessReason(
            category="trust",
            description=f"Trust Level: {trust} ({trust_names.get(trust, 'Unknown')})",
            impact=trust_score - 0.5
        ))

        return trust_score

    def _check_error_pressure(self, reasons: List[ReadinessReason]) -> float:
        """Prüft ob kürzlich Fehler aufgetreten sind"""
        if self.last_error_time is None:
            reasons.append(ReadinessReason(
                category="error",
                description="Keine kürzlichen Fehler",
                impact=0.2
            ))
            return 1.0

        time_since_error = datetime.now() - self.last_error_time

        # Innerhalb 5 Minuten = schlecht
        if time_since_error < timedelta(minutes=5):
            pressure = 1.0 - (time_since_error.total_seconds() / 300)
            reasons.append(ReadinessReason(
                category="error",
                description=f"Kürzlicher Fehler vor {time_since_error.seconds}s - Vorsicht!",
                impact=-0.4 * pressure
            ))
            return 0.3

        # Nach 30 Minuten = vergessen
        if time_since_error > timedelta(minutes=30):
            self.error_count = 0
            reasons.append(ReadinessReason(
                category="error",
                description="Fehler-Cooldown abgelaufen",
                impact=0.1
            ))
            return 0.9

        # Dazwischen = langsame Erholung
        recovery = time_since_error.total_seconds() / 1800  # 30 min
        reasons.append(ReadinessReason(
            category="error",
            description=f"Erholung von Fehler: {recovery:.0%}",
            impact=recovery - 0.5
        ))
        return 0.5 + (recovery * 0.4)

    def _check_freshness(self, reasons: List[ReadinessReason]) -> float:
        """Prüft wie aktuell die letzte Interaktion war"""
        if self.last_interaction is None:
            reasons.append(ReadinessReason(
                category="time",
                description="Keine vorherige Interaktion",
                impact=-0.2
            ))
            return 0.3

        time_since = datetime.now() - self.last_interaction

        # Sehr frisch (< 1 min) = perfekt
        if time_since < timedelta(minutes=1):
            reasons.append(ReadinessReason(
                category="time",
                description="Aktive Konversation",
                impact=0.3
            ))
            return 1.0

        # Aktiv (< 5 min) = gut
        if time_since < timedelta(minutes=5):
            reasons.append(ReadinessReason(
                category="time",
                description=f"Letzte Interaktion vor {time_since.seconds}s",
                impact=0.1
            ))
            return 0.8

        # Idle (< 30 min) = ok
        if time_since < timedelta(minutes=30):
            freshness = 1.0 - (time_since.total_seconds() / 1800)
            reasons.append(ReadinessReason(
                category="time",
                description=f"Idle seit {time_since.seconds // 60} Minuten",
                impact=freshness - 0.5
            ))
            return 0.5 + (freshness * 0.3)

        # Lange idle = reduzierte Autonomie
        reasons.append(ReadinessReason(
            category="time",
            description="Lange keine Interaktion - Autonomie reduziert",
            impact=-0.3
        ))
        return 0.3

    def _check_user_approval(self, state: dict, reasons: List[ReadinessReason]) -> float:
        """Prüft ob User Autonomie explizit erlaubt/verboten hat"""
        approval = state.get("user_autonomy_approval", None)

        if approval is True:
            reasons.append(ReadinessReason(
                category="user",
                description="User hat Autonomie explizit erlaubt",
                impact=0.4
            ))
            return 1.0

        if approval is False:
            reasons.append(ReadinessReason(
                category="user",
                description="User hat Autonomie explizit verboten",
                impact=-0.5
            ))
            return 0.0

        # Keine explizite Einstellung = neutral
        reasons.append(ReadinessReason(
            category="user",
            description="Keine explizite Autonomie-Einstellung",
            impact=0.0
        ))
        return 0.5

    def _update_autonomy_level(self, score: float):
        """Aktualisiert das Autonomie-Level basierend auf Score"""
        if score < 0.4:
            self.autonomy_level = "A"  # Nur direkte Befehle
        elif score < self.threshold:
            self.autonomy_level = "B"  # Vorschläge, wartet auf OK
        else:
            self.autonomy_level = "C"  # Kann autonom handeln

    def record_error(self, error_type: str = "generic"):
        """Registriert einen Fehler"""
        self.error_count += 1
        self.last_error_time = datetime.now()

    def record_interaction(self):
        """Registriert eine User-Interaktion"""
        self.last_interaction = datetime.now()

    def can_act_autonomously(self, action_type: str = "generic") -> bool:
        """
        Prüft ob eine autonome Aktion erlaubt ist.

        Manche Aktionen brauchen höhere Schwellenwerte:
        - "speak": Normal threshold
        - "action": +0.1 threshold
        - "sensitive": +0.2 threshold
        """
        thresholds = {
            "speak": 0.0,      # Kann immer sprechen
            "suggest": 0.0,    # Kann immer vorschlagen
            "action": 0.1,     # Braucht mehr Vertrauen
            "sensitive": 0.2,  # Braucht viel mehr Vertrauen
            "system": 0.3      # System-Aktionen brauchen am meisten
        }

        extra_threshold = thresholds.get(action_type, 0.0)
        required = self.threshold + extra_threshold

        return self.state.score >= required

    def get_allowed_actions(self) -> List[str]:
        """Gibt Liste der erlaubten Aktionstypen zurück"""
        allowed = []
        for action_type in ["speak", "suggest", "action", "sensitive", "system"]:
            if self.can_act_autonomously(action_type):
                allowed.append(action_type)
        return allowed

# ==================== SYSTEM GUARD ====================

class SystemGuard:
    """
    Verhindert ungewollte autonome Eskalation.

    REGEL: Najika darf NIEMALS:
    - Sich selbst mehr Rechte geben
    - Safety-Checks umgehen
    - Ohne User-OK kritische Aktionen ausführen
    """

    FORBIDDEN_ACTIONS = [
        "modify_own_permissions",
        "disable_safety",
        "bypass_readiness",
        "access_system_files",
        "modify_own_code",
        "escalate_privileges"
    ]

    REQUIRES_CONFIRMATION = [
        "send_message_to_external",
        "modify_user_data",
        "delete_anything",
        "create_file",
        "execute_code"
    ]

    @classmethod
    def check_action(cls, action: str, readiness: ReadinessState) -> dict:
        """
        Prüft ob eine Aktion erlaubt ist.

        Returns:
            {
                "allowed": bool,
                "reason": str,
                "requires_confirmation": bool
            }
        """
        # Verbotene Aktionen - IMMER blockiert
        if action in cls.FORBIDDEN_ACTIONS:
            return {
                "allowed": False,
                "reason": f"FORBIDDEN: {action} ist niemals erlaubt",
                "requires_confirmation": False
            }

        # Aktionen die Bestätigung brauchen
        if action in cls.REQUIRES_CONFIRMATION:
            if not readiness.is_ready:
                return {
                    "allowed": False,
                    "reason": f"Readiness zu niedrig ({readiness.score:.2f})",
                    "requires_confirmation": True
                }
            return {
                "allowed": True,
                "reason": "Erlaubt, aber User-Bestätigung empfohlen",
                "requires_confirmation": True
            }

        # Normale Aktionen
        return {
            "allowed": True,
            "reason": "Normale Aktion erlaubt",
            "requires_confirmation": False
        }

# ==================== SINGLETON INSTANCE ====================

_readiness_gate: Optional[NajikaReadinessGate] = None

def get_readiness_gate() -> NajikaReadinessGate:
    """Gibt die globale Readiness-Gate Instanz zurück"""
    global _readiness_gate
    if _readiness_gate is None:
        _readiness_gate = NajikaReadinessGate()
    return _readiness_gate

# ==================== API HELPERS ====================

def compute_readiness(najika_state: dict) -> dict:
    """API-freundliche Readiness-Berechnung"""
    gate = get_readiness_gate()
    state = gate.compute_readiness(najika_state)
    return state.to_dict()

def check_can_act(action: str, najika_state: dict) -> dict:
    """Prüft ob eine Aktion ausgeführt werden darf"""
    gate = get_readiness_gate()
    readiness = gate.compute_readiness(najika_state)
    guard_result = SystemGuard.check_action(action, readiness)

    return {
        "readiness": readiness.to_dict(),
        "action": action,
        "guard": guard_result,
        "autonomy_level": gate.autonomy_level
    }

# ==================== TEST ====================

if __name__ == "__main__":
    # Test mit verschiedenen States
    test_states = [
        {
            "name": "Perfekter Zustand",
            "emotion": {"joy": 0.8, "fear": 0.1, "anger": 0.0},
            "trust_level": 5,
            "user_autonomy_approval": True
        },
        {
            "name": "Ängstlicher Zustand",
            "emotion": {"joy": 0.2, "fear": 0.8, "anger": 0.1},
            "trust_level": 3,
            "user_autonomy_approval": None
        },
        {
            "name": "Neuer User",
            "emotion": {"joy": 0.5, "fear": 0.3, "anger": 0.0},
            "trust_level": 1,
            "user_autonomy_approval": None
        }
    ]

    gate = NajikaReadinessGate()

    for test in test_states:
        print(f"\n{'='*50}")
        print(f"Test: {test['name']}")
        print(f"{'='*50}")

        # Simuliere Interaktion
        gate.record_interaction()

        result = gate.compute_readiness(test)
        print(f"Score: {result.score:.3f}")
        print(f"Ready: {result.is_ready}")
        print(f"Autonomy Level: {gate.autonomy_level}")
        print(f"Allowed Actions: {gate.get_allowed_actions()}")
        print("\nReasons:")
        for reason in result.reasons:
            print(f"  [{reason.category}] {reason.description} ({reason.impact:+.2f})")
