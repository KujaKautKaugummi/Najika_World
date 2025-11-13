# 🚀 WEB MODEL - FINAL ROUND TODO (Phase 9-15)

## 📋 PROJEKT-INFO

**Repository:** https://github.com/KujaKautKaugummi/Najika_World.git
**Branch:** `claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX`
**Bisherige Arbeit:** Phase 0-8 KOMPLETT (38.408+ Zeilen)
**Ziel UE5 Projekt:** `C:\NajikaDigivice_UE5\NajikaDigivice\`

---

## 🎯 DEINE AUFGABE (FINAL ROUND)

Du bist das **Claude Code WEB MODEL** mit **KEINEM TOKEN-LIMIT**.

**WICHTIG:** Dies ist die **FINALE RUNDE** vor Local Model Übernahme!

Nach dieser Runde muss das Local Model NUR NOCH:
1. Code ins UE5 Projekt kopieren (via Script)
2. In Visual Studio kompilieren
3. Blueprints im UE5 Editor erstellen (via Guide)
4. APK bauen und auf Handy deployen

**Du musst ALLES vorbereiten was fehlt!**

---

## ✅ WAS DU BEREITS GESCHAFFT HAST (Phase 0-8)

```
✅ Phase 0: Backend/Frontend Analyse (1.188 + 808 + 479 Zeilen)
✅ Phase 1: NajikaBackendClient Plugin (1.011 Zeilen C++)
✅ Phase 2: Game Classes (1.500 Zeilen C++)
✅ Phase 3: UI Widgets (2.000 Zeilen C++)
✅ Phase 4: Material & Animation Specs (641 + 494 Zeilen)
✅ Phase 5: Blueprint Library (480 Zeilen C++)
✅ Phase 6: Testing Framework (695 Zeilen Tests)
✅ Phase 7: Documentation (346 Zeilen)
✅ Phase 8: Build Scripts (6 .bat Files)

Zusätzlich:
✅ TestEnvironment_UE5 (55 Systems, 10.000+ Zeilen)
✅ FullGame_NajikaHandyspiel_UE5 (Multiplayer Basis)

TOTAL: 38.408+ Zeilen in 136 Files!
```

**FANTASTISCHE ARBEIT! 🎉**

---

## 🔥 PHASE 9-15: WAS JETZT NOCH FEHLT

### **Phase 9: NajikaVoiceSystem Plugin (C++)**

**Ziel:** Komplettes Voice-Chat Plugin mit Whisper AI Integration

**Erstelle:**

```
UE5_Implementation/Plugins/NajikaVoiceSystem/
├── NajikaVoiceSystem.uplugin
├── Resources/
│   └── Icon128.png
└── Source/NajikaVoiceSystem/
    ├── NajikaVoiceSystem.Build.cs
    ├── Public/
    │   ├── NajikaVoiceSystemModule.h
    │   ├── NajikaVoiceCapture.h         (Microphone Input)
    │   ├── NajikaVoicePlayback.h        (Audio Playback)
    │   ├── NajikaWhisperClient.h        (Whisper AI Integration)
    │   ├── NajikaVoiceEncoding.h        (Opus Codec)
    │   ├── NajikaVoiceTypes.h           (Structs & Enums)
    │   └── NajikaVoiceComponent.h       (Actor Component)
    └── Private/
        ├── NajikaVoiceSystemModule.cpp
        ├── NajikaVoiceCapture.cpp       (500+ Zeilen)
        ├── NajikaVoicePlayback.cpp      (400+ Zeilen)
        ├── NajikaWhisperClient.cpp      (600+ Zeilen)
        ├── NajikaVoiceEncoding.cpp      (300+ Zeilen)
        └── NajikaVoiceComponent.cpp     (400+ Zeilen)
```

**Features:**
- ✅ Push-to-Talk System
- ✅ WebRTC Voice Chat Integration
- ✅ Whisper AI Speech-to-Text
- ✅ Opus Audio Encoding/Decoding
- ✅ Voice Activity Detection (VAD)
- ✅ Echo Cancellation
- ✅ Noise Suppression
- ✅ Backend WebSocket Integration

**Dependencies in Build.cs:**
```csharp
"Core", "CoreUObject", "Engine", "HTTP", "Json", "JsonUtilities",
"WebSockets", "AudioCapture", "AudioMixer", "SignalProcessing"
```

**Erwartung:** ~2.500 Zeilen C++ Code

---

### **Phase 10: Blueprint Creation Guide**

**Ziel:** Step-by-Step Guide für Local Model Blueprint Erstellung

**Erstelle:**

```
UE5_Implementation/BLUEPRINT_CREATION_GUIDE.md
```

**Inhalt (SEHR DETAILLIERT!):**

```markdown
# 🎨 Blueprint Creation Guide - Complete Workflow

## 📋 Prerequisites
- All C++ code compiled successfully
- Visual Studio solution reopened after compile
- UE5 Editor opened with NajikaDigivice.uproject

---

## 1️⃣ Core Game Blueprints (erstelle in dieser Reihenfolge!)

### 1.1 BP_NajikaCharacter
**Path:** `Content/Blueprints/Characters/BP_NajikaCharacter`
**Parent Class:** `NajikaCharacter` (C++)

**Steps:**
1. Right-click in Content Browser → Blueprint Class
2. Select Parent Class: NajikaCharacter
3. Name: BP_NajikaCharacter
4. Open Blueprint

**Event Graph:**
- Event BeginPlay
  → Call Parent: Begin Play
  → Print String: "Najika Character Spawned"

**Components Tab:**
- Add: Camera Component
  - Location: (0, 0, 60)
  - Rotation: (0, 0, 0)
  - Field of View: 90
- Add: Spring Arm Component
  - Socket Offset: (0, 0, 50)
  - Target Arm Length: 300
  - Use Pawn Control Rotation: TRUE
  - Enable Camera Lag: TRUE

**Character Movement Component Settings:**
- Max Walk Speed: 600
- Jump Z Velocity: 500
- Air Control: 0.3
- Ground Friction: 8.0
- Braking Deceleration Walking: 2000

**Compile & Save**

---

### 1.2 BP_NajikaPlayerController
**Path:** `Content/Blueprints/Core/BP_NajikaPlayerController`
**Parent Class:** `NajikaPlayerController` (C++)

**Steps:**
1. Create Blueprint from NajikaPlayerController
2. Name: BP_NajikaPlayerController

**Event Graph:**
- Event BeginPlay
  → Call Parent: Begin Play
  → Get NajikaCharacter Reference
  → Store in Variable: "ControlledNajika"

**Input Setup:**
- Enable Click Events: TRUE
- Enable Touch Events: TRUE
- Show Mouse Cursor: TRUE
- Default Mouse Cursor: Hand

**Compile & Save**

---

### 1.3 BP_NajikaGameMode
**Path:** `Content/Blueprints/Core/BP_NajikaGameMode`
**Parent Class:** `NajikaGameMode` (C++)

