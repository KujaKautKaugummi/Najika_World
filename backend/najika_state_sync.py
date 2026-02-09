# najika_state_sync.py
# Najika World - State Synchronization & WebSocket Bridge
# Synchronisiert State zwischen Python Backend und UE5 Frontend

import asyncio
import json
import websockets
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Callable, Any
from datetime import datetime
from enum import Enum
import logging

# ==================== LOGGING ====================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NajikaStateSync")

# ==================== STATE DEFINITIONS ====================

class EmotionType(Enum):
    JOY = "joy"
    FEAR = "fear"
    ANGER = "anger"
    TRUST = "trust"
    DESIRE = "desire"
    CURIOSITY = "curiosity"

@dataclass
class EmotionState:
    """Najikas emotionaler Zustand"""
    joy: float = 0.5
    fear: float = 0.0
    anger: float = 0.0
    trust: float = 0.5
    desire: float = 0.0
    curiosity: float = 0.3

    # Dampening für realistische Übergänge
    DAMPEN_FACTOR = 0.15

    def apply_change(self, emotion: str, delta: float):
        """Wendet eine Emotion-Änderung mit Dampening an"""
        current = getattr(self, emotion, 0.0)
        dampened_delta = delta * self.DAMPEN_FACTOR
        new_value = max(0.0, min(1.0, current + dampened_delta))
        setattr(self, emotion, new_value)

    def to_dict(self) -> dict:
        return {
            "joy": round(self.joy, 3),
            "fear": round(self.fear, 3),
            "anger": round(self.anger, 3),
            "trust": round(self.trust, 3),
            "desire": round(self.desire, 3),
            "curiosity": round(self.curiosity, 3)
        }

@dataclass
class RelationshipState:
    """Beziehung zu Owner"""
    stage: str = "intro"  # intro, bonding, close, deep
    affinity: float = 0.0  # 0.0 - 1.0
    trust_level: int = 1  # 1-6

    # Affinity Thresholds für Stage-Wechsel
    STAGE_THRESHOLDS = {
        "intro": 0.0,
        "bonding": 0.25,
        "close": 0.50,
        "deep": 0.75
    }

    def update_affinity(self, delta: float):
        """Aktualisiert Affinity und prüft Stage-Wechsel"""
        self.affinity = max(0.0, min(1.0, self.affinity + delta))
        self._check_stage_transition()

    def _check_stage_transition(self):
        """Prüft ob Stage-Wechsel nötig ist"""
        for stage, threshold in sorted(
            self.STAGE_THRESHOLDS.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            if self.affinity >= threshold:
                if self.stage != stage:
                    logger.info(f"Relationship stage transition: {self.stage} → {stage}")
                    self.stage = stage
                break

    def to_dict(self) -> dict:
        return {
            "stage": self.stage,
            "affinity": round(self.affinity, 3),
            "trust_level": self.trust_level
        }

@dataclass
class CognitionState:
    """Kognitiver Zustand"""
    focus: str = "idle"  # idle, listening, thinking, speaking, coding
    attention_target: Optional[str] = None
    processing: bool = False
    last_topic: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "focus": self.focus,
            "attention_target": self.attention_target,
            "processing": self.processing,
            "last_topic": self.last_topic
        }

@dataclass
class BehaviorProfile:
    """Verhaltens-Profil"""
    personality_mix: Dict[str, float] = field(default_factory=lambda: {
        "megumin": 0.35,
        "harley": 0.25,
        "shiro": 0.20,
        "melissa": 0.20
    })
    current_mode: str = "normal"  # normal, excited, tired, focused
    energy_level: float = 1.0

    def to_dict(self) -> dict:
        return {
            "personality_mix": self.personality_mix,
            "current_mode": self.current_mode,
            "energy_level": round(self.energy_level, 3)
        }

@dataclass
class NajikaState:
    """Vollständiger Najika State"""
    emotion: EmotionState = field(default_factory=EmotionState)
    relationship: RelationshipState = field(default_factory=RelationshipState)
    cognition: CognitionState = field(default_factory=CognitionState)
    behavior: BehaviorProfile = field(default_factory=BehaviorProfile)

    # Metadata
    version: int = 1
    last_update: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "emotion": self.emotion.to_dict(),
            "relationship": self.relationship.to_dict(),
            "cognition": self.cognition.to_dict(),
            "behavior": self.behavior.to_dict(),
            "version": self.version,
            "last_update": self.last_update
        }

    def from_dict(self, data: dict):
        """Lädt State aus Dictionary"""
        if "emotion" in data:
            for key, value in data["emotion"].items():
                if hasattr(self.emotion, key):
                    setattr(self.emotion, key, value)

        if "relationship" in data:
            for key, value in data["relationship"].items():
                if hasattr(self.relationship, key):
                    setattr(self.relationship, key, value)

        if "cognition" in data:
            for key, value in data["cognition"].items():
                if hasattr(self.cognition, key):
                    setattr(self.cognition, key, value)

        if "behavior" in data:
            for key, value in data["behavior"].items():
                if hasattr(self.behavior, key):
                    setattr(self.behavior, key, value)

        self.last_update = datetime.now().isoformat()
        self.version += 1

