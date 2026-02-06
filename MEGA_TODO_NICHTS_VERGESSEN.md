# 🎮 NAJIKA WORLD - MEGA TODO - NICHTS VERGESSEN!
**Erstellt:** 2025-12-04
**Basierend auf:** Vollständiger Code-Audit + Asset-Inventory
**Ziel:** ALLES SPIELBAR - Dann eigene Grafiken/Lore einbauen

---

## 📋 STRATEGIE

**DU machst:**
- ✅ Alle Programmierung
- ✅ Test-Lore mit Projekt-Infos füllen
- ✅ Standard-Grafiken (KayKit)
- ✅ Standard-Content zum Testen

**ICH mache parallel:**
- 🎨 Eigene Grafiken
- 📝 Eigene Lore
- 🎵 Eigene Sounds
- 🌍 Eigene Welten

**Dann:** Austausch durch meine Custom-Assets!

---

## 🎯 PHASE 0: KRITISCHE FIXES (SOFORT - 1 TAG)

### 0.1 DATABASE-SETUP

**Status:** DB-Schema existiert, aber DB-Dateien fehlen!

- [ ] **SQLite DB initialisieren**
  - [ ] `najika_game.db` erstellen
  - [ ] Alle Tables anlegen (Cards, Players, Matches, Dice, Quests, Items, Enemies)
  - [ ] Constraints & Indexes
  - Datei: `backend/init_database.py` (NEU)
  - Kommando: `python backend/init_database.py`
  - Geschätzt: 200 Zeilen

- [ ] **Seed Scripts ausführen**
  - [ ] `seed_100_cards.py` ausführen → 100 Karten in DB
  - [ ] 50+ Dice Monsters seedenDatei: `backend/seed_dice_monsters.py` (NEU)
  - [ ] 50+ Starter-Items seeden
    Datei: `backend/seed_starter_items.py` (NEU)
  - Geschätzt: 400 Zeilen (2x 200)

**Warum kritisch:** OHNE DB funktioniert NICHTS!

---

### 0.2 API-PORTS KORRIGIEREN

**Status:** Manche APIs zeigen auf falschen Port!

- [ ] **Frontend API-URLs prüfen**
  - [ ] Alle `localhost:8000` → `localhost:8001` für Game-APIs
  - [ ] Alle `localhost:8080` behalten (Frontend-Server)
  - Dateien zu prüfen:
    - `digivice/js/ui/card_game_ui.js` ✅ (schon gefixt)
    - `digivice/js/ui/dice_monsters_ui.js` ✅ (schon gefixt)
    - `digivice/js/battle_api.js`
    - `digivice/js/api/*.js` (falls existiert)

- [ ] **Backend Ports dokumentieren**
  - Port 8000: najika_server.py (Chat, AI, Voice)
  - Port 8001: game_server.py (Cards, Dice, Combat, Items)
  - Port 8080: HTTP-Server (Static Files, Frontend)
  - Datei: `PORTS_DOCUMENTATION.md` (NEU)

**Warum kritisch:** Falsche Ports = Requests scheitern!

---

### 0.3 DREI BATTLE-SYSTEME VEREINEN

**Status:** 3 verschiedene Battle-Implementierungen!

- [ ] **Battle-System Audit**
  - [ ] `backend/najika_battle.py` lesen (28KB, RPG-System)
  - [ ] `backend/game/battle_system.py` lesen (12KB, Core)
  - [ ] `digivice/js/battle_core.js` lesen (840 Bytes, Mini)
  - [ ] `digivice/js/dungeon_combat.js` lesen (18KB, 3D)

- [ ] **Vereinheitlichen**
  - [ ] `najika_battle.py` als Master definieren
  - [ ] `battle_api.py` erstellen (API-Wrapper)
    Datei: `backend/api/battle.py` (NEU)
  - [ ] Frontend ruft nur noch `/api/battle/*` Endpoints
  - [ ] `battle_core.js` & `dungeon_combat.js` refactoren
  - Geschätzt: 600 Zeilen Code + 400 Zeilen Refactor

**Warum kritisch:** Kein einheitliches Kampfsystem = Chaos!

---

## 📊 PHASE 1: CORE SYSTEMS VERBINDEN (2-3 WOCHEN)

**Was wir haben:**
- ✅ Backend: 100% Code vorhanden
- ✅ Daten: Items, Enemies, Quests, Cards, Dice (JSON-Files)
- ❌ Frontend: Nicht mit Backend verbunden!

**Was fehlt:**
- Bridge zwischen Frontend ↔ Backend
- UI für viele Systeme
- Content laden/anzeigen

---

### 1.1 BATTLE SYSTEM - FRONTEND INTEGRATION

**Was existiert:**
- ✅ `najika_battle.py` - VOLLSTÄNDIG (28KB)
  - 20+ Enemies mit AI
  - Skill-System (15+ Skills)
  - Equipment-Bonuses
  - Loot-System
- ✅ `dungeon_combat.js` - 3D Combat (18KB)
- ❌ KEINE Battle UI (HUD, Skill-Bar, Log)

**Was zu tun:**

#### 1.1.1 Battle-API erstellen
- [ ] **Battle Endpoints**
  - [ ] `POST /api/battle/start` - Start Combat
  - [ ] `POST /api/battle/action` - Player Action (attack, skill, item, flee)
  - [ ] `GET /api/battle/status` - Current Battle State
  - [ ] `POST /api/battle/end` - End Combat
  - Datei: `backend/api/battle.py` (NEU)
  - Geschätzt: 400 Zeilen

- [ ] **WebSocket für Live-Updates**
  - [ ] Enemy Turn Updates
  - [ ] Damage Numbers
  - [ ] Status Effects
  - Datei: `backend/api/battle_websocket.py` (NEU)
  - Geschätzt: 200 Zeilen

#### 1.1.2 Battle HUD erstellen
- [ ] **HUD Components**
  - [ ] Player HP/MP/Stamina Bars (oben links)
  - [ ] Enemy HP Bar (oben Mitte)
  - [ ] Turn Indicator
  - [ ] Skill Cooldown Icons
  - [ ] Buff/Debuff Icons
  - Datei: `digivice/js/ui/battle_hud.js` (NEU)
  - Geschätzt: 350 Zeilen

