# 📋 MERGE-PLAN DETAILLIERT - C:\Najika + C:\NajikaCore

**Ziel:** Alles in `C:\Najika` zusammenführen

---

## 📊 IST-ZUSTAND

### **C:\NajikaCore** (Quelle - Python Backend):
```
📁 C:\NajikaCore\
├── 📄 128 Python-Dateien (najika_*.py)
├── 📄 .env (Backend-Config)
├── 📁 assets/ (KayKit 3D Models)
├── 📁 chroma_db/ (Vektor-Datenbank)
├── 📁 config/
├── 📁 digivice/ (alte HTML-Version)
├── 📁 logs/
├── 📁 voice_data/
├── 📁 training_data/
└── 📄 Viele .md Dokumentations-Dateien
```

### **C:\Najika** (Ziel - React Frontend):
```
📁 C:\Najika\
├── 📁 frontend/ (React + Three.js) ← BLEIBT!
├── 📁 backend/  (alte Struktur, fast leer)
├── 📁 mobile/
├── 📁 assets/
├── 📁 config/
├── 📁 data/
├── 📁 logs/
├── 📄 .env (Frontend-Config)
├── 📄 README.md
├── 📄 START_NAJIKA.bat
└── 📄 Mehrere .md Dateien (Combat-Docs)
```

---

## 🎯 WAS WIRD WIE ÜBERNOMMEN?

### **✅ 1. PYTHON BACKEND (von NajikaCore → Najika/backend/)**

**Übernehmen:** ALLE `.py` Dateien (128 Stück)

**Wichtigste Files:**
```
najika_server.py              → backend/najika_server.py
najika_battle.py              → backend/najika_battle.py
najika_living_system.py       → backend/najika_living_system.py
najika_enhanced_personality.py → backend/najika_enhanced_personality.py
najika_memory_enhanced.py     → backend/najika_memory_enhanced.py
najika_search.py              → backend/najika_search.py
najika_tor.py                 → backend/najika_tor.py
najika_security.py            → backend/najika_security.py
najika_claude_code.py         → backend/najika_claude_code.py
... (und alle anderen najika_*.py)
```

**Aktion:**
```batch
xcopy "C:\NajikaCore\*.py" "C:\Najika\backend\" /Y
```

---

### **✅ 2. .env CONFIG (Merge beider Configs)**

**C:\NajikaCore\.env** (Backend):
```env
HOST=0.0.0.0
PORT=8000
AI_PROVIDER=ollama
OLLAMA_MODEL_ALIAS=najika-local
CLOUD_ENABLED=true
CLOUD_PIN=xxx
NSFW_LOCAL=true
```

**C:\Najika\.env** (Frontend - teilweise überschneidend):
```env
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_WEBSOCKET_URL=ws://localhost:8000
```

**LÖSUNG:**
- Backend .env → `C:\Najika\backend\.env` (kopieren)
- Frontend .env → `C:\Najika\frontend\.env` (NEUE Datei erstellen)
- Root .env → LÖSCHEN oder umbenennen zu `.env.backup`

**Aktion:**
```batch
copy "C:\NajikaCore\.env" "C:\Najika\backend\.env" /Y
move "C:\Najika\.env" "C:\Najika\.env.backup"
```

---

### **✅ 3. ASSETS (3D Models)**

**C:\NajikaCore\assets\** (KayKit 3D Models):
```
KayKit_AnimatedCharacters_1.1/
KayKit_DungeonRemastered_1.1/
room_config_detailed.json
... (mehrere GB!)
```

**C:\Najika\assets\** (teilweise doppelt?):
```
... (prüfen ob gleich)
```

**LÖSUNG:**
- Prüfen ob identisch
- Falls JA: NUR room_config_detailed.json aktualisieren
- Falls NEIN: Merge (größere Version behalten)

**Aktion:**
```batch
REM Erst prüfen, dann entscheiden
REM Vorerst: Überspringen (Frontend nutzt eigene assets)
```

---

### **✅ 4. DATENBANKEN & DATA**

**C:\NajikaCore\chroma_db\** (Vektor-DB):
```
ChromaDB Dateien (Memory-System)
→ WICHTIG! Najika's Erinnerungen!
```

**C:\NajikaCore\voice_data\**:
```
TTS Cache, Voice Samples
```

**C:\NajikaCore\training_data\**:
```
Training Sessions, PDFs
```

