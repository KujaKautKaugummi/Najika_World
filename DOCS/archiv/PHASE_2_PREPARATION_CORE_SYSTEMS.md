# PHASE 2 VORBEREITUNG: CORE SYSTEMS
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**Phase:** 2 - Core Systems (Woche 2-3)

---

## 🎯 PHASE 2 ÜBERSICHT

### **Was wird gebaut:**
```
✅ Najika Character (Skeletal Mesh + Animations)
✅ Animation System (State Machine, Blend Spaces)
✅ World Setup (Die Schwarze Mühle, 2400x2400 Map)
✅ Camera System (Orbit, Third-Person, First-Person)
✅ Input System (Touch Controls + Keyboard/Mouse für Testing)
```

### **Geschätzte Dauer:** 2 Wochen
### **Priorität:** P0 (KRITISCH)

---

## 📋 TODO 2.1: NAJIKA CHARACTER

### **Asset-Quellen:**
```
Existierende Assets:
C:\Najika_World\assets\models\      ← Najika VRM Models (falls vorhanden)
C:\Najika_World\digivice\static\models\  ← GLTF Models

KayKit Assets:
~25GB lokal verfügbar (GLTF Format)
```

### **Import-Workflow:**

#### **Option A: VRM Model Import** (Falls Najika VRM existiert)
```
1. Download VRM4U Plugin für UE5:
   https://github.com/ruyo/VRM4U

2. Im UE5 Editor:
   - Edit → Plugins → Search "VRM4U"
   - Enable Plugin
   - Restart Editor

3. Import VRM:
   - Content Browser → Import
   - Select: najika_character.vrm
   - Import Settings:
     ✅ Import Mesh
     ✅ Import Skeleton
     ✅ Import Materials
     ✅ Import Animations (if any)
   - Import Location: Content/Characters/Najika/

4. Result:
   - SK_Najika (Skeletal Mesh)
   - SKEL_Najika (Skeleton)
   - M_Najika_* (Materials)
```

#### **Option B: Custom Character Creation** (Falls kein VRM)
```
1. Use MetaHuman Creator:
   https://www.unrealengine.com/metahuman

2. Customize to match Najika:
   - Hair: Crimson/Red (Megumin-style)
   - Eyes: Red/Crimson
   - Face: Anime-inspired
   - Body: Slender, young adult

3. Export MetaHuman → Import to Project

4. Or: Use Mixamo/Adobe Fuse for anime character
```

#### **Option C: Use Placeholder** (Quick Start)
```
1. Use UE5 Mannequin temporarily:
   Content/Characters/Mannequins/

2. Create Blueprint: BP_NajikaCharacter
   Parent: Character (C++ Class)
   Mesh: Mannequin (temporary)

3. Replace later with actual Najika model
```

### **Character Setup:**
```
Location: Content/Characters/Najika/

Files to create:
- SK_Najika              ← Skeletal Mesh
- SKEL_Najika            ← Skeleton
- PHYS_Najika            ← Physics Asset
- ABP_Najika             ← Animation Blueprint
- M_Najika_Body          ← Body Material
- M_Najika_Hair          ← Hair Material
- M_Najika_Eyes          ← Eyes Material
- BP_NajikaCharacter     ← Character Blueprint (Game)
```

---

## 🎭 TODO 2.2: ANIMATION SYSTEM

### **Animation State Machine:**

```
STATE MACHINE: ABP_Najika

States:
┌─────────────┐
│    IDLE     │ ← Default State
└─────────────┘
      │
      ├──► WALK (Speed > 0.1)
      │      │
      │      └──► RUN (Speed > 300)
      │
      ├──► JUMP (IsInAir == true)
      │
      ├──► TALK (VoiceCall Active)
      │      ├──► Talk_Happy
      │      ├──► Talk_Sad
      │      └──► Talk_Excited
      │
      └──► EMOTES
             ├──► Emote_Happy
             ├──► Emote_Sad
             ├──► Emote_Angry
             ├──► Emote_Explosion! (Megumin!)
             └──► Emote_Love
```

### **Blend Spaces:**

#### BS_Najika_Locomotion (Bewegung)
```
Horizontal Axis: Direction (-180 to 180)
Vertical Axis:   Speed (0 to 600)

Grid:
         600  ┌────────┬────────┬────────┐
              │ Run    │ Run    │ Run    │
              │ Back   │Forward │ Back   │
         300  ├────────┼────────┼────────┤
              │ Walk   │ Walk   │ Walk   │
              │ Back   │Forward │ Back   │
           0  └────────┴────────┴────────┘
             -180      0       180
```

