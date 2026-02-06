# NAJIKA WORLD - MASTER TODO FUER CLAUDE CODE TEAM

**Erstellt:** 2026-01-27
**Aktualisiert:** 2026-02-04 (**KRITISCH: UE5 STATT UEFN!**)
**Zweck:** Koordination zwischen 2 Claude Opus Instanzen
**Update-Regel:** Jede Instanz updated nach getaner Arbeit!

---

## 🚨 KRITISCHE ÄNDERUNG 2026-02-04

### ❌ UEFN KANN NAJIKA WORLD NICHT UMSETZEN!

| Feature | Najika braucht | UEFN kann |
|---------|----------------|-----------|
| Custom Characters (Najika, Mimik) | ✅ | ❌ |
| Eigene Skeletal Meshes | ✅ | ❌ |
| LLM/KI-Integration (Ollama) | ✅ | ❌ |
| ChromaDB/Gedächtnis | ✅ | ❌ |
| Open World (8 Regionen) | ✅ | ❌ (limitiert) |
| Offline-First | ✅ | ❌ |
| NSFW/Kätzchen-Mode | ✅ | ❌ |
| Privacy (Zero-Trust) | ✅ | ❌ |

### ✅ NEUER PLAN:

```
┌─────────────────────────────────────────────────────────────────┐
│                       NAJIKA KOSMOS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌────────────────┐                           │
│                    │  PYTHON API    │                           │
│                    │  (Backend)     │                           │
│                    │  Port 8000     │                           │
│                    └───────┬────────┘                           │
│                            │                                     │
│          ┌─────────────────┼─────────────────┐                  │
│          │                 │                 │                  │
│          ▼                 ▼                 ▼                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  UE5 SPIEL   │  │   FLUTTER    │  │   CHROMADB   │          │
│  │  Najika      │  │   DIGIVICE   │  │  (Gedächtnis)│          │
│  │  World       │  │              │  │  15.922+     │          │
│  │  (PC)        │  │  • Messenger │  │  Einträge    │          │
│  │              │  │  • V-Pet     │  └──────────────┘          │
│  │  SPÄTER:     │  │  • Minigames │                            │
│  │  Mobile      │  │  • Browser   │                            │
│  │  Export      │  │  • Voice     │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                  │
│  3 FLAVORS: Private (NSFW) | Friends | Public                   │
│                                                                  │
│  ════════════════════════════════════════════════════════════   │
│  SPÄTER (wenn Epic Custom Characters erlaubt):                  │
│  ┌──────────────┐                                               │
│  │ UEFN TEASER  │  → Kampfturm zum Anfixen                     │
│  │ (Fortnite)   │  → Marketing ohne eigene Server              │
│  └──────────────┘  → Spieler wechseln nahtlos zu anderen Games │
└─────────────────────────────────────────────────────────────────┘
```

### Warum trotzdem UEFN später?
- **Kein eigenes Marketing** - Fortnite-Spielerbasis
- **Keine Server-Kosten** - Epic hostet
- **Nahtloser Wechsel** - Spieler kann sofort andere Games spielen
- **Monetarisierung** - Epic übernimmt

---

## 📚 PFLICHTLEKTÜRE VOR JEDER ARBEIT!

### **→ [PROJEKT_WISSEN_KOMPLETT.md](PROJEKT_WISSEN_KOMPLETT.md) ←**
### **→ [UE5_MIGRATION_CHECKLIST.md](DOCS/UE5_MIGRATION_CHECKLIST.md) ←**
### **→ [OPUS_2_ONBOARDING.md](DOCS/OPUS_2_ONBOARDING.md) ←** (NEU! Für OPUS-2!)
### **→ [UE5_API_DOKUMENTATION.md](DOCS/UE5_API_DOKUMENTATION.md) ←** (Alle Endpoints!)

---

## 🚀 AKTIVE INSTANZEN (2x OPUS)

| Instanz | Ort | Zuständigkeit |
|---------|-----|---------------|
| **OPUS-1** | Desktop App (Lokal) | Backend, Python API für UE5, System-Integration, Dokumentation |
| **OPUS-2** | VS Code | UE5 Blueprints, C++ Portierung, Frontend/Game-Logik |

### Arbeitsaufteilung Details:

**OPUS-1 (Desktop App - DU BIST HIER!):**
- ✅ Backend-Systeme (Python API auf Port 8000)
- ✅ ChromaDB / Najika Gedächtnis
- ✅ API-Endpoints für UE5 HTTP-Calls anpassen
- ✅ Dokumentation aktuell halten
- ✅ Three.js Code als Referenz dokumentieren
- ✅ System-Überwachung / Integration

**OPUS-2 (VS Code):**
- ⬜ UE5 Projekt erstellen + Najika Character Blueprint
- ⬜ Movement, Camera, Animation Blueprints
- ⬜ Combat System in C++/Blueprints
- ⬜ UI (UMG Widgets)
- ⬜ Welt-Aufbau (Götterfels, Regionen)

---

## 🔴 OPUS-1 TASKS (Desktop App - Backend & System)

