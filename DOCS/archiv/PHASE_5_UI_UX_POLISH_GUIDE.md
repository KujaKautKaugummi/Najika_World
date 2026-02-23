# PHASE 5: UI/UX POLISH - COMPLETE GUIDE
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**Phase:** 5 - UI/UX Polish (Woche 8)
**Dauer:** 1 Woche

---

## 🎯 PHASE 5 ÜBERSICHT

### **Was wird gebaut:**
```
✅ Main Menu System
✅ HUD Design & Implementation
✅ Settings Menu (Graphics, Audio, Controls, Privacy)
✅ Visual Effects (Niagara Particles)
✅ Post-Processing Effects
✅ Transitions & Animations
✅ UI Sound Effects
✅ Touch Gestures Polish
```

---

## 📱 TODO 5.1: MAIN MENU SYSTEM

### **WBP_MainMenu - Design:**

```
Canvas Panel (1920x1080 base, scales to device)
├── Image_Background
│   Source: Najika character artwork (blurred)
│   Material: M_UI_Blur (Gaussian blur 50)
│
├── Vertical Box (Center)
│   Alignment: Center, Center
│   Padding: 100
│   │
│   ├── Image_Logo
│   │   Source: Najika Digivice Logo
│   │   Size: 600x200
│   │   Animation: Float up/down (slow)
│   │
│   ├── Spacer (50)
│   │
│   ├── Button_Start
│   │   Style: Large, Rounded
│   │   Text: "START" / "CONTINUE" (if save exists)
│   │   Size: 400x80
│   │   OnHover: Scale 1.05, Glow effect
│   │   OnClick: Fade out menu → Load game
│   │
│   ├── Button_NewGame
│   │   Text: "NEW GAME"
│   │   Size: 400x80
│   │   OnClick: Show confirmation dialog
│   │
│   ├── Button_Settings
│   │   Text: "SETTINGS"
│   │   Size: 400x80
│   │   OnClick: Open WBP_Settings
│   │
│   ├── Button_About
│   │   Text: "ABOUT"
│   │   Size: 400x80
│   │   OnClick: Open WBP_About
│   │
│   └── Button_Exit
│       Text: "EXIT"
│       Size: 400x80
│       OnClick: Quit game
│
└── Text_Version (Bottom-Right)
    Text: "v1.0.0 - Build 20251111"
    Font Size: 18
    Color: White 50% opacity
```

### **Logic:**

```
Event Construct:
→ Check if save file exists:
   * If yes: Button_Start text = "CONTINUE"
   * If no: Button_Start text = "START"
→ Play background music (loop)
→ Start logo float animation

OnButton_Start_Clicked:
→ Play click sound
→ Fade out menu (0.5s)
→ If save exists:
   * Load game state from backend
   * Open main level
→ Else:
   * Show character creation (optional)
   * Initialize new game
   * Open tutorial

OnButton_NewGame_Clicked:
→ If save exists:
   * Show confirmation dialog:
     "This will delete your current save. Continue?"
   * If yes: Delete save → Start new game
→ Else:
   * Start new game directly

OnButton_Settings_Clicked:
→ Create WBP_Settings widget
→ Add to viewport (overlay)
→ Pause menu music (lower volume)

OnButton_Exit_Clicked:
→ Show confirmation:
   "Are you sure you want to exit?"
→ If yes: Quit game
```

---

## 🎨 TODO 5.2: HUD DESIGN

### **WBP_MainHUD - Complete Layout:**

