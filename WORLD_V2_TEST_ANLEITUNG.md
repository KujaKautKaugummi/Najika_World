# 🌍 NAJIKA WORLD V2 - TEST ANLEITUNG

**Erstellt:** 2025-11-08
**Status:** Bereit zum Testen
**Port:** 8001 (parallel zu Hauptserver auf 8000)

---

## 🎯 WAS IST DAS?

World Manager V2 ist das neue 8-Regionen-System mit:
- ✅ 8 Regionen (Wüste, Wald, Küste, Hochland, Sumpf, Eis, Vulkan, Höhlen)
- ✅ Götterfels (Zentrum)
- ✅ 5 Städte (Handelsfestung, Dampf-Hain, Salzige Bucht, Runenheim, Funken-Siedlung)
- ✅ World Manager System (Streaming, LOD, Biomes)
- ✅ 9600x9600 Map (statt 900x900)

**WICHTIG:** Dies ist ein **separater Test** - deine laufende Najika auf Port 8000 wird NICHT gestört!

---

## 🚀 SCHNELLSTART

### Windows:
```batch
START_WORLD_V2_TEST.bat
```

### Linux/Mac:
```bash
./START_WORLD_V2_TEST.sh
```

### Dann im Browser öffnen:
```
http://localhost:8001/najika_world_v2.html
```

---

## 🎮 STEUERUNG

### Bewegung:
- **W** - Vorwärts
- **S** - Rückwärts
- **A** - Links
- **D** - Rechts
- **Shift** - Rennen (doppelte Geschwindigkeit)

### Kamera:
- **Maus bewegen** - Kamera drehen
- **Mausrad** - Zoom in/out

### Teleport (Buttons unten):
- 🏜️ **Handelsfestung** - Wüsten-Stadt (PvP Arena)
- 🌲 **Dampf-Hain** - Wald-Stadt (Onsen)
- 🌊 **Salzige Bucht** - Küsten-Stadt (Hafen)
- ⚡ **Runenheim** - Hochland-Stadt (Magie-Akademie)
- 🌋 **Funken-Siedlung** - Vulkan-Stadt (Schmiede)
- ⛰️ **Berg** - Götterfels (Zentrum)

### Debug:
- 📊 **Stats Button** - Zeigt Statistiken in Browser-Konsole (F12)

---

## 🔍 WAS TESTEN?

### 1. **Lädt die Seite?**
- ✅ Loading Screen erscheint
- ✅ Progress Bar läuft bis 100%
- ✅ Loading Screen verschwindet

### 2. **WASD-Bewegung funktioniert?**
- ✅ Charakter (grüne Kapsel) bewegt sich
- ✅ Kamera folgt dem Charakter
- ✅ Shift macht schneller
- ✅ Position im UI wird aktualisiert

### 3. **Teleport funktioniert?**
- ✅ Click auf Stadt-Button → Charakter springt zur Stadt
- ✅ Region-Name im UI ändert sich
- ✅ Position im UI ändert sich

### 4. **Konsole zeigt keine Fehler?**
- ✅ Drücke F12 → Konsole Tab
- ✅ Prüfe auf rote Fehler
- ❌ Falls Fehler: Screenshot machen!

### 5. **Performance OK?**
- ✅ FPS im UI sollte ~60 sein
- ✅ Keine Ruckler beim Bewegen
- ✅ Smooth Camera-Bewegung

---

## 📊 BEKANNTE EINSCHRÄNKUNGEN

**Aktuell NICHT implementiert (ist normal!):**

### Assets:
- ❌ Echte 3D-Modelle werden noch nicht geladen
- ❌ Terrain ist flach (kein Perlin Noise)
- ❌ Vegetation fehlt noch
- ❌ Städte sind Placeholder

### Biomes:
- ❌ Fog/Lighting ändert sich noch nicht
- ❌ Biome-Farben fehlen noch
- ❌ Wetter-Effekte fehlen

**WARUM?**
Weil die Assets lokal bei dir liegen und noch nicht ins System geladen wurden. Das ist der nächste Schritt!

---

## ✅ ERWARTETES VERHALTEN

**Was DU sehen solltest:**

1. **Loading Screen:**
   ```
   🌍 Lade Najika World V2...
   World Manager System
   [Progress Bar: 0% → 100%]
   ```

2. **Nach Laden:**
   - Grüne Kapsel (Charakter) in der Mitte
   - Flacher grauer/grüner Boden
   - Blauer Himmel
   - UI oben links zeigt:
     ```
     Position: 4800, 4800
     Region: Götterfels
     Biome: mountain
     FPS: 60
     ```

