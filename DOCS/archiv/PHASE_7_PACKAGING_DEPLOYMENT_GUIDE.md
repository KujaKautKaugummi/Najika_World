# PHASE 7: PACKAGING & DEPLOYMENT - COMPLETE GUIDE
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**Phase:** 7 - Packaging & Deployment (Woche 10)
**Dauer:** 1 Woche

---

## 🎯 PHASE 7 ÜBERSICHT

### **Was wird gemacht:**
```
✅ Build Configuration (Shipping)
✅ Android APK/AAB Packaging
✅ Signing with Release Keystore
✅ Testing on Xiaomi 11T Pro
✅ Bug Fixing
✅ Google Play Console Setup (optional)
✅ Beta Testing (optional)
```

---

## 📦 TODO 7.1: BUILD CONFIGURATION

### **Project Settings - Packaging:**

```
Edit → Project Settings → Packaging

Build Configuration:
→ Build Configuration: Shipping
   (NOT Development or DebugGame!)

Packaging Settings:
✅ Create compressed cooked packages
✅ Exclude editor content
✅ For distribution
✅ Include prerequisites installer
✅ Include crash reporter
❌ Include debug files (only for Development builds)

Project:
→ Project Name: NajikaDigivice
→ Project Version: 1.0.0
→ Company Name: Najika
→ Copyright Notice: © 2025 Najika

Advanced:
✅ Share Material Shader Code
✅ Shared Material Native Libraries
→ Cook everything in project content directory
```

### **Android Settings:**

```
Project Settings → Platforms → Android

APK Packaging:
→ Package for ARM64: ✅ Yes (modern devices)
→ Package for x86-64: ❌ No (not needed)
→ Package for ARMv7: ❌ No (old devices)

Application:
→ Package Name: com.najika.digivice
→ Store Version: 1
→ Store Version Name: 1.0.0
→ Minimum SDK Version: 29 (Android 10)
→ Target SDK Version: 34 (Android 14)
→ Install Location: Auto
→ Orientation: Landscape / Sensor (user choice)

Icons & Launch Images:
→ Default Icon: Upload icon_512x512.png
→ Foreground Icon: Upload icon_adaptive_fg.png (adaptive icons)
→ Background Icon: Upload icon_adaptive_bg.png
→ Splash Screen: Upload splash_1920x1080.png

Distribution Signing:
→ Enable: For distribution

APK Services:
✅ Enable Google Play Services (für Achievements später)
✅ Enable Firebase Analytics (optional)
❌ Enable Ads (NO ADS!)
```

---

## 🔑 TODO 7.2: SIGNING CONFIGURATION

### **Generate Release Keystore:**

```bash
# Open PowerShell in C:\NajikaDigivice_UE5\Build\Android\

# Generate keystore
keytool -genkey -v -keystore najika-release.keystore \
  -alias najika \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Prompts:
# Enter keystore password: [CHOOSE STRONG PASSWORD]
# Re-enter password: [SAME PASSWORD]
# What is your first and last name? Najika Digivice
# What is the name of your organizational unit? Development
# What is the name of your organization? Najika
# What is the name of your City or Locality? [Your City]
# What is the name of your State or Province? [Your State]
# What is the two-letter country code for this unit? DE
# Is this correct? yes
# Enter key password: [SAME AS KEYSTORE PASSWORD or different]

# Result: najika-release.keystore created!
```

### **Configure in UE5:**

```
Project Settings → Platforms → Android → Distribution Signing

Keystore:
→ Key Store: Browse → najika-release.keystore
→ Key Alias: najika
→ Key Store Password: [YOUR PASSWORD]
→ Key Password: [YOUR KEY PASSWORD]

✅ Enable Signing

IMPORTANT:
⚠️ BACKUP THIS KEYSTORE FILE SOMEWHERE SAFE!
⚠️ If lost, you CANNOT update your app on Google Play!
⚠️ Store password in password manager!
```

---

## 🏗️ TODO 7.3: BUILDING APK/AAB

### **Build Android Package:**

```
In UE5 Editor:

Method 1: Package Project (APK)
1. File → Package Project → Android → Android (ASTC)
2. Choose output folder: C:\Builds\NajikaDigivice\Android\
3. Wait for packaging (10-30 minutes first time!)
4. Output: NajikaDigivice-Android-Shipping.apk

Method 2: Generate App Bundle (AAB) - For Google Play
1. File → Package Project → Android → Android (ASTC)
2. Settings:
   → Generate App Bundle (AAB): ✅ Yes
   → Enable Universal APK: ✅ Yes (for testing)
3. Output: NajikaDigivice-Android-Shipping.aab
```

### **Packaging Process:**