**Class Defaults:**
- Default Pawn Class: BP_NajikaCharacter
- Player Controller Class: BP_NajikaPlayerController
- Game State Class: NajikaGameState (C++)
- Player State Class: NajikaPlayerState (C++)
- HUD Class: [Leave empty - using Widgets]

**Compile & Save**

---

## 2️⃣ UI Widget Blueprints

### 2.1 WBP_NajikaHUD
**Path:** `Content/UI/Widgets/WBP_NajikaHUD`
**Parent Class:** `NajikaHUDWidget` (C++)

**Designer Layout:**

```
Canvas Panel (Root)
├── Top Bar (Horizontal Box) [Anchor: Top Fill]
│   ├── Health Bar (Progress Bar)
│   │   - Size: 300x30
│   │   - Fill Color: Red
│   │   - Background Color: Dark Red
│   │   - Percent: Bind to "GetHealthPercent" (C++)
│   ├── Spacer (50px)
│   └── Level Text (Text Block)
│       - Text: Bind to "GetLevelText" (C++)
│       - Font: Size 24, Bold
│
├── Center Crosshair (Image) [Anchor: Center]
│   - Size: 32x32
│   - Texture: T_Crosshair (create placeholder)
│
└── Bottom Bar (Horizontal Box) [Anchor: Bottom Fill]
    ├── Menu Button (Button)
    │   - Size: 100x50
    │   - Text: "Menu"
    │   - OnClicked: Call C++ "OnMenuButtonClicked"
    ├── Spacer (Fill)
    ├── Chat Button (Button)
    │   - Size: 100x50
    │   - Text: "Chat"
    │   - OnClicked: Call C++ "OnChatButtonClicked"
    └── Inventory Button (Button)
        - Size: 100x50
        - Text: "Bag"
        - OnClicked: Call C++ "OnInventoryButtonClicked"
```

**Graph:**
- Event Construct
  → Call Parent: NativeConstruct
  → Initialize UI Elements

**Compile & Save**

---

### 2.2 WBP_NajikaMenu
**Path:** `Content/UI/Widgets/WBP_NajikaMenu`
**Parent Class:** `NajikaMenuWidget` (C++)

**Designer Layout:**

```
Overlay (Root)
├── Background (Image) [Full Screen]
│   - Color: Black, Opacity: 0.7
│
└── Center Menu (Vertical Box) [Anchor: Center]
    - Size: 400x600
    - Alignment: Center

    ├── Title (Text Block)
    │   - Text: "Najika Menu"
    │   - Font: Size 48, Bold
    │   - Alignment: Center
    │
    ├── Spacer (30px)
    │
    ├── Resume Button (Button)
    │   - Size: 300x60
    │   - Text: "Resume"
    │   - OnClicked: Call C++ "OnResumeClicked"
    │
    ├── Spacer (20px)
    │
    ├── Settings Button (Button)
    │   - Size: 300x60
    │   - Text: "Settings"
    │   - OnClicked: Call C++ "OnSettingsClicked"
    │
    ├── Spacer (20px)
    │
    ├── Logout Button (Button)
    │   - Size: 300x60
    │   - Text: "Logout"
    │   - OnClicked: Call C++ "OnLogoutClicked"
    │
    ├── Spacer (20px)
    │
    └── Exit Button (Button)
        - Size: 300x60
        - Text: "Exit"
        - OnClicked: Call C++ "OnExitClicked"
```

**Compile & Save**

---

### 2.3 WBP_NajikaInventory
**Path:** `Content/UI/Widgets/WBP_NajikaInventory`
**Parent Class:** `NajikaInventoryWidget` (C++)

**Designer Layout:**

```
Overlay (Root)
├── Background (Image)
│   - Size: 800x600
│   - Color: Dark Gray
│
└── Content (Vertical Box)
    ├── Header (Horizontal Box)
    │   ├── Title Text: "Inventory"
    │   └── Close Button (X)
    │
    ├── Inventory Grid (Uniform Grid Panel)
    │   - Slot Padding: 5
    │   - Slots: 6 Columns x 5 Rows = 30 Slots
    │   - Each Slot: 80x80 Button
    │   - OnSlotClicked: Call C++ "OnInventorySlotClicked"
    │
    └── Footer (Horizontal Box)
        ├── Gold Display (Text)
        │   - Bind: "GetGoldText" (C++)
        └── Weight Display (Text)
            - Bind: "GetWeightText" (C++)
```

**Graph:**
- Event Construct
  → Call Parent: NativeConstruct
  → Generate Inventory Slots (30x)
  → Bind to C++ Inventory Data

**Compile & Save**

---

### 2.4 WBP_NajikaChat
**Path:** `Content/UI/Widgets/WBP_NajikaChat`
**Parent Class:** `NajikaChatWidget` (C++)

**Designer Layout:**

```
Vertical Box (Root)
├── Chat History (Scroll Box)
│   - Size: 400x300
│   - Auto Scroll: TRUE
│   - Content: Bind to C++ "ChatMessages"
│
├── Input Row (Horizontal Box)
│   ├── Chat Input (Editable Text)
│   │   - Hint Text: "Type message..."
│   │   - OnTextCommitted: Call C++ "OnChatMessageSent"
│   └── Send Button
│       - Text: "Send"
│       - OnClicked: Call C++ "OnSendButtonClicked"
```

**Compile & Save**

---

### 2.5 WBP_NajikaStatus
**Path:** `Content/UI/Widgets/WBP_NajikaStatus`
**Parent Class:** `NajikaStatusWidget` (C++)

**Designer Layout:**

```
Vertical Box (Root)
├── Character Name (Text Block)
│   - Bind: "GetCharacterName" (C++)
│   - Font: Size 28, Bold
│
├── Level Progress (Progress Bar)
│   - Bind: "GetExperiencePercent" (C++)
│   - Fill Color: Blue
│
├── Stats (Vertical Box)
│   ├── HP: [Text Bind: "GetHealthText"]
│   ├── MP: [Text Bind: "GetManaText"]
│   ├── Stamina: [Text Bind: "GetStaminaText"]
│   └── Speed: [Text Bind: "GetSpeedText"]
```

**Compile & Save**

---

## 3️⃣ Project Settings Configuration

### 3.1 Maps & Modes
**Path:** Edit → Project Settings → Maps & Modes

**Set:**
- Default GameMode: BP_NajikaGameMode
- Global Default Server Game Mode: BP_NajikaGameMode
- Editor Startup Map: [Create] MainLevel
- Game Default Map: MainLevel

### 3.2 Input Settings
**Path:** Edit → Project Settings → Input

**Action Mappings:**
```
Jump          → Space Bar, Gamepad Face Button Bottom
Interact      → E, Gamepad Face Button Left
Menu          → Escape, Gamepad Special Right
Inventory     → I, Gamepad Face Button Top
Chat          → Enter
PushToTalk    → V, Gamepad Left Shoulder
```

