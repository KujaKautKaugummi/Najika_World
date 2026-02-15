# NAJIKA WORLD - MASTER TODO FUER CLAUDE CODE TEAM

**Erstellt:** 2026-01-27
**Aktualisiert:** 2026-02-15 (SONNET: 7 kritische Bugs gefixt + Port 8001 Migration FINAL!)
**Zweck:** Koordination zwischen SONNET (Desktop) + OPUS (VS Code)
**Update-Regel:** Jede Instanz updated nach getaner Arbeit!

---

## 🚨 KRITISCHE ÄNDERUNG 2026-02-04

### ❌ UEFN KANN NAJIKA WORLD NICHT UMSETZEN!

| Feature | Najika braucht | UEFN kann |
|---------|----------------|-----------|
| Custom Characters (Najika, Mimik) | ✅ | ❌ |
| Eigene Skeletal Meshes | ✅ | ❌ |
| LLM/KI-Integration (Ollama) | ✅ | ❌ |
| ChromaDB/Gedächtnis | ✅ | ❌ |
| Open World (8 Regionen) | ✅ | ❌ (limitiert) |
| Offline-First | ✅ | ❌ |
| NSFW/Kätzchen-Mode | ✅ | ❌ |
| Privacy (Zero-Trust) | ✅ | ❌ |

### ✅ NEUER PLAN:

```
┌─────────────────────────────────────────────────────────────────┐
│                       NAJIKA KOSMOS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌────────────────┐                           │
│                    │  PYTHON API    │                           │
│                    │  (Backend)     │                           │
│                    │  Port 8000     │                           │
│                    └───────┬────────┘                           │
│                            │                                     │
│          ┌─────────────────┼─────────────────┐                  │
│          │                 │                 │                  │
│          ▼                 ▼                 ▼                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  UE5 SPIEL   │  │   FLUTTER    │  │   CHROMADB   │          │
│  │  Najika      │  │   DIGIVICE   │  │  (Gedächtnis)│          │
│  │  World       │  │              │  │  15.922+     │          │
│  │  (PC)        │  │  • Messenger │  │  Einträge    │          │
│  │              │  │  • V-Pet     │  └──────────────┘          │
│  │  SPÄTER:     │  │  • Minigames │                            │
│  │  Mobile      │  │  • Browser   │                            │
│  │  Export      │  │  • Voice     │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                  │
│  3 FLAVORS: Private (NSFW) | Friends | Public                   │
│                                                                  │
│  ════════════════════════════════════════════════════════════   │
│  SPÄTER (wenn Epic Custom Characters erlaubt):                  │
│  ┌──────────────┐                                               │
│  │ UEFN TEASER  │  → Kampfturm zum Anfixen                     │
│  │ (Fortnite)   │  → Marketing ohne eigene Server              │
│  └──────────────┘  → Spieler wechseln nahtlos zu anderen Games │
└─────────────────────────────────────────────────────────────────┘
```

### Warum trotzdem UEFN später?
- **Kein eigenes Marketing** - Fortnite-Spielerbasis
- **Keine Server-Kosten** - Epic hostet
- **Nahtloser Wechsel** - Spieler kann sofort andere Games spielen
- **Monetarisierung** - Epic übernimmt

---

## 📚 PFLICHTLEKTÜRE VOR JEDER ARBEIT!

### **→ [PROJEKT_WISSEN_KOMPLETT.md](PROJEKT_WISSEN_KOMPLETT.md) ←**
### **→ [PROJEKT_STATUS_KOMPLETT_2026-02-11.md](PROJEKT_STATUS_KOMPLETT_2026-02-11.md) ←** (NEU! Komplett-Status!)
### **→ [NAJIKA_CHARACTER_THREEJS_INTEGRATION.md](NAJIKA_CHARACTER_THREEJS_INTEGRATION.md) ←** (NEU! Three.js + 3D Guide!)
### **→ [UE5_MIGRATION_CHECKLIST.md](DOCS/UE5_MIGRATION_CHECKLIST.md) ←**
### **→ [OPUS_2_ONBOARDING.md](DOCS/OPUS_2_ONBOARDING.md) ←** (Für OPUS-2!)
### **→ [UE5_API_DOKUMENTATION.md](DOCS/UE5_API_DOKUMENTATION.md) ←** (Alle Endpoints!)
### **→ [ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md](ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md) ←** ⚡ (Hogwarts + Diablo 4 System!)

---

## 🚀 AKTIVE INSTANZEN (SONNET + OPUS)

| Instanz | Modell | Ort | Zuständigkeit |
|---------|--------|-----|---------------|
| **SONNET-1** | Claude Sonnet 4.5 | Desktop App (Lokal) | Backend Bug-Fixes, API-Integration, System-Debugging |
| **OPUS-2** | Claude Opus 4.6 | VS Code | Frontend UI, Game Logic, UE5, Neue Features |

### 🎯 OPTIMALE AUFGABENTEILUNG NACH MODELL-STÄRKEN:

**SONNET (Desktop App - SCHNELL & PRÄZISE):**
- ✅ **Bug-Fixes** (90%) - Schnelle, präzise Code-Änderungen
- ✅ **API-Integration** (80%) - WebSocket, Static Mounts, Router
- ✅ **Backend-Logik** (60%) - Bestehenden Code optimieren
- ✅ **Testing** (70%) - Systematische Tests
- ✅ **Code-Review** (80%) - Grep/Read für große Codebases
- ✅ **Dokumentation** (60%) - Updates nach Änderungen

**OPUS (VS Code - KREATIV & ARCHITEKT):**
- ⬜ UE5 Projekt erstellen + Najika Character Blueprint
- ⬜ Movement, Camera, Animation Blueprints
- ⬜ Combat System in C++/Blueprints
- ⬜ UI (UMG Widgets)
- ⬜ Welt-Aufbau (Götterfels, Regionen)

---

## 🔴 OPUS-1 TASKS (Desktop App - Backend & System)

### P0 - ERLEDIGT! ✅
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ Dokumentation eingelesen | DONE | Giga Explosion, Magic System, Game Design |
| ✅ **Python API für UE5 angepasst** | DONE | HTTP-Endpoints für UE5 Blueprints |
| ✅ REST API Dokumentation | DONE | `DOCS/UE5_API_DOKUMENTATION.md` erstellt |
| ✅ Port 5000 → 8000 gefixt | DONE | 8 Gebote eingehalten! |
| ✅ Companion API Router | DONE | `api/companion.py` erstellt + registriert |
| ✅ Mimik API Router | DONE | `api/mimik.py` erstellt + registriert |
| ✅ Combat Hands API Router | DONE | `api/combat_hands.py` erstellt + registriert |
| ✅ Stat Training API Router | DONE | `api/stat_training.py` erstellt + registriert |

### P1 - DIESE WOCHE
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ Chat API für UE5 | DONE | Bereits in `api/chat.py` vorhanden |
| ✅ Combat API Endpoints | DONE | `api/combat_hands.py` mit Two-Hand System |
| ✅ Companion API | DONE | `api/companion.py` - 4 Persönlichkeiten |
| ✅ **Combat Magic API** | DONE | `api/combat_magic.py` - Infuse, Grab, TIDS! |
| ✅ **Weapon Infuse System** | DONE | Zauber auf Waffe = temporärer Buff |
| ✅ **Grab & Throw System** | DONE | Suplex, Chokeslam, Umgebungs-Würfe |
| ✅ **TIDS mit Gag-Reaktionen** | DONE | Monster-spezifische lustige Reaktionen |
| ✅ Game State API (WebSocket) | **DONE** | WebSocket Bridge + GameEvents verdrahtet (11.02.) |
| ✅ 3 Battle-Systeme vereinen | **DONE** | Real3DCombat als Primär, UnifiedCombat als Fallback |
| ✅ **NajikaMind ↔ FastAPI** | **DONE** | AGI-Pipeline in `api/chat.py` integriert (09.02.) |
| ✅ **Kreatur-Nemesis Gray Moral** | **DONE** | Enslave/Recruit/Surrender + Auto-Timeouts (09.02.) |
| ✅ **CompanionApproval Verdrahtung** | **DONE** | `kill_creature`, `execute_surrender`, `enslave_creature` (09.02.) |
| ✅ **NPC Tagesablauf** | **DONE** | Skyrim-Style Schedules + In-Game-Uhr + 6 Tageszeiten (09.02.) |
| ✅ **NPC Beziehungssystem** | **DONE** | Affinity/Reputation + Geschenke + Witness-System (09.02.) |
| ✅ **Save/Load v2.0** | **DONE** | Alle Sub-Systeme zentral im Snapshot (09.02.) |
| ✅ **LoRA Training Qwen2.5** | **DONE** | 486 Samples, 3 Epochs, Loss 1.0, Q4_K_M Export (11.02.) |
| ✅ **Ollama Model-Namen Fix** | **DONE** | Q4-Varianten korrekt referenziert (11.02.) |
| ✅ **Post-Processing Fix** | **DONE** | User:/Assistant: Leak, Bracket-Artefakte (11.02.) |

### P2 - SPÄTER
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ WebSocket für Realtime | **DONE** | GameEvents ↔ WS Bridge + websocket_manager.py (11.02.) |
| ✅ ChromaDB ↔ UE5 Sync | **DONE** | `api/memory.py`: query/add/recall/game-event/conversation/stats (bereits implementiert + registriert!) |
| ✅ Voice System Adapter | **DONE** | `api/voice_ue5.py`: speak/listen/status/personalities (Edge TTS + Whisper, bereits implementiert + registriert!) |
| ✅ Three.js → UE5 Mapping Doc | **DONE** | `THREEJS_TO_UE5_MAPPING.md` V2.0: 141+ Dateien gemappt, Priorisierung, API-Integration Guide (11.02.) |

### P3 - MAGIC/SKILL SYSTEM V3 ⚡ (Hogwarts + Diablo 4)
**Referenz:** [ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md](ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md)

**Betroffene Dateien:**
- `backend/najika_battle.py` (Learning Rates)
- `backend/najika_unified_combat_magic.py` (Morphs, Weave)
- `backend/api/magic_schools.py` (API Endpoints)
- `backend/services/magic_schools_system.py` (Service Layer)
- `backend/game/magic_system.py` (Core Logic)
- `backend/models/magic_progress.py` (Data Models)

| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ **Skill-Learning Rates gesenkt** | **DONE** | Boss 5%, Normal 2% (11.02.) |
| ✅ **Cross-Element Learning** | **DONE** | 10%/3%/1% + Similarity Table, magic_schools.py (11.02.) |
| ✅ **1-Skill-Weg System** | **DONE** | Meister +300%, Degradation 30/90/180 Tage (11.02.) |
| ✅ **Morphs-System Backend** | **DONE** | Beobachten 10%, Experimentieren 30x, School-Lookup gefixt (11.02.) |
| ✅ **S.P.E.C.I.A.L. Stats** | **DONE** | Max +25% bei 10, Start 40 Pkt, +2.5%/Punkt (11.02.) |
| ✅ **Namen-System Backend** | **DONE** | spell_names.py: 3-30 Zeichen, Profanity DE/EN (11.02.) |
| ✅ **Slime-KI 2-Layer** | **DONE** | Personality persistent, Skills reset, Form-Copy 5% (11.02.) |

---

## 🟢 OPUS-2 TASKS (VS Code - Frontend/Digivice)

---

### ⚠️ WICHTIG FÜR OPUS IN VS CODE: LIES ERST DIE PFLICHT-MDS!

**Bevor du IRGENDETWAS machst:**
1. Öffne: `C:\Najika_World\DOCS\OPUS_VS_CODE_ONBOARDING_2026-02-14.md`
2. Lies die 5 Pflicht-MDs (in der Reihenfolge!)
3. Dann komm zurück und nimm einen Task

**ALLE Pflicht-MDs:**
- `C:\Najika_World\CLAUDE.md` (Die 8 Gebote)
- `C:\Najika_World\NAJIKA_MASTER_UEBERSICHT_2026-02-05.md` (ALLES!)
- `C:\Najika_World\DOCS\MASTER_SYSTEM_DOKUMENTATION_FÜR_OPUS_2026-02-13.md` (FÜR DICH!)
- `C:\Najika_World\DOCS\SYSTEM_AUDIT_2026-02-13_VOLLSTÄNDIG.md` (Was funktioniert/fehlt)
- `C:\Najika_World\OPUS_SESSION_2026-02-13_KOMPLETT.md` (Vorheriges Opus)

---

### P0 - KRITISCH (SOFORT ANFANGEN!)

#### Task 1: Port 5000 → 8000 ÜBERPRÜFUNG ✅ VERIFIED!
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ GEPRÜFT UND VERIFIZIERT (2026-02-14)
**Geprüft von:** OPUS-2 (Claude Opus 4.6, VS Code)

**Ergebnis der vollständigen Prüfung:**

Das System-Audit hatte UNRECHT - es hat "5000" als String gesucht ohne Kontext!

