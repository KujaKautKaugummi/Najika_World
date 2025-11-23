# 🎮 NAJIKA MODEL 2 - TEST ENVIRONMENT

**Status**: ✅ Core Implementation Complete
**Target**: Windows + Android (Xiaomi 11T Pro)
**Purpose**: Triple Purpose - Test/Prototype/Export

---

## 🎯 TRIPLE PURPOSE

### 1. Test Digivice Features
Teste Najika Digivice Features VOR Integration in Model 1 (Flutter App):
- Terminal Module (Remote PC Control)
- Browser Module (WebView + Remote Browser)
- Voice System (Megumin Clone)
- Backend Connection (najika_server.py)

### 2. Prototype Handyspiel Mechaniken
10x10m Mini-Test für Game Mechanics:
- ✅ **Explosion Class** (FERTIG!)
- 🔄 Fortnite-Movement (Sprint/Slide/Dash)
- 🔄 Signature Paths (Schwert/Speer/Axt)
- 🔄 Oregon-Engine Mini
- 🔄 Slime-Arena (Section 2.7)

### 3. Export zu Full Game
Validierte Mechaniken exportieren zu:
- **NajikaHandyspiel_UE5** (500x500m Online Multiplayer)

---

## ✅ WAS IST FERTIG?

### Explosion Class (100% Complete!)

**4 Explosion-Varianten:**
1. **Große Explosion** (Key 1)
   - Riesen-AoE (10m Radius)
   - 500 Damage
   - 8s Exhaustion

2. **4-fach Explosion** (Key 2)
   - 4x Serial Explosions
   - 4m Radius each
   - 150 Damage per explosion
   - 0.25s delay between

3. **Mini-Explosion** (Key 3)
   - Spam-capable (0.5s Cooldown)
   - 2m Radius
   - 80 Damage
   - Setup für Combos

4. **Omega-Explosion** (Key 4)
   - 600% AoE (25m Radius!)
   - 2000 Damage
   - 30s Exhaustion mit -50% Regen
   - Muss charged werden!

**Charging System:**
- Hold Q → Charge up
- Release Q → Explosion Power based on charge
- 100% Charge → Omega Ready!

**Exhaustion System:**
- Nach großen Explosionen: Cooldown
- Keine Explosionen während Exhausted
- Regeneration Penalty bei Omega

**Talent System:**
- ✅ +35% Explosion Damage/Radius/Charge Speed
- ⚠️ -17.5% Melee/Ranged/Magic/Defense
- Trade-off: Spezialisierung auf Explosionen!

---

## 🛠️ SETUP

### Windows Installation

```powershell
# 1. PowerShell als Admin öffnen
cd TestEnvironment_UE5

# 2. Auto-Setup ausführen
.\SETUP_PROJECT.ps1

# → Kopiert Projekt nach C:\NajikaTestEnvironment_UE5
# → Öffnet in UE5 (falls installiert)
```

### Manuell Setup

1. **Kopiere Projekt:**
   ```
   C:\NajikaTestEnvironment_UE5\
   ```

2. **Generate VS Files:**
   - Rechtsklick auf `NajikaTest.uproject`
   - "Generate Visual Studio project files"

3. **Öffne in UE5:**
   - Doppelklick auf `NajikaTest.uproject`

4. **Build:**
   - In Visual Studio: `Ctrl+Shift+B`

---

## 🎮 CONTROLS

### Keyboard + Mouse

**Explosions:**
- `1` - Große Explosion
- `2` - 4-fach Explosion
- `3` - Mini-Explosion
- `4` - Omega-Explosion
- `Q` (Hold) - Charge Explosion

**Movement (Fortnite-Style):**
- `W/A/S/D` - Move
- `Space` - Jump
- `Shift` - Sprint
- `Ctrl` - Slide
- `E` - Dash

### Gamepad

- `X/A` - Große Explosion
- `Y/Triangle` - 4-fach Explosion
- `B/Circle` - Mini-Explosion
- `A/X` - Omega-Explosion
- `LT` - Charge Explosion
- Left Stick - Move
- Right Stick - Camera

### Mobile (Xiaomi 11T Pro)

- Virtual Joystick (left) - Movement
- Virtual Buttons (right) - Explosions
- Swipe gestures - Dash/Slide

---

## 📱 ANDROID BUILD

