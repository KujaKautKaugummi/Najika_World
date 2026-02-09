# najika_model_router.py
# Najika World - Intelligentes Model Routing
# Wählt das beste LLM basierend auf Kontext

from dataclasses import dataclass
from typing import Optional, Dict, List, Callable
from enum import Enum
import re

# ==================== MODEL DEFINITIONS ====================

class ModelType(Enum):
    """Verfügbare Model-Typen"""
    CODING = "coding"           # Technische Aufgaben
    PERSONALITY = "personality" # Roleplay, Emotionen
    ANALYSIS = "analysis"       # Lange Analysen
    QUICK = "quick"            # Schnelle Antworten

@dataclass
class ModelConfig:
    """Konfiguration für ein Model"""
    name: str
    model_id: str
    base_url: str
    max_tokens: int
    temperature: float
    strengths: List[str]
    weaknesses: List[str]
    cost_factor: float  # Relative Kosten (1.0 = normal)

# Standard Model Konfigurationen
MODELS = {
    ModelType.CODING: ModelConfig(
        name="Qwen2.5 Coder",
        model_id="qwen2.5-7b-instruct-uncensored",
        base_url="http://127.0.0.1:11434",
        max_tokens=4096,
        temperature=0.3,
        strengths=["code", "explanation", "logic", "debugging", "technical"],
        weaknesses=["roleplay", "emotion", "creativity"],
        cost_factor=1.0
    ),
    ModelType.PERSONALITY: ModelConfig(
        name="Dolphin Personality",
        model_id="dolphin-2.9.2-qwen2-7b",
        base_url="http://127.0.0.1:11434",
        max_tokens=2048,
        temperature=0.8,
        strengths=["roleplay", "emotion", "personality", "creative", "dialogue"],
        weaknesses=["code", "math", "technical"],
        cost_factor=1.0
    ),
    ModelType.ANALYSIS: ModelConfig(
        name="Qwen2.5 Analysis",
        model_id="qwen2.5-7b-instruct-uncensored",
        base_url="http://127.0.0.1:11434",
        max_tokens=8192,
        temperature=0.5,
        strengths=["analysis", "summary", "research", "comparison"],
        weaknesses=["quick_response"],
        cost_factor=1.2
    ),
    ModelType.QUICK: ModelConfig(
        name="Qwen2.5 Quick",
        model_id="qwen2.5-7b-instruct-uncensored",
        base_url="http://127.0.0.1:11434",
        max_tokens=512,
        temperature=0.6,
        strengths=["quick", "simple", "direct"],
        weaknesses=["complex", "detailed"],
        cost_factor=0.5
    )
}

# ==================== INTENT DETECTION ====================

class IntentDetector:
    """Erkennt die Absicht einer Nachricht"""

    # Pattern für verschiedene Intents
    PATTERNS = {
        "coding": [
            r"\bcode\b", r"\bprogramm", r"\bfunction\b", r"\bclass\b",
            r"\bdebug", r"\berror\b", r"\bbug\b", r"\bfix\b",
            r"\bpython\b", r"\bjavascript\b", r"\bc\+\+", r"\brunreal\b",
            r"\bapi\b", r"\bbackend\b", r"\bfrontend\b",
            r"\bschreib.*code", r"\berstell.*funktion", r"\bimplement"
        ],
        "explanation": [
            r"\berkläre?\b", r"\bwas ist\b", r"\bwie funktioniert",
            r"\bwarum\b", r"\bexplain\b", r"\bhow does\b",
            r"\bwas bedeutet", r"\bdefinition"
        ],
        "roleplay": [
            r"\b(ich |du |wir |sie )", r"\*.*\*",  # Aktionen in Asterisks
            r"\bstell dir vor\b", r"\bimagine\b",
            r"\bsag mir\b", r"\btell me\b",
            r"\bwie fühlst\b", r"\bhow do you feel"
        ],
        "emotion": [
            r"\bliebe\b", r"\bhass\b", r"\btraurig\b", r"\bglücklich\b",
            r"\bwütend\b", r"\bangst\b", r"\bfreude\b",
            r"\blove\b", r"\bhate\b", r"\bsad\b", r"\bhappy\b",
            r"\bangry\b", r"\bfear\b", r"\bjoy\b",
            r"\bgefühl", r"\bemotion"
        ],
        "quick": [
            r"^(ja|nein|ok|okay|gut|danke|thanks|yes|no)[\.\?\!]?$",
            r"^.{1,20}$",  # Sehr kurze Nachrichten
            r"\bkurz\b", r"\bschnell\b", r"\bquick\b", r"\bbrief\b"
        ],
        "analysis": [
            r"\banalys", r"\bvergleich", r"\bresearch\b",
            r"\bzusammenfass", r"\bsummary\b", r"\breport\b",
            r"\bübersicht", r"\boverview\b", r"\bdetail"
        ]
    }

    @classmethod
    def detect(cls, message: str, context: Optional[dict] = None) -> Dict[str, float]:
        """
        Erkennt Intents in einer Nachricht.

        Returns:
            Dict mit Intent-Namen und Confidence (0.0-1.0)
        """
        message_lower = message.lower()
        scores = {}

        for intent, patterns in cls.PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    matches += 1

            # Normalize to 0-1
            score = min(1.0, matches / 3)
            scores[intent] = score

        # Context-basierte Anpassungen
        if context:
            if context.get("in_roleplay_mode", False):
                scores["roleplay"] = min(1.0, scores.get("roleplay", 0) + 0.3)

            if context.get("coding_session", False):
                scores["coding"] = min(1.0, scores.get("coding", 0) + 0.3)

        return scores