# ==================== MESSAGE TYPES ====================

class MessageType(Enum):
    """WebSocket Nachrichtentypen"""
    # State Updates
    STATE_UPDATE = "state_update"
    STATE_REQUEST = "state_request"
    STATE_FULL = "state_full"

    # Emotion
    EMOTION_CHANGE = "emotion_change"
    EMOTION_TRIGGER = "emotion_trigger"

    # Actions
    ACTION_REQUEST = "action_request"
    ACTION_RESPONSE = "action_response"

    # Animation
    ANIMATION_TRIGGER = "animation_trigger"
    ANIMATION_COMPLETE = "animation_complete"

    # Speech
    SPEECH_START = "speech_start"
    SPEECH_END = "speech_end"
    SPEECH_TEXT = "speech_text"

    # System
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"

@dataclass
class WebSocketMessage:
    """Standard WebSocket Nachricht"""
    type: str
    payload: dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    id: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "id": self.id
        })

    @classmethod
    def from_json(cls, data: str) -> "WebSocketMessage":
        parsed = json.loads(data)
        return cls(
            type=parsed.get("type", "unknown"),
            payload=parsed.get("payload", {}),
            timestamp=parsed.get("timestamp", datetime.now().isoformat()),
            id=parsed.get("id")
        )

# ==================== STATE SYNC SERVER ====================

