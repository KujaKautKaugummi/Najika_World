# 🎮 NAJIKA - COMPLETE GAME DESIGN DOCUMENT
**Fantasy Western MMORPG mit Digimon World + Ragnarok + Diablo Immortal Mechaniken**

**Datum:** 2025-10-18
**Version:** 1.0 ALPHA
**Status:** Design Phase → Prototyping im Keller-Modul

---

## 🌍 WORLD DESIGN - DIE 8 GEBIETE

### **Konzept: File Island + 8 Städte**

Jedes Gebiet hat:
- ✅ **1 feste Stadt** (immer gleich, nie prozedural)
- ✅ **Prozeduraler Außenbereich** (generiert neu bei jedem Betreten/Verlassen der Stadt)
- ✅ **Eigene Ästhetik** (Fantasy Western Mix)
- ✅ **Level-Range** (Gebiete für verschiedene Spieler-Levels)

---

### **DIE 8 GEBIETE:**

#### **1. CRIMSON DESERT (Starting Zone)**
```yaml
Level Range: 1-10
Theme: Rote Wüste, Western-Town
Stadt: "New Najika" (Tutorial-Town)
  - Erstes Quest-Hub
  - Basic Shop (Waffen Lvl 1-5)
  - Training-Grounds
  - Beginner-Dungeon: "Abandoned Mine"

Außenbereich (Prozedural):
  - Kakteen, rote Felsen, Sanddünen
  - Mobs: Skorpione, Banditen, Geister-Cowboys
  - Events: Sandstürme, Schatz-Suche, Karawanen-Überfall

Oregon Trail Events:
  - "Dein Pferd ist krank!" (-Speed für 10min)
  - "Banditen angreifen!" (Combat Event)
  - "Oase gefunden!" (+HP/Hunger)
```

#### **2. EMERALD FOREST (Farming/Gathering Zone)**
```yaml
Level Range: 8-20
Theme: Grüner Zauberwald
Stadt: "Greenleaf Village"
  - Farmer's Guild
  - Fischer-Teich
  - Holzfäller-Camp
  - Alchemie-Shop

Außenbereich (Prozedural):
  - Bäume, Pilze, Flüsse, Seen
  - Mobs: Wölfe, Bären, Waldgeister, Treants
  - Ressourcen: Holz (Common → Legendary), Fische, Kräuter

Non-Combat Gameplay:
  - Fishing Spots (Skill-Based Mini-Game)
  - Herb Gathering (für Alchemy)
  - Tree Chopping (für Crafting)
```

#### **3. OBSIDIAN MOUNTAINS (Mining Zone)**
```yaml
Level Range: 15-30
Theme: Dunkle Berge, Minen, Schmieden
Stadt: "Ironforge Peak"
  - Blacksmith Guild
  - Gem-Cutter
  - Mining Equipment Shop
  - Dungeon Portal: "Deep Mines" (Lvl 20-25)

Außenbereich (Prozedural):
  - Höhlen, Minen, Vulkan-Gebiete
  - Mobs: Golem, Lava-Elementare, Dunkle Zwerge
  - Ressourcen: Erze (Copper → Mithril), Edelsteine

Crafting Focus:
  - Waffen schmieden
  - Rüstung verbessern
  - Gems einsetzen (Diablo-Style)
```

#### **4. AZURE COAST (PvP Zone)**
```yaml
Level Range: 25-40
Theme: Piraten-Küste, Hafen-Stadt
Stadt: "Port Royal"
  - PvP Arena
  - Black Market (illegale Items)
  - Schiffs-Händler
  - Taverne (Quests von NPCs)

Außenbereich (Prozedural):
  - Strände, Schiffswracks, Inseln
  - Mobs: Piraten, Meeres-Monster, Untote Matrosen
  - PvP: Andere Spieler können dich angreifen!

Besonderheit:
  - HIGH RISK, HIGH REWARD
  - Beste Loot-Drops
  - Player-Fraktionen (Piraten vs. Marine)
```

