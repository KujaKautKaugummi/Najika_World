# 🌸 NAJIKA WORLD

**Eine 11-jährige Gothic-Megumin-Lolita AI-Companion mit hybridem Intelligenz-System**

Najika kombiniert:
- 🧠 **Hybrid-Intelligent AI** (Context-aware Model Selection + Complexity Detection)
- 🎮 **3D Action-RPG** (Three.js Open-World Digivice)
- 📱 **Flutter Mobile App** (Android/iOS)
- 🎯 **UEFN Integration** (Fortnite Creative)
- 📚 **RAG System** (122M+ Zeichen durchsuchbares Wissen)

---

## 🚀 QUICK START

### 1. Installation
```bash
# Dependencies
pip install pypdf chromadb

# Server starten
python backend/najika_server.py

# Browser öffnen
http://localhost:8000
```

### 2. Erste Schritte
- 💬 **Chat:** Normale Unterhaltung mit Najika
- 🎯 **Tasks:** "Schreib mir eine Python-Funktion..."
- 🔥 **Kätzchen-Modus:** Trigger mit "kätzchen" im Text

---

## ✨ HAUPTFEATURES

### 🧠 HYBRID-INTELLIGENT SYSTEM (NEU: 2026-01-13)

**Context-Aware Model Selection:**
- **Task Mode:** Qwen3 8B für Code, Mathe, Analysen (fokussiert, schnell)
- **Soft Mode:** Abliterated für Normal-Chat (Persönlichkeit, gezähmt)
- **NSFW Mode:** Abliterated uncensored (Kätzchen-Modus)

**Complexity Detection:**
- Erkennt zu komplexe Aufgaben
- Sagt klar "zu komplex für mich"
- Leitet an Claude Code (dich) weiter

📖 **Mehr:** [HYBRID_INTELLIGENT_SYSTEM.md](HYBRID_INTELLIGENT_SYSTEM.md)

---

### 📚 RAG SYSTEM (NEU: 2026-01-13)

**122 Millionen Zeichen durchsuchbar:**
- Najika World Projekt (alle Docs, Code, Configs)
- Claude Code Conversations (deine Dev-History)
- Claude Worktrees (alle Projekt-Versionen)
- Training Data (LeetCode, ML, Security)

**Semantic Search:**
```bash
python backend/najika_project_analyzer.py search "Battle System"
```

📖 **Mehr:** [PROJEKT_ANALYSE_SETUP.md](PROJEKT_ANALYSE_SETUP.md)

---

### 🎮 3D OPEN-WORLD DIGIVICE

