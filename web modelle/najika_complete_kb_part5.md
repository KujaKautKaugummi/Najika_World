# 🌟 NAJIKA WORLD - COMPLETE KNOWLEDGE BASE
## TEIL 5/10: OPEN WORLD, COMBAT & SKILLS

**Erstellt:** 2025-01-01  
**Teil:** 5 von 10  
**Thema:** Weltstruktur, Kampfsystem, Skill-Progression

---

# 🗺️ OPEN WORLD STRUKTUR

## 1. MAP-GRÖSSE

### Dimensionen
```yaml
Gesamt: 9.6km × 9.6km
Units: 9600 × 9600 (1 unit = 1 meter)
Fläche: 92.16 km²
Vergleich: ~3× Fortnite Battle Royale Map

Movement Bounds: ±4800 (von Zentrum)
Zentrum: (0, 0) = Schwarze Mühle
```

### Vergleiche
```yaml
Najika World: 92.16 km²
Fortnite BR: ~30 km²
Skyrim: ~37 km²
GTA V: ~127 km²

→ Najika = Mittelgroß, aber dicht gepackt!
```

---

## 2. DIE 9 REGIONEN (3×3 GRID)

### Grid-Layout
```yaml
Je Region: 3200m × 3200m (10.24 km² pro Region)

Layout:
  ┌─────────┬─────────┬─────────┐
  │   Ice   │ Highland│  Desert │ (Nord)
  ├─────────┼─────────┼─────────┤
  │  Swamp  │Mountain │  Coast  │ (Mitte)
  │         │(Mühle)⭐│         │
  ├─────────┼─────────┼─────────┤
  │  Caves  │ Forest  │ Volcano │ (Süd)
  └─────────┴─────────┴─────────┘

Koordinaten (Zentrum jeder Region):
  Ice:      (-3200, 3200)
  Highland: (0, 3200)
  Desert:   (3200, 3200)
  Swamp:    (-3200, 0)
  Mountain: (0, 0) ⭐ SCHWARZE MÜHLE
  Coast:    (3200, 0)
  Caves:    (-3200, -3200)
  Forest:   (0, -3200)
  Volcano:  (3200, -3200)
```

---

## 3. REGIONEN IM DETAIL

### Ice Region (Nord-West)
```yaml
Biome: Schneelandschaft, Gletscher
Temperatur: -20°C bis -5°C
Schwierigkeit: Mittel (Levels 15-30)

Features:
  - Ewiger Winter
  - Schnee-Effekte
  - Rutschige Oberflächen
  - Eishöhlen

Monster:
  - Frost-Wölfe
  - Eis-Golems
  - Yetis
  - Frost-Drache (Boss)

Resources:
  - Eis-Kristalle
  - Schnee-Pilze
  - Gefrorene Fische
```

### Highland Region (Nord)
```yaml
Biome: Hochland, Berge, Wiesen
Temperatur: 5°C bis 15°C
Schwierigkeit: Leicht-Mittel (Levels 5-20)

Features:
  - Hügelige Landschaft
  - Klares Wetter
  - Weite Sicht
  - Windmühlen

Monster:
  - Wilde Hasen
  - Greife
  - Bergziegen
  - Highland-Wächter (Boss)

Resources:
  - Heilkräuter
  - Wildblumen
  - Bergkristalle
```

### Desert Region (Nord-Ost)
```yaml
Biome: Wüste, Sanddünen, Oasen
Temperatur: 30°C bis 45°C
Schwierigkeit: Mittel-Hoch (Levels 25-40)

Features:
  - Sandstürme
  - Hitzewellen (Damage over Time!)
  - Versteckte Oasen
  - Alte Ruinen

Monster:
  - Sand-Skorpione
  - Banditen
  - Sand-Würmer
  - Wüsten-Pharao (Boss)

Resources:
  - Kakteen
  - Goldadern
  - Alte Artefakte
```

### Swamp Region (West)
```yaml
Biome: Sumpf, Moore, Nebel
Temperatur: 10°C bis 20°C
Schwierigkeit: Mittel (Levels 20-35)

Features:
  - Dichter Nebel
  - Giftige Gewässer
  - Schlechte Sicht
  - Morast (Slow-Effekt!)

Monster:
  - Gift-Frösche
  - Sumpf-Zombies
  - Riesenschlangen
  - Sumpf-Hexe (Boss)

Resources:
  - Gift-Pilze
  - Sumpf-Kräuter
  - Schlangen-Haut
```

