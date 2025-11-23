# UE5 MATERIAL TEMPLATES - NAJIKA DIGIVICE
**Model 1 - Digivice APK**
**Created:** 2025-11-11

---

## 🎨 MATERIAL SYSTEM ÜBERSICHT

Diese Datei enthält alle Material-Templates für Najika Digivice!

**Material-Kategorien:**
```
✅ Character Materials (Najika Skin, Hair, Eyes, Clothes)
✅ UI Materials (Buttons, Bars, Effects)
✅ Environment Materials (World, Props)
✅ VFX Materials (Particles, Magic Effects)
✅ Post-Processing Materials (Screen Effects)
✅ Mobile Optimization Tips
```

---

## 👧 CATEGORY 1: CHARACTER MATERIALS

### **M_Najika_Skin (PBR Character Skin)**

**Location:** `Content/Materials/Characters/M_Najika_Skin.uasset`
**Purpose:** Realistic anime skin with subsurface scattering

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Opaque
Shading Model: Subsurface Profile

Texture Inputs:
- T_Najika_BaseColor (RGB: Skin color, A: AO)
- T_Najika_Normal (RGB Normal Map)
- T_Najika_ORM (R: Occlusion, G: Roughness, B: Metallic)
- T_Najika_Subsurface (RGB: Subsurface color)

Material Graph:
─────────────────────────────────────
[T_Najika_BaseColor] → Base Color
[T_Najika_Normal] → Normal
[T_Najika_ORM.R] → Ambient Occlusion
[T_Najika_ORM.G] → Roughness
[T_Najika_ORM.B] → Metallic (0.0 for skin!)

[T_Najika_Subsurface] → Subsurface Color
[Constant: 0.5] → Opacity (for SSS)

Subsurface Profile: SP_Skin (UE5 default)
─────────────────────────────────────
```

**Mobile Optimization:**
```
✅ Use 1024x1024 textures (max!)
✅ Compress: BC7 (Desktop), ASTC (Mobile)
✅ Combine maps (ORM = Occlusion+Roughness+Metallic)
✅ Disable expensive features:
   - No SSS on low-end devices (use simple diffuse)
   - Use Material Quality Switch
```

**Material Parameters (for variants):**
```
- SkinTintColor (Vector3) - Adjust skin tone
- RoughnessMultiplier (Scalar) - Adjust shine
- SubsurfaceIntensity (Scalar) - SSS strength
```

---

### **M_Najika_Hair (Anime Hair)**

**Location:** `Content/Materials/Characters/M_Najika_Hair.uasset`
**Purpose:** Stylized anime hair with highlights

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Opaque
Shading Model: Default Lit

Texture Inputs:
- T_Najika_Hair_BaseColor (RGB: Hair color, A: Opacity mask)
- T_Najika_Hair_Normal (Optional for detail)
- T_Najika_Hair_Mask (R: Highlight mask, G: AO, B: Specular)

Material Graph:
─────────────────────────────────────
[T_Najika_Hair_BaseColor.RGB] → Base Color

[T_Najika_Hair_Mask.R] × [HairHighlightColor] → Add to Base Color

[T_Najika_Hair_Normal] → Normal

[T_Najika_Hair_Mask.B] → Specular

[Constant: 0.6] → Roughness (shiny anime hair!)

[T_Najika_Hair_Mask.G] → Ambient Occlusion

Anisotropy (optional for strand look):
[Constant: 0.5] → Anisotropy
─────────────────────────────────────
```

**Anime Hair Shader Trick:**
```
Add rim lighting for anime style:

[FresnelNode]
    Exponent: 2.0
    Base Reflect Fraction: 0.1
→ Multiply by [RimColor (Bright)]
→ Add to Emissive Color

Result: Bright edges on hair! (Anime style!)
```

**Material Parameters:**
```
- HairBaseColor (Vector3)
- HairHighlightColor (Vector3)
- RimLightColor (Vector3)
- RimLightIntensity (Scalar)
```

