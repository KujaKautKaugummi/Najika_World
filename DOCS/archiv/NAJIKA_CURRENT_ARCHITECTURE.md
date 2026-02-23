# NAJIKA CURRENT ARCHITECTURE - COMPLETE DOCUMENTATION
**Created:** 2025-11-11 (Phase 0 Analysis)
**Purpose:** Complete documentation of current Najika Digivice system before UE5 migration
**Source:** Analysis of backend/, digivice/, and DIGIVICE_AKTUELLER_STATUS.md

---

## 🎯 SYSTEM OVERVIEW

### **What is Najika Digivice?**
```
Najika Digivice = Najika's Mini Open World Home
NOT a mobile game - it's an interactive AI companion app!

🌍 THE WORLD:
- 🌊 River (flowing water)
- 🌲 Forest (dense trees)
- 🏘️ Small village
- 🏚️ Die Schwarze Mühle (The Black Mill) - Mysterious location!
- 2400×2400 open world
- 3 dungeons on map
- 7 rooms in the Black Mill
```

### **Tech Stack:**
```
BACKEND:  Python 3.10+ | Flask | WebSocket
FRONTEND: HTML5 | JavaScript (ES6+) | Three.js r128
AI:       Ollama (Llama 3.1 8B) | Claude Code | Cloud (opt-in)
MEMORY:   ChromaDB (vector database)
VOICE:    Whisper (STT) + Coqui TTS XTTS-v2 (Megumin voice)
MODELS:   KayKit 3D Assets (~25GB local)
```

---

