# 🗺️ LEVEL DESIGN GUIDE - NAJIKA'S WORLD
**Model 1 - Digivice APK**
**Created:** 2025-11-11
**Complete World Building Guide**

---

## 🌍 WORLD OVERVIEW

### **Najika's World Concept:**

```
THEME: Die Schwarze Mühle + Fantasy + Anime

SIZE: 2400m × 2400m (expandable!)

BIOMES:
1. Village Center (Safe zone, Najika's house)
2. Forest Area (Exploration, hidden items)
3. Lake & Fishing Spots
4. Mountain Area (Challenges)
5. Secret Garden (Peaceful zone)
6. Battle Arena (Combat zone)
7. Mystery Cave (Dungeon-style)

STYLE:
→ Anime/Cel-shaded look
→ Bright colors
→ Fantasy elements
→ Cozy atmosphere
→ Mobile-optimized!
```

---

## 🏗️ ZONE 1: VILLAGE CENTER (SPAWN AREA)

### **Layout:**

```
Village Center (400m × 400m)

Points of Interest:
─────────────────────────────────────
1. Najika's House (Main building)
   - Player spawn point
   - Tamagotchi care station
   - Chat room
   - Furniture (bed, table, decorations)

2. Fountain Plaza (Center)
   - Social hub
   - Decorative fountain
   - Benches
   - Meeting point for future multiplayer

3. Item Shop (NPC building)
   - Buy food
   - Buy items
   - Sell loot
   - Quest giver (future)

4. Training Grounds
   - Practice combat
   - Tutorial area
   - Dummy enemies

5. Village Gate
   - Exit to other zones
   - Transition point
─────────────────────────────────────
```

### **Najika's House - Detailed Layout:**

```
EXTERIOR:
- Small fantasy house (anime style)
- Warm lighting from windows
- Flowers around entrance
- Najika's nameplate on door
- Size: ~10m × 10m

INTERIOR (FIRST FLOOR):
┌─────────────────────────┐
│   Najika's House        │
│                         │
│  [Bed]         [Table]  │
│                         │
│           ✧             │  ✧ = Player Spawn
│                         │
│  [Wardrobe]  [Mirror]   │
│                         │
│     [Door to Outside]   │
└─────────────────────────┘

FURNITURE:
- Bed (for sleep mechanic)
- Table (for eating)
- Wardrobe (outfit changes - future!)
- Mirror (character customization)
- Decorations (posters, plushies, anime stuff!)
- Window with view outside

INTERACTIONS:
→ Sit on bed: Sleep (restore energy!)
→ Use table: Feed Najika
→ Use mirror: Character viewer
→ Open wardrobe: Change outfit (future)
```

### **Lighting:**

```
TIME OF DAY: Fixed (or dynamic - your choice!)

VILLAGE CENTER LIGHTING:
- Warm sunlight (golden hour feel)
- Soft shadows
- Ambient occlusion
- Point lights in buildings (warm glow)
- Fountain has particle lights (sparkles!)

Sky:
→ Use UE5 Sky Atmosphere
→ Directional Light (Sun)
→ Sky Light (ambient)
→ Exponential Height Fog (atmosphere)
```

### **Assets Needed:**

```
BUILDINGS:
- House_Najika (custom or asset pack)
- House_ItemShop
- Fountain_Center
- Gate_Village

PROPS:
- Bed, Table, Chair, Wardrobe, Mirror
- Benches, Lamp posts, Flower pots
- Signs, Fences, Path stones

NATURE:
- Trees (small, decorative)
- Grass patches
- Flowers
- Bushes

OPTIMIZATION:
→ Use LODs for all meshes
→ Combine static meshes where possible
→ Bake lighting (no dynamic lights!)
→ Instanced foliage for grass/flowers
```

---

## 🌲 ZONE 2: FOREST AREA

### **Layout:**

```
Forest (600m × 600m)

Features:
─────────────────────────────────────
- Dense trees (but navigable paths!)
- Hidden treasure chests
- Wild animals (friendly NPCs)
- Mushroom patches (collectable!)
- Forest shrine (lore/quests)
- Wooden bridges over streams
- Clearings with benches (rest spots)
─────────────────────────────────────
```

### **Forest Design Tips:**

```
TREES:
- Use UE5 Foliage tool
- 3-4 tree types (variety!)
- Spacing: Not too dense (mobile performance!)
- LODs: 3 levels minimum
- Instancing: Yes!

GROUND:
- Forest floor texture (leaves, dirt)
- Moss patches
- Fallen logs
- Rocks scattered

ATMOSPHERE:
- Volumetric fog (light rays through trees!)
- Ambient sounds (birds, wind)
- Particle effects (fireflies at night!)

PATHS:
- Clear dirt paths between zones
- Markers (signs, torches)
- Mini-map icons (future feature)
```