---

### **M_Najika_Eyes (Anime Eyes with Glow)**

**Location:** `Content/Materials/Characters/M_Najika_Eyes.uasset`
**Purpose:** Emissive anime eyes

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Masked
Shading Model: Default Lit

Texture Inputs:
- T_Najika_Eyes_BaseColor (RGB: Eye color)
- T_Najika_Eyes_Emissive (RGB: Glow/Highlights)
- T_Najika_Eyes_OpacityMask (A: Mask)

Material Graph:
─────────────────────────────────────
[T_Najika_Eyes_BaseColor] → Base Color

[T_Najika_Eyes_Emissive] × [GlowIntensity: 2.0] → Emissive Color

[T_Najika_Eyes_OpacityMask.A] → Opacity Mask

[Constant: 0.3] → Roughness

[Constant: 0.0] → Metallic
─────────────────────────────────────
```

**Animated Eye Glow:**
```
Pulsing glow effect:

[Time] → Sin → Abs
→ Multiply by 0.5
→ Add 0.5
→ Multiply [T_Najika_Eyes_Emissive]
→ Emissive Color

Result: Eyes pulse softly!
```

**Material Parameters:**
```
- EyeColor (Vector3)
- GlowIntensity (Scalar)
- PulseSpeed (Scalar)
```

---

### **M_Najika_Clothes (Outfit Material)**

**Location:** `Content/Materials/Characters/M_Najika_Clothes.uasset`
**Purpose:** Cloth with patterns

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Opaque
Shading Model: Cloth

Texture Inputs:
- T_Najika_Clothes_BaseColor
- T_Najika_Clothes_Normal
- T_Najika_Clothes_ORM

Material Graph:
─────────────────────────────────────
[T_Najika_Clothes_BaseColor] → Base Color

[T_Najika_Clothes_Normal] → Normal

[T_Najika_Clothes_ORM.R] → AO
[T_Najika_Clothes_ORM.G] → Roughness
[T_Najika_Clothes_ORM.B] → Metallic

[Constant: FuzzColor] → Fuzz Color (cloth sheen)
[Constant: 0.3] → Cloth (amount)
─────────────────────────────────────
```

**Material Parameters:**
```
- ClothColor (Vector3) - Tint outfit
- FuzzColor (Vector3) - Fabric sheen color
- RoughnessMultiplier (Scalar)
```

---

## 🖼️ CATEGORY 2: UI MATERIALS

### **M_UI_Button (Interactive Button)**

**Location:** `Content/Materials/UI/M_UI_Button.uasset`
**Purpose:** Animated button material

**Material Setup:**

```
Material Domain: User Interface
Blend Mode: Translucent

Texture Inputs:
- T_Button_Base (RGBA: Button texture)
- T_Button_Glow (RGB: Glow effect)

Material Graph:
─────────────────────────────────────
[T_Button_Base] → Base Color

[T_Button_Base.A] → Opacity

Hover Effect:
[T_Button_Glow] × [HoverIntensity: 0.0-1.0] → Add to Emissive

Press Effect:
[ButtonPressed: 0.0-1.0] → Darken Base Color
─────────────────────────────────────
```

**Dynamic Parameters (Material Instance):**
```
Create Material Instance: MI_UI_Button

In Blueprint:
→ Get Dynamic Material Instance
→ Set Scalar Parameter "HoverIntensity" (On hover: 1.0, else: 0.0)
→ Set Scalar Parameter "ButtonPressed" (On press: 1.0, else: 0.0)
```

**Material Parameters:**
```
- ButtonColor (Vector3)
- HoverIntensity (Scalar) - 0.0 to 1.0
- ButtonPressed (Scalar) - 0.0 to 1.0
- GlowColor (Vector3)
```

---

### **M_UI_ProgressBar (Health/Hunger Bar)**

**Location:** `Content/Materials/UI/M_UI_ProgressBar.uasset`
**Purpose:** Animated progress bar with gradient

**Material Setup:**