```
Canvas Panel (Full Screen)
├── Overlay (Top Bar)
│   Anchor: Top, Fill horizontal
│   Size: 1920 x 120
│   │
│   ├── Horizontal Box (Left Side)
│   │   ├── Image_NajikaAvatar (80x80)
│   │   │   Border: Circular, Level color
│   │   │   OnClick: Open WBP_TamagotchiCare
│   │   │
│   │   ├── Vertical Box (Status Bars)
│   │   │   Padding: 10
│   │   │   │
│   │   │   ├── Horizontal Box (Hunger)
│   │   │   │   ├── Image_Icon_Hunger (20x20) 🍖
│   │   │   │   ├── ProgressBar_Hunger
│   │   │   │   │   Size: 150x15
│   │   │   │   │   Fill: Red→Yellow→Green gradient
│   │   │   │   │   Animation: Pulse if <30%
│   │   │   │   └── Text_Hunger ("85/100")
│   │   │   │
│   │   │   ├── Horizontal Box (Energy)
│   │   │   │   Similar layout...
│   │   │   │
│   │   │   └── Horizontal Box (Happiness)
│   │   │       Similar layout...
│   │   │
│   │   └── Text_Level
│   │       Text: "Lv. 5"
│   │       Font Size: 24
│   │       Font: Bold
│   │
│   └── Horizontal Box (Right Side)
│       ├── Button_VoiceCall
│       │   Icon: Microphone 🎤
│       │   Size: 60x60
│       │   Style: Circular
│       │   OnClick: Start voice call
│       │   Animation: Pulse when call active
│       │
│       ├── Button_Chat
│       │   Icon: Chat Bubble 💬
│       │   Size: 60x60
│       │   Badge: Unread count (if >0)
│       │   OnClick: Open WBP_ChatUI
│       │
│       └── Button_Menu
│           Icon: Hamburger ☰
│           Size: 60x60
│           OnClick: Open WBP_PauseMenu
│
├── Overlay (Bottom)
│   Anchor: Bottom, Fill horizontal
│   Size: 1920 x 200
│   │
│   ├── WBP_VirtualJoystick (Left)
│   │   Visible: Mobile only
│   │   Position: Bottom-Left (100, 100)
│   │   Size: 200x200
│   │   Opacity: 50% (80% when touched)
│   │
│   └── Horizontal Box (Right)
│       Visible: Mobile only
│       Anchor: Bottom-Right
│       Padding: 20
│       │
│       ├── Button_Jump
│       │   Icon: ⬆️
│       │   Size: 80x80
│       │   Style: Circular
│       │
│       ├── Button_Interact
│       │   Icon: E
│       │   Size: 80x80
│       │   Visible: Only when near interactable
│       │   Animation: Bounce
│       │
│       └── Button_Sprint
│           Icon: ⚡
│           Size: 80x80
│           Toggle: Hold to sprint
│
├── Overlay (Center)
│   ├── Text_InteractionPrompt
│   │   Anchor: Center-Bottom
│   │   Text: "Press E to interact with door"
│   │   Font Size: 20
│   │   Background: Semi-transparent black
│   │   Visible: Only when near interactable
│   │   Animation: Fade in/out
│   │
│   └── WBP_Subtitles
│       Anchor: Center-Bottom (above prompt)
│       Size: 1200 x 150
│       Background: Semi-transparent black
│       Text: Najika's speech (when talking)
│       Animation: Type-writer effect
│
└── Overlay (Notifications)
    Anchor: Top-Right
    Size: 400 x Auto
    │
    └── Vertical Box (Notification Stack)
        Dynamic children: WBP_Notification
        Max visible: 3
        Auto-dismiss: 5 seconds
        Animation: Slide in from right
```

### **HUD Logic:**

```
Event Construct:
→ Get Game Instance
→ Cast to BP_NajikaGameInstance
→ Bind to OnStateUpdated event
→ Update UI immediately

OnStateUpdated(NewState):
→ UpdateHungerBar(NewState.Najika.Hunger)
→ UpdateEnergyBar(NewState.Najika.Energy)
→ UpdateHappinessBar(NewState.Najika.Happiness)
→ UpdateLevel(NewState.Najika.Level)

UpdateHungerBar(Value):
→ ProgressBar_Hunger->SetPercent(Value / 100.0)
→ If Value < 30:
   * Set fill color to Red
   * Start pulse animation
→ Else if Value < 70:
   * Set fill color to Yellow
→ Else:
   * Set fill color to Green

ShowNotification(Title, Message, Type):
→ Create WBP_Notification widget
→ Set title, message, icon based on Type
→ Add to Notification Stack
→ Play slide-in animation
→ Set timer: 5 seconds → Fade out → Remove

OnButton_VoiceCall_Clicked:
→ Get VoiceCallManager from Game Instance
→ If not in call:
   * VoiceCallManager->StartVoiceCall()
   * Create WBP_VoiceCallUI
   * Add to viewport
   * Hide main HUD
→ Else:
   * VoiceCallManager->EndVoiceCall()
   * Show main HUD
```

