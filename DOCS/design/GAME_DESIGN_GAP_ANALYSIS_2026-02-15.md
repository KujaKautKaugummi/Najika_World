# GAME DESIGN GAP-ANALYSE 2026-02-15

**Erstellt von:** SONNET (Claude Sonnet 4.5)
**Zweck:** Identifikation fehlender Content & Design-Entscheidungen
**Basierend auf:** Explore-Agent Inventory vom 2026-02-15

---

## 🎯 EXECUTIVE SUMMARY

### ✅ Was ist KOMPLETT:
- **Basis-Systeme:** Combat, Magic, Skills, Crafting, Alchemy, Housing ✅
- **Welt-Struktur:** 9 Regionen, 5 Major Cities, Biome ✅
- **3D Assets:** 3,761 Dateien (Chars, Items, Effects) ✅
- **Core NPCs:** ~25-30 NPCs mit Persönlichkeiten ✅
- **Items:** 230+ Items (Waffen, Rüstungen, Consumables) ✅

### ⚠️ Was FEHLT oder ist UNVOLLSTÄNDIG:
- **Quest Coverage:** NUR 10 Quests für 9 Regionen (0-2 pro Region!)
- **NPC Density:** Nur 25-30 NPCs für 5 Major Cities + 9 Regionen
- **Weapon Progression:** Keine klare Tier-Struktur (Common → Legendary)
- **Currency Balance:** 3 Währungen definiert, aber keine Economy-Rules
- **Endgame Content:** Keine Raids, Dungeons, PvP-Arena-Struktur
- **Lore & Dialoge:** NPCs existieren, aber Dialog-Trees fehlen
- **Enemy Variety:** 40+ Enemies, aber keine Boss-Mechanics dokumentiert

---

## 📊 DETAILLIERTE GAP-ANALYSE

### 1️⃣ QUEST-SYSTEM

**Status:** ⚠️ **KRITISCHER CONTENT-GAP!**

**Was EXISTIERT:**
| Quest-Typ | Anzahl | Status |
|-----------|--------|--------|
| Haupt-Quests | 4 | ✅ Implementiert |
| Side-Quests | 6 | ✅ Implementiert |
| **GESAMT** | **10** | ⚠️ **ZU WENIG!** |

**Was FEHLT:**
- ❌ **Pro Region:** Sollte 5-10 Quests haben (aktuell: 0-2)
- ❌ **Quest-Chains:** Keine mehrteiligen Quest-Linien
- ❌ **Daily/Weekly Quests:** Keine wiederholbaren Quests
- ❌ **Faction-Quests:** 0 Ruf-Quests für Fraktionen
- ❌ **Tutorial-Quest-Chain:** Neue Spieler-Einführung fehlt

**EMPFEHLUNG:**
```
SOLL-ZUSTAND (Phase 1):
- Tutorial-Chain: 5 Quests (Schwarze Mühle Intro)
- Pro Region: Min. 3-5 Quests
- Main Story: 15-20 Quests (Chapter-System)
- Side-Quests: 30-50 optionale Quests
- Daily/Weekly: 10 wiederholbare Quests

GESAMT: ~100 Quests für MVP
```

**BEISPIEL Quest-Struktur pro Region:**
```yaml
# Beispiel: Flüsterwald
quests:
  - name: "Das verlorene Digimon"
    type: "main"
    level: 5-10
    reward: "300 Münzen, Wald-Amulett"

  - name: "Kräuter für Apotheker Riku"
    type: "side"
    level: 8
    reward: "150 Münzen, 3x Heiltrank"

  - name: "Die Geister des Waldes"
    type: "lore"
    level: 12
    reward: "Wald-Lore Fragment #3"
```

---

### 2️⃣ NPC-DENSITY

**Status:** ⚠️ **UNTERBEVÖLKERT!**

**Was EXISTIERT:**
| Location | NPCs | Status |
|----------|------|--------|
| Schwarze Mühle (Hub) | ~8 NPCs | ⚠️ Sollte 15-20 haben |
| Großstadt Argentum | ~3 NPCs | ❌ Sollte 20+ haben |
| Andere Cities | ~2-3 pro Stadt | ❌ Sollte 10-15 haben |
| Overworld Encounters | ~5 NPCs | ✅ OK für Wanderer |
| **GESAMT** | **~25-30** | ❌ **Sollte 100+** |