3. **Nach Teleport (z.B. Handelsfestung):**
   - Position ändert sich zu ~8400, 8200
   - Region ändert sich zu "Heiße Dünen"
   - Biome ändert sich zu "desert"

4. **Konsole (F12) zeigt:**
   ```
   ✅ Najika World V2 loaded!
   🌍 World Manager initialized
   [Keine roten Fehler!]
   ```

---

## 🐛 FEHLERSUCHE

### Problem: "Failed to load world data"
**Lösung:**
```bash
# Prüfe ob Dateien existieren:
ls digivice/data/regions.json
ls digivice/data/biomes.json
ls digivice/data/cities.json

# Falls fehlt: Nochmal kopieren
cp entwicklung/data/*.json digivice/data/
```

### Problem: "Cannot find module 'world_manager.js'"
**Lösung:**
```bash
# Prüfe ob Module existieren:
ls digivice/js/world/world_manager.js

# Falls fehlt: Nochmal kopieren
cp entwicklung/world/*.js digivice/js/world/
```

### Problem: Server startet nicht auf Port 8001
**Lösung:**
```bash
# Prüfe ob Port schon belegt:
netstat -ano | findstr :8001    # Windows
lsof -i :8001                   # Linux/Mac

# Falls belegt: Anderen Port nutzen
cd digivice
python -m http.server 8002
# Dann: http://localhost:8002/najika_world_v2.html
```

### Problem: FPS ist sehr niedrig (<30)
**Normal!** World Manager lädt viele Systeme. Performance wird optimiert wenn Assets geladen sind.

### Problem: Charakter fällt durch Boden
**Das sollte NICHT passieren!** Screenshot + Konsolen-Fehler schicken.

---

## 📝 TEST-PROTOKOLL (Ausfüllen!)

```
Datum: __________
Tester: __________

[ ] Loading Screen erscheint
[ ] Progress Bar läuft durch
[ ] Charakter sichtbar
[ ] WASD funktioniert
[ ] Teleport funktioniert
[ ] FPS: _____ (sollte ~60 sein)
[ ] Keine Konsolen-Fehler

Probleme:
- ________________________________
- ________________________________
- ________________________________

Screenshots:
- ________________________________
```

---

## 🔄 PARALLEL ZU HAUPTSERVER

**Port 8000 (Hauptserver - najika_server.py):**
- ✅ Digivice (alte Version)
- ✅ Najika KI/Chat
- ✅ Training System
- ✅ Backend APIs
- **BLEIBT UNBERÜHRT!**

**Port 8001 (Test-Server - World V2):**
- ✅ Nur World Manager V2
- ✅ Nur Frontend-Test
- ✅ Kein Backend nötig
- **NUR ZUM TESTEN!**

**Du kannst beide parallel laufen lassen!**

---

## 🎯 NÄCHSTE SCHRITTE

Nach erfolgreichem Test:

1. **Phase 1: Assets laden** ✅ NÄCHSTES
   - Quaternius Pack integrieren
   - KayKit Assets laden
   - Echte 3D-Modelle anzeigen

2. **Phase 2: Terrain generieren**
   - Perlin Noise aktivieren
   - Höhen-Variationen
   - Biome-Texturen

3. **Phase 3: Vegetation**
   - Bäume platzieren
   - Gras/Büsche spawnen
   - Regionen-spezifisch

4. **Phase 4: Städte bauen**
   - KayKit Medieval Assets
   - 5 Städte konstruieren
   - NPCs platzieren

5. **Phase 5: Integration**
   - Merge mit Hauptserver
   - Najika KI verbinden
   - Final Testing

---

## 💡 TIPPS

**Performance:**
- Falls laggy: Reduziere Browser-Zoom (Ctrl+0)
- Falls weiterhin laggy: Andere Programme schließen
- FPS im UI beobachten

**Testing:**
- Erst alle Buttons testen BEVOR du bugst
- Screenshots von Problemen machen (F12 Konsole!)
- Position beim Bug notieren

**Debug:**
- F12 → Console Tab ist dein Freund
- Rot = Fehler (wichtig!)
- Gelb = Warnung (OK)
- Blau/Grau = Info (normal)

---

## 📞 SUPPORT

Bei Problemen:
1. Prüfe Konsole (F12) auf Fehler
2. Mache Screenshot
3. Notiere Position + Region
4. Sag mir Bescheid!

---

**Stand:** 2025-11-08
**Version:** V2.0
**Status:** ✅ Bereit zum Testen!
