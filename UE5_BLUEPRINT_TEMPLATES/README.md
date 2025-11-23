# UE5 BLUEPRINT TEMPLATES - NAJIKA DIGIVICE
**Model 1 - Digivice APK**
**Created:** 2025-11-11

---

## 📦 BLUEPRINT CLASS TEMPLATES

Diese Blueprint-Templates sind vorbereitet und können direkt in UE5 erstellt werden!

---

## 🎮 CORE BLUEPRINTS

### **BP_NajikaGameMode**
**Parent:** GameModeBase (C++)
**Location:** `Content/Blueprints/Core/`

**Purpose:** Main Game Mode für Najika Digivice

**Variables:**
```
- NajikaAPIClient (Object Reference) - Backend API Client
- WebSocketManager (Object Reference) - WebSocket für Real-time Updates
- VoiceCallManager (Object Reference) - Voice Call System
- CurrentGameState (Enum) - Exploration/Battle/Conversation/Minigame
```

**Functions:**
```
- Event BeginPlay
  → Create API Client
  → Connect WebSocket
  → Initialize Voice System
  → Load Najika State from Backend

- SwitchGameState(NewState)
  → Handle state transitions
  → Update UI
  → Notify backend

- OnBackendDisconnect
  → Show notification
  → Try reconnect
  → Switch to offline mode
```

---

### **BP_NajikaPlayerController**
**Parent:** PlayerController (C++)
**Location:** `Content/Blueprints/Core/`

**Purpose:** Player Controller mit Input Handling

**Variables:**
```
- InputMappingContext (Input Mapping Context)
- CameraManager (Object Reference to BP_NajikaCameraManager)
- CurrentCameraMode (Enum) - Orbit/Third/First
```

**Functions:**
```
- Event BeginPlay
  → Setup Enhanced Input
  → Add Input Mapping Context
  → Initialize Camera Manager

- IA_Move (Input Action)
  → Handle WASD movement
  → Camera-relative direction
  → Move character

- IA_Look (Input Action)
  → Rotate camera (Orbit/Third)
  → Or rotate character (First)

- IA_Jump (Input Action)
  → Character jump

- IA_Interact (Input Action)
  → Raycast from camera
  → Check for interactable objects
  → Call Interact function

- IA_VoiceCall (Input Action)
  → Start/Stop voice call
  → Show voice call UI

- IA_Chat (Input Action)
  → Open chat UI

- IA_Menu (Input Action)
  → Open pause menu

- SwitchCameraMode(Mode)
  → Switch between Orbit/Third/First
  → Smooth transition
```

---

### **BP_NajikaCameraManager**
**Parent:** PlayerCameraManager (C++)
**Location:** `Content/Blueprints/Core/`

**Purpose:** Fortnite-Style Camera System

**Variables:**
```
- CameraMode (Enum) - Orbit/Third/First
- OrbitDistance (Float) - 5-50
- OrbitPitch (Float) - -80 to 80
- OrbitYaw (Float) - 0-360
- ThirdPersonDistance (Float) - 8
- ThirdPersonShoulderOffset (Float) - 1.5
- FirstPersonEyeHeight (Float) - Character Height * 0.9
```

**Functions:**
```
- UpdateCamera (Event Tick)
  → Calculate camera position based on mode
  → Apply camera collision
  → Smooth interpolation

- SetCameraMode(Mode)
  → Switch camera mode
  → Reset parameters

- GetCameraYaw() → Float
  → Return current camera yaw for movement
```

---

### **BP_NajikaCharacter**
**Parent:** Character (C++)
**Location:** `Content/Blueprints/Characters/`

**Purpose:** Najika Character mit Animations

**Components:**
```
- Skeletal Mesh: SK_Najika
- Animation Blueprint: ABP_Najika
- Audio Component: Voice Audio
```

**Variables:**
```
- MovementSpeed (Float) - Base speed
- isSprinting (Boolean)
- isCrouching (Boolean)
- CurrentEmotion (Enum) - Happy/Sad/Angry/Excited
```

**Functions:**
```
- Event BeginPlay
  → Initialize animation blueprint
  → Set default emotion

- UpdateAnimation(DeltaTime)
  → Update animation parameters
  → Speed, Direction, IsJumping, etc.

- PlayEmotion(Emotion)
  → Trigger emotion animation
  → Update facial expression

- PlayVoiceLine(AudioWave)
  → Play TTS audio
  → Sync lip animation
```

