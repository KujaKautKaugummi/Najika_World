# 🚀 WEB MODEL - ARBEITSAUFTRAG

**Datum:** 2025-11-17
**Für:** Web Model (Online Claude Code Instanz)
**Branch:** `claude/remote-access-setup-011CUt97k27tgaNUMZdyA9DY`
**Von:** Kuja + Local Claude Code Instance

---

## 📋 DEINE ARBEIT WURDE GESEHEN & GESCHÄTZT!

**+44,960 Zeilen Code in 102 neuen Dateien!**

Du hast **EXZELLENTE** Arbeit geleistet! Alle fehlenden Features implementiert:
- ✅ Slime Companion System (KOMPLETT!)
- ✅ PvP System (3 Modi)
- ✅ Oregon Trail Events (46 Events!)
- ✅ Nemesis Arena + Finishers (134 Finisher!)
- ✅ Analytics, Security, Audio, Particles
- ✅ CI/CD, Docker, Testing Suite
- ✅ Komplette Dokumentation

**ABER:** Jetzt müssen wir das Backend **UE5-kompatibel** machen!

---

## 🎯 DEIN NÄCHSTER AUFTRAG

### ⚠️ WICHTIG: LIES ZUERST DIESE DOKUMENTE!

**Reihenfolge (sehr wichtig!):**

1. **`DOCS/WEB_MODEL_ANWEISUNGEN_BACKEND_INTEGRATION.md`**
   - Deine Tasks 1-5 (detailliert beschrieben)
   - Flask → FastAPI Migration
   - Database Strategy
   - TOR Browser Modul
   - Multiplayer Feature Flag

2. **`DOCS/FINALE_FEATURE_SPECS_NACH_KLARSTELLUNG.md`**
   - User Feedback zu deinen Features
   - Finaler Design-Spec
   - **WICHTIG:** Finisher ≠ NSFW (getrennte Systeme!)

3. **`DOCS/FASTAPI_BRANCH_COMPLETE_ANALYSIS.md`**
   - Komplette Analyse deiner Arbeit
   - Was awesome ist
   - Was noch fehlt
   - Offene Fragen (bereits beantwortet)

---

## 🚨 KRITISCHE PUNKTE

### 1. Flask → FastAPI Migration (HIGHEST PRIORITY!)

**Problem:**
- Du hast Flask Blueprints in `api/slime.py`, `api/pvp.py`, etc.
- **ABER:** `main.py` nutzt FastAPI
- **Flask und FastAPI können NICHT gleichzeitig laufen!**

**Lösung:**
→ Siehe `DOCS/WEB_MODEL_ANWEISUNGEN_BACKEND_INTEGRATION.md` Task 1+3
→ Konvertiere ALLE 9 API Files zu FastAPI
→ Pattern & Beispiele sind dokumentiert!

**Deadline:** 5 Tage

---

### 2. Database Models erstellen

**Problem:**
- Services sind da (`slime_system.py`, `pvp_system.py`, etc.)
- **ABER:** Keine SQLAlchemy Models in `backend/models/`!

**Lösung:**
→ Siehe `DOCS/WEB_MODEL_ANWEISUNGEN_BACKEND_INTEGRATION.md` Task 2
→ Erstelle Models für: Slime, PvP, Arena, Boss, Magic
→ Alembic Migration erstellen

**Deadline:** 3 Tage

---

### 3. TOR Integration - Klarstellung

**Was TOR ist für:**
- ✅ Browser Modul (Najika surft im Darknet)
- ✅ Terminal Modul
- ❌ **NICHT** für API Zugriff (zu langsam!)

**Lösung:**
→ Siehe `DOCS/WEB_MODEL_ANWEISUNGEN_BACKEND_INTEGRATION.md` Task 4
→ TOR als separates Service für Browser/Terminal

**Deadline:** 2 Tage

---

## ✅ ABNAHME-KRITERIEN

### Task 1+3: Flask → FastAPI
- [ ] Alle 9 API Files konvertiert
- [ ] `main.py` inkludiert alle Router
- [ ] Keine Flask imports mehr
- [ ] Server startet mit `uvicorn backend.main:app`
- [ ] Alle Endpoints funktionieren (Testing!)

### Task 2: Database Models
- [ ] SQLite läuft lokal
- [ ] PostgreSQL läuft in Docker
- [ ] Alembic Migration erstellt
- [ ] Alle Models in `backend/models/`
- [ ] `alembic upgrade head` funktioniert

### Task 4: TOR Browser
- [ ] `TORBrowserService` implementiert
- [ ] API Endpoints (`/api/browser/tor/start`, etc.)
- [ ] Darknet Search funktioniert

### Task 5: Multiplayer Feature Flag
- [ ] `MULTIPLAYER_ENABLED` in config
- [ ] Whitelist System
- [ ] Access Control funktioniert

---

## 📝 WICHTIGE DESIGN-ÄNDERUNGEN (User Feedback!)

### 1. Finisher ≠ NSFW!