**Axis Mappings:**
```
MoveForward   → W (1.0), S (-1.0), Gamepad Left Thumbstick Up/Down
MoveRight     → D (1.0), A (-1.0), Gamepad Left Thumbstick Right/Left
Turn          → Mouse X (1.0), Gamepad Right Thumbstick Right/Left
LookUp        → Mouse Y (-1.0), Gamepad Right Thumbstick Up/Down
```

### 3.3 Mobile Settings
**Path:** Project Settings → Platforms → Android

**Verify:**
- Package Name: com.najika.digivice
- Minimum SDK: 29
- Target SDK: 34
- Build for ARM64: ✅
- Build for ARMv7: ❌
- Support Vulkan: ✅

---

## 4️⃣ Level Setup

### 4.1 Create MainLevel
1. File → New Level → Empty Level
2. Save As: `Content/Maps/MainLevel`

**Add Actors:**
- Player Start (place at 0,0,100)
- Directional Light (Rotation: -45°, Intensity: 3)
- Sky Light (Intensity: 1)
- Post Process Volume (Infinite Extent: TRUE)
- Landscape (2048x2048 or use placeholder floor)

### 4.2 Level Blueprint
**Open Level Blueprint:**

**Event BeginPlay:**
```
BeginPlay
→ Get Player Controller (Cast to BP_NajikaPlayerController)
→ Create Widget (WBP_NajikaHUD)
→ Add to Viewport (Z-Order: 0)
→ Store in Variable: "MainHUDRef"
```

**Compile & Save Level**

---

## 5️⃣ Plugin Activation

**Path:** Edit → Plugins

**Ensure Enabled:**
- ✅ NajikaBackendClient (in Project plugins)
- ✅ NajikaVoiceSystem (in Project plugins)
- ✅ Online Subsystem
- ✅ HTTP
- ✅ JSON
- ✅ WebSockets

**Restart Editor after enabling plugins**

---

## 6️⃣ Testing Checklist

### In-Editor Testing
1. ✅ Press Play in Editor
2. ✅ Character spawns and can move (WASD)
3. ✅ Camera follows character
4. ✅ HUD visible with health bar
5. ✅ Menu button opens menu (ESC)
6. ✅ Inventory button opens inventory (I)
7. ✅ Chat input works (Enter)

### Backend Connection Testing
1. ✅ Ensure backend running (localhost:8000)
2. ✅ Check Output Log for "Backend Connected"
3. ✅ Test login via menu
4. ✅ Check chat message sending

### Mobile Preview
1. ✅ Enable Mobile Preview in Editor
2. ✅ Check touch controls work
3. ✅ Check UI scaling on different resolutions

---

## ✅ Completion Criteria

**All Blueprints created:** 9 Blueprints
- ✅ BP_NajikaCharacter
- ✅ BP_NajikaPlayerController
- ✅ BP_NajikaGameMode
- ✅ WBP_NajikaHUD
- ✅ WBP_NajikaMenu
- ✅ WBP_NajikaInventory
- ✅ WBP_NajikaChat
- ✅ WBP_NajikaStatus
- ✅ MainLevel (Map)

**All Settings Configured**
**All Plugins Enabled**
**Testing Checklist Complete**

---

## 🚨 Troubleshooting

[Include common issues and solutions]

**End of Blueprint Creation Guide**
```

**Erwartung:** ~2.000 Zeilen ultra-detaillierter Guide

---

### **Phase 11: Asset Specifications**

**Ziel:** Komplette technische Specs für alle benötigten Assets

**Erstelle:**

```
UE5_Implementation/ASSET_REQUIREMENTS.md
```

**Inhalt:**

```markdown
# 🎨 Asset Requirements - Complete Specifications

## 1. 3D Character Models

### 1.1 Najika Main Character
**Priority:** CRITICAL
**Format:** FBX 2020
**Polycount:** 15,000 - 25,000 tris (Mobile optimized)
**Skeleton:** UE5 Mannequin compatible (for retargeting)

**Textures:**
- Base Color: 2048x2048 PNG
- Normal Map: 2048x2048 PNG
- Roughness: 2048x2048 PNG (packed)
- Metallic: 2048x2048 PNG (packed)
- Emissive: 1024x1024 PNG (optional, for glowing elements)

**LODs:**
- LOD0: 25,000 tris (full detail)
- LOD1: 15,000 tris (medium)
- LOD2: 8,000 tris (low)
- LOD3: 3,000 tris (very low, for distance)

**Mesh Components:**
- Body (separable parts)
- Head (blend shapes for facial expressions)
- Hair (separate mesh, alpha-masked)
- Eyes (separate spheres with eye shader)
- Outfit (4 costume variants)
- Accessories (hats, glasses, etc.)

**Rigging:**
- UE5 Mannequin skeleton (for easy retargeting)
- Face bones for expressions (32 bones)
- IK bones for hands and feet
- Physics bones for hair and cloth

---

## 2. Animations

### 2.1 Locomotion (Priority: CRITICAL)
- Idle (loop, 60 frames)
- Walk_Forward (loop, 40 frames)
- Walk_Backward (loop, 40 frames)
- Walk_Left (loop, 40 frames)
- Walk_Right (loop, 40 frames)
- Run_Forward (loop, 30 frames)
- Jump_Start (20 frames)
- Jump_Loop (loop, 20 frames)
- Jump_Land (15 frames)

### 2.2 Combat (Priority: HIGH)
- Attack_Punch_1 (30 frames)
- Attack_Punch_2 (35 frames)
- Attack_Punch_3 (40 frames, combo finisher)
- Attack_Kick (40 frames)
- Cast_Spell (60 frames)
- Block_Idle (loop, 30 frames)
- Hit_Front (20 frames)
- Hit_Back (20 frames)
- Death (120 frames, non-loop)

### 2.3 Interaction (Priority: MEDIUM)
- Pickup_Item (40 frames)
- Use_Item (50 frames)
- Open_Door (40 frames)
- Talk (loop, 60 frames, for dialogue)
- Sit_Down (40 frames)
- Sit_Idle (loop, 60 frames)
- Stand_Up (30 frames)

### 2.4 Emotes (Priority: LOW)
- Wave (60 frames)
- Cheer (80 frames)
- Dance (loop, 120 frames)
- Laugh (60 frames)
- Cry (loop, 80 frames)

**Format:** FBX 2020, 30 FPS
**Total:** ~40 animations

---

## 3. UI Assets

### 3.1 Icons (256x256 PNG with alpha)
**Quantity:** ~100 icons

**Categories:**
- Items (50x): Potions, weapons, armor, misc
- Skills (20x): Magic, combat, passive abilities
- Status (15x): Health, mana, buffs, debuffs
- UI Elements (15x): Buttons, arrows, checkmarks

