# NAJIKA WORLD - API DOKUMENTATION FÜR UE5

**Erstellt:** 2026-02-04
**Autor:** OPUS-1 (Backend)
**Ziel:** OPUS-2 kann diese Endpoints in UE5 via HTTP aufrufen

---

## VERBINDUNGS-INFO

```
Host: 127.0.0.1
Port: 8000
Base-URL: http://127.0.0.1:8000
Format: JSON
Auth: Bearer Token (Header: Authorization: Bearer <token>)
```

### UE5 HTTP Setup

In UE5 nutze das **HTTP-Modul** oder **VaRest Plugin**:

```cpp
// C++ Beispiel
#include "HttpModule.h"
#include "Http.h"

void ANajikaCharacter::CallChatAPI(FString Message)
{
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL("http://127.0.0.1:8000/api/chat");
    Request->SetVerb("POST");
    Request->SetHeader("Content-Type", "application/json");
    Request->SetContentAsString(FString::Printf(TEXT("{\"message\":\"%s\",\"mode\":\"public\"}"), *Message));
    Request->OnProcessRequestComplete().BindUObject(this, &ANajikaCharacter::OnChatResponse);
    Request->ProcessRequest();
}
```

---

## 🗨️ CHAT API

### POST `/api/chat`
Chat mit Najika (Haupt-Endpoint!)

**Request:**
```json
{
    "message": "Hallo Najika!",
    "mode": "public"  // "public" oder "private" (Kätzchen-Modus)
}
```

**Response:**
```json
{
    "response": "Kuja! *hüpf hüpf* EXPLOSION!!! Ich freue mich so dich zu sehen! 💥✨",
    "mode": "public",
    "emotion": "explosive",  // "excited", "sad", "angry", "tired", "happy", "explosive"
    "model_used": "najika-local"
}
```

**UE5 Nutzung:**
- Emotion → Animationen triggern (explosive = Explosion-Pose)
- Response → Text-to-Speech oder UI
- Mode → NSFW nur bei 127.0.0.1 erlaubt!

---

### POST `/api/chat/stream`
Streaming-Antwort (Token für Token)

**Request:** Gleich wie `/api/chat`

**Response:** Server-Sent Events (SSE)
```
data: {"token": "Kuja"}
data: {"token": "!"}
data: {"token": " *"}
data: {"token": "hüpf"}
data: [DONE]
```

---

### GET `/api/chat/health`
Prüfen ob Ollama läuft

**Response:**
```json
{
    "ollama_running": true,
    "models_available": ["najika-local", "najika-nsfw"]
}
```

---

## 👤 CHARACTER API

### POST `/game/character/create`
Neuen Character erstellen

**Request:**
```json
{
    "name": "Kuja",
    "species": "Mimik",
    "nickname": "Mr. K"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Kuja",
    "species": "Mimik",
    "level": 1,
    "stats": {
        "attack": 10.0,
        "defense": 5.0,
        "speed": 8.0,
        "magic": 15.0
    },
    "status": {
        "health": 100.0,
        "max_health": 100.0,
        "hunger": 50.0,
        "happiness": 75.0
    },
    "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    }
}
```

---

### GET `/game/character`
Character-Daten abrufen

**Response:** Gleich wie oben

---

### POST `/game/character/update`
Character-Position/Stats aktualisieren

**Request:**
```json
{
    "position_x": 150.5,
    "position_y": 20.0,
    "position_z": -30.0,
    "health": 85.0,
    "hunger": 40.0
}
```

**Response:**
```json
{
    "success": true,
    "message": "Character updated"
}
```

---

## ⚔️ COMBAT API

### POST `/game/combat/action`
Kampf-Aktion ausführen

**Request:**
```json
{
    "action": "attack",  // "attack", "dodge", "block", "parry", "skill"
    "enemy_id": "goblin_01",
    "skill_id": null  // Optional: für Skill-Aktionen
}
```

**Response:**
```json
{
    "success": true,
    "damage": 25,
    "player_health": 85.0,
    "enemy_health": 25.0,
    "message": "Dealt 25 damage! Took 15 damage.",
    "loot": null,
    "xp_gained": 0
}
```

**Bei Sieg (enemy_health <= 0):**
```json
{
    "success": true,
    "damage": 30,
    "player_health": 85.0,
    "enemy_health": 0.0,
    "message": "Victory! Enemy defeated.",
    "loot": [
        {"item": "health_potion_small", "quantity": 1}
    ],
    "xp_gained": 20
}
```