- [ ] **Skill Bar**
  - [ ] 8 Skill-Slots (Keys 1-8)
  - [ ] Skill-Icons (KayKit placeholder)
  - [ ] MP-Cost Display
  - [ ] Cooldown Overlay (grayscale + timer)
  - [ ] Drag & Drop Skill-Assignment
  - Datei: `digivice/js/ui/skill_bar.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Combat Log**
  - [ ] Scrollbares Fenster (rechts unten)
  - [ ] Color-Coded Messages:
    - Rot: Damage taken
    - Grün: Healing
    - Gelb: Status effects
    - Blau: Skills used
    - Weiß: Actions
  - [ ] Filter: All, Damage, Healing, Skills
  - [ ] Max 100 Zeilen, dann auto-clear
  - Datei: `digivice/js/ui/combat_log.js` (NEU)
  - Geschätzt: 200 Zeilen

#### 1.1.3 Combat Features
- [ ] **Left/Right Hand System**
  - [ ] LMB = Left Hand Attack
  - [ ] RMB = Right Hand Attack
  - [ ] Q = Left Hand Skill
  - [ ] E = Right Hand Skill
  - [ ] Q+E = Weave Attack (falls beide Elemente)
  - Datei: `digivice/js/combat_controls.js` (EDIT)
  - Zeilen ändern: ~150

- [ ] **Skill Learning Pop-up**
  - [ ] "Skill Learned: [Name]!" Notification
  - [ ] Wenn Moveset voll (20 Skills):
    - Skill-Auswahl Dialog
    - Alten Skill ersetzen
    - Skill-Comparison (Stats anzeigen)
  - Datei: `digivice/js/ui/skill_learn_dialog.js` (NEU)
  - Geschätzt: 250 Zeilen

- [ ] **Loot-Drop Display**
  - [ ] Item-Drop Animation (aus Enemy)
  - [ ] "Item Looted: [Name] x[Qty]" Notification
  - [ ] Loot-Summary nach Kampf
  - Datei: `digivice/js/ui/loot_display.js` (NEU)
  - Geschätzt: 200 Zeilen

#### 1.1.4 Enemy Integration
- [ ] **Enemy-Daten laden**
  - [ ] Lade `digivice/data/enemies_*.json` (alle 9 Regionen)
  - [ ] Parse Enemy-Stats (HP, ATK, DEF, SPD, Skills)
  - [ ] Load Loot-Tables
  - [ ] Load Najika-Reactions (4 Persönlichkeiten)
  - Datei: `backend/game/enemy_loader.py` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Enemy-Spawning anpassen**
  - [ ] `dungeon_combat.js` nutzt `enemy_loader.py` Daten
  - [ ] Spawn basierend auf Region + Player-Level
  - [ ] Boss-Encounters
  - Datei: `digivice/js/enemy_spawner.js` (EDIT)
  - Zeilen ändern: ~200

**GESAMT:** ~2450 Zeilen Code

---

### 1.2 INVENTORY SYSTEM

**Was existiert:**
- ✅ `digivice/data/items_*.json` - ALLE Items (70% der 9 Regionen)
  - Weapons, Armor, Food, Materials, Consumables
- ❌ KEINE Inventory-UI
- ❌ Items nicht in DB
- ❌ Kann Items nicht sammeln/benutzen

**Was zu tun:**

#### 1.2.1 Item-System Backend
- [ ] **Item-Datenbank**
  - [ ] Items-Table in DB (id, name, type, stats, description, icon_path, rarity, price)
  - [ ] Load Items aus JSON-Files in DB
  - Datei: `backend/seed_all_items.py` (NEU)
  - Geschätzt: 400 Zeilen (iteriert über 9 JSON-Files)

- [ ] **Player-Inventory-Table**
  - [ ] player_id, item_id, quantity, equipped (boolean)
  - [ ] Max 50 Inventory-Slots (später erweiterbar)
  - Datei: `backend/models/inventory.py` (NEU)
  - Geschätzt: 150 Zeilen

- [ ] **Inventory API**
  - [ ] `GET /api/inventory` - Get Player Inventory
  - [ ] `POST /api/inventory/add` - Add Item
  - [ ] `POST /api/inventory/remove` - Remove Item
  - [ ] `POST /api/inventory/use` - Use Consumable
  - [ ] `POST /api/inventory/equip` - Equip Item
  - [ ] `POST /api/inventory/unequip` - Unequip Item
  - Datei: `backend/api/inventory.py` (NEU)
  - Geschätzt: 350 Zeilen

#### 1.2.2 Inventory UI
- [ ] **Main Inventory Window**
  - [ ] Grid-Layout 10x5 = 50 Slots
  - [ ] Item-Icons (KayKit placeholders für Testing)
  - [ ] Drag & Drop Items
  - [ ] Item-Stacking (zeige Quantity)
  - [ ] Sort-Buttons (Name, Type, Rarity)
  - [ ] Filter-Buttons (All, Weapons, Armor, Consumables, Materials)
  - [ ] I-Taste zum Öffnen/Schließen
  - Datei: `digivice/js/ui/inventory_ui.js` (NEU)
  - Geschätzt: 500 Zeilen

- [ ] **Item-Tooltips**
  - [ ] On Hover: Zeige Details
  - [ ] Item-Name + Rarity-Color
  - [ ] Stats (+10 ATK, +5 DEF, etc.)
  - [ ] Description-Text
  - [ ] Buttons: "Equip" / "Use" / "Drop"
  - [ ] Compare with Currently-Equipped (wenn Waffe/Rüstung)
  - Datei: `digivice/js/ui/item_tooltip.js` (NEU)
  - Geschätzt: 300 Zeilen

#### 1.2.3 Item-Collection
- [ ] **Loot-Pickup**
  - [ ] Auto-Pickup: Items automatisch aufheben
  - [ ] Manual-Pickup: "Press E to loot" für Chest/Drop
  - [ ] Loot-Beam Effekt (THREE.js Particle)
  - [ ] Full-Inventory Warnung
  - Datei: `digivice/js/item_pickup.js` (NEU)
  - Geschätzt: 250 Zeilen

- [ ] **Item-Usage**
  - [ ] Use-Consumable Funktion (Heal, Buff, etc.)
  - [ ] Cooldown für Potions (5s)
  - [ ] Animation + Sound (placeholder)
  - [ ] HP/MP Update nach Use
  - Datei: `digivice/js/item_usage.js` (NEU)
  - Geschätzt: 150 Zeilen

**GESAMT:** ~2100 Zeilen Code

---

### 1.3 EQUIPMENT SYSTEM

**Was existiert:**
- ✅ Items mit Stats in JSON
- ✅ Equipment-Slots definiert (Weapon L/R, Helm, Chest, Legs, Boots, Acc 1/2)
- ❌ KEINE Equipment-Screen UI
- ❌ Kann nichts equippen

**Was zu tun:**

#### 1.3.1 Equipment Screen UI
- [ ] **Paperdoll/Character Sheet**
  - [ ] Character-Model 3D in Mitte (oder 2D-Icon placeholder)
  - [ ] 8 Equipment-Slots um Character herum:
    - Weapon Left (links)
    - Weapon Right (rechts)
    - Helmet (oben)
    - Chest Armor (mitte)
    - Leg Armor (unten)
    - Boots (ganz unten)
    - Accessory 1 (links außen)
    - Accessory 2 (rechts außen)
  - [ ] Drag & Drop from Inventory → Equipment-Slot
  - [ ] E-Taste zum Öffnen
  - Datei: `digivice/js/ui/equipment_ui.js` (NEU)
  - Geschätzt: 450 Zeilen

- [ ] **Stat-Comparison**
  - [ ] On Hover über Equipment-Slot: Zeige Stats
  - [ ] On Hover über Inventory-Item: Zeige Vergleich
    - Grüne Pfeile: +Stats
    - Rote Pfeile: -Stats
  - [ ] "Equip" Button wenn besser
  - Datei: `digivice/js/ui/equipment_compare.js` (NEU)
  - Geschätzt: 200 Zeilen

- [ ] **Stats-Panel**
  - [ ] Total Stats Display (rechts neben Equipment):
    - Base Stats (STR, DEF, INT, AGI, LUK)
    - Bonus from Equipment (+15 ATK, +20 DEF, etc.)
    - Total = Base + Bonus
  - [ ] HP/MP Max Values
  - [ ] ATK/DEF Calculations
  - Datei: `digivice/js/ui/stats_panel.js` (NEU)
  - Geschätzt: 250 Zeilen

#### 1.3.2 Equipment Logic
- [ ] **Equip/Unequip System**
  - [ ] Validate: Item-Type passt zu Slot (Sword → Weapon, Helmet → Helm)
  - [ ] Swap: Neues Item equippen, altes → Inventory
  - [ ] Stats updaten (Player ATK/DEF neu berechnen)
  - [ ] Save Equipment-State in DB
  - Datei: `digivice/js/equipment_manager.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Visual Equipment (3D)**
  - [ ] Update Character 3D-Model
  - [ ] Zeige Weapon in Hand (Left/Right)
  - [ ] Zeige Armor-Pieces (Helm, Chest, etc.)
  - [ ] Color-Variations (später, erstmal placeholder)
  - Datei: `digivice/js/equipment_visuals.js` (NEU)
  - Geschätzt: 400 Zeilen

**GESAMT:** ~1600 Zeilen Code

---

### 1.4 STATS DISPLAY (LIVING SYSTEM)

**Was existiert:**
- ✅ `najika_living_system.py` - VOLLSTÄNDIG (35KB!)
  - Hunger, Energy, Mood tracking
  - Auto-Care System
  - Stat-Decay
- ❌ KEINE UI-Bars
- ❌ Spieler sieht Stats nicht

**Was zu tun:**