#### BS_Najika_Emotions (Emotionen)
```
Horizontal Axis: Valence (Happy ← → Sad)
Vertical Axis:   Arousal (Calm ← → Excited)

Grid:
   Excited  ┌────────┬────────┬────────┐
            │ Angry  │Excited │ Scared │
       Mid  ├────────┼────────┼────────┤
            │ Sad    │ Neutral│ Happy  │
      Calm  └────────┴────────┴────────┘
            Negative Neutral Positive
```

### **Animation Sequences benötigt:**

**Locomotion:**
- Idle
- Walk Forward/Back/Left/Right
- Run Forward/Back/Left/Right
- Jump Start/Loop/Land
- Crouch Idle/Walk

**Talk (für Voice Calls!):**
- Talk_Idle (kleine Kopfbewegungen)
- Talk_Gestures (Handbewegungen)
- Jaw_Open (Mund öffnen - für Lip Sync!)

**Emotes:**
- Happy (arms up, smile)
- Sad (head down, slouch)
- Angry (fist clench, eyebrows)
- Explosion! (Megumin signature pose!)
- Love (hands on heart)

**Combat (später):**
- Attack_Melee
- Attack_Cast (magic)
- Hit_React
- Death

### **Lip Sync System:**

#### **Option A: Audio2Face (NVIDIA)** - BEST!
```
URL: https://www.nvidia.com/en-us/omniverse/apps/audio2face/

- Converts audio → facial animation
- Works with Coqui TTS output
- Real-time or pre-rendered
```

#### **Option B: OVRLipSync (Meta)** - GOOD
```
URL: https://developer.oculus.com/downloads/package/oculus-lipsync-unreal/

- Plugin für UE5
- Analyzes audio → phonemes → morph targets
- Works with any audio source
```

#### **Option C: Manual Morph Targets** - BASIC
```
Create Morph Targets:
- Jaw_Open (A, E, O sounds)
- Lips_Pucker (U, W sounds)
- Lips_Spread (I, S sounds)
- Tongue_Up (L, T, D sounds)

Then: Animate based on audio amplitude (simple but effective!)
```

---

## 🌍 TODO 2.3: WORLD SETUP

### **Level Structure:**

```
Content/Maps/

Main Levels:
- L_MainWorld           ← 2400x2400 Open World
- L_SchwarzenMuehle     ← Die Schwarze Mühle (7 Rooms)
- L_Test                ← Testing Level (klein)

Sublevel Strategy (Level Streaming):
- L_MainWorld_Persistent    ← Always loaded (sky, lighting)
- L_MainWorld_Forest        ← Forest region
- L_MainWorld_River         ← River region
- L_MainWorld_Village       ← Village region
- L_SchwarzenMuehle_Entrance
- L_SchwarzenMuehle_Room1
- L_SchwarzenMuehle_Room2
- ... (bis Room7)
```

### **World Composition:**

#### L_MainWorld (2400x2400 = 576,000 m²)
```
Layout:
                    N
                    ↑
    ┌───────────────────────────┐
    │   Forest      │ Village   │
    │               │           │
W ← ├───────────────┼───────────┤ → E
    │   River       │Schwarze   │
    │               │ Mühle     │
    └───────────────────────────┘
                    ↓
                    S

Regions:
1. Forest:         600x600m (NW)
2. Village:        600x600m (NE)
3. River:          600x600m (SW)
4. Schwarze Mühle: 600x600m (SE)
```

### **Lighting Setup:**

```
1. Directional Light (Sun):
   - Intensity: 3.0 lux
   - Color: Warm white (temp 5500K)
   - Dynamic Shadows: Yes
   - Mobility: Movable (for day/night cycle later)

2. Sky Light:
   - Intensity: 1.0
   - Color: Sky blue
   - Cubemap: Sky_HDR (or Captured)
   - Mobility: Stationary

3. Post Process Volume:
   - Infinite Extent: Yes
   - Auto Exposure: On
   - Bloom: Subtle (Intensity 0.5)
   - Ambient Occlusion: On (Radius 200)
   - Color Grading: Warm tone (+5 temp)

4. Lumen (Mobile):
   - Enable: Project Settings → Rendering → Lumen → Mobile
   - Global Illumination: Lumen
   - Reflections: Lumen
   - Screen Space: On (fallback)
```

### **Landscape (Optional):**

```
If using Landscape:
- Size: 2017x2017 (fits 2400x2400 well)
- Material Layers: 4 (Grass, Dirt, Rock, Sand)
- LOD: 3 levels
- Collision: Simple

If using Modular Pieces:
- KayKit Terrain Tiles
- 10m x 10m grid snapping
- Reusable pieces (performance!)
```