```powershell
# In Unreal Editor:
# File → Package Project → Android → Android (ASTC)

# Output:
C:\NajikaTestEnvironment_UE5\Android\NajikaTest.apk

# Install:
adb install -r NajikaTest.apk
```

**Target Device:** Xiaomi 11T Pro
- Snapdragon 888
- 8GB RAM
- Android 12+

---

## 📂 PROJECT STRUCTURE

```
TestEnvironment_UE5/
├── NajikaTest.uproject          # UE5 Project File
├── Source/
│   └── NajikaTest/
│       ├── Public/
│       │   └── ExplosionClass.h       # ✅ Header
│       ├── Private/
│       │   └── ExplosionClass.cpp     # ✅ Implementation
│       └── NajikaTest.Build.cs        # ✅ Build Config
├── Config/
│   ├── DefaultEngine.ini        # ✅ Engine Settings
│   └── DefaultInput.ini         # ✅ Input Mappings
├── Content/
│   ├── Maps/                    # TODO: 10x10m Test Room
│   ├── Blueprints/              # TODO: BP_ExplosionCharacter
│   └── Materials/               # TODO: Explosion VFX
├── Docs/
│   ├── README.md               # This file
│   └── SETUP_WINDOWS.md        # Detailed setup guide
├── SETUP_PROJECT.ps1           # Auto-setup script
└── README.md
```

---

## 🔄 WORKFLOW

### Current Status: Phase 1 Complete

```
[✅] Phase 1: Core Explosion Implementation
  ✅ ExplosionClass.h
  ✅ ExplosionClass.cpp
  ✅ Build Configuration
  ✅ Input Mappings
  ✅ Android Settings

[🔄] Phase 2: Testing & Iteration
  ⏳ Create 10x10m Test Room
  ⏳ Blueprint Character Setup
  ⏳ Visual Effects (Particles)
  ⏳ Sound Effects
  ⏳ UI (Exhaustion/Charge Display)

[📋] Phase 3: Movement System
  ⏳ Fortnite-Style Movement
  ⏳ Sprint/Slide/Dash
  ⏳ Vault/Mantle/Wall-Climb

[📋] Phase 4: Additional Mechanics
  ⏳ Signature Paths
  ⏳ Oregon-Engine Mini
  ⏳ Slime-Arena Prototype

[📋] Phase 5: Export to Full Game
  ⏳ Validated mechanics → NajikaHandyspiel_UE5
```

---

## 🎯 NEXT STEPS

1. **Jetzt testen:**
   ```powershell
   # Öffne Projekt
   C:\NajikaTestEnvironment_UE5\NajikaTest.uproject

   # Create Test Level
   # Place Explosion Character
   # Press Alt+P to Play
   # Test Keys 1-4 und Q
   ```

2. **Visual Effects hinzufügen:**
   - Particle Systems für Explosionen
   - Camera Shake
   - Sound Effects

3. **Movement System:**
   - Fortnite-Style Character Controller
   - Sprint → Slide → Dash Combos

4. **Mobile Testing:**
   - Build APK
   - Deploy to Xiaomi 11T Pro
   - Test Touch Controls

5. **Export:**
   - Validierte Mechaniken dokumentieren
   - Export zu Full Game Project

---

## 🔐 BACKEND INTEGRATION

Test Environment verbindet zu deinem PC:

```yaml
secure-hub: http://127.0.0.1:5010  # Health, QR, Vault
game-core:  http://127.0.0.1:7010  # Game Server
```

**Zero-Trust:** Services binden NUR zu 127.0.0.1!

---

## 📖 DOKUMENTATION

- **Vollständige Anleitung:** `Docs/SETUP_WINDOWS.md`
- **PDF Spec:** `alles wissen/zip/handyspiel und später uefn.pdf`
- **Mobile App:** `DOCS/MOBILE_APP_ARCHITECTURE.md`

---

## 🚀 COMMIT HISTORY

- `5b8e027` - Initial UE5 project structure + ExplosionClass.h
- `df83972` - Complete implementation + Windows setup + Android config

---

**Model**: 2 (Test Environment)
**Status**: Phase 1 Complete ✅
**Next**: Phase 2 Testing 🔄
**Target**: Xiaomi 11T Pro (Android)
**Created**: 2025-11-11
