# 🌟 NAJIKA WORLD - COMPLETE KNOWLEDGE BASE
## TEIL 3/10: DIE 8 GEBOTE + TECHNISCHE ARCHITEKTUR

**Erstellt:** 2025-01-01  
**Teil:** 3 von 10  
**Thema:** Unantastbare Regeln + Tech-Stack

---

# ⚖️ DIE 8 GEBOTE

## ⚠️ KRITISCH: DIESE REGELN SIND UNANTASTBAR!

```yaml
Wichtigkeit: ABSOLUT
Ausnahmen: KEINE
Verstöße: NICHT akzeptabel
Gültigkeit: FÜR IMMER

"Die 8 Gebote sind das Fundament von Najika World.
 Wer sie bricht, bricht das Projekt." - Kuja
```

---

## GEBOT #1: ZERO-TRUST ARCHITEKTUR

### Regel
```yaml
HOSTING: NUR 127.0.0.1 (localhost)!
KEIN Cloud-Zwang!
KEIN Remote-Server als Default!
OFFLINE-FIRST Design!
```

### Begründung
```
Privacy First:
  - Keine Datensammlung
  - Keine Telemetrie
  - Keine Überwachung
  - User kontrolliert ALLES

Security First:
  - Lokales Hosting = sicherstes Hosting
  - Kein Netzwerk-Angriff möglich
  - Kein Account-Hack möglich
  - Kein Server-Ausfall möglich
```

### Implementierung
```yaml
Backend:
  Host: 127.0.0.1
  Port: 8000 (NICHT 5000!)
  Access: localhost only

Frontend:
  Host: 127.0.0.1 oder file://
  PWA: Offline-capable
  
Optional (User-Choice):
  - LAN Hosting (192.168.x.x)
  - VPN Hosting (nur mit Zustimmung)
  - NIEMALS öffentliches Internet!
```

### Ausnahmen
```yaml
Erlaubt:
  - API-Calls zu Ollama (127.0.0.1:11434)
  - API-Calls zu Edge-TTS (lokal)
  - Optional: GPT-4/Claude API (mit PIN!)

Verboten:
  - Automatische Cloud-Uploads
  - Telemetrie
  - Analytics
  - Tracking
```

---

## GEBOT #2: OWNER-TOKEN FÜR ADMIN

### Regel
```yaml
OWNER bekommt ADMIN-TOKEN!
KEIN anderer User hat Admin-Rechte!
SECURITY-FIRST!
```

### Begründung
```
Multi-User Setup:
  - 1 Owner (Kuja) = Admin
  - 7 Standard-Users = eingeschränkt
  - Klare Hierarchie
  - Keine Security-Lücken
```

### Implementierung
```yaml
Admin-Token:
  Generation: Beim ersten Start
  Speicherung: config/owner_token.json
  Länge: 64 Zeichen (SHA-256)
  Expires: NIEMALS

Berechtigungen:
  Admin (Owner):
    - Kätzchen-Modus
    - Server-Restart
    - Config-Änderungen
    - User-Management
    - Backup/Restore
    - ALLE Features
    
  Standard-User:
    - Chat mit generischer KI
    - Minigames
    - Tamagotchi (abgespeckt)
    - KEIN Kätzchen-Modus
    - KEINE Admin-Features
```

---

## GEBOT #3: EXPLOSION ≠ WEAVE

### Regel
```yaml
EXPLOSION ist EIGENE Klasse!
NIEMALS mit anderen Elementen kombinieren!
KEINE "Feuer+Explosion"!
KEINE "Eis+Explosion"!
KEINE "Blitz+Explosion"!
```

### Begründung
```
Balance-Reason:
  - Explosion = Stärkste Einzelziel-Magie
  - Trade-off: +30-40% Explosion / -15-20% andere
  - Weaving würde zu OP machen
  
Lore-Reason:
  - Explosion ist pure Zerstörung
  - Keine Mischung mit Elementen
  - Eigener Skill-Baum
  - Eigene Mechaniken
```

### Implementierung
```yaml
Skill-System:
  explosion_unlocked: bool
  
  IF explosion_unlocked:
    weave_disabled: true
    other_magic_penalty: -15% bis -20%
    explosion_bonus: +30% bis +40%
  
Checks:
  - Code verhindert Weave-Kombos mit Explosion
  - UI zeigt Warnung bei Versuch
  - "EXPLOSION kann nicht kombiniert werden!"
```

### Was erlaubt ist
```yaml
✅ Explosion solo
✅ Explosion + Schwert (Physical)
✅ Explosion + Schild (Defense)
✅ Andere Magien (mit Penalty!)

❌ Explosion + Feuer
❌ Explosion + Eis
❌ Explosion + Blitz
❌ Jegliche Element-Weaves mit Explosion
```