**Was FEHLT:**
- ❌ **Vendors:** Nur 3 Shops (Brauchen: 15+)
- ❌ **Quest-Giver:** Nur 10 Quests = Max 10 Quest-NPCs (Brauchen: 50+)
- ❌ **Flavor-NPCs:** 0 NPCs ohne Funktion (sollte 30+ haben für Immersion)
- ❌ **Faction-Leaders:** Keine Gilden-/Fraktions-NPCs
- ❌ **Trainers:** Keine Skill-Trainer NPCs

**EMPFEHLUNG - NPC-Verteilung:**
```
SCHWARZE MÜHLE (Safe Hub):
- Vendors: 5 (Waffen, Rüstung, Alchemy, Food, General)
- Services: 3 (Bank, Teleporter, Stable)
- Quest-Givers: 5
- Flavor: 7 (Bürger, Kinder, Tiere)
GESAMT: 20 NPCs

ARGENTUM (Hauptstadt):
- Vendors: 8
- Services: 5 (Bank, Auktionshaus, Transmog, etc.)
- Quest-Givers: 10
- Faction-Leaders: 3
- Trainers: 5 (Skill-Meister)
- Flavor: 15
GESAMT: 46 NPCs

ANDERE CITIES (4 Stück):
- Pro Stadt: 10-15 NPCs
GESAMT: 40-60 NPCs

OVERWORLD:
- Wanderer, Händler, Random Encounters: 20 NPCs

GESAMT-SOLL: ~130-150 NPCs
```

---

### 3️⃣ WAFFEN & ITEMS

**Status:** ✅ **Grundlage OK** | ⚠️ **Progression UNKLAR**

**Was EXISTIERT:**
| Kategorie | Anzahl | Status |
|-----------|--------|--------|
| Waffen | 55+ | ✅ Gute Basis |
| Rüstungen | ~30 | ✅ OK |
| Consumables | ~50 | ✅ OK |
| Quest-Items | ~20 | ⚠️ Zu wenig (wegen Quest-Gap) |
| Crafting-Mats | ~40 | ✅ OK |
| **GESAMT** | **~230** | ✅ Solide Basis |

**Was FEHLT:**
- ❌ **Tier-System:** Keine klare Rarity-Struktur
- ❌ **Level-Requirements:** Waffen haben keine Min-Level
- ❌ **Set-Items:** Keine Set-Boni definiert
- ❌ **Legendary-Items:** 0 Unique-Waffen mit Lore
- ❌ **Item-Descriptions:** Viele Items haben nur Namen, keine Lore

**EMPFEHLUNG - Rarity & Tier System:**
```yaml
# BEISPIEL Waffen-Progression:

weapon_tiers:
  common:
    level: 1-10
    stats_multiplier: 1.0
    examples:
      - "Rostiges Schwert"
      - "Holzstab"
      - "Jägerbogen"

  uncommon:
    level: 10-20
    stats_multiplier: 1.5
    examples:
      - "Stahlschwert"
      - "Kristallstab"
      - "Verstärkter Bogen"

  rare:
    level: 20-30
    stats_multiplier: 2.0
    special: "+1 Random Stat"
    examples:
      - "Flammenschwert"
      - "Blitzstab"
      - "Elfenbogen"

  epic:
    level: 30-40
    stats_multiplier: 3.0
    special: "+2 Stats, Passive Ability"
    examples:
      - "Drachentöter"
      - "Arkaner Meisterstab"
      - "Mondlichtbogen"

  legendary:
    level: 40+
    stats_multiplier: 4.0
    special: "Unique Ability, Set-Bonus"
    examples:
      - "Megumin's Explosion Staff" (reduziert Cast-Time für Explosion)
      - "Najika's Crimson Blade" (Life-Steal 5%)
      - "Kuja's Judgment Bow" (+50% Crit vs Bosses)
```

**AKTUELL FEHLENDE LEGENDARY-ITEMS (Vorschläge):**
1. **Megumin's Explosion Staff** - Cast Explosion with -30% Mana Cost
2. **Harley's Chaos Hammer** - 10% Chance to confuse Enemies
3. **Shiro's Calculation Grimoire** - +50% XP Gain for Tactical Skills
4. **Melissa's Nature Bow** - Poison Arrows, +DMG vs Beasts
5. **Kuja's Judgment Sword** - Holy DMG, +100% DMG vs Demons

---

### 4️⃣ WÄHRUNGS- & ECONOMY-SYSTEM

**Status:** ⚠️ **DEFINIERT aber NICHT BALANCED**