### P0 - ERLEDIGT! ✅
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ Dokumentation eingelesen | DONE | Giga Explosion, Magic System, Game Design |
| ✅ **Python API für UE5 angepasst** | DONE | HTTP-Endpoints für UE5 Blueprints |
| ✅ REST API Dokumentation | DONE | `DOCS/UE5_API_DOKUMENTATION.md` erstellt |
| ✅ Port 5000 → 8000 gefixt | DONE | 8 Gebote eingehalten! |
| ✅ Companion API Router | DONE | `api/companion.py` erstellt + registriert |
| ✅ Mimik API Router | DONE | `api/mimik.py` erstellt + registriert |
| ✅ Combat Hands API Router | DONE | `api/combat_hands.py` erstellt + registriert |
| ✅ Stat Training API Router | DONE | `api/stat_training.py` erstellt + registriert |

### P1 - DIESE WOCHE
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ Chat API für UE5 | DONE | Bereits in `api/chat.py` vorhanden |
| ✅ Combat API Endpoints | DONE | `api/combat_hands.py` mit Two-Hand System |
| ✅ Companion API | DONE | `api/companion.py` - 4 Persönlichkeiten |
| ✅ **Combat Magic API** | DONE | `api/combat_magic.py` - Infuse, Grab, TIDS! |
| ✅ **Weapon Infuse System** | DONE | Zauber auf Waffe = temporärer Buff |
| ✅ **Grab & Throw System** | DONE | Suplex, Chokeslam, Umgebungs-Würfe |
| ✅ **TIDS mit Gag-Reaktionen** | DONE | Monster-spezifische lustige Reaktionen |
| ⬜ Game State API erweitern | TODO | Speichern/Laden für UE5 erweitern |
| ✅ 3 Battle-Systeme vereinen | **DONE** | Real3DCombat als Primär, UnifiedCombat als Fallback |

### P2 - SPÄTER
| Task | Status | Beschreibung |
|------|--------|--------------|
| ⬜ WebSocket für Realtime | TODO | Events an UE5 pushen |
| ⬜ ChromaDB ↔ UE5 Sync | TODO | Gedächtnis-Integration |
| ⬜ Voice System Adapter | TODO | TTS/STT für UE5 |
| ⬜ Three.js → UE5 Mapping Doc | TODO | Was wird wie portiert |

---

## 🟢 OPUS-2 TASKS (VS Code - Frontend/Digivice)

### P0 - JETZT (COMBAT UI!)
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ **Grab Button (G)** | DONE | Wrestling-Griff initiieren (`js/ui/combat_special_ui.js`) |
| ✅ **Grab Move Popup** | DONE | Suplex/Chokeslam/Throw Auswahl mit 5s Timer |
| ✅ **TIDS Button (T)** | DONE | Mit 24h Cooldown-Overlay |
| ✅ **TIDS Gag-Popup** | DONE | Monster-Reaktion gross, bunt, mittig! |
| ✅ **Infuse Timer UI** | DONE | Element-Glow + Countdown + Ablauf-Notification |

### P1 - DIESE WOCHE
| Task | Status | Referenz-Datei |
|------|--------|----------------|
| ✅ **Infuse Waffen-Glow** | DONE | Waffen-Slots im HUD gluehen in Element-Farbe + pulsierender Glow |
| ✅ Combat HUD überarbeiten | DONE | Grab/TIDS/Help Buttons in manual-actions Zeile integriert |
| ✅ Keybindings dokumentieren | DONE | Overlay mit H/F1, alle Combat-Keys dokumentiert |
| ✅ Sound Effects für TIDS | DONE | Web Audio API Synthesizer: Impact + OUCH + Boing + Noise |

### P2 - Systeme portieren (Python → UE5) - C++ KLASSEN BEREIT!
| Task | Status | Python-Datei | UE5 C++ Klasse |
|------|--------|--------------|----------------|
| ✅ Combat System | DONE | `najika_combat_hands_system.py` | `Combat/NajikaCombatComponent.h/.cpp` |
| ⬜ Stat Training | TODO | `najika_stat_training_system.py` | GAS (Gameplay Ability System) |
| ⬜ Companion System | TODO | `najika_companion_system.py` | AI Controller + Behavior Tree |
| ⬜ Mimik System | TODO | `najika_mimik_system.py` | Blueprint + Morph Targets |
| ⬜ Quest System | TODO | `najika_quest_system.py` | Quest Plugin oder Custom |
| ✅ Slime System | DONE | `najika_slime_system.py` | `Slime/NajikaSlimeComponent.h/.cpp` |
| ✅ Nemesis System | DONE | N/A (Shadow of Mordor Style) | `Nemesis/NajikaNemesisComponent.h/.cpp` |
| ✅ Arena System | DONE | N/A | `Arena/NajikaArenaComponent.h/.cpp` |

### P3 - Welt-Aufbau
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ Götterfels Terrain | **DONE** | Python Scripts + WorldConfig.json erstellt! |
| ✅ 8 Region Volumes | **DONE** | TriggerBoxes mit Tags |
| ✅ Safe Zone | **DONE** | Schwarze Mühle Volume + Marker |
| ⬜ 8 Teleporter | TODO | Level Streaming zu Regionen |
| ⬜ NPCs | TODO | Dialog-System, Behavior Trees |