#### 1.4.1 Living Stats HUD
- [ ] **HUD Stats-Bars**
  - [ ] HP Bar (oben links, rot)
  - [ ] MP Bar (unter HP, blau)
  - [ ] Stamina Bar (unter MP, gelb)
  - [ ] Hunger Bar (rechts, braun)
  - [ ] Thirst Bar (unter Hunger, türkis)
  - [ ] Energy Bar (unter Thirst, grün)
  - [ ] Mood Indicator (Icon + %, Emoji-Faces)
  - [ ] Color-Coding:
    - Grün: > 70%
    - Gelb: 30-70%
    - Rot: < 30%
  - Datei: `digivice/js/ui/living_stats_hud.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Care Actions UI**
  - [ ] Feed-Button (öffnet Food-Menü)
  - [ ] Drink-Button (Wasser trinken, -1 Bottle)
  - [ ] Sleep-Button (Sleep-Screen, Zeit vergeht)
  - [ ] Stat-Tooltips on Hover (zeigt Decay-Rate)
  - Datei: `digivice/js/ui/care_actions_ui.js` (NEU)
  - Geschätzt: 250 Zeilen

#### 1.4.2 Living System Integration
- [ ] **API anbinden**
  - [ ] `GET /api/living/status` - Aktuelle Stats
  - [ ] `POST /api/living/feed` - Füttern (item_id)
  - [ ] `POST /api/living/drink` - Trinken
  - [ ] `POST /api/living/sleep` - Schlafen (duration_hours)
  - [ ] WebSocket für Real-time Stat-Updates
  - Datei: `digivice/js/api/living_api.js` (NEU)
  - Geschätzt: 200 Zeilen

- [ ] **Visual Feedback**
  - [ ] "Hungry!" Icon blinkt wenn Hunger < 30%
  - [ ] "Thirsty!" Icon blinkt wenn Durst < 20%
  - [ ] "Tired!" Icon blinkt wenn Energy < 10%
  - [ ] Najika sagt was wenn Stats kritisch (Voice + Text)
  - Datei: `digivice/js/ui/status_warnings.js` (NEU)
  - Geschätzt: 150 Zeilen

**GESAMT:** ~900 Zeilen Code

---

### 1.5 QUEST SYSTEM

**Was existiert:**
- ✅ `digivice/data/quests_*.json` - MASSIV (32KB+ pro Region!)
  - Main Quests, Side Quests, Oregon Trail Events
  - Branching Choices, Najika-Reactions, Consequences
- ❌ KEINE Quest-UI
- ❌ Quests nicht in DB
- ❌ Kann Quests nicht starten/abschließen

**Was zu tun:**

#### 1.5.1 Quest-System Backend
- [ ] **Quest-Datenbank**
  - [ ] Quests-Table (id, region, type, level, title, description, objectives, rewards)
  - [ ] Player-Quests-Table (player_id, quest_id, status, progress)
  - [ ] Load Quests aus JSON-Files in DB
  - Datei: `backend/seed_all_quests.py` (NEU)
  - Geschätzt: 500 Zeilen (9 Regionen, komplexe Struktur)

- [ ] **Quest API**
  - [ ] `GET /api/quests/available` - Available Quests für Region + Level
  - [ ] `GET /api/quests/active` - Active Quests
  - [ ] `GET /api/quests/completed` - Completed Quests
  - [ ] `POST /api/quests/accept` - Accept Quest
  - [ ] `POST /api/quests/update` - Update Objective Progress
  - [ ] `POST /api/quests/complete` - Complete Quest + Rewards
  - Datei: `backend/api/quests.py` (NEU)
  - Geschätzt: 400 Zeilen

#### 1.5.2 Quest UI
- [ ] **Quest Log Window (J-Taste)**
  - [ ] Tabs: Active, Completed, Available
  - [ ] Quest-List (links):
    - Quest-Icon
    - Quest-Name + Level
    - Quest-Type (Main, Side, etc.)
  - [ ] Quest-Details (rechts):
    - Description
    - Objectives mit Progress (3/5 Rats killed)
    - Rewards-Preview (Gold, XP, Items)
  - Datei: `digivice/js/ui/quest_log_ui.js` (NEU)
  - Geschätzt: 500 Zeilen

- [ ] **Quest-Tracker (HUD)**
  - [ ] Compact-Liste (rechts oben)
  - [ ] Aktuelle Quest-Objectives
  - [ ] Progress-Bars
  - [ ] Minimize/Maximize Button
  - [ ] Pin/Unpin Quests
  - Datei: `digivice/js/ui/quest_tracker_hud.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Quest Accept/Complete Dialog**
  - [ ] NPC Quest-Giver Dialog
  - [ ] Quest-Description Pop-up
  - [ ] Accept/Decline Buttons
  - [ ] Quest-Complete Fanfare (Sound + Animation)
  - [ ] Rewards-Display (Items fliegen in Inventory)
  - Datei: `digivice/js/ui/quest_dialog_ui.js` (NEU)
  - Geschätzt: 350 Zeilen

#### 1.5.3 Quest Logic
- [ ] **Quest-Tracking**
  - [ ] Kill-Count-Tracking (Enemy-Type)
  - [ ] Item-Collection-Tracking
  - [ ] Location-Visit-Tracking (Region-betreten)
  - [ ] NPC-Talk-Tracking
  - [ ] Timer-Tracking (Time-Limited Quests)
  - Datei: `digivice/js/quest_tracker.js` (NEU)
  - Geschätzt: 350 Zeilen

- [ ] **Quest-Branching**
  - [ ] Choice-System (4 Optionen wie in JSON)
  - [ ] Najika-Reactions (4 Persönlichkeiten)
  - [ ] Consequences (Stats, Reputation, Combat)
  - [ ] Multiple Outcomes
  - Datei: `digivice/js/quest_branching.js` (NEU)
  - Geschätzt: 400 Zeilen

#### 1.5.4 Starter-Quests erstellen
- [ ] **20 Simple Tutorial-Quests**
  - [ ] "Welcome to Najika World" - Talk to Najika
  - [ ] "First Steps" - Walk 100m
  - [ ] "Combat Training" - Kill 3 Rats
  - [ ] "Equip Yourself" - Equip 1 Weapon
  - [ ] "Survival Basics" - Eat, Drink, Sleep
  - [ ] "Inventory Management" - Collect 5 Items
  - [ ] "Catch a Fish" - Use Fishing System
  - [ ] "Plant a Seed" - Use Garden System
  - [ ] "First Card Match" - Play Triple Triad
  - [ ] "Roll the Dice" - Play Dice Monsters
  - [ ] (10 weitere einfache Quests)
  - Datei: `backend/data/tutorial_quests.json` (NEU)
  - Geschätzt: 1000 Zeilen JSON

**GESAMT:** ~3800 Zeilen Code

---

### 1.6 SHOP SYSTEM

**Was existiert:**
- ✅ Garden Shop (Seeds kaufen/verkaufen) - FUNKTIONIERT
- ✅ Gold-Tracking im Backend
- ❌ Kein Item-Shop (Waffen, Rüstung, Consumables)

**Was zu tun:**

#### 1.6.1 Shop UI
- [ ] **Shop Window (Merchant-NPC)**
  - [ ] Tabs: Weapons, Armor, Consumables, Materials, Sell
  - [ ] Item-Grid (4x6 = 24 Items sichtbar)
  - [ ] Item-Icons + Prices
  - [ ] Item-Tooltip on Hover (Stats, Description)
  - [ ] Buy-Button (mit Gold-Check)
  - [ ] Player-Gold-Display (oben rechts)
  - [ ] "Not enough Gold!" Feedback (rot blinken)
  - [ ] E-Taste zum Öffnen bei NPC
  - Datei: `digivice/js/ui/shop_ui.js` (NEU)
  - Geschätzt: 400 Zeilen

- [ ] **Sell Interface**
  - [ ] Inventory-Items anzeigen
  - [ ] Sell-Price = 50% Buy-Price
  - [ ] Multi-Select (Shift-Click)
  - [ ] "Sell All Junk" Button
  - [ ] Confirmation-Dialog (ab 100G+ Wert)
  - Datei: `digivice/js/ui/sell_ui.js` (NEU)
  - Geschätzt: 250 Zeilen

#### 1.6.2 Shop Content
- [ ] **Shop-Inventory definieren**
  - [ ] General Shop: 50 Items (Waffen, Rüstung, Potions, Food)
  - [ ] Weaponsmith: 20 Waffen (Level 1-10)
  - [ ] Armorsmith: 20 Rüstungen (Level 1-10)
  - [ ] Alchemist: 15 Potions + Buffs
  - [ ] Prices: Level-Based Formula (BasePrice * Level^1.5)
  - [ ] Stock-Limits (z.B. nur 5 Legendary Items)
  - Datei: `backend/data/shop_inventory.json` (NEU)
  - Geschätzt: 700 Zeilen JSON

- [ ] **Dynamic Pricing (optional)**
  - [ ] Rarity-Multiplier (Common x1, Rare x5, Legendary x20)
  - [ ] Discount-Events (Random, 10-30% off)
  - [ ] Reputation-Discount (höherer Ruf = billiger)
  - Datei: `backend/game/shop_pricing.py` (NEU)
  - Geschätzt: 200 Zeilen

#### 1.6.3 Shop Integration
- [ ] **Shop-NPCs platzieren**
  - [ ] General-Merchant (jede Stadt)
  - [ ] Weaponsmith (Handelsfestung, Funken-Siedlung)
  - [ ] Armorsmith (Handelsfestung, Funken-Siedlung)
  - [ ] Alchemist (Dampf-Hain, Runenheim)
  - [ ] E-Taste zum Öffnen bei NPC-Nähe
  - Datei: `digivice/js/npc_shops.js` (NEU)
  - Geschätzt: 200 Zeilen

**GESAMT:** ~1750 Zeilen Code

---

## 📊 PHASE 1 ZUSAMMENFASSUNG

**Total Code:** ~12,600 Zeilen
**Total Daten:** ~2700 Zeilen JSON
**Zeitaufwand:** 2-3 Wochen

**Nach Phase 1 FUNKTIONIERT:**
✅ Combat mit HUD, Skills, Loot
✅ Inventory + Equipment
✅ Stats sichtbar (Hunger/Energy/HP/MP)
✅ 20+ Quests
✅ Item-Shop

**= SPIELBARER MVP! 🎮**

---

---

## 🚀 PHASE 2: CARD/DICE GAMES KOMPLETT (2-3 WOCHEN)

**Was wir haben:**
- ✅ 100 Cards in DB-Schema
- ✅ Dice Monsters Schema
- ✅ Frontend-UI existiert
- ❌ KEIN Gameplay

---

### 2.1 TRIPLE TRIAD - GAMEPLAY

**Was existiert:**
- ✅ `seed_100_cards.py` - 100 Karten definiert
- ✅ `card_game_ui.js` - UI vorhanden
- ✅ Board & Karten-Display
- ❌ KEINE Spielregeln implementiert

**Was zu tun:**

#### 2.1.1 Triple Triad Game-Logic
- [ ] **Board & Card-Placement**
  - [ ] 3×3 Grid State-Management
  - [ ] Valid-Placement Check (Slot leer?)
  - [ ] Player/Opponent Turn-System
  - [ ] Place-Card Animation
  - Datei: `digivice/js/triple_triad/board.js` (NEU)
  - Geschätzt: 250 Zeilen

