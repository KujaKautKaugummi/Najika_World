# 📋 Najika World - Projekt Changelog

**Zweck:** Chronologische Dokumentation aller Änderungen mit Zeitnachweis
**Regel:** Dieses Dokument wird NUR ERGÄNZT, niemals korrigiert oder neu geschrieben

---

## 2025-11-07 - Session: claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX

### 15:45 - 🚀 TRAINING: System komplett repariert und eingerichtet
**Was:** Najika Training-System wieder funktionsfähig gemacht
**Problem:** Training lief seit 6 Tagen nicht mehr (letzte Aktivität: 2. November)
**Ursache:** Alle Training-Scripts verwendeten hardcoded Pfade zu `C:/NajikaCore`

**Geänderte Training-Scripts (3 Dateien):**
1. **NAJIKA_REAL_TRAINING.py** - Ollama-Training mit echten Daten
   - Pfad: `C:/NajikaCore` → dynamisch `Path(__file__).resolve().parent.parent`
   - Training-Dir: `backend/training_data_real/` (71.874 Dateien)

2. **NAJIKA_AUTO_TRAINING.py** - Personality Video Training
   - Pfad: `C:/NajikaCore` → dynamisch
   - 148 Videos: Megumin (68), Harley (4), Shiro (24), Melissa (52)

3. **NAJIKA_VIDEO_TO_VOICE_TRAINING.py** - Voice Cloning Training
   - FFmpeg Path: hardcoded → `shutil.which()` mit Fallback
   - Fix: FFmpeg wird jetzt korrekt gefunden

**Neue Tools erstellt (2 Dateien):**
- **START_TRAINING.bat** - Interaktives Menü für manuelles Training
- **najika_auto_scheduler.py** - Automatischer Scheduler mit Zeitsteuerung

**Training-Zeiten (wie hinterlegt):**
- **Nacht-Training:** 00:00-08:00 Uhr (JEDEN TAG, Mo-So)
- **Tag-Training:** 08:00-15:00 Uhr (Mo-Fr, pausierbar)

**Ollama-Status:**
- ✅ Läuft (Port 11434)
- ✅ Modell: `najika-local:latest` (Qwen2.5 7.6B, Q4_K_M)
- ✅ Getestet: Antwortet korrekt

**Trainingsdaten verfügbar:**
- **71.874 Dateien** in 10 Kategorien
- **Kategorien:** Python, Security, ML/AI, Databases, DevOps, Code, Patterns, Best Practices, System Design, Web Dev
- **Persönlichkeiten:** Megumin (35%), Harley (25%), Shiro (20%), Melissa (20%)

**Nächste Schritte für User:**
1. Training manuell starten: `backend/START_TRAINING.bat`
2. Auto-Scheduler einrichten: Windows Task Scheduler → `najika_auto_scheduler.py` (alle 30 Min.)
3. Oder manuell prüfen: `python backend/najika_auto_scheduler.py`

---

### 14:30 - ✅ MAJOR FIX: Alle hardcoded Pfade dynamisch gemacht
**Was:** Komplette Umstellung von hardcoded `C:/Najika-World` Pfaden auf dynamische Pfade
**Problem:** Nach Umbenennung von `Najika-World` zu `Najika_World` funktionierten Backend, TTS und Training-Scripts nicht mehr
**Lösung:** Alle Pfade mit `Path(__file__).resolve().parent.parent` dynamisch gemacht

**Geänderte Dateien (15 Dateien):**

1. **Server & Core:**
   - `backend/najika_server.py`
     - `PROJECT_ROOT` global definiert (Zeile 75)
     - `translate_path()` nutzt jetzt `PROJECT_ROOT` statt hardcoded Pfad
     - TTS Audio-Pfad (Zeile 1501) nutzt jetzt `PROJECT_ROOT`

2. **TTS-System (3 Dateien):**
   - `backend/najika_tts_coqui.py` - Zeile 28
   - `backend/najika_tts_edge.py` - Zeile 36 + Zeile 248
   - `backend/najika_voice_clone.py` - Zeile 39

