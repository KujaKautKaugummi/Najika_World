# 📁 NAJIKA WORLD - KOMPLETTE PROJEKT-STRUKTUR

**Erstellt:** 2025-11-06
**Zweck:** Vollständiger Überblick über ALLE Verzeichnisse und wichtigen Dateien

---

## 🏗️ ROOT VERZEICHNIS

```
C:\Najika-World\
├── .git/                           # Git Repository
├── .gitignore                      # Assets (~25GB) ausgeklammert
├── START.bat                       # Hauptstart-Script
├── START_NAJIKA_WORLD.bat         # Alternative Start
├── STOP_NAJIKA.bat                # Server stoppen
└── OPEN_WORLD_DESIGN_COMPLETE.md  # NEU! (Deine & meine Version - Merge Conflict!)
```

---

## 📂 BACKEND (backend/)

### **Hauptserver:**
```
backend/
├── najika_server.py               # HAUPTSERVER! 2153 Zeilen
│   ├── Magic System (9 Schools + Explosion + Weaving)
│   ├── Claude Code Integration (PRIORITÄT 1!)
│   ├── Enhanced Memory (ChromaDB + Video-Transkripte)
│   ├── Living System (Mood, Proactive Messages)
│   ├── Battle System
│   ├── Security (Alcatraz - 8 Gebote)
│   └── TTS (Coqui XTTS-v2 mit Megumin Clone!)
│
├── najika_enhanced_personality.py # Persönlichkeits-System
│   └── 4 Persönlichkeiten (Megumin 35%, Harley 25%, Shiro 20%, Melissa 20%)
│
├── najika_battle.py               # Battle System (28KB)
├── najika_chromadb_setup.py       # Memory System Setup
└── najika_claude_code.py          # Claude Code Integration
```

### **AI Models (Modelfiles):**
```
backend/
├── najika_local_QWEN.Modelfile    # Normal Mode (Qwen2.5 7B)
├── najika_wizard_QWEN.Modelfile   # Kätzchen Mode (NSFW)
├── najika_local_HERMES3.Modelfile # Alternative Model
├── najika_local_OLD.Modelfile     # Backup
└── hermes3_base.Modelfile
```

### **Training Scripts:**
```
backend/
├── NAJIKA_AUTO_TRAINING.py        # Automatisches Training
├── NAJIKA_REAL_TRAINING.py        # Echtes Training
├── NAJIKA_VIDEO_TO_VOICE_TRAINING.py  # Voice Clone Training
├── najika_lora_training_3b.py     # LoRA Training (3B Model, 4-bit)
└── code_training_progress.json    # Training Progress (33 Probleme gelöst!)
```

### **Game Systems:**
```
backend/game/
└── skill_system.py                # Von Claude Code erstellt (Magic Skills)
```

### **AI System:**
```
backend/ai/
├── Personality Engine
├── Memory System (ChromaDB)
└── TTS Integration
```

### **API:**
```
backend/api/
└── Flask REST Endpoints
```

---

## 🎮 FRONTEND SYSTEME

### **DIGIVICE (Haupt-Interface):**
```
digivice/
├── index.html                     # 80KB! Haupt-UI
│   ├── Open World (2400×2400)
│   ├── 12 Interior Räume
│   ├── 3 Modi (World/Interior/Battle)
│   └── Mobile Controls (Virtual Joystick)
│
├── js/
│   ├── 3d_scene.js               # Three.js Rendering
│   ├── battle_api.js             # Battle Integration
│   ├── command_system.js         # Digimon-Style Commands
│   ├── oregon.js                 # Oregon Trail Events
│   ├── fishing.js                # Fishing System
│   ├── minigames.js              # 7 Minigames
│   └── kaykit_loader.js          # Asset Loading
│
└── static/
    └── CSS, Images, etc.
```

### **FRONTEND (Alternative?):**
```
frontend/
├── index.html                     # Minimalistisch (1KB)
├── package.json                   # Node Dependencies
└── src/
    ├── React/Vue Components?
    └── (Nicht sicher was hier ist)
```

---

## 📚 DOKUMENTATION