---

## 📱 FLUTTER DIGIVICE (Modul-System!)

### 3 Apps × 3 Flavors = 9 Versionen

**Apps:**
| App | Pfad | Status |
|-----|------|--------|
| `najika_digivice` | `app/flutter_app/najika_digivice/` | Haupt-App ✅ |
| `najika_app` | `app/flutter_app/najika_app/` | Kopie |
| `najika_simple` | `app/flutter_app/najika_simple/` | Minimal |

**Flavors (pro App):**
| Flavor | App-Name | Zweck |
|--------|----------|-------|
| `private` | "Najika (Private)" | NSFW/Kätzchen-Mode, nur für Kuja |
| `friends` | "Najika (Friends)" | Mit Freunden teilen |
| `public` | "Najika" | Öffentliche Version |

### Digivice Module (Flutter):
| Modul | Status | Features |
|-------|--------|----------|
| **Sicherer Messenger** | 70% | Post-Quantum Crypto, Signal Protocol, E2E |
| **V-Pet Slime** | 50% | Tamagotchi-Style, Sync mit UE5 |
| **Minigames** | 30% | Triple Triad, Dungeon Dice |
| **Sicherer Browser** | 20% | Tor-Integration, VPN Profile |
| **Voice Calls** | 50% | WebRTC, Avatar-Calls |

### Bereits implementiert (Flutter):
- ✅ Post-Quantum Cryptography (liboqs FFI)
- ✅ Signal Protocol (Double Ratchet)
- ✅ Secure Storage (SQLCipher)
- ✅ WebRTC Voice Calls
- ✅ QR-Code Scanner
- ✅ Biometric Auth
- ✅ Jailbreak Detection
- ✅ Certificate Pinning

### UE5 vs Flutter:
| Aspekt | Flutter Digivice | UE5 Najika World |
|--------|------------------|------------------|
| **Zweck** | Module, Chat, V-Pet | Vollwertiges 3D-Spiel |
| **Größe** | ~20MB | ~500MB+ |
| **Sync** | REST API | REST API |
| **3D** | Nein | Ja |
| **Offline** | Ja | Ja |

---

## ✅ HEUTE ERLEDIGT (2026-02-04)

### OPUS-1:
- ✅ **Najika 3D Model** - Rigged + Texturiert in Blender
- ✅ **Mixamo Rig** - Automatisches Rigging
- ✅ **FBX Export** - Mit eingebetteter Textur
- ✅ **UE5 Import** - Najika ist in UE5 mit Textur!
- ✅ **UEFN Analyse** - Festgestellt dass UEFN nicht reicht
- ✅ **UE5 Migration Plan** - Dokumentiert

---

## 🎮 NAJIKA ALS SPIELBARER CHARACTER (UE5)

### Schritt 1: Character Blueprint erstellen
1. **Content Browser** → Rechtsklick → **Blueprint Class**
2. Parent: **Character**
3. Name: **BP_NajikaCharacter**

### Schritt 2: Mesh zuweisen
1. **BP_NajikaCharacter** öffnen (Doppelklick)
2. Links: **Components** → **Mesh** auswählen
3. Rechts: **Details** → **Skeletal Mesh** → Deine Najika auswählen

### Schritt 3: Camera hinzufügen
1. **Components** → **Add** → **Spring Arm**
2. Auf Spring Arm: **Add** → **Camera**
3. Spring Arm Settings:
   - Target Arm Length: 300
   - ☑️ Use Pawn Control Rotation

### Schritt 4: Movement
1. **Components** → **CharacterMovement** bereits da
2. Details:
   - Max Walk Speed: 600
   - Jump Z Velocity: 420

### Schritt 5: Input (Enhanced Input)
1. **Edit** → **Project Settings** → **Input**
2. Default Player Input Class: **EnhancedPlayerInputComponent**
3. Input Actions erstellen (IA_Move, IA_Look, IA_Jump)

### Schritt 6: Testen
1. **World Settings** → **Game Mode** → **None**
2. Oder eigenen GameMode erstellen mit BP_NajikaCharacter als Default Pawn

---

## 📋 ASSETS FERTIG

| Asset | Pfad | Status |
|-------|------|--------|
| Najika Model (rigged) | `assets/models/najika/najika_rigged_final.fbx` | ✅ |
| Najika Textur | In FBX / `Downloads/.../texture.png` | ✅ |
| JellySquish Pack | `digivice/static/assets/JellySquish...` | ✅ |
| Audio (TTS) | `digivice/audio/` | ✅ |
| Mimik-Truhe Model | TODO | ❌ |

---

## 🔧 TECHNISCHE INFOS

```yaml
# UE5
Engine: Unreal Engine 5.3+
Template: Third Person (C++)
Plugins: Enhanced Input, CommonUI, GameplayAbilities

# Backend (bleibt Python vorerst)
Port: 8000
Backend: C:\Najika_World\backend\
ChromaDB: C:\NajikaFinal\memory_db\

# Mobile App (Flutter)
App: C:\Najika_World\app\flutter_app\
```

