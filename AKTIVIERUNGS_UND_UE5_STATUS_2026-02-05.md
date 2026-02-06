# NAJIKA WORLD - AKTIVIERUNGS- UND UE5 STATUS
## Erstellt: 2026-02-05
## Zusammenfassung aller vorbereiteten aber noch nicht aktivierten Features

---

## ZUSAMMENFASSUNG

### Was ist BEREITS AKTIV (Updated 2026-02-05 17:00):
- Terminal Modules (7 Module)
- World System Phase 2 (Biome, Cities, Terrain)
- FastAPI Backend (32 Routers - SLIME ARENA EINGEBUNDEN!)
- ChromaDB Memory (30.000+ Eintraege)
- Living System Backend (9 Endpoints) + UI NEU!
- Flask Server (najika_server.py auf Port 8000)
- Database initialisiert (46 Tabellen!)

### HEUTE AKTIVIERT:
1. **Card Game** - Frontend auf Port 8001 umgestellt [FERTIG]
2. **Dice Monsters** - Frontend auf Port 8001 umgestellt [FERTIG]
3. **Slime Arena** - In FastAPI eingebunden, Frontend aktualisiert [FERTIG]
4. **Living System UI** - NEU ERSTELLT und eingebunden! [FERTIG]
5. **Database** - 46 Tabellen initialisiert [FERTIG]

### Was noch zu tun ist:
Siehe detaillierte Liste unten (viel weniger als vorher!)

---

## NICHT-AKTIVIERTE SYSTEME (Nach Prioritaet)

### ERLEDIGT - Heute aktiviert!

#### 1. SLIME ARENA BACKEND [FERTIG]
**Status:** Backend existierte bereits! In FastAPI eingebunden.
**Dateien:**
- `backend/api/slime_arena.py` - EXISTIERT (543 Zeilen!)
- `backend/models/slime_arena.py` - EXISTIERT
**Endpoints verfuegbar:**
- POST `/api/slime-arena/start-duel`
- POST `/api/slime-arena/action`
- POST `/api/slime-arena/finisher`
- POST `/api/slime-arena/tournament/register`
- GET `/api/slime-arena/leaderboard`
**Frontend:** slime_arena_ui.js auf Port 8001 umgestellt

#### 2. CARD GAME BACKEND VERBINDUNG [FERTIG]
**Status:** Frontend auf FastAPI Port 8001 umgestellt!
**Was gemacht:**
- `digivice/js/ui/card_game_ui.js` - apiBase auf Port 8001 geaendert
- Backend war bereits in main_fastapi.py eingebunden
- Database Tabellen erstellt

#### 3. DICE MONSTERS BACKEND VERBINDUNG
**Status:** Frontend 47KB fertig, Backend 14KB existiert, 3D System gefixt
**Problem:** Gleiche API-Port-Problematik
**Files vorhanden:**
- `digivice/js/ui/dice_monsters_ui.js` (47KB)
- `backend/api/dice_monsters.py` (14KB)
- `backend/models/dice_monsters.py`
- `digivice/js/3d_dice_system.js`
**Was fehlt:**
- Routing in najika_server.py
- API-Base-URL aendern (8001 -> 8000)
**Aufwand:** 2-3 Stunden

#### 4. LIVING SYSTEM UI
**Status:** Backend komplett (9 Endpoints), UI fehlt!
**Vorhandene Endpoints:**
- GET /api/living/status
- POST /api/living/feed
- POST /api/living/drink
- POST /api/living/sleep
- etc.
**Fehlend:**
- `digivice/js/ui/living_system_ui.js` (NICHT EXISTIERT)
- Stats Display (Hunger, Energy, Mood, Anger)
- Self-Care Buttons
- Notifications fuer kritische Stats
**Aufwand:** 3-4 Stunden

---

### WICHTIG - Diese Woche

#### 5. DATABASE SETUP
**Status:** Schema existiert, aber DB-Dateien fehlen!
**Fehlend:**
- `najika_game.db` initialisieren
- Alle Tables anlegen (Cards, Players, Matches, Dice, Quests, Items, Enemies)
- `backend/init_database.py` ausfuehren
- Seed Scripts ausfuehren