### Mountain Region (Zentrum) ⭐
```yaml
Biome: Berge, Götterfels, Wiesen
Temperatur: 10°C bis 20°C
Schwierigkeit: Variabel (Safe Zone + Endgame)

Features:
  - SCHWARZE MÜHLE (Hub!)
  - Götterfels (Endgame-Dungeon!)
  - Weite Wiesen
  - Klare Luft

Monster:
  - Starter-Zone: Level 1-10
  - Götterfels: Level 50+ (Endgame!)

Resources:
  - Bergkräuter
  - Kristalle
  - Metall-Erze
```

### Coast Region (Ost)
```yaml
Biome: Küste, Strand, Meer
Temperatur: 15°C bis 25°C
Schwierigkeit: Leicht-Mittel (Levels 10-25)

Features:
  - Strände
  - Klippen
  - Schiffswracks
  - Angel-Spots (beste!)

Monster:
  - Krabben
  - Piraten
  - Meeres-Untote
  - Seeschlange (Boss)

Resources:
  - Muscheln
  - Fische
  - Perlen
  - Schiffs-Teile
```

### Caves Region (Süd-West)
```yaml
Biome: Höhlen, Untergrund, Dunkelheit
Temperatur: 5°C bis 15°C
Schwierigkeit: Hoch (Levels 30-45)

Features:
  - Komplexes Höhlensystem
  - Dunkelheit (Fackel nötig!)
  - Enge Gänge
  - Versteckte Schätze

Monster:
  - Fledermäuse
  - Höhlen-Spinnen
  - Trolle
  - Drachen-Wurm (Boss)

Resources:
  - Erze (Gold, Silber, Eisen)
  - Edelsteine
  - Pilze
```

### Forest Region (Süd)
```yaml
Biome: Wald, Dschungel, Lichtungen
Temperatur: 15°C bis 25°C
Schwierigkeit: Leicht (Levels 1-15)

Features:
  - Dichter Wald
  - Lichtungen
  - Bäche
  - Alte Bäume

Monster:
  - Wölfe
  - Bären
  - Waldfeen (neutral/feindlich)
  - Wald-König (Boss)

Resources:
  - Holz
  - Beeren
  - Kräuter
  - Honig
```

### Volcano Region (Süd-Ost)
```yaml
Biome: Vulkan, Lava, Aschefeld
Temperatur: 40°C bis 60°C
Schwierigkeit: Sehr Hoch (Levels 40-50+)

Features:
  - Aktiver Vulkan
  - Lava-Flüsse (Instant Death!)
  - Ascheregen
  - Hitzeschaden

Monster:
  - Feuer-Elementare
  - Lava-Golems
  - Magma-Drache
  - Vulkan-Gott (Boss)

Resources:
  - Obsidian
  - Lava-Kristalle
  - Feuer-Erze
```

---

## 4. DIE 5 STÄDTE

### 1. Akatsuki (Akademie-Stadt)
```yaml
Region: Highland
Typ: Starter-Stadt
Population: ~5.000

Features:
  - Akademie (Tutorial!)
  - Anfänger-Quests
  - Basic Shops
  - Inn (Respawn-Point)

NPCs:
  - Lehrer (Quest-Geber)
  - Händler (Basic Items)
  - Trainer (Skill-Training)
```

### 2. Haven (Händler-Hub)
```yaml
Region: Coast
Typ: Handels-Zentrum
Population: ~10.000

Features:
  - Großer Markt
  - Auktionshaus
  - Bank
  - Schmiede

NPCs:
  - Händler (alle Items!)
  - Auktionator
  - Banker
```

### 3. Ironforge (Schmiede-Stadt)
```yaml
Region: Mountain
Typ: Handwerks-Zentrum
Population: ~3.000

Features:
  - Master-Schmiede
  - Rüstungsmeister
  - Enchanter
  - Mining-Guild

NPCs:
  - Schmied (Custom Weapons!)
  - Rüstmeister (Armor)
  - Enchanter (Enhancements)
```

### 4. Crystalheim (Magie-Stadt)
```yaml
Region: Ice
Typ: Magier-Zentrum
Population: ~4.000

Features:
  - Magier-Akademie
  - Zauberbuch-Shop
  - Alchemist
  - Magic-Library

NPCs:
  - Magier-Lehrer (Spell-Training)
  - Alchemist (Potions)
  - Bibliothekar (Lore)
```