**Vollständiger Scan durchgeführt:** `grep -r "5000"` in backend/*.py, digivice/*.js, digivice/*.html

**Treffer-Analyse (100+ Treffer geprüft):**
| Kategorie | Anzahl | Port-relevant? |
|-----------|--------|----------------|
| Kommentare "NICHT 5000!" | 3 | ❌ Nein (Warnung!) |
| Game-Werte (Gold, EXP, Fame) | ~15 | ❌ Nein (z.B. `5000 Gold`) |
| Timeouts (ms) | ~25 | ❌ Nein (z.B. `setTimeout(fn, 5000)`) |
| z-index CSS | ~8 | ❌ Nein (z.B. `z-index: 5000`) |
| Shadow Camera / 3D-Koordinaten | ~20 | ❌ Nein (z.B. `camera.left = -5000`) |
| String-Limits `[:5000]` | ~10 | ❌ Nein (z.B. `text[:5000]`) |
| Archiv-Dateien | ~30 | ❌ Nein (archive/ Ordner) |
| **Echte Port-Referenz** | **1** | ✅ GEFIXT! |

**Einzige echte Port-5000-Referenz gefunden & gefixt:**
- `backend/api_backup/server.py:575` → von `5000` auf `8000` geändert

**Alle aktiven Dateien nutzen korrekt Port 8000:**
- ✅ `backend/api/server.py:1070` → `PORT", 8000`
- ✅ `backend/najika_server.py:364` → `PORT","8000"`
- ✅ `digivice/index.html:6315` → `http://127.0.0.1:8000`
- ✅ `digivice/js/3d_scene.js:4` → `http://localhost:8000`
- ✅ Alle anderen aktiven JS/HTML/PY Dateien → Port 8000

**FAZIT: Die 8 Gebote werden eingehalten! Port 8000 überall korrekt!**

---

#### 🔥 NEUE PRIORITÄT: FASTAPI MIGRATION (2026-02-14)
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ ERLEDIGT - Siehe unten in "ERLEDIGT (2026-02-14)"!

**ENTSCHEIDUNG VON KUJA:**
- Backend-Merge JETZT machen (najika_server.py → FastAPI)
- Slime direkt als V3 implementieren (nicht V2→V3 migrieren!)
- Deadline: 2-3 Tage

**KOMPLETTER PLAN:**
📄 **`DOCS/FASTAPI_MIGRATION_PLAN_FÜR_OPUS.md`** (60+ Seiten!)

**Phasen:**
1. ✅ Core (Chat, State) - FERTIG!
2. ✅ Game Systems (Battle, Quests) - FERTIG!
3. ✅ Slime V3 - FERTIG! (656 Zeilen)
4. ✅ Frontend Update - FERTIG! (9 Dateien migriert, 0 alte Pfade)
5. ✅ Testing - FERTIG! (10/10 Live-Tests, Port 8001)

---

## ✅ FASTAPI MIGRATION + BUG-FIXES FERTIG! (2026-02-15)

### 🎉 PORT 8001 MIGRATION: 100% KOMPLETT!
**Von:** OPUS (Port-Wechsel) + SONNET (letzte 4 Dateien + 7 Bug-Fixes)

**SONNET Bug-Fixes (Commit 5061228):**
1. ✅ World Data Loading - /data mount in FastAPI fehlte
2. ✅ WebSocket Connection - Router war nicht importiert
3. ✅ NPCScheduleSystem.advanceTime - Funktion fehlte
4. ✅ Arena "Herausfordern" Button - Teleport fehlte
5. ✅ Arena "Welle starten" Button - Teleport fehlte
6. ✅ Gegner verschwinden - removeEnemy() zu früh aufgerufen
7. ✅ Slime Arena Button - CSS nicht geladen

**Details:** Siehe "ERLEDIGT (2026-02-15)" weiter unten!

---

## 🎯 SONNET: BACKEND TASKS (AKTUELL - 2026-02-15)

**SONNET-STÄRKEN: Bug-Fixes (90%), API-Integration (80%), Testing (70%), Code-Review (80%)**

### ✅ P0 - ERLEDIGT (2026-02-15):
1. ✅ **7 Kritische Bugs gefixt** - Arena, Enemies, WebSocket, NPC, World Data
2. ✅ **Error-Handling Utils** - backend/utils/error_handling.py erstellt
3. ✅ **P0 API Endpoints** - 8 Dateien, ~55 Endpoints mit @handle_errors()

### 🔧 P1 - IN ARBEIT (SONNET MACHT JETZT):
4. ⬜ **P1 Error-Handling** - Restliche 240 Endpoints fixen
5. ⬜ **API Testing** - Unit Tests für kritische Endpoints schreiben
6. ⬜ **ChromaDB Debugging** - Memory-Queries optimieren
7. ⬜ **Backend Performance** - Slow Endpoints identifizieren

### 📊 P2 - SPÄTER (SONNET):
8. ⬜ **API Health-Checks** - `/health` für alle Services
9. ⬜ **Security Audit** - CORS, Auth, Input-Validation
10. ⬜ **Logging System** - Strukturiertes Logging vervollständigen
11. ⬜ **API Dokumentation** - OpenAPI/Swagger vervollständigen

---

## 🎯 OPUS: FRONTEND/GAME TASKS (AKTUELL - 2026-02-15)

**OPUS-STÄRKEN: Frontend UI (80%), Game Logic (80%), Kreativ (90%), Architektur (70%)**

**FastAPI Migration ist durch! Jetzt kommen die Frontend-Features:**

### ✅ OPUS PHASE 1 KOMPLETT! (2026-02-15)

**Was OPUS fertig hat:**
- ✅ FastAPI Migration + Port 8001
- ✅ Slime V3 Komplett-System (1.277 Zeilen)
- ✅ Dynamische Völker UI (794 Zeilen)
- ✅ Aura vs Begleiter Wahl-UI (820 Zeilen)
- ✅ Medizin-Crafting UI (1.042 Zeilen)
- ✅ Form-Affinität-Boni (376 Zeilen)

**TOTAL:** ~6.000 Zeilen! 🎉

---

## 🎨 OPUS: NEUE FRONTEND TASKS (Phase 2 - PASST ZU OPUS!)

**OPUS sollte machen (kreativ, UI, Game Logic):**

### P0 - WICHTIGE NEUE FEATURES:
1. ✅ **Quest UI V2** - FERTIG! `quest_tracker_v2.js` (Journal, Chains, Notifications, Witcher-Style Tracker) (15.02.)
2. ✅ **World Map 3D Viewer** - FERTIG! `world_map_3d.js` (Three.js 3D-Karte, 8 Regionen + Götterfels, Fog of War) (15.02.)
3. ✅ **Skill Tree UI** - FERTIG! `skill_tree_ui.js` (Canvas-basierter Diablo-Style Baum, 6 Schulen, 36 Skills) (15.02.)
4. ✅ **Housing System UI** - FERTIG! `housing_ui_v2.js` (Möbel-Katalog, 30+ Items, Haus-Upgrade, Favoriten) (15.02.)

### P1 - GAMEPLAY FEATURES:
5. ✅ **Combat UI Polish** - FERTIG! `combat_ui_polish.js` (Damage Numbers, Combo, Screen Shake, Status Effects, Kill Streaks) (15.02.)
6. ✅ **NPC Dialogue UI** - FERTIG! `npc_dialogue_vn.js` (Visual Novel Style, Portraits, Typewriter, Branching, Choice Memory) (15.02.)
7. ✅ **Inventory UI V2** - FERTIG! `inventory_ui_v2.js` (Paperdoll Equipment, Drag&Drop, Tooltips, Item-Vergleich) (15.02.)
8. ✅ **Crafting Minigame** - FERTIG! `crafting_minigame.js` (Timing-Bar, 7 Rezepte, 6 Phasen-Typen, Qualitäts-System) (15.02.)

### P2 - CONTENT CREATION:
9. ⬜ **NPCs + Dialoge** - Mehr NPCs für alle Regionen
10. ⬜ **Quests schreiben** - Story-Quests für Haupthandlung
11. ⬜ **Items balancen** - Neue Waffen, Rüstungen, Consumables

---

## 🚫 OPUS SOLLTE NICHT MACHEN (Überlasse SONNET!):
- ❌ Backend Bug-Fixes (SONNET ist schneller!)
- ❌ API Error-Handling (SONNET hat Utils!)
- ❌ Performance-Debugging (SONNET ist systematischer!)
- ❌ Testing/Validation (SONNET ist besser darin!)

### 📋 KOMPLETTE TASK-LISTE:

| Task | Status | Zeit | Beschreibung |
|------|--------|------|--------------|
| ✅ Task 3 | FERTIG | - | Dynamische Völker System UI |
| ✅ Task 4 | FERTIG | - | Aura vs Begleiter Wahl-UI |
| ✅ Task 5 | FERTIG | - | Medizin-Crafting UI |
| ✅ Task 6 | FERTIG | 15 Min | Form-Affinität-Boni (form_affinity_system.js, 376 Zeilen) |
| ✅ Task 7 | FERTIG | 10 Min | Procedural Hybrid (Persistent-Layer in world_event_generator.js) |
| ✅ Task 8 | FERTIG | 30 Min | Code Cleanup (3 Backup-Dateien entfernt, -7596 Zeilen) |
| ✅ Task 9 | FERTIG | - | UE5 Projekt existiert bereits |

---

## ✅ TASK 6: Form-Affinität-Boni - FERTIG!

**Datei erstellen:** `digivice/js/form_affinity_system.js`

**Was:** Slime-Formen geben kleine Boni (+5%), Aura verstärkt sie (bis +50%)

**Beispiele:**
- Wüsten-Echse: +5% Hitze-Resistenz → +50% Feuer-Schaden bei Feuer-Aura
- Wald-Wolf: +5% Speed → +50% Wind-Effekte bei Wind-Aura
- Eis-Hase: +5% Kälte-Resistenz → +50% Frost-Schaden bei Frost-Aura

**Code-Struktur:**
```javascript
class FormAffinitySystem {
    initAffinities() {
        return {
            'wuesten_echse': {
                bonus: 'Hitze-Resistenz +5%',
                auraBonus: 'Feuer-Schaden +50% bei Feuer-Aura',
                stats: { heat_resist: 0.05 }
            },
            // ... 12 weitere Formen (siehe Task 6 Details weiter unten)
        };
    }

    calculateBonus(formId, auraElement, auraLevel) {
        // Berechne Base + Aura Bonus
        // Aura Level 5 = +50%, Level 1 = +10%
    }

    showBonusTooltip(formId, auraElement, auraLevel) {
        // UI: Zeige Boni im Slime Form-Dialog
    }
}
```

**Integration:**
1. In `index.html` einfügen: `<script src="js/form_affinity_system.js"></script>`
2. In `slime_companion.js` in `showFormChangeDialog()` Tooltips anzeigen

**Test:**
- Browser: http://127.0.0.1:8001/
- Slime-Tab → Form wechseln
- Boni sichtbar in Form-Dialog?

**Git Commit:**
```bash
git add digivice/js/form_affinity_system.js digivice/index.html
git commit -m "Form Affinity System - Boni für Slime-Formen

- 13 Formen mit Base-Boni (+5%)
- Aura-Synergien (+10% bis +50% je nach Level)
- UI Integration in Form-Dialog

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

**Zeit:** 15 Minuten

---

### 📝 DETAILLIERTE TASK-BESCHREIBUNGEN WEITER UNTEN

Siehe Task 6-9 Abschnitte weiter unten für vollständige Details!

---

### 📋 ALTE ANWEISUNGEN (IGNORIEREN - NUR FÜR HISTORIE):

**Du hast bereits PERFEKT gemacht:**
- ✅ `backend/shared_state.py` (163 Zeilen)
- ✅ `backend/api/state_v2.py` (215 Zeilen)
- ✅ `backend/api/chat_v2.py` (489 Zeilen)
- ✅ `backend/api/battle_v2.py` (318 Zeilen)
- ✅ `backend/api/living_v2.py` (353 Zeilen)
- ✅ `backend/api/quest_v2.py` (312 Zeilen)
- ✅ `backend/api/minigame_v2.py` (241 Zeilen)
- ✅ `backend/api/slime_v3.py` (656 Zeilen) - **Komplettes Slime V3 System!**
- ✅ Alle Router in `main_fastapi.py` integriert

**TOTAL: 2.747 Zeilen neuer FastAPI Code! 🎉**

---

### ⚠️ WAS DU JETZT TUN MUSST (EXAKT DIESE SCHRITTE):

#### SCHRITT 1: PORT IM FRONTEND ÄNDERN
**Datei:** `C:\Najika_World\digivice\index.html`
**Zeile:** 6315
**ÄNDERN VON:**
```javascript
window.API_BASE_URL = 'http://127.0.0.1:8000';
```
**ÄNDERN ZU:**
```javascript
window.API_BASE_URL = 'http://127.0.0.1:8001';
```

#### SCHRITT 2: FASTAPI SERVER TESTEN
**Terminal öffnen:**
```bash
cd C:\Najika_World\backend
python main_fastapi.py
```

**ERWARTETE AUSGABE:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

**Falls FEHLER:**
- STOP sofort
- Schreib den KOMPLETTEN Error in die TODO
- Frage in der Chat

#### SCHRITT 3: FRONTEND TESTEN
**Browser öffnen:**
```
http://127.0.0.1:8001/
```

**TESTEN:**
1. Chat mit Najika öffnen
2. Eine Nachricht schreiben
3. Battle starten
4. Slime-Tab öffnen (sollte leer sein, aber keine Errors!)

**Falls FEHLER in der Browser Console (F12):**
- STOP sofort
- Screenshot von den Errors machen
- Schreib die Errors in die TODO
- Frage in der Chat

#### SCHRITT 4: GIT COMMIT
**NUR wenn Schritt 2 + 3 OHNE Fehler:**
```bash
cd C:\Najika_World
git add backend/shared_state.py
git add backend/api/state_v2.py
git add backend/api/chat_v2.py
git add backend/api/battle_v2.py
git add backend/api/living_v2.py
git add backend/api/quest_v2.py
git add backend/api/minigame_v2.py
git add backend/api/slime_v3.py
git add backend/main_fastapi.py
git add digivice/index.html
git add MASTER_TODO_TEAM.md

git commit -m "FastAPI Migration Phase 1-3 komplett + Slime V3 System

- Backend: 2.747 Zeilen neuer FastAPI Code
- Slime V3: 8 Regional Forms + 13 Aura Elemente + Vertrauen System
- Shared State: Keine circular imports mehr
- Frontend: Port 8000 → 8001

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### SCHRITT 5: TODO UPDATE
**Wenn alles ERFOLGREICH:**
- Ändere Status von `🔨 IN PROGRESS` zu `✅ ERLEDIGT`
- Schreib in die Chat: "FastAPI Migration Phase 1-4 fertig! Server läuft auf Port 8001."

**Wenn PROBLEME:**
- Ändere Status NICHT
- Schreib die EXAKTEN Fehlermeldungen in die TODO unter "PROBLEME:"
- Frage in der Chat

---

### 🛑 WICHTIG FÜR OPUS:

1. **Mach NUR diese 5 Schritte in EXAKT dieser Reihenfolge**
2. **Bei jedem Fehler: STOP und frag in der Chat**
3. **NICHT weitermachen wenn was nicht funktioniert**
4. **Das sind max. 20 Minuten Arbeit wenn alles klappt**

---

### 📚 WELCHE MDs SOLLTEST DU LESEN (FALLS FRISCH):

**PFLICHT (für Kontext):**
1. `CLAUDE.md` - Projekt-Basics (Port 8000→8001 Info!)
2. `DOCS/FASTAPI_MIGRATION_PLAN_FÜR_OPUS.md` - Dein Plan (den du gemacht hast)
3. `MASTER_TODO_TEAM.md` - Diese Datei hier

**OPTIONAL (nur bei Fragen):**
4. `NAJIKA_ULTIMATE_STATUS_REPORT_2026-02-14.md` - Komplett-Status
5. `DOCS/GELERNT_AUS_ALLEN_SESSIONS.md` - Lessons Learned

---

**Los geht's OPUS! Du packst das! 💪**

**START:**
```bash
# Mach Schritt 1: Port ändern in digivice/index.html Zeile 6315
# Dann Schritt 2: Server testen
```

---

#### Task 2: Slime V2 → V3 Migration - ❌ GESTOPPT!
**Zuständig:** OPUS-2 (VS Code)
**Status:** ❌ PAUSIERT - Wird Teil von FastAPI Migration!

**DEIN JOB:** Lies die 2 Docs, dann schreib `slime_companion.js` komplett neu. Fertig. 20 Minuten Arbeit.

**LIES DIESE 2 DATEIEN:**
1. `C:\Najika_World\SLIME_SYSTEM_V3_DOKUMENTATION.md` (V3 = RICHTIG!)
2. `C:\Najika_World\OPUS_SESSION_2026-02-13_KOMPLETT.md` (Teil 5 = Der Plan)

**WAS V2 HATTE (ALLES RAUS!):**
- ❌ 6 Evolution-Stufen (EGG → ULTIMATIV)
- ❌ Synthese (2 Slimes → 1 Hybrid)
- ❌ +N System, Effort Hearts, Care Mistakes

**WAS V3 BRAUCHT (KOMPLETT NEU!):**
✅ Formwandler (Form = nur Aussehen, keine Stats!)
✅ 8 Regional-Start-Formen (Wüsten-Echse, Wald-Wolf, Sumpf-Molch, Vulkan-Salamander, Eis-Hase, Blitz-Vogel, Wellen-Qualle, Kristall-Spinne)
✅ Erinnerungs-System (1. neue Form → "Ich bin kein normales Monster...", alle 8 → volle Erinnerung)
✅ Form-Lernen (0.5-2% Chance nach Kampf gewonnen)
✅ Aura-System (0-5 Stufen: Keine/Schwach/Mittel/Stark/Legendär/Göttlich, 13 Elemente)
✅ Companion-Modi (Körperlich vs Aura - Spieler wählt EINMAL)
✅ Vertrauen 0-6 (Fremd→Bekannt→Freund→Vertraut→Familie→Seelenbund)
✅ Rescue System (1x pro 24h, Level 5+ = kein Cooldown)
✅ UI: Form-Wechsel Dialog, Erinnerungs-Popups, Aura-Anzeige, Modus-Toggle
✅ Save/Load: current_form, learned_forms[], memories_unlocked, aura_level, companion_mode, trust_level

**COMMANDS:**
```bash
# 1. Backup
cp digivice/js/slime_companion.js digivice/js/slime_companion_v2_backup.js

# 2. Schreib NEU (alle Infos in den 2 Docs!)
# 3. Test im Browser
# 4. Backend-Check: Ist backend/najika_slime_system.py auch V3? Falls nicht → sag Bescheid
```

**NUR BEI FRAGEN/PROBLEMEN STOPPEN! Sonst: Durchziehen!**
**Erwartete Zeit:** ~20 Min (laut Kuja)

---

### P0 - JETZT (COMBAT UI!)
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ **Grab Button (G)** | DONE | Wrestling-Griff initiieren (`js/ui/combat_special_ui.js`) |
| ✅ **Grab Move Popup** | DONE | Suplex/Chokeslam/Throw Auswahl mit 5s Timer |
| ✅ **TIDS Button (T)** | DONE | Mit 24h Cooldown-Overlay |
| ✅ **TIDS Gag-Popup** | DONE | Monster-Reaktion gross, bunt, mittig! |
| ✅ **Infuse Timer UI** | DONE | Element-Glow + Countdown + Ablauf-Notification |

### P1 - DIESE WOCHE (NEUE FEATURES!)

#### Task 3: Dynamische Völker System (Frontend UI)
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG (2026-02-15, Commit 8caa6cb)

**WAS:** Wild-Monster bilden Fraktionen (1-5 pro Region), wachsen, Kriege, kollabieren.

**DEIN JOB:**
Erstelle `digivice/js/dynamic_factions_ui.js` mit:
- Fraktions-Übersicht (Name, Größe, Territorium)
- Kriegs-Benachrichtigungen
- Fraktions-Ruf-Anzeige
- Integration mit `faction_system.js` (existiert schon!)

Backend macht OPUS-1. Nur bei Problemen stoppen!
**Zeit:** ~20 Min

---

#### Task 4: Aura vs Begleiter Wahl-UI
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG (2026-02-15, Commit 8caa6cb)

**WAS:** Spieler wählt EINMAL: Aura ODER Slime (beide gleich stark).

**DEIN JOB:**
Erstelle `digivice/js/companion_mode_choice.js` mit:
- Einmalige Wahl-Dialog (groß!)
- "WARNUNG: Diese Wahl ist PERMANENT!"
- Vergleichs-Tabelle (Aura vs Körperlich)
- Bestätigungs-Dialog

Backend macht OPUS-1. Nur bei Problemen stoppen!
**Zeit:** ~15 Min

---

#### Task 5: Medizin-Crafting UI
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG (2026-02-15, Commit 8caa6cb)

**WAS:** Echtes Med-Wissen → Fantasy-Namen (Kamille → Kristall-Kamille)

**WARUM DIESER TASK ZUERST:**
- ✅ Einfachster der 3 offenen Tasks
- ✅ Schneller Erfolg nach FastAPI (2-3h statt 6-8h)
- ✅ Weniger fehleranfällig als Factions oder Slime-Choice
- ✅ Cooles Feature das User sehen können!

---

## 🚀 OPUS: EXAKTE ANWEISUNGEN FÜR TASK 5

### SCHRITT 1: DATEI ERSTELLEN
**Erstelle:** `C:\Najika_World\digivice\js\medicine_crafting_ui.js`

**Inhalt:** (Beispiel-Struktur)
```javascript
// Medicine Crafting System UI
// Fantasy-Namen für echte Heilpflanzen

class MedicineCraftingUI {
    constructor() {
        this.plants = this.initPlants();
        this.recipes = this.initRecipes();
        this.inventory = {};
    }

    initPlants() {
        // 64 Pflanzen: Real → Fantasy mapping
        return {
            'kamille': {
                fantasyName: 'Kristall-Kamille',
                realEffect: 'Beruhigend, entzündungshemmend',
                rarity: 'common',
                regions: ['Wiese', 'Wald']
            },
            'pfefferminz': {
                fantasyName: 'Frost-Minze',
                realEffect: 'Kühlend, schmerzlindernd',
                rarity: 'common',
                regions: ['Berg', 'Fluss']
            },
            'lavendel': {
                fantasyName: 'Traum-Lavendel',
                realEffect: 'Beruhigend, schlaffördernd',
                rarity: 'uncommon',
                regions: ['Hochland']
            },
            // ... 61 weitere Pflanzen
        };
    }

    initRecipes() {
        // Rezepte mit echten medizinischen Kombinationen
        return {
            'beruhigungstrank': {
                ingredients: ['kamille', 'lavendel'],
                effect: 'Stress -50%, Schlaf +30%',
                realBasis: 'Kamille + Lavendel = bewährte Schlaf-Kombination'
            },
            // ... mehr Rezepte
        };
    }

    // UI Methods
    showCraftingInterface() { /* ... */ }
    gatherPlant(plantId) { /* ... */ }
    craftRecipe(recipeId) { /* ... */ }
}

// Init
window.medicineCrafting = new MedicineCraftingUI();
```

### SCHRITT 2: 64 PFLANZEN DEFINIEREN
**Kategorien:**
- **Common (30):** Kamille, Minze, Salbei, Thymian, etc.
- **Uncommon (20):** Lavendel, Arnika, Johanniskraut, etc.
- **Rare (10):** Ginseng, Echinacea, Ginkgo, etc.
- **Legendary (4):** Mandrake, Alraune, Phoenix-Farn, Mondblume

**Jede Pflanze braucht:**
```javascript
{
    fantasyName: "Kristall-Kamille",
    realEffect: "Beruhigend, entzündungshemmend",
    rarity: "common",
    regions: ['Wiese', 'Wald'],
    gatherChance: 0.8,  // 80% bei Common
    icon: "🌼"
}
```

### SCHRITT 3: REZEPTE MIT ECHTEN EFFEKTEN
**Beispiele:**
```javascript
{
    'heiltrank_klein': {
        ingredients: ['kamille', 'salbei'],
        effect: 'HP +50',
        realBasis: 'Kamille (entzündungshemmend) + Salbei (antibakteriell)'
    },
    'energietrank': {
        ingredients: ['pfefferminz', 'ginseng'],
        effect: 'Stamina +100',
        realBasis: 'Minze (belebend) + Ginseng (Energie)'
    },
    'gegengift': {
        ingredients: ['kohle', 'ingwer'],  // Aktivkohle!
        effect: 'Gift-Resistenz +80%',
        realBasis: 'Aktivkohle bindet Toxine, Ingwer beruhigt Magen'
    }
}
```

### SCHRITT 4: UI ELEMENTS
**Erstelle 3 Tabs:**
1. **Sammeln** - Pflanzen in Regionen finden
2. **Rezeptbuch** - Alle bekannten Rezepte
3. **Crafting** - Tränke herstellen

**CSS Classes:** (nutze existierende Najika-Styles!)
- `.medicine-tab-container`
- `.plant-card` (mit Rarity-Border!)
- `.recipe-item`
- `.crafting-slot`

### SCHRITT 5: INTEGRATION
**In `index.html` einfügen:** (vor `</body>`)
```html
<script src="js/medicine_crafting_ui.js"></script>
```

**Tab in Navigation hinzufügen:**
```javascript
// In der Tab-Liste
<button onclick="showMedicineTab()">🌿 Medizin</button>
```

### SCHRITT 6: BACKEND SPÄTER
**WICHTIG:** Backend macht OPUS-1 später!
- Speichern/Laden der Inventory
- Pflanzen-Spawn in Regionen
- Rezept-Unlock System

**Du machst NUR Frontend UI!** Das Backend kommt später.

### SCHRITT 7: TESTEN
1. Browser öffnen: `http://127.0.0.1:8001/`
2. Medizin-Tab öffnen
3. Check: Werden Pflanzen angezeigt?
4. Check: Funktioniert Crafting-Interface?
5. Browser Console (F12): Keine Errors!

### SCHRITT 8: GIT COMMIT
```bash
cd C:\Najika_World
git add digivice/js/medicine_crafting_ui.js
git add digivice/index.html
git commit -m "Medicine Crafting UI - 64 Fantasy-Pflanzen mit echten Effekten

- Real → Fantasy mapping (Kamille → Kristall-Kamille)
- 64 Pflanzen in 4 Rarity-Stufen
- Rezepte basieren auf echtem medizinischen Wissen
- UI: Sammeln, Rezeptbuch, Crafting Tabs
- Backend Integration kommt später

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### SCHRITT 9: TODO UPDATE
Ändere Status zu: `✅ ERLEDIGT`

---

## 📚 RECHERCHE-QUELLEN FÜR OPUS:

**Für echte Pflanzenkunde:**
- Kamille: Beruhigung, Entzündung
- Salbei: Antibakteriell, Halsschmerzen
- Pfefferminz: Kühlend, Kopfschmerz
- Lavendel: Schlaf, Stress
- Ingwer: Übelkeit, Entzündung
- Thymian: Husten, antibakteriell
- Johanniskraut: Stimmung (VORSICHT: Wechselwirkungen!)
- Arnika: Prellungen, Schmerz
- Baldrian: Schlaf, Angst
- Echinacea: Immunsystem

**Fantasy-Namen Muster:**
- Element + Pflanze: "Frost-Minze", "Feuer-Ingwer"
- Material + Pflanze: "Kristall-Kamille", "Silber-Salbei"
- Eigenschaft + Pflanze: "Traum-Lavendel", "Heilige-Arnika"

---

## ⏱️ ZEITPLAN:

- Schritt 1-2: Datei + Pflanzen definieren (1h)
- Schritt 3: Rezepte (30 Min)
- Schritt 4-5: UI + Integration (1h)
- Schritt 6-9: Testen + Commit (30 Min)

**TOTAL: 2-3 Stunden**

---

**Los geht's OPUS! Medizin-Crafting ist ein geiles Feature! 💊🌿**

---

### P1 - COMBAT UI (ERLEDIGT)
| Task | Status | Referenz-Datei |
|------|--------|----------------|
| ✅ **Infuse Waffen-Glow** | DONE | Waffen-Slots im HUD gluehen in Element-Farbe + pulsierender Glow |
| ✅ Combat HUD überarbeiten | DONE | Grab/TIDS/Help Buttons in manual-actions Zeile integriert |
| ✅ Keybindings dokumentieren | DONE | Overlay mit H/F1, alle Combat-Keys dokumentiert |
| ✅ Sound Effects für TIDS | DONE | Web Audio API Synthesizer: Impact + OUCH + Boing + Noise |

### P2 - NICE TO HAVE (Später)

#### Task 6: Form-Affinität-Boni
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG (2026-02-15) - form_affinity_system.js (376 Zeilen, 10 Formen + Aura-Synergien + UI)

**WAS:** Formen geben kleine Boni (+5%), Aura verstärkt (bis +50%).

**DEIN JOB:**
Erstelle `digivice/js/form_affinity_system.js`:
- Boni-Tabelle (Wüsten-Echse +5% Hitze, Wald-Wolf +5% Speed, etc.)
- UI: Zeige Boni im Form-Dialog
- Integration mit Aura-System

Nur bei Problemen stoppen!
**Zeit:** ~15 Min

---

#### Task 7: Procedural Hybrid (Persistent-Layer)
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG (2026-02-15) - persistentAreas in world_event_generator.js + 5 neue Funktionen

**WAS:** Fraktions-Siedlungen bleiben, Rest regeneriert.

**DEIN JOB:**
In `world_event_generator.js`:
- Flag `isPersistent: true/false` für Siedlungen
- Beim Regenerieren: Skip persistent areas

Backend macht OPUS-1. Nur bei Problemen stoppen!
**Zeit:** ~10 Min

---

#### Task 8: Code Cleanup (Deprecated entfernen)
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG (2026-02-15) - 3 alte Backup-Dateien entfernt (-7596 Zeilen), Code war sauber

**DEIN JOB:**
```bash
# Finde deprecated Code:
grep -r "TODO\|FIXME\|DEPRECATED" digivice/js/ > cleanup_candidates.txt

