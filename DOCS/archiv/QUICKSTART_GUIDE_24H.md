# ⚡ QUICKSTART GUIDE - NAJIKA IN 24 STUNDEN! ⚡
**Model 1 - Digivice APK**
**Created:** 2025-11-11
**Ziel:** Von 0 zu funktionierendem Najika Prototype in 24 Stunden!

---

## 🎯 24-STUNDEN CHALLENGE ÜBERSICHT

```
ZIEL: Ein spielbares Najika Digivice APK in 24 Stunden!

Was funktioniert nach 24h:
✅ UE5 Projekt läuft
✅ Najika Character sichtbar
✅ 3D World navigierbar
✅ Chat System funktioniert
✅ Tamagotchi System (Feed/Drink/Wash)
✅ Basic UI (Status bars, Chat)
✅ Backend verbunden
✅ APK auf Handy installierbar

Was NICHT fertig ist:
❌ Voice Calls (kommt später)
❌ Battle System (kommt später)
❌ Minigames (kommt später)
❌ Polished Graphics (kommt später)

FOKUS: CORE FUNCTIONALITY FIRST! 🔥
```

---

## ⏰ ZEITPLAN (24 STUNDEN)

### **STUNDE 0-4: SETUP & INSTALLATION**

```
[0:00-1:00] UE5 Installation
  → Download UE5 5.6 (80GB!)
  → Install Visual Studio 2022
  → Install Android SDK/NDK
  ⏱️ Meist automatisch, parallel arbeiten!

[1:00-2:00] Projekt erstellen
  → Create UE5 Project (Third Person Template)
  → Configure Android settings
  → First PIE test (Play in Editor)
  ✅ MILESTONE: UE5 läuft!

[2:00-3:00] Backend Setup
  → Start najika_server.py
  → Test health endpoint
  → Verify Ollama running
  ✅ MILESTONE: Backend läuft!

[3:00-4:00] Plugins installieren
  → Copy NajikaBackendClient Plugin
  → Build & Compile
  → Test API connection
  ✅ MILESTONE: UE5 ↔ Backend verbunden!
```

---

### **STUNDE 4-8: CORE SYSTEMS**

```
[4:00-5:00] Character Setup (SCHNELL!)
  → Import Placeholder Character (UE5 Mannequin!)
  → Rename to "Najika"
  → Add to level
  → Add basic material (pink/purple!)
  ✅ MILESTONE: Najika ist sichtbar!

[5:00-6:00] Camera System
  → Create BP_NajikaCameraManager
  → Orbit camera (simplified!)
  → Touch controls for mobile
  → Test in PIE
  ✅ MILESTONE: Kamera funktioniert!

[6:00-7:00] World Setup (MINIMAL!)
  → Create simple 2000x2000 Landscape
  → Add grass material (green!)
  → Add sky (simple!)
  → Add basic lighting
  → Test performance
  ✅ MILESTONE: World navigierbar!

[7:00-8:00] Input System
  → Enhanced Input Setup
  → Touch Virtual Joystick
  → Camera rotation (touch drag)
  → Test on device (if possible)
  ✅ MILESTONE: Controls funktionieren!
```

---

### **STUNDE 8-12: GAMEPLAY BASICS**

```
[8:00-9:00] Tamagotchi System - Backend
  → Verify /api/najika/status endpoint
  → Verify /api/najika/feed endpoint
  → Test with curl
  ✅ MILESTONE: Backend ready!

[9:00-10:00] Tamagotchi System - UE5
  → Create BP_TamagotchiManager
  → GET Status every 5 seconds
  → POST Feed when button clicked
  → Log results
  ✅ MILESTONE: Tamagotchi backend works!

[10:00-11:00] UI - Status Bars (SIMPLE!)
  → WBP_NajikaStatus Widget
  → 3 Progress Bars (Hunger, Energy, Happiness)
  → Update from API data
  → Display on HUD
  ✅ MILESTONE: Status visible!

[11:00-12:00] UI - Action Buttons
  → WBP_TamagotchiCare Widget
  → 3 Buttons: Feed, Drink, Wash
  → Click → POST to API
  → Update status bars
  ✅ MILESTONE: Tamagotchi playable!
```

---

### **STUNDE 12-16: CHAT SYSTEM**