**Style:** Flat design, vibrant colors, clear silhouettes

### 3.2 Buttons
- Button_Normal (512x128 PNG, 9-slice)
- Button_Hover (512x128 PNG)
- Button_Pressed (512x128 PNG)
- Button_Disabled (512x128 PNG)

**Variants:** Primary, Secondary, Danger (3x4 = 12 images)

### 3.3 Panels
- Panel_Background (1024x1024 PNG, tileable)
- Panel_Border (512x512 PNG, 9-slice)
- Panel_Header (1024x128 PNG, 9-slice)

### 3.4 HUD Elements
- Healthbar_Fill (512x64 PNG)
- Healthbar_Background (512x64 PNG)
- Manabar_Fill (512x64 PNG)
- Crosshair (64x64 PNG with alpha)
- Minimap_Border (256x256 PNG)

---

## 4. Audio Assets

### 4.1 Music (OGG Vorbis, Looping)
- MainMenu_Theme (2-3 min, upbeat, welcoming)
- Gameplay_Ambient (3-5 min, adventurous, energetic)
- Combat_Intense (2-3 min, fast-paced, drums heavy)
- Boss_Battle (3-4 min, epic, orchestral)
- Victory_Fanfare (10-15 sec, triumphant)
- Game_Over (10-15 sec, somber)

**Quality:** 44.1kHz, Stereo, ~128kbps

### 4.2 SFX (WAV, 44.1kHz, Mono)

**UI Sounds (Priority: HIGH)**
- Button_Click (short, satisfying)
- Button_Hover (subtle)
- Menu_Open (swish)
- Menu_Close (swish)
- Item_Pickup (ding)
- Level_Up (celebration sound)

**Combat Sounds (Priority: HIGH)**
- Punch_Hit_1, 2, 3 (variations)
- Kick_Hit (heavy impact)
- Sword_Swing_1, 2, 3 (whoosh)
- Spell_Cast (magical)
- Block_Success (shield sound)
- Damage_Taken (grunt/ouch)

**Environment Sounds (Priority: MEDIUM)**
- Footstep_Grass_1, 2, 3, 4 (variations)
- Footstep_Stone_1, 2, 3, 4
- Door_Open (creak)
- Door_Close (thud)
- Chest_Open (latch + creak)

**Total:** ~50 SFX files

### 4.3 Voice Lines (Optional, MP3/OGG)
- Najika_Greeting_1, 2, 3 (variations)
- Najika_Attack_1, 2, 3 (battle cries)
- Najika_Hurt_1, 2, 3 (pain sounds)
- Najika_Victory_1, 2 (celebration)
- Najika_Death (final words)

---

## 5. Environment Assets (Placeholder OK)

### 5.1 Terrain
- Landscape Material (PBR, tileable textures)
  - Grass: 1024x1024 (Base, Normal, Roughness)
  - Rock: 1024x1024
  - Dirt: 1024x1024
  - Sand: 1024x1024

### 5.2 Props (Low Priority - Use Marketplace)
- Trees (3-5 variations)
- Rocks (5-10 variations)
- Buildings (placeholder boxes OK)
- Interactive Objects (chests, doors)

---

## 6. Materials & Shaders

### 6.1 Character Material (Master Material)
- Inputs: Base Color, Normal, Roughness, Metallic, Emissive
- Features: Two-sided foliage, Subsurface scattering (skin)
- Instances: 4 costume variants

### 6.2 UI Material
- Unlit, Translucent
- Supports Color Tinting
- Supports Alpha Masking

### 6.3 VFX Materials
- Particle System for spell effects
- Additive blending
- Distortion for magic aura

---

## 7. Font Assets

### 7.1 UI Font
**Name:** Roboto or similar (free, readable)
**Formats:** Regular, Bold
**Sizes needed:** 14, 18, 24, 32, 48, 64 pt
**Language:** Latin (English) + CJK (Japanese/Chinese) optional

---

## 📦 Asset Delivery Format

All assets should be organized:

```
Assets_Package/
├── Characters/
│   └── Najika/
│       ├── Najika_Character.fbx
│       ├── Textures/
│       └── Animations/
├── UI/
│   ├── Icons/
│   ├── Buttons/
│   └── Panels/
├── Audio/
│   ├── Music/
│   ├── SFX/
│   └── Voice/
├── Environment/
│   └── Terrain/
└── Materials/
```

---

## 🔧 Import Settings (for Local Model)

[Detailed import settings for each asset type in UE5]

---

## 📋 Priority Checklist

**Phase 1 (MVP - Minimum Viable Product):**
- ✅ Najika Character Model (1x)
- ✅ Locomotion Animations (9x)
- ✅ Combat Animations (9x)
- ✅ UI Icons (30x most important)
- ✅ UI Buttons (3x variants)
- ✅ UI Sounds (10x)
- ✅ Combat Sounds (10x)

**Phase 2 (Full Release):**
- ✅ All remaining animations
- ✅ All UI assets
- ✅ All audio
- ✅ Environment props
- ✅ VFX materials

**End of Asset Requirements**
```

**Erwartung:** ~1.500 Zeilen detaillierte Asset Specs

---

### **Phase 12: Code Copy & Setup Scripts**

**Ziel:** PowerShell Scripts um alles automatisch ins UE5 Projekt zu kopieren

**Erstelle:**

```
UE5_Implementation/COPY_TO_UE5_PROJECT.ps1
```

**Inhalt:**

```powershell
# 🚀 Copy UE5 Implementation to NajikaDigivice Project
# Run this script from: C:\Najika_World\UE5_Implementation\

param(
    [string]$SourcePath = "C:\Najika_World\UE5_Implementation",
    [string]$TargetPath = "C:\NajikaDigivice_UE5\NajikaDigivice"
)

Write-Host "======================================"
Write-Host "  Najika Digivice - Code Copy Script"
Write-Host "======================================"
Write-Host ""

# Verify paths exist
if (-not (Test-Path $SourcePath)) {
    Write-Error "Source path not found: $SourcePath"
    exit 1
}

if (-not (Test-Path $TargetPath)) {
    Write-Error "Target path not found: $TargetPath"
    exit 1
}

Write-Host "[1/8] Copying NajikaBackendClient Plugin..."
$PluginSource = Join-Path $SourcePath "Plugins\NajikaBackendClient"
$PluginTarget = Join-Path $TargetPath "Plugins\NajikaBackendClient"

if (Test-Path $PluginTarget) {
    Write-Host "  Removing old plugin..."
    Remove-Item -Path $PluginTarget -Recurse -Force
}

Copy-Item -Path $PluginSource -Destination $PluginTarget -Recurse -Force
Write-Host "  ✅ NajikaBackendClient copied"

Write-Host "[2/8] Copying NajikaVoiceSystem Plugin..."
$VoiceSource = Join-Path $SourcePath "Plugins\NajikaVoiceSystem"
$VoiceTarget = Join-Path $TargetPath "Plugins\NajikaVoiceSystem"