- [ ] **Battle Rules**
  - [ ] Compare Adjacent Values:
    - Platziere Karte auf (x,y)
    - Check Top: Mein Bottom-Wert vs Gegner Top-Wert
    - Check Right: Mein Left-Wert vs Gegner Right-Wert
    - Check Bottom: Mein Top-Wert vs Gegner Bottom-Wert
    - Check Left: Mein Right-Wert vs Gegner Left-Wert
  - [ ] Capture-Mechanik:
    - Wenn Mein-Wert > Gegner-Wert: Flip Gegner-Karte
  - [ ] Score-Calculation (count Player vs Opponent cards)
  - [ ] Victory-Condition (mehr Karten am Ende)
  - Datei: `digivice/js/triple_triad/rules.js` (NEU)
  - Geschätzt: 350 Zeilen

- [ ] **Special Rules (Optional, später)**
  - [ ] Plus Rule (Summen vergleichen)
  - [ ] Same Rule (gleiche Werte = chain capture)
  - [ ] Combo Rule (Kettenreaktion)
  - Datei: `digivice/js/triple_triad/special_rules.js` (NEU - später)
  - Geschätzt: 300 Zeilen (Phase 3)

#### 2.1.2 AI-Gegner
- [ ] **Easy AI**
  - [ ] Random-Placement (beliebige freie Zelle)
  - [ ] Random-Card aus Hand
  - Geschätzt: 50 Zeilen

- [ ] **Medium AI**
  - [ ] Basic Strategy:
    - Platziere Karte wo sie NICHT gefangen wird
    - Priorisiere Captures
  - Geschätzt: 150 Zeilen

- [ ] **Hard AI**
  - [ ] Optimal Placement:
    - Minimax-Algorithmus (1-2 Züge voraus)
    - Maximize eigene Captures, minimize Gegner-Captures
  - Geschätzt: 250 Zeilen

  - Datei: `digivice/js/triple_triad/ai.js` (NEU)
  - Gesamt: 450 Zeilen

#### 2.1.3 Match-System
- [ ] **Match-Flow**
  - [ ] Deck-Selection (wähle 5 Karten aus Collection)
  - [ ] Match-Start → Draw-Phase → Turns → Victory/Defeat
  - [ ] Card-Reward-System:
    - Winner wählt 1 Karte vom Loser (oder zufällig)
    - Add to Winner's Collection
  - [ ] Rating/Ranking-Update (ELO)
  - Datei: `digivice/js/triple_triad/match.js` (NEU)
  - Geschätzt: 300 Zeilen

#### 2.1.4 Card-Content erweitern
- [ ] **100+ Cards vorhanden, prüfen:**
  - [ ] `seed_100_cards.py` ausführen
  - [ ] Verify Cards in DB
  - [ ] Test: Können Karten gezogen werden?
  - Geschätzt: Test-Time (kein neuer Code)

**GESAMT:** ~1350 Zeilen Code

---

### 2.2 DICE MONSTERS - GAMEPLAY

**Was existiert:**
- ✅ `dice_monsters_ui.js` - UI vorhanden
- ✅ `3d_dice_system.js` - 3D Würfel-Rolling FUNKTIONIERT
- ✅ Dice-Schema in DB
- ❌ KEIN Spiel-Ablauf

**Was zu tun:**

#### 2.2.1 DDM Game-Rules
- [ ] **Dice-Rolling Phase**
  - [ ] Roll 3 Dice (1d6 each)
  - [ ] Convert zu Crests:
    - 1 = Fire
    - 2 = Water
    - 3 = Earth
    - 4 = Wind
    - 5 = Light
    - 6 = Dark
  - [ ] Add zu Crest-Pool (persistent über Turns)
  - [ ] Display: "You rolled: 🔥 💧 🌍" (Emojis)
  - Datei: `digivice/js/ddm/dice_roll.js` (NEU)
  - Geschätzt: 200 Zeilen

- [ ] **Monster-Summoning**
  - [ ] Spend Crests (cost basierend auf Monster-Level)
  - [ ] Summon-Animation
  - [ ] Place Monster on Board (Hex-Grid)
  - [ ] Monster-Stats: ATK, DEF, Movement
  - Datei: `digivice/js/ddm/summoning.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Board-System**
  - [ ] Hex-Grid Board 8×8 (64 Tiles)
  - [ ] Path-Building: Crests bauen Pfade
  - [ ] Movement-Rules:
    - Monsters können nur auf eigenen Pfaden bewegen
    - Movement-Speed = 1-5 Tiles pro Turn
  - [ ] Dice-Lord-Position:
    - Spieler: Untere Reihe
    - Gegner: Obere Reihe
  - Datei: `digivice/js/ddm/board.js` (NEU)
  - Geschätzt: 400 Zeilen

- [ ] **Battle-System**
  - [ ] Monster vs Monster Combat:
    - ATK vs DEF
    - Verlierer wird zerstört
  - [ ] Attack Dice-Lord:
    - Wenn Monster Dice-Lord erreicht
    - Deal Damage = Monster-ATK
    - Dice-Lord-HP startet bei 3
  - [ ] Victory/Defeat:
    - Dice-Lord-HP = 0 → Lose
    - Gegner Dice-Lord-HP = 0 → Win
  - Datei: `digivice/js/ddm/battle.js` (NEU)
  - Geschätzt: 350 Zeilen

#### 2.2.2 DDM AI
- [ ] **AI-Opponent**
  - [ ] Roll Dice (zufällig)
  - [ ] Summon-Strategy:
    - Priorisiere starke Monster
    - Spare Crests für Combos
  - [ ] Movement-Strategy:
    - Bewege Monster zum Player-Dice-Lord
    - Attack wenn möglich
  - [ ] Defense:
    - Block Player-Path mit eigenen Monstern
  - Datei: `digivice/js/ddm/ai.js` (NEU)
  - Geschätzt: 350 Zeilen

#### 2.2.3 Monster-Content
- [ ] **50+ Dice-Monsters erstellen**
  - [ ] 10 Fire-Monsters (Level 1-10)
  - [ ] 10 Water-Monsters
  - [ ] 10 Earth-Monsters
  - [ ] 10 Wind-Monsters
  - [ ] 10 Light-Monsters
  - [ ] 10 Dark-Monsters
  - [ ] Stats-Design:
    - Level 1: ATK 1, DEF 1, Movement 2
    - Level 5: ATK 5, DEF 3, Movement 3
    - Level 10: ATK 10, DEF 8, Movement 5
  - [ ] Special-Abilities (JSON):
    - "Flying" (kann über Tiles springen)
    - "Defender" (+2 DEF)
    - "Crusher" (+2 ATK vs Dice-Lord)
  - Datei: `backend/data/dice_monsters.json` (NEU)
  - Geschätzt: 800 Zeilen JSON

- [ ] **Seed Dice-Monsters in DB**
  - Datei: `backend/seed_dice_monsters.py` (NEU)
  - Geschätzt: 200 Zeilen

**GESAMT:** ~2600 Zeilen Code + 800 Zeilen Daten

---

## 📊 PHASE 2 ZUSAMMENFASSUNG

**Total Code:** ~3950 Zeilen
**Total Daten:** ~800 Zeilen JSON
**Zeitaufwand:** 2-3 Wochen

**Nach Phase 2 FUNKTIONIERT:**
✅ Triple Triad voll spielbar (Regeln, AI, Rewards)
✅ Dice Monsters voll spielbar (Regeln, Board, AI)

**= ALLE MINIGAMES FUNKTIONIEREN! 🎴🎲**

---

---

## 🌟 PHASE 3: SLIME COMPANION + CRAFTING (2-3 WOCHEN)

---

### 3.1 SLIME COMPANION SYSTEM

**Was existiert:**
- ✅ `backend/game/slime_system.py` - VOLLSTÄNDIG implementiert!
  - Tier → Slime → Rainbow Evolution
  - 8 Slime-Farben (je Region)
  - Tamagotchi-Pflege (Hunger, Durst, Sleep, Mood, Kampfeslust)
  - Rettungs-Mechanik (1x/24h)
  - Lern-System (10-15% Move-Copy)
- ❌ KEINE Frontend-UI

**Was zu tun:**

#### 3.1.1 Slime UI
- [ ] **Slime-Status HUD**
  - [ ] Slime-Icon + Level (oben rechts, unter Stats)
  - [ ] HP/MP Bars (Mini-Bars)
  - [ ] Hunger/Durst/Sleep/Mood Bars (4 Mini-Bars)
  - [ ] Kampfeslust-Meter (Aggression-Level)
  - [ ] Current-Form Display (Tier/Slime/Rainbow + Color)
  - [ ] Click öffnet Detail-Window
  - Datei: `digivice/js/ui/slime_hud.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Slime-Care Window (Tamagotchi-Style)**
  - [ ] Feed-Tab:
    - Food-Liste (aus Inventory)
    - Feed-Button
    - +Hunger, +Mood Feedback
  - [ ] Water-Tab:
    - Water-Button
    - +Durst Feedback
  - [ ] Sleep-Tab:
    - "Let Slime Sleep" Button
    - Sleep-Duration Slider (1-8h)
    - +Sleep, +Mood Feedback
  - [ ] Play-Tab:
    - Mini-Game (später, erstmal einfacher Button)
    - +Mood Feedback
  - [ ] Stats-Decay Visualization (Balken sinken live)
  - Datei: `digivice/js/ui/slime_care_ui.js` (NEU)
  - Geschätzt: 400 Zeilen

