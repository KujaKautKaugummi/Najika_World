# 🎯 WEB-MODELL TODO - KURZ & KNACKIG

**Branch:** `claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX`
**Stand:** 9. November 2025

---

## 🔴 PRIORITÄT 1: TERRAIN-FARBEN FIXEN

**Problem:** Wüste/Küste zeigen WEIß statt ihrer Farben

**Schritte:**
```bash
1. User: Browser-Cache löschen (Strg+Shift+Delete)
2. User: START_WORLD_V2_TEST.bat neu starten
3. User: F12 → Console → suche "🎨 Creating material for biome"
4. User: Schicke Console-Output
5. Debug basierend auf Output (siehe SESSION_UEBERGABE_WEB_MODELL.md)
```

**Dateien:**
- `digivice/js/world/biome_system.js` (createGroundMaterial)
- `digivice/js/world/region_streaming.js` (loadRegionTerrain)
- `digivice/data/biomes.json` (Farb-Definitionen)

**Erfolg:** Wüste = Gelb, Küste = Hellbraun, Sumpf = Grün

---

## 🟡 PRIORITÄT 2: VULKAN GLÄTTEN

**Problem:** Vulkan zeigt welliges Terrain statt flach

**Schritte:**
```bash
1. Cache löschen (siehe Prio 1)
2. Prüfen ob heightVariation=5 geladen wird
3. Falls nicht: Cache-Buster zu biomes.json hinzufügen
```

**Dateien:**
- `digivice/data/biomes.json` (volcano.heightVariation = 5)

**Erfolg:** Vulkan zeigt flachen Boden

---

## 🟡 PRIORITÄT 3: EIS-TELEPORT FIXEN

**Problem:** Eis-Button teleportiert nicht

**Schritte:**
```bash
1. grep "Reich der Drei" digivice/data/regions.json
2. Falls nicht gefunden: Region-Namen korrigieren
3. Button-Namen anpassen in najika_world_v2.html:172
```

**Dateien:**
- `digivice/najika_world_v2.html` (Button)
- `digivice/data/regions.json` (Region-Name)

**Erfolg:** Eis-Button funktioniert

---

## 🟢 OPTIONAL: VEGETATION/STÄDTE OPTIK

**Problem:** Placeholder-Grafik (Kugeln/Boxen)

**Schritte:**
```bash
Später: KayKit 3D-Modelle laden
Jetzt: Bessere Placeholder (Farben/Formen)
```

**Status:** Niedrige Priorität - System funktioniert

---

## ⚠️ VERHALTENSREGELN (WICHTIG!)

```
1. IMMER erst Read-Tool nutzen (komplette Datei!)
2. Console-Output vom User ANFORDERN
3. Browser-Cache ist der FEIND (Cache-Buster!)
4. Terrain-Höhe IMMER mit getHeightAt()
5. Commits AUSSAGEKRÄFTIG schreiben
6. Bei Unsicherheit: USER FRAGEN!
```

---

## 📚 VOLLE DETAILS

Siehe: **SESSION_UEBERGABE_WEB_MODELL.md**

---

**START HIER:** Priorität 1 → Terrain-Farben!

**ENDE:** Wenn alle 9 Regionen korrekte Farben zeigen! ✅