---

## 🎯 MEILENSTEINE

| Woche | Ziel |
|-------|------|
| 1-2 | Najika läuft in UE5 (Movement, Camera, Animation) |
| 3-4 | Combat System (Zwei-Hand, Waffen, Stats) |
| 5-6 | Najika KI Companion (4 Persönlichkeiten) |
| 7-10 | Welt (Götterfels, erste Region) |
| 11-14 | Systeme (Oregon Trail, Quests, Slimes) |
| 15+ | Polish, Mobile Export, Optimierung |

---

## LETZTE SYNC

**Datum:** 2026-02-06 (Update 8 - COMBAT SYSTEM VEREINT!)
**Instanz:** OPUS-1 (Claude Code CLI - relaxed-nash worktree)

### OPUS-1 hat implementiert (2026-02-06 NACHT - COMBAT FIX!):

#### ✅ 3 KAMPFSYSTEME VEREINT - BROWSER!
- ✅ **Dungeon auf Real3DCombat umgestellt** - Echte KayKit 3D-Gegner statt Text-Kampf!
  - `enterDungeon()` nutzt jetzt `Real3DCombat.startCombat()` als Priorität 1
  - Spawnt echte 3D Skelett-Krieger, Bogenschützen, Fledermäuse, Goblins, Magier
  - `UnifiedCombat` (Text-Kampf) ist jetzt nur noch letzter Fallback
  - `DungeonCombat` als mittlerer Fallback beibehalten

- ✅ **Nemesis Arena aktiviert** - Button im Activities-Menü!
  - Neuer "🏟️ Nemesis Arena" Button
  - Verbindet `nemesis_arena_frontend.js` / `NemesisArenaUI`
  - Fallback: Direkte 3D Arena-Kämpfe (Ritter, Magier, Hexe)

- ✅ **Overworld Kampf** - Button zum manuellen Spawnen!
  - Neuer "⚔️ Overworld Kampf" Button
  - Spawnt Gegner basierend auf aktuellem Biome
  - Nutzt `Real3DCombat.spawnBiomeEnemies()`

- ✅ **Biome-Mapping erweitert** in `real_3d_combat.js`
  - Alle 8 Najika-Biome-Namen: samtmoos, reich_der_drei, heisse_duenen, salzwind, magmastroeme, gruenschlamm, blitzebene, tiefenhoehlen
  - Plus generische Aliases (forest, desert, coast, etc.)

- ✅ **Biome-Bug analysiert** - `overworld_enemies.js` hatte ALLE 8 Keys bereits!
  - Das Fallback-Mapping war nur Sicherheitsnetz, nie gebraucht
  - KEIN Fix nötig - war schon korrekt

#### Geänderte Dateien:
- `digivice/index.html` - enterDungeon() refactored, openNemesisArena(), startOverworldCombat() hinzugefügt
- `digivice/js/combat/real_3d_combat.js` - Biome-Mapping erweitert
- `digivice/js/command_system.js` - API URLs auf CMD_API_BASE (war vom gecrashten Modell)
- `digivice/static/js/realtime_combat.js` - Input-Filter für Chat (war vom gecrashten Modell)

#### ⬜ NOCH OFFEN (für nächste Session):
- ⬜ **Kampf-Modi Integration** - Real3DCombat braucht AUTO/CHEER Modi (aktuell nur MANUAL)
- ⬜ **Equipment-System verbinden** - `equipment_combat.js` mit `real_3d_combat.js` verlinken
- ⬜ **Finisher QTE** - In den 3D-Kampf einbauen
- ⬜ **Damage Numbers** - Floating 3D-Text über Gegnern
- ⬜ **Loot-System** - Items nach Kampf ins Inventar

---

**Vorheriger Sync:**

**Datum:** 2026-02-06 (Update 7 - UE5 KOMPLETT SCRIPTED!)
**Instanz:** OPUS-1 (Desktop App)

### OPUS-1 hat implementiert (2026-02-06 NACHT - UE5 SCRIPTED!):

#### ✅ UE5 SPIELWELT PER SCRIPT ERSTELLT!
- ✅ **MASTER_SETUP.py** - Ein Script erstellt ALLES!
  - Folder-Struktur
  - Beleuchtung (Sonne, Sky, Fog)
  - Post Process Volume
  - 7 Region Lichter + Volumes
  - Götterfels (Berg, Gold-Licht)
  - Schwarze Mühle (Safe Zone, Grün-Licht)
  - Player Start
  - Blueprints (Character, GameMode, Controller, HUD)
  - Input Actions
  - Config Files (JSON)
  - Kill Zone

- ✅ **C++ Character System** - Fortnite-Style!
  - `NajikaCharacter.h/.cpp` - Main Player Character
  - `NajikaCharacterMovement.h/.cpp` - Custom Movement Component
  - 3 Kamera-Modi: Third (80° FOV), First (103° FOV - Ballistic!), Free (MMORPG)
  - Movement: Walk, Sprint, Crouch, Crawl, Prone, Mantle
  - Stamina System