---

## 📦 INVENTORY API

### GET `/game/inventory`
Inventar abrufen

**Response:**
```json
{
    "items": [
        {
            "id": 1,
            "item_id": "health_potion_small",
            "name": "Kleiner Heiltrank",
            "item_type": "consumable",
            "quantity": 5,
            "is_stackable": true
        },
        {
            "id": 2,
            "item_id": "iron_sword",
            "name": "Eisenschwert",
            "item_type": "weapon",
            "quantity": 1,
            "is_stackable": false
        }
    ]
}
```

---

### POST `/game/inventory/action`
Item hinzufügen/entfernen/benutzen

**Request:**
```json
{
    "action": "add",  // "add", "remove", "use", "equip", "unequip"
    "item_id": "health_potion_small",
    "quantity": 3
}
```

**Response:**
```json
{
    "success": true,
    "message": "Added 3x health_potion_small"
}
```

---

### GET `/game/inventory/equipment`
Ausrüstung abrufen

**Response:**
```json
{
    "equipment": {
        "head": null,
        "chest": "leather_armor",
        "legs": null,
        "feet": null,
        "main_hand": "iron_sword",
        "off_hand": "wooden_shield",
        "accessory_1": null,
        "accessory_2": null
    }
}
```

---

## 💾 SAVE/LOAD API

### POST `/game/save`
Spielstand speichern

**Response:**
```json
{
    "success": true,
    "message": "Game saved successfully"
}
```

---

### POST `/game/load`
Spielstand laden

**Response:**
```json
{
    "success": true,
    "data": {
        "user_id": 1,
        "character": { ... },
        "saved_at": "2026-02-04T15:30:00"
    }
}
```

---

## 🐾 COMPANION API (Najika)

> **HINWEIS:** Diese Endpoints sind in `najika_companion_system.py` definiert aber noch nicht als Router registriert. OPUS-1 wird das erledigen.

### GET `/api/companion/najika`
Najika's aktuellen Status

**Response:**
```json
{
    "name": "Najika",
    "active_personality": "megumin",
    "personality_weights": {
        "megumin": 0.35,
        "harley": 0.25,
        "shiro": 0.20,
        "melissa": 0.20
    },
    "relationship_level": 4,
    "relationship_name": "Close Friend",
    "mood": "excited",
    "combat_style": {
        "name": "Explosion Magic",
        "type": "burst_mage",
        "damage_bonus": 1.5,
        "dodge_bonus": 0.0
    }
}
```

---

### POST `/api/companion/activity`
Gemeinsame Aktivität mit Najika

**Request:**
```json
{
    "activity": "train_explosion",  // "train_explosion", "cook", "explore", "rest", "play"
    "duration_minutes": 30
}
```

**Response:**
```json
{
    "success": true,
    "relationship_points": 15,
    "message": "*EXPLOSION!!!* Das war PERFEKT, Mr. K! 💥",
    "skill_progress": {
        "explosion_magic": 5
    }
}
```

---

### POST `/api/companion/personality/shift`
Persönlichkeits-Shift triggern

**Request:**
```json
{
    "trigger": "combat_victory"  // "combat_victory", "near_death", "romantic", "analytical_needed"
}
```

**Response:**
```json
{
    "previous": "megumin",
    "current": "harley",
    "message": "*kicher* Das war SPASSIG, Mr. K! Nochmal! 🃏"
}
```

---

## 🎭 MIMIK API (Kuja's Charakter)

> **HINWEIS:** Definiert in `najika_mimik_system.py`, Router muss noch registriert werden.

### GET `/api/mimik/status`
Kuja's Mimik-Status

**Response:**
```json
{
    "player_id": "kuja",
    "current_form": "chest",  // "chest" oder "human"
    "is_hidden": false,
    "stomach_contents": [],
    "abilities": {
        "unlocked": ["snap_bite", "mimic_hide", "treasure_lure"],
        "locked": ["human_transformation", "najika_sync"]
    },
    "najika_bond": 75
}
```

---

### POST `/api/mimik/transform`
Form wechseln

**Request:**
```json
{
    "target_form": "human"  // "chest" oder "human"
}
```

**Response:**
```json
{
    "success": true,
    "new_form": "human",
    "message": "Kuja verwandelt sich in seine Menschenform!"
}
```

---

### POST `/api/mimik/ability`
Mimik-Fähigkeit nutzen

