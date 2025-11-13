# 🎮 NAJIKA HANDYSPIEL - FULL GAME (500x500m)

**Model 2 - Full Game Project**
**Target**: Windows + Android (Xiaomi 11T Pro)
**Mode**: Online Multiplayer Survival-RPG

---

## 🎯 OVERVIEW

**Genre**: Single-Player (später Koop) Survival-RPG
**World Size**: 500x500m (expandable)
**Platform**: Mobile-First (Xiaomi 11T Pro target)
**Backend**: Zero-Trust Architecture (127.0.0.1 only)

---

## 🌟 CORE FEATURES

### ✅ Aus Test Environment importiert:

1. **Explosion Class** (Standalone, never mixed)
   - 4 Explosion variants
   - Charging system
   - Exhaustion mechanics
   - Talent system (+35% explosion, -17.5% others)

2. **Fortnite-Style Movement**
   - Sprint → Slide → Dash
   - Vault → Mantle → Wall-Climb
   - I-Frames system

3. **Signature Paths** (11 Weapons)
   - Schwert: Ultimativer Schnitt
   - Speer: Himmelsdurchbohrer
   - Axt: Spalter
   - Hammer: Zertrümmerer
   - Bogen: Zenit-Schuss
   - Armbrust: Präzisions-Schuss
   - Stab: Arkane Kaskade
   - Dolch: Schatten-Durchschlag
   - Sense: Ernte der Seelen
   - Peitsche: Kettengeißel
   - Explosion: Omega-Explosion

4. **Oregon-Engine** (Procedural Events)
   - >1 Million scene variations
   - Grammar-based dimensional events
   - In-World experiences (no UI popups)

5. **Slime-Arena** (Section 2.7)
   - Assist Mode (Anfeuern system)
   - Auto Mode (AI control)
   - PvE/PvP brackets (separate scaling)
   - Meta-learning (anonymized)

6. **Crafting System**
   - Pipeline: Rohstoffe → Veredeln → Herstellen → Verzaubern → Fein-Tuning
   - Alchemy (Lore-based, NO real medical advice)
   - Real-world herbs (Weidenrinde, Ingwer, Honig, etc.)
   - Flavor buffs

7. **Backend Integration**
   - secure-hub (Port 5010)
   - game-core (Port 7010)
   - Zero-Trust (127.0.0.1 only)
   - Owner-Gate (X-OWNER-TOKEN)

### 🔄 Full Game Zusätze:

8. **Online Multiplayer**
   - Dedicated Server
   - Peer-to-Peer (fallback)
   - Matchmaking
   - Friend System

9. **500x500m Open World**
   - Multiple Biomes
   - Dynamic Weather
   - Day/Night Cycle
   - Procedural Events

10. **Progression System**
    - Use-based skill progression
    - Talent trees
    - Achievement system
    - Reputation system

11. **Combat System**
    - Real-time action combat
    - Combo system
    - PvE + PvP
    - Boss battles

12. **Economy**
    - Player trading
    - NPC merchants
    - Auction house
    - Currency system

---

## 📂 PROJECT STRUCTURE

```
FullGame_NajikaHandyspiel_UE5/
├── NajikaGame.uproject
├── Source/
│   └── NajikaGame/
│       ├── Public/
│       │   ├── MultiplayerGameMode.h
│       │   ├── OpenWorldManager.h
│       │   ├── ProgressionSystem.h
│       │   └── [Imported from Test Environment]
│       ├── Private/
│       └── NajikaGame.Build.cs
├── Config/
│   ├── DefaultEngine.ini
│   ├── DefaultGame.ini
│   └── DefaultInput.ini
├── Content/
│   ├── Maps/
│   │   ├── MainWorld_500x500.umap
│   │   ├── TestArena.umap
│   │   └── Lobby.umap
│   ├── Blueprints/
│   │   ├── BP_MultiplayerController.uasset
│   │   └── BP_OpenWorldGameMode.uasset
│   ├── Multiplayer/
│   │   ├── BP_DedicatedServer.uasset
│   │   └── BP_NetworkManager.uasset
│   └── UI/
│       ├── MainMenu.uasset
│       └── HUD.uasset
└── Docs/
    ├── README.md (this file)
    └── MULTIPLAYER_SETUP.md
```

---

## 🔐 8 GEBOTE (Hard Rules)

Aus dem PDF "handyspiel und später uefn.pdf":

1. **Zero-Trust by default** – Services nur 127.0.0.1
2. **Owner-Gate** – Admin routes nur mit X-OWNER-TOKEN
3. **Explosion ≠ Weave** – Explosion ist EIGENE KLASSE
4. **PvE/PvP-Trennung** – Getrennte Skalare & Resistenzen
5. **Use-based Progress** – Skills steigen durchs Benutzen
6. **NSFW & Real-World-Wissen**: aus, "Lore only"
7. **Privacy & Lernsystem** – Slime-Arena: anonymisierte Moves
8. **Offline-first & Audit** – Logs lokal, Backups rotieren

---

## 🚀 SETUP

