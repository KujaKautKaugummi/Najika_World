# 📋 Najika World - Projekt Changelog

**Zweck:** Chronologische Dokumentation aller Änderungen mit Zeitnachweis
**Regel:** Dieses Dokument wird NUR ERGÄNZT, niemals korrigiert oder neu geschrieben

---

## 2025-11-07 - Session: claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX

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

**Letzte Aktualisierung:** 2025-11-07 10:52
**Session:** claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
**Branch:** claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