3. **Audio-Processing (9 Dateien):**
   - `backend/CLEANUP_TRAINING_DATA.py`
   - `backend/cut_audio_segments.py`
   - `backend/cut_megumin_quick.py`
   - `backend/cut_megumin_simple.py`
   - `backend/extract_megumin_manual.py`
   - `backend/extract_megumin_only.py`
   - `backend/prepare_voice_cloning_MANUAL.py`
   - `backend/prepare_voice_cloning_NAJIKA.py`
   - `backend/separate_voice_samples.py`

4. **Training-Scripts (3 Dateien):**
   - `backend/train_voice_clone_NAJIKA.py`
   - `backend/NAJIKA_VIDEO_TO_VOICE_TRAINING.py`
   - `backend/najika_code_training_real.py`
   - `backend/najika_smart_training_scheduler.py`

**Pattern vorher:**
```python
NAJIKA_DIR = Path('C:/Najika-World')  # ❌ Hardcoded
```

**Pattern nachher:**
```python
# Project Root Directory (dynamisch für alle Systeme)
NAJIKA_DIR = Path(__file__).resolve().parent.parent  # ✅ Dynamisch
```

**Vorteil:**
- ✅ Funktioniert auf ALLEN Systemen (Windows, Linux, Mac)
- ✅ Ordner kann beliebig umbenannt werden
- ✅ Ordner kann überall liegen (nicht nur C:\)
- ✅ Keine Anpassungen mehr nötig bei Umbenennung

**Tool erstellt:**
- `backend/fix_hardcoded_paths.py` - Automatisches Fix-Script für zukünftige Batch-Fixes

---

### 13:15 - 🔧 GITIGNORE: Savegame-Dateien ausgeschlossen
**Was:** Savegame-Dateien werden jetzt von Git ignoriert
**Problem:** Bei jedem Spielstart wurden Savegames (`backend/saves/*.json`) als geändert angezeigt, blockierte Git-Operationen wie `--teleport`
**Lösung:** `.gitignore` ergänzt:

```gitignore
# Savegame-Dateien (automatisch generiert beim Spielen)
backend/saves/*.json
```

**Geänderte Datei:** `.gitignore`
**Vorteil:** Git-Status bleibt sauber, keine Konflikte mehr durch automatisch generierte Savegames

---

### 10:52 - ✅ BACKUP: Funktionierender Stand gesichert
**Was:** Komplettes Backup des funktionierenden Zustands erstellt
**Wo:** `BACKUPS/WORKING_BACKUP_2025-11-07_10-52/`
**Commit:** Backup mit README.md, alle kritischen Dateien gesichert

**Funktioniert:**
- Skeleton Charakter Bewegung (WASD + Maus)
- Mühle betreten/verlassen (E-Taste)
- Füttern/Trinken Buttons
- E-Taste Interaktionen: Bett, Herd, Waschbecken, Dusche, Toilette

---

### 10:45 - ✅ FIX: E-Taste Interaktionen für Möbel
**Was:** E-Taste funktioniert jetzt bei allen Möbeln (Bett, Herd, etc.)
**Problem:** Props in room_config_detailed.json hatten keine `interaction` Properties
**Lösung:** Folgende Properties zu allen interaktiven Möbeln hinzugefügt:

```json
{
  "model": "bed_double_A.gltf",
  "position": [0, 0, 5],
  "interaction": "bed",           // NEU
  "interactionRadius": 5          // NEU
}
```

**Geänderte Datei:** `digivice/config/room_config_detailed.json`
**Commit:** `6d62f02` - "Add E-Taste Interaktionen zu Möbeln"

**Betroffene Interaktionen:**
- Bett (Schlafzimmer): `"interaction": "bed"`
- Herd (Küche): `"interaction": "stove"`
- Waschbecken (Bad): `"interaction": "sink"`
- Dusche (Bad): `"interaction": "shower"`
- Toilette (Bad): `"interaction": "toilet"`