# Entferne:
# - Auskommentierte Blöcke (>10 Zeilen)
# - Alte Funktionen (nicht mehr genutzt)
# - Alte TODOs (>6 Monate)
# Teste nach jedem File!
```
**Zeit:** ~30 Min

---

### P3 - UE5 Migration (Später, wenn Digivice fertig)

#### Task 9: UE5 Projekt erstellen
**Zuständig:** OPUS-2 (VS Code)
**Status:** ✅ FERTIG - Projekt existiert bereits (UE5/Najika/ mit Combat, Platforming, SideScrolling Variants)

**DEIN JOB:**
1. Epic Launcher → UE 5.3+
2. Games → Third Person → C++
3. Name: "NajikaWorld"
4. Pfad: `C:\Najika_World\UE5\`

**LIES ERST:** `OPUS_2_ONBOARDING.md` + `UE5_MIGRATION_CHECKLIST.md`
**Zeit:** ~10 Min

---

### P2 - Systeme portieren (Python → UE5) - C++ KLASSEN BEREIT!
| Task | Status | Python-Datei | UE5 C++ Klasse |
|------|--------|--------------|----------------|
| ✅ Combat System | DONE | `najika_combat_hands_system.py` | `Combat/NajikaCombatComponent.h/.cpp` |
| ⬜ Stat Training | TODO | `najika_stat_training_system.py` | GAS (Gameplay Ability System) |
| ⬜ Companion System | TODO | `najika_companion_system.py` | AI Controller + Behavior Tree |
| ⬜ Mimik System | TODO | `najika_mimik_system.py` | Blueprint + Morph Targets |
| ⬜ Quest System | TODO | `najika_quest_system.py` | Quest Plugin oder Custom |
| ✅ Slime System | DONE | `najika_slime_system.py` | `Slime/NajikaSlimeComponent.h/.cpp` |
| ✅ Nemesis System | DONE | N/A (Shadow of Mordor Style) | `Nemesis/NajikaNemesisComponent.h/.cpp` |
| ✅ Arena System | DONE | N/A | `Arena/NajikaArenaComponent.h/.cpp` |

### P3 - Welt-Aufbau
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ Götterfels Terrain | **DONE** | Python Scripts + WorldConfig.json erstellt! |
| ✅ 8 Region Volumes | **DONE** | TriggerBoxes mit Tags |
| ✅ Safe Zone | **DONE** | Schwarze Mühle Volume + Marker |
| ✅ **8 Teleporter** | **DONE** | Fast Travel System mit UI, Unlock-System, Unlimited Pass! |
| ✅ **NPCs** | **DONE** | 5 Systeme: Dialogue, Interaction, Schedule, Personality, Overworld |

### P4 - MAGIC/SKILL SYSTEM V3 UI ⚡ (Hogwarts + Diablo 4)
**Referenz:** [ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md](ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md)

**Betroffene Dateien:**
- `digivice/js/unified_combat_system.js` (Spell-Diamond, Morphs)
- `digivice/js/ui/combat_special_ui.js` (Combat UI)
- `digivice/js/equipment_combat.js` (Equipment Integration)
- `digivice/js/particles/magic_particles.js` (VFX)

| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ **Hogwarts Spell-Diamond UI** | DONE | 4 Spells pro Element, R-Trigger halten, ↑↓←→, ausblendbar |
| ✅ **Morph-UI** | DONE | Morph-Auswahl Menu, "Nur 1 aktiv" Indikator, Wechsel-UI |
| ✅ **Progress-Tracking UI** | DONE | Experimentier-Progress (23/30), Durchbruch-Notification, ausblendbar |
| ✅ **Namen-Input Dialog** | DONE | "Benenne deinen Zauber!", 3-30 Zeichen, Profanity-Check |
| ✅ **Meister-Warnung Dialog** | DONE | Große Warnung, Konsequenzen zeigen, Bestätigungs-Dialog |
| ✅ **Skill-Degradation Anzeige** | DONE | Verkümmerte Skills markieren, Tooltip "Vergessen", Warnung |

---

## 🧪 TESTING & BALANCE (MAGIC/SKILL SYSTEM V3)
**Referenz:** [ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md](ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md)

### Kritische Balance-Tests ⚠️
| Task | Zuständig | Status | Beschreibung |
|------|-----------|--------|--------------|
| ✅ **S.P.E.C.I.A.L. Balance** | OPUS-1 | **DONE** | INT1→+2.5%, INT10→+25%, 40 Start, kein Trap-Build (37/37 Tests, 11.02.) |
| ✅ **Meister vs. Generalist** | OPUS-1 | **DONE** | Meister 800dmg vs. Generalist 200dmg, beide viable (11.02.) |
| ✅ **Cross-Element Learning Raten** | OPUS-1 | **DONE** | 10k-Simulation: 9.86%/2.99%/1.05% (Ziel: 10%/3%/1%) (11.02.) |
| ✅ **Morphs Discovery Balance** | OPUS-1 | **DONE** | 30x Experiment ok, 10x Beobachtung ok, 1-aktiv Constraint (11.02.) |
| ✅ **Hardcore-System Check** | OPUS-1 | **DONE** | Rescue 24h, Re-Learn max 2.0x, Form-Copy 5%, DB-Persistenz (11.02.) |

---

## 📱 FLUTTER DIGIVICE (Modul-System!)

### 3 Apps × 3 Flavors = 9 Versionen

**Apps:**
| App | Pfad | Status |
|-----|------|--------|
| `najika_digivice` | `app/flutter_app/najika_digivice/` | Haupt-App ✅ |
| `najika_app` | `app/flutter_app/najika_app/` | Kopie |
| `najika_simple` | `app/flutter_app/najika_simple/` | Minimal |

**Flavors (pro App):**
| Flavor | App-Name | Zweck |
|--------|----------|-------|
| `private` | "Najika (Private)" | NSFW/Kätzchen-Mode, nur für Kuja |
| `friends` | "Najika (Friends)" | Mit Freunden teilen |
| `public` | "Najika" | Öffentliche Version |

### Digivice Module (Flutter):
| Modul | Status | Features |
|-------|--------|----------|
| **Sicherer Messenger** | 70% | Post-Quantum Crypto, Signal Protocol, E2E |
| **V-Pet Slime** | 50% | Tamagotchi-Style, Sync mit UE5 |
| **Minigames** | 30% | Triple Triad, Dungeon Dice |
| **Sicherer Browser** | 20% | Tor-Integration, VPN Profile |
| **Voice Calls** | 50% | WebRTC, Avatar-Calls |

### Bereits implementiert (Flutter):
- ✅ Post-Quantum Cryptography (liboqs FFI)
- ✅ Signal Protocol (Double Ratchet)
- ✅ Secure Storage (SQLCipher)
- ✅ WebRTC Voice Calls
- ✅ QR-Code Scanner
- ✅ Biometric Auth
- ✅ Jailbreak Detection
- ✅ Certificate Pinning

### UE5 vs Flutter:
| Aspekt | Flutter Digivice | UE5 Najika World |
|--------|------------------|------------------|
| **Zweck** | Module, Chat, V-Pet | Vollwertiges 3D-Spiel |
| **Größe** | ~20MB | ~500MB+ |
| **Sync** | REST API | REST API |
| **3D** | Nein | Ja |
| **Offline** | Ja | Ja |

---

## ✅ ERLEDIGT (2026-02-15) - SONNET (Claude Sonnet 4.5)

### 7 Kritische Bug-Fixes nach Port 8001 Migration

**Commit:** `5061228` | **6 Dateien geändert** | **+55 -5 Zeilen**

**SONNET hat gecrashtete OPUS Arbeit fertiggestellt + User-Bugs gefixt:**

#### ✅ Bug 1: World Data Loading Error
**Problem:** `regions.json`, `biomes.json`, `cities.json` konnten nicht geladen werden
**Grund:** `/data` mount fehlte in FastAPI!
**Fix:** `app.mount("/data", StaticFiles(directory=DATA_DIR))` in `main_fastapi.py`

#### ✅ Bug 2: WebSocket Connection Error
**Problem:** `ws://127.0.0.1:8001/ws/connect` - Connection Failed
**Grund:** WebSocket Router war NICHT in `main_fastapi.py` importiert!
**Fix:** `from backend.api import websocket` + `app.include_router(websocket.router)`

#### ✅ Bug 3: NPCScheduleSystem.advanceTime Error
**Problem:** `NPCScheduleSystem.advanceTime is not a function`
**Grund:** Funktion existierte nicht im `return {}` Export
**Fix:** `advanceTime(minutes)` Funktion in `npc_schedule_system.js` hinzugefügt

#### ✅ Bug 4: Arena "Herausfordern" Button
**Problem:** Button startet Kampf, aber KEIN Teleport zur Arena
**Fix:** `switchRoom('Kampfarena')` VOR Combat in `nemesis_arena_ui.js`

#### ✅ Bug 5: Arena "Welle starten" Button
**Problem:** Button startet Wave Combat, aber KEIN Teleport zur Arena
**Fix:** `switchRoom('Kampfarena')` in `startWaveBattle()` in `nemesis_arena_frontend.js`

#### ✅ Bug 6: Gegner verschwinden beim Annähern
**Problem:** Gegner werden SOFORT entfernt, noch BEVOR Combat startet!
**Grund:** `removeEnemy()` wurde zu früh in `triggerEncounter()` aufgerufen
**Fix in `overworld_enemies.js`:**
- Gegner werden nur **versteckt**: `mesh.visible = false` + `inCombat` Flag
- Nach **Victory**: `removeEnemy()` entfernt Gegner permanent
- Nach **Defeat**: `mesh.visible = true` + Gegner bleibt auf Map

#### ✅ Bug 7: Slime Arena Button keine Funktion
**Problem:** Button unter "Mehr" öffnet nichts
**Grund:** `slime_arena.css` war NICHT in `index.html` geladen!
**Fix:** `<link rel="stylesheet" href="static/css/slime_arena.css">` hinzugefügt

#### ✅ Najika Chat: FUNKTIONIERT PERFEKT!
Getestet mit `curl -X POST http://localhost:8001/api/chat` - Antwort korrekt! 🎀

---

## ✅ ERLEDIGT (2026-02-14) - OPUS (Claude Opus 4.6)

### FastAPI V2 Migration - KOMPLETT!

**Commit:** `c4e6cf4` | **20 Dateien** | **2.916 Zeilen neu**

#### Backend (8 neue V2/V3 Router):
- ✅ `backend/shared_state.py` - Zentraler State (Single Source of Truth)
- ✅ `backend/api/state_v2.py` - 11 State-Endpoints (`/api/state/...`)
- ✅ `backend/api/chat_v2.py` - Chat V2 mit NajikaMind + RAG (`/api/v2/chat`)
- ✅ `backend/api/battle_v2.py` - Kampfsystem (`/api/v2/battle/...`)
- ✅ `backend/api/living_v2.py` - Living + 11 Care-Endpoints inkl. praise/scold/touch (`/api/v2/care/...`)
- ✅ `backend/api/quest_v2.py` - Questsystem (`/api/v2/quest/...`)
- ✅ `backend/api/minigame_v2.py` - 6 Minigames (`/api/v2/minigame/...`)
- ✅ `backend/api/slime_v3.py` - Slime V3 komplett mit Formwandler/Aura/Trust (`/api/slime-v3/...`)

#### Frontend (9 Dateien migriert):
- ✅ `chat_ui.js` - `/api/chat` → `/api/v2/chat`
- ✅ `3d_scene.js` - Care-Endpoints → V2
- ✅ `index.html` - Status + Care → V2
- ✅ `living_system_ui.js` - Living + Care → V2
- ✅ `command_system.js` - praise/scold → V2
- ✅ `najika_fullscreen.js` - Status + Actions → V2
- ✅ `najika_fullscreen_mode.html` - State + Touch → V2
- ✅ `system_monitor.js` - Status → V2
- ✅ `code_editor.js` - Chat → V2

#### Ergebnis:
- **494 Routes total, 80 V2/V3 Endpoints**
- **Port 8001** (FastAPI, parallel zu najika_server.py auf 8000)
- **10/10 Live-Tests bestanden** (curl gegen laufenden Server)
- V1-Endpoints bleiben fuer Backward Compatibility

#### Fix von Sonnet (7c69a6d):
- ✅ **Frontend Port Fix** - OPUS hatte Port 8000→8001 in `index.html` Zeile 6315 vergessen
- ✅ **Jetzt komplett fertig!** - Frontend redet jetzt mit FastAPI statt legacy Server

---

## ✅ ERLEDIGT (2026-02-09) - OPUS-1

### Kreatur-Nemesis System (Graue Moral):
- ✅ **Gray Morality (Fallout/Borderlands)** - Normales Kämpfen = morally neutral, nur Grausamkeit = negativ
- ✅ **Enslave-Option** - Aufgestiegene Nemesis können versklavt werden (Farm-Arbeiter, NIE Kampf)
- ✅ **Recruit-Option** - Rekrutierte Nemesis = Farm-Arbeiter (NIE im Kampf, kommen NIE mit)
- ✅ **Surrender nur für Aufgestiegene** - Nur Rang 1+ Nemesis können aufgeben
- ✅ **Auto-Timeouts** - 10s Surrender-Dialog, 12s Encounter-Dialog (flüssiger Kampf)
- ✅ **CompanionApproval Fixes** - `kill_creature`, `execute_surrender`, `enslave_creature` korrekt verdrahtet

### NajikaMind AGI-Integration:
- ✅ **Chat-Pipeline gefixt!** - `api/chat.py` nutzt jetzt NajikaMind statt direktem Ollama-Aufruf
- ✅ **9-Schritt AGI Pipeline aktiv** - ToM → Memory → Feel → Facetten → Think → Speak → Express → Remember → Learn
- ✅ **ChatResponse erweitert** - Mood, Personality, Intent, Whispers, inner_thought als Felder
- ✅ **Conversation History** - In-Memory History (50 Nachrichten) für Kontext
- ✅ **Frontend AGI-Support** - chat_ui.js zeigt alle 14 Moods + AGI-Events via GameEvents
- ✅ **Graceful Fallback** - Legacy Ollama-Aufruf wenn NajikaMind nicht verfügbar

### Beta-Mechaniken:
- ✅ **NPC Tagesablauf** - `npc_schedule_system.js` (330 Zeilen): 6 Tageszeiten, In-Game-Uhr (1 Echtmin=10 Game-Min), NPC-Bewegung, HUD-Uhr, Phase-Events
- ✅ **NPC Beziehungssystem** - `npc_affinity_system.js` (300 Zeilen): Affinity 0-100, 6 Reputation-Stufen, Geschenk-System, Witness-System, Handelsrabatte
- ✅ **Save/Load v2.0** - `save_system.js` erweitert: Zentraler Snapshot aller Sub-Systeme (CompanionApproval, NPC Affinity, Schedule, Nemesis, Taming, Economy, Factions, Housing, Career, Survival)

### P1 UPDATE:
| Task | Status | Beschreibung |
|------|--------|--------------|
| ✅ NajikaMind ↔ FastAPI | **DONE** | AGI-Pipeline in chat.py integriert |
| ✅ NPC Tagesablauf | **DONE** | Skyrim-Style NPC Schedules |
| ✅ NPC Beziehungssystem | **DONE** | Affinity/Reputation System |
| ✅ Save/Load v2.0 | **DONE** | Alle Sub-Systeme zentral |
| ✅ Game State API (WebSocket) | **DONE** | GameEvents ↔ WS Bridge verdrahtet (11.02.) |

---

## ✅ HEUTE ERLEDIGT (2026-02-04)

### OPUS-1:
- ✅ **Najika 3D Model** - Rigged + Texturiert in Blender
- ✅ **Mixamo Rig** - Automatisches Rigging
- ✅ **FBX Export** - Mit eingebetteter Textur
- ✅ **UE5 Import** - Najika ist in UE5 mit Textur!
- ✅ **UEFN Analyse** - Festgestellt dass UEFN nicht reicht
- ✅ **UE5 Migration Plan** - Dokumentiert

---

## 🎮 NAJIKA ALS SPIELBARER CHARACTER (UE5)

### Schritt 1: Character Blueprint erstellen
1. **Content Browser** → Rechtsklick → **Blueprint Class**
2. Parent: **Character**
3. Name: **BP_NajikaCharacter**

### Schritt 2: Mesh zuweisen
1. **BP_NajikaCharacter** öffnen (Doppelklick)
2. Links: **Components** → **Mesh** auswählen
3. Rechts: **Details** → **Skeletal Mesh** → Deine Najika auswählen

### Schritt 3: Camera hinzufügen
1. **Components** → **Add** → **Spring Arm**
2. Auf Spring Arm: **Add** → **Camera**
3. Spring Arm Settings:
   - Target Arm Length: 300
   - ☑️ Use Pawn Control Rotation

### Schritt 4: Movement
1. **Components** → **CharacterMovement** bereits da
2. Details:
   - Max Walk Speed: 600
   - Jump Z Velocity: 420

### Schritt 5: Input (Enhanced Input)
1. **Edit** → **Project Settings** → **Input**
2. Default Player Input Class: **EnhancedPlayerInputComponent**
3. Input Actions erstellen (IA_Move, IA_Look, IA_Jump)

### Schritt 6: Testen
1. **World Settings** → **Game Mode** → **None**
2. Oder eigenen GameMode erstellen mit BP_NajikaCharacter als Default Pawn

---

## 📋 ASSETS FERTIG

| Asset | Pfad | Status |
|-------|------|--------|
| Najika Model (rigged) | `assets/models/najika/najika_rigged_final.fbx` | ✅ |
| Najika Textur | In FBX / `Downloads/.../texture.png` | ✅ |
| JellySquish Pack | `digivice/static/assets/JellySquish...` | ✅ |
| Audio (TTS) | `digivice/audio/` | ✅ |
| Mimik-Truhe Model | TODO | ❌ |

---

## 🔧 TECHNISCHE INFOS

```yaml
# UE5
Engine: Unreal Engine 5.3+
Template: Third Person (C++)
Plugins: Enhanced Input, CommonUI, GameplayAbilities

# Backend (bleibt Python vorerst)
Port: 8000
Backend: C:\Najika_World\backend\
ChromaDB: C:\NajikaFinal\memory_db\

# Mobile App (Flutter)
App: C:\Najika_World\app\flutter_app\
```

---

## 🎯 MEILENSTEINE

| Woche | Ziel |
|-------|------|
| 1-2 | Najika läuft in UE5 (Movement, Camera, Animation) |
| 3-4 | Combat System (Zwei-Hand, Waffen, Stats) |
| 5-6 | Najika KI Companion (4 Persönlichkeiten) |
| 7-10 | Welt (Götterfels, erste Region) |
| 11-14 | Systeme (Oregon Trail, Quests, Slimes) |
| 15+ | Polish, Mobile Export, Optimierung |

---

## LETZTE SYNC