### 5. Shadowport (Unterwelt-Stadt)
```yaml
Region: Caves
Typ: Schattenwelt
Population: ~2.000 (offiziell)

Features:
  - Schwarzmarkt
  - Diebesgilde
  - Arena (PvP!)
  - Versteckte Quests

NPCs:
  - Schwarzhändler (illegale Items)
  - Gildenmeister (Assassinen-Quests)
  - Arena-Master (PvP-Turniere)
```

---

# ⚔️ COMBAT-SYSTEM

## 1. GRUNDMECHANIK

### Stil
```yaml
Inspiration: Skyrim + Soulframe + Digimon World
NICHT: Souls-like! (NIEMALS so nennen!)

Basis:
  - Real-time Combat
  - Action-basiert
  - Dual-Wielding (2 Hände = 2 Waffen!)
  - Timing wichtig (Parry, Dodge)
```

### Controls
```yaml
Desktop:
  Q: Linke Hand Attacke
  E: Rechte Hand Attacke (vorher Interaktion, jetzt getrennt!)
  Shift: Ausweichen (Dodge)
  Strg: Parieren (Block)
  R: Skills/Magie-Menü
  Space: Springen
  F: Interaktion (NEU!)

Mobile:
  Virtual Joystick: Bewegung
  Button Links: Linke Hand
  Button Rechts: Rechte Hand
  Button Dodge: Ausweichen
  Button Block: Parieren
```

---

## 2. KAMPF-MODI (3)

### MANUAL Mode (Default)
```yaml
Control: Spieler hat volle Kontrolle
Najika: Gibt Tipps, aber greift nicht ein

Best for: Erfahrene Spieler
Difficulty: Höchste
Rewards: +20% XP/Loot
```

### ASSIST Mode
```yaml
Control: Spieler + Najika zusammen
Najika: Übernimmt Auto-Dodge bei kritischen Hits
        Warnt vor Angriffen
        Schlägt Skills vor

Best for: Normale Spieler
Difficulty: Mittel
Rewards: Normal
```

### AUTO Mode (Digimon World-Style!)
```yaml
Control: Najika übernimmt komplett
Spieler: Kann anfeuern ("Go!", "Dodge!", "Use Skill!")

Best for: Entspanntes Spielen, Grinding
Difficulty: Niedrig
Rewards: -20% XP/Loot

Features:
  - Najika kämpft selbst
  - KI entscheidet Strategy
  - Spieler kann befehlen (wie Digimon World!)
  - "EXPLOSION!!!" = Najika nutzt Ultimate
```

---

## 3. TIMING-FENSTER

### Parry (Perfect Block)
```yaml
Window: 40ms (sehr präzise!)
Success: Reflektiert 50% Damage zurück
Failure: Nimmt vollen Schaden

Skill-Improvement:
  - Parry-Skill 0-20: 40ms Window
  - Parry-Skill 20-40: 60ms Window
  - Parry-Skill 40-60: 80ms Window
  - Parry-Skill 60+: 100ms Window
```

### Dodge (i-Frames)
```yaml
i-Frames: 12 Frames (~200ms bei 60 FPS)
Cooldown: 1.5 Sekunden
Stamina-Cost: 15

Success: Unverwundbar während Dodge
Failure: Vulnerable während Cooldown

Skill-Improvement:
  - Dodge-Skill 0-20: 12 Frames
  - Dodge-Skill 20-40: 15 Frames
  - Dodge-Skill 40-60: 18 Frames
  - Dodge-Skill 60+: 24 Frames (0.4s!)
```

### Combo-Window
```yaml
Window: 200ms zwischen Hits
Extend: +50ms pro Combo-Hit (bis max 500ms)

Combo-Bonus:
  2 Hits: +10% Damage
  3 Hits: +20% Damage
  4 Hits: +30% Damage
  5+ Hits: +50% Damage

Break: Wenn 200ms überschritten → Reset
```

---

## 4. KAMERA-MODI (3)

### 1. Orbit Cam (Digimon World-Style)
```yaml
Type: Frei drehbar um Charakter
Control: Maus / Touch-Drag
Distance: 5-15 Meter (zoombar)

Best for: Übersicht, Exploration
Default: JA
```

### 2. Third Person (Folge-Kamera)
```yaml
Type: Folgt Charakter von hinten
Control: Automatisch (schwenkt bei Bewegung)
Distance: 3-5 Meter

Best for: Action, schnelle Kämpfe
```

