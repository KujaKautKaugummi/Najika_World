# 🎨 Blueprint Creation Guide - Complete Workflow

**For Local Model: Step-by-step instructions to create all Blueprints in UE5**

This guide assumes:
- All C++ code has been compiled successfully in Visual Studio
- Visual Studio solution has been reopened after compilation
- UE5 Editor is open with NajikaDigivice.uproject

**Estimated Time:** 2-3 hours

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Core Game Blueprints](#core-game-blueprints)
3. [UI Widget Blueprints](#ui-widget-blueprints)
4. [Project Settings](#project-settings)
5. [Level Setup](#level-setup)
6. [Plugin Activation](#plugin-activation)
7. [Testing Checklist](#testing-checklist)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### ✅ Before You Start

**Must be completed:**
- [x] All C++ code compiled without errors
- [x] Visual Studio solution reopened after compile
- [x] UE5 Editor opened with Najika Digivice.uproject
- [x] No errors in Output Log on editor startup

**Verify C++ Classes Available:**

1. Open Content Browser
2. Click "View Options" (eye icon)
3. Enable: "Show C++ Classes"
4. Navigate to folder: `NajikaDigivice C++ Classes`

**You should see:**
- NajikaCharacter
- NajikaPlayerController
- NajikaGameMode
- NajikaGameState
- NajikaPlayerState
- NajikaHUDWidget
- NajikaChatWidget
- NajikaStatusWidget
- NajikaMenuWidget
- NajikaInventoryWidget

**If any are missing:**
→ Go back to Visual Studio Compilation Guide
→ Ensure all modules compiled successfully
→ Restart UE5 Editor

---

## 1️⃣ Core Game Blueprints

Create these Blueprints in order, as later Blueprints depend on earlier ones.

---

### 1.1 BP_NajikaCharacter

**Purpose:** Player-controlled character with movement, animation, and interaction

**Path:** `Content/Blueprints/Characters/BP_NajikaCharacter`

**Steps:**

1. **Create Blueprint Class**
   - Right-click in Content Browser → Blueprint Class
   - In "Pick Parent Class" window:
     - Expand "All Classes"
     - Search: "NajikaCharacter"
     - Select: `NajikaCharacter` (C++ class)
     - Click "Select"

2. **Name the Blueprint**
   - Name: `BP_NajikaCharacter`
   - Save to: `Content/Blueprints/Characters/`

3. **Open Blueprint**
   - Double-click `BP_NajikaCharacter` to open Blueprint Editor

4. **Components Tab Setup**

   **Add Camera Components:**

   a. Add Spring Arm:
   - Click "Add Component" → Search "Spring Arm"
   - Name: `CameraSpringArm`
   - Location (X, Y, Z): `(0, 0, 60)`
   - Rotation: `(0, 0, 0)`

   **Details Panel Settings for Spring Arm:**
   - Target Arm Length: `300.0`
   - Socket Offset (Z): `50.0`
   - Use Pawn Control Rotation: ✅ TRUE
   - Enable Camera Lag: ✅ TRUE
   - Camera Lag Speed: `10.0`
   - Enable Camera Rotation Lag: ✅ TRUE
   - Camera Rotation Lag Speed: `10.0`

   b. Add Camera:
   - Select `CameraSpringArm` in Components list
   - Click "Add Component" → Search "Camera"
   - This attaches camera to spring arm
   - Name: `FollowCamera`
   - Location: `(0, 0, 0)` (relative to spring arm)
   - Field of View: `90.0`

5. **Character Movement Component Settings**

   - In Components panel, select: `CharacterMovement (Inherited)`

   **Movement Settings (Details Panel):**
   - Max Walk Speed: `600.0`
   - Max Walk Speed Crouched: `300.0`
   - Jump Z Velocity: `500.0`
   - Air Control: `0.3`
   - Ground Friction: `8.0`
   - Braking Deceleration Walking: `2000.0`
   - Braking Deceleration Falling: `1000.0`
   - Braking Deceleration Flying: `3000.0`

   **Advanced:**
   - Can Walk Off Ledges: ✅ TRUE
   - Can Walk Off Ledges When Crouching: ✅ TRUE
   - Use Flat Base for Floor Checks: ✅ TRUE

6. **Capsule Component Settings**

   - Select: `CapsuleComponent (Inherited)`
   - Capsule Half Height: `88.0`
   - Capsule Radius: `34.0`

7. **Mesh Component Settings**

   - Select: `Mesh (Inherited)`
   - Location (Z): `-88.0` (offset to ground)
   - Rotation (Z): `-90.0` (face forward)

   **Skeletal Mesh:**
   - Skeletal Mesh: (Leave empty for now - placeholder OK)
   - Animation Mode: `Use Animation Blueprint`
   - Anim Class: (Leave empty for now - placeholder OK)

8. **Event Graph Setup**

   **Event BeginPlay:**
   ```
   Event BeginPlay
   → Call Parent: Begin Play (right-click → Add call to parent function)
   → Print String (for testing)
     - In String: "Najika Character Spawned"
     - Text Color: Green
     - Duration: 3.0
   ```

   **Event Tick (Optional - for testing):**
   ```
   Event Tick
   → (Leave empty for now)
   ```

9. **Class Defaults**

   - Click "Class Defaults" button (in toolbar)
   - **Pawn:**
     - Auto Possess Player: `Player 0` (for single-player)
     - Base Eye Height: `64.0`

10. **Compile & Save**
    - Click "Compile" button (green checkmark)
    - Wait for compilation
    - If errors appear → fix them
    - Click "Save" button
    - Close Blueprint Editor

**✅ Success Criteria:**
- Blueprint compiles without errors
- Green checkmark appears
- Can see "Najika Character Spawned" message in later testing

**Screenshot Placeholder:** `[BP_NajikaCharacter_Components.png]`
**Screenshot Placeholder:** `[BP_NajikaCharacter_EventGraph.png]`

---

### 1.2 BP_NajikaPlayerController

**Purpose:** Handles player input and UI management

**Path:** `Content/Blueprints/Core/BP_NajikaPlayerController`

**Steps:**

1. **Create Blueprint Class**
   - Right-click in Content Browser → Blueprint Class
   - Search parent: "NajikaPlayerController"
   - Select: `NajikaPlayerController` (C++ class)
   - Name: `BP_NajikaPlayerController`
   - Save to: `Content/Blueprints/Core/`

2. **Open Blueprint**
   - Double-click to open

3. **Event Graph Setup**

   **Event BeginPlay:**
   ```
   Event BeginPlay
   → Call Parent: Begin Play
   → Get Controlled Pawn
     → Cast to BP_NajikaCharacter
       → Promote to Variable: "ControlledNajika"
       → Print String: "Player Controller Initialized"
   ```

4. **Input Setup (Class Defaults)**

   - Click "Class Defaults"
   - **Mouse Interface:**
     - Show Mouse Cursor: ✅ TRUE
     - Enable Click Events: ✅ TRUE
     - Enable Touch Events: ✅ TRUE
     - Default Mouse Cursor: `Hand`

   - **Input:**
     - Enable Touch Over UI: ✅ FALSE (prevent UI blocking 3D interaction)

5. **Functions (Optional - for later use)**

   Create custom function: `ShowMenu`
   - Add Function (plus icon in Functions panel)
   - Name: `ShowMenu`
   - Inputs: None
   - Outputs: None
   - Implementation:
     ```
     Set Input Mode UI Only
     → Show Mouse Cursor: TRUE
     ```

   Create custom function: `ShowGameplay`
   - Name: `ShowGameplay`
   - Implementation:
     ```
     Set Input Mode Game Only
     → Show Mouse Cursor: FALSE
     ```

6. **Compile & Save**
   - Compile
   - Save
   - Close

**✅ Success Criteria:**
- Blueprint compiles without errors
- ControlledNajika variable is set correctly

**Screenshot Placeholder:** `[BP_NajikaPlayerController_EventGraph.png]`

---

### 1.3 BP_NajikaGameMode

**Purpose:** Core game rules and class assignments

**Path:** `Content/Blueprints/Core/BP_NajikaGameMode`

**Steps:**

1. **Create Blueprint Class**
   - Parent: `NajikaGameMode` (C++ class)
   - Name: `BP_NajikaGameMode`
   - Location: `Content/Blueprints/Core/`

2. **Open Blueprint**

3. **Class Defaults Settings**

   - Click "Class Defaults"

   **Classes (IMPORTANT!):**
   - Default Pawn Class: `BP_NajikaCharacter` (select from dropdown)
   - Player Controller Class: `BP_NajikaPlayerController`
   - Game State Class: `NajikaGameState` (C++ class - no BP needed)
   - Player State Class: `NajikaPlayerState` (C++ class - no BP needed)
   - HUD Class: (Leave `None` - we use Widgets instead)
   - Spectator Class: (Leave default)
   - Replay Spectator Player Controller Class: (Leave default)

   **Game:**
   - Game Session Class: (Leave default)
   - Server Stat Replicator Class: (Leave default)

4. **Event Graph (Optional)**

   **Event BeginPlay:**
   ```
   Event BeginPlay
   → Call Parent: Begin Play
   → Print String: "Game Mode Started - Najika Digivice"
     - Text Color: Cyan
     - Duration: 5.0
   ```

   **Event PostLogin (Optional - for player spawn):**
   ```
   Event PostLogin
   → New Player (parameter)
   → Print String: "Player Joined"
   ```

5. **Compile & Save**

**✅ Success Criteria:**
- All class assignments correct
- Blueprint compiles
- Game Mode shows in World Settings later

**Screenshot Placeholder:** `[BP_NajikaGameMode_ClassDefaults.png]`

---

## 2️⃣ UI Widget Blueprints

Create all 5 UI widgets. These are UMG (Unreal Motion Graphics) Blueprints.

**General Workflow for Widgets:**
1. Create Widget Blueprint
2. Design visual layout in Designer tab
3. Add bindings in Graph tab
4. Compile & Save

---

### 2.1 WBP_NajikaHUD

**Purpose:** Main HUD overlay displayed during gameplay

**Path:** `Content/UI/Widgets/WBP_NajikaHUD`

**Steps:**

1. **Create Widget Blueprint**
   - Right-click in Content Browser → User Interface → Widget Blueprint
   - Name: `WBP_NajikaHUD`
   - Save to: `Content/UI/Widgets/`

2. **Open Widget Designer**
   - Double-click to open
   - You see: Designer tab (visual editor) + Graph tab (logic)

3. **Designer Layout**

   **Root:** Canvas Panel (already exists)

   **Top Bar (Health, Level, etc.):**

   a. Add Horizontal Box:
   - Drag "Horizontal Box" from Palette (left panel) onto Canvas
   - Rename: `TopBar`
   - Anchors: Top Stretch (click Anchor button → select top row, middle icon)
   - Position: X=0, Y=0
   - Size: X=Screen Width, Y=60
   - Alignment: X=0.5, Y=0.0

   b. Add Health Bar (inside TopBar):
   - Drag "Progress Bar" into TopBar Horizontal Box
   - Rename: `HealthBar` (IMPORTANT: exact name for C++ binding)
   - Size To Content: ❌ FALSE
   - Fill: `300 x 30`
   - Percent: `1.0` (100% for preview)
   - Fill Color and Opacity: `Red (R=1.0, G=0.0, B=0.0, A=1.0)`
   - Background Color: `Dark Red (R=0.3, G=0.0, B=0.0, A=0.8)`
   - Padding: Left=10, Right=5

   c. Add Spacer:
   - Drag "Spacer" into TopBar
   - Size: `50 x 1` (acts as horizontal spacing)

   d. Add Mana Bar:
   - Drag "Progress Bar" into TopBar
   - Rename: `ManaBar`
   - Size: `300 x 30`
   - Fill Color: `Blue (R=0.0, G=0.5, B=1.0, A=1.0)`
   - Background Color: `Dark Blue (R=0.0, G=0.0, B=0.3, A=0.8)`

   e. Add Spacer:
   - Spacer: `50 x 1`

   f. Add Level Text:
   - Drag "Text Block" into TopBar
   - Rename: `LevelText`
   - Text: "Level 1" (placeholder)
   - Font: Roboto, Size 24, Bold
   - Color: `White`
   - Justification: Center
   - Padding: `10` all sides

   **Center Crosshair:**

   a. Add Image:
   - Drag "Image" onto Canvas (outside TopBar)
   - Rename: `Crosshair`
   - Anchors: Center
   - Position: X=0, Y=0 (centered)
   - Size: `32 x 32`
   - Image: (Leave empty for now - placeholder)
   - Color: `White with Alpha 0.7`
   - Visibility: `Hidden` initially (show in combat)

   **Bottom Bar (Buttons):**

   a. Add Horizontal Box:
   - Rename: `BottomBar`
   - Anchors: Bottom Stretch
   - Position: X=0, Y=-60 (60 pixels from bottom)
   - Size: X=Screen Width, Y=60
   - Alignment: X=0.5, Y=1.0

   b. Add Menu Button:
   - Drag "Button" into BottomBar
   - Rename: `MenuButton`
   - Size: `120 x 50`
   - Style → Normal: Dark Gray
   - Style → Hovered: Gray
   - Style → Pressed: Light Gray

   c. Add Text to Button:
   - Drag "Text Block" onto MenuButton
   - Text: "Menu"
   - Font: Size 18
   - Justification: Center

   d. Add Spacer (Fill):
   - Spacer with Size Rule: `Fill`
   - This pushes buttons apart

   e. Add Chat Button:
   - Button: `ChatButton`
   - Size: `120 x 50`
   - Text: "Chat"
   - (Repeat styling from Menu Button)

   f. Add Spacer (Fill)

   g. Add Inventory Button:
   - Button: `InventoryButton`
   - Size: `120 x 50`
   - Text: "Bag"

4. **Graph Tab - Bindings & Logic**

   Switch to "Graph" tab.

   **Binding Functions (for C++):**

   a. Bind Health Bar Percent:
   - In Designer, select `HealthBar`
   - In Details panel, find "Percent"
   - Click "Bind" → Create Binding → Name: `GetHealthPercent`
   - This creates a function in Graph
   - Implementation:
     ```
     Return Node
     → Return Value: 0.75 (placeholder - will be replaced by C++)
     ```

   (NOTE: In C++, NajikaHUDWidget will override this)

   b. Bind Level Text:
   - Select `LevelText`
   - Bind "Text" property → Create Binding: `GetLevelText`
   - Return: `Return Value (Text): "Level 1"` (placeholder)

   **Button Click Events:**

   a. Menu Button:
   - Select `MenuButton` in Hierarchy
   - In Details → Events → Click "OnClicked"
   - This creates event in Graph
   - Implementation:
     ```
     OnClicked (MenuButton)
     → Print String: "Menu Clicked" (for testing)
     → (Later: Call C++ function OnMenuButtonClicked)
     ```

   b. Chat Button:
   - OnClicked → Print String: "Chat Clicked"

   c. Inventory Button:
   - OnClicked → Print String: "Inventory Clicked"

   **Event Construct (Initialization):**
   ```
   Event Construct
   → Print String: "HUD Initialized"
   ```

5. **Compile & Save**
   - Click Compile
   - Fix any errors
   - Save

**✅ Success Criteria:**
- All widgets visible in preview
- Bindings created (show in Graph)
- Button clicks print to log
- No compilation errors

**Screenshot Placeholder:** `[WBP_NajikaHUD_Designer.png]`
**Screenshot Placeholder:** `[WBP_NajikaHUD_Graph.png]`

---

### 2.2 WBP_NajikaMenu

**Purpose:** Pause menu with settings and logout

**Path:** `Content/UI/Widgets/WBP_NajikaMenu`

**Steps:**

1. **Create Widget Blueprint**
   - User Interface → Widget Blueprint
   - Name: `WBP_NajikaMenu`
   - Location: `Content/UI/Widgets/`

2. **Designer Layout**

   **Root:** Canvas Panel

   **Background Overlay:**
   - Add "Image" to Canvas
   - Rename: `Background`
   - Anchors: Fill Screen (stretch all)
   - Offset: `0, 0, 0, 0`
   - Color: `Black`
   - Opacity (A): `0.7` (semi-transparent)

   **Center Menu Panel:**
   - Add "Vertical Box" to Canvas
   - Rename: `MenuPanel`
   - Anchors: Center
   - Alignment: X=0.5, Y=0.5
   - Position: X=0, Y=0
   - Size: `400 x 600`

   **Title:**
   - Add "Text Block" into MenuPanel
   - Text: "Najika Menu"
   - Font: Size 48, Bold
   - Justification: Center
   - Color: `White`

   **Spacer:**
   - Height: `30`

   **Resume Button:**
   - Add "Button" into MenuPanel
   - Rename: `ResumeButton`
   - Size: `300 x 60`
   - Add Text: "Resume"

   **Spacer:** 20px

   **Settings Button:**
   - Button: `SettingsButton`
   - Size: `300 x 60`
   - Text: "Settings"

   **Spacer:** 20px

   **Logout Button:**
   - Button: `LogoutButton`
   - Size: `300 x 60`
   - Text: "Logout"

   **Spacer:** 20px

   **Exit Button:**
   - Button: `ExitButton`
   - Size: `300 x 60`
   - Text: "Exit Game"

3. **Graph - Button Logic**

   **Resume Button OnClicked:**
   ```
   OnClicked (ResumeButton)
   → Remove from Parent (removes this widget)
   → Get Player Controller
     → Set Input Mode Game Only
     → Set Show Mouse Cursor: FALSE
   ```

   **Settings Button OnClicked:**
   ```
   OnClicked (SettingsButton)
   → Print String: "Settings not implemented yet"
   ```

   **Logout Button OnClicked:**
   ```
   OnClicked (LogoutButton)
   → Print String: "Logout - TODO: Call C++ Backend Logout"
   ```

   **Exit Button OnClicked:**
   ```
   OnClicked (ExitButton)
   → Quit Game
   ```

4. **Compile & Save**

**✅ Success Criteria:**
- Menu appears centered
- Resume closes menu
- Exit quits game

**Screenshot Placeholder:** `[WBP_NajikaMenu_Designer.png]`

---

### 2.3 WBP_NajikaInventory

**Purpose:** Grid-based inventory for items

**Path:** `Content/UI/Widgets/WBP_NajikaInventory`

**Steps:**

1. **Create Widget Blueprint**
   - Name: `WBP_NajikaInventory`
   - Location: `Content/UI/Widgets/`

2. **Designer Layout**

   **Root:** Canvas Panel

   **Background Panel:**
   - Add "Image"
   - Anchors: Center
   - Size: `800 x 600`
   - Color: `Dark Gray (R=0.2, G=0.2, B=0.2, A=0.95)`

   **Header (Horizontal Box):**
   - Add inside Image (or use Overlay)
   - Contains:
     a. Title Text: "Inventory"
     b. Close Button (X) - top right

   **Inventory Grid:**
   - Add "Uniform Grid Panel"
   - Rename: `InventoryGrid`
   - Slot Padding: `5`
   - Min Desired Slot Width: `80`
   - Min Desired Slot Height: `80`

   **Generate Slots (Do this in Graph):**
   - We'll create 30 slots (6 columns x 5 rows) in Event Construct

   **Footer (Gold, Weight):**
   - Horizontal Box at bottom
   - Text: "Gold: 0" (binding: GetGoldText)
   - Text: "Weight: 0/100" (binding: GetWeightText)

3. **Graph - Slot Generation**

   **Event Construct:**
   ```
   Event Construct
   → For Loop (0 to 29 - for 30 slots)
     → Create Widget: WBP_InventorySlot (we'll create this next)
       → Add Child to Uniform Grid Panel (InventoryGrid)
         - Column: Loop Index % 6 (modulo for wrapping)
         - Row: Loop Index / 6 (integer division)
   ```

   **Binding: GetGoldText:**
   ```
   Return: "Gold: 0" (placeholder - C++ will update)
   ```

   **Binding: GetWeightText:**
   ```
   Return: "Weight: 0/100"
   ```

4. **Create WBP_InventorySlot (Sub-Widget)**

   **New Widget:** `WBP_InventorySlot`
   - Designer:
     - Button (80x80)
     - Image inside (item icon)
     - Text (item count)
   - Graph:
     - OnClicked → Print "Slot Clicked"

5. **Compile & Save**

**✅ Success Criteria:**
- 30 slots visible in grid (6x5)
- Slots clickable
- Gold/Weight text visible

**Screenshot Placeholder:** `[WBP_NajikaInventory_Designer.png]`

---

### 2.4 WBP_NajikaChat

**Purpose:** Chat interface with message history

**Path:** `Content/UI/Widgets/WBP_NajikaChat`

**Steps:**

1. **Create Widget Blueprint**
   - Name: `WBP_NajikaChat`
   - Location: `Content/UI/Widgets/`

2. **Designer Layout**

   **Root:** Vertical Box

   **Chat History (Scroll Box):**
   - Add "Scroll Box"
   - Rename: `ChatHistory`
   - Size: `400 x 300`
   - Auto Scroll: ✅ TRUE
   - Scroll Bar Visibility: `Visible When Needed`

   **Input Row (Horizontal Box):**
   - Add "Horizontal Box"

   Components inside:
   a. Chat Input:
   - "Editable Text"
   - Rename: `ChatInput`
   - Hint Text: "Type message..."
   - Size: Fill

   b. Send Button:
   - "Button"
   - Text: "Send"
   - Size: `60 x 30`

3. **Graph - Chat Logic**

   **OnTextCommitted (ChatInput):**
   ```
   OnTextCommitted (ChatInput)
   → Branch (Commit Method == OnEnter?)
     TRUE:
       → Get Text (ChatInput)
       → Print String: [Concatenate: "Chat: " + Text]
       → Set Text (ChatInput): "" (clear input)
       → TODO: Send to C++ Backend
   ```

   **OnClicked (Send Button):**
   ```
   Same logic as OnTextCommitted
   ```

4. **Compile & Save**

**✅ Success Criteria:**
- Can type in chat input
- Enter key sends message
- Send button works
- Input clears after send

**Screenshot Placeholder:** `[WBP_NajikaChat_Designer.png]`

---

### 2.5 WBP_NajikaStatus

**Purpose:** Detailed character status screen

**Path:** `Content/UI/Widgets/WBP_NajikaStatus`

**Steps:**

1. **Create Widget Blueprint**
   - Name: `WBP_NajikaStatus`
   - Location: `Content/UI/Widgets/`

2. **Designer Layout**

   **Structure:**
   - Background Image (800x600, centered)
   - Vertical Box inside:
     a. Character Name (Text Block, Large Font)
     b. Level Progress Bar
     c. Stats Vertical Box:
        - HP: [Binding]
        - MP: [Binding]
        - Stamina: [Binding]
        - Speed: [Binding]
        - (22 total stats from C++ NajikaPlayerState)
     d. Equipment Section (TODO)

3. **Graph - Bindings**

   **GetCharacterName:**
   ```
   Return: "Najika" (placeholder)
   ```

   **GetHealthText:**
   ```
   Return: "HP: 100/100"
   ```

   *... (Repeat for all stats)*

4. **Compile & Save**

**✅ Success Criteria:**
- All stats visible
- Bindings work
- Layout clear and readable

**Screenshot Placeholder:** `[WBP_NajikaStatus_Designer.png]`

---

## 3️⃣ Project Settings Configuration

**Critical:** These settings MUST be configured for the game to work correctly.

---

### 3.1 Maps & Modes

**Path:** Edit → Project Settings → Maps & Modes

**Settings:**

1. **Default Modes:**
   - Default GameMode: `BP_NajikaGameMode` ✅
   - Global Default Server Game Mode: `BP_NajikaGameMode`

2. **Default Maps:**
   - Editor Startup Map: `MainLevel` (we'll create this next)
   - Game Default Map: `MainLevel`
   - Transition Map: (Leave empty)
   - Server Default Map: `MainLevel`

3. **Local Multiplayer:**
   - Number of Player Splits: `1`

**Screenshot Placeholder:** `[ProjectSettings_MapsAndModes.png]`

---

### 3.2 Input Settings

**Path:** Edit → Project Settings → Engine → Input

**Action Mappings:**

Click "+" next to "Action Mappings" to add each:

```
Jump
  - Keyboard: Space Bar
  - Gamepad: Face Button Bottom (A/Cross)

Interact
  - Keyboard: E
  - Gamepad: Face Button Left (X/Square)

Menu
  - Keyboard: Escape
  - Gamepad: Special Right (Start/Options)

Inventory
  - Keyboard: I
  - Gamepad: Face Button Top (Y/Triangle)

Chat
  - Keyboard: Enter
  - Gamepad: D-Pad Down

PushToTalk
  - Keyboard: V
  - Gamepad: Left Shoulder (L1/LB)
```

**Axis Mappings:**

```
MoveForward
  - Keyboard: W (Scale: 1.0)
  - Keyboard: S (Scale: -1.0)
  - Gamepad: Left Thumbstick Up/Down

MoveRight
  - Keyboard: D (Scale: 1.0)
  - Keyboard: A (Scale: -1.0)
  - Gamepad: Left Thumbstick Right/Left

Turn
  - Mouse: Mouse X (Scale: 1.0)
  - Gamepad: Right Thumbstick Right/Left (Scale: 1.0)

LookUp
  - Mouse: Mouse Y (Scale: -1.0)
  - Gamepad: Right Thumbstick Up/Down (Scale: -1.0)
```

**Additional Settings:**
- Consume Input: ✅ TRUE (for all)

**Screenshot Placeholder:** `[ProjectSettings_Input_Actions.png]`
**Screenshot Placeholder:** `[ProjectSettings_Input_Axis.png]`

---

### 3.3 Android Settings

**Path:** Project Settings → Platforms → Android

**(Important for Mobile Build)**

**APK Packaging:**
- Package Name: `com.najika.digivice`
- Version Code: `1`
- Version Display Name: `1.0.0`
- Minimum SDK Version: `29` (Android 10)
- Target SDK Version: `34` (Android 14)
- Install Location: `Auto`

**Build:**
- ✅ Build for ARM64 (64-bit)
- ❌ Build for ARMv7 (32-bit - disabled)
- ❌ Build for x86-64 (disabled)

**Rendering:**
- ✅ Support OpenGL ES3.1
- ✅ Support Vulkan
- ✅ Support Vulkan Desktop
- Texture Format: `ASTC` + `ETC2` (multi-target)

**Advanced:**
- ✅ Use Gradle instead of Ant
- ✅ Package game data inside APK
- ❌ Enable FullScreen (disable for status bar)
- ✅ Enable bundle (.aab) support

**Permissions:**

Extra Permissions (comma-separated):
```
android.permission.INTERNET
android.permission.ACCESS_NETWORK_STATE
android.permission.WAKE_LOCK
android.permission.VIBRATE
android.permission.RECORD_AUDIO
android.permission.MODIFY_AUDIO_SETTINGS
```

**Screenshot Placeholder:** `[ProjectSettings_Android_Packaging.png]`
**Screenshot Placeholder:** `[ProjectSettings_Android_Build.png]`

---

## 4️⃣ Level Setup

Create the main gameplay level.

---

### 4.1 Create MainLevel

**Steps:**

1. **New Level**
   - File → New Level
   - Select: "Empty Level" (clean slate)

2. **Add Essential Actors**

   a. **Player Start:**
   - Place Actors → Basic → Player Start
   - Drag into level
   - Position: `(0, 0, 100)` (slightly above ground)
   - Rotation: `(0, 0, 0)`

   b. **Directional Light (Sun):**
   - Place Actors → Lights → Directional Light
   - Position: `(0, 0, 500)`
   - Rotation: `(-45, 0, 0)` (45° downward)
   - Intensity: `3.0`
   - Light Color: Warm White
   - ✅ Atmosphere Sun Light

   c. **Sky Light:**
   - Lights → Sky Light
   - Intensity: `1.0`
   - Source Type: `Captured Scene`
   - ✅ Real Time Capture

   d. **Sky Atmosphere:**
   - Visual Effects → Sky Atmosphere
   - (Use default settings)

   e. **Post Process Volume:**
   - Visual Effects → Post Process Volume
   - **IMPORTANT:** In Details → check "Infinite Extent (Unbound)" ✅
   - Exposure: Auto Exposure
   - Bloom: Enabled (Intensity: 0.5)

   f. **Landscape (or Floor):**

   Option A - Landscape (Proper):
   - Landscape → Landscape Mode → Create New
   - Section Size: 63x63
   - Sections Per Component: 1
   - Number of Components: 8x8
   - Overall Resolution: 2017x2017
   - Click "Create"
   - Creates large terrain

   Option B - Simple Floor (Quick Testing):
   - Place Actors → Basic → Cube
   - Scale: `(100, 100, 1)` (large flat plane)
   - Position: `(0, 0, 0)`
   - Material: (Gray placeholder OK)

   g. **Fog (Optional):**
   - Visual Effects → Exponential Height Fog
   - Fog Density: `0.02`
   - Fog Height Falloff: `0.2`

3. **World Settings**

   - Window → World Settings
   - **Game Mode:**
     - GameMode Override: `BP_NajikaGameMode` ✅ (CRITICAL!)
   - **Rendering:**
     - Default Reverberation Send: (Leave default)

4. **Lighting Build Settings**

   - Build → Build Options → Lighting Quality: `Production`
   - Build → Build Options → Build Lighting Only: ✅
   - Click "Build" → Wait for completion (5-10 min)

5. **Save Level**
   - File → Save Current Level As...
   - Name: `MainLevel`
   - Location: `Content/Maps/MainLevel`
   - Click Save

**Screenshot Placeholder:** `[MainLevel_Overview.png]`
**Screenshot Placeholder:** `[MainLevel_WorldSettings.png]`

---

### 4.2 Level Blueprint

Add HUD spawning logic to the level.

**Steps:**

1. **Open Level Blueprint**
   - Blueprints → Open Level Blueprint

2. **Event BeginPlay Logic**

   ```
   Event BeginPlay
   → Get Player Controller (Index 0)
     → Cast To: BP_NajikaPlayerController
       → Create Widget: WBP_NajikaHUD
         → Add to Viewport (Z-Order: 0)
         → Promote to Variable: "MainHUDRef"
   → Print String: "MainLevel Loaded"
   ```

3. **Optional: Input for Menu**

   ```
   Event: M (Keyboard)
   → Create Widget: WBP_NajikaMenu
     → Add to Viewport (Z-Order: 10)
   → Get Player Controller
     → Set Input Mode UI Only
     → Set Show Mouse Cursor: TRUE
   ```

4. **Compile & Save**
   - Compile
   - Save Level Blueprint
   - Close

**Screenshot Placeholder:** `[LevelBlueprint_BeginPlay.png]`

---

## 5️⃣ Plugin Activation

Ensure all plugins are enabled.

**Path:** Edit → Plugins

**Search and Enable:**

1. **NajikaBackendClient** ✅
   - Location: Project Plugins
   - Status: Enabled
   - Description: "Backend API Integration"

2. **NajikaVoiceSystem** ✅
   - Location: Project Plugins
   - Status: Enabled
   - Description: "Voice Chat with Whisper AI"

3. **Online Subsystem** ✅
   - Built-in Engine plugin
   - Required for networking

4. **HTTP** ✅
   - Built-in
   - Required for backend communication

5. **JSON** ✅
   - Built-in

6. **WebSockets** ✅
   - Built-in

**After Enabling:**
- Click "Restart Now" button
- Editor will close and reopen
- Wait for shader compilation (5-10 min)

**Screenshot Placeholder:** `[Plugins_ProjectPlugins.png]`

---

## 6️⃣ Testing Checklist

**Test in-editor before building APK.**

### In-Editor Play Testing

1. **Press Play (Alt+P)**
   - Level loads → ✅
   - Character spawns at Player Start → ✅
   - Camera follows character → ✅

2. **Movement Testing**
   - WASD keys move character → ✅
   - Mouse look rotates camera → ✅
   - Space bar jumps → ✅
   - Movement is smooth, no stuttering → ✅

3. **HUD Testing**
   - HUD visible on screen → ✅
   - Health bar shows (red) → ✅
   - Mana bar shows (blue) → ✅
   - Level text shows "Level 1" → ✅
   - Menu button visible → ✅
   - Chat button visible → ✅
   - Inventory button visible → ✅

4. **Button Testing**
   - Click Menu button → Prints "Menu Clicked" → ✅
   - Click Chat button → Prints "Chat Clicked" → ✅
   - Click Inventory button → Prints "Inventory Clicked" → ✅

5. **Keyboard Shortcuts**
   - Press Escape → (Menu opens when implemented) → ✅
   - Press I → (Inventory opens when implemented) → ✅
   - Press Enter → (Chat opens when implemented) → ✅

### Backend Connection Testing

**(Requires backend server running on localhost:8000)**

1. **Start Backend Server**
   ```powershell
   cd C:\Najika_World\backend
   python najika_server.py
   ```

2. **Check Output Log**
   - Play in editor
   - Window → Developer Tools → Output Log
   - Look for: "Backend Connected" or similar
   - If error → Check backend URL in code

3. **Test API Call**
   - (Implement test button in HUD)
   - Click button → Sends GET request
   - Check Output Log for response

### Mobile Preview

**(Test mobile rendering)**

1. **Enable Mobile Preview**
   - Settings → Preview Rendering Level → Android ES 3.1
   - Restart Editor

2. **Mobile Previewer**
   - Window → Mobile Previewer
   - Select: Xiaomi 11T Pro (or similar Android device)
   - Press Play

3. **Check:**
   - Graphics render correctly → ✅
   - UI scales to mobile resolution → ✅
   - Touch controls work (if implemented) → ✅
   - Performance: >30 FPS → ✅

**Screenshot Placeholder:** `[Testing_InEditor_Play.png]`
**Screenshot Placeholder:** `[Testing_MobilePreview.png]`

---

## 7️⃣ Completion Criteria

**All Blueprints Created:** 9 Blueprints

- ✅ BP_NajikaCharacter
- ✅ BP_NajikaPlayerController
- ✅ BP_NajikaGameMode
- ✅ WBP_NajikaHUD
- ✅ WBP_NajikaMenu
- ✅ WBP_NajikaInventory
- ✅ WBP_NajikaChat
- ✅ WBP_NajikaStatus
- ✅ MainLevel (Map)

**All Settings Configured:**
- ✅ Maps & Modes (GameMode set)
- ✅ Input (Actions and Axis)
- ✅ Android (Packaging settings)

**All Plugins Enabled:**
- ✅ NajikaBackendClient
- ✅ NajikaVoiceSystem
- ✅ Engine plugins (HTTP, JSON, WebSockets)

**Testing Complete:**
- ✅ In-editor play works
- ✅ Movement works (WASD)
- ✅ HUD displays
- ✅ Buttons clickable
- ✅ No critical errors in Output Log

---

## 8️⃣ Troubleshooting

### Issue: Blueprint won't compile

**Symptoms:** Red X icon, errors in Compiler Results

**Solutions:**
1. Check all variable types are correct
2. Ensure all node connections are valid
3. Look for red node outlines (broken connections)
4. Check Output Log for specific error message
5. Right-click blueprint in Content Browser → Refresh
6. Restart UE5 Editor

---

### Issue: C++ class not showing as parent option

**Symptoms:** NajikaCharacter not in parent class list

**Solutions:**
1. Verify C++ code compiled successfully in Visual Studio
2. Check for compilation errors in VS Output window
3. Close UE5 Editor
4. Rebuild solution in Visual Studio
5. Reopen UE5 Editor
6. Wait for shaders to compile
7. Try again

---

### Issue: HUD not appearing in game

**Symptoms:** Play in editor, no HUD visible

**Solutions:**
1. Check Level Blueprint has Create Widget logic
2. Verify WBP_NajikaHUD is set in Create Widget node
3. Ensure Add to Viewport is called
4. Check Z-Order (should be 0 or positive)
5. Verify Widget is not set to Hidden
6. Check Output Log for widget creation errors

---

### Issue: Character falls through floor

**Symptoms:** Character spawns and immediately falls

**Solutions:**
1. Ensure floor has collision enabled
2. Check Player Start is above floor (Z > 100)
3. Verify Character has Capsule Component
4. Check Capsule Component collision settings:
   - Collision Preset: "Pawn"
   - Collision Enabled: "Query and Physics"
5. Ensure floor is set to "Block All" or "WorldStatic"

---

### Issue: Buttons don't respond to clicks

**Symptoms:** UI buttons visible but clicking does nothing

**Solutions:**
1. Verify button OnClicked event is bound in Graph
2. Check Widget has "Is Focusable" enabled
3. Ensure no other UI blocking clicks (Z-Order)
4. Check Input Mode is set to "UI Only" or "Game and UI"
5. Verify Show Mouse Cursor is TRUE

---

### Issue: Movement doesn't work

**Symptoms:** WASD keys do nothing

**Solutions:**
1. Check Input Settings have MoveForward/MoveRight axis mappings
2. Verify NajikaCharacter C++ code has input binding
3. Ensure Player Controller class is BP_NajikaPlayerController
4. Check Input Mode is "Game Only" or "Game and UI"
5. Verify Character Movement Component exists and is enabled

---

### Issue: Camera doesn't follow character

**Symptoms:** Camera is static or at wrong angle

**Solutions:**
1. Check Spring Arm and Camera components exist
2. Verify "Use Pawn Control Rotation" is enabled on Spring Arm
3. Ensure Camera is attached to Spring Arm (parent-child relationship)
4. Check Auto Activate is TRUE for Camera
5. Verify Player Controller is possessing the character

---

### Issue: Plugins not loading

**Symptoms:** Plugins show as "Failed to Load"

**Solutions:**
1. Check plugin .uplugin file exists
2. Verify Build.cs has correct dependencies
3. Ensure plugin compiled in Visual Studio
4. Check plugin DLL exists in: `Binaries/Win64/`
5. Try: Right-click .uproject → Generate Visual Studio Files
6. Rebuild solution
7. Restart editor

---

### Issue: Android build fails

**Symptoms:** Package Android shows errors

**Solutions:**
1. Verify Android SDK installed (Android Studio)
2. Check JDK 17 installed and JAVA_HOME set
3. Ensure NDK installed (r25c or later)
4. Verify Project Settings → Android:
   - Package name correct
   - SDK paths set
   - Build for ARM64 enabled
5. Check Output Log for specific error
6. Try: File → Refresh Visual Studio Project
7. Try: Rebuild project in VS before packaging

---

### Issue: Voice system not working

**Symptoms:** Voice chat errors in log

**Solutions:**
1. Check NajikaVoiceSystem plugin enabled
2. Verify backend server is running (localhost:8000)
3. Check microphone permission granted (Windows Settings)
4. Ensure UNajikaVoiceComponent added to Player Controller or Character
5. Verify Initialize() is called in BeginPlay
6. Check Output Log for "NajikaVoiceSystem: Initialized" message
7. Test microphone in Windows Sound Settings

---

### Issue: Performance is slow in editor

**Symptoms:** Low FPS, stuttering

**Solutions:**
1. Close other applications
2. Editor: Settings → Engine Scalability → Low (for testing)
3. Disable real-time rendering: Click "Realtime" button in viewport
4. Reduce viewport resolution
5. Disable Lumen (Project Settings → Rendering)
6. Build lighting (reduces real-time calculations)
7. Use Mobile Preview for mobile performance testing

---

## 📚 Additional Resources

**UE5 Documentation:**
- Blueprints: https://docs.unrealengine.com/en-US/ProgrammingAndScripting/Blueprints/
- UMG: https://docs.unrealengine.com/en-US/InteractiveExperiences/UMG/
- Input: https://docs.unrealengine.com/en-US/InteractiveExperiences/Input/

**Project Files:**
- See: VISUAL_STUDIO_COMPILATION_GUIDE.md
- See: ANDROID_BUILD_DEPLOYMENT_GUIDE.md
- See: TESTING_VALIDATION_CHECKLIST.md

---

## ✅ Final Checklist

Before proceeding to APK build:

- [ ] All 9 Blueprints created and compiled
- [ ] All Project Settings configured
- [ ] All Plugins enabled
- [ ] MainLevel created and saved
- [ ] In-editor testing passed
- [ ] No errors in Output Log
- [ ] Character movement works
- [ ] HUD displays correctly
- [ ] Buttons respond to clicks

**If all checked → Proceed to ANDROID_BUILD_DEPLOYMENT_GUIDE.md** ✅

---

**End of Blueprint Creation Guide**

**Estimated Time:** 2-3 hours
**Created:** 2025-11-13
**For:** Local Model - Najika Digivice UE5 Project
**Author:** Claude Code Web Model