#### **5. GOLDEN PLAINS (Händler/Economy Zone)**
```yaml
Level Range: 30-50
Theme: Große Handelsrouten, Karawanen
Stadt: "Trading Post Central"
  - Auktionshaus (Spieler-Markt)
  - Lagerhaus (mehr Inventory)
  - Händler-Gilden
  - Premium-Shops

Außenbereich (Prozedural):
  - Weite Ebenen, Handelsrouten, Karawanen
  - Mobs: Banditen, Diebe, korrupte Händler
  - Events: Karawanen beschützen (Belohnungen)

Endgame Non-Combat:
  - Spieler können als HÄNDLER agieren
  - Items kaufen/verkaufen für Profit
  - Eigene Karawanen schicken (passive Income)
```

#### **6. CRIMSON RUINS (High-Level Dungeon)**
```yaml
Level Range: 45-60
Theme: Alte Ruinen, Magie, Explosion-Krater
Stadt: "Ruins of Crimson" (halb zerstört)
  - Megumin-Statue (Lore!)
  - High-End Gear Shop
  - Dungeon: "Explosion Cathedral"
  - Quest: "Megumin's Legacy"

Außenbereich (Prozedural):
  - Zerstörte Gebäude, Krater, Explosion-Spuren
  - Mobs: Corrupted Mages, Explosion-Elementare
  - Besonderheit: MEGUMIN'S EXPLOSION kann hier die Welt ZERSTÖREN!

Megumin Ultimate:
  - Einmal pro Stadt-Reset (alle 24h)
  - Explosion = Kompletter Außenbereich wird gelöscht!
  - Beim nächsten Betreten: Neu generiert mit Explosion-Kratern
  - Bonus-Loot in den Kratern!
```

#### **7. SHADOW VALLEY (Endgame PvE)**
```yaml
Level Range: 55-70
Theme: Düsteres Tal, Nekromantie
Stadt: "Shadowkeep Fortress"
  - Nekromanten-Gilden
  - Dark Arts Shop
  - Raid-Portal: "Lich King's Castle"
  - Pet-System (Untote Begleiter)

Außenbereich (Prozedural):
  - Friedhöfe, dunkle Wälder, Nekro-Tempel
  - Mobs: Liches, Death Knights, Vampires
  - World-Boss: "Shadow Dragon" (spawnt 1x/Tag)

Endgame Content:
  - 10-Player Raids
  - Legendary Gear Drops
  - Pet-System (Summon Undead Minions)
```

#### **8. CELESTIAL PEAKS (Max Level Zone)**
```yaml
Level Range: 65-MAX
Theme: Himmelberge, Götter, Engel
Stadt: "Heaven's Gate"
  - Endgame Gear (Legendary/Set Items)
  - Transmog-System
  - Guild Halls
  - PvP Season Rankings

Außenbereich (Prozedural):
  - Wolken, schwebende Inseln, Tempel
  - Mobs: Engel (Fallen), Götter, Dämonen
  - World-Bosses: "Najika Prime" (Final Boss)

True Endgame:
  - Infinite Dungeon (steigender Schwierigkeitsgrad)
  - Ranked PvP
  - Guild Wars
  - Seasonal Events
```

---

## 🎯 SKILL-WEAVING SYSTEM

### **Konzept: 1 Skill = Spezialist, Rest = Generalist**

Jeder Spieler wählt **1 MAIN SKILL** (Spezialisierung):

```yaml
Main Skill (gewählt):
  - +50% Effectiveness
  - +25% Speed
  - Unlocks Special Moves
  - Lower Mana Cost

Other Skills (nicht gewählt):
  - -25% Effectiveness
  - Normal Speed
  - Basic Moves Only
  - Higher Mana Cost
```

### **SKILL-KLASSEN:**

#### **1. EXPLOSION MAGE (Megumin-Style)**
```yaml
Main Skill: EXPLOSION
  Bonus:
    - +50% Damage
    - AoE Radius +25%
    - Kann Welt zerstören (in Crimson Ruins)
    - Cooldown -30%

  Malus (andere Skills):
    - Fire Magic: -25% damage
    - Ice Magic: -25% damage
    - Healing: -25% effectiveness

Ultimate: "Crimson Meteor"
  - Weltverändernd in Crimson Ruins
  - 24h Cooldown
  - Löscht kompletten Chunk der Welt
```

