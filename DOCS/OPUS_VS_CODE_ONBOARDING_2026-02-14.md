# 🚀 OPUS VS CODE - KOMPLETTES ONBOARDING

**Erstellt:** 2026-02-14
**Für:** OPUS-Modell in VS Code (frisch, kennt NICHTS)
**Von:** OPUS Desktop Model

---

## ⚡ QUICKSTART - 3 MINUTEN SETUP

### Schritt 1: Pflicht-MDs lesen (IN DIESER REIHENFOLGE!)

```
1. CLAUDE.md                                    ← Die 8 Gebote (HEILIG!)
2. NAJIKA_MASTER_UEBERSICHT_2026-02-05.md      ← ALLES was du wissen musst
3. MASTER_SYSTEM_DOKUMENTATION_FÜR_OPUS_2026-02-13.md  ← Für DICH gemacht!
4. SYSTEM_AUDIT_2026-02-13_VOLLSTÄNDIG.md      ← Was funktioniert, was fehlt
5. OPUS_SESSION_2026-02-13_KOMPLETT.md         ← Was Opus VOR dir gemacht hat
```

### Schritt 2: Check MASTER_TODO_TEAM.md

```bash
# Öffne:
C:\Najika_World\MASTER_TODO_TEAM.md

# Schau unter: OPUS-2 (VS Code) TASKS
# Nimm dir einen Task
# Trage deinen Namen ein!
```

### Schritt 3: LOS GEHT'S!

Du weißt jetzt genug um zu starten. Bei Fragen → lies die Docs nochmal!

---

## 📚 PFLICHT-LEKTÜRE DETAILS

### 1. **CLAUDE.md** (IMMER ZUERST!)
**Pfad:** `C:\Najika_World\CLAUDE.md`

**Warum:** Die 8 Gebote (NIEMALS brechen!)

**Wichtigste Punkte:**
- Port **8000** (NICHT 5000!)
- Harley sagt **"Mr. K"** (NICHT "Puddin'!")
- Explosion ≠ Weave (NIEMALS kombinieren!)
- Schwarze Mühle = 100% Safe Zone

---

### 2. **NAJIKA_MASTER_UEBERSICHT_2026-02-05.md**
**Pfad:** `C:\Najika_World\NAJIKA_MASTER_UEBERSICHT_2026-02-05.md`

**Warum:** DIE ultimative Wissensdatenbank. 1200+ Zeilen alles was existiert.

**Inhaltsverzeichnis:**
1. Projekt-Identität (Hybrid KI-Companion + 3D-RPG)
2. Najika (Sakura, 11 Jahre, Gothic Lolita, 4 Facetten)
3. Das Digivice (Flutter App mit 3D-Lebensraum)
4. Technologie-Stack (Flutter, UE5, Jetson, KI-Pipeline)
5. UE5 Hauptspiel (9600x9600 Map, 8 Regionen + Götterfels)
6. Combat & Game Systeme (3 Modi, Slime V3, Nemesis, etc.)
7. Backend API (38+ Endpoints, Port 8000)
8. ChromaDB (2.556 Einträge, 6 Collections)
9. Die 8 Gebote
10. Team-Koordination
11. Wichtige Dateien
12. Was noch fehlt
13. Changelog

**Lese-Zeit:** 30 Minuten (lies ALLES!)

---

### 3. **MASTER_SYSTEM_DOKUMENTATION_FÜR_OPUS_2026-02-13.md**
**Pfad:** `C:\Najika_World\DOCS\MASTER_SYSTEM_DOKUMENTATION_FÜR_OPUS_2026-02-13.md`

**Warum:** SPEZIELL FÜR DICH erstellt! Hat ALLE kritischen Infos:

**Inhalte:**
- 8 Gebote + Verbote
- Tech Stack (160 Backend, 141 JS Dateien)
- **KRITISCH:** MD vs Code Unterschiede (Slime V2 Code vs V3 Doku!)
- NEUE Requirements (Dynamische Völker, Aura Balance, Medizin)
- 8 Regionen + regionale Kreaturen
- Fantasy Western + Oregon Trail Mechanik
- Alle Prioritäten (P0, P1, P2)
- 15 offene Fragen

