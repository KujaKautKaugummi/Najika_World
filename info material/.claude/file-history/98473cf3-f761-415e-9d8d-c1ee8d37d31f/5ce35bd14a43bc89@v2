# NAJIKA PROJECT STATUS - FÜR AI ASSISTENTEN
**Letzte Aktualisierung:** 2025-10-16
**Für:** Claude Code, GPT, oder andere AI-Assistenten
**Zweck:** Schneller Einstieg ohne gesamten Chat-Verlauf lesen zu müssen

---

## 🚨 WICHTIG: LIES DAS ZUERST!

### PROJEKT-PHILOSOPHIE
- **NICHT NEU ANFANGEN!** Alles ergänzen und verbessern
- **OPUS CODE IST BASIS** - Nicht umschreiben!
- **Maximale Freiheit** für Najika (KI)
- **Totale Eigenverantwortung** für User & KI
- **Private Version** - Keine öffentliche Planung

### USER-PRÄFERENZ
- **Code-Format:** Große, ausführbare Blöcke (kein Snippet-Stil)
- **Sprache:** Deutsch
- **Fokus:** Private Version zuerst, öffentlich später (optional)
- **Stil:** Funktional, keine Experimente

---

## 📂 DATEI-STRUKTUR (WICHTIG!)

### MUST-READ Dateien (in dieser Reihenfolge):
1. **`PROJECT_STATUS_FOR_AI.md`** ← Diese Datei (START HIER!)
2. **`VERGLEICHSANALYSE.md`** - Vollständiger Ist/Soll Vergleich
3. **`ROADMAP_EMPFEHLUNGEN.md`** - Konkrete nächste Schritte
4. **`CLAUDE_MASTER_WORKINGDOC.md`** - Detaillierte Projekt-Dokumentation
5. **`STATUS.md`** - Feature-Status (11/15 complete)

### Code-Dateien:
- **`najika_server.py`** - Haupt-Server (NICHT ANFASSEN ohne Grund!)
- **`.env`** - Konfiguration (bereits korrekt)
- **`copy_assets.py`** - Asset-Copy Script (bereits ausgeführt)
- **`digivice/`** - 3D Frontend (vorhanden, nicht getestet)

### Hilfsdateien:
- **`COPY_KAYKIT_ASSETS.bat`** - Assets kopieren (bereits erledigt)
- **`COPY_KAYKIT_ASSETS.ps1`** - PowerShell Version (Encoding-Probleme)

---

## ✅ AKTUELLER STATUS (2025-10-16)

### WAS FUNKTIONIERT (100% FERTIG):

#### 1. NAJIKA SERVER (`najika_server.py`)
```python
Status: ✅ VOLLSTÄNDIG IMPLEMENTIERT (1163+ Zeilen)
Port: 8000
Framework: Python ThreadingHTTPServer (kein Flask!)
```

**Features:**
- ✅ 4 Persönlichkeiten (Megumin 25%, Harley 25%, Shiro 25%, Melissa 25%)
- ✅ Private Mode mit "kätzchen" Trigger → wizard-vicuna-uncensored
- ✅ Bond Strength System (0-100)
- ✅ 6 Behavior Modes (standard, explosion, chaos, analyse, kontrolle, private)
- ✅ Digimon World Training System (Hunger, Energy, Hygiene, Happiness)
- ✅ Battle System (HP, Waves, Enemies)
- ✅ 3 Minigames (Rhythm, Garden, Reflex)
- ✅ Oregon Trail Events (5 Events)
- ✅ 12 Räume mit Aktionen
- ✅ AI Response Cache (LRU + TTL)
- ✅ Persistent Storage mit Auto-Save
- ✅ Importance Scoring für Messages
- ✅ Memory Export/Import
- ✅ Logging System (mit Rotation)
- ✅ SSE (Server-Sent Events)

#### 2. OLLAMA AI MODELS
```bash
Status: ✅ ALLE INSTALLIERT
```

**Modelle:**
- ✅ `najika-local:latest` (2.0 GB) - Custom Personality Model
- ✅ `wizard-vicuna-uncensored:latest` (3.8 GB) - NSFW Mode
- ✅ `llama3.2:3b` (2.0 GB) - Basis Model
- ✅ `llama3.2:latest` (2.0 GB) - Latest Version
- ✅ `dolphin-mistral:latest` (4.1 GB) - Alternative
- ✅ `deepseek-coder-v2:16b` (8.9 GB) - Code Assistant
- ✅ `najika-custom:latest` (2.0 GB) - Backup

