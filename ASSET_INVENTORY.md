# 📦 NAJIKA DIGIVICE - ASSET INVENTORY
**Project:** Najika Digivice UE5 Migration
**Purpose:** Complete list of all assets needed for UE5 implementation
**Status:** Specification Phase (assets to be sourced/created)

---

## 🎨 ASSET SUMMARY

| Category | Count | Total Size (Est.) | Source |
|----------|-------|-------------------|--------|
| 3D Models (Characters) | 1 | ~50 MB | KayKit AnimatedCharacter |
| 3D Models (Environment) | 50+ | ~200 MB | KayKit Dungeon/Adventurers |
| Textures | 100+ | ~150 MB | KayKit Packs |
| Animations | 15+ | ~20 MB | KayKit AnimatedCharacter |
| Audio (Music) | 10+ | ~50 MB | Custom/Royalty-Free |
| Audio (SFX) | 50+ | ~25 MB | Custom/Royalty-Free |
| UI Icons | 100+ | ~10 MB | Custom/UI Pack |
| Particle Effects | 20+ | ~15 MB | UE5 Niagara |
| **TOTAL** | **346+** | **~520 MB** | - |

---

## 👤 CHARACTER ASSETS

### Najika Character
```
Source: KayKit AnimatedCharacter Pack
Format: GLTF/GLB
Poly Count: ~5,000 triangles
Textures: 1024x1024 (Diffuse, Normal, Roughness)
Rig: Humanoid skeleton (Mixamo-compatible)
```

**Files:**
- `Character_Najika.glb` - Main character model
- `Character_Najika_Diffuse.png` - Texture
- `Character_Najika_Normal.png` - Normal map

**Customization:**
- Hair: Purple/pink gradient
- Eyes: Red/crimson
- Outfit: Megumin-style (red/black)
- Accessories: Hat, cape, staff

---

## 🎬 ANIMATION ASSETS

### Character Animations (KayKit AnimatedCharacter)

| Animation | Duration | Loop | Priority | Use Case |
|-----------|----------|------|----------|----------|
| Idle | 2s | ✅ | 0 | Standing still |
| Walk | 1s | ✅ | 1 | Walking (WASD) |
| Run | 0.8s | ✅ | 2 | Running (Shift+WASD) |
| Jump_Start | 0.3s | ❌ | 5 | Jump beginning |
| Jump_Loop | 0.5s | ✅ | 5 | Airborne |
| Jump_End | 0.3s | ❌ | 5 | Landing |
| Attack_1 | 0.6s | ❌ | 10 | Light attack (Q) |
| Attack_2 | 0.8s | ❌ | 10 | Heavy attack (E) |
| Attack_3 | 1.0s | ❌ | 10 | Dual strike |
| Block | 1.5s | ✅ | 8 | Blocking |
| Parry | 0.4s | ❌ | 9 | Parry window |
| Dodge_Roll | 0.5s | ❌ | 9 | Dodge i-frames |
| Hit | 0.3s | ❌ | 9 | Taking damage |
| Death | 2.0s | ❌ | 15 | Death animation |
| Eat | 2.0s | ❌ | 3 | Feeding action |
| Drink | 1.5s | ❌ | 3 | Drinking action |
| Sit | 1.0s | ✅ | 1 | Sitting on furniture |
| Sleep | 3.0s | ✅ | 1 | Sleeping in bed |

**Total:** 18 animations

---

## 🏠 ENVIRONMENT ASSETS

### Rooms (KayKit Dungeon Pack / Adventurers Pack)

| Room | 3D Model | Poly Count | Textures | Size (units) |
|------|----------|------------|----------|--------------|
| Wohnzimmer (Living Room) | Living_Room.glb | ~10k | 3 | 24x24 |
| Schlafzimmer (Bedroom) | Bedroom.glb | ~8k | 3 | 20x20 |
| Küche (Kitchen) | Kitchen.glb | ~12k | 4 | 20x20 |
| Badezimmer (Bathroom) | Bathroom.glb | ~6k | 2 | 16x16 |
| Garten (Garden) | Garden.glb | ~15k | 5 | 32x32 |
| Musikraum (Music Room) | Music_Room.glb | ~8k | 3 | 20x20 |
| Medizin (Medical Room) | Medical_Room.glb | ~7k | 3 | 18x18 |
| Terminal (Tech Room) | Terminal_Room.glb | ~9k | 4 | 20x20 |
| Studieren & Crafting | Crafting_Room.glb | ~11k | 4 | 24x24 |
| Trainingszimmer | Training_Room.glb | ~10k | 3 | 28x28 |
| Kampfarena | Arena.glb | ~20k | 6 | 40x40 |
| Schwarze Mühle – Keller | Dungeon_Basement.glb | ~18k | 5 | 36x36 |