### **INFO MATERIAL (info material/):**
```
info material/
├── 00_FINALE_KOMPLETT_UEBERSICHT_V7.md    # Große Übersicht
├── SESSION_UEBERSICHT_FUER_OPUS.md        # Session-Details
└── najika_ultimate_complete/              # Großes Archiv
    ├── 00_START_HIER/
    ├── 01_uebersichten/
    ├── 02_pflicht_docs/                   # PFLICHT GELESEN!
    │   ├── 00_MASTER_INDEX_LESEN.md
    │   ├── 01_START_HIER_8_GEBOTE.md
    │   ├── 02_V5_HANDOFF.md
    │   ├── 04_ANATOMIE_KAETZCHEN.md
    │   ├── 05_COMBAT_SYSTEM.md
    │   ├── 06_MASTER_ZUSAMMENFASSUNG.md
    │   ├── 07_KONOSUBA_OREGON_EVENTS.md   # 2682 Zeilen!
    │   └── 08_1_SKILL_WEG_SYSTEM.md
    ├── 03_code/
    ├── 04_optional_docs/                  # 14 Dokumente
    │   ├── NAJIKA_V7_PLAN_FINAL.md        # V7 Roadmap (AKTUALISIERT!)
    │   └── ... viele weitere
    ├── 05_chat_verlaeufe/                 # ALLE GELESEN!
    │   ├── 111                            # Hardcore Mode Details
    │   ├── 1111111111111111.txt           # Tech Installation
    │   ├── n_3                            # NSFW Deep-Dive
    │   ├── wefewfwe.txt                   # 3D Scene Development
    │   └── ... 18+ Chat-Verläufe
    ├── 08_phase3_ideen/
    │   ├── PHASE3_ALLE_FUNDE_ZUSAMMENFASSUNG.md  # 74 FEATURES!
    │   ├── PHASE3_CLAUDE_SESSIONS_IDEEN.md
    │   ├── PHASE3_NAJIKACORE_IDEEN.md
    │   └── PHASE3_ZIP_ORDNER_IDEEN.md
    ├── 09_training/
    └── 11_anleitungen_xonline/
```

### **ALLES WISSEN (alles wissen/):**
```
alles wissen/
├── neu neu/                       # Neueste Infos
│   └── PROJECT_GUIDE.md
│
├── zip/
│   ├── xonline/                   # Große Sammlung
│   │   ├── projekt_docs/          # 20+ Dokumente
│   │   │   ├── PHASE3_*.md
│   │   │   ├── KONOSUBA_*.md
│   │   │   └── NAJIKA_*.md
│   │   ├── pflicht_docs/          # Duplikate von info material
│   │   ├── optional/              # Zusatz-Infos
│   │   ├── code_examples/         # Code-Beispiele
│   │   │   ├── frontend/
│   │   │   └── backend/
│   │   └── anleitungen/           # Anleitungen
│   │
│   ├── najika_ultimate_v2_complete/  # Ältere Version
│   │   └── najika_ultimate_complete/
│   │
│   └── Najika finalee/            # Verschiedene Versionen
│       ├── grund idee ki nicht perfekt/
│       ├── grund idee und ki inklsuive aller neuereung.../
│       ├── zusammenfassung aus allen datein lokal.../
│       └── najika installer nach claud zusammenfassung.../
```

### **DOCS (DOCS/):**
```
DOCS/
├── Weitere Dokumentation
└── (Nicht komplett gescannt)
```

---

## 🎯 ROOT DOKUMENTATION

### **Status Reports:**
```
├── FINALE_SESSION_REPORT.md
├── CLAUDE_SESSION_HANDOFF_2025_11_03.md
├── CLAUDE_SESSION_HANDOFF_2025_11_04.md
└── NAJIKA_WORLD_SYSTEM_COMPLETE.md
```

### **Feature Reports:**
```
├── MEGUMIN_VOICE_CLONE_INTEGRIERT.md
├── CODE_TRAINING_FUNKTIONIERT.md
├── HAPPINESS_DISCIPLINE_SYNC_GEFIXT.md
├── COMBAT_STATUS_SYNC_KOMPLETT_GEFIXT.md
└── NAJIKA_TRAINING_DATA_STRATEGIE.md
```

### **Installation:**
```
├── NAJIKA_WORLD_INSTALLER_V4.bat  # 1740 Zeilen!
├── INSTALLATION_ERFOLGREICH.md
├── INSTALLER_PROBLEM_ANALYSE.md
└── INSTALLER_UPLOAD_PACKAGE_LISTE.md
```

### **Training Setup:**
```
├── SETUP_AUTO_TRAINING.bat
├── SETUP_INTENSIVE_TRAINING.bat
├── START_NIGHT_TRAINING.bat
├── TRAIN_NOW.bat
└── CREATE_2_TASKS.bat
```

---

## 🔧 SCRIPTS & AUTOMATION

### **Task Management:**
```
├── LIST_TASKS.bat / .ps1
├── CREATE_CODE_TRAINING_TASK.bat
├── DELETE_ALL_NAJIKA_TASKS.bat
└── manage_tasks.py
```

### **GitHub:**
```
├── github_push.ps1
├── setup_github_token.ps1
├── setup_tokens.ps1
└── upload_to_github.ps1
```

### **Cleanup:**
```
├── CLEANUP_ALL_TASKS.ps1
├── CLEANUP_ALL_TASKS_ADMIN.bat
└── WINDOWS_DEFENDER_AUSNAHME.bat
```

---

## 📊 WAS FUNKTIONIERT

### **✅ BACKEND (95% funktional):**
- Magic System (9 Schools + Explosion + Skill-Weaving) ✅
- Claude Code Integration (PRIORITÄT 1!) ✅
- Enhanced Memory (ChromaDB + Video-Transkripte) ✅
- Living System (Mood, Proactive Messages) ✅
- Battle System ✅
- Security (Alcatraz - 8 Gebote) ✅
- TTS (Coqui XTTS-v2 mit Megumin Clone!) ✅
- LoRA Training API (Qwen2.5 7B) ✅