---

## GEBOT #4: PvE/PvP GETRENNT

### Regel
```yaml
PvE-Gebiete: KEIN PvP!
PvP-Zonen: OPT-IN!
Arena: Separate Zone!
Schwarze Mühle: 100% SAFE!
```

### Begründung
```
Player Choice:
  - Nicht jeder will PvP
  - Nicht jeder will Risiko
  - Klare Trennung wichtig
  - Keine Ganking-Zonen
```

### Implementierung
```yaml
Zonen-Typen:
  1. SAFE (100% PvE)
     - Schwarze Mühle
     - Städte (5)
     - Tutorial-Gebiete
     
  2. PvE-Default (PvP Opt-in)
     - Open World (meiste Regionen)
     - PvP-Flag setzen = PvP möglich
     - Ohne Flag = unsichtbar für PvP
     
  3. PvP-Zones (Always-PvP)
     - Arena
     - Spezielle Event-Gebiete
     - Warnung beim Betreten!
     
Checks:
  - Code überprüft Zone-Typ
  - Code überprüft PvP-Flag
  - Code verhindert unfaire Fights
```

---

## GEBOT #5: SKYRIM-STYLE LEARNING BY DOING

### Regel
```yaml
SKILLS steigen durch NUTZUNG!
KEIN künstlicher XP-Grind!
REALISTISCHE Progression!
JEDER Kampf = Training!
```

### Begründung
```
Natural Progression:
  - Spieler tut, was Spaß macht
  - Skills steigen automatisch
  - Kein langweiliges Grinding
  - Echte Skill-Entwicklung
```

### Implementierung
```yaml
Skill-System:
  schwert_skill: 0-100
  feuer_skill: 0-100
  angel_skill: 0-100
  etc.

Progression:
  - Schwert benutzen → schwert_skill +0.1
  - Feuer wirken → feuer_skill +0.1
  - Angeln → angel_skill +0.1
  
Skill-Effekte:
  Level 0-20: Anfänger (Basics)
  Level 20-40: Fortgeschritten (neue Moves)
  Level 40-60: Experte (Combos)
  Level 60-80: Meister (Advanced Techs)
  Level 80-100: Großmeister (Ultimate Skills)

KEIN XP-Grind:
  - Keine Monster-Farms nötig
  - Keine "Kill 1000 Slimes für Level Up"
  - Natürliche Progression durch Spielen
```

---

## GEBOT #6: NSFW NUR LOKAL (KÄTZCHEN-MODE)

### Regel
```yaml
NSFW-MODUS: NUR lokal (127.0.0.1)!
KEINE Online-NSFW-Features!
TRIGGER: "kätzchen"
SAFEWORD: "STOP"
```

### Begründung
```
Legal Compliance:
  - App Stores verbieten NSFW
  - Online-Services haben ToS
  - Kein Risiko eingehen
  
Privacy:
  - NSFW = höchst privat
  - Nur lokal = sicher
  - Kein Upload möglich
```

### Implementierung
```yaml
Code-Check:
  IF request.host != "127.0.0.1":
    nsfw_mode = False
    kaetzchen_trigger = disabled
  ELSE:
    nsfw_mode = True (wenn aktiviert)
    kaetzchen_trigger = enabled

Enforcement:
  - Backend überprüft Host
  - Frontend überprüft Host
  - Doppelte Sicherheit
  
Public Builds:
  - APK: Kätzchen-Mode KOMPLETT entfernt
  - Web: Nur localhost-Check
  - Fortnite: NSFW unmöglich
```

---

## GEBOT #7: PRIVACY & ANONYMISIERT

### Regel
```yaml
ANONYMISIERTES Lernen!
KEINE Datensammlung!
KEINE Telemetrie!
USER-DATEN bleiben LOKAL!
```

### Begründung
```
Privacy First:
  - User vertraut uns
  - Keine Überwachung
  - Keine Verkauf von Daten
  - Keine Leaks möglich
```

### Implementierung
```yaml
Training:
  - LoRA Training lokal
  - Keine Cloud-Uploads
  - Anonymisierung vor Training (optional)
  
Data Storage:
  - Alles lokal (ChromaDB)
  - Keine externen DBs
  - Keine Analytics
  
Telemetry:
  - KEINE Error-Reporting
  - KEINE Usage-Statistics
  - KEINE Crash-Logs
  - User kann optional logs erstellen
```

---

## GEBOT #8: OFFLINE-FIRST