**Was EXISTIERT:**
```json
{
  "Münzen (Gold)": "Standard-Währung",
  "Kristalle": "Premium? Event?",
  "Arena-Punkte": "PvP/Arena-Belohnungen"
}
```

**Was FEHLT:**
- ❌ **Preise:** Items haben keine Kosten definiert
- ❌ **Drop-Rates:** Enemies haben keine Münz-Drops dokumentiert
- ❌ **Quest-Rewards:** Keine Standard-Formel (z.B. Level * 50 Münzen)
- ❌ **Vendor-Preise:** Keine Preis-Tabellen
- ❌ **Inflation-Prevention:** Keine Money-Sinks (Repairs, Taxes, etc.)

**EMPFEHLUNG - Economy-Regeln:**
```yaml
# CURRENCY EARNING RATES (Pro Stunde Gameplay):

sources:
  quests:
    main_quest: 200-500 Münzen
    side_quest: 50-150 Münzen
    daily_quest: 100 Münzen

  combat:
    normal_enemy: 5-20 Münzen (abhängig von Level)
    elite_enemy: 50-100 Münzen
    boss: 500-2000 Münzen

  selling_items:
    common_item: 10-50 Münzen
    rare_item: 100-500 Münzen
    epic_item: 500-2000 Münzen

# CURRENCY SPENDING (Money-Sinks):

vendors:
  weapon_tier1: 100 Münzen
  weapon_tier2: 500 Münzen
  weapon_tier3: 2000 Münzen
  weapon_tier4: 10000 Münzen

repairs:
  per_durability_point: 5 Münzen

teleport_costs:
  same_region: 10 Münzen
  different_region: 50 Münzen

housing:
  small_house: 5000 Münzen
  medium_house: 20000 Münzen
  large_house: 100000 Münzen

# PREMIUM CURRENCY (Kristalle):
earning:
  daily_login: 5 Kristalle
  weekly_quest: 20 Kristalle
  achievement: 10-50 Kristalle

spending:
  cosmetic_item: 50-200 Kristalle
  mount: 500 Kristalle
  instant_craft: 10 Kristalle

# ARENA-PUNKTE:
earning:
  win: 10 Punkte
  loss: 2 Punkte

spending:
  arena_gear_tier1: 100 Punkte
  arena_gear_tier2: 500 Punkte
  arena_title: 1000 Punkte
```

---

### 5️⃣ ENEMY & BOSS DESIGN

**Status:** ✅ **Viele Enemies** | ❌ **Keine Mechanics dokumentiert**

**Was EXISTIERT:**
- ✅ 40+ Enemy-Typen (Slimes, Goblins, Drachen, etc.)
- ✅ 9 Boss-Typen (Sumpfdrache, Eiskönig, etc.)
- ✅ Level-Ranges für Enemies

**Was FEHLT:**
- ❌ **Boss-Abilities:** Keine Phase-2 Mechanics
- ❌ **Enemy-AI-Patterns:** Alle gleich oder unterschiedlich?
- ❌ **Loot-Tables:** Was droppen Bosse?
- ❌ **Spawn-Locations:** Wo spawnen welche Enemies?
- ❌ **Respawn-Times:** Wie schnell respawnen Bosse?

**EMPFEHLUNG - Boss-Mechanics Beispiele:**
```yaml
# BEISPIEL BOSS: Sumpfdrache (Level 15)

boss_sumpfdrache:
  name: "Faulzahn der Verdorbene"
  level: 15
  hp: 5000
  location: "Sumpf von Myrkr"
  respawn_time: "30 Minuten"

  phase_1: # 100%-50% HP
    abilities:
      - name: "Giftatem"
        damage: 150
        effect: "Poison DoT (10 DMG/s für 5s)"
        cooldown: 8s

      - name: "Schwanzschlag"
        damage: 200
        effect: "Knockback 5m"
        cooldown: 12s

  phase_2: # 50%-0% HP
    enrage: true
    speed_increase: "+30%"
    abilities:
      - name: "Sumpfexplosion"
        damage: 300 (AoE 10m Radius)
        effect: "Blind 3s"
        cooldown: 15s
        warning: "Boden leuchtet grün (2s Vorlauf)"

      - name: "Gift-Minions spawnen"
        summons: "3x Giftige Slimes (Level 10)"
        cooldown: 30s

  loot_table:
    guaranteed:
      - "Sumpfdrachen-Zahn" (Quest-Item)
      - 500 Münzen

    chance_drops:
      - "Sumpfrüstung (Chest)" (20% Chance)
      - "Giftwiderstands-Ring" (10% Chance)
      - "Rezept: Großer Gegengift-Trank" (5% Chance)

  achievements:
    - "Sumpfdrachen-Jäger" (Ersten Kill)
    - "Sumpfdrachen-Meister" (10 Kills)
    - "Solo-Drachentöter" (Solo Kill ohne NPC-Hilfe)
```