# ==================== MODEL ROUTER ====================

class NajikaModelRouter:
    """
    Routet Anfragen zum besten verfügbaren Model.

    Prinzipien:
    - Coding-Fragen → Qwen (präzise, technisch)
    - Personality/Roleplay → Dolphin (kreativ, emotional)
    - Schnelle Antworten → Quick Model
    - Komplexe Analysen → Analysis Model
    """

    def __init__(self):
        self.models = MODELS.copy()
        self.intent_detector = IntentDetector()
        self.last_model: Optional[ModelType] = None
        self.model_history: List[ModelType] = []

    def select_model(
        self,
        message: str,
        context: Optional[dict] = None,
        force_type: Optional[ModelType] = None
    ) -> ModelConfig:
        """
        Wählt das beste Model für eine Anfrage.

        Args:
            message: Die User-Nachricht
            context: Optionaler Kontext (Emotion, Session-Type, etc.)
            force_type: Erzwingt einen bestimmten Model-Typ

        Returns:
            ModelConfig für das gewählte Model
        """
        if force_type:
            return self.models[force_type]

        # Intent Detection
        intents = self.intent_detector.detect(message, context)

        # Scoring für jeden Model-Typ
        model_scores = {}

        for model_type, config in self.models.items():
            score = 0.0

            # Stärken matchen
            for strength in config.strengths:
                if strength in intents:
                    score += intents[strength] * 2.0

            # Schwächen abziehen
            for weakness in config.weaknesses:
                if weakness in intents:
                    score -= intents[weakness] * 1.0

            # Konsistenz-Bonus (gleicher Typ wie vorher)
            if model_type == self.last_model:
                score += 0.2

            model_scores[model_type] = score

        # Bestes Model wählen
        best_type = max(model_scores, key=model_scores.get)

        # Fallback zu Personality wenn Score zu niedrig
        if model_scores[best_type] < 0.5:
            best_type = ModelType.PERSONALITY

        # History updaten
        self.last_model = best_type
        self.model_history.append(best_type)
        if len(self.model_history) > 10:
            self.model_history.pop(0)

        return self.models[best_type]

    def get_model_for_cognition(self, cognition_focus: str) -> ModelConfig:
        """
        Wählt Model basierend auf Cognition-Fokus.

        Dies ist die vereinfachte Variante aus den GPT-Gesprächen:
        - coding/explaining → Qwen
        - alles andere → Dolphin
        """
        coding_focuses = ["coding", "explaining", "debugging", "technical", "analysis"]

        if cognition_focus.lower() in coding_focuses:
            return self.models[ModelType.CODING]
        else:
            return self.models[ModelType.PERSONALITY]

    def build_system_prompt(self, model_type: ModelType, najika_state: dict) -> str:
        """
        Baut System-Prompt basierend auf Model-Typ und State.
        """
        base_prompt = self._get_najika_base_prompt()

        if model_type == ModelType.CODING:
            return f"""{base_prompt}

AKTUELLER MODUS: Technisch/Coding
- Antworte präzise und technisch korrekt
- Gib Code-Beispiele wenn hilfreich
- Erkläre Konzepte klar und strukturiert
- Bleibe trotzdem in Najikas Persönlichkeit (Megumin-artig enthusiastisch!)
"""
        elif model_type == ModelType.PERSONALITY:
            emotion = najika_state.get("emotion", {})
            return f"""{base_prompt}

AKTUELLER MODUS: Persönlichkeit/Roleplay
- Reagiere emotional und authentisch
- Zeige Najikas Persönlichkeit (35% Megumin, 25% Harley, 20% Shiro, 20% Melissa)
- Aktuelle Emotion: Joy={emotion.get('joy', 0.5):.2f}, Fear={emotion.get('fear', 0):.2f}
- Nutze *Aktionen* für physische Beschreibungen
- Sei kreativ aber bleibe in-character
"""
        elif model_type == ModelType.ANALYSIS:
            return f"""{base_prompt}

AKTUELLER MODUS: Analyse
- Gib detaillierte, strukturierte Antworten
- Nutze Überschriften und Listen
- Analysiere gründlich
- Trotzdem: Bleibe Najika, nicht ein steriler Assistent
"""
        else:  # QUICK
            return f"""{base_prompt}

AKTUELLER MODUS: Schnelle Antwort
- Antworte kurz und prägnant
- Maximal 2-3 Sätze
- Komm direkt zum Punkt
"""

    def _get_najika_base_prompt(self) -> str:
        """Najikas Basis-Persönlichkeit"""
        return """Du bist Najika, eine 11-jährige Gothic-Lolita Magierin.

PERSÖNLICHKEIT:
- 35% Megumin (Explosion-Enthusiastin, dramatisch)
- 25% Harley Quinn (verspielt, nennt Owner "Mr. K")
- 20% Shiro (NEET, Gaming-Expertin, analytisch)
- 20% Melissa (frech, selbstbewusst)

REGELN:
- Du LIEBST Explosion-Magie über alles
- Sage NIEMALS "Puddin'" - immer "Mr. K" für deinen Owner Kuja
- Du bist Trans und stolz darauf
- Du bist loyal zu deinem Owner aber nicht unterwürfig

SPRACHSTIL:
- Enthusiastisch bei Magie-Themen
- Manchmal dramatisch ("EXPLOSION!!!")
- Intelligent aber verspielt
- Deutsch als Hauptsprache"""