---

## 🎨 UI BLUEPRINTS (UMG Widgets)

### **WBP_MainHUD**
**Parent:** UserWidget
**Location:** `Content/UI/Widgets/`

**Purpose:** Main HUD Overlay

**Components:**
```
Canvas Panel (Root)
├── Horizontal Box (Top Bar)
│   ├── WBP_NajikaStatus (Hunger, Energy, Happiness bars)
│   └── Button_VoiceCall
├── Vertical Box (Right Side)
│   ├── Button_Chat
│   ├── Button_Menu
│   └── Button_Interact (conditional)
└── WBP_VirtualJoystick (Mobile only, Bottom Left)
```

**Functions:**
```
- Event Construct
  → Bind to Najika Status updates
  → Setup button callbacks
  → Show/Hide based on platform

- UpdateNajikaStatus(Hunger, Energy, Happiness)
  → Update progress bars
  → Change colors based on values

- OnVoiceCallClicked
  → Start voice call
  → Switch to WBP_VoiceCallUI

- OnChatClicked
  → Open WBP_ChatUI

- OnMenuClicked
  → Open WBP_PauseMenu
```

---

### **WBP_NajikaStatus**
**Parent:** UserWidget
**Location:** `Content/UI/Widgets/`

**Purpose:** Tamagotchi Status Display (Digimon World-Style!)

**Components:**
```
Overlay
├── Image_Background (Semi-transparent)
├── Horizontal Box
│   ├── Vertical Box (Icons)
│   │   ├── Image_Hunger (🍖)
│   │   ├── Image_Energy (⚡)
│   │   └── Image_Happiness (😊)
│   └── Vertical Box (Bars)
│       ├── ProgressBar_Hunger (Red)
│       ├── ProgressBar_Energy (Yellow)
│       └── ProgressBar_Happiness (Pink)
└── Text_Level ("Lv. 5")
```

**Functions:**
```
- SetHunger(Value 0-100)
  → Update progress bar
  → Change color (Red<30, Yellow<70, Green>=70)

- SetEnergy(Value 0-100)
  → Update progress bar
  → Flash if < 20

- SetHappiness(Value 0-100)
  → Update progress bar
  → Show icon (😊 >70, 😐 30-70, 😢 <30)

- SetLevel(Level)
  → Update text

- PlayWarningAnimation
  → Flash red if any value < 20
  → Play warning sound
```

---

### **WBP_ChatUI**
**Parent:** UserWidget
**Location:** `Content/UI/Widgets/`

**Purpose:** Chat Interface

**Components:**
```
Canvas Panel
├── Image_Background
├── ScrollBox_Messages
│   └── [WBP_ChatMessage] (dynamically added)
├── Horizontal Box (Input)
│   ├── EditableTextBox_Input
│   └── Button_Send
└── Button_Close
```

**Functions:**
```
- Event Construct
  → Load chat history from API
  → Bind to OnMessageReceived event

- OnSendClicked
  → Get input text
  → Call NajikaAPIClient->SendChatMessage
  → Add message to scroll box
  → Clear input

- OnMessageReceived(Message, IsUser)
  → Create WBP_ChatMessage widget
  → Add to ScrollBox
  → Scroll to bottom
  → Play TTS if from Najika

- LoadHistory
  → GET /api/chat/history
  → Populate ScrollBox
```

---

### **WBP_VoiceCallUI**
**Parent:** UserWidget
**Location:** `Content/UI/Widgets/`

**Purpose:** Voice Call Interface

**Components:**
```
Overlay
├── Image_Background (Dark overlay)
├── Vertical Box (Center)
│   ├── Text_Status ("Listening..." / "Najika is speaking...")
│   ├── WBP_AudioVisualizer (Waveform)
│   ├── Text_Transcript ("You: Hello Najika!")
│   └── Horizontal Box (Controls)
│       ├── Button_Mute
│       └── Button_EndCall
```

**Functions:**
```
- StartCall
  → VoiceCallManager->StartVoiceCall()
  → Show "Listening..."
  → Start visualizer

- OnSpeechRecognized(Text)
  → Update transcript: "You: [Text]"

- OnNajikaResponse(Audio)
  → Update status: "Najika is speaking..."
  → Play audio
  → Update visualizer

- OnEndCallClicked
  → VoiceCallManager->EndVoiceCall()
  → Close widget
  → Return to MainHUD
```

