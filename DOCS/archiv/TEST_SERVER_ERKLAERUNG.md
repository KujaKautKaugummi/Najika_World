# 🌐 TEST-SERVER ERKLÄRUNG

**Warum:** `cd digivice` + `python3 -m http.server 8001`?

## 🎯 DAS PROBLEM

Najika World V2 ist ein **separates System** das parallel zum Hauptserver getestet werden soll.

### Datei-Struktur:
```
C:\Najika_World\
├── backend/
│   └── najika_server.py        ← Hauptserver (Port 8000)
└── digivice/
    ├── najika_world_v2.html    ← World V2 Test-Datei
    ├── data/                   ← World-Daten (regions.json, etc.)
    ├── static/                 ← Assets (3D-Models)
    └── js/world/               ← World-System Module
```

## ⚙️ DIE LÖSUNG

### 1. Server im `digivice/` Ordner starten

```bash
cd digivice
python3 -m http.server 8001
```

**Warum `cd digivice`?**
- Server-Root wird `digivice/`
- Alle Pfade relativ zu `digivice/`
- URLs sind kurz und korrekt!

### 2. Pfade funktionieren jetzt

**Server-Root:** `C:\Najika_World\digivice\`

| Code (najika_world_v2.html) | Server sucht in | Datei existiert? |
|------------------------------|-----------------|------------------|
| `/data/regions.json` | `digivice/data/regions.json` | ✅ 200 OK |
| `/static/assets/...` | `digivice/static/assets/...` | ✅ 200 OK |
| `/js/world/world_manager.js` | `digivice/js/world/...` | ✅ 200 OK |

**OHNE `cd digivice` (Server in Root):**

| Code | Server sucht in | Datei existiert? |
|------|-----------------|------------------|
| `/data/regions.json` | `C:\Najika_World\data\` | ❌ 404 (existiert nicht!) |
| `/digivice/data/regions.json` | `C:\Najika_World\digivice\data\` | ✅ 200 (aber URL zu lang!) |

### 3. Port 8001 = Parallel-Betrieb

```
┌─────────────────────────────────────────┐
│  Port 8000: najika_server.py           │
│  - Haupt-System (Najika AI)            │
│  - Living-System                        │
│  - Chat, Digivice, etc.                │
│  → PRODUKTIV                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Port 8001: python -m http.server       │
│  - NUR World V2 Test                    │
│  - Statische Dateien                    │
│  - Keine AI, kein Backend               │
│  → TEST/DEVELOPMENT                     │
└─────────────────────────────────────────┘
```

**Vorteil:**
- Beide Server laufen **gleichzeitig**
- Hauptsystem wird **nicht beeinflusst**
- World V2 kann **isoliert** getestet werden

## 🚀 WORKFLOW

### Development:
1. **Start Test-Server:**
   ```bash
   cd C:\Najika_World
   .\START_WORLD_V2_TEST.bat
   ```
   → Port 8001, Server-Root = `digivice/`

2. **Teste World V2:**
   ```
   http://localhost:8001/najika_world_v2.html
   ```

3. **Haupt-System läuft weiter:**
   ```
   http://localhost:8000/digivice/
   ```

### Production (später):
Wenn World V2 fertig ist:
1. Integriere in `digivice/index.html`
2. Nutze Hauptserver (Port 8000)
3. Test-Server nicht mehr nötig

## ❓ HÄUFIGE FRAGEN

### Q: Warum nicht `najika_server.py` für Tests nutzen?

**A:** Overhead! Du brauchst:
- ❌ Ollama (AI-Backend)
- ❌ ChromaDB (Memory)
- ❌ Living-System
- ❌ Komplexe Routen

Für World V2 Test brauchst du nur:
- ✅ Statische Dateien (HTML, JS, JSON)
- ✅ GLTF-Models
- ✅ CORS-Headers

→ `python -m http.server` ist perfekt!

### Q: Warum Pfade ohne `/digivice/` Prefix?

**A:** Server-Root ist `digivice/`!

```javascript
// Server in C:\Najika_World\digivice\

// FALSCH:
fetch('/digivice/data/regions.json')
// → Sucht: C:\Najika_World\digivice\digivice\data\ ❌

// RICHTIG:
fetch('/data/regions.json')
// → Sucht: C:\Najika_World\digivice\data\ ✅
```

### Q: Kann ich Port ändern?

**A:** Ja, aber:
```bash
# Port 8001 (Standard)
python3 -m http.server 8001

# Port 3000 (andere)
python3 -m http.server 3000
# → URL wird: http://localhost:3000/najika_world_v2.html
```

Aber: 8001 ist konventionell neben 8000!

## 🎓 WICHTIG FÜR WEB-MODELL

**Regel:** Server-Root bestimmt Pfade!

```bash
# Server in digivice/
cd digivice
python -m http.server 8001
# → /data/ wird zu digivice/data/

# Server in Root
cd C:\Najika_World
python -m http.server 8001
# → /data/ wird zu C:\Najika_World\data/
```

**Deshalb:**
- CLI-Modell hat Pfade auf `/data/` gefixt (ohne `/digivice/`)
- Web-Modell hatte `/digivice/data/` → 404!
- Unterschied: Server-Root!

## ✅ ZUSAMMENFASSUNG

**Der Test-Server:**
```bash
cd digivice                    # 1. Server-Root = digivice/
python3 -m http.server 8001   # 2. Statischer Server, Port 8001
```

**Warum so?**
- ✅ Pfade funktionieren (`/data/`, `/static/`)
- ✅ URL ist kurz (`/najika_world_v2.html`)
- ✅ Parallel zum Hauptserver (8000)
- ✅ Einfach zu starten (1 Befehl)
- ✅ Keine Dependencies

**Das Web-Modell muss verstehen:**
Server-Root = `digivice/` → Alle Pfade relativ dazu!
