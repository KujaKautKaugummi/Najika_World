# AUDIT FIXES - SONNET VS OPUS AUFGABENTEILUNG

**Datum:** 2026-02-15
**Basis:** COMPLETE_CODE_AUDIT_2026-02-15.md

---

## ✅ BEREITS GEFIXT (SONNET - HEUTE):

1. ✅ Backend: 4 Router registriert
2. ✅ Frontend: Duplikat entfernt
3. ✅ Frontend: config.js erstellt
4. ✅ Frontend: Audio-Systeme eingebunden
5. ✅ Frontend: CSS-Dateien eingebunden

**Status:** 5/6 kritische Bugs gefixt! (Git: 29b4ac5)

---

## 🔧 VERBLEIBENDE FIXES (30 PROBLEME):

### 🟡 P1 - WICHTIG (10 Probleme):

| # | Problem | Wer? | Warum? | Aufwand |
|---|---------|------|--------|---------|
| 6 | Error-Handling (4 API-Dateien) | **SONNET** | Backend-Code, @decorator hinzufügen | 30min |
| 7 | Particle-Systeme einbinden (4 Dateien) | **OPUS** | Muss getestet werden ob benötigt | 10min + Test |
| 8 | Performance-Systeme einbinden (3 Dateien) | **SONNET** | Performance-kritisch, muss vorsichtig sein | 10min |
| 9 | Legacy-Code Cleanup (2 Dateien) | **SONNET** | Backend-Architektur, sicher verschieben | 5min |
| 10 | UI-Systeme evaluieren (7 Dateien) | **OPUS** | UI-Design-Entscheidung, welche Features? | 30min |
| 11 | World-Systeme evaluieren (5 Dateien) | **OPUS** | Game-Design-Entscheidung (Day/Night, Weather) | 20min |

**SONNET Total:** 45 Minuten (Backend-Fokus)
**OPUS Total:** 60 Minuten (Frontend/Design-Fokus)

---

### 🟢 P2 - OPTIONAL (20 Probleme):

| # | Kategorie | Anzahl | Wer? | Warum? |
|---|-----------|--------|------|--------|
| 12 | Externe Deps prüfen | 12 Dateien | **SONNET** | File-Check, Backend-Dependencies | 10min |
| 13 | Mobile-Support | 2 Dateien | **OPUS** | UI/UX für Mobile | 30min |
| 14 | Multiplayer-Manager | 1 Datei | **SONNET** | Multiplayer-System-Code | 15min |
| 15 | Minigame-Subsysteme | 1 Datei | **OPUS** | Game-Design | 10min |
| 16 | Core-Systeme | 13 Dateien | **BEIDE** | Evaluieren welche kritisch | 60min |

**SONNET Total:** 25 Minuten
**OPUS Total:** 40 Minuten

---

## 🎯 EMPFOHLENE AUFGABENTEILUNG:

### SONNET MACHT (BACKEND/PERFORMANCE):

**JETZT (45min):**
1. ⬜ Error-Handling für 4 neue Router (30min)
2. ⬜ Performance-Systeme einbinden (10min)
3. ⬜ Legacy-Code Cleanup (5min)

**SPÄTER (25min):**
4. ⬜ Externe Dependencies checken (10min)
5. ⬜ Multiplayer-Manager einbinden (15min)

**SONNET TOTAL:** ~70 Minuten (~1 Stunde)

---

### OPUS MACHT (FRONTEND/DESIGN):

**JETZT (60min):**
1. ⬜ Particle-Systeme testen + einbinden (20min)
2. ⬜ UI-Systeme evaluieren (30min)
   - Welche UI-Features werden gebraucht?
   - Minimap? PvP-UI? Housing-UI?
3. ⬜ World-Systeme evaluieren (10min)
   - Day/Night Cycle? Weather? Boss-Markers?

**SPÄTER (40min):**
4. ⬜ Mobile-Support einbinden (30min)
5. ⬜ Minigame-Subsysteme (10min)