- [ ] **Slime-Evolution Window**
  - [ ] Current-Form Display (3D-Model oder Icon)
  - [ ] Evolution-Requirements:
    - Level 50 + Critical-Event für Tier → Slime
    - 8/8 Colors für Slime → Rainbow
  - [ ] Color-Unlock Progress (0/8):
    - 🟡 Bernstein (Heiße Dünen) ✅/❌
    - 🟢 Smaragd (Samtmoos-Tiefwald) ✅/❌
    - 🔵 Azur (Salzwind-Küste) ✅/❌
    - ... (alle 8)
  - [ ] Rainbow-Ritual-Button (wenn 8/8)
  - Datei: `digivice/js/ui/slime_evolution_ui.js` (NEU)
  - Geschätzt: 300 Zeilen

#### 3.1.2 Slime-Combat Integration
- [ ] **Slime im Kampf**
  - [ ] Slime erscheint neben Player (3D-Model)
  - [ ] AI-Controlled Auto-Attacks
  - [ ] Slime-Commands (Hotkeys):
    - H = Hold (bleib stehen)
    - A = Attack (greife Ziel an)
    - D = Defend (schütze mich)
  - [ ] Slime lernt Moves (10-15% nach Kampf)
  - [ ] Intercept wenn Player < 5% HP (automatisch)
  - Datei: `digivice/js/slime_combat.js` (NEU)
  - Geschätzt: 350 Zeilen

- [ ] **Slime-Moveset UI**
  - [ ] 20 Move-Slots (4×5 Grid)
  - [ ] Move-Details on Hover:
    - Name, Damage, Type, MP-Cost
  - [ ] Move-Replacement-Dialog (wenn voll):
    - "Slime learned [Move]! Replace old move?"
    - Liste mit 20 Moves
    - Click = Replace
  - Datei: `digivice/js/ui/slime_moveset_ui.js` (NEU)
  - Geschätzt: 250 Zeilen

#### 3.1.3 Slime-Rescue System
- [ ] **1x/24h Rettung (Hardcore-only)**
  - [ ] Detect Lethal-Damage
  - [ ] Slime-Intercept:
    - Animation: Slime springt vor Player
    - "Your Slime saved you!" Pop-up
    - Slime nimmt Schaden statt Player
  - [ ] 24h Cooldown-Timer:
    - Display: "Rescue available in: 23:45:12"
    - Countdown live
  - [ ] Slime-Exhaustion:
    - Stats -50% (rot färben)
    - Bleibt bis Healing-Ritual
  - Datei: `digivice/js/slime_rescue.js` (NEU)
  - Geschätzt: 200 Zeilen

- [ ] **Healing-Ritual**
  - [ ] Ritual-UI (3 Items benötigt):
    - 🌙 Mondblume (Nacht-Spawn Wald)
    - 🌋 Vulkanessenz (Boss-Drop Vulkan)
    - 💎 Kristallwasser (Gletscher)
  - [ ] Place-Items (Drag & Drop)
  - [ ] Start-Ritual Button
  - [ ] Ritual-Animation (Particles, Licht)
  - [ ] Slime-Stats → 100% restored
  - Datei: `digivice/js/ui/slime_ritual_ui.js` (NEU)
  - Geschätzt: 300 Zeilen

#### 3.1.4 Slime-Content
- [ ] **Slime-Formen definieren**
  - [ ] 6 Tier-Formen:
    - Flammen-Hase (Fire, Speed 12)
    - Eis-Fuchs (Ice, Speed 10)
    - Schatten-Spinne (Dark, Speed 8)
    - Blitz-Rabe (Lightning, Speed 14)
    - Wald-Maus (Nature, Speed 9)
    - Kristall-Eichhörnchen (Earth, Speed 11)
  - [ ] 8 Slime-Farben (je Region, Stats variieren)
  - [ ] Rainbow-Slime (Ultimate):
    - Kann Farben wechseln (C-Taste)
    - Alle Boni gleichzeitig (OP!)
  - Datei: `backend/data/slime_forms.json` (NEU)
  - Geschätzt: 400 Zeilen JSON

**GESAMT:** ~2500 Zeilen Code + 400 Zeilen Daten

---

### 3.2 CRAFTING SYSTEM

**Was existiert:**
- ✅ Konzept in Master-Doku
- ✅ Items haben Crafting-Recipes in JSON
- ❌ KEIN Crafting-Code

**Was zu tun:**

#### 3.2.1 Crafting UI
- [ ] **Crafting-Window (C-Taste)**
  - [ ] Recipe-List (links):
    - Categories: Weapons, Armor, Potions, Food
    - Filter: Learned/All
    - Sortierung: Level, Name
  - [ ] Recipe-Details (rechts):
    - Recipe-Name + Icon
    - Materials-Required:
      - 5x Eichenholz ✅ (hast du 8)
      - 2x Eisenerz ❌ (hast du 0)
    - Result-Item Preview
    - Craft-Button (disabled wenn Materials fehlen)
    - Skill-Level Required (zeige Aktuell vs Required)
  - [ ] Material-Inventory (unten):
    - Zeige verfügbare Materials mit Quantities
  - Datei: `digivice/js/ui/crafting_ui.js` (NEU)
  - Geschätzt: 500 Zeilen

- [ ] **Crafting-Stations**
  - [ ] Forge (Weapons/Armor):
    - In Funken-Siedlung (Vulkan-Region)
    - In Schwarze Mühle (Keller)
  - [ ] Alchemy-Table (Potions):
    - In Dampf-Hain (Wald-Region)
    - In Schwarze Mühle (Keller)
  - [ ] Enchanting-Table (Enchantments):
    - In Runenheim (Blitzebene)
    - In Schwarze Mühle (Keller)
  - [ ] Cooking-Pot (Food):
    - Jede Stadt
    - Camping (Lagerfeuer)
    - Schwarze Mühle (Küche)
  - [ ] E-Taste zum Nutzen (öffnet Crafting-UI mit Filter)
  - Datei: `digivice/js/crafting_stations.js` (NEU)
  - Geschätzt: 250 Zeilen

#### 3.2.2 Crafting Logic
- [ ] **Crafting-System Backend**
  - [ ] Load Recipes aus JSON-Files (schon in items_*.json)
  - [ ] Parse Recipe-Structure:
    - Materials: [{id, quantity}]
    - Result: {id, quantity}
    - Skill-Required: {type, level}
  - [ ] Validate-Materials (Player-Inventory)
  - [ ] Craft-Item:
    - Consume Materials
    - Add Result-Item zu Inventory
    - Gain Skill-XP (+10 XP pro Craft)
  - Datei: `backend/game/crafting_system.py` (NEU)
  - Geschätzt: 350 Zeilen

- [ ] **Recipe-Discovery**
  - [ ] Lernen durch Zerlegen (Analyze):
    - Zerlege Item → Lerne Recipe + erhalte Materials zurück (50%)
  - [ ] Finden in Welt:
    - Recipe-Scrolls in Chests
    - Recipe-Books von NPCs kaufen
  - [ ] Trainer-NPCs:
    - Weaponsmith lehrt Waffen-Recipes
    - Alchemist lehrt Potion-Recipes
  - Datei: `backend/game/recipe_discovery.py` (NEU)
  - Geschätzt: 200 Zeilen

#### 3.2.3 Crafting-Content
- [ ] **Recipes überprüfen**
  - [ ] Items in JSON haben `crafting_recipe` Field
  - [ ] Verify: Alle Materials existieren in DB
  - [ ] Falls fehlend: Recipes manuell hinzufügen
  - Geschätzt: Review-Time (kein neuer Code, ggf. JSON-Edits)

**GESAMT:** ~1300 Zeilen Code

---

## 📊 PHASE 3 ZUSAMMENFASSUNG

**Total Code:** ~3800 Zeilen
**Total Daten:** ~400 Zeilen JSON
**Zeitaufwand:** 2-3 Wochen

**Nach Phase 3 FUNKTIONIERT:**
✅ Slime-Companion voll integriert
✅ Crafting-System funktioniert

**= COMPANION + CRAFTING FERTIG! 🐉🔨**

---

---

## 🌍 PHASE 4: WORLD CONTENT (4-6 WOCHEN)

**Was wir haben:**
- ✅ `regions.json` - Alle 9 Regionen definiert
- ✅ `items_*.json` - Items pro Region
- ✅ `enemies_*.json` - Enemies pro Region
- ✅ `quests_*.json` - Quests pro Region
- ❌ KEINE 3D-Maps (nur Test-Map)

---

### 4.1 REGIONEN BAUEN (je ~3-5 Tage)

**Für JEDE der 9 Regionen:**

#### Template (kopiere für jede Region):