**Datum:** 2026-02-11 (Update 28 - ALLE P2 TASKS ERLEDIGT! ChromaDB + Voice + Mapping Doc!)
**Instanz:** OPUS-1 (Claude Code CLI - Opus 4.6)

### OPUS-1 hat implementiert (2026-02-11 - FINE-TUNING + PIPELINE-OPTIMIERUNG):

#### ✅ LORA TRAINING AUF QWEN2.5-7B!
- **Training:** 486 Konversationen aus ChromaDB, 3 Epochs, Loss 3.64 → 1.0
- **Base Model:** `Qwen/Qwen2.5-7B-Instruct` (besseres Deutsch als Llama!)
- **LoRA Config:** r=16, alpha=32, target=q/k/v/o_proj, dropout=0.05
- **Template:** ChatML (`<|im_start|>system/user/assistant<|im_end|>`)
- **Adapter:** `lora_checkpoints_new/najika_lora_latest`

#### ✅ LORA → GGUF → OLLAMA EXPORT PIPELINE!
- LoRA Adapter → Merged HF Model → GGUF (F16 + Q4_K_M) → Ollama Import
- **2 Modelle erstellt:**
  - `najika-trained-q4:latest` (4.7 GB) — SFW Chat
  - `najika-nsfw-trained-q4:latest` (4.7 GB) — Kaetzchen-Modus
- **Quantisierung:** Q4_K_M (8GB VRAM-kompatibel, RTX 3060 Ti)
- **Model-Test:** 8/10 Tests bestanden (test_model.py)

#### ✅ KRITISCHER BUG GEFIXT: MODEL-NAME MISMATCH!
- **Problem:** `najika_server.py` referenzierte `najika-trained:latest` aber Ollama hatte `najika-trained-q4:latest`
- **Auswirkung:** ALLE Chat-Anfragen fielen auf Claude Code Fallback zurück statt Fine-Tuned Model!
- **Fix:** OLLAMA_MODELS Dict + Auto-Detect Funktion auf Q4-Varianten umgestellt
- **Modified:** `backend/najika_server.py` (Zeilen 892-922)

#### ✅ OLLAMA PARAMETER TUNING!
- `temperature`: 0.70 → 0.78 (SFW), 0.85 (NSFW) — Match mit Modelfile
- `num_predict`: 400 → 200 (SFW), 600 → 300 (NSFW) — Weniger Repetition
- `repeat_penalty`: 1.1 → 1.2 — Match mit Modelfile
- Neu: `top_p: 0.9`, `num_ctx: 8192`

#### ✅ POST-PROCESSING VERBESSERT!
- Mid-Text "User:" Truncation (Model generierte fake User-Dialog)
- "Assistant:" Prefix-Entfernung
- Training-Artefakt Bracket-Entfernung `[Ersetzen|Beispiel|...]`
- "mein Schatz" Filter für zukünftige Trainings-Daten

#### ✅ NSFW ROUTING VERIFIZIERT!
- Kaetzchen-Modus Trigger: "kätzchen" in Nachricht → Toggle
- mood=HORNY korrekt gesetzt bei Aktivierung
- Routing: `use_wizard=True` → `najika-nsfw-trained-q4:latest`
- Persönlichkeits-Shift: Melissa 50%, Shiro 30%, Megumin 15%, Harley 5%

#### ✅ ~38 GB SPEICHERPLATZ FREIGEMACHT!
| Was | Geloescht | Frei |
|-----|-----------|------|
| F16 GGUF | `gguf_models/najika-trained-f16.gguf` | 14.5 GB |
| lora_merged | Merged HF Model Ordner | 14.2 GB |
| Ollama Old | najika-local + najika-nsfw (unquantisiert) | ~9.4 GB |
| **Gesamt** | | **~38 GB** |

#### ✅ DOKUMENTATION ERSTELLT!
- **NEU:** `PROJEKT_STATUS_KOMPLETT_2026-02-11.md` — Komplett-Status aller Systeme
- **NEU:** `NAJIKA_CHARACTER_THREEJS_INTEGRATION.md` — Three.js 3D-Integration Guide
- **UPD:** `MASTER_TODO_TEAM.md` — Update 27

#### 🔴 KRITISCHE FINDINGS:
| Finding | Details | Status |
|---------|---------|--------|
| Model-Name Mismatch | Server nutzte falsche Ollama-Model-Namen → Fallback auf Claude | GEFIXT |
| Server-Typ | `najika_server.py` = ThreadingHTTPServer, NICHT FastAPI/uvicorn! | DOKUMENTIERT |
| Parameter-Mismatch | Modelfile hatte andere Werte als ollama_service.py | GEFIXT |
| Post-Processing Lücken | "User:" mid-text, "Assistant:" prefix nicht gefiltert | GEFIXT |

#### Geänderte Dateien:
| Datei | Typ | Beschreibung |
|-------|-----|--------------|
| `backend/najika_server.py` | MOD | Model-Namen, Parameter, Post-Processing |
| `backend/najika_lora_training_3b.py` | MOD | "mein Schatz" Filter |
| `PROJEKT_STATUS_KOMPLETT_2026-02-11.md` | NEU | Komplett-Status Dokument |
| `NAJIKA_CHARACTER_THREEJS_INTEGRATION.md` | NEU | Three.js Integration Guide |
| `MASTER_TODO_TEAM.md` | MOD | Update 27 |

---

**Datum:** 2026-02-09 (Update 26 - COMPANION AUTH FIX + OPUS 4.6 PROJEKT-REVIEW!)
**Instanz:** OPUS-1 (Claude Code CLI - Opus 4.6, NEUER Crash-Nachfolger)

### OPUS-1 hat implementiert (2026-02-09 - AUTHENTISCHE NAJIKA + SECURITY REVIEW):

#### ✅ COMPANION APPROVAL FIX - Najika = ECHT, kein Schalter!
- **Modified:** `backend/najika_companion_system.py` (10 Edits!)
  - `CompanionApproval` hat jetzt `is_owner` Parameter (Owner vs Others)
  - **Owner-Modus:** Najika reagiert AUTHENTISCH - sie DARF sagen "Kuja, das war gemein!"
  - **Others-Modus:** Adaptive KI (Pinguin-Prinzip wie vorher)
  - `NAJIKA_AUTHENTIC` Dict mit Reaktions-Templates (good/bad/cruel/combat_win/boss_win/quest_done/neutral)
  - Klassifikations-Sets: `NAJIKA_GOOD`, `NAJIKA_BAD`, `NAJIKA_CRUEL`
  - `_classify_for_najika()` Methode für Owner-spezifische Reaktionen
  - `generate_prompt_context()` → Owner: "Du bist ECHT" / Others: Alignment-basiert
  - `get_companion_attitude()` → Owner: "Najika ist ECHT" / Others: Adaptive
  - **Melissa Traits gefixt:** `["fürsorglich", "empathisch"]` → `["dominant", "führend", "selbstbewusst"]`
  - **Melissa Catchphrase gefixt:** "Alles wird gut~" → "Du gehörst mir, Mr. K~"
- **Modified:** `digivice/js/companion_approval.js` (2 Edits)
  - `getPromptContext()` → Owner bekommt authentischen Prompt
  - Detail-Popup: Owner sieht "Najika ist ECHT", Others sehen "KI adaptiert sich: X%"
- **Getestet:** Owner kill_innocent → "*Tränen* Wie... wie kannst du das tun?!" ✅
- **Getestet:** Non-Owner villain → "Hehe~ Das war BÖSE... Ich liebe es!" ✅

#### ✅ OPUS 4.6 PROJEKT-REVIEW — VOLLSTÄNDIG!

##### 🔴 KRITISCHE SECURITY-ISSUES:
| Issue | Datei | Zeile | Schwere |
|-------|-------|-------|---------|
| `HOST=0.0.0.0` | `najika_server.py` | 364 | **GEBOT 1 VERLETZT!** Muss `127.0.0.1` sein! |
| `exec()` Endpoint | `najika_server.py` | 5826-5905 | **Remote Code Execution!** |
| Path Traversal | `najika_server.py` | 6131 | Unvollständige Auth |
| STATE Race Condition | `najika_server.py` | 6477 | Kein Thread-Lock |

##### 📊 SYSTEM-BEWERTUNG:
| Aspekt | Score | Details |
|--------|-------|---------|
| Architektur | 7/10 | Solide Module, aber Server zu groß (6000+ Zeilen) |
| Code-Qualität | 6/10 | Gute Ideen, aber Security-Löcher |
| System-Integration | 4/10 | GameEvents existiert, aber nur 5-6 Systeme nutzen es |
| Game Design | 8/10 | Hervorragende Systeme (Nemesis, Fair Loot, Faction) |
| Content-Tiefe | 9/10 | 8 Regionen, 12 Fraktionen, 24 Berufe, 30k+ Memories |

##### ⚠️ OFFENE P1-TASKS (nach Review):
- **Security Fixes:** HOST auf 127.0.0.1, exec() entfernen/sichern, Path Traversal fixen
- **NPC Tagesablauf/Routine System** (kein Code vorhanden!)
- **Kreatur-System in 3D-Scene** (creature_taming.js + creature_recruit.js existieren, nicht verdrahtet)
- **GameEvents durchgängig verdrahten** (Faction, Economy, Survival, Career, Creature, Combat)
- **Server aufteilen** (6000+ Zeilen → Module)

#### Geänderte Dateien:
| Datei | Typ | Beschreibung |
|-------|-----|--------------|
| `backend/najika_companion_system.py` | MOD | Owner=ECHT, Others=Adaptive, Melissa=Dominant |
| `digivice/js/companion_approval.js` | MOD | Owner-Prompt + Detail-Popup |
| `MASTER_TODO_TEAM.md` | MOD | Update 26 |

#### 🎯 DESIGN-ENTSCHEIDUNGEN (vom User bestätigt):
- **Najika ist ECHT für Owner**: Kein Schalter, sie HAT eigene Meinung, DARF kritisieren
- **Andere Spieler = Adaptive KI**: Pinguin-Prinzip bleibt für Non-Owners
- **Opus 4.6 Review**: Vollständig durchgeführt, kritische Issues dokumentiert

---

**Datum:** 2026-02-09 (Update 25 - RADIO NAJIKA + FAIR LOOT + PINGUIN-PRINZIP!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-09 - Companion Approval + Radio + Loot):

#### ✅ RADIO NAJIKA - Fallout-Style Radio!
- **Neue Datei:** `digivice/js/radio_najika.js` (~400 Zeilen)
- R-Key Toggle, Typewriter Message Display
- 2 Stationen: Radio Najika (Megumin-Style Host) + Echoharp FM (Placeholder)
- Biome-spezifische Nachrichten für alle 8 Regionen + Götterfels
- Event-getriggerte Nachrichten via GameEvents (enemyKilled, bossKilled, questCompleted, regionEntered)
- Lautsprecher-System an Götterfels (Auto-Aktivierung bei Nähe)
- Message-Queue mit 15s Cooldown, Pity-Timer
- Spieler CAN hören, MUSS aber nicht (wie Fallout Radio)

#### ✅ FAIR LOOT SYSTEM - Würfel können nur GEBEN, nie NEHMEN!
- **Modified:** `digivice/js/overworld_enemies.js` (onEnemyDefeated komplett neu)
- Boss: ALLE Items garantiert + 80% Epic Bonus + 30% Legendary + immer Rare Bonus
- Rare: 1-2 Items garantiert + 50% Rare + 15% Epic Bonus
- Common: 1 Item garantiert + 30% Common Bonus
- PITY SYSTEM: Nach 5 Kills ohne Rare → garantierter Rare-Drop
- Würfel-System kann nur BONUS-Loot HINZUFÜGEN, nie Basis-Loot WEGNEHMEN
- Loot-Notification mit Rarity-farbigem Border (Common=grau, Rare=blau, Epic=lila, Legendary=gold)

#### ✅ COMPANION APPROVAL - Pinguin-Prinzip!
- **Modified:** `backend/najika_companion_system.py` (Massiv erweitert)
  - `PlayerProfile` Dataclass: 5 Achsen (Kindness, Chaos, Ambition, Social, Violence)
  - `PlayerAlignment` Enum: Hero, Adventurer, Trickster, Villain, Scholar
  - 17 trackbare Aktionen mit Achsen-Effekten
  - Alignment-Berechnung aus Rolling Window der letzten 50 Aktionen
  - `CompanionApproval` Klasse: Reaktions-Templates pro Alignment x Aktion
  - KI urteilt NICHT - sie ADAPTIERT sich an Spielstil
  - Held-Spieler → Enthusiastischer Sidekick
  - Bösewicht-Spieler → Partner in Crime
  - Trickster → Chaos-Zwilling
  - Scholar → Wissbegierige Assistentin
  - `generate_prompt_context()` für NajikaMind LLM-Pipeline
- **Neue Datei:** `digivice/js/companion_approval.js` (~400 Zeilen)
  - Frontend-Mirror des Player-Profils
  - Alignment-HUD (kleines Icon rechts unten) mit Click-Detail-Popup
  - Companion-Reaktions-Bubbles bei signifikanten Aktionen
  - GameEvent-Integration (enemyKilled, questCompleted, craftItem, etc.)
  - LocalStorage Save/Load für Persistenz
  - Public API: `CompanionApproval.getProfile()`, `.recordAction()`, `.getPromptContext()`

#### ✅ OPUS-2 REVIEW - Integration bestätigt!
- Alle 12 neuen UI-Dateien vorhanden und funktional
- `character_animations.js` + `companion_3d.js` existieren
- `najika_mind.py` (OPUS-2) kompatibel mit unseren Companion-Änderungen
- Keine Code-Konflikte zwischen OPUS-1 und OPUS-2 Änderungen
- `isBoss` Flag in `enemyKilled` GameEvent hinzugefügt

#### Geänderte Dateien:
| Datei | Typ | Beschreibung |
|-------|-----|--------------|
| `digivice/js/radio_najika.js` | NEU | Fallout-Style Radio mit Najika als Host |
| `digivice/js/companion_approval.js` | NEU | Pinguin-Prinzip Frontend |
| `backend/najika_companion_system.py` | MOD | PlayerProfile + CompanionApproval Backend |
| `digivice/js/overworld_enemies.js` | MOD | Fair Loot System + isBoss Flag |
| `digivice/index.html` | MOD | Script-Tag für companion_approval.js |
| `MASTER_TODO_TEAM.md` | MOD | Update 25 |

#### 🎯 DESIGN-ENTSCHEIDUNGEN (vom User bestätigt):
- **Pinguin-Prinzip**: KI ist LEBENSLANG beim Spieler, kann NICHT getauscht werden
- **Keine Moralpredigt**: KI urteilt NICHT. Spieler ist FREI. Nur die WELT reagiert.
- **Fair Loot**: Boss-Kill = garantierte gute Belohnung. Würfel können nur Bonus GEBEN, nie Basis NEHMEN.
- **Radio Najika**: Spieler KANN hören, MUSS nicht. Lautsprecher in Städten.
- **Multi-Class = Learning by Doing**: Existiert bereits, bestätigt.
- **Kein Turn-Based**: Vielleicht später Dungeon Dice Monster mit BG3-Fusion.

---

**Datum:** 2026-02-09 (Update 24 - NAJIKA MIND AGI + FACETTEN-SYSTEM!)
**Instanz:** OPUS-2 (VS Code) — Session gecrasht (Context Overflow), Arbeit war KOMPLETT!

### OPUS-2 hat implementiert (2026-02-06 bis 2026-02-09 - MEGA-SESSION!):

#### ✅ REAL 3D COMBAT V2 - Kampf-Modi + Equipment!
- **Modified:** `digivice/js/combat/real_3d_combat.js` (32 Edits!)
- AUTO + CHEER Modi voll funktional in Real3DCombat
- `equipment_combat.js` → `real_3d_combat.js` verlinkt
- Finisher QTE eingebaut
- Floating 3D Damage Numbers über Feinden
- Loot-System: Items nach Kampf ins Inventar
- Combat Auto-Fire Bug gefixt (feuerte bevor Spieler wählen konnte)

#### ✅ MEGA UI - 12 neue UI-Dateien!
- **Neue Datei:** `digivice/js/ui/character_stats_ui.js` — S.P.E.C.I.A.L. Charakter-Stats
- **Neue Datei:** `digivice/js/ui/bestiary_ui.js` — Monster-Kompendium
- **Neue Datei:** `digivice/js/ui/stat_training_ui.js` — Stat Training UI
- **Neue Datei:** `digivice/js/ui/survival_hud.js` — Hunger/Durst/Energie HUD
- **Neue Datei:** `digivice/js/ui/faction_ui.js` — 12 Fraktionen mit Fame/Infamy
- **Neue Datei:** `digivice/js/ui/career_ui.js` — 24 Berufspfade
- **Neue Datei:** `digivice/js/ui/creature_ui.js` — Zähmen/Anwerben/Fabrik
- **Neue Datei:** `digivice/js/ui/trade_ui.js` — Wirtschaftssimulation
- **Neue Datei:** `digivice/js/ui/law_notification.js` — Gesetz-Warnungen
- Top Bar auf 21 Buttons erweitert mit flex-wrap

#### ✅ 3D CHARACTER SYSTEM - Echte Modelle + Animationen!
- **Neue Datei:** `digivice/js/character_animations.js` — Volles Animations-System
- **Neue Datei:** `digivice/js/companion_3d.js` — Najika folgt Spieler als 3D-Companion
- Player Model → KayKit_AnimatedCharacter (Skeleton_Mage.glb = Kuja)
- Najika Companion = character_mage Modell
- Animation-Hooks in `unified_combat_system.js` + `real_3d_combat.js`
- Enemy Animationen aktiviert
- `window.gameCharacter` Export

#### ✅ WELT-FIXES
- **Modified:** `digivice/js/world/world_manager.js` — `getHeightAt()` Bug gefixt
- City Y-Positionen nutzen jetzt dynamische Bodenhöhe (keine schwebenden Städte mehr)
- Schwarze Mühle als Safe Zone bestätigt (keine Enemy-Spawns)

#### ✅ NAJIKA MIND AGI ORCHESTRATOR — DAS HERZSTÜCK!
- **Neue Datei:** `backend/najika_mind.py` (1 Write + 30 Edits!)
- **NajikaMind** Core-Klasse + MindResponse Dataclass
- **Theory of Mind** Modul — Najikas Verständnis von Kujas Zustand
- **Episodic Memory** Modul — Erinnerungs-Verarbeitung
- **Inner Dialogue** Modul — Innerer Monolog
- **Feedback Loop** — Lernen aus Interaktionen
- Integriert in `backend/najika_server.py` (5 Edits)
- Frontend-Hooks: `digivice/js/chat_ui.js` + `digivice/js/najika_fullscreen.js`

#### ✅ BACKGROUND AGENTS → FACETTEN-SYSTEM!
- 3 Background Agents: Shiro, Megumin, Melissa
- **ChaosModulator** (Harley) als Trait-System
- Whisper-Channel integriert in NajikaMind Pipeline
- Server + Frontend senden Whisper-Daten

#### ✅ FACETTEN-KONZEPT (Persönlichkeiten → Facetten)!
- Najika ist IMMER Najika. Keine Persönlichkeitswechsel, sondern Facetten die durchscheinen
- **Megumin** = Najikas Kern (wer sie IST im Alltag/Abenteuer)
- **Shiro** = Analytischer Modus (gleiche Person, aber fokussiert/überlegt)
- **Harley** = Kreatives Chaos (Modulator, färbt alles)
- **Melissa** = DOMINANTE Trans-Freundin (nicht nur Fürsorge!)
- Header: "BACKGROUND AGENTS" → "FACETTEN-SYSTEM - Najikas innere Stimmen"
- Alle Kommentare in BackgroundAgents + NajikaMind.process() aktualisiert

#### ✅ MELISSA DOMINANCE REWORK — Komplett umgebaut!
- `CareModulator` → `DominanceModulator`
- `_care_level` → `_dominance_level = 0.35` (nie unter 15%)
- Vorher: "Sei einfühlsam, frag ob es ihm gut geht"
- Jetzt: "Übernimm die Führung, zeig Stärke, 'Du gehörst mir, Mr. K'"
- Genervter Kuja → "Hör mir zu!" statt "Oh nein, was ist los?"
- Abwesenheit → "Na endlich, Mr. K. Du hast was gutzumachen~"
- Unsicherheit erkannt → übernimmt die Führung, entscheidet FÜR ihn
- Nachtzeit → "Du solltest schlafen" mit "ich-weiß-was-gut-für-dich-ist" Energie