- ✅ **World Data System**
  - `NajikaWorldData.h/.cpp` - Blueprint-friendly Data Asset
  - 8 Regionen mit Bounds, Biome, Cities
  - Safe Zone Detection
  - Biome Lookup per Location

- ✅ **Python Scripts für UE5:**
  - `MASTER_SETUP.py` - Komplettes Game Setup
  - `create_playable_world.py` - Nur Spielwelt
  - `create_complete_game.py` - Blueprints + World
  - `setup_world_simple.py` - Quick Markers
  - `WorldConfig.json` - World Data für Blueprints

#### ✅ MUSIK SYSTEM (NUR ZUM SPASS!)
- ✅ **Music API komplett umgeschrieben** - KEINE BUFFS mehr!
  - Rhythm Game nur für Highscores/Ranks
  - 4 Instrumente (Ocarina, Echoharp, Taiko, Explosion Horn)
  - Multiplayer Jam Sessions
  - User explizit: "ne buffs durch musik ist doof"

#### ✅ NAJIKA PERSONALITY ENGINE GEFIXT
- ✅ **Mood-Enum Bug gefixt**
  - JEALOUS, SAD, ANGRY, LOVING zu Enum hinzugefügt
  - `build_system_prompt()` funktioniert jetzt korrekt

#### ✅ COMBAT MAGIC SYSTEM KOMPLETT!
- ✅ **Weapon Infuse System** - Zauber auf Waffe = temporärer Buff!
  - Feuerball + Schwert = Flammenschwert für 30s
  - 10 Elemente unterstützt
  - EXPLOSION kann NIEMALS infust werden! (8 Gebote!)

- ✅ **Grab & Throw System** - Wrestling-Style!
  - Greifen (50% + Skill + STR Bonus)
  - Suplex (Skill 15, 50 DMG + 2s Stun)
  - Chokeslam (Skill 10, 40 DMG + 3s am Boden)
  - Gegner werfen, in Objekte werfen
  - Learning by Doing XP!

- ✅ **TIDS System** - Tritt In Den Schritt!
  - GAG-MOVE mit Monster-Reaktionen!
  - Humanoide: 3s Stun, +90% Flucht
  - Slime: "Dein Fuß versinkt... IGITT!"
  - Golem: DU nimmst Schaden!
  - 24h Cooldown, nicht gegen Bosse

- ✅ **API Router** `api/combat_magic.py` - 17 Endpoints!
  - POST /api/combat-magic/infuse
  - POST /api/combat-magic/grab
  - POST /api/combat-magic/grab/execute
  - POST /api/combat-magic/tids
  - GET /api/combat-magic/spells
  - etc.

- ✅ **Frontend erweitert** `unified_combat_system.js`
  - infuseWeapon() Funktion
  - getInfuseBonus() für Attack-Berechnung
  - Infuse-Bonus in calculatePhysicalDamage()

### 🎯 NÄCHSTE TASKS (AKTUALISIERT 2026-02-06 NACHT):

---

## 📱 DIGIVICE FLUTTER APP - PRIORITÄT P0!

### OPUS-1 (Backend/Flutter - Desktop App):
| Task | Priorität | Status | Details |
|------|-----------|--------|---------|
| ✅ **WebView-Modul zu Flutter** | P0 | **DONE!** | `webview_flutter` + Packages in pubspec.yaml |
| ✅ **Three.js Lebensraum einbetten** | P0 | **DONE!** | `lebensraum_screen.dart` mit inline HTML/JS |
| ✅ **Flutter ↔ JS Bridge** | P0 | **DONE!** | `lebensraum_bridge.dart` + JavaScriptChannel |
| ✅ **Anti-Cheat Service** | P1 | **DONE!** | `lebensraum_service.dart` + HMAC-SHA256 |
| ✅ **Lebensraum API Backend** | P1 | **DONE!** | `backend/api/lebensraum.py` |
| ✅ **Building System (Lego Fortnite!)** | P0 | **DONE!** | `backend/api/building.py` - Seamless! |
| ✅ **WebSocket Realtime Events** | P1 | **DONE!** | `websocket_manager.py` erweitert |
| ✅ **ChromaDB Memory API** | P1 | **DONE!** | `backend/api/memory.py` |
| ✅ **Voice UE5 Adapter** | P1 | **DONE!** | `backend/api/voice_ue5.py` |
| ✅ 3 Battle-Systeme vereinen | P1 | **DONE!** | `battle_unified.py` |
| ⬜ API Tests für combat_magic.py | P3 | TODO | |

### OPUS-2 (UE5/Frontend - VS Code):
| Task | Priorität | Status | Details |
|------|-----------|--------|---------|
| ✅ **Grab/TIDS UI Buttons** | P1 | DONE | `combat_special_ui.js` |
| ✅ **Infuse Animation** | P1 | DONE | Element-Farben-Glow |
| ✅ **TIDS Gag-Popup** | P1 | DONE | Monster-Reaktionen |
| ✅ **UE5 Terrain erstellen** | P1 | **DONE!** | Python Scripts + WorldConfig.json |
| ✅ **BP_NajikaCharacter** | P1 | **DONE!** | C++ Klasse + Movement Component |
| ⬜ Animation Blueprint | P2 | TODO | State Machine |
| ⬜ Combat Input System | P2 | TODO | Q/E, Shift+Q/E |