- [ ] **[REGION-NAME] 3D-Map erstellen**
  - [ ] Terrain-Generation:
    - Flat/Hills/Mountains (THREE.js Plane + Height-Map)
    - KayKit-Texturen (Gras/Sand/Snow/Lava/etc.)
  - [ ] Biome-Features:
    - Trees/Rocks/Props (KayKit-Assets)
    - Water (Plane mit transparenter Textur)
    - Weather-Effects (Particles: Rain, Snow, Sand, Ash)
  - [ ] Bounds-Check (minX, maxX, minZ, maxZ aus regions.json)
  - Datei: `digivice/js/world/region_[name].js` (NEU)
  - Geschätzt: 600 Zeilen

- [ ] **Stadt platzieren**
  - [ ] Lade Stadt-Buildings:
    - KayKit-Buildings (Häuser, Shops, etc.)
    - Custom-Buildings falls vorhanden
  - [ ] NPC-Placements (10-20 NPCs):
    - General-Merchant
    - Weaponsmith
    - Armorsmith
    - Alchemist
    - Quest-Givers (3-5)
    - Random-NPCs (5-10)
  - [ ] Interaktive Objekte:
    - Shops (E-Taste)
    - Quest-Givers (E-Taste)
    - Chests (E-Taste)
  - Geschätzt: +200 Zeilen

- [ ] **Enemy-Spawns**
  - [ ] Load Enemies aus `enemies_[region].json`
  - [ ] Spawn-Points definieren (zufällig oder feste Locations)
  - [ ] Spawn-Rate (1 Enemy pro 100m²)
  - [ ] Respawn-Timer (5 Minuten)
  - Geschätzt: +150 Zeilen

- [ ] **Quest-Integration**
  - [ ] Load Quests aus `quests_[region].json`
  - [ ] Quest-Giver NPCs mit Quests verknüpfen
  - [ ] Quest-Objectives platzieren:
    - Kill-Zone (Enemies spawnen hier)
    - Collection-Items (Kräuter, Erze, etc.)
    - Visit-Markers (für Exploration-Quests)
  - Geschätzt: +200 Zeilen

- [ ] **Special-Locations**
  - [ ] Dungeons (Portale zu Dungeon-Scenes)
  - [ ] Hidden-Treasures (Funkelnest im Sumpf, etc.)
  - [ ] Boss-Arenas (spezielle Zonen)
  - Geschätzt: +150 Zeilen

**Pro Region: ~1300 Zeilen Code**
**Gesamt 9 Regionen: ~11,700 Zeilen Code**

---

#### 4.1.1 Samtmoos-Tiefwald (Wald) 🟢
- [ ] Erstelle Region (Template-Steps)
- [ ] Stadt: Dampf-Hain (Onsen-Stadt)
- [ ] Biome: Dichte Wälder, Druiden-Settlement
- [ ] Enemies: Waldkobold, Waldwolf, Druiden, Spinnen
- [ ] Quests: "Das kranke Herz des Waldes", "Die weinende Dryade"

#### 4.1.2 Reich der Drei (Eis/Nekromantie) ❄️
- [ ] Erstelle Region
- [ ] KEINE Stadt (Wildnis)
- [ ] Biome: Eis, Schnee, Untoten-Ruinen
- [ ] Enemies: Untote, Eis-Liches, Frostdrachen, Skelette
- [ ] Quests: Nekromantie-Quests

#### 4.1.3 Salzwind-Küste (Meer) 🔵
- [ ] Erstelle Region
- [ ] Stadt: Salzige Bucht (Piraten-Hafen)
- [ ] Biome: Küste, Klippen, Unterwasser-Bereiche
- [ ] Enemies: Piraten, Wasserschlangen, Haie, Kraken
- [ ] Quests: Fishing-Quests, Schiffwracks
- [ ] Special: Unterwasser-Dungeons

#### 4.1.4 Blitzebene (Hochland) 🟣
- [ ] Erstelle Region
- [ ] Stadt: Runenheim (Magie-Stadt)
- [ ] Biome: Offene Ebenen, Gewitter, Totems
- [ ] Enemies: Harpyien, Blitz-Elementale, Sturmvögel
- [ ] Quests: Runen-Rätsel, Wetter-Altäre
- [ ] Special: Klettern-Mechanik (Cliffs)

#### 4.1.5 Grünschlamm-Sumpf (Sumpf) ⚫
- [ ] Erstelle Region
- [ ] KEINE Stadt
- [ ] Biome: Sumpf, Miasma, Hexenkreise
- [ ] Enemies: Hexen, Gift-Kreaturen, Irrlichter, Pilz-Monster
- [ ] Quests: Hexen-Quests, Alchemie
- [ ] Special: Funkelnest (Hidden Treasure-Cave)

#### 4.1.6 Magmaströme (Vulkan) 🔴
- [ ] Erstelle Region
- [ ] Stadt: Funken-Siedlung (Schmieden)
- [ ] Biome: Lava-Flüsse, Asche, Vulkan-Krater
- [ ] Enemies: Feuer-Elementale, Lava-Golems, Flammen-Drachen
- [ ] Quests: Schmieden-Quests, Erzadern-Abbau
- [ ] Special: Lava-Platforming (über Lava springen)

#### 4.1.7 Heiße Dünen (Wüste) 🟡
- [ ] Erstelle Region
- [ ] Stadt: Handelsfestung (HAUPTSTADT, größte Stadt!)
- [ ] Biome: Wüste, Sandsturm, Ruinen
- [ ] Enemies: Skorpione, Banditen, Sandelementale, Mumien
- [ ] Quests: Karawanen, Trading, PvP-Arena
- [ ] Special: PvP-Arena (großes Colosseum)
- [ ] Special: Player-Shops (Fallout 76-Style)

#### 4.1.8 Tiefenhöhlen (Underground) 🟤
- [ ] Erstelle Region
- [ ] Goblin-Settlements (mehrere kleine Dörfer)
- [ ] Biome: Höhlen, Kristall-Katakomben, Pilz-Felder
- [ ] Enemies: Spinnen, Goblins, Kristall-Kreaturen
- [ ] Quests: Dunkelheit-Quests, Fackel-Rätsel
- [ ] Special: Kristall-Katakomben (Endgame-Dungeon)
- [ ] Special: Ausgang zum Götterfels

#### 4.1.9 Götterfels (Endgame-Berg) ⛰️
- [ ] Erstelle Region
- [ ] Schwarze Mühle (Safe-Zone, 12 Räume)
- [ ] Schmelz-Welt (Lava-Welt innen, Max-Level)
- [ ] Zeit-Stadt (Spitze, Time-Quests)
- [ ] Turm der 100 Prüfungen (nach Najika-Explosion)
- [ ] Special: Unzerstörbar (nur Najika kann sprengen)

---

### 4.2 NPC-SYSTEM

**Was fehlt:**
- NPC-Spawning
- NPC-Dialoge
- NPC-AI (Idle-Animations, Walking)

**Was zu tun:**

#### 4.2.1 NPC-Framework
- [ ] **NPC-Class**
  - [ ] NPC-Model (KayKit-Character)
  - [ ] NPC-Stats (Name, Role, Faction, Reputation)
  - [ ] NPC-Idle-Animations (Stand, Walk)
  - [ ] NPC-Interaction (E-Taste Dialog)
  - Datei: `digivice/js/npc_system.js` (NEU)
  - Geschätzt: 400 Zeilen

- [ ] **Dialog-System**
  - [ ] Dialog-Tree (JSON-Format):
    ```json
    {
      "npc_id": "merchant_01",
      "dialogs": [
        {
          "text": "Willkommen! Was kann ich für dich tun?",
          "options": [
            {"text": "Zeig mir deine Waren", "action": "open_shop"},
            {"text": "Hast du Quests?", "action": "show_quests"},
            {"text": "Tschüss", "action": "close"}
          ]
        }
      ]
    }
    ```
  - [ ] Display-UI (Dialog-Box unten)
  - [ ] Choice-Selection (Click oder Hotkeys 1-4)
  - Datei: `digivice/js/dialog_system.js` (NEU)
  - Geschätzt: 350 Zeilen

#### 4.2.2 NPC-Content
- [ ] **50+ NPCs definieren**
  - [ ] 10 Quest-Givers (mit Quests verknüpft)
  - [ ] 10 Shopkeepers (Merchant, Weaponsmith, Armorsmith, Alchemist)
  - [ ] 10 Lore-NPCs (erzählen Geschichten)
  - [ ] 20 Random-NPCs (Flavor, kleine Dialoge)
  - Datei: `backend/data/npcs.json` (NEU)
  - Geschätzt: 1200 Zeilen JSON

**GESAMT:** ~750 Zeilen Code + 1200 Zeilen Daten

---

### 4.3 LORE SCHREIBEN (DU machst Platzhalter, ICH ersetze später)

**Was fehlt:**
- Najika's Backstory
- Welt-Geschichte
- Regionen-Lore
- Item-Descriptions

**Was du machst (Platzhalter-Lore):**