### **Hidden Treasures:**

```
TREASURE CHEST PLACEMENT:
1. Off main path (exploration reward!)
2. Behind large tree
3. In small cave entrance
4. Near forest shrine
5. Under waterfall (if stream added)

TREASURE CONTENTS:
- Items (food, potions)
- Currency (gold, gems)
- Cosmetics (future: outfits, accessories)
- Lore items (readable notes)
```

---

## 🎣 ZONE 3: LAKE & FISHING AREA

### **Layout:**

```
Lake Area (500m × 500m)

Features:
─────────────────────────────────────
- Large central lake (60m × 60m)
- Fishing dock (interactive!)
- Beach area (sandy shore)
- Boat (decorative or rideable!)
- Lily pads & reeds
- Fish visible in water (particle effects!)
- Waterfall from mountain zone
─────────────────────────────────────
```

### **Water Setup:**

```
WATER MATERIAL: M_Water_Lake
→ See UE5_MATERIAL_TEMPLATES.md for details!

WATER SETTINGS:
- Translucent
- Refraction: 1.2
- Normal map: Animated waves
- Color: Blue-green tint
- Opacity: 0.6-0.8
- Specular: High (shiny!)

UNDERWATER (Optional):
- Post Process Volume (underwater fog!)
- Buoyancy (if player falls in)
- Swim animation (future!)
```

### **Fishing Dock:**

```
FISHING DOCK DESIGN:
- Wooden planks
- Railing (for safety!)
- Fishing rod stand
- Bucket (for caught fish)
- Bench (sit & relax)
- Lamp post (for night fishing!)

INTERACTION:
→ Walk to edge of dock
→ Press "F" (Interact)
→ Start fishing minigame (see PHASE_4_GAMEPLAY_SYSTEMS_GUIDE.md)
```

---

## ⛰️ ZONE 4: MOUNTAIN AREA

### **Layout:**

```
Mountain (400m × 800m)

Features:
─────────────────────────────────────
- Climbable paths (no actual climbing - just walkable slopes!)
- Mountain peak (highest point, scenic view!)
- Cave entrance (to Mystery Cave zone)
- Waterfall source (flows to lake)
- Rocky terrain
- Rare resources (crystals, ore)
- Stronger enemies (future battles)
─────────────────────────────────────
```

### **Terrain Setup:**

```
LANDSCAPE LAYERS:
- Rock (steep areas)
- Dirt/Gravel (paths)
- Grass (lower slopes)
- Snow (peak - optional!)

SLOPE RULES:
- Walkable: 0-45 degrees
- Too steep: >45 degrees (invisible walls or slide down)

HEIGHT MAP:
- Base: 0m
- Mid slopes: 50-100m
- Peak: 150m
- Gentle slopes for paths (15-30 degree)
```

### **Scenic View Point:**

```
MOUNTAIN PEAK:
- Flag or marker (player reached top!)
- Bench (sit & enjoy view)
- Telescope (look around world!)
- Achievement unlock: "Mountain Climber" 🏔️

VIEW:
→ Can see entire map from here!
→ Village, Forest, Lake all visible
→ Screenshot opportunity! 📸
```

---

## 🌸 ZONE 5: SECRET GARDEN

### **Layout:**

```
Secret Garden (300m × 300m)

Features:
─────────────────────────────────────
- Hidden entrance (through cave or behind waterfall)
- Beautiful flowers everywhere!
- Butterfly particles
- Peaceful music (unique to this zone!)
- Rainbow effect (particle)
- Healing fountain (restore all stats!)
- Meditation spot (boost happiness!)
─────────────────────────────────────
```

### **Garden Design:**

```
THEME: Paradise, Eden, Magical

PLANTS:
- Cherry blossom trees (anime style!)
- Flower beds (roses, tulips, sunflowers)
- Glowing plants (bioluminescent!)
- Fruit trees (apples, oranges)

ATMOSPHERE:
- Warm lighting (perpetual sunset glow)
- Sparkle particles everywhere
- No enemies (safe zone!)
- Relaxing ambience

CENTER FEATURE:
→ Healing Fountain (crystal clear water)
→ Walk into fountain → Full heal!
→ "Najika: Wow! I feel so refreshed! ✨"
```

---

## ⚔️ ZONE 6: BATTLE ARENA

### **Layout:**

```
Battle Arena (200m × 200m)

Features:
─────────────────────────────────────
- Circular arena (50m diameter)
- Stone walls/barriers (defines space)
- Entrance gate (dramatic!)
- Spectator stands (empty - for atmosphere!)
- Battle preparation zone
- Victory podium
─────────────────────────────────────
```

### **Arena Design:**