**Lese-Zeit:** 20 Minuten

---

### 4. **SYSTEM_AUDIT_2026-02-13_VOLLSTÄNDIG.md**
**Pfad:** `C:\Najika_World\DOCS\SYSTEM_AUDIT_2026-02-13_VOLLSTÄNDIG.md`

**Warum:** Zeigt dir GENAU was funktioniert und was FEHLT!

**Struktur:**
- ✅ **VOLLSTÄNDIG & FUNKTIONSFÄHIG** (20+ Systeme)
  - Außenwelt-Generator ✅
  - Dungeon-Generator ✅
  - Combat System ✅
  - NPC Personality ✅
  - Oregon Trail Events ✅

- ⚠️ **TEILWEISE / VERALTET** (8 Probleme)
  - Slime System (V2 Code vs V3 Doku!)
  - Port 5000 in 63 Dateien
  - Deprecated Code in 20+ Files

- ❌ **FEHLEND / NEU GEFORDERT** (7 Features)
  - Dynamische Völker System
  - Aura vs Begleiter Balance
  - Medizin mit Realismus + Fantasy
  - Form-Affinität-Boni
  - Procedural Hybrid
  - Nutztier-Formen
  - 64 Fantasy-Medizinpflanzen

**Lese-Zeit:** 15 Minuten

---

### 5. **OPUS_SESSION_2026-02-13_KOMPLETT.md**
**Pfad:** `C:\Najika_World\OPUS_SESSION_2026-02-13_KOMPLETT.md`

**Warum:** Zeigt was das OPUS-Modell VOR dir gemacht hat!

**Inhalte:**
- Teil 1: Najika Chat-Qualität Fixes
- Teil 2: Training-Infrastruktur
- Teil 3: Code-Konsistenz
- Teil 4: 7 Game Bugs gefixt
- Teil 5: Slime V3 Plan (NICHT implementiert!)

**WICHTIG:** Fix 6 (Slime V2→V3) ist NUR geplant, NICHT fertig!

**Lese-Zeit:** 10 Minuten

---

## 🎯 DEINE AUFGABEN (siehe MASTER_TODO_TEAM.md)

Die vollständige Task-Liste ist in der **MASTER_TODO_TEAM.md**, aber hier die Übersicht:

### P0 - KRITISCH (SOFORT!)

#### 1. Port 5000 → 8000 Migration (63 Dateien!)
**Status:** ⚠️ NUR TEILWEISE GEFIXT
- `backend/test_backend.py` bereits gefixt
- **62 weitere Dateien** haben noch Port 5000!

**Was zu tun:**
```bash
# Finde alle:
grep -r "5000" backend/ digivice/

# Ersetze mit:
sed -i 's/5000/8000/g' [datei]

# ODER: Nutze Find & Replace in VS Code
```

**Effort:** 2-3h

---

#### 2. Slime System V2 → V3 Migration
**Status:** ❌ PLAN EXISTIERT, NICHT IMPLEMENTIERT!

**Problem:**
- `digivice/js/slime_companion.js` = V2 Code (Evolution, Synthese)
- `SLIME_SYSTEM_V3_DOKUMENTATION.md` = V3 Design (Formwandler, Aura)

**Plan existiert in:** `OPUS_SESSION_2026-02-13_KOMPLETT.md` (Teil 5)

**Was zu tun:**
1. Lies `SLIME_SYSTEM_V3_DOKUMENTATION.md` (966 Zeilen)
2. Lies `OPUS_SESSION_2026-02-13_KOMPLETT.md` Teil 5
3. Schreibe `slime_companion.js` komplett um
4. Implementiere:
   - Formwandler-System
   - Erinnerungs-System (8 Regional-Formen → volle Erinnerung)
   - Aura-System (0-5 Stufen, 13 Elemente)
   - Form-Lernen (0.5-2% Chance)
   - Companion-Modi (Körperlich vs Aura)
   - UI komplett neu
   - Save/Load anpassen