**Total:** 12 room models (~134k triangles)

### Props & Furniture (Per Room)
- Sofa, Chair, Table, Bed, Desk, Bookshelf, etc.
- ~20 props per room
- **Total:** ~240 prop models

### Dungeon Assets (KayKit Dungeon Pack)
- Wall segments (straight, corner, T-junction, cross)
- Floor tiles (stone, wood, dirt)
- Doors (wooden, iron, secret)
- Torches, braziers, candles
- Chests, barrels, crates
- Pillars, arches, stairs
- **Total:** ~50 dungeon pieces

---

## 🎨 TEXTURE ASSETS

### Character Textures
- Character_Najika_Diffuse.png (1024x1024)
- Character_Najika_Normal.png (1024x1024)
- Character_Najika_Roughness.png (1024x1024)
- Character_Najika_Emission.png (1024x1024) - For glowing eyes

### Environment Textures (KayKit Style)
- Stone_Wall_Diffuse.png (512x512)
- Wood_Floor_Diffuse.png (512x512)
- Metal_Door_Diffuse.png (512x512)
- Glass_Window_Diffuse.png (512x512)
- Grass_Ground_Diffuse.png (512x512)
- **Total:** ~80 environment textures

### UI Textures
- Button_Normal.png (128x128)
- Button_Hover.png (128x128)
- Button_Pressed.png (128x128)
- HP_Bar_Fill.png (256x32)
- Stamina_Bar_Fill.png (256x32)
- Icon_Attack.png (64x64)
- Icon_Defend.png (64x64)
- Icon_Heal.png (64x64)
- **Total:** ~100 UI icons/textures

---

## 🔊 AUDIO ASSETS

### Music Tracks
```
Format: OGG Vorbis (looping)
Bitrate: 128 kbps
Duration: 2-5 minutes each
```

| Track | Use Case | Mood | Duration |
|-------|----------|------|----------|
| Menu_Theme.ogg | Main menu | Calm, mysterious | 2:30 |
| Living_Room.ogg | Living Room | Cozy, warm | 3:00 |
| Battle_Theme.ogg | Combat | Intense, fast | 2:45 |
| Battle_Boss.ogg | Boss fights | Epic, dramatic | 3:30 |
| Garden.ogg | Garden | Peaceful, nature | 3:15 |
| Training_Room.ogg | Training | Motivational, energetic | 2:50 |
| Arena.ogg | Arena | Competitive, pumped | 3:00 |
| Dungeon.ogg | Dungeon | Dark, ominous | 3:20 |
| Private_Mode.ogg | Private mode | Sensual, mysterious | 3:40 |
| Victory.ogg | Win screen | Triumphant, short | 0:30 |

**Total:** 10 music tracks (~30 MB)

### Sound Effects (SFX)
```
Format: WAV (44.1 kHz, 16-bit)
Duration: 0.1-3 seconds
```

**Combat SFX:**
- Sword_Swing_1.wav
- Sword_Swing_2.wav
- Sword_Hit_1.wav
- Shield_Block.wav
- Parry_Success.wav
- Dodge_Roll.wav
- Critical_Hit.wav
- Player_Hit.wav
- Player_Death.wav
- Enemy_Hit.wav
- Enemy_Death.wav

**Movement SFX:**
- Footstep_Stone_1.wav
- Footstep_Stone_2.wav
- Footstep_Wood_1.wav
- Footstep_Grass_1.wav
- Jump.wav
- Land.wav

**UI SFX:**
- Button_Click.wav
- Button_Hover.wav
- Menu_Open.wav
- Menu_Close.wav
- Item_Pickup.wav
- Item_Use.wav
- Level_Up.wav
- Achievement_Unlock.wav