```
FLOOR:
- Stone tiles (grid pattern)
- Battle scars (cracks, burns - decorative!)
- Central emblem (Najika logo!)

WALLS:
- High stone walls (3-5m)
- Torches on walls (fire particles!)
- Banners (anime style!)

ATMOSPHERE:
- Dramatic lighting
- Sound echo effect
- Battle music (intense!)

BATTLE START:
→ Player enters through gate
→ Gate closes (locked in!)
→ Enemy spawns opposite side
→ Battle UI appears
→ FIGHT! ⚔️
```

---

## 🕳️ ZONE 7: MYSTERY CAVE (DUNGEON)

### **Layout:**

```
Mystery Cave (Dungeon - 400m paths)

Features:
─────────────────────────────────────
- Dark atmosphere (need torch!)
- Winding paths
- Dead ends & branching paths
- Treasure rooms
- Enemy encounters
- Boss room (end of cave)
- Glowing crystals (light sources)
─────────────────────────────────────
```

### **Cave Design:**

```
LIGHTING:
- Very dark (almost black!)
- Player has torch/light
- Glowing crystals (blue, purple)
- Bioluminescent mushrooms
- Fire particles (wall torches)

MATERIALS:
- Rock walls (dark grey/brown)
- Wet floor (reflective!)
- Dripping water particles
- Spider webs (decorative!)

ATMOSPHERE:
- Fog/Dust particles
- Echo sound effects
- Dripping water sounds
- Scary ambience (but not too scary!)

LAYOUT TIPS:
→ Linear with branches (not maze!)
→ Mark correct path (subtle visual cues)
→ Dead ends have treasure (reward exploration!)
→ Boss room is largest chamber
```

---

## 🎨 WORLD AESTHETICS

### **Art Style:**

```
TARGET STYLE: Anime/Cel-Shaded

TECHNIQUES:
1. Outline Shader (Post-Process)
   → See UE5_MATERIAL_TEMPLATES.md
   → M_PP_OutlineEffect

2. Color Grading (Vibrant)
   → Increase saturation (1.2-1.3×)
   → Warm color temperature
   → High contrast

3. Simple Textures
   → Not photorealistic!
   → Hand-painted look
   → Bright colors
   → Clear readability

4. Exaggerated Proportions
   → Larger heads (anime style - for NPCs!)
   → Bigger eyes
   → Stylized trees/buildings
```

### **Color Palette:**

```
PRIMARY COLORS:
- Sky Blue: #66CCFF
- Grass Green: #66FF66
- Najika Purple: #9966FF
- Warm Yellow: #FFCC66

ACCENT COLORS:
- Hot Pink: #FF66CC
- Orange: #FF9966
- Cyan: #66FFFF

USE:
→ Buildings: Warm colors (yellow, orange, brown)
→ Nature: Green, blue
→ UI: Purple, pink (Najika theme!)
→ Effects: Cyan, white (magic!)
```

---

## 🔊 ZONE AUDIO

### **Background Music:**

```
VILLAGE: Cheerful, Upbeat (home feeling)
FOREST: Mysterious, Peaceful (exploration)
LAKE: Calm, Relaxing (fishing vibe)
MOUNTAIN: Epic, Adventurous (climb energy!)
SECRET GARDEN: Dreamy, Magical (paradise)
BATTLE ARENA: Intense, Fast (combat!)
MYSTERY CAVE: Tense, Dark (dungeon)

TRANSITIONS:
→ Crossfade between zones (3-5 seconds)
→ Seamless blending
→ Volume adjusts based on distance
```

### **Ambient Sounds:**

```
VILLAGE:
- People chatting (distant)
- Birds chirping
- Fountain water
- Wind chimes

FOREST:
- Birds, crickets
- Leaves rustling
- Wind through trees
- Stream flowing (if near water)

LAKE:
- Water lapping
- Frogs croaking
- Fish splashing
- Seagulls (optional)

MOUNTAIN:
- Wind howling
- Rocks falling (distant)
- Eagles crying
- Echo effect

SECRET GARDEN:
- Soft wind
- Butterfly sounds
- Magical sparkles
- Peaceful melody

BATTLE ARENA:
- Crowd cheering (muffled - background)
- Torch fires crackling
- Metal clanging (ambient)

MYSTERY CAVE:
- Dripping water
- Echo footsteps
- Bat sounds
- Distant rumbling
```

---

## 🚶 NAVIGATION & WAYFINDING

### **Paths:**

```
MAIN PATHS:
- 5m wide
- Clear visual distinction (dirt, stone)
- Connect all major zones
- Markers every 50m (signs, torches)

SIDE PATHS:
- 2-3m wide
- Lead to secrets
- Less obvious
- Reward exploration!

PATH MATERIALS:
→ Village: Stone tiles
→ Forest: Dirt/Leaves
→ Mountain: Gravel/Rock
→ Cave: Wet stone
```