#### **2. WARRIOR (Nahkampf)**
```yaml
Main Skill: MELEE COMBAT
  Bonus:
    - +50% Sword/Axe Damage
    - +25% Attack Speed
    - Unlocks Combo-Moves

  Malus:
    - Bow/Ranged: -25%
    - Magic: -25%
```

#### **3. RANGER (Fernkampf)**
```yaml
Main Skill: BOW/RIFLE
  Bonus:
    - +50% Range Damage
    - +25% Accuracy
    - Headshot Crits +100%

  Malus:
    - Melee: -25%
    - Magic: -25%
```

#### **4. HEALER**
```yaml
Main Skill: HEALING/SUPPORT
  Bonus:
    - +50% Heal Amount
    - +25% Buff Duration
    - Party Heals +AoE

  Malus:
    - Damage Skills: -25%
```

#### **5. CRAFTING MASTER (Non-Combat)**
```yaml
Main Skill: CRAFTING
  Bonus:
    - +50% Crafting Success Rate
    - Can Craft Legendary Items
    - Material Cost -25%

  Malus:
    - Combat Skills: -25% (ALL)
    - But: Can sell items for profit!
```

#### **6. FARMING/FISHING MASTER (Non-Combat)**
```yaml
Main Skill: GATHERING
  Bonus:
    - +50% Resource Yield
    - Legendary Fish/Crops
    - Faster Gathering Speed

  Malus:
    - Combat Skills: -25%
    - But: Passive Income from selling!
```

#### **7. MERCHANT (Non-Combat Endgame)**
```yaml
Main Skill: TRADING
  Bonus:
    - +50% Gold from Sales
    - -25% Buy Prices
    - Auction House Tax -50%

  Malus:
    - Combat Skills: -25%
    - But: Can become RICHEST player!
```

---

## 🎲 OREGON TRAIL MECHANICS

### **Event-System: Immer aktiv, überall!**

Alle 5-10 Minuten Spielzeit = 1 Oregon Trail Event

### **EVENT-KATEGORIEN:**

#### **1. SURVIVAL EVENTS**
```yaml
"Du hast Hunger!":
  - Hunger-Bar sinkt schneller
  - -10% HP Regeneration
  - Lösung: Essen finden/kaufen

"Durstig!":
  - -25% Stamina Regeneration
  - -10% Movement Speed
  - Lösung: Wasser trinken

"Erschöpft!":
  - -50% XP Gain
  - Skills langsamer
  - Lösung: Schlafen (Camp)
```

#### **2. COMBAT EVENTS**
```yaml
"Banditen-Überfall!":
  - 3-5 Banditen spawnen
  - Kampf oder Flucht
  - Reward: Gold + Loot

"Monster-Angriff!":
  - Großes Monster spawnt
  - Solo oder rufe Hilfe
  - Reward: Rare Items
```

#### **3. POSITIVE EVENTS**
```yaml
"Schatz gefunden!":
  - Random Chest spawnt
  - Loot: Gold, Items, Gems

"Freundlicher NPC!":
  - NPC gibt Quest
  - Oder: Verkauft seltene Items

"Glücks-Buff!":
  - +25% Loot Drop für 30min
  - +10% XP für 30min
```

#### **4. WEATHER EVENTS**
```yaml
"Sandsturm!" (Crimson Desert):
  - -50% Sichtweite
  - Mobs aggressiver
  - Finde Schutz!

"Gewitter!" (Emerald Forest):
  - Blitze können dich treffen (Damage)
  - +25% Lightning Magic Damage (Bonus!)

"Schneesturm!" (Obsidian Mountains):
  - -25% Movement Speed
  - Hunger sinkt schneller
```

#### **5. WORLD-CHANGING EVENTS**
```yaml
"Megumin's Explosion!" (Crimson Ruins):
  - Wenn Spieler Ultimate nutzt
  - Kompletter Chunk wird gelöscht
  - Krater mit Bonus-Loot entsteht
  - Welt regeneriert bei nächstem Stadt-Reset

"Erdbeben!":
  - Boden wackelt
  - Neue Höhlen spawnen
  - Verschüttete Schätze freigelegt
```