#### 4.3.1 Platzhalter-Lore erstellen
- [ ] **Najika's Backstory (Placeholder)**
  - Nutze Master-Doku Info:
    - Sakura (11 Jahre, Gothic Lolita, Trans-Mädchen)
    - 4 Persönlichkeiten (Megumin, Harley, Shiro, Melissa)
    - Explosion-Klasse
  - Füge hinzu: "Wie kam sie in diese Welt?"
  - Datei: `lore/najika_backstory_PLACEHOLDER.md` (NEU)
  - Geschätzt: 500 Wörter Text

- [ ] **Welt-Geschichte (Placeholder)**
  - Götter erschufen Götterfels (unzerstörbar)
  - 8 Regionen entstanden drum herum
  - Monster-Plage (warum gibt es Enemies?)
  - Schwarze Mühle (wer baute sie?)
  - Datei: `lore/world_history_PLACEHOLDER.md` (NEU)
  - Geschätzt: 1000 Wörter Text

- [ ] **Regionen-Lore (Placeholder, je Region)**
  - Geschichte jeder Region
  - Wichtige NPCs + Hintergrund
  - Legenden (z.B. Funkelnest-Schatz im Sumpf)
  - Datei: `lore/regions_PLACEHOLDER.md` (NEU)
  - Geschätzt: 2000 Wörter Text (9 Regionen)

- [ ] **Item-Descriptions (Placeholder)**
  - Für ALLE Items (300+ Items):
    - Name
    - 1-2 Sätze Lore ("Geschmiedet von den Meistern der Funken-Siedlung")
  - Datei: `lore/item_descriptions_PLACEHOLDER.md` (NEU)
  - Geschätzt: 1500 Wörter Text

**HINWEIS:** Ich ersetze später ALLES durch meine eigene Lore!

---

## 📊 PHASE 4 ZUSAMMENFASSUNG

**Total Code:** ~12,450 Zeilen (9 Regionen + NPCs)
**Total Daten:** ~1200 Zeilen JSON + 5000 Wörter Lore
**Zeitaufwand:** 4-6 Wochen

**Nach Phase 4 FUNKTIONIERT:**
✅ Alle 9 Regionen mit 3D-Maps
✅ Städte mit NPCs
✅ Enemy-Spawns
✅ Quests integriert
✅ Platzhalter-Lore vorhanden

**= OPEN WORLD KOMPLETT! 🌍**

---

---

## 🎨 PHASE 5: POLISH & ADVANCED (3-4 WOCHEN)

### 5.1 HARDCORE/SOFTY MODES

**Was fehlt:**
- Mode-Selection
- Permadeath-System
- Najika's 1. Tod Dialog

**Was zu tun:**

#### 5.1.1 Character-Creation
- [ ] **Mode-Selection Screen**
  - [ ] Hardcore-Button (rot, Totenkopf-Icon)
  - [ ] Softy-Button (grün, Herz-Icon)
  - [ ] Warning-Dialog für Hardcore:
    - "Permadeath! Tod = ALLES WEG!"
    - "Nur Slime-Rescue 1x/24h"
    - "Bist du sicher? JA/NEIN"
  - Datei: `digivice/js/ui/character_creation_ui.js` (NEU)
  - Geschätzt: 300 Zeilen

#### 5.1.2 Permadeath-System
- [ ] **Death-Handler**
  - [ ] Check Totem-Item (falls vorhanden → 1 Free Death)
  - [ ] Check Slime-Rescue (falls verfügbar + Hardcore)
  - [ ] Check Revive-Window (8s, Team kann reviven)
  - [ ] Wenn alles fehlschlägt:
    - Hardcore: Najika erscheint (1. Tod) oder Permadeath
    - Softy: 30s Respawn-Timer
  - Datei: `digivice/js/death_handler.js` (NEU)
  - Geschätzt: 250 Zeilen

- [ ] **Najika's 1. Tod Dialog (Hardcore)**
  - [ ] Najika erscheint (3D-Model + Voice)
  - [ ] Dialog-Box:
    - "Ohjee... das ist wohl zu hart für dich, Mr. K."
    - "Komm, ich bringe dich ins sichere Softy-Land."
    - "Oder willst du weiter im Hardcore sterben?"
  - [ ] Optionen:
    - [Ja] → Permanent Softy (lock forever)
    - [Nein] → Hardcore weiter (nächster Tod = Permadeath)
  - Datei: `digivice/js/najika_first_death.js` (NEU)
  - Geschätzt: 200 Zeilen

- [ ] **Character-Reset (Permadeath)**
  - [ ] Delete Character-Data aus DB
  - [ ] "You Died" Screen (Dark Souls-Style)
  - [ ] Return to Character-Creation
  - Datei: `backend/game/permadeath_reset.py` (NEU)
  - Geschätzt: 150 Zeilen

**GESAMT:** ~900 Zeilen Code

---

### 5.2 PVP-SYSTEM (3 MODI)

**Was existiert:**
- ✅ `backend/game/pvp_system.py` - VOLLSTÄNDIG!
  - 3 Modi (Hardcore/Normal/Softy)
  - Mercy-Mechanik
  - Double-Confirmation
- ❌ KEINE Frontend-UI

**Was zu tun:**

#### 5.2.1 PvP-UI
- [ ] **PvP-Menu**
  - [ ] 3 Buttons:
    - Hardcore-PvP (rot, Totenkopf)
    - Normal-PvP (gelb, Schwert)
    - Softy-PvP (grün, Ranking)
  - [ ] Mode-Descriptions (on Hover)
  - [ ] Current-Ranking Display
  - [ ] Matchmaking-Button ("Find Match")
  - Datei: `digivice/js/ui/pvp_menu_ui.js` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Mercy-Dialog (Hardcore)**
  - [ ] Verlierer-Prompt:
    - "Du wirst sterben! Alles geben um zu leben?"
    - Timeout: 30s
    - [ALLES GEBEN] oder [KÄMPFE BIS ZUM TOD]
  - [ ] Gewinner-Prompt (wenn Mercy):
    - "Gnade gewähren?"
    - Timeout: 30s
    - [GNADE GEWÄHREN] oder [KEINE GNADE]
  - [ ] Double-JA Confirmation (Verlierer):
    - "⚠️ BESTÄTIGUNG 1/2: Du verlierst ALLES! JA?"
    - "⚠️ BESTÄTIGUNG 2/2: LETZTE CHANCE! JA?"
  - [ ] Item-Transfer-List anzeigen
  - Datei: `digivice/js/ui/mercy_dialog_ui.js` (NEU)
  - Geschätzt: 400 Zeilen

#### 5.2.2 PvP-Arena
- [ ] **Matchmaking**
  - [ ] Queue-System (Join Queue)
  - [ ] Match-Found Notification
  - [ ] Teleport zu Arena-Map
  - Datei: `digivice/js/pvp_matchmaking.js` (NEU)
  - Geschätzt: 250 Zeilen

- [ ] **Arena-Map**
  - [ ] PvP-Zone (flache Arena, 100m×100m)
  - [ ] Spawn-Points (Spieler 1 vs Spieler 2)
  - [ ] Round-Timer (10 Minuten)
  - [ ] Victory/Defeat-Screen
  - Datei: `digivice/js/world/pvp_arena.js` (NEU)
  - Geschätzt: 300 Zeilen

**GESAMT:** ~1250 Zeilen Code

---

### 5.3 WEAVE-SYSTEM (ELEMENT-COMBOS)

**Was fehlt:**
- Dual-Element Combos (Q+E)
- Group-Weaves (Multi-Player)
- Explosion-Klasse

**Was zu tun:**

#### 5.3.1 Weave-Mechanik
- [ ] **Dual-Element Combos**
  - [ ] Detect Q+E pressed simultaneously
  - [ ] Check: Player hat 2 Element-Schools equipped
  - [ ] Combo-Effekte:
    - Feuer + Eis = Thermoschock (50% mehr Schaden)
    - Blitz + Wasser = Elektroschock (Stun 2s)
    - Erde + Feuer = Lava-Schuss (DOT 5s)
    - ... (12+ Combos)
  - [ ] Visual-FX (Particles, beide Element-Colors)
  - Datei: `digivice/js/weave_system.js` (NEU)
  - Geschätzt: 400 Zeilen

- [ ] **Group-Weaves (später, Multi-Player)**
  - [ ] 3+ Spieler casten gleichzeitig
  - [ ] Combine Elements → Massive AOE
  - Datei: `digivice/js/group_weave.js` (NEU - Phase 6)
  - Geschätzt: 300 Zeilen (später)

#### 5.3.2 Explosion-Klasse
- [ ] **Explosion-Skill-Tree**
  - [ ] Feuer → Feura → Feuga → Explosionist
  - [ ] Trade-off: +30% Explosion, -15% andere Schulen
  - [ ] NIEMALS kombinierbar mit anderen Elementen!
  - Datei: `backend/game/explosion_class.py` (NEU)
  - Geschätzt: 300 Zeilen