### **Signs & Markers:**

```
DIRECTIONAL SIGNS:
"← Village Center (200m)"
"→ Fishing Lake (150m)"
"↑ Mountain Path"

LOCATION SIGNS:
"Najika's House"
"Secret Garden (Shh! 🤫)"
"⚠️ Danger: Strong Enemies Ahead!"

INTERACTIVE MARKERS:
- Glowing orbs (quest markers)
- Exclamation marks (NPCs)
- Question marks (hints)
- Treasure icons (chests nearby)
```

---

## 📱 MOBILE OPTIMIZATION

### **Performance Budget:**

```
TARGET: 60 FPS on Xiaomi 11T Pro

LIMITS:
- Max Draw Calls: 500/frame
- Max Triangles Visible: 500K
- Max Texture Memory: 500MB
- Max Actors: 2000

TECHNIQUES:
1. LOD System (3 levels minimum)
2. Occlusion Culling (hide what's not visible)
3. Instanced Static Meshes (reuse meshes!)
4. Baked Lighting (no dynamic shadows!)
5. Texture Streaming (load/unload as needed)
6. Distance Culling (far objects hidden)
```

### **Level Streaming:**

```
DIVIDE WORLD INTO STREAMING LEVELS:

Persistent Level: Village Center (always loaded)
Streaming Levels:
- Forest (load when nearby)
- Lake (load when nearby)
- Mountain (load when nearby)
- Secret Garden (load when entered)
- Battle Arena (load when entered)
- Mystery Cave (load when entered)

BENEFITS:
→ Lower memory usage
→ Better performance
→ Faster loading
→ Seamless transitions
```

---

## 🎯 LEVEL DESIGN CHECKLIST

```
For each zone:

LAYOUT:
☐ Zone size defined
☐ Main path clear
☐ Side paths for exploration
☐ Points of interest placed
☐ Transitions to other zones marked

VISUALS:
☐ Terrain sculpted
☐ Textures painted
☐ Props placed (trees, rocks, etc.)
☐ Lighting setup
☐ Atmosphere effects (fog, particles)

GAMEPLAY:
☐ Interactive objects placed
☐ Collectables hidden
☐ Enemy spawn points (if combat zone)
☐ Safe zones defined

OPTIMIZATION:
☐ LODs created for all meshes
☐ Lighting baked
☐ Occlusion volumes placed
☐ Streaming setup (if zone is large)
☐ Performance tested (>30 FPS minimum)

AUDIO:
☐ Background music assigned
☐ Ambient sounds placed
☐ Audio volumes set (no too loud!)

POLISH:
☐ Skybox/Sky Atmosphere
☐ Color grading
☐ Post-processing
☐ Nav mesh generated (for AI)

TESTING:
☐ Walked through entire zone
☐ No invisible walls blocking paths
☐ All interactables work
☐ No performance drops
☐ Looks good on mobile device
```

---

## 🗺️ WORLD MAP (LAYOUT)

```
                    ⛰️ MOUNTAIN PEAK
                         |
                         |
    🌲 FOREST ---- 🏘️ VILLAGE ---- 🎣 LAKE
         |             |              |
         |         [GATES]           |
         |             |              |
    🌸 SECRET      ⚔️ ARENA      🕳️ CAVE
     GARDEN          (below)       (below)

LEGEND:
🏘️ Village Center (Spawn, Safe)
🌲 Forest (Exploration)
🎣 Lake (Fishing, Relaxing)
⛰️ Mountain (Challenge, View)
🌸 Secret Garden (Hidden, Heal)
⚔️ Battle Arena (Combat)
🕳️ Mystery Cave (Dungeon)

CONNECTIONS:
- All zones connect to Village (hub)
- Forest → Secret Garden (hidden path)
- Mountain → Cave (entrance at base)
- Lake → Waterfall → Mountain (visual connection)
```

---

## 🎉 LEVEL DESIGN COMPLETE!

**Summary:**
- ✅ 7 Zones designed
- ✅ Each zone has unique theme
- ✅ Navigation clear (paths & signs)
- ✅ Mobile-optimized
- ✅ Audio planned
- ✅ Ready to build!

**Implementation Steps:**
1. Start with Village Center (spawn point)
2. Add Forest (first exploration zone)
3. Add Lake (relaxing zone)
4. Expand to Mountain, Garden, Arena, Cave
5. Optimize performance
6. Polish & test!

**Next:** Create all assets in UE5 Content Browser, follow this guide!

---

**Model 1 - Digivice APK Development**
**Guide:** Complete Level Design
**Status:** Ready to Build! ✅

**BUILD NAJIKA'S WORLD! 🗺️🚀**