```
Material Domain: User Interface
Blend Mode: Translucent

Material Graph:
─────────────────────────────────────
UV Coordinates:
[TextureCoordinate[0]] → UV

Fill Amount (0.0-1.0):
If (UV.X < FillAmount):
    → Display FillColor
Else:
    → Display EmptyColor

Gradient:
[Lerp]
    A: ColorLow (Red)
    B: ColorHigh (Green)
    Alpha: FillAmount
→ Base Color

Border:
If (UV.X < 0.05 OR UV.X > 0.95 OR UV.Y < 0.1 OR UV.Y > 0.9):
    → BorderColor
─────────────────────────────────────
```

**Blueprint Usage:**
```
In WBP_NajikaStatus:
→ Get ProgressBar Material
→ Set Scalar Parameter "FillAmount" (Hunger / 100.0)
→ Updates in real-time!
```

**Material Parameters:**
```
- FillAmount (Scalar) - 0.0 to 1.0
- ColorLow (Vector3) - Red (low value)
- ColorHigh (Vector3) - Green (high value)
- EmptyColor (Vector3)
- BorderColor (Vector3)
```

---

### **M_UI_ParticleEffect (UI Sparkles)**

**Location:** `Content/Materials/UI/M_UI_ParticleEffect.uasset`
**Purpose:** Sparkle effect for UI

**Material Setup:**

```
Material Domain: User Interface
Blend Mode: Additive (for glow!)

Texture Inputs:
- T_Sparkle (RGBA: Sparkle texture)

Material Graph:
─────────────────────────────────────
[T_Sparkle.RGB] × [SparkleColor] → Emissive Color

[T_Sparkle.A] × [Opacity] → Opacity

Rotation:
[Rotator]
    Coordinate: TextureCoordinate[0]
    Time: [Time] × [RotationSpeed]
→ Use for T_Sparkle UV

Scale Pulse:
[Sin(Time × PulseSpeed)] × 0.5 + 0.5
→ Multiply Emissive
─────────────────────────────────────
```

**Use in Niagara:**
```
Create Niagara System: NS_UI_Sparkles
→ Use M_UI_ParticleEffect
→ Spawn on button hover/click
```

---

## 🌍 CATEGORY 3: ENVIRONMENT MATERIALS

### **M_Ground_Grass (Grass Terrain)**

**Location:** `Content/Materials/Environment/M_Ground_Grass.uasset`
**Purpose:** Grass terrain with wind

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Opaque
Shading Model: Default Lit

Texture Inputs:
- T_Grass_BaseColor (RGB)
- T_Grass_Normal
- T_Grass_ORM

Material Graph:
─────────────────────────────────────
[T_Grass_BaseColor] → Base Color

[T_Grass_Normal] → Normal

[T_Grass_ORM.R] → AO
[T_Grass_ORM.G] → Roughness
[T_Grass_ORM.B] → Metallic (0 for grass!)

Wind Effect:
[WorldPositionOffset]
    [Sin(Time + WorldPosition.X)] × WindStrength
→ World Position Offset (grass waves!)
─────────────────────────────────────
```

**Material Parameters:**
```
- GrassTint (Vector3)
- WindStrength (Scalar)
- WindSpeed (Scalar)
```

---

### **M_Water (Stylized Water)**

**Location:** `Content/Materials/Environment/M_Water.uasset`
**Purpose:** Simple stylized water

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Translucent
Shading Model: Default Lit

Texture Inputs:
- T_Water_Normal (Animated normal map)

Material Graph:
─────────────────────────────────────
Base Color: [WaterColor: Blue]

Normal:
[T_Water_Normal]
    UV: [TextureCoordinate[0]] + [Time × FlowSpeed]
→ Normal

Opacity: 0.6

Refraction:
[SceneTexture:SceneColor] + [Refraction: 1.2]

Specular: 0.8 (shiny water!)
Roughness: 0.2
─────────────────────────────────────
```

