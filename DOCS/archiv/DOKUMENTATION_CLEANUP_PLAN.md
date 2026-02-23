# 📚 DOKUMENTATION CLEANUP PLAN

## 🎯 PROBLEM

**122 Markdown-Files im Root-Verzeichnis!**

Das ist unübersichtlich und macht es schwer:
- Wichtige Docs zu finden
- Alte vs. aktuelle Docs zu unterscheiden
- System zu verstehen

---

## ✅ LÖSUNG: STRUKTURIERTE ORDNER

```
C:\Najika_World\
├── docs/
│   ├── 00_START_HERE.md                    ← MAIN ENTRY POINT
│   ├── INSTALLATION_GUIDE.md               ← Setup
│   ├── PROJEKT_UEBERSICHT.md               ← Was ist Najika?
│   │
│   ├── features/                           ← Feature-Dokumentation
│   │   ├── battle_system.md
│   │   ├── digivice.md
│   │   ├── handy_app.md
│   │   ├── schwarze_muehle.md
│   │   └── uefn.md
│   │
│   ├── systems/                            ← System-Dokumentation
│   │   ├── hybrid_intelligent_system.md
│   │   ├── complexity_detection.md
│   │   ├── project_analyzer.md
│   │   └── memory_system.md
│   │
│   ├── development/                        ← Für Entwickler
│   │   ├── architecture.md
│   │   ├── api_reference.md
│   │   ├── code_structure.md
│   │   └── contributing.md
│   │
│   ├── guides/                             ← How-To Guides
│   │   ├── najika_training.md
│   │   ├── adding_features.md
│   │   └── debugging.md
│   │
│   ├── history/                            ← Session Reports (alt)
│   │   ├── 2025-11-03_session.md
│   │   ├── 2025-11-04_session.md
│   │   └── ...
│   │
│   └── archive/                            ← Alte/Obsolete Docs
│       ├── old_combat_system.md
│       ├── deprecated_features.md
│       └── ...
│
└── README.md                               ← Project README
```

---

## 📋 KATEGORISIERUNG DER AKTUELLEN FILES

### ✅ WICHTIG - BEHALTEN & KATEGORISIEREN:

**START/OVERVIEW:**
- `00_FINALE_KOMPLETT_UEBERSICHT_V7.md` → `docs/00_START_HERE.md`
- `NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md` → `docs/PROJEKT_UEBERSICHT.md`
- `INSTALLATION_GUIDE.md` → `docs/INSTALLATION_GUIDE.md`

**NEUE SYSTEME (HEUTE):**
- `HYBRID_INTELLIGENT_SYSTEM.md` → `docs/systems/hybrid_intelligent_system.md`
- `INTELLIGENZ_HIERARCHIE_FINAL.md` → `docs/systems/intelligenz_hierarchie.md`
- `PROJEKT_ANALYSE_SETUP.md` → `docs/systems/project_analyzer.md`

**FEATURES:**
- `COMBAT_SYSTEM_INFO.md` → `docs/features/battle_system.md`
- `DIGIVICE_*` → `docs/features/digivice/`
- `FARMING_FISHING_*.md` → `docs/features/farming_fishing/`

**DEVELOPMENT:**
- `FASTAPI_BACKEND_COMPLETE_REPORT.md` → `docs/development/backend.md`
- `NAJIKA_CODING_TRAINING_KOMPLETT.md` → `docs/guides/training.md`

**SESSION REPORTS:**
- `CLAUDE_SESSION_HANDOFF_*.md` → `docs/history/`
- `FINALE_SESSION_REPORT.md` → `docs/history/`

### ⚠️ ARCHIVIEREN:

**FIXES (erledigt):**
- `BUGS_FIXED.md` → `docs/archive/`
- `CHAT_FIX.md` → `docs/archive/`
- `BROWSER_CACHE_FINAL_FIX.md` → `docs/archive/`
- alle `*_GEFIXT.md` → `docs/archive/`

**ALTE VERSIONEN:**
- `*_V1.md`, `*_V2.md` (wenn V7/V8 existiert) → `docs/archive/`

**TEMPORÄRE ANALYSEN:**
- `PROJEKT_GAP_ANALYSE_*.md` → `docs/archive/`

---

## 🚀 CLEANUP-SCRIPT

