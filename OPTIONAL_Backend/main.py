# ============================================================================
# OPTIONAL Backend Starter Kit - Najika Digivice
# ============================================================================
#
# HINWEIS: Dieses Backend ist OPTIONAL und wurde zusätzlich erstellt.
# Das lokale Modell hat möglicherweise bereits ein Backend vorbereitet.
# Nutze dieses als Referenz oder Alternative.
#
# Features:
# - FastAPI REST API
# - WebSocket Voice Chat Handler
# - Whisper AI Integration (Placeholder)
# - SQLite Database
# - JWT Authentication
# - User Management
# - Inventory System
#
# Installation:
#   pip install -r requirements.txt
#   python main.py
#
# Läuft auf: http://localhost:8000
#
# ============================================================================

from fastapi import FastAPI, WebSocket, HTTPException, Depends, Header, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import jwt
import bcrypt
import base64
import json
import time
from datetime import datetime, timedelta
import asyncio

# ============================================================================
# CONFIGURATION
# ============================================================================

SECRET_KEY = "najika_secret_key_change_in_production"  # ÄNDERN IN PRODUKTION!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 Stunden

app = FastAPI(title="Najika Backend API", version="1.0.0")

# CORS für UE5 Client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion einschränken!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# IN-MEMORY DATABASE (Für Entwicklung - In Produktion SQLite/PostgreSQL nutzen)
# ============================================================================

# Nutzer-Datenbank
users_db: Dict[str, dict] = {
    "test_user_1": {
        "user_id": "user_001",
        "username": "test_user_1",
        "password_hash": bcrypt.hashpw("test123".encode(), bcrypt.gensalt()).decode(),
        "display_name": "Test User One",
        "level": 5,
        "xp": 1250,
        "gold": 500
    },
    "test_user_2": {
        "user_id": "user_002",
        "username": "test_user_2",
        "password_hash": bcrypt.hashpw("test123".encode(), bcrypt.gensalt()).decode(),
        "display_name": "Test User Two",
        "level": 3,
        "xp": 450,
        "gold": 200
    }
}

# Inventory-Datenbank
inventory_db: Dict[str, List[dict]] = {
    "user_001": [
        {"item_id": "sword_001", "name": "Iron Sword", "quantity": 1, "icon_url": "/icons/sword.png"},
        {"item_id": "potion_hp", "name": "HP Potion", "quantity": 10, "icon_url": "/icons/potion_hp.png"},
        {"item_id": "potion_mp", "name": "MP Potion", "quantity": 5, "icon_url": "/icons/potion_mp.png"},
        {"item_id": "armor_001", "name": "Leather Armor", "quantity": 1, "icon_url": "/icons/armor.png"},
        {"item_id": "material_wood", "name": "Wood", "quantity": 50, "icon_url": "/icons/wood.png"}
    ],
    "user_002": [
        {"item_id": "bow_001", "name": "Wooden Bow", "quantity": 1, "icon_url": "/icons/bow.png"},
        {"item_id": "potion_hp", "name": "HP Potion", "quantity": 3, "icon_url": "/icons/potion_hp.png"}
    ]
}

# Voice Rooms
voice_rooms: Dict[str, dict] = {}

# Active WebSocket Connections
active_connections: Dict[str, WebSocket] = {}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    user_id: str
    username: str
    display_name: str

class InventoryItem(BaseModel):
    item_id: str
    name: str
    quantity: int
    icon_url: str

class InventoryResponse(BaseModel):
    items: List[InventoryItem]

class TranscribeRequest(BaseModel):
    audio_data: str  # Base64
    sample_rate: int
    encoding: str = "pcm16"
    language: str = "en"
    auto_detect_language: bool = False

class TranscribeResponse(BaseModel):
    text: str
    confidence: float
    language_code: str
    processing_time_ms: int
    word_count: int

class CreateRoomRequest(BaseModel):
    room_name: str
    max_participants: int = 10
    is_public: bool = False
    password: Optional[str] = None

