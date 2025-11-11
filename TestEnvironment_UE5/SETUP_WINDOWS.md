# 🎮 NAJIKA TEST ENVIRONMENT - WINDOWS SETUP

## 📍 Model 2 - Test Environment (10x10m)

**Ziel**: Teste Digivice Features + Prototype Handyspiel Mechaniken

---

## 🚀 INSTALLATION (Windows)

### 1. Unreal Engine 5.4 installieren

```powershell
# Download Epic Games Launcher
# https://www.epicgames.com/store/download

# In Epic Games Launcher:
# - Library → Engine Versions → + → UE 5.4
```

### 2. Projekt zu Windows kopieren

```powershell
# Kopiere dieses Projekt nach:
C:\NajikaTestEnvironment_UE5\

# Struktur sollte sein:
C:\NajikaTestEnvironment_UE5\
├── NajikaTest.uproject
├── Source\
│   └── NajikaTest\
│       ├── Public\
│       │   └── ExplosionClass.h
│       └── Private\
│           └── ExplosionClass.cpp
├── Config\
├── Content\
└── Docs\
```

### 3. Visual Studio 2022 installieren

```powershell
# Download VS 2022 Community (kostenlos)
# https://visualstudio.microsoft.com/downloads/

# Workloads installieren:
☑ Game development with C++
☑ .NET desktop development
```

### 4. Projekt öffnen

```powershell
# Rechtsklick auf NajikaTest.uproject
# → "Generate Visual Studio project files"

# Dann: Doppelklick auf NajikaTest.uproject
# → Öffnet Unreal Editor
```

---

## 🎯 WAS IST DRIN?

### ✅ Explosion Class (Fertig implementiert!)

**Features:**
- ✅ Große Explosion (Riesen-AoE, 8s Exhaustion)
- ✅ 4-fach Explosion (Serial, 4x kleinere Explosionen)
- ✅ Mini-Explosion (Spam-fähig, 0.5s Cooldown)
- ✅ Omega-Explosion (600% AoE, 30s -50% Regen)
- ✅ Charging System (Hold to charge → Release für Power)
- ✅ Exhaustion System (Cooldown nach großen Explosionen)
- ✅ Talent System (+35% Explosion, -17.5% andere Skills)

**Hard Rule #3**: Explosion ≠ Weave - Standalone Class!

---

## 🛠️ BUILD & TEST

### Build Projekt

```powershell
# In Unreal Editor:
# Tools → Refresh Visual Studio Project
# Build → Build Solution (Ctrl+Shift+B)
```

### Test in Editor

```powershell
# 1. Öffne NajikaTest.uproject
# 2. Erstelle neuen Level (10x10m Test Room)
# 3. Place Explosion Character in Level
# 4. Play (Alt+P)

# Input Bindings (in Project Settings):
# - GrosseExplosion: 1
# - VierfachExplosion: 2
# - MiniExplosion: 3
# - OmegaExplosion: 4
# - ChargeExplosion: Hold Q
```

---

## 📱 ANDROID BUILD (Xiaomi 11T Pro)

### Prerequisites

```powershell
# 1. Android Studio installieren
# https://developer.android.com/studio

# 2. In Unreal Editor:
# Edit → Project Settings → Platforms → Android
# ☑ Configure Now (installiert Android SDK/NDK)

# 3. USB Debugging auf Xiaomi aktivieren:
# Settings → About Phone → MIUI Version (7x tippen)
# Settings → Additional Settings → Developer Options
# ☑ USB Debugging
```

### Build APK

```powershell
# In Unreal Editor:
# File → Package Project → Android → Android (ASTC)

# Output:
# C:\NajikaTestEnvironment_UE5\Android\NajikaTest.apk
```

### Install auf Handy

```powershell
# USB-Kabel anschließen
# ADB installieren falls noch nicht:
# choco install adb (via Chocolatey)

# Dann:
adb devices  # Check ob Handy erkannt
adb install -r NajikaTest.apk
```

---

## 🔄 WORKFLOW: Test Environment → Full Game

```
┌─────────────────────────────────────────────────┐
│   TEST ENVIRONMENT (10x10m)                    │
│   C:\NajikaTestEnvironment_UE5\                │
│                                                 │
│   ✅ Prototype Mechaniken hier!                │
│   ✅ Teste Digivice Features                   │
│   ✅ Kleine, schnelle Tests                    │
│   ✅ Alles muss hier funktionieren             │
└─────────────────────────────────────────────────┘
                    ⬇ EXPORT
┌─────────────────────────────────────────────────┐
│   FULL GAME (500x500m)                         │
│   C:\NajikaHandyspiel_UE5\                     │
│                                                 │
│   🎮 Komplettes Survival-RPG                   │
│   🌍 500x500m Open World                       │
│   👥 Online Multiplayer                        │
│   🎯 Oregon-Engine (Procedural Events)         │
│   ⚔️ Crafting, Combat, Slime-Arena             │
└─────────────────────────────────────────────────┘
```

---

## 📋 TODO für Test Environment

### Phase 1: Core Testing (CURRENT)
- [x] Explosion Class implementiert
- [ ] 10x10m Test Room (Blueprint)
- [ ] Basic Character Controller
- [ ] Movement System (Fortnite-Style)
- [ ] Debug UI (Exhaustion, Charge, Talents)

### Phase 2: Digivice Features Testing
- [ ] Najika Voice Integration (Megumin Clone)
- [ ] Backend Connection (najika_server.py)
- [ ] Terminal Module (Remote PC Control)
- [ ] Browser Module (WebView)

### Phase 3: Handyspiel Prototyping
- [ ] Signature Paths (Schwert, Speer, Axt, etc.)
- [ ] Oregon-Engine Mini (Procedural Events)
- [ ] Slime-Arena Prototype (Section 2.7!)
- [ ] Crafting Pipeline (Herbs, Alchemy)

### Phase 4: Mobile Testing
- [ ] Android Build Pipeline
- [ ] Deploy to Xiaomi 11T Pro
- [ ] Performance Testing
- [ ] Touch Controls

---

## 🎯 NÄCHSTE SCHRITTE

1. **Jetzt sofort**: Öffne Projekt in UE5 Editor
2. **Teste Explosion Class**: Erstelle Test Level, place Character
3. **Debug & Tune**: Teste alle 4 Explosion-Varianten
4. **Add Movement**: Fortnite-Style (Sprint, Slide, Dash)
5. **Export validated mechanics** zu Full Game

---

## 🔐 SECURE-HUB INTEGRATION

Test Environment verbindet zu deinem PC Backend:

```yaml
secure-hub: http://127.0.0.1:5010  # Health, QR, Vault
game-core:  http://127.0.0.1:7010  # Game Server
```

**Zero-Trust**: Services binden ONLY zu 127.0.0.1!

---

## 📞 SUPPORT

Bei Problemen:
1. Check UE5 Output Log (Window → Developer Tools → Output Log)
2. Check Visual Studio Build Errors
3. Check Android Logcat (für Mobile)

---

**Erstellt**: 2025-11-11
**Model**: 2 (Test Environment)
**Status**: Ready to Test! 🚀
