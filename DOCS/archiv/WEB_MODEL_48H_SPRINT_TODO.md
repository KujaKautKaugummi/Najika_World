# ⚡ WEB MODEL - 48H SPRINT TODO (SIMPLIFIED)

**Repository:** https://github.com/KujaKautKaugummi/Najika_World.git
**Branch:** `claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX`

**KRITISCH:** Dies ist 48H SPRINT MODE - NUR DAS NÖTIGSTE!

**Ziel:** Beta APK in 48 Stunden!

---

## ⚠️ SIMPLIFIED SCOPE

**Phase 0-8:** ✅ BEREITS FERTIG (38.408+ Zeilen)

**Phase 9-15 SIMPLIFIED:**
- **NUR für Beta APK nötig**
- **Keine perfectionism**
- **Schnell & funktional**

---

## 🔥 PHASE 9: NajikaVoiceSystem Plugin (SIMPLIFIED)

**Target:** ~1.000 Zeilen (statt 2.500) - Nur Basics!

### Was du erstellen musst:

```
UE5_Implementation/Plugins/NajikaVoiceSystem/
├── NajikaVoiceSystem.uplugin
├── Resources/Icon128.png (placeholder OK)
└── Source/NajikaVoiceSystem/
    ├── NajikaVoiceSystem.Build.cs
    ├── Public/
    │   ├── NajikaVoiceSystemModule.h
    │   ├── NajikaVoiceCapture.h         (MIC input ONLY)
    │   ├── NajikaVoicePlayback.h        (Audio out ONLY)
    │   └── NajikaVoiceComponent.h       (Actor Component)
    └── Private/
        ├── NajikaVoiceSystemModule.cpp
        ├── NajikaVoiceCapture.cpp       (~200 lines - basic mic)
        ├── NajikaVoicePlayback.cpp      (~200 lines - basic playback)
        └── NajikaVoiceComponent.cpp     (~200 lines - PTT button)
```

**SKIP für Beta:**
- ❌ Whisper AI Integration (Backend macht das!)
- ❌ Voice Encoding (raw audio OK)
- ❌ Echo Cancellation
- ❌ Noise Suppression
- ❌ Voice Activity Detection

**MUST HAVE für Beta:**
- ✅ Microphone Capture (basic)
- ✅ Push-to-Talk (V key)
- ✅ Send Audio to Backend (WebSocket)
- ✅ Receive Audio from Backend
- ✅ Play Audio

**Dependencies (Build.cs):**
```csharp
"Core", "CoreUObject", "Engine", "AudioCapture", "AudioMixer", "WebSockets"
```

**Expected:** ~600 Zeilen C++ (statt 2.500)

---

## 🔥 PHASE 10: Blueprint Creation Guide (SIMPLIFIED)

**Target:** ~800 Zeilen (statt 2.000) - Nur Essentials!

### Datei:
```
UE5_Implementation/BLUEPRINT_CREATION_GUIDE_SIMPLIFIED.md
```

**Inhalt (NUR DAS NÖTIGSTE!):**

### 1. Core Blueprints (3 only!)
- **BP_NajikaCharacter** (minimal setup)
  - Camera + Spring Arm
  - Movement settings
  - Animation Blueprint link
- **BP_NajikaPlayerController** (minimal)
  - Input setup (WASD, V for PTT)
  - Widget spawn
- **BP_NajikaGameMode** (minimal)
  - Set defaults only

### 2. UI Widgets (3 only!)
- **WBP_HUD** (minimal)
  - Health bar
  - Chat button
  - Menu button
- **WBP_Chat** (minimal)
  - Input box
  - Message display
- **WBP_Menu** (minimal)
  - Resume
  - Exit

### 3. Project Settings (essential only!)
- Maps & Modes
- Input Mappings (WASD + V)
- Android Verify

**SKIP:**
- ❌ Inventory Widget
- ❌ Status Widget
- ❌ Complex UI layouts
- ❌ Level setup (placeholder floor OK)

**Expected:** ~800 Zeilen Guide

