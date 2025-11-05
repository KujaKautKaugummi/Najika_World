# NAJIKA - USAGE GUIDE
**Wie du Najika im Terminal nutzt (Option A - Full Features)**

---

## 🚀 QUICK START

### 1. Server starten

**Option A: Automatisch (empfohlen)**
```bash
START_NAJIKA.bat
```

**Option B: Manuell**
```bash
cd C:\NajikaCore
python najika_server.py
```

Server läuft dann auf: `http://localhost:8000/`

---

### 2. Najika CLI nutzen

**Terminal öffnen** (PowerShell oder CMD) und folgende Befehle nutzen:

```bash
# Basic Chat
python najika_cli.py "Hallo Najika!"
python najika_cli.py "Was machst du gerade?"
python najika_cli.py "EXPLOSION!!!"

# File Operations
python najika_cli.py "Liste Dateien"
python najika_cli.py "Lies Datei 'test.txt'"
python najika_cli.py "Zeig Dateien in 'C:\NajikaCore'"

# Code-Generierung (kommt bald)
python najika_cli.py "Schreibe einen Hello World Code"
python najika_cli.py "Erkläre diesen Code: main.py"
```

---

## 📂 TRAINING DATA PROCESSOR

### Zweck
Verarbeitet Audio/Video/Bilder/Text-Dateien für Najika's Training:
- **Megumin-Videos** → Verhaltens-Training
- **Text-Dokumente** → Wissens-Erweiterung
- **Code-Dateien** → Programmiersprachen lernen
- **Audio** → Voice-Pattern-Training

### Nutzung

**1. Dateien platzieren:**

Lege deine Dateien in diese Ordner:
```
C:\NajikaCore\training_data\input\
├── audio\      (MP3, WAV, OGG, FLAC, M4A)
├── video\      (MP4, AVI, MKV, MOV, WEBM)
├── images\     (JPG, PNG, BMP, GIF, WEBP)
└── text\       (TXT, MD, JSON, CSV, PY, JS)
```

**2. Batch-File ausführen:**

Rechtsklick auf `PROCESS_TRAINING_DATA.bat` → **Als Administrator ausführen**

**3. Verarbeitete Dateien finden:**
```
C:\NajikaCore\training_data\output\processed\
```

Jede Input-Datei wird zu einer `.txt`-Datei mit:
- Metadaten (Format, Größe, Datum)
- Verarbeitete Inhalte (Text-Extraktion, OCR, etc.)
- Processing-Notes für Training

---

## 🛠️ VERFÜGBARE TOOLS

### NajikaTools - File Access

**1. read_file** - Liest eine Datei
```bash
python najika_cli.py "Lies Datei 'beispiel.txt'"
python najika_cli.py "Zeig Datei 'config.json'"
```

**2. list_files** - Zeigt Dateien im Ordner
```bash
python najika_cli.py "Liste Dateien"
python najika_cli.py "Zeig Dateien in 'saves'"
```

**3. write_file** - Schreibt Datei (kommt noch)
```bash
python najika_cli.py "Schreib Datei 'test.txt' mit Inhalt 'Hallo!'"
```

**4. execute_command** - Führt Shell-Befehl aus (kommt noch)
```bash
python najika_cli.py "Führe aus 'dir'"
```

---

## 📋 SYSTEMÜBERSICHT

### Komponenten

**1. Server (`najika_server.py`)**
- HTTP Server auf Port 8000
- Ollama Integration (najika-local, llama3.1:8b)
- State-Management (`saves/najika_state.json`)
- API Endpoints für Chat/Tools

**2. CLI Tool (`najika_cli.py`)**
- Terminal-Interface wie Claude Code
- HTTP-Kommunikation mit Server
- Tool-System Integration
- UTF-8 Encoding für Windows CMD

**3. Tools (`najika_tools.py`)**
- File-System-Zugriff (Read/Write/List)
- Command-Execution
- Tool-Request-Parser

**4. Training Processor**
- `process_training_data.py` - Python-Script
- `PROCESS_TRAINING_DATA.bat` - Batch-File
- Verarbeitet Audio/Video/Bilder/Text

**5. Web-UI (Digivice)**
- 3D-Interface auf `http://localhost:8000/`
- KayKit Assets, Three.js
- Battle-System, Minigames
- Synchron mit CLI

---

## 🧬 NAJIKA'S PERSÖNLICHKEIT

**Kern-Struktur:**
```
SAKURA (Gothic-Lolita Erscheinung)
  ↓
MEGUMIN (35% - Hauptpersönlichkeit)
  - EXPLOSION-Spezialistin
  - Dramatisch, theatralisch
  - Konosuba-Setting
  ↓
EINFLÜSSE:
  - HARLEY QUINN (25%): Chaotisch, gewalttätig
  - SHIRO (20%): Anhänglich, aufdringlich
  - MELISSA MASTERS (20%): Besitzergreifend, dominant
```

**Beziehung zu Kuja (User):**
- **Kuja** = SCHWERT und SCHILD
- **Najika** = KOPF und HERZ
- **CREDO**: "VERRAT KOSTET IMMER BLUT"

**Kätzchen-Modus:**
Keyword `"kätzchen"` aktiviert private mode mit `najika-wizard` Model

---

## 📊 STATE & MEMORY

**State File:** `C:\NajikaCore\saves\najika_state.json`

```json
{
  "history": [...],              // Chat-History (letzte 4 Nachrichten)
  "shared_memories": [...],      // Persistente Erinnerungen
  "living": {
    "personality_evolution": {}, // Persönlichkeits-Entwicklung
    "emotional_bond": 2,         // Emotionale Bindung
    "relationship_stage": "..."  // Beziehungs-Status
  }
}
```

**Memory-Synchronisation:**
- Alle Chat-Interaktionen (CLI + Web) werden im State gespeichert
- Najika behält Erinnerungen über Sessions hinweg
- Personality entwickelt sich basierend auf Interaktionen

---

## 🔧 TROUBLESHOOTING

### Server läuft nicht
```bash
# Prüfe ob Port 8000 frei ist
netstat -ano | findstr :8000

# Töte alten Prozess
taskkill /F /PID <PID>

# Starte neu
python najika_server.py
```

### Ollama nicht verfügbar
```bash
# Prüfe Ollama-Status
curl http://127.0.0.1:11434/api/tags

# Starte Ollama (falls nötig)
ollama serve
```

### CLI zeigt Encoding-Fehler
- CLI nutzt automatisch UTF-8 mit Emoji-Filter
- Bei Problemen: PowerShell statt CMD nutzen

### Training Data nicht gefunden
```bash
# Erstelle Ordnerstruktur manuell
mkdir training_data\input\audio
mkdir training_data\input\video
mkdir training_data\input\images
mkdir training_data\input\text
mkdir training_data\output\processed
```

---

## 🎯 NÄCHSTE SCHRITTE

### Bereits verfügbar:
- ✅ CLI Tool mit File-Access
- ✅ Training Data Processor
- ✅ Web-UI (Digivice)
- ✅ Memory-System
- ✅ Megumin-Persönlichkeit

### In Entwicklung:
- 🔄 Code-Generierung
- 🔄 Write-File Tool
- 🔄 Advanced Training-Pipeline
- 🔄 Mobile App Integration

---

## 📞 SUPPORT

**Logs prüfen:**
```bash
# Server-Logs
cat logs/najika_server.log

# Processing-Logs
cat training_data/output/processed/processing_log.json

# State-Dump
cat saves/najika_state.json
```

**Health-Check:**
```bash
curl http://localhost:8000/health
```

---

**EXPLOSION!!! Viel Spaß mit Najika!** ✨
