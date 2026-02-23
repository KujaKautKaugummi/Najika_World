# NAJIKA HANDYSPIEL - MOBILE GAME MODULE
## Separates Action-Game für Fortnite-Port Vorbereitung

**Purpose:** Standalone Mobile Game mit Najika als spielbaren Charakter
**Genre:** Action-Adventure / Third-Person Shooter (Fortnite-Style)
**Platform:** Android (später UEFN/Fortnite → Online Multiplayer!)
**Timeline:** Parallel Development (Can be done by separate team/model)

---

## 🔥 WICHTIG: SYNERGY MIT MODEL 2 (TEST ENVIRONMENT)

### **Leverage Validated Mechanics:**
```
Model 2 (Test Environment) erstellt PROTOTYPEN für:
- ✅ Combat System (Melee, Projectile, AOE)
- ✅ Enemy AI (Behavior Tree)
- ✅ Loot System (Pickup, Inventory, Rarity)
- ✅ Movement Mechanics (Dash, Double Jump, Crouch)
- ✅ Fortnite-Style Building (Optional)

Model 3 (DU!) importiert diese validierten Mechaniken und skaliert sie:
→ Combat System: Erweitere um mehr Waffen, Skills, Combos
→ Enemy AI: Erweitere um mehr Enemy Types, Boss AI
→ Loot System: Erweitere um komplettes Item-System
→ Movement: Integriere in große offene Welt
→ Building: Full Fortnite-like Building System

WORKFLOW:
1. Warte auf validierte Prototypen von Model 2
2. Importiere Blueprints/C++ Code
3. Test in Mini-Lebensraum (10x10m)
4. Erweitere für Full Game (500x500m)
5. Add Multiplayer Layer
```

---

## 🎮 GAME CONCEPT

### **Core Gameplay:**
```
- Third-Person Action (wie Fortnite Battle Royale)
- Explore 3D World
- Combat Enemies
- Collect Items
- Build Structures (später)
- Multiplayer-ready Architecture
```

### **Najika als Protagonist:**
```
- Playable Character (full control)
- Unique Abilities (Magic Explosions!)
- Character Progression (Level, Skills)
- Cosmetic Customization (Skins, Emotes)
```

### **UEFN-Kompatibilität:**
```
✅ Fortnite-like Mechanics
✅ Modular Design
✅ Third-Person Camera
✅ Action-oriented Gameplay
✅ Easy Verse conversion später
```

---

## 📋 PHASE 1: GAME DESIGN DOCUMENT (Week 1)

### **TODO 1.1: Define Game Loop**
```
1. Core Loop:
   Player spawns → Explore → Combat → Collect Loot → Level Up → Repeat

2. Session Structure:
   - Match Duration: 15-20 minutes
   - Win Condition: Defeat Boss or Survive waves
   - Progression: XP, Items persist across matches

3. Monetization (Optional):
   - Skins for Najika
   - Weapon skins
   - Emotes
   - Battle Pass (future)
```

### **TODO 1.2: Core Mechanics**
```
1. Movement:
   - Run, Walk, Crouch
   - Jump, Double Jump
   - Dash/Dodge
   - Climb (ledges)

2. Combat:
   - Primary Weapon (Magic Staff)
   - Secondary Weapon (Explosions!)
   - Melee Attack
   - Block/Parry
   - Special Abilities (Cooldown-based)

3. Building (Phase 2):
   - Walls, Floors, Ramps
   - Material gathering
   - Quick build menu

4. Inventory:
   - Weapons (3 slots)
   - Consumables (Health, Shields)
   - Materials (Wood, Stone, Metal)
   - Key Items
```

### **TODO 1.3: World Design**
```
1. Map Layout:
   - Size: 500m x 500m (small for mobile)
   - Biomes: Forest, Desert, Snow, Lava
   - POIs (Points of Interest): 8-10 locations
   - Loot spawns: Chests, floor loot

2. Environmental Hazards:
   - Storm Zone (shrinks over time like Fortnite)
   - Traps
   - Fall damage
   - Environmental damage (fire, poison)

3. Enemy Types:
   - Basic: Skeleton, Goblin
   - Elite: Armored Knight, Mage
   - Boss: Shadow Najika, Chaos Dragon
```