### Requirements

- Unreal Engine 5.4
- Visual Studio 2022
- Android Studio (for mobile builds)
- Windows 10/11

### Installation

```powershell
# 1. Clone/Copy project to:
C:\NajikaHandyspiel_UE5\

# 2. Generate Visual Studio files
Right-click NajikaGame.uproject → Generate VS project files

# 3. Open in UE5
Double-click NajikaGame.uproject

# 4. Build in Visual Studio
Ctrl+Shift+B
```

---

## 🌐 MULTIPLAYER SETUP

### Dedicated Server

```powershell
# Build Server target
UE5Editor.exe NajikaGame.uproject -run=Cook -TargetPlatform=WindowsServer

# Launch Server
NajikaGameServer.exe -log
```

### Client Connection

```cpp
// In Blueprint or C++
OpenLevel("192.168.1.100:7777");  // Server IP:Port
```

---

## 📱 ANDROID BUILD

```powershell
# Package for Android
File → Package Project → Android → Android (ASTC)

# Output:
C:\NajikaHandyspiel_UE5\Android\NajikaGame.apk

# Install on Xiaomi 11T Pro
adb install -r NajikaGame.apk
```

---

## 🎯 DEVELOPMENT ROADMAP

### Phase 1: Core Systems (DONE ✅)
- [x] Explosion Class
- [x] Movement System
- [x] Signature Paths
- [x] Oregon-Engine
- [x] Slime-Arena
- [x] Crafting
- [x] Backend Integration

### Phase 2: Multiplayer (IN PROGRESS 🔄)
- [ ] Dedicated Server Setup
- [ ] Client-Server Communication
- [ ] Matchmaking System
- [ ] Friend System
- [ ] Chat System

### Phase 3: Open World (PENDING 📋)
- [ ] 500x500m Map
- [ ] Multiple Biomes
- [ ] Dynamic Weather
- [ ] Day/Night Cycle
- [ ] NPC System

### Phase 4: Content (PENDING 📋)
- [ ] 10+ Boss Fights
- [ ] 50+ Quests
- [ ] 100+ Items
- [ ] 20+ Achievements

### Phase 5: Polish & Launch (PENDING 📋)
- [ ] Mobile Optimization
- [ ] Tutorial System
- [ ] Localization (DE/EN)
- [ ] Beta Testing
- [ ] Launch!

---

## 🔄 IMPORT FROM TEST ENVIRONMENT

Alle Core-Systeme aus `TestEnvironment_UE5` können direkt importiert werden:

```cpp
// Copy headers and source files:
TestEnvironment_UE5/Source/NajikaTest/Public/*.h
  → FullGame_NajikaHandyspiel_UE5/Source/NajikaGame/Public/

TestEnvironment_UE5/Source/NajikaTest/Private/*.cpp
  → FullGame_NajikaHandyspiel_UE5/Source/NajikaGame/Private/
```

**Files to import:**
- ExplosionClass.h/.cpp
- FortniteMovementComponent.h/.cpp
- SignaturePathsSystem.h/.cpp
- OregonEngine.h/.cpp
- SlimeArena.h/.cpp
- CraftingSystem.h/.cpp
- BackendConnector.h/.cpp
- NajikaHUD.h/.cpp

---

## 📖 DOCUMENTATION

- **Test Environment**: `../TestEnvironment_UE5/README.md`
- **PDF Spec**: `../alles wissen/zip/handyspiel und später uefn.pdf`
- **Mobile Architecture**: `../DOCS/MOBILE_APP_ARCHITECTURE.md`

---

## 🎮 CONTROLS

### PC (Keyboard + Mouse)
- **WASD** - Movement
- **Shift** - Sprint
- **Ctrl** - Slide
- **E** - Dash
- **Space** - Jump
- **1-4** - Explosions
- **Q (Hold)** - Charge Explosion
- **F** - Interact
- **I** - Inventory
- **M** - Map

### Mobile (Touch)
- **Virtual Joystick** (left) - Movement
- **Virtual Buttons** (right) - Abilities
- **Swipe** - Dash/Slide
- **Tap** - Interact
- **Pinch** - Zoom Map

---

## 🔐 BACKEND URLS

```yaml
secure-hub: http://127.0.0.1:5010  # Health, QR, Vault, Push
game-core:  http://127.0.0.1:7010  # Assets, Oregon, Combat
```

**Zero-Trust**: Services bind ONLY to 127.0.0.1!

---

## 📊 STATS

- **World Size**: 500x500m (250,000 m²)
- **Target Players**: 10-50 per server
- **Event Variations**: >1,000,000
- **Weapons**: 11 types
- **Signature Moves**: 11 unique
- **Crafting Recipes**: 100+
- **Herbs**: 10 types
- **Biomes**: 7 types

---

**Model**: 2 (Full Game)
**Status**: Phase 1 Complete ✅, Phase 2 In Progress 🔄
**Target Device**: Xiaomi 11T Pro (Snapdragon 888, 8GB RAM)
**Created**: 2025-11-11