---

### 6️⃣ REGIONEN & WORLD-CONTENT

**Status:** ✅ **Welt-Struktur komplett** | ⚠️ **Content pro Region zu dünn**

**Was EXISTIERT:**
| Region | Biome | Cities | Quests | NPCs | Dungeons |
|--------|-------|--------|--------|------|----------|
| Schwarze Mühle | Safe Zone | 1 (Hub) | 5 | 8 | 0 |
| Flüsterwald | Wald | 0 | 1 | 2 | 0 |
| Kristallberge | Gebirge | 1 | 1 | 3 | 0 |
| Sumpf von Myrkr | Sumpf | 0 | 0 | 1 | 0 |
| Frostgipfel | Schnee | 1 | 1 | 3 | 0 |
| Wüste Kal'Thara | Wüste | 1 | 0 | 2 | 0 |
| Vulkan Aetherion | Vulkan | 0 | 1 | 1 | 0 |
| Argentum | Stadt | 1 (Capital) | 1 | 5 | 0 |
| Arena-Dimensionen | PvP | - | 0 | 0 | 3 Arena-Modes |

**Was FEHLT pro Region:**
- ❌ **Dungeons/Instanzen:** 0 Dungeons definiert!
- ❌ **Hidden Areas:** Keine Secret-Locations
- ❌ **World-Bosses:** Nur 9 Bosse für 9 Regionen (1 pro Region?)
- ❌ **Gathering-Nodes:** Keine Mining/Herbalism-Spots dokumentiert
- ❌ **POIs (Points of Interest):** Keine Landmarks, Ruins, etc.

**EMPFEHLUNG - Content pro Region:**
```yaml
# BEISPIEL: Flüsterwald (Level 5-15 Region)

region_fluesterswald:
  level_range: "5-15"
  biome: "Mystischer Wald"

  quests:
    main: 2 Quests (Teil der Story-Chain)
    side: 5 Quests
    daily: 1 Quest ("Kräuter sammeln")

  npcs:
    vendors: 1 ("Waldhüter-Händler")
    quest_givers: 5
    flavor: 3 ("Waldgeister", "Eremit", "Druidin")

  enemies:
    normal:
      - "Waldslime" (Level 5-7)
      - "Goblin-Späher" (Level 8-10)
      - "Waldwolf" (Level 10-12)
    elite:
      - "Alpha-Wolf" (Level 13)
      - "Goblin-Kriegsherr" (Level 14)
    boss:
      - "Uralte Waldeiche" (Level 15, World-Boss)

  dungeons:
    - name: "Verlassene Druidenhöhle"
      level: 10-12
      length: "15-20 Minuten"
      bosses: 1 ("Verdorbener Druide")

  pois:
    - "Moonwell" (Heilt HP/MP komplett, 1x pro Tag)
    - "Elfen-Ruinen" (Lore-Fragment + Chest)
    - "Versteckter Wasserfall" (Achievement + Cosmetic)

  gathering:
    herbs:
      - "Waldkraut" (Alchemy Tier 1)
      - "Mondblume" (Alchemy Tier 2, nur Nachts)
    mining:
      - "Eisen-Vorkommen" (3 Nodes)
```

---

### 7️⃣ MAGIC & SKILL PROGRESSION

**Status:** ✅ **System komplett** | ⚠️ **Skill-Trees fehlen**

**Was EXISTIERT:**
- ✅ 10 Magic-Schools (Feuer, Wasser, Blitz, etc.)
- ✅ "Learning by Doing" System (Skyrim-Style)
- ✅ Explosion-Magic (Special, nicht kombinierbar)
- ✅ 100+ Zauber definiert

**Was FEHLT:**
- ❌ **Skill-Trees:** Keine visuellen Skill-Trees
- ❌ **Talent-Points:** Wie bekommt man Punkte?
- ❌ **Skill-Synergien:** Keine Cross-School-Combos dokumentiert
- ❌ **Meisterschaft-System:** Keine Master-Levels (100+)