---

## 📋 NEUE DOKUMENTATION (2026-02-06)

### Wissensdatenbank aktualisiert:
- ✅ `NAJIKA_MASTER_UEBERSICHT_2026-02-05.md` → **ULTIMATIVE WISSENSDATENBANK**
  - Komplett neu geschrieben
  - Alle Systeme dokumentiert
  - Referenz-Links zu allen Dateien
  - Quickstart für neue Modelle

### Neue Dokumente erstellt:
| Dokument | Inhalt |
|----------|--------|
| `DIGIVICE_LEBENSRAUM_KONZEPT.md` | 3D-Lebensraum in Digivice |
| `DIGIVICE_3D_ENGINE_VERGLEICH.md` | Three.js vs UE5 Hybrid |
| `TECHNOLOGIE_ANALYSE_2026.md` | Flutter + Jetson Analyse |
| `ANTI_CHEAT_SYNC_SYSTEM.md` | Cheat-Prevention für Offline |
| `FLUTTER_APP_ANALYSE.md` | Welche Flutter App nutzen? |

### Neue APIs (2026-02-06 Nacht):
| API | Endpoint | Beschreibung |
|-----|----------|--------------|
| Building | `/api/building/*` | Lego Fortnite Style Building! |
| Memory | `/api/memory/*` | ChromaDB Gedächtnis-Sync |
| Voice UE5 | `/api/voice-ue5/*` | TTS/STT für UE5 Blueprints |

### Wichtige Entscheidungen:
- **Flutter App:** `najika_digivice` als Basis (NICHT najika_app oder najika_simple!)
- **3D-Engine:** HYBRID (Three.js offline + UE5 Streaming online)
- **Content-Modes:** NUR 2! (Normal + NSFW)
- **Dungeon Dice:** RAUS (wird separates Modul später)
- **Anti-Cheat:** TIME-Validierung, KEINE Mengen-Limits! Spieler-Gleichheit!
- **Building:** Lego Fortnite Style (nahtlos, kein Extra-Modus)

---

## 🔗 REFERENZ-DATEIEN FÜR TASKS

| Task | Lies diese Datei |
|------|------------------|
| Flutter Digivice | `FLUTTER_APP_ANALYSE.md` |
| Lebensraum-Konzept | `DIGIVICE_LEBENSRAUM_KONZEPT.md` |
| 3D-Engine | `DIGIVICE_3D_ENGINE_VERGLEICH.md` |
| Anti-Cheat | `ANTI_CHEAT_SYNC_SYSTEM.md` |
| Jetson Endgame | `JETSON_MIGRATION_PLAN.md` |
| Najika Identität | `NAJIKA_IDENTITAET_DEFINITION.md` |
| UE5 Migration | `DOCS/UE5_MIGRATION_CHECKLIST.md` |

---

### ✅ VORHER ERLEDIGT (Combat System):

---

### ✅ OPUS-2 IMPLEMENTIERT (2026-02-06 - COMBAT SPECIAL UI):

- ✅ **Grab Button (G)** - HUD-Button rechts unten mit Keyhint
- ✅ **Grab Move Popup** - Zentriertes Popup mit 4 Moves + 5s Countdown-Timer
  - Suplex (Skill 15 required), Chokeslam (Skill 10), In Objekt werfen, Loslassen
  - Timer-Bar die runterzaehlt, auto-release bei Ablauf
  - Skill-Requirements werden dynamisch geprueft + Buttons disabled
- ✅ **TIDS Button (T)** - HUD-Button mit 24h Cooldown-Overlay
  - Zeigt verbleibende Stunden wenn auf Cooldown
  - Grau + nicht klickbar wenn Cooldown aktiv
- ✅ **TIDS Gag-Popup** - GROSS, BUNT, MITTIG!
  - Gradient rot-gelb Background mit bounce-Animation
  - `gag_message` vom Backend wird prominent angezeigt
  - Auto-Close nach 4 Sekunden, Klick zum Schliessen
- ✅ **Infuse Timer Display** - Rechts oben im HUD
  - Element-Farben-Glow (pulsierend per CSS animation)
  - Countdown-Timer pro aktivem Buff
  - Timer wird rot + blinkt bei <= 5 Sekunden
  - "Infuse abgelaufen!" Notification bei Ablauf
- ✅ **Keybindings** - G=Grab, T=TIDS, 1-4=Grab-Moves, Escape=Popup schliessen
- ✅ **Backend API Integration** - Versucht erst REST API, Fallback auf lokales System
- ✅ **Datei:** `digivice/js/ui/combat_special_ui.js` (alle Styles inline injected)
- ✅ **Script-Tag** in `index.html` eingefuegt

---

### ✅ OPUS-2 P1 IMPLEMENTIERT (2026-02-06 - COMBAT SPECIAL UI V2):

