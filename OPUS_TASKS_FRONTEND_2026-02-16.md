# 🎨 OPUS TASKS - FRONTEND & DESIGN
## Browser Beta Preparation - Phase 2

**Session:** 2026-02-16 Round 3
**Assigned to:** OPUS Model (Frontend/Design Spezialist)
**Geschätzter Aufwand:** ~100 Minuten

---

## 📋 AUFGABEN-ÜBERSICHT

Basierend auf **COMPLETE_CODE_AUDIT_2026-02-15.md** - OPUS Tasks:

### 1. ⚛️ Particle Systems Evaluation (20min) - P2

**Dateien:**
- `digivice/js/particles/particle_system.js`
- `digivice/js/particles/weather_particles.js`
- `digivice/js/particles/magic_particles.js`

**Status:** Nicht in index.html eingebunden

**Aufgabe:**
- Prüfe ob Particle-Systeme funktionsfähig sind
- Teste auf Konflikte mit Three.js r128
- Wenn funktional → In index.html einbinden nach Three.js
- Wenn broken → Dokumentiere Probleme für spätere Fixes

**Erwartetes Ergebnis:**
- ✅ Particle-Systeme eingebunden ODER
- 📝 Bug-Report mit konkreten Problemen

---

### 2. 🎮 UI Systems Evaluation (30min) - P1

**Dateien:**
- `digivice/js/ui/inventory_ui.js`
- `digivice/js/ui/quest_tracker_ui.js`
- `digivice/js/ui/minimap_ui.js`
- `digivice/js/ui/skill_tree_ui.js`
- `digivice/js/ui/character_sheet_ui.js`
- `digivice/js/ui/notification_system.js`

**Status:** Nicht in index.html eingebunden

**Aufgabe:**
- Teste jedes UI-System einzeln
- Prüfe auf DOM-Konflikte (z.B. doppelte IDs)
- Prüfe ob CSS-Dependencies fehlen
- Binde funktionierende Systeme ein
- Dokumentiere broken Systeme

**Erwartetes Ergebnis:**
- ✅ Funktionierende UI-Systeme eingebunden
- 📝 Liste der broken Systeme mit Fehlerursachen

---

### 3. 🌍 World Systems Evaluation (10min) - P2

**Dateien:**
- `digivice/js/world/day_night_cycle.js`
- `digivice/js/world/weather_system.js`

**Status:** Nicht in index.html eingebunden

**Aufgabe:**
- Teste Day/Night Cycle
- Teste Weather System
- Prüfe Integration mit bestehendem World Manager
- Bei Erfolg → Einbinden nach world_manager.js

**Erwartetes Ergebnis:**
- ✅ World-Systeme eingebunden ODER
- 📝 Konflikte dokumentiert

---

### 4. 📱 Mobile Support (30min) - P2

**Dateien:**
- `digivice/js/mobile/touch_controls.js`
- `digivice/js/mobile/mobile_ui_adapter.js`
- `digivice/css/mobile.css` (bereits in index.html!)

**Status:** CSS eingebunden, JS fehlt

**Aufgabe:**
- Teste Touch Controls auf Desktop (Maus-Simulation)
- Teste Mobile UI Adapter
- Prüfe ob responsive Design funktioniert
- Binde JS-Dateien ein wenn funktional

**Erwartetes Ergebnis:**
- ✅ Mobile JS eingebunden
- 📱 Touch Controls funktionieren
- 📝 Mobile-Test-Bericht

---

### 5. 🎲 Minigame Subsystems (10min) - P3

**Dateien:**
- `digivice/js/minigames/fishing_minigame.js`
- `digivice/js/minigames/lockpicking_minigame.js`
- `digivice/js/minigames/rhythm_game.js`

**Status:** Nicht in index.html eingebunden

**Aufgabe:**
- Schnellcheck ob Minigames standalone funktionieren
- Bei Erfolg → Einbinden nach minigame_v2.js
- Bei Problemen → Dokumentieren (niedrige Priorität)

**Erwartetes Ergebnis:**
- ✅ Minigames eingebunden ODER
- 📝 "Für Beta nicht kritisch" - Skip

---

## 🎯 PRIORITÄTEN

### KRITISCH für Browser Beta (MUSS):
1. ✅ **UI Systems** (30min) - Inventory, Quest Tracker, Notifications
2. ✅ **Mobile Support** (30min) - Touch Controls, Responsive UI

### WICHTIG für Polished Beta (SOLLTE):
3. ⚛️ **Particle Systems** (20min) - Visueller Polish
4. 🌍 **World Systems** (10min) - Day/Night Cycle, Weather

### NICE TO HAVE (KANN):
5. 🎲 **Minigames** (10min) - Zusätzlicher Content

---

## 📝 DOKUMENTATIONS-FORMAT

Für jedes System:

```markdown
### System: [NAME]
**Status:** ✅ Funktioniert | ⚠️ Teilweise | ❌ Broken
**Eingebunden:** Ja/Nein
**Zeile in index.html:** [Nummer]

**Probleme gefunden:**
- Problem 1
- Problem 2

**Fixes angewendet:**
- Fix 1
- Fix 2

**Testergebnis:**
- [Beschreibung]
```

---

## 🚀 WORKFLOW

1. **Starte mit UI Systems** (höchste Priorität)
2. **Teste jedes System isoliert** (Console öffnen!)
3. **Dokumentiere Fehler sofort**
4. **Committe funktionierende Systeme einzeln**
5. **Erstelle Bug-Report für broken Systeme**

---

## ⚙️ TEST-SETUP

```bash
# Server starten
cd C:\Najika_World
python backend/najika_server.py

# Browser öffnen
http://127.0.0.1:8001

# Console öffnen (F12)
# Teste jedes System einzeln:
console.log(window.InventoryUI);  // Sollte [object] oder Function sein
```

---

## 📦 EXPECTED COMMITS

- `Frontend: UI Systems eingebunden (Inventory, Quest, Notifications)`
- `Frontend: Mobile Support aktiviert (Touch Controls + Adapter)`
- `Frontend: Particle Systems integriert`
- `Frontend: World Systems aktiviert (Day/Night, Weather)`
- `Frontend: Minigames eingebunden (Fishing, Lockpicking, Rhythm)`

ODER (wenn Probleme):

- `Docs: Frontend Systems Bug Report (UI/Particles/World)`

---

## 🎨 DESIGN-FOKUS

OPUS ist Spezialist für:
- **Frontend/Design** → UI-Systeme, Particles, Visuals
- **User Experience** → Mobile Controls, Responsive Design
- **Polish** → Animations, Transitions, Eye Candy

**NICHT** für OPUS:
- Backend-Code
- Performance-Optimierung
- Algorithmus-Logik

---

## ✅ SUCCESS CRITERIA

**Minimum (Browser Beta Ready):**
- ✅ 3+ UI-Systeme funktionieren
- ✅ Mobile Support aktiviert
- 📝 Bug-Report für broken Systeme

**Optimal (Polished Beta):**
- ✅ Alle UI-Systeme funktionieren
- ✅ Particle Systems laufen
- ✅ Day/Night Cycle aktiv
- ✅ Mobile vollständig getestet

---

**Erstellt:** 2026-02-16 09:15
**SONNET Session:** Abgeschlossen (5/5 Tasks ✅)
**OPUS Session:** Bereit zu starten