---

## 🔥 PHASE 11: SKIP (Assets handled separately)

**WIR HABEN BEREITS:**
- Asset Acquisition Guide ✅
- User macht Najika Avatar ✅
- Mixamo für Animations ✅
- Freesound für Audio ✅

**Du musst NICHTS für Assets schreiben!**

---

## 🔥 PHASE 12: Copy & Setup Scripts (CRITICAL!)

**Target:** ~300 Zeilen PowerShell

### Datei:
```
UE5_Implementation/COPY_TO_UE5_PROJECT.ps1
```

**Muss kopieren:**
1. NajikaBackendClient Plugin → `C:\NajikaDigivice_UE5\NajikaDigivice\Plugins\`
2. NajikaVoiceSystem Plugin → `C:\NajikaDigivice_UE5\NajikaDigivice\Plugins\`
3. Source Code (Public/*.h, Private/*.cpp) → `Source\NajikaDigivice\`
4. Tests → `Source\NajikaDigivice\Tests\`
5. Build Scripts → `Build\`
6. Docs → Root

**Script Struktur:**
```powershell
# Verify paths
if (-not (Test-Path $TargetPath)) { exit 1 }

# Copy Plugins
Copy-Item -Path "Plugins\NajikaBackendClient" -Destination "$TargetPath\Plugins\" -Recurse -Force
Copy-Item -Path "Plugins\NajikaVoiceSystem" -Destination "$TargetPath\Plugins\" -Recurse -Force

# Copy Source
Copy-Item -Path "Source\NajikaDigivice\Public\*.h" -Destination "$TargetPath\Source\NajikaDigivice\Public\" -Force
Copy-Item -Path "Source\NajikaDigivice\Private\*.cpp" -Destination "$TargetPath\Source\NajikaDigivice\Private\" -Force

# Copy Tests
Copy-Item -Path "Source\NajikaDigivice\Tests\" -Destination "$TargetPath\Source\NajikaDigivice\Tests\" -Recurse -Force

# Copy Build Scripts
Copy-Item -Path "Build\*.bat" -Destination "$TargetPath\Build\" -Force

# Update Build.cs (add plugins to dependencies)
# Generate Project Files
& "C:\Program Files\Epic Games\UE_5.6\Engine\Build\BatchFiles\GenerateProjectFiles.bat" -project="$TargetPath\NajikaDigivice.uproject"