**EMPFEHLUNG:**
```yaml
# SKILL-PROGRESSION Beispiel: Feuer-Magie

fire_magic:
  rank_system:
    novice: "Level 0-20 (Basisfeuer-Zauber)"
    apprentice: "Level 20-40 (Feuerball)"
    adept: "Level 40-60 (Feuer-Wand)"
    expert: "Level 60-80 (Meteor)"
    master: "Level 80-100 (Inferno)"

  skill_tree:
    branch_damage:
      - "Verbesserte Flammen I" (+10% Fire DMG)
      - "Verbesserte Flammen II" (+20% Fire DMG)
      - "Kritische Verbrennung" (+15% Crit Chance Fire Spells)

    branch_utility:
      - "Feuerschutz I" (+25% Fire Resist)
      - "Flammenaura" (Enemies take 10 DMG/s in 5m Radius)

    branch_mastery:
      - "Doppel-Cast Feuer" (10% Chance zu 2x Schaden)
      - "Phoenix-Wiedergeburt" (1x pro Tag: Revive mit 50% HP bei Tod)

  talent_points:
    earning:
      - "1 Punkt pro Level-Up (Max Level 50 = 50 Punkte)"
      - "Bonus-Punkte durch Achievements"

  master_levels: # Nach Level 100
    level_101_150:
      bonus: "+1% Fire DMG pro Level"
      cosmetic: "Flammen-Aura um Charakter"
```

---

### 8️⃣ ENDGAME CONTENT

**Status:** ❌ **FEHLT KOMPLETT!**

**Was EXISTIERT:**
- ✅ Arena-System (PvP/PvE Wellen)
- ✅ Housing (Player-Häuser)

**Was FEHLT:**
- ❌ **Raids:** Keine 4-8 Spieler Dungeons
- ❌ **Mythic+ System:** Keine skalierbaren Schwierigkeiten
- ❌ **World-PvP:** Keine contested Zones
- ❌ **Ranked-PvP:** Keine Ladder/Elo-System
- ❌ **Seasonal-Content:** Keine Events
- ❌ **Transmog/Cosmetics:** Keine Fashion-System
- ❌ **Achievements:** Nur teilweise dokumentiert

**EMPFEHLUNG - Endgame-Loops:**
```yaml
# ENDGAME (Level 50+)

daily_activities:
  - "3x Daily Quests" (15-20 Min)
  - "Daily Dungeon Run" (20 Min)
  - "Arena Daily Win" (10 Min)

weekly_activities:
  - "Weekly Raid" (60-90 Min, 4-8 Spieler)
  - "Weekly World-Boss" (15 Min, Open-World Event)
  - "Ranked PvP Matches" (60 Min für Rank-Climb)

long_term_goals:
  - "Full BiS (Best-in-Slot) Gear" (2-3 Monate)
  - "All Magic-Schools auf Master" (3-6 Monate)
  - "Legendary-Waffe farmen" (1-2 Monate)
  - "PvP Rank 1" (Season-abhängig)
  - "Housing Dekoration" (unbegrenzt)
  - "Achievement-Hunting" (unbegrenzt)

progression_systems:
  gear_tiers:
    - "Rare Gear (Level 50)" → Dungeons
    - "Epic Gear (iLevel 60)" → Weekly Raids
    - "Legendary Gear (iLevel 70)" → Mythic Raids / Arena Rank 5+

  mythic_plus:
    levels: "Mythic +1 bis +20"
    scaling: "+10% Enemy HP/DMG pro Level"
    rewards:
      - "Mythic +5: Epic Loot"
      - "Mythic +10: Legendary Loot"
      - "Mythic +15: Transmog-Sets"
      - "Mythic +20: Titel + Mount"
```

---

## 🚨 KRITISCHE DESIGN-ENTSCHEIDUNGEN BENÖTIGT!

### ❓ FRAGE 1: WÄHRUNGS-BALANCE
```
Wie viele Münzen sollte ein Level-50-Spieler pro Stunde verdienen?
Vorschlag: 5000-10000 Münzen/Stunde (für Repairs, Teleports, etc.)
```

### ❓ FRAGE 2: WEAPON-PROGRESSION
```
Wie viele Legendary-Waffen sollte es geben?
Vorschlag: 1-2 pro Waffen-Typ (15 Typen = 15-30 Legendaries)
```