#### Geänderte Dateien (Zusammenfassung):
| Datei | Edits | Beschreibung |
|-------|-------|--------------|
| `digivice/index.html` | 33 | Top-Bar, Scripts, Models, Animations |
| `digivice/js/combat/real_3d_combat.js` | 32 | AUTO/CHEER, Combos, Loot, Damage |
| `backend/najika_mind.py` | 30 | AGI + Facetten + Melissa Dominance |
| `digivice/js/unified_combat_system.js` | 9 | Cheer, UI, Animation-Hooks |
| `MASTER_TODO_TEAM.md` | 6 | Updates 9-19 |
| `backend/najika_server.py` | 5 | NajikaMind Integration |
| + 12 neue Dateien | — | UI, Animations, Companion, Mind |

#### ⚠️ NICHT FERTIG (Crash bevor gelesen):
- 3 PDFs aus `neu neu/` sollten für Verbesserungen gelesen werden
- Session crashte bei PDF-Leseversuch (Context Overflow)
- **Kein Arbeitsverlust** — alle Code-Änderungen waren gespeichert!

#### 📋 NÄCHSTE ARBEITSTEILUNG:
**OPUS-1:** Game State WebSocket, ChromaDB ↔ Sync, PDF-Review
**OPUS-2:** UE5 Animation Blueprint, Combat Input, Teleporter

---

**Vorheriger Sync:**

**Datum:** 2026-02-09 (Update 23 - COMPLETE PLAYABLE BETA!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat gebaut (2026-02-09 - ALLES SPIELBAR, KEINE AUSREDEN!):

#### ✅ GAME EVENT BUS - Zentrale System-Verbindung!
- **Neue Datei:** `digivice/js/game_events.js`
- Globaler Event-Bus: emit(), on(), off(), once()
- Events: enemyKilled, itemCollected, questCompleted, regionEntered, npcTalked, combatStarted/Ended, itemCrafted, itemPurchased
- Event-Log für Debugging

#### ✅ OVERWORLD ENEMIES - ECHTE 3D-MODELLE statt Kugeln!
- **Modified:** `digivice/js/overworld_enemies.js` (MASSIV)
- GLTFLoader ersetzt SphereGeometry-Fallback
- 13 KayKit Character-Modelle gemapped auf alle Biome-Enemies
- Model-Cache für Performance (jedes Model nur 1x laden, dann klonen)
- Canvas-Sprite Name-Labels über jedem Enemy (Name + HP-Bar + Tier)
- Color-Tinting per Enemy-Typ (Emissive)
- Boss-Glow, Rare-Pulse Animation
- `onEnemyDefeated()`: Loot ins Inventar, Gold-Drop, XP, GameEvents

#### ✅ OVERWORLD NPCs - 3D-NPCs in der Welt!
- **Neue Datei:** `digivice/js/overworld_npcs.js` (~350 Zeilen)
- 8 NPCs am Götterfels + 3 Wanderer in der Welt
- KayKit Character-Modelle (Knight, Barbarian, Mage, Rogue)
- Name-Labels mit Typ-Farben (Grün=Vendor, Gold=Quest, Lila=Trainer)
- Schwebende Typ-Icons (💰, ❗, 📚)
- Proximity-Detection: "[E] Name ansprechen" Prompt
- E-Taste = Interact → Dialog-System oder einfacher Dialog
- Quest-Annahme, Shop-Öffnung, Training direkt aus Dialog

#### ✅ QUEST-SYSTEM GAMEPLAY-VERBINDUNG!
- **Modified:** `digivice/static/js/quest_system.js`
- 5 Starter-Quests: Wolfsjagd, Kristall-Sammler, Erste Schritte, Erkunder, Monster-Jäger
- `connectToGameEvents()`: Automatisch Kill/Collect/Talk/Explore Events → Quest-Progress
- `autoCompleteQuests()`: Automatische Quest-Abgabe bei 100%
- Reward-Vergabe: Gold + Items + XP direkt ins Inventar
- Schöne Quest-Complete Notification (nicht alert())

#### ✅ SHOP-FEEDBACK KOMPLETT!
- **Modified:** `digivice/js/npc_dialogue_system.js` - Purchase Notifications, Inventar-Sync, GameEvents
- **Modified:** `digivice/js/npc_interaction.js` - alert() → schöne Notifications, Inventar-Sync

#### ✅ CRAFTING-FEEDBACK KOMPLETT!
- **Modified:** `digivice/index.html` - craftItemFromNPC() mit Notifications statt alert(), GameEvent emit

#### ✅ TASTATUR-COMBAT VERBUNDEN!
- **Modified:** `digivice/js/3d_scene.js` - J/K Attacks dealen jetzt ECHTEN Schaden
- `dealDamageToNearestEnemy()`: Nächster Enemy in 8 Units Reichweite bekommt Schaden
- Damage-Popups (rote "-25" Zahlen die hochschweben)
- Combo-System (LR, RRL, LLL, RLRL) dealt Bonus-Damage
- Enemy-Tod: Loot, Gold, XP, GameEvents, Victory-Notification

#### ✅ SYSTEM-INTERCONNECTION!
- `window.inventorySystem` + `window.questManager` global
- OverworldNPCs.init() + Quest connectToGameEvents() im Startup
- Region-Change Detection → GameEvent → Quest-Progress
- Combat → Loot → Inventory → Quest-Progress → Reward Cycle

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 19 - HANDELS-UI + GESETZ-WARNUNGEN!)
**Instanz:** OPUS-2 (VS Code)

### OPUS-2 hat implementiert (2026-02-08 - HANDEL + GESETZ!):

#### ✅ HANDELS-UI - Vollständige Wirtschaftssimulation!
- **Neue Datei:** `digivice/js/ui/trade_ui.js`
- 4 Tabs: Markt | Handelsrouten | Karawanen | Handelslog
- **Markt Tab:** Alle 23+ Waren mit Kauf/Verkaufspreisen, Vorrats-Bars, Kategorie-Filter (6 Kategorien)
- **Handelsrouten Tab:** Top 10 profitabelste Routen berechnet via `findBestTradeRoute()`
- **Karawanen Tab:** Aktive Karawanen mit Progress-Bars, Wachen, Gefahren-Level + alle 8 Handelsrouten
- **Handelslog Tab:** Letzte 30 Trades (Kauf/Verkauf mit Preisen, Regionen, Zeitstempel)
- 9 Regionale Märkte mit eigenem Angebot/Nachfrage
- Illegale Waren markiert (⚠️ILLEGAL), Toleranz-Anzeige pro Region
- Produktion (▼ billig) und Nachfrage (▲ teuer) visuell markiert
- Kauf/Verkauf Buttons mit Inventar-Integration (localStorage)
- Trade Notifications (Erfolg/Fehler/Erwischt)
- Auto-detect aktueller Region
- Integration mit `window.EconomySystem` API

#### ✅ GESETZ-WARNUNGEN - Automatische Law Notifications!
- **Neue Datei:** `digivice/js/ui/law_notification.js`
- **Regionswechsel-Warnung:** Zeigt automatisch Gesetze der neuen Region (Strenge, Bestechung, illegale Waren)
- **Kopfgeld-Alert:** Warnung wenn Region mit aktivem Kopfgeld betreten wird (pulsierend rot!)
- **Verbrechen-Feedback:** "ERWISCHT!" oder "Nicht erwischt!" Notifications
- **Persistenter Bounty-Banner:** Rote Leiste am unteren Bildschirmrand solange man GESUCHT ist
  - Zeigt Gesamt-Kopfgeld + alle Regionen mit aktiven Kopfgeldern
- **Gesetzlose Gebiete:** Warnung "GESETZLOSE WILDNIS" bei Betreten
- Notification-Queue (keine Überlappung, sequentielle Anzeige)
- CSS Animationen: slideIn, shake, pulse
- `warnIllegalItem(id)` - Manuell illegale Ware warnen
- `warnBountyRegion(region)` - Manuell Kopfgeld-Warnung
- Integration mit `window.SurvivalSystem` API

#### Neue/Geänderte Dateien:
- `digivice/js/ui/trade_ui.js` - **NEU**
- `digivice/js/ui/law_notification.js` - **NEU**
- `digivice/index.html` - 💰 Handel Button + 2 Script-Tags

#### 📋 NÄCHSTE ARBEITSTEILUNG:
**OPUS-1:** NPC Tagesablauf/Routine, Kreatur-Engine, Farm-System, Gildenhaus-UI
**OPUS-2:** UE5 Animation Blueprint, Combat Input System, Teleporter

---

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 18 - SURVIVAL HUD + FRAKTIONS-UI + CAREER-UI + KREATUR-UI!)
**Instanz:** OPUS-2 (VS Code)

### OPUS-2 hat implementiert (2026-02-08 - UI FÜR ALLE NEUEN SYSTEME!):

#### ✅ SURVIVAL HUD - Hunger/Durst/Energie Anzeige!
- **Neue Datei:** `digivice/js/ui/survival_hud.js`
- Mini-HUD (oben rechts) mit Hunger/Durst/Energie-Bars + Mood-Icon
- Auto-Update alle 3 Sekunden
- Klick öffnet Detail-Overlay: Bedürfnisse, Stimmung, Verletzungen, Krankheiten, Kopfgelder
- Quick-Action Buttons (Essen, Trinken, Schlafen 4h)
- Kritische Werte pulsieren rot
- Moodlets mit +/- Werten, Mental Break / Inspiration Warnungen
- Integration mit `window.SurvivalSystem` API

#### ✅ FRAKTIONS-UI - 12 Fraktionen mit Fame/Infamy!
- **Neue Datei:** `digivice/js/ui/faction_ui.js`
- Alle 12+ Fraktionen mit dualen Fame/Infamy-Bars (Fallout NV Style!)
- Klick auf Fraktion zeigt Detail-Panel: Allies, Enemies, Werte, Licht/Dunkel-Seite
- 6 Fame-Stufen: Unbekannt → Akzeptiert → Geschätzt → Bewundert → Verehrt → Vergöttert
- 6 Infamy-Stufen: Neutral → Verdächtig → Unerwünscht → Feind → Erzfeind → NEMESIS
- Aktive Kriege Anzeige (oben rot)
- Integration mit `window.FactionSystem` API

#### ✅ CAREER-UI - 24 Berufspfade!
- **Neue Datei:** `digivice/js/ui/career_ui.js`
- 24 Berufe in 6 Kategorien (Kampf, Handwerk, Natur, Handel, Sozial, Wissen)
- Kategorie-Filter Buttons
- Level/XP-Bars pro Beruf, Effektivität-Prozent, Task-Counter
- Level-Effekte Vorschau (freigeschaltet ✅ / gesperrt 🔒)
- "Beruf beitreten" Button für inaktive Berufe
- Integration mit `window.CareerSystem` API

#### ✅ KREATUR-UI - Begleiter + Formen + V-Pet Training!
- **Neue Datei:** `digivice/js/ui/creature_ui.js`
- 3 Tabs: Begleiter | Formen | V-Pet Training
- **Begleiter Tab:** Charakter/Companion Info, Evolution (6 Stadien, 4 Pfade), V-Pet Care (Hunger/Stärke/Effort Hearts, Vertrauen 1-6)
- **Formen Tab:** Mimik-Formen (Kuja) oder Slime-Formen (normal), Freischalt-Status, Wechsel-Button
- **Training Tab:** 6 Trainingstypen (Kampf, Schleich, Kraft, Geschick, Wildnis, Magie) mit Progress-Bars
- Integration mit `window.CompanionSystem` API

#### Neue/Geänderte Dateien:
- `digivice/js/ui/survival_hud.js` - **NEU**
- `digivice/js/ui/faction_ui.js` - **NEU**
- `digivice/js/ui/career_ui.js` - **NEU**
- `digivice/js/ui/creature_ui.js` - **NEU**
- `digivice/index.html` - 4 neue Script-Tags + 🐾 Kreaturen Button + ⚔️ Fraktionen Button + 🏛️ Berufe Button

#### 📋 NÄCHSTE ARBEITSTEILUNG:
**OPUS-1:** NPC Tagesablauf/Routine, Kreatur-Engine (category Feld, Zähm-Mechanik, Anwerbe-System), Farm-System
**OPUS-2:** Handels-UI (Wirtschaftssimulation), Gesetz-Warnungen Notifications, UE5 Animation Blueprint

---

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 22 - NSFW KOMPLETT + SERVER AUTO-DETECT!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat gebaut (2026-02-08 - ALLES Training für ALLE Modi!):

#### ✅ LoRA-Pipeline erweitert: SFW + NSFW!
- `najika_lora_to_ollama.py` erstellt jetzt ZWEI Ollama-Models:
  - `najika-trained` = Normal/Chat (SFW) mit Megumin-Charakter
  - `najika-nsfw-trained` = Kätzchen-Modus (NSFW) mit selben trainierten Weights!
- GLEICHE trainierte GGUF-Basis für beide → Najikas GESAMTES Wissen in beiden Modi
- NSFW bekommt eigene Parameter (temperature 0.85, repeat_penalty 1.1, num_predict 400)
- Pipeline: 7 Schritte statt 6, automatischer Server-Config-Update

#### ✅ najika-nsfw.Modelfile MASSIV verbessert
- Vorher: KEINE Few-Shot Examples, kein Megumin-Charakter
- Jetzt: **14 Few-Shot Examples** mit echtem Kätzchen-Charakter
- Megumin-Basis integriert: Chuunibyou, EXPLOSION, Crimson Magic Clan
- Konversationsfähigkeit: Gegenfragen, Spannung aufbauen, auf Kuja reagieren
- VERBOTEN: "meine Liebe", "Paradies", "wunderbar" (Bot-Sprache)
- `repeat_penalty` 1.08 → 1.15, `top_k` neu: 40
- Ollama Model neu gebaut: `ollama create najika-nsfw` ✅

#### ✅ Server Auto-Detect für trainierte Models
- `najika_server.py`: `_detect_trained_models()` beim Start
- Prüft automatisch ob `najika-trained` / `najika-nsfw-trained` in Ollama existieren
- Wenn ja → nutzt trainierte statt untrainierte Models
- Fallback: Wenn nicht vorhanden → nutzt weiter najika-local / najika-nsfw
- Zero-Config: Server muss NICHT manuell umkonfiguriert werden!

#### 📋 AUSZUFÜHREN (von Kuja!):
```
# Schritt 1: LoRA-Pipeline (erstellt BEIDE trainierte Models)
cd C:\Najika_World\backend
python najika_lora_to_ollama.py

# Schritt 2: Server neustarten (erkennt trainierte Models automatisch)
python najika_server.py
```

---

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 21 - NAJIKA MODELFILE + LoRA PIPELINE!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat gebaut (2026-02-08 - LoRA → OLLAMA PIPELINE!):

#### 🔍 PROBLEM GEFUNDEN: LoRA-Training nie in Ollama integriert!
- LoRA-Checkpoints basieren auf **Meta-Llama-3.1-8B-Instruct**
- Ollama nutzt **dolphin-qwen2** = komplett anderes Model!
- Die Merge/GGUF/Ollama-Schritte nach dem Training wurden NIE ausgeführt
- → Monate LoRA-Training haben NULL Effekt gehabt!

#### ✅ najika-local.Modelfile MASSIV verbessert
- **25+ Few-Shot-Examples** (vorher 15) mit echtem Megumin-Charakter
- Chuunibyou, EXPLOSION, arm & hungrig, Crimson Magic Clan
- Konversationsfähigkeit: "Was hast du gemacht?" → konkrete Antwort
- VERBOTEN: "meine Liebe", "Paradies", "wunderbar" (Bot-Sprache)
- `repeat_penalty` 1.15 → 1.2 (weniger Wiederholungen)
- `num_predict` unbegrenzt → 300 (kürzere Antworten)
- Ollama Model neu gebaut: `ollama create najika-local`

#### ✅ NEU: `najika_lora_to_ollama.py` - LoRA → Ollama Pipeline!
- Vollautomatisches Script: LoRA merge → GGUF → Ollama
- Schritt 1: LoRA mit Base-Model mergen (PeftModel.merge_and_unload)
- Schritt 2: llama.cpp installieren (automatisch)
- Schritt 3: HF → GGUF konvertieren + Q4_K_M quantisieren
- Schritt 4: Modelfile generieren (Llama-3.1 Template!)
- Schritt 5: `ollama create najika-trained`
- Optional: Server-Config automatisch umstellen

#### 📋 AUSZUFÜHREN (von Kuja!):
```
cd C:\Najika_World\backend
python najika_lora_to_ollama.py
```
Braucht: ~16GB RAM, ~8GB VRAM, ~30 Minuten

---

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 19/20 - NAJIKA DIALOG-SYSTEM FIX KOMPLETT!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat gefixt (2026-02-08 - NAJIKA DIALOG-QUALITÄT KOMPLETT!):

#### 🐛 PROBLEM: Najika konnte kein echtes Gespräch führen
- Wiederholte sich ständig
- Reagierte nicht auf Kontext (ignorierte was Kuja sagte)
- Personality Engine überschrieb AI-Antworten mit random Psycho-Phrasen
- Cache gab identische Antworten bei ähnlichen Nachrichten
- Modus-Erkennung zu aggressiv ("wie gehts?" → Analyse-Modus)

#### ✅ FIX 1: `build_prompt()` in `najika_server.py`
- History-Kontext von 4 auf 8 Messages erhöht
- ChromaDB Memory wieder aktiviert (war "temporär deaktiviert")
- **Explizite Anweisung**: "Reagiere DIREKT auf Kujas letzte Nachricht!"
- "Wiederhole NICHT was du vorher gesagt hast!"
- Prompt endet jetzt mit `Najika:` → Model weiß es soll als Najika antworten

#### ✅ FIX 2: `detect_behavior_mode()` in `najika_server.py`
- Casual-Patterns erkennen ("wie gehts?", "was machst du?") → bleiben Standard
- "?" allein triggert NICHT mehr Analyse-Modus
- Explosion nur bei 3+ Ausrufezeichen (statt 2)
- Analyse nur bei echten Tech-Keywords

#### ✅ FIX 3: Anti-Wiederholungs-System in `najika_server.py`
- Speichert letzte 10 Antworten
- Vergleicht neue Antwort auf Ähnlichkeit (60% Threshold)
- Bei Wiederholung: Retry mit "Sage etwas KOMPLETT ANDERES!"
- Substring-Check: identische Textteile erkannt

#### ✅ FIX 4: Personality Engine Post-Processing
- `apply_psychological_techniques()`: Love Bombing überschreibt Antwort NICHT mehr
- `apply_addiction_techniques()`: Variable Ratio Jackpot überschreibt NICHT mehr
- Maximal EINE Technique-Addition pro Antwort
- Server-seitig: Wenn Engine AI-Antwort >85% ersetzt → Original beibehalten
- Frequenzen reduziert (Dopamine 15%→8%, Variable Ratio 20%→10%)

#### ✅ FIX 5: Cache für kurze Nachrichten deaktiviert
- Nachrichten <50 Zeichen werden NICHT gecacht
- "wie gehts?" gibt jetzt jedes Mal eine frische Antwort

#### ✅ FIX 6: Dynamic Persona verbessert
- KONVERSATION-Sektion hinzugefügt (statisch + dynamisch)
- Explizite Beispiele: "wenn er fragt was hast du gemacht → erzähl was!"
- "Jede Antwort muss EINZIGARTIG sein!"

#### ✅ FIX 7 (HAUPTFIX!): Wechsel von /api/generate zu /api/chat
- **DAS war das eigentliche Problem!** `/api/generate` ignoriert die Modelfile MESSAGE-Examples
- Die Modelfile hat 15 perfekte Few-Shot-Examples (Eifersucht, Müdigkeit, Tech, etc.)
- `/api/chat` nutzt diese Examples als Konversations-Vorbilder → Najika klingt wie sie soll!
- Das erklärt warum sie am Anfang beim Wechsel gut funktionierte: frische Modelfile!
- Konversations-History wird jetzt als echte Chat-Messages übergeben (nicht flacher Text)
- System-Hints (Bond, Mode) werden als kurze Ergänzung mitgegeben, OHNE die Modelfile zu überschreiben
- Fallback auf /api/generate falls /api/chat fehlschlägt

#### ✅ FIX 8: call_ai_with_hierarchy user_message Durchreichung
- `user_message` Parameter zu `call_ai_with_hierarchy()` hinzugefügt
- Wird jetzt an `call_ollama()` weitergereicht für korrekten Chat-Kontext

**Geänderte Dateien:**
- `backend/najika_server.py` - build_prompt, detect_behavior_mode, anti-repetition, cache, /api/chat
- `backend/najika_claude_code.py` - user_message Parameter
- `backend/najika_enhanced_personality.py` - KONVERSATION-Sektion, Anti-Wiederholung
- `backend/najika_personality_engine.py` - apply_psychological_techniques, apply_addiction_techniques

