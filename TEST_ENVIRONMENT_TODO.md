# NAJIKA TEST ENVIRONMENT - MINI LEBENSRAUM
## Separates Testing Setup für Feature-Validierung + Handyspiel Prototyping

**Purpose:** Kleiner isolierter Testbereich mit DOPPELTEM Zweck:
1. **Digivice Features testen** VOR Integration in Haupt-APK
2. **Handyspiel Mechaniken prototypen** VOR Full-Game Development

**Location:** C:\NajikaTestEnvironment_UE5
**Timeline:** Parallel zu APK Development (Week 2-10)

---

## 🎯 WARUM TEST ENVIRONMENT?

### **Problem:**
- APK Development dauert 10-12 Wochen
- Features müssen schnell getestet werden
- Keine Wartezeit bis komplette APK fertig
- Handyspiel braucht validated Mechaniken (Combat, Movement, etc.)

### **Lösung - DUAL PURPOSE:**
Mini-Version mit:
- ✅ Einzelner kleiner Raum (10x10m)
- ✅ Najika Character (basic)
- ✅ Alle Digivice Features isoliert testbar
- ✅ Handyspiel Mechaniken prototypen (Combat, AI, Loot)
- ✅ Schnelle Iteration
- ✅ Kein Risiko für Haupt-APK oder Full-Game

### **Workflow:**
```
Test Environment (Model 2)
    ↓
    ├─→ Feature validiert? → Export zu Digivice APK (Model 1)
    └─→ Mechanik validiert? → Export zu Handyspiel (Model 3)
```

---

## 📋 PHASE 1: MINIMAL SETUP (Day 1)

### **TODO 1.1: Create Test Project**
```
1. Create New UE5 Project:
   - Name: NajikaTestEnvironment
   - Template: Blank
   - Location: C:\NajikaTestEnvironment_UE5
   - Settings: Mobile (Optimized)

2. Configure:
   - Minimum Android SDK: 29
   - Target SDK: 34
   - Enable Vulkan
   - Disable unnecessary features

3. Create Test Level:
   - Name: L_TestRoom
   - Size: 10x10 meters
   - Simple geometry (cube room)
   - Basic lighting
```

### **TODO 1.2: Import Najika (Basic)**
```
1. Import Character:
   - Use simplest Najika model available
   - Or use Mannequin temporarily
   - Skeletal Mesh only, minimal animations

2. Test Movement:
   - WASD controls (PC)
   - Touch controls (Mobile)
   - Camera rotation

3. Place in Test Room
```

---

## 🧪 PHASE 2: FEATURE TESTING STATIONS

### **TODO 2.1: Backend Connection Test**
```
1. Create Test Widget:
   - WBP_BackendTest
   - Buttons:
     - "Test /api/status"
     - "Test /api/chat"
     - "Test /api/najika/feed"
   - Response display (text box)

2. Implement HTTP calls:
   - Use UE5 HTTP module
   - Target: http://127.0.0.1:8000
   - Display JSON responses

3. Test:
   - Start Python backend
   - Run test level
   - Click all test buttons
   - Verify responses
```

### **TODO 2.2: Voice Call Test Station**
```
1. Create Voice Test Area:
   - Dedicated corner of room
   - Visual indicator (icon)

2. Implement:
   - Mic capture (Android AudioCapture)
   - Send to /api/voice_call/audio
   - Receive TTS response
   - Play audio

3. Test:
   - Speak into microphone
   - Wait for Najika response
   - Verify audio plays
   - Check latency (<500ms target)

4. Visual Feedback:
   - Audio waveform display
   - Status text ("Listening...", "Processing...", "Speaking...")
```

### **TODO 2.3: Animation Test Station**
```
1. Animation Test UI:
   - Dropdown: Select animation
   - Button: Play Animation
   - Slider: Animation Speed

2. Test All Animations:
   - Idle
   - Walk/Run
   - Jump
   - Talk (lip sync!)
   - Emotes (Happy, Sad, Angry)

3. Blend Testing:
   - Smooth transitions
   - Blend spaces
   - Animation layering
```

### **TODO 2.4: UI Test Station**
```
1. UI Gallery:
   - Show all UI widgets
   - Test interactions
   - Test on different resolutions

2. Widgets to Test:
   - Chat UI
   - Tamagotchi Status
   - Voice Call UI
   - Settings Menu
   - Notifications

3. Interaction Tests:
   - Touch
   - Drag
   - Pinch
   - Swipe
```

### **TODO 2.5: Physics Test Station**
```
1. Simple Physics Objects:
   - Cubes, spheres
   - Throwable items
   - Destructible objects

2. Test:
   - Collision
   - Ragdoll (if Najika falls)
   - Object interaction
   - Performance with many objects
```