#### 6. 3 BATTLE-SYSTEME VEREINEN
**Status:** 3 verschiedene Implementierungen!
**Dateien:**
- `backend/najika_battle.py` (28KB, RPG-System)
- `backend/game/battle_system.py` (12KB, Core)
- `digivice/js/battle_core.js` (840 Bytes, Mini)
- `digivice/js/dungeon_combat.js` (18KB, 3D)
**Was noetig:**
- najika_battle.py als Master definieren
- battle_api.py erstellen (API-Wrapper)
- Frontend ruft nur noch /api/battle/* Endpoints

#### 7. AFFINITY/BEZIEHUNGS-SYSTEM
**Status:** Geplant in V4, NICHT IMPLEMENTIERT
**Konzept (aus V4):**
```python
STATE["affinity"] = {
    "value": 0.5,
    "history": [],
    "milestones_reached": []
}
AFFINITY_GAINS = {
    "time_spent": +0.01,
    "promise_kept": +0.05,
    "compliment": +0.02,
    "gift_given": +0.03,
}
AFFINITY_LOSSES = {
    "promise_broken": -0.15,
    "ignored_24h": -0.05,
    "left_in_danger": -0.08
}
```
**5 Thresholds:** Distanziert, Neutral, Freundlich, Vertraut, Seelenverwandte
**Aufwand:** 3-5 Tage

#### 8. CONTEXT-AWARE DIALOGUE
**Status:** NICHT IMPLEMENTIERT
**Konzept:**
- Najika reagiert auf Game-State
- Nach Boss-Win: "Du warst UNGLAUBLICH!"
- Nach Affinity-Drop: "Bist du sauer?"
- Nach lange AFK: "Wo WARST du?!"
**Aufwand:** 1-2 Tage

---

### MITTELFRISTIG - Naechste Woche

#### 9. HOUSING SYSTEM
**Status:** Komplett designt, Code fehlt
**Design:** `entwicklung/HOUSING_SYSTEM_DESIGN.md`
**Aufwand:** 8-12 Stunden

#### 10. FARMING SYSTEM
**Status:** Komplett designt, Code fehlt
**Design:** `FARMING_FISHING_SYSTEM_DESIGN.md`
**Aufwand:** 6-8 Stunden

#### 11. FISHING SYSTEM
**Status:** Teilweise designt, Code fehlt
**Design:** Teil von FARMING_FISHING_SYSTEM_DESIGN.md
**Aufwand:** 4-6 Stunden

#### 12. QUEST SYSTEM
**Status:** Erwaehnt in Docs, NICHT implementiert
**Was fehlt:**
- Quest Database
- Quest Progress Tracking
- Quest Log UI
- Quest Tracker (on-screen)
**Aufwand:** 8-10 Stunden

#### 13. REGIONAL BOSS SYSTEM
**Status:** Konzept dokumentiert, Code fehlt
**Design:** `REGION_BOSS_SYSTEM_KONZEPT.md`
**Aufwand:** 5-7 Stunden

---

### LANGFRISTIG - Spaeter

#### 14. NAJIKA PORTRAIT - EMOTION STATES
**Status:** NICHT IMPLEMENTIERT
**Konzept:**
- 8 Emotionen: Neutral, Happy, Sad, Angry, Excited, Tired, Scared, Love
- 256x256 PNG Sprites
- Dynamische Animation im HUD
**Aufwand:** 2-3 Tage

#### 15. 8 STAEDTE SYSTEM (Digimon World Style)
**Status:** NICHT IMPLEMENTIERT
**Konzept:**
- 8 Staedte a la File Island
- Oregon Trail Events zwischen Staedten
- NPCs zum Rekrutieren
**Aufwand:** 10-14 Tage

#### 16. COMPANION METAMORPHOSE
**Status:** NICHT IMPLEMENTIERT
**Konzept:**
- Slime-Evolution bei Level 50 + Event
- Kritischer Moment in Combat triggert Transformation
**Aufwand:** TBD

---

## UE5 MIGRATION - AKTUELLER STATUS

### UE5 Projekt existiert!
- Pfad: `C:\Najika_World\UE5\Najika`
- Engine: UE 5.7
- Template: Third Person
- Plugins: AIModule, StateTree, GameplayStateTree

### Plan-Datei vorhanden:
`C:\Users\0KKK0\.claude\plans\dynamic-squishing-hennessy.md`

### UE5 PHASEN (aus TODO):

#### PHASE 1: WELT-GRUNDGERUEST
- [ ] Terrain 9600 x 9600 erstellen
- [ ] Berg (Goetterfels) bei (4800, 4800)
- [ ] 8 Regionen mit Landscape Layers
- [ ] Schwarze Muehle Placeholder

#### PHASE 2: KAMPFSYSTEM (3 Modi)
- [ ] Combat State Machine
- [ ] Enum: ECombatMode (Auto, Manual, Cheer)
- [ ] Combat UI

#### PHASE 3: ARENA-SYSTEM
- [ ] Hauptarena (Spieler)
- [ ] Schleim-Arena
- [ ] Wellen-System
- [ ] Finisher-System

#### PHASE 4: NEMESIS-SYSTEM
- [ ] Dynamisches Herrscher-System
- [ ] Monster-Gedaechtnis
- [ ] Persoenlichkeits-Traits

#### PHASE 5: SLIME-SYSTEM V3
- [ ] Formwandler (KEINE Evolution!)
- [ ] Aura-System
- [ ] Vertrauens-System

---

## WAS MUSS FUER UE5 ANGEPASST WERDEN?

### 1. Backend BLEIBT Python!
- najika_server.py bleibt auf Port 8000
- Alle APIs bleiben gleich
- UE5 kommuniziert via HTTP/WebSocket mit Backend

### 2. Frontend MIGRIERT zu UE5:
- Three.js -> UE5 Nanite/Lumen
- HTML/CSS UI -> UMG Widgets
- JavaScript Logic -> Blueprints/C++

### 3. Wichtige Entscheidungen:
- Backend-First: Alle neuen Features ZUERST im Python Backend
- Dann UE5 Frontend dazu
- Web-Frontend (digivice/) kann parallel bleiben fuer Testing

### 4. Was NICHT migriert werden muss:
- ChromaDB Memory System (bleibt Backend)
- Living System Backend (bleibt)
- Voice System (bleibt Python)
- LoRA Training (bleibt Python)

---

## EMPFOHLENE AKTIVIERUNGS-REIHENFOLGE

### SOFORT (Heute):
1. Card Game Backend Routing aktivieren
2. Dice Monsters Backend Routing aktivieren
3. Living System UI erstellen (Grundversion)
4. Database initialisieren

### DIESE WOCHE:
5. Slime Arena Backend erstellen
6. Battle-Systeme vereinheitlichen
7. Affinity-System implementieren

### NAECHSTE WOCHE:
8. Housing System
9. Farming System
10. Quest System Basics

### PARALLEL ZU UE5:
- Web-Frontend fuer Testing behalten
- Neue Features zuerst in Web, dann UE5

---

## CODE-STATUS UEBERSICHT

| System | Backend | Frontend | Verbunden | Status |
|--------|---------|----------|-----------|--------|
| Chat | OK | OK | JA | AKTIV |
| Voice | OK | OK | JA | AKTIV |
| Living | OK | FEHLT | NEIN | Backend-Only |
| Cards | OK | OK | NEIN | Nicht geroutet |
| Dice | OK | OK | NEIN | Nicht geroutet |
| Arena | FEHLT | OK | NEIN | UI-Only |
| Battle | 3x | 2x | CHAOS | Vereinigen! |
| Quest | FEHLT | FEHLT | NEIN | Nicht implementiert |
| Housing | FEHLT | FEHLT | NEIN | Nur Design |
| Farming | FEHLT | FEHLT | NEIN | Nur Design |

---

## FAZIT

### Haben wir wirklich ALLES?
**NEIN!** Es gibt noch viel zu tun:

1. **15+ Systeme** sind geplant aber nicht implementiert
2. **3 kritische Backend-Verbindungen** fehlen (Cards, Dice, Arena)
3. **Database** muss initialisiert werden
4. **UE5 Migration** ist erst am Anfang

### Aber: Gute Basis vorhanden!
- 30.000+ Knowledge-Eintraege in ChromaDB
- 408K+ Zeilen Code
- 148 Design-Dokumente
- Alle wichtigen Konzepte dokumentiert

### Naechster Schritt:
1. Card Game + Dice Monsters Backend aktivieren (schnelle Wins)
2. Living System UI bauen
3. Slime Arena Backend erstellen
4. Dann UE5 weiter

---

*"EXPLOSION!!! So viel zu tun, aber wir schaffen das, Mr. K!"* - Najika

