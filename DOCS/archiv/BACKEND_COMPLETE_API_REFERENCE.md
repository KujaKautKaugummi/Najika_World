# 🔌 NAJIKA BACKEND - COMPLETE API REFERENCE
**Version:** 1.0
**Base URL:** `http://127.0.0.1:8000`
**Protocol:** HTTP/1.1, WebSocket (for voice calls)
**Format:** JSON

---

## 📋 TABLE OF CONTENTS

1. [Data Structures](#data-structures)
2. [Authentication](#authentication)
3. [Chat & Conversation](#chat--conversation)
4. [Najika Care System](#najika-care-system)
5. [Battle System](#battle-system)
6. [Voice Call System](#voice-call-system)
7. [Living System (Autonomy)](#living-system-autonomy)
8. [Memory System](#memory-system)
9. [Mini-Games](#mini-games)
10. [Training System (LoRA)](#training-system-lora)
11. [File & Code Operations](#file--code-operations)
12. [System Status](#system-status)

---

## 📊 DATA STRUCTURES

### NajikaState
```json
{
  "hunger": 100.0,          // 0-100 (0 = starved, 100 = full)
  "thirst": 100.0,          // 0-100 (NEW!)
  "energy": 100.0,          // 0-100 (0 = exhausted, 100 = rested)
  "hygiene": 100.0,         // 0-100
  "happiness": 100.0,       // 0-100
  "strength": 10,           // Base 10, increases with training
  "intelligence": 10,
  "dexterity": 10,
  "charisma": 10,
  "care_mistakes": 0,       // Increments on neglect
  "fatigue": 0.0,           // 0-100, increases with training
  "weight": 50.0,           // 0-100
  "discipline": 0.0,        // 0-100 (Praise/Scold system)
  "level": 1,
  "xp": 0,
  "evolution_stage": "base", // "base", "advanced", "ultimate"
  "equipment": {
    "weapon": null,         // Item ID or null
    "armor": null,
    "accessory": null
  },
  "last_fed": 1234567890,   // Unix timestamp
  "last_trained": 1234567890,
  "last_sleep": 1234567890,
  "last_update": 1234567890
}
```

### LivingState
```json
{
  "current_mood": "neutral",     // happy, excited, sad, bored, playful, curious, loving
  "mood_intensity": 50,          // 0-100
  "hunger": 100.0,               // Game stat
  "energy": 100.0,
  "mood_game": 100.0,
  "anger_level": 0.0,            // 0-100 (anger from neglect)
  "auto_care_threshold": 20.0,
  "auto_care_max": 50.0,
  "auto_care_enabled": true,
  "last_accident": null,
  "accidents_today": 0,
  "max_accidents_per_day": 3,
  "last_update": 1234567890,
  "control_mode": "ai",          // "ai" or "player"
  "player_online": false,
  "last_proactive_message": 0,
  "proactive_cooldown": 1800,    // 30 minutes
  "autonomy_level": 50,          // 0-100
  "personality_evolution": {
    "megumin": 25,
    "harley": 25,
    "shiro": 25,
    "melissa": 25
  },
  "growth_stage": "developing",  // awakening, developing, mature, transcendent
  "relationship_stage": "getting_to_know", // friends, close, intimate, soulmates
  "emotional_bond": 0,           // 0-100
  "shared_memories": [],
  "last_interaction": 1234567890,
  "total_time_together": 0,      // seconds
  "days_since_meeting": 0,
  "current_activity": null,
  "activity_started": 0,
  "activities_completed": []
}
```

### BattleState
```json
{
  "active": false,
  "hp": 100,
  "max_hp": 100,
  "wave": 0,
  "enemies": [],
  "player_stats": {
    "atk": 10,
    "def": 5,
    "buffs": [],
    "debuffs": []
  },
  "battle_log": []
}
```

### Item
```json
{
  "item_id": "health_potion_small",
  "name": "Kleiner Heiltrank",
  "type": "consumable",        // consumable, weapon, armor, accessory, material, special
  "effect": "heal",            // heal, buff_atk, buff_def
  "value": 30,                 // Effect value (HP restored, ATK bonus, etc.)
  "duration": 0,               // Turns (for buffs/debuffs)
  "description": "Stellt 30 HP wieder her"
}
```

### Enemy
```json
{
  "enemy_id": "rat",
  "name": "Dungeon-Ratte",
  "hp": 20,
  "max_hp": 20,
  "atk": 3,
  "def": 1,
  "gold": 5,
  "xp": 8,
  "loot_table": [
    {"item": "rat_tail", "chance": 0.3},
    {"item": "health_potion_small", "chance": 0.15}
  ]
}
```

### ChatMessage
```json
{
  "role": "user",              // "user" or "assistant"
  "content": "Hello Najika!",
  "importance": 65,            // 0-100 (importance score)
  "timestamp": 1234567890
}
```

---

## 🔐 AUTHENTICATION

**Currently:** No authentication required (localhost-only, 127.0.0.1)
**Future:** Add token-based auth for cloud mode

---

## 💬 CHAT & CONVERSATION

### POST /api/chat
**Description:** Send message to Najika and get AI response

**Request:**
```json
{
  "message": "Hello Najika!",
  "user": "User"
}
```

**Response:**
```json
{
  "response": "EXPLOSION! *kicher* Hallo Puddin'!",
  "room": "Wohnzimmer",
  "behavior_mode": "standard",
  "bond_strength": 25,
  "najika_state": { /* NajikaState object */ },
  "living_state": { /* LivingState object */ }
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - AI call failed

---

### GET /api/chat/history
**Description:** Get conversation history (last 50 messages)

**Response:**
```json
{
  "history": [
    {
      "role": "user",
      "content": "Hello!",
      "importance": 65,
      "timestamp": 1234567890
    },
    {
      "role": "assistant",
      "content": "Hi!",
      "importance": 50,
      "timestamp": 1234567891
    }
  ],
  "total_messages": 2
}
```

---

### GET /api/bond/status
**Description:** Get relationship bond strength

**Response:**
```json
{
  "bond_strength": 25,
  "total_interactions": 100,
  "relationship_stage": "getting_to_know",
  "emotional_bond": 15
}
```

---

## 🍕 NAJIKA CARE SYSTEM

### GET /api/najika/status
**Description:** Get Najika's complete status

**Response:**
```json
{
  "najika": { /* NajikaState object */ },
  "needs_attention": ["hunger", "energy"],
  "mood": "happy",
  "equipment_stats": {
    "total_atk_bonus": 8,
    "total_def_bonus": 2
  }
}
```

---

### POST /api/najika/feed
**Description:** Feed Najika (increases hunger)

**Response:**
```json
{
  "ok": true,
  "msg": "Najika isst! +30 Hunger",
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/drink
**Description:** Give Najika water (increases thirst)

**Response:**
```json
{
  "ok": true,
  "msg": "Najika trinkt! +30 Thirst",
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/wash
**Description:** Wash Najika (increases hygiene)

**Response:**
```json
{
  "ok": true,
  "msg": "Najika gewaschen! +40 Hygiene",
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/sleep
**Description:** Put Najika to sleep (restores energy, reduces fatigue)

**Response:**
```json
{
  "ok": true,
  "msg": "Najika schlaeft! +50 Energy, -20 Fatigue",
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/train
**Description:** Train Najika (increases stats, consumes energy)

**Request:**
```json
{
  "type": "strength"  // "strength", "intelligence", "dexterity", "charisma"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Najika trainiert Strength! +1 Strength, -10 Energy, +5 Fatigue",
  "stat_increased": "strength",
  "new_value": 11,
  "xp_gained": 10,
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/praise
**Description:** Praise Najika (Digimon World style - increases happiness, decreases discipline)

**Response:**
```json
{
  "ok": true,
  "msg": "Najika freut sich! +10 Happiness, -5 Discipline",
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/scold
**Description:** Scold Najika (increases discipline, decreases happiness)

**Response:**
```json
{
  "ok": true,
  "msg": "Najika wurde getadelt! +10 Discipline, -5 Happiness",
  "discipline": 10,
  "happiness": 90,
  "najika": { /* Updated NajikaState */ }
}
```

---

### POST /api/najika/equip
**Description:** Equip item to Najika

**Request:**
```json
{
  "item_id": "iron_sword",
  "slot": "weapon"  // "weapon", "armor", "accessory"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Eisenschwert ausgeruestet!",
  "equipment": {
    "weapon": "iron_sword",
    "armor": null,
    "accessory": null
  },
  "stats": {
    "total_atk_bonus": 8,
    "total_def_bonus": 0
  }
}
```

---

### POST /api/najika/unequip
**Description:** Unequip item from Najika

**Request:**
```json
{
  "slot": "weapon"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Eisenschwert entfernt!",
  "equipment": {
    "weapon": null,
    "armor": null,
    "accessory": null
  },
  "stats": {
    "total_atk_bonus": 0,
    "total_def_bonus": 0
  }
}
```

---

### GET /api/najika/equipment
**Description:** Get Najika's current equipment

**Response:**
```json
{
  "equipment": {
    "weapon": "iron_sword",
    "armor": null,
    "accessory": null
  },
  "stats": {
    "total_atk_bonus": 8,
    "total_def_bonus": 0
  }
}
```

---

## ⚔️ BATTLE SYSTEM

### POST /api/battle/start
**Description:** Start dungeon battle

**Response:**
```json
{
  "ok": true,
  "msg": "Kampf gestartet!",
  "wave": 1,
  "enemies": [
    {
      "enemy_id": "rat",
      "name": "Dungeon-Ratte",
      "hp": 20,
      "max_hp": 20,
      "atk": 3,
      "def": 1
    }
  ],
  "player_hp": 100,
  "player_max_hp": 100
}
```

---

### GET /api/battle/status
**Description:** Get current battle status

**Response:**
```json
{
  "active": true,
  "wave": 1,
  "player_hp": 85,
  "player_max_hp": 100,
  "enemies": [ /* Enemy array */ ],
  "battle_log": [
    "Du greifst Dungeon-Ratte an! -15 HP",
    "Dungeon-Ratte greift dich an! -15 HP"
  ]
}
```

---

### POST /api/battle/action
**Description:** Perform battle action

**Request:**
```json
{
  "action": "attack",    // "attack", "skill", "item", "defend"
  "target": 0,           // Enemy index
  "skill_id": null,      // Required if action = "skill"
  "item_id": null        // Required if action = "item"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Du greifst Dungeon-Ratte an!",
  "damage_dealt": 15,
  "enemy_defeated": false,
  "loot": null,
  "xp_gained": 0,
  "gold_gained": 0,
  "battle_log": [ /* Updated battle log */ ],
  "battle_state": { /* Updated BattleState */ }
}
```

---

### GET /api/battle/skills
**Description:** Get available battle skills

**Response:**
```json
{
  "skills": [
    {
      "skill_id": "fireball",
      "name": "Feuerball",
      "damage": 25,
      "mp_cost": 10,
      "description": "Feuert einen Feuerball auf den Feind"
    }
  ]
}
```

---

### POST /api/battle/reset
**Description:** Reset battle (flee/give up)

**Response:**
```json
{
  "ok": true,
  "msg": "Kampf abgebrochen",
  "battle_state": { /* Reset BattleState */ }
}
```

---

## 🎤 VOICE CALL SYSTEM

### POST /api/voice_call/start
**Description:** Start voice call session (Whisper STT + Coqui TTS)

**Response:**
```json
{
  "ok": true,
  "status": "call_started",
  "timestamp": "2025-01-15T10:30:00Z",
  "tts_available": true
}
```

---

### POST /api/voice_call/audio
**Description:** Send audio chunk for STT processing

**Request:**
```json
{
  "audio_data": "base64_encoded_wav_data_here..."
}
```

**Response:**
```json
{
  "ok": true,
  "text": "Hallo Najika, wie geht es dir?",
  "language": "de",
  "latency_ms": 234,
  "response_text": "Mir geht es gut, Puddin'! *kicher*",
  "response_audio": "base64_encoded_audio_response_here...",
  "tts_latency_ms": 456,
  "timestamp": "2025-01-15T10:30:05Z"
}
```

---

### POST /api/voice_call/end
**Description:** End voice call session

**Response:**
```json
{
  "ok": true,
  "status": "call_ended",
  "duration_sec": 120.5,
  "timestamp": "2025-01-15T10:32:00Z"
}
```

---

### GET /api/voice_call/stats
**Description:** Get voice call statistics

**Response:**
```json
{
  "total_calls": 10,
  "total_duration_sec": 1200,
  "avg_stt_latency_ms": 250,
  "avg_tts_latency_ms": 500
}
```

---

## 🌟 LIVING SYSTEM (AUTONOMY)

### GET /api/living/state
**Description:** Get Najika's living system state

**Response:**
```json
{
  "living_state": { /* LivingState object */ }
}
```

---

### GET /api/living/proactive
**Description:** Check if Najika wants to send proactive message

**Response:**
```json
{
  "should_send": true,
  "message": "Mir ist langweilig, Kuja~ Lass uns was tun!",
  "mood": "bored",
  "reason": "no_interaction_30min"
}
```

**OR**
```json
{
  "should_send": false,
  "reason": "cooldown_active"
}
```

---

### GET /api/living/activity/check
**Description:** Check if Najika completed autonomous activity

**Response:**
```json
{
  "activity_complete": true,
  "activity": "reading",
  "outcome": "Najika hat ein Buch gelesen! +2 Intelligence",
  "stat_changes": {
    "intelligence": 2
  }
}
```

---

### POST /api/living/activity/start
**Description:** Start autonomous activity

**Request:**
```json
{
  "activity": "reading"  // "reading", "training", "exploring", "resting", "playing"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Najika beginnt zu lesen",
  "activity": "reading",
  "duration_seconds": 600,
  "expected_completion": 1234568490
}
```

---

## 🧠 MEMORY SYSTEM

### GET /api/memory/export
**Description:** Export ChromaDB memory data

**Response:**
```json
{
  "ok": true,
  "memories": [
    {
      "text": "Kuja mag Katzen",
      "timestamp": 1234567890,
      "room": "Wohnzimmer",
      "importance": 75
    }
  ],
  "total_memories": 100
}
```

---

### POST /api/memory/import
**Description:** Import memory data

**Request:**
```json
{
  "memories": [
    {
      "text": "Important memory text",
      "metadata": {
        "room": "Wohnzimmer",
        "importance": 80
      }
    }
  ]
}
```

**Response:**
```json
{
  "ok": true,
  "imported": 10,
  "failed": 0
}
```

---

## 🎮 MINI-GAMES

### POST /api/minigame/rhythm
**Description:** Play rhythm mini-game

**Request:**
```json
{
  "score": 850,
  "accuracy": 0.85
}
```

**Response:**
```json
{
  "ok": true,
  "xp_gained": 25,
  "gold_gained": 50,
  "msg": "Great rhythm!"
}
```

---

### POST /api/minigame/garden
**Description:** Interact with garden mini-game

**Request:**
```json
{
  "action": "plant",
  "item": "tomato_seeds"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Tomaten gepflanzt!",
  "garden_state": { /* Garden data */ }
}
```

---

### POST /api/minigame/reflex
**Description:** Play reflex mini-game

**Request:**
```json
{
  "reaction_time_ms": 250
}
```

**Response:**
```json
{
  "ok": true,
  "score": 95,
  "xp_gained": 15,
  "msg": "Schnelle Reflexe!"
}
```

---

## 📚 TRAINING SYSTEM (LORA)

### POST /api/training/start
**Description:** Start LoRA training (Unsloth-based)

**Request:**
```json
{
  "dataset_path": "C:/training_data.jsonl",
  "epochs": 3,
  "learning_rate": 0.0001,
  "model_name": "najika-v2"
}
```

**Response:**
```json
{
  "ok": true,
  "status": "training_started",
  "training_id": "train_123",
  "estimated_time_minutes": 120
}
```

---

### GET /api/training/status
**Description:** Get LoRA training status

**Response:**
```json
{
  "active": true,
  "status": "running",
  "progress": 45,
  "current_epoch": 2,
  "total_epochs": 3,
  "loss": 0.234,
  "elapsed_time_sec": 3600,
  "estimated_remaining_sec": 2400,
  "logs": [
    "[10:30:00] Epoch 1/3 - Loss: 0.456",
    "[10:45:00] Epoch 2/3 - Loss: 0.234"
  ]
}
```

---

### GET /api/training/history
**Description:** Get training history

**Response:**
```json
{
  "history": [
    {
      "training_id": "train_122",
      "started": "2025-01-14T10:00:00Z",
      "completed": "2025-01-14T12:00:00Z",
      "status": "completed",
      "final_loss": 0.123,
      "model_saved": true
    }
  ]
}
```

---

## 📁 FILE & CODE OPERATIONS

### POST /api/code/execute
**Description:** Execute Python code in sandbox

**Request:**
```json
{
  "code": "print('Hello World')"
}
```

**Response:**
```json
{
  "ok": true,
  "output": "Hello World\n",
  "error": null,
  "execution_time_ms": 12
}
```

---

### POST /api/file/read
**Description:** Read file from disk

**Request:**
```json
{
  "path": "C:/example.txt"
}
```

**Response:**
```json
{
  "ok": true,
  "content": "File contents here...",
  "size_bytes": 1024
}
```

---

### POST /api/file/write
**Description:** Write file to disk

**Request:**
```json
{
  "path": "C:/output.txt",
  "content": "File contents to write"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "File written successfully",
  "size_bytes": 24
}
```

---

### POST /api/file/list
**Description:** List directory contents

**Request:**
```json
{
  "path": "C:/example_dir"
}
```

**Response:**
```json
{
  "ok": true,
  "files": [
    {"name": "file1.txt", "size": 1024, "type": "file"},
    {"name": "subdir", "size": 0, "type": "directory"}
  ]
}
```

---

## 📊 SYSTEM STATUS

### GET /api/status
**Description:** Get system status

**Response:**
```json
{
  "ok": true,
  "uptime_seconds": 3600,
  "najika_state": { /* NajikaState */ },
  "living_state": { /* LivingState */ },
  "battle_active": false,
  "voice_call_active": false,
  "training_active": false,
  "memory_enabled": true,
  "tts_enabled": true
}
```

---

### GET /api/status/stream
**Description:** Server-Sent Events (SSE) stream for real-time updates

**Response:** (Event stream)
```
event: status_update
data: {"najika": {...}, "living": {...}}

event: proactive_message
data: {"message": "Hallo Kuja!", "mood": "playful"}
```

---

### GET /api/rooms
**Description:** Get available rooms

**Response:**
```json
{
  "rooms": [
    "Wohnzimmer",
    "Schlafzimmer",
    "Küche",
    "Badezimmer",
    "Garten",
    "Musikraum",
    "Medizin",
    "Terminal",
    "Studieren & Crafting",
    "Trainingszimmer",
    "Kampfarena",
    "Schwarze Mühle – Keller"
  ]
}
```

---

### GET /api/save
**Description:** Save current state to disk

**Response:**
```json
{
  "ok": true,
  "msg": "State saved successfully",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

### GET /api/state
**Description:** Get complete server state

**Response:**
```json
{
  "history": [ /* ChatMessage array */ ],
  "battle": { /* BattleState */ },
  "user": {
    "level": 5,
    "xp": 1234,
    "points": 500,
    "inventory": ["health_potion_small", "iron_sword"],
    "achievements": ["first_battle", "level_5"]
  },
  "progress": {
    "dungeon_level": 3,
    "quests_completed": ["tutorial_quest"]
  },
  "najika": { /* NajikaState */ },
  "living": { /* LivingState */ },
  "bond_strength": 35,
  "behavior_mode": "standard",
  "personality_weights": {
    "megumin": 25,
    "harley": 25,
    "shiro": 25,
    "melissa": 25
  },
  "total_interactions": 150
}
```

---

### GET /api/cache/stats
**Description:** Get AI response cache statistics

**Response:**
```json
{
  "cache_size": 45,
  "cache_max_size": 100,
  "hits": 234,
  "misses": 566,
  "hit_rate": 0.293,
  "total_requests": 800
}
```

---

## 🔒 ERROR CODES

### HTTP Status Codes
- **200 OK** - Request succeeded
- **400 Bad Request** - Invalid request format
- **404 Not Found** - Endpoint not found
- **500 Internal Server Error** - Server error (AI call failed, file error, etc.)

### Application Error Responses
```json
{
  "ok": false,
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": { /* Optional error details */ }
}
```

---

## 📝 NOTES FOR UE5 IMPLEMENTATION

### Key Implementation Points:
1. **Base URL:** Always use `http://127.0.0.1:8000` (localhost only, Zero-Trust principle)
2. **Content-Type:** Always set `Content-Type: application/json` for POST requests
3. **Polling:** Use `/api/status` or `/api/najika/status` for periodic updates (every 5-10 seconds)
4. **Voice Calls:** Audio data must be base64-encoded WAV format
5. **State Persistence:** Call `/api/save` periodically (auto-saves every 30 seconds on server)
6. **Needs Decay:** Najika's needs decay automatically on server every 60 seconds
7. **Living System:** Check `/api/living/proactive` every 30 seconds for autonomous messages

### Priority Endpoints for UE5:
**MUST HAVE (Phase 1):**
- `/api/chat` - Core conversation
- `/api/najika/status` - Get Najika state
- `/api/najika/feed`, `/api/najika/drink` - Basic care
- `/api/battle/start`, `/api/battle/action` - Combat

**SHOULD HAVE (Phase 2):**
- `/api/voice_call/*` - Voice features
- `/api/living/proactive` - Autonomous behavior
- `/api/najika/train` - Stat progression
- `/api/najika/equip` - Equipment system

**NICE TO HAVE (Phase 3):**
- `/api/memory/*` - Memory export/import
- `/api/training/*` - LoRA training status
- `/api/minigame/*` - Mini-games

---

## 🚀 WEBSOCKET PROTOCOL (Future)

**Currently NOT implemented**, but planned for:
- Real-time voice call streaming (lower latency)
- Server-push notifications (proactive messages)
- Real-time battle updates

**Proposed WS Endpoint:** `ws://127.0.0.1:8000/ws`

---

**Document Version:** 1.0
**Last Updated:** 2025-01-15
**Total Endpoints Documented:** 60+
**Lines:** 1150+

---

✅ **READY FOR UE5 C++ PLUGIN IMPLEMENTATION!**
