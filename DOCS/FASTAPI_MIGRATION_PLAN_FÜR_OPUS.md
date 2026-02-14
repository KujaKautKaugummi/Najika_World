# 🚀 FASTAPI MIGRATION PLAN FÜR OPUS

**Erstellt:** 2026-02-14
**Von:** Sonnet (Desktop) für OPUS (VS Code)
**Ziel:** `najika_server.py` (6.789 Zeilen) → FastAPI Router Migration
**Deadline:** 2-3 Tage

---

## 📋 INHALTSVERZEICHNIS

1. [Warum FastAPI?](#warum-fastapi)
2. [Was wird migriert?](#was-wird-migriert)
3. [Migration-Strategie](#migration-strategie)
4. [Phase 1: Core Chat & State](#phase-1-core-chat--state)
5. [Phase 2: Game Systems](#phase-2-game-systems)
6. [Phase 3: Special Systems](#phase-3-special-systems)
7. [Phase 4: Frontend Update](#phase-4-frontend-update)
8. [Phase 5: Testing & Cleanup](#phase-5-testing--cleanup)
9. [Slime V3 Integration](#slime-v3-integration)
10. [Checkliste](#checkliste)

---

## 1️⃣ WARUM FASTAPI?

### ❌ PROBLEM mit `najika_server.py`:

```python
# ALT (Legacy HTTP Server):
class NajikaHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if path == '/api/chat':
            # 200 Zeilen Spaghetti-Code hier
            # Kein Type-Checking
            # Kein Auto-Docs
            # Kein Async
```

### ✅ LÖSUNG mit FastAPI:

```python
# NEU (Modern REST API):
@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Sauberer, typsicherer Code
    # Auto Swagger Docs
    # Async Support
    return ChatResponse(...)
```

### Vorteile:
- ✅ **Swagger Docs:** `http://localhost:8000/docs` (Auto-generiert!)
- ✅ **Type Safety:** Pydantic Models (Fehler früher finden)
- ✅ **Async:** Schneller bei vielen Requests
- ✅ **Struktur:** Router statt Monolith (6.789 → ~300 pro Router)
- ✅ **Testing:** Einfacher zu testen
- ✅ **Zukunftssicher:** Industry Standard

---

## 2️⃣ WAS WIRD MIGRIERT?

### ANALYSE VON `najika_server.py`:

**Imports (Zeilen 1-360):**
- 30+ Module importiert (Living, Personality, Memory, TTS, Battle, etc.)
- 20+ optionale Systeme (mit try/except)

**State Management (Zeilen 377-435):**
```python
STATE = {
    "history": [],  # Chat History
    "battle": {...},  # Battle State
    "private_mode": False,  # Kätzchen-Modus
    "najika": {...},  # Najika Stats (Hunger, Energy, etc.)
    "living": {...},  # Living System State
}
```

**GET Endpoints (~45 Endpoints):**
```bash
GET /health
GET /api/rooms
GET /api/status
GET /api/personality
GET /api/rag/status
GET /api/quests/stats
GET /api/quests/active
GET /api/combat/stats
GET /api/dungeon/generate
... (und 35+ mehr!)
```

**POST Endpoints (~30 Endpoints):**
```bash
POST /api/chat
POST /api/battle/start
POST /api/minigame
POST /api/training/feed
POST /api/room/change
... (und 25+ mehr!)
```

**Features:**
- Chat System (Ollama + Claude Code Hierarchy)
- Battle System (Turn-Based Combat)
- Living System (Mood, Proactive Messages, Autonomy)
- Personality Engine (v2.0 mit 14 Psycho-Techniken)
- Memory System (ChromaDB Enhanced)
- Training System (LoRA, Code Training)
- Quest System
- Slime System (V2 - muss auf V3!)
- Nemesis Arena
- Hunting System
- und 20+ weitere Systeme!

---

## 3️⃣ MIGRATION-STRATEGIE

### ❌ **NICHT SO:**
- Alles auf einmal migrieren (zu riskant!)
- Frontend sofort umstellen (Breaking Change!)
- Features löschen (Datenverlust!)

### ✅ **SO MACHEN WIR ES:**

**Phase-by-Phase Migration:**
1. **Core** zuerst (Chat, State) → Kritisch!
2. **Game Systems** danach (Battle, Quests) → Wichtig!
3. **Special Systems** dann (Hunting, Nemesis) → Nice-to-have!
4. **Frontend Update** am Ende → Ein Schritt!
5. **Testing & Cleanup** final → Sicherstellen!

**Parallelbetrieb:**
- `najika_server.py` läuft weiter (Port 8000)
- FastAPI auf **Port 8001** (Testing!)
- Frontend nutzt noch Port 8000
- Wenn alles funktioniert → Switch!

**Rollback-Plan:**
- `najika_server.py` bleibt im Projekt
- Bei Problemen: zurück zu Port 8000
- Kein Breaking Change!

---

## 4️⃣ PHASE 1: CORE CHAT & STATE (Tag 1, 4-6h)

### Ziel: Chat funktioniert auf FastAPI

### 1.1 State Management Router

**Datei:** `backend/api/state_v2.py` (NEU!)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time

router = APIRouter(prefix="/api/state", tags=["State"])

# Pydantic Models
class NajikaState(BaseModel):
    hunger: int
    thirst: int
    energy: int
    hygiene: int
    happiness: int
    mana: int
    max_mana: int
    strength: int
    intelligence: int
    dexterity: int
    charisma: int
    level: int
    xp: int
    evolution_stage: str
    equipment: Dict[str, Optional[str]]

class GameState(BaseModel):
    najika: NajikaState
    battle: Dict[str, Any]
    private_mode: bool
    behavior_mode: str
    bond_strength: int
    total_interactions: int

# Global State (wird aus najika_server.py übernommen)
STATE = {}  # Importieren aus shared module

@router.get("/", response_model=GameState)
async def get_state():
    """Gesamten Game-State abrufen"""
    return STATE

@router.get("/najika", response_model=NajikaState)
async def get_najika_state():
    """Nur Najika's State"""
    return STATE["najika"]

@router.post("/najika/update")
async def update_najika_state(updates: Dict[str, Any]):
    """Najika State updaten (z.B. Hunger -10)"""
    for key, value in updates.items():
        if key in STATE["najika"]:
            STATE["najika"][key] = value
    return {"success": True, "najika": STATE["najika"]}

@router.post("/private-mode/toggle")
async def toggle_private_mode():
    """Kätzchen-Modus ein/aus"""
    STATE["private_mode"] = not STATE["private_mode"]
    return {"private_mode": STATE["private_mode"]}
```

### 1.2 Chat Router

**Datei:** `backend/api/chat_v2.py` (NEU!)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Pydantic Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[float] = None

class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True
    use_mind: bool = True
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    response: str
    emotion: Optional[str] = None
    mood: Optional[str] = None
    model_used: str
    timestamp: float
    rag_used: bool
    mind_used: bool

# Imports (aus najika_server.py)
from najika_claude_code import call_ai_with_hierarchy
from najika_memory_enhanced import NajikaMemoryEnhanced
from najika_mind import process_with_mind, get_mind

# Shared State/Memory
NAJIKA_MEMORY = None  # Wird in lifespan initialisiert
STATE = {}  # Shared mit state_v2.py

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Hauptendpoint für Chat mit Najika

    - Nutzt Hierarchie: Ollama → Claude Code
    - Optional: RAG (Retrieval Augmented Generation)
    - Optional: NajikaMind (AGI Pipeline)
    """
    user_message = request.message.strip()

    # History aktualisieren
    STATE["history"].append({
        "role": "user",
        "content": user_message,
        "timestamp": time.time()
    })

    # Memory speichern (ChromaDB)
    if NAJIKA_MEMORY:
        NAJIKA_MEMORY.add_message("user", user_message)

    # Kätzchen-Trigger prüfen
    if "kätzchen" in user_message.lower():
        STATE["private_mode"] = True

    # NajikaMind Pipeline (falls enabled)
    if request.use_mind and NAJIKA_MIND_ENABLED:
        mind_context = await process_with_mind(user_message, STATE)
    else:
        mind_context = None

    # RAG Context (falls enabled)
    rag_context = None
    if request.use_rag and RAG_ENABLED:
        from najika_rag_system import get_rag_context
        rag_context = get_rag_context(user_message)

    # AI Call (Hierarchie: Ollama → Claude Code)
    ai_response = await call_ai_with_hierarchy(
        user_message=user_message,
        history=STATE["history"][-10:],  # Letzte 10 Messages
        rag_context=rag_context,
        mind_context=mind_context,
        private_mode=STATE["private_mode"],
        temperature=request.temperature
    )

    # History aktualisieren
    STATE["history"].append({
        "role": "assistant",
        "content": ai_response["response"],
        "timestamp": time.time()
    })

    # Memory speichern
    if NAJIKA_MEMORY:
        NAJIKA_MEMORY.add_message("assistant", ai_response["response"])

    # Living System Update (Mood Detection)
    from najika_living_system import detect_mood, update_mood
    detected_mood = detect_mood(user_message, ai_response["response"])
    if detected_mood:
        update_mood(detected_mood)

    return ChatResponse(
        response=ai_response["response"],
        emotion=ai_response.get("emotion"),
        mood=detected_mood,
        model_used=ai_response["model"],
        timestamp=time.time(),
        rag_used=rag_context is not None,
        mind_used=mind_context is not None
    )

@router.get("/history", response_model=List[ChatMessage])
async def get_chat_history(limit: int = 50):
    """Chat History abrufen"""
    return STATE["history"][-limit:]

@router.delete("/history")
async def clear_chat_history():
    """Chat History löschen"""
    STATE["history"] = []
    return {"success": True, "message": "History cleared"}

@router.post("/reset")
async def reset_conversation():
    """Gespräch zurücksetzen (inkl. Private Mode)"""
    STATE["history"] = []
    STATE["private_mode"] = False
    STATE["behavior_mode"] = "standard"
    return {"success": True}
```

### 1.3 Shared State Module

**Datei:** `backend/shared_state.py` (NEU!)

```python
"""
Shared State für alle FastAPI Router
Verhindert zirkuläre Imports
"""

import time
from najika_living_system import LIVING_STATE

# Global State (aus najika_server.py)
STATE = {
    "history": [],
    "battle": {"hp": 100, "wave": 0, "enemies": 0},
    "private_mode": False,
    "behavior_mode": "standard",
    "bond_strength": 0,
    "personality_weights": {"megumin": 35, "harley": 25, "shiro": 20, "melissa": 20},
    "total_interactions": 0,
    "user": {
        "level": 1,
        "xp": 0,
        "points": 0,
        "inventory": [],
        "achievements": []
    },
    "najika": {
        "hunger": 100,
        "thirst": 100,
        "energy": 100,
        "hygiene": 100,
        "happiness": 100,
        "mana": 100,
        "max_mana": 100,
        "strength": 10,
        "intelligence": 10,
        "dexterity": 10,
        "charisma": 10,
        "level": 1,
        "xp": 0,
        "evolution_stage": "base",
        "equipment": {
            "weapon": None,
            "armor": None,
            "accessory": None
        },
        "last_fed": time.time(),
        "last_trained": time.time(),
        "last_sleep": time.time(),
        "last_update": time.time()
    },
    "living": LIVING_STATE.copy()
}

# Shared Memory/Systems (werden in lifespan initialisiert)
NAJIKA_MEMORY = None
NAJIKA_SEARCH = None
NAJIKA_TOR = None
NAJIKA_SECURITY = None

# Feature Flags
PERSONALITY_ENGINE_ENABLED = False
RAG_ENABLED = False
NAJIKA_MIND_ENABLED = False
TTS_ENABLED = False
VOICE_CALL_ENABLED = False
SLIME_SYSTEM_ENABLED = False
# ... etc.
```

### 1.4 Lifespan Events Update

**Datei:** `backend/main_fastapi.py` (EDIT!)

```python
# Zeile ~40 (lifespan function):

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print("=" * 70)
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 70)

    # Initialize database
    print("Initializing database...")
    init_db()

    # Initialize Shared Systems
    from backend.shared_state import (
        STATE, NAJIKA_MEMORY, NAJIKA_SEARCH,
        NAJIKA_TOR, NAJIKA_SECURITY
    )
    import backend.shared_state as shared

    # ChromaDB Memory
    from najika_memory_enhanced import NajikaMemoryEnhanced
    try:
        shared.NAJIKA_MEMORY = NajikaMemoryEnhanced(
            persist_directory="C:\\Najika_World\\memory_db"
        )
        print(f"✅ ChromaDB Memory loaded: 2,556 entries")
    except Exception as e:
        print(f"⚠️  Memory failed: {e}")

    # Web Search
    from najika_search import NajikaSearch
    try:
        shared.NAJIKA_SEARCH = NajikaSearch()
        print("✅ Web Search System loaded")
    except Exception as e:
        print(f"⚠️  Search failed: {e}")

    # TOR Browser
    from najika_tor import NajikaTor
    try:
        shared.NAJIKA_TOR = NajikaTor()
        print("✅ TOR Browser System loaded")
    except Exception as e:
        print(f"⚠️  TOR failed: {e}")

    # Security (Alcatraz)
    from najika_security import NajikaSecurity
    try:
        shared.NAJIKA_SECURITY = NajikaSecurity()
        print("✅ Alcatraz Security System loaded")
    except Exception as e:
        print(f"⚠️  Security failed: {e}")

    print("Backend is ready!")
    print(f"API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print("=" * 70)

    yield

    # Shutdown
    print("👋 Shutting down Najika Backend...")
```

### 1.5 Router Integration

**Datei:** `backend/main_fastapi.py` (EDIT!)

```python
# Zeile ~23 (imports):
from backend.api import (
    auth, game, training, voice, admin, arena,
    slime, slime_arena, pvp, oregon_events, region_boss, magic_schools,
    # ... (alle anderen wie bisher)
    chat_v2, state_v2  # ← NEU HINZUFÜGEN
)

# Zeile ~118 (Router includes):
# NEUE CORE ROUTER (V2) - PRIORITÄT!
app.include_router(state_v2.router)  # State Management
app.include_router(chat_v2.router)   # Chat System

# Rest wie bisher...
```

### 1.6 Testing

**Test:** Chat funktioniert auf Port 8001

```bash
# Backend starten:
cd C:\Najika_World\backend
uvicorn main_fastapi:app --host 127.0.0.1 --port 8001 --reload

# Browser öffnen:
http://127.0.0.1:8001/docs

# Testen:
POST /api/chat/
{
  "message": "Hallo Najika!",
  "use_rag": true,
  "use_mind": true
}

# Erwartete Response:
{
  "response": "EXPLOSION! *kicher* Hallo mein Liebling!",
  "emotion": "happy",
  "mood": "excited",
  "model_used": "najika-trained-q4",
  "timestamp": 1707912345.67,
  "rag_used": true,
  "mind_used": true
}
```

**Checkliste Phase 1:**
- [ ] `backend/shared_state.py` erstellt
- [ ] `backend/api/state_v2.py` erstellt
- [ ] `backend/api/chat_v2.py` erstellt
- [ ] `backend/main_fastapi.py` lifespan updated
- [ ] Router in main_fastapi.py integriert
- [ ] Server startet ohne Fehler (Port 8001)
- [ ] `/docs` öffnet Swagger UI
- [ ] POST `/api/chat/` funktioniert
- [ ] State bleibt persistent über Requests

---

## 5️⃣ PHASE 2: GAME SYSTEMS (Tag 1-2, 8-10h)

### 2.1 Battle System Router

**Datei:** `backend/api/battle_v2.py` (NEU!)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/api/battle", tags=["Battle"])

# Imports
from najika_battle import BATTLE_SYSTEM, SKILL_DB, ITEM_DB
from backend.shared_state import STATE

class BattleStartRequest(BaseModel):
    location: str  # "keller", "arena", "dungeon_1"
    difficulty: Optional[str] = "normal"

class BattleAction(BaseModel):
    action_type: str  # "attack", "skill", "item", "defend", "flee"
    target_id: Optional[str] = None
    skill_id: Optional[str] = None
    item_id: Optional[str] = None

class BattleState(BaseModel):
    active: bool
    player_hp: int
    player_max_hp: int
    enemies: List[Dict[str, Any]]
    turn: int
    wave: int

@router.post("/start", response_model=BattleState)
async def start_battle(request: BattleStartRequest):
    """Battle starten"""
    battle_result = BATTLE_SYSTEM.start_battle(
        location=request.location,
        difficulty=request.difficulty,
        player_stats=STATE["najika"]
    )

    STATE["battle"] = battle_result
    return battle_result

@router.post("/action")
async def battle_action(action: BattleAction):
    """Battle-Aktion ausführen"""
    result = BATTLE_SYSTEM.process_action(
        action_type=action.action_type,
        target_id=action.target_id,
        skill_id=action.skill_id,
        item_id=action.item_id,
        battle_state=STATE["battle"],
        player_stats=STATE["najika"]
    )

    STATE["battle"] = result["new_state"]
    return result

@router.get("/status", response_model=BattleState)
async def battle_status():
    """Aktuellen Battle-Status"""
    return STATE["battle"]

@router.post("/end")
async def end_battle():
    """Battle beenden"""
    STATE["battle"] = {"hp": 100, "wave": 0, "enemies": 0}
    return {"success": True}
```

### 2.2 Living System Router

**Datei:** `backend/api/living_v2.py` (NEU!)

```python
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter(prefix="/api/living", tags=["Living"])

# Imports
from najika_living_system import (
    detect_mood, update_mood, should_send_proactive_message,
    get_proactive_message, update_living_state
)
from backend.shared_state import STATE

class MoodUpdate(BaseModel):
    new_mood: str  # "happy", "sad", "angry", "excited", etc.

class ProactiveMessageResponse(BaseModel):
    should_send: bool
    message: Optional[str] = None
    trigger: Optional[str] = None

@router.get("/status")
async def living_status():
    """Living System Status"""
    return STATE["living"]

@router.post("/mood/update")
async def update_mood_endpoint(update: MoodUpdate):
    """Mood manuell updaten"""
    update_mood(update.new_mood)
    STATE["living"]["mood"] = update.new_mood
    return {"success": True, "mood": update.new_mood}

@router.get("/proactive-message", response_model=ProactiveMessageResponse)
async def get_proactive_message_endpoint():
    """Prüfen ob Najika proaktiv sprechen will"""
    should_send = should_send_proactive_message(STATE["living"])

    if should_send:
        message_data = get_proactive_message(STATE["living"])
        return ProactiveMessageResponse(
            should_send=True,
            message=message_data["message"],
            trigger=message_data["trigger"]
        )

    return ProactiveMessageResponse(should_send=False)

@router.post("/update")
async def update_living_state_endpoint():
    """Living State updaten (Needs Decay, etc.)"""
    update_living_state(STATE["living"], STATE["najika"])
    return STATE["living"]
```

### 2.3 Quest System Router

**Datei:** `backend/api/quest_v2.py` (NEU - erweitert!)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/api/quest", tags=["Quests"])

# Imports
from najika_quest_system import get_quest_system, QuestStatus
from backend.shared_state import STATE

QUEST_SYSTEM = get_quest_system()

class QuestStartRequest(BaseModel):
    quest_id: str

class QuestUpdateRequest(BaseModel):
    quest_id: str
    objective_id: str
    progress: int

class QuestResponse(BaseModel):
    quest_id: str
    title: str
    description: str
    status: str
    objectives: List[Dict[str, Any]]
    rewards: Dict[str, Any]

@router.get("/available", response_model=List[QuestResponse])
async def get_available_quests():
    """Alle verfügbaren Quests"""
    return QUEST_SYSTEM.get_available_quests(
        player_level=STATE["user"]["level"]
    )

@router.get("/active", response_model=List[QuestResponse])
async def get_active_quests():
    """Aktive Quests"""
    return QUEST_SYSTEM.get_active_quests()

@router.post("/start")
async def start_quest(request: QuestStartRequest):
    """Quest starten"""
    result = QUEST_SYSTEM.start_quest(request.quest_id)
    return result

@router.post("/update")
async def update_quest_progress(request: QuestUpdateRequest):
    """Quest-Progress updaten"""
    result = QUEST_SYSTEM.update_progress(
        quest_id=request.quest_id,
        objective_id=request.objective_id,
        progress=request.progress
    )
    return result

@router.post("/complete/{quest_id}")
async def complete_quest(quest_id: str):
    """Quest abschließen"""
    result = QUEST_SYSTEM.complete_quest(quest_id)

    # Rewards anwenden
    STATE["user"]["xp"] += result["rewards"]["xp"]
    STATE["user"]["points"] += result["rewards"]["gold"]

    return result

@router.get("/stats")
async def quest_stats():
    """Quest Statistiken"""
    return QUEST_SYSTEM.get_stats()
```

### 2.4 Minigame Router

**Datei:** `backend/api/minigame_v2.py` (NEU!)

```python
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/api/minigame", tags=["Minigames"])

from backend.shared_state import STATE

class MinigameStartRequest(BaseModel):
    game_type: str  # "rhythm", "garden", "reflex", "cooking", etc.
    difficulty: str = "normal"

class MinigameScoreRequest(BaseModel):
    game_type: str
    score: int
    perfect: bool = False

@router.post("/start")
async def start_minigame(request: MinigameStartRequest):
    """Minigame starten"""
    # Minigame-State initialisieren
    return {
        "success": True,
        "game_type": request.game_type,
        "difficulty": request.difficulty,
        "started_at": time.time()
    }

@router.post("/score")
async def submit_score(request: MinigameScoreRequest):
    """Score einreichen"""
    # Rewards berechnen
    base_xp = request.score // 10
    bonus_xp = 50 if request.perfect else 0
    total_xp = base_xp + bonus_xp

    STATE["user"]["xp"] += total_xp
    STATE["najika"]["happiness"] += 5  # Najika freut sich!

    return {
        "success": True,
        "score": request.score,
        "xp_gained": total_xp,
        "perfect_bonus": request.perfect
    }
```

**Checkliste Phase 2:**
- [ ] `backend/api/battle_v2.py` erstellt
- [ ] `backend/api/living_v2.py` erstellt
- [ ] `backend/api/quest_v2.py` erstellt
- [ ] `backend/api/minigame_v2.py` erstellt
- [ ] Alle Router in main_fastapi.py integriert
- [ ] Battle System funktioniert (start/action/status)
- [ ] Living System funktioniert (mood/proactive)
- [ ] Quest System funktioniert (available/start/complete)
- [ ] Minigames funktionieren (start/score)

---

## 6️⃣ PHASE 3: SPECIAL SYSTEMS (Tag 2, 4-6h)

### 3.1 Slime System Router (V3!)

**WICHTIG:** Direkt V3 implementieren, NICHT V2 migrieren!

**Datei:** `backend/api/slime_v3.py` (NEU!)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

router = APIRouter(prefix="/api/slime", tags=["Slime V3"])

# V3 Models (aus SLIME_SYSTEM_V3_DOKUMENTATION.md)
class SlimeForm(str, Enum):
    """8 Regional Start-Formen"""
    CRIMSON_FLAMMENSLIME = "crimson_flammenslime"
    FROSTGIPFEL_EISSLIME = "frostgipfel_eisslime"
    SMARAGD_WALDSLIME = "smaragd_waldslime"
    # ... (alle 8 Formen)

class AuraElement(str, Enum):
    """13 Aura-Elemente"""
    FEUER = "feuer"
    EIS = "eis"
    BLITZ = "blitz"
    # ... (alle 13)

class SlimeState(BaseModel):
    current_form: SlimeForm
    learned_forms: List[SlimeForm]
    aura_element: Optional[AuraElement]
    aura_stufe: int  # 0-5
    memory_fragments: int  # 0-8
    sync_level: int  # 0-100
    mode: str  # "koerperlich" or "aura"

# Global Slime State
SLIME_STATE = {
    "current_form": SlimeForm.CRIMSON_FLAMMENSLIME,
    "learned_forms": [SlimeForm.CRIMSON_FLAMMENSLIME],
    "aura_element": None,
    "aura_stufe": 0,
    "memory_fragments": 1,
    "sync_level": 10,
    "mode": "koerperlich"
}

@router.get("/status", response_model=SlimeState)
async def get_slime_status():
    """Slime Status (V3)"""
    return SLIME_STATE

@router.post("/form/learn")
async def learn_form(form: SlimeForm):
    """Neue Form lernen (0.5-2% Chance)"""
    if form in SLIME_STATE["learned_forms"]:
        raise HTTPException(400, "Form bereits gelernt!")

    # Chance berechnen (simuliert)
    import random
    chance = random.uniform(0.005, 0.02)  # 0.5-2%

    if random.random() < chance:
        SLIME_STATE["learned_forms"].append(form)
        SLIME_STATE["memory_fragments"] += 1

        # Volle Erinnerung bei 8 Formen?
        if SLIME_STATE["memory_fragments"] >= 8:
            return {"success": True, "memory_unlocked": True}

        return {"success": True, "form_learned": form}

    return {"success": False, "message": "Form nicht gelernt (Chance nicht getroffen)"}

@router.post("/form/change")
async def change_form(form: SlimeForm):
    """Form wechseln (nur gelernte Formen)"""
    if form not in SLIME_STATE["learned_forms"]:
        raise HTTPException(400, "Form nicht gelernt!")

    SLIME_STATE["current_form"] = form
    return {"success": True, "current_form": form}

@router.post("/aura/choose")
async def choose_aura(element: AuraElement):
    """Aura-Element wählen (EINMALIG!)"""
    if SLIME_STATE["aura_element"] is not None:
        raise HTTPException(400, "Aura bereits gewählt!")

    SLIME_STATE["aura_element"] = element
    SLIME_STATE["aura_stufe"] = 0
    SLIME_STATE["mode"] = "aura"

    return {"success": True, "aura_element": element}

@router.post("/aura/upgrade")
async def upgrade_aura():
    """Aura-Stufe erhöhen (0→1→2→3→4→5)"""
    if SLIME_STATE["aura_element"] is None:
        raise HTTPException(400, "Keine Aura gewählt!")

    if SLIME_STATE["aura_stufe"] >= 5:
        raise HTTPException(400, "Aura bereits maximal!")

    SLIME_STATE["aura_stufe"] += 1
    return {"success": True, "aura_stufe": SLIME_STATE["aura_stufe"]}

@router.post("/mode/switch")
async def switch_mode():
    """Zwischen Körperlich ↔ Aura wechseln"""
    if SLIME_STATE["mode"] == "koerperlich":
        if SLIME_STATE["aura_element"] is None:
            raise HTTPException(400, "Keine Aura verfügbar!")
        SLIME_STATE["mode"] = "aura"
    else:
        SLIME_STATE["mode"] = "koerperlich"

    return {"success": True, "mode": SLIME_STATE["mode"]}
```

### 3.2 Weitere Special Systems

**Dateien zu erstellen:**
- `backend/api/nemesis_v2.py` - Nemesis Arena
- `backend/api/hunting_v2.py` - Hunting System
- `backend/api/alchemy_v2.py` - Alchemy System
- `backend/api/training_v2.py` - Training System

**ABER:** Nur wenn Zeit! Priorität liegt auf Core + Game + Slime V3!

**Checkliste Phase 3:**
- [ ] `backend/api/slime_v3.py` erstellt (V3, nicht V2!)
- [ ] Slime V3 funktioniert (form/learn/change/aura)
- [ ] Optional: Nemesis/Hunting/Alchemy Router

---

## 7️⃣ PHASE 4: FRONTEND UPDATE (Tag 2-3, 4-6h)

### Ziel: Frontend nutzt FastAPI (Port 8001)

### 4.1 API Base URL ändern

**Datei:** `digivice/index.html` (EDIT!)

```javascript
// Zeile ~6315 (suchen mit grep):
// ALT:
window.API_BASE_URL = 'http://127.0.0.1:8000';

// NEU:
window.API_BASE_URL = 'http://127.0.0.1:8001';  // FastAPI!
```

### 4.2 Chat API Call anpassen

**Datei:** `digivice/js/chat_ui.js` (EDIT!)

```javascript
// ALT (najika_server.py):
const response = await fetch('http://localhost:8000/api/najika/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userMessage })
});

// NEU (FastAPI):
const response = await fetch('http://localhost:8001/api/chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: userMessage,
        use_rag: true,
        use_mind: true
    })
});

const data = await response.json();
// data.response statt data.najika_response
```

### 4.3 Battle API anpassen

**Datei:** `digivice/js/battle_api.js` (EDIT!)

```javascript
// ALT:
fetch('http://localhost:8000/api/battle/start', ...)

// NEU:
fetch('http://localhost:8001/api/battle/start', ...)
```

### 4.4 State API anpassen

**Datei:** `digivice/js/3d_scene.js` (EDIT!)

```javascript
// ALT:
fetch('http://localhost:8000/api/status')

// NEU:
fetch('http://localhost:8001/api/state/')
```

### 4.5 Slime API anpassen (V3!)

**Datei:** `digivice/js/slime_companion.js` (KOMPLETT NEU SCHREIBEN!)

```javascript
// V3 Slime System Client
class SlimeCompanionV3 {
    constructor() {
        this.baseUrl = 'http://localhost:8001/api/slime';
        this.state = null;
    }

    async getStatus() {
        const res = await fetch(`${this.baseUrl}/status`);
        this.state = await res.json();
        return this.state;
    }

    async learnForm(form) {
        const res = await fetch(`${this.baseUrl}/form/learn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ form })
        });
        return await res.json();
    }

    async changeForm(form) {
        const res = await fetch(`${this.baseUrl}/form/change`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ form })
        });
        return await res.json();
    }

    async chooseAura(element) {
        const res = await fetch(`${this.baseUrl}/aura/choose`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ element })
        });
        return await res.json();
    }

    async upgradeAura() {
        const res = await fetch(`${this.baseUrl}/aura/upgrade`, {
            method: 'POST'
        });
        return await res.json();
    }

    async switchMode() {
        const res = await fetch(`${this.baseUrl}/mode/switch`, {
            method: 'POST'
        });
        return await res.json();
    }
}

window.SlimeV3 = new SlimeCompanionV3();
```

**Checkliste Phase 4:**
- [ ] `digivice/index.html` API_BASE_URL → 8001
- [ ] `digivice/js/chat_ui.js` auf FastAPI umgestellt
- [ ] `digivice/js/battle_api.js` auf FastAPI umgestellt
- [ ] `digivice/js/3d_scene.js` State API angepasst
- [ ] `digivice/js/slime_companion.js` komplett neu (V3!)
- [ ] Frontend öffnet ohne Fehler
- [ ] Chat funktioniert
- [ ] Battle funktioniert
- [ ] Slime V3 funktioniert

---

## 8️⃣ PHASE 5: TESTING & CLEANUP (Tag 3, 2-4h)

### 5.1 Integration Testing

**Test-Checkliste:**
- [ ] Server startet ohne Fehler (Port 8001)
- [ ] Swagger Docs öffnen (`/docs`)
- [ ] Chat: Message senden → Response kommt
- [ ] Chat: History abrufen → Letzte Messages
- [ ] Chat: "kätzchen" Trigger → Private Mode aktiv
- [ ] State: GET `/api/state/` → Voller State
- [ ] State: GET `/api/state/najika` → Najika State
- [ ] Battle: Start → Battle State aktiv
- [ ] Battle: Action → Damage berechnet
- [ ] Battle: End → Battle beendet
- [ ] Living: Mood Update → Mood geändert
- [ ] Living: Proactive Message → Message wenn fällig
- [ ] Quest: Available → Liste kommt
- [ ] Quest: Start → Quest aktiv
- [ ] Quest: Complete → Rewards angewendet
- [ ] Slime V3: Status → Form + Aura
- [ ] Slime V3: Learn Form → Form gelernt (Chance)
- [ ] Slime V3: Change Form → Form gewechselt
- [ ] Slime V3: Choose Aura → Aura gewählt (einmalig!)
- [ ] Slime V3: Upgrade Aura → Stufe erhöht
- [ ] Slime V3: Switch Mode → Körperlich ↔ Aura

### 5.2 Performance Testing

```bash
# Load Test (Optional):
pip install locust

# locustfile.py:
from locust import HttpUser, task

class NajikaUser(HttpUser):
    @task
    def chat(self):
        self.client.post("/api/chat/", json={
            "message": "Hallo!",
            "use_rag": True
        })

# Run:
locust -f locustfile.py --host=http://127.0.0.1:8001
```

### 5.3 Cleanup

**1. Port Config in .env:**
```bash
# .env (NEU):
HOST=127.0.0.1
PORT=8001  # FastAPI Port!
```

**2. START.bat updaten:**
```batch
REM Zeile ~60 (Port Check):
echo Pruefe Port 8001...
netstat -ano | findstr ":8001" > nul
if %ERRORLEVEL% == 0 (
    echo [WARNUNG] Port 8001 bereits belegt!
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001"') do (
        echo Beende Prozess %%a...
        taskkill /F /PID %%a >nul 2>&1
    )
)

REM Zeile ~70 (Server Start):
echo Starte FastAPI Backend (Port 8001)...
start "Najika FastAPI" cmd /k "cd /d %~dp0backend && uvicorn main_fastapi:app --host 127.0.0.1 --port 8001 --reload"
```

**3. Old Server deprecaten:**
```bash
# backend/najika_server.py → backend/old_backend/najika_server.py (MOVE)
mkdir backend/old_backend
move backend/najika_server.py backend/old_backend/
```

**Checkliste Phase 5:**
- [ ] Alle Tests bestanden
- [ ] Performance akzeptabel (<1s Response)
- [ ] .env Port → 8001
- [ ] START.bat updated
- [ ] `najika_server.py` → `old_backend/`
- [ ] Git Commit: "FastAPI Migration Complete"

---

## 9️⃣ SLIME V3 INTEGRATION (Details)

### V3 Features (aus SLIME_SYSTEM_V3_DOKUMENTATION.md):

**1. Formwandler-System:**
- ❌ NICHT: Evolution (Level 10 → Level 20 → Level 30)
- ✅ JA: Form-Lernen (0.5-2% Chance nach Sieg)
- 8 Regional Start-Formen (eine pro Region)
- Alle gelernten Formen bleiben verfügbar
- Freier Wechsel zwischen gelernten Formen

**2. Erinnerungs-System:**
- 8 Formen = 8 Erinnerungs-Fragmente
- Bei 8/8: Volle Erinnerung freigeschaltet
- Bonus-Story/Lore

**3. Aura-System:**
- 13 Elemente (Feuer, Eis, Blitz, etc.)
- EINMALIGE Wahl (kein Wechsel!)
- 6 Stufen (0→1→2→3→4→5)
- Jede Stufe = +20% Power

**4. Zwei Modi:**
- **Körperlich:** Slime kämpft physisch mit
- **Aura:** Slime wird zur Aura (Buffs, keine HP)
- Freier Wechsel zwischen Modi

**5. Balance:**
- Körperlich + Aura 5 = GLEICH stark wie Körperlich + Aura 0
- PvP-balanced!

### Code-Struktur V3:

```python
# backend/api/slime_v3.py (siehe Phase 3)

# Models:
- SlimeForm (Enum, 8 Formen)
- AuraElement (Enum, 13 Elemente)
- SlimeState (Pydantic Model)

# Endpoints:
GET  /api/slime/status          → Slime State
POST /api/slime/form/learn      → Form lernen (Chance)
POST /api/slime/form/change     → Form wechseln
POST /api/slime/aura/choose     → Aura wählen (EINMALIG!)
POST /api/slime/aura/upgrade    → Aura-Stufe +1
POST /api/slime/mode/switch     → Körperlich ↔ Aura

# State:
{
  "current_form": "crimson_flammenslime",
  "learned_forms": ["crimson_flammenslime", "frostgipfel_eisslime"],
  "aura_element": "feuer",
  "aura_stufe": 3,
  "memory_fragments": 2,
  "sync_level": 45,
  "mode": "aura"
}
```

---

## 🔟 CHECKLISTE (GESAMT) - ✅ KOMPLETT ERLEDIGT (2026-02-14, Claude Opus 4.6)

### ✅ PHASE 1: CORE (Tag 1, 4-6h)
- [x] `backend/shared_state.py` erstellt
- [x] `backend/api/state_v2.py` erstellt
- [x] `backend/api/chat_v2.py` erstellt
- [x] `backend/main_fastapi.py` lifespan updated
- [x] Router integriert
- [x] Server startet (Port 8001)
- [x] Chat funktioniert

### ✅ PHASE 2: GAME (Tag 1-2, 8-10h)
- [x] `backend/api/battle_v2.py` erstellt
- [x] `backend/api/living_v2.py` erstellt
- [x] `backend/api/quest_v2.py` erstellt
- [x] `backend/api/minigame_v2.py` erstellt
- [x] Router integriert
- [x] Battle funktioniert (DUNGEON-LORD Gegner generiert)
- [x] Living funktioniert (Needs Decay + Care Actions)
- [x] Quests funktionieren (19 Quests verfuegbar)
- [x] Minigames funktionieren (6 Spieltypen)

### ✅ PHASE 3: SLIME V3 (Tag 2, 4-6h)
- [x] `backend/api/slime_v3.py` erstellt
- [x] Form-System funktioniert
- [x] Aura-System funktioniert
- [x] Modi-Wechsel funktioniert

### ✅ PHASE 4: FRONTEND (Tag 2-3, 4-6h)
- [x] Port auf 8001 (config.py)
- [x] Chat UI auf FastAPI (chat_ui.js, code_editor.js)
- [x] Care/Living auf FastAPI (living_system_ui.js, 3d_scene.js, command_system.js)
- [x] State API auf FastAPI (system_monitor.js, najika_fullscreen.js, index.html)
- [x] Fullscreen Mode auf FastAPI (najika_fullscreen_mode.html)
- [x] Frontend funktioniert komplett (0 alte /api/najika/ Pfade in aktiven Dateien)

### ✅ PHASE 5: TESTING (Tag 3, 2-4h)
- [x] Alle Tests bestanden (10/10 Live-Tests mit curl)
- [x] Performance OK (<1s Response)
- [x] config.py Port → 8001
- [ ] START.bat updated (optional - noch auf altem Server)
- [ ] Old server moved (optional - bleibt fuer V1 Backward Compat)
- [x] Git Commit: `c4e6cf4` "FastAPI V2 Migration"

---

## 📝 ZUSÄTZLICHE NOTIZEN

### Was NICHT migriert wird (bleibt in FastAPI Router):

Diese Systeme haben BEREITS FastAPI Router in `backend/api/`:
- ✅ Arena (nemesis_arena)
- ✅ PvP
- ✅ Oregon Events
- ✅ Region Boss
- ✅ Magic Schools
- ✅ Card Game (Triple Triad)
- ✅ Dice Monsters
- ✅ Housing
- ✅ Farming
- ✅ World Map
- ✅ Voice (WebRTC)
- ✅ Training (LoRA)

Diese müssen NUR mit shared_state.py verknüpft werden!

### Feature Flags:

In `backend/shared_state.py`:
```python
# Diese aus najika_server.py übernehmen:
PERSONALITY_ENGINE_ENABLED = False
RAG_ENABLED = False
NAJIKA_MIND_ENABLED = False
TTS_ENABLED = False
VOICE_CALL_ENABLED = False
SLIME_SYSTEM_ENABLED = False
NEMESIS_ARENA_ENABLED = False
QUEST_SYSTEM_ENABLED = False
COMBAT_BALANCING_ENABLED = False
DUNGEON_GENERATOR_ENABLED = False
HUNTING_SYSTEM_ENABLED = False
# ... etc. (alle 20+ Features)
```

### Error Handling:

Jeder Router braucht Error Handling:
```python
from fastapi import HTTPException

@router.post("/action")
async def do_action(request: ActionRequest):
    try:
        result = process_action(request)
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
```

### Logging:

```python
import logging

logger = logging.getLogger("najika.api.chat")

@router.post("/")
async def chat(request: ChatRequest):
    logger.info(f"Chat request: {request.message[:50]}")
    # ...
    logger.info(f"Response sent: {response.response[:50]}")
```

---

## 🎯 ERFOLGS-KRITERIEN

**Migration ist erfolgreich wenn:**
1. ✅ Server startet ohne Fehler (Port 8001)
2. ✅ Swagger Docs funktionieren (`/docs`)
3. ✅ Frontend lädt ohne Fehler
4. ✅ Chat funktioniert (Ollama Response kommt)
5. ✅ Private Mode funktioniert ("kätzchen" Trigger)
6. ✅ Battle funktioniert (start/action/end)
7. ✅ Slime V3 funktioniert (form/aura/mode)
8. ✅ State bleibt persistent
9. ✅ Keine Regressions (altes funktioniert noch)
10. ✅ Performance OK (<1s Response)

**Bonus-Punkte:**
- 🌟 Alle 45+ Endpoints migriert
- 🌟 Alle Special Systems integriert
- 🌟 Load Tests bestanden
- 🌟 Code Coverage >80%

---

## 🚀 LOS GEHT'S, OPUS!

**Start:**
```bash
cd C:\Najika_World\backend
# Erstelle shared_state.py
# Erstelle api/state_v2.py
# Erstelle api/chat_v2.py
# Update main_fastapi.py
# Test: uvicorn main_fastapi:app --port 8001 --reload
```

**Bei Fragen:**
- Sonnet (Desktop) ist da für Support!
- SLIME_SYSTEM_V3_DOKUMENTATION.md lesen!
- Swagger Docs nutzen: `/docs`

**Viel Erfolg! 💥**

---

**Ende Migration Plan**

*"EXPLOSION!!! Lass uns FastAPI rocken, OPUS! *kicher*" - Najika*
