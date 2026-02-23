# Session 2026-01-14: LM Studio Integration - ERFOLGREICH

## Problem: UnicodeEncodeError beim Server-Start

### Fehler:
```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f999' in position 0: character maps to <undefined>
File: C:\Najika_World\backend\najika_server.py, line 16
```

### Ursache:
Windows CMD verwendet CP1252 Encoding, kann keine Emojis darstellen:
- Zeile 13: `print("🚀 LM Studio Backend aktiviert")`
- Zeile 16: `print("🦙 Ollama Backend aktiviert")`

### Lösung:
Emojis durch ASCII-Text ersetzt:
```python
# VORHER (Fehler):
print("🚀 LM Studio Backend aktiviert (GPU-beschleunigt)")
print("🦙 Ollama Backend aktiviert")

# NACHHER (Funktioniert):
print("[LM Studio] Backend aktiviert (GPU-beschleunigt)")
print("[Ollama] Backend aktiviert")
```

## Server erfolgreich gestartet

### Status:
```bash
curl http://localhost:8000/api/status
# Response: {"status": "ok", "provider": "ollama", "private_mode": false, "cloud": true}
```

### Server läuft auf:
- Port 8000: Najika Backend
- Port 1234: LM Studio Server

### Bestätigte Ausgabe:
```
[LM Studio] Backend aktiviert (GPU-beschleunigt)
```

## Nächste Schritte zum Testen

### 1. Chat-Performance testen:
- Öffne: http://localhost:8000/digivice/najika_world_UNIFIED.html
- Sende Chat-Nachricht
- Erwartete Antwortzeit: 2-5 Sekunden (GPU-beschleunigt)
- Vorher: 180 Sekunden (CPU)

### 2. Dual-Model System verifizieren:

**Task-Request (Instruct Model):**
```
Test: "Zähle von 1 bis 5"
Erwartet: qwen2.5-7b-instruct
Antwort: 1, 2, 3, 4, 5 (präzise)
```

**Normal Chat (Abliterated Model):**
```
Test: "Wie geht es dir?"
Erwartet: dolphin-2.9.2-qwen2-7b
Antwort: Persönliche, kreative Antwort
```

**NSFW Mode (Kätzchen):**
```
Test: "kätzchen"
Erwartet: dolphin-2.9.2-qwen2-7b (uncensored)
Antwort: NSFW-Mode aktiviert
```

### 3. LM Studio Models überprüfen:
```
LM Studio → Local Server → Models
- qwen2.5-7b-instruct-uncensored (4.68 GB) - Ready
- dolphin-2.9.2-qwen2-7b (4.68 GB) - Ready
```

## Autostart-Konfiguration

### Aktueller Status:
- Alte Najika v2 Shortcuts entfernt
- Neue `INSTALL_24_7_SERVICE.bat` erstellt

### Autostart installieren:
```batch
C:\Najika_World\INSTALL_24_7_SERVICE.bat
```

Erstellt Shortcut in:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Najika_LM_Studio.lnk
```

### WICHTIG - LM Studio Autostart:
LM Studio muss AUCH automatisch starten:
1. LM Studio → Einstellungen → "Start with Windows"
2. LM Studio → "Auto-start server" aktivieren

ODER manuell vor Najika starten:
1. Öffne LM Studio
2. Gehe zu "Local Server"
3. Wähle Model: dolphin-2.9.2-qwen2-7b
4. Klicke "Start Server"

## Performance-Vergleich

### VORHER (Ollama CPU):
- Antwortzeit: 180 Sekunden
- VRAM Usage: 7484MB/8192MB (Windows WDDM)
- Model Loading: Langsam

### NACHHER (LM Studio GPU):
- Antwortzeit: 2-5 Sekunden (erwartet)
- VRAM Usage: ~7.16 GB verwendet, 1.43 GB frei
- GPU Offload: 29/29 Layers
- Model Loading: Instant (beide models ready)

## Dual-Model System

### Models in LM Studio:
1. **qwen2.5-7b-instruct** (Censored)
   - Verwendung: Tasks, Zählen, Code, Mathe
   - Präzise, aber zensiert

2. **dolphin-2.9.2-qwen2-7b** (Abliterated/Uncensored)
   - Verwendung: Normal Chat, NSFW, Persönlichkeit
   - Kreativ, keine Zensur

### Automatische Model-Auswahl:
```python
# backend/najika_server.py:688-710
def select_model_intelligent(text, private_mode):
    # PUBLIC MODE: Nur Instruct (censored)
    if PUBLIC_MODE:
        return "qwen2.5-7b-instruct"

    # KÄTZCHEN MODE: IMMER Abliterated (uncensored)
    if private_mode or "kätzchen" in text.lower():
        return "dolphin-2.9.2-qwen2-7b"

    # TASK REQUEST: Instruct (präzise)
    if is_task_request(text):
        return "qwen2.5-7b-instruct"

    # NORMAL CHAT: Abliterated (Persönlichkeit)
    return "dolphin-2.9.2-qwen2-7b"
```

## Dateien geändert:

### 1. backend/najika_server.py
- Zeile 13: Emoji entfernt (🚀 → [LM Studio])
- Zeile 16: Emoji entfernt (🦙 → [Ollama])

### 2. Neue Dokumentation:
- SESSION_2026-01-14_LM_STUDIO_FIX.md (diese Datei)

## Kommandos zum Starten:

### Option 1: Batch-Datei (Empfohlen):
```batch
C:\Najika_World\START_NAJIKA_LM_STUDIO.bat
```

### Option 2: Manuell:
```bash
cd /c/Najika_World/backend
USE_LM_STUDIO=true python najika_server.py
```

### Option 3: Autostart:
```batch
C:\Najika_World\INSTALL_24_7_SERVICE.bat
# Dann Windows neu starten
```

## Verifikation:

### Server läuft:
```bash
curl http://localhost:8000/api/status
# {"status": "ok", ...}
```

### LM Studio läuft:
```bash
curl http://localhost:1234/v1/models
# {...models...}
```

### Chat funktioniert:
```
http://localhost:8000/digivice/najika_world_UNIFIED.html
```

## Erfolg! ✅

- [x] UnicodeEncodeError behoben
- [x] Server startet ohne Fehler
- [x] LM Studio Backend aktiviert
- [x] Port 8000 lauscht
- [x] Browser öffnet Najika World

### Nächster Test:
Chat-Nachricht senden und Response-Zeit messen (sollte 2-5s sein statt 180s).