### **Asset Import from digivice/:**

```
Existing 3D Models (Three.js → UE5):
1. Find models in: C:\Najika_World\digivice\static\models\
2. Format: GLTF/GLB (Three.js format)
3. Convert: Import directly to UE5 (supports GLTF)
4. Process:
   - Content Browser → Import → Select .gltf/.glb
   - Import Settings:
     ✅ Import Mesh
     ✅ Import Materials
     ✅ Import Textures
     ✅ Auto Generate Collision
   - Import Location: Content/Environment/

5. Result: Static Meshes ready to use!
```

---

## 📷 TODO 2.4: CAMERA SYSTEM

### **Camera Manager Blueprint:**

```
Location: Content/Blueprints/Camera/
File: BP_NajikaCameraManager

Parent Class: PlayerCameraManager (C++)

Camera Modes:
1. ORBIT      ← Free rotation around Najika
2. THIRD      ← Third-Person (Fortnite-style)
3. FIRST      ← First-Person (Ego view)
```

### **Camera Mode: ORBIT**

```
Properties:
- Distance:        5-50 units (variable)
- Pitch:           -80° to +80°
- Yaw:             0-360° (free rotation)
- Target Offset:   (0, 0, 100) - Look at chest, not feet!

Controls:
- Touch Drag:      Rotate camera
- Pinch:           Zoom in/out
- Double Tap:      Reset to default

Implementation:
┌─────────────────┐
│   Target (Najika)│
│        ●         │
└─────────────────┘
          ↑
          │ (Distance = 14)
          │
      ┌───┴───┐
      │Camera │
      └───────┘

Camera Position = Target + (
    sin(Yaw) * cos(Pitch) * Distance,
    sin(Pitch) * Distance,
    cos(Yaw) * cos(Pitch) * Distance
)
```

### **Camera Mode: THIRD-PERSON**

```
Properties:
- Distance:        8 units (fixed)
- Height Offset:   2.5 (shoulder height)
- Shoulder Offset: 1.5 (right shoulder)
- Pitch:           -60° to +60°
- Yaw:             Independent from character!

Fortnite-Style:
┌─────────────────┐
│   Najika        │
│      ●          │
│     ↗           │ ← Character faces WASD direction
└─────────────────┘
       ↑
       │ Camera looks independent!
   ┌───┴───┐
   │Camera │
   └───────┘

Key: Character rotates to movement, Camera rotates with mouse!
```

### **Camera Mode: FIRST-PERSON**

```
Properties:
- Eye Height:      Character Height * 0.40
- FOV:             90° (adjustable)
- Head Bob:        Subtle (amplitude 2)

Implementation:
Camera Position = Character Position + (0, 0, EyeHeight)
Camera Rotation = Character Rotation + Mouse Look
```

### **Camera Collision:**

```
Prevent clipping through walls:

Blueprint Logic:
1. Line Trace from Target to Desired Camera Position
2. If Hit:
   - Move Camera to Hit Location - 10 units
   - Smooth transition (interpolate)
3. If No Hit:
   - Camera at desired position

Smoothing:
CurrentPos = Lerp(CurrentPos, DesiredPos, DeltaTime * 10.0)
```

---

## 🎮 TODO 2.5: INPUT SYSTEM

### **Enhanced Input System (UE5):**

```
Location: Content/Input/

Files to create:
- IMC_Default                   ← Input Mapping Context
- IA_Move                       ← Input Action (Vector2D)
- IA_Look                       ← Input Action (Vector2D)
- IA_Jump                       ← Input Action (Boolean)
- IA_Interact                   ← Input Action (Boolean)
- IA_Menu                       ← Input Action (Boolean)
- IA_VoiceCall                  ← Input Action (Boolean)
- IA_Chat                       ← Input Action (Boolean)
```

### **Input Mappings:**

#### Desktop/Testing (Keyboard + Mouse):
```
IA_Move:
- W/A/S/D      → Vector2D (Forward/Back, Left/Right)
- Gamepad LS   → Vector2D

IA_Look:
- Mouse X/Y    → Vector2D (Yaw/Pitch)
- Gamepad RS   → Vector2D

IA_Jump:
- Space        → Pressed
- Gamepad A    → Pressed

IA_Interact:
- E            → Pressed
- Gamepad X    → Pressed

IA_VoiceCall:
- V            → Pressed
- Hold for Push-to-Talk

IA_Chat:
- T            → Pressed

IA_Menu:
- Esc          → Pressed
- Gamepad Start→ Pressed
```