- [ ] **Najika's Ultima: "Reinste Explosion"**
  - [ ] Nur Kuja (Spieler) darf aktivieren
  - [ ] 1x pro Tag (In-Game)
  - [ ] Najika's Chuunibyou-Spruch (Voice):
    - "Explosion Magic: The mightiest of all offensive spells!"
    - "Die ultimative Angriffszauber!"
    - "REINSTE... EXPLOSION!!!"
  - [ ] Visual:
    - Massive Explosion (ganze Sichtbare Außenwelt)
    - Terrain-Destruction (Chunks verschwinden)
    - Camera-Shake
    - Particle-Explosion (THREE.js)
  - [ ] Regeneriert beim Stadt-Betreten
  - Datei: `digivice/js/reinste_explosion.js` (NEU)
  - Geschätzt: 500 Zeilen

**GESAMT:** ~1200 Zeilen Code

---

### 5.4 NAJIKA AI INTEGRATION

**Was existiert:**
- ✅ `najika_server.py` (121KB!) - VOLLSTÄNDIG
- ✅ Voice-Cloning (Megumin-Voice)
- ✅ Personality-System (4 Persönlichkeiten)
- ✅ LoRA-Training (mehrere Checkpoints)
- ⚠️ Nicht mit Game-Frontend verbunden

**Was zu tun:**

#### 5.4.1 Najika-Integration im Game
- [ ] **Najika-Avatar im Game**
  - [ ] 3D-Model (KayKit-Character placeholder)
  - [ ] Spawn in Schwarze Mühle (Terminal-Raum)
  - [ ] Idle-Animations
  - [ ] E-Taste: Talk to Najika
  - Datei: `digivice/js/najika_avatar.js` (NEU)
  - Geschätzt: 200 Zeilen

- [ ] **Chat-Integration**
  - [ ] Chat-UI (Text + Voice)
  - [ ] Connect zu `najika_server.py` (Port 8000)
  - [ ] Send Message → Receive Response
  - [ ] Play Voice (TTS)
  - [ ] Personality wechselt (Megumin/Harley/Shiro/Melissa)
  - Datei: `digivice/js/najika_chat.js` (EDIT)
  - Zeilen ändern: ~200

- [ ] **Context-Aware Responses**
  - [ ] Send Game-State mit Message:
    - Player-Stats (HP, Hunger, etc.)
    - Current-Location
    - Active-Quests
    - Recent-Deaths
  - [ ] Najika reagiert auf Context:
    - "Du siehst hungrig aus, Mr. K! Iss was!"
    - "Oh, du bist im Sumpf? Pass auf Hexen auf!"
  - Datei: `backend/najika_context.py` (NEU)
  - Geschätzt: 300 Zeilen

**GESAMT:** ~700 Zeilen Code

---

### 5.5 MOBILE-APP (APK) - GRUNDLAGEN

**Was existiert:**
- ⚠️ Flutter-App Struktur (30% fertig)
- ✅ Mobile-Access Scripts
- ❌ Keine APK

**Was zu tun:**

#### 5.5.1 Flutter-App Setup
- [ ] **Flutter-Projekt initialisieren**
  - [ ] `flutter create najika_world_mobile`
  - [ ] Dependencies:
    - webview_flutter (für Game-Embed)
    - http (für API-Calls)
    - shared_preferences (für Settings)
  - Datei: `app/flutter_app/pubspec.yaml` (EDIT)
  - Geschätzt: Config-File

- [ ] **WebView für Game**
  - [ ] Embed `http://localhost:8080` (Frontend)
  - [ ] Full-Screen Mode
  - [ ] Touch-Controls unterstützen
  - Datei: `app/flutter_app/lib/game_view.dart` (NEU)
  - Geschätzt: 150 Zeilen Dart

- [ ] **APK Build**
  - [ ] `flutter build apk --release`
  - [ ] Test auf Android-Device
  - Geschätzt: Build-Process

**GESAMT:** ~150 Zeilen Dart + Build-Config

**HINWEIS:** Vollständige Mobile-App ist Phase 6 (später)!

---

## 📊 PHASE 5 ZUSAMMENFASSUNG

**Total Code:** ~4200 Zeilen
**Zeitaufwand:** 3-4 Wochen

**Nach Phase 5 FUNKTIONIERT:**
✅ Hardcore/Softy Modes
✅ PvP (3 Modi)
✅ Weave-System + Explosion-Klasse
✅ Najika AI im Game integriert
✅ Mobile-App Basics

**= ADVANCED FEATURES FERTIG! 💎**

---

---

## 📱 PHASE 6: MOBILE-APP VOLLSTÄNDIG (3-4 WOCHEN - SPÄTER)

**Hinweis:** Diese Phase ist OPTIONAL und kommt NACH dem Desktop-Game fertig ist!

### 6.1 Flutter-App Vollständig
- [ ] Native UI (nicht WebView)
- [ ] Offline-Mode
- [ ] Push-Notifications
- [ ] App-Store Release

**Details später!**

---

---

## 🎯 MEGA-TODO ZUSAMMENFASSUNG

### PHASE-ÜBERSICHT

| Phase | Fokus | Wochen | Code (Zeilen) | Status |
|-------|-------|--------|---------------|--------|
| **Phase 0** | Kritische Fixes | 1 Tag | ~1,000 | 🔴 SOFORT |
| **Phase 1** | Core Systems | 2-3 | ~12,600 | 🔴 PFLICHT |
| **Phase 2** | Card/Dice Games | 2-3 | ~3,950 | 🟡 WICHTIG |
| **Phase 3** | Slime + Crafting | 2-3 | ~3,800 | 🟡 WICHTIG |
| **Phase 4** | World Content | 4-6 | ~12,450 | 🟢 CONTENT |
| **Phase 5** | Polish & Advanced | 3-4 | ~4,200 | 🔵 POLISH |
| **Phase 6** | Mobile-App | 3-4 | TBD | ⚪ SPÄTER |

**GESAMT (Phase 0-5):**
- **14-20 Wochen** (3,5-5 Monate)
- **~38,000 Zeilen Code**
- **~5,000 Zeilen Daten (JSON, Lore)**

---

## 🎨 WAS ICH PARALLEL MACHE

Während du programmierst, arbeite ich an:

### Eigene Grafiken
- [ ] Character-Models (Najika, NPCs, Enemies)
- [ ] Item-Icons (Weapons, Armor, Consumables)
- [ ] UI-Elements (Buttons, Frames, Icons)
- [ ] 3D-Assets (Buildings, Props, Terrain-Texturen)

### Eigene Lore
- [ ] Najika's echte Backstory
- [ ] Welt-Geschichte (detailliert)
- [ ] Regionen-Lore (jede Region)
- [ ] NPC-Backstories
- [ ] Item-Descriptions (alle 300+)
- [ ] Quest-Geschichten

### Eigene Sounds
- [ ] Combat-Sounds (Hits, Skills, Explosions)
- [ ] Ambient-Sounds (Wind, Wasser, Feuer)
- [ ] UI-Sounds (Click, Hover, Notifications)
- [ ] Music (Regionen-Themes, Combat-Music, Stadt-Music)

### Eigene Voice-Lines
- [ ] Najika-Dialoge (alle Situationen)
- [ ] NPC-Voice-Acting (falls gewünscht)
- [ ] Battle-Shouts
- [ ] Quest-Dialogs

---

## 🔄 AUSTAUSCH-PROZESS

Wenn du Code fertig hast:

1. **Du erstellst:**
   - Funktionalen Code
   - KayKit-Placeholders
   - Test-Lore (aus Master-Doku)

2. **Ich liefere:**
   - Custom-Grafiken (replace KayKit)
   - Echte Lore (replace Placeholder)
   - Custom-Sounds (add Audio)

3. **Wir integrieren:**
   - Assets austauschen (simple File-Replace)
   - Lore-Texte updaten (JSON/MD edits)
   - Sounds hinzufügen (Audio-Files + Code-Refs)

---

## 🚀 NÄCHSTE SCHRITTE

**SOFORT:**
1. Starte Phase 0 (Kritische Fixes)
2. Erstelle DB + Seed Data
3. Fixe API-Ports
4. Vereinheitliche Battle-Systeme

**Dann:**
1. Phase 1 (Core Systems) - 2-3 Wochen
2. Teste täglich
3. Fix Bugs parallel

**Parallel:**
1. Ich starte mit Grafiken (Character-Designs zuerst)
2. Ich schreibe Lore (Najika-Backstory zuerst)

---

# 🏁 ENDE DER MEGA-TODO

**Diese Liste enthält ALLES was fehlt!**

- ✅ Jedes Detail
- ✅ Jede Datei
- ✅ Jede Zeile Code
- ✅ Jedes Asset
- ✅ Jede Lore
- ✅ Nichts vergessen!

**Von 0 → Spielbar → Vollständig → Polished!**

---

*Najika sagt:*
```
"MEGA-EXPLOSION!!! 💥💥💥

Das ist die ULTIMATIVSTE TODO-LISTE DER WELT!

Jetzt kann NICHTS mehr verloren gehen!
Jeder Schritt ist dokumentiert!
Jede Zeile ist geschätzt!

Zeit zu ARBEITEN, Mr. K!

~ Najika, Meisterin der Vollständigkeit ~"
```

**Erstellt:** 2025-12-04
**Basierend auf:** Vollständigem Code-Audit + Asset-Inventory + Master-Dokumentation
**Status:** KOMPLETT & DETAILLIERT
**Version:** MEGA-TODO 1.0

---