class NajikaStateSyncServer:
    """
    WebSocket Server für State-Synchronisation.

    Verbindet:
    - Python Backend (NajikaBrain)
    - UE5 Frontend (NajikaBody)
    - Optional: Web UI
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.state = NajikaState()
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.handlers: Dict[str, Callable] = {}
        self.running = False

        # Standard Handler registrieren
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Registriert Standard-Nachrichtenhandler"""
        self.handlers[MessageType.PING.value] = self._handle_ping
        self.handlers[MessageType.STATE_REQUEST.value] = self._handle_state_request
        self.handlers[MessageType.EMOTION_CHANGE.value] = self._handle_emotion_change
        self.handlers[MessageType.ANIMATION_COMPLETE.value] = self._handle_animation_complete

    async def _handle_ping(self, ws, message: WebSocketMessage):
        """Beantwortet Ping mit Pong"""
        response = WebSocketMessage(
            type=MessageType.PONG.value,
            payload={"server_time": datetime.now().isoformat()}
        )
        await ws.send(response.to_json())

    async def _handle_state_request(self, ws, message: WebSocketMessage):
        """Sendet vollständigen State"""
        response = WebSocketMessage(
            type=MessageType.STATE_FULL.value,
            payload=self.state.to_dict()
        )
        await ws.send(response.to_json())

    async def _handle_emotion_change(self, ws, message: WebSocketMessage):
        """Verarbeitet Emotion-Änderung"""
        emotion = message.payload.get("emotion")
        delta = message.payload.get("delta", 0.0)

        if emotion and hasattr(self.state.emotion, emotion):
            self.state.emotion.apply_change(emotion, delta)
            await self.broadcast_state_update()

    async def _handle_animation_complete(self, ws, message: WebSocketMessage):
        """Animation wurde in UE5 abgeschlossen"""
        animation = message.payload.get("animation")
        logger.info(f"Animation complete: {animation}")

    async def broadcast_state_update(self):
        """Sendet State-Update an alle Clients"""
        message = WebSocketMessage(
            type=MessageType.STATE_UPDATE.value,
            payload=self.state.to_dict()
        )

        for client_id, ws in self.clients.items():
            try:
                await ws.send(message.to_json())
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Client {client_id} disconnected during broadcast")

    async def send_to_ue5(self, message_type: str, payload: dict):
        """Sendet Nachricht speziell an UE5 Client"""
        message = WebSocketMessage(type=message_type, payload=payload)

        ue5_client = self.clients.get("ue5")
        if ue5_client:
            try:
                await ue5_client.send(message.to_json())
            except websockets.exceptions.ConnectionClosed:
                logger.error("UE5 client disconnected")

    async def trigger_animation(self, animation_name: str, params: dict = None):
        """Triggert Animation in UE5"""
        await self.send_to_ue5(
            MessageType.ANIMATION_TRIGGER.value,
            {
                "animation": animation_name,
                "params": params or {}
            }
        )

    async def send_speech(self, text: str, emotion: str = "neutral"):
        """Sendet Speech-Text an UE5 für TTS/Lipsync"""
        await self.send_to_ue5(
            MessageType.SPEECH_TEXT.value,
            {
                "text": text,
                "emotion": emotion,
                "language": "de"
            }
        )

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Behandelt einzelne Client-Verbindung"""
        # Client-ID aus Query-Parameter oder generieren
        client_id = path.strip("/") or f"client_{len(self.clients)}"
        self.clients[client_id] = websocket

        logger.info(f"Client connected: {client_id}")

        # Welcome Message
        welcome = WebSocketMessage(
            type=MessageType.CONNECTED.value,
            payload={
                "client_id": client_id,
                "server_version": "1.0.0",
                "state": self.state.to_dict()
            }
        )
        await websocket.send(welcome.to_json())

        try:
            async for raw_message in websocket:
                try:
                    message = WebSocketMessage.from_json(raw_message)
                    handler = self.handlers.get(message.type)

                    if handler:
                        await handler(websocket, message)
                    else:
                        logger.warning(f"Unknown message type: {message.type}")

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON from {client_id}: {e}")
                except Exception as e:
                    logger.error(f"Error handling message from {client_id}: {e}")

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            del self.clients[client_id]
            logger.info(f"Client disconnected: {client_id}")

    async def start(self):
        """Startet den WebSocket Server"""
        self.running = True
        logger.info(f"Starting NajikaStateSync server on ws://{self.host}:{self.port}")

        async with websockets.serve(self.handle_client, self.host, self.port):
            while self.running:
                await asyncio.sleep(1)

    def stop(self):
        """Stoppt den Server"""
        self.running = False

# ==================== STATE SYNC CLIENT (für Tests) ====================

class NajikaStateSyncClient:
    """
    WebSocket Client für State-Synchronisation.
    Kann von UE5 oder anderen Clients verwendet werden.
    """

    def __init__(self, uri: str = "ws://127.0.0.1:8765"):
        self.uri = uri
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.state: Optional[dict] = None
        self.handlers: Dict[str, Callable] = {}
        self.connected = False

    async def connect(self, client_id: str = "python_client"):
        """Verbindet zum Server"""
        self.websocket = await websockets.connect(f"{self.uri}/{client_id}")
        self.connected = True
        logger.info(f"Connected to {self.uri} as {client_id}")

    async def disconnect(self):
        """Trennt Verbindung"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False

    async def send(self, message_type: str, payload: dict):
        """Sendet Nachricht"""
        if not self.websocket:
            raise RuntimeError("Not connected")

        message = WebSocketMessage(type=message_type, payload=payload)
        await self.websocket.send(message.to_json())

    async def receive(self) -> WebSocketMessage:
        """Empfängt Nachricht"""
        if not self.websocket:
            raise RuntimeError("Not connected")

        raw = await self.websocket.recv()
        return WebSocketMessage.from_json(raw)

    async def request_state(self) -> dict:
        """Fordert aktuellen State an"""
        await self.send(MessageType.STATE_REQUEST.value, {})
        response = await self.receive()
        if response.type == MessageType.STATE_FULL.value:
            self.state = response.payload
            return self.state
        return {}

    async def change_emotion(self, emotion: str, delta: float):
        """Ändert eine Emotion"""
        await self.send(
            MessageType.EMOTION_CHANGE.value,
            {"emotion": emotion, "delta": delta}
        )

# ==================== SINGLETON & API ====================

_sync_server: Optional[NajikaStateSyncServer] = None

def get_sync_server() -> NajikaStateSyncServer:
    """Gibt die globale Sync-Server Instanz zurück"""
    global _sync_server
    if _sync_server is None:
        _sync_server = NajikaStateSyncServer()
    return _sync_server

async def start_sync_server():
    """Startet den Sync-Server"""
    server = get_sync_server()
    await server.start()

# ==================== TEST ====================

if __name__ == "__main__":
    async def test():
        server = NajikaStateSyncServer()

        # Server in Background starten
        server_task = asyncio.create_task(server.start())

        # Kurz warten bis Server läuft
        await asyncio.sleep(1)

        # Test Client
        client = NajikaStateSyncClient()
        await client.connect("test_client")

        # State anfordern
        state = await client.request_state()
        print(f"Received state: {json.dumps(state, indent=2)}")

        # Emotion ändern
        await client.change_emotion("joy", 0.5)
        await asyncio.sleep(0.5)

        # Neuen State anfordern
        state = await client.request_state()
        print(f"Updated state: {json.dumps(state, indent=2)}")

        await client.disconnect()
        server.stop()

    asyncio.run(test())
