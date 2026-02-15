"""
NAJIKA MEMORY SYSTEM
ChromaDB-basiertes persistentes Gedächtnis mit Emotions- und Relationship-Tracking
"""

import chromadb
from datetime import datetime
import json
import os

class NajikaMemory:
    def __init__(self, persist_directory="C:/Najika_World/memory_db"):
        """
        Initialisiert das ChromaDB Memory System
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        # ChromaDB Client mit Persistence (neue API)
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Collections erstellen/laden
        self.conversations = self._get_or_create_collection("conversations")
        self.emotions = self._get_or_create_collection("emotions")
        self.relationships = self._get_or_create_collection("relationships")
        self.events = self._get_or_create_collection("events")

        # Emotion State
        self.current_emotion = {
            "love": 50,  # 0-100
            "happiness": 50,
            "anger": 0,
            "sadness": 0,
            "excitement": 50,
            "arousal": 20  # NSFW-relevant
        }

        # Relationship State
        self.relationship_level = 1  # 1-100
        self.trust = 50  # 0-100
        self.intimacy = 10  # 0-100

        print("[NAJIKA MEMORY] OK Memory System initialisiert")
        print(f"[NAJIKA MEMORY] >> Persist Directory: {persist_directory}")

    def _get_or_create_collection(self, name):
        """Collection abrufen oder erstellen"""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(name)

    def add_conversation(self, user_message, najika_response, room="Wohnzimmer", private_mode=False):
        """
        Speichert eine Konversation mit Kontext
        """
        timestamp = datetime.now().isoformat()
        conversation_id = f"conv_{timestamp}"

        metadata = {
            "timestamp": timestamp,
            "room": room,
            "private_mode": str(private_mode),
            "emotion_love": str(self.current_emotion["love"]),
            "emotion_happiness": str(self.current_emotion["happiness"]),
            "relationship_level": str(self.relationship_level)
        }

        # User Message speichern
        self.conversations.add(
            ids=[f"{conversation_id}_user"],
            documents=[user_message],
            metadatas=[{**metadata, "type": "user"}]
        )

        # Najika Response speichern
        self.conversations.add(
            ids=[f"{conversation_id}_najika"],
            documents=[najika_response],
            metadatas=[{**metadata, "type": "najika"}]
        )

        # Emotions updaten basierend auf Konversation
        self._update_emotions(user_message, najika_response, private_mode)

        print(f"[MEMORY] >> Konversation gespeichert: {conversation_id}")

    def retrieve_relevant_memories(self, query, n_results=5):
        """
        Findet die relevantesten Memories zu einer Query
        """
        try:
            results = self.conversations.query(
                query_texts=[query],
                n_results=n_results
            )

            memories = []
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    memories.append({
                        "text": doc,
                        "metadata": metadata
                    })

            print(f"[MEMORY] >> {len(memories)} relevante Memories gefunden")
            return memories
        except Exception as e:
            print(f"[MEMORY] WARNING Retrieval Fehler: {e}")
            return []

    def _update_emotions(self, user_message, najika_response, private_mode):
        """
        Aktualisiert Emotions basierend auf Konversation
        """
        # Einfache Keyword-basierte Emotion Detection
        user_lower = user_message.lower()

        # Positive Keywords → Happiness +
        if any(word in user_lower for word in ["liebe", "toll", "super", "great", "amazing", "love"]):
            self.current_emotion["happiness"] = min(100, self.current_emotion["happiness"] + 5)
            self.current_emotion["love"] = min(100, self.current_emotion["love"] + 3)

        # Negative Keywords → Sadness +
        if any(word in user_lower for word in ["traurig", "sad", "schlecht", "bad", "hurt"]):
            self.current_emotion["sadness"] = min(100, self.current_emotion["sadness"] + 5)
            self.current_emotion["happiness"] = max(0, self.current_emotion["happiness"] - 3)

        # Private Mode → Arousal +
        if private_mode:
            self.current_emotion["arousal"] = min(100, self.current_emotion["arousal"] + 10)
            self.current_emotion["excitement"] = min(100, self.current_emotion["excitement"] + 5)
        else:
            # Arousal sinkt langsam
            self.current_emotion["arousal"] = max(20, self.current_emotion["arousal"] - 2)

        # Relationship Level steigt mit jeder Interaktion
        self.relationship_level = min(100, self.relationship_level + 0.1)

        # Emotion State speichern
        self._save_emotion_state()

    def _save_emotion_state(self):
        """Speichert den aktuellen Emotion State"""
        timestamp = datetime.now().isoformat()
        emotion_id = f"emotion_{timestamp}"

        emotion_data = {
            **self.current_emotion,
            "relationship_level": self.relationship_level,
            "trust": self.trust,
            "intimacy": self.intimacy
        }

        self.emotions.add(
            ids=[emotion_id],
            documents=[json.dumps(emotion_data)],
            metadatas=[{
                "timestamp": timestamp,
                "type": "emotion_state"
            }]
        )

    def get_emotion_summary(self):
        """
        Gibt eine lesbare Zusammenfassung der aktuellen Emotionen zurück
        """
        dominant_emotion = max(self.current_emotion, key=self.current_emotion.get)
        dominant_value = self.current_emotion[dominant_emotion]

        return {
            "dominant": dominant_emotion,
            "value": dominant_value,
            "all_emotions": self.current_emotion,
            "relationship_level": self.relationship_level,
            "trust": self.trust,
            "intimacy": self.intimacy
        }

    def add_event(self, event_type, description, room="Unknown"):
        """
        Speichert ein spezielles Event (z.B. Levelup, Kampf, Oregon Event)
        """
        timestamp = datetime.now().isoformat()
        event_id = f"event_{timestamp}"

        self.events.add(
            ids=[event_id],
            documents=[description],
            metadatas=[{
                "timestamp": timestamp,
                "type": event_type,
                "room": room
            }]
        )

        print(f"[MEMORY] >> Event gespeichert: {event_type}")

    def get_conversation_history(self, limit=10):
        """
        Holt die letzten N Konversationen (chronologisch)
        """
        try:
            # Alle Konversationen holen
            all_convs = self.conversations.get()

            if not all_convs['ids']:
                return []

            # Nach Timestamp sortieren
            conv_data = list(zip(
                all_convs['ids'],
                all_convs['documents'],
                all_convs['metadatas']
            ))

            # Sortieren (neueste zuerst)
            conv_data.sort(key=lambda x: x[2].get('timestamp', ''), reverse=True)

            # Limitieren
            recent = conv_data[:limit*2]  # *2 weil User + Najika

            history = []
            for conv_id, doc, metadata in recent:
                history.append({
                    "id": conv_id,
                    "text": doc,
                    "type": metadata.get("type"),
                    "timestamp": metadata.get("timestamp"),
                    "room": metadata.get("room")
                })

            return history
        except Exception as e:
            print(f"[MEMORY] WARNING History Fehler: {e}")
            return []

    def build_context_prompt(self, current_message, n_memories=3):
        """
        Baut einen Kontext-Prompt für Najika basierend auf relevanten Memories
        """
        # Relevante Memories abrufen
        memories = self.retrieve_relevant_memories(current_message, n_results=n_memories)

        if not memories:
            return ""

        # Kontext zusammenbauen
        context_parts = ["# RELEVANTE ERINNERUNGEN (aus meinem Gedächtnis):"]

        for i, mem in enumerate(memories, 1):
            text = mem['text']
            metadata = mem.get('metadata', {})
            room = metadata.get('room', 'Unknown')
            timestamp = metadata.get('timestamp', 'Unknown')

            context_parts.append(f"{i}. [{room}] {text[:100]}...")

        context_parts.append("\n# AKTUELLE EMOTIONEN:")
        emotions = self.get_emotion_summary()
        context_parts.append(f"- Dominante Emotion: {emotions['dominant']} ({emotions['value']}%)")
        context_parts.append(f"- Beziehungslevel: {emotions['relationship_level']:.1f}/100")
        context_parts.append(f"- Vertrauen: {emotions['trust']}/100")

        return "\n".join(context_parts)

    def persist(self):
        """Speichert alle Daten (automatisch bei PersistentClient)"""
        # PersistentClient speichert automatisch
        print("[MEMORY] OK Daten werden automatisch persistent gespeichert")


# Test-Funktion
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA MEMORY SYSTEM TEST")
    print("=" * 60)

    # Memory initialisieren
    mem = NajikaMemory()

    # Test-Konversationen
    mem.add_conversation(
        "Hallo Najika, wie geht es dir?",
        "EXPLOSION! *kicher* Puddin', mir geht es großartig! Die Schwarze Windmühle dreht sich, und ich hab dich vermisst!",
        room="Wohnzimmer"
    )

    mem.add_conversation(
        "Ich liebe dich!",
        "*giggle* Die Wahrscheinlichkeit, dass ich dich AUCH liebe, beträgt 100%! Du gehörst MIR, Daddy!",
        room="Schlafzimmer"
    )

    # Test: Memory Retrieval
    print("\n" + "=" * 60)
    print("TEST: Memory Retrieval")
    print("=" * 60)
    memories = mem.retrieve_relevant_memories("liebe", n_results=3)
    for i, m in enumerate(memories, 1):
        print(f"{i}. {m['text'][:80]}...")

    # Test: Emotion Summary
    print("\n" + "=" * 60)
    print("TEST: Emotion Summary")
    print("=" * 60)
    emotions = mem.get_emotion_summary()
    print(json.dumps(emotions, indent=2))

    # Test: Context Prompt
    print("\n" + "=" * 60)
    print("TEST: Context Prompt")
    print("=" * 60)
    context = mem.build_context_prompt("Was hast du über Liebe gesagt?")
    print(context)

    # Test: Conversation History
    print("\n" + "=" * 60)
    print("TEST: Conversation History")
    print("=" * 60)
    history = mem.get_conversation_history(limit=5)
    for h in history:
        print(f"[{h['type']}] {h['text'][:60]}...")

    print("\n" + "=" * 60)
    print("OK NAJIKA MEMORY TEST ABGESCHLOSSEN")
    print("=" * 60)