---

## ⚙️ TODO 5.3: SETTINGS MENU

### **WBP_Settings - Tabbed Layout:**

```
Canvas Panel
├── Image_Background
│   Color: Black 90% opacity
│   Blur: 20
│
├── Border (Settings Panel)
│   Anchor: Center
│   Size: 1200 x 800
│   Background: Dark grey gradient
│   Border: 2px white
│   │
│   ├── Vertical Box
│   │   ├── Text_Title
│   │   │   Text: "SETTINGS"
│   │   │   Font Size: 36
│   │   │   Alignment: Center
│   │   │
│   │   ├── Horizontal Box (Tabs)
│   │   │   ├── Button_Tab_Graphics (Active)
│   │   │   ├── Button_Tab_Audio
│   │   │   ├── Button_Tab_Controls
│   │   │   └── Button_Tab_Privacy
│   │   │
│   │   ├── Switcher (Tab Content)
│   │   │   │
│   │   │   ├── Panel_Graphics
│   │   │   │   ├── ComboBox_Quality
│   │   │   │   │   Options: Low, Medium, High, Epic
│   │   │   │   │   Default: High (Snapdragon 888)
│   │   │   │   │
│   │   │   │   ├── Slider_ResolutionScale
│   │   │   │   │   Range: 50% - 100%
│   │   │   │   │   Default: 100%
│   │   │   │   │   Label: "Resolution: {value}%"
│   │   │   │   │
│   │   │   │   ├── Slider_FrameRate
│   │   │   │   │   Range: 30, 60, 120
│   │   │   │   │   Default: 60
│   │   │   │   │   Label: "FPS Limit: {value}"
│   │   │   │   │
│   │   │   │   ├── CheckBox_VSync
│   │   │   │   │   Label: "VSync"
│   │   │   │   │   Default: Off
│   │   │   │   │
│   │   │   │   ├── CheckBox_Bloom
│   │   │   │   │   Label: "Bloom Effect"
│   │   │   │   │   Default: On
│   │   │   │   │
│   │   │   │   ├── CheckBox_MotionBlur
│   │   │   │   │   Label: "Motion Blur"
│   │   │   │   │   Default: Off
│   │   │   │   │
│   │   │   │   └── Text_Warning
│   │   │   │       Text: "⚠ Restart required for some changes"
│   │   │   │       Visible: Only if changes pending
│   │   │   │
│   │   │   ├── Panel_Audio
│   │   │   │   ├── Slider_MasterVolume
│   │   │   │   │   Range: 0-100
│   │   │   │   │   Default: 80
│   │   │   │   │   OnValueChanged: Apply immediately
│   │   │   │   │
│   │   │   │   ├── Slider_VoiceVolume
│   │   │   │   │   Range: 0-100
│   │   │   │   │   Default: 100
│   │   │   │   │   Label: "Najika Voice Volume"
│   │   │   │   │
│   │   │   │   ├── Slider_MusicVolume
│   │   │   │   │   Range: 0-100
│   │   │   │   │   Default: 60
│   │   │   │   │
│   │   │   │   ├── Slider_SFXVolume
│   │   │   │   │   Range: 0-100
│   │   │   │   │   Default: 80
│   │   │   │   │
│   │   │   │   └── Button_TestSound
│   │   │   │       Text: "Test Sound"
│   │   │   │       OnClick: Play test sound at current volume
│   │   │   │
│   │   │   ├── Panel_Controls
│   │   │   │   ├── Slider_JoystickSize
│   │   │   │   │   Range: 100-300
│   │   │   │   │   Default: 200
│   │   │   │   │   Label: "Virtual Joystick Size: {value}"
│   │   │   │   │   Platform: Mobile only
│   │   │   │   │
│   │   │   │   ├── Slider_JoystickOpacity
│   │   │   │   │   Range: 30-100
│   │   │   │   │   Default: 50
│   │   │   │   │   Label: "Joystick Opacity: {value}%"
│   │   │   │   │
│   │   │   │   ├── Slider_CameraSensitivity
│   │   │   │   │   Range: 0.5-2.0
│   │   │   │   │   Default: 1.0
│   │   │   │   │   Label: "Camera Sensitivity: {value}x"
│   │   │   │   │
│   │   │   │   ├── CheckBox_InvertY
│   │   │   │   │   Label: "Invert Y Axis"
│   │   │   │   │   Default: Off
│   │   │   │   │
│   │   │   │   ├── ComboBox_ButtonLayout
│   │   │   │   │   Options: Default, Left-handed, Custom
│   │   │   │   │   Default: Default
│   │   │   │   │
│   │   │   │   └── Button_ResetControls
│   │   │   │       Text: "Reset to Default"
│   │   │   │
│   │   │   └── Panel_Privacy
│   │   │       ├── CheckBox_DataCollection
│   │   │       │   Label: "Allow Anonymous Analytics"
│   │   │       │   Default: Off
│   │   │       │   Description: "Helps improve the game"
│   │   │       │
│   │   │       ├── CheckBox_CrashReports
│   │   │       │   Label: "Send Crash Reports"
│   │   │       │   Default: On
│   │   │       │
│   │   │       ├── Text_Permissions (Android)
│   │   │       │   Text: "Permissions:"
│   │   │       │
│   │   │       ├── CheckBox_Camera
│   │   │       │   Label: "📷 Camera (for Scanner)"
│   │   │       │   OnChanged: Request/Revoke permission
│   │   │       │
│   │   │       ├── CheckBox_Microphone
│   │   │       │   Label: "🎤 Microphone (for Voice Calls)"
│   │   │       │   OnChanged: Request/Revoke permission
│   │   │       │
│   │   │       ├── Button_PrivacyPolicy
│   │   │       │   Text: "View Privacy Policy"
│   │   │       │   OnClick: Open browser
│   │   │       │
│   │   │       ├── Button_DeleteData
│   │   │       │   Text: "Delete All Data"
│   │   │       │   Style: Danger (Red)
│   │   │       │   OnClick: Show confirmation
│   │   │       │
│   │   │       └── Text_DataLocation
│   │   │           Text: "Data stored locally only"
│   │   │           Font Size: 14
│   │   │           Color: Grey
│   │   │
│   │   └── Horizontal Box (Buttons)
│   │       Anchor: Bottom
│   │       ├── Button_Apply
│   │       │   Text: "APPLY"
│   │       │   Enabled: Only if changes made
│   │       │
│   │       ├── Button_Cancel
│   │       │   Text: "CANCEL"
│   │       │
│   │       └── Button_Default
│   │           Text: "RESET TO DEFAULT"
```