**Material Parameters:**
```
- WaterColor (Vector3)
- FlowSpeed (Scalar)
- WaterOpacity (Scalar)
```

---

## ✨ CATEGORY 4: VFX MATERIALS

### **M_Particle_Fire (Fire Effect)**

**Location:** `Content/Materials/VFX/M_Particle_Fire.uasset`
**Purpose:** Fire particles for magic/attacks

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Additive
Shading Model: Unlit (for glow!)

Texture Inputs:
- T_Fire (RGBA: Fire texture)
- T_Fire_Distortion (Grayscale noise)

Material Graph:
─────────────────────────────────────
Distortion:
[T_Fire_Distortion]
    UV: [TextureCoordinate[0]] + [Time × DistortionSpeed]
→ DistortedUV

[T_Fire] sampled with DistortedUV
→ Multiply by [FireColor: Orange/Yellow]
→ Emissive Color

[T_Fire.A] × [Particle Alpha] → Opacity
─────────────────────────────────────
```

**Use in Niagara:**
```
NS_Fireball:
→ Sprite Renderer
→ Material: M_Particle_Fire
→ Color over lifetime: Yellow → Orange → Red
```

---

### **M_Particle_Magic (Magic Sparkles)**

**Location:** `Content/Materials/VFX/M_Particle_Magic.uasset`
**Purpose:** Magic effect particles

**Material Setup:**

```
Material Domain: Surface
Blend Mode: Additive
Shading Model: Unlit

Texture Inputs:
- T_Star (RGBA: Star shape)

Material Graph:
─────────────────────────────────────
[T_Star.RGB] × [ParticleColor (Dynamic!)] → Emissive Color

[T_Star.A] × [Particle Alpha] → Opacity

Rotation:
[RotateAboutAxis]
    Position: VertexPosition
    Axis: Z
    Angle: [Time] × [RotationSpeed]
→ World Position Offset

Scale Pulse:
[Sin(Time × 5.0)] × 0.2 + 1.0
→ Multiply Vertex Position (pulsing!)
─────────────────────────────────────
```

**Niagara Usage:**
```
NS_MagicSparkles:
→ Initialize Particle: Color (Random color from curve!)
→ Material receives ParticleColor
→ Rainbow sparkles! 🌈
```

---

## 🎬 CATEGORY 5: POST-PROCESSING MATERIALS

### **M_PP_OutlineEffect (Anime Outline)**

**Location:** `Content/Materials/PostProcess/M_PP_OutlineEffect.uasset`
**Purpose:** Anime-style character outlines

**Material Setup:**

```
Material Domain: Post Process
Blend Mode: Opaque
Shading Model: Unlit

Material Graph:
─────────────────────────────────────
Edge Detection:

[SceneTexture:SceneDepth] at UV
[SceneTexture:SceneDepth] at UV + Offset (sample neighbors)

Compare depths:
If (Depth difference > Threshold):
    → Draw outline (Black)
Else:
    → Original scene color

Final:
[Lerp]
    A: [SceneTexture:SceneColor]
    B: [OutlineColor: Black]
    Alpha: Edge mask
→ Emissive Color
─────────────────────────────────────
```

**Add to Post Process Volume:**
```
1. Create Post Process Volume in level
2. Set "Infinite Extent (Unbound)" = True
3. Post Process Materials → Add Array Element
4. Material: M_PP_OutlineEffect
5. Adjust OutlineThickness parameter
```

**Material Parameters:**
```
- OutlineColor (Vector3)
- OutlineThickness (Scalar)
- DepthThreshold (Scalar)
```

---

### **M_PP_ColorGrading (Anime Look)**

**Location:** `Content/Materials/PostProcess/M_PP_ColorGrading.uasset`
**Purpose:** Vibrant anime colors

**Material Setup:**

```
Material Domain: Post Process
Blend Mode: Opaque
Shading Model: Unlit

Material Graph:
─────────────────────────────────────
[SceneTexture:SceneColor]

