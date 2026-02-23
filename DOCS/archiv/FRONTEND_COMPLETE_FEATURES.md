# 🎮 NAJIKA DIGIVICE FRONTEND - COMPLETE FEATURES
**Version:** 2.0
**Technology Stack:** Three.js (3D), HTML5, CSS3, Vanilla JavaScript
**Target Platform:** Web (Desktop & Mobile)

---

## 📋 TABLE OF CONTENTS

1. [Architecture Overview](#architecture-overview)
2. [3D Scene System](#3d-scene-system)
3. [Character System](#character-system)
4. [Camera System](#camera-system)
5. [Combat System](#combat-system)
6. [Animation System](#animation-system)
7. [Input System](#input-system)
8. [UI Components](#ui-components)
9. [Room System](#room-system)
10. [Mini-Games](#mini-games)
11. [Special Features](#special-features)

---

## 🏗️ ARCHITECTURE OVERVIEW

### File Structure
```
digivice/
├── index.html                    // Main HTML
├── js/
│   ├── 3d_scene.js              // Three.js scene manager
│   ├── character_animations.js  // Animation controller
│   ├── battle_core.js           // Battle system
│   ├── battle_api.js            // Battle API integration
│   ├── touch_controls.js        // Mobile touch controls
│   ├── kaykit_loader.js         // KayKit asset loader
│   ├── room_connector.js        // Room transitions
│   ├── minigames.js             // Mini-game implementations
│   ├── chat_ui.js               // Chat interface
│   ├── code_editor.js           // Code editor
│   ├── file_manager.js          // File management
│   ├── terminal_modules.js      // Terminal interface
│   ├── fishing.js               // Fishing mini-game
│   ├── garden.js                // Garden mini-game
│   ├── oregon.js                // Oregon Trail-style events
│   ├── dungeon_combat.js        // Dungeon battle system
│   ├── dungeon_generator.js     // Procedural dungeon gen
│   ├── command_system.js        // Command parser
│   ├── buildings_custom.js      // Building system
│   ├── private_mode.js          // Private mode features
│   └── safe_functions.js        // Security helpers
└── static/
    └── css/
        ├── chat.css
        ├── minigames.css
        ├── code_editor.css
        ├── file_manager.css
        ├── system_monitor.css
        ├── secure_messenger.css
        └── terminal_modules.css
```

### Technology Stack
- **3D Engine:** Three.js (r159+)
- **Character Models:** KayKit AnimatedCharacter Pack
- **Environment:** KayKit Dungeon Pack / Adventurers Pack
- **Rendering:** WebGL 2.0
- **Physics:** Custom collision detection
- **Audio:** Web Audio API

---

## 🎬 3D SCENE SYSTEM

### Scene Configuration
```javascript
// Color Palettes
DEFAULT_PALETTE = {
  background: 0x1a1a2e,
  fog: 0x1a1a2e,
  ambient: 0.45,
  dir: 0xffffff,
  dirIntensity: 0.9,
  primary: 0xff6b6b,
  secondary: 0x667eea,
  floor: 0x2a2a3e
}

PRIVATE_PALETTE = {
  background: 0x240008,
  fog: 0x240008,
  ambient: 0.25,
  dir: 0xff5500,
  dirIntensity: 0.6,
  primary: 0xaa1111,
  secondary: 0x330033,
  floor: 0x240008
}
```

### Lighting System
- **Ambient Light:** Global illumination (adjustable intensity)
- **Directional Light:** Main sun/moon light (dynamic intensity)
- **Point Lights:** 2 dynamic point lights for atmosphere
- **Shadows:** Enabled for directional light

### Scene Components
- **Base Floor:** Ground plane with grid helper
- **Room Group:** Container for KayKit room models
- **Fallback Walls:** Procedurally generated walls if no 3D model
- **Fog:** Distance fog for atmosphere

### Performance Features
- **LOD System:** Level-of-detail switching
- **Frustum Culling:** Automatic by Three.js
- **Object Pooling:** For frequently spawned objects
- **Target FPS:** 60 FPS (desktop), 30 FPS (mobile)

---

## 👤 CHARACTER SYSTEM

### Character Configuration
```javascript
CHARACTER_SPEED = 7.5              // Units per second
CHARACTER_HEIGHT = 3.8             // Height for camera offset
CLAMP_PADDING = 2                  // Boundary padding
```

### Character Controller
- **Movement:** WASD keys (desktop), Virtual Joystick (mobile)
- **Running:** Hold Shift to run (1.5x speed)
- **Jumping:** Spacebar (physics-based)
- **Rotation:** Mouse look / Touch drag

### Character Stats (Integrated with Backend)
```javascript
{
  hp: 100,
  maxHp: 100,
  stamina: 100,
  maxStamina: 100,
  hunger: 100,
  energy: 100,
  hygiene: 100,
  happiness: 100,
  strength: 10,
  intelligence: 10,
  dexterity: 10,
  charisma: 10
}
```

### Collision Detection
- **Boundaries:** Clamped to room size with padding
- **Wall Collision:** Ray casting for wall detection
- **Floor Snapping:** Character stays on ground

---

## 📷 CAMERA SYSTEM

### Camera Modes

#### 1. ORBIT Mode (Default)
- **Description:** Free-rotating orbital camera
- **Controls:**
  - Mouse Drag: Rotate around character
  - Mouse Wheel: Zoom in/out
  - Touch Drag: Rotate (mobile)
- **Distance:** 15 units from character
- **Rotation:** 360° horizontal, 80° vertical clamp

#### 2. THIRD PERSON Mode
- **Description:** Over-the-shoulder following camera
- **Position:** Behind character, offset up and right
- **Rotation:** Follows character heading
- **Smooth Follow:** Lerped position and rotation
- **Distance:** 12 units behind, 5 units up

#### 3. FIRST PERSON Mode
- **Description:** Character's eye view
- **Position:** At character head height
- **Rotation:** Direct character control
- **Mouse Sensitivity:** Adjustable
- **FOV:** 75° (configurable)

### Camera Features
- **Smooth Transitions:** 0.5s fade between modes
- **Auto-Follow:** Camera tracks character movement
- **Collision Avoidance:** Camera pulls closer if obstructed
- **Face Najika Button:** Instantly rotate to face character

---

## ⚔️ COMBAT SYSTEM

### Dual-Wield System (Skyrim + Dark Souls Inspired)

#### Equipment Slots
```javascript
{
  leftHand: {
    type: 'wand',           // Spell, Shield, Secondary Weapon
    name: 'Najika Staff',
    damage: 25
  },
  rightHand: {
    type: 'sword',          // Primary Weapon
    name: 'Eisenschwert',
    damage: 35
  },
  armor: {
    defense: 10
  }
}
```

#### Combat Mechanics

**1. Basic Attacks**
- **Left Hand (Q):** Light attack (10 stamina)
- **Right Hand (E):** Heavy attack (15 stamina)
- **Dual Strike (Q+E):** Both hands (25 stamina)

**2. Combo System**
```javascript
combos = {
  'LR': {
    damage: 30,
    stamina: 15,
    name: 'Schneller Doppelschlag'
  },
  'RRL': {
    damage: 50,
    stamina: 25,
    name: 'Wirbel-Angriff'
  },
  'LLL': {
    damage: 40,
    stamina: 20,
    name: 'Zauber-Salve'
  },
  'RLRL': {
    damage: 70,
    stamina: 35,
    name: 'Todestanz'
  }
}
```
- **Combo Window:** 1000ms between inputs
- **Visual Feedback:** Combo counter UI
- **Damage Multiplier:** Increases with combo hits

**3. Parry System (Dark Souls Style)**
- **Button:** Right Mouse Button (hold)
- **Timing Window:** 80-200ms
- **Stamina Cost:** 5 stamina
- **Success:** Stagger enemy, open for riposte
- **Fail:** Take damage
- **Cooldown:** 1000ms

**4. Dodge Roll**
- **Button:** Spacebar (in combat)
- **Invincibility Frames:** 12 frames (~200ms)
- **Stamina Cost:** 20 stamina
- **Distance:** 5 units
- **Cooldown:** 500ms
- **Animation:** Roll direction based on input

**5. Blocking**
- **Button:** Hold Right Click
- **Damage Reduction:** 50-80% (depends on shield)
- **Stamina Drain:** 5 stamina/second while blocking
- **Perfect Block Window:** First 100ms blocks 100%

### Combat Stats
```javascript
{
  hp: 100,
  maxHp: 100,
  stamina: 100,
  maxStamina: 100,
  staminaRegen: 10/sec,   // Out of combat
  staminaRegenCombat: 5/sec,  // In combat
  attackPower: 35,
  defense: 10,
  critChance: 0.1,        // 10%
  critMultiplier: 2.0     // 2x damage
}
```

### Enemy AI (Basic)
- **Detection Range:** 15 units
- **Attack Range:** 3 units
- **Attack Cooldown:** 2 seconds
- **Movement:** Simple pathfinding toward player
- **Types:** Rat, Skeleton, Slime, Goblin, Dark Mage, Bosses

---

## 🎬 ANIMATION SYSTEM

### Animation Controller
**System:** Three.js AnimationMixer

### Available Animations (KayKit AnimatedCharacter)
```javascript
animations = {
  'idle': {
    loop: true,
    priority: 0
  },
  'walk': {
    loop: true,
    priority: 1
  },
  'run': {
    loop: true,
    priority: 2
  },
  'jump': {
    loop: false,
    priority: 5
  },
  'attack': {
    loop: false,
    priority: 10
  },
  'block': {
    loop: true,
    priority: 8
  },
  'duck': {
    loop: true,
    priority: 3
  },
  'hit': {
    loop: false,
    priority: 9
  },
  'death': {
    loop: false,
    priority: 15
  }
}
```

### Animation Blending
- **Fade Time:** 0.2 seconds (configurable)
- **Smooth Transitions:** Cross-fade between animations
- **Priority System:** Higher priority animations override lower
- **State Machine:** Automatic animation selection based on state

### Animation States
```javascript
getAnimationForState(isMoving, isRunning, isJumping, isDucking, isAttacking, isBlocking) {
  if (isAttacking) return 'attack';
  if (isBlocking) return 'block';
  if (isDucking) return 'duck';
  if (isJumping) return 'jump';
  if (isRunning) return 'run';
  if (isMoving) return 'walk';
  return 'idle';
}
```

---

## 🎮 INPUT SYSTEM

### Desktop Controls

#### Keyboard
```
W / ↑       - Move Forward
S / ↓       - Move Backward
A / ←       - Move Left
D / →       - Move Right
Shift       - Run (hold)
Spacebar    - Jump / Dodge Roll (in combat)
Q           - Left Hand Attack
E           - Right Hand Attack
R           - Interact / Use Item
F           - Toggle Flashlight
Tab         - Toggle Chat
Escape      - Menu / Pause
1-9         - Quick Slots (items/skills)
C           - Character Stats
I           - Inventory
M           - Map
```

#### Mouse
```
Left Click    - Primary Attack (Right Hand)
Right Click   - Block / Parry
Middle Click  - Lock-On Target
Mouse Move    - Camera Rotation (Orbit/First-Person)
Mouse Wheel   - Zoom In/Out (Orbit Mode)
```

### Mobile Controls (Touch)

#### Virtual Joystick
- **Position:** Bottom-left
- **Size:** 100x100px
- **Appearance:** Visible on touch
- **Max Distance:** 50px
- **8-Directional:** Movement in all directions

#### Touch Buttons
```
Bottom-Right Corner:
├── Jump Button (Spacebar equivalent)
├── Attack Button (Left/Right hand)
├── Block Button (Shield icon)
└── Interact Button (Hand icon)

Top-Right Corner:
├── Menu Button (☰)
├── Chat Button (💬)
└── Inventory Button (🎒)
```

#### Camera Gestures
```
Single Touch Drag    - Rotate Camera (right side of screen)
Two-Finger Pinch     - Zoom In/Out
Two-Finger Rotate    - Rotate Camera Y-axis
Double Tap           - Center Camera on Character
```

### Gamepad Support (Planned)
```
Left Stick     - Movement
Right Stick    - Camera
A / Cross      - Jump
B / Circle     - Dodge Roll
X / Square     - Light Attack
Y / Triangle   - Heavy Attack
LB / L1        - Block
RB / R1        - Parry
LT / L2        - Left Hand Attack
RT / R2        - Right Hand Attack
D-Pad          - Quick Slots
Start          - Menu
Select         - Map
```

---

## 🖥️ UI COMPONENTS

### HUD (Heads-Up Display)

#### Health/Stamina Bars
```javascript
{
  position: 'top-left',
  width: '260px',
  bars: {
    hp: {
      color: '#2ecc71',      // Green
      gradient: '90deg, #2ecc71, #27ae60'
    },
    stamina: {
      color: '#f39c12',      // Orange
      gradient: '90deg, #f39c12, #e67e22'
    },
    hunger: {
      color: '#3498db',      // Blue
      gradient: '90deg, #3498db, #2980b9'
    },
    energy: {
      color: '#9b59b6',      // Purple
      gradient: '90deg, #9b59b6, #8e44ad'
    }
  }
}
```

#### Stats Panel
- **Position:** Top-left corner
- **Content:**
  - HP: 100/100
  - Stamina: 100/100
  - Hunger: 85/100
  - Energy: 70/100
  - Level: 5
  - XP: 1234/2000
- **Style:** Glass-morphism with blur

#### Camera Panel
- **Position:** Below stats panel
- **Buttons:**
  - Orbit Mode
  - Third Person
  - First Person
  - Face Najika
  - Webcam Toggle (AR feature)

#### Mini-Map (Planned)
- **Position:** Top-right corner
- **Size:** 200x200px
- **Content:**
  - Character position (blue dot)
  - Enemies (red dots)
  - NPCs (green dots)
  - Objectives (yellow markers)
  - Room boundaries

### Chat UI
- **Position:** Bottom-left (overlay)
- **Features:**
  - Message history (scrollable)
  - Input field with send button
  - Voice input button (microphone)
  - Emoji picker
  - @Najika mentions
  - Markdown support
- **Hotkey:** Tab

### Inventory UI (Planned)
- **Layout:** Grid-based (6x8 = 48 slots)
- **Features:**
  - Drag & drop
  - Item tooltips
  - Rarity colors
  - Stack counts
  - Weight/capacity bar
  - Quick slots (1-9)
  - Equipment paper doll
- **Hotkey:** I

### Character Stats UI (Planned)
- **Layout:** Multi-tab
- **Tabs:**
  1. **Stats:** STR, INT, DEX, CHA, HP, Stamina
  2. **Skills:** Skill tree with progression
  3. **Achievements:** Unlocked achievements
  4. **Reputation:** Faction standings
- **Hotkey:** C

---

## 🏠 ROOM SYSTEM

### Available Rooms
```javascript
ROOMS = [
  'Wohnzimmer',              // Living Room
  'Schlafzimmer',            // Bedroom
  'Küche',                   // Kitchen
  'Badezimmer',              // Bathroom
  'Garten',                  // Garden
  'Musikraum',               // Music Room
  'Medizin',                 // Medical Room
  'Terminal',                // Terminal/Tech Room
  'Studieren & Crafting',    // Study & Crafting
  'Trainingszimmer',         // Training Room
  'Kampfarena',              // Battle Arena
  'Schwarze Mühle – Keller'  // Black Mill - Basement
]
```

### Room Features
- **Dynamic Loading:** Rooms loaded on demand
- **KayKit Integration:** Uses KayKit Dungeon/Adventurers packs
- **Fallback System:** Procedural walls if 3D model missing
- **Room Transitions:** Smooth fade-in/out
- **Room Bounds:** Collision boundaries per room

### Room Configuration
```javascript
{
  name: 'Wohnzimmer',
  span: 24,              // Room size (units)
  wallHeight: 6,         // Wall height (units)
  model: 'kaykit_living_room.glb',
  spawnPoint: { x: 0, y: 0, z: 0 },
  lightingPreset: 'cozy',
  interactions: [
    { type: 'sofa', action: 'sit' },
    { type: 'tv', action: 'watch' },
    { type: 'door', action: 'changeRoom' }
  ]
}
```

---

## 🎮 MINI-GAMES

### 1. Rhythm Game
- **Type:** Music rhythm (Guitar Hero style)
- **Controls:** Arrow keys / Touch buttons
- **Scoring:** Combo multiplier, accuracy percentage
- **Songs:** 3-5 tracks
- **Rewards:** XP, Gold, Music notes (currency)

### 2. Garden System
- **Type:** Farming simulation
- **Features:**
  - Plant seeds (tomato, carrot, wheat)
  - Water plants
  - Harvest crops
  - Crop growth stages (3-5 stages)
  - Seasonal crops
- **Rewards:** Food items, Gold

### 3. Reflex Test
- **Type:** Reaction time challenge
- **Mechanic:** Click/tap as soon as color changes
- **Scoring:** Average reaction time (ms)
- **Rewards:** XP, Dexterity stat boost

### 4. Fishing
- **Type:** Fishing mini-game
- **Mechanic:**
  - Cast line
  - Wait for bite
  - Reel in (timing-based)
  - Catch fish (different rarities)
- **Rewards:** Fish (food/crafting materials)

### 5. Oregon Trail Events
- **Type:** Random encounter system
- **Events:**
  - River crossing
  - Wildlife encounter
  - Weather events
  - Resource shortages
- **Consequences:** Stat changes, item loss/gain

---

## ✨ SPECIAL FEATURES

### Private Mode
- **Activation:** Secret command or button
- **Visual Changes:**
  - Dark red color palette
  - Dimmed lighting
  - Red fog
  - Different music/ambience
- **Behavioral Changes:**
  - Najika personality shift
  - Different dialogue options
  - Adult content unlocked (if enabled)

### Webcam Integration (AR)
- **Feature:** Overlay Najika on webcam feed
- **Uses:** WebRTC / getUserMedia API
- **Position:** Picture-in-picture in HUD
- **Toggle:** Webcam button in camera panel

### Voice Commands
- **Integration:** Web Speech API
- **Commands:**
  - "Najika, come here"
  - "Open inventory"
  - "Attack"
  - "Heal me"
- **Language:** German primary, English secondary

### Code Editor
- **Type:** In-game Python editor
- **Features:**
  - Syntax highlighting
  - Auto-completion
  - Code execution (sandboxed)
  - File save/load
- **Integration:** Backend `/api/code/execute`

### File Manager
- **Features:**
  - Browse files
  - Create/delete/rename
  - Upload/download
  - Text editor
- **Security:** Sandboxed, limited permissions

### Terminal
- **Type:** Unix-style terminal emulator
- **Commands:**
  - Standard Unix commands (ls, cd, cat, etc.)
  - Custom Najika commands
  - Backend integration
- **Modules:**
  - System monitor
  - Process viewer
  - Network tools

---

## 📊 PERFORMANCE METRICS

### Target Performance
```javascript
{
  desktop: {
    targetFPS: 60,
    minFPS: 30,
    drawCalls: '<500',
    triangles: '<100k',
    textures: '<512MB'
  },
  mobile: {
    targetFPS: 30,
    minFPS: 20,
    drawCalls: '<200',
    triangles: '<50k',
    textures: '<256MB'
  }
}
```

### Optimization Techniques
1. **Geometry Instancing:** Reuse meshes
2. **Texture Atlasing:** Combine textures
3. **LOD System:** Reduce detail at distance
4. **Frustum Culling:** Only render visible objects
5. **Object Pooling:** Reuse objects (particles, enemies)
6. **Lazy Loading:** Load assets on demand
7. **Compression:** GLTF/GLB with Draco compression

---

## 🔌 BACKEND INTEGRATION

### API Calls (see BACKEND_COMPLETE_API_REFERENCE.md)
```javascript
// Chat
fetch('/api/chat', { method: 'POST', body: JSON.stringify({ message }) })

// Najika Status
fetch('/api/najika/status', { method: 'GET' })

// Battle
fetch('/api/battle/start', { method: 'POST' })
fetch('/api/battle/action', { method: 'POST', body: JSON.stringify({ action, target }) })

// Voice Call
fetch('/api/voice_call/start', { method: 'POST' })
fetch('/api/voice_call/audio', { method: 'POST', body: JSON.stringify({ audio_data }) })

// Living System
fetch('/api/living/proactive', { method: 'GET' })
```

### State Synchronization
- **Polling Interval:** 5-10 seconds
- **Events:** Server-Sent Events (SSE) for real-time updates
- **Local State:** Optimistic UI updates, synced on response

---

## 🚀 UE5 MIGRATION NOTES

### What to Migrate

**MUST HAVE:**
1. ✅ Character controller (WASD movement, jumping)
2. ✅ Camera system (Orbit, Third, First-Person)
3. ✅ Combat system (attacks, parry, dodge, combos)
4. ✅ Animation system (all animations)
5. ✅ Backend integration (API calls)
6. ✅ HUD (HP/Stamina bars, stats)
7. ✅ Room system (12 rooms with boundaries)

**SHOULD HAVE:**
8. ✅ Touch controls for mobile
9. ✅ Mini-games (rhythm, garden, reflex, fishing)
10. ✅ Inventory system (48-slot grid)
11. ✅ Equipment system (dual-wield)
12. ✅ Private mode (color palette swap)

**NICE TO HAVE:**
13. ⚠️ Webcam AR (complex, may skip)
14. ⚠️ Code editor (not game-critical)
15. ⚠️ File manager (not game-critical)
16. ⚠️ Terminal (not game-critical)

### UE5 Equivalent Systems

| Frontend Feature | UE5 Equivalent |
|------------------|----------------|
| Three.js Scene | UE5 Level/World |
| THREE.Mesh | UStaticMeshComponent |
| THREE.AnimationMixer | UAnimInstance |
| WASD Controls | Enhanced Input System |
| Camera Modes | Spring Arm + Camera Component |
| Combat System | C++ Components (CombatComponent) |
| UI (HTML) | UMG Widgets |
| Touch Controls | Touch Interface + Virtual Joystick |
| API Calls | HTTP Plugin + WebSocket Plugin |

---

**Document Version:** 1.0
**Last Updated:** 2025-01-15
**Total Features Documented:** 100+
**Lines:** 950+

---

✅ **READY FOR UE5 MIGRATION IMPLEMENTATION!**