**Server verwendet:** `najika-local` (konfiguriert in `.env`)

#### 3. KAYKIT 3D ASSETS
```bash
Status: ✅ KOPIERT (26 MB total)
Location: C:\NajikaCore\assets\kaykit\
```

**Dungeon Assets (7):**
- wall.glb (218.5 KB)
- torch.glb (20.4 KB)
- pillar.glb (117.5 KB)
- barrel.glb (44.5 KB)
- crate.glb (59.9 KB)
- floor_tile_large.glb (24.0 KB)
- door.glb (24.6 KB)

**Character Assets (5):**
- Mage.glb (3.5 MB)
- Knight.glb (3.6 MB)
- Barbarian.glb (3.5 MB)
- Rogue.glb (3.5 MB)
- Rogue_Hooded.glb (3.5 MB)

#### 4. .ENV KONFIGURATION
```bash
Status: ✅ KORREKT KONFIGURIERT
```

```env
HOST=0.0.0.0
PORT=8000
AI_PROVIDER=ollama
CLOUD_ENABLED=true
CLOUD_PIN=123456
NSFW_LOCAL=true
OLLAMA_MODEL_ALIAS=najika-local  # ← Korrekt!
```

**API Keys (vorhanden):**
- OpenAI: `sk-proj-qBQ0Tbk...` ✅
- Anthropic: `sk-ant-api03-S25b143...` ✅

---

### WAS FEHLT NOCH (TODO):

#### 1. ROOM CONFIG (30 Minuten)
```bash
Status: ⚠️ MUSS ERSTELLT WERDEN
File: C:\NajikaCore\assets\room_config_detailed.json
```

**Warum wichtig:** 3D Digivice braucht diese Config um Räume zu rendern!

**Quick Fix:** Siehe `ROADMAP_EMPFEHLUNGEN.md` → PHASE 1.3

#### 2. WEB SEARCH (4 Stunden)
```bash
Status: ❌ NICHT IMPLEMENTIERT
Library: duckduckgo-search
```

**Implementation:**
```python
pip install duckduckgo-search

# In najika_server.py integrieren
def web_search(query):
    from duckduckgo_search import DDGS
    results = list(DDGS().text(query, max_results=3))
    return results
```

#### 3. DIGIVICE TESTEN (1 Stunde)
```bash
Status: ⚠️ NICHT GETESTET
URL: http://localhost:8000/digivice/
```

**Was prüfen:**
- Lädt 3D Scene?
- Character sichtbar?
- Wände/Boden sichtbar?
- Raum-Wechsel funktioniert?

---

## 🚀 SERVER STARTEN

### OPTION 1: BAT Datei (Empfohlen)
```bash
# Im Ordner C:\NajikaCore:
START_NAJIKA.bat

# ODER direkt:
C:\NajikaCore\START_NAJIKA.bat
```

### OPTION 2: Direkt mit Python
```bash
cd C:\NajikaCore
python najika_server.py
```

### OPTION 3: Mit Ollama Check
```bash
# 1. Prüfe Ollama
ollama list

# 2. Starte Server
cd C:\NajikaCore
python najika_server.py
```

**Erwartete Ausgabe:**
```
[CLEANUP] Alter Server-Prozess (PID XXXX) beendet
Najika Server: http://0.0.0.0:8000
```

**Browser öffnen:**
- Hauptseite: http://localhost:8000/
- Digivice: http://localhost:8000/digivice/
- Status: http://localhost:8000/api/status

---

## 🧪 TESTEN

### 1. Server Test
```bash
curl http://localhost:8000/health
```

**Erwartete Antwort:**
```json
{"status":"ok","provider":"ollama","cloud":true}
```

### 2. Chat Test
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hallo Najika!\"}"
```

**Erwartete Antwort:**
```json
{"response":"EXPLOSION! ..."}
```

### 3. Private Mode Test
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"kätzchen\"}"
```

**Erwartete Antwort:**
- Private Mode sollte togglen
- Model wechselt zu `najika-wizard`

