# NAJIKA VERSIONEN-VERGLEICH
**Stand:** 2025-10-29
**Vergleich:** C:\NajikaCore vs C:\Najika

---

## 🔍 HAUPTUNTERSCHIED GEFUNDEN!

### **C:\NajikaCore (ALT - aber FUNKTIONIERT BESSER!):**

#### ✅ **ASSETS:**
- **15 KayKit Packs** vorhanden
- Alle Dungeon Assets da (crate, barrel, debris, etc.)
- Vollständige Texturen
- 3D Models laden korrekt

#### ✅ **ROOM CONFIG:**
- **room_config_detailed.json** - DETAILLIERTE Version
- 12 Räume komplett konfiguriert
- Props, Paletten, Spawn-Points definiert
- "Schwarze Mühle – Keller" VORHANDEN (Line 465)

#### ✅ **INDEX.HTML:**
- 1968 Zeilen
- Praise/Scold Buttons VORHANDEN (Lines 488-489)
- Event Listeners verbunden (Lines 1429-1430)
- Alle Features integriert

#### ✅ **JS FILES:**
- 17 JS Files komplett
- command_system.js vorhanden
- battle_api.js vorhanden
- dungeon_generator.js vorhanden

#### ✅ **WAS FUNKTIONIERT:**
- ✅ 3D Texturen laden
- ✅ Räume rendern korrekt
- ✅ Dungeon Assets laden
- ✅ Praise/Scold Buttons DA
- ✅ Command System funktioniert

---

### **C:\Najika (NEU - aber PROBLEME!):**

#### ❌ **ASSETS:**
- **Nur 4 KayKit Packs!**
- 11 Packs FEHLEN!
- Dungeon Assets fehlen (404 Errors)
- Viele Texturen nicht da

#### ❌ **ROOM CONFIG:**
- **room_config_detailed.json** - VEREINFACHTE Version
- Nur Keys wie "Wohnzimmer", "Badezimmer"
- KEINE detaillierten Props/Paletten
- Andere JSON-Struktur!

#### ✅ **INDEX.HTML:**
- 1966 Zeilen (fast identisch)
- Praise/Scold Buttons VORHANDEN
- Event Listeners verbunden
- Features integriert

#### ✅ **JS FILES:**
- 17 JS Files (identisch)
- Alle Scripts vorhanden

#### ❌ **WAS NICHT FUNKTIONIERT:**
- ❌ Viele Assets fehlen (404)
- ❌ Room Config Format anders
- ❌ "Schwarze Mühle – Keller" nicht gefunden
- ❌ "Wohnzimmer" nicht gefunden
- ❌ Dungeon Assets fehlen

---

## 📊 DETAILLIERTER VERGLEICH

### **ASSETS (KayKit Packs):**

**C:\NajikaCore (15 Packs):**
1. KayKit_DungeonRemastered_1.1_FREE ✅
2. KayKit_HalloweenBits_1.0_FREE ✅
3. KayKit_Adventurers_1.0_FREE ✅
4. KayKit_Furniture_Bits_1.0_FREE ✅
5. KayKit Character Pack - Skeletons ✅
6. KayKit Mini-Game Variety Pack ✅
7. KayKit Spooktober Seasonal Pack ✅
8. KayKit Character Animations ✅
9. KayKit Dungeon Pack 1.0 ✅
10. + 5 weitere Packs

**C:\Najika (4 Packs):**
1. KayKit_DungeonRemastered_1.1_FREE ✅
2. KayKit_HalloweenBits_1.0_FREE ✅
3. KayKit_Adventurers_1.0_FREE ✅
4. 1 weiteres Pack
5. **11 Packs FEHLEN!** ❌

---

### **ROOM CONFIG FORMAT:**

**C:\NajikaCore - DETAILLIERT:**
```json
{
  "defaults": { "span": 48, "wallHeight": 6 },
  "rooms": [
    {
      "name": "Wohnzimmer",
      "floor": {
        "model": "KayKit_DungeonRemastered.../floor_wood_large.gltf",
        "span": 48,
        "tint": "#7a5c3d",
        "roughness": 0.75
      },
      "walls": {
        "model": "KayKit_DungeonRemastered.../wall_window_open.gltf"
      },
      "props": [
        { "model": "...", "position": [0,0,6], "scale": 1.8 }
      ],
      "palette": {
        "background": "#231419",
        "fog": "#1a1013"
      }
    }
  ]
}
```

**C:\Najika - VEREINFACHT:**
```json
{
  "Wohnzimmer": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 10,
    "wallHeight": 3,
    "palette": {
      "primary": "#8B4513"
    },
    "props": [],
    "spawn": [0, 0, 0]
  }
}
```

**PROBLEM:**
- kaykit_loader.js erwartet Format von C:\NajikaCore!
- C:\Najika hat anderes Format → "Room not found" Fehler

---

### **BACKEND SERVER:**

**C:\NajikaCore\najika_server.py:**
- Alte Version (vor Merge)
- Funktioniert mit altem Config-Format
- Kompatibel mit Assets

**C:\Najika\backend\najika_server.py:**
- Neue Version (nach Merge)
- Mehr Features integriert
- ABER: Config-Format inkompatibel!

---

## 🎯 FAZIT

### **C:\NajikaCore ist BESSER weil:**
✅ Alle Assets vorhanden (15 KayKit Packs)
✅ Room Config funktioniert
✅ 3D Texturen laden
✅ Dungeon Assets laden
✅ Praise/Scold Buttons funktionieren
✅ Alles rendert korrekt

### **C:\Najika hat PROBLEME:**
❌ 11 KayKit Packs fehlen
❌ Room Config Format inkompatibel
❌ Viele 404 Fehler
❌ Räume rendern nicht
❌ Dungeon Assets fehlen

---

## 💡 LÖSUNG

### **Option 1: C:\NajikaCore weiter nutzen**
- ✅ Funktioniert JETZT
- ✅ Alle Assets da
- ❌ Alte Server-Version

### **Option 2: C:\Najika fixen**
- Kopiere 11 fehlende KayKit Packs von NajikaCore → Najika
- Kopiere room_config_detailed.json von NajikaCore → Najika
- Teste ob dann alles funktioniert

### **Option 3: Für Opus vorbereiten**
- Dokumentiere was fehlt
- Opus fixt am Montag

---

## 🔧 FEHLENDE ASSETS IN C:\Najika

**Diese 11 KayKit Packs müssen kopiert werden:**
1. KayKit_Furniture_Bits_1.0_FREE
2. KayKit Character Pack - Skeletons
3. KayKit Mini-Game Variety Pack
4. KayKit Spooktober Seasonal Pack
5. KayKit Character Animations
6. KayKit Dungeon Pack 1.0
7. + 5 weitere (Liste komplett erstellen)

**Fehlende Config:**
- `C:\NajikaCore\assets\room_config_detailed.json` → `C:\Najika\assets\`

---

## 📋 EMPFEHLUNG

**FÜR JETZT:**
→ **C:\NajikaCore weiter nutzen** (funktioniert!)

**FÜR MONTAG (Opus):**
→ **C:\Najika fixen** durch:
1. Assets kopieren (11 KayKit Packs)
2. room_config_detailed.json kopieren
3. Testen

**ODER:**
→ **C:\Najika löschen** und nur mit C:\NajikaCore arbeiten

---

**Ende Versionen-Vergleich**