**LÖSUNG:**
- chroma_db → `C:\Najika\backend\chroma_db\` (verschieben)
- voice_data → `C:\Najika\backend\voice_data\` (verschieben)
- training_data → `C:\Najika\backend\training_data\` (verschieben)

**Aktion:**
```batch
xcopy "C:\NajikaCore\chroma_db" "C:\Najika\backend\chroma_db\" /E /I /Y
xcopy "C:\NajikaCore\voice_data" "C:\Najika\backend\voice_data\" /E /I /Y
xcopy "C:\NajikaCore\training_data" "C:\Najika\backend\training_data\" /E /I /Y
```

---

### **✅ 5. LOGS**

**C:\NajikaCore\logs\**:
```
server.log
battle.log
...
```

**C:\Najika\logs\**:
```
(eventuell leer oder alte Logs)
```

**LÖSUNG:**
- Alte Logs archivieren
- Neue Logs in `C:\Najika\backend\logs\`

**Aktion:**
```batch
mkdir "C:\Najika\backend\logs"
REM NajikaCore logs NICHT kopieren (zu alt/unnötig)
REM Neue Logs werden automatisch erstellt
```

---

### **✅ 6. DOKUMENTATION**

**C:\NajikaCore\*.md** (VIELE Docs):
```
CLAUDE.md
CLAUDE_PFLICHT_START.md
CLAUDE_UPDATE.md
API_REFERENCE.md
DUNGEON_SYSTEM_GUIDE.md
... (30+ Dateien)
```

**C:\Najika\*.md** (Combat-Docs):
```
NAJIKA_ENHANCED_DIGIMON_COMBAT.md
COMBAT_MODES_VERGLEICH.md
ORIGINAL_VS_NEU_VERGLEICH.md
NAJIKA_SYSTEM_STATUS.md
HEUTE_FERTIG_2025-10-25.md
```

**LÖSUNG:**
- ALLE .md aus NajikaCore → `C:\Najika\DOCS\backend\`
- Bestehende .md in Najika → `C:\Najika\DOCS\frontend\`
- Neue Merge-Docs → `C:\Najika\DOCS\`

**Aktion:**
```batch
mkdir "C:\Najika\DOCS\backend"
mkdir "C:\Najika\DOCS\frontend"
copy "C:\NajikaCore\*.md" "C:\Najika\DOCS\backend\" /Y
move "C:\Najika\*.md" "C:\Najika\DOCS\frontend\"
REM Außer: README.md und Merge-Scripts bleiben im Root
```

---

### **❌ 7. NICHT ÜBERNEHMEN**

**Diese Files/Ordner NICHT kopieren:**

**C:\NajikaCore:**
```
❌ __pycache__/           (Python Cache)
❌ .claude/               (Session-Daten, nur lokal)
❌ digivice/              (alte HTML-Version, veraltet)
❌ *.bat (außer wichtige) (viele Test-Scripts)
❌ file_structure.txt     (zu alt)
❌ analyze_*.py           (nur für Entwicklung)
❌ extract_*.py           (nur für Entwicklung)
❌ test_*.py              (Unit-Tests, optional)
```

**C:\Najika:**
```
❌ backend/ (alter Ordner) → WIRD ÜBERSCHRIEBEN!
❌ mobile/                 (unvollständig, später)
❌ data/                   (leer?)
```

---

### **✅ 8. LAUNCHER & SCRIPTS**

**C:\NajikaCore:**
```
START_NAJIKA.bat (alter Launcher)
```

**C:\Najika:**
```
START_NAJIKA.bat (existiert schon)
MERGE_01_BACKUP.bat
MERGE_02_EXECUTE.bat
MERGE_03_TEST.bat
```

**LÖSUNG:**
- Neuer Launcher wird von MERGE_02 erstellt
- Alte Launcher archivieren

**Neuer Launcher** (wird erstellt):
```batch
@echo off
echo Starting Backend...
cd backend
start /B python najika_server.py
cd ..

timeout /t 3 /nobreak

echo Starting Frontend...
cd frontend
start /B npm start
cd ..

