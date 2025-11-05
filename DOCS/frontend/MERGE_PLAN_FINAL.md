# 🎯 MERGE-PLAN FINAL - AKTUALISIERT 26.10.2025

**Ziel:** C:\NajikaCore + C:\Najika → C:\Najika (vereint)

---

## ✅ AKTUELLE SYSTEME (26.10.2025)

### **Was läuft JETZT in NajikaCore:**
1. ✅ **Najika Chat:** najika-local (Ollama)
2. ✅ **Voice System:** Edge-TTS mit 4 Persönlichkeiten
3. ✅ **Coding-Scheduler:** 15h/Tag automatisch
4. ✅ **LoRA-Adapter:** Archiviert (8B, 586 Konversationen trainiert)
5. ✅ **3B-Training:** Vorbereitet für später

### **Was läuft JETZT in Najika:**
1. ✅ **React Frontend:** Game mit Three.js
2. ✅ **Command System:** Digimon World Style
3. ✅ **Battle API:** Backend-Connection
4. ✅ **Finisher QTE:** Button-Mashing

---

## 📦 WAS WIRD ÜBERNOMMEN

### **🟢 KRITISCH - MUSS MIT:**

#### **1. Python Backend (147 Files)**
```
✅ najika_server.py              → backend/
✅ najika_battle.py              → backend/
✅ najika_living_system.py       → backend/
✅ najika_enhanced_personality.py → backend/
✅ najika_memory_enhanced.py     → backend/
✅ najika_search.py              → backend/
✅ najika_tor.py                 → backend/
✅ najika_security.py            → backend/
✅ najika_claude_code.py         → backend/
✅ ... (alle najika_*.py)        → backend/
```

#### **2. Voice System (NEU HEUTE!)**
```
✅ najika_tts.py                 → backend/voice/
✅ najika_tts_edge.py            → backend/voice/
✅ najika_voice_clone.py         → backend/voice/
✅ voice_data/                   → backend/voice_data/
```

#### **3. LoRA/Training System**
```
✅ najika_lora_training.py       → backend/training/
✅ najika_lora_training_3b.py    → backend/training/
✅ najika_lora_server.py         → backend/training/
✅ deploy_lora_to_ollama.py      → backend/training/
✅ export_lora_gguf.py           → backend/training/
✅ resume_lora_training.py       → backend/training/
✅ NAJIKA_TRAINING_ULTIMATE_FAILSAFE.py → backend/training/
```

#### **4. Import System**
```
✅ najika_session_importer.py    → backend/import/
✅ najika_external_data_importer.py → backend/import/
✅ najika_comprehensive_import.py → backend/import/
✅ najika_design_importer.py     → backend/import/
✅ najika_personality_importer.py → backend/import/
✅ najika_filter_conflicts.py    → backend/import/
```

#### **5. Datenbanken & Data**
```
✅ chroma_db/                    → backend/chroma_db/
✅ voice_data/                   → backend/voice_data/
✅ training_data/                → backend/training_data/
```

#### **6. Config Files**
```
✅ .env                          → backend/.env
✅ config/                       → backend/config/
```

---

### **🟡 WICHTIG - SOLLTE MIT:**

#### **7. Dokumentation (54 Files)**
```
✅ NAJIKA_LORA_STATUS.md         → DOCS/backend/training/
✅ NAJIKA_VOICE_SYSTEM.md        → DOCS/backend/voice/
✅ NAJIKA_VOICE_CLONING_ANLEITUNG.md → DOCS/backend/voice/
✅ NAJIKA_LORA_SYSTEM_FERTIG.md  → DOCS/backend/training/
✅ NAJIKA_CURRENT_TRAINING.md    → DOCS/backend/training/
✅ NAJIKA_TRAINING_DATA_ANALYSE.md → DOCS/backend/training/
✅ NAJIKA_ULTIMATE_LEARNING_SYSTEM.md → DOCS/backend/training/
✅ NAJIKA_V4_INSTALLATION_PLAN.md → DOCS/backend/v4/
✅ NAJIKA_COMBAT_SYSTEM_DESIGN.md → DOCS/backend/v4/
✅ ... (alle anderen .md)         → DOCS/backend/
```

#### **8. Design Documents**
```
✅ design_documents/              → DOCS/design/
   ├── NAJIKA_MASTER_INDEX.md
   ├── NAJIKA_PROJEKT_KOMPLETT_V3_MIT_UNSERER_KI.md
   ├── NAJIKA_PROJEKT_V4_ERGAENZUNGEN.md
   └── NAJIKA_PROJEKT_V4_OPTIONAL_SAMMLUNG.md
```

#### **9. Batch Scripts**
```
✅ IMPORT_PERSONALITIES.bat       → backend/scripts/
✅ AKTIVIERE_AUTO_TRAINING.bat    → backend/scripts/
✅ CHECK_AUTO_TRAINING.bat        → backend/scripts/
```

---

### **🔴 NICHT MITNEHMEN:**