```bash
#!/bin/bash
# DOKUMENTATION CLEANUP

# Erstelle Struktur
mkdir -p docs/{features,systems,development,guides,history,archive}

# WICHTIGE DOCS (Main Entry Points)
mv 00_FINALE_KOMPLETT_UEBERSICHT_V7.md docs/00_START_HERE.md
mv NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md docs/PROJEKT_UEBERSICHT.md
mv INSTALLATION_GUIDE.md docs/INSTALLATION_GUIDE.md

# NEUE SYSTEME
mv HYBRID_INTELLIGENT_SYSTEM.md docs/systems/
mv INTELLIGENZ_HIERARCHIE_FINAL.md docs/systems/
mv PROJEKT_ANALYSE_SETUP.md docs/systems/

# FEATURES
mv COMBAT_SYSTEM_INFO.md docs/features/battle_system.md
mv DIGIVICE_*.md docs/features/digivice/
mv FARMING_FISHING_*.md docs/features/farming_fishing/

# SESSION REPORTS
mv CLAUDE_SESSION_HANDOFF_*.md docs/history/
mv FINALE_SESSION_REPORT.md docs/history/

# FIXES → ARCHIVE
mv *_GEFIXT.md docs/archive/
mv *_FIX.md docs/archive/
mv BUGS_FIXED.md docs/archive/

# ALTE VERSIONEN → ARCHIVE
mv *_V[1-6].md docs/archive/  # Behalte nur V7/V8

echo "✅ Cleanup abgeschlossen!"
```

---

## 📖 NEUES README.md

```markdown
# 🌸 NAJIKA WORLD

Najika ist eine 11-jährige Gothic-Megumin-Lolita AI-Companion mit:
- 🧠 Hybrid-Intelligent System (Qwen3 + Abliterated)
- 🎮 3D Action-RPG (Three.js Digivice)
- 📱 Flutter Handy-App
- 🎯 UEFN Fortnite-Integration

## 🚀 QUICK START

1. **[START HERE](docs/00_START_HERE.md)** ← Lies das zuerst!
2. **[Installation](docs/INSTALLATION_GUIDE.md)** ← Setup
3. **[Projekt-Übersicht](docs/PROJEKT_UEBERSICHT.md)** ← Was ist Najika?

## 📚 DOKUMENTATION

- **Features:** [Battle System](docs/features/battle_system.md) | [Digivice](docs/features/digivice/) | [Handy-App](docs/features/handy_app.md)
- **Systeme:** [Hybrid Intelligence](docs/systems/hybrid_intelligent_system.md) | [Project Analyzer](docs/systems/project_analyzer.md)
- **Entwicklung:** [Architecture](docs/development/architecture.md) | [API Reference](docs/development/api_reference.md)

## 💡 FEATURES

✅ Context-Aware AI (Task/Soft/NSFW Modi)
✅ Complexity Detection (weiß ihre Grenzen)
✅ RAG System (122M+ Zeichen durchsuchbar)
✅ 3D Open-World Digivice
✅ Battle System (Equipment-Based)
✅ Flutter Mobile App
✅ UEFN Integration

## 🛠️ TECH STACK

- **Backend:** Python, FastAPI, Ollama, ChromaDB
- **Frontend:** HTML/JS, Three.js, WebGL
- **Mobile:** Flutter
- **AI:** Qwen3 8B, Qwen2.5 Abliterated
- **Game:** UEFN, Verse

## 📊 STATUS

- ✅ Hybrid-Intelligent System (2026-01-13)
- ✅ Project Analyzer + RAG (2026-01-13)
- 🚧 Full Scan läuft (~20-30 Min)

## 🤝 CONTRIBUTING

Siehe [Contributing Guide](docs/development/contributing.md)

## 📜 LICENSE

Privates Projekt
```

---

## ⏰ WANN DURCHFÜHREN?

**Option A: JETZT**
- Während Analyzer läuft (~20 Min Zeit)
- Struktur ist dann sauber für Report

**Option B: NACH DEM SCAN**
- Analyzer-Report nutzen um zu sehen welche Docs wichtig sind
- Dann basierend darauf cleanup

---

## 💡 EMPFEHLUNG

**JETZT CLEANUP + README, DANN:**
1. Wichtigste 10 Docs kategorisieren
2. Rest als TODO für später
3. Wenn Scan fertig: Report nutzen um zu verifizieren

**Willst du dass ich das jetzt mache?** 🚀