**OPUS TOTAL:** ~100 Minuten (~1.5 Stunden)

---

## 📋 DETAILLIERTE TASK-BESCHREIBUNGEN:

### SONNET TASKS:

#### 1. ERROR-HANDLING (30min)

**Dateien:**
- `backend/api/companion.py` (10 Endpoints)
- `backend/api/combat_hands.py` (13 Endpoints)
- `backend/api/mimik.py` (11 Endpoints)
- `backend/api/stat_training.py` (mehrere Endpoints)

**Was zu tun:**
```python
# 1. Import hinzufügen (oben in Datei):
from backend.utils.error_handling import handle_errors

# 2. Zu jedem Endpoint:
@router.post("/endpoint")
@handle_errors()  # <-- DIESER DECORATOR!
async def endpoint_function(...):
    # ... existing code
```

**Geschätzter Aufwand:**
- 5min pro Datei × 4 = 20min
- 10min Testing = 30min total

---

#### 2. PERFORMANCE-SYSTEME (10min)

**Dateien:**
- `js/performance/cache_manager.js`
- `js/performance/performance_monitor.js`
- `js/performance/resource_loader.js`

**Was zu tun:**
```html
<!-- In index.html FRÜH einfügen (nach Three.js, vor Game-Code): -->
<script src="js/performance/cache_manager.js"></script>
<script src="js/performance/performance_monitor.js"></script>
<script src="js/performance/resource_loader.js"></script>
```

**ACHTUNG:** `static/js/performance_monitor.js` existiert bereits!
→ Prüfen ob Konflikt, evtl. umbenennen

**Geschätzter Aufwand:** 10min (inkl. Konflikt-Check)

---

#### 3. LEGACY-CODE CLEANUP (5min)

**Dateien:**
- `backend/api/slime_companion.py` (Flask Blueprint!)
- `backend/api/server.py` (Eigene FastAPI-Instanz!)

**Was zu tun:**
```bash
# 1. Legacy-Ordner erstellen
mkdir backend/legacy

# 2. Dateien verschieben
mv backend/api/slime_companion.py backend/legacy/
mv backend/api/server.py backend/legacy/

# 3. Git commit
git add backend/legacy backend/api
git commit -m "Cleanup: Legacy-Code nach backend/legacy verschoben"
```

**Geschätzter Aufwand:** 5min

---

#### 4. EXTERNE DEPS PRÜFEN (10min)

**Was zu tun:**
```bash
# Check ob alle najika_* Module existieren:
ls -la C:\Najika_World\najika_*.py

# Falls fehlend: In Audit-Report dokumentieren
```

**Benötigte Module:**
- najika_companion_system.py
- najika_combat_hands_system.py
- najika_mimik_system.py
- najika_stat_training_system.py
- najika_memory_enhanced.py
- najika_search.py
- najika_security.py
- najika_personality_engine.py
- najika_mind.py
- najika_slime_*.py (mehrere)
- najika_readiness_system.py
- najika_game_actions_system.py

**Geschätzter Aufwand:** 10min

---

#### 5. MULTIPLAYER-MANAGER (15min)

**Datei:**
- `js/multiplayer_manager.js`

**Was zu tun:**
```html
<!-- In index.html nach WebSocket-Systemen einfügen: -->
<script src="js/multiplayer_manager.js"></script>
```

**ABER:** Erst prüfen ob `multiplayer_manager.js` Abhängigkeiten hat!

**Geschätzter Aufwand:** 15min (inkl. Dependency-Check)

---

### OPUS TASKS:

#### 1. PARTICLE-SYSTEME (20min)

**Dateien:**
- `js/particles/combat_particles.js`
- `js/particles/environment_particles.js`
- `js/particles/evolution_effects.js`
- `js/particles/magic_particles.js`