### **Settings Logic:**

```
Variables:
- OriginalSettings (Struct): Settings when opened
- CurrentSettings (Struct): Modified settings
- HasChanges (Boolean): Dirty flag

Event Construct:
→ Load settings from save file
→ Store in OriginalSettings
→ Copy to CurrentSettings
→ Apply to UI controls

OnAnyControl_Changed:
→ Update CurrentSettings
→ HasChanges = true
→ Enable Button_Apply

OnButton_Apply_Clicked:
→ Apply settings to game:
   * Graphics: r.SetRes, sg.ViewDistanceQuality, etc.
   * Audio: Set sound mix volumes
   * Controls: Update input sensitivity
   * Privacy: Update permission states
→ Save settings to file
→ OriginalSettings = CurrentSettings
→ HasChanges = false
→ Show notification: "Settings applied!"

OnButton_Cancel_Clicked:
→ If HasChanges:
   * Show confirmation: "Discard changes?"
→ CurrentSettings = OriginalSettings
→ Close widget

OnButton_Default_Clicked:
→ Show confirmation: "Reset all settings to default?"
→ If yes:
   * Load default settings
   * Apply to UI
   * HasChanges = true
```

---

## ✨ TODO 5.4: VISUAL EFFECTS (Niagara)

### **Particle Systems zu erstellen:**