Write-Host "✅ COPY COMPLETE!"
```

**Expected:** ~200 Zeilen

---

## 🔥 PHASE 13: VS Compilation Guide (SIMPLIFIED)

**Target:** ~400 Zeilen (statt 800)

### Datei:
```
UE5_Implementation/VISUAL_STUDIO_COMPILATION_GUIDE_SIMPLIFIED.md
```

**Inhalt (NUR Essentials!):**

### 1. Open Solution
- Open `NajikaDigivice.sln`
- Config: Development Editor, Win64

### 2. Build Plugins
- Right-click NajikaBackendClient → Build
- Right-click NajikaVoiceSystem → Build
- Wait for success

### 3. Build Game Module
- Right-click NajikaDigivice → Build
- Wait 2-5 minutes

### 4. Verify
- Check Binaries/Win64/ for DLLs

### 5. Common Errors (Top 5 only!)
- Include file not found → Build plugins first
- Unresolved external → Check dependencies in Build.cs
- (3 more)

**SKIP:**
- ❌ Screenshots (text only)
- ❌ Detailed error explanations
- ❌ Advanced troubleshooting

**Expected:** ~400 Zeilen

---

## 🔥 PHASE 14: Android Build Guide (SIMPLIFIED)

**Target:** ~500 Zeilen (statt 1.200)

### Datei:
```
UE5_Implementation/ANDROID_BUILD_DEPLOYMENT_GUIDE_SIMPLIFIED.md
```

**Inhalt (NUR Essentials!):**

### 1. Prerequisites Check
- Android SDK installed?
- NDK installed?
- Device connected?

### 2. Project Settings
- Package Name: com.najika.digivice
- Min SDK: 29, Target SDK: 34
- Build for ARM64: YES

### 3. Build APK
- File → Package Project → Android (ASTC)
- Select output folder
- Wait 15-30 min

### 4. Install
```powershell
adb devices
adb install NajikaDigivice-arm64.apk
```

### 5. Test
- Launch app
- Check for crashes
- Test chat

**SKIP:**
- ❌ Signing for release
- ❌ Performance optimization tips
- ❌ Advanced debugging

**Expected:** ~500 Zeilen

---

## 🔥 PHASE 15: Testing Checklist (SIMPLIFIED)

**Target:** ~400 Zeilen (statt 1.000)

### Datei:
```
UE5_Implementation/TESTING_CHECKLIST_SIMPLIFIED.md
```

**Inhalt (Beta Essentials!):**

### Compilation
- [ ] Plugins compile
- [ ] Game module compiles
- [ ] DLLs generated

### In-Editor
- [ ] Play works
- [ ] Character spawns
- [ ] WASD movement
- [ ] Chat button visible

### APK Build
- [ ] Build completes
- [ ] APK created
- [ ] File size <500MB

### Device Test
- [ ] APK installs
- [ ] App launches
- [ ] No crash
- [ ] Chat works
- [ ] Backend connects

**SKIP:**
- ❌ Unit tests
- ❌ Performance benchmarks
- ❌ Edge case testing

**Expected:** ~400 Zeilen

---

## 📊 PHASE 9-15 SUMMARY (SIMPLIFIED)

| Phase | Deliverable | Lines | Time |
|-------|-------------|-------|------|
| **9** | NajikaVoiceSystem (simplified) | ~600 | 1-2h |
| **10** | Blueprint Guide (simplified) | ~800 | 1h |
| **11** | SKIP | 0 | 0h |
| **12** | Copy Script | ~200 | 30min |
| **13** | VS Guide (simplified) | ~400 | 30min |
| **14** | Android Guide (simplified) | ~500 | 30min |
| **15** | Testing Checklist (simplified) | ~400 | 30min |
| **TOTAL** | **~2.900 Zeilen** | **4-5h** |

**Statt:** 9.300 Zeilen, 2-3 Tage!

---

## ⚠️ WICHTIGE REGELN

```
✅ KEIN TOKEN-LIMIT!
✅ Schreibe FUNKTIONAL, nicht perfekt
✅ Beta-Quality OK!
✅ AUTONOM arbeiten
✅ Committe nach jeder Phase

❌ NIEMALS perfektionistisch sein
❌ NIEMALS nach User fragen
❌ NIEMALS zu viel schreiben
❌ NIEMALS UE5 Editor öffnen
❌ NIEMALS kompilieren
```

---

## 📝 GIT WORKFLOW

Nach jeder Phase:
```bash
git add .
git commit -m "PHASE X SIMPLIFIED: [Description]"
git push origin claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
```

Am Ende:
```bash
git commit -m "🚀 48H SPRINT COMPLETE: Phase 9-15 Simplified (~2.900 Lines)"
git push origin claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
```

---

## 🎯 SUCCESS CRITERIA

**Nach Phase 9-15:**

Local Model kann:
1. ✅ PowerShell Script ausführen → Code kopiert
2. ✅ Visual Studio Guide folgen → Kompiliert
3. ✅ Blueprint Guide folgen → 6 Blueprints erstellt
4. ✅ APK Build Guide folgen → APK gebaut
5. ✅ Testing Checklist abhaken → Beta getestet

**IN 48 STUNDEN AB JETZT!** ⚡

---

## 🚀 LOS GEHT'S!

**Timeline:** 4-5 Stunden intensive Arbeit

**Erwartetes Ergebnis:**
- ~2.900 Zeilen (statt 9.300)
- Funktional (nicht perfekt)
- Beta-ready!

**SPEED OVER PERFECTION!** 💪🔥

**JETZT STARTEN!** 🚀