### **✅ FRONTEND (90% funktional):**
- Open World (2400×2400) ✅
- 6 Gebäude + Interior Räume ✅
- 3 Modi (World/Interior/Battle) ✅
- Mobile Controls (Virtual Joystick) ✅
- 12 Räume mit KayKit Assets ✅

### **✅ TRAINING (95.65% Success Rate!):**
- Code Training: 33 Probleme gelöst ✅
- LoRA Training: 3 Sessions erfolgreich ✅
- ChromaDB Enhancement: 4 Sessions ✅
- Voice Clone: Megumin's deutsche Stimme ✅

---

## ❌ WAS FEHLT

### **Assets:**
- ❌ KayKit GLTF Models (lokal bei dir, ~25GB!)
- ❌ Skeleton_Mage.glb
- ❌ room_config_detailed.json
- ❌ Decorations

### **Features (V7 Plan):**
- ❌ EXPLOSION Ultimate Skill
- ❌ Konosuba Oregon Events (Comedy-Ton)
- ❌ 8-Orte Open World (Design fertig, Umsetzung fehlt!)
- ❌ 5 Städte (Design fertig, Umsetzung fehlt!)
- ❌ 3 Special Locations (Design fertig, Umsetzung fehlt!)
- ❌ Weapon-Morphs (9 Styles)
- ❌ Procedural Dungeons
- ❌ Affinity/Beziehungs-System (KRITISCH!)

### **Bugs:**
- ❌ CSS Fehler (chat.css:249, code_editor.css:361)
- ❌ Merge Conflict: OPEN_WORLD_DESIGN_COMPLETE.md
- ❌ najika_human_like_trainer.py fehlt Methode

---

## 🎯 AKTUELLER STATUS

### **Git:**
- **Branch:** claude/remote-access-setup-011CUrJfTrTc8Dwa8N1QqrHQ
- **Letzter Commit:** OPEN_WORLD_DESIGN_COMPLETE.md
- **Merge Conflict:** OPEN_WORLD_DESIGN_COMPLETE.md (deine + meine Version!)

### **Heute erledigt:**
1. ✅ Harley Quinn "Puddin'" → "Mr.K" gefixt (überall!)
2. ✅ V7 Plan aktualisiert: Keller → 3 Dungeons
3. ✅ Asset-Scanning Scripts erstellt (scan_assets.ps1/.sh)
4. ✅ OPEN_WORLD_DESIGN_COMPLETE.md erstellt (8 Regionen, 5 Städte, 3 Orte)
5. ⚠️ MERGE CONFLICT bei OPEN_WORLD_DESIGN_COMPLETE.md

---

## 🚀 NÄCHSTE SCHRITTE

### **Sofort:**
1. ⬜ Merge Conflict lösen (OPEN_WORLD_DESIGN_COMPLETE.md)
2. ⬜ Asset-Scanner ausführen (.\scan_assets.ps1)
3. ⬜ Feedback zu Namen (User: "Hotel, Stadt und Ortsnamen gefallen mir nicht")

### **Kurzfristig:**
1. ⬜ Neue Namen finden für: Hotel, Städte, Orte
2. ⬜ CSS-Fehler fixen
3. ⬜ room_config_detailed.json erstellen

### **Mittelfristig (V7.1):**
1. ⬜ 3 Dungeons bauen
2. ⬜ EXPLOSION Ultimate Skill
3. ⬜ Konosuba Oregon Events (10 Events)
4. ⬜ Affinity-System (KRITISCH!)

---

## 📝 WICHTIGE ERKENNTNISSE

### **Projekt-Organisation:**
- **3 FRONTEND-SYSTEME:** digivice/ (Haupt), frontend/ (Alternative?), root HTML files
- **MEGA-DOKUMENTATION:** 106+ Dateien in info material/alles wissen
- **TRAINING LÄUFT:** 95.65% Success Rate, Voice Clone perfekt
- **ASSETS GETRENNT:** ~25GB lokal, nicht in GitHub (.gitignore korrekt!)

### **Design-Philosophie:**
- **Najika's Lebensraum (Map) = 100% SAFE**
- **Gefahr NUR in:** Dungeons + Arena + Special Locations
- **3 Dungeons statt Keller** (User-Feedback integriert!)
- **Hotel = Horror → Luxury Hub** (Endgame Portal-Dungeons!)

### **Inspirationen:**
- **Konosuba:** Comedy, EXPLOSION, absurde Events
- **Digimon World:** Skill-Learning, File Forest, Commands
- **Fantasy Western:** Ghost Towns, Saloons, Dusthaven
- **No Game No Life:** Colorful fantasy world

---

**Erstellt von:** Claude Code
**Letztes Update:** 2025-11-06
**Zweck:** Kompletter Überblick für besseres Verständnis

🔥 JETZT HAB ICH DEN ÜBERBLICK! 🔥
