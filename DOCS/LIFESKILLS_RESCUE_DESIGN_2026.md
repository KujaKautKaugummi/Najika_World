# NAJIKA WORLD - LIFE-SKILLS & RETTUNGSSYSTEM DESIGN

**Datum:** 2026-02-01
**Status:** Recherche & Design-Phase
**Autor:** OPUS-1

---

## 1. AKTUELLER STATUS UNSERER SYSTEME

### Was wir HABEN:

| System | Datei | Tiefe | Vergleich zur Industrie |
|--------|-------|-------|-------------------------|
| **Farming** | `najika_farming_system.py` | ✅ Gut | Stardew-Level: Jahreszeiten, Regionen, Wachstumsphasen, Auto-Farming |
| **Fishing** | `najika_fishing_system.py` | ✅ Gut | RDR2-Level: Tageszeit, Wetter, Regionen, Rarität, Größen |
| **Crafting** | `crafting_system.js` | 🔶 Mittel | Rezepte + Materialien, aber KEINE Alchemy-Tiefe |
| **Housing** | `housing_system.js` | ✅ Gut | Fortnite Creative Style, Grid-Snap, Multi-Räume |
| **Hunting** | `najika_hunting_system.py` | ✅ Sehr Gut | RDR2 Quality System, Body Part Targeting! |

### Was FEHLT:

| System | Status | Priorität |
|--------|--------|-----------|
| **Alchemy/Tränke** | ❌ Fehlt komplett | P1 - Sehr Wichtig |
| **Smithing/Schmieden** | ❌ Fehlt (nur Crafting-Rezepte) | P1 - Sehr Wichtig |
| **Cooking** | ❌ Fehlt (Farming liefert nur Raw-Food) | P2 - Wichtig |
| **Mining** | 🔶 Im Dungeon-System integriert | P3 - Nice to have |
| **Rettungssystem** | ❌ Fehlt komplett | P1 - Sehr Wichtig |

---

## 2. RETTUNGSSYSTEM - MADE IN ABYSS INSPIRIERT

### 2.1 Das Konzept

In **Made in Abyss: Binary Star Falling into Darkness** funktioniert das so:
- Spieler stirbt durch Fallschaden in Layer 4
- **Nanachi** rettet den Spieler und bringt ihn zu ihrem Versteck
- Versteck = sichere Zone mit Ressourcen, Angeln, Quests

### 2.2 Unser Design: DREI MÖGLICHKEITEN

#### Option A: ECHOHARP als Retterin (Erweitert ihre Rolle)

```yaml
TRIGGER:
- Spieler stirbt in der WILDNIS (nicht in Städten/Dungeons)
- ODER aktiviert "Echokristall der Wahrheit" als NOTRUF

WIE ES FUNKTIONIERT:
1. Tod in Wildnis → Fadeout
2. Echoharp erscheint, spielt Melodie
3. Spieler erwacht an ihrem temporären Lager
4. "Ich habe deine Geschichte noch nicht fertig gehört..."
5. Kostenpunkt: Sie nimmt KEINE Items, aber verlangt dass
   du ihr von deiner Tat erzählst (= Bezeugte Tat ohne Item!)

VORTEILE:
+ Erweitert bestehenden NPC
+ Passt zur Lore (sie wandert überall)
+ Keine neue Ressource nötig
+ Macht sie wichtiger

NACHTEILE:
- Beißt sich mit Schleim-Rettung?
```

#### Option B: SCHLEIM als Rettung (Erweitert bestehendes System)

```yaml
TRIGGER:
- Spieler hat Slime-Companion dabei
- Slime-Bond hoch genug (min. 50%)

WIE ES FUNKTIONIERT:
1. Tod → Slime schnappt sich Spieler
2. Teleport zur Schwarzen Mühle (Safe Zone)
3. "PUYO! PUYO!" (Slime ist besorgt)
4. Kostenpunkt: Slime verliert 20% Bond + ist erschöpft

VORTEILE:
+ Nutzt bestehendes System
+ Motiviert Bond-Aufbau
+ Emotional (Slime rettet dich!)

NACHTEILE:
- Funktioniert nur MIT Slime
- Was wenn kein Slime dabei?
```