#### **1. PS_LevelUp (Level-Up Effect)**
```
Niagara System: PS_LevelUp
Emitters:
1. Sparkles_Burst
   - Spawn Rate: 200 particles (burst)
   - Lifetime: 1.5s
   - Velocity: Radial outward (100-200)
   - Size: 5-20 (random)
   - Color: Gold gradient
   - Material: M_Particle_Star

2. Light_Flash
   - Spawn: 1 particle
   - Lifetime: 0.5s
   - Size: 500 (sphere)
   - Color: Bright white → Fade
   - Light: Point light (intensity 5000)

3. Ring_Expand
   - Spawn: 3 particles (0, 0.2s, 0.4s)
   - Lifetime: 1.0s
   - Size: 0 → 300 (expand)
   - Color: Gold
   - Material: M_Particle_Ring

Usage:
→ Spawn at character position when level up
→ Play sound: S_LevelUp
→ Camera shake: Light
```

#### **2. PS_Healing (Healing Effect)**
```
Niagara System: PS_Healing
Emitters:
1. Green_Particles
   - Spawn Rate: 50/s
   - Lifetime: 2.0s
   - Velocity: Upward (50-100)
   - Size: 10-30
   - Color: Light green → White
   - Material: M_Particle_Glow

2. Sparkles
   - Spawn Rate: 20/s
   - Lifetime: 1.0s
   - Velocity: Radial
   - Color: White

Usage:
→ Attach to character when healing
→ Duration: 2 seconds
→ Sound: S_Heal
```

#### **3. PS_Damage (Hit Effect)**
```
Niagara System: PS_Damage
Emitters:
1. Red_Flash
   - Spawn: Burst 50
   - Lifetime: 0.5s
   - Velocity: Random
   - Color: Red → Transparent

2. Impact_Sparks
   - Spawn: Burst 20
   - Lifetime: 0.3s
   - Velocity: Outward from hit point
   - Gravity: Enabled

Usage:
→ Spawn at hit location
→ Camera shake: Medium
→ Sound: S_Hit
```

#### **4. PS_Food_Hearts (When feeding Najika)**
```
Niagara System: PS_Food_Hearts
Emitters:
1. Hearts
   - Spawn Rate: 10/s
   - Lifetime: 2.0s
   - Velocity: Upward + Random wobble
   - Size: 20-40
   - Color: Pink
   - Material: M_Heart_Icon
   - Rotation: Spinning

Usage:
→ Spawn above Najika's head when fed
→ Duration: 2 seconds
→ Sound: S_Eating
```

#### **5. PS_Love_Explosion (When praising)**
```
Niagara System: PS_Love_Explosion
Emitters:
1. Heart_Burst
   - Spawn: Burst 20
   - Lifetime: 1.5s
   - Velocity: Radial explosion
   - Size: 30-60
   - Color: Pink → Red
   - Material: M_Heart_Icon

2. Sparkles
   - Spawn: Burst 50
   - Lifetime: 2.0s
   - Color: Pink/White

Usage:
→ Spawn at character when praised
→ Sound: S_Love
→ UI: Flash happiness bar
```

---

## 🎬 TODO 5.5: POST-PROCESSING

### **Post-Process Volume Setup:**

```
Level: L_MainWorld
Actor: PostProcessVolume
Settings:
- Infinite Extent: True (affects whole level)
- Priority: 1

Post Process Settings:

1. Bloom:
   ✅ Enabled: True
   - Intensity: 0.5
   - Threshold: 1.0
   - Size Scale: 4.0
   - Method: Standard

2. Auto Exposure:
   ✅ Enabled: True
   - Method: Manual
   - Exposure Compensation: 0.0
   - Min Brightness: 0.5
   - Max Brightness: 2.0

3. Color Grading:
   ✅ Enabled: True
   - Temperature: +5 (warm)
   - Tint: 0
   - Saturation: 1.1 (slightly saturated)
   - Contrast: 1.05
   - Gamma: (1.0, 1.0, 1.0)
   - Gain: (1.0, 1.0, 1.0)

4. Depth of Field:
   ❌ Disabled (performance)

5. Motion Blur:
   ❌ Disabled (causes nausea)

6. Ambient Occlusion:
   ✅ Enabled: True
   - Intensity: 0.5
   - Radius: 200
   - Quality: Medium

7. Screen Space Reflections:
   ✅ Enabled: True (Mobile supports!)
   - Intensity: 50
   - Quality: Medium

8. Vignette:
   ✅ Enabled: True (subtle)
   - Intensity: 0.3
```