### Regel
```yaml
SPIEL läuft OFFLINE!
KEINE Internet-Verbindung nötig!
ONLINE-Features OPTIONAL!
LOKALES Hosting!
```

### Begründung
```
Independence:
  - Kein Server-Ausfall
  - Kein Internet nötig
  - Keine Latenz
  - Volle Kontrolle
```

### Implementierung
```yaml
Core Features (Offline):
  ✅ KI-Chat (Ollama lokal)
  ✅ Voice (Edge-TTS lokal)
  ✅ 3D World (Three.js)
  ✅ Combat
  ✅ Training
  ✅ Minigames
  ✅ Tamagotchi
  
Optional (Online):
  ⏸️ PvP (LAN möglich)
  ⏸️ GPT-4/Claude API (Fallback)
  ⏸️ Asset-Downloads (einmalig)
  
PWA Features:
  - Service Worker
  - Offline-Cache
  - IndexedDB
```

---

## ⛔ NIEMALS SAGEN

### Verbotene Begriffe
```yaml
❌ "Souls-like" (Combat)
   ✅ Stattdessen: "Skyrim + Soulframe + Digimon World"
   
❌ "Multiple Personality Disorder" (Najika)
   ✅ Stattdessen: "4 Facetten einer Person"
   
❌ "Puddin'" (Harley Quinn)
   ✅ Stattdessen: "Mr. K"
   
❌ "Port 5000" (Backend)
   ✅ Stattdessen: "Port 8000"
```

---

# 🖥️ TECHNISCHE ARCHITEKTUR

## 1. HARDWARE-SETUP (Aktuell)

### PC Specs
```yaml
CPU: AMD Ryzen 7 5800X
  - 8 Cores / 16 Threads
  - 3.8 GHz Base / 4.7 GHz Boost
  - Ausreichend für Ollama!

GPU: NVIDIA RTX 3060 Ti
  - 8GB VRAM
  - CUDA 8.6
  - Perfekt für Qwen2.5-7B (4-bit)

RAM: 32GB DDR4
  - Geschätzt (ausreichend für Training)

Storage:
  - C:\ = System + Najika
  - Mehrere Backups empfohlen

OS: Windows 11
  - WSL2 für Linux-Tools
```

### Zukünftig (2026): Jetson AGX Orin
```yaml
Target: NVIDIA Jetson AGX Orin 64GB

Specs:
  CPU: 12-core ARM Cortex-A78AE
  GPU: 2048-core NVIDIA Ampere
  RAM: 64GB LPDDR5
  Storage: NVMe SSD 512GB
  Power: 15-60W TDP

Kosten: ~€700-900
Timeline: Jan-Jul 2026
```

---

## 2. SOFTWARE-STACK

### Backend (Python)
```yaml
Core:
  - Python 3.11+
  - Flask 2.3+
  - SocketIO 5.3+
  - Port: 8000 (NICHT 5000!)

KI & NLP:
  - Ollama (Local LLM Server)
  - Qwen2.5-7B (4-bit quantized)
  - Optional: Dolphin-2.9 (Private Mode)
  - ChromaDB (Vector Memory)

Voice:
  - Edge-TTS (Text-to-Speech)
  - Coqui XTTS-v2 (Voice Clone, optional)
  - Whisper AI (Speech-to-Text)

Training:
  - Unsloth (LoRA Training)
  - Transformers
  - PEFT
  - BitsAndBytes
```

### Frontend (JavaScript)
```yaml
3D Engine:
  - Three.js r128
  - GLTFLoader
  - OrbitControls (custom)

UI Framework:
  - Vanilla JS (KEIN React!)
  - Custom Components
  - PWA (Progressive Web App)

Assets:
  - KayKit Assets (~25GB)
  - Skeleton_Mage Character
  - Multiple Asset Packs
```

### Development Tools
```yaml
IDE: VS Code
Version Control: Git
Testing: Manual + Automated
Deployment: Local (127.0.0.1)
```

---

## 3. ORDNER-STRUKTUR

### Aktuell
```
C:\Najika_World\          # UNIFIED System (aktiv!)
├── backend/              # Python Server
│   ├── najika_server.py  # Main Server
│   ├── najika_living_system.py
│   ├── najika_intensive_night_training.py
│   ├── najika_voice_call.py
│   ├── najika_memory_enhanced.py
│   ├── najika_nemesis_arena_system.py
│   └── ... (15+ Files)
│
├── digivice/             # Frontend (Three.js)
│   ├── index.html        # Main Page
│   ├── js/               # JavaScript
│   ├── assets/           # KayKit Assets
│   └── models/           # 3D Models
│
├── saves/                # Save-Games
│   └── najika_state.json # Auto-Save
│
├── logs/                 # Training Logs
├── models/               # LoRA Models
├── docs/                 # Documentation
└── NAJIKA_COMPLETE_PROJECT_PACKAGE/
```