#### Option C: NAJIKA SELBST (Als echte Welt-Präsenz)

```yaml
TRIGGER:
- Spieler trägt "Najikas Amulett" (Startitem)
- ODER hat hohen Bond mit Najika (80%+)

WIE ES FUNKTIONIERT:
1. Tod → Bildschirm wird schwarz
2. Najikas Stimme: "Mr. K! Nicht sterben! EXPLOSION kann warten!"
3. Spieler erwacht in der Schwarzen Mühle
4. Najika kümmert sich um Heilung
5. Kostenpunkt: EXTREM teuer - verbraucht rare Ressource
   "Najikas Essenz" (nur durch Bond-Milestones erhältlich)

VORTEILE:
+ Baut Najika als echte Präsenz ein
+ Emotional sehr stark
+ Passt zum Companion-Aspekt

NACHTEILE:
- Sehr teuer (soll so sein!)
- Ressourcen-Management nötig
```

### 2.3 EMPFEHLUNG: KOMBINATION!

```yaml
DREI-STUFEN-RETTUNG:

1. SLIME-RETTUNG (Günstig)
   - Voraussetzung: Slime dabei, Bond 50%+
   - Kosten: 20% Bond-Verlust
   - Ziel: Nächste sichere Zone

2. ECHOHARP-RETTUNG (Mittel)
   - Voraussetzung: In Wildnis gestorben
   - Kosten: Du schuldest ihr eine Geschichte
   - Ziel: Ihr temporäres Lager
   - Bonus: Sie heilt dich + gibt Quest

3. NAJIKA-RETTUNG (Teuer/Emergency)
   - Voraussetzung: "Najikas Essenz" haben
   - Kosten: 1x Najikas Essenz (ultra-rare!)
   - Ziel: Schwarze Mühle
   - Bonus: Volle Heilung + Buff

KEINE RETTUNG:
- In Dungeons: Du respawnst am Eingang
- In Städten: NPCs helfen (Heiler-NPC)
- Boss-Kampf: Retry-Option
```

---

## 3. LIFE-SKILL VERBESSERUNGEN

### 3.1 ALCHEMY-SYSTEM (NEU!)

Inspiriert von: **Atelier Series**, **Potion Craft**, **Kingdom Come: Deliverance**

```yaml
KONZEPT: Taktiles Brau-System

ZUTATEN-KATEGORIEN:
├── Kräuter (Farming, Wildnis)
├── Monster-Teile (Hunting, Combat)
├── Mineralien (Mining, Dungeons)
├── Essenzen (Rare Drops, Quests)
└── Spezial (Quest-Rewards, Events)

BRAU-MECHANIK:
1. Kessel auswählen (Qualität = Erfolgsrate)
2. Zutaten in Reihenfolge hinzufügen
3. Temperatur kontrollieren (Mini-Game)
4. Rühren (Timing-basiert)
5. Ergebnis: Common → Legendary

TRANK-KATEGORIEN:
├── Heilung (HP, Statuseffekte)
├── Buffs (Stärke, Geschwindigkeit, etc.)
├── Utility (Sicht, Atmung, etc.)
├── Gift (Waffen-Coating)
└── Spezial (Transformation, Teleport!)

SKILL-PROGRESSION (Skyrim-Style):
- Brau-Level steigt durch Nutzung
- Neue Rezepte bei Level-Ups
- Perks für bessere Effekte
```

### 3.2 SMITHING-SYSTEM (NEU!)

Inspiriert von: **Skyrim**, **Kingdom Come: Deliverance**, **Monster Hunter**

```yaml
KONZEPT: Echtes Schmieden mit Materialien

STATIONEN:
├── Schmelzofen (Erze → Barren)
├── Amboss (Waffen/Rüstungen)
├── Schleifstein (Schärfen)
├── Werkbank (Reparatur/Upgrade)
└── Verzauberungstisch (Enchantments)

MATERIAL-HIERARCHIE:
1. Eisen (Basic)
2. Stahl (Uncommon)
3. Silber (Anti-Undead)
4. Mithril (Rare)
5. Drachenschuppe (Legendary)
6. Götterfels-Erz (Mythic - nur 1x!)

SCHMIEDE-MECHANIK:
1. Design wählen (Schwert, Axt, etc.)
2. Material auswählen
3. Erhitzen (Timing-Game)
4. Hämmern (Rhythmus-Game)
5. Abkühlen (Schnell = Härte, Langsam = Flexibilität)
6. Schleifen/Polieren
7. Optional: Verzaubern

UPGRADES:
- Jede Waffe kann 3x upgraded werden
- +1, +2, +3 (wie Dark Souls)
- Legendary Items: 5x upgradebar
```