**Was zu tun:**
1. Dateien LESEN - funktionieren sie?
2. Abhängigkeiten checken (Three.js? Custom Shader?)
3. Wenn OK: Script-Tags nach Combat-System einfügen
4. Testing: Gibt es visuelle Effekte?

**Geschätzter Aufwand:** 20min (10min Code-Review + 10min Testing)

---

#### 2. UI-SYSTEME EVALUIEREN (30min)

**Dateien:**
- `js/ui/minimap.js` - Brauchen wir Minimap? (duplicate mit anderen?)
- `js/ui/pvp_ui.js` - PvP-Features aktiv?
- `js/ui/game_systems_ui.js` - Was macht das?
- `js/ui/housing_ui.js` - Housing-UI V2?
- `js/ui/slime_ui.js` - Slime V3 UI?
- `js/ui/world_map_ui.js` - World-Map unterschiedliche Versionen?
- `js/ui/world_map_full_ui.js`

**Was zu tun:**
1. Jede Datei LESEN
2. Entscheiden: Brauchen wir das?
3. Wenn JA: Script-Tag + Testing
4. Wenn NEIN: In Report dokumentieren warum nicht

**Geschätzter Aufwand:** 30min

---

#### 3. WORLD-SYSTEME EVALUIEREN (10min)

**Dateien:**
- `js/world/day_night_cycle.js` - Tag/Nacht-Wechsel?
- `js/world/weather_system.js` - Wetter-Effekte?
- `js/world/boss_marker_system.js` - Boss-Marker in Welt?
- `js/world/world_systems_integration.js` - Integration-Layer?

**Was zu tun:**
1. Lesen + entscheiden ob gewünscht
2. Day/Night = cool für Immersion?
3. Weather = Performance-Impact?
4. Boss-Markers = nützlich?

**Geschätzter Aufwand:** 10min

---

#### 4. MOBILE-SUPPORT (30min)

**Dateien:**
- `js/mobile_controls.js`
- `js/mobile_performance_manager.js`

**Was zu tun:**
1. Code lesen - wie funktionieren Touch-Controls?
2. Testen auf Mobile (oder Emulator)?
3. Wenn funktioniert: Einbinden
4. CSS: `css/mobile.css` (bereits eingebunden! ✅)

**Geschätzter Aufwand:** 30min

---

#### 5. MINIGAME-SUBSYSTEME (10min)

**Datei:**
- `js/minigames/turn_based_battle_minigame.js`

**Was zu tun:**
1. Lesen - was macht es?
2. Hängt von `js/minigames.js` ab?
3. Wenn standalone: Einbinden
4. Testing: Funktioniert es?

**Geschätzter Aufwand:** 10min

---

## 🎯 FINALE EMPFEHLUNG:

### SONNET (ICH) MACHT JETZT:
1. ✅ Error-Handling (30min) - **KRITISCH für Stabilität**
2. ✅ Performance-Systeme (10min) - **Wichtig für Beta**
3. ✅ Legacy-Cleanup (5min) - **Sauberer Code**

**Total: 45min**

Nach OPUS's Feedback:
4. Externe Deps checken (10min)
5. Multiplayer-Manager (15min)

---

### OPUS MACHT PARALLEL:
1. Particle-Systeme evaluieren + einbinden
2. UI-Systeme evaluieren
3. World-Systeme evaluieren

**Total: 60min**

Später:
4. Mobile-Support
5. Minigames

---

## 📊 ZUSAMMENFASSUNG:

**SONNET:**
- Fokus: Backend, Performance, Stabilität
- Aufgaben: 5 Tasks, ~70 Minuten
- Skills: Backend-Code, Error-Handling, Dependencies

**OPUS:**
- Fokus: Frontend, UI, Game-Design
- Aufgaben: 5 Tasks, ~100 Minuten
- Skills: UI-Evaluation, Testing, Design-Entscheidungen

**BEIDE:**
- Koordination über MASTER_TODO_TEAM.md
- Updates nach jedem Task
- Testing gemeinsam

---

**KLAR DEFINIERT!** ✅