### **TODO 2.6: Performance Test Station**
```
1. Stress Test Area:
   - Spawn many objects
   - Complex lighting
   - Particle effects
   - Multiple animations

2. Monitor:
   - FPS (stat fps)
   - Memory (stat memory)
   - Draw calls (stat rhi)
   - CPU/GPU time (stat unit)

3. Scalability Test:
   - Test on Low/Med/High/Epic settings
   - Find optimal settings for Snapdragon 888
```

### **TODO 2.7: HANDYSPIEL MECHANICS PROTOTYPING** 🎮
```
🔥 WICHTIG: Diese Station dient als TESTLAUF für das Handyspiel!
Alle hier validierten Mechaniken werden später zu Model 3 (Handyspiel) exportiert.

1. Combat System Prototype:
   - Basic melee attack (Najika punches/slashes)
   - Projectile weapon (Magic staff)
   - AOE attack (Explosion spell!)
   - Damage numbers (floating text)
   - Hit detection & feedback

2. Enemy AI Prototype:
   - Simple AI enemy (basic Behavior Tree)
   - Chase player when in range
   - Attack when close
   - Health system
   - Death animation

3. Loot System Prototype:
   - Spawn pickup items (cubes with icons)
   - Proximity detection
   - Pickup interaction
   - Add to inventory (simple UI)
   - Rarity system (colors: white/green/blue/purple)

4. Movement Mechanics:
   - Dash/Dodge ability
   - Double jump
   - Crouch
   - Sprint

5. Fortnite-Style Mechanics (Optional):
   - Building prototype (place walls/ramps)
   - Material gathering (hit objects to collect)
   - Storm zone (damage outside area)

6. Testing Checklist:
   - [ ] Combat feels responsive
   - [ ] AI enemies react properly
   - [ ] Loot system works
   - [ ] Movement smooth on mobile
   - [ ] Performance stable (60 FPS)

7. Export Validated Mechanics:
   - Document what works well
   - Package Blueprints/C++ code
   - Send to Model 3 (Handyspiel) for integration
```

---

## 📱 PHASE 3: MOBILE TESTING

### **TODO 3.1: Deploy to Xiaomi 11T Pro**
```
1. Package Test APK:
   - Development build (with logging)
   - Sign with debug key
   - Install via ADB

2. Test Checklist:
   - [ ] App launches
   - [ ] Touch controls work
   - [ ] Backend connects (local network!)
   - [ ] Voice calls work
   - [ ] Animations play
   - [ ] UI responsive
   - [ ] No crashes

3. Performance Check:
   - Monitor FPS
   - Monitor battery drain
   - Check for overheating
```

### **TODO 3.2: Fix Issues**
```
1. Document bugs:
   - Create TestEnvironment_BUGS.md
   - List all issues found

2. Fix critical issues:
   - Crashes
   - Non-functional features
   - Severe performance problems

3. Iterate:
   - Fix → Package → Test → Repeat
```

---

## 🔄 PHASE 4: INTEGRATION WITH MAIN APK

### **TODO 4.1: Export Tested Features**
```
Once feature tested successfully:
1. Export from Test Environment:
   - Blueprints
   - C++ plugins
   - Assets
   - UI widgets

2. Import to Main APK project:
   - Copy to NajikaDigivice_UE5
   - Integrate into main systems
   - Test in context

3. Mark as "Production Ready"
```

### **TODO 4.2: Continuous Testing**
```
As Main APK develops:
1. Test new features in Test Environment FIRST
2. Only add to Main APK after validation
3. Keep Test Environment updated
```

---

## ✅ SUCCESS CRITERIA

### **Test Environment is successful if:**
```
✅ All features testable independently
✅ Quick iteration (minutes, not hours)
✅ Accurate representation of performance
✅ Easy to deploy to device
✅ Doesn't interfere with Main APK development
```

---

## 📊 FEATURE TEST STATUS TABLE

| Feature | Test Station | Status | Notes |
|---------|--------------|--------|-------|
| Backend HTTP | Station 2.1 | ⏳ | - |
| Voice Calls | Station 2.2 | ⏳ | - |
| Animations | Station 2.3 | ⏳ | - |
| UI Systems | Station 2.4 | ⏳ | - |
| Physics | Station 2.5 | ⏳ | - |
| Performance | Station 2.6 | ⏳ | - |
| Chat | TBD | ⏳ | - |
| Tamagotchi | TBD | ⏳ | - |
| Battle System | TBD | ⏳ | - |
| Minigames | TBD | ⏳ | - |
| Scanner | TBD | ⏳ | - |

---

**END OF TEST ENVIRONMENT TODO**