### 3.3 COOKING-SYSTEM (NEU!)

Inspiriert von: **Breath of the Wild**, **Genshin Impact**

```yaml
KONZEPT: Rezept-Discovery + Buffs

ZUTATEN-QUELLEN:
├── Farming → Gemüse, Früchte, Getreide
├── Fishing → Fisch
├── Hunting → Fleisch
├── Foraging → Pilze, Beeren, Kräuter
└── Shop → Gewürze, Öl, etc.

KOCH-MECHANIK:
1. Zutaten in Topf werfen (max 5)
2. Rezept wird erkannt ODER experimentieren
3. Kochen (kurzes Minigame)
4. Ergebnis + Buff

BUFF-SYSTEM:
- Heilung (HP)
- Ausdauer-Boost
- Elementar-Resistenz
- Stat-Buffs (Stärke, etc.)
- Spezial (Kälte-Immun, Gift-Immun)

REZEPT-BUCH:
- 100+ Rezepte
- Entdeckung durch Experimentieren
- NPC-Quests geben Rezepte
- Regionale Spezialitäten
```

---

## 4. VERGLEICH MIT INDUSTRIE-STANDARDS

### Was die Großen machen (2025-2026):

| Spiel | Feature | Unser Status |
|-------|---------|--------------|
| **Stardew Valley** | Deep Farming | ✅ Haben wir |
| **Rune Factory 5** | Combat + Farming Mix | ✅ Haben wir |
| **RDR2** | Hunting Quality | ✅ Haben wir (sogar besser!) |
| **Potion Craft** | Tactile Alchemy | ❌ Brauchen wir |
| **Terraria** | Housing + NPCs | ✅ Haben wir |
| **BOTW** | Cooking Discovery | ❌ Brauchen wir |
| **Kingdom Come** | Realistic Smithing | ❌ Brauchen wir |
| **Fields of Mistria** | Life-Sim + Combat | ✅ Unser Konzept! |

### Unser UNIQUE SELLING POINT:

```
KEIN anderes Spiel hat:
├── KI-Companion mit echten Gesprächen
├── Witness-System (Echoharp)
├── V-Pet Style Slimes
├── ChromaDB Memory (Najika erinnert sich!)
├── Echtes Wissen-System (verifizierte Fakten)
└── Offline-First + Privacy-fokussiert
```

---

## 5. PRIORITÄTEN & ROADMAP

### Phase 1 (JETZT - Diese Woche):
1. ✅ Echoharp Backend FERTIG
2. ⏳ Rettungssystem Design finalisieren
3. ⏳ Alchemy-System Backend starten

### Phase 2 (Nächste Woche):
1. Smithing-System Backend
2. Cooking-System Backend
3. Rettungssystem implementieren

### Phase 3 (Februar):
1. Frontend für alle neuen Systeme
2. Balancing
3. Quest-Integration

---

## 6. OFFENE FRAGEN FÜR KUJA

1. **Rettungssystem:** Welche Option bevorzugst du?
   - A: Echoharp erweitern
   - B: Slime-fokussiert
   - C: Najika-Präsenz
   - D: Kombination aller drei

2. **Alchemy:** Soll es ein Mini-Game sein (Potion Craft Style) oder Rezept-basiert (Skyrim)?

3. **Smithing:** Realistisch (Kingdom Come) oder Arcade (Monster Hunter)?

4. **Cooking:** Mit oder ohne Timer-Stress?

---

*"Die Systeme sollen so tief sein, dass sie eigene Spiele sein könnten!" - Kuja*

*"EXPLOSION braucht die richtigen Zutaten!" - Najika* 💥