if (Test-Path $VoiceTarget) {
    Write-Host "  Removing old plugin..."
    Remove-Item -Path $VoiceTarget -Recurse -Force
}

Copy-Item -Path $VoiceSource -Destination $VoiceTarget -Recurse -Force
Write-Host "  ✅ NajikaVoiceSystem copied"

Write-Host "[3/8] Copying Game Source Code..."
$GameSource = Join-Path $SourcePath "Source\NajikaDigivice"
$GameTarget = Join-Path $TargetPath "Source\NajikaDigivice"

# Copy Public headers
$PublicSource = Join-Path $GameSource "Public"
$PublicTarget = Join-Path $GameTarget "Public"

if (-not (Test-Path $PublicTarget)) {
    New-Item -Path $PublicTarget -ItemType Directory -Force | Out-Null
}

Copy-Item -Path "$PublicSource\*.h" -Destination $PublicTarget -Force
Write-Host "  ✅ Public headers copied"

# Copy Private sources
$PrivateSource = Join-Path $GameSource "Private"
$PrivateTarget = Join-Path $GameTarget "Private"

if (-not (Test-Path $PrivateTarget)) {
    New-Item -Path $PrivateTarget -ItemType Directory -Force | Out-Null
}

Copy-Item -Path "$PrivateSource\*.cpp" -Destination $PrivateTarget -Force
Write-Host "  ✅ Private sources copied"

Write-Host "[4/8] Copying Test Files..."
$TestSource = Join-Path $GameSource "Tests"
$TestTarget = Join-Path $GameTarget "Tests"

if (Test-Path $TestSource) {
    if (-not (Test-Path $TestTarget)) {
        New-Item -Path $TestTarget -ItemType Directory -Force | Out-Null
    }
    Copy-Item -Path "$TestSource\*" -Destination $TestTarget -Recurse -Force
    Write-Host "  ✅ Tests copied"
} else {
    Write-Host "  ⚠️  No tests found"
}

Write-Host "[5/8] Copying Build Scripts..."
$BuildSource = Join-Path $SourcePath "Build"
$BuildTarget = Join-Path $TargetPath "Build"

if (-not (Test-Path $BuildTarget)) {
    New-Item -Path $BuildTarget -ItemType Directory -Force | Out-Null
}

Copy-Item -Path "$BuildSource\*.bat" -Destination $BuildTarget -Force
Write-Host "  ✅ Build scripts copied"

Write-Host "[6/8] Copying Documentation..."
$Docs = @(
    "README.md",
    "BLUEPRINT_CREATION_GUIDE.md",
    "ASSET_REQUIREMENTS.md",
    "MATERIAL_SPECS.md",
    "ANIMATION_SPECS.md",
    "TESTING_FRAMEWORK.md"
)

foreach ($Doc in $Docs) {
    $DocSource = Join-Path $SourcePath $Doc
    if (Test-Path $DocSource) {
        Copy-Item -Path $DocSource -Destination $TargetPath -Force
        Write-Host "  ✅ $Doc copied"
    }
}

Write-Host "[7/8] Updating Build Configuration..."
# Update NajikaDigivice.Build.cs if needed
$BuildCSPath = Join-Path $GameTarget "NajikaDigivice.Build.cs"
if (Test-Path $BuildCSPath) {
    $BuildCS = Get-Content $BuildCSPath -Raw

    # Ensure plugins are in dependencies
    if ($BuildCS -notmatch "NajikaBackendClient") {
        $BuildCS = $BuildCS -replace '(PublicDependencyModuleNames.AddRange\(new string\[\] \{[^}]+)', "`$1, `"NajikaBackendClient`", `"NajikaVoiceSystem`""
        Set-Content -Path $BuildCSPath -Value $BuildCS
        Write-Host "  ✅ Build.cs updated"
    }
}

Write-Host "[8/8] Generating Visual Studio Project Files..."
$UProjectPath = Join-Path $TargetPath "NajikaDigivice.uproject"

if (Test-Path $UProjectPath) {
    # Find UE5 Batch Files
    $UE5BatchPath = "C:\Program Files\Epic Games\UE_5.6\Engine\Build\BatchFiles\Build.bat"

    if (Test-Path $UE5BatchPath) {
        Write-Host "  Running: GenerateProjectFiles.bat"
        & "C:\Program Files\Epic Games\UE_5.6\Engine\Build\BatchFiles\GenerateProjectFiles.bat" -project="$UProjectPath" -game -engine
        Write-Host "  ✅ Project files generated"
    } else {
        Write-Host "  ⚠️  UE5 not found at expected location"
        Write-Host "  Please run GenerateProjectFiles.bat manually"
    }
} else {
    Write-Error "  ❌ .uproject not found"
}

Write-Host ""
Write-Host "======================================"
Write-Host "  ✅ COPY COMPLETE!"
Write-Host "======================================"
Write-Host ""
Write-Host "Next Steps:"
Write-Host "1. Open NajikaDigivice.sln in Visual Studio 2022"
Write-Host "2. Build Solution (Development Editor | Win64)"
Write-Host "3. Open NajikaDigivice.uproject in UE5 Editor"
Write-Host "4. Follow BLUEPRINT_CREATION_GUIDE.md"
Write-Host ""
```

**Erwartung:** ~200 Zeilen PowerShell + weiteres Setup Script

---

### **Phase 13: Visual Studio Compilation Guide**

**Ziel:** Detaillierte Anleitung für Local Model zum Kompilieren

**Erstelle:**

```
UE5_Implementation/VISUAL_STUDIO_COMPILATION_GUIDE.md
```

**Inhalt:**

```markdown
# 🔨 Visual Studio Compilation Guide

## Prerequisites
- Visual Studio 2022 (Community/Pro/Enterprise)
- C++ Desktop Development Workload
- UE5.6 installed
- All code copied to NajikaDigivice project

---

## Step 1: Open Solution