#### Mobile (Touch):
```
IA_Move:
- Virtual Joystick (Left side)
  Position: (100, 100) from bottom-left
  Size: 150x150
  Dead Zone: 0.2

IA_Look:
- Touch Drag (Right side)
  Area: Right 60% of screen
  Sensitivity: 1.0

IA_Jump:
- Touch Button (Bottom-right)
  Position: (Screen.Width - 100, Screen.Height - 100)
  Size: 80x80
  Icon: Jump

IA_Interact:
- Touch Button (Right-center)
  Position: (Screen.Width - 100, Screen.Height / 2)
  Size: 80x80
  Icon: E

IA_VoiceCall:
- Touch Button (Top-right)
  Position: (Screen.Width - 100, 100)
  Size: 80x80
  Icon: Microphone

IA_Chat:
- Touch Button (Top-left)
  Position: (100, 100)
  Size: 80x80
  Icon: Chat Bubble
```

### **Virtual Joystick Setup:**

```
1. Create Widget: WBP_VirtualJoystick
   Parent: UserWidget

2. Components:
   - Background Circle (Image)
   - Thumb Circle (Image)
   - Touch Area (Canvas Panel)

3. Logic:
   - OnTouchDown: Store initial position
   - OnTouchMove: Calculate offset from center
   - OnTouchUp: Reset thumb to center
   - Output: Vector2D (-1 to 1, -1 to 1)

4. Add to Viewport:
   PlayerController → BeginPlay → Add to Viewport
```

### **Touch Gestures:**

```
Gestures to implement:
- Single Touch Drag:    Camera rotation (Third/Orbit mode)
- Two-Finger Pinch:     Zoom (Orbit mode only)
- Double Tap:           Reset camera / Interact
- Swipe Up:             Jump
- Swipe Down:           Crouch
- Long Press:           Context menu
```

---

## 📦 ASSET CHECKLIST

### **To Import:**
```
From C:\Najika_World\assets\:
- [ ] Najika Character Model (VRM/FBX)
- [ ] Textures (Body, Hair, Eyes)
- [ ] Audio Files (Voice lines, SFX)

From C:\Najika_World\digivice\static\:
- [ ] World Models (GLTF → Static Mesh)
- [ ] UI Images (PNG → Texture2D)
- [ ] Icons (for buttons, inventory)

From KayKit (~25GB):
- [ ] Environment pieces (trees, rocks, grass)
- [ ] Building pieces (Schwarze Mühle)
- [ ] Props (furniture, decor)
```

### **To Download:**
```
Animations:
- [ ] Mixamo Animations (Free!)
      URL: https://www.mixamo.com
      - Idle, Walk, Run, Jump
      - Talk animations
      - Emotes

Plugins:
- [ ] VRM4U (if using VRM)
- [ ] OVRLipSync (for voice calls)
- [ ] CommonUI (for mobile UI)
```

---

## ✅ PHASE 2 ABSCHLUSS-CHECKLISTE

### **Character:**
- [ ] Najika Character imported (or placeholder)
- [ ] Materials setup (Body, Hair, Eyes)
- [ ] Physics Asset created
- [ ] Animation Blueprint created (ABP_Najika)
- [ ] State Machine implemented (Idle, Walk, Run, Jump, Talk)
- [ ] Blend Spaces created (Locomotion, Emotions)

### **World:**
- [ ] L_MainWorld created (2400x2400)
- [ ] Lighting setup (Directional, Sky, Post-Process)
- [ ] Environment assets imported
- [ ] Die Schwarze Mühle basic layout
- [ ] Level Streaming configured

### **Camera:**
- [ ] BP_NajikaCameraManager created
- [ ] Orbit Mode implemented
- [ ] Third-Person Mode implemented
- [ ] First-Person Mode implemented
- [ ] Camera collision working

### **Input:**
- [ ] Enhanced Input System configured
- [ ] Input Actions created (Move, Look, Jump, etc.)
- [ ] Keyboard/Mouse mappings working
- [ ] Virtual Joystick implemented (mobile)
- [ ] Touch buttons working
- [ ] Touch gestures functional

### **Testing:**
- [ ] Character moves in all directions
- [ ] Animations transition smoothly
- [ ] Camera modes switch correctly
- [ ] No clipping through geometry
- [ ] Performance: 60 FPS on desktop

---

## 🎉 READY FOR PHASE 3!

Wenn alle Checkboxen ✅ sind, ist **Phase 2 abgeschlossen!**

**Nächster Schritt:** Phase 3 - Backend Integration (HTTP Client Plugin)

---

**Geschätzte Dauer:** 2 Wochen
**Nach Abschluss:** Progress Report + Git Commit + Push