```
[12:00-13:00] Chat UI (SIMPLE!)
  → WBP_ChatUI Widget
  → Text input box
  → Send button
  → Chat history (scrollbox)
  ✅ MILESTONE: Chat UI visible!

[13:00-14:00] Chat Backend Integration
  → POST /api/chat on send
  → Parse response
  → Display in chat history
  → Test with Ollama
  ✅ MILESTONE: Chat funktioniert!

[14:00-15:00] Chat Improvements
  → Add "Najika is typing..." animation
  → Add message bubbles (simple!)
  → Add timestamps
  → Test different messages
  ✅ MILESTONE: Chat feels good!

[15:00-16:00] Integration Test
  → Play full loop:
    * Start app
    * Check Najika status
    * Feed Najika
    * Chat with Najika
    * Walk around world
  → Fix any bugs
  ✅ MILESTONE: Core loop works!
```

---

### **STUNDE 16-20: PACKAGING & TESTING**

```
[16:00-17:00] Android Build Setup
  → Project Settings → Android
  → Configure package name
  → Configure SDK/NDK paths
  → Set icons (placeholder OK!)
  → Configure permissions
  ✅ MILESTONE: Build settings ready!

[17:00-18:00] First APK Build
  → Package → Android → APK
  → Wait for build (15-30 min!)
  → Check for errors
  → Fix if needed, rebuild
  ✅ MILESTONE: APK created!

[18:00-19:00] Device Testing
  → Install APK on Xiaomi 11T Pro
  → Test startup
  → Test controls
  → Test backend connection (WiFi!)
  → Test tamagotchi system
  → Test chat
  ✅ MILESTONE: Works on device!

[19:00-20:00] Bug Fixing
  → Fix crashes (if any)
  → Fix UI scaling issues
  → Fix performance issues
  → Rebuild & retest
  ✅ MILESTONE: Stable on device!
```

---

### **STUNDE 20-24: POLISH & DOCUMENTATION**

```
[20:00-21:00] Basic Polish
  → Add app icon (use Najika icon!)
  → Add splash screen (simple!)
  → Add background music (optional)
  → Add UI sounds (optional)
  ✅ MILESTONE: Feels more polished!

[21:00-22:00] Performance Optimization
  → Check FPS (stat FPS)
  → Reduce draw calls if needed
  → Lower texture resolution if needed
  → Test battery usage (1h session)
  ✅ MILESTONE: Runs well!

[22:00-23:00] Final Testing
  → Complete 30-min play session
  → Test all features
  → Document any issues
  → Create bug list for later
  ✅ MILESTONE: Feature-complete prototype!

[23:00-24:00] Documentation & Backup
  → Write down what works
  → Write down what doesn't
  → Git commit & push
  → Backup APK file
  → Celebrate! 🎉
  ✅ MILESTONE: 24H CHALLENGE COMPLETE!
```

---

## 🛠️ QUICK REFERENCE COMMANDS

### **Backend:**
```bash
# Start backend
cd C:\Najika_World\backend
python najika_server.py

# Test backend
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{\"message\":\"Hello\"}"
```

### **UE5:**
```
Play in Editor: Alt+P
Stop: Escape
Package APK: File → Package Project → Android → Android (ASTC)
Build: Ctrl+Shift+B (in Visual Studio)
Refresh VS Project: Right-click .uproject → Generate VS project files
```

### **Android:**
```bash
# Install APK
adb install NajikaDigivice.apk

# View logs
adb logcat -s UE

# Uninstall
adb uninstall com.najika.digivice
```

---

## 📋 MINIMAL CHECKLIST (MUST-HAVE!)

```
HOUR 0-4: SETUP
☐ UE5 installed
☐ Project created
☐ Backend running
☐ Plugin compiled

HOUR 4-8: CORE
☐ Character visible
☐ Camera works
☐ World created
☐ Controls work

HOUR 8-12: GAMEPLAY
☐ Tamagotchi API works
☐ Status bars show
☐ Buttons work
☐ Can feed Najika

HOUR 12-16: CHAT
☐ Chat UI visible
☐ Can send message
☐ Receive AI response
☐ Chat history works

HOUR 16-20: BUILD
☐ APK builds
☐ APK installs on device
☐ Runs on device
☐ No crashes

HOUR 20-24: POLISH
☐ Icon added
☐ Performance OK (>30 FPS)
☐ Final test passed
☐ Documented & backed up
```

---

## ⚡ SPEED TIPS

### **Time-Savers:**

```
1. Use Placeholders!
   → UE5 Mannequin instead of custom character
   → Simple landscape instead of detailed world
   → Basic UI instead of polished UI
   → OPTIMIZATION LATER!

2. Skip Non-Essential!
   → No voice calls (complex!)
   → No battle system (time-consuming!)
   → No minigames (later!)
   → CORE FEATURES FIRST!

3. Copy-Paste from Guides!
   → All code in Phase guides
   → All Blueprints documented
   → Don't reinvent the wheel!

4. Test in Editor First!
   → PIE is faster than device
   → Only test on device when stable
   → Save time on builds

5. Use Version Control!
   → Git commit every hour
   → Easy to roll back if broken
   → Peace of mind!
```