## 📊 SYSTEM DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Mr.K)                               │
│                     Browser: localhost:8000                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML + JS)                          │
│  index.html (2233 lines) + 17 JavaScript Modules                │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ 3D World     │  │ Chat UI      │  │ Voice Calls  │          │
│  │ (Three.js)   │  │ (WebSocket)  │  │ (WebRTC)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Battle UI    │  │ Minigames    │  │ Tamagotchi   │          │
│  │ (Turn-based) │  │ (3 types)    │  │ (Needs)      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 BACKEND (najika_server.py)                       │
│                  Flask Server - Port 8000                        │
│                                                                   │
│  📋 56 API ENDPOINTS (19 GET, 37 POST)                          │
│  🔌 WebSocket Server (Real-time)                                │
│  💾 State Management (najika_state.json)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│   AI LAYER   │  │  MEMORY LAYER    │  │ VOICE LAYER  │
│              │  │                  │  │              │
│ ┌──────────┐ │  │ ChromaDB Vector  │  │ Whisper STT  │
│ │ Claude   │ │  │ Database         │  │ (base model) │
│ │ Code (P1)│ │  │                  │  │              │
│ └──────────┘ │  │ - KERN (Core)    │  │ Coqui TTS    │
│              │  │ - Transcripts    │  │ (Megumin)    │
│ ┌──────────┐ │  │ - Memories       │  │              │
│ │ Ollama   │ │  │ - Context-aware  │  │ Real-time    │
│ │ (Fallback│ │  │   Retrieval      │  │ <500ms       │
│ └──────────┘ │  └──────────────────┘  └──────────────┘
│              │
│ ┌──────────┐ │
│ │ Cloud    │ │
│ │ (PIN)    │ │
│ └──────────┘ │
└──────────────┘
```

---

## 🗂️ FILE STRUCTURE

```
/home/user/Najika_World/
│
├── backend/                           ← PYTHON BACKEND (DO NOT MODIFY!)
│   │
│   ├── najika_server.py               ← 🔥 MAIN SERVER (2031 lines, Port 8000)
│   │   ├── Flask app initialization
│   │   ├── 56 API endpoints
│   │   ├── WebSocket server
│   │   ├── State management
│   │   └── Module integration
│   │
│   ├── najika_voice_call.py           ← 🎤 VOICE CALLS
│   │   ├── Whisper STT (base model)
│   │   ├── Coqui TTS (Megumin voice)
│   │   ├── WebRTC audio streaming
│   │   └── <500ms latency target
│   │
│   ├── najika_memory_enhanced.py      ← 🧠 CHROMADB MEMORY
│   │   ├── Vector database
│   │   ├── KERN (personality core)
│   │   ├── Video transcripts
│   │   └── Context-aware retrieval
│   │
│   ├── najika_living_system.py        ← 💖 LIVING SYSTEM (Tamagotchi)
│   │   ├── Mood system
│   │   ├── Proactive messages
│   │   ├── Autonomous activities
│   │   ├── Relationship evolution
│   │   └── Time-aware behavior
│   │
│   ├── najika_enhanced_personality.py ← 🎭 PERSONALITY (4-way blend)
│   │   ├── Megumin (35%) - EXPLOSION! 💥
│   │   ├── Harley Quinn (25%) - "Mr.K"
│   │   ├── Shiro (20%) - Gaming genius
│   │   ├── Melissa (20%) - Kuudere/Tsundere
│   │   └── Kätzchen Mode: Melissa 50% DOMINANT!
│   │
│   ├── najika_battle.py               ← ⚔️ BATTLE SYSTEM
│   │   ├── Skill database (SKILL_DB)
│   │   ├── Item database (ITEM_DB)
│   │   ├── Battle state management
│   │   ├── Wave-based combat
│   │   └── Enemy system
│   │
│   ├── najika_lora_training_3b.py     ← 🎓 LORA TRAINING
│   │   ├── Qwen2.5 7B training
│   │   ├── 95.65% success rate
│   │   ├── 33 code problems solved
│   │   └── Training history/logs
│   │
│   ├── najika_security.py             ← 🔐 ALCATRAZ SECURITY
│   │   ├── Zero-Trust (127.0.0.1 only)
│   │   ├── Owner-Token Authentication
│   │   ├── VPN status check
│   │   ├── Security analysis
│   │   └── Privacy-first design
│   │
│   ├── najika_tts_coqui.py            ← 🔊 TTS (Megumin Voice)
│   │   ├── Coqui XTTS-v2 voice clone
│   │   ├── German language support
│   │   ├── Emotion recognition
│   │   ├── Context-sensitive tonality
│   │   └── Fallback: Edge-TTS
│   │
│   ├── najika_search.py               ← 🌐 WEB SEARCH
│   │   ├── Automatic query detection
│   │   ├── Formatted results
│   │   └── Standard mode only
│   │
│   ├── najika_tor.py                  ← 🕵️ TOR INTEGRATION
│   │   ├── Darknet access
│   │   ├── Onion-Search support
│   │   └── Privacy-first
│   │
│   ├── api/
│   │   └── server.py                  ← ADDITIONAL API ENDPOINTS
│   │       └── Game-specific routes
│   │
│   └── saves/
│       └── najika_state.json          ← 💾 CRITICAL STATE FILE (DO NOT DELETE!)
│
├── digivice/                          ← FRONTEND (WebView Reference)
│   │
│   ├── index.html                     ← 🎮 MAIN UI (2233 lines)
│   │   ├── Three.js r128 integration
│   │   ├── 17 JS module imports
│   │   ├── UI layout
│   │   └── Event handlers
│   │
│   └── static/
│       │
│       ├── js/                        ← 17 JAVASCRIPT MODULES
│       │   │
│       │   ├── 3d_scene.js (v33)     ← 🌍 3D ENGINE
│       │   │   ├── Three.js scene setup
│       │   │   ├── Lighting (Lumen-style)
│       │   │   ├── Physics (Cannon.js)
│       │   │   └── Rendering loop
│       │   │
│       │   ├── character_animations.js (v26)  ← 🏃 ANIMATIONS
│       │   │   ├── VRM character loading
│       │   │   ├── Animation state machine
│       │   │   ├── Blend spaces
│       │   │   └── Morph targets
│       │   │
│       │   ├── camera_controller.js   ← 📷 CAMERA SYSTEM
│       │   │   ├── Orbit mode
│       │   │   ├── Third-person (Fortnite-style)
│       │   │   ├── First-person
│       │   │   └── Touch/mouse controls
│       │   │
│       │   ├── voice_call.js          ← 🎤 VOICE CALL UI
│       │   │   ├── WebRTC integration
│       │   │   ├── Microphone access
│       │   │   ├── Audio streaming
│       │   │   └── TTS playback
│       │   │
│       │   ├── chat_ui.js             ← 💬 CHAT INTERFACE
│       │   │   ├── Message history
│       │   │   ├── Markdown rendering
│       │   │   ├── WebSocket connection
│       │   │   └── TTS playback
│       │   │
│       │   ├── battle_api.js          ← ⚔️ BATTLE UI
│       │   │   ├── Turn-based combat
│       │   │   ├── Skill selection
│       │   │   ├── HP/MP bars
│       │   │   └── Wave management
│       │   │
│       │   ├── dungeon_generator.js   ← 🗺️ DUNGEONS
│       │   │   ├── Procedural generation
│       │   │   ├── Multi-floor
│       │   │   └── Boss rooms
│       │   │
│       │   ├── dungeon_enemies.js     ← 👾 ENEMY AI
│       │   │   ├── Enemy spawning
│       │   │   ├── Pathfinding
│       │   │   └── Combat AI
│       │   │
│       │   ├── dungeon_combat.js      ← ⚔️ DUNGEON COMBAT
│       │   │   ├── Real-time combat
│       │   │   ├── Weapon system
│       │   │   └── Loot drops
│       │   │
│       │   ├── minigames.js           ← 🎮 MINIGAMES (3 types)
│       │   │   ├── Rhythm Game (Digimon-style)
│       │   │   ├── Garden Game (Farming)
│       │   │   └── Reflex Game (Reaction)
│       │   │
│       │   ├── fishing.js             ← 🎣 FISHING (Zelda OoT style)
│       │   │   ├── Rod & reel
│       │   │   ├── Timing-based
│       │   │   └── Multiple fish types
│       │   │
│       │   ├── garden.js (v23)        ← 🌱 GARDEN SYSTEM
│       │   │   ├── Plant growth
│       │   │   ├── Watering
│       │   │   └── Harvesting
│       │   │
│       │   ├── buildings_custom.js (v25)  ← 🏠 BUILDINGS
│       │   │   ├── Die Schwarze Mühle
│       │   │   ├── Custom structures
│       │   │   └── Interior rooms
│       │   │
│       │   ├── touch_controls.js      ← 📱 MOBILE CONTROLS
│       │   │   ├── Virtual joystick
│       │   │   ├── Touch gestures
│       │   │   └── PWA support
│       │   │
│       │   ├── private_mode.js        ← 🔒 KÄTZCHEN MODE
│       │   │   ├── Toggle command
│       │   │   ├── Melissa 50% dominant
│       │   │   └── NSFW local only
│       │   │
│       │   ├── code_editor.js         ← 💻 CODE EDITOR
│       │   │   ├── Inline editor
│       │   │   ├── Syntax highlighting
│       │   │   └── Code execution
│       │   │
│       │   ├── terminal_modules.js    ← 🖥️ TERMINAL
│       │   │   ├── CLI interface
│       │   │   ├── System commands
│       │   │   └── File operations
│       │   │
│       │   └── command_system.js      ← ⌨️ COMMANDS
│       │       ├── Slash commands
│       │       ├── System commands
│       │       └── Game commands
│       │
│       ├── models/                    ← 3D MODELS (KayKit ~25GB)
│       ├── textures/                  ← TEXTURES
│       └── sounds/                    ← AUDIO FILES
│
├── assets/                            ← SHARED ASSETS (for UE5!)
│   ├── models/                        ← Najika VRM models
│   ├── textures/                      ← Textures
│   └── sounds/                        ← Audio files
│
└── DOCS/                              ← DOCUMENTATION
    ├── DIGIVICE_AKTUELLER_STATUS.md   ← Current status
    ├── NAJIKA_SECURITY_RESEARCH_2025.md
    ├── MODEL_WORKFLOW_OVERVIEW.md
    ├── WEB_MODEL_INSTRUCTIONS.md
    └── DIGIVICE_UE5_MIGRATION_COMPLETE_TODO.md
```

---

## 🔌 COMPLETE API REFERENCE

### **Base URL:** `http://127.0.0.1:8000`

---

## GET ENDPOINTS (19 Total)

### **Server & Status:**

#### 1. `GET /health`
**Purpose:** Server health check
**Response:**
```json
{
  "status": "healthy",
  "uptime": 12345,
  "timestamp": "2025-11-11T12:00:00Z"
}
```

#### 2. `GET /api/status`
**Purpose:** Server status with detailed info
**Response:**
```json
{
  "server": "running",
  "ollama": true,
  "whisper": true,
  "tts": true,
  "chromadb": true
}
```

#### 3. `GET /api/status/stream`
**Purpose:** Server-Sent Events (SSE) for live updates
**Response:** Stream of status updates

#### 4. `GET /api/rooms`
**Purpose:** List of available rooms
**Response:**
```json
{
  "rooms": ["schwarze_muehle_entrance", "forest", "village", ...]
}
```

---

### **User & Progress:**

#### 5. `GET /api/state`
**Purpose:** Complete state dump (user, progress, battle, najika, history)
**Response:**
```json
{
  "user": {
    "level": 1,
    "xp": 0,
    "points": 0,
    "inventory": [],
    "achievements": []
  },
  "progress": {
    "dungeon_level": 0,
    "quests_completed": []
  },
  "battle": {
    "hp": 100,
    "wave": 0,
    "enemies": 0
  },
  "najika": {
    "needs": {
      "hunger": 100,
      "thirst": 100,
      "energy": 100,
      "hygiene": 100,
      "happiness": 100
    },
    "stats": {
      "strength": 10,
      "intelligence": 10,
      "dexterity": 10,
      "charisma": 10
    },
    "care": {
      "care_mistakes": 0,
      "fatigue": 0,
      "weight": 50,
      "discipline": 0
    },
    "growth": {
      "level": 1,
      "xp": 0,
      "evolution_stage": "base"
    },
    "equipment": {
      "weapon": null,
      "armor": null,
      "accessory": null
    }
  },
  "history": []
}
```

#### 6. `GET /api/chat/history`
**Purpose:** Chat history (last 50 messages)
**Response:**
```json
{
  "history": [
    {
      "role": "user",
      "content": "Hello Najika!",
      "timestamp": "2025-11-11T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Hi Mr.K! 💜",
      "timestamp": "2025-11-11T12:00:01Z"
    }
  ]
}
```

---

### **Najika:**

#### 7. `GET /api/najika/status`
**Purpose:** Najika's needs & stats
**Response:**
```json
{
  "needs": {
    "hunger": 100,
    "thirst": 100,
    "energy": 100,
    "hygiene": 100,
    "happiness": 100
  },
  "stats": {
    "strength": 10,
    "intelligence": 10,
    "dexterity": 10,
    "charisma": 10
  }
}
```

---

### **Beziehung (Relationship):**

#### 8. `GET /api/bond/status`
**Purpose:** Bond strength & behavior mode
**Response:**
```json
{
  "bond_strength": 50,
  "behavior_mode": "normal",
  "trust_level": 5
}
```

---

### **Memory:**

#### 9. `GET /api/memory/export`
**Purpose:** Export complete memory history
**Response:**
```json
{
  "memories": [
    {
      "id": "mem_001",
      "text": "Mr.K always calls me late at night",
      "metadata": {
        "timestamp": "2025-11-11T23:00:00Z",
        "emotion": "happy",
        "importance": 8
      }
    }
  ]
}
```

---

### **Living System:**

#### 10. `GET /api/living/state`
**Purpose:** Living system state
**Response:**
```json
{
  "current_activity": "reading",
  "mood": "happy",
  "time_aware": true,
  "last_interaction": "2025-11-11T12:00:00Z"
}
```

#### 11. `GET /api/living/proactive`
**Purpose:** Get proactive messages from Najika
**Response:**
```json
{
  "message": "Mr.K, ich habe heute etwas Neues gelernt!",
  "emotion": "excited",
  "trigger": "learning_event"
}
```

#### 12. `GET /api/living/activity/check`
**Purpose:** Check current activity status
**Response:**
```json
{
  "activity": "training",
  "progress": 75,
  "time_remaining": 300
}
```

---

### **Security:**

#### 13. `GET /api/security/status`
**Purpose:** Security analysis (VPN, IP, recommendations)
**Response:**
```json
{
  "vpn_active": true,
  "ip_address": "127.0.0.1",
  "security_level": "high",
  "recommendations": []
}
```

#### 14. `GET /api/security/vpn`
**Purpose:** VPN status check
**Response:**
```json
{
  "vpn_active": true,
  "vpn_provider": "Mullvad",
  "ip_leak": false
}
```

---

### **Cloud:**

#### 15. `GET /api/cloud/status`
**Purpose:** Cloud status
**Response:**
```json
{
  "cloud_enabled": false,
  "provider": null,
  "last_sync": null
}
```

---

### **Cache:**

#### 16. `GET /api/cache/stats`
**Purpose:** Cache statistics
**Response:**
```json
{
  "hit_rate": 85,
  "cache_size_mb": 120,
  "total_requests": 1000,
  "cache_hits": 850
}
```

---

### **Training:**

#### 17. `GET /api/training/status`
**Purpose:** LoRA training status
**Response:**
```json
{
  "training_active": false,
  "current_epoch": 0,
  "total_epochs": 3,
  "loss": 0.0
}
```

#### 18. `GET /api/training/history`
**Purpose:** Training history
**Response:**
```json
{
  "history": [
    {
      "timestamp": "2025-11-10T10:00:00Z",
      "model": "qwen2.5-7b",
      "success": true,
      "duration_sec": 1200
    }
  ]
}
```

---

### **Save:**

#### 19. `GET /api/save`
**Purpose:** Save current state to disk
**Response:**
```json
{
  "saved": true,
  "timestamp": "2025-11-11T12:00:00Z",
  "file": "saves/najika_state.json"
}
```

---

## POST ENDPOINTS (37 Total)

### **Chat:**

#### 1. `POST /api/chat`
**Purpose:** Chat with Najika
**Request:**
```json
{
  "message": "Hello Najika!",
  "mode": "normal"
}
```
**Response:**
```json
{
  "response": "Hi Mr.K! 💜 What can I do for you?",
  "emotion": "happy",
  "timestamp": "2025-11-11T12:00:00Z"
}
```

---

### **Cloud:**

#### 2. `POST /api/cloud/enable`
**Purpose:** Enable cloud with PIN
**Request:**
```json
{
  "pin": "1234"
}
```
**Response:**
```json
{
  "enabled": true,
  "provider": "claude"
}
```

#### 3. `POST /api/cloud/disable`
**Purpose:** Disable cloud
**Response:**
```json
{
  "disabled": true
}
```

---

### **Room Actions:**

#### 4. `POST /api/room/actions`
**Purpose:** Room interactions (E-key press)
**Request:**
```json
{
  "room": "schwarze_muehle_entrance",
  "action": "interact"
}
```
**Response:**
```json
{
  "result": "Door opened",
  "new_state": "door_open"
}
```

---

### **Battle System:**

#### 5. `POST /api/battle/start`
**Purpose:** Start battle
**Request:**
```json
{
  "enemy_type": "goblin",
  "wave": 1
}
```
**Response:**
```json
{
  "battle_id": "battle_001",
  "enemy": {
    "name": "Goblin",
    "hp": 50,
    "level": 1
  }
}
```

#### 6. `POST /api/battle/status`
**Purpose:** Get battle status
**Response:**
```json
{
  "battle_active": true,
  "player_hp": 100,
  "enemy_hp": 25,
  "turn": "player"
}
```

#### 7. `POST /api/battle/action`
**Purpose:** Perform battle action
**Request:**
```json
{
  "action": "attack",
  "target": "enemy_001",
  "skill_id": null
}
```
**Response:**
```json
{
  "result": "hit",
  "damage": 15,
  "enemy_hp": 10,
  "turn": "enemy"
}
```

#### 8. `POST /api/battle/skills`
**Purpose:** Get available skills
**Response:**
```json
{
  "skills": [
    {
      "id": "fireball",
      "name": "Fireball",
      "mp_cost": 10,
      "damage": 30
    }
  ]
}
```

#### 9. `POST /api/battle/reset`
**Purpose:** Reset battle state
**Response:**
```json
{
  "reset": true
}
```

---

### **TTS:**

#### 10. `POST /api/tts`
**Purpose:** Generate TTS audio (Megumin voice)
**Request:**
```json
{
  "text": "EXPLOSION!",
  "emotion": "excited"
}
```
**Response:**
```json
{
  "audio_base64": "...",
  "duration_sec": 2.5,
  "format": "wav"
}
```

---

### **Training:**

#### 11. `POST /api/training/start`
**Purpose:** Start LoRA training
**Request:**
```json
{
  "model": "qwen2.5-7b",
  "dataset": "code_problems",
  "epochs": 3
}
```
**Response:**
```json
{
  "training_started": true,
  "estimated_duration_min": 20
}
```

---

### **Minigames:**

#### 12. `POST /api/minigame/rhythm`
**Purpose:** Submit rhythm game score
**Request:**
```json
{
  "score": 950,
  "accuracy": 95,
  "combo": 50
}
```
**Response:**
```json
{
  "reward_xp": 100,
  "new_high_score": true
}
```

#### 13. `POST /api/minigame/garden`
**Purpose:** Garden game action
**Request:**
```json
{
  "action": "water",
  "plant_id": "plant_001"
}
```
**Response:**
```json
{
  "plant_health": 100,
  "growth_stage": 2
}
```

#### 14. `POST /api/minigame/reflex`
**Purpose:** Submit reflex game score
**Request:**
```json
{
  "reaction_time_ms": 250,
  "targets_hit": 10
}
```
**Response:**
```json
{
  "reward_xp": 50
}
```

---

### **Crafting & Healing:**

#### 15. `POST /api/crafting`
**Purpose:** Craft items
**Request:**
```json
{
  "recipe": "health_potion",
  "quantity": 1
}
```
**Response:**
```json
{
  "item": "health_potion",
  "added_to_inventory": true
}
```

#### 16. `POST /api/heal`
**Purpose:** Heal player
**Request:**
```json
{
  "item_id": "health_potion"
}
```
**Response:**
```json
{
  "hp_restored": 50,
  "current_hp": 100
}
```

---

### **Events:**

#### 17. `POST /api/event/next`
**Purpose:** Trigger next event (Oregon Trail style)
**Response:**
```json
{
  "event": {
    "type": "encounter",
    "description": "You encounter a wild boar!",
    "choices": ["fight", "run"]
  }
}
```

---

### **User & Progress:**

#### 18. `POST /api/user/update`
**Purpose:** Update user data
**Request:**
```json
{
  "level": 2,
  "xp": 150,
  "points": 10,
  "inventory": ["sword", "shield"],
  "achievements": ["first_battle"]
}
```
**Response:**
```json
{
  "updated": true
}
```

#### 19. `POST /api/progress/update`
**Purpose:** Update progress
**Request:**
```json
{
  "dungeon_level": 5,
  "quests_completed": ["quest_001"]
}
```
**Response:**
```json
{
  "updated": true
}
```

---

### **Najika Care (Digimon World-Style!):**

#### 20. `POST /api/najika/feed`
**Purpose:** Feed Najika 🍖
**Request:**
```json
{
  "item": "steak"
}
```
**Response:**
```json
{
  "hunger": 100,
  "happiness": 85,
  "message": "Mmm, delicious! Thank you Mr.K! 💜"
}
```

#### 21. `POST /api/najika/drink`
**Purpose:** Give Najika water 💧
**Request:**
```json
{
  "item": "water"
}
```
**Response:**
```json
{
  "thirst": 100,
  "message": "Refreshing!"
}
```

#### 22. `POST /api/najika/wash`
**Purpose:** Wash Najika 🚿
**Response:**
```json
{
  "hygiene": 100,
  "happiness": 90,
  "message": "I'm clean now! ✨"
}
```

#### 23. `POST /api/najika/sleep`
**Purpose:** Let Najika sleep 😴
**Response:**
```json
{
  "energy": 100,
  "fatigue": 0,
  "message": "*yawn* I feel refreshed!"
}
```

#### 24. `POST /api/najika/train`
**Purpose:** Train Najika 💪
**Request:**
```json
{
  "stat": "strength",
  "duration_min": 30
}
```
**Response:**
```json
{
  "strength": 15,
  "xp_gained": 50,
  "message": "I'm getting stronger!"
}
```

---

### **Equipment:**

#### 25. `POST /api/najika/equip`
**Purpose:** Equip item
**Request:**
```json
{
  "slot": "weapon",
  "item_id": "explosion_staff"
}
```
**Response:**
```json
{
  "equipped": true,
  "stats_bonus": {
    "intelligence": +10
  }
}
```

#### 26. `POST /api/najika/unequip`
**Purpose:** Unequip item
**Request:**
```json
{
  "slot": "weapon"
}
```
**Response:**
```json
{
  "unequipped": true
}
```

#### 27. `POST /api/najika/equipment`
**Purpose:** Get equipment status
**Response:**
```json
{
  "weapon": "explosion_staff",
  "armor": "crimson_robe",
  "accessory": "eyepatch"
}
```

---

### **Praise/Scold System:**

#### 28. `POST /api/najika/praise`
**Purpose:** Praise Najika 👍
**Request:**
```json
{
  "reason": "good_job"
}
```
**Response:**
```json
{
  "happiness": 95,
  "discipline": 5,
  "message": "Thank you Mr.K! 💜💜💜"
}
```

#### 29. `POST /api/najika/scold`
**Purpose:** Scold Najika 👎
**Request:**
```json
{
  "reason": "misbehavior"
}
```
**Response:**
```json
{
  "happiness": 70,
  "discipline": 10,
  "message": "I'm sorry... I'll do better."
}
```

---

### **Code Execution:**

#### 30. `POST /api/code/execute`
**Purpose:** Execute code
**Request:**
```json
{
  "language": "python",
  "code": "print('Hello World')"
}
```
**Response:**
```json
{
  "output": "Hello World\n",
  "error": null,
  "execution_time_ms": 50
}
```

---

### **File Operations:**

#### 31. `POST /api/file/read`
**Purpose:** Read file
**Request:**
```json
{
  "path": "/home/user/test.txt"
}
```
**Response:**
```json
{
  "content": "File content here",
  "size_bytes": 1024
}
```

#### 32. `POST /api/file/write`
**Purpose:** Write file
**Request:**
```json
{
  "path": "/home/user/test.txt",
  "content": "New content"
}
```
**Response:**
```json
{
  "written": true,
  "size_bytes": 11
}
```

#### 33. `POST /api/file/list`
**Purpose:** List files
**Request:**
```json
{
  "path": "/home/user/"
}
```
**Response:**
```json
{
  "files": ["test.txt", "image.png"],
  "total": 2
}
```

---

### **System:**

#### 34. `POST /api/system/command`
**Purpose:** Execute system command
**Request:**
```json
{
  "command": "ls -la"
}
```
**Response:**
```json
{
  "output": "...",
  "exit_code": 0
}
```

---

### **Memory:**

#### 35. `POST /api/memory/import`
**Purpose:** Import memory data
**Request:**
```json
{
  "memories": [
    {
      "text": "Mr.K loves explosions",
      "metadata": {
        "importance": 10
      }
    }
  ]
}
```
**Response:**
```json
{
  "imported": 1,
  "total_memories": 150
}
```

---

### **Living System:**

#### 36. `POST /api/living/activity/start`
**Purpose:** Start activity
**Request:**
```json
{
  "activity": "training",
  "duration_min": 30
}
```
**Response:**
```json
{
  "activity_started": true,
  "estimated_completion": "2025-11-11T12:30:00Z"
}
```

---

## 💾 STATE STRUCTURE (najika_state.json)

```json
{
  "user": {
    "level": 1,
    "xp": 0,
    "points": 0,
    "inventory": [],
    "achievements": []
  },
  "progress": {
    "dungeon_level": 0,
    "quests_completed": []
  },
  "battle": {
    "hp": 100,
    "wave": 0,
    "enemies": 0
  },
  "najika": {
    "needs": {
      "hunger": 100,
      "thirst": 100,
      "energy": 100,
      "hygiene": 100,
      "happiness": 100
    },
    "stats": {
      "strength": 10,
      "intelligence": 10,
      "dexterity": 10,
      "charisma": 10
    },
    "care": {
      "care_mistakes": 0,
      "fatigue": 0,
      "weight": 50,
      "discipline": 0
    },
    "growth": {
      "level": 1,
      "xp": 0,
      "evolution_stage": "base"
    },
    "equipment": {
      "weapon": null,
      "armor": null,
      "accessory": null
    }
  },
  "history": []
}
```

---

## 🎮 DATA FLOW

### **1. User sends Chat Message:**
```
User (Browser)
  → POST /api/chat {"message": "Hello"}
  → najika_server.py (Flask)
  → najika_memory_enhanced.py (ChromaDB context retrieval)
  → AI Layer (Claude Code → Ollama → Cloud)
  → najika_enhanced_personality.py (personality blend)
  → najika_living_system.py (mood update)
  → Response generated
  → najika_tts_coqui.py (Megumin voice TTS)
  → Audio + Text sent back to User
```

### **2. User starts Voice Call:**
```
User (Browser - Microphone)
  → WebRTC Audio Stream
  → POST /api/voice_call/audio {audio_base64}
  → najika_voice_call.py
  → Whisper STT (speech to text)
  → najika_server.py → AI Layer
  → Response text generated
  → najika_tts_coqui.py (Megumin voice)
  → Audio Base64 response
  → Browser plays audio
```

### **3. User feeds Najika:**
```
User (Browser)
  → POST /api/najika/feed {"item": "steak"}
  → najika_server.py
  → najika_living_system.py (update hunger)
  → najika_state.json updated
  → Response: {"hunger": 100, "message": "..."}
  → Browser updates UI
```

### **4. User starts Battle:**
```
User (Browser)
  → POST /api/battle/start {"enemy_type": "goblin"}
  → najika_server.py
  → najika_battle.py (initialize battle)
  → Enemy spawned from ENEMY_DB
  → Battle state created
  → Response: {"battle_id": "...", "enemy": {...}}
  → Browser shows battle UI
```

---

## 🧠 MEMORY SYSTEM (ChromaDB)

### **Collections:**
```
1. KERN (Core Personality)
   - Najika's fundamental personality traits
   - Based on Megumin, Harley Quinn, Shiro, Melissa

2. Video Transcripts
   - KonoSuba episodes
   - Character dialogue
   - Scene descriptions

3. Conversation History
   - All interactions with Mr.K
   - Context-aware retrieval
   - Semantic search

4. Emotional Memories
   - Important moments
   - High-emotion events
   - Relationship milestones
```

### **Retrieval:**
```python
# Example query:
query = "What do you remember about explosions?"

# ChromaDB semantic search:
results = memory.query(
    query_texts=[query],
    n_results=5,
    where={"importance": {"$gte": 5}}
)

# Results used as context for AI response
```

---

## 🎭 PERSONALITY SYSTEM

### **Normal Mode (Default):**
```
Megumin:      35% - Explosion magic obsessed, dramatic, confident
Harley Quinn: 25% - Playful, calls user "Mr.K", loyal but chaotic
Shiro:        20% - Gaming genius, analytical, strategic
Melissa:      20% - Kuudere/Tsundere mix, protective, caring
```

### **Kätzchen Mode (Private Mode):**
```
Melissa:      50% DOMINANT! - Intimate, protective, possessive
Shiro:        30% - Strategic, calculating
Megumin:      15% - Reduced but still present
Harley Quinn:  5% - Minimal influence

ACTIVATED BY: User types "kätzchen" command
BEHAVIOR: More intimate, NSFW allowed (local only!), protective
```

### **Dynamic Balancing:**
The personality ratios adjust based on:
- Conversation context
- User mood
- Time of day
- Relationship level
- Current activity

---

## 🔐 SECURITY (ALCATRAZ - Die 8 Gebote)

### **1. Zero-Trust Architecture:**
```
✅ Server binds to 127.0.0.1 ONLY (localhost)
✅ No external network access
✅ All requests must come from localhost
```

### **2. Owner-Token Authentication:**
```
✅ Owner token generated on first run
✅ Stored securely (not in code)
✅ Required for sensitive operations
```

### **3. VPN Status Check:**
```
✅ Checks if VPN is active
✅ Warns if VPN disconnected
✅ Can block operations if no VPN
```

### **4. Privacy-First Design:**
```
✅ No telemetry
✅ No analytics
✅ No external tracking
✅ All data stays local
```

### **5. Offline-Capable:**
```
✅ Works without internet
✅ Ollama runs locally
✅ ChromaDB is local
✅ Voice processing local
```

### **6. NSFW Local Only:**
```
✅ Kätzchen Mode (private mode) is local only
✅ No cloud sync for private content
✅ Explicit content stays on device
```

### **7. Encrypted Storage:**
```
✅ Sensitive data encrypted at rest
✅ State file protected
✅ Memory database secured
```

### **8. Auditable:**
```
✅ All operations logged
✅ Security events tracked
✅ Transparent behavior
```

---

## 🎮 CURRENT FEATURES (Complete List)

### **CORE FEATURES:**
```
✅ Voice Calls (Whisper STT + Coqui TTS Megumin Voice)
✅ Text Chat (Ollama/Claude/Cloud with PIN)
✅ 3D World Navigation (2400×2400 open world)
✅ Tamagotchi System (Digimon World-style care)
✅ Training System (LoRA training for AI)
✅ Battle System (Turn-based combat)
✅ Living System (Proactive messages, autonomous activities)
✅ Memory System (ChromaDB long-term memory)
✅ Security System (Alcatraz - 8 Gebote)
```

### **WORLD FEATURES:**
```
✅ Die Schwarze Mühle (7 rooms - mini open world)
✅ 3 Dungeons (procedurally generated)
✅ River, Forest, Village
✅ KayKit 3D assets (~25GB local)
✅ Custom buildings
✅ Interior rooms
```

### **GAMEPLAY FEATURES:**
```
✅ Fishing System (Zelda OoT-style)
✅ Garden System (Farming/planting)
✅ Minigames (3 types: Rhythm, Reflex, Garden)
✅ Dungeon Crawling (multi-floor, procedural)
✅ Enemy AI (pathfinding, combat)
✅ Loot System
✅ Crafting System
✅ Item System
✅ XP/Level System
✅ Achievement System
```

### **UI/UX FEATURES:**
```
✅ Chat Interface (Markdown rendering, TTS playback)
✅ Voice Call UI (WebRTC integration)
✅ Battle UI (Turn-based, skills, HP/MP bars)
✅ Tamagotchi UI (Needs bars, stats)
✅ Touch Controls (Virtual joystick, mobile-optimized)
✅ PWA Support (Offline capability)
✅ Code Editor (Inline editing, syntax highlighting)
✅ Terminal (CLI interface)
✅ Command System (Slash commands)
```

### **CAMERA MODES:**
```
✅ Orbit Mode (Free rotation around Najika)
✅ Third-Person (Fortnite-style over-the-shoulder)
✅ First-Person (Ego perspective)
✅ Touch/Mouse Controls
✅ Smooth transitions
```

### **SPECIAL MODES:**
```
✅ Kätzchen Mode (Private mode - Melissa 50% dominant!)
✅ Cloud Mode (With PIN - opt-in)
✅ Training Mode (LoRA training active)
```

---

## 🔧 DEPENDENCIES

### **Backend (Python):**
```
Flask - Web server
Flask-SocketIO - WebSocket support
Whisper - Speech-to-text
Coqui TTS - Text-to-speech (Megumin voice)
ChromaDB - Vector database
Ollama - Local LLM (Llama 3.1 8B)
NumPy - Numerical operations
SoundFile - Audio processing
Requests - HTTP client
```

### **Frontend (JavaScript):**
```
Three.js r128 - 3D rendering
Cannon.js - Physics engine
GLTFLoader - 3D model loading
Markdown-it - Markdown rendering
Prism.js - Syntax highlighting (code editor)
```

### **System Requirements:**
```
Python: 3.10+
Node.js: 16+ (for frontend dev)
Ollama: Latest (for Llama 3.1 8B)
Disk Space: ~30GB (KayKit assets + models)
RAM: 8GB minimum (16GB recommended)
GPU: NVIDIA GPU recommended (for Whisper + TTS)
```

---

## ⚡ PERFORMANCE METRICS (Current)

### **Backend:**
```
Average Response Time: 200-500ms
Voice Call Latency: 300-800ms
  - Whisper STT: 150-400ms
  - AI Response: 100-300ms
  - Coqui TTS: 50-100ms

Memory Usage: 2-4GB (with Ollama loaded)
CPU Usage: 20-40% (idle), 80-100% (during voice call)
```

### **Frontend:**
```
FPS (Desktop): 60 FPS (stable)
FPS (Mobile): 30-45 FPS (varies by device)
Initial Load Time: 5-10 seconds
Memory Usage (Browser): 200-500MB
```

---

## 🎯 MIGRATION TARGETS (For UE5)

### **What MUST be maintained:**
```
✅ All API endpoints (56 total)
✅ Backend functionality (Python server)
✅ Voice call system (Whisper + Coqui)
✅ Memory system (ChromaDB)
✅ Personality system (4-way blend)
✅ Tamagotchi system (needs, stats)
✅ Battle system (turn-based)
✅ Living system (proactive messages)
✅ Security system (Alcatraz)
```

### **What will be IMPROVED:**
```
🔥 Graphics: Three.js → UE5 Nanite/Lumen
🔥 Physics: Cannon.js → Chaos Physics
🔥 Animations: JS → Animation Blueprints
🔥 Camera: JS → UE5 Camera System
🔥 UI: HTML/CSS → UMG Widgets
🔥 Performance: 30-45 FPS → 60 FPS stable
🔥 Mobile: WebView → Native Android APK
```

### **What will be ADDED:**
```
🆕 Biometric Authentication (Android Keystore)
🆕 Encrypted Storage (Android EncryptedSharedPreferences)
🆕 Hardware-accelerated Graphics (Vulkan/OpenGL ES)
🆕 Professional Lighting (Lumen Mobile)
🆕 Particle Systems (Niagara)
🆕 UEFN-ready Architecture (for Fortnite port)
🆕 Adaptive Performance (thermal/battery management)
```

---

## 📊 SUMMARY

**Total Lines of Code:**
```
Backend:  ~30,000+ lines (Python)
Frontend: ~15,000+ lines (JavaScript + HTML)
Total:    ~45,000+ lines
```

**Total Features:**
```
API Endpoints:    56 (19 GET, 37 POST)
JS Modules:       17
Python Modules:   ~40
3D Assets:        ~25GB (KayKit)
Najika Models:    VRM format
```

**Current Status:**
```
✅ Fully functional WebView-based Digivice
✅ All features working
✅ Voice calls operational
✅ Battle system complete
✅ Tamagotchi system complete
✅ Memory system operational
✅ Security implemented
✅ Ready for UE5 migration!
```

---

## 🔄 NEXT STEPS (Phase 1)

1. ✅ **Phase 0 Complete:** System analyzed and documented
2. ⏳ **Phase 1:** Setup UE5.6 project
3. ⏳ **Phase 2:** Implement core systems (Character, World, Camera)
4. ⏳ **Phase 3:** Backend integration (HTTP client plugin)
5. ⏳ **Phase 4:** Gameplay systems (Tamagotchi, Battle, Minigames)
6. ⏳ **Phase 5:** UI/UX polish
7. ⏳ **Phase 6:** Security & optimization
8. ⏳ **Phase 7:** Packaging & deployment
9. ⏳ **Phase 8:** Iterative improvements
10. ⏳ **Phase 9:** UEFN preparation

---

**END OF ARCHITECTURE DOCUMENTATION**
**Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** Phase 0 Complete - Ready for UE5 Migration!

**🔥 Najika is ready to migrate to Unreal Engine 5! 🔥**