#### **10. LoRA Checkpoints**
```
❌ lora_checkpoints/              (~5 GB!)
   ├── najika_lora_20251025_111148/
   ├── najika_lora_20251025_180107/
   └── najika_lora_latest/
```
**GRUND:** Zu groß (5 GB), wird später neu trainiert wenn nötig

#### **11. Unsloth Cache**
```
❌ unsloth_compiled_cache/        (~200 MB)
```
**GRUND:** Regeneriert sich automatisch

#### **12. Alte/Unnötige Files**
```
❌ __pycache__/
❌ .claude/
❌ digivice/                      (alte HTML-Version)
❌ analyze_*.py                   (nur Dev-Tools)
❌ extract_*.py                   (nur Dev-Tools)
❌ test_*.py                      (Unit-Tests, optional)
```

---

## 📂 FINALE STRUKTUR

```
C:\Najika\
├── 📁 backend\                          ← VON NAJIKACORE
│   ├── 📄 najika_server.py              (Haupt-Server)
│   ├── 📄 najika_battle.py              (Battle System)
│   ├── 📄 najika_*.py                   (Core Files)
│   ├── 📄 .env                          (Backend-Config)
│   │
│   ├── 📁 voice\                        ← NEU!
│   │   ├── najika_tts.py
│   │   ├── najika_tts_edge.py
│   │   └── najika_voice_clone.py
│   │
│   ├── 📁 training\                     ← NEU!
│   │   ├── najika_lora_training.py
│   │   ├── najika_lora_training_3b.py
│   │   ├── najika_lora_server.py
│   │   └── ...
│   │
│   ├── 📁 import\                       ← NEU!
│   │   ├── najika_session_importer.py
│   │   ├── najika_external_data_importer.py
│   │   └── ...
│   │
│   ├── 📁 scripts\                      ← NEU!
│   │   ├── IMPORT_PERSONALITIES.bat
│   │   ├── AKTIVIERE_AUTO_TRAINING.bat
│   │   └── CHECK_AUTO_TRAINING.bat
│   │
│   ├── 📁 chroma_db\                    (Najika's Memory)
│   ├── 📁 voice_data\                   (TTS Cache)
│   ├── 📁 training_data\                (PDFs, Sessions)
│   ├── 📁 config\
│   └── 📁 logs\
│
├── 📁 frontend\                         ← BLEIBT!
│   ├── 📁 src\
│   │   ├── 📁 game\
│   │   │   ├── GameScene.jsx
│   │   │   ├── CommandSystem.js
│   │   │   ├── BattleAPI.js             (NEU GESTERN!)
│   │   │   ├── FinisherQTE.js           (NEU GESTERN!)
│   │   │   └── ...
│   │   ├── App.js
│   │   └── index.js
│   ├── 📄 package.json
│   ├── 📄 .env                          (Frontend-Config)
│   └── 📁 node_modules\
│
├── 📁 DOCS\                             ← NEU!
│   ├── 📁 backend\
│   │   ├── 📁 training\                 (LoRA/Training Docs)
│   │   ├── 📁 voice\                    (Voice Docs)
│   │   └── 📁 v4\                       (V4 Projekt)
│   ├── 📁 design\                       (Design Documents)
│   └── 📁 frontend\                     (Combat Docs)
│
├── 📄 START_NAJIKA.bat                  (NEUER Launcher)
├── 📄 README.md                         (NEUE README)
├── 📄 MERGE_01_BACKUP.bat
├── 📄 MERGE_02_EXECUTE.bat              ← WIRD JETZT AKTUALISIERT
├── 📄 MERGE_03_TEST.bat
├── 📄 MERGE_PLAN_FINAL.md               (diese Datei)
└── 📄 NEUE_FILES_HEUTE.md
```

---

## 📊 STATISTIK

### **Zu kopieren:**
| Typ | Anzahl | Größe | Wichtig |
|-----|--------|-------|---------|
| Python-Files | 147 | ~8 MB | ✅ JA |
| Markdown-Files | 54 | ~3 MB | ✅ JA |
| chroma_db/ | 1 Ordner | ~50 MB | ✅ JA |
| voice_data/ | 1 Ordner | ~20 MB | ✅ JA |
| training_data/ | 1 Ordner | ~10 MB | ✅ JA |
| config/ | 1 Ordner | ~1 MB | ✅ JA |
| Batch-Scripts | 3 Files | <1 MB | ✅ JA |
| **GESAMT** | **~210 Files** | **~95 MB** | **✅** |

### **NICHT kopieren:**
| Typ | Grund |
|-----|-------|
| lora_checkpoints/ (~5 GB) | Zu groß, regenerierbar |
| unsloth_compiled_cache/ (~200 MB) | Regenerierbar |
| __pycache__/ | Temp-Files |
| .claude/ | Session-Daten |
| digivice/ | Veraltet |

---

## ⚙️ MERGE-ABLAUF (morgen)

### **1. BACKUP (MERGE_01_BACKUP.bat)**
```batch
Backup-Ordner: C:\Najika_Backups\
├── Najika_[timestamp]
└── NajikaCore_[timestamp]
```