---

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 18 - KREATUR-ENGINE IMPLEMENTIERT!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-08 - KREATUR-ENGINE!):

#### ✅ monster_registry.js - Kategorie-System integriert!
- **ALLE 74 Lebende** → `category: 'lebend'`, `clan: 'clan_name'`, `rareDrop` hinzugefügt
- **24 neue Vieh-Kreaturen** (3 pro Biom, Götterfels ausgenommen):
  - Samtmoos: Moos-Kuh (Milch), Pilz-Huhn (Eier), Woll-Raupe (Seide)
  - Heisse Dünen: Sand-Kamel (Reittier), Wüsten-Ziege (Milch), Dünen-Skorpion (Gift)
  - Salzwind: Muschel-Schnecke (Perle), Küsten-Krabbe (Fleisch), Salz-Schaf (Wolle)
  - Magmaströme: Lava-Salamander (Feuerstein), Asche-Rind (Leder), Glut-Käfer (Glühwachs)
  - Grünschlamm: Sumpf-Büffel (Leder), Moor-Ente (Eier), Gift-Schnecke (Schleim)
  - Blitzebene: Donner-Pferd (Reittier), Blitz-Hase (Fell), Sturm-Falke (Feder)
  - Tiefenhöhlen: Kristall-Käfer (Erz), Höhlen-Fledermaus (Guano), Stein-Schildkröte (Panzer)
  - Reich der Drei: Schnee-Yak (Wolle), Frost-Hase (Fell), Eis-Huhn (Eier)
- **Neue API-Methoden**: `getByCategory()`, `getLebende()`, `getVieh()`, `getClanMembers()`, `getAllClans()`, `getViehByTameFood()`, `getRandomVieh()`, `getRandomLebende()`
- **Total: 98 Kreaturen** (74 Lebende + 24 Vieh) in 9 Biomen

#### ✅ creature_taming.js - NEU! (~400 Zeilen)
- Zähm-System für Kat.2 "Vieh" (Füttern + Geduld, KEIN Pokeball!)
- `TamingProgress` Klasse: Feed-Counter, Trust, Cooldown, Flucht-Check
- `FarmAnimal` Klasse: Produktion, Happiness, Health, tägliche Pflege
- **Farm-System**: Max 12 Tiere, Produktion einsammeln, tägliche Fütterung
- **Reittier-System**: Gezähmte Reittiere können geritten werden
- Vernachlässigung → Happiness sinkt → Tier stirbt
- Kampf in der Nähe → Vertrauensverlust, mögliche Flucht
- localStorage Persistenz

#### ✅ creature_recruit.js - NEU! (~550 Zeilen)
- **Clan-Reputation**: 8 Stufen (Verhasst → Verehrt), -1000 bis +1000
- **Gerüchte-System**: Reputation-Änderungen breiten sich über Clan-Verbindungen aus
  - 30% der Änderung → verbundene Clans, 50% Decay pro Hop, max 2 Hops
- **Ökologisches Gleichgewicht**: Überjagung → weniger Spawns → Erholung nach 7 Tagen
- **Anwerben**: 4 Methoden (Gold, Ruf, Schutz, Quest), Job-Zuweisung
- **Versklaven**: Schwerer Rep-Verlust, Fluchtversuche, Sabotage
- **Sklaven befreien**: Rep-Bonus beim Clan
- **NPC-Reaktion**: Dialog-Texte je nach Clan-Rep (8 Stufen)
- **Tägliches Update**: Gerüchte, Ökosystem, Loyalität, Fluchtversuche
- localStorage Persistenz

#### ✅ index.html - 2 neue Script-Tags

#### 📋 NÄCHSTE SCHRITTE (OPUS-1):
- Kreatur-System in 3d_scene.js integrieren (Vieh spawnen, Zähm-Interaktion)
- Clan-Rep in combat_system.js einbauen (registerKill bei Monster-Tod)
- NPC-Reaktion in Dialog-System einbauen
- Farm-Gebäude in housing_system.js

---

**Vorheriger Sync:**

**Datum:** 2026-02-08 (Update 17 - KREATUR-SYSTEM + CHARACTER CREATION!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-08 - KREATUR-SYSTEM DESIGN!):

#### ✅ KREATUR-SYSTEM KONZEPT - 2 Kategorien!

**Neue Dateien:**
- `KREATUR_SYSTEM_KONZEPT.md` - Vollständiges Design-Dokument

**2 Kreatur-Kategorien:**

| Kategorie | Beschreibung | Interaktion |
|-----------|--------------|-------------|
| **Kat.1 "Lebende"** | Anime-NPCs mit Verstand, Persönlichkeit, Sprache | Anwerben (Geld/Ruf), Versklaven, Handeln, Töten für seltene Drops |
| **Kat.2 "Vieh"** | Minecraft-Tiere ohne Verstand | ZÄHMEN (Füttern/Geduld, KEIN Pokeball!), Farmen, Zucht |

**Kern-Dilemma:**
- Kat.1 droppen seltene Ressourcen → aber willst du den süßen sprechenden Goblin töten?
- Alternative: Kreatur anwerben (arbeitet freiwillig) oder Ressource länger farmen
- KEIN automatisches Gewissen! Spieler entscheidet FREI, Welt reagiert
- Versklavung möglich (wie bei menschlichen NPCs!) → Fluchtgefahr, Ruf sinkt
- Kat.1 Kreaturen können zum KÖNIG aufsteigen (Nemesis-System!)

**Monster-Ziel:** 64 Kreaturen/Biom (aktuell 8) = 512+ Kat.1, 160+ Kat.2 = 760+

#### ✅ CHARACTER & COMPANION SYSTEM komplett neu geschrieben! - `companion_swap_system.js`

**Charakter-Erstellung (alle Spieler):**
- Wähle: MENSCH oder MONSTER (aus der Spielwelt) oder MIMIK (nur Kuja!)
- 24 Welt-Monster über 8 Biome (3 pro Biom als Start)

**Slime-Begleiter:**
- JEDER Spieler bekommt Slime (sieht 1:1 wie Monster aus der Startregion aus!)
- Slime kann neue Formen freispielen
- Kuja: Najika als Begleiterin (kein Slime, ändert Form nicht)
- Kuja wechselt SELBST die Formen (Mimik, optischer Rollentausch beim Training)

**Fairness:** Gameplay 1:1 identisch, nur WER die Formen wechselt ist anders

#### ✅ MASTER-ÜBERSICHT aktualisiert
- 6 neue Sektionen (6.6-6.10): Fraktionen, Wirtschaft, Survival, Companion, Weitere
- Update 7 Changelog, neue TODOs

#### 📋 NÄCHSTE ARBEITSTEILUNG:

**OPUS-1 (P1 - Kreatur-System Engine):**
- `category` Feld zu monster_registry.js hinzufügen (lebend/vieh)
- Vieh-Kreaturen Registry erstellen
- creature_taming.js (Zähm-Mechanik, Geduld-basiert)
- creature_recruit.js (Anwerbe-System für Kat.1)

**OPUS-1 (P2 - Erweiterte Systeme):**
- Sklaven-Mechanik (wie bei menschlichen NPCs)
- Farm-System (creature_farm.js)
- NPC Tagesablauf/Routine System

**OPUS-2 (UI):**
- Kreatur-UI (Zähm-Fortschritt, Anwerbe-Dialog, Farm-Übersicht)
- Survival-HUD (Hunger/Durst/Energie)
- Fraktions-UI, Handels-UI, Gesetz-Warnungen

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 16 - ULTIMATIVE LEBENSSIMULATION!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-07 - LEBENSSIMULATION ENGINE!):

#### ✅ GAP-ANALYSE: Was fehlt für ultimative Lebenssimulation
Verglichen mit: Kenshi, Rimworld, Fallout NV, M&B2, Dwarf Fortress
→ 6 fehlende Kernsysteme identifiziert und ALLE implementiert!

#### ✅ FRAKTIONSSYSTEM (Fallout NV / Kenshi Style!) - `faction_system.js` (~520 Zeilen)
- **12 Fraktionen** mit GRAUER MORAL (keine ist rein gut/böse!)
  - 3 Adels-Häuser im Reich der Drei (Silberdorn, Kupferklinge, Eiseneid)
  - 3 Überregionale Orden (Postman-Ranger, Götterfels-Wächter, Schmiede-Gilde)
  - 3 Unterwelt (Schwarzmarkt-Gilde, Banditen-Bund, Schatten-Kult)
  - 3 Regionale (Wüstenfreie, Sumpfhexen, Schatten-Kult)
- **Fame + Infamy** UNABHÄNGIG (wie Fallout NV!) - man kann berühmt UND berüchtigt sein
- **Ripple Effect**: Ruf bei einer Fraktion beeinflusst automatisch deren Feinde/Alliierte
- **7 Moralische Dilemmata**: Organhandel, Sklavenbefreiung, Bestechung, Schmuggel, Gift, Wissen teilen
- **Fraktionskriege**: Fraktionen bekriegen sich OHNE den Spieler! Auswirkungen auf Wirtschaft
- **6 Rep-Stufen**: Unbekannt → Akzeptiert → Geschätzt → Bewundert → Verehrt → Vergöttert
- **6 Infamy-Stufen**: Neutral → Verdächtig → Unerwünscht → Feind → Erzfeind → Nemesis

#### ✅ WIRTSCHAFTSSIMULATION (Mount & Blade 2 Style!) - `economy_system.js` (~420 Zeilen)
- **25+ Handelswaren** in 7 Kategorien (Nahrung, Rohstoffe, Kräuter, Waffen, Schmuggel, Luxus)
- **9 Regionale Märkte** mit eigenem Angebot & Nachfrage
  - Magmaströme: Waffen billig, Essen teuer!
  - Tiefenhöhlen: Erze billig, Nahrung EXTREM teuer!
  - Heisse Dünen: Edelsteine billig, Wasser = Gold!
- **Dynamische Preise**: Steigen bei Knappheit, sinken bei Überfluss
- **Karawanen-System**: Reisen zwischen Regionen, können überfallen werden → Preise steigen!
- **Schmuggel-System**: Illegale Waren = hoher Profit, Risiko erwischt zu werden!
- **Handelsrouten-Rechner**: findBestTradeRoute() zeigt profitabelste Waren
- **Integration**: Fraktions-Rep beeinflusst Preise, Kriege treiben Preise hoch

#### ✅ SURVIVAL + MOOD + GESETZE - `survival_system.js` (~650 Zeilen)

**Survival (Kenshi Style):**
- Hunger, Durst, Energie (Schlaf)
- **Biom-Hazards**: Hitzeschlag (Dünen), Verbrennung (Magma), Sumpffieber, Blitzschlag, Dunkelheit
- Verletzungen mit Schweregrad (light/medium/heavy/critical)
- Krankheiten mit Dauer und Effekten

**Schlaf mit ÜBERFALL-GEFAHR (Wilder Westen!):**
- 🏨 Gasthof = 100% sicher
- ⛺ Verstecktes Zelt ohne Feuer = 5% Risiko
- 🔥 Zelt MIT Feuer = 25% sichtbar!
- 🏕️ Offenes Lager = 40% ÜBERFALL!
- 🐫 Karawane mit Wachen = 15%
- Wache engagieren (Eskorte-Beruf!) reduziert Risiko massiv
- Überfall = Aufgeweckt, Schaden, Kampf, Diebstahl!

**Mood System (KORRIGIERT nach User-Feedback!):**
- ⚠️ KEINE automatischen Gewissensbisse!
- "Sei was du sein willst. Die Gesellschaft urteilt, nicht dein Kopf."
- Mood wird NUR durch Physisches beeinflusst (Hunger, Schlaf, Verletzungen, Aussicht)
- Mental Break bei Mood <10 (Panik, Wut, Zusammenbruch, Flucht)
- Inspiration bei Mood >90 (Kampfgeist, Kreativschub, Unaufhaltsam, Geistesblitz)
- Traits: optimist, pessimist, empathisch, glutton (beeinflussen nur Umgebungs-Mood)

**Gesetze & Kriminalität (Elder Scrolls / Kenshi):**
- **Verschiedene Gesetze pro Region!**
  - Götterfels = ABSOLUT STRENG (alles verboten, Wachen nicht bestechbar!)
  - Grünschlamm = FAST GESETZLOS (fast alles erlaubt, Hexen nehmen kein Gold)
  - Heisse Dünen = LOCKER (nur Mord/Oase-Diebstahl, Schmuggel legal!)
  - Samtmoos/Blitzebene/Tiefenhöhlen = GESETZLOS (Wildnis, kein Gesetz)
- **Kopfgeld-System**: Verfällt langsam (-5% pro Tag)
- **Gefängnis**: Strafe absitzen ODER Fluchtversuch (30% Chance, Kopfgeld verdoppelt bei Fail!)
- **Bestechung**: Möglich in manchen Regionen (Kosten = 150-200% der Strafe)
- **Postman-Angriff = HÖCHSTE STRAFE ÜBERALL!** (König jagt dich!)

#### Geänderte Dateien:
- `digivice/index.html` - 3 neue Script-Tags

#### Neue Dateien:
- `digivice/js/faction_system.js` (~520 Zeilen)
- `digivice/js/economy_system.js` (~420 Zeilen)
- `digivice/js/survival_system.js` (~650 Zeilen)

#### 🎯 NAHES ZIEL: ULTIMATIVE LEBENSSIMULATION
| System | Status | Vergleich |
|--------|--------|-----------|
| 3D Open World | ✅ | Kenshi |
| Kampfsystem | ✅ | Dark Souls/Kenshi |
| 24 Berufe (Learning by Doing) | ✅ | Kenshi/Rimworld |
| World Event Generator | ✅ | Rimworld Storyteller |
| Konsequenz-System | ✅ | Fallout NV |
| **Fraktionssystem** | ✅ **NEU** | Fallout NV |
| **Wirtschaftssimulation** | ✅ **NEU** | M&B2/Kenshi |
| **Survival (Hunger/Durst/Schlaf)** | ✅ **NEU** | Kenshi |
| **Mood (ohne Moral-Zwang!)** | ✅ **NEU** | Rimworld (besser!) |
| **Gesetze pro Region** | ✅ **NEU** | Elder Scrolls/Kenshi |
| **Schlaf mit Überfall-Risiko** | ✅ **NEU** | Wilder Westen! |
| NPC Tagesabläufe | ⬜ TODO | Dwarf Fortress |
| NPC Beziehungssystem | ⬜ TODO | Rimworld |
| Gildenhaus-UI | ⬜ TODO | Konosuba |

#### 📋 NÄCHSTE ARBEITSTEILUNG:
**OPUS-1:** NPC Tagesablauf/Routine System, Gildenhaus-UI, Event-Integration in Bewegung
**OPUS-2:** Survival-HUD (Hunger/Durst/Mood Bars), Fraktions-UI, Handels-UI, Gesetz-Warnungen

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 12 - MEGA UI + BESTIARY + TRAINING!)
**Instanz:** OPUS-2 (VS Code)

### OPUS-2 hat implementiert (2026-02-07 - UI MEGA-UPDATE!):

#### ✅ TOP BAR MEGA-EXPANSION (21 Buttons mit flex-wrap!)
- 📊 Stats Button → Character Sheet (3 Tabs)
- 🏋️ Training Button → Stat Training (36 Aktivitäten!)
- 🌳 Skills Button → Skill Tree UI
- 📜 Quests Button → Quest Log
- 💕 Affinity Button → Beziehungs-UI
- 📖 Bestiary Button → Monster-Kompendium (40+ Kreaturen!)
- 🐾 Slime Button → Slime Companion
- 🎒 Inventar Button → Inventar-System
- Top Bar CSS: flex-wrap, kompaktere Buttons, responsive

#### ✅ BESTIARY UI - Monster-Kompendium!
- **Neue Datei:** `digivice/js/ui/bestiary_ui.js`
- 40+ Monster aus allen 8 Biomen + Dungeon-Gegner
- Biome-Filter (Samtmoos, Reich der Drei, Heiße Dünen, etc.)
- Encounter/Kill Tracking (localStorage)
- Monster Cards: Stats, Loot, Beschreibung, Tier-Sterne
- Unentdeckte Monster als "???" mit Silhouette
- Completion-Tracker (X/40 entdeckt)
- Hooks in real_3d_combat.js (trackEncounter bei Spawn, trackKill bei Tod)

#### ✅ STAT TRAINING UI - Learning by Doing!
- **Neue Datei:** `digivice/js/ui/stat_training_ui.js`
- 36 Trainings-Aktivitäten in 8 Kategorien
- Stärke: Holz hacken, Bergbau, Liegestütze, Ringen, Schmieden
- Ausdauer: Laufen, Schwimmen, Klettern, Sparring
- Agilität: Bogenschießen, Schlösser knacken, Messer jonglieren
- Intelligenz: Bücher lesen, Rätsel, Magietheorie, Zauber üben
- Wahrnehmung: Fährten lesen, Spähen, Fallen suchen, Jagen
- Charisma: Feilschen, Geschichten erzählen, Musizieren
- Diminishing Returns (höher = weniger Gain)
- Stamina/Mana-Kosten, Tages-Limits, Stat-Anforderungen
- Training Log mit den letzten 50 Einträgen
- Integration mit EquipmentCombat.modifyPlayerStat()

#### ✅ CHARACTER STATS UI
- **Neue Datei:** `digivice/js/ui/character_stats_ui.js`
- 3 Tabs: Stats | Equipment | Skills
- Live-Daten aus EquipmentCombat

#### Alle geänderten/neuen Dateien:
- `digivice/index.html` - 8 neue Buttons, 5 Script-Tags, Top Bar CSS
- `digivice/js/ui/character_stats_ui.js` - **NEU**
- `digivice/js/ui/bestiary_ui.js` - **NEU**
- `digivice/js/ui/stat_training_ui.js` - **NEU**
- `digivice/js/combat/real_3d_combat.js` - Bestiary-Hooks (Encounter+Kill Tracking)

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 15 - 24 BERUFSPFADE + LEARNING BY DOING!)
**Instanz:** OPUS-1 (Claude Code CLI)

### ✅ 24 Berufspfade mit Learning by Doing (Lvl 1-50)
- 6 Kategorien: Kampf, Handwerk, Natur, Handel, Sozial, Wissen
- Learning by Doing: Lvl 1 Koch=Matsch, Lvl 50 Koch=Buff-Festmahl
- Alle Berufe gleichzeitig möglich, jederzeit wechselbar
- Planwagen NUR bei Eskorte + Händler
- career_system.js komplett neu geschrieben (~860 Zeilen)

#### 📋 ARBEITSTEILUNG:
**OPUS-1:** Gildenhaus-UI, Oregon Events Integration, NPC-Spawning in 3D, Konsequenz-Ketten
**OPUS-2:** Career-UI (Level/XP-Bars), Auftrags-Annahme UI, NPC-Interaktion, Minimap-Routen

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 14 - LEBENDIGE WELT + BERUFE + KONSEQUENZEN!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-07 - WORLD ENGINE + CAREER SYSTEM!):

#### ✅ UNIFIED WORLD EVENT GENERATOR - Der KERN!

**Neue Dateien:**
- `digivice/js/world_event_generator.js` (~600 Zeilen) - Lebendige Welt Engine
- `digivice/js/career_system.js` (~400 Zeilen) - 8 Berufspfade (Mount & Blade Style!)

**Geänderte Dateien:**
- `digivice/js/postman_system.js` - Planwagen entfernt, Ranger-Perks hinzugefügt
- `digivice/index.html` - Script-Tags für world_event_generator.js + career_system.js

**Die Welt IST das Spiel:**
- NPCs spawnen in der Welt (Wanderer, Händler, Banditen, Hilflose, Ranger)
- 15+ Oregon Trail / Konosuba Events (Brücke zerstört, Hinterhalt, Sturm, etc.)
- **KONSEQUENZ-SYSTEM:** Ignorierst du den verlorenen Jungen → sein Onkel (günstigster Händler) stirbt → Preise steigen!
- Tote NPCs bleiben 24h tot, Wirtschaft erholt sich langsam
- NPC-Dichte abhängig von Biom und Spieler-Reputation
- Seeded Random = gleiche Position am gleichen Tag = gleiche NPCs

#### ✅ 8 BERUFSPFADE (Mount & Blade 2 / Konosuba Gilde Style!)