Color Adjustments:
→ Multiply Saturation (1.3 for vibrant!)
→ Multiply Contrast (1.1 for pop!)
→ Add Brightness (0.1 for lighter look)

HSV Adjustment:
Convert RGB → HSV
→ Shift Hue (optional)
→ Boost Saturation
Convert HSV → RGB

→ Emissive Color
─────────────────────────────────────
```

---

## 📱 MOBILE OPTIMIZATION

### **Material Quality Switching:**

```
Use Material Quality Switch Node:

[MaterialQualitySwitch]
    Low: Simple diffuse only
    Medium: Normal maps, no SSS
    High: Full PBR with SSS
    Epic: All features
→ Base Color
```

### **Texture Compression:**

```
Desktop: BC7 (high quality)
Mobile: ASTC 6x6 (good quality, small size)

In Texture Settings:
→ Compression Settings: BC7 (Default)
→ Mobile Compression: ASTC
→ Maximum Texture Size: 1024
```

### **Reduce Material Complexity:**

```
Mobile-Friendly Materials:
✅ Max 30 shader instructions
✅ Avoid complex math (sin/cos/pow)
✅ No World Position Offset (expensive!)
✅ No Parallax Occlusion Mapping
✅ Limit texture samplers (max 4-5)
✅ Use Mobile HDR: False
```

### **LOD Materials:**

```
Create simplified materials for LOD1, LOD2:

LOD0 (Close): Full material
LOD1 (Medium): Remove SSS, simplify normals
LOD2 (Far): Single texture, no normal map

In Static/Skeletal Mesh:
→ LOD Settings → Material Slots
→ Override Material for LOD1, LOD2
```

---

## 🎨 MATERIAL INSTANCES

### **Why Use Material Instances?**

```
Material Instances (MI) let you create variants without duplicating materials!

Example:
M_Najika_Clothes (Master Material)
├── MI_Najika_Clothes_Blue (Instance - Blue outfit)
├── MI_Najika_Clothes_Red (Instance - Red outfit)
└── MI_Najika_Clothes_Green (Instance - Green outfit)

Benefits:
✅ Reuse same shader
✅ Only change parameters (colors, textures)
✅ Better performance (shader compiled once!)
```

### **How to Create:**

```
1. Right-click on M_Najika_Clothes
2. Create Material Instance
3. Name: MI_Najika_Clothes_Blue
4. Open instance
5. Check boxes to override parameters
6. Change ClothColor to Blue
7. Apply to character!
```

---

## 🛠️ MATERIAL CREATION CHECKLIST

```
For each new material:

☐ Choose correct Material Domain
☐ Choose correct Blend Mode
☐ Choose correct Shading Model
☐ Add texture inputs
☐ Connect nodes properly
☐ Add Material Parameters (for tweaking!)
☐ Test on target device (Xiaomi 11T Pro)
☐ Optimize for mobile (reduce complexity)
☐ Create Material Instances for variants
☐ Document parameters
☐ Save and compile
```

---

## 📊 MATERIAL SUMMARY

```
✅ Character Materials: 4 (Skin, Hair, Eyes, Clothes)
✅ UI Materials: 3 (Button, ProgressBar, Particles)
✅ Environment Materials: 2 (Grass, Water)
✅ VFX Materials: 2 (Fire, Magic)
✅ Post-Process Materials: 2 (Outline, ColorGrading)

TOTAL: 13 Material Templates!

All optimized for mobile performance! 📱
```

---

## 🎉 MATERIAL TEMPLATES COMPLETE!

**Usage:**
1. Create materials in UE5 Content Browser
2. Follow node graphs from this document
3. Create Material Instances for variants
4. Apply to meshes and UI
5. Test performance on device
6. Iterate and optimize!

**Next:** Create Animation Blueprint templates!

---

**Model 1 - Digivice APK Development**
**Status:** Material Templates Ready ✅
**Templates:** 13 Material Setups Created

**MATERIALS READY FOR NAJIKA! 🎨🚀**