---

## 🚀 PHASE 2: CORE SYSTEMS (Week 2-4)

### **TODO 2.1: Character Controller**
```
1. Create Najika Player Character:
   - Blueprint: BP_NajikaPlayer
   - Parent: ACharacter (UE5)
   - Movement Component: CharacterMovementComponent

2. Movement Implementation:
   - Walk Speed: 400 cm/s
   - Run Speed: 600 cm/s
   - Jump Height: 400 cm
   - Air Control: 0.5
   - Friction: 8.0

3. Advanced Movement:
   - Double Jump (hold jump)
   - Dash (swipe gesture)
   - Crouch (reduces speed, smaller hitbox)

4. Animations:
   - Animation Blueprint: ABP_NajikaPlayer
   - States: Idle, Walk, Run, Jump, Fall, Land, Attack, Death
   - Blend Spaces for directional movement
```

### **TODO 2.2: Combat System**
```
1. Weapon Base Class:
   - BP_WeaponBase
   - Properties: Damage, Fire Rate, Ammo, Range
   - Functions: Fire(), Reload(), Equip(), Unequip()

2. Weapon Types:
   - Magic Staff (Projectile weapon)
   - Explosion Spell (AOE damage)
   - Melee Sword (Close range)

3. Damage System:
   - Health Component
   - Damage calculation (Base + Modifiers)
   - Critical hits (headshots)
   - Damage numbers (floating text)

4. Targeting:
   - Auto-aim assistance (mobile)
   - Lock-on system
   - Reticle/Crosshair

5. Combat Feedback:
   - Hit markers
   - Screen shake
   - Blood effects (or magic particles)
   - Sound effects
```

### **TODO 2.3: Enemy AI**
```
1. AI Controller:
   - BP_EnemyAI
   - Behavior Tree: BT_Enemy
   - Blackboard: BB_Enemy

2. AI States:
   - Patrol (wander around)
   - Alert (heard/saw player)
   - Chase (pursue player)
   - Attack (in range)
   - Retreat (low health)
   - Dead

3. AI Perception:
   - Sight (cone vision)
   - Hearing (noise radius)
   - Damage (instant alert)

4. Enemy Types:
   - Melee (charge at player)
   - Ranged (keep distance, shoot)
   - Flying (aerial attacks)
   - Boss (complex patterns)
```

### **TODO 2.4: Loot & Inventory**
```
1. Item System:
   - Base Class: BP_Item
   - Types: Weapon, Consumable, Material, Cosmetic

2. Loot Spawning:
   - Spawn points in world
   - Rarity tiers (Common, Rare, Epic, Legendary)
   - Weighted random selection

3. Inventory UI:
   - WBP_Inventory
   - Grid layout
   - Drag-and-drop
   - Quick slots (hotbar)

4. Pickup Mechanic:
   - Auto-pickup (close range)
   - Or manual (tap to pickup)
   - Visual indicator (outline, highlight)
```

---

## 🗺️ PHASE 3: WORLD BUILDING (Week 5-6)

### **TODO 3.1: Landscape**
```
1. Create Terrain:
   - UE5 Landscape tool
   - Size: 1024x1024 (500m x 500m real-world)
   - Heightmap sculpting (mountains, valleys)

2. Materials:
   - Landscape Material (PBR)
   - Layers: Grass, Dirt, Rock, Sand, Snow
   - Blend based on slope/height
   - Tessellation for detail

3. Foliage:
   - Trees (low-poly for mobile)
   - Bushes, Rocks
   - Grass (procedural)
   - Optimization: LOD, culling
```