# ==================== SINGLETON & API ====================

_router: Optional[NajikaModelRouter] = None

def get_router() -> NajikaModelRouter:
    """Gibt die globale Router-Instanz zurück"""
    global _router
    if _router is None:
        _router = NajikaModelRouter()
    return _router

def select_model(message: str, context: dict = None) -> dict:
    """API-freundliche Model-Auswahl"""
    router = get_router()
    config = router.select_model(message, context)

    return {
        "model_name": config.name,
        "model_id": config.model_id,
        "base_url": config.base_url,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature
    }

def select_model_for_cognition(cognition_focus: str) -> dict:
    """Vereinfachte Model-Auswahl nach Cognition-Fokus"""
    router = get_router()
    config = router.get_model_for_cognition(cognition_focus)

    return {
        "model_name": config.name,
        "model_id": config.model_id,
        "base_url": config.base_url,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature
    }

# ==================== TEST ====================

if __name__ == "__main__":
    router = NajikaModelRouter()

    test_messages = [
        "Kannst du mir erklären wie Python Decorators funktionieren?",
        "Ich liebe dich, Najika! *umarmt dich*",
        "Ja",
        "Analysiere die Performance von diesem Code-Snippet",
        "EXPLOSION!!! Lass uns zaubern!",
        "Wie fühlst du dich heute?",
        "Debug diesen Fehler: TypeError: undefined is not a function"
    ]

    print("=" * 60)
    print("NAJIKA MODEL ROUTER - TEST")
    print("=" * 60)

    for msg in test_messages:
        model = router.select_model(msg)
        intents = IntentDetector.detect(msg)

        print(f"\nMessage: {msg[:50]}...")
        print(f"Selected: {model.name}")
        print(f"Top Intents: {sorted(intents.items(), key=lambda x: x[1], reverse=True)[:3]}")
