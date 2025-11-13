# UE5 Material Specifications for Najika Digivice

**Project:** Najika Digivice UE5 Migration
**Target Platform:** Windows (Development) → Android (Xiaomi 11T Pro)
**Art Style:** Stylized 3D (Anime/Cel-Shaded)
**Date:** 2025-11-13

---

## Table of Contents

1. [Master Materials](#master-materials)
2. [Character Materials](#character-materials)
3. [Environment Materials](#environment-materials)
4. [UI Materials](#ui-materials)
5. [VFX Materials](#vfx-materials)
6. [Post-Process Materials](#post-process-materials)
7. [Mobile Optimization](#mobile-optimization)

---

## Master Materials

### M_MasterCelShaded

**Purpose:** Base material for all cel-shaded characters and objects.

**Features:**
- Cel-shaded lighting (3-5 lighting steps)
- Outline rendering (inverted hull method)
- Rim lighting
- Fresnel effect
- Normal map support
- Emissive mask

**Parameters:**
- **Base Color** (Texture2D)
- **Normal Map** (Texture2D)
- **Outline Thickness** (Float, 0.01-0.1, Default: 0.02)
- **Outline Color** (LinearColor, Default: Black)
- **Lighting Steps** (Integer, 3-5, Default: 4)
- **Rim Light Color** (LinearColor, Default: White)
- **Rim Light Power** (Float, 1.0-5.0, Default: 2.0)
- **Emissive Texture** (Texture2D, Optional)
- **Emissive Strength** (Float, 0.0-10.0, Default: 1.0)

**Shader Graph Overview:**
```
BaseColor → Quantize (Lighting Steps) → Cel-Shaded Result
Normals → WorldNormal → Rim Light Calculation
Outline: Extrude vertices along normals (inverted hull)
```

**Material Instances:**
- MI_Najika_Body
- MI_Najika_Hair
- MI_Najika_Outfit
- MI_Najika_Eyes

---

### M_MasterPBR

**Purpose:** Standard PBR material for environment assets.

**Features:**
- Roughness/Metallic workflow
- Normal maps
- Ambient occlusion
- Height/displacement (optional)
- Tiling control

**Parameters:**
- **Base Color** (Texture2D)
- **Normal Map** (Texture2D)
- **Roughness Map** (Texture2D or Float)
- **Metallic Map** (Texture2D or Float)
- **AO Map** (Texture2D)
- **Tiling** (Vector2D, Default: (1, 1))
- **Brightness** (Float, Default: 1.0)

**Material Instances:**
- MI_Wood_Floor
- MI_Stone_Wall
- MI_Metal_Door
- MI_Glass_Window

---

### M_MasterUI

**Purpose:** Base material for UI elements.

**Features:**
- Unlit shading
- Alpha masking
- Color tinting
- Glow/emissive support

**Parameters:**
- **UI Texture** (Texture2D)
- **Tint Color** (LinearColor, Default: White)
- **Opacity** (Float, 0.0-1.0, Default: 1.0)
- **Glow Enabled** (Boolean, Default: False)
- **Glow Color** (LinearColor)
- **Glow Strength** (Float, 0.0-5.0, Default: 1.0)

---

## Character Materials

### MI_Najika_Body

**Parent:** M_MasterCelShaded

**Parameters:**
- **Base Color:** T_Najika_Body_D (512x512)
- **Normal Map:** T_Najika_Body_N
- **Outline Thickness:** 0.025
- **Outline Color:** RGB(50, 30, 50) (Dark purple)
- **Lighting Steps:** 4
- **Rim Light Color:** RGB(255, 200, 255) (Light pink)
- **Rim Light Power:** 2.5

**Notes:**
- Skin tone: Light peachy tone
- Subsurface scattering (optional, disable on mobile)

---

### MI_Najika_Hair

**Parent:** M_MasterCelShaded

**Parameters:**
- **Base Color:** T_Najika_Hair_D (512x512)
- **Normal Map:** T_Najika_Hair_N
- **Outline Thickness:** 0.03 (Thicker for emphasis)
- **Outline Color:** RGB(80, 30, 80) (Purple-black)
- **Lighting Steps:** 3 (Simplified for hair)
- **Rim Light Color:** RGB(200, 100, 255) (Purple highlight)
- **Rim Light Power:** 3.0 (Strong rim for anime style)

**Notes:**
- Hair color: Purple/pink gradient
- Anisotropic highlights (optional, disable on mobile)

---

### MI_Najika_Outfit

**Parent:** M_MasterCelShaded

**Parameters:**
- **Base Color:** T_Najika_Outfit_D (512x512)
- **Normal Map:** T_Najika_Outfit_N
- **Outline Thickness:** 0.02
- **Outline Color:** RGB(0, 0, 0) (Black)
- **Lighting Steps:** 4
- **Emissive Texture:** T_Najika_Outfit_E (Red accents)
- **Emissive Strength:** 2.0

**Notes:**
- Megumin-inspired outfit (red/black color scheme)
- Emissive for magical accents

---

### MI_Najika_Eyes

**Parent:** M_MasterCelShaded

**Parameters:**
- **Base Color:** T_Najika_Eyes_D (256x256)
- **Outline Thickness:** 0.01 (Thin)
- **Outline Color:** RGB(0, 0, 0)
- **Lighting Steps:** 2 (Simple for eyes)
- **Emissive Texture:** T_Najika_Eyes_E (Bright red iris)
- **Emissive Strength:** 3.0 (Glowing eyes)

**Notes:**
- Large anime-style eyes
- Bright red iris color
- Highlight/sparkle texture in emissive

---

## Environment Materials

### MI_Wood_Floor

**Parent:** M_MasterPBR

**Parameters:**
- **Base Color:** T_Wood_Floor_D (1024x1024, from Poly Haven)
- **Normal Map:** T_Wood_Floor_N
- **Roughness Map:** T_Wood_Floor_R
- **Metallic:** 0.0
- **AO Map:** T_Wood_Floor_AO
- **Tiling:** (2, 2)

**Usage:** Wohnzimmer, Schlafzimmer floor

---

### MI_Stone_Wall

**Parent:** M_MasterPBR

**Parameters:**
- **Base Color:** T_Stone_Wall_D (1024x1024)
- **Normal Map:** T_Stone_Wall_N
- **Roughness Map:** T_Stone_Wall_R
- **Metallic:** 0.0
- **AO Map:** T_Stone_Wall_AO
- **Tiling:** (1.5, 1.5)

**Usage:** Kampfarena, Schwarze Mühle - Keller walls

---

### MI_Grass

**Parent:** M_MasterPBR

**Parameters:**
- **Base Color:** T_Grass_D (512x512)
- **Normal Map:** T_Grass_N
- **Roughness:** 0.8
- **Metallic:** 0.0
- **Tiling:** (4, 4)

**Usage:** Garten ground

**Notes:**
- May use vertex color for variation
- Consider using Foliage tool for grass meshes

---

### MI_Metal_Door

**Parent:** M_MasterPBR

**Parameters:**
- **Base Color:** T_Metal_Door_D (1024x1024)
- **Normal Map:** T_Metal_Door_N
- **Roughness Map:** T_Metal_Door_R
- **Metallic:** 0.9
- **AO Map:** T_Metal_Door_AO
- **Tiling:** (1, 1)

**Usage:** Terminal, Schwarze Mühle doors

---

## UI Materials

### MI_UI_Button

**Parent:** M_MasterUI

**Parameters:**
- **UI Texture:** T_UI_Button_D
- **Tint Color:** RGB(200, 200, 255) (Light blue)
- **Opacity:** 0.9
- **Glow Enabled:** True
- **Glow Color:** RGB(100, 150, 255)
- **Glow Strength:** 1.5

**Usage:** HUD buttons, menu buttons

---

### MI_UI_ProgressBar

**Parent:** M_MasterUI

**Parameters:**
- **UI Texture:** T_UI_ProgressBar_D
- **Tint Color:** RGB(100, 255, 100) (Green for health/hunger)
- **Opacity:** 1.0
- **Glow Enabled:** False

**Usage:** Status bars (Hunger, Thirst, Energy, etc.)

**Variants:**
- MI_UI_ProgressBar_Red (HP)
- MI_UI_ProgressBar_Blue (Stamina)
- MI_UI_ProgressBar_Yellow (XP)

---

## VFX Materials

### M_VFX_Particle

**Purpose:** Base material for particle effects.

**Features:**
- Unlit
- Additive blending
- Soft particles (depth fade)
- UV distortion (optional)
- Color over lifetime

**Parameters:**
- **Particle Texture** (Texture2D)
- **Color** (LinearColor, Default: White)
- **Opacity** (Float, 0.0-1.0, Default: 0.5)
- **Depth Fade Distance** (Float, Default: 100.0)
- **Emissive Strength** (Float, 0.0-10.0, Default: 2.0)

**Material Instances:**
- MI_VFX_Sparkle (for UI effects, level up, etc.)
- MI_VFX_Smoke
- MI_VFX_Fire
- MI_VFX_Magic (purple/pink for Najika's magic)

---

### MI_VFX_Magic

**Parent:** M_VFX_Particle

**Parameters:**
- **Particle Texture:** T_VFX_Magic_D (Swirly energy texture)
- **Color:** RGB(255, 100, 200) (Pink)
- **Opacity:** 0.6
- **Emissive Strength:** 5.0

**Usage:** Najika's magic attacks, training effects

---

## Post-Process Materials

### M_PostProcess_Outline

**Purpose:** Screen-space outline for all characters/objects.

**Features:**
- Sobel edge detection
- Custom depth/stencil buffer
- Adjustable thickness and color

**Parameters:**
- **Outline Thickness** (Float, 1.0-5.0, Default: 2.0)
- **Outline Color** (LinearColor, Default: Black)
- **Outline Intensity** (Float, 0.0-1.0, Default: 0.8)

**Implementation:**
- Add to Post Process Volume in each room
- Characters should write to Custom Depth buffer

---

### M_PostProcess_ColorGrading

**Purpose:** Stylized color grading for anime aesthetic.

**Features:**
- Saturation boost
- Slight bloom
- Vignette
- Film grain (optional, disable on mobile)

**Parameters:**
- **Saturation** (Float, 1.0-1.5, Default: 1.2)
- **Bloom Intensity** (Float, 0.0-2.0, Default: 0.5)
- **Vignette Intensity** (Float, 0.0-1.0, Default: 0.3)
- **Film Grain** (Float, 0.0-1.0, Default: 0.1)

**Usage:** Global post-process volume

---

## Mobile Optimization

### Performance Guidelines

**Target:** Xiaomi 11T Pro (Snapdragon 888, Adreno 660)

**Texture Sizes:**
- Character textures: 512x512 (downscale from 1024x1024 on PC)
- Environment textures: 512x512 to 1024x1024 max
- UI textures: 256x256 to 512x512
- VFX textures: 256x256

**Material Complexity:**
- Max shader instructions: ~300-400 per material (mobile)
- Avoid complex math (sin, cos, pow) in pixel shader
- Use texture lookups instead of procedural noise
- Disable features on mobile:
  - Subsurface scattering
  - Anisotropic highlights
  - Film grain
  - Complex post-process effects

**Mobile Material Settings:**
- Enable "Fully Rough" on simple materials
- Use "Masked" blend mode sparingly (expensive on mobile)
- Prefer "Opaque" or "Translucent" blend modes
- Enable "Mobile Separate Translucency" for UI

**Conditional Features (PC only):**
```cpp
#if PLATFORM_ANDROID || PLATFORM_IOS
    // Disable expensive features
    SubsurfaceScattering = false;
    AnisotropicHighlights = false;
    FilmGrain = false;
#else
    // Enable on PC
    SubsurfaceScattering = true;
    AnisotropicHighlights = true;
    FilmGrain = true;
#endif
```

---

## Implementation Checklist

### Phase 1: Master Materials
- [ ] Create M_MasterCelShaded
- [ ] Create M_MasterPBR
- [ ] Create M_MasterUI
- [ ] Create M_VFX_Particle
- [ ] Test on simple cube

### Phase 2: Character Materials
- [ ] Create MI_Najika_Body
- [ ] Create MI_Najika_Hair
- [ ] Create MI_Najika_Outfit
- [ ] Create MI_Najika_Eyes
- [ ] Apply to character mesh
- [ ] Test lighting in all rooms

### Phase 3: Environment Materials
- [ ] Create MI_Wood_Floor
- [ ] Create MI_Stone_Wall
- [ ] Create MI_Grass
- [ ] Create MI_Metal_Door
- [ ] Apply to room meshes

### Phase 4: UI Materials
- [ ] Create MI_UI_Button
- [ ] Create MI_UI_ProgressBar (all variants)
- [ ] Apply to UI widgets

### Phase 5: VFX Materials
- [ ] Create MI_VFX_Magic
- [ ] Create MI_VFX_Sparkle
- [ ] Test in particle systems

### Phase 6: Post-Process
- [ ] Create M_PostProcess_Outline
- [ ] Create M_PostProcess_ColorGrading
- [ ] Add to Post Process Volume
- [ ] Test in all rooms

### Phase 7: Mobile Optimization
- [ ] Create mobile material variants
- [ ] Test on Android build
- [ ] Profile with UE5 Profiler
- [ ] Optimize texture sizes

---

## Asset Sources

**Textures:**
- [Poly Haven](https://polyhaven.com/) - PBR textures (CC0)
- [Textures.com](https://www.textures.com/) - Additional textures
- Custom character textures (hand-painted in Substance Painter)

**Tools:**
- Substance Painter (character texture painting)
- Substance Designer (procedural textures)
- Photoshop (texture editing)

---

## Notes

- All materials use forward slash paths in C++: `TEXT("Material'/Game/Materials/M_MasterCelShaded.M_MasterCelShaded'")`
- Material instances are preferred for runtime performance
- Use Material Parameter Collections for global material parameters (time of day, weather, etc.)
- Consider creating a Blueprint Function Library for material parameter manipulation

---

**END OF MATERIAL_SPECS.md**
