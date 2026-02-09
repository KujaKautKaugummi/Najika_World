# Android Build & Deployment Guide - Najika UE5 Project

**Version:** 1.0
**Last Updated:** 2025-01-13
**Target Device:** Xiaomi 11T Pro (and compatible Android devices)
**UE5 Version:** 5.3+
**Android Version:** Android 11+ (API Level 30+)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Android SDK/NDK Installation](#android-sdkndk-installation)
4. [UE5 Android Platform Setup](#ue5-android-platform-setup)
5. [Project Configuration](#project-configuration)
6. [Building the APK](#building-the-apk)
7. [Signing & Distribution](#signing--distribution)
8. [Device Deployment](#device-deployment)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)
11. [Xiaomi 11T Pro Specific Settings](#xiaomi-11t-pro-specific-settings)

---

## Overview

### Build Pipeline

```
UE5 Project (C++ + Blueprints)
    ↓
Compile C++ for ARM64
    ↓
Package Assets (textures, audio, etc.)
    ↓
Create APK with Gradle
    ↓
Sign APK with Keystore
    ↓
Deploy to Device via ADB
    ↓
Launch on Xiaomi 11T Pro
```

### Target Specifications

| Component | Specification |
|-----------|---------------|
| **Device** | Xiaomi 11T Pro |
| **Chipset** | MediaTek Dimensity 1200-Ultra |
| **GPU** | Mali-G77 MC9 |
| **RAM** | 8 GB / 12 GB |
| **Android Version** | Android 11 (upgradable to 13) |
| **Display** | 6.67" AMOLED, 120Hz, 1080x2400 |
| **Architecture** | ARM64-v8a |

### Build Types

| Build Type | Purpose | Size | Performance | Use Case |
|------------|---------|------|-------------|----------|
| **Development** | Testing | ~500 MB | Medium | Daily testing, debugging |
| **Shipping** | Production | ~300 MB | High | Release to users |
| **Distribution** | Store upload | ~350 MB | High | Google Play Store |

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Unreal Engine** | 5.3+ | Game engine |
| **Android Studio** | 2021.3.1+ (Electric Eel) | SDK/NDK manager |
| **Java JDK** | 11 or 17 | Required by Gradle |
| **Python** | 3.9+ | Build scripts |
| **ADB** | Latest | Device communication |

### Hardware Requirements

**Development PC:**
- **OS:** Windows 10/11 (64-bit)
- **CPU:** 8+ cores (for fast builds)
- **RAM:** 32 GB recommended (16 GB minimum)
- **Storage:** 100 GB free SSD space
- **USB:** USB 3.0 port for device connection

**Android Device (Xiaomi 11T Pro):**
- **Developer Options:** Enabled
- **USB Debugging:** Enabled
- **Install from Unknown Sources:** Enabled
- **Battery:** Fully charged (builds can take time)

### Network Requirements

- Stable internet for downloading SDK/NDK (~10 GB)
- USB cable for device connection (USB-C for Xiaomi 11T Pro)

---

## Android SDK/NDK Installation

### Step 1: Download Android Studio

1. Go to https://developer.android.com/studio
2. Download **Android Studio Electric Eel** or newer
3. Run the installer:
   - **Windows:** `android-studio-2021.3.1.17-windows.exe`
4. Follow installation wizard:
   - Install Type: **Standard**
   - Components: Select all
   - Install Location: `C:\Program Files\Android\Android Studio`

### Step 2: Install Android SDK

1. Launch Android Studio
2. Skip creating a project (click **More Actions > SDK Manager**)
3. **SDK Platforms** tab:
   - Check **Android 13.0 (Tiramisu)** API Level 33
   - Check **Android 12.0 (S)** API Level 31
   - Check **Android 11.0 (R)** API Level 30
   - Click **Apply** to download

4. **SDK Tools** tab:
   - Check **Android SDK Build-Tools 33** (or latest)
   - Check **NDK (Side by side)** version **25.1.8937393** (recommended)
   - Check **CMake** version 3.22.1
   - Check **Android SDK Command-line Tools**
   - Check **Android Emulator** (optional, for testing without device)
   - Check **Android SDK Platform-Tools** (includes ADB)
   - Click **Apply** to download (~8 GB, takes 15-30 minutes)

### Step 3: Configure Environment Variables

**Windows:**

1. Press `Win + X` → **System**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Under **System variables**, click **New**:

   - **Variable name:** `ANDROID_HOME`
   - **Variable value:** `C:\Users\YourUsername\AppData\Local\Android\Sdk`
   - Click **OK**

5. Click **New** again:
   - **Variable name:** `ANDROID_NDK_ROOT`
   - **Variable value:** `C:\Users\YourUsername\AppData\Local\Android\Sdk\ndk\25.1.8937393`
   - Click **OK**

6. Edit **Path** variable:
   - Select **Path** → **Edit**
   - Click **New** and add: `%ANDROID_HOME%\platform-tools`
   - Click **New** and add: `%ANDROID_HOME%\tools`
   - Click **OK** on all dialogs

### Step 4: Verify Installation

Open **Command Prompt** and run:

```batch
adb --version
```

Expected output:
```
Android Debug Bridge version 1.0.41
Version 34.0.4-10411341
```

Check SDK location:
```batch
echo %ANDROID_HOME%
```

Expected output:
```
C:\Users\YourUsername\AppData\Local\Android\Sdk
```

Check NDK:
```batch
dir "%ANDROID_NDK_ROOT%"
```

Should show NDK files.

### Step 5: Install Java JDK

**Check if Java is installed:**
```batch
java -version
```

**If not installed:**

1. Download **OpenJDK 17** from https://adoptium.net/
2. Run installer
3. Set `JAVA_HOME` environment variable:
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Eclipse Adoptium\jdk-17.0.5.8-hotspot`

4. Verify:
   ```batch
   java -version
   ```

   Expected:
   ```
   openjdk version "17.0.5" 2022-10-18
   ```

---

## UE5 Android Platform Setup

### Step 1: Install Android Platform Support in UE5

1. Open **Epic Games Launcher**
2. Go to **Unreal Engine > Library**
3. Find **UE 5.3** → Click the dropdown arrow
4. Click **Options**
5. Check **Android**
6. Click **Apply** (downloads ~2 GB)
7. Wait for installation to complete

### Step 2: Configure UE5 Android Settings

1. Launch **Unreal Engine 5**
2. Open your **NajikaDigivice** project
3. Go to **Edit > Project Settings**
4. Search for "Android" in the search box

#### Android SDK Configuration

Navigate to **Platforms > Android SDK**:

1. **SDK API Level:** `android-33` (or latest)
2. **NDK API Level:** `android-30` (minimum for UE5.3)
3. **Android SDK Path:**
   ```
   C:\Users\YourUsername\AppData\Local\Android\Sdk
   ```
   Click **Browse** if not auto-detected

4. **Android NDK Path:**
   ```
   C:\Users\YourUsername\AppData\Local\Android\Sdk\ndk\25.1.8937393
   ```

5. **Java Path:**
   ```
   C:\Program Files\Eclipse Adoptium\jdk-17.0.5.8-hotspot
   ```

6. Click **Validate** buttons to ensure all paths are correct
   - ✅ Green checkmarks should appear next to each path

### Step 3: Accept Android SDK Licenses

In UE5 Project Settings:

1. Scroll to **Platforms > Android SDK**
2. Click **Accept SDK License**
3. A command window opens
4. Type `y` and press Enter to accept all licenses
5. Wait for completion

---

## Project Configuration

### Step 1: Android Platform Settings

In **Project Settings**, navigate to **Platforms > Android**:

#### Package Settings

| Setting | Value | Notes |
|---------|-------|-------|
| **Package Name** | `com.najika.digivice` | Unique identifier (reverse domain) |
| **Store Version** | `1` | Increment with each release |
| **Store Version Offset (arm64)** | `0` | Leave as default |
| **Application Display Name** | `Najika Digivice` | Name shown to users |
| **Version Display Name** | `1.0.0` | User-facing version |
| **Min SDK Version** | `30` | Android 11+ |
| **Target SDK Version** | `33` | Android 13 |
| **Install Location** | `Auto` | Let system decide |

#### Build Settings

| Setting | Value | Notes |
|---------|-------|-------|
| **Build for ARM64** | ✅ Checked | Required for modern devices |
| **Build for x86-64** | ❌ Unchecked | Not needed for Xiaomi 11T Pro |
| **Build for ES31** | ✅ Checked | OpenGL ES 3.1 support |
| **Build for Vulkan** | ✅ Checked | Better performance on Xiaomi 11T Pro |
| **Support Vulkan Desktop** | ❌ Unchecked | Not needed |

#### APK Packaging

| Setting | Value | Notes |
|---------|-------|-------|
| **Package game data inside APK** | ✅ Checked (Development) | Single APK file |
|  | ❌ Unchecked (Shipping) | Use OBB for smaller APK |
| **Use ExternalFilesDir for UE4Game dir** | ✅ Checked | Modern Android storage |
| **Create OBB if data is too large** | ✅ Checked | Auto-create OBB if >100 MB |
| **Use Display Cutout** | ✅ Checked | Support notches |

#### Permissions

Navigate to **Platforms > Android > Advanced APK Packaging**:

**Required Permissions (check these):**
- ✅ `INTERNET` - Backend communication
- ✅ `ACCESS_NETWORK_STATE` - Check network status
- ✅ `RECORD_AUDIO` - Voice chat (NajikaVoiceSystem)
- ✅ `MODIFY_AUDIO_SETTINGS` - Voice chat
- ✅ `WAKE_LOCK` - Prevent sleep during gameplay
- ✅ `VIBRATE` - Haptic feedback (optional)

**Optional Permissions:**
- `CAMERA` - If adding AR features
- `READ_EXTERNAL_STORAGE` - If loading user files
- `WRITE_EXTERNAL_STORAGE` - If saving to SD card

#### Graphics Settings

Navigate to **Platforms > Android > Rendering**:

| Setting | Value | Notes |
|---------|-------|-------|
| **Mobile HDR** | ✅ Checked | Better visuals on AMOLED |
| **Support Mobile Multi-View** | ✅ Checked | Performance boost |
| **Mobile MSAA** | `4x` | Anti-aliasing |
| **Mobile Shader Quality** | `High` | Xiaomi 11T Pro can handle it |

#### Icon & Splash Screen

Navigate to **Platforms > Android > Icons**:

**App Icon:**
1. Prepare icons at these sizes:
   - `xxxhdpi`: 192x192 px
   - `xxhdpi`: 144x144 px
   - `xhdpi`: 96x96 px
   - `hdpi`: 72x72 px
   - `mdpi`: 48x48 px

2. In Project Settings:
   - **Icon xxxhdpi:** Browse to your 192x192 icon PNG
   - **Icon xxhdpi:** Browse to your 144x144 icon PNG
   - etc.

**Splash Screen:**
- **Launch Screen Image:** Browse to your splash screen image (1080x2400 for Xiaomi 11T Pro)

### Step 2: Input Configuration for Mobile

Navigate to **Project Settings > Engine > Input**:

**Add Mobile Touch Interface:**

1. **Default Touch Interface:** `/Engine/MobileResources/HUD/DefaultVirtualJoysticks.DefaultVirtualJoysticks`
   - Or create custom touch controls

2. **Always Show Touch Interface:** ✅ Checked (for testing)

**Adjust Touch Sensitivity:**

3. **Initial Button Repeat Delay:** `0.2`
4. **Button Repeat Delay:** `0.1`

### Step 3: Audio Configuration

Navigate to **Project Settings > Platforms > Android > Audio**:

| Setting | Value | Notes |
|---------|-------|-------|
| **Sample Rate** | `48000` | Matches NajikaVoiceSystem |
| **Callback Buffer Size** | `1024` | Low latency for voice chat |
| **Number of Buffers to Queue** | `3` | Balance between latency and stability |

### Step 4: Network Configuration

Since we're using `localhost:8000` backend on device:

**Option A: Use Android Port Forwarding (Recommended for Testing)**

After deploying APK, run on PC:
```batch
adb reverse tcp:8000 tcp:8000
```

This forwards device's `localhost:8000` to PC's `localhost:8000`.

**Option B: Use PC's Local IP Address**

In `NajikaBackendClient` code, change BaseURL from:
```cpp
BaseURL = TEXT("http://localhost:8000");
```

To:
```cpp
BaseURL = TEXT("http://192.168.1.100:8000");  // Your PC's local IP
```

Find your PC's IP:
```batch
ipconfig
```

Look for **IPv4 Address** under your network adapter.

---

## Building the APK

### Build Method 1: Package from UE5 Editor (Recommended)

#### Step 1: Select Platform

1. In UE5 Editor toolbar, click **Platforms** dropdown
2. Select **Android > Android (ASTC)**
   - ASTC: Adaptive Scalable Texture Compression (best for Xiaomi 11T Pro)

#### Step 2: Start Packaging

1. **Platforms > Android > Package Project**
2. Browse to output folder (e.g., `C:\Builds\NajikaDigivice\Android`)
3. Click **Select Folder**

#### Step 3: Monitor Build Progress

A build window appears showing:
```
Cooking content for Android...
Compiling shaders for Android...
Packaging (Android (ASTC))...
Building APK...
```

**Build time expectations:**
- **First build:** 45-90 minutes
- **Incremental builds:** 10-20 minutes

**Output:**
- `Install_NajikaDigivice_arm64.bat` - Installation script
- `NajikaDigivice.apk` - The Android package
- `NajikaDigivice.obb` - Data file (if assets > 100 MB)

### Build Method 2: Package from Command Line

For automated builds or CI/CD:

```batch
"C:\Program Files\Epic Games\UE_5.3\Engine\Build\BatchFiles\RunUAT.bat" ^
  BuildCookRun ^
  -project="C:\Path\To\NajikaDigivice\NajikaDigivice.uproject" ^
  -platform=Android ^
  -clientconfig=Development ^
  -cook ^
  -stage ^
  -package ^
  -build ^
  -pak ^
  -archive ^
  -archivedirectory="C:\Builds\NajikaDigivice" ^
  -utf8output
```

**Parameters explained:**
- `-platform=Android` - Target platform
- `-clientconfig=Development` - Build configuration (Development/Shipping)
- `-cook` - Cook content
- `-stage` - Stage files
- `-package` - Create APK
- `-build` - Compile C++ code
- `-pak` - Package assets into .pak files
- `-archive` - Copy to archive directory

### Build Method 3: Visual Studio (Advanced)

For C++ developers who want control:

1. In Visual Studio, change configuration to:
   - **Configuration:** `Development`
   - **Platform:** `Android`

2. **Build > Build Solution**

3. After C++ compilation, use Method 1 or 2 to package

### Understanding Build Configurations

| Configuration | Optimizations | Logging | Debug Symbols | APK Size | Use Case |
|--------------|---------------|---------|---------------|----------|----------|
| **DebugGame** | None | Full | Yes | ~800 MB | Debugging crashes |
| **Development** | Medium | Medium | Partial | ~500 MB | Daily testing |
| **Shipping** | Maximum | Minimal | No | ~300 MB | Release to users |

**For testing:** Use **Development**
**For release:** Use **Shipping**

---

## Signing & Distribution

### Creating a Keystore (One-time Setup)

**IMPORTANT:** Keep your keystore file safe! If lost, you cannot update your app on Google Play.

#### Step 1: Generate Keystore

Open Command Prompt:

```batch
cd C:\Users\YourUsername\Documents
keytool -genkey -v -keystore najika-release.keystore -alias najika -keyalg RSA -keysize 2048 -validity 10000
```

**Prompts:**
```
Enter keystore password: [Create a strong password]
Re-enter new password: [Repeat password]
What is your first and last name? [Your name or company]
What is the name of your organizational unit? [Team name]
What is the name of your organization? [Company name]
What is the name of your City or Locality? [City]
What is the name of your State or Province? [State]
What is the two-letter country code for this unit? [US/DE/etc]
Is CN=..., OU=..., O=..., L=..., ST=..., C=... correct? [yes]
```

**Result:**
- File created: `C:\Users\YourUsername\Documents\najika-release.keystore`

**BACKUP THIS FILE IMMEDIATELY!**

#### Step 2: Configure UE5 to Use Keystore

In UE5 **Project Settings > Platforms > Android > Distribution Signing**:

1. **Keystore Filename:**
   ```
   C:\Users\YourUsername\Documents\najika-release.keystore
   ```

2. **Keystore Password:** [Your keystore password]

3. **Key Alias:** `najika`

4. **Key Password:** [Your key password - usually same as keystore password]

#### Step 3: Build Signed APK

1. Change build configuration to **Shipping**
2. **Platforms > Android > Package Project (for Distribution)**
3. Select output folder
4. UE5 builds and signs the APK automatically

**Output:**
- `NajikaDigivice-arm64.apk` (signed, ready for distribution)

### Google Play Store Preparation

#### Step 1: Create App Bundle (AAB)

Google Play prefers AAB format over APK:

In UE5 **Project Settings > Platforms > Android**:
- ✅ **Generate bundle (AAB)**

Rebuild:
- **Platforms > Android > Package Project (for Distribution)**

**Output:**
- `NajikaDigivice-arm64.aab`

#### Step 2: Upload to Google Play Console

1. Go to https://play.google.com/console
2. Create a new app
3. **Production > Create new release**
4. Upload `NajikaDigivice-arm64.aab`
5. Fill in store listing (description, screenshots, etc.)
6. Submit for review

---

## Device Deployment

### Prepare Xiaomi 11T Pro

#### Enable Developer Options

1. **Settings > About phone**
2. Tap **MIUI version** 7 times rapidly
3. Message appears: "You are now a developer!"

#### Enable USB Debugging

1. **Settings > Additional settings > Developer options**
2. Enable **USB debugging**
3. Enable **Install via USB**
4. Enable **USB debugging (Security settings)** (if available)

#### Connect Device

1. Connect Xiaomi 11T Pro to PC via USB-C cable
2. On device, a prompt appears: "Allow USB debugging?"
3. Check **Always allow from this computer**
4. Tap **OK**

### Verify ADB Connection

On PC, open Command Prompt:

```batch
adb devices
```

Expected output:
```
List of devices attached
abc12345    device
```

If shows `unauthorized`:
- Check device screen for prompt
- Re-accept USB debugging

### Install APK Methods

#### Method 1: Using Install Script (Easiest)

Navigate to build output folder:

```batch
cd C:\Builds\NajikaDigivice\Android
Install_NajikaDigivice_arm64.bat
```

This script automatically:
- Installs APK
- Installs OBB (if present)
- Grants permissions
- Launches the app

#### Method 2: Manual ADB Install

```batch
adb install -r C:\Builds\NajikaDigivice\Android\NajikaDigivice.apk
```

**Parameters:**
- `-r` - Reinstall (keeps data)
- `-g` - Grant all permissions

Full command with permissions:
```batch
adb install -r -g C:\Builds\NajikaDigivice\Android\NajikaDigivice.apk
```

**If using OBB file:**

```batch
adb push C:\Builds\NajikaDigivice\Android\main.1.com.najika.digivice.obb /sdcard/Android/obb/com.najika.digivice/
```

#### Method 3: Launch from UE5 Editor

1. In UE5 Editor, ensure device is connected
2. **Platforms > Android > Launch on [Your Device Name]**
3. UE5 automatically builds, installs, and launches

### Post-Installation

#### Grant Permissions Manually

If permissions weren't granted during install:

On device:
1. **Settings > Apps > Najika Digivice > Permissions**
2. Grant:
   - **Microphone** - Allow
   - **Phone** - Allow (if requested for device ID)

#### Setup Port Forwarding (for localhost backend)

On PC:
```batch
adb reverse tcp:8000 tcp:8000
```

This allows the app to connect to `http://localhost:8000` (your PC's backend).

**Verify forwarding:**
```batch
adb reverse --list
```

Expected:
```
tcp:8000 tcp:8000
```

### Launch App

**From ADB:**
```batch
adb shell am start -n com.najika.digivice/com.epicgames.unreal.GameActivity
```

**From Device:**
- Tap app icon on home screen or app drawer

---

## Performance Optimization

### Frame Rate Targets

Xiaomi 11T Pro supports 120Hz display. Configure in **Project Settings**:

Navigate to **Engine > Rendering > Default Settings**:
- **Frame Rate Limit:** `120` (to match display)
- **Use Fixed Frame Rate:** ❌ Unchecked (let it adapt)

### LOD (Level of Detail) Settings

For mobile performance, configure LODs:

Navigate to **Engine > Rendering > LOD Settings**:
- **Num LODs:** `4` (multiple quality levels)
- **LOD 0 Screen Size:** `1.0` (full detail when close)
- **LOD 1 Screen Size:** `0.5`
- **LOD 2 Screen Size:** `0.25`
- **LOD 3 Screen Size:** `0.1`

### Texture Streaming

Navigate to **Engine > Rendering > Textures**:
- **Texture Streaming:** ✅ Enabled
- **Texture Streaming Pool Size:** `3000` MB (Xiaomi 11T Pro has 8-12 GB RAM)

### Mobile Optimizations

Navigate to **Platforms > Android > Rendering**:

- **Mobile Multi-View:** ✅ Enabled (GPU optimization)
- **Mobile Pixel Projected Reflection:** ✅ Enabled
- **Support Software Occlusion Culling:** ✅ Enabled (CPU optimization)

### Vulkan vs OpenGL ES

Xiaomi 11T Pro (Mali-G77) performs better with **Vulkan**.

To force Vulkan:

In **Project Settings > Platforms > Android**:
- **Build for Vulkan:** ✅ Checked
- **Build for ES31:** ❌ Unchecked (disable OpenGL fallback for testing)

**For production, check both** to support more devices.

### Profiling on Device

#### Enable Stat Commands

On device, enable console:

In **Project Settings > Engine > Input > Console Keys**:
- Add console key (e.g., `Tilde`)

On device, tap screen with 3 fingers to open console, then type:

```
stat fps
```

Shows frame rate in top-right corner.

Other useful commands:
- `stat unit` - CPU/GPU/Frame time
- `stat game` - Game thread time
- `stat memory` - Memory usage
- `stat gpu` - GPU performance

#### Use Unreal Insights

For detailed profiling:

1. In UE5 Editor, **Window > Developer Tools > Unreal Insights**
2. On device, type in console:
   ```
   trace.start
   ```
3. Play for 30-60 seconds
4. Type:
   ```
   trace.stop
   ```
5. Files saved to device's internal storage
6. Pull trace file:
   ```batch
   adb pull /sdcard/Android/data/com.najika.digivice/files/UE5/Profiling/ C:\Traces\
   ```
7. Open `.utrace` file in Unreal Insights

---

## Troubleshooting

### Error: "Installation failed with error: INSTALL_FAILED_INSUFFICIENT_STORAGE"

**Cause:** Not enough space on device.

**Solution:**
1. Check device storage:
   ```batch
   adb shell df -h
   ```
2. Free up space (delete apps, clear cache)
3. Or install to SD card (if device has one):
   - In Project Settings > Android > APK Packaging
   - **Install Location:** `Prefer External`

### Error: "App not installed" (on device)

**Cause:** Conflicting signature (different keystore).

**Solution:**
1. Uninstall existing app:
   ```batch
   adb uninstall com.najika.digivice
   ```
2. Reinstall APK

### Error: "The application could not be installed: INSTALL_FAILED_UPDATE_INCOMPATIBLE"

**Cause:** Package name or signature mismatch.

**Solution:**
```batch
adb uninstall com.najika.digivice
adb install -r YourApp.apk
```

### Error: "App crashes immediately on launch"

**Cause:** Missing permissions or incompatible architecture.

**Solution:**

**Check logs:**
```batch
adb logcat | findstr "AndroidRuntime"
```

Look for errors like:
```
FATAL EXCEPTION: UnrealEngine
```

**Common fixes:**
- Rebuild with ARM64 architecture checked
- Grant all required permissions
- Ensure Min SDK version <= device's Android version

### Error: "Black screen on launch"

**Cause:** Shader compilation issues or graphics API mismatch.

**Solution:**

1. Force rebuild shaders:
   - In UE5, **File > Package Project > Cooking Settings**
   - Check **Share Material Shader Code**
   - Rebuild

2. Try OpenGL ES instead of Vulkan:
   - **Project Settings > Platforms > Android**
   - ✅ **Build for ES31**
   - ❌ **Build for Vulkan** (temporarily disable)
   - Rebuild

### Error: "Voice chat not working"

**Cause:** Microphone permission not granted or audio settings incorrect.

**Solution:**

1. Grant microphone permission:
   ```batch
   adb shell pm grant com.najika.digivice android.permission.RECORD_AUDIO
   ```

2. Check audio settings in **Project Settings > Platforms > Android > Audio**

3. Test microphone:
   ```batch
   adb shell
   su
   toybox microphone record /sdcard/test.wav
   # Press Ctrl+C after 3 seconds
   exit
   adb pull /sdcard/test.wav
   # Play test.wav on PC to verify recording works
   ```

### Error: "Cannot connect to backend (localhost:8000)"

**Cause:** Port forwarding not set up or backend not running.

**Solution:**

1. Verify backend is running on PC:
   ```batch
   curl http://localhost:8000/api/health
   ```

2. Setup port forwarding:
   ```batch
   adb reverse tcp:8000 tcp:8000
   ```

3. Test from device:
   ```batch
   adb shell
   curl http://localhost:8000/api/health
   ```

   Should return JSON response.

4. If still fails, use PC's local IP:
   - Find PC IP: `ipconfig` → IPv4 Address
   - Change NajikaBackendClient BaseURL to `http://192.168.1.100:8000`
   - Ensure PC firewall allows port 8000

### Performance: Low frame rate (< 30 FPS)

**Cause:** Settings too high for device, or thermal throttling.

**Solution:**

1. Lower graphics settings:
   - **Mobile MSAA:** `2x` or `No MSAA`
   - **Mobile Shader Quality:** `Medium`
   - **Shadow Quality:** `Low`

2. Reduce resolution scaling:
   ```cpp
   // In console
   r.ScreenPercentage 75
   ```

3. Check thermal throttling:
   - Let device cool down
   - Test in air-conditioned environment

4. Profile to find bottleneck:
   ```
   stat unit
   ```
   - If **Frame** is high: Overall bottleneck
   - If **Game** is high: CPU bottleneck (optimize Blueprints/C++)
   - If **Draw** is high: GPU bottleneck (reduce graphics quality)

---

## Xiaomi 11T Pro Specific Settings

### Optimal Graphics Settings

Based on Xiaomi 11T Pro hardware (Mali-G77 MC9, 120Hz display):

| Setting | Recommended Value | Rationale |
|---------|-------------------|-----------|
| **Target Frame Rate** | `60` or `120` | Match 120Hz display, or lock to 60 for better battery |
| **Mobile MSAA** | `4x` | GPU can handle it |
| **Mobile Shader Quality** | `High` | Mali-G77 is capable |
| **Shadow Quality** | `Medium` to `High` | Balance quality/performance |
| **Post Processing** | `Medium` | Avoid excessive bloom/effects |
| **Texture Quality** | `High` | 8-12 GB RAM available |
| **Vulkan** | ✅ Enabled | Better performance than OpenGL |

### MIUI-Specific Settings

Xiaomi's MIUI has aggressive battery optimization that can kill background processes.

**Disable battery optimization for your app:**

On device:
1. **Settings > Apps > Manage apps**
2. Find **Najika Digivice**
3. **Battery saver > No restrictions**
4. **Autostart > Enable**
5. **Display pop-up windows while running in the background > Enable**

### Screen Notch Support

Xiaomi 11T Pro has a centered punch-hole notch.

In **Project Settings > Platforms > Android > Advanced APK Packaging**:
- ✅ **Use Display Cutout**

Adjust UI to avoid notch area (see BLUEPRINT_CREATION_GUIDE.md for safe zones).

### 120Hz Display Optimization

To take advantage of 120Hz:

1. **Project Settings > Engine > Rendering**:
   - **Frame Rate Limit:** `120`
   - **VSync:** ✅ Enabled (to match display refresh)

2. In Blueprints, avoid heavy operations in Tick:
   - Use Timers instead of Tick when possible
   - Reduce Event Tick frequency

3. Test on device with `stat fps` to verify 120 FPS

---

## Build Size Optimization

### Reducing APK Size

**Current build sizes:**
- Development (all data in APK): ~500 MB
- Shipping (with OBB): ~300 MB APK + 200 MB OBB

**To reduce further:**

#### 1. Enable Pak File Compression

**Project Settings > Project > Packaging**:
- ✅ **Create compressed cooked packages**
- **Compression Method:** `Oodle` (best compression)

Reduces size by 30-50%.

#### 2. Exclude Debug Files

**Project Settings > Project > Packaging**:
- ✅ **Exclude editor content**
- ❌ **Include Debug Files** (uncheck for Shipping)

#### 3. Asset Reduction

In **Content Browser**:
- Delete unused assets (textures, meshes, sounds)
- Use **Size Map** to find large assets:
  - **Window > Statistics > Size Map**

#### 4. Texture Compression

For Android, use ASTC:
- In **Texture** assets, set:
  - **Compression Settings:** `TC_Default`
  - **LOD Group:** `World` (or appropriate)
- UE5 automatically uses ASTC for Android

#### 5. Audio Compression

In **Sound Wave** assets:
- **Compression Quality:** `40` (good balance)
- **Sound Class:** Use appropriate class

#### 6. Remove Unused Plugins

**Edit > Plugins**:
- Disable plugins you're not using
- Keep only:
  - NajikaBackendClient
  - NajikaVoiceSystem
  - Essential engine plugins

---

## Continuous Integration (CI/CD)

### Automated Builds with GitHub Actions

Example `.github/workflows/android-build.yml`:

```yaml
name: Build Android APK

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v2

      - name: Setup Java
        uses: actions/setup-java@v2
        with:
          java-version: '17'

      - name: Build APK
        run: |
          & "C:\Program Files\Epic Games\UE_5.3\Engine\Build\BatchFiles\RunUAT.bat" `
            BuildCookRun `
            -project="${{ github.workspace }}\NajikaDigivice.uproject" `
            -platform=Android `
            -clientconfig=Development `
            -cook -stage -package -build

      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: NajikaDigivice-APK
          path: |
            **/*.apk
```

---

## Quick Reference

### Essential ADB Commands

| Command | Purpose |
|---------|---------|
| `adb devices` | List connected devices |
| `adb install -r app.apk` | Install/reinstall APK |
| `adb uninstall com.najika.digivice` | Uninstall app |
| `adb logcat` | View device logs |
| `adb shell am start -n com.najika.digivice/...` | Launch app |
| `adb reverse tcp:8000 tcp:8000` | Port forwarding |
| `adb pull /sdcard/file.txt C:\` | Copy file from device |
| `adb push C:\file.txt /sdcard/` | Copy file to device |
| `adb shell pm grant com.najika.digivice PERMISSION` | Grant permission |

### Build Checklist

Before each build:

- ✅ Close UE5 Editor (for command-line builds)
- ✅ Verify all C++ code compiles
- ✅ Check Project Settings (package name, version, permissions)
- ✅ Verify keystore path (for signed builds)
- ✅ Clean previous build artifacts
- ✅ Ensure sufficient disk space (30+ GB free)

After build:

- ✅ Verify APK exists in output folder
- ✅ Check APK size (should be < 500 MB for Development)
- ✅ Test install on device
- ✅ Test basic functionality (login, voice chat, gameplay)
- ✅ Check logs for errors (`adb logcat`)

---

## Next Steps

After successful APK deployment:

1. ✅ **Run Full Tests** - Follow `TESTING_CHECKLIST.md`
2. ✅ **Performance Profiling** - Use `stat` commands and Unreal Insights
3. ✅ **Multiplayer Testing** - Test voice chat and backend connectivity
4. ✅ **User Acceptance Testing** - Get feedback from test users
5. ✅ **Prepare for Release** - Build Shipping APK, create store listing

---

## Support Resources

### Documentation

- `BLUEPRINT_CREATION_GUIDE.md` - Create game Blueprints
- `VISUAL_STUDIO_COMPILATION_GUIDE.md` - Compile C++ code
- `TESTING_CHECKLIST.md` - Test procedures
- `ASSET_REQUIREMENTS.md` - Asset specifications

### Online Resources

- **UE5 Android Documentation:** https://docs.unrealengine.com/5.3/en-US/android-development/
- **Android Developer Guide:** https://developer.android.com/guide
- **ADB Documentation:** https://developer.android.com/studio/command-line/adb

---

**End of Android Build & Deployment Guide**

*This guide is part of the Najika UE5 Implementation documentation suite.*