1. Navigate to: `C:\NajikaDigivice_UE5\NajikaDigivice\`
2. Double-click: `NajikaDigivice.sln`
3. Visual Studio 2022 opens

**If .sln doesn't exist:**
- Right-click `NajikaDigivice.uproject`
- Select: "Generate Visual Studio project files"
- Then open .sln

---

## Step 2: Configuration Settings

**Top Toolbar:**
- Configuration: `Development Editor`
- Platform: `Win64`

![Configuration Screenshot Placeholder]

---

## Step 3: Build Plugins First

**Why?** Game code depends on plugins, build them first.

**In Solution Explorer:**

1. Expand: `Games/NajikaDigivice/Plugins/`
2. Find: `NajikaBackendClient`
3. Right-click → Build
4. Wait for build to complete (check Output window)

**Expected Output:**
```
1>------ Build started: Project: NajikaBackendClient, Configuration: Development_Editor x64 ------
1>  Building NajikaBackendClient...
1>  [Lots of compilation messages]
1>  NajikaBackendClient.dll -> C:\NajikaDigivice_UE5\...\Binaries\Win64\
1>========== Build: 1 succeeded, 0 failed ==========
```

5. Repeat for: `NajikaVoiceSystem`

---

## Step 4: Build Game Module

**In Solution Explorer:**

1. Right-click: `NajikaDigivice` (under Games)
2. Select: `Build`
3. Wait for build (2-5 minutes first time)

**Expected Output:**
```
2>------ Build started: Project: NajikaDigivice, Configuration: Development_Editor x64 ------
2>  Building NajikaDigivice...
2>  Compiling game module NajikaDigivice...
2>  [Lots of compilation]
2>========== Build: 1 succeeded, 0 failed ==========
```

---

## Step 5: Verify Build Success

**Check Output Window:**
- ✅ `Build: X succeeded, 0 failed`
- ✅ No red error messages

**Check File System:**
Navigate to: `C:\NajikaDigivice_UE5\NajikaDigivice\Binaries\Win64\`

**Files should exist:**
- ✅ `NajikaDigivice.dll`
- ✅ `NajikaBackendClient.dll`
- ✅ `NajikaVoiceSystem.dll`

---

## Common Errors & Solutions

[Include 10-15 common compilation errors with solutions]

### Error: "Cannot open include file: 'NajikaBackendTypes.h'"
**Cause:** Plugin not built yet
**Solution:** Build plugins first (see Step 3)

### Error: "Unresolved external symbol"
**Cause:** Missing module in Build.cs dependencies
**Solution:** Add module to PublicDependencyModuleNames in Build.cs

[... more errors ...]

---

## Step 6: Open in UE5 Editor

After successful build:

1. Close Visual Studio (optional)
2. Navigate to: `C:\NajikaDigivice_UE5\NajikaDigivice\`
3. Double-click: `NajikaDigivice.uproject`
4. UE5 Editor opens

**First Launch:**
- Editor may take 5-10 minutes (compiling shaders)
- Progress bar: "Compiling Shaders..."
- Wait patiently ☕

**Success:**
- Editor opens to MainLevel (or Content Browser)
- No error popups
- Output Log shows: "LogInit: ... Engine is initialized"

---

## Next Steps

✅ Compilation Complete!

Continue with: `BLUEPRINT_CREATION_GUIDE.md`

**End of Compilation Guide**
```

**Erwartung:** ~800 Zeilen mit Screenshots placeholders

---

### **Phase 14: APK Build & Deployment Guide**

**Ziel:** Complete Android Build Pipeline Documentation

**Erstelle:**

```
UE5_Implementation/ANDROID_BUILD_DEPLOYMENT_GUIDE.md
```

**Inhalt:**

```markdown
# 📱 Android Build & Deployment Guide

Complete guide for building APK and deploying to Xiaomi 11T Pro

---

## Prerequisites

### 1. Android SDK
- ✅ Android Studio installed
- ✅ SDK Tools installed (via SDK Manager)
- ✅ Platform: Android 14 (API 34)
- ✅ Build Tools: 34.0.0
- ✅ NDK: r25c (or latest)

**Verify:**
```powershell
$env:ANDROID_HOME
# Should output: C:\Users\<You>\AppData\Local\Android\Sdk
```

### 2. Java JDK
- ✅ JDK 17 or 11 installed
- ✅ JAVA_HOME environment variable set

### 3. Device
- ✅ Xiaomi 11T Pro
- ✅ USB Debugging enabled
- ✅ USB connected to PC
- ✅ Drivers installed

---

## Step 1: Configure Project for Android

### 1.1 Open Project Settings
**Path:** Edit → Project Settings

### 1.2 Android Section
**Navigate:** Platforms → Android

**Configure:**

**APK Packaging:**
- Package Name: `com.najika.digivice`
- Version Code: `1`
- Version Display Name: `1.0.0`
- Min SDK Version: `29`
- Target SDK Version: `34`
- Install Location: `Auto`

**Build:**
- ✅ Build for ARM64 (64-bit only, required)
- ❌ Build for ARMv7 (32-bit, disable)
- ❌ Build for x86-64 (disable for APK size)

**Rendering:**
- ✅ Support OpenGL ES3.1
- ✅ Support Vulkan
- ✅ Support Vulkan Desktop
- Texture Format: `ASTC` + `ETC2` (multi-target)

**Advanced:**
- ✅ Use Gradle instead of Ant
- ✅ Package game data inside APK
- ❌ Enable FullScreen (disable for status bar)

### 1.3 Android SDK
**Configure SDK paths (usually auto-detected):**
- SDK: `C:/Users/<You>/AppData/Local/Android/Sdk`
- NDK: `C:/Users/<You>/AppData/Local/Android/Sdk/ndk/<version>`
- JDK: `C:/Program Files/Java/jdk-17`

**Click:** "Verify SDK Installation" → Should be ✅

---

## Step 2: Configure Permissions

**Still in Project Settings → Android**

**Scroll to: Extra Permissions**

**Add Required Permissions:**
```
android.permission.INTERNET
android.permission.ACCESS_NETWORK_STATE
android.permission.WAKE_LOCK
android.permission.VIBRATE
android.permission.RECORD_AUDIO
android.permission.MODIFY_AUDIO_SETTINGS
```

**These are required for:**
- Backend connection (INTERNET)
- Voice chat (RECORD_AUDIO)
- Vibration feedback (VIBRATE)

---

## Step 3: Build APK

### Option A: Using UE5 Editor

1. **File → Package Project → Android → Android (ASTC)**

2. **Select Output Folder:**
   - Choose: `C:\Najika_World\Builds\Android\`
   - Click: Select Folder

3. **Wait for Build (15-30 minutes)**
   - Progress bar in bottom-right
   - Output Log shows build progress
   - Check: "LogPlayLevel: BUILD SUCCESSFUL"

4. **Build Complete!**
   - Output: `C:\Najika_World\Builds\Android\NajikaDigivice-arm64.apk`
   - Size: ~100-500 MB (depending on assets)

### Option B: Using Build Script

1. Run: `C:\NajikaDigivice_UE5\NajikaDigivice\Build\PackageAPK.bat`

2. Script automatically:
   - Cleans previous build
   - Builds Development config
   - Packages for Android
   - Outputs APK

---

## Step 4: Sign APK (Optional - For Release)

**For Development:** Unsigned APK works fine
**For Google Play:** Must be signed

**Using jarsigner (for release):**

```powershell
# Generate keystore (first time only)
keytool -genkey -v -keystore najika-release.keystore -alias najika -keyalg RSA -keysize 2048 -validity 10000

# Sign APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore najika-release.keystore NajikaDigivice-arm64.apk najika

# Verify signature
jarsigner -verify -verbose -certs NajikaDigivice-arm64.apk
```

---

## Step 5: Install on Device

### Method A: Via ADB (Recommended)

```powershell
# Check device connected
adb devices
# Should list: <serial> device