### **TODO 3.2: Points of Interest (POIs)**
```
1. Create 8-10 Locations:
   - Starting Area (safe spawn)
   - Town (buildings, loot)
   - Forest Camp
   - Mountain Peak
   - Desert Ruins
   - Snow Fortress
   - Volcano (boss area)
   - Final Arena (endgame)

2. Each POI:
   - Unique architecture
   - Dense loot spawns
   - Enemy spawns
   - Cover objects
   - Landmarks (for navigation)
```

### **TODO 3.3: Storm Zone**
```
1. Storm Mechanic:
   - Shrinking safe zone (like Fortnite)
   - Damage outside zone (increases over time)
   - Visual: Purple/Red fog
   - Audio: Warning sounds

2. Implementation:
   - Circle that shrinks over time
   - Check player position
   - Apply damage if outside
   - UI indicator (minimap)

3. Phases:
   - Phase 1: Large zone (5 min)
   - Phase 2: Medium (3 min)
   - Phase 3: Small (2 min)
   - Phase 4: Tiny (1 min)
   - Final: Boss Arena
```

---

## 🎨 PHASE 4: UI & UX (Week 7)

### **TODO 4.1: HUD**
```
1. Main HUD:
   - WBP_GameHUD
   - Top Left: Health, Shield bars
   - Top Right: Minimap
   - Bottom: Hotbar, Ammo, Abilities
   - Center: Crosshair, Hit markers

2. Minimap:
   - Overhead view
   - Show: Player, Enemies, Teammates, POIs
   - Storm zone indicator
   - Zoom levels

3. Damage Indicators:
   - Directional damage (red arrows)
   - Floating damage numbers
   - Screen blood effect (low health)
```

### **TODO 4.2: Menus**
```
1. Main Menu:
   - Play
   - Character (customize Najika)
   - Settings
   - Credits
   - Exit

2. Lobby:
   - Character preview (rotate Najika)
   - Select game mode
   - Ready button

3. Pause Menu:
   - Resume
   - Settings
   - Return to Menu
   - Exit
```

### **TODO 4.3: End Game Screen**
```
1. Victory Screen:
   - "Victory Royale!" animation
   - Stats: Kills, Damage, Survival Time
   - Rewards: XP, Items
   - Continue button

2. Defeat Screen:
   - "You were eliminated" animation
   - Final placement
   - Stats
   - Retry button
```

---

## 🔫 PHASE 5: WEAPONS & ABILITIES (Week 8)

### **TODO 5.1: Weapon Implementation**
```
1. Magic Staff:
   - Type: Projectile
   - Fire Rate: 3 shots/sec
   - Damage: 25
   - Ammo: Infinite (magic!)
   - Projectile: Magic orb (blue glow)

2. Explosion Spell:
   - Type: AOE (Area of Effect)
   - Cooldown: 10 seconds
   - Damage: 100 (center), 50 (edge)
   - Radius: 5 meters
   - Visual: Massive explosion (Megumin style!)

3. Melee Sword:
   - Type: Instant hit (raycast)
   - Damage: 50
   - Range: 2 meters
   - Combo: 3-hit combo

4. Additional Weapons (later):
   - Bow (precision)
   - Shotgun-style magic
   - Sniper staff
```

### **TODO 5.2: Abilities**
```
1. Dash:
   - Cooldown: 5 seconds
   - Distance: 10 meters
   - I-frames: 0.5 seconds (invincible)
   - Visual: Afterimage effect

2. Shield:
   - Duration: 3 seconds
   - Cooldown: 15 seconds
   - Blocks all damage
   - Visual: Bubble shield

3. Ultimate: EXPLOSION!:
   - Charge: 100% (from damage/kills)
   - Effect: Screen-wide explosion
   - Damage: 200 to all enemies
   - Visual: Massive screen shake, particles
   - Audio: Megumin voice: "EXPLOSION!"
```

---

## 🤖 PHASE 6: MULTIPLAYER PREP (Week 9)