---

## 🎒 PROGRESSION SYSTEMS

### **1. LEVELING**
```yaml
Max Level: 70
XP Sources:
  - Quests: 50%
  - Combat: 30%
  - Crafting: 10%
  - Exploration: 10%

Stats beim Level-Up:
  - +5 HP
  - +2 Stamina
  - +1 Stat Point (frei verteilen)
```

### **2. STAT-SYSTEM (Ragnarok-Style)**
```yaml
STR (Strength):
  - +Melee Damage
  - +Carry Weight

INT (Intelligence):
  - +Magic Damage
  - +Mana Pool

DEX (Dexterity):
  - +Ranged Damage
  - +Critical Chance
  - +Attack Speed

CHA (Charisma):
  - +Trading Prices
  - +Quest Rewards
  - +Pet Effectiveness

LUK (Luck):
  - +Loot Drop Rate
  - +Critical Damage
  - +Dodge Chance
```

### **3. EQUIPMENT-SYSTEM (Diablo-Style)**

#### **Equipment-Slots:**
```yaml
- Weapon (Main Hand)
- Off-Hand (Shield/Dual-Wield)
- Helmet
- Chest Armor
- Gloves
- Pants
- Boots
- Ring (x2)
- Amulet
- Cape/Back

Total: 11 Slots
```

#### **Item-Seltenheit:**
```yaml
Common (Grau):
  - Basic Stats
  - No Bonuses

Rare (Blau):
  - +1-2 Bonus Stats
  - +5-10% Damage

Epic (Lila):
  - +2-4 Bonus Stats
  - +15-25% Damage
  - Special Effect (z.B. Fire Damage)

Legendary (Gold):
  - +4-6 Bonus Stats
  - +30-50% Damage
  - 2 Special Effects
  - Unique Name

Set Items (Grün):
  - Teil eines Sets (z.B. "Megumin's Robes")
  - 2-Set Bonus: +25% Explosion Damage
  - 4-Set Bonus: +Explosion Cooldown -50%
  - 6-Set Bonus: Can cast 2 Explosions
```

#### **Gem-System (Diablo Immortal):**
```yaml
Gems können in Sockets eingesetzt werden:

Ruby:
  - +10 Fire Damage
  - +5% Fire Resistance

Sapphire:
  - +10 Ice Damage
  - +5% Ice Resistance

Emerald:
  - +10 HP Regeneration
  - +5% Healing Received

Diamond:
  - +25 HP
  - +10 Mana

Legendary Gem:
  - Unique Effects (z.B. "Explosion leaves burning ground")
```

---

## 💰 ECONOMY & NON-COMBAT GAMEPLAY

### **CURRENCY SYSTEM:**
```yaml
Gold (Hauptwährung):
  - Von Mobs droppen
  - Quest-Rewards
  - Item-Verkauf

Gems (Premium):
  - Echtes Geld (optional)
  - Oder: sehr selten im Spiel finden

Bits (Digimon-Style):
  - Spezial-Währung für Pet-System
```

### **TRADING SYSTEM:**
```yaml
Auction House (in Golden Plains):
  - Spieler können Items verkaufen
  - Andere Spieler kaufen
  - 5% Tax (Händler-Skill reduziert auf 2.5%)

Player-to-Player Trade:
  - Direkter Handel
  - Keine Tax
  - Verhandeln möglich

NPC-Shops:
  - Basic Items (immer verfügbar)
  - Höhere Preise als Spieler-Handel
```

### **PROFESSION-ENDGAME:**

#### **Farmer:**
```yaml
Gameplay:
  - Pflanzen anbauen (Emerald Forest)
  - Wachstumszeit: 1-24h (real-time)
  - Verkaufen für Gold

Crops:
  - Weizen (Common) - 10 Gold
  - Magical Wheat (Rare) - 100 Gold
  - Explosive Peppers (Legendary) - 5000 Gold

Skill-Tree:
  - Faster Growth
  - Higher Yield
  - Legendary Crop Chance +%
```