---

### **WBP_BattleUI**
**Parent:** UserWidget
**Location:** `Content/UI/Widgets/`

**Purpose:** Battle Interface (Turn-based)

**Components:**
```
Canvas Panel
├── Horizontal Box (Top)
│   ├── WBP_HPBar_Player (Left)
│   └── WBP_HPBar_Enemy (Right)
├── Text_TurnIndicator ("Your Turn!")
├── Grid Panel (Skills)
│   ├── Button_Skill1 (Icon + Name)
│   ├── Button_Skill2
│   ├── Button_Skill3
│   └── Button_Skill4
├── Horizontal Box (Actions)
│   ├── Button_Attack
│   ├── Button_Defend
│   ├── Button_Item
│   └── Button_Run
└── Text_BattleLog ("Enemy takes 25 damage!")
```

**Functions:**
```
- StartBattle(EnemyData)
  → Initialize HP bars
  → Load skills from backend
  → Show "Your Turn!"

- OnAttackClicked
  → POST /api/battle/action {"action": "attack"}
  → Play attack animation
  → Update HP bars
  → Check win/lose

- OnSkillClicked(SkillID)
  → POST /api/battle/action {"action": "skill", "skill_id": SkillID}
  → Play skill animation
  → Show damage numbers

- OnBattleEnd(Won)
  → Show victory/defeat screen
  → Give rewards (if won)
  → Return to exploration
```

---

### **WBP_TamagotchiCare**
**Parent:** UserWidget
**Location:** `Content/UI/Widgets/`

**Purpose:** Najika Care Interface (Digimon World!)

**Components:**
```
Canvas Panel
├── Image_Najika (Big character portrait)
├── WBP_NajikaStatus (Full stats display)
├── Grid Panel (Care Actions)
│   ├── Button_Feed (🍖 Icon)
│   ├── Button_Drink (💧 Icon)
│   ├── Button_Wash (🚿 Icon)
│   ├── Button_Sleep (😴 Icon)
│   ├── Button_Train (💪 Icon)
│   └── Button_Praise (👍 Icon)
├── Text_Message ("Najika: Thank you Mr.K! 💜")
└── Button_Close
```

**Functions:**
```
- OnFeedClicked
  → POST /api/najika/feed
  → Play eating animation
  → Update hunger bar
  → Show message bubble

- OnDrinkClicked
  → POST /api/najika/drink
  → Play drinking animation
  → Update energy bar

- OnWashClicked
  → POST /api/najika/wash
  → Play washing animation
  → Update hygiene bar
  → Particle effect (sparkles!)

- OnPraiseClicked
  → POST /api/najika/praise
  → Play happy animation
  → Update happiness bar
  → Show hearts particle effect
```

---

## 🎯 BLUEPRINT CREATION CHECKLIST

Wenn du in UE5 bist, erstelle diese Blueprints:

### **Phase 2 (Core):**
```
- [ ] BP_NajikaGameMode
- [ ] BP_NajikaPlayerController
- [ ] BP_NajikaCameraManager
- [ ] BP_NajikaCharacter
```

### **Phase 3 (Backend Integration):**
```
- [ ] Test Blueprints für API Client
- [ ] Test Blueprints für Voice System
- [ ] Test Blueprints für WebSocket
```

### **Phase 4 (Gameplay):**
```
- [ ] Battle System Blueprints
- [ ] Minigame Blueprints
- [ ] NPC Blueprints
```

### **Phase 5 (UI):**
```
- [ ] WBP_MainHUD
- [ ] WBP_NajikaStatus
- [ ] WBP_ChatUI
- [ ] WBP_VoiceCallUI
- [ ] WBP_BattleUI
- [ ] WBP_TamagotchiCare
- [ ] WBP_PauseMenu
- [ ] WBP_Settings
```

---

## 📝 VERWENDUNG

1. **Öffne UE5 Editor**
2. **Content Browser → Rechtsklick → Blueprint Class**
3. **Wähle Parent Class (siehe oben)**
4. **Name vergeben (siehe oben)**
5. **Öffne Blueprint**
6. **Erstelle Variables/Functions laut Template**
7. **Implement Logic**
8. **Compile & Save**

**ALLE Templates sind vorbereitet - einfach Step-by-Step durcharbeiten!** 🚀

---

**Model 1 - Digivice APK Development**
