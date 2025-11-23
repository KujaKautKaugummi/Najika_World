# 🎨 Asset Requirements - Complete Specifications

**Complete technical specifications for all required assets**

This document specifies EVERY asset needed for the Najika Digivice project, including:
- 3D models (characters, props, environment)
- Animations (locomotion, combat, emotes)
- UI assets (icons, buttons, fonts)
- Audio (music, SFX, voice)
- Materials and textures

**Target Platform:** Mobile (Xiaomi 11T Pro - Snapdragon 888, ARM64)
**Engine:** Unreal Engine 5.6
**Art Style:** Anime / Cel-Shaded

---

## 📋 Table of Contents

1. [3D Character Models](#1-3d-character-models)
2. [Animations](#2-animations)
3. [UI Assets](#3-ui-assets)
4. [Audio Assets](#4-audio-assets)
5. [Environment Assets](#5-environment-assets)
6. [Materials & Shaders](#6-materials--shaders)
7. [Font Assets](#7-font-assets)
8. [Asset Delivery Format](#8-asset-delivery-format)
9. [Import Settings](#9-import-settings)
10. [Priority Checklist](#10-priority-checklist)
11. [Asset Sources](#11-asset-sources)

---

## 1. 3D Character Models

### 1.1 Najika Main Character

**Priority:** 🔴 CRITICAL (MVP)
**Polycount:** 15,000 - 25,000 triangles (mobile optimized)
**Format:** FBX 2020
**Skeleton:** UE5 Mannequin compatible (for animation retargeting)

**Textures Required:**

| Texture Type | Resolution | Format | Usage |
|--------------|------------|--------|-------|
| Base Color (Diffuse) | 2048x2048 | PNG | Main color/albedo |
| Normal Map | 2048x2048 | PNG | Surface details |
| Roughness Map | 2048x2048 | PNG | Surface smoothness |
| Metallic Map | 2048x2048 | PNG | Metal areas |
| Emissive Map | 1024x1024 | PNG (Optional) | Glowing elements |
| Opacity Mask | 1024x1024 | PNG (Optional) | Hair alpha |

**Level of Detail (LOD):**

- **LOD0:** 25,000 tris (full detail, 0-5m distance)
- **LOD1:** 15,000 tris (medium, 5-15m)
- **LOD2:** 8,000 tris (low, 15-30m)
- **LOD3:** 3,000 tris (very low, 30m+)

**Mesh Components (Separable Parts):**

1. **Body** (Base mesh)
   - Torso, arms, legs
   - Should be one continuous mesh for efficiency

2. **Head**
   - Include blend shapes for facial expressions:
     - Neutral (default)
     - Happy (smile)
     - Sad (frown)
     - Angry (eyebrows down)
     - Surprised (eyes wide)
     - Talk (mouth open variations - A, E, I, O, U)

3. **Hair**
   - Separate mesh from head
   - Alpha-masked transparency
   - Physics bones for movement (5-10 bones)

4. **Eyes**
   - Separate spheres (left + right)
   - UV mapped for eye shader
   - Socket bones for look-at system

5. **Outfit (4 Costume Variants)**
   - Default: School uniform / casual
   - Combat: Battle outfit
   - Formal: Dress / special occasion
   - Swimsuit: Beach / pool area
   - Each outfit: separate mesh, same skeleton

6. **Accessories (Optional)**
   - Hat (socket attachment)
   - Glasses (socket)
   - Earrings (socket)
   - Backpack (socket)

**Rigging Requirements:**

- **Main Skeleton:** UE5 Mannequin hierarchy (54 bones)
  - Root
  - Pelvis → Spine → Chest → Neck → Head
  - Left/Right: Clavicle → Shoulder → Elbow → Wrist → Hand (5 fingers each)
  - Left/Right: Thigh → Knee → Ankle → Foot → Toes

- **Facial Rig:** 32 additional bones
  - Jaw (open/close)
  - Eyebrows (left/right, up/down)
  - Eyelids (left/right, blink)
  - Lips (corners, upper, lower)
  - Cheeks (puff)

- **IK Bones:**
  - IK_Foot_L / IK_Foot_R (for foot placement)
  - IK_Hand_L / IK_Hand_R (for hand placement)

- **Physics Bones (Hair/Cloth):**
  - Hair_01 through Hair_10 (ponytail, side strands)
  - Skirt_F, Skirt_B, Skirt_L, Skirt_R (if applicable)

**Technical Specs:**

- Pivot Point: Ground level, centered
- Scale: 1 Unreal Unit = 1 cm (character ~170cm tall)
- Up Axis: Z-up
- Forward Axis: X-forward
- Handedness: Right-handed
- Bone Orientation: X-forward, Y-right, Z-up

**File Naming:**

```
Najika_Character_LOD0.fbx
Najika_Character_LOD1.fbx
Najika_Character_LOD2.fbx
Najika_Character_LOD3.fbx
Najika_Outfit_Default.fbx
Najika_Outfit_Combat.fbx
Najika_Outfit_Formal.fbx
Najika_Outfit_Swimsuit.fbx
Najika_Hair_01.fbx
Najika_Accessories_Hat_01.fbx
...
```

**Texture Naming:**

```
T_Najika_Body_BaseColor.png
T_Najika_Body_Normal.png
T_Najika_Body_Roughness.png
T_Najika_Body_Metallic.png
T_Najika_Hair_BaseColor.png
T_Najika_Hair_Alpha.png
T_Najika_Eyes_BaseColor.png
...
```

---

### 1.2 Enemy Characters (Lower Priority)

**Priority:** 🟡 MEDIUM (Post-MVP)
**Quantity:** 5-10 enemy types
**Polycount:** 8,000 - 15,000 tris each

**Enemy Types:**

1. **Goblin** (Melee)
2. **Skeleton** (Melee/Ranged)
3. **Slime** (Simple, low poly)
4. **Orc** (Heavy melee)
5. **Witch** (Ranged magic)

**Requirements:**

- Same skeleton as Najika (for animation sharing)
- LOD0 + LOD1 only (less detail needed)
- Textures: 1024x1024 (lower res than player)
- Simplified rigging (no facial bones needed)

---

## 2. Animations

**Format:** FBX 2020, 30 FPS
**Skeleton:** UE5 Mannequin compatible
**Total Required:** ~45 animations

---

### 2.1 Locomotion Animations (CRITICAL - MVP)

**Priority:** 🔴 CRITICAL

| Animation | Duration | Loop | Description |
|-----------|----------|------|-------------|
| Idle | 60 frames (2s) | ✅ | Standing still, breathing |
| Walk_Forward | 40 frames | ✅ | Normal walking |
| Walk_Backward | 40 frames | ✅ | Walking backwards |
| Walk_Left | 40 frames | ✅ | Strafing left |
| Walk_Right | 40 frames | ✅ | Strafing right |
| Run_Forward | 30 frames (1s) | ✅ | Running fast |
| Jump_Start | 20 frames | ❌ | Jump takeoff |
| Jump_Loop | 20 frames | ✅ | In-air falling |
| Jump_Land | 15 frames | ❌ | Landing impact |

**Total:** 9 animations

**Blendspace Setup:**

- **Locomotion 2D Blendspace:**
  - Horizontal Axis: Move Direction (-180° to 180°)
  - Vertical Axis: Speed (0 = Idle, 300 = Walk, 600 = Run)
  - Samples: Idle (center), Walk Forward/Back/Left/Right, Run Forward

---

### 2.2 Combat Animations (HIGH Priority)

**Priority:** 🟠 HIGH

| Animation | Duration | Type | Damage Frame |
|-----------|----------|------|--------------|
| Attack_Punch_1 | 30 frames | Combo 1 | Frame 15 |
| Attack_Punch_2 | 35 frames | Combo 2 | Frame 18 |
| Attack_Punch_3 | 40 frames | Combo Finisher | Frame 25 |
| Attack_Kick | 40 frames | Heavy | Frame 20 |
| Cast_Spell | 60 frames (2s) | Magic | Frame 40 |
| Block_Idle | 30 frames | Loop | - |
| Dodge_Roll | 40 frames | Evasion | - |
| Hit_Front | 20 frames | React | - |
| Hit_Back | 20 frames | React | - |
| Death | 120 frames (4s) | Final | - |

**Total:** 10 animations

**Animation Notifies:**

- **AN_DealDamage** (placed on damage frame)
- **AN_PlaySound** (whoosh, impact, etc.)
- **AN_ParticleEffect** (VFX spawn)
- **AN_IFrameStart / IFrameEnd** (invincibility window)

---

### 2.3 Interaction Animations (MEDIUM Priority)

**Priority:** 🟡 MEDIUM

| Animation | Duration | Use Case |
|-----------|----------|----------|
| Pickup_Item | 40 frames | Picking up objects |
| Use_Item | 50 frames | Using consumables |
| Open_Door | 40 frames | Door interaction |
| Talk | 60 frames, Loop | Dialogue scenes |
| Sit_Down | 40 frames | Entering seated state |
| Sit_Idle | 60 frames, Loop | Sitting animation |
| Stand_Up | 30 frames | Exiting seated state |
| Eat | 80 frames | Eating food |
| Drink | 60 frames | Drinking potion |

**Total:** 9 animations

---

### 2.4 Emote Animations (LOW Priority)

**Priority:** 🟢 LOW (Post-MVP, Social Features)

| Animation | Duration | Description |
|-----------|----------|-------------|
| Wave | 60 frames (2s) | Greeting |
| Cheer | 80 frames | Celebration |
| Dance | 120 frames, Loop | Dancing |
| Laugh | 60 frames | Laughing |
| Cry | 80 frames, Loop | Crying |
| Salute | 50 frames | Formal greeting |
| Thumbs_Up | 40 frames | Approval |
| Clap | 60 frames, Loop | Applause |

**Total:** 8 animations

---

### 2.5 Special Animations (OPTIONAL)

**Priority:** 🟢 OPTIONAL

- Swim_Idle (loop)
- Swim_Forward (loop)
- Climb_Idle (loop)
- Climb_Up (loop)
- Glide (loop, for glider item)
- Mount_Horse (transition)
- Riding_Horse_Idle (loop)

**Total:** 7 animations

---

### Animation Summary

**Total Animations:** 43 minimum (MVP = 19 critical)

**File Naming:**

```
Anim_Najika_Idle.fbx
Anim_Najika_Walk_Forward.fbx
Anim_Najika_Attack_Punch_1.fbx
...
```

**Import Settings in UE5:**

- Skeleton: Najika_Skeleton
- Animation Length: Exported Time
- Sample Rate: 30 FPS
- Import Bone Tracks: ✅
- Import Custom Attributes: ✅
- Remove Redundant Keys: ✅ (Tolerance: 0.001)

---

## 3. UI Assets

### 3.1 Icons (256x256 PNG with Alpha)

**Priority:** 🔴 CRITICAL
**Quantity:** ~120 icons
**Format:** PNG, 256x256 pixels, Transparent background
**Style:** Flat design, vibrant colors, clear silhouettes

**Categories:**

**Items (60 icons):**

- Consumables (20):
  - Health Potion (small, medium, large)
  - Mana Potion (small, medium, large)
  - Stamina Potion
  - Antidote
  - Food items (bread, apple, meat, water, etc.)
  - Elixir (full restore)

- Equipment (25):
  - Weapons: Sword, Bow, Staff, Dagger, Axe
  - Armor: Helmet, Chestplate, Gloves, Boots, Shield
  - Accessories: Ring, Necklace, Bracelet, Earring, Amulet

- Materials (15):
  - Wood, Stone, Iron Ore, Gold Ore
  - Herbs, Flowers, Crystals
  - Leather, Cloth, Thread
  - Special materials (rare)

**Skills (25 icons):**

- Combat Skills (10):
  - Slash, Stab, Bash, Whirlwind
  - Fireball, Ice Shard, Lightning Bolt
  - Heal, Shield, Buff

- Passive Skills (10):
  - Strength Up, Speed Up, Defense Up
  - HP Regen, MP Regen
  - Critical Hit, Evasion
  - Experience Boost

- Magic Schools (5):
  - Fire Magic, Ice Magic, Lightning Magic
  - Healing Magic, Dark Magic

**Status Effects (20 icons):**

- Buffs (10):
  - Attack Up, Defense Up, Speed Up
  - Regeneration, Protection, Haste
  - Lucky, Blessed, Inspired

- Debuffs (10):
  - Poison, Burn, Freeze, Stun
  - Slow, Weakness, Curse, Bleed

**UI Elements (15 icons):**

- Menu: Settings, Inventory, Map, Quest, Social
- Actions: Confirm, Cancel, Back, Close, Help
- Indicators: Arrow Up/Down/Left/Right, Checkmark, X

**File Naming:**

```
Icon_Potion_Health_Small.png
Icon_Sword_Iron.png
Icon_Skill_Fireball.png
Icon_Buff_AttackUp.png
Icon_UI_Settings.png
...
```

---

### 3.2 Buttons & UI Elements

**Priority:** 🔴 CRITICAL
**Format:** PNG, 9-Slice compatible (borders stretchable)

**Button Set (3 Variants x 4 States = 12 Images):**

**Variants:**

1. Primary (Green) - Confirm actions
2. Secondary (Blue) - Info/neutral
3. Danger (Red) - Delete/destructive

**States (each variant):**

- Normal (default)
- Hovered (mouse over)
- Pressed (clicked)
- Disabled (grayed out)

**Sizes:**

- Large: 512x128 pixels
- Medium: 256x64 pixels
- Small: 128x32 pixels

**9-Slice Borders:**

- Border Width: 16px on all sides (for stretching)

**File Naming:**

```
Button_Primary_Normal.png
Button_Primary_Hovered.png
Button_Primary_Pressed.png
Button_Primary_Disabled.png
Button_Secondary_Normal.png
...
```

---

### 3.3 Panels & Backgrounds

**Format:** PNG, tileable or 9-slice

| Asset | Size | Type | Usage |
|-------|------|------|-------|
| Panel_Background | 1024x1024 | Tileable | Window backgrounds |
| Panel_Border | 512x512 | 9-Slice | Window frames |
| Panel_Header | 1024x128 | 9-Slice | Title bars |
| Divider_Horizontal | 512x8 | Stretchable | Section separators |
| Divider_Vertical | 8x512 | Stretchable | Column separators |
| Scroll_Bar_Track | 32x256 | 9-Slice | Scrollbar background |
| Scroll_Bar_Thumb | 32x64 | - | Scrollbar handle |
| Tooltip_Background | 256x128 | 9-Slice | Hover tooltips |

---

### 3.4 HUD Elements

**Priority:** 🔴 CRITICAL

| Asset | Size | Format | Description |
|-------|------|--------|-------------|
| Healthbar_Fill | 512x64 | PNG | Red gradient bar |
| Healthbar_Background | 512x64 | PNG | Dark red backing |
| Manabar_Fill | 512x64 | PNG | Blue gradient bar |
| Manabar_Background | 512x64 | PNG | Dark blue backing |
| Staminabar_Fill | 512x64 | PNG | Yellow gradient |
| Experiencebar_Fill | 512x64 | PNG | Green gradient |
| Crosshair_Default | 64x64 | PNG, Alpha | White crosshair |
| Crosshair_Enemy | 64x64 | PNG, Alpha | Red crosshair (enemy targeted) |
| Minimap_Border | 256x256 | PNG | Circular frame |
| Minimap_Mask | 256x256 | PNG | Circular mask |
| Damage_Number_Font | Spritesheet | PNG | Floating damage numbers |
| Level_Up_Effect | 512x512 | PNG Sequence | Level up burst (8 frames) |

---

## 4. Audio Assets

### 4.1 Music (Background Music)

**Priority:** 🟠 HIGH
**Format:** OGG Vorbis, 44.1kHz, Stereo, ~128kbps
**Length:** 2-5 minutes, seamlessly looping

**Tracks:**

| Track Name | Duration | Mood | Usage |
|------------|----------|------|-------|
| MainMenu_Theme | 2-3 min | Upbeat, Welcoming | Main menu screen |
| Gameplay_Ambient | 4-5 min | Adventurous, Energetic | Exploration, towns |
| Combat_Intense | 2-3 min | Fast-paced, Drums heavy | Combat encounters |
| Boss_Battle | 3-4 min | Epic, Orchestral | Boss fights |
| Victory_Fanfare | 10-15 sec | Triumphant | Battle victory |
| Level_Up_Jingle | 5 sec | Cheerful | Level up moment |
| Game_Over | 10-15 sec | Somber | Death screen |
| Peaceful_Night | 3-4 min, Loop | Calm, Relaxing | Safe areas, rest |

**Total:** 8 music tracks

**File Naming:**

```
Music_MainMenu_Theme.ogg
Music_Gameplay_Ambient.ogg
Music_Combat_Intense.ogg
...
```

---

### 4.2 Sound Effects (SFX)

**Priority:** 🔴 CRITICAL
**Format:** WAV, 44.1kHz, Mono (or Stereo for ambience), 16-bit
**Length:** 0.5 - 3 seconds

**UI Sounds (HIGH Priority - 15 SFX):**

- Button_Click (short, satisfying)
- Button_Hover (subtle)
- Menu_Open (swish)
- Menu_Close (swish)
- Item_Pickup (ding)
- Item_Drop (thud)
- Level_Up (celebration sound)
- Quest_Complete (success chime)
- Error (buzzer)
- Notification (ping)
- Tab_Switch (click)
- Scroll (subtle whoosh)
- Inventory_Full (error buzz)
- Gold_Coin (jingle)
- Dialogue_Beep (text typing sound)

**Combat Sounds (HIGH Priority - 25 SFX):**

- Punch_Hit_1, 2, 3 (variations)
- Kick_Hit (heavy impact)
- Sword_Swing_1, 2, 3 (whoosh)
- Sword_Hit_Metal (clang)
- Sword_Hit_Flesh (schlick)
- Bow_Draw (creak)
- Arrow_Release (twang)
- Arrow_Hit (thunk)
- Spell_Cast (magical whoosh)
- Spell_Impact_Fire (boom)
- Spell_Impact_Ice (shatter)
- Spell_Impact_Lightning (zap)
- Block_Success (shield sound)
- Damage_Taken_Player (grunt/ouch)
- Damage_Taken_Enemy (enemy pain sound)
- Heal_Spell (magical sparkle)
- Buff_Applied (positive chime)
- Debuff_Applied (negative tone)
- Critical_Hit (special impact)
- Dodge_Success (whoosh)

**Environment Sounds (MEDIUM Priority - 20 SFX):**

- Footstep_Grass_1, 2, 3, 4 (variations)
- Footstep_Stone_1, 2, 3, 4
- Footstep_Wood_1, 2, 3, 4
- Door_Open (creak)
- Door_Close (thud)
- Chest_Open (latch + creak)
- Chest_Close (thud)
- Water_Splash (jump in water)
- Fire_Crackling (campfire, loop)
- Wind_Ambience (outdoor, loop)
- Birds_Chirping (daytime, loop)
- Crickets (nighttime, loop)

**Total SFX:** ~60 sounds

**File Naming:**

```
SFX_UI_Button_Click.wav
SFX_Combat_Punch_Hit_01.wav
SFX_Footstep_Grass_01.wav
...
```

---

### 4.3 Voice Lines (OPTIONAL)

**Priority:** 🟢 LOW (Post-MVP)
**Format:** MP3 or OGG Vorbis, 44.1kHz, Mono, ~64kbps
**Language:** Japanese (with subtitles)

**Najika Voice Lines:**

- Greetings (5 variations)
- Combat Attacks (10 battle cries)
- Hurt Sounds (5 pain reactions)
- Victory (3 celebration lines)
- Death (1 final words)
- Emotes (laugh, cry, cheer - 5 total)

**Total:** ~30 voice clips

**File Naming:**

```
Voice_Najika_Greeting_01_JP.ogg
Voice_Najika_Attack_01_JP.ogg
...
```

---

## 5. Environment Assets

**Priority:** 🟡 MEDIUM (Can use placeholders initially)

### 5.1 Terrain Materials

**Format:** Material with 4 textures each (Base Color, Normal, Roughness, Height)
**Resolution:** 1024x1024 (tileable)

**Required Terrains:**

1. **Grass** (default ground)
2. **Rock** (mountains, cliffs)
3. **Dirt** (paths, cleared areas)
4. **Sand** (beach, desert areas)
5. **Water** (lake, ocean - with shader)

**Each Material Set:**

- T_[Terrain]_BaseColor.png
- T_[Terrain]_Normal.png
- T_[Terrain]_Roughness.png
- T_[Terrain]_Height.png

---

### 5.2 Props & Environment Objects

**Priority:** 🟢 LOW (Use Marketplace assets initially)

**Recommended Sources:**

- **Trees:** 5-10 variations (palm, oak, pine)
- **Rocks:** 10-15 variations (small to large boulders)
- **Grass:** Foliage clusters (auto-placed)
- **Buildings:** Placeholder boxes OK (can use from Marketplace)
- **Interactive Objects:**
  - Chest (openable)
  - Door (swinging)
  - Campfire
  - Signpost
  - NPCs (use simple capsules initially)

**Suggested Marketplace Packs:**

- KayKit Character Pack (FREE) - for placeholder characters
- Stylized Forest Pack
- Modular Building Kit

---

## 6. Materials & Shaders

### 6.1 Character Master Material

**Name:** `M_Character_Master`
**Type:** Material with Material Instances

**Features:**

- Cel-Shading (anime look)
- Outline/Rim Light
- Subsurface scattering (skin)
- Two-sided foliage (hair transparency)
- Color tinting support

**Inputs:**

- Base Color Texture
- Normal Map
- Roughness Map
- Metallic Map
- Emissive Map (optional)
- Color Tint (parameter)
- Outline Width (parameter, default 0.1)
- Outline Color (parameter, default black)

**Material Instances (4):**

- MI_Najika_Default
- MI_Najika_Combat
- MI_Najika_Formal
- MI_Najika_Swimsuit

---

### 6.2 UI Material

**Name:** `M_UI_Master`
**Type:** Unlit, Translucent

**Features:**

- Supports color tinting
- Alpha masking
- Sprite animation (for effects)

---

### 6.3 VFX Materials

**For Spell Effects:**

- Additive blending
- Distortion (heat haze)
- Particle textures (smoke, fire, sparks)

---

## 7. Font Assets

### 7.1 UI Font

**Name:** Roboto or Noto Sans
**License:** Open Font License (FREE)
**Formats:** Regular, Bold
**Sizes Needed:** 14, 18, 24, 32, 48, 64 pt

**Language Support:**

- Latin (English) ✅
- CJK (Japanese/Chinese) ✅ (Use Noto Sans CJK)

**File Format:** TTF or OTF

**File Naming:**

```
Roboto-Regular.ttf
Roboto-Bold.ttf
NotoSansCJK-Regular.otf
```

---

### 7.2 Damage Number Font

**Style:** Bold, outlined, easy to read
**Recommended:** Impact or similar thick font
**Usage:** Floating damage numbers in combat

---

## 8. Asset Delivery Format

All assets should be organized in this folder structure:

```
Assets_Package/
├── Characters/
│   └── Najika/
│       ├── Meshes/
│       │   ├── Najika_Character_LOD0.fbx
│       │   ├── Najika_Outfit_Default.fbx
│       │   └── ...
│       ├── Textures/
│       │   ├── T_Najika_Body_BaseColor.png
│       │   ├── T_Najika_Body_Normal.png
│       │   └── ...
│       └── Animations/
│           ├── Anim_Najika_Idle.fbx
│           ├── Anim_Najika_Walk_Forward.fbx
│           └── ...
├── UI/
│   ├── Icons/
│   │   ├── Items/
│   │   ├── Skills/
│   │   ├── Status/
│   │   └── UIElements/
│   ├── Buttons/
│   │   ├── Button_Primary_Normal.png
│   │   └── ...
│   └── Panels/
│       ├── Panel_Background.png
│       └── ...
├── Audio/
│   ├── Music/
│   │   ├── Music_MainMenu_Theme.ogg
│   │   └── ...
│   ├── SFX/
│   │   ├── UI/
│   │   ├── Combat/
│   │   └── Environment/
│   └── Voice/
│       └── Najika/
├── Environment/
│   └── Terrain/
│       ├── Grass/
│       ├── Rock/
│       └── ...
└── Materials/
    └── (Material files exported from Substance Painter, etc.)
```

---

## 9. Import Settings (for Local Model)

### 9.1 Static Meshes

**When importing .fbx environment props:**

- Skeletal Mesh: ❌ (disable)
- Import Materials: ✅
- Import Textures: ✅
- Auto Generate Collision: ✅
- Combine Meshes: ✅ (for multiple parts)
- Generate Lightmap UVs: ✅
- Lightmap Resolution: 128 or 256

---

### 9.2 Skeletal Meshes (Character)

**When importing Najika_Character.fbx:**

- Skeletal Mesh: ✅
- Skeleton: Create new "Najika_Skeleton" (first import) or use existing
- Import Materials: ✅
- Import Textures: ✅
- Preserve Smoothing Groups: ✅
- Update Skeleton Reference Pose: ✅
- Use T0 as Ref Pose: ❌

---

### 9.3 Animations

**When importing Anim_*.fbx:**

- Skeleton: Select "Najika_Skeleton"
- Animation Length: Exported Time
- Import Bone Tracks: ✅
- Import Custom Attributes: ✅
- Remove Redundant Keys: ✅ (Tolerance: 0.001)
- Preserve Local Transform: ❌
- Sample Rate: 30

---

### 9.4 Textures

**Auto-import settings:**

- sRGB: ✅ (for Base Color, Emissive)
- sRGB: ❌ (for Normal, Roughness, Metallic)
- Compression: TC_Default (Base Color)
- Compression: TC_Normalmap (Normal)
- Compression: TC_Masks (Roughness, Metallic)
- MipGenSettings: Sharpen0
- Texture Group: Character (for characters)

---

### 9.5 Audio

**Music:**

- Format: OGG
- Quality: Compressed (128 kbps)
- Loading Behavior: Streaming ✅

**SFX:**

- Format: WAV
- Quality: Uncompressed PCM
- Loading Behavior: Decompress On Load ✅

---

## 10. Priority Checklist

### Phase 1: MVP (Minimum Viable Product)

**Must-Have for First Build:**

**3D Assets:**
- [x] Najika Character Model (1x, LOD0 only)
- [x] Placeholder skeleton/capsule for enemies

**Animations:**
- [x] Locomotion Set (9 animations)
- [x] Basic Combat (Attack x1, Block, Hit, Death)

**UI Assets:**
- [x] Essential Icons (30x: potions, weapons, UI buttons)
- [x] Button Set (Primary variant, 4 states)
- [x] HUD Elements (health bar, mana bar)

**Audio:**
- [x] UI Sounds (10x: click, hover, notification)
- [x] Combat Sounds (10x: punch, sword, magic)
- [x] Music (2x: Main Menu, Gameplay)

**Total MVP Assets:** ~60 files

---

### Phase 2: Full Release

**Complete the Game:**

**3D Assets:**
- [x] All LODs for Najika (LOD1, 2, 3)
- [x] All 4 Costume Variants
- [x] Enemy Characters (5 types)

**Animations:**
- [x] All 43 animations
- [x] Facial expressions (blend shapes)

**UI Assets:**
- [x] All 120 icons
- [x] All UI elements (complete set)

**Audio:**
- [x] All 8 music tracks
- [x] All 60 SFX
- [x] Voice lines (optional)

**Environment:**
- [x] Terrain materials (5 types)
- [x] Environment props (from Marketplace or custom)

**Total Full Release:** ~300-400 files

---

## 11. Asset Sources

### 11.1 FREE Resources

**3D Models:**

- **Mixamo** (https://www.mixamo.com)
  - FREE rigged characters
  - FREE animations (can retarget to UE5 Mannequin)
  - License: Can use in commercial projects ✅

- **Sketchfab** (https://sketchfab.com)
  - Search "Free Download" + "Creative Commons"
  - Many anime-style characters available
  - Check license per model

- **Unreal Marketplace FREE Assets:**
  - KayKit Character Pack (FREE)
  - Stylized Character Pack (FREE monthly)

**UI Assets:**

- **Kenney.nl** (https://kenney.nl)
  - 1000s of FREE UI assets
  - Icons, buttons, panels
  - License: CC0 (public domain) ✅

- **Game-Icons.net** (https://game-icons.net)
  - 3000+ FREE game icons
  - SVG format (scalable)
  - License: CC BY 3.0

**Audio:**

- **Freesound.org** (https://freesound.org)
  - Huge library of SFX
  - License varies (check per sound)

- **Incompetech** (https://incompetech.com/music)
  - FREE music by Kevin MacLeod
  - License: CC BY (credit required)

- **Purple Planet Music** (https://www.purple-planet.com)
  - FREE game music
  - License: Free with attribution

**Fonts:**

- **Google Fonts** (https://fonts.google.com)
  - Roboto, Noto Sans, etc.
  - License: Open Font License ✅

---

### 11.2 PAID Resources (Premium Quality)

**3D Models:**

- **TurboSquid** (https://www.turbosquid.com)
  - Professional 3D models
  - ~$50-200 per character

- **CGTrader** (https://www.cgtrader.com)
  - Lower prices than TurboSquid
  - ~$20-100 per character

- **ArtStation Marketplace** (https://www.artstation.com/marketplace)
  - High-quality game assets
  - ~$30-150

**Audio:**

- **AudioJungle** (https://audiojungle.net)
  - Music tracks ~$20-50
  - SFX packs ~$10-30

- **Epidemic Sound** (https://www.epidemicsound.com)
  - Subscription: $15/month
  - Unlimited music downloads

**Complete Asset Packs:**

- **Unreal Marketplace**
  - Search "Stylized Character"
  - Full packs: $50-200
  - Includes models + animations

---

### 11.3 Commission Custom Assets

**If budget allows:**

**Character Artist:**

- Fiverr / ArtStation Freelancers
- Price: $300-1000 for full rigged character with textures
- Timeline: 2-4 weeks

**Animator:**

- Upwork / Fiverr
- Price: $20-50 per animation
- Timeline: 1 week for 10 animations

**UI Artist:**

- Fiverr
- Price: $100-300 for complete UI pack
- Timeline: 1-2 weeks

**Audio Composer:**

- Price: $200-500 per music track
- Price: $50-100 for SFX pack
- Timeline: 2-3 weeks

---

## 📊 Asset Budget Estimate

### FREE Approach (Marketplace + Free Resources)

**Cost:** $0
**Time:** 2-3 weeks (searching, downloading, importing)
**Quality:** 7/10 (good for prototype/MVP)

---

### PAID Approach (Premium Assets)

**3D Character:** $500 (custom commission)
**Animations:** $800 (40 anims x $20)
**UI Pack:** $200
**Audio Pack:** $400 (music + SFX)
**Environment:** $100 (Marketplace pack)

**Total:** ~$2000
**Time:** 4-6 weeks
**Quality:** 9/10 (professional)

---

## ✅ Final Asset Checklist

**Before starting UE5 import:**

- [ ] All character models (.fbx) with textures
- [ ] All animations (.fbx) compatible with skeleton
- [ ] All UI icons (PNG, 256x256, transparent)
- [ ] All UI buttons (PNG, 9-slice ready)
- [ ] All audio files (OGG for music, WAV for SFX)
- [ ] All fonts (TTF/OTF)
- [ ] Materials/textures organized by category
- [ ] Asset folder structure matches delivery format

**If checklist complete → Import to UE5 using Import Settings (Section 9)**

---

**End of Asset Requirements**

**Created:** 2025-11-13
**For:** Local Model - Najika Digivice UE5 Project
**Author:** Claude Code Web Model
**Lines:** ~1,500