```
Steps UE5 performs:
1. ✅ Compile all Blueprints
2. ✅ Compile C++ Plugins
3. ✅ Cook all assets (convert to platform format)
4. ✅ Compress textures (ASTC format)
5. ✅ Package into APK/AAB
6. ✅ Sign with release keystore
7. ✅ Optimize (zipalign)
8. ✅ Verify signature

Expected Duration:
- First build: 20-40 minutes
- Subsequent builds: 5-15 minutes (incremental)

Expected Size:
- APK size: ~200-500 MB (depends on assets)
- AAB size: ~150-400 MB (smaller, dynamic delivery)
```

---

## 📱 TODO 7.4: TESTING ON DEVICE

### **Install APK on Xiaomi 11T Pro:**

```
Prerequisites:
1. Enable USB Debugging on phone:
   Settings → About Phone → Tap Build Number 7 times
   Settings → Additional Settings → Developer Options
   → Enable USB Debugging

2. Connect phone to PC via USB

3. Install ADB (if not already):
   - Installed with Android Studio
   - Or download: https://developer.android.com/studio/releases/platform-tools

Method 1: ADB Install
```bash
cd C:\Builds\NajikaDigivice\Android\
adb devices  # Should show your device
adb install -r NajikaDigivice-Android-Shipping.apk

# -r flag: Reinstall keeping data
```

Method 2: Transfer & Install Manually
1. Copy APK to phone (USB/Cloud/Email)
2. Open file manager on phone
3. Tap APK file
4. Allow "Install from unknown sources" if prompted
5. Install
```

### **Testing Checklist:**

```
CRITICAL TESTS (Must Pass):

Launch & Startup:
☐ App launches without crash
☐ Splash screen shows
☐ Main menu loads
☐ No black screens
☐ No freezing

Performance:
☐ FPS: 30+ minimum, 60 target
☐ No stuttering during gameplay
☐ Smooth UI interactions
☐ Load times < 10 seconds

Graphics:
☐ 3D world renders correctly
☐ Najika character visible
☐ Textures load properly
☐ No z-fighting or graphical glitches
☐ Post-processing working (bloom, etc.)

Controls:
☐ Touch controls responsive
☐ Virtual joystick works
☐ Buttons clickable
☐ Camera rotation smooth
☐ Character movement works

Backend Connection:
☐ Connects to 127.0.0.1:8000 (if backend running)
☐ Chat messages send/receive
☐ Status updates work
☐ Voice calls work (microphone permission)

Audio:
☐ Background music plays
☐ Sound effects work
☐ Voice TTS playback works
☐ Volume controls work

UI:
☐ All menus accessible
☐ Settings save/load
☐ Notifications show
☐ UI scales correctly on screen

Save/Load:
☐ Game state saves
☐ Game state loads on restart
☐ No data loss

Permissions:
☐ Microphone permission requests properly
☐ Storage permission (if needed)
☐ All permissions functional

Battery & Thermal:
☐ Battery drain acceptable (< 25% per hour)
☐ Phone doesn't overheat
☐ Thermal throttling works (if implemented)

Memory:
☐ No memory leaks (test 1+ hour)
☐ Memory usage < 2GB
☐ No crashes after extended play

Crash Testing:
☐ No crashes on: Pause/Resume
☐ No crashes on: Background/Foreground
☐ No crashes on: Phone call interrupt
☐ No crashes on: Low battery
☐ No crashes on: Network disconnect
```

---

## 🐛 TODO 7.5: BUG FIXING

### **Bug Tracking:**

```
Create: C:\Najika_World\BUGS\BUGS_PHASE7.md

Format:
# BUG TRACKING - Phase 7 Testing

## Critical Bugs (Must fix before release)
### BUG-001: App crashes on startup
**Severity:** Critical
**Platform:** Android
**Device:** Xiaomi 11T Pro
**Steps to Reproduce:**
1. Install APK
2. Launch app
3. Crash after splash screen

**Expected:** App should load main menu
**Actual:** Crash with error "..."
**Log:** [Include logcat output]

**Status:** 🔴 Open / 🟡 In Progress / 🟢 Fixed
**Assigned:** Model 1
**Fix:** [Describe fix when done]

---

### BUG-002: Touch controls not working
**Severity:** High
**Platform:** Android
**Device:** Xiaomi 11T Pro
...

## High Priority Bugs
...

## Medium Priority Bugs
...

## Low Priority / Known Issues
...
```

### **Debugging on Device:**

```
View Logcat (Real-time Logs):
```bash
adb logcat -s UE

# Filter for Najika logs:
adb logcat | grep Najika

