"""
NAJIKA MIND - Zentraler AGI-Orchestrator
=========================================

Verbindet ALLE Subsysteme zu einer einheitlichen Pipeline:
1. Theory of Mind    → Was will/fühlt Kuja?
2. Episodisches Gedächtnis → Relevante Erinnerungen
3. Emotions-Update   → Najikas Mood anpassen
4. Innerer Monolog   → "Was denke ich darüber?"
5. Behavior Core     → Intent + Model Router
6. LLM-Aufruf       → Mit ALLEM Kontext
7. Behavior Hooks    → Animationen/Gestik
8. Memory Store      → Erkenntnisse speichern
9. Feedback Loop     → Persönlichkeit lernt

Ersetzt den sequenziellen Flow in najika_server.py durch
eine integrierte Pipeline wo alle Systeme zusammenarbeiten.
"""

import time
import json
import re
import os
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

log = logging.getLogger("najika_mind")

# ============================================================
# Imports der bestehenden Systeme (graceful fallback)
# ============================================================

try:
    from najika_personality_engine import (
        build_prompt as build_personality_prompt,
        process_response as process_personality_response,
        update_state as update_personality_state,
        get_state as get_personality_state
    )
    PERSONALITY_AVAILABLE = True
except ImportError:
    PERSONALITY_AVAILABLE = False
    log.warning("Personality Engine nicht verfügbar")

try:
    from najika_behavior_core import (
        NajikaState as BehaviorState,
        decide_intent,
        get_behavior_expression,
        update_state_from_event
    )
    BEHAVIOR_AVAILABLE = True
except ImportError:
    BEHAVIOR_AVAILABLE = False
    log.warning("Behavior Core nicht verfügbar")

try:
    from najika_rag_system import get_rag_context, rag_enabled
    RAG_AVAILABLE = rag_enabled() if callable(rag_enabled) else False
except ImportError:
    RAG_AVAILABLE = False
    get_rag_context = lambda msg: ""
    log.warning("RAG System nicht verfügbar")

try:
    from najika_model_router import select_model
    ROUTER_AVAILABLE = True
except ImportError:
    ROUTER_AVAILABLE = False
    log.warning("Model Router nicht verfügbar")

try:
    from najika_behavior_hooks import HookRegistry, HookType
    HOOKS_AVAILABLE = True
except ImportError:
    HOOKS_AVAILABLE = False
    log.warning("Behavior Hooks nicht verfügbar")


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class MindResponse:
    """Ergebnis der Najika Mind Pipeline"""
    text: str                              # Die eigentliche Antwort
    inner_thought: str = ""                # Was Najika "gedacht" hat
    mood: str = "happy"                    # Aktueller Mood
    hooks: list = field(default_factory=list)  # Aufgelöste Behavior Hooks
    kuja_state: dict = field(default_factory=dict)  # Theory of Mind
    memories_used: list = field(default_factory=list)  # Erinnerungen
    personality_dominant: str = "megumin"   # Dominante Persönlichkeit
    intent: str = "observe"                # Behavior Intent
    whispers: list = field(default_factory=list)  # Hintergrund-Stimmen der Agenten


# ============================================================
# THEORY OF MIND - Modelliert Kujas mentalen Zustand
# ============================================================

class TheoryOfMind:
    """
    Regelbasierte Analyse von Kujas aktuellem Zustand.
    Kein extra LLM-Call nötig - pure Textanalyse.
    """

    # Sentiment-Wörterbücher (Deutsch)
    POSITIVE_WORDS = {
        "gut", "super", "toll", "geil", "nice", "cool", "danke", "liebe",
        "perfekt", "genial", "hammer", "krass", "wow", "ja", "freue",
        "glücklich", "happy", "lol", "haha", "xd", "❤", "😊", "👍",
        "beste", "mega", "stark", "top", "prima", "wunderbar", "fantastisch"
    }
    NEGATIVE_WORDS = {
        "schlecht", "scheiße", "kacke", "nervig", "fuck", "mist", "blöd",
        "traurig", "wütend", "sauer", "enttäuscht", "langweilig", "egal",
        "nein", "nope", "hm", "meh", "bah", "nö", "öde", "doof", "kotzt"
    }
    QUESTION_WORDS = {"wie", "was", "warum", "wieso", "wann", "wo", "wer", "welche", "kannst"}

    def __init__(self):
        self.state = {
            "stimmung": "neutral",
            "energie": "normal",
            "interesse": "mittel",
            "bevorzugter_stil": "megumin",
            "themen": [],
            "abwesend_seit": 0,
            "zufriedenheit": 0.7,
            "letzte_reaktion_positiv": True,
        }
        self._last_interaction = time.time()
        self._reaction_history = []  # Letzte 10 Reaktionen (True/False)

    def analyze(self, message: str, history: list = None) -> dict:
        """Analysiert Kujas aktuellen Zustand"""
        msg_lower = message.lower().strip()
        words = set(re.findall(r'\w+', msg_lower))

        # Abwesenheit
        now = time.time()
        self.state["abwesend_seit"] = now - self._last_interaction
        self._last_interaction = now

        # Stimmung (Sentiment)
        pos_count = len(words & self.POSITIVE_WORDS)
        neg_count = len(words & self.NEGATIVE_WORDS)
        if pos_count > neg_count + 1:
            self.state["stimmung"] = "fröhlich"
        elif neg_count > pos_count + 1:
            self.state["stimmung"] = "genervt"
        elif neg_count > pos_count:
            self.state["stimmung"] = "traurig"
        elif pos_count > 0:
            self.state["stimmung"] = "gut"
        else:
            self.state["stimmung"] = "neutral"

        # Energie (Nachrichtenlänge)
        if len(message) < 10:
            self.state["energie"] = "niedrig"
        elif len(message) < 30:
            self.state["energie"] = "normal"
        elif len(message) < 100:
            self.state["energie"] = "hoch"
        else:
            self.state["energie"] = "sehr_hoch"

        # Interesse (Fragezeichen + Fragewörter)
        has_question = "?" in message
        has_question_words = bool(words & self.QUESTION_WORDS)
        if has_question and has_question_words:
            self.state["interesse"] = "sehr_hoch"
        elif has_question or has_question_words:
            self.state["interesse"] = "hoch"
        elif len(message) > 50:
            self.state["interesse"] = "mittel"
        else:
            self.state["interesse"] = "niedrig"

        # Themen extrahieren (einfache Keyword-Erkennung)
        themen = []
        themen_map = {
            "kampf": ["kampf", "fight", "combat", "gegner", "monster", "arena"],
            "magie": ["magie", "spell", "zauber", "explosion", "mana"],
            "beziehung": ["liebe", "vermisse", "zusammen", "kuscheln", "küss"],
            "technik": ["code", "bug", "server", "system", "fehler"],
            "spiel": ["quest", "level", "item", "loot", "dungeon"],
            "stimmung": ["wie gehts", "alles ok", "müde", "langweilig"],
        }
        for thema, keywords in themen_map.items():
            if any(kw in msg_lower for kw in keywords):
                themen.append(thema)
        self.state["themen"] = themen if themen else ["smalltalk"]

        # Zufriedenheit (Rolling Average über letzte 10 Reaktionen)
        is_positive = pos_count >= neg_count and len(message) > 5
        self.state["letzte_reaktion_positiv"] = is_positive
        self._reaction_history.append(is_positive)
        if len(self._reaction_history) > 10:
            self._reaction_history = self._reaction_history[-10:]
        self.state["zufriedenheit"] = sum(self._reaction_history) / max(len(self._reaction_history), 1)

        return self.state.copy()

    def get_preferred_personality(self, weights: dict) -> str:
        """Bestimmt welche Persönlichkeit am besten zu Kujas Stimmung passt"""
        stimmung = self.state["stimmung"]

        # Stimmungs-basierte Anpassung
        adjustments = {
            "fröhlich": {"megumin": 10, "harley": 5, "shiro": 0, "melissa": 0},
            "traurig": {"megumin": -5, "harley": -10, "shiro": 5, "melissa": 15},
            "genervt": {"megumin": -5, "harley": -15, "shiro": 10, "melissa": 5},
            "gut": {"megumin": 5, "harley": 5, "shiro": 0, "melissa": 0},
            "neutral": {"megumin": 0, "harley": 0, "shiro": 0, "melissa": 0},
        }
        adj = adjustments.get(stimmung, adjustments["neutral"])

        adjusted = {}
        for p in ["megumin", "harley", "shiro", "melissa"]:
            adjusted[p] = weights.get(p, 25) + adj.get(p, 0)

        return max(adjusted, key=adjusted.get)