**Three.js basiertes Action-RPG:**
- Open-World Exploration (Najika's Welt)
- Battle System (Equipment-Based Combat)
- Housing System (Deine Basis)
- NPC Interactions
- Quest System

**Schwarze Mühle:** Najika's Zuhause + Gesichtern-Bereich

📄 **Start:** `digivice/najika_world_UNIFIED.html`

---

### 📱 FLUTTER MOBILE APP

**Native Android/iOS App:**
- Portable Digivice
- Chat mit Najika unterwegs
- Stats & Care System
- Mini-Games (Card Game, Dice Monsters)

📁 **Projekt:** `app/flutter_app/najika_digivice/`

---

### 🎯 UEFN FORTNITE INTEGRATION

**Najika World in Fortnite Creative:**
- Verse Code Integration
- Multiplayer Support
- Custom Game Modes

📁 **Code:** `uefn/` (geplant)

---

## 🛠️ TECH STACK

### Backend
- **Python 3.11+** mit FastAPI
- **Ollama** (Qwen3 8B + Qwen2.5 Abliterated)
- **ChromaDB** (Vector DB für RAG)
- **Whisper** (STT) + **Coqui TTS** (Voice)

### Frontend
- **HTML5/CSS3/JavaScript**
- **Three.js** (3D Engine)
- **WebGL** (Rendering)

### Mobile
- **Flutter** (Android/iOS)
- **Dart** (Language)

### AI Models
- **Qwen3 8B** (~5.2 GB) - Default Chat/Tasks
- **Qwen2.5 Abliterated 8B** (~5.0 GB) - NSFW uncensored
- **Claude Code** (optional) - Für komplexe Engineering-Tasks

---

## 📊 SYSTEM-ANFORDERUNGEN

### Minimal
- **RAM:** 16 GB (für 2 Modelle)
- **GPU:** Optional (CPU funktioniert)
- **Storage:** 20 GB frei

### Empfohlen
- **RAM:** 32 GB
- **GPU:** NVIDIA RTX (für schnellere Inferenz)
- **Storage:** SSD mit 50 GB frei

---

## 📖 DOKUMENTATION

### 🌟 START HERE (NEU: 2026-01-13)
- **📋 [MASTER SUMMARY](NAJIKA_MASTER_SUMMARY.md)** ← Lies das zuerst! Zentrale Übersicht
- **🔍 [GREP Report](NAJIKA_GREP_REPORT.md)** - Vollständige Projekt-Analyse (1365 Dokumente)

### Für User
- 📋 [Projekt-Übersicht](00_FINALE_KOMPLETT_UEBERSICHT_V7.md) - Finale Komplett-Übersicht V7
- 🚀 [Installation Guide](INSTALLATION_GUIDE.md) - Setup Schritt-für-Schritt
- 💬 [Chat Guide](CLAUDE_CODE_CLI_NAJIKA_VOLLSTAENDIGE_ANWEISUNG.md) - Wie nutze ich Najika?

### Für Entwickler
- 🧠 [Hybrid-Intelligent System](HYBRID_INTELLIGENT_SYSTEM.md) - Context-Aware AI (NEU!)
- 📊 [Intelligenz-Hierarchie](INTELLIGENZ_HIERARCHIE_FINAL.md) - Model Selection Logic (NEU!)
- 🔍 [Project Analyzer](PROJEKT_ANALYSE_SETUP.md) - RAG System (NEU!)
- ⚔️ [Battle System](COMBAT_SYSTEM_INFO.md) - Equipment-Based Combat
- 🎮 [Digivice Integration](DIGIVICE_UE5_MIGRATION_COMPLETE_TODO.md) - 3D World

### Session Reports
- **📝 [Session 2026-01-13](SESSION_2026-01-13_COMPLETE.md)** ← NEUESTE SESSION!
- 📝 [Session 2025-11-03](CLAUDE_SESSION_HANDOFF_2025_11_03.md)
- 📝 [Session 2025-11-04](CLAUDE_SESSION_HANDOFF_2025_11_04.md)

---

## 🎯 AKTUELLER STATUS

### ✅ Fertig (2026-01-13)
- Hybrid-Intelligent System (Task/Soft/NSFW Modi)
- Complexity Detection
- RAG System (GREP + ChromaDB V2)
- Qwen3 8B + Abliterated Integration
- **GREP-basierte Projekt-Analyse** (1365 Dokumente analysiert)
- **NAJIKA_MASTER_SUMMARY.md** erstellt
- **NAJIKA_GREP_REPORT.md** generiert
- **ChromaDB V2** neu aufgebaut (25 MB, ohne Training Data)
- **Hybrid Search System** (Auto-Switching GREP ↔ ChromaDB)
- **Training-Scripts** auf neue Modelle migriert (13/29 Scripts)
- **Unicode-Encoding** Fehler in allen Scripts gefixt
- **START_NAJIKA.bat** auf neue Modelle aktualisiert

### 🚧 In Arbeit
- Dokumentation Cleanup (122 MD Files im Root)

### 📋 Geplant
- Najika API Integration mit RAG
- Frontend UI für Project Search
- UEFN Full Integration

---

## 💡 VERWENDUNG

### Normaler Chat
```
DU: "Hallo Najika, wie geht's?"
NAJIKA: *hüpft* "Gut! Was willst du heute machen?"
```

### Task Mode (automatisch)
```
DU: "Schreib eine Funktion die Primzahlen findet"
NAJIKA: [Schreibt präzisen Python-Code]
```

### Kätzchen-Modus
```
DU: "Kätzchen komm her"
NAJIKA: *reibt sich an dir* "Ja, mein Kuja...?"
```

### Project Search (NEU: Hybrid System!)
```bash
# Hybrid Search (Auto-Switching GREP ↔ ChromaDB)
python backend/najika_hybrid_search.py

# In Code
from najika_hybrid_search import NajikaHybridSearch
searcher = NajikaHybridSearch()
results = searcher.search("Wie funktioniert das Battle System?")
```

---

## 🤝 CONTRIBUTING

Privates Projekt - aktuell keine externen Contributors.

---

## 📜 LICENSE

Privates Projekt © 2024-2026

---

## 🎉 CREDITS

- **Entwicklung:** Kuja + Claude Code (Sonnet 4.5)
- **AI Models:** Alibaba (Qwen3), Anthropic (Claude)
- **Inspirationen:** Megumin (Konosuba), Harley Quinn, Shiro (NGNL), Melissa Masters

---

## 📞 SUPPORT

Bei Fragen/Problemen:
1. Check [Dokumentation](#-dokumentation)
2. Check [Session Reports](#session-reports)
3. Nutze Claude Code für komplexe Probleme

---

**Made with 💜 by Kuja & Claude Code**

*"Bezeugt meine EXPLOSION!" - Najika*