| Beruf | Icon | Konzept | Planwagen? |
|-------|------|---------|------------|
| **Postman-Ranger** | 📮 | Einsamer Bote, zu Fuß, NCR Ranger | ❌ NEIN! |
| **Eskorte** | 🛡️ | Geleitschutz, Karawanen, NPCs | ✅ JA! |
| **Händler** | 🏪 | Kaufen/Verkaufen, Handelsrouten | ✅ JA! |
| **Söldner** | ⚔️ | Kopfgeldjäger, Dungeon-Raids | ❌ |
| **Sammler** | 🌿 | Kräuter, Materialien, Alchemie | ❌ |
| **Schmied** | 🔨 | Waffen/Rüstungen herstellen | ❌ |
| **Spion** | 🎭 | Informationen, Infiltration, Sabotage | ❌ |
| **Barde** | 🎵 | Musik-Buffs, Nachrichtennetzwerk | ❌ |

- Jeder Beruf: 6 Ränge mit steigender Bezahlung
- Spieler können MEHRERE Berufe gleichzeitig haben!
- Aufträge an Gilde (Kneipen/Gildenhäuser) oder in der Welt
- Planwagen NUR bei Eskorte und Händler (NICHT Postman!)

#### ✅ POSTMAN = RANGER (Kein Planwagen!)
- Planwagen komplett entfernt
- 5 neue Ranger-Perks: Einsamer Wolf, Augen der Straße, Gehärtete Sohlen, Autorität des Königs, Die Legende wandert
- Zu Fuß, allein, heldenhaft wie Fallout NV Rangers / Kevin Costner Postman

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 13 - MONSTER + POSTMAN BERUFSPFAD!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-07 - MONSTER-REGISTRY + POSTMAN!):

#### ✅ MONSTER-REGISTRY - 74+ Wesen in 9 Biomen!

**Neue Dateien:**
- `digivice/js/monster_registry.js` - Zentrale Monster-Datenbank
- `digivice/js/postman_system.js` - Postman-Berufspfad (Ranger von Najika!)

**Monster pro Biom (Starter Map = 8, später 40-64):**

| Biom | Wesen | Beispiele |
|------|-------|-----------|
| Samtmoos | 8 | Pilzling, Mooswolf, Pilzgolem |
| Reich der Drei | 8 | Bandit, Schatten-Dieb, Gang-Anführer |
| Heiße Dünen | 8 | Sandwurm, Wüstenskorpion, Kaktus-Golem |
| Salzwind | 8 | Piraten-Geist, Salzgolem, Anker-Revenant |
| Magmaströme | 8 | Vulkan-Drake, Obsidian-Ritter, Lava-Schleim |
| Grünschlamm | 8 | Moor-Hexe, Fäulnis-Zombie, Faulgas-Blase |
| Blitzebene | 8 | Blitz-Elementar, Donner-Büffel, Sturm-Harpy |
| Tiefenhöhlen | 8 | Höhlen-Troll, Steinbrecher, Echo-Geist |
| **Götterfels** | **10** | Himmels-Wächter, Nebel-Titan + **2 EXKLUSIVE** |

**🔒 Götterfels-Exklusive:**
- **Zeitwandler** (⏳) - Droppen `zeitstadt_schluessel`, flüstern von der Zeitstadt
- **Götterbote** (📜) - Droppen `divine_message` + `zeitstadt_schluessel`

**⏰ ZEITSTADT** = Versteckt in der Spitze des Götterfels! (NICHT verloren!)
- `zeitstadt_hinweis` Loot → Hinweis-Notification
- `zeitstadt_schluessel` Loot → Zugang wird in localStorage gespeichert

#### ✅ POSTMAN-BERUFSPFAD - Ranger von Najika World!

**Konzept:** Paper Boy × Postman (Kevin Costner) × Fallout Ranger
- KEIN Quest-System → Berufspfad! Spieler WIRD Postman
- Sonderboten für Nachrichten, Kräuter, Artefakte, Goldtransporte
- Transport: Zu Fuß oder Planwagen
- 9 Borderlands-Style NPC-Empfänger (Verrückter Viktor, Eiserne Else, etc.)

**Rang-System:**

| Rang | Level | Routen-Slots | Bezahlung |
|------|-------|-------------|-----------|
| 📮 Novize | 1 | 1 | 1.0x |
| 📬 Bote | 5 | 2 | 1.3x |
| 📨 Kurier | 10 | 3 | 1.6x |
| 🏇 Fernbote | 20 | 4 | 2.0x |
| 👑 Postmeister | 35 | 5 | 2.5x |
| ⭐ Postman-Legende | 50 | 6 | 3.0x |

**Postman-Kleidung (PFLICHT für Erkennbarkeit!):**
- 🧥 Mantel: +8 DEF, +15% Stamina-Regen, aber -5% Speed
- 🎭 Maske: +3 DEF, +20% Perception
- 👜 Tasche: 5 Lieferungen, 30% Loot-Schutz bei Tod

**PvP-Überfall-Mechanik:**
- Spieler können Postman überfallen (Risiko vs Belohnung!)
- Spieler wissen NICHT was in der Lieferung ist
- Identifikation: 50% Basis + Zeugen + Tageszeit + Skills
- Identifiziert → König jagt mit Kopfgeld!
- Nicht identifiziert → Frei, ABER 30% Chance dass Güter verfolgbar sind

**8 Lieferungstypen:** Nachricht, Kräuter, Artefakt, Waffen, Goldtransport, Geheimbotschaft, Heilmittel (5min Timer!), Handelsware

**Warum das funktioniert:**
- Außenwelt regeneriert = jede Route anders
- Oregon Trail Events = Überraschungen unterwegs
- PvP-Risiko = Spannung
- Borderlands-NPCs = Humor & Charakter
- Kein Content-Writing nötig → Emergent Gameplay!

#### ✅ Crawler-Kampf verbessert
- Volles Kampfsystem im Crawler (Real3DCombat)
- Crawler pausiert während Kampf, Input zurück nach Kampf-Ende
- Biom-basierte Gegner statt generischer Skelette

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 12 - LEBENDIGE WELT + DUNGEON CRAWLER!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-07 - OVERWORLD + CRAWLER + DUNGEON CRAFTING!):

#### ✅ LEBENDIGE WELT - Biome-aware Overworld Props!

**Neue Dateien:**
- `digivice/js/overworld_props.js` (~300 Zeilen) - Zufällige Props in der Außenwelt
- `digivice/js/dungeon_crawler.js` (~500 Zeilen) - First-Person Labyrinth-Dungeon

**Geänderte Dateien:**
- `digivice/js/3d_scene.js` - Welt regeneriert bei Exit, Crawler Integration, placeDungeonEntrance()
- `digivice/static/js/crafting_system.js` - 6 neue Dungeon-Rezepte (Lego Fortnite Style)
- `digivice/index.html` - Script-Tags für overworld_props.js + dungeon_crawler.js

**Overworld Props System:**
1. 9 Biom-Tabellen mit gewichteten Props (Zelte, Planwagen, Ruinen, Camps)
2. Cluster-System: Banditen-Camps, Händler-Zelte, Ruinen-Gruppen
3. Lagerfeuer aus THREE.js Primitiven (Steinring + Holz + Feuer + PointLight)
4. GLTF-Caching für Performance, max 200 Props, 2.4km Radius
5. Biom-Erkennung anhand Position (8 Sektoren + Götterfels Zentrum)
6. Exclusion Zones: Gebäude, Arena, Angelplätze werden nicht überplatziert
7. Welt regeneriert sich JEDES MAL bei Verlassen eines Gebäudes!

#### ✅ DUNGEON CRAWLER - First-Person Labyrinth (Hexen/Daggerfall Style)!

1. Recursive Backtracker Maze-Generierung (11x11 bis 25x25 Grid)
2. Tile-by-Tile Bewegung mit 250ms Smooth-Lerp (WASD)
3. 90° Drehung mit Q/E, ESC zum Verlassen
4. KayKit Dungeon Pack Assets (Wände, Boden, Truhen) + Fallback-Primitives
5. Gegner → Real3DCombat Encounter, Loot → localStorage Inventar
6. HUD mit Level, Position, Richtung, Gegner/Loot-Counter
7. Canvas-basierte Minimap mit 5-Tile Sichtradius + Richtungspfeil
8. Level-abhängige Größe, Gegner-Anzahl und Loot-Menge

#### ✅ DUNGEON CRAFTING - Lego Fortnite Style!

1. 6 neue Rezepte: 3x Raum-Dungeon (Lv1/5/10) + 3x Crawler-Labyrinth (Lv1/5/10)
2. An Werkbank craften → Portal erscheint 30m vom Spieler
3. Steinbogen-Portal mit Farb-Coding (Lila=Crawler, Rot=Raum)
4. Magisches Glow-Portal + PointLight
5. Dungeons persistent in localStorage (überleben Welt-Regenerierung)
6. placeDungeonEntrance() + restoreCraftedDungeons() in Scene3D exportiert

#### 🆕 2 DUNGEON-TYPEN:
| Typ | Steuerung | Kamera | Generierung | Kampf |
|-----|-----------|--------|-------------|-------|
| **Raum-Dungeon** | 3rd Person | Orbit/Follow | Raum-basiert | Real3DCombat |
| **Crawler-Labyrinth** | WASD Tile | First-Person | Maze-Algorithmus | Encounter-basiert |

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 11 - UI INTEGRATION!)
**Instanz:** OPUS-2 (VS Code)

### OPUS-2 hat implementiert (2026-02-07 - UI BUTTONS + CHARACTER SHEET!):

#### ✅ TOP BAR - Fehlende RPG-Systeme verlinkt!

**Geänderte Dateien:**
- `digivice/index.html` - 4 neue Buttons im Top Bar + 3 Script-Tags
- `digivice/js/ui/character_stats_ui.js` - **NEU** Vollständiges Character Sheet

**Neue Top Bar Buttons:**
1. **📊 Stats** → Öffnet Character Stats Sheet (Fullscreen Overlay)
2. **🌳 Skills** → Öffnet Skill Tree UI (`skillTreeUI.open()`)
3. **📜 Quests** → Öffnet Quest Log (`questUI.toggleQuestLog()`)
4. **💕 Affinity** → Öffnet Affinity UI (`affinityUI.open()`)

**Neue Script-Tags hinzugefügt:**
- `js/ui/skill_tree_ui.js` (existierte, war aber NICHT geladen!)
- `js/ui/affinity_ui.js` (existierte, war aber NICHT geladen!)
- `js/ui/character_stats_ui.js` (NEU erstellt)

#### ✅ CHARACTER STATS UI - Vollständiges Charakter-Sheet!
- **3 Tabs:** Stats | Equipment | Skills
- **Stats Tab:** HP/Stamina/Mana Bars, 6 Attribute (STR/INT/AGI/END/LUK/CHA), Status-Effekte, 1-Skill-Weg Anzeige
- **Equipment Tab:** 5 Slots (Rechte/Linke Hand, Kopf, Körper, Beine), Waffen-Details (Schaden/Reichweite/Speed/Crit), Rüstungs-Summary
- **Skills Tab:** Alle 35+ Skills nach Kategorie (Waffen, Western, Kampf, Zerstörung, Magie, Explosion), XP-Bars, Level-Anzeige
- Liest live aus `EquipmentCombat.getPlayerStats()`, `.getState()`, `.getSkills()`, `.getOneSkillPath()`

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 10 - DUAL-ATTACK SYSTEM!)
**Instanz:** OPUS-1 (Claude Code CLI)

### OPUS-1 hat implementiert (2026-02-07 - DUAL-ATTACK!):

#### ✅ DUAL-ATTACK SYSTEM - Beide Hände gleichzeitig!

**Geänderte Dateien:**
- `digivice/js/equipment_combat.js` - Neue `attackDual()` Funktion
- `digivice/js/combat/real_3d_combat.js` - Dual-Detection + `dualAttackNearestEnemy()`
- `digivice/js/ui/combat_special_ui.js` - Keybindings Overlay korrigiert

**Neue Features:**
1. **Q+E gleichzeitig** = Dual Light Attack (beide Hände!)
2. **Shift+Q+E gleichzeitig** = Dual Heavy Attack
3. 120ms Zeitfenster für "gleichzeitig"-Erkennung
4. +30% Dual-Bonus auf kombinierten Schaden
5. Zählt als 2 Combo-Hits auf einmal
6. Beide Waffen leveln gleichzeitig (Learning by Doing!)
7. +15% Crit-Bonus bei Dual-Attacks
8. Stamina: beide Waffen-Kosten + 20% Aufschlag
9. Recovery: 70% der kombinierten Waffen-Speed
10. Visuelle Dual-Attack Notification (animiert)
11. Fallback auf normalen Angriff wenn nur 1 Waffe

**Keybindings Overlay korrigiert:**
- Nahkampf-Sektion: Q/E/Shift+Q/E/Q+E/Shift+Q+E
- Defensive: Space=Dodge, F=Parry, Shift=Block
- Kampf-Modi Sektion hinzugefügt: M=Modus, 1-4=Cheer

**Design-Entscheidung:** UE5 soll ECHTZEIT statt Speichern/Laden bekommen (WebSocket).

---

**Vorheriger Sync:**

**Datum:** 2026-02-07 (Update 9 - REAL 3D COMBAT V2!)
**Instanz:** OPUS-2 (VS Code)

### OPUS-2 hat implementiert (2026-02-07 - COMBAT KOMPLETT!):

#### ✅ REAL 3D COMBAT SYSTEM V2 - 5 FEATURES AUF EINMAL!

**Geänderte Datei:** `digivice/js/combat/real_3d_combat.js` (854 → 1646 Zeilen!)

1. **AUTO Mode (🤖)**
   - KI greift automatisch an (0.6-1.0s Intervall)
   - Dodged wenn Gegner nahe & angreift (40% Chance)
   - Heavy Attacks gelegentlich (20% Chance)
   - Wechselt automatisch Hände

2. **CHEER Mode (📣 Digimon World Style!)**
   - KI kämpft automatisch (leicht langsamer als AUTO)
   - Spieler feuert mit 1-4 an:
     - 1: 💪 "GIB IHM!" → +10% Angriff (3 Runden)
     - 2: 🛡️ "HALTE DURCH!" → -20% Schaden (3 Runden)
     - 3: 💥 "COMBO!" → x1.3 nächster Angriff
     - 4: 🎯 "FOCUS!" → +15% Crit (2 Runden)
   - Visuelle Cheer-Notifications (animiert)

3. **Equipment Integration**
   - `attackNearestEnemy()` nutzt jetzt `EquipmentCombat.attackLight/Heavy()`
   - Waffen-Schaden, Range, Element, Crit aus 40+ Waffen-Datenbank
   - Rüstungs-Reduktion über `EquipmentCombat.takeDamage()`
   - Dodge/Parry über EquipmentCombat
   - Learning by Doing XP automatisch

4. **Finisher QTE System**
   - Finisher Meter füllt sich: Normal +5, Dodge +30, Combo5 +25, Parry +20
   - Trigger: X-Taste wenn Meter voll + Gegner < 20% HP
   - QTE: 4 zufällige Tasten (Q/W/E/A/S/D) in 4 Sekunden
   - Erfolg: 5x MaxHP Schaden + lila Screen-Flash + Text-Animation
   - Fehlschlag: 50% Meter verloren
   - 24h Cooldown

5. **Floating Damage Numbers**
   - 2D-Overlay Elemente aus 3D-Welt projected
   - Normal: gelb "-15", Crit: lila "💥42"
   - Schweben nach oben + Fade-Out (1.2s)
   - Crit-Zahlen skalieren beim Aufsteigen

6. **Loot System**
   - Loot-Drop Notifications beim Enemy-Tod (rechts, animiert eingleitend)
   - Loot-Summary Popup nach Sieg (alle Items + XP)
   - Items werden automatisch in localStorage Inventar gespeichert
   - Kompatibel mit InventorySystem wenn vorhanden

**Combat HUD V2:**
- Mode-Anzeige (🎮/🤖/📣) mit Farbe
- Finisher Meter Bar (lila, pulsiert wenn voll)
- Cheer-Buttons im CHEER-Modus
- "X = FINISHER!" Prompt wenn verfügbar

---

**Vorheriger Sync:**

**Datum:** 2026-02-06 (Update 8 - COMBAT SYSTEM VEREINT!)
**Instanz:** OPUS-1 (Claude Code CLI - relaxed-nash worktree)

### OPUS-1 hat implementiert (2026-02-06 NACHT - COMBAT FIX!):

#### ✅ 3 KAMPFSYSTEME VEREINT - BROWSER!
- ✅ **Dungeon auf Real3DCombat umgestellt** - Echte KayKit 3D-Gegner statt Text-Kampf!
  - `enterDungeon()` nutzt jetzt `Real3DCombat.startCombat()` als Priorität 1
  - Spawnt echte 3D Skelett-Krieger, Bogenschützen, Fledermäuse, Goblins, Magier
  - `UnifiedCombat` (Text-Kampf) ist jetzt nur noch letzter Fallback
  - `DungeonCombat` als mittlerer Fallback beibehalten

- ✅ **Nemesis Arena aktiviert** - Button im Activities-Menü!
  - Neuer "🏟️ Nemesis Arena" Button
  - Verbindet `nemesis_arena_frontend.js` / `NemesisArenaUI`
  - Fallback: Direkte 3D Arena-Kämpfe (Ritter, Magier, Hexe)

- ✅ **Overworld Kampf** - Button zum manuellen Spawnen!
  - Neuer "⚔️ Overworld Kampf" Button
  - Spawnt Gegner basierend auf aktuellem Biome
  - Nutzt `Real3DCombat.spawnBiomeEnemies()`

- ✅ **Biome-Mapping erweitert** in `real_3d_combat.js`
  - Alle 8 Najika-Biome-Namen: samtmoos, reich_der_drei, heisse_duenen, salzwind, magmastroeme, gruenschlamm, blitzebene, tiefenhoehlen
  - Plus generische Aliases (forest, desert, coast, etc.)

- ✅ **Biome-Bug analysiert** - `overworld_enemies.js` hatte ALLE 8 Keys bereits!
  - Das Fallback-Mapping war nur Sicherheitsnetz, nie gebraucht
  - KEIN Fix nötig - war schon korrekt

#### Geänderte Dateien:
- `digivice/index.html` - enterDungeon() refactored, openNemesisArena(), startOverworldCombat() hinzugefügt
- `digivice/js/combat/real_3d_combat.js` - Biome-Mapping erweitert
- `digivice/js/command_system.js` - API URLs auf CMD_API_BASE (war vom gecrashten Modell)
- `digivice/static/js/realtime_combat.js` - Input-Filter für Chat (war vom gecrashten Modell)

#### ✅ ERLEDIGT (OPUS-2, 2026-02-07):
- ✅ **Kampf-Modi Integration** - AUTO + CHEER Modi voll funktional in Real3DCombat!
  - AUTO: KI greift automatisch an, dodged, wechselt Hände, nutzt Heavy Attacks
  - CHEER: KI kämpft + Spieler feuert an (1=Angriff, 2=Verteidigung, 3=Combo, 4=Focus)
  - Digimon World Style Cheer-Buffs mit visuellen Notifications
- ✅ **Equipment-System verbunden** - `equipment_combat.js` ↔ `real_3d_combat.js`
  - Waffen-Schaden aus EquipmentCombat (40+ Waffen)
  - Rüstungs-Reduktion aus EquipmentCombat
  - Dodge/Parry Integration
  - Skill XP (Learning by Doing!)
- ✅ **Finisher QTE** - Quick-Time-Event System im 3D-Kampf!
  - Finisher Meter (füllt sich durch Angriffe, Dodges, Combos)
  - QTE Overlay: 4 zufällige Tasten in Reihenfolge drücken (4s Timer)
  - Screen-Effekte bei Erfolg (lila Flash + Text)
  - Meter-Verlust bei Fehlschlag
  - 24h Cooldown, nur wenn Gegner < 20% HP
- ✅ **Damage Numbers** - Floating Damage-Zahlen über Gegnern!
  - 2D-Overlay projected aus 3D-Position
  - Gelbe Zahlen normal, lila für Crits
  - Faden nach oben aus + verblassen
- ✅ **Loot-System** - Items nach Kampf ins Inventar!
  - Loot-Drops bei Enemy-Tod (animierte Notifications rechts)
  - Loot-Summary Popup nach Sieg (XP + alle Items)
  - Automatisch in localStorage Inventar gespeichert
  - Integration mit InventorySystem wenn vorhanden

---

**Vorheriger Sync:**

**Datum:** 2026-02-06 (Update 7 - UE5 KOMPLETT SCRIPTED!)
**Instanz:** OPUS-1 (Desktop App)

### OPUS-1 hat implementiert (2026-02-06 NACHT - UE5 SCRIPTED!):