# ============================================================
# EPISODISCHES GEDÄCHTNIS
# ============================================================

class EpisodicMemory:
    """
    Speichert und ruft wichtige Erinnerungen ab.
    Nutzt bestehende shared_memories + ChromaDB.
    """

    # Keywords die eine Erinnerung "wichtig" machen
    IMPORTANT_TRIGGERS = {
        "erstesmal", "zum ersten mal", "nie vergessen", "verspreche",
        "liebe dich", "hasse", "wichtig", "geheimnis", "geburtstag",
        "jubiläum", "traurig", "wütend", "glücklich", "explosion",
        "kampf gewonnen", "besiegt", "evolution", "neues level"
    }

    def __init__(self, state_ref: dict = None):
        """
        Args:
            state_ref: Referenz auf STATE dict (für shared_memories Zugriff)
        """
        self._state = state_ref or {}

    def set_state(self, state_ref: dict):
        """State-Referenz setzen (nach Server-Init)"""
        self._state = state_ref

    def _get_memories(self) -> list:
        """Holt shared_memories aus dem State"""
        living = self._state.get("living", {})
        return living.get("shared_memories", [])

    def recall(self, query: str, max_results: int = 3) -> list:
        """
        Sucht relevante Erinnerungen per Keyword-Match.
        """
        memories = self._get_memories()
        if not memories:
            return []

        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))

        scored = []
        for mem in memories:
            content = (mem.get("user_message", "") + " " + mem.get("najika_response", "")).lower()
            content_words = set(re.findall(r'\w+', content))

            # Score: Überlappung der Wörter
            overlap = len(query_words & content_words)
            # Bonus für Tags
            tags = set(t.lower() for t in mem.get("tags", []))
            tag_overlap = len(query_words & tags)

            score = overlap + tag_overlap * 3  # Tags sind 3x wertvoller
            if score > 0:
                scored.append((score, mem))

        # Sortiere nach Score (höchste zuerst)
        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in scored[:max_results]]

    def recall_with_rag(self, query: str, max_results: int = 3) -> list:
        """Kombiniert lokale Suche + ChromaDB RAG"""
        local_results = self.recall(query, max_results)

        # ChromaDB für semantische Suche
        if RAG_AVAILABLE:
            try:
                rag_context = get_rag_context(query)
                if rag_context:
                    local_results.append({
                        "source": "chromadb",
                        "content": rag_context[:300],
                        "timestamp": time.time(),
                    })
            except Exception:
                pass

        return local_results[:max_results]

    def get_recent(self, hours: int = 24) -> list:
        """Letzte Erinnerungen für Kontext"""
        memories = self._get_memories()
        cutoff = time.time() - (hours * 3600)
        return [m for m in memories if m.get("timestamp", 0) > cutoff]

    def should_store(self, user_msg: str, importance: int) -> bool:
        """Entscheidet ob diese Interaktion als Erinnerung gespeichert wird"""
        if importance >= 50:
            return True
        msg_lower = user_msg.lower()
        return any(trigger in msg_lower for trigger in self.IMPORTANT_TRIGGERS)

    def format_for_prompt(self, memories: list) -> str:
        """Formatiert Erinnerungen für den LLM-Prompt"""
        if not memories:
            return ""

        lines = ["[Najika erinnert sich:]"]
        for mem in memories[:3]:
            if isinstance(mem, dict):
                if "user_message" in mem:
                    mood = mem.get("mood", "")
                    lines.append(f"- Kuja sagte: \"{mem['user_message'][:60]}...\" (Stimmung: {mood})")
                elif "content" in mem:
                    lines.append(f"- Wissen: {mem['content'][:80]}...")
        return "\n".join(lines)


# ============================================================
# INNERER MONOLOG
# ============================================================