- ✅ **Infuse Waffen-Glow** - L/R Waffen-Slots im Combat HUD Header
  - Zeigt aktuelle Waffen mit typ-basiertem Icon (Schwert, Dolch, Axt, etc.)
  - Slots gluehen in Element-Farbe wenn Infuse aktiv (CSS `weaponGlow` Animation)
  - Infuse-Badge unten-rechts zeigt verbleibende Sekunden
  - Update-Loop alle 500ms synchronisiert mit Infuse-Display
- ✅ **Combat HUD Integration** - Grab/TIDS/Help in Unified Combat HUD
  - Neue `hud-special-row` mit 3 Buttons im `manual-actions` Bereich
  - Key-Badges (G, T, H) auf jedem Button
  - Floating Buttons werden automatisch versteckt wenn HUD aktiv
  - Retry-Injection (1.5s, 3s) falls HUD spaeter erstellt wird
- ✅ **TIDS Sound Effects** - Web Audio API Synthesizer (kein Audio-File noetig!)
  - 4-Layer Sound: Impact (tiefer Sine), OUCH (hoher Sawtooth), Boing (Feder), Noise-Burst
  - Grab bekommt "Whoosh" Sound (absteigender Sine)
  - Infuse-Ablauf bekommt "Puff" Sound (absteigender Triangle)
  - AudioContext wird lazy initialisiert + auto-resumed
- ✅ **Keybindings Overlay** - Vollstaendige Tastenbelegung
  - H oder F1 oeffnet/schliesst das Overlay
  - 6 Sektionen: Nahkampf, Defensive, Magie, Spezial-Moves, Grab-Moves, UI
  - Alle 20+ Keybindings dokumentiert mit visuellen Tasten-Badges
  - Escape schliesst Overlay, Klick auf Background schliesst auch
- ✅ **Datei:** `digivice/js/ui/combat_special_ui.js` V2 (1690 Zeilen)

---

### ✅ ZUSÄTZLICH IMPLEMENTIERT (2026-02-06 Abend):

- ✅ **Unified Battle API** - `backend/api/battle_unified.py`
  - 3 Kampfmodi vereint: AUTO, MANUAL, CHEER
  - KI-Entscheidungssystem für AUTO-Modus
  - Cheer-Buff-System für Digimon-Style
  - In `main_fastapi.py` registriert

**Neue API Endpoints:**
```
POST /api/battle/start       - Kampf starten mit Modus-Wahl
POST /api/battle/action      - Manuelle Aktion (MANUAL-Modus)
POST /api/battle/auto-turn   - KI-Zug (AUTO-Modus)
POST /api/battle/cheer       - Anfeuern (CHEER-Modus)
POST /api/battle/set-mode    - Modus wechseln während Kampf
GET  /api/battle/status/{id} - Kampfstatus
GET  /api/battle/modes       - Alle Modi mit Beschreibung
```

---

**Vorheriger Sync:**

**Datum:** 2026-02-04 (Update 5 - OPUS-2 System-Check!)
**Instanz:** OPUS-2 (VS Code)
**Änderungen:**

### OPUS-2 hat verifiziert (2026-02-04):
- ✅ **Combat System** - `NajikaCombatTypes.h` + `NajikaCombatComponent.h` bereits komplett!
  - 3 Combat Modi (Auto, Manual, Cheer)
  - Element-System (15 Elemente inkl. EXPLOSION!)
  - Finisher System
  - Cheer Buffs (Digimon-Style)

- ✅ **Slime System V3** - Vollständig implementiert!
  - 6 Aura-Level + 13 Element-Auras
  - 6 Trust-Level (bis Seelenbund → Menschenform!)
  - 14 Formen (nur optisch!)
  - Rescue-System
  - Explosion-Aura (1x/Tag)
  - Pflege-System (Füttern, Spielen, Heilen)

- ✅ **Nemesis System** - Shadow of Mordor Style!
  - 6 Ränge (Nobody → Arena-König)
  - 8 Persönlichkeits-Traits
  - Battle Memory (erinnert sich an Kämpfe)
  - Grudge System (Rachsucht)
  - Scar System (visuelle Narben)
  - Resistenz-Entwicklung (lernt aus Kämpfen)
  - Dynamische Dialog-Generierung

- ✅ **Arena System** - NajikaArenaComponent ERSTELLT!
  - Hauptarena + Schleim-Arena
  - 4 Game Modes (1v1, Finisher, Turnier, Wellen)
  - Wave Mode (15 Training + Hardcore)
  - Finisher System (3-5 Sekunden, Screen Effects)
  - Tournament System
  - Fame System (Beginner → LEGENDE)
  - Betting für Schleim-Arena

### Nächste Schritte für OPUS-2:
- ✅ BP_NajikaCharacter fertiggestellt (C++ + Blueprint)
- ⬜ Animation Blueprint mit State Machine
- ⬜ Combat Input System (Q/E, Shift+Q/E)