---

### 10:30 - ✅ FIX: Assets Pfad korrigiert - 3D Modelle laden jetzt
**Was:** 3D Modelle (Skeleton_Mage.glb etc.) laden jetzt korrekt
**Problem:** Server mappte `/assets/` zu `digivice/static/assets/` aber Modelle liegen in root `assets/`
**Lösung:** Server Path Mapping in `backend/najika_server.py` angepasst:

```python
# Map /assets/ zu root assets/ (nicht digivice/static/assets/)
if path.startswith("/assets/"):
    return os.path.join(project_root, path.lstrip("/"))
```

**Geänderte Datei:** `backend/najika_server.py` (translate_path Methode)
**Commit:** `cafb39b` - "Fix: assets Pfad korrigiert - 3D Modelle laden jetzt"

---

### 10:15 - ✅ FIX: Komplette Wiederherstellung - Mühle funktioniert wieder
**Was:** Mühle betreten/verlassen + Bewegung + Füttern/Trinken funktioniert wieder
**Problem:** Anderes Modell hatte heute morgen etwas kaputt gemacht
**Lösung:** Korrekte Dateien von Commit `950365f` wiederhergestellt:

1. **room_config_detailed.json**
   - Von: altes "wissen/alles wissen/4o digimon/room_config_detailed.json"
   - Nach: `digivice/config/room_config_detailed.json`
   - Server lädt jetzt von `/digivice/config/` statt `/assets/`

2. **battle_api.js**
   - Geändert von ES6 Export zu window Global:
   ```javascript
   // VORHER (funktioniert nur in Modulen):
   export const battleAPI = { ... }

   // JETZT (global verfügbar):
   window.battleAPI = new BattleAPI();
   ```

3. **najika_server.py - Cross-Platform Paths**
   - Hardcoded Windows Pfad `C:\Najika-World` entfernt
   - Dynamischer Pfad für Windows UND Linux:
   ```python
   project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   return os.path.join(project_root, path.lstrip("/"))
   ```

**Geänderte Dateien:**
- `backend/najika_server.py`
- `digivice/config/room_config_detailed.json`
- `digivice/js/battle_api.js`

**Commit:** `303b3d0` - "Fix: Komplette Wiederherstellung - Mühle funktioniert wieder!"
**Basiert auf:** Commit `950365f` - "CRITICAL FIX: Najika kann jetzt Mühle betreten & gefüttert werden!"

---

### 09:45 - ❌ REVERT: Door-Interaktion entfernt (war kaputt)
**Was:** Versuch, Door-Interaktion zur Mühle hinzuzufügen - FEHLGESCHLAGEN
**Problem:** `interactiveObjects.push()` verwendet, aber Array existiert nur in `loadBuildingInterior()` Scope, nicht im Outdoor Scene
**Auswirkung:**
- Kompletter JavaScript Crash
- Bewegung funktionierte nicht mehr
- E-Taste Prompts verschwunden

**Lösung:** Kompletter Revert aller Änderungen
**Geänderte Datei:** `digivice/js/3d_scene.js` (39 Zeilen entfernt)
**Commit:** `d8eb77c` - "Revert: Entferne kaputte Door-Interaktion (JS Error)"

**Gelerntes:**
- `interactiveObjects` Array ist nur im Interior-Scope verfügbar
- Outdoor Building Detection funktioniert über `nearBuilding` System
- Keine Änderungen an `buildWindmill()` nötig - Detection läuft über `userData.buildingName` und `userData.buildingRadius`

---

## Legende

- ✅ = Erfolgreich implementiert
- ❌ = Fehlgeschlagen / Reverted
- 🔧 = In Arbeit
- 📝 = Dokumentation
- 🐛 = Bugfix
- ⚠️ = Wichtige Warnung

---

**Letzte Aktualisierung:** 2025-11-07 15:45
**Session:** claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
**Branch:** claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