**Najika Voice:**
- Najika_Hello.wav
- Najika_Attack.wav
- Najika_Hit.wav
- Najika_Victory.wav
- Najika_Laugh.wav
- Najika_Sad.wav
- Najika_Excited.wav
- Najika_Explosion.wav (Signature line!)

**Ambient SFX:**
- Fire_Crackle.wav (loop)
- Wind_Outdoor.wav (loop)
- Water_Stream.wav (loop)
- Birds_Chirping.wav (loop)

**Total:** ~60 SFX files (~25 MB)

---

## ✨ PARTICLE EFFECTS (UE5 Niagara)

### Combat Effects
- Sword_Trail (blue/purple glow)
- Impact_Sparks (metal on metal)
- Critical_Hit_Flash (yellow burst)
- Parry_Shockwave (circular wave)
- Dodge_Blur (motion blur trail)
- Blood_Spray (enemy hit)
- Heal_Particles (green sparkles)

### Magic Effects
- Fireball (red/orange sphere)
- Lightning_Bolt (blue/white arc)
- Ice_Shard (cyan projectile)
- Explosion (Megumin signature!)
- Buff_Aura (character glow)
- Debuff_Cloud (purple smoke)

### Environment Effects
- Torch_Fire (flickering flame)
- Dust_Particles (ambient)
- Rain_Drops (weather)
- Snow_Flakes (weather)
- Fog_Mist (atmospheric)

**Total:** ~20 particle systems

---

## 🎮 UI ICON ASSETS

### Action Icons (64x64)
- Attack_Icon.png
- Defend_Icon.png
- Heal_Icon.png
- Run_Icon.png
- Jump_Icon.png
- Dodge_Icon.png
- Parry_Icon.png
- Use_Item_Icon.png

### Stat Icons (32x32)
- HP_Icon.png
- Stamina_Icon.png
- Hunger_Icon.png
- Energy_Icon.png
- Strength_Icon.png
- Intelligence_Icon.png
- Dexterity_Icon.png
- Charisma_Icon.png

### Item Icons (64x64)
- Health_Potion_Icon.png
- Mana_Potion_Icon.png
- Sword_Icon.png
- Shield_Icon.png
- Armor_Icon.png
- Food_Icon.png
- Key_Icon.png
- Gold_Icon.png

### Camera Mode Icons (48x48)
- Camera_Orbit_Icon.png
- Camera_Third_Icon.png
- Camera_First_Icon.png

**Total:** ~100 UI icons

---

## 📁 ASSET ORGANIZATION (UE5 Content Browser)

```
Content/
├── Characters/
│   └── Najika/
│       ├── Meshes/
│       │   └── SK_Najika.uasset
│       ├── Textures/
│       │   ├── T_Najika_Diffuse.uasset
│       │   ├── T_Najika_Normal.uasset
│       │   └── T_Najika_Roughness.uasset
│       ├── Materials/
│       │   └── M_Najika.uasset
│       ├── Animations/
│       │   ├── A_Idle.uasset
│       │   ├── A_Walk.uasset
│       │   ├── A_Run.uasset
│       │   └── ... (all animations)
│       └── Blueprints/
│           ├── BP_Najika.uasset
│           └── ABP_Najika.uasset (Animation Blueprint)
├── Environments/
│   ├── Rooms/
│   │   ├── LivingRoom/
│   │   ├── Bedroom/
│   │   ├── Kitchen/
│   │   └── ... (all rooms)
│   ├── Dungeon/
│   │   ├── Walls/
│   │   ├── Floors/
│   │   └── Props/
│   └── Materials/
│       └── M_Environment.uasset
├── Audio/
│   ├── Music/
│   │   ├── Menu_Theme.uasset
│   │   ├── Battle_Theme.uasset
│   │   └── ... (all music)
│   ├── SFX/
│   │   ├── Combat/
│   │   ├── Movement/
│   │   ├── UI/
│   │   └── Voice/
│   └── SoundCues/
│       └── SC_Footsteps.uasset
├── UI/
│   ├── Textures/
│   │   ├── Icons/
│   │   └── Buttons/
│   ├── Materials/
│   │   └── M_UI_Glass.uasset
│   └── Widgets/
│       ├── WBP_HUD.uasset
│       ├── WBP_MainMenu.uasset
│       └── WBP_Inventory.uasset
├── VFX/
│   ├── Niagara/
│   │   ├── NS_Sword_Trail.uasset
│   │   ├── NS_Explosion.uasset
│   │   └── ... (all effects)
│   └── Materials/
│       └── M_Particle.uasset
└── Blueprints/
    ├── GameModes/
    │   └── BP_NajikaGameMode.uasset
    ├── Controllers/
    │   └── BP_NajikaPlayerController.uasset
    └── Components/
        ├── BP_CombatComponent.uasset
        └── BP_InventoryComponent.uasset
```

