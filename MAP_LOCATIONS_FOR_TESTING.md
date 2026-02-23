# 🗺️ NAJIKA WORLD - MAP LOCATIONS FOR TESTING
**Created:** 2025-11-05
**Purpose:** Document locations to place on Open Mini World (2400×2400)

---

## 🏠 CENTRAL HUB

### **Black Windmill Village (Schwarze Windmühle)**
**Type:** Safe Zone (Najika's Home)
**Status:** Already implemented
**Features:**
- Erdgeschoss: Werkbank, Altar, Quest-Board
- 2. Stock: Trainingsraum, Archiv, Owner-Panel
- Katakomben: Rätsel, Craft-Altäre, MK-ähnliche Krypta
- Umgebung: Dorf mit NPCs (meiden die Mühle)
- 100% SAFE ZONE - no danger, no PvP

**Implementation:** Currently has 12 interior rooms

---

## 🌍 DIE 8 REGIONEN (DISCOVERED FROM DOCS)

These 8 regions are referenced in game design docs. Each has:
- Unique slime color
- Environmental risks
- Special events
- Themed biome

### 1. **Heiße Dünen**
**Biome:** Desert (Wüste)
**Stadt:** Handelsfestung (Hauptstadt!)
**Risiken:** Durst, Sandsturm
**Events:** Karawanenhandel, versandete Ruinen
**Besonderheit:** Seltene Alchemie-Zutaten in Oasen

### 2. **Samtmoos-Tiefwald**
**Biome:** Forest (Wald)
**Stadt:** Dampf-Hain (japanisch-mystisch, Onsen, Druiden)
**Risiken:** Verirren, Parasiten
**Events:** Druidenrätsel, Kräutersuche
**Besonderheit:** Versteckte Pfade, sprechende Bäume

### 3. **Salzwind-Küste**
**Biome:** Coastal (Küste)
**Stadt:** Salzige Bucht (Piraten-Hafen, Leuchtturm)
**Risiken:** Sturmflut, Ertrinken
**Events:** Schiffwracks, Gezeitenkisten, Angeln
**Besonderheit:** Unterwasser-Höhlen

### 4. **Blitzebene**
**Biome:** Highland (Hochland)
**Stadt:** Runenheim (Magie-Akademie)
**Risiken:** Blitzschlag, Sturm
**Events:** Wetter-Altäre, Totems
**Besonderheit:** Elementar-Ladungen für Experimente

### 5. **Grünschlamm-Sumpf**
**Biome:** Swamp/Marsh (Sumpf)
**Stadt:** KEINE (Hexen-Gebiet!)
**Risiken:** Krankheit, Miasma
**Events:** Hexenkreise, Moor-Bosse
**Besonderheit:** Nekromantie-Forschung

### 6. **Magmaströme**
**Biome:** Volcano (Vulkan)
**Stadt:** Funken-Siedlung (Schmiede, vulkanisch-industriell)
**Risiken:** Überhitzung, Asche
**Events:** Lava-Kanäle, Erzadern
**Besonderheit:** Schmiedekunst auf höchstem Niveau

### 7. **Tiefenhöhlen**
**Biome:** Cave (Höhlen)
**Stadt:** KEINE (Goblin-Gebiet!)
**Risiken:** Einstürze, Dunkelheit
**Events:** Erzadern, unterirdische Seen
**Besonderheit:** Seltene Erze, Goblin-Lager

### 8. **Reich der Drei**
**Biome:** Tundra/Ice (Eis/Undead)
**Stadt:** KEINE (Untote/Nekromanten-Gebiet!)
**Risiken:** Erfrierung, Untote
**Events:** Nekromanten-Rituale, Geister
**Besonderheit:** Härteste Herausforderungen, Endgame-Gebiet

---

## ✅ 5 STÄDTE (DEFINIERT - aus cities.json)

| Stadt | Region | Stil |
|-------|--------|------|
| **Handelsfestung** (Hauptstadt) | Heiße Dünen | Western, PvP-Arena, Spieler-Shops |
| **Dampf-Hain** | Samtmoos-Tiefwald | Japanisch-mystisch, Onsen, Druiden |
| **Salzige Bucht** | Salzwind-Küste | Piraten-Küste, Hafen, Leuchtturm |
| **Runenheim** | Blitzebene | Magisches Hochland, Magie-Akademie |
| **Funken-Siedlung** | Magmaströme | Vulkanisch-industriell, Schmiede |

**3 Regionen OHNE Stadt:** Grünschlamm-Sumpf (Hexen), Tiefenhöhlen (Goblins), Reich der Drei (Untote)

---

### **SPEZIALORTE**
- **Götterfels** = Zentraler Berg (wie Mount Everest, in ALLEN 8 Regionen sichtbar/erreichbar)
  - Schwarze Mühle (Safe Zone, Fast-Travel Hub)
  - Schmelz-Welt (Lava-Interior, Dungeon)
  - Turm der 100 Prüfungen (Mega-Dungeon)

---

## 🎯 NEW STRATEGY (2025-11-05)

### **SAFE ZONE = OPEN MINI WORLD**
- Najika's living space (2400×2400 map) = 100% SAFE
- NO danger on the map!
- Non-combat mechanics tested here:
  - Oregon Trail Events
  - NPC interactions
  - Crafting/Gathering
  - Exploration

### **DANGER ONLY IN:**
✅ **3 Dungeons** (replace old Keller concept)
- Dungeon 1: MEGA-DUNGEON
- Dungeon 2: MEGA-DUNGEON
- Dungeon 3: NORMAL-DUNGEON

✅ **Kampfarena** (Combat Arena)

---

## 🚧 NEXT STEPS

1. **Placement Strategy:** Positionen aus regions.json + cities.json auf 2400×2400 Mini-Map mappen
2. **Implementation:** Als Markers/Waypoints umsetzen
3. **Testing:** Non-Combat Mechaniken testen

---

**Status:** Städte + Regionen DEFINIERT (siehe regions.json + cities.json)
**File:** MAP_LOCATIONS_FOR_TESTING.md