### 3. First Person (Ego-Perspektive)
```yaml
Type: Aus Augen des Charakters
Control: Maus / Touch
FOV: 90°

Best for: Immersion, Präzision
Usage: Optional (nicht empfohlen für Combat)
```

---

## 5. FINISHER-SYSTEM (QTE)

### Trigger
```yaml
Condition: Gegner HP < 10%
Prompt: "E" erscheint über Gegner
Window: 3 Sekunden
```

### QTE-Mechanik
```yaml
Type: Timed Button-Presses
Buttons: Q/E/Space in Sequenz
Speed: Zufällig (0.5s - 1.5s pro Input)

Ranks:
  S-Rank: Perfect (100% Accuracy, <0.1s Reaktion)
    → 3× Damage, +30% XP, Guaranteed Rare Loot
    
  A-Rank: Excellent (90-99% Accuracy, <0.3s)
    → 2× Damage, +20% XP, High Rare Loot Chance
    
  B-Rank: Good (70-89% Accuracy, <0.5s)
    → 1.5× Damage, +10% XP, Normal Loot
    
  C-Rank: OK (50-69% Accuracy, <1s)
    → Normal Damage, Normal XP
    
  Fail: Miss (Gegner überlebt mit 1 HP!)
```

---

# 🎓 SKILL-SYSTEM

## 1. LEARNING BY DOING (Skyrim-Style)

### Prinzip
```yaml
"Tu es → Werde besser darin!"

KEIN XP-Grind!
KEINE künstlichen Level-Gates!
REALISTISCHE Progression!
```

### Beispiele
```yaml
Schwert benutzen → Schwert-Skill +0.1 pro Hit
Feuer wirken → Feuer-Skill +0.1 pro Cast
Angeln → Angel-Skill +0.1 pro Fang
Kochen → Koch-Skill +0.1 pro Gericht
Laufen → Ausdauer-Skill +0.01 pro 100m

= Spieler tut was Spaß macht
= Skills steigen automatisch
```

---

## 2. SKILL-KATEGORIEN

### Waffen-Skills (6)
```yaml
1. Schwert (0-100)
   - Unlock: Start
   - Progression: Hits zählen
   - Perks: +ATK, Combo-Extend, Crit-Chance

2. Axt (0-100)
   - Unlock: Level 5
   - Progression: Hits zählen
   - Perks: +ATK, Armor-Break, Heavy-Hit

3. Speer (0-100)
   - Unlock: Level 10
   - Progression: Hits zählen
   - Perks: +Range, Pierce, Quick-Jab

4. Bogen (0-100)
   - Unlock: Level 8
   - Progression: Shots zählen
   - Perks: +Accuracy, Crit-Damage, Multi-Shot

5. Magie-Stab (0-100)
   - Unlock: Level 12
   - Progression: Casts zählen
   - Perks: +MATK, Mana-Efficiency, Cast-Speed

6. Fäuste (0-100)
   - Unlock: Start (Always available!)
   - Progression: Hits zählen
   - Perks: +Speed, Combo-Master, Stun-Punch
```

### Magie-Skills (5+)
```yaml
1. Feuer (0-100)
   Progression: Feuer → Feura → Feuga → Feuraga
   
2. Eis (0-100)
   Progression: Eis → Eisra → Eisga → Eisraga
   
3. Blitz (0-100)
   Progression: Blitz → Blitzra → Blitzga → Blitzraga
   
4. Heilung (0-100)
   Progression: Vita → Vitra → Vitga → Vitraga
   
5. EXPLOSION (0-100) [EIGENE KLASSE!]
   Progression: Explosion → Mega-Explosion → ULTRA-EXPLOSION
   Perks: +30-40% Explosion Damage
   Penalty: -15-20% Andere Magie
```

### Leben-Skills (10+)
```yaml
1. Angeln (0-100)
2. Kochen (0-100)
3. Crafting (0-100)
4. Alchemie (0-100)
5. Mining (0-100)
6. Farming (0-100) [GEPLANT]
7. Hunting (0-100) [GEPLANT]
8. Lockpicking (0-100)
9. Stealth (0-100)
10. Charisma (0-100)
```

---

## 3. EXPLOSION-KLASSE (Details)