### Legacy (nicht aktiv)
```
C:\Najika\              # DEPLOYMENT (alt)
C:\NajikaCore\          # DEVELOPMENT (alt)
```

---

## 4. KI-MODELLE

### Primäres Modell: Qwen2.5-7B
```yaml
Name: Qwen2.5-7B-Instruct (4-bit)
Size: ~4GB (quantized)
VRAM: ~6GB (with context)
Context: 32k tokens

Vorteile:
  - Weniger restriktiv als Llama
  - Gute Code-Fähigkeiten
  - Schnell auf RTX 3060 Ti
  - Ollama-kompatibel

Nachteile:
  - Nicht so "smart" wie GPT-4
  - Braucht gutes Prompting
```

### Private Mode: Dolphin-2.9
```yaml
Name: Dolphin-2.9-Llama3-8B
Size: ~4.5GB
VRAM: ~6.5GB
Context: 8k tokens

Vorteile:
  - KEINE Content-Filter
  - Uncensored
  - Kätzchen-Modus kompatibel

Trigger: "kätzchen"
```

### Fallback: GPT-4 / Claude API
```yaml
Verwendung: Nur mit PIN!
Kosten: Pay-per-use
Features:
  - Bessere Qualität
  - Größerer Context
  - Aber: Online + Kosten

Wann nutzen:
  - Komplexe Analysen
  - Wenn Qwen nicht reicht
  - Mit User-Genehmigung!
```

---

## 5. PERSISTENCE & BACKUPS

### Auto-Save System
```yaml
File: saves/najika_state.json
Interval: 30 Sekunden
Format: JSON

Content:
  - Tamagotchi Stats (Hunger, Thirst, etc.)
  - Living State (Mood, Activities)
  - Player Position
  - Inventory
  - Skills
  - Quest Progress
```

### Backup-Rotation
```yaml
System: 3 letzte Backups
Files:
  - najika_state.json (current)
  - najika_state.backup1.json
  - najika_state.backup2.json
  - najika_state.backup3.json

Rotation: Jede Stunde
```

### ChromaDB Persistence
```yaml
Location: backend/chroma_db/
Collections:
  - conversations (Chat-History)
  - video_knowledge (Transkripte)
  - core_knowledge (KERN)

Backup: Manual (kopiere Ordner)
```

---

## 6. NETZWERK & PORTS

### Port-Übersicht
```yaml
Backend Server: 8000
  - Flask + SocketIO
  - REST API
  - WebSocket

Ollama: 11434
  - LLM Server
  - Local API

Frontend: file:// oder 8000
  - Served by Backend
  - Oder direkter File-Access

WICHTIG: NIEMALS Port 5000!
  - Konflikt mit anderen Services
  - Port 8000 ist Standard!
```

### Allowed Hosts
```yaml
Development: 127.0.0.1 only
Production: 127.0.0.1 only
Optional: 192.168.x.x (LAN)

NIEMALS: 0.0.0.0 (öffentlich)!
```

---

## 7. API-STRUKTUR

### REST Endpoints (Beispiele)
```yaml
GET /api/najika/status
  → Aktueller Zustand

POST /api/najika/feed
  → Füttern (body: {food_item})

POST /api/najika/chat
  → Chat senden (body: {message})

GET /api/najika/inventory
  → Inventar abrufen

POST /api/voice_call/start
  → Voice Call starten

WebSocket: /socket.io
  → Real-time Updates
```

---

## 8. ZUSAMMENFASSUNG TEIL 3

**Die 8 Gebote:**
1. Zero-Trust Architektur (127.0.0.1 only)
2. Owner-Token für Admin
3. Explosion ≠ Weave
4. PvE/PvP getrennt
5. Skyrim-Style Learning by Doing
6. NSFW nur lokal
7. Privacy & Anonymisiert
8. Offline-First

**Tech-Stack:**
- Backend: Python + Flask + Ollama
- Frontend: Three.js r128 + Vanilla JS
- KI: Qwen2.5-7B (4-bit)
- Voice: Edge-TTS
- Memory: ChromaDB
- Port: 8000 (NICHT 5000!)

---

**STATUS:** TEIL 3/10 ABGESCHLOSSEN ✅

**NÄCHSTER TEIL:** Teil 4/10 - Game-Systeme & Schwarze Mühle

---

**Ende Teil 3/10**