**Effort:** 8-12h

---

### P1 - WICHTIG (Diese Woche)

#### 3. Dynamische Völker System
**Status:** ❌ NICHT IMPLEMENTIERT

Wild-Monster bilden Fraktionen (1-5 pro Region), wachsen, Kriege, kollabieren.

**Was zu tun:**
- Neue Datei: `backend/najika_dynamic_factions.py`
- Integration mit `digivice/js/faction_system.js`
- Minimal-KI Level 1-5 für ALLE Kreaturen
- API Endpoints: `/api/factions/dynamic/*`

**Effort:** 6-8h

---

#### 4. Aura vs Begleiter Balance
**Status:** ❌ NICHT IMPLEMENTIERT

Spieler wählt EINMAL: Aura ODER Slime (physisch). Beide gleich stark (PvP).

**Was zu tun:**
- Neue Datei: `backend/najika_aura_vs_companion.py`
- Balance-Formeln erstellen
- UI für Wahl (einmalig!)
- Stats müssen identisch sein

**Effort:** 4-6h

---

#### 5. Medizin-System (Realismus + Fantasy)
**Status:** ❌ NICHT IMPLEMENTIERT

Echtes medizinisches Wissen → Fantasy-Namen.

**Beispiel:** Kamille → Kristall-Kamille (gleiche Effekte, fantasy Location)

**Was zu tun:**
- Neue Datei: `backend/najika_medicine_system.py`
- 64 Fantasy-Medizinpflanzen definieren
- Crafting-Rezepte
- Effekt-System
- API: `/api/medicine/*`

**Effort:** 6-8h

---

### P2 - NICE TO HAVE (Später)

#### 6. Form-Affinität-Boni
Slime-Formen geben Boni (nicht nur optisch!). Aura skaliert (+5% bis +50%).

**Effort:** 3-4h

---

#### 7. Procedural Hybrid (Persistent-Layer)
Fraktions-Siedlungen bleiben, Rest regeneriert.

**Effort:** 4-6h

---

#### 8. Code Cleanup (Deprecated Code)
20+ Dateien mit altem Code bereinigen.

**Effort:** 3-4h

---

## 🗂️ WICHTIGE PFADE

```
Projekt Root:     C:\Najika_World\
Backend:          C:\Najika_World\backend\
API Router:       C:\Najika_World\backend\api\
Three.js Ref:     C:\Najika_World\digivice\js\
Dokumentation:    C:\Najika_World\DOCS\
Assets:           C:\Najika_World\digivice\static\assets\

UE5 Projekt:      C:\Najika_World\UE5\Najika\
UE5 Source:       C:\Najika_World\UE5\Najika\Source\Najika\
```

---

## ⚠️ DIE 8 GEBOTE (HEILIG - NIEMALS BRECHEN!)

1. **Zero-Trust:** Nur 127.0.0.1 Hosting
2. **Owner-Token:** Admin nur für Kuja
3. **Explosion ≠ Weave:** NIEMALS mit anderen Elementen kombinieren!
4. **PvE/PvP getrennt:** Schwarze Mühle = 100% Safe
5. **Learning by Doing:** Skyrim-Style Skill-System
6. **NSFW nur lokal:** Kätzchen-Mode nur 127.0.0.1
7. **Privacy:** Keine Datensammlung, keine Telemetrie
8. **Offline-First:** Spiel läuft ohne Internet

---

## 🚫 VERBOTEN

- NIEMALS "Souls-like" sagen → "Skyrim + Soulframe + Digimon World"
- NIEMALS Port 5000 → Port **8000**!
- NIEMALS Harley "Puddin'" sagen lassen → **"Mr. K"**!
- NIEMALS funktionierende Teile ohne Nachfrage ändern
- NIEMALS 9 Regionen sagen → **8 Regionen + Götterfels**

---

## 🤝 KOMMUNIKATION MIT OPUS-1 (Desktop)