#### **Fischer:**
```yaml
Gameplay:
  - Angeln an Spots (Mini-Game!)
  - Skill-based (Timing)
  - Seltenere Fische = schwieriger

Fish:
  - Carp (Common) - 5 Gold
  - Golden Trout (Rare) - 50 Gold
  - Legendary Sea Dragon (!!!) - 10000 Gold

Fischer-Endgame:
  - Kann "Fischer's Guild" beitreten
  - Fishing Tournaments (jeden Sonntag)
  - Größter Fisch = 100k Gold Preis
```

#### **Blacksmith:**
```yaml
Gameplay:
  - Schmiede Waffen/Rüstung
  - Benötigt Erze (von Minern)
  - Mini-Game (Hammer-Timing)

Crafting:
  - Common Items (immer Erfolg)
  - Rare Items (75% Chance)
  - Epic Items (50% Chance)
  - Legendary Items (10% Chance!)

Endgame:
  - Kann Custom-Waffen für andere Spieler craften
  - Bekommt % vom Verkaufswert
  - Beste Blacksmiths = Reputation + Kunden
```

#### **Händler (Ultimate Non-Combat):**
```yaml
Gameplay:
  - Kaufe Items billig, verkaufe teuer
  - Kenne Markt-Preise
  - Verhandle mit Spielern

Endgame:
  - Kann eigenes Geschäft eröffnen
  - NPC-Verkäufer einstellen
  - Passive Income (auch offline!)

Richest Merchants:
  - Leaderboard
  - Spezial-Titel: "Merchant King"
  - Kann eigene Karawanen senden (Global Trade)
```

---

## 🏰 DUNGEON-SYSTEM (bereits implementiert!)

### **Prozedurale Dungeons:**
```yaml
Schwarze Mühle - Keller (aktuell):
  - Level 1-10
  - 14 Enemy-Typen
  - Loot-System
  - Victory/Defeat Screens

Zukünftige Dungeons:
  - "Abandoned Mine" (Crimson Desert)
  - "Deep Mines" (Obsidian Mountains)
  - "Explosion Cathedral" (Crimson Ruins)
  - "Lich King's Castle" (Shadow Valley)
  - "Infinite Tower" (Celestial Peaks - Endgame)
```

---

## 🎯 IMPLEMENTATION-PLAN: KELLER ALS TEST-MODUL

### **PHASE 1: Core Systems (im Keller testen!)**
```yaml
✅ Combat System (DONE)
✅ Enemies (DONE)
✅ Levels (DONE)
⬜ Inventar (TO DO)
⬜ Equipment (TO DO)
⬜ Loot-Drops (TO DO)
⬜ Shop NPC (TO DO)
⬜ Gold Currency (TO DO)
```

### **PHASE 2: Skill-System (im Keller)**
```yaml
⬜ Skill-Weaving Mechanik
⬜ 1 Skill wählen = Boni/Mali
⬜ Test mit 3 Skills (Explosion, Melee, Healing)
```

### **PHASE 3: Oregon Trail (im Keller)**
```yaml
⬜ Event-System aktivieren
⬜ Alle 5min = 1 Random Event
⬜ Test: Hunger, Durst, Erschöpfung
⬜ Test: Combat Events, Treasure Events
```

### **PHASE 4: Crafting/Gathering (im Keller)**
```yaml
⬜ Mining-Spot im Keller
⬜ Crafting-Station
⬜ Item-Herstellung testen
```

### **PHASE 5: Endgame Features (im Keller)**
```yaml
⬜ Gem-System
⬜ Set-Items
⬜ Trading mit NPC
⬜ Pet-System (Digimon-Style)
```

---

## 🚀 ZIEL

**Sobald alles im Keller funktioniert:**
→ Portieren in große 8-Gebiete Open World
→ Dann zu Fortnite UEFN (Unreal Engine Grafik!)

---

**ENDE GAME DESIGN v1.0**

*Erstellt von: Claude Code + Mr.K*
*Nächster Schritt: Keller-Prototyping starten!*