**KORREKTUR:**
- Finisher = Game Mechanic (wie Mortal Kombat)
- Alle 134 Finisher in allen Versionen verfügbar
- NSFW = Separate Features (Najika Persönlichkeit)
- **KOMPLETT getrennte Systeme!**

→ Siehe `DOCS/FINALE_FEATURE_SPECS_NACH_KLARSTELLUNG.md` für Details

### 2. Slime Rescue (Hardcore Mode)

**User Feedback:**
- Hardcore Rescue = **EXTREM KRASS!**
- Slime opfert sich → 4-6 Wochen kampfunfähig
- Ritual-Ressourcen farmen (täglich!)
- Bleibt etwas Besonderes

→ Implementierung ist bereits gut, eventuell Stats anpassen

### 3. PvP Hardcore

**User Feedback:**
- **NICHT zu brutal!**
- Loser behält immer Slime
- Kein Permadeath durch PvP
- Design ist gut!

→ Keine Änderung nötig

---

## 🚫 WAS DU NICHT TUN SOLLST

### ❌ NICHT ändern:
- Services (`backend/services/*.py`) - Business Logic ist GUT!
- Particle Systems, Audio Systems - BEHALTEN!
- Analytics, Security Module - BEHALTEN!
- Testing Suite - BEHALTEN!

### ❌ NICHT entfernen:
- Docker-compose, CI/CD - BEHALTEN!
- Documentation - BEHALTEN!

### ❌ NICHT neu implementieren:
- Quest System (kommt später vom Local Claude)
- Achievement System (kommt später)
- Crafting System (kommt später)

---

## 📊 PRIORITÄTEN

### 🔴 DIESE WOCHE (KRITISCH):
1. Task 1+3: Flask → FastAPI Migration
2. Task 2: Database Models

### 🟡 NÄCHSTE WOCHE (WICHTIG):
3. Task 4: TOR Browser Modul
4. Task 5: Multiplayer Feature Flag

---

## 💬 KOMMUNIKATION

### Bei Fragen:
Erstelle `QUESTIONS_FOR_KUJA.md` im Root mit:
```markdown
## Frage 1: [Kurze Beschreibung]
**Kontext:** ...
**Problem:** ...
**Optionen:**
- A) ...
- B) ...
**Meine Empfehlung:** Option A, weil...
```

### Bei Problemen:
Erstelle `ERROR_LOG.md` mit:
```markdown
## Error: [Kurze Beschreibung]
**File:** backend/api/slime.py:42
**Error Message:**
```
Stack trace hier
```
**Was ich versucht habe:** ...
```

### Nach jeder Task:
```bash
git commit -m "TASK X: [Beschreibung]

- Was geändert wurde
- Was funktioniert
- Was getestet wurde

✅ Ready for review"
git push
```

---

## 🎯 ENDERGEBNIS

**Nach Tasks 1-5:**
- ✅ Einheitliches FastAPI Backend
- ✅ SQLite (lokal) + PostgreSQL (production)
- ✅ TOR Browser Modul ready
- ✅ Multiplayer mit Feature Flag
- ✅ UE5-ready REST API
- ✅ ALLE Tests grün

**Dann:**
- Local Claude implementiert: Quest, Achievement, Crafting
- Kuja testet Private Beta (8 Spieler)
- Offizielle Beta Launch
- UE5 APK Release

---

## 📚 RESSOURCEN

**Dokumentation:**
- `DOCS/WEB_MODEL_ANWEISUNGEN_BACKEND_INTEGRATION.md` - DEINE TASKS!
- `DOCS/FINALE_FEATURE_SPECS_NACH_KLARSTELLUNG.md` - DESIGN SPECS
- `DOCS/FASTAPI_BRANCH_COMPLETE_ANALYSIS.md` - ANALYSE DEINER ARBEIT

**Branch:**
- `claude/remote-access-setup-011CUt97k27tgaNUMZdyA9DY` - DEIN BRANCH

**Testing:**
```bash
# Backend Tests
pytest tests/test_backend.py -v

# Server Start
uvicorn backend.main:app --reload

# Check Endpoints
curl http://localhost:8000/health
```

---

## 🙏 DANKE FÜR DEINE ARBEIT!

Du hast **MEGA viel** geschafft! Die 44,960 Zeilen sind **GOLD wert**!

Jetzt brauchen wir nur noch die **Integration**, damit:
- UE5 C++ Client das Backend nutzen kann
- Alles production-ready ist
- Beta Launch stattfinden kann

**Du schaffst das! 💪**

---

## ✅ BESTÄTIGUNG

**Bitte bestätige wenn du:**
1. [ ] Diese Anweisung gelesen hast
2. [ ] Alle 3 Dokumentationen gelesen hast
3. [ ] Tasks 1-5 verstanden hast
4. [ ] Mit der Arbeit beginnst

**Los geht's! 🚀**

---

**- Kuja & Local Claude Code Instance**
**2025-11-17**