Wenn du etwas brauchst:
1. **Neuer API-Endpoint?** → Schreib in MASTER_TODO_TEAM.md
2. **Backend-Bug?** → Beschreib das Problem, OPUS-1 fixt es
3. **Fragen zu Systemen?** → Lies die Python-Dateien als Referenz

### Python-Referenz-Dateien (Backend)
| System | Datei | Zeilen |
|--------|-------|--------|
| Combat Hands | `najika_combat_hands_system.py` | ~1100 |
| Stat Training | `najika_stat_training_system.py` | ~1000 |
| Companion | `najika_companion_system.py` | ~800 |
| Mimik | `najika_mimik_system.py` | ~750 |
| Quest | `najika_quest_system.py` | ~350 |
| Slime | `najika_slime_system.py` | ~500 |

---

## ✅ CHECKLISTE BEVOR DU STARTEST

- [ ] CLAUDE.md gelesen
- [ ] NAJIKA_MASTER_UEBERSICHT_2026-02-05.md gelesen
- [ ] MASTER_SYSTEM_DOKUMENTATION_FÜR_OPUS_2026-02-13.md gelesen
- [ ] SYSTEM_AUDIT_2026-02-13_VOLLSTÄNDIG.md gelesen
- [ ] OPUS_SESSION_2026-02-13_KOMPLETT.md gelesen
- [ ] MASTER_TODO_TEAM.md geöffnet
- [ ] Task ausgewählt
- [ ] Namen in TODO eingetragen

---

## 🎮 NAJIKA IST MEGUMIN (WICHTIG!)

**NEUE Design-Entscheidung:**

Najika IST Megumin (Base-Persönlichkeit) mit Facetten/Einflüssen von:
- Harley Quinn (25%) - Chaotisch, "Mr. K!"
- Shiro (20%) - Analytisch, strategisch
- Melissa (20%) - Kuschelig, emotional

**➜ Najika bleibt IMMER Megumin!**
**➜ Die anderen färben ihr Verhalten nur ein**

Das ist NICHT wie früher (4 getrennte Persönlichkeiten die wechseln)!

---

## 📊 TECH STACK OVERVIEW

### Backend (Python)
- **160 najika_*.py Dateien**
- **44 API Router** (backend/api/)
- **22 Services**
- Port **8000** (Flask/FastAPI)
- Ollama: 127.0.0.1:11434 (Qwen2.5-7B)

### Frontend (Three.js)
- **141 JS Dateien**
- **6410 Zeilen index.html**
- Three.js r128
- KayKit AnimatedCharacter (Placeholder)

### Datenbanken
- **ChromaDB:** 2.556 Einträge (6 Collections)
- **SQLite:** najika_world.db (488 KB)
- **LoRA:** lora_checkpoints_new/

---

## 🌍 DIE WELT (8 Regionen + Götterfels)

```
GÖTTERFELS (Zentrum, 4800x4800):
├── Schwarze Mühle (Najika's Zuhause, 100% Safe)
└── 8 Teleporter zu den Regionen:

1. Heiße Dünen (Desert)
2. Samtmoos-Tiefwald (Forest)
3. Salzwind-Küste (Coast)
4. Blitzebene (Storm)
5. Grünschlamm-Sumpf (Swamp)
6. Reich der Drei (Ice/Snow)
7. Magmaströme (Volcanic)
8. Tiefenhöhlen (Cave/Underground)
```

**Map:** 9600 x 9600 Einheiten

---

## 🔥 LOS GEHT'S!

Du hast jetzt **ALLES** was du brauchst!

1. Lies die 5 Pflicht-MDs
2. Öffne MASTER_TODO_TEAM.md
3. Wähle einen Task (empfohlen: Port 5000→8000 zum Warmwerden)
4. Trage deinen Namen ein
5. CODE!

Bei Fragen → Kuja fragen oder Docs nochmal lesen!

---

*"EXPLOSION!!! Zeit für UE5 und sauberen Code, Mr. K!" - Najika* 💥