---

## 📊 ASSET REQUIREMENTS FOR UE5

### Format Compatibility

| Asset Type | Source Format | UE5 Import Format | Notes |
|------------|---------------|-------------------|-------|
| 3D Models | GLTF/GLB | FBX recommended | Re-export if needed |
| Textures | PNG/JPG | PNG/TGA | Power-of-2 sizes |
| Audio (Music) | OGG | WAV/OGG | UE5 supports both |
| Audio (SFX) | WAV | WAV | 44.1kHz, 16-bit |
| Animations | GLTF embedded | FBX with rig | Retarget to UE5 skeleton |

### Texture Specifications
- **Resolution:** Power-of-2 (256, 512, 1024, 2048)
- **Format:** PNG (source), BC7 (compressed in UE5)
- **Mipmaps:** Auto-generated by UE5
- **Compression:** High-quality for character, Medium for environment

### Audio Specifications
- **Music:**
  - Format: WAV or OGG Vorbis
  - Sample Rate: 44.1 kHz
  - Bitrate: 128-192 kbps (OGG)
  - Looping: Yes (set in UE5)
- **SFX:**
  - Format: WAV
  - Sample Rate: 44.1 kHz
  - Bit Depth: 16-bit
  - Mono for most SFX, Stereo for ambient

---

## 📦 ASSET SOURCES

### Current Assets
- **KayKit Packs:** AnimatedCharacter, Dungeon, Adventurers
- **Custom Najika Model:** Based on KayKit, customized in Blender

### Assets to Create/Source
- **Music:** Royalty-free (e.g., Purple Planet, Incompetech) or commission
- **Voice Lines:** TTS (Coqui with Megumin voice clone) or voice actor
- **UI Icons:** Create in Figma/Illustrator or purchase UI pack
- **Particle Effects:** Create in UE5 Niagara (native)

### Licensing
- **KayKit:** CC0 (Public Domain) - Free for commercial use
- **Music:** Ensure royalty-free or licensed
- **Voice:** Custom TTS or licensed voice actor

---

## ✅ ASSET CHECKLIST (Pre-Implementation)

**Phase 0 (Specification) - ✅ COMPLETE**
- [x] Document all required assets
- [x] Estimate file sizes
- [x] Plan content directory structure

**Phase 1 (Sourcing):**
- [ ] Download KayKit packs
- [ ] Customize Najika character model
- [ ] Source/create music tracks
- [ ] Record/generate voice lines
- [ ] Create UI icons

**Phase 2 (Import to UE5):**
- [ ] Import all 3D models (FBX)
- [ ] Import all textures (PNG → compressed)
- [ ] Import all animations (retarget to UE5 skeleton)
- [ ] Import all audio (WAV/OGG)
- [ ] Set up materials (PBR workflow)

**Phase 3 (Optimization):**
- [ ] LOD generation for all meshes
- [ ] Texture compression (BC7/BC5)
- [ ] Audio compression (OGG for long tracks)
- [ ] Particle system optimization
- [ ] Blueprint optimization (nativization)

---

## 📝 NOTES FOR LOCAL MODEL

**Assets Location (After UE5 Import):**
```
C:\NajikaDigivice_UE5\NajikaDigivice\Content\
```

**Import Order:**
1. Character models & textures → Materials → Animations
2. Environment models & textures → Materials
3. Audio files → Sound Cues
4. UI textures → Widget Blueprints
5. Particle systems (create in UE5 directly)

**Total Project Size (Estimated):**
- Source Assets: ~520 MB
- Imported to UE5: ~800 MB (with compression)
- Cooked for Android APK: ~350 MB (heavily compressed)

---

**Document Version:** 1.0
**Last Updated:** 2025-01-15
**Total Assets Documented:** 346+
**Lines:** 480+

---

✅ **ASSET SPECIFICATION COMPLETE!**