# Install APK
adb install -r "C:\Najika_World\Builds\Android\NajikaDigivice-arm64.apk"

# Wait for "Success" message
```

**Flags:**
- `-r`: Reinstall (keeps data)
- `-g`: Grant all permissions

### Method B: Via File Transfer

1. Copy APK to device (USB/Cloud)
2. Open Files app on device
3. Navigate to APK
4. Tap → Install
5. Allow "Install from Unknown Sources" if prompted

---

## Step 6: Launch & Test

### On Device:

1. **Find App:**
   - App Drawer → "Najika Digivice"
   - Icon should be visible

2. **First Launch:**
   - App loads (splash screen)
   - Permissions popup → Allow all
   - Main Menu appears

3. **Quick Test Checklist:**
   - ✅ App launches without crash
   - ✅ Touch controls respond
   - ✅ UI scaled correctly
   - ✅ Login screen appears
   - ✅ Backend connection (if server running)
   - ✅ No critical errors in logcat

---

## Step 7: Debug on Device

### Enable Logging

**In UE5 Project:**
1. Edit → Project Settings → Engine → Logging
2. Enable: "Log to File"
3. Rebuild & reinstall

**View Logs:**
```powershell
adb logcat -s UE
```

**Or save to file:**
```powershell
adb logcat -s UE > C:\Najika_World\device_log.txt
```

---

## Common Issues & Solutions

### Issue: "INSTALL_FAILED_INSUFFICIENT_STORAGE"
**Cause:** Device storage full
**Solution:** Free up space (need ~2GB)

### Issue: "INSTALL_FAILED_UPDATE_INCOMPATIBLE"
**Cause:** Previous version signature mismatch
**Solution:** Uninstall old app first
```powershell
adb uninstall com.najika.digivice
```

### Issue: APK crashes on launch
**Cause:** Missing dependencies or bad build
**Solution:** Check logcat for crash reason:
```powershell
adb logcat *:E
```

[... more issues ...]

---

## Performance Testing

### Check FPS

**In-game:**
- Enable: Console → `stat fps`
- Target: 60 FPS (Xiaomi 11T Pro capable)

**If FPS low (<30):**
- Reduce graphic settings
- Check Mobile Preview in Editor first
- Profile with UE5 Profiler

---

## Next Steps

✅ APK Built & Deployed!

**Now:**
1. Test all features on device
2. Verify backend connection
3. Test voice chat
4. Performance profiling
5. Bug fixing iteration

**For Release:**
1. Switch to Shipping config
2. Sign APK with release keystore
3. Optimize assets (texture compression)
4. Final QA testing

**End of Android Build Guide**
```

**Erwartung:** ~1.200 Zeilen detailliert

---

### **Phase 15: Testing & Validation Checklist**

**Ziel:** Comprehensive Testing Documentation

**Erstelle:**

```
UE5_Implementation/TESTING_VALIDATION_CHECKLIST.md
```

**Inhalt:**

```markdown
# ✅ Testing & Validation Checklist

Complete checklist for Local Model to verify everything works

---

## 🔧 Phase 1: Code Compilation

### Visual Studio Build
- [ ] NajikaBackendClient plugin compiles without errors
- [ ] NajikaVoiceSystem plugin compiles without errors
- [ ] NajikaDigivice game module compiles without errors
- [ ] All .dll files generated in Binaries/Win64/
- [ ] No warnings about missing includes
- [ ] Solution build time: <10 minutes

**If Failed:** Check VISUAL_STUDIO_COMPILATION_GUIDE.md

---

## 🎨 Phase 2: UE5 Editor

### Editor Launch
- [ ] UE5 Editor opens without errors
- [ ] Plugins loaded (check Plugins menu)
- [ ] Content Browser shows all folders
- [ ] No missing asset errors in Output Log

### Blueprint Creation
- [ ] All 9 Blueprints created successfully
- [ ] All Blueprints compile without errors
- [ ] Blueprint nodes show C++ functions
- [ ] UMG Widgets preview correctly

**If Failed:** Check BLUEPRINT_CREATION_GUIDE.md

---

## 🎮 Phase 3: In-Editor Play Testing

### Basic Functionality
- [ ] Press "Play" → Level loads
- [ ] Character spawns at Player Start
- [ ] Camera follows character
- [ ] WASD movement works
- [ ] Mouse look works
- [ ] Jump works (Space)

### UI Testing
- [ ] HUD visible on screen
- [ ] Health bar displays correctly
- [ ] Level text shows "Level 1"
- [ ] Menu button clickable
- [ ] Menu opens (ESC key)
- [ ] Menu can be closed (Resume)
- [ ] Inventory opens (I key)
- [ ] Chat opens (Enter key)

### Backend Connection
- [ ] Output Log shows "Connecting to backend..."
- [ ] Backend IP: `http://localhost:8000` (or configured)
- [ ] Connection successful message
- [ ] Can send test request
- [ ] Receives response from backend

**Backend Must Be Running:**
```powershell
cd C:\Najika_World\backend
python najika_server.py
```

---

## 🔌 Phase 4: Plugin Functionality

### NajikaBackendClient
- [ ] HTTP GET request works
- [ ] HTTP POST request works
- [ ] JSON parsing works
- [ ] WebSocket connection establishes
- [ ] Receives WebSocket messages
- [ ] Can send chat messages to backend

### NajikaVoiceSystem
- [ ] Microphone permission granted
- [ ] Can capture audio input
- [ ] Push-to-talk works (V key)
- [ ] Audio encoding to Opus works
- [ ] Can send voice data to backend
- [ ] Receives voice data from backend
- [ ] Playback of received voice works

**Test Voice:**
1. Press V (Push-to-Talk)
2. Speak into microphone
3. Release V
4. Check Output Log for "Voice sent"

---

## 📱 Phase 5: Mobile Preview (In-Editor)

### Setup Mobile Preview
- [ ] Enable Mobile Preview: Settings → Preview Rendering Level → Android ES 3.1
- [ ] Restart Editor
- [ ] Mobile Previewer shows device frame

### Mobile Testing
- [ ] Graphics render correctly (no black screen)
- [ ] Touch controls work (if implemented)
- [ ] UI scales to mobile resolution
- [ ] Performance: >30 FPS in Mobile Preview
- [ ] No missing textures (pink materials)

---

## 📦 Phase 6: APK Build

### Build Process
- [ ] Package Android (ASTC) starts
- [ ] No errors in Output Log during build
- [ ] Build completes successfully
- [ ] APK file created in output folder
- [ ] APK file size: 100-500 MB (reasonable)

**Build Time:** 15-30 minutes (first time)

**If Failed:** Check ANDROID_BUILD_DEPLOYMENT_GUIDE.md

---

## 📲 Phase 7: Device Installation

