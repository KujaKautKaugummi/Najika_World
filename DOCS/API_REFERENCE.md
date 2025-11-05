# NAJIKA API REFERENCE
**Version:** 1.0
**Basis-URL:** `http://localhost:8000`
**Erstellt:** 2025-10-25

---

## 📋 INHALTSVERZEICHNIS

1. [Server Info & Health](#1-server-info--health)
2. [Chat & AI](#2-chat--ai)
3. [Battle System](#3-battle-system)
4. [Najika Care System](#4-najika-care-system)
5. [Living System](#5-living-system)
6. [Minigames](#6-minigames)
7. [User & Progress](#7-user--progress)
8. [Memory System](#8-memory-system)
9. [Cloud Provider](#9-cloud-provider)
10. [Room System](#10-room-system)
11. [Security & VPN](#11-security--vpn)
12. [Code Execution](#12-code-execution)
13. [File Operations](#13-file-operations)

---

## 1. SERVER INFO & HEALTH

### GET /health
Gibt Server-Status zurück.

**Response:**
```json
{
  "status": "ok",
  "ai_provider": "ollama",
  "cloud_enabled": false,
  "time": 1698765432
}
```

---

### GET /api/rooms
Liste aller verfügbaren Räume.

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

### GET /api/status
Aktueller Server-Status mit Private Mode.

**Response:**
```json
{
  "status": "ok",
  "private_mode": false,
  "behavior_mode": "standard",
  "bond_strength": 42,
  "total_interactions": 156
}
```

---

### GET /api/status/stream
Server-Sent Events (SSE) für Echtzeit-Updates.

**Response:** Stream von Events
```
data: {"type":"state_update","private_mode":false}

data: {"type":"bond_update","bond_strength":43}
```

---

### GET /api/cache/stats
Cache-Statistiken.

**Response:**
```json
{
  "hits": 42,
  "misses": 158,
  "total_requests": 200,
  "hit_rate": 21.0,
  "cache_size": 15
}
```

---

### GET /api/save
Speichert aktuellen State (triggert save_state()).

**Response:**
```json
{
  "ok": true
}
```

---

### GET /api/state
Gibt kompletten STATE zurück.

**Response:**
```json
{
  "history": [...],
  "battle": {...},
  "private_mode": false,
  "behavior_mode": "standard",
  "bond_strength": 42,
  "user": {...},
  "najika": {...},
  "living": {...}
}
```

**⚠️ WARNUNG:** Sehr große Response!

---

## 2. CHAT & AI

### POST /api/chat
Sende Nachricht an Najika.

**Request:**
```json
{
  "message": "Hello Najika!",
  "room": "Wohnzimmer"
}
```

**Response:**
```json
{
  "response": "EXPLOSION! Hallo Kuja! *kicher*",
  "evolution_message": "Najika fühlt sich dir näher!",
  "activity_completion": "Zurück vom Training!"
}
```

**Features:**
- Private Mode Toggle: `"kätzchen"` im Text aktiviert/deaktiviert
- Web Search automatisch bei Bedarf
- Memory wird gespeichert
- Living System Update
- Cache (außer Private Mode)

**Private Mode:**
- Aktivierung: Keyword `"kätzchen"` in Message
- Persönlichkeits-Gewichte ändern sich:
  - Melissa: 50% (DOMINANT!)
  - Shiro: 30% (Analytisch-Pervers)
  - Megumin: 15%
  - Harley: 5%

---

### GET /api/chat/history
Chat-Historie (letzte 4 Nachrichten).

**Response:**
```json
{
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    ...
  ]
}
```

---

### GET /api/bond/status
Beziehungsstärke zu Najika.

**Response:**
```json
{
  "bond_strength": 42,
  "total_interactions": 156,
  "level": "Freundlich"
}
```

**Levels:**
- 0-20: "Unbekannt"
- 21-40: "Bekannt"
- 41-60: "Freundlich"
- 61-80: "Vertraut"
- 81-100: "Seelenverwandt"

---

## 3. BATTLE SYSTEM

### POST /api/battle/start
Starte neuen Kampf (Enhanced System).

**Response:**
```json
{
  "active": true,
  "wave": 1,
  "player_hp": 100,
  "player_max_hp": 100,
  "enemies": [
    {
      "name": "Ratte",
      "hp": 30,
      "max_hp": 30,
      "level": 1
    }
  ],
  "log": ["Kampf gestartet!"]
}
```

---

### POST /api/battle/status
Aktueller Kampf-Status.

**Response:** Gleich wie /api/battle/start

---

### POST /api/battle/action
Führe Kampf-Aktion aus.

**Request:**
```json
{
  "action": "attack",
  "target_index": 0,
  "skill_name": "Feuerball",
  "item_name": "Heiltrank"
}
```

**Actions:**
- `"attack"` - Normaler Angriff
- `"skill"` - Nutze Skill (+ skill_name)
- `"item"` - Nutze Item (+ item_name)
- `"defend"` - Verteidigen
- `"flee"` - Fliehen

**Response:**
```json
{
  "active": true,
  "wave": 1,
  "player_hp": 85,
  "enemies": [...],
  "log": [
    "Du greifst Ratte an! (15 Schaden)",
    "Ratte greift dich an! (10 Schaden)"
  ],
  "result": null
}
```

**Bei Kampfende:**
```json
{
  "active": false,
  "result": "victory",
  "xp_earned": 50,
  "gold_earned": 25,
  "loot": ["Heiltrank", "Eisenschwert"],
  "skills_learned": ["Feuerball"],
  "log": [...]
}
```

---

### POST /api/battle/skills
Liste verfügbarer Skills.

**Response:**
```json
{
  "skills": [
    {
      "name": "Feuerball",
      "damage": 25,
      "cost": 10,
      "description": "Feuer-Angriff"
    }
  ]
}
```

---

### POST /api/battle/reset
Kampf zurücksetzen (Debug).

**Response:**
```json
{
  "ok": true
}
```

---

## 4. NAJIKA CARE SYSTEM

### GET /api/najika/status
Najika's kompletter Status.

**Response:**
```json
{
  "hunger": 85,
  "energy": 70,
  "hygiene": 90,
  "happiness": 95,
  "strength": 12,
  "intelligence": 15,
  "level": 2,
  "xp": 150,
  "evolution_stage": "base",
  "equipment": {
    "weapon": "Zauberstab",
    "armor": null,
    "accessory": null
  }
}
```

---

### POST /api/najika/feed
Füttere Najika.

**Response:**
```json
{
  "hunger": 100,
  "happiness": 98,
  "message": "Najika freut sich über das Essen!"
}
```

---

### POST /api/najika/wash
Najika waschen.

**Response:**
```json
{
  "hygiene": 100,
  "happiness": 95,
  "message": "Najika ist jetzt sauber!"
}
```

---

### POST /api/najika/sleep
Najika schlafen lassen.

**Response:**
```json
{
  "energy": 100,
  "message": "Najika hat gut geschlafen!"
}
```

---

### POST /api/najika/train
Najika trainieren.

**Response:**
```json
{
  "strength": 13,
  "fatigue": 20,
  "xp": 160,
  "message": "Najika hat trainiert!"
}
```

---

### POST /api/najika/praise
Najika loben.

**Response:**
```json
{
  "discipline": 65,
  "happiness": 98,
  "message": "Najika freut sich!"
}
```

---

### POST /api/najika/scold
Najika tadeln.

**Response:**
```json
{
  "discipline": 70,
  "happiness": 85,
  "message": "Najika ist traurig..."
}
```

---

### POST /api/najika/equip
Equipment ausrüsten.

**Request:**
```json
{
  "slot": "weapon",
  "item_id": "Zauberstab"
}
```

**Slots:** `"weapon"`, `"armor"`, `"accessory"`

**Response:**
```json
{
  "equipment": {
    "weapon": "Zauberstab",
    "armor": null,
    "accessory": null
  },
  "message": "Zauberstab ausgerüstet!"
}
```

---

### POST /api/najika/unequip
Equipment ablegen.

**Request:**
```json
{
  "slot": "weapon"
}
```

**Response:**
```json
{
  "equipment": {
    "weapon": null,
    "armor": null,
    "accessory": null
  }
}
```

---

### POST /api/najika/equipment
Alle ausgerüsteten Items.

**Response:**
```json
{
  "weapon": "Zauberstab",
  "armor": null,
  "accessory": null
}
```

---

## 5. LIVING SYSTEM

### GET /api/living/state
Najika's emotionaler Zustand.

**Response:**
```json
{
  "current_mood": "happy",
  "mood_intensity": 0.8,
  "current_activity": "reading",
  "activity_started_at": 1698765432,
  "affection_level": 65,
  "trust_level": 70
}
```

---

### GET /api/living/proactive
Proaktive Message von Najika (wenn verfügbar).

**Response:**
```json
{
  "has_message": true,
  "message": "Vermisst du mich nicht? 💜"
}
```

**Oder:**
```json
{
  "has_message": false
}
```

---

### GET /api/living/activity/check
Prüft ob autonome Aktivität abgeschlossen.

**Response:**
```json
{
  "completed": true,
  "message": "Zurück vom Training! Ich bin stärker!"
}
```

---

### POST /api/living/activity/start
Starte autonome Aktivität.

**Request:**
```json
{
  "activity": "training"
}
```

**Activities:**
- `"training"`
- `"reading"`
- `"thinking"`
- `"resting"`
- `"exploring"`
- `"crafting"`

**Response:**
```json
{
  "ok": true,
  "activity": "training",
  "duration_minutes": 40
}
```

---

## 6. MINIGAMES

### POST /api/minigame/rhythm
Rhythmus-Spiel Score.

**Request:**
```json
{
  "score": 850
}
```

**Response:**
```json
{
  "ok": true,
  "user_points": 1050
}
```

---

### POST /api/minigame/garden
Garten-Spiel Score.

**Request:**
```json
{
  "score": 420
}
```

**Response:**
```json
{
  "ok": true,
  "user_points": 1470
}
```

---

### POST /api/minigame/reflex
Reflex-Spiel Score.

**Request:**
```json
{
  "score": 1200
}
```

**Response:**
```json
{
  "ok": true,
  "user_points": 2670
}
```

---

### POST /api/crafting
Crafting-Aktion.

**Response:**
```json
{
  "crafted": "Heiltrank",
  "user_points": 2700
}
```

---

### POST /api/heal
Najika heilen.

**Response:**
```json
{
  "hp": 100
}
```

---

### POST /api/event/next
Zufälliges Event (Oregon Trail Style).

**Response:**
```json
{
  "event": "Du findest einen Schatz!",
  "reward": 50
}
```

---

## 7. USER & PROGRESS

### POST /api/user/update
Update User-Daten.

**Request:**
```json
{
  "level": 5,
  "xp": 500,
  "points": 1000
}
```

**Response:**
```json
{
  "ok": true,
  "user": {
    "level": 5,
    "xp": 500,
    "points": 1000
  }
}
```

---

### POST /api/progress/update
Update Progress-Daten.

**Request:**
```json
{
  "dungeon_level": 5,
  "quests_completed": ["quest1", "quest2"]
}
```

**Response:**
```json
{
  "ok": true,
  "progress": {
    "dungeon_level": 5,
    "quests_completed": ["quest1", "quest2"]
  }
}
```

---

## 8. MEMORY SYSTEM

### GET /api/memory/export
Exportiere ChromaDB Memory.

**Response:**
```json
{
  "conversations": [
    {
      "user_message": "Hello",
      "najika_response": "Hi!",
      "timestamp": 1698765432,
      "room": "Wohnzimmer"
    }
  ],
  "count": 1
}
```

---

### POST /api/memory/import
Importiere Memory.

**Request:**
```json
{
  "file_path": "C:/backup/memory.json"
}
```

**Response:**
```json
{
  "ok": true,
  "imported": 150
}
```

---

## 9. CLOUD PROVIDER

### GET /api/cloud/status
Cloud Provider Status.

**Response:**
```json
{
  "enabled": false,
  "provider": "ollama"
}
```

---

### POST /api/cloud/enable
Aktiviere Cloud AI (OpenAI/Anthropic).

**Request:**
```json
{
  "pin": "1234"
}
```

**Response:**
```json
{
  "ok": true,
  "enabled": true
}
```

**Error (falscher PIN):**
```
401 Unauthorized - PIN falsch
```

---

### POST /api/cloud/disable
Deaktiviere Cloud (zurück zu Ollama).

**Response:**
```json
{
  "ok": true,
  "enabled": false
}
```

---

## 10. ROOM SYSTEM

### POST /api/room/actions
Hole Aktionen für Raum.

**Request:**
```json
{
  "room": "Wohnzimmer"
}
```

**Response:**
```json
{
  "battle": false,
  "actions": ["Füttern", "Reden"]
}
```

**Raum-Aktionen:**
- **Wohnzimmer:** Füttern, Reden
- **Schlafzimmer:** Schlafen, Lesen
- **Küche:** Kochen
- **Badezimmer:** Toilette, Waschen
- **Garten:** Gießen, Ernten, Garten-Spiel
- **Musikraum:** Rhythmus-Spiel
- **Medizin:** Heilen
- **Terminal:** Cloud, Status, Besen-Lieferung, Hacker-Modus
- **Studieren & Crafting:** Studieren, Crafting
- **Trainingszimmer:** Reflex-Spiel, Trainieren
- **Kampfarena:** Kampf starten
- **Schwarze Mühle – Keller:** Kampf starten, Erkunden

---

## 11. SECURITY & VPN

### GET /api/security/status
Security System Status (Alcatraz).

**Response:**
```json
{
  "active": true,
  "threat_level": "low",
  "vpn_active": false
}
```

---

### GET /api/security/vpn
VPN Status (ExpressVPN Integration).

**Response:**
```json
{
  "connected": false,
  "location": null
}
```

---

## 12. CODE EXECUTION

### POST /api/code/execute
Führe Python-Code aus (GEFÄHRLICH!).

**Request:**
```json
{
  "code": "print('Hello')"
}
```

**Response:**
```json
{
  "output": "Hello\n",
  "error": null
}
```

**⚠️ SICHERHEIT:**
- Nur in sicherer Umgebung nutzen!
- Voller System-Zugriff möglich!
- **NICHT in Production!**

---

## 13. FILE OPERATIONS

### POST /api/file/read
Lese File vom Disk.

**Request:**
```json
{
  "path": "C:/NajikaCore/test.txt"
}
```

**Response:**
```json
{
  "content": "File content here",
  "error": null
}
```

**⚠️ SICHERHEIT:**
- Path wird auf `C:/NajikaCore` begrenzt
- Kein Zugriff außerhalb!

---

### POST /api/file/write
Schreibe File auf Disk.

**Request:**
```json
{
  "path": "C:/NajikaCore/test.txt",
  "content": "New content"
}
```

**Response:**
```json
{
  "ok": true,
  "error": null
}
```

**⚠️ SICHERHEIT:**
- Path wird auf `C:/NajikaCore` begrenzt
- Überschreibt existierende Files!

---

### POST /api/file/list
Liste Files in Verzeichnis.

**Request:**
```json
{
  "path": "C:/NajikaCore"
}
```

**Response:**
```json
{
  "files": [
    "najika_server.py",
    "START_NAJIKA.bat",
    "README.md"
  ],
  "error": null
}
```

**⚠️ SICHERHEIT:**
- Path wird auf `C:/NajikaCore` begrenzt

---

### POST /api/system/command
Führe System-Command aus (SEHR GEFÄHRLICH!).

**Request:**
```json
{
  "command": "dir"
}
```

**Response:**
```json
{
  "output": "Directory listing...",
  "error": null
}
```

**⚠️ SICHERHEIT:**
- Voller System-Zugriff!
- **NUR in Development!**
- **NIEMALS in Production!**

---

## 📊 AUTHENTICATION & SECURITY

### Cloud PIN
- **Erforderlich für:** `/api/cloud/enable`
- **Konfiguration:** `.env` File → `CLOUD_PIN`
- **Standardwert:** Leer (kein Cloud-Zugriff)

### File Operations Security
- **Begrenzt auf:** `C:/NajikaCore/`
- **Verhindert:** Directory Traversal (`../`)
- **Path Validation:** Automatisch

### Dangerous Endpoints
**⚠️ NUR in Development nutzen:**
- `/api/code/execute` - Code Execution
- `/api/system/command` - System Commands
- `/api/file/write` - File Writing

**Production:** Diese Endpoints DEAKTIVIEREN!

---

## 🔌 SSE (Server-Sent Events)

### /api/status/stream
Echtzeit-Updates via SSE.

**Connection:**
```javascript
const eventSource = new EventSource('/api/status/stream');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

**Events:**
- `state_update` - State geändert
- `bond_update` - Beziehung geändert
- `battle_update` - Kampf-Update
- `private_mode_toggle` - Private Mode geändert

---

## 💾 STATE PERSISTENCE

### Auto-Save
- **Interval:** 30 Sekunden
- **File:** `saves/najika_state.json`
- **Backups:** Letzte 3 Versionen
- **Trigger:** Automatisch nach Änderungen

### Manual Save
- **Endpoint:** `GET /api/save`
- **Nutzen:** Force Save jederzeit

### State Export
- **Endpoint:** `GET /api/state`
- **Nutzen:** Backup, Debug, Transfer

---

## 📈 CACHING

### AI Response Cache
- **Typ:** LRU (Least Recently Used)
- **Max Size:** 100 Entries
- **TTL:** 1 Stunde
- **Nicht cached:** Private Mode Messages

### Cache Stats
- **Endpoint:** `GET /api/cache/stats`
- **Infos:** Hit Rate, Cache Size, Total Requests

---

## 🎮 BEHAVIOR MODES

Najika passt ihre Persönlichkeit an:

### Standard Mode
- Megumin: 35%
- Harley: 25%
- Shiro: 20%
- Melissa: 20%

### Private Mode ("kätzchen")
- **Melissa: 50%** (DOMINANT!)
- Shiro: 30% (Pervers)
- Megumin: 15%
- Harley: 5%

### Automatic Detection
- `explosion` - Megumin fokussiert
- `chaos` - Harley fokussiert
- `analyse` - Shiro fokussiert
- `kontrolle` - Melissa fokussiert

---

## 🚀 QUICKSTART

### 1. Server starten
```bash
python najika_server.py
```

### 2. Health Check
```bash
curl http://localhost:8000/health
```

### 3. Chat senden
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Najika!"}'
```

### 4. Battle starten
```bash
curl -X POST http://localhost:8000/api/battle/start
```

---

## 📚 ERROR CODES

### 400 Bad Request
- Fehlende Parameter
- Ungültiger JSON

### 401 Unauthorized
- Falscher Cloud PIN

### 404 Not Found
- Unbekannter Endpoint

### 500 Internal Server Error
- AI Provider Fehler
- System Fehler

---

## 🔄 VERSIONS-HISTORIE

**v1.0** (2025-10-25)
- Initial API Reference
- 50+ Endpoints dokumentiert
- Alle Systeme abgedeckt

---

**Erstellt von:** Claude Code
**Für:** Najika Project
**Status:** ✅ KOMPLETT