# Save log to file:
adb logcat > najika_device_log.txt
```

Common Issues & Fixes:

**Issue: Black screen on startup**
Fix: Check asset cooking, may need to re-cook

**Issue: Controls not responding**
Fix: Check Input Mapping Context is added in Player Controller

**Issue: Crash on backend API call**
Fix: Check network security config allows localhost

**Issue: Textures not loading**
Fix: Check texture compression settings, use ASTC

**Issue: Low FPS**
Fix: Reduce quality settings, check LOD, disable expensive effects
```

---

## 🚀 TODO 7.6: GOOGLE PLAY CONSOLE (Optional)

### **Setup Google Play Console:**

```
ONLY if publishing to Google Play Store!

1. Create Google Play Developer Account:
   → https://play.google.com/console/signup
   → One-time fee: $25
   → Fill out account info

2. Create App:
   → Click "Create app"
   → App name: Najika Digivice
   → Language: German / English
   → App or Game: Game
   → Free or Paid: Free (no ads!)
   → Declarations: Accept policies

3. Upload App Bundle (AAB):
   → Production → Create new release
   → Upload AAB file
   → Release name: "1.0.0 - Initial Release"
   → Release notes (German):
     "Willkommen bei Najika Digivice!
     - Interagiere mit Najika in 3D
     - Voice Calls (Whisper + TTS)
     - Tamagotchi-System
     - Turn-based Combat
     - Und mehr!"

4. Store Listing:
   → App Name: Najika Digivice
   → Short Description (80 chars):
     "Deine AI Companion Najika in einer interaktiven 3D-Welt!"

   → Full Description (4000 chars):
     [Detaillierte Beschreibung aller Features]

   → Screenshots (Required):
     - Phone: Min 2, recommended 8 (1080x1920)
     - Tablet: Optional
     Upload screenshots showing:
     * Main menu
     * 3D world exploration
     * Chat interface
     * Voice call UI
     * Battle system
     * Tamagotchi care
     * Settings menu
     * Different gameplay moments

   → Feature Graphic:
     - 1024x500 banner
     - Eye-catching design with Najika

   → App Icon:
     - 512x512 PNG
     - Alpha channel
     - Najika logo/character

5. Content Rating:
   → Complete questionnaire
   → Expected: Teen (13+) or Everyone 10+
   → No violence, no NSFW content in public build

6. Pricing & Distribution:
   → Free
   → Countries: Worldwide (or specific)
   → Ads: No
   → In-App Purchases: No (for now)

7. Privacy Policy:
   → Required!
   → Create page explaining:
     - What data is collected (minimal!)
     - How it's used (locally only!)
     - No third-party sharing
     - User rights (delete data)
   → Host on GitHub Pages or website
   → Link in Play Console

8. Release:
   → Review & Rollout
   → Submit for review (2-7 days)
   → Once approved: Published!
```

---

## 🧪 TODO 7.7: BETA TESTING (Optional)

### **Closed Beta via Google Play:**

```
1. Create Closed Testing Track:
   → Testing → Closed Testing
   → Create new track: "Beta"
   → Upload AAB

2. Add Testers:
   → Create email list
   → Or: Create shareable link
   → Max 100 testers (free tier)

3. Beta Testers get:
   → Opt-in link
   → Install beta APK
   → Can send feedback via Play Console

4. Collect Feedback:
   → Monitor crash reports
   → Read reviews
   → Fix critical bugs
   → Update beta build

5. When stable:
   → Promote to Production
   → Full public release!
```

### **Or: Manual Beta Testing:**

```
1. Build APK
2. Share via:
   - Email
   - Cloud storage (Google Drive, Dropbox)
   - USB transfer
3. Testers install manually
4. Collect feedback via:
   - Google Forms
   - Discord/Telegram
   - Email
5. Track bugs in BUGS.md
```

---

## 📊 SUCCESS CRITERIA

**Phase 7 ist komplett wenn:**

```
✅ APK/AAB successfully built
   - Shipping configuration
   - Signed with release keystore
   - Optimized (zipalign)

✅ Tested on Xiaomi 11T Pro
   - All critical tests passed
   - No crashes
   - Performance acceptable (30+ FPS)
   - Battery life good (4+ hours)

✅ All critical bugs fixed
   - No crashes
   - All features functional
   - UI works correctly

✅ APK ready for distribution
   - Signed
   - Tested
   - Stable

✅ (Optional) Google Play ready
   - Store listing complete
   - Screenshots uploaded
   - Privacy policy published
   - Submitted for review
```

---

## 🎉 PHASE 7 COMPLETE!

**Nächster Schritt:** Phase 8 - Iterative Improvements

**Geschätzte Dauer Phase 7:** 1 Woche

---

**Model 1 - Digivice APK Development**
**Phase:** 7/9 - Packaging & Deployment
**Status:** Ready to Execute