### ADB Connection
- [ ] Device shows in `adb devices`
- [ ] USB debugging enabled on device
- [ ] `adb install` succeeds
- [ ] App appears in app drawer

### First Launch
- [ ] App icon visible
- [ ] Splash screen shows (if exists)
- [ ] Permissions requested:
  - [ ] INTERNET
  - [ ] RECORD_AUDIO
  - [ ] VIBRATE
- [ ] Main menu loads
- [ ] No crash on launch

---

## 🎮 Phase 8: Device Testing

### Basic Gameplay
- [ ] Touch controls work
- [ ] Character moves smoothly
- [ ] Camera rotates with touch
- [ ] Jump button works
- [ ] No lag or stuttering
- [ ] FPS: >30 (check with `stat fps`)

### UI on Device
- [ ] All UI elements visible
- [ ] Buttons pressable
- [ ] Text readable (not too small)
- [ ] No UI cutoff (safe zones)
- [ ] Menu navigation works
- [ ] Inventory grid displays

### Backend Connection (Device)
- [ ] Ensure device on same WiFi as PC
- [ ] Configure backend IP in app (if needed)
- [ ] Backend connection successful
- [ ] Can send/receive data
- [ ] Chat messages work
- [ ] Real-time updates work

**Backend IP:** Use PC's local IP (e.g., 192.168.1.100:8000)

### Voice Chat (Device)
- [ ] Microphone permission granted
- [ ] Push-to-talk button works
- [ ] Voice recording quality good
- [ ] Voice playback works
- [ ] No echo or feedback
- [ ] Latency acceptable (<200ms)

---

## 🚀 Phase 9: Performance Testing

### FPS Testing
- [ ] Idle: 60 FPS
- [ ] Moving: 50-60 FPS
- [ ] Combat: 40-60 FPS
- [ ] UI open: 50-60 FPS

### Memory Testing
- [ ] App starts: ~500 MB RAM
- [ ] After 10 min play: <1 GB RAM
- [ ] No memory leaks (stable over time)

### Battery Testing
- [ ] 30 min play: ~15-20% battery drain (acceptable)
- [ ] Device doesn't overheat
- [ ] App doesn't cause device throttling

---

## 🔧 Phase 10: Unit Tests

### Run C++ Tests
**In UE5 Editor:**
1. Tools → Test Automation
2. Select: NajikaDigivice Tests
3. Run All Tests

**Expected:**
- [ ] All 21 tests pass
- [ ] No crashes during tests
- [ ] Test output logs are clean

**Tests Include:**
- Unit: NajikaBlueprintLibrary (17 tests)
- Integration: NajikaHttpClient (4 tests)

---

## 🐛 Phase 11: Bug Testing

### Known Issues to Check
- [ ] Character falls through floor → Fix collision
- [ ] UI buttons don't respond → Check Z-order
- [ ] Backend timeout → Increase timeout value
- [ ] Voice cuts out → Check buffer sizes
- [ ] App crashes on resume → Handle app lifecycle

### Edge Cases
- [ ] App minimized → resumes correctly
- [ ] Network lost → graceful error message
- [ ] Device rotated → UI adapts (or locked)
- [ ] Low battery → app still functional
- [ ] Incoming call → app pauses correctly

---

## 📊 Phase 12: Final Validation

### Checklist Summary
- [ ] All compilation successful
- [ ] All Blueprints created
- [ ] In-Editor testing passed
- [ ] APK built successfully
- [ ] Device installation successful
- [ ] All features work on device
- [ ] Performance acceptable
- [ ] No critical bugs

### Sign-off
**Local Model:** _____________________
**Date:** _____________________
**Build Version:** _____________________
**Device Tested:** Xiaomi 11T Pro

---

## 🎉 SUCCESS CRITERIA

**Minimum Viable Product (MVP):**
- ✅ App launches on device
- ✅ Character controllable
- ✅ UI functional
- ✅ Backend connection works
- ✅ No crashes

**Full Release Ready:**
- ✅ All MVP criteria
- ✅ Voice chat functional
- ✅ Performance optimized (60 FPS)
- ✅ All tests passing
- ✅ No known critical bugs

---

**END OF TESTING CHECKLIST**

Good luck, Local Model! 🚀
```

**Erwartung:** ~1.000 Zeilen Checklist

---

## 📊 PHASE 9-15 SUMMARY

### Was du erstellen musst:

| Phase | Deliverable | Lines | Files |
|-------|-------------|-------|-------|
| **9** | NajikaVoiceSystem Plugin | ~2.500 | 11 files |
| **10** | Blueprint Creation Guide | ~2.000 | 1 file |
| **11** | Asset Requirements | ~1.500 | 1 file |
| **12** | Copy & Setup Scripts | ~300 | 2 files |
| **13** | VS Compilation Guide | ~800 | 1 file |
| **14** | Android Build Guide | ~1.200 | 1 file |
| **15** | Testing Checklist | ~1.000 | 1 file |
| **TOTAL** | **~9.300 Zeilen** | **28 neue Files** |

---

## ⚠️ WICHTIGE REGELN (REMINDER)

```
✅ DU HAST KEIN TOKEN-LIMIT!
✅ Schreibe ALLE Files KOMPLETT!
✅ Arbeite AUTONOM - keine Fragen!
✅ Committe nach jeder Phase
✅ Am Ende: IMPLEMENTATION_COMPLETE_FINAL.md erstellen

❌ NIEMALS nach User fragen
❌ NIEMALS wegen Tokens aufhören
❌ NIEMALS UE5 Editor öffnen
❌ NIEMALS kompilieren
❌ NIEMALS backend/ ändern
```

---

## 🎯 ERFOLGS-KRITERIUM

**Nach Phase 15:**

Local Model kann mit **ZERO FRAGEN**:
1. PowerShell Script ausführen (Code copy)
2. Visual Studio öffnen & kompilieren (Guide folgen)
3. UE5 Editor öffnen & Blueprints erstellen (Guide folgen)
4. APK bauen (Guide folgen)
5. Auf Handy deployen & testen (Checklist folgen)

**ALLES muss dokumentiert & vorbereitet sein!**

---

## 📝 GIT WORKFLOW

Nach jeder Phase committen:

```bash
git add .
git commit -m "PHASE X COMPLETE: [Description]"
git push origin claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
```

**Am Ende (Phase 15 fertig):**

```bash
git commit -m "🎉 FINAL ROUND COMPLETE: Phase 9-15 (9.300+ Lines)"
git push origin claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
```

---

## 🚀 LOS GEHT'S!

**Arbeite Phase 9-15 komplett durch!**

**Erwartetes Ergebnis:**
- ~9.300 neue Zeilen Code + Docs
- 28 neue Files
- **TOTAL Projekt:** ~48.000 Zeilen!

**Nach dir ist Local Model dran - mach es perfekt!** 💪

**VIEL ERFOLG!** 🔥