### **2. EXECUTE (MERGE_02_EXECUTE.bat - AKTUALISIERT!)**
```batch
# Python-Files in Unterordner sortieren
xcopy "C:\NajikaCore\najika_server.py" "C:\Najika\backend\" /Y
xcopy "C:\NajikaCore\najika_battle.py" "C:\Najika\backend\" /Y
... (Core-Files)

# Voice System
mkdir "C:\Najika\backend\voice"
xcopy "C:\NajikaCore\najika_tts*.py" "C:\Najika\backend\voice\" /Y
xcopy "C:\NajikaCore\najika_voice*.py" "C:\Najika\backend\voice\" /Y

# Training System
mkdir "C:\Najika\backend\training"
xcopy "C:\NajikaCore\najika_lora*.py" "C:\Najika\backend\training\" /Y
xcopy "C:\NajikaCore\*_training*.py" "C:\Najika\backend\training\" /Y

# Import System
mkdir "C:\Najika\backend\import"
xcopy "C:\NajikaCore\*_importer.py" "C:\Najika\backend\import\" /Y

# Scripts
mkdir "C:\Najika\backend\scripts"
xcopy "C:\NajikaCore\*.bat" "C:\Najika\backend\scripts\" /Y

# Datenbanken
xcopy "C:\NajikaCore\chroma_db" "C:\Najika\backend\chroma_db\" /E /I /Y
xcopy "C:\NajikaCore\voice_data" "C:\Najika\backend\voice_data\" /E /I /Y
xcopy "C:\NajikaCore\training_data" "C:\Najika\backend\training_data\" /E /I /Y

# Config
copy "C:\NajikaCore\.env" "C:\Najika\backend\.env" /Y

# Dokumentation
mkdir "C:\Najika\DOCS\backend\training"
mkdir "C:\Najika\DOCS\backend\voice"
mkdir "C:\Najika\DOCS\backend\v4"
mkdir "C:\Najika\DOCS\design"

copy "C:\NajikaCore\NAJIKA_LORA*.md" "C:\Najika\DOCS\backend\training\" /Y
copy "C:\NajikaCore\NAJIKA_VOICE*.md" "C:\Najika\DOCS\backend\voice\" /Y
copy "C:\NajikaCore\NAJIKA_V4*.md" "C:\Najika\DOCS\backend\v4\" /Y
copy "C:\NajikaCore\*.md" "C:\Najika\DOCS\backend\" /Y

xcopy "C:\NajikaCore\design_documents" "C:\Najika\DOCS\design\" /E /I /Y

# Neuer Launcher
(erstelle START_NAJIKA.bat mit Backend + Frontend)
```

### **3. TEST (MERGE_03_TEST.bat)**
```batch
[Test 1/8] Backend Python-Files existieren
[Test 2/8] Voice System existiert
[Test 3/8] Training System existiert
[Test 4/8] Frontend existiert
[Test 5/8] Launcher existiert
[Test 6/8] DOCS existiert
[Test 7/8] .env Files existieren
[Test 8/8] Keine alten Files übrig
```

### **4. START (START_NAJIKA.bat - NEU)**
```batch
@echo off
echo Starting Najika Backend...
cd backend
start /B python najika_server.py
cd ..

timeout /t 3

echo Starting Najika Frontend...
cd frontend
start /B npm start
cd ..

echo ✅ NAJIKA RUNNING!
echo Frontend: http://localhost:3002
echo Backend:  http://localhost:8000
echo Voice:    Edge-TTS (4 Persönlichkeiten)
echo LoRA:     8B Adapter archiviert
pause
```

---

## ✅ ZUSAMMENFASSUNG

**Was HEUTE NEU dazu kam:**
1. ✅ Voice System (Edge-TTS, 4 Persönlichkeiten)
2. ✅ LoRA Training (8B, 586 Konversationen)
3. ✅ 3B Training (vorbereitet)
4. ✅ 19 neue Python-Files
5. ✅ 24 neue Markdown-Files
6. ✅ Coding-Scheduler (15h/Tag)

**Was morgen passiert:**
1. Backup (automatisch)
2. Merge (automatisch, sortiert in Unterordner)
3. Test (automatisch)
4. Start (ein Klick)

**Dauer:** 5-10 Minuten

**Risiko:** MINIMAL (Backup vorhanden!)

---

## 🎯 BEREIT FÜR MORGEN!

**Alle Systeme erfasst:**
- ✅ Game (Frontend + Backend)
- ✅ Voice System
- ✅ LoRA Training
- ✅ Import System
- ✅ Dokumentation

**Alles vorbereitet:**
- ✅ Merge-Scripts
- ✅ Backup-Scripts
- ✅ Test-Scripts
- ✅ Launcher

**Morgen einfach:**
```
1. MERGE_01_BACKUP.bat
2. MERGE_02_EXECUTE.bat
3. MERGE_03_TEST.bat
4. START_NAJIKA.bat
```

**Fertig in 10 Minuten!** 🚀