---

## 🐛 QUICK TROUBLESHOOTING

### **Problem: Build fails**
```
→ Check Visual Studio installed
→ Regenerate VS project files
→ Build in Visual Studio first
→ Then build in UE5
```

### **Problem: APK won't install**
```
→ Uninstall old version first
→ Check package name unique
→ Enable "Unknown sources" on device
```

### **Problem: Can't connect to backend**
```
→ Backend running? (curl http://127.0.0.1:8000/health)
→ Firewall blocking?
→ Correct IP address? (127.0.0.1 for local)
→ Device on same WiFi network?
```

### **Problem: Low FPS**
```
→ Lower screen resolution (Project Settings)
→ Disable Lumen (use basic lighting)
→ Reduce draw calls (merge meshes)
→ Lower texture quality
```

### **Problem: Crash on startup**
```
→ Check logcat: adb logcat -s UE
→ Missing permissions in AndroidManifest?
→ Shader compilation? (wait longer)
→ Check TROUBLESHOOTING_DATABASE.md
```

---

## 🎯 SUCCESS CRITERIA

**After 24 hours, you should have:**

```
✅ Lauffähiges APK auf Xiaomi 11T Pro
✅ Najika sichtbar in 3D World
✅ Kamera steuerbar
✅ Tamagotchi System funktioniert:
   - Status bars zeigen Hunger/Energy/Happiness
   - Feed/Drink/Wash buttons funktionieren
   - Backend speichert Status
✅ Chat System funktioniert:
   - Kann Nachricht senden
   - Bekommt AI-Antwort
   - Chat history sichtbar
✅ Performance akzeptabel (>30 FPS)
✅ Keine Crashes
✅ Dokumentiert & in Git committed

WENN JA: 🎉 CHALLENGE ERFOLGREICH! 🎉
```

---

## 💡 AFTER 24H - WHAT'S NEXT?

```
Week 2: Polish & Features
  → Better character model (VRM import!)
  → Better world (detailed landscape)
  → Better UI (polished materials)
  → Add animations

Week 3: Voice System
  → Implement NajikaVoiceSystem plugin
  → Add Whisper STT
  → Add TTS playback
  → Add lip sync

Week 4: Battle System
  → Turn-based combat
  → Enemy AI
  → Skills & abilities
  → Rewards

Week 5-6: Minigames
  → Rhythm game
  → Reflex game
  → Garden game

Week 7-8: Security & Optimization
  → Biometric auth
  → Encrypted storage
  → Performance optimization
  → Battery optimization

Week 9-10: Testing & Packaging
  → Comprehensive testing
  → Bug fixing
  → Final build
  → Prepare for launch

Week 11+: LAUNCH! 🚀
```

---

## 🔥 MOTIVATION

```
Remember:
→ 24 hours is TIGHT but DOABLE! 💪
→ Focus on CORE, not PERFECTION! ⚡
→ You have ALL the guides ready! 📖
→ Plugins are ALREADY WRITTEN! ✅
→ Just FOLLOW THE PLAN! 🎯

DON'T GET STUCK ON:
→ Perfect graphics (placeholder OK!)
→ Complex features (later!)
→ Edge cases (fix later!)

FOCUS ON:
→ Making it RUN! 🏃
→ Core loop WORKING! 🔄
→ APK on DEVICE! 📱

YOU CAN DO THIS! 🔥🔥🔥
```

---

## 🎊 FINAL CHECKLIST

```
Before starting 24h challenge:

☐ Read this entire guide
☐ Have all tools downloaded:
   - UE5 5.6 installer ready
   - Visual Studio 2022 installer ready
   - Android SDK/NDK ready
   - Git installed
☐ Backend ready to go:
   - najika_server.py tested
   - Ollama running
   - All dependencies installed
☐ Phone ready:
   - Xiaomi 11T Pro charged
   - USB Debugging enabled
   - Connected to same WiFi
☐ Food & drinks ready! (You'll be coding for 24h! 🍕☕)
☐ Music playlist ready! (Stay focused! 🎵)
☐ Tell friends you're busy! (No interruptions! 🔕)

READY? LET'S GO! 🚀
```

---

**Model 1 - Digivice APK Development**
**Guide:** Quickstart 24H Challenge
**Status:** Complete ✅
**Goal:** Functional Najika Prototype in 24 Hours!

**START YOUR TIMER... NOW! ⏰🔥**