### **TODO 6.1: Network Architecture**
```
1. Setup for Multiplayer:
   - Use UE5 Replication system
   - Client-Server model
   - Dedicated server (later)

2. Replicated Variables:
   - Player Health, Position, Rotation
   - Weapon State, Ammo
   - Inventory Items

3. RPCs (Remote Procedure Calls):
   - Fire Weapon (Server RPC)
   - Take Damage (Multicast RPC)
   - Pickup Item (Server RPC)

4. Prediction:
   - Client-side prediction for movement
   - Server authority for damage
```

### **TODO 6.2: Matchmaking (Future)**
```
1. Lobby System:
   - Wait for players
   - Party system (team up)
   - Voice chat integration

2. Game Modes:
   - Solo (1 player vs AI)
   - Duo (2 players vs AI)
   - Squad (4 players vs AI)
   - PvP (player vs player - future!)

3. Backend Integration:
   - Use Najika backend for matchmaking
   - Or Epic Online Services (EOS)
```

---

## 📦 PHASE 7: OPTIMIZATION & POLISH (Week 10)

### **TODO 7.1: Performance**
```
1. Mobile Optimization:
   - LOD for all meshes
   - Texture compression (ASTC)
   - Reduce draw calls (batching)
   - Occlusion culling
   - Distance culling

2. Target Performance:
   - 60 FPS (Snapdragon 888)
   - 30 FPS (minimum on low-end)
   - <2GB memory
   - <5W power consumption

3. Profiling:
   - Use UE5 profiler
   - Identify bottlenecks
   - Optimize hot paths
```

### **TODO 7.2: Visual Polish**
```
1. Post-Processing:
   - Bloom (subtle)
   - Color grading (stylized)
   - Motion blur (light)
   - Depth of field (background)

2. Particles:
   - Weapon effects
   - Hit effects
   - Environmental effects
   - Victory effects

3. Audio:
   - Weapon sounds
   - Footsteps
   - Ambient sounds
   - Music (dynamic)
   - Najika voice lines!
```

---

## 🎯 PHASE 8: UEFN PORT PREPARATION

### **TODO 8.1: UEFN Compatibility Audit**
```
1. Check all systems:
   - Movement: ✅ Standard CharacterMovementComponent
   - Combat: ✅ Can be converted to Verse
   - AI: ✅ Behavior Trees work in UEFN
   - UI: ⚠️ Needs Verse UI system
   - Weapons: ✅ Can be Verse classes

2. Identify blockers:
   - Custom C++ plugins (need Verse equivalent)
   - Third-party plugins (need UEFN alternative)

3. Create conversion plan:
   - Blueprint → Verse mapping
   - Asset compatibility check
```

### **TODO 8.2: Fortnite Island Prototype**
```
1. Create UEFN project
2. Import Najika character as Fortnite skin
3. Import world as island terrain
4. Convert core gameplay to Verse
5. Test in Fortnite Creative
6. Publish Island Code
7. Iterate based on feedback
```

---

## ✅ SUCCESS METRICS

### **Technical:**
```
✅ 60 FPS on Snapdragon 888
✅ <2GB memory usage
✅ <10 second load time
✅ Stable network (if multiplayer)
✅ No crashes (<0.1% rate)
```

### **Gameplay:**
```
✅ Fun combat (playtest feedback)
✅ Smooth controls (responsive)
✅ Engaging progression
✅ Replay value
✅ UEFN-ready architecture
```

---

## 📊 DEVELOPMENT SPLIT

### **This can be done by SEPARATE team/model:**
```
Team A: Digivice APK (main companion app)
Team B: Handyspiel (action game)

Both share:
- Najika character model
- Backend API (for progression)
- Art style
- Brand/IP
```

### **Timeline:**
```
Parallel development: Both finish around Week 10-12
Then merge: Handyspiel becomes "Najika World Game Mode" in Digivice
```

---

**END OF HANDYSPIEL TODO**
**Version:** 1.0
**Next Step:** Assign to separate Claude Code Web Model (higher token limit)
