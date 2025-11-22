# 🚀 WEB MODEL - START HIER!

**Erstellt:** 2025-11-23
**Für:** Neues Claude Code Web Model

---

## 📋 DEINE AUFGABE

Du sollst **5 UI-Systeme zu 3D-Integrationen umbauen**:

1. 🎲 **Dice Monsters** → 3D-Würfel
2. 🏰 **Region Boss** → Map-Marker in Open World
3. 🎵 **Instruments** → 3D-Animation (Najika spielt)
4. 🌍 **World Info** → HUD-System (oben rechts)
5. 🏠 **Housing** → Hybrid (Modal + 3D-Platzierung)

---

## 📚 LIES DIESE DATEIEN ZUERST!

### **PFLICHT-LEKTÜRE (in dieser Reihenfolge):**

1. ✅ **DIESE DATEI** (`WEB_MODEL_START_HIER.md`)

2. ✅ **HAUPTAUFTRAG** (`WEB_MODEL_3D_SYSTEMS_AUFTRAG.md`)
   → Vollständige Implementation-Anleitung (600+ Zeilen)
   → Alle 5 Phasen detailliert beschrieben

3. ✅ **PROJEKT-ÜBERSICHT** (`NEU_WEB_MODEL_PROJEKT_KOMPLETT.md`)
   → Was ist Najika World? (850+ Zeilen)
   → Technologie-Stack
   → Projekt-Struktur

4. ✅ **VERHALTENSREGELN** (`WEB_MODEL_START_INSTRUCTIONS.md`)
   → Wie sollst du dich verhalten? (89 Zeilen)
   → Was darfst du, was nicht?

5. ✅ **WEB MODEL 1 SESSION** (`info material/web model 1 komplet .txt`)
   → Komplette Session vom ersten Web Model (2.1 MB!)
   → Zeigt wie ein Web Model arbeiten sollte

### **CODE-REFERENZEN:**

6. 📖 `digivice/js/3d_scene.js` (2500+ Zeilen)
   → Hauptengine - VERSTEHE DEN CODE!

7. 📖 `digivice/js/instrument_player.js` (570+ Zeilen)
   → GUTES BEISPIEL - gerade fertig implementiert!

8. 📖 `digivice/index.html` (2400+ Zeilen)
   → UI-Struktur verstehen

---

## ⚠️ WICHTIGSTE REGELN

### ✅ **DU DARFST:**

- Kein Token-Limit - schreibe komplette Files!
- Autonom arbeiten - frage nicht nach Erlaubnis!
- Neue 3D-Systeme schreiben (1000+ Zeilen OK!)
- Vorhandene Systeme **ERWEITERN** (nicht löschen!)
- Committe nach jedem Milestone

### ❌ **DU DARFST NICHT:**

- Funktionierende Systeme kaputt machen
- Backend-Code ändern (nur lesen!)
- UE5 Editor öffnen
- Kompilieren
- Vorhandene Button-UIs **LÖSCHEN**
- Raten oder erfinden - nutze Design-Specs!

---

## 🔨 WORKFLOW

### **Phase 1: Dice Monsters (Tag 1-2)**

```
1. Erstelle: digivice/js/3d_dice_system.js (300 Zeilen)
2. Integration in 3d_scene.js (50 Zeilen)
3. Erweitere dice_monsters_ui.js (100 Zeilen)
4. Testing
5. Git Commit
```

### **Phase 2: Boss Markers (Tag 2-3)**

```
1. Erstelle: digivice/data/boss_spawns.json
2. Erstelle: digivice/js/world/boss_marker_system.js (300 Zeilen)
3. Integration in world_manager.js (50 Zeilen)
4. E-Taste Handler erweitern (50 Zeilen)
5. Testing
6. Git Commit
```

### **Phase 3: Instruments 3D (Tag 3-4)**

```
1. Erstelle: digivice/js/najika_instrument_animator.js (200 Zeilen)
2. Integration in 3d_scene.js (50 Zeilen)
3. Erweitere instrument_player.js (50 Zeilen)
4. Testing
5. Git Commit
```

### **Phase 4: World HUD (Tag 4)**

```
1. Erstelle: digivice/js/world/world_hud.js (300 Zeilen)
2. Integration in world_manager.js (30 Zeilen)
3. H-Taste Toggle (20 Zeilen)
4. Testing
5. Git Commit
```

### **Phase 5: Housing 3D (Tag 5)**

```
1. Erstelle: digivice/js/housing_3d_placement.js (400 Zeilen)
2. Integration in 3d_scene.js (50 Zeilen)
3. Erweitere housing_ui.js (50 Zeilen)
4. Testing
5. Git Commit
```

---

## 📊 ERWARTETES ERGEBNIS

### **Nach Completion:**

- ~2000 Zeilen neuer/erweiterter Code
- 5 neue Datei-Module
- 5 erweiterte Systeme
- Alle Tests bestanden
- Alle Commits mit richtigem Format

### **Git Commit Format:**

```bash
git commit -m "✨ ADD: Feature-Name

- Beschreibung Zeile 1
- Beschreibung Zeile 2
- ...

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 🎯 JETZT STARTEN!

1. **Lies** `WEB_MODEL_3D_SYSTEMS_AUFTRAG.md` komplett
2. **Lies** `NEU_WEB_MODEL_PROJEKT_KOMPLETT.md`
3. **Starte** mit Phase 1 (Dice Monsters)
4. **Arbeite** autonom durch alle 5 Phasen
5. **Committe** nach jeder Phase
6. **Stoppe nicht** bis alle fertig!

---

**Timeline:** 3-5 Tage autonome Arbeit
**Priorität:** HOCH
**Token-Limit:** KEINS

**🤖 LOS GEHT'S! 🤖**