### ❓ FRAGE 3: LEVEL-CAP
```
Was ist das Max-Level?
Aktuell: Unklar (Enemies gehen bis Level 50+)
Vorschlag: Level 50 (+ Master-Levels bis 150)
```

### ❓ FRAGE 4: PVP VS PVE BALANCE
```
Sollen PvP und PvE separate Stat-Scaling haben?
Vorschlag: JA (vermeidet PvP-Imbalance durch PvE-Gear)
```

### ❓ FRAGE 5: MULTIPLAYER-SKALIERUNG
```
Max Gruppengröße?
Aktuell: Unklar
Vorschlag: 4 Spieler (Dungeons), 8 Spieler (Raids), 1v1/2v2/3v3 (Arena)
```

### ❓ FRAGE 6: QUEST-LEVEL-SCALING
```
Sollen Quests mit Spieler-Level skalieren (wie ESO)?
Oder feste Quest-Levels (wie WoW)?
Vorschlag: FESTE Levels (klare Progression)
```

---

## 📋 CONTENT-CREATION PRIORITÄTEN

### 🔴 P0 - KRITISCH (MVP braucht das!):
1. **QUESTS:** Min. 50 Quests erstellen
   - Tutorial-Chain: 5 Quests
   - Main Story: 15 Quests
   - Side-Quests pro Region: 3-5 (Total: 30 Quests)

2. **NPCs:** Min. 80 NPCs erstellen
   - Schwarze Mühle: 15 NPCs
   - Argentum: 30 NPCs
   - Andere Cities: 10 pro Stadt (40 NPCs)
   - Overworld: 10 NPCs

3. **ECONOMY:** Preise + Loot-Tables definieren
   - Alle Items brauchen Vendor-Preise
   - Alle Enemies brauchen Münz-Drops
   - Quest-Rewards standardisieren

### 🟡 P1 - WICHTIG (für Beta):
4. **LEGENDARY ITEMS:** 15-30 Unique-Waffen mit Lore
5. **BOSS-MECHANICS:** Alle 9 Bosse brauchen Phase-2 Mechanics
6. **DUNGEONS:** Min. 5 Dungeons (1 pro Haupt-Region)
7. **SKILL-TREES:** Visuelles Talent-System

### 🟢 P2 - NICE TO HAVE (Post-Launch):
8. **ENDGAME:** Raids, Mythic+, Ranked PvP
9. **SEASONAL CONTENT:** Events, Battle-Passes
10. **TRANSMOG:** Fashion-System

---

## 📝 NEXT STEPS FÜR OPUS

**OPUS sollte folgende Tasks übernehmen (Kreativ + Content):**

1. **Quest-Writing** (P0):
   - Tutorial-Chain für Schwarze Mühle schreiben
   - Main-Story-Arc planen (15 Quests)
   - Pro Region 3-5 Side-Quests erstellen

2. **NPC-Creation** (P0):
   - NPC-Liste für Schwarze Mühle (15 NPCs)
   - NPC-Liste für Argentum (30 NPCs)
   - Dialog-Trees für wichtige NPCs

3. **Legendary-Items Design** (P1):
   - 15-30 Legendary-Waffen mit Lore + Abilities
   - Set-Items definieren (z.B. "Megumin's Explosion Set")

4. **Boss-Mechanics** (P1):
   - Alle 9 Bosse: Phase-1 + Phase-2 Abilities dokumentieren
   - Loot-Tables für Bosse

5. **Economy-Balancing** (P0):
   - Item-Preise festlegen
   - Enemy-Münz-Drops
   - Quest-Reward-Formeln

**SONNET kann unterstützen mit:**
- Daten-Strukturen für Quests/NPCs erstellen
- Backend-Endpoints für neue Features
- Testing der Economy-Balance

---

## 📚 REFERENZEN

**Inspirationen für Content-Dichte:**
- **The Witcher 3:** ~450 Quests (davon 100 Main/Side, 350 Contracts/Treasure Hunts)
- **Skyrim:** ~300 Quests, ~1100 NPCs
- **World of Warcraft:** ~10000 Quests (über alle Addons)

**Najika World Ziel (Phase 1 MVP):**
- ~100 Quests
- ~150 NPCs
- ~300 Items (aktuell: 230 ✅)
- ~50 Enemies (aktuell: 40+ ✅)
- ~10 Dungeons (aktuell: 0 ❌)

---

**Status:** Warte auf Design-Entscheidungen & OPUS Content-Creation! 🎨
