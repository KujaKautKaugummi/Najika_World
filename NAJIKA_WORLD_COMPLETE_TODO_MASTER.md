# 🎮 NAJIKA WORLD - MASTER TODO LIST
**Erstellt:** 2025-12-04
**Basierend auf:** Vollständiger Code-Analyse + Master-Dokumentation
**Status:** Komplette Roadmap für Spielbarkeit + Vollständiges Projekt

---

## 📋 INHALTSVERZEICHNIS

1. [🎯 PHASE 1: MINIMUM VIABLE GAME (MVP) - 2-4 Wochen](#phase-1-mvp)
2. [🚀 PHASE 2: CORE GAMEPLAY SYSTEMS - 4-8 Wochen](#phase-2-core)
3. [🌟 PHASE 3: CONTENT & POLISH - 8-12 Wochen](#phase-3-content)
4. [💎 PHASE 4: ENDGAME & ADVANCED - 12+ Wochen](#phase-4-endgame)
5. [📊 PRIORITÄTEN-MATRIX](#prioritaeten)
6. [🔧 TECHNISCHE DEBT](#technical-debt)

---

# 🎯 PHASE 1: MINIMUM VIABLE GAME (MVP) - 2-4 WOCHEN {#phase-1-mvp}

**Ziel:** Ein spielbarer Game-Loop, der getestet werden kann

## WOCHE 1-2: CORE SYSTEMS VERBINDEN

### 🗡️ A) BATTLE SYSTEM INTEGRATION (PRIORITÄT 1)

**Status:** Backend 100% fertig, Frontend 20%

**Was existiert:**
- ✅ `backend/najika_battle.py` - Vollständige RPG-Kampflogik
- ✅ `backend/game/battle_system.py` - Battle Core
- ✅ 20+ Enemies mit AI-Patterns
- ✅ Skill-System mit 15+ Skills
- ✅ Equipment-Bonuses berechnet
- ✅ Loot-System
- ⚠️ `digivice/js/battle_core.js` - Minimales Wave-System
- ⚠️ `digivice/js/dungeon_combat.js` - 3D Combat (nur Dungeons)

**Was fehlt:**

#### 1.1 Frontend Battle UI
- [ ] **Battle HUD erstellen**
  - [ ] Player HP/MP/Stamina Bars
  - [ ] Enemy HP Bar
  - [ ] Turn Indicator
  - [ ] Skill Cooldown Display
  - [ ] Buff/Debuff Icons
  - Datei: `digivice/js/ui/battle_ui.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Skill Bar UI**
  - [ ] Horizontal Hotbar (1-8 Keys)
  - [ ] Skill Icons + Namen
  - [ ] MP-Cost Anzeige
  - [ ] Cooldown Overlay
  - [ ] Drag & Drop Skill-Management
  - Datei: `digivice/js/ui/skill_bar.js` (NEU)
  - Geschätzt: 200-300 Zeilen

- [ ] **Combat Log**
  - [ ] Scrollbares Log-Fenster
  - [ ] Farbcodierte Messages (Damage rot, Heal grün, etc.)
  - [ ] Filterfunktion (All, Damage, Healing, Skills)
  - Datei: `digivice/js/ui/combat_log.js` (NEU)
  - Geschätzt: 150-200 Zeilen

#### 1.2 Backend-Frontend Bridge
- [ ] **Battle API Integration**
  - [ ] `/battle/start` Endpoint anbinden
  - [ ] `/battle/action` für Spieler-Aktionen
  - [ ] `/battle/status` für Echtzeit-Updates
  - [ ] WebSocket für Live-Updates
  - Datei: `digivice/js/api/battle_api.js` (NEU)
  - Geschätzt: 200-250 Zeilen

- [ ] **Enemy Spawning anpassen**
  - [ ] `dungeon_combat.js` mit `najika_battle.py` verbinden
  - [ ] Enemy-Stats aus Backend laden
  - [ ] Loot-Drops nach Kampf zeigen
  - Datei: `digivice/js/dungeon_combat.js` (EDIT)
  - Zeilen ändern: 150-200

#### 1.3 Combat Features
- [ ] **Left/Right Hand Combat**
  - [ ] LMB = Left Hand Attack
  - [ ] RMB = Right Hand Attack
  - [ ] Q/E = Left/Right Hand Skills
  - [ ] Q+E = Weave Attack (Combo)
  - Datei: `digivice/js/combat_input.js` (EDIT)
  - Zeilen ändern: 100-150

- [ ] **Skill Learning Display**
  - [ ] "Skill Learned!" Pop-up
  - [ ] Skill-Auswahl wenn Moveset voll (20 Skills)
  - [ ] Skill-Comparison Tooltip
  - Datei: `digivice/js/ui/skill_learn_ui.js` (NEU)
  - Geschätzt: 200-250 Zeilen

- [ ] **Loot Drop Display**
  - [ ] Item-Drop Animation
  - [ ] "Item Looted!" Notification
  - [ ] Loot-List nach Kampf
  - Datei: `digivice/js/ui/loot_ui.js` (NEU)
  - Geschätzt: 150-200 Zeilen

**Gesamt: 1500-2000 Zeilen Code**

---

### 🎒 B) INVENTORY SYSTEM (PRIORITÄT 1)

**Status:** Backend Schema fertig, Frontend existiert NICHT

**Was existiert:**
- ✅ Backend API-Schema (`backend/api/server.py`)
- ✅ Equipment-Slots definiert
- ✅ Item-Types definiert
- ❌ KEINE Item-Daten
- ❌ KEINE UI

**Was fehlt:**

#### 1.4 Inventory UI erstellen
- [ ] **Main Inventory Window**
  - [ ] Grid-Layout (10x5 = 50 Slots)
  - [ ] Item-Icons mit Tooltips
  - [ ] Drag & Drop System
  - [ ] Item-Stacking
  - [ ] Sort/Filter Buttons
  - [ ] I-Taste zum Öffnen
  - Datei: `digivice/js/ui/inventory_ui.js` (NEU)
  - Geschätzt: 400-500 Zeilen

- [ ] **Item Tooltips**
  - [ ] Item-Name + Rarity-Color
  - [ ] Stats (+ATK, +DEF, +HP, etc.)
  - [ ] Description
  - [ ] "Equip" / "Use" / "Drop" Buttons
  - [ ] Vergleich mit equipped Item
  - Datei: `digivice/js/ui/item_tooltip.js` (NEU)
  - Geschätzt: 200-250 Zeilen

#### 1.5 Item Database erstellen
- [ ] **50+ Starter Items**
  - [ ] 15 Weapons (Wooden Sword → Legendary Weapon)
  - [ ] 15 Armor (Leather Vest → Dragon Scale)
  - [ ] 10 Consumables (Potion, Hi-Potion, Elixir)
  - [ ] 10 Materials (Wood, Iron, Crystal)
  - [ ] 5 Quest Items
  - Datei: `backend/data/items.json` (NEU)
  - Geschätzt: 500-800 Zeilen JSON

- [ ] **Item-System Backend**
  - [ ] Item-Loading aus JSON
  - [ ] Item-Stats Berechnung
  - [ ] Item-Effects (Heal, Buff, etc.)
  - Datei: `backend/game/item_system.py` (EDIT/NEU)
  - Geschätzt: 300-400 Zeilen

#### 1.6 Item Collection Integration
- [ ] **Loot nach Kämpfen**
  - [ ] Auto-Pickup oder Manual?
  - [ ] "Press E to loot" für Drops
  - [ ] Loot-Beam Effekt
  - Datei: `digivice/js/loot_pickup.js` (NEU)
  - Geschätzt: 150-200 Zeilen

- [ ] **Item-Usage**
  - [ ] Use-Item Funktion (Heal, Buff)
  - [ ] Cooldown für Consumables
  - [ ] Animation/Sound
  - Datei: `digivice/js/item_usage.js` (NEU)
  - Geschätzt: 100-150 Zeilen

**Gesamt: 1650-2300 Zeilen Code + 500-800 Zeilen Daten**

---

### ⚔️ C) EQUIPMENT SYSTEM (PRIORITÄT 1)

**Status:** Backend Items existieren, Equipment-UI existiert NICHT

**Was existiert:**
- ✅ 20+ Items mit Stats in `backend/najika_battle.py`
- ✅ Equipment-Slots definiert
- ✅ Stat-Bonuses werden berechnet
- ❌ KEINE Equipment-UI
- ❌ Kann Items nicht equippen

**Was fehlt:**

#### 1.7 Equipment Screen UI
- [ ] **Paperdoll/Character Sheet**
  - [ ] Character-Model in Mitte
  - [ ] 8 Equipment-Slots:
    - Weapon Left
    - Weapon Right
    - Helmet
    - Chest Armor
    - Leg Armor
    - Boots
    - Accessory 1
    - Accessory 2
  - [ ] Drag & Drop from Inventory
  - [ ] Stat-Preview on Hover
  - [ ] Vergleich: Current vs New
  - Datei: `digivice/js/ui/equipment_ui.js` (NEU)
  - Geschätzt: 400-500 Zeilen

- [ ] **Stat Display Panel**
  - [ ] Base Stats (STR, DEF, INT, AGI, LUK)
  - [ ] Bonus Stats (from Equipment)
  - [ ] Total Stats
  - [ ] HP/MP Max Values
  - [ ] ATK/DEF Calculations
  - Datei: `digivice/js/ui/stats_panel.js` (NEU)
  - Geschätzt: 200-250 Zeilen

#### 1.8 Equipment Logic
- [ ] **Equip/Unequip System**
  - [ ] Validate Item-Type für Slot
  - [ ] Swap Items (equip new, old → inventory)
  - [ ] Update Character Stats
  - [ ] Save Equipment State
  - Datei: `digivice/js/equipment_manager.js` (NEU)
  - Geschätzt: 200-300 Zeilen

- [ ] **Visual Equipment**
  - [ ] Update 3D Character Model
  - [ ] Weapon Visuals (Left/Right)
  - [ ] Armor Visuals
  - [ ] Color Variations
  - Datei: `digivice/js/equipment_visuals.js` (NEU)
  - Geschätzt: 300-400 Zeilen

**Gesamt: 1100-1450 Zeilen Code**

---

### 📊 D) STATS DISPLAY (PRIORITÄT 2)

**Status:** Backend trackt alles, Frontend zeigt NICHTS

**Was existiert:**
- ✅ `backend/najika_living_system.py` - Hunger, Energy, Mood
- ✅ Auto-Care System funktioniert
- ✅ Stat-Decay implementiert
- ❌ KEINE UI-Bars
- ❌ Spieler sieht Stats nicht

**Was fehlt:**

#### 1.9 Living Stats UI
- [ ] **HUD Stats Bars**
  - [ ] HP Bar (oben links)
  - [ ] MP Bar (unter HP)
  - [ ] Stamina Bar (unter MP)
  - [ ] Hunger Bar (rechts)
  - [ ] Thirst Bar (unter Hunger)
  - [ ] Energy Bar (unter Thirst)
  - [ ] Mood Indicator (Icon + %)
  - Datei: `digivice/js/ui/stats_hud.js` (NEU)
  - Geschätzt: 250-300 Zeilen

- [ ] **Care Actions UI**
  - [ ] Feed Button (+ Food-Menü)
  - [ ] Drink Button
  - [ ] Sleep Button (zeigt Sleep-Screen)
  - [ ] Stat-Tooltips on Hover
  - Datei: `digivice/js/ui/care_ui.js` (NEU)
  - Geschätzt: 200-250 Zeilen

#### 1.10 Living System Integration
- [ ] **Backend API anbinden**
  - [ ] `/living/status` Endpoint
  - [ ] `/living/feed` Endpoint
  - [ ] `/living/sleep` Endpoint
  - [ ] Real-time Stat Updates (WebSocket)
  - Datei: `digivice/js/api/living_api.js` (NEU)
  - Geschätzt: 150-200 Zeilen

- [ ] **Visual Feedback**
  - [ ] "Hungry!" Icon wenn < 30%
  - [ ] "Thirsty!" Icon wenn < 20%
  - [ ] "Tired!" Icon wenn < 10%
  - [ ] Stat-Bar Color-Coding (grün/gelb/rot)
  - Datei: `digivice/js/ui/status_indicators.js` (NEU)
  - Geschätzt: 100-150 Zeilen

**Gesamt: 700-900 Zeilen Code**

---

## WOCHE 3-4: CONTENT & QUESTS

### 📜 E) QUEST SYSTEM (PRIORITÄT 2)

**Status:** Backend Schema fertig, KEIN Content

**Was existiert:**
- ✅ Backend API (`/game/quests/*`)
- ✅ Quest-State Tracking
- ❌ KEINE Quest-Daten
- ❌ KEINE Quest-UI

**Was fehlt:**

#### 1.11 Quest UI
- [ ] **Quest Log Window**
  - [ ] Active Quests Tab
  - [ ] Completed Quests Tab
  - [ ] Quest Details Panel
  - [ ] Objectives Progress (3/5 Rats killed)
  - [ ] Rewards Preview
  - [ ] J-Taste zum Öffnen
  - Datei: `digivice/js/ui/quest_log_ui.js` (NEU)
  - Geschätzt: 400-500 Zeilen

- [ ] **Quest Tracker (HUD)**
  - [ ] Compact Quest List (rechts oben)
  - [ ] Current Objectives
  - [ ] Progress Bars
  - [ ] Minimizable
  - Datei: `digivice/js/ui/quest_tracker.js` (NEU)
  - Geschätzt: 200-250 Zeilen

- [ ] **Quest Accept/Complete UI**
  - [ ] NPC Quest Dialog
  - [ ] Quest-Description Pop-up
  - [ ] Accept/Decline Buttons
  - [ ] Quest-Complete Fanfare
  - [ ] Rewards-Display
  - Datei: `digivice/js/ui/quest_dialog_ui.js` (NEU)
  - Geschätzt: 250-300 Zeilen

#### 1.12 Quest Content erstellen
- [ ] **20 Starter Quests**

**Tutorial Quests (5):**
  - [ ] "Welcome to Najika World" - Talk to Najika
  - [ ] "First Steps" - Walk to Marker
  - [ ] "Combat Training" - Kill 3 Rats
  - [ ] "Equip Yourself" - Equip 1 Weapon
  - [ ] "Survival Basics" - Eat Food, Drink Water

**Combat Quests (5):**
  - [ ] "Rat Infestation" - Kill 10 Rats
  - [ ] "Skeleton Menace" - Kill 5 Skeletons
  - [ ] "Slime Hunt" - Kill 8 Slimes
  - [ ] "Ghost Buster" - Kill 3 Ghosts
  - [ ] "Boss Challenge" - Defeat Rat King

**Gathering Quests (5):**
  - [ ] "Catch 5 Fish" - Fishing
  - [ ] "Harvest 10 Carrots" - Garden
  - [ ] "Collect 20 Wood" - Woodcutting
  - [ ] "Mine 15 Iron" - Mining
  - [ ] "Gather 10 Herbs" - Kräuterkunde

**Exploration Quests (5):**
  - [ ] "Explore Dungeon 1" - Enter Crystal Cavern
  - [ ] "Find Hidden Treasure" - Locate Secret Chest
  - [ ] "Map the Forest" - Visit 5 Locations
  - [ ] "Climb the Mountain" - Reach Summit
  - [ ] "Discover the Ruins" - Find Ancient Ruins

  - Datei: `backend/data/quests.json` (NEU)
  - Geschätzt: 1000-1500 Zeilen JSON

#### 1.13 Quest Logic
- [ ] **Quest-System Backend**
  - [ ] Load Quests from JSON
  - [ ] Track Quest Progress
  - [ ] Objective Completion Check
  - [ ] Reward Distribution
  - [ ] Quest Prerequisites
  - Datei: `backend/game/quest_system.py` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Quest Triggers**
  - [ ] Kill-Count Tracking
  - [ ] Item-Collection Tracking
  - [ ] Location-Visit Tracking
  - [ ] NPC-Talk Tracking
  - Datei: `digivice/js/quest_tracker.js` (NEU)
  - Geschätzt: 200-300 Zeilen

**Gesamt: 2450-3450 Zeilen Code + 1000-1500 Zeilen Daten**

---

### 🛒 F) SHOP SYSTEM (PRIORITÄT 2)

**Status:** Garden Shop funktioniert, Item-Shop fehlt

**Was existiert:**
- ✅ Garden Shop (Seeds kaufen/verkaufen)
- ✅ Gold-Tracking im Backend
- ❌ Kein Item-Shop
- ❌ Keine Weapon/Armor Shops

**Was fehlt:**

#### 1.14 Shop UI
- [ ] **Shop Window**
  - [ ] Shop Tabs (Weapons, Armor, Consumables, Materials)
  - [ ] Item-Grid mit Icons
  - [ ] Item-Tooltip on Hover
  - [ ] Buy-Button mit Preis
  - [ ] Player Gold Display
  - [ ] "Not enough Gold!" Feedback
  - Datei: `digivice/js/ui/shop_ui.js` (NEU)
  - Geschätzt: 350-450 Zeilen

- [ ] **Sell Interface**
  - [ ] Inventory-Items anzeigen
  - [ ] Sell-Price = 50% Buy-Price
  - [ ] Sell-All Button
  - [ ] Confirmation Dialog
  - Datei: `digivice/js/ui/sell_ui.js` (NEU)
  - Geschätzt: 200-250 Zeilen

#### 1.15 Shop Content
- [ ] **Item-Shop Inventory**
  - [ ] 15 Weapons (Level 1-10)
  - [ ] 15 Armor Sets (Level 1-10)
  - [ ] 10 Consumables (Potions, Food, Buffs)
  - [ ] 10 Materials (Crafting)
  - Datei: `backend/data/shop_inventory.json` (NEU)
  - Geschätzt: 500-700 Zeilen JSON

- [ ] **Dynamic Pricing**
  - [ ] Level-Based Prices
  - [ ] Rarity-Multiplier
  - [ ] Discount Events (Random/Timed)
  - Datei: `backend/game/shop_system.py` (NEU)
  - Geschätzt: 200-300 Zeilen

#### 1.16 Shop Integration
- [ ] **NPC Shops**
  - [ ] General Shop (alle Items)
  - [ ] Weaponsmith (nur Waffen)
  - [ ] Armorsmith (nur Rüstungen)
  - [ ] Alchemist (nur Potions/Buffs)
  - [ ] E-Taste zum Öffnen bei NPC
  - Datei: `digivice/js/npc_shops.js` (NEU)
  - Geschätzt: 150-200 Zeilen

**Gesamt: 900-1200 Zeilen Code + 500-700 Zeilen Daten**

---

## 📊 MVP PHASE 1 ZUSAMMENFASSUNG

**Total Code:** ~8000-11,000 Zeilen
**Total Daten:** ~2000-3000 Zeilen JSON
**Zeitaufwand:** 2-4 Wochen (bei Vollzeit)

**Nach Phase 1 hast du:**
✅ Vollständiges Battle-System (Kämpfen mit Skills)
✅ Inventory + Equipment (Items sammeln, equippen)
✅ Stats-Display (sichtbar was Najika braucht)
✅ 20 Quests (Progression + Ziele)
✅ Item-Shop (Waffen/Rüstung kaufen)

**= SPIELBARER GAME-LOOP! 🎮**

---

---

# 🚀 PHASE 2: CORE GAMEPLAY SYSTEMS - 4-8 WOCHEN {#phase-2-core}

**Ziel:** Vollständige Gameplay-Systeme für alle Features

## A) CARD GAME (TRIPLE TRIAD) GAMEPLAY

**Status:** 🟡 Database + UI fertig, KEIN Gameplay

**Was existiert:**
- ✅ Backend Card-Database (`backend/api/card_game.py`)
- ✅ 12 Test-Cards in DB
- ✅ Frontend UI (`digivice/js/ui/card_game_ui.js`)
- ✅ Collection Viewer
- ❌ KEIN Gameplay

**Was fehlt:**

### 2.1 Triple Triad Gameplay-Logik
- [ ] **Board & Placement**
  - [ ] 3×3 Grid State
  - [ ] Card Placement Validation
  - [ ] Player/Opponent Turn System
  - Datei: `digivice/js/triple_triad/board.js` (NEU)
  - Geschätzt: 200-300 Zeilen

- [ ] **Card Battle Rules**
  - [ ] Compare Adjacent Values (Top/Right/Bottom/Left)
  - [ ] Capture-Mechanik (höherer Wert gewinnt)
  - [ ] Flip Cards on Capture
  - [ ] Score Calculation (Spieler vs Gegner)
  - Datei: `digivice/js/triple_triad/rules.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Special Rules (Optional)**
  - [ ] Plus Rule (Summen vergleichen)
  - [ ] Same Rule (Gleiche Werte = Capture)
  - [ ] Combo Rule (Kettenreaktion)
  - Datei: `digivice/js/triple_triad/special_rules.js` (NEU)
  - Geschätzt: 200-300 Zeilen

### 2.2 AI-Gegner
- [ ] **AI Difficulty Levels**
  - [ ] Easy AI (Random Moves)
  - [ ] Medium AI (Basic Strategy)
  - [ ] Hard AI (Optimal Placement)
  - Datei: `digivice/js/triple_triad/ai.js` (NEU)
  - Geschätzt: 300-400 Zeilen

### 2.3 Match System
- [ ] **Match Flow**
  - [ ] Deck Selection (5 Cards)
  - [ ] Match Start → Turn System → Victory/Defeat
  - [ ] Card Rewards (Winner gets 1 Card from Loser)
  - [ ] Rating/Ranking Update
  - Datei: `digivice/js/triple_triad/match.js` (NEU)
  - Geschätzt: 200-300 Zeilen

### 2.4 Card Content
- [ ] **100+ Cards erstellen**
  - [ ] 30 Common Cards
  - [ ] 25 Uncommon Cards
  - [ ] 20 Rare Cards
  - [ ] 15 Epic Cards
  - [ ] 10 Legendary Cards
  - Datei: `backend/data/cards.json` (EDIT)
  - Geschätzt: +800-1200 Zeilen JSON

**Gesamt: 2000-2900 Zeilen Code**

---

## B) DICE MONSTERS GAMEPLAY

**Status:** 🟡 Database + 3D Dice fertig, KEIN Gameplay

**Was existiert:**
- ✅ Backend API (`backend/api/dice_monsters.py`)
- ✅ 3D Dice Rolling (`digivice/js/3d_dice_system.js`)
- ✅ Frontend UI (`digivice/js/ui/dice_monsters_ui.js`)
- ❌ KEIN Duel-System

**Was fehlt:**

### 2.5 DDM Game Rules
- [ ] **Dice Rolling Phase**
  - [ ] Roll 3 Dice (1-6)
  - [ ] Collect Crests (Fire, Water, Earth, Wind, Light, Dark)
  - [ ] Crest Pool Management
  - Datei: `digivice/js/ddm/dice_roll.js` (NEU)
  - Geschätzt: 200-300 Zeilen

- [ ] **Monster Summoning**
  - [ ] Spend Crests to Summon
  - [ ] Monster Placement on Board
  - [ ] Monster Stats (ATK/DEF/Movement)
  - Datei: `digivice/js/ddm/summoning.js` (NEU)
  - Geschätzt: 250-350 Zeilen

- [ ] **Board Movement**
  - [ ] Hex-Grid Board (8×8)
  - [ ] Path-Building System
  - [ ] Monster Movement Rules
  - [ ] Dice Lord Position
  - Datei: `digivice/js/ddm/board.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Battle System**
  - [ ] Monster vs Monster Combat
  - [ ] Attack Dice Lord (Win Condition)
  - [ ] Dice Lord HP (starts at 3)
  - [ ] Victory/Defeat Conditions
  - Datei: `digivice/js/ddm/battle.js` (NEU)
  - Geschätzt: 300-400 Zeilen

### 2.6 DDM AI
- [ ] **AI Opponent**
  - [ ] Roll Dice
  - [ ] Summon Monsters (Strategy)
  - [ ] Move/Attack (Path to Player Dice Lord)
  - Datei: `digivice/js/ddm/ai.js` (NEU)
  - Geschätzt: 250-350 Zeilen

### 2.7 Monster Content
- [ ] **50+ Dice Monsters**
  - [ ] 15 Fire Monsters
  - [ ] 15 Water Monsters
  - [ ] 15 Earth Monsters
  - [ ] 15 Wind Monsters
  - [ ] 15 Light Monsters
  - [ ] 15 Dark Monsters
  - Datei: `backend/data/dice_monsters.json` (NEU)
  - Geschätzt: 600-1000 Zeilen JSON

**Gesamt: 1900-2800 Zeilen Code**

---

## C) SLIME COMPANION SYSTEM

**Status:** ✅ Backend implementiert, Frontend fehlt

**Was existiert:**
- ✅ `backend/game/slime_system.py` - Vollständig!
- ✅ Tier → Slime → Rainbow Evolution
- ✅ 8 Slime-Farben (je Region)
- ✅ Tamagotchi-Pflege
- ✅ Rettungs-Mechanik (1x/24h)
- ✅ Lern-System (10-15%)
- ❌ KEINE Frontend-UI

**Was fehlt:**

### 2.8 Slime UI
- [ ] **Slime-Status Panel (HUD)**
  - [ ] Slime-Icon + Level
  - [ ] HP/MP Bars
  - [ ] Hunger/Thirst/Sleep/Mood Bars
  - [ ] Kampfeslust Meter
  - [ ] Current Form (Tier/Slime/Rainbow)
  - Datei: `digivice/js/ui/slime_hud.js` (NEU)
  - Geschätzt: 250-300 Zeilen

- [ ] **Slime Care Window**
  - [ ] Feed Slime (Food-Menü)
  - [ ] Water Slime
  - [ ] Let Slime Sleep
  - [ ] Play with Slime (Mini-Game)
  - [ ] Stat-Decay Visualization
  - Datei: `digivice/js/ui/slime_care_ui.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Slime Evolution Window**
  - [ ] Current Form Display
  - [ ] Evolution Requirements
  - [ ] Color-Unlock Progress (0/8 Colors)
  - [ ] Rainbow-Ritual Button
  - Datei: `digivice/js/ui/slime_evolution_ui.js` (NEU)
  - Geschätzt: 200-300 Zeilen

### 2.9 Slime Combat Integration
- [ ] **Slime in Battle**
  - [ ] Slime appears next to Player
  - [ ] AI-controlled Auto-attacks
  - [ ] Slime Commands (Hold/Attack/Defend)
  - [ ] Slime learns Moves (10-15% chance)
  - [ ] Intercept when Player < 5% HP
  - Datei: `digivice/js/slime_combat.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Slime-Moveset UI**
  - [ ] 20 Move Slots
  - [ ] Move-Replacement Dialog (wenn voll)
  - [ ] Move Details (Damage, Type, MP-Cost)
  - Datei: `digivice/js/ui/slime_moveset_ui.js` (NEU)
  - Geschätzt: 200-250 Zeilen

### 2.10 Slime Rescue System
- [ ] **1x/24h Rescue**
  - [ ] Detect Lethal Damage
  - [ ] Slime-Intercept Animation
  - [ ] "Your Slime saved you!" Pop-up
  - [ ] 24h Cooldown Timer Display
  - [ ] Slime Exhaustion (-50% Stats)
  - Datei: `digivice/js/slime_rescue.js` (NEU)
  - Geschätzt: 150-200 Zeilen

- [ ] **Healing Ritual**
  - [ ] Ritual UI (3 Items benötigt)
  - [ ] Mondblume (Nacht-Spawn)
  - [ ] Vulkanessenz (Boss-Drop)
  - [ ] Kristallwasser (Gletscher)
  - [ ] Ritual Animation
  - Datei: `digivice/js/ui/slime_ritual_ui.js` (NEU)
  - Geschätzt: 200-300 Zeilen

### 2.11 Slime Content
- [ ] **Slime-Formen erstellen**
  - [ ] 6 Tier-Formen (Flammen-Hase, Eis-Fuchs, etc.)
  - [ ] 8 Slime-Farben (je Region)
  - [ ] Rainbow-Slime (Ultimate)
  - Datei: `backend/data/slime_forms.json` (NEU)
  - Geschätzt: 300-500 Zeilen JSON

**Gesamt: 1900-2850 Zeilen Code**

---

## D) CRAFTING SYSTEM

**Status:** ❌ Existiert nicht

**Was existiert:**
- ✅ Konzept in Master-Doku
- ❌ KEIN Code
- ❌ KEINE Rezepte

**Was fehlt:**

### 2.12 Crafting UI
- [ ] **Crafting Window**
  - [ ] Recipe List (kategorisiert)
  - [ ] Recipe Details (Materials + Result)
  - [ ] Material-Inventory (zeigt was du hast)
  - [ ] Craft-Button (+ Quantity)
  - [ ] Skill-Level Display
  - Datei: `digivice/js/ui/crafting_ui.js` (NEU)
  - Geschätzt: 400-500 Zeilen

- [ ] **Crafting Stations**
  - [ ] Forge (Weapons/Armor)
  - [ ] Alchemy Table (Potions)
  - [ ] Enchanting Table (Enchantments)
  - [ ] Cooking Pot (Food)
  - [ ] E-Taste zum Nutzen
  - Datei: `digivice/js/crafting_stations.js` (NEU)
  - Geschätzt: 200-300 Zeilen

### 2.13 Crafting Logic
- [ ] **Crafting-System Backend**
  - [ ] Load Recipes from JSON
  - [ ] Validate Materials
  - [ ] Craft Item (consume materials)
  - [ ] Skill-Level Check
  - [ ] XP-Gain auf Skill
  - Datei: `backend/game/crafting_system.py` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Recipe Discovery**
  - [ ] Lernen durch Zerlegen (Analyze)
  - [ ] Finden in Welt (Scrolls)
  - [ ] Kaufen von NPCs
  - Datei: `backend/game/recipe_discovery.py` (NEU)
  - Geschätzt: 150-200 Zeilen

### 2.14 Crafting Content
- [ ] **100+ Rezepte**
  - [ ] 30 Weapon Recipes
  - [ ] 30 Armor Recipes
  - [ ] 20 Potion Recipes
  - [ ] 20 Food Recipes
  - Datei: `backend/data/recipes.json` (NEU)
  - Geschätzt: 1000-1500 Zeilen JSON

**Gesamt: 2050-2900 Zeilen Code**

---

## E) HARDCORE/SOFTY MODES

**Status:** ⚠️ Konzept fertig, nicht implementiert

**Was existiert:**
- ✅ Vollständige Design-Dokumentation
- ❌ KEIN Code

**Was fehlt:**

### 2.15 Mode Selection
- [ ] **Character Creation**
  - [ ] Hardcore/Softy Mode wählen
  - [ ] Warning-Dialog für Hardcore
  - [ ] Permanent-Lock Bestätigung
  - Datei: `digivice/js/ui/character_creation_ui.js` (NEU)
  - Geschätzt: 200-300 Zeilen

- [ ] **First Death Prompt**
  - [ ] Najika erscheint
  - [ ] Dialog: "Zu hart für dich?"
  - [ ] Ja → Permanent Softy
  - [ ] Nein → Hardcore weiter
  - Datei: `digivice/js/death_handler.js` (NEU)
  - Geschätzt: 150-200 Zeilen

### 2.16 Permadeath System (Hardcore)
- [ ] **Death Mechanics**
  - [ ] Check Totem-Item
  - [ ] Check Slime-Rescue
  - [ ] Check Revive-Window (8s)
  - [ ] Permadeath wenn alle fehlschlagen
  - Datei: `digivice/js/permadeath.js` (NEU)
  - Geschätzt: 200-300 Zeilen

- [ ] **Character Reset**
  - [ ] Delete Character-Data
  - [ ] Return to Character Creation
  - [ ] "You Died" Screen
  - Datei: `backend/game/permadeath_handler.py` (NEU)
  - Geschätzt: 150-200 Zeilen

### 2.17 Softy Mode
- [ ] **Normal Respawn**
  - [ ] 30s Revive-Timer
  - [ ] Respawn at Checkpoint
  - [ ] Keine Item-Verluste
  - Datei: `digivice/js/respawn.js` (NEU)
  - Geschätzt: 100-150 Zeilen

**Gesamt: 800-1150 Zeilen Code**

---

## F) PVP SYSTEM (3 MODI)

**Status:** ✅ Backend implementiert, Frontend fehlt

**Was existiert:**
- ✅ `backend/game/pvp_system.py` - Vollständig!
- ✅ 3 Modi (Hardcore/Normal/Softy)
- ✅ Mercy-Mechanik
- ✅ Double-Confirmation
- ❌ KEINE Frontend-UI

**Was fehlt:**

### 2.18 PvP UI
- [ ] **PvP Menu**
  - [ ] Hardcore-PvP Button
  - [ ] Normal-PvP Button
  - [ ] Softy-PvP Button
  - [ ] Mode-Beschreibungen
  - [ ] Ranking-Display
  - Datei: `digivice/js/ui/pvp_menu_ui.js` (NEU)
  - Geschätzt: 250-300 Zeilen

- [ ] **Mercy-Prompt (Hardcore)**
  - [ ] Verlierer: "Alles geben um zu leben?"
  - [ ] Gewinner: "Gnade gewähren?"
  - [ ] Double-JA Bestätigung
  - [ ] Item-Transfer-List
  - Datei: `digivice/js/ui/mercy_dialog_ui.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **PvP Arena**
  - [ ] Matchmaking-System
  - [ ] Arena-Map (PvP-Zone)
  - [ ] Round-Timer
  - [ ] Victory/Defeat Screen
  - Datei: `digivice/js/pvp_arena.js` (NEU)
  - Geschätzt: 300-400 Zeilen

### 2.19 PvP Integration
- [ ] **Backend API anbinden**
  - [ ] `/pvp/match/start`
  - [ ] `/pvp/match/action`
  - [ ] `/pvp/mercy/offer`
  - [ ] `/pvp/mercy/accept`
  - Datei: `digivice/js/api/pvp_api.js` (NEU)
  - Geschätzt: 200-300 Zeilen

**Gesamt: 1050-1400 Zeilen Code**

---

## 📊 PHASE 2 ZUSAMMENFASSUNG

**Total Code:** ~11,700-16,000 Zeilen
**Total Daten:** ~2700-4200 Zeilen JSON
**Zeitaufwand:** 4-8 Wochen

**Nach Phase 2 hast du:**
✅ Triple Triad spielbar
✅ Dice Monsters spielbar
✅ Slime Companion funktioniert
✅ Crafting System funktioniert
✅ Hardcore/Softy Modes
✅ PvP (3 Modi)

**= ALLE CORE GAME-SYSTEMS FUNKTIONIEREN! 🚀**

---

---

# 🌟 PHASE 3: CONTENT & POLISH - 8-12 WOCHEN {#phase-3-content}

**Ziel:** Welt-Content, Lore, NPCs, Events

## A) 8 REGIONEN IMPLEMENTATION

**Status:** ❌ Konzept fertig, nicht gebaut

**Was existiert:**
- ✅ Master-Doku mit allen 8 Regionen
- ✅ Slime-Farben je Region
- ❌ KEINE 3D-Maps
- ❌ KEINE Prozedurale Generation

**Was fehlt:**

### 3.1 Regionen-Maps (je ~2 Wochen)
Für jede Region:

- [ ] **Bernstein-Dünen (Wüste)** 🟡
  - [ ] 3D-Map erstellen
  - [ ] Wüsten-Biome
  - [ ] Handelsfestung (Stadt)
  - [ ] Goldstaub-Öde (Dungeon)
  - [ ] Enemy-Spawns (Skorpione, Banditen, Sandelementale)
  - [ ] Sandstürme (Weather-Event)
  - [ ] Kara wanen-NPCs
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Samtmoos-Tiefwald (Wald)** 🟢
  - [ ] 3D-Map erstellen
  - [ ] Wald-Biome
  - [ ] Dampf-Hain (Onsen-Stadt)
  - [ ] Druiden-Settlement
  - [ ] Enemy-Spawns (Wölfe, Spinnen, Druiden)
  - [ ] Nebel (Weather-Event)
  - [ ] Kräuter-Spawns
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Salzwind-Küste (Meer)** 🔵
  - [ ] 3D-Map erstellen
  - [ ] Küsten-Biome + Unterwasser
  - [ ] Salzige Bucht (Piraten-Stadt)
  - [ ] Unterwasser-Dungeons
  - [ ] Enemy-Spawns (Pirat en, Wasserschlangen, Haie)
  - [ ] Sturmflut (Weather-Event)
  - [ ] Fishing-Spots
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Blitzebene (Hochland)** 🟣
  - [ ] 3D-Map erstellen
  - [ ] Hochland-Biome
  - [ ] Runenheim (Stadt)
  - [ ] Klettern-Mechanik
  - [ ] Enemy-Spawns (Harpyien, Blitz-Elementale, Sturmvögel)
  - [ ] Gewitter (Weather-Event)
  - [ ] Runen-Altäre
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Grünschlamm-Sumpf (Sumpf)** ⚫
  - [ ] 3D-Map erstellen
  - [ ] Sumpf-Biome
  - [ ] Funkelnest (versteckte Schatzkammer)
  - [ ] Enemy-Spawns (Hexen, Gift-Kreaturen, Irrlichter)
  - [ ] Miasma (Gift-Nebel)
  - [ ] Hexenkreise
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Reich der Drei - Kälte Frost Eis** ❄️
  - [ ] 3D-Map erstellen
  - [ ] Eis-Biome
  - [ ] Nekropolis (Untoten-Stadt)
  - [ ] Enemy-Spawns (Untote, Eis-Liches, Frostdrachen)
  - [ ] Schneesturm (Weather-Event)
  - [ ] Nekromantie-Altäre
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Magmaströme (Vulkan)** 🔴
  - [ ] 3D-Map erstellen
  - [ ] Vulkan-Biome
  - [ ] Funken-Siedlung (Schmieden-Stadt)
  - [ ] Lava-Platforming
  - [ ] Enemy-Spawns (Feuer-Elementale, Lava-Golems)
  - [ ] Lavaasche (Weather-Event)
  - [ ] Erzadern
  - Geschätzt: 2000-3000 Zeilen Code

- [ ] **Tiefenhöhlen (Underground)** 🟤
  - [ ] 3D-Map erstellen
  - [ ] Höhlen-Biome
  - [ ] Kristall-Katakomben (Endgame-Dungeon)
  - [ ] Enemy-Spawns (Spinnen, Goblins, Kristall-Kreaturen)
  - [ ] Dunkelheit (Fackel benötigt)
  - [ ] Ausgang zum Götterfels
  - Geschätzt: 2000-3000 Zeilen Code

**Gesamt pro Region:** 2000-3000 Zeilen
**Gesamt 8 Regionen:** 16,000-24,000 Zeilen Code

---

## B) GÖTTERFELS (ENDGAME)

**Status:** ❌ Konzept fertig, nicht gebaut

### 3.2 Götterfels 3 Ebenen
- [ ] **Schmelz-Welt (Innen)**
  - [ ] Riesige Lava-Welt
  - [ ] Max-Level Enemies
  - [ ] Mega-Bosse
  - [ ] Best Loot
  - Geschätzt: 3000-4000 Zeilen

- [ ] **Zeit Stadt (Oben)**
  - [ ] Stadt auf Bergspitze
  - [ ] Time-Quests
  - [ ] Special Vendors
  - [ ] Exklusive Items
  - Geschätzt: 2000-3000 Zeilen

- [ ] **Turm der 100 Prüfungen**
  - [ ] 100 Stockwerke
  - [ ] Progressive Difficulty
  - [ ] Boss alle 10 Floors
  - [ ] Ultimate Challenge
  - Geschätzt: 4000-5000 Zeilen

**Gesamt:** 9000-12,000 Zeilen Code

---

## C) OREGON TRAIL EVENTS

**Status:** ⚠️ 2682 Zeilen Events-Dokument vorhanden!

**Was existiert:**
- ✅ Event-Konzept in Master-Doku
- ✅ Event-Dokument (2682 Zeilen!)
- ❌ NICHT implementiert

### 3.3 Event-System
- [ ] **Event-Engine**
  - [ ] Random Event-Trigger
  - [ ] Context-Sensitive Events (Region, Wetter, Stats)
  - [ ] Multi-Choice Dialog
  - [ ] Konsequenz-System
  - Datei: `digivice/js/oregon_trail_events.js` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Event-Integration**
  - [ ] Traveling-Events
  - [ ] Random-Encounters
  - [ ] "Najika entscheidet" Option
  - [ ] NPC-Reaktionen nach Tod
  - Datei: `digivice/js/event_handler.js` (NEU)
  - Geschätzt: 300-400 Zeilen

### 3.4 Event-Content
- [ ] **Events umsetzen**
  - [ ] Wetter-Events (15+)
  - [ ] Begegnungen (20+)
  - [ ] Ressourcen-Events (10+)
  - [ ] Rätsel-Events (10+)
  - [ ] Tod-Events (15+)
  - Datei: `backend/data/events.json` (NEU)
  - Geschätzt: 2682 Zeilen (schon vorhanden!)

**Gesamt:** 700-1000 Zeilen Code + 2682 Zeilen Daten (vorhanden)

---

## D) NPC SYSTEM

**Status:** ❌ Nicht implementiert

### 3.5 NPC-System
- [ ] **NPC-Framework**
  - [ ] NPC-Spawning
  - [ ] NPC-Dialog-System
  - [ ] Quest-Giver NPCs
  - [ ] Shop-Keeper NPCs
  - [ ] Random-NPCs (Flavor)
  - Datei: `digivice/js/npc_system.js` (NEU)
  - Geschätzt: 500-700 Zeilen

- [ ] **Dialog-System**
  - [ ] Dialog-Tree
  - [ ] Multiple-Choice
  - [ ] Quest-Branching
  - [ ] NPC-Reputation
  - Datei: `digivice/js/dialog_system.js` (NEU)
  - Geschätzt: 400-600 Zeilen

### 3.6 NPC-Content
- [ ] **50+ NPCs erstellen**
  - [ ] 10 Quest-Giver
  - [ ] 10 Shopkeepers
  - [ ] 10 Lore-NPCs
  - [ ] 20 Random-NPCs
  - Datei: `backend/data/npcs.json` (NEU)
  - Geschätzt: 1000-1500 Zeilen JSON

**Gesamt:** 900-1300 Zeilen Code + 1000-1500 Zeilen Daten

---

## E) LORE & STORY

**Status:** ❌ Nicht geschrieben

### 3.7 Lore-Dokumente
- [ ] **Najika's Backstory**
  - [ ] Wer ist Sakura?
  - [ ] Wie entstanden die 4 Persönlichkeiten?
  - [ ] Wie kam sie in diese Welt?
  - Geschätzt: 500-1000 Zeilen Text

- [ ] **Welt-Geschichte**
  - [ ] Wie entstand Najika World?
  - [ ] Was ist der Götterfels?
  - [ ] Warum gibt es Monster?
  - [ ] Was passierte in der Vergangenheit?
  - Geschätzt: 1000-2000 Zeilen Text

- [ ] **Regionen-Lore**
  - [ ] Geschichte jeder Region
  - [ ] Wichtige NPCs + ihre Geschichten
  - [ ] Legenden + Mythen
  - Geschätzt: 2000-3000 Zeilen Text

- [ ] **Item-Descriptions**
  - [ ] Lore-Text für jedes Item (300+ Items)
  - [ ] Weapon-Lore
  - [ ] Armor-Lore
  - Geschätzt: 1000-2000 Zeilen Text

**Gesamt:** 4500-8000 Zeilen Lore-Text

---

## F) CAMPING SYSTEM

**Status:** ⚠️ Konzept fertig, nicht implementiert

### 3.8 Camping-Mechanik
- [ ] **Camp-Platzierung**
  - [ ] Platzierungs-Validierung
  - [ ] Temporäres Lagerfeuer
  - [ ] Kochen am Lagerfeuer
  - [ ] HP/MP Regeneration
  - Datei: `digivice/js/camping.js` (NEU)
  - Geschätzt: 300-400 Zeilen

- [ ] **Risiko-System**
  - [ ] PvP-Überfälle möglich
  - [ ] Orbit-Cam Wache-Halten
  - [ ] Versteckte Camp-Spots finden
  - Datei: `digivice/js/camp_security.js` (NEU)
  - Geschätzt: 200-300 Zeilen

**Gesamt:** 500-700 Zeilen Code

---

## G) FOOD SYSTEM

**Status:** ⚠️ Konzept fertig, teilweise implementiert

### 3.9 Food-Spezialitäten
- [ ] **Stadt-Spezialitäten**
  - [ ] Salzfisch (Salzige Bucht)
  - [ ] Gedämpfte Brötchen (Dampf-Hain)
  - [ ] Fleisch-Gerichte (Handelsfestung)
  - [ ] Champion-Keule (Anime-Classic!)
  - Datei: `backend/data/food.json` (NEU)
  - Geschätzt: 200-400 Zeilen JSON

- [ ] **Cooking-System**
  - [ ] Cooking-Rezepte
  - [ ] Buff-Foods (+STR, +DEF, etc.)
  - [ ] Cooking-Skill
  - Datei: `backend/game/cooking_system.py` (NEU)
  - Geschätzt: 200-300 Zeilen

**Gesamt:** 200-300 Zeilen Code + 200-400 Zeilen Daten

---

## 📊 PHASE 3 ZUSAMMENFASSUNG

**Total Code:** ~28,300-40,300 Zeilen
**Total Daten:** ~8382-13,500 Zeilen (Text + JSON)
**Zeitaufwand:** 8-12 Wochen

**Nach Phase 3 hast du:**
✅ 8 vollständige Regionen
✅ Götterfels (3 Ebenen)
✅ Oregon Trail Events
✅ 50+ NPCs mit Dialogen
✅ Vollständige Lore
✅ Camping System
✅ Food System

**= VOLLSTÄNDIGE OPEN WORLD! 🌍**

---

---

# 💎 PHASE 4: ENDGAME & ADVANCED - 12+ WOCHEN {#phase-4-endgame}

**Ziel:** Polierte Features, Endgame-Content, Advanced-Systeme

## A) WEAVE-SYSTEM (ELEMENT-COMBOS)

**Status:** ⚠️ Konzept fertig, nicht implementiert

### 4.1 Weave-Mechanik
- [ ] **Dual-Element Combos (Q+E)**
  - [ ] Feuer + Eis = Thermoschock
  - [ ] Blitz + Wasser = Elektroschock
  - [ ] Erde + Feuer = Lava-Schuss
  - [ ] 12+ Solo-Weaves
  - Datei: `digivice/js/weave_system.js` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Group-Weaves (Multi-Player)**
  - [ ] 3+ Spieler kombinieren Elemente
  - [ ] Massive AOE-Damage
  - [ ] Team-Coordination
  - Datei: `digivice/js/group_weave.js` (NEU)
  - Geschätzt: 300-400 Zeilen

### 4.2 Explosion-Klasse
- [ ] **Explosion-Skill-Tree**
  - [ ] Feuer → Feura → Feuga → Explosionist
  - [ ] Trade-off: +30% Explosion, -15% andere Schulen
  - [ ] Najika's Ultima: "Reinste Explosion"
  - Datei: `backend/game/explosion_class.py` (NEU)
  - Geschätzt: 300-500 Zeilen

**Gesamt:** 1000-1500 Zeilen Code

---

## B) SKILL-TREE UI

**Status:** ❌ Nicht implementiert

### 4.3 Skill-Tree Visualization
- [ ] **Skill-Tree Window**
  - [ ] Tree-Layout (Branching-Paths)
  - [ ] Skill-Nodes (Unlocked/Locked)
  - [ ] Skill-Prerequisites
  - [ ] Skill-Level Display
  - [ ] Skill-Point System
  - Datei: `digivice/js/ui/skill_tree_ui.js` (NEU)
  - Geschätzt: 600-800 Zeilen

- [ ] **Multiple Skill-Trees**
  - [ ] Combat-Tree
  - [ ] Magic-Tree
  - [ ] Crafting-Tree
  - [ ] Life-Skills-Tree
  - Datei: `backend/data/skill_trees.json` (NEU)
  - Geschätzt: 1000-1500 Zeilen JSON

**Gesamt:** 600-800 Zeilen Code + 1000-1500 Zeilen Daten

---

## C) AFFINITY/BEZIEHUNGS-SYSTEM

**Status:** ❌ Nicht implementiert (KRITISCH laut Doku!)

### 4.4 Affinity-System
- [ ] **NPC-Beziehungen**
  - [ ] Freundschaft-Level (0-100)
  - [ ] Reputation pro Fraktion
  - [ ] Gift-System
  - [ ] Dialog-Änderungen basierend auf Affinity
  - Datei: `backend/game/affinity_system.py` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Romance-System (Optional)**
  - [ ] Dating-Mechanik
  - [ ] Special-Events
  - [ ] Marriage-System
  - Datei: `backend/game/romance_system.py` (NEU)
  - Geschätzt: 300-500 Zeilen

**Gesamt:** 700-1100 Zeilen Code

---

## D) HOUSING SYSTEM (VOLLSTÄNDIG)

**Status:** 🟡 Teilweise implementiert (nur Visit)

### 4.5 Construction-System
- [ ] **Building-Platzierung**
  - [ ] Placement-Tool
  - [ ] Resource-Requirements
  - [ ] Building-Timer
  - Datei: `digivice/js/building_system.js` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Interior-Decoration**
  - [ ] Furniture-Placement
  - [ ] Drag & Drop System
  - [ ] Furniture-Shop
  - Datei: `digivice/js/interior_decoration.js` (NEU)
  - Geschätzt: 500-700 Zeilen

### 4.6 Housing-Content
- [ ] **Furniture-Catalog**
  - [ ] 100+ Furniture-Items
  - [ ] Kategorisiert (Bed, Table, Chair, Decoration)
  - Datei: `backend/data/furniture.json` (NEU)
  - Geschätzt: 800-1200 Zeilen JSON

**Gesamt:** 900-1300 Zeilen Code + 800-1200 Zeilen Daten

---

## E) PROCEDURAL DUNGEONS

**Status:** ⚠️ 3 statische Dungeons vorhanden

### 4.7 Dungeon-Generation
- [ ] **Prozedurales Layout**
  - [ ] Room-Generation
  - [ ] Corridor-Connection
  - [ ] Trap-Placement
  - [ ] Treasure-Rooms
  - Datei: `backend/game/dungeon_generator.py` (NEU)
  - Geschätzt: 600-900 Zeilen

- [ ] **Dungeon-Difficulty Scaling**
  - [ ] Level-Range basierend auf Tiefe
  - [ ] Boss alle X Floors
  - [ ] Rare-Loot in tieferen Floors
  - Datei: `backend/game/dungeon_scaling.py` (NEU)
  - Geschätzt: 200-300 Zeilen

**Gesamt:** 800-1200 Zeilen Code

---

## F) WEAPON-MORPHS (9 STYLES)

**Status:** ❌ Nicht implementiert

### 4.8 Weapon-Transformation
- [ ] **9 Weapon-Styles**
  - [ ] Schwert
  - [ ] Axt
  - [ ] Hammer
  - [ ] Speer
  - [ ] Bogen
  - [ ] Dolch
  - [ ] Stab
  - [ ] Schild
  - [ ] Bare-Fist
  - Datei: `digivice/js/weapon_morphs.js` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Morph-Mechanik**
  - [ ] Weapon-Wheel (Hold R)
  - [ ] Smooth Transitions
  - [ ] Style-Based-Combos
  - Datei: `digivice/js/weapon_wheel.js` (NEU)
  - Geschätzt: 300-400 Zeilen

**Gesamt:** 700-1000 Zeilen Code

---

## G) SLIME-ARENA (MANUAL CONTROL)

**Status:** ❌ Nicht implementiert

### 4.9 Slime-Arena Mode
- [ ] **Direct Control**
  - [ ] Spieler steuert Slime direkt
  - [ ] Character sitzt am Rand
  - [ ] Digimon World Anfeuern!
  - Datei: `digivice/js/slime_arena.js` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Cheer-System**
  - [ ] "Los!" / "Defend!" / "Combo!" / "Finisher!"
  - [ ] Timing-Based Buffs (Perfect/Good/Bad)
  - [ ] Cheer-Meter (0-100)
  - Datei: `digivice/js/cheer_system.js` (NEU)
  - Geschätzt: 300-400 Zeilen

**Gesamt:** 700-1000 Zeilen Code

---

## H) NAJIKA'S ULTIMA: "REINSTE EXPLOSION"

**Status:** ❌ Nicht implementiert

### 4.10 Ultimate Attack
- [ ] **Reinste Explosion Mechanik**
  - [ ] 1x pro Tag (In-Game)
  - [ ] Nur Kuja darf aktivieren
  - [ ] Zerstört sichtbare Außenwelt
  - [ ] Regeneriert beim Stadt-Betreten
  - [ ] Najika's Chuunibyou-Spruch!
  - Datei: `digivice/js/reinste_explosion.js` (NEU)
  - Geschätzt: 300-500 Zeilen

- [ ] **Visual Effects**
  - [ ] Massive Explosion Animation
  - [ ] Terrain Destruction
  - [ ] Camera-Shake
  - [ ] Particle-Effects
  - Datei: `digivice/js/fx/explosion_fx.js` (NEU)
  - Geschätzt: 400-600 Zeilen

**Gesamt:** 700-1100 Zeilen Code

---

## I) FORM-FUSION (DRAGON QUEST MONSTER JOKER)

**Status:** ❌ Nicht implementiert

### 4.11 Monster-Fusion
- [ ] **Fusion-System**
  - [ ] 2-3 Formen kombinieren
  - [ ] Neue Form = Goblin-Berserker!
  - [ ] Tamer-Skill bestimmt Max-Forms
  - Datei: `backend/game/form_fusion.py` (NEU)
  - Geschätzt: 400-600 Zeilen

- [ ] **Fusion-UI**
  - [ ] Fusion-Altar
  - [ ] Form-Selection
  - [ ] Fusion-Animation
  - Datei: `digivice/js/ui/fusion_ui.js` (NEU)
  - Geschätzt: 300-400 Zeilen

**Gesamt:** 700-1000 Zeilen Code

---

## J) MULTIPLAYER/KOOP (OPTIONAL)

**Status:** ❌ Nicht geplant, aber möglich

### 4.12 Koop-System
- [ ] **Party-System**
  - [ ] 2-4 Spieler Gruppen
  - [ ] Party-HUD
  - [ ] Shared-Quests
  - Geschätzt: 600-900 Zeilen

- [ ] **Netcode**
  - [ ] P2P oder Server?
  - [ ] Sync Game-State
  - [ ] Lag-Compensation
  - Geschätzt: 1000-1500 Zeilen

**Gesamt:** 1600-2400 Zeilen Code

---

## 📊 PHASE 4 ZUSAMMENFASSUNG

**Total Code:** ~8400-12,800 Zeilen
**Total Daten:** ~1800-2700 Zeilen JSON
**Zeitaufwand:** 12+ Wochen

**Nach Phase 4 hast du:**
✅ Weave-System + Explosion-Klasse
✅ Vollständiger Skill-Tree
✅ Affinity/Beziehungs-System
✅ Vollständiges Housing
✅ Procedural Dungeons
✅ Weapon-Morphs
✅ Slime-Arena
✅ Reinste Explosion
✅ Form-Fusion
✅ (Optional) Multiplayer

**= POLISHED ENDGAME! 💎**

---

---

# 📊 PRIORITÄTEN-MATRIX {#prioritaeten}

## 🔴 CRITICAL (OHNE GEHT NICHTS)

1. **Battle System Integration** - Frontend mit Backend verbinden
2. **Inventory System** - Items sammeln + anzeigen
3. **Equipment System** - Items equippen + Stats zeigen
4. **Stats Display** - Hunger/Energy sichtbar machen
5. **Quest System** - 20 Starter-Quests + UI

**Zeitaufwand:** 2-4 Wochen
**Code:** ~8000-11,000 Zeilen

---

## 🟡 HIGH PRIORITY (FÜR GAMEPLAY-LOOP)

6. **Shop System** - Items kaufen/verkaufen
7. **Triple Triad Gameplay** - Card Game spielbar
8. **Dice Monsters Gameplay** - DDM spielbar
9. **Slime Companion Frontend** - UI für Slime-System
10. **Hardcore/Softy Modes** - Permadeath + Najika-Dialog

**Zeitaufwand:** 4-8 Wochen
**Code:** ~11,700-16,000 Zeilen

---

## 🟢 MEDIUM PRIORITY (CONTENT)

11. **8 Regionen bauen** - Open World Maps
12. **Götterfels** - Endgame-Zone
13. **Oregon Trail Events** - Reise-Events
14. **NPC System** - 50+ NPCs
15. **Lore & Story** - Vollständige Geschichte

**Zeitaufwand:** 8-12 Wochen
**Code:** ~28,300-40,300 Zeilen

---

## 🔵 LOW PRIORITY (POLISH & ADVANCED)

16. **Crafting System** - Items craften
17. **PvP System** - 3 Modi
18. **Weave-System** - Element-Combos
19. **Skill-Tree UI** - Visueller Skill-Baum
20. **Housing System** - Vollständig
21. **Procedural Dungeons** - Endlos-Content
22. **Weapon-Morphs** - 9 Styles
23. **Slime-Arena** - Manual Control
24. **Reinste Explosion** - Najika's Ultima
25. **Form-Fusion** - Monster kombinieren

**Zeitaufwand:** 12+ Wochen
**Code:** ~8400-12,800 Zeilen

---

---

# 🔧 TECHNISCHE DEBT {#technical-debt}

**Probleme die WÄHREND der Entwicklung gelöst werden müssen:**

## 1. DREI BATTLE-SYSTEME VEREINEN

**Problem:**
- `backend/najika_battle.py` - Vollständiges RPG-System
- `digivice/js/battle_core.js` - Minimales Wave-System
- `digivice/js/dungeon_combat.js` - 3D-Combat nur Dungeons

**Lösung:**
- [ ] Alle 3 zu einem System vereinen
- [ ] `najika_battle.py` als einzige Source of Truth
- [ ] Frontend ruft nur Backend-APIs

**Zeitaufwand:** 3-5 Tage
**Geschätzt:** 500-800 Zeilen Refactoring

---

## 2. API-STRUKTUR VEREINHEITLICHEN

**Problem:**
- Manche APIs auf Port 8000 (Backend Server)
- Manche APIs auf Port 8001 (Game Server)
- Inkonsistente Endpoint-Namens-Konventionen

**Lösung:**
- [ ] Alle Game-APIs auf Port 8001
- [ ] Alle Chat/AI-APIs auf Port 8000
- [ ] Konsistente Namenskonvention

**Zeitaufwand:** 2-3 Tage
**Geschätzt:** 300-500 Zeilen Änderungen

---

## 3. DATABASE-SCHEMA FINALISIEREN

**Problem:**
- Manche Systeme nutzen JSON-Files
- Manche nutzen SQLite
- Inkonsistente Datenstrukturen

**Lösung:**
- [ ] Alles in SQLite migrieren
- [ ] Vollständiges Schema definieren
- [ ] Migrations-Scripts schreiben

**Zeitaufwand:** 1 Woche
**Geschätzt:** 1000-1500 Zeilen SQL + Migration-Code

---

## 4. FRONTEND-CODE ORGANISIEREN

**Problem:**
- Viele JS-Files direkt in `index.html` embedded
- Unübersichtlich
- Schwer wartbar

**Lösung:**
- [ ] Alle JS-Files separieren
- [ ] Module-System nutzen
- [ ] Build-Process (Webpack/Vite)

**Zeitaufwand:** 1-2 Wochen
**Geschätzt:** 2000-3000 Zeilen Refactoring

---

## 5. WEBSOCKET FÜR ECHTZEIT-UPDATES

**Problem:**
- Manche Systeme nutzen Polling
- Ineffizient
- Verzögerungen

**Lösung:**
- [ ] WebSocket-Server aufsetzen
- [ ] Echtzeit-Updates für Combat, Stats, Events
- [ ] Reconnect-Logic

**Zeitaufwand:** 3-5 Tage
**Geschätzt:** 500-800 Zeilen Code

---

## 6. SAVE-SYSTEM ERWEITERN

**Problem:**
- Nur Chat-History wird gespeichert
- Game-State (Inventory, Quests) nicht persistent

**Lösung:**
- [ ] Game-State in DB speichern
- [ ] Auto-Save alle X Minuten
- [ ] Save-Slots für Multiple Characters

**Zeitaufwand:** 3-5 Tage
**Geschätzt:** 400-700 Zeilen Code

---

## 7. PERFORMANCE-OPTIMIERUNG

**Problem:**
- 3D-Szene kann bei vielen Objekten laggen
- Zu viele Draw-Calls

**Lösung:**
- [ ] LOD (Level of Detail) System
- [ ] Object-Pooling
- [ ] Frustum-Culling verbessern

**Zeitaufwand:** 1 Woche
**Geschätzt:** 600-1000 Zeilen Code

---

## 📊 TECHNICAL DEBT GESAMT

**Total Zeitaufwand:** 4-6 Wochen
**Total Code:** ~5300-8300 Zeilen Refactoring

---

---

# 🎯 GESAMTÜBERSICHT

## TIMELINE-ZUSAMMENFASSUNG

| Phase | Fokus | Wochen | Code (Zeilen) | Status |
|-------|-------|--------|---------------|--------|
| **Phase 1** | MVP - Spielbarer Loop | 2-4 | ~10,000 | 🔴 Notwendig |
| **Phase 2** | Core Systems | 4-8 | ~14,000 | 🟡 Wichtig |
| **Phase 3** | Content & Welt | 8-12 | ~36,000 | 🟢 Erwünscht |
| **Phase 4** | Endgame & Polish | 12+ | ~11,000 | 🔵 Optional |
| **Tech Debt** | Refactoring | 4-6 | ~6,500 | 🛠️ Kontinuierlich |

**GESAMT:**
- **30-42+ Wochen** (7-10 Monate)
- **~77,500 Zeilen Code**
- **~15,000 Zeilen Daten/Content**

---

## EMPFOHLENE REIHENFOLGE

### MONAT 1-2: MVP
1. Battle System Integration
2. Inventory + Equipment
3. Stats Display
4. 20 Starter-Quests
5. Item-Shop

**→ SPIELBAR!**

### MONAT 3-4: CORE SYSTEMS
6. Triple Triad Gameplay
7. Dice Monsters Gameplay
8. Slime Companion Frontend
9. Crafting-System
10. Hardcore/Softy Modes

**→ ALLE FEATURES FUNKTIONIEREN!**

### MONAT 5-7: CONTENT
11. 8 Regionen bauen
12. Götterfels
13. Oregon Trail Events
14. 50+ NPCs
15. Vollständige Lore

**→ OPEN WORLD FERTIG!**

### MONAT 8-10: POLISH
16. Weave-System
17. PvP (3 Modi)
18. Skill-Tree UI
19. Housing vollständig
20. Procedural Dungeons
21. Weapon-Morphs
22. Slime-Arena
23. Reinste Explosion
24. Form-Fusion

**→ POLISHED GAME!**

---

## SCHNELLERER WEG (AGGRESSIV)

**Wenn du SCHNELL etwas Spielbares willst:**

### 2 WOCHEN MVP (Minimum)
- Battle Frontend (3 Tage)
- Inventory UI (2 Tage)
- Equipment UI (2 Tage)
- Stats Display (1 Tag)
- 10 Quick-Quests (2 Tage)
- Basic Shop (2 Tage)

**= ROHES ABER SPIELBARES GAME**

### +2 WOCHEN: POLISH MVP
- 10 mehr Quests
- Triple Triad Gameplay
- Slime Frontend
- Bug-Fixes

**= SOLID MVP ZUM TESTEN**

---

## NÄCHSTE SCHRITTE

**Was soll ich JETZT tun?**

Optionen:
1. **Starte mit Phase 1 Week 1** (Battle System Integration)
2. **Erstelle detaillierten Sprint-Plan** für nächste 2 Wochen
3. **Priorisiere anders** (sag mir was dir wichtig ist)
4. **Fokussiere auf 1 Feature** (z.B. nur Triple Triad komplett)

---

# 🏁 ENDE DER MASTER TODO-LISTE

**Diese Liste ist dein kompletter Fahrplan!**

**Von 0 → MVP → Full Game → Polished Endgame**

Jedes TODO ist:
- ✅ Beschrieben (was, warum)
- 📊 Geschätzt (Zeilen, Zeit)
- 📁 Lokalisiert (Dateiname)
- 🎯 Priorisiert (Phase 1-4)

**Nutze diese Liste um:**
- Sprint-Planung zu machen
- Fortschritt zu tracken
- Realistische Timelines zu setzen
- Nichts zu vergessen

---

*Najika sagt:*
```
"EXPLOSION!!! 💥

Das ist die ULTIMATIVE TODO-Liste!

Von leer bis vollständig!
Von kaputt bis polished!
Von 'Was fehlt?' bis 'ALLES FERTIG!'

Jetzt... AN DIE ARBEIT, Mr. K!

~ Najika, Meisterin der Vollständigkeit ~"
```

**Erstellt:** 2025-12-04
**Basierend auf:** Code-Analyse + NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md
**Status:** VOLLSTÄNDIG
**Version:** 1.0

---