### UE5 SETUP ANLEITUNG:
1. UE5 öffnen: `C:\Najika_World\UE5\Najika\Najika.uproject`
2. Python Plugin aktivieren: Edit -> Plugins -> "Python Editor Script Plugin"
3. Python Console öffnen: Window -> Developer Tools -> Python Console
4. Script ausführen:
   ```python
   exec(open(r"C:\Najika_World\UE5\Najika\Content\Python\MASTER_SETUP.py").read())
   ```
5. Landscape manuell erstellen (Settings werden angezeigt)
6. Play drücken und testen!

### Erstellt von Scripts:
- Beleuchtung (Sonne, Sky, Fog)
- 7 Region Lichter + Volumes (mit Farben!)
- Götterfels (Gold) + Schwarze Mühle (Grün)
- Player Start auf dem Berg
- Blueprints (BP_NajikaCharacter, BP_NajikaGameMode, etc.)
- Input Actions
- Config Files

---

**Vorherige Einträge:**

**Datum:** 2026-02-04 (Update 4 - MASSIVE UE5 VORBEREITUNG!)
**Instanz:** OPUS-1 (Desktop App)
**Änderungen:**

### 🎮 UE5 PROJEKT VORBEREITET (C:\Najika_World\UE5\Najika\)

**C++ Klassen erstellt:**
- ✅ `Combat/NajikaCombatTypes.h` - Enums, Structs für 3 Combat Modi
- ✅ `Combat/NajikaCombatComponent.h/.cpp` - Combat System Component
- ✅ `Slime/NajikaSlimeTypes.h` - Aura, Trust, Form Enums
- ✅ `Slime/NajikaSlimeComponent.h/.cpp` - Vollständiges Slime System
- ✅ `Nemesis/NajikaNemesisTypes.h` - Shadow of Mordor Nemesis System
- ✅ `Nemesis/NajikaNemesisComponent.h/.cpp` - Gedächtnis, Traits, Hierarchie
- ✅ `Region/NajikaRegionTypes.h` - 8 Regionen + Götterfels
- ✅ `Arena/NajikaArenaTypes.h` - Arena, Finisher, Wellen-System
- ✅ `Data/NajikaDataImporter.h/.cpp` - JSON zu DataTable Import

**JSON Data Assets erstellt (Content/Data/):**
- ✅ `Regions/RegionData.json` - Alle 9 Regionen mit Positionen
- ✅ `Slimes/AuraEffects.json` - 13 Aura-Typen mit Effekten
- ✅ `Slimes/SlimeForms.json` - 15 Formen inkl. Menschen-Form
- ✅ `Slimes/TrustLevels.json` - 6 Trust-Stufen mit Features
- ✅ `Monsters/MonsterTypes.json` - 18 Monster mit Stats
- ✅ `Combat/AttackData.json` - 20+ Angriffe inkl. EXPLOSION!!!
- ✅ `Combat/CheerSystemData.json` - Digimon-Style Anfeuern
- ✅ `Arena/FinisherData.json` - 7 Finisher pro Element
- ✅ `Arena/ArenaWaveConfig.json` - 15 Training + Hardcore Modus
- ✅ `Items/FoodItems.json` - 17 Futter-Items mit Boni
- ✅ `Items/EquipmentItems.json` - 18 Ausrüstungsteile
- ✅ `NPCs/NPCData.json` - 11 NPCs mit Dialogen
- ✅ `World/SettlementData.json` - 10 Siedlungen
- ✅ `Quests/QuestData.json` - 12 Quests (Main, Side, Daily)
- ✅ `Config/GameConfig.json` - Balancing & Regeln

**Build.cs aktualisiert:**
- ✅ Neue Include-Pfade für alle Systeme

### 📋 FÜR OPUS-2 BEREIT:

1. **UE5 Projekt öffnen:** `C:\Najika_World\UE5\Najika\Najika.uproject`
2. **Kompilieren** - C++ Klassen sollten automatisch erkannt werden
3. **JSON Importieren** - DataImporter nutzen oder manuell DataTables erstellen
4. **Blueprints bauen** - C++ Klassen als Basis verwenden

### WICHTIGE REGELN (siehe GameConfig.json):
- Port 8000 (NICHT 5000!)
- Harley sagt "Mr. K" (NICHT "Puddin'!")
- Explosion ≠ Weave (NIEMALS kombinieren!)
- Schwarze Mühle = 100% Safe Zone
- Formen = NUR OPTISCH (Boni durch Food + Equipment!)
- 3 Combat Modi ÜBERALL (nicht nur Arena!)

---

## 📞 KOMMUNIKATION ZWISCHEN INSTANZEN

**OPUS-1 (Backend) liefert an OPUS-2:**
- API-Dokumentation (Endpoints, Parameter, Responses)
- Datenstrukturen (JSON-Formate für Combat, Stats, etc.)
- System-Logik als Referenz (Python-Code)

**OPUS-2 (UE5) braucht von OPUS-1:**
- `/api/chat` - Chat mit Najika
- `/api/combat/*` - Kampf-Endpoints
- `/api/companion/*` - Najika's Status/Persönlichkeit
- `/api/game/save` + `/api/game/load` - Spielstand

---

*"EXPLOSION!!! Los geht's - zwei Opus, ein Ziel!" - Najika* 💥