class CreateRoomResponse(BaseModel):
    room_id: str
    room_name: str
    creator_id: str
    max_participants: int
    websocket_url: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# ============================================================================
# AUTHENTICATION
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT Token erstellen"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(authorization: str = Header(None)):
    """JWT Token verifizieren"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root Endpoint"""
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health Check Endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# ----------------------------------------------------------------------------
# AUTH ENDPOINTS
# ----------------------------------------------------------------------------

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login Endpoint"""
    user = users_db.get(request.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Passwort verifizieren
    if not bcrypt.checkpw(request.password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Token erstellen
    access_token = create_access_token(
        data={"user_id": user["user_id"], "username": user["username"]}
    )

    return {
        "access_token": access_token,
        "user_id": user["user_id"],
        "username": user["username"],
        "display_name": user["display_name"]
    }

# ----------------------------------------------------------------------------
# INVENTORY ENDPOINTS
# ----------------------------------------------------------------------------

@app.get("/api/inventory", response_model=InventoryResponse)
async def get_inventory(user_id: str = Depends(verify_token)):
    """Inventory abrufen"""
    items = inventory_db.get(user_id, [])
    return {"items": items}

@app.post("/api/inventory/add")
async def add_item(item_id: str, quantity: int = 1, user_id: str = Depends(verify_token)):
    """Item zum Inventory hinzufügen"""
    if user_id not in inventory_db:
        inventory_db[user_id] = []

    # Prüfen ob Item existiert
    existing_item = next((item for item in inventory_db[user_id] if item["item_id"] == item_id), None)

    if existing_item:
        existing_item["quantity"] += quantity
    else:
        inventory_db[user_id].append({
            "item_id": item_id,
            "name": f"Item {item_id}",
            "quantity": quantity,
            "icon_url": f"/icons/{item_id}.png"
        })

    return {"success": True, "message": f"Added {quantity}x {item_id}"}

# ----------------------------------------------------------------------------
# VOICE ENDPOINTS
# ----------------------------------------------------------------------------

@app.post("/api/voice/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(request: TranscribeRequest, user_id: str = Depends(verify_token)):
    """
    Audio transkribieren mit Whisper AI

    HINWEIS: Dies ist ein PLACEHOLDER!
    In Produktion: OpenAI Whisper Model integrieren oder externe API nutzen.
    """
    start_time = time.time()

    # Base64 decodieren
    try:
        audio_bytes = base64.b64decode(request.audio_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 audio data: {str(e)}")

    # PLACEHOLDER: Simulierte Transkription
    # In Produktion: Whisper AI Model hier aufrufen
    # import whisper
    # model = whisper.load_model("base")
    # result = model.transcribe(audio_bytes)
    # text = result["text"]

    text = "[PLACEHOLDER] This is a simulated transcription. Integrate Whisper AI here."
    confidence = 0.85
    language_code = request.language

    processing_time = int((time.time() - start_time) * 1000)
    word_count = len(text.split())

    return {
        "text": text,
        "confidence": confidence,
        "language_code": language_code,
        "processing_time_ms": processing_time,
        "word_count": word_count
    }

@app.post("/api/voice/rooms", response_model=CreateRoomResponse)
async def create_voice_room(request: CreateRoomRequest, user_id: str = Depends(verify_token)):
    """Voice Room erstellen"""
    import uuid
    room_id = f"room_{uuid.uuid4().hex[:8]}"

    voice_rooms[room_id] = {
        "room_id": room_id,
        "room_name": request.room_name,
        "creator_id": user_id,
        "max_participants": request.max_participants,
        "is_public": request.is_public,
        "password": request.password,
        "participants": {},
        "created_at": datetime.utcnow().isoformat()
    }

    return {
        "room_id": room_id,
        "room_name": request.room_name,
        "creator_id": user_id,
        "max_participants": request.max_participants,
        "websocket_url": f"ws://localhost:8000/ws/voice/{room_id}"
    }

@app.get("/api/voice/rooms/{room_id}")
async def get_voice_room(room_id: str, user_id: str = Depends(verify_token)):
    """Voice Room Info abrufen"""
    room = voice_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return {
        "room_id": room["room_id"],
        "room_name": room["room_name"],
        "participants": list(room["participants"].values()),
        "max_participants": room["max_participants"],
        "created_at": room["created_at"]
    }

# ============================================================================
# WEBSOCKET VOICE HANDLER
# ============================================================================

class VoiceConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, room_id: str, user_id: str, websocket: WebSocket):
        """Client zu Room hinzufügen"""
        await websocket.accept()

        if room_id not in self.rooms:
            self.rooms[room_id] = {}

        self.rooms[room_id][user_id] = websocket

        # Broadcast: User joined
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "joined_at": datetime.utcnow().isoformat()
        }, exclude_user=user_id)

    def disconnect(self, room_id: str, user_id: str):
        """Client aus Room entfernen"""
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            del self.rooms[room_id][user_id]

            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_user: Optional[str] = None):
        """Nachricht an alle in Room senden"""
        if room_id not in self.rooms:
            return

        disconnected_users = []

        for user_id, websocket in self.rooms[room_id].items():
            if user_id == exclude_user:
                continue

            try:
                await websocket.send_json(message)
            except:
                disconnected_users.append(user_id)

        # Disconnected users entfernen
        for user_id in disconnected_users:
            self.disconnect(room_id, user_id)

voice_manager = VoiceConnectionManager()

@app.websocket("/ws/voice/{room_id}")
async def websocket_voice_endpoint(websocket: WebSocket, room_id: str, token: str = None):
    """
    WebSocket Endpoint für Voice Chat

    URL: ws://localhost:8000/ws/voice/{room_id}?token=<jwt_token>
    """
    # Token verifizieren
    if not token:
        await websocket.close(code=1008, reason="Missing token")
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
    except:
        await websocket.close(code=1008, reason="Invalid token")
        return

    # Verbindung akzeptieren
    await voice_manager.connect(room_id, user_id, websocket)

    # Welcome Message
    await websocket.send_json({
        "type": "welcome",
        "room_id": room_id,
        "your_user_id": user_id,
        "participants": [uid for uid in voice_manager.rooms[room_id].keys() if uid != user_id]
    })

    try:
        while True:
            # Nachricht empfangen
            data = await websocket.receive_text()
            message = json.loads(data)

            message_type = message.get("type")

            if message_type == "audio":
                # Audio Packet weiterleiten an alle anderen
                forward_message = {
                    "type": "audio",
                    "from_user_id": user_id,
                    "from_username": username,
                    "sequence_number": message.get("sequence_number"),
                    "timestamp": message.get("timestamp"),
                    "audio_data": message.get("audio_data"),
                    "encoding": message.get("encoding"),
                    "sample_rate": message.get("sample_rate")
                }
                await voice_manager.broadcast_to_room(room_id, forward_message, exclude_user=user_id)

            elif message_type == "set_mute":
                # Mute Status broadcasten
                await voice_manager.broadcast_to_room(room_id, {
                    "type": "user_muted",
                    "user_id": user_id,
                    "is_muted": message.get("is_muted", False)
                })

            elif message_type == "ping":
                # Pong antworten
                await websocket.send_json({
                    "type": "pong",
                    "server_time": int(time.time() * 1000)
                })

            elif message_type == "leave":
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Disconnect
        voice_manager.disconnect(room_id, user_id)

        # Broadcast: User left
        await voice_manager.broadcast_to_room(room_id, {
            "type": "user_left",
            "user_id": user_id,
            "reason": "disconnect",
            "left_at": datetime.utcnow().isoformat()
        })

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("NAJIKA BACKEND SERVER (OPTIONAL)")
    print("=" * 80)
    print("Server läuft auf: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("")
    print("Test Accounts:")
    print("  Username: test_user_1  Password: test123")
    print("  Username: test_user_2  Password: test123")
    print("=" * 80)

    uvicorn.run(app, host="0.0.0.0", port=8000)