echo Najika Running!
echo Frontend: http://localhost:3002
echo Backend:  http://localhost:8000
pause
```

---

## 📂 FINALE STRUKTUR

Nach dem Merge:

```
C:\Najika\
├── 📁 backend\                    ← VON NAJIKACORE
│   ├── 📄 najika_server.py        (Haupt-Server)
│   ├── 📄 najika_battle.py        (Battle System)
│   ├── 📄 najika_*.py             (128 Python-Files)
│   ├── 📄 .env                    (Backend-Config)
│   ├── 📁 chroma_db\              (Najika's Memory)
│   ├── 📁 voice_data\             (TTS Cache)
│   ├── 📁 training_data\          (PDFs, Sessions)
│   └── 📁 logs\                   (neue Logs)
│
├── 📁 frontend\                   ← BLEIBT!
│   ├── 📁 src\
│   │   ├── 📁 game\
│   │   │   ├── GameScene.jsx
│   │   │   ├── CommandSystem.js
│   │   │   ├── BattleAPI.js       (NEU HEUTE!)
│   │   │   ├── FinisherQTE.js     (NEU HEUTE!)
│   │   │   └── ...
│   │   ├── App.js
│   │   └── index.js
│   ├── 📄 package.json
│   ├── 📄 .env                    (Frontend-Config, NEU)
│   └── 📁 node_modules\
│
├── 📁 DOCS\                       ← NEU
│   ├── 📁 backend\                (Docs von NajikaCore)
│   ├── 📁 frontend\               (Combat-Docs)
│   └── 📄 MERGE_PLAN_DETAILLIERT.md (diese Datei)
│
├── 📁 assets\                     ← Optional
├── 📁 config\                     ← Optional
│
├── 📄 START_NAJIKA.bat            (NEUER Launcher)
├── 📄 README.md                   (NEUE README)
├── 📄 MERGE_01_BACKUP.bat
├── 📄 MERGE_02_EXECUTE.bat
└── 📄 MERGE_03_TEST.bat
```

---

## 🔢 ZUSAMMENFASSUNG: WAS WIRD KOPIERT?

| Quelle | Ziel | Anzahl | Größe | Wichtig |
|--------|------|--------|-------|---------|
| `*.py` | `backend/` | 128 Files | ~5 MB | ✅ JA |
| `.env` | `backend/.env` | 1 File | 1 KB | ✅ JA |
| `chroma_db/` | `backend/chroma_db/` | Ordner | ~50 MB | ✅ JA |
| `voice_data/` | `backend/voice_data/` | Ordner | ~20 MB | ✅ JA |
| `training_data/` | `backend/training_data/` | Ordner | ~10 MB | ✅ JA |
| `*.md` | `DOCS/backend/` | ~30 Files | ~2 MB | ✅ JA |
| `__pycache__/` | - | - | - | ❌ NEIN |
| `digivice/` | - | - | - | ❌ NEIN |
| `.claude/` | - | - | - | ❌ NEIN |

**Gesamt zu kopieren:** ~90 MB, ~200 Files

**Zeit:** ~2-3 Minuten

---

## ⚠️ WICHTIGE ENTSCHEIDUNGEN

### **FRAGE 1: Assets (KayKit 3D Models)**

**NajikaCore\assets\** vs **Najika\assets\**

**Option A:** Backend-Assets behalten
- Pro: Vollständig
- Con: Sehr groß (mehrere GB)

**Option B:** Frontend-Assets behalten
- Pro: Frontend nutzt bereits
- Con: Eventuell unvollständig

**Option C:** Merge beide
- Pro: Alle Models
- Con: Am meisten Speicher

**MEINE EMPFEHLUNG:** Option B (Frontend-Assets behalten)
- Backend braucht keine 3D Models
- Frontend hat schon alles was es braucht

---

### **FRAGE 2: Alte Backend-Ordner löschen?**

**C:\Najika\backend\** (existiert schon, fast leer):
```
ai/
api/
game/
utils/
test_backend.py
```

**Aktion:**
- Komplett löschen oder
- Umbenennen zu `backend_old/`?

**MEINE EMPFEHLUNG:** Löschen
- Ist fast leer
- NajikaCore-Backend ist viel vollständiger

---

### **FRAGE 3: mobile/ Ordner?**

**C:\Najika\mobile\** (unvollständig)

**Aktion:**
- Behalten für später oder
- Jetzt löschen?

**MEINE EMPFEHLUNG:** Behalten
- Schadet nicht
- Vielleicht später nützlich

---

## ✅ FINALE CHECKLISTE

**VOR dem Merge:**
- [ ] Backup erstellt (MERGE_01_BACKUP.bat)
- [ ] Alle Programme geschlossen (Frontend/Backend)
- [ ] Entscheidungen getroffen:
  - [ ] Assets: Frontend behalten ✅
  - [ ] Alter backend/: Löschen ✅
  - [ ] mobile/: Behalten ✅

**WÄHREND Merge:**
- [ ] MERGE_02_EXECUTE.bat ausführen
- [ ] Keine Fehler in Konsole?

**NACH Merge:**
- [ ] MERGE_03_TEST.bat ausführen
- [ ] Alle 5 Tests grün?
- [ ] START_NAJIKA.bat starten
- [ ] Backend läuft (Port 8000)?
- [ ] Frontend läuft (Port 3002)?
- [ ] Commands funktionieren?
- [ ] Finisher funktioniert?

---

**BEREIT FÜR MORGIGEN MERGE!** 🚀

**Fragen noch offen?**
- Assets-Strategie OK?
- Alter backend/ löschen OK?
- Noch andere Files wichtig?