### Das Trade-Off
```yaml
Wenn EXPLOSION gewählt:
  ✅ +30-40% Explosion Damage
  ✅ Eigener Skill-Baum
  ✅ Ultimate: 300% Damage
  
  ❌ -15-20% Andere Magie
  ❌ KEIN Element-Weaving
  ❌ Cooldown: 10 Minuten

Choice: Permanent (nach Level 20 Entscheidung!)
```

### Skill-Baum
```yaml
Level 1-20: Basic Explosion
  - Explosion (50 Damage, 5m Radius)
  - Cooldown: 10 Minuten
  - Mana: 80

Level 20-40: Mega-Explosion
  - 120 Damage, 10m Radius
  - Cooldown: 8 Minuten
  - Mana: 150

Level 40-60: Giga-Explosion
  - 250 Damage, 15m Radius
  - Cooldown: 6 Minuten
  - Mana: 250

Level 60-80: Tera-Explosion
  - 500 Damage, 20m Radius
  - Cooldown: 5 Minuten
  - Mana: 400

Level 80-100: ULTRA-EXPLOSION (Ultimate!)
  - 1000 Damage, 30m Radius
  - Cooldown: 10 Minuten
  - Mana: ALL (100%)
  - Exhaustion: 60 Sekunden (kann nicht kämpfen!)
  - Visuals: Sichtbare Welt-Zerstörung!
```

---

## 4. ELEMENT-WEAVING (OHNE Explosion!)

### Kombinations-System
```yaml
Feuer + Eis = Steam
  - Effect: Blindheit (3 Sekunden)
  - Damage: 80% von beiden

Feuer + Blitz = Plasma
  - Effect: DoT (5 Sekunden, 20 DPS)
  - Damage: 100% von beiden

Eis + Blitz = Shatter
  - Effect: Stun (2 Sekunden)
  - Damage: 120% von beiden

Eis + Wasser = Frost
  - Effect: Slow (50%, 5 Sekunden)
  - Damage: 90% von beiden

Feuer + Wind = Inferno
  - Effect: AoE Expand (+50% Radius)
  - Damage: 110% von beiden

⚠️ EXPLOSION darf NIEMALS geweaved werden!
```

---

## 5. SKILL-LEARNING VON GEGNERN

### Slime-Begleiter (10-15% Chance)
```yaml
Mechanic: Kopiert Move von besiegtem Gegner
Chance: 10-15% (zufällig)
Max Moves: 20 im Moveset

Beispiel:
  - Besiegter Feuer-Magier
  - Slime kopiert "Feuerball"
  - Slime kann jetzt Feuerball nutzen!
```

### Spieler (1% Chance - USER-ENTSCHEIDUNG!)
```yaml
Mechanic: Lernt Skill von Gegner (Mega Man-Style!)
Chance: 1% (sehr selten!)
Bedingung: Skill muss GESEHEN werden!

User-Choice:
  - System fragt: "Skill 'X' gelernt! Behalten?"
  - User wählt: JA/NEIN
  - Wenn JA: Skill im Skill-Baum
  
Beispiel:
  - Boss nutzt "Meteor-Strike"
  - 1% Chance nach Sieg
  - "Skill gelernt: Meteor-Strike (Level 1)"
  - User kann behalten oder ablehnen
```

---

## 6. ZUSAMMENFASSUNG TEIL 5

**Open World:**
- 9.6km × 9.6km (92.16 km²)
- 9 Regionen (3×3 Grid)
- 5 Städte
- Zentrum: Schwarze Mühle (Mountain Region)

**Combat-System:**
- Real-time (Skyrim + Soulframe + Digimon World)
- Dual-Wielding (Q/E für Links/Rechts)
- 3 Modi (Manual, Assist, Auto)
- Timing-Windows (Parry 40ms, Dodge 12 Frames)
- 3 Kamera-Modi
- QTE-Finisher (S/A/B/C Ranks)

**Skill-System:**
- Learning by Doing (Skyrim-Style)
- Waffen-Skills (6)
- Magie-Skills (5+)
- Leben-Skills (10+)
- EXPLOSION-Klasse (eigener Baum!)
- Element-Weaving (ohne Explosion!)
- Skill-Learning von Gegnern (Slime 10-15%, Spieler 1%)

---

**STATUS:** TEIL 5/10 ABGESCHLOSSEN ✅

**NÄCHSTER TEIL:** Teil 6/10 - PvP, Slime-Begleiter, Oregon Trail

---

**Ende Teil 5/10**