### **Dynamic Post-Process Effects:**

```
Blueprint: BP_PostProcessController

Function: ApplyDamageEffect:
→ Create temporary Post Process Component
→ Set ChromaticAberration: 1.0
→ Set Saturation: 0.5
→ Lerp back to normal over 0.5s
→ Remove component

Function: ApplyLowHealthEffect:
→ If HP < 20%:
   * Set Vignette Intensity: 0.7
   * Set Saturation: 0.7
   * Add red tint
→ Else:
   * Reset to default

Function: ApplyNightVision (Scanner mode):
→ Set Color Grading:
   * Temperature: -20 (cool)
   * Tint: +10 (green)
   * Gain: (1.5, 1.8, 1.2)
→ Increase Bloom intensity
```

---

## 🎵 TODO 5.6: UI SOUND EFFECTS

### **Sound Cues zu erstellen:**

```
Sound Cues Needed:

UI Interactions:
1. SC_Button_Hover
   - Source: Soft click/beep
   - Volume: 30%
   - Pitch: 1.0-1.1 (randomized)

2. SC_Button_Click
   - Source: Satisfying click
   - Volume: 50%
   - Pitch: 0.95-1.05

3. SC_Menu_Open
   - Source: Whoosh + soft bell
   - Volume: 40%

4. SC_Menu_Close
   - Source: Whoosh (reverse)
   - Volume: 40%

Notifications:
5. SC_Notification_Info
   - Source: Gentle chime
   - Volume: 35%

6. SC_Notification_Warning
   - Source: Alert beep
   - Volume: 50%

7. SC_Notification_Error
   - Source: Buzzer
   - Volume: 60%

8. SC_Notification_Success
   - Source: Success jingle
   - Volume: 45%

Najika Actions:
9. SC_Level_Up
   - Source: Victory fanfare (short)
   - Volume: 70%

10. SC_Heart_Pop
    - Source: Cute pop
    - Volume: 40%

11. SC_Eat
    - Source: Nom nom
    - Volume: 50%

12. SC_Wash
    - Source: Water splash
    - Volume: 40%
```

### **Implementation:**

```
Any UI Widget:

Event Construct:
→ Get all buttons
→ For each button:
   * Bind OnHovered → PlaySound(SC_Button_Hover)
   * Bind OnClicked → PlaySound(SC_Button_Click)

Function PlaySound(SoundCue):
→ PlaySound2D(SoundCue)
→ Optional: Haptic feedback (mobile)
```

---

## 📊 SUCCESS CRITERIA

**Phase 5 ist komplett wenn:**

```
✅ Main Menu funktioniert
   - Start/Continue toggle
   - All buttons work
   - Smooth transitions

✅ HUD funktioniert
   - Status bars update real-time
   - Notifications show/dismiss
   - Touch controls responsive
   - Interaction prompts appear

✅ Settings Menu funktioniert
   - All settings save/load
   - Graphics settings apply
   - Audio volumes work
   - Controls customizable
   - Privacy toggles functional

✅ Visual Effects funktionieren
   - Niagara particles spawn correctly
   - Level-up effect plays
   - Healing/Damage effects work
   - Food hearts appear

✅ Post-Processing funktioniert
   - Bloom looks good
   - Color grading applied
   - Dynamic effects (damage, low health)

✅ UI Sounds funktionieren
   - Button clicks have sound
   - Notifications have sound
   - Volume settings respected
```

---

## 🎉 PHASE 5 COMPLETE!

**Nächster Schritt:** Phase 6 - Security & Optimization

**Geschätzte Dauer Phase 5:** 1 Woche

---

**Model 1 - Digivice APK Development**
**Phase:** 5/9 - UI/UX Polish
**Status:** Ready to Execute