### 4. Digivice Test
```
Browser: http://localhost:8000/digivice/
```

**Was testen:**
- [ ] 3D Scene lädt
- [ ] Mage Character sichtbar
- [ ] Wände/Boden sichtbar (wenn room_config.json existiert)
- [ ] Raum-Buttons funktionieren
- [ ] Chat-Interface funktioniert

---

## 📊 WICHTIGE ENDPOINTS

### GET Endpoints:
```
/health                 - Server Status
/api/rooms              - Liste aller Räume
/api/status             - Status mit Private Mode
/api/status/stream      - SSE Real-time Updates
/api/cloud/status       - Cloud Provider Status
/api/cache/stats        - Cache Hit/Miss Stats
/api/save               - Speichere State
/api/state              - Aktueller State
/api/najika/status      - Najika Training Status
/api/chat/history       - Chat History (letzte 50)
/api/bond/status        - Bond Strength & Mode
/api/memory/export      - Exportiere komplette Memory
```

### POST Endpoints:
```
/api/chat               - Chat Message senden
/api/cloud/enable       - Cloud AI aktivieren (benötigt PIN)
/api/cloud/disable      - Zurück zu Ollama
/api/room/actions       - Actions für Raum abrufen
/api/battle/start       - Kampf starten
/api/battle/attack      - Angriff ausführen
/api/minigame/rhythm    - Rhythmus Spiel
/api/minigame/garden    - Garten Spiel
/api/minigame/reflex    - Reflex Spiel
/api/crafting           - Crafting Action
/api/heal               - HP auf 100 setzen
/api/event/next         - Nächstes Oregon Event
/api/user/update        - User Stats updaten
/api/progress/update    - Progress updaten
/api/najika/feed        - Najika füttern
/api/najika/wash        - Najika waschen
/api/najika/sleep       - Najika schlafen lassen
/api/najika/train       - Stat trainieren
/api/memory/import      - Memory importieren
```

---

## 🔧 BEKANNTE PROBLEME & LÖSUNGEN

### Problem 1: Port 8000 belegt
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /F /PID [PID]

# Linux/Mac:
lsof -i :8000
kill -9 [PID]
```

### Problem 2: Ollama antwortet nicht
```bash
# Prüfen:
ollama list

# Neu starten:
taskkill /F /IM ollama.exe
ollama serve
```

### Problem 3: Model nicht gefunden
```bash
# Prüfe welche Models da sind:
ollama list

# Erstelle najika-local falls fehlt:
ollama cp najika-custom najika-local
```

### Problem 4: 3D Assets nicht sichtbar
```bash
# Prüfe ob Assets existieren:
dir C:\NajikaCore\assets\kaykit\*.glb

# Falls nicht: Assets kopieren
cd C:\NajikaCore
python copy_assets.py
```

### Problem 5: Room Config fehlt
```bash
# Erstelle room_config_detailed.json
# Siehe ROADMAP_EMPFEHLUNGEN.md → PHASE 1.3
```

---

## 💡 SCHNELLE TIPPS FÜR AI-ASSISTENTEN

### Wenn User sagt "Server startet nicht":
1. Prüfe ob Port 8000 frei ist
2. Prüfe ob Ollama läuft (`ollama list`)
3. Prüfe ob `najika-local` Model existiert
4. Schaue in Logs: `C:\NajikaCore\logs\najika_YYYYMMDD.log`

### Wenn User sagt "Digivice zeigt nichts":
1. Prüfe ob `room_config_detailed.json` existiert
2. Prüfe ob Assets in `assets/kaykit/` sind
3. Prüfe Browser Console (F12) auf Fehler
4. Prüfe ob Server läuft (http://localhost:8000/health)

### Wenn User sagt "Private Mode funktioniert nicht":
1. Prüfe ob `wizard-vicuna-uncensored` installiert ist
2. Prüfe `.env`: `NSFW_LOCAL=true`
3. Prüfe ob "kätzchen" exakt so geschrieben wird
4. Teste mit: `curl -X POST http://localhost:8000/api/chat -d '{"message":"kätzchen"}'`