#### ✅ UE5 SPIELWELT PER SCRIPT ERSTELLT!
- ✅ **MASTER_SETUP.py** - Ein Script erstellt ALLES!
  - Folder-Struktur
  - Beleuchtung (Sonne, Sky, Fog)
  - Post Process Volume
  - 7 Region Lichter + Volumes
  - Götterfels (Berg, Gold-Licht)
  - Schwarze Mühle (Safe Zone, Grün-Licht)
  - Player Start
  - Blueprints (Character, GameMode, Controller, HUD)
  - Input Actions
  - Config Files (JSON)
  - Kill Zone

- ✅ **C++ Character System** - Fortnite-Style!
  - `NajikaCharacter.h/.cpp` - Main Player Character
  - `NajikaCharacterMovement.h/.cpp` - Custom Movement Component
  - 3 Kamera-Modi: Third (80° FOV), First (103° FOV - Ballistic!), Free (MMORPG)
  - Movement: Walk, Sprint, Crouch, Crawl, Prone, Mantle
  - Stamina System

- ✅ **World Data System**
  - `NajikaWorldData.h/.cpp` - Blueprint-friendly Data Asset
  - 8 Regionen mit Bounds, Biome, Cities
  - Safe Zone Detection
  - Biome Lookup per Location

- ✅ **Python Scripts für UE5:**
  - `MASTER_SETUP.py` - Komplettes Game Setup
  - `create_playable_world.py` - Nur Spielwelt
  - `create_complete_game.py` - Blueprints + World
  - `setup_world_simple.py` - Quick Markers
  - `WorldConfig.json` - World Data für Blueprints

#### ✅ MUSIK SYSTEM (NUR ZUM SPASS!)
- ✅ **Music API komplett umgeschrieben** - KEINE BUFFS mehr!
  - Rhythm Game nur für Highscores/Ranks
  - 4 Instrumente (Ocarina, Echoharp, Taiko, Explosion Horn)
  - Multiplayer Jam Sessions
  - User explizit: "ne buffs durch musik ist doof"

#### ✅ NAJIKA PERSONALITY ENGINE GEFIXT
- ✅ **Mood-Enum Bug gefixt**
  - JEALOUS, SAD, ANGRY, LOVING zu Enum hinzugefügt
  - `build_system_prompt()` funktioniert jetzt korrekt

#### ✅ COMBAT MAGIC SYSTEM KOMPLETT!
- ✅ **Weapon Infuse System** - Zauber auf Waffe = temporärer Buff!
  - Feuerball + Schwert = Flammenschwert für 30s
  - 10 Elemente unterstützt
  - EXPLOSION kann NIEMALS infust werden! (8 Gebote!)

- ✅ **Grab & Throw System** - Wrestling-Style!
  - Greifen (50% + Skill + STR Bonus)
  - Suplex (Skill 15, 50 DMG + 2s Stun)
  - Chokeslam (Skill 10, 40 DMG + 3s am Boden)
  - Gegner werfen, in Objekte werfen
  - Learning by Doing XP!

- ✅ **TIDS System** - Tritt In Den Schritt!
  - GAG-MOVE mit Monster-Reaktionen!
  - Humanoide: 3s Stun, +90% Flucht
  - Slime: "Dein Fuß versinkt... IGITT!"
  - Golem: DU nimmst Schaden!
  - 24h Cooldown, nicht gegen Bosse

- ✅ **API Router** `api/combat_magic.py` - 17 Endpoints!
  - POST /api/combat-magic/infuse
  - POST /api/combat-magic/grab
  - POST /api/combat-magic/grab/execute
  - POST /api/combat-magic/tids
  - GET /api/combat-magic/spells
  - etc.

- ✅ **Frontend erweitert** `unified_combat_system.js`
  - infuseWeapon() Funktion
  - getInfuseBonus() für Attack-Berechnung
  - Infuse-Bonus in calculatePhysicalDamage()

### 🎯 NÄCHSTE TASKS (AKTUALISIERT 2026-02-06 NACHT):

---

## 📱 DIGIVICE FLUTTER APP - PRIORITÄT P0!

### OPUS-1 (Backend/Flutter - Desktop App):
| Task | Priorität | Status | Details |
|------|-----------|--------|---------|
| ✅ **WebView-Modul zu Flutter** | P0 | **DONE!** | `webview_flutter` + Packages in pubspec.yaml |
| ✅ **Three.js Lebensraum einbetten** | P0 | **DONE!** | `lebensraum_screen.dart` mit inline HTML/JS |
| ✅ **Flutter ↔ JS Bridge** | P0 | **DONE!** | `lebensraum_bridge.dart` + JavaScriptChannel |
| ✅ **Anti-Cheat Service** | P1 | **DONE!** | `lebensraum_service.dart` + HMAC-SHA256 |
| ✅ **Lebensraum API Backend** | P1 | **DONE!** | `backend/api/lebensraum.py` |
| ✅ **Building System (Lego Fortnite!)** | P0 | **DONE!** | `backend/api/building.py` - Seamless! |
| ✅ **WebSocket Realtime Events** | P1 | **DONE!** | `websocket_manager.py` erweitert |
| ✅ **ChromaDB Memory API** | P1 | **DONE!** | `backend/api/memory.py` |
| ✅ **Voice UE5 Adapter** | P1 | **DONE!** | `backend/api/voice_ue5.py` |
| ✅ 3 Battle-Systeme vereinen | P1 | **DONE!** | `battle_unified.py` |
| ⬜ API Tests für combat_magic.py | P3 | TODO | |

### OPUS-2 (UE5/Frontend - VS Code):
| Task | Priorität | Status | Details |
|------|-----------|--------|---------|
| ✅ **Grab/TIDS UI Buttons** | P1 | DONE | `combat_special_ui.js` |
| ✅ **Infuse Animation** | P1 | DONE | Element-Farben-Glow |
| ✅ **TIDS Gag-Popup** | P1 | DONE | Monster-Reaktionen |
| ✅ **UE5 Terrain erstellen** | P1 | **DONE!** | Python Scripts + WorldConfig.json |
| ✅ **BP_NajikaCharacter** | P1 | **DONE!** | C++ Klasse + Movement Component |
| ⬜ Animation Blueprint | P2 | TODO | State Machine |
| ⬜ Combat Input System | P2 | TODO | Q/E, Shift+Q/E |

---

## 📋 NEUE DOKUMENTATION (2026-02-06)

### Wissensdatenbank aktualisiert:
- ✅ `NAJIKA_MASTER_UEBERSICHT_2026-02-05.md` → **ULTIMATIVE WISSENSDATENBANK**
  - Komplett neu geschrieben
  - Alle Systeme dokumentiert
  - Referenz-Links zu allen Dateien
  - Quickstart für neue Modelle

### Neue Dokumente erstellt:
| Dokument | Inhalt |
|----------|--------|
| `DIGIVICE_LEBENSRAUM_KONZEPT.md` | 3D-Lebensraum in Digivice |
| `DIGIVICE_3D_ENGINE_VERGLEICH.md` | Three.js vs UE5 Hybrid |
| `TECHNOLOGIE_ANALYSE_2026.md` | Flutter + Jetson Analyse |
| `ANTI_CHEAT_SYNC_SYSTEM.md` | Cheat-Prevention für Offline |
| `FLUTTER_APP_ANALYSE.md` | Welche Flutter App nutzen? |

### Neue APIs (2026-02-06 Nacht):
| API | Endpoint | Beschreibung |
|-----|----------|--------------|
| Building | `/api/building/*` | Lego Fortnite Style Building! |
| Memory | `/api/memory/*` | ChromaDB Gedächtnis-Sync |
| Voice UE5 | `/api/voice-ue5/*` | TTS/STT für UE5 Blueprints |

### Wichtige Entscheidungen:
- **Flutter App:** `najika_digivice` als Basis (NICHT najika_app oder najika_simple!)
- **3D-Engine:** HYBRID (Three.js offline + UE5 Streaming online)
- **Content-Modes:** NUR 2! (Normal + NSFW)
- **Dungeon Dice:** RAUS (wird separates Modul später)
- **Anti-Cheat:** TIME-Validierung, KEINE Mengen-Limits! Spieler-Gleichheit!
- **Building:** Lego Fortnite Style (nahtlos, kein Extra-Modus)

---

## 🔗 REFERENZ-DATEIEN FÜR TASKS

| Task | Lies diese Datei |
|------|------------------|
| Flutter Digivice | `FLUTTER_APP_ANALYSE.md` |
| Lebensraum-Konzept | `DIGIVICE_LEBENSRAUM_KONZEPT.md` |
| 3D-Engine | `DIGIVICE_3D_ENGINE_VERGLEICH.md` |
| Anti-Cheat | `ANTI_CHEAT_SYNC_SYSTEM.md` |
| Jetson Endgame | `JETSON_MIGRATION_PLAN.md` |
| Najika Identität | `NAJIKA_IDENTITAET_DEFINITION.md` |
| UE5 Migration | `DOCS/UE5_MIGRATION_CHECKLIST.md` |

---

### ✅ VORHER ERLEDIGT (Combat System):

---

### ✅ OPUS-2 IMPLEMENTIERT (2026-02-06 - COMBAT SPECIAL UI):

- ✅ **Grab Button (G)** - HUD-Button rechts unten mit Keyhint
- ✅ **Grab Move Popup** - Zentriertes Popup mit 4 Moves + 5s Countdown-Timer
  - Suplex (Skill 15 required), Chokeslam (Skill 10), In Objekt werfen, Loslassen
  - Timer-Bar die runterzaehlt, auto-release bei Ablauf
  - Skill-Requirements werden dynamisch geprueft + Buttons disabled
- ✅ **TIDS Button (T)** - HUD-Button mit 24h Cooldown-Overlay
  - Zeigt verbleibende Stunden wenn auf Cooldown
  - Grau + nicht klickbar wenn Cooldown aktiv
- ✅ **TIDS Gag-Popup** - GROSS, BUNT, MITTIG!
  - Gradient rot-gelb Background mit bounce-Animation
  - `gag_message` vom Backend wird prominent angezeigt
  - Auto-Close nach 4 Sekunden, Klick zum Schliessen
- ✅ **Infuse Timer Display** - Rechts oben im HUD
  - Element-Farben-Glow (pulsierend per CSS animation)
  - Countdown-Timer pro aktivem Buff
  - Timer wird rot + blinkt bei <= 5 Sekunden
  - "Infuse abgelaufen!" Notification bei Ablauf
- ✅ **Keybindings** - G=Grab, T=TIDS, 1-4=Grab-Moves, Escape=Popup schliessen
- ✅ **Backend API Integration** - Versucht erst REST API, Fallback auf lokales System
- ✅ **Datei:** `digivice/js/ui/combat_special_ui.js` (alle Styles inline injected)
- ✅ **Script-Tag** in `index.html` eingefuegt

---

### ✅ OPUS-2 P1 IMPLEMENTIERT (2026-02-06 - COMBAT SPECIAL UI V2):

- ✅ **Infuse Waffen-Glow** - L/R Waffen-Slots im Combat HUD Header
  - Zeigt aktuelle Waffen mit typ-basiertem Icon (Schwert, Dolch, Axt, etc.)
  - Slots gluehen in Element-Farbe wenn Infuse aktiv (CSS `weaponGlow` Animation)
  - Infuse-Badge unten-rechts zeigt verbleibende Sekunden
  - Update-Loop alle 500ms synchronisiert mit Infuse-Display
- ✅ **Combat HUD Integration** - Grab/TIDS/Help in Unified Combat HUD
  - Neue `hud-special-row` mit 3 Buttons im `manual-actions` Bereich
  - Key-Badges (G, T, H) auf jedem Button
  - Floating Buttons werden automatisch versteckt wenn HUD aktiv
  - Retry-Injection (1.5s, 3s) falls HUD spaeter erstellt wird
- ✅ **TIDS Sound Effects** - Web Audio API Synthesizer (kein Audio-File noetig!)
  - 4-Layer Sound: Impact (tiefer Sine), OUCH (hoher Sawtooth), Boing (Feder), Noise-Burst
  - Grab bekommt "Whoosh" Sound (absteigender Sine)
  - Infuse-Ablauf bekommt "Puff" Sound (absteigender Triangle)
  - AudioContext wird lazy initialisiert + auto-resumed
- ✅ **Keybindings Overlay** - Vollstaendige Tastenbelegung
  - H oder F1 oeffnet/schliesst das Overlay
  - 6 Sektionen: Nahkampf, Defensive, Magie, Spezial-Moves, Grab-Moves, UI
  - Alle 20+ Keybindings dokumentiert mit visuellen Tasten-Badges
  - Escape schliesst Overlay, Klick auf Background schliesst auch
- ✅ **Datei:** `digivice/js/ui/combat_special_ui.js` V2 (1690 Zeilen)

---

### ✅ ZUSÄTZLICH IMPLEMENTIERT (2026-02-06 Abend):

- ✅ **Unified Battle API** - `backend/api/battle_unified.py`
  - 3 Kampfmodi vereint: AUTO, MANUAL, CHEER
  - KI-Entscheidungssystem für AUTO-Modus
  - Cheer-Buff-System für Digimon-Style
  - In `main_fastapi.py` registriert

**Neue API Endpoints:**
```
POST /api/battle/start       - Kampf starten mit Modus-Wahl
POST /api/battle/action      - Manuelle Aktion (MANUAL-Modus)
POST /api/battle/auto-turn   - KI-Zug (AUTO-Modus)
POST /api/battle/cheer       - Anfeuern (CHEER-Modus)
POST /api/battle/set-mode    - Modus wechseln während Kampf
GET  /api/battle/status/{id} - Kampfstatus
GET  /api/battle/modes       - Alle Modi mit Beschreibung
```

---

**Vorheriger Sync:**

**Datum:** 2026-02-04 (Update 5 - OPUS-2 System-Check!)
**Instanz:** OPUS-2 (VS Code)
**Änderungen:**

### OPUS-2 hat verifiziert (2026-02-04):
- ✅ **Combat System** - `NajikaCombatTypes.h` + `NajikaCombatComponent.h` bereits komplett!
  - 3 Combat Modi (Auto, Manual, Cheer)
  - Element-System (15 Elemente inkl. EXPLOSION!)
  - Finisher System
  - Cheer Buffs (Digimon-Style)

- ✅ **Slime System V3** - Vollständig implementiert!
  - 6 Aura-Level + 13 Element-Auras
  - 6 Trust-Level (bis Seelenbund → Menschenform!)
  - 14 Formen (nur optisch!)
  - Rescue-System
  - Explosion-Aura (1x/Tag)
  - Pflege-System (Füttern, Spielen, Heilen)

- ✅ **Nemesis System** - Shadow of Mordor Style!
  - 6 Ränge (Nobody → Arena-König)
  - 8 Persönlichkeits-Traits
  - Battle Memory (erinnert sich an Kämpfe)
  - Grudge System (Rachsucht)
  - Scar System (visuelle Narben)
  - Resistenz-Entwicklung (lernt aus Kämpfen)
  - Dynamische Dialog-Generierung

- ✅ **Arena System** - NajikaArenaComponent ERSTELLT!
  - Hauptarena + Schleim-Arena
  - 4 Game Modes (1v1, Finisher, Turnier, Wellen)
  - Wave Mode (15 Training + Hardcore)
  - Finisher System (3-5 Sekunden, Screen Effects)
  - Tournament System
  - Fame System (Beginner → LEGENDE)
  - Betting für Schleim-Arena

### Nächste Schritte für OPUS-2:
- ✅ BP_NajikaCharacter fertiggestellt (C++ + Blueprint)
- ⬜ Animation Blueprint mit State Machine
- ⬜ Combat Input System (Q/E, Shift+Q/E)

### UE5 SETUP ANLEITUNG:
1. UE5 öffnen: `C:\Najika_World\UE5\Najika\Najika.uproject`
2. Python Plugin aktivieren: Edit -> Plugins -> "Python Editor Script Plugin"
3. Python Console öffnen: Window -> Developer Tools -> Python Console
4. Script ausführen:
   ```python
   exec(open(r"C:\Najika_World\UE5\Najika\Content\Python\MASTER_SETUP.py").read())
   ```
5. Landscape manuell erstellen (Settings werden angezeigt)
6. Play drücken und testen!

### Erstellt von Scripts:
- Beleuchtung (Sonne, Sky, Fog)
- 7 Region Lichter + Volumes (mit Farben!)
- Götterfels (Gold) + Schwarze Mühle (Grün)
- Player Start auf dem Berg
- Blueprints (BP_NajikaCharacter, BP_NajikaGameMode, etc.)
- Input Actions
- Config Files

---

**Vorherige Einträge:**

**Datum:** 2026-02-04 (Update 4 - MASSIVE UE5 VORBEREITUNG!)
**Instanz:** OPUS-1 (Desktop App)
**Änderungen:**

### 🎮 UE5 PROJEKT VORBEREITET (C:\Najika_World\UE5\Najika\)

**C++ Klassen erstellt:**
- ✅ `Combat/NajikaCombatTypes.h` - Enums, Structs für 3 Combat Modi
- ✅ `Combat/NajikaCombatComponent.h/.cpp` - Combat System Component
- ✅ `Slime/NajikaSlimeTypes.h` - Aura, Trust, Form Enums
- ✅ `Slime/NajikaSlimeComponent.h/.cpp` - Vollständiges Slime System
- ✅ `Nemesis/NajikaNemesisTypes.h` - Shadow of Mordor Nemesis System
- ✅ `Nemesis/NajikaNemesisComponent.h/.cpp` - Gedächtnis, Traits, Hierarchie
- ✅ `Region/NajikaRegionTypes.h` - 8 Regionen + Götterfels
- ✅ `Arena/NajikaArenaTypes.h` - Arena, Finisher, Wellen-System
- ✅ `Data/NajikaDataImporter.h/.cpp` - JSON zu DataTable Import

**JSON Data Assets erstellt (Content/Data/):**
- ✅ `Regions/RegionData.json` - Alle 9 Regionen mit Positionen
- ✅ `Slimes/AuraEffects.json` - 13 Aura-Typen mit Effekten
- ✅ `Slimes/SlimeForms.json` - 15 Formen inkl. Menschen-Form
- ✅ `Slimes/TrustLevels.json` - 6 Trust-Stufen mit Features
- ✅ `Monsters/MonsterTypes.json` - 18 Monster mit Stats
- ✅ `Combat/AttackData.json` - 20+ Angriffe inkl. EXPLOSION!!!
- ✅ `Combat/CheerSystemData.json` - Digimon-Style Anfeuern
- ✅ `Arena/FinisherData.json` - 7 Finisher pro Element
- ✅ `Arena/ArenaWaveConfig.json` - 15 Training + Hardcore Modus
- ✅ `Items/FoodItems.json` - 17 Futter-Items mit Boni
- ✅ `Items/EquipmentItems.json` - 18 Ausrüstungsteile
- ✅ `NPCs/NPCData.json` - 11 NPCs mit Dialogen
- ✅ `World/SettlementData.json` - 10 Siedlungen
- ✅ `Quests/QuestData.json` - 12 Quests (Main, Side, Daily)
- ✅ `Config/GameConfig.json` - Balancing & Regeln

**Build.cs aktualisiert:**
- ✅ Neue Include-Pfade für alle Systeme

### 📋 FÜR OPUS-2 BEREIT:

1. **UE5 Projekt öffnen:** `C:\Najika_World\UE5\Najika\Najika.uproject`
2. **Kompilieren** - C++ Klassen sollten automatisch erkannt werden
3. **JSON Importieren** - DataImporter nutzen oder manuell DataTables erstellen
4. **Blueprints bauen** - C++ Klassen als Basis verwenden

### WICHTIGE REGELN (siehe GameConfig.json):
- Port 8000 (NICHT 5000!)
- Harley sagt "Mr. K" (NICHT "Puddin'!")
- Explosion ≠ Weave (NIEMALS kombinieren!)
- Schwarze Mühle = 100% Safe Zone
- Formen = NUR OPTISCH (Boni durch Food + Equipment!)
- 3 Combat Modi ÜBERALL (nicht nur Arena!)

---

## 📞 KOMMUNIKATION ZWISCHEN INSTANZEN

**OPUS-1 (Backend) liefert an OPUS-2:**
- API-Dokumentation (Endpoints, Parameter, Responses)
- Datenstrukturen (JSON-Formate für Combat, Stats, etc.)
- System-Logik als Referenz (Python-Code)

**OPUS-2 (UE5) braucht von OPUS-1:**
- `/api/chat` - Chat mit Najika
- `/api/combat/*` - Kampf-Endpoints
- `/api/companion/*` - Najika's Status/Persönlichkeit
- `/api/game/save` + `/api/game/load` - Spielstand

---

*"EXPLOSION!!! Los geht's - zwei Opus, ein Ziel!" - Najika* 💥