**Request:**
```json
{
    "ability_id": "snap_bite",
    "target_id": "goblin_01"
}
```

**Response:**
```json
{
    "success": true,
    "damage": 45,
    "effect": "Goblin wurde verschlungen!",
    "cooldown": 10
}
```

---

## 🎲 MINIGAMES API

### Triple Triad
- `GET /api/card-game/deck` - Deck abrufen
- `POST /api/card-game/play` - Karte spielen
- `GET /api/card-game/rules` - Regeln abrufen

### Dungeon Dice Monsters
- `GET /api/dice-monsters/status` - Spielstatus
- `POST /api/dice-monsters/roll` - Würfeln
- `POST /api/dice-monsters/summon` - Monster beschwören

### Slime Arena
- `GET /api/slime-arena/status` - Arena-Status
- `POST /api/slime-arena/battle` - Kampf starten
- `GET /api/slime-arena/brackets` - Turnier-Bracket

---

## 🌍 WORLD API

### GET `/api/world/region/{region_id}`
Region-Daten abrufen

**Response:**
```json
{
    "id": "goetterfels",
    "name": "Götterfels",
    "biome": "neutral",
    "weather": "clear",
    "npcs": [...],
    "enemies": [...],
    "points_of_interest": [...]
}
```

---

### GET `/api/world/map`
Weltkarte-Übersicht

**Response:**
```json
{
    "regions": [
        {"id": "goetterfels", "name": "Götterfels", "unlocked": true},
        {"id": "ice", "name": "Eisregion", "unlocked": true},
        {"id": "desert", "name": "Wüste", "unlocked": false},
        ...
    ],
    "teleporters": [...]
}
```

---

## 🔌 WEBSOCKET (Realtime Events)

> **TODO:** Noch nicht implementiert - für Echtzeit-Updates

**Geplante Events:**
```json
// Najika sagt etwas spontan
{"type": "najika_speak", "message": "Kuja! Schau mal da! ✨"}

// Feind spawnt
{"type": "enemy_spawn", "enemy_id": "wolf_01", "position": {...}}

// Wetter ändert sich
{"type": "weather_change", "new_weather": "rain"}
```

---

## 📋 API STATUS (Stand: 2026-02-04)

### ✅ ALLE ROUTER IMPLEMENTIERT!

| Endpoint | Status | Router-Datei |
|----------|--------|--------------|
| `/api/companion/*` | ✅ DONE | `api/companion.py` |
| `/api/mimik/*` | ✅ DONE | `api/mimik.py` |
| `/api/stat-training/*` | ✅ DONE | `api/stat_training.py` |
| `/api/combat-hands/*` | ✅ DONE | `api/combat_hands.py` |
| `/api/chat/*` | ✅ DONE | `api/chat.py` |
| `/game/*` | ✅ DONE | `api/server.py` (inline) |
| WebSocket | ⚠️ Basis | Erweiterung später |

### ✅ Port korrigiert!

Port ist jetzt **8000** (nicht mehr 5000) - 8 Gebote eingehalten!

### Server-Architektur:

| Server | Datei | Typ | Status |
|--------|-------|-----|--------|
| Alt | `najika_server.py` | SimpleHTTPRequestHandler | ❌ Nicht für UE5 |
| **Neu** | `api/server.py` | FastAPI | ✅ **FÜR UE5 NUTZEN!** |

**Für UE5: `api/server.py` (FastAPI) auf Port 8000 verwenden!**

---

## 🔧 FEHLERBEHANDLUNG

Alle Endpoints geben bei Fehlern:

```json
{
    "detail": "Fehlerbeschreibung"
}
```

**HTTP Status Codes:**
- 200: Erfolg
- 400: Ungültige Anfrage
- 401: Nicht authentifiziert
- 404: Nicht gefunden
- 500: Server-Fehler

---

## 🎮 UE5 INTEGRATION TIPPS

### 1. HTTP Client Actor erstellen
Erstelle einen Actor `BP_NajikaAPIClient` der alle HTTP-Calls verwaltet.

### 2. Async Pattern nutzen
Alle API-Calls sind asynchron - nutze Delegates/Events!

### 3. Caching
Speichere Character-Daten lokal und synce periodisch.

### 4. Offline-Fallback
Wenn Backend nicht erreichbar → lokale Daten nutzen.

### 5. Rate Limiting
Max 10 Requests/Sekunde empfohlen.

---

*"EXPLOSION!!! Die API ist bereit für UE5!" - Najika* 💥