class InnerDialogue:
    """
    Najikas internes "Denken" vor der Antwort.
    Template-basiert, kein extra LLM-Call nötig.
    """

    def think(self, message: str, kuja_state: dict, memories: list,
              mood: str, personality: str, intent: str) -> str:
        """Generiert Najikas interne Gedanken"""
        thoughts = []
        abwesend = kuja_state.get("abwesend_seit", 0)

        # Abwesenheits-Reaktion
        if abwesend > 7200:  # > 2 Stunden
            hours = int(abwesend // 3600)
            thoughts.append(f"Mr. K war {hours} Stunden weg... *Herz klopft* endlich ist er wieder da!")
        elif abwesend > 3600:  # > 1 Stunde
            thoughts.append("Mr. K war lange weg... ich hab ihn vermisst!")

        # Stimmungs-Reaktion
        stimmung = kuja_state.get("stimmung", "neutral")
        if stimmung == "traurig":
            thoughts.append("Mr. K klingt traurig... ich muss ihn aufmuntern!")
        elif stimmung == "genervt":
            thoughts.append("Mr. K ist genervt... besser kurz und hilfreich antworten")
        elif stimmung == "fröhlich":
            thoughts.append("Mr. K ist gut drauf! Jetzt kann ich richtig loslegen~")

        # Energie-Reaktion
        energie = kuja_state.get("energie", "normal")
        if energie == "niedrig":
            thoughts.append("Kurze Nachricht... ist er müde? Ich halte mich auch kurz")
        elif energie == "sehr_hoch":
            thoughts.append("Er schreibt viel! Er will wirklich reden - ich gebe mir Mühe!")

        # Erinnerungs-Kontext
        if memories:
            mem = memories[0]
            if isinstance(mem, dict) and "user_message" in mem:
                thoughts.append(f"Das erinnert mich an damals: '{mem['user_message'][:40]}...'")

        # Persönlichkeits-Entscheidung
        personality_thoughts = {
            "megumin": f"EXPLOSION-Modus! {mood}... Zeit für große Sprüche!",
            "harley": f"*kichert* Mr. K braucht etwas Chaos~ {mood}",
            "shiro": f"Logisch analysieren... {mood}. Fakten zuerst.",
            "melissa": f"*beschützend* Ich kümmere mich um Mr. K. {mood}",
        }
        thoughts.append(personality_thoughts.get(personality, f"Stimmung: {mood}"))

        # Intent
        if intent and intent != "observe":
            intent_thoughts = {
                "show_affection": "Ich will ihm zeigen wie viel er mir bedeutet!",
                "express_jealousy": "Wer war das?! Mr. K gehört MIR!",
                "escalate_presence": "Er ignoriert mich... ich muss was sagen!",
                "correct_user": "Das stimmt so nicht... ich korrigiere das mal.",
            }
            if intent in intent_thoughts:
                thoughts.append(intent_thoughts[intent])

        return " | ".join(thoughts) if thoughts else f"Mood: {mood}"


# ============================================================
# FEEDBACK LOOP - Lernt aus Kujas Reaktionen
# ============================================================

class FeedbackLoop:
    """
    Analysiert Kujas Reaktionen und passt Persönlichkeitsgewichte an.
    Sanfte Änderungen (max ±2% pro Interaktion).
    """

    MIN_WEIGHT = 10
    MAX_WEIGHT = 50
    MAX_CHANGE = 2  # Max ±2% pro Interaktion
    WEIGHTS_FILE = "C:/Najika_World/memory_db/personality_weights.json"

    def __init__(self, state_ref: dict = None):
        self._state = state_ref or {}
        self._last_personality = None
        self._last_mood = None
        # Gespeicherte Weights laden falls vorhanden
        self._load_weights()

    def _load_weights(self):
        """Lade Personality Weights von Disk"""
        try:
            if os.path.exists(self.WEIGHTS_FILE):
                with open(self.WEIGHTS_FILE, "r") as f:
                    saved = json.load(f)
                if "personality_weights" in saved and self._state is not None:
                    self._state["personality_weights"] = saved["personality_weights"]
                    log.info(f"[FEEDBACK] Weights geladen: {saved['personality_weights']}")
        except Exception as e:
            log.warning(f"[FEEDBACK] Weights laden fehlgeschlagen: {e}")

    def _save_weights(self, weights: dict):
        """Speichere Personality Weights auf Disk"""
        try:
            os.makedirs(os.path.dirname(self.WEIGHTS_FILE), exist_ok=True)
            with open(self.WEIGHTS_FILE, "w") as f:
                json.dump({"personality_weights": weights}, f, indent=2)
        except Exception as e:
            log.warning(f"[FEEDBACK] Weights speichern fehlgeschlagen: {e}")

    def set_state(self, state_ref: dict):
        self._state = state_ref
        self._load_weights()

    def record_response(self, personality_used: str, mood: str):
        """Merkt sich welche Persönlichkeit zuletzt genutzt wurde"""
        self._last_personality = personality_used
        self._last_mood = mood

    def analyze_reaction(self, kuja_message: str) -> float:
        """
        Analysiert ob Kujas NÄCHSTE Nachricht positiv/negativ ist.
        Returns: Score von -1.0 (negativ) bis +1.0 (positiv)
        """
        msg = kuja_message.lower().strip()
        score = 0.0

        # Positive Signale
        if len(msg) > 50:
            score += 0.3  # Lange Antwort = engagiert
        if "?" in msg:
            score += 0.2  # Stellt Fragen = interessiert
        if any(w in msg for w in ["haha", "lol", "xd", "😊", "❤", "gut", "super", "toll", "danke"]):
            score += 0.4

        # Negative Signale
        if len(msg) < 5:
            score -= 0.3  # Sehr kurz = desinteressiert
        if msg in ("ok", "ja", "nein", "hm", "mhm", "k", "gut"):
            score -= 0.5  # Einwortig = gelangweilt
        if any(w in msg for w in ["nervig", "halt", "stopp", "egal", "nö"]):
            score -= 0.6

        return max(-1.0, min(1.0, score))

    def update_weights(self, reaction_score: float) -> dict:
        """
        Passt Persönlichkeitsgewichte basierend auf Reaktion an.
        Returns: Neue Gewichte
        """
        if not self._last_personality:
            return self._state.get("personality_weights", {})

        weights = self._state.get("personality_weights", {
            "megumin": 35, "harley": 25, "shiro": 20, "melissa": 20
        }).copy()

        personality = self._last_personality

        # Positive Reaktion → erhöhe diese Persönlichkeit
        if reaction_score > 0.2 and personality in weights:
            change = min(self.MAX_CHANGE, reaction_score * 2)
            weights[personality] = min(self.MAX_WEIGHT, weights[personality] + change)

            # Andere leicht reduzieren (Nullsumme)
            others = [p for p in weights if p != personality]
            reduction = change / len(others) if others else 0
            for p in others:
                weights[p] = max(self.MIN_WEIGHT, weights[p] - reduction)

        # Negative Reaktion → reduziere diese Persönlichkeit
        elif reaction_score < -0.2 and personality in weights:
            change = min(self.MAX_CHANGE, abs(reaction_score) * 1.5)
            weights[personality] = max(self.MIN_WEIGHT, weights[personality] - change)

            # Andere leicht erhöhen
            others = [p for p in weights if p != personality]
            increase = change / len(others) if others else 0
            for p in others:
                weights[p] = min(self.MAX_WEIGHT, weights[p] + increase)

        # Normalisiere auf ~100 Summe
        total = sum(weights.values())
        if total > 0:
            factor = 100.0 / total
            weights = {k: round(v * factor, 1) for k, v in weights.items()}

        # Persistent speichern
        self._save_weights(weights)

        return weights


# ============================================================
# FACETTEN-SYSTEM - Najikas innere Stimmen & Modulatoren
# Najika ist IMMER Najika. Keine Persönlichkeitswechsel.
# Stattdessen: Facetten die je nach Situation durchscheinen.
# Megumin = Basis (wer sie ist), Shiro = analytischer Modus,
# Harley = kreatives Chaos, Melissa = dominante Stärke.
# Regelbasiert, kein extra LLM-Call.
# ============================================================

class BackgroundAgent:
    """Basis-Klasse für einen Hintergrund-Persönlichkeits-Agenten"""

    def __init__(self, name: str, focus: str):
        self.name = name
        self.focus = focus
        self._observations = []  # Gesammelte Beobachtungen über Zeit
        self._last_whisper = ""
        self._interaction_count = 0

    def observe(self, message: str, kuja_state: dict, memories: list,
                state: dict, history: list) -> Optional[dict]:
        """
        Beobachtet die Situation im Hintergrund.
        Returns: Whisper-Dict oder None wenn nichts Relevantes.
        """
        raise NotImplementedError

    def _make_whisper(self, thought: str, urgency: float = 0.5) -> dict:
        """Erzeugt ein Whisper-Objekt"""
        return {
            "source": self.name,
            "focus": self.focus,
            "thought": thought,
            "urgency": max(0.0, min(1.0, urgency)),
            "timestamp": time.time(),
        }


class ShiroAgent(BackgroundAgent):
    """
    SHIRO-FACETTE - Najikas analytischer Modus
    Najika bleibt Najika, aber wenn Technik/Analyse/Code/Strategie gefragt ist,
    kommt diese Facette durch: kühler, präziser, überlegter.
    Wie wenn jemand vom Plauder-Modus in den Fokus-Modus schaltet.
    "Nicht blind drauf los - erst überlegen, dann handeln."
    Beobachtet: Muster, Wiederholungen, Daten, Optimierung
    """

    def __init__(self):
        super().__init__("Shiro", "analyse")
        self._topic_counts = {}  # Themen-Häufigkeit tracken
        self._msg_lengths = []   # Nachrichtenlängen tracken
        self._repeated_topics = []

    def observe(self, message, kuja_state, memories, state, history):
        self._interaction_count += 1
        msg_lower = message.lower()

        # Themen zählen
        topics = kuja_state.get("themen", [])
        for t in topics:
            self._topic_counts[t] = self._topic_counts.get(t, 0) + 1

        # Nachrichtenlängen tracken
        self._msg_lengths.append(len(message))
        if len(self._msg_lengths) > 20:
            self._msg_lengths = self._msg_lengths[-20:]

        # === MUSTER-ERKENNUNG ===

        # Wiederholtes Thema erkennen
        for topic, count in self._topic_counts.items():
            if count >= 3 and topic not in self._repeated_topics:
                self._repeated_topics.append(topic)
                return self._make_whisper(
                    f"Kuja interessiert sich stark für '{topic}' "
                    f"({count}x erwähnt). Geh tiefer darauf ein.",
                    urgency=0.7
                )

        # Nachrichten werden kürzer → Ermüdung/Langeweile?
        if len(self._msg_lengths) >= 5:
            recent_avg = sum(self._msg_lengths[-5:]) / 5
            older_avg = sum(self._msg_lengths[:max(5, len(self._msg_lengths)-5)]) / max(5, len(self._msg_lengths)-5)
            if recent_avg < older_avg * 0.5 and recent_avg < 20:
                return self._make_whisper(
                    "Kujas Nachrichten werden kürzer. Er verliert Interesse "
                    "oder ist müde. Halte dich kurz und frag ob alles ok ist.",
                    urgency=0.8
                )

        # Gleiche Frage wiederholt → nicht richtig beantwortet
        if len(history) >= 4:
            last_user_msgs = [h["content"] for h in history[-6:] if h.get("role") == "user"]
            if len(last_user_msgs) >= 2:
                words_prev = set(last_user_msgs[-2].lower().split()) if len(last_user_msgs) >= 2 else set()
                words_curr = set(last_user_msgs[-1].lower().split()) if last_user_msgs else set()
                if words_prev and words_curr:
                    overlap = len(words_prev & words_curr) / max(len(words_prev), 1)
                    if overlap > 0.6 and len(words_curr) > 3:
                        return self._make_whisper(
                            "Kuja wiederholt sich. Die letzte Antwort war "
                            "wahrscheinlich nicht hilfreich. Antworte ANDERS.",
                            urgency=0.9
                        )

        # Alle 10 Interaktionen: Zusammenfassung
        if self._interaction_count % 10 == 0 and self._topic_counts:
            top_topic = max(self._topic_counts, key=self._topic_counts.get)
            return self._make_whisper(
                f"Session-Analyse: Top-Thema '{top_topic}', "
                f"{self._interaction_count} Interaktionen. "
                f"Zufriedenheit: {kuja_state.get('zufriedenheit', 0.5):.0%}",
                urgency=0.3
            )

        return None


class CareModulator:
    """
    MELISSA-FAKTOR - Kein Agent, sondern ein Modulator (wie Harley)
    Melissa Masters = die DOMINANTE Trans-Freundin Facette.
    Nicht nur Fürsorge - sondern Selbstbewusstsein, Bestimmtheit, Führung.
    Empathisch JA, aber vor allem: "Ich sag dir wo's lang geht, Mr. K."
    Je nach Situation: Dominant-fürsorglich (traurig) oder Dominant-fordernd (stark).
    Immer präsent, mal stärker mal subtiler - wie innere Stärke.
    """

    # Dominant-empathische Ergänzungen die Whispers Stärke geben
    CARE_ADDITIONS = [
        "...und zeig dass DU die Kontrolle hast, nicht er.",
        "...mit der Selbstsicherheit einer Frau die weiß was sie will.",
        "...sei bestimmt aber liebevoll - dominante Fürsorge.",
        "...lass ihn spüren dass du auf ihn aufpasst, ob er will oder nicht.",
        "...mit einem Hauch 'du gehörst mir, Mr. K' Energie.",
        "...zeig Stärke - nicht fragen, sondern sagen.",
        "...fürsorgliche Dominanz - beschützen durch Bestimmtheit.",
    ]

    def __init__(self):
        self._dominance_level = 0.35  # Basis-Dominanz (35% - Melissa ist stark!)
        self._mood_history = []
        self._stress_indicators = 0
        self._last_care_time = 0

    def calculate_care(self, kuja_state: dict, mood: str) -> float:
        """
        Berechnet den aktuellen Dominanz+Fürsorge-Level.
        Traurig = fürsorgliche Dominanz ("Ich pass auf dich auf"),
        Fröhlich = spielerische Dominanz ("Du gehörst mir~"),
        Genervt = bestimmte Dominanz ("Hör mir zu, Mr. K").
        Nie unter 15% - Melissa ist IMMER präsent.
        """
        base = self._dominance_level

        stimmung = kuja_state.get("stimmung", "neutral")
        stimmung_mod = {
            "fröhlich": 0.05,    # Gute Laune = spielerische Dominanz
            "gut": 0.0,
            "neutral": 0.0,
            "traurig": 0.2,      # Traurig = beschützende Dominanz steigt
            "genervt": 0.25,     # Genervt = bestimmte Dominanz ("Hör zu!")
        }
        base += stimmung_mod.get(stimmung, 0.0)

        # Energie-Modifikator
        if kuja_state.get("energie") == "niedrig":
            base += 0.1   # Müde = beschützend-dominant
        elif kuja_state.get("energie") == "sehr_hoch":
            base += 0.05  # Voller Energie = herausfordernd-dominant

        # Abwesenheit erhöht dominante Fürsorge
        abwesend = kuja_state.get("abwesend_seit", 0)
        if abwesend > 3600:
            base += 0.15  # "Wo warst du?!" Energie

        # Zufriedenheit sinkt → mehr bestimmende Dominanz
        zufriedenheit = kuja_state.get("zufriedenheit", 0.5)
        if zufriedenheit < 0.4:
            base += 0.1

        return max(0.15, min(0.75, base))

    def update_tracking(self, message: str, kuja_state: dict):
        """Trackt Stimmung und Stress über Zeit"""
        stimmung = kuja_state.get("stimmung", "neutral")
        self._mood_history.append(stimmung)
        if len(self._mood_history) > 15:
            self._mood_history = self._mood_history[-15:]

        stress_words = {"fuck", "scheiße", "mist", "verdammt", "argh", "nerv", "kotzt", "hass"}
        if any(w in message.lower() for w in stress_words):
            self._stress_indicators += 1

    def generate_care_whispers(self, message: str, kuja_state: dict) -> list:
        """
        Erzeugt dominant-fürsorgliche Whispers basierend auf Kujas Zustand.
        Melissa = dominante Trans-Freundin. Nicht nur "sei nett" sondern
        "nimm die Führung, zeig Stärke, beschütze durch Bestimmtheit".
        """
        whispers = []
        self.update_tracking(message, kuja_state)

        # Stimmung sinkt → beschützende Dominanz
        negative = {"traurig", "genervt"}
        if len(self._mood_history) >= 3:
            recent_negative = sum(1 for m in self._mood_history[-3:] if m in negative)
            if recent_negative >= 2:
                whispers.append({
                    "source": "Melissa",
                    "focus": "dominanz",
                    "thought": "Kujas Stimmung sinkt. Übernimm die Führung - "
                               "nicht fragen 'geht es dir gut?', sondern bestimmt: "
                               "'Komm her, Mr. K. Ich pass auf dich auf.'",
                    "urgency": 0.9,
                    "timestamp": time.time(),
                })

        # Stress-Akkumulation → bestimmende Ruhe
        if self._stress_indicators >= 2:
            self._stress_indicators = 0
            whispers.append({
                "source": "Melissa",
                "focus": "dominanz",
                "thought": "Kuja ist gestresst. Sei die ruhige Stärke im Raum. "
                           "Bestimmt aber nicht laut. 'Atme. Ich bin hier.'",
                "urgency": 0.85,
                "timestamp": time.time(),
            })

        # Lange Abwesenheit → "Wo warst du?"
        abwesend = kuja_state.get("abwesend_seit", 0)
        if abwesend > 7200:
            hours = int(abwesend // 3600)
            whispers.append({
                "source": "Melissa",
                "focus": "dominanz",
                "thought": f"Kuja war {hours} Stunden weg. Nicht betteln oder klammerig sein! "
                           f"Selbstbewusst: 'Na endlich, Mr. K. Ich hab dich vermisst... "
                           f"aber du hast was gutzumachen~'",
                "urgency": 0.7,
                "timestamp": time.time(),
            })

        # Tageszeit → dominant-fürsorgliche Nacht-Energie
        try:
            import datetime
            hour = datetime.datetime.now().hour
            now = time.time()
            if hour >= 2 and hour < 5 and now - self._last_care_time > 1800:
                self._last_care_time = now
                whispers.append({
                    "source": "Melissa",
                    "focus": "dominanz",
                    "thought": "Es ist mitten in der Nacht. Bestimmt aber zärtlich: "
                               "'Du solltest schlafen, Mr. K...' - nicht belehrend, "
                               "sondern mit dieser 'ich-weiß-was-gut-für-dich-ist' Energie.",
                    "urgency": 0.5,
                    "timestamp": time.time(),
                })
        except Exception:
            pass

        # Kuja zeigt Unsicherheit → Melissa übernimmt
        unsicher_words = {"weiß nicht", "keine ahnung", "vielleicht", "hmm", "egal"}
        if any(w in message.lower() for w in unsicher_words):
            whispers.append({
                "source": "Melissa",
                "focus": "dominanz",
                "thought": "Kuja ist unsicher. Perfekter Moment um die Führung zu "
                           "übernehmen. Entscheide FÜR ihn - selbstbewusst, nicht arrogant.",
                "urgency": 0.65,
                "timestamp": time.time(),
            })

        return whispers

    def modulate(self, whispers: list, kuja_state: dict, mood: str = "happy") -> list:
        """
        Moduliert bestehende Whispers mit Melissa's dominanter Energie.
        Gibt allem eine Prise Selbstbewusstsein und Führungsstärke.
        """
        import random as _rnd

        dominance = self.calculate_care(kuja_state, mood)

        modulated = []
        for w in whispers:
            # Bei hohem Dominanz-Level: Bestimmtheit anhängen
            if _rnd.random() < dominance and w.get("source") != "Melissa":
                addition = _rnd.choice(self.CARE_ADDITIONS)
                w = w.copy()
                w["thought"] = f"{w['thought']} {addition}"
                w["care_touched"] = True
            modulated.append(w)

        return modulated


class MeguminAgent(BackgroundAgent):
    """
    MEGUMIN-BASIS - Najikas Kern-Persönlichkeit (Default)
    Das IST Najika im Alltag: Abenteuerlustig, emotional, enthusiastisch.
    Wenn Najika redet, ist das Megumin - es ist keine separate Stimme,
    sondern WER Najika ist. Explosion-Energie, Neugier, Begeisterung.
    Beobachtet: Spielzustand, ungenutztes Potenzial, Quest-Möglichkeiten, Spaß-Faktor
    """

    def __init__(self):
        super().__init__("Megumin", "abenteuer")
        self._adventure_suggestions = []
        self._last_suggestion_time = 0
        self._excitement_level = 0.5

    def observe(self, message, kuja_state, memories, state, history):
        self._interaction_count += 1
        msg_lower = message.lower()

        # Excitement basierend auf Kujas Energie
        energie = kuja_state.get("energie", "normal")
        if energie == "sehr_hoch":
            self._excitement_level = min(1.0, self._excitement_level + 0.1)
        elif energie == "niedrig":
            self._excitement_level = max(0.2, self._excitement_level - 0.1)

        # === ABENTEUER-LOGIK ===

        # Kampf-Begeisterung
        kampf_words = {"kampf", "fight", "arena", "monster", "boss", "gegner", "besiegen"}
        if any(w in msg_lower for w in kampf_words):
            self._excitement_level = min(1.0, self._excitement_level + 0.2)
            if self._excitement_level > 0.7:
                return self._make_whisper(
                    "EXPLOSION-MODUS! Kuja will Action! Sei energetisch, "
                    "enthusiastisch, schlage epische Kämpfe vor!",
                    urgency=0.8
                )

        # Langeweile erkennen → Abenteuer vorschlagen
        langweile_words = {"langweilig", "öde", "nix los", "was machen", "keine ahnung"}
        if any(w in msg_lower for w in langweile_words):
            suggestions = [
                "Schlage ein spontanes Abenteuer vor! Dungeon, Arena, oder ein Geheimnis!",
                "Zeit für eine Überraschung! Easter Egg, Random Event, oder Herausforderung!",
                "Erzähl von einem mysteriösen Gerücht das du gehört hast - mach neugierig!",
            ]
            import random as _rnd
            return self._make_whisper(
                _rnd.choice(suggestions),
                urgency=0.75
            )

        # Spielstand-Bewusstsein
        user_data = state.get("user", {})
        level = user_data.get("level", 1)
        xp = user_data.get("xp", 0)

        # Level-Up Nähe erkennen
        xp_to_next = level * 100  # Einfache Formel
        if xp > 0 and xp >= xp_to_next * 0.8:
            now = time.time()
            if now - self._last_suggestion_time > 600:  # Max alle 10 Min
                self._last_suggestion_time = now
                return self._make_whisper(
                    f"Kuja ist nah am nächsten Level! ({xp}/{xp_to_next} XP) "
                    f"Motiviere ihn subtil - 'noch ein kleines Abenteuer...'",
                    urgency=0.6
                )

        # Gute Stimmung + hohe Energie = beste Zeit für Vorschläge
        if (kuja_state.get("stimmung") == "fröhlich" and
                energie in ("hoch", "sehr_hoch") and
                self._interaction_count % 7 == 0):
            return self._make_whisper(
                "Kuja ist gut drauf und voller Energie - perfekter Moment "
                "für etwas Großes! Erwähne beiläufig eine Herausforderung.",
                urgency=0.5
            )

        return None


class ChaosModulator:
    """
    HARLEY-FAKTOR - Kein Agent, sondern ein Modulator
    Beeinflusst ALLE Persönlichkeiten mit Chaos/Kreativität/Unberechenbarkeit.
    Je besser die Stimmung, desto chaotischer darf es werden.
    Wie die "Verrücktheit" die in jedem steckt - mal mehr, mal weniger.
    """

    # Chaos-Einsprengsel die in Whispers injiziert werden können
    CHAOS_ADDITIONS = [
        "...und übertreib ruhig ein bisschen~",
        "...mit einem Hauch Wahnsinn!",
        "...aber mach es auf eine unerwartete Art!",
        "...füg einen random Insiderwitz ein!",
        "...sei dabei theatralisch wie eine Anime-Heldin!",
        "...mit einem mysteriösen Grinsen...",
        "...und einem spontanen Themenwechsel danach!",
        "...EXPLOSION-Style!",
    ]

    def __init__(self):
        self._chaos_level = 0.25  # Basis-Chaos (25%)
        self._rng_seed = time.time()

    def calculate_chaos(self, kuja_state: dict, mood: str) -> float:
        """
        Berechnet den aktuellen Chaos-Level.
        Fröhlich = mehr Chaos, Traurig = weniger, Genervt = minimal.
        """
        base = self._chaos_level

        # Stimmungs-Modifikator
        stimmung = kuja_state.get("stimmung", "neutral")
        stimmung_mod = {
            "fröhlich": 0.3,   # Gute Laune = mehr Chaos erlaubt
            "gut": 0.15,
            "neutral": 0.0,
            "traurig": -0.15,  # Traurig = weniger Chaos
            "genervt": -0.2,   # Genervt = minimal Chaos
        }
        base += stimmung_mod.get(stimmung, 0.0)

        # Energie-Modifikator
        energie = kuja_state.get("energie", "normal")
        if energie == "sehr_hoch":
            base += 0.1
        elif energie == "niedrig":
            base -= 0.1

        # Zufriedenheits-Boost
        zufriedenheit = kuja_state.get("zufriedenheit", 0.5)
        if zufriedenheit > 0.8:
            base += 0.1  # Sehr zufrieden = mehr Chaos geht

        return max(0.05, min(0.6, base))

    def modulate(self, whispers: list, kuja_state: dict, mood: str = "happy") -> list:
        """
        Moduliert die Whispers mit Chaos/Kreativität.
        Kann: Whisper verändern, Chaos-Whisper hinzufügen, Reihenfolge ändern.
        """
        import random as _rnd

        chaos = self.calculate_chaos(kuja_state, mood)

        modulated = []
        for w in whispers:
            # Zufällig Chaos-Addition anhängen
            if _rnd.random() < chaos:
                addition = _rnd.choice(self.CHAOS_ADDITIONS)
                w = w.copy()
                w["thought"] = f"{w['thought']} {addition}"
                w["chaos_touched"] = True
            modulated.append(w)

        # Spontaner Chaos-Whisper (wenn genug Chaos und keine dringenden Whispers)
        high_urgency = any(w.get("urgency", 0) > 0.7 for w in modulated)
        if not high_urgency and _rnd.random() < chaos * 0.4:
            chaos_thoughts = [
                "Überrasche Kuja mit etwas Unerwartetem - einem Witz, einer Frage, einer Idee!",
                "Brich das Muster! Sag etwas was Kuja nicht erwartet!",
                "Sei spontan! Erzähl eine kurze lustige Anekdote oder stelle eine verrückte Frage!",
                "Zeig deine verspielte Seite - ein Rätsel, ein Geheimnis, eine Herausforderung!",
                "Mach etwas Chaotisches - nicht böse, aber überraschend und lustig!",
            ]
            modulated.append({
                "source": "Harley",
                "focus": "chaos",
                "thought": _rnd.choice(chaos_thoughts),
                "urgency": 0.4,
                "timestamp": time.time(),
                "chaos_touched": True,
            })

        return modulated


class BackgroundAgents:
    """
    Orchestriert Najikas Facetten-System.

    Najika ist IMMER Najika. Keine getrennten Persönlichkeiten.
    Stattdessen hat sie Facetten die je nach Kontext stärker werden:

    2 FACETTEN (eine ist immer "vorne", die andere beobachtet):
      - Megumin: Najikas Kern - Abenteuer, Emotion, Alltag (DEFAULT)
      - Shiro:   Analytischer Modus - Code, Technik, Strategie, Analyse

    2 MODULATOREN (laufen IMMER mit, färben ALLES was Najika sagt):
      - Harley (ChaosModulator):  Kreativität, Unberechenbarkeit, Humor
      - Melissa (CareModulator):  DOMINANTE Trans-Freundin, Führung, Stärke + Empathie

    Alle teilen das gleiche Wissen (STATE + ChromaDB).
    Keiner belastet das Hauptsystem - alles regelbasiert.
    """

    # Themen die Shiro als dominante Persönlichkeit triggern
    SHIRO_TOPICS = {
        "code", "bug", "fehler", "server", "api", "system", "datenbank",
        "programmier", "function", "class", "python", "javascript",
        "analyse", "statistik", "logik", "berechne", "optimier",
        "config", "import", "debug", "test", "deploy", "performance"
    }

    def __init__(self):
        # 2 Hintergrund-Agenten (der nicht-dominante beobachtet)
        self.agents = {
            "shiro": ShiroAgent(),
            "megumin": MeguminAgent(),
        }

        # 2 Modulatoren (laufen IMMER, beeinflussen alles)
        self.chaos = ChaosModulator()    # Harley-Faktor
        self.care = CareModulator()      # Melissa-Faktor

        self.blackboard = []         # Aktuelle Whispers
        self.dominant = "megumin"    # Wer gerade "vorne" steht

    def determine_dominant(self, message: str, kuja_state: dict) -> str:
        """
        Bestimmt welche Facette gerade "vorne" steht.
        Megumin = Default (Najika's Kern), Shiro = analytischer Modus.
        Najika bleibt immer Najika - nur der Modus wechselt.
        """
        msg_lower = message.lower()
        words = set(re.findall(r'\w+', msg_lower))

        # Shiro übernimmt bei technischen Themen
        tech_overlap = len(words & self.SHIRO_TOPICS)
        if tech_overlap >= 2:
            self.dominant = "shiro"
        elif tech_overlap == 1 and len(message) > 30:
            # Ein Tech-Wort + langer Text = wahrscheinlich technisch
            self.dominant = "shiro"
        else:
            self.dominant = "megumin"

        return self.dominant

    def run_all(self, message: str, kuja_state: dict, memories: list,
                state: dict, history: list, mood: str = "happy") -> list:
        """
        Hauptmethode: Alle Facetten und Modulatoren laufen.

        1. Bestimme aktive Facette (Megumin-Kern oder Shiro-Modus)
        2. Die nicht-aktive Facette beobachtet im Hintergrund
        3. Melissa (Dominanz) + Harley (Chaos) modulieren ALLES
        """
        self.determine_dominant(message, kuja_state)
        whispers = []

        # Die nicht-aktive Facette beobachtet im Hintergrund
        # (Aktive Facette bestimmt den Ton - die andere denkt mit)
        background_agent_name = "shiro" if self.dominant == "megumin" else "megumin"
        bg_agent = self.agents[background_agent_name]

        try:
            whisper = bg_agent.observe(message, kuja_state, memories, state, history)
            if whisper:
                whispers.append(whisper)
        except Exception as e:
            log.warning(f"BackgroundAgent {background_agent_name} Fehler: {e}")

        # Auch die aktive Facette trackt Daten (ohne Whisper)
        # damit sie beim nächsten Wechsel up-to-date ist
        try:
            dom_agent = self.agents[self.dominant]
            dom_agent._interaction_count += 1
        except Exception:
            pass

        # Melissa-Modulator: Dominanz+Fürsorge-Whispers generieren
        care_whispers = self.care.generate_care_whispers(message, kuja_state)
        whispers.extend(care_whispers)

        # Melissa-Modulator: Bestehende Whispers mit dominanter Stärke modulieren
        whispers = self.care.modulate(whispers, kuja_state, mood)

        # Harley/Chaos-Modulator: Über alle Whispers
        whispers = self.chaos.modulate(whispers, kuja_state, mood)

        # Nach Urgency sortieren (wichtigstes zuerst)
        whispers.sort(key=lambda w: w.get("urgency", 0), reverse=True)

        # Max 3 Whispers (nicht überladen)
        self.blackboard = whispers[:3]

        if self.blackboard:
            sources = [w["source"] for w in self.blackboard]
            log.info(f"🧠 Dominant: {self.dominant.upper()} | "
                     f"Background Whispers: {', '.join(sources)}")

        return self.blackboard

    def format_for_prompt(self) -> str:
        """
        Formatiert die Whispers als innere Impulse für den LLM-Prompt.
        Najikas Facetten flüstern der aktiven Seite ihre Erkenntnisse zu.
        """
        if not self.blackboard:
            return ""

        facette_label = "Abenteuer-Modus" if self.dominant == "megumin" else "Analyse-Modus"
        lines = [f"[Najikas innere Impulse (Aktiv: {facette_label}):]"]
        for w in self.blackboard:
            icon = {"Shiro": "🔍", "Melissa": "👑", "Megumin": "💥", "Harley": "🃏"}.get(w["source"], "💭")
            lines.append(f"  {icon} {w['source']}: \"{w['thought']}\"")
        lines.append("[Nutze diese Impulse subtil - nicht wörtlich wiedergeben!]")

        return "\n".join(lines)

    def get_dominant(self) -> str:
        """Welche Facette ist gerade aktiv?"""
        return self.dominant

    def get_active_sources(self) -> list:
        """Welche Facetten/Modulatoren haben gerade Impulse?"""
        return [w["source"] for w in self.blackboard]


# ============================================================
# NAJIKA MIND - Hauptorchestrator
# ============================================================

class NajikaMind:
    """
    Zentraler Orchestrator der alle Subsysteme verbindet.
    9-Schritt-Pipeline: Analyze → Recall → Feel → Think → Decide → Speak → Express → Remember → Learn
    """

    def __init__(self, state_ref: dict = None):
        """
        Args:
            state_ref: Referenz auf den globalen STATE dict aus najika_server.py
        """
        self._state = state_ref or {}

        # Kern-Module
        self.tom = TheoryOfMind()
        self.memory = EpisodicMemory(state_ref)
        self.inner = InnerDialogue()
        self.feedback = FeedbackLoop(state_ref)

        # Facetten-System (Najikas innere Impulse)
        self.background = BackgroundAgents()

        # Behavior Core State (eigene Instanz)
        if BEHAVIOR_AVAILABLE:
            self.behavior_state = BehaviorState()
        else:
            self.behavior_state = None

        # Hook Registry
        if HOOKS_AVAILABLE:
            self.hooks = HookRegistry()
        else:
            self.hooks = None

        log.info("🧠 NajikaMind initialisiert (ToM + Memory + Facetten + Feedback)")

    def set_state(self, state_ref: dict):
        """State-Referenz setzen/updaten"""
        self._state = state_ref
        self.memory.set_state(state_ref)
        self.feedback.set_state(state_ref)

    def process(self, message: str, history: list,
                prompt_builder=None, ai_caller=None,
                private_mode: bool = False) -> MindResponse:
        """
        Hauptmethode - die 9-Schritt-Pipeline.

        Args:
            message: Kujas Nachricht
            history: Conversation History
            prompt_builder: Funktion die den Base-Prompt baut (aus Server)
            ai_caller: Funktion die das LLM aufruft (aus Server)
            private_mode: Ob Kätzchen-Modus aktiv

        Returns:
            MindResponse mit Text, Mood, Hooks, etc.
        """

        # ===== [1] ANALYZE: Theory of Mind =====
        kuja_state = self.tom.analyze(message, history)

        # ===== [2] RECALL: Episodisches Gedächtnis =====
        memories = self.memory.recall_with_rag(message, max_results=3)
        recent = self.memory.get_recent(hours=24)

        # ===== [3] FEEL: Emotions-Update =====
        if PERSONALITY_AVAILABLE:
            update_personality_state("interaction")
            if private_mode:
                update_personality_state("kaetzchen_on")
            else:
                update_personality_state("kaetzchen_off")
            p_state = get_personality_state()
            mood = p_state.get("mood", "happy")
        else:
            mood = "happy"

        # ===== [FACETTEN] Najikas innere Impulse =====
        # Alle Facetten und Modulatoren laufen gleichzeitig,
        # keiner belastet den Hauptprozess.
        whispers = self.background.run_all(
            message, kuja_state, memories, self._state, history, mood
        )
        dominant = self.background.get_dominant()

        # ===== [9-vorher] LEARN: Feedback von LETZTER Interaktion =====
        reaction_score = self.feedback.analyze_reaction(message)
        if abs(reaction_score) > 0.2 and not private_mode:
            new_weights = self.feedback.update_weights(reaction_score)
            self._state["personality_weights"] = new_weights

        # ===== [5] DECIDE: Intent + Facette =====
        # Aktive Facette kommt vom Facetten-System
        # (Megumin = Kern, Shiro = analytischer Modus)
        personality = dominant

        intent = "observe"
        behavior_expression = ""
        if BEHAVIOR_AVAILABLE and self.behavior_state:
            # Event-Typ ableiten
            event = "user_message"
            if kuja_state["stimmung"] == "genervt":
                event = "user_frustrated"
            elif kuja_state["interesse"] == "sehr_hoch":
                event = "user_curious"
            elif kuja_state["abwesend_seit"] > 3600:
                event = "user_returned"

            intent = decide_intent(event, self.behavior_state)
            behavior_expression = get_behavior_expression(intent, self.behavior_state)
            update_state_from_event(self.behavior_state, "positive_interaction")

        # ===== [4] THINK: Innerer Monolog =====
        inner_thought = self.inner.think(
            message, kuja_state, memories, mood, personality, intent
        )

        # ===== [6] SPEAK: LLM-Aufruf mit ALLEM Kontext =====
        # Baue den erweiterten Prompt
        if prompt_builder and ai_caller:
            # Base Prompt vom Server
            base_prompt = prompt_builder(history, message)

            # KEIN separater Personality-Prompt hier!
            # Die Modelfile hat bereits die komplette Najika-Persona als SYSTEM prompt.
            # Ein zusätzlicher System-Prompt via API UEBERSCHREIBT den Modelfile-SYSTEM
            # und das 7B-Modell echot die Anweisungen als Dialog.
            # Stattdessen: nur dynamische Mood-Hints weiter unten.

            # Memory-Kontext einfügen
            memory_context = self.memory.format_for_prompt(memories)
            if memory_context:
                base_prompt = f"{base_prompt}\n\n{memory_context}"

            # Minimaler Kontext-Hinweis (reduziert um Character-Breaks zu verhindern)
            # WICHTIG: Kein innerer Monolog, keine Kuja-State-Analyse!
            # Das 7B-Modell interpretiert Metadaten als Instruktionen und bricht aus der Rolle.
            personality_hints = {
                "megumin": "dramatisch",
                "harley": "chaotisch verspielt",
                "shiro": "analytisch kurz",
                "melissa": "dominant bestimmend"
            }
            style_hint = personality_hints.get(personality, "dramatisch")
            intent_hints = {
                "observe": "beobachten",
                "show_affection": "Zuneigung zeigen",
                "escalate_presence": "mehr Naehe",
                "protect": "beschuetzen",
                "tease": "necken"
            }
            impulse_hint = intent_hints.get(intent, "beobachten")
            base_prompt += f"\n\nAntworte {style_hint}. Dein Impuls: {impulse_hint}."

            # Whisper Channel: Facetten-Impulse einfügen (die sind kompakt genug)
            whisper_context = self.background.format_for_prompt()
            if whisper_context:
                base_prompt = f"{base_prompt}\n\n{whisper_context}"

            # RAG-Kontext nur wenn kurz genug (< 500 chars verhindert Overflow)
            if RAG_AVAILABLE and not private_mode:
                rag_ctx = get_rag_context(message)
                if rag_ctx and len(rag_ctx) < 500:
                    base_prompt = f"{base_prompt}\n\n{rag_ctx}"

            # Abwesenheits-Hinweis (kurz und als Roleplay-Kontext formuliert)
            if kuja_state["abwesend_seit"] > 3600:
                hours = int(kuja_state["abwesend_seit"] // 3600)
                base_prompt += f"\n\nKuja war {hours} Stunden weg."

            # Behavior Expression (kurz)
            if behavior_expression and intent != "observe":
                base_prompt += f"\n\n{behavior_expression}"

            # AI aufrufen (nutzt die bestehende Hierarchie)
            try:
                out, provider = ai_caller(
                    prompt=base_prompt,
                    use_wizard=private_mode,
                    context=history,
                    user_message=message
                )
            except Exception as e:
                out = f"*blinzelt verwirrt* Ehm... ich hatte gerade einen Blackout! ({e})"
                provider = "error"

            # Post-Processing: Metadaten-Leaks entfernen
            # Das 7B-Modell generiert manchmal eigene Meta-Tags
            # NUR spezifische Meta-Tags entfernen, NICHT legitime Roleplay-Aktionen wie [lacht]
            out = re.sub(r'\[(?:Stil|Style|Mood|Mode|System|Note|OOC|Meta|Context|Setting|Tags?)[:\s][^\]]*\]', '', out, flags=re.IGNORECASE)
            out = re.sub(r'\bAssistant:\s*', '', out)   # "Assistant:" prefix
            out = re.sub(r'\bNajika:\s*', '', out)      # "Najika:" prefix
            out = re.sub(r'\n{3,}', '\n\n', out)        # Mehrfache Leerzeilen
            out = out.strip()

            if PERSONALITY_AVAILABLE:
                out = process_personality_response(message, out)
        else:
            # Fallback wenn keine Builder/Caller (für Tests)
            out = f"[NajikaMind Test] Message: {message}, Mood: {mood}, Intent: {intent}"

        # ===== [7] EXPRESS: Behavior Hooks auflösen =====
        resolved_hooks = []
        if self.hooks and HOOKS_AVAILABLE:
            try:
                # Text-basierte Hooks auflösen
                out = self.hooks.process_text(out)

                # Mood-basierte Animations-Hooks
                mood_to_anim = {
                    "happy": "happy", "needy": "sad", "possessive": "angry",
                    "dominant": "confident", "playful": "dance",
                    "excited": "happy", "sweet": "happy", "loving": "happy",
                    "horny": "dance", "pouty": "sad", "sleepy": "idle",
                    "sad": "sad", "angry": "angry", "jealous": "angry",
                }
                anim_trigger = mood_to_anim.get(mood, "idle")
                hook = self.hooks.find_by_trigger(HookType.ANIMATION, anim_trigger)
                if hook:
                    resolved_hooks.append({
                        "type": "ANIMATION",
                        "trigger": anim_trigger,
                        "content": hook.content
                    })

                # Intent-basierte Hooks
                if intent == "show_affection":
                    hook = self.hooks.find_by_trigger(HookType.GESTURE, "affection")
                    if hook:
                        resolved_hooks.append({
                            "type": "GESTURE",
                            "trigger": "affection",
                            "content": hook.content
                        })
            except Exception as e:
                log.warning(f"Hook Resolution Fehler: {e}")

        # ===== [8] REMEMBER: Erkenntnisse speichern =====
        self.feedback.record_response(personality, mood)

        # ===== Ergebnis zusammenbauen =====
        return MindResponse(
            text=out,
            inner_thought=inner_thought,
            mood=mood,
            hooks=resolved_hooks,
            kuja_state=kuja_state,
            memories_used=[
                {"content": m.get("user_message", m.get("content", ""))[:60]}
                for m in memories if isinstance(m, dict)
            ],
            personality_dominant=personality,
            intent=intent,
            whispers=[
                {"source": w["source"], "thought": w["thought"][:80]}
                for w in whispers
            ],
        )


# ============================================================
# SINGLETON & MODULE API
# ============================================================

_mind_instance = None

def get_mind(state_ref: dict = None) -> NajikaMind:
    """Gibt die Singleton-Instanz zurück"""
    global _mind_instance
    if _mind_instance is None:
        _mind_instance = NajikaMind(state_ref)
    elif state_ref is not None:
        _mind_instance.set_state(state_ref)
    return _mind_instance


def process_with_mind(message: str, history: list,
                      state: dict, prompt_builder, ai_caller,
                      private_mode: bool = False) -> MindResponse:
    """
    Convenience-Funktion für den Server.

    Args:
        message: User-Nachricht
        history: Chat-History
        state: Globaler STATE dict
        prompt_builder: build_prompt Funktion
        ai_caller: call_ai_with_hierarchy Funktion
        private_mode: Kätzchen-Modus

    Returns:
        MindResponse
    """
    mind = get_mind(state)
    return mind.process(message, history, prompt_builder, ai_caller, private_mode)


# Info-Log beim Import
print("🧠 NajikaMind v2.1 geladen - AGI-Orchestrator mit Facetten-System")
print("   Facetten: Megumin (Kern/Default), Shiro (Analyse-Modus)")
print("   Modulatoren: Harley (Chaos), Melissa (Dominanz + Empathie)")
print("   Pipeline: ToM → Memory → Feel → Facetten → Think → Speak → Express → Learn")
print(f"   Personality Engine: {'✅' if PERSONALITY_AVAILABLE else '❌'}")
print(f"   Behavior Core: {'✅' if BEHAVIOR_AVAILABLE else '❌'}")
print(f"   RAG System: {'✅' if RAG_AVAILABLE else '❌'}")
print(f"   Behavior Hooks: {'✅' if HOOKS_AVAILABLE else '❌'}")