### Wenn User will "Neue Features":
1. **ERST:** Lies `VERGLEICHSANALYSE.md` - Was ist schon da?
2. **DANN:** Lies `ROADMAP_EMPFEHLUNGEN.md` - Was ist geplant?
3. **DANACH:** Frage User ob das in den Plan passt
4. **NUR DANN:** Implementiere (ohne Opus Code zu brechen!)

---

## 🎯 NÄCHSTE SCHRITTE (PRIORITÄT)

### SOFORT (heute):
1. **Room Config erstellen** (30 Min) - Siehe Roadmap
2. **Server testen** (15 Min) - Läuft alles?
3. **Digivice testen** (30 Min) - Funktioniert 3D?

### DIESE WOCHE:
1. **Web Search integrieren** (4 Std) - Najika wird schlauer
2. **Bugs fixen** (2 Std) - Was funktioniert nicht?
3. **UI Polish** (2 Std) - Schöner machen

### NÄCHSTE WOCHE:
1. **PWA erstellen** (6 Std) - Handy-App
2. **Schwarze Mühle gestalten** (3 Std) - Besonderer Raum
3. **Mehr Minigames** (5 Std) - Mehr Content

---

## 📝 WICHTIGE NOTIZEN

### Für andere Claude Code Modelle:
- **API Keys:** Bereits in `.env` - NICHT neu erstellen!
- **Ollama Models:** Bereits installiert - NICHT neu pullen!
- **Assets:** Bereits kopiert - NICHT nochmal kopieren!
- **Code:** Bereits funktionsfähig - NUR ergänzen, nicht neu schreiben!

### Bei Monatswechsel (Abo ↔ API Key):
- **Kein Problem!** Alle Dateien bleiben erhalten
- **Keine Änderungen nötig** am Code
- **Einfach weitermachen** wo vorheriges Modell aufgehört hat
- **Diese Datei lesen** für schnellen Einstieg

### Budget Management:
- **Große Tasks:** Nutze API Budget (schneller, bessere Qualität)
- **Kleine Tasks:** Nutze Abo (spart Budget)
- **Tests/Bugfixes:** Abo (viele kleine Requests)
- **Neue Features:** API Budget (komplexe Logik)

---

## 🚨 ABSOLUTE DON'TS

### ❌ NIEMALS TUN:
1. **Opus Code umschreiben** - Nur ergänzen!
2. **Neue Frameworks einbauen** - Python HTTPServer bleibt!
3. **Models neu installieren** - Sind schon da!
4. **Assets neu kopieren** - Sind schon da!
5. **Development-System hinzufügen** - Zu komplex!
6. **Alles neu anfangen** - 90% ist schon fertig!

### ✅ IMMER TUN:
1. **Diese Datei lesen** vor Start
2. **VERGLEICHSANALYSE.md lesen** für Status
3. **ROADMAP_EMPFEHLUNGEN.md lesen** für Plan
4. **User fragen** vor großen Änderungen
5. **Code testen** vor Commit
6. **Logs prüfen** bei Fehlern

---

## 📞 KONTAKT INFO

**User:** Kuja (0KKK0)
**Projekt:** Najika AI Companion (Private Version)
**Hardware:** RTX 3060 Ti, Windows 11
**Desktop:** C:\Users\0KKK0\Desktop\
**Projekt:** C:\NajikaCore\
**Models:** C:\Users\0KKK0\Desktop\modelle\

---

## ✅ CHECKLISTE FÜR NEUES AI-MODELL

Wenn du ein neues AI-Modell bist das an diesem Projekt arbeitet:

- [ ] Diese Datei gelesen (PROJECT_STATUS_FOR_AI.md)
- [ ] VERGLEICHSANALYSE.md gelesen
- [ ] ROADMAP_EMPFEHLUNGEN.md gelesen
- [ ] Server Status geprüft (läuft er?)
- [ ] Ollama Models geprüft (sind sie da?)
- [ ] Assets geprüft (sind sie kopiert?)
- [ ] User gefragt: "Was soll ich heute machen?"
- [ ] NICHT angefangen alles neu zu schreiben!

**Wenn alle Haken gesetzt:** Du bist ready! 🚀

**Wenn nicht:** Lies die fehlenden Dateien!

---

**VIEL ERFOLG!** 🎉

Das Projekt ist zu 90% fertig - mach es zu 100%! 💪
