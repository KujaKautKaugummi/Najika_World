# NAJIKA DIGIVICE - UNREAL ENGINE 5 MOBILE MIGRATION
## COMPLETE TODO FOR CLAUDE CODE WEB MODEL

**Created:** 2025-11-11
**Current Status:** WebView-based Digivice (funktionierend!)
**Goal:** Unreal Engine 5 Mobile App (Android) mit UEFN-Kompatibilität
**Target Device:** Xiaomi 11T Pro (Snapdragon 888, 8GB RAM)
**Timeline:** 8-12 Wochen

---

## 📋 PROJECT OVERVIEW

### **Was BLEIBT (Backend - 100% funktionierend!):**
```
✅ Python Server (najika_server.py)
✅ Voice Calls (najika_voice_call.py - Whisper + Coqui TTS)
✅ Ollama Integration (Llama 3.1 8B)
✅ ChromaDB Memory System
✅ LoRA Training System
✅ Living System (Tamagotchi)
✅ Battle System
✅ All HTTP/WebSocket APIs
```

### **Was WIRD MIGRIERT (Frontend → Unreal Engine 5):**
```
⏳ 3D World (Three.js → UE5 Nanite/Lumen)
⏳ Najika Character (VRM → Skeletal Mesh)
⏳ UI (HTML/CSS → UMG Widgets)
⏳ Camera System (JS → UE5 Camera)
⏳ Physics (Cannon.js → Chaos Physics)
⏳ Animations (JS → Animation Blueprints)
⏳ Touch Controls (JS → UE5 Touch Interface)
```

### **Was NEU KOMMT:**
```
🆕 Unreal Engine 5.6 Mobile Integration
🆕 C++ Backend Communication Plugin
🆕 Biometric Authentication (Android Keystore)
🆕 Hardware-accelerated Graphics (Vulkan/OpenGL ES)
🆕 Advanced Physics (Chaos)
🆕 Professional Lighting (Lumen Mobile)
🆕 Particle Systems (Niagara)
🆕 UEFN-ready Architecture (für späteren Fortnite Port)
```

---

## 🎯 PHASE 0: ANALYSIS & BACKUP (Week 0)

### **TODO 0.1: Analyze Existing System**
```
1. Read all backend files:
   - C:\Najika_World\backend\najika_server.py
   - C:\Najika_World\backend\najika_voice_call.py
   - C:\Najika_World\backend\najika_memory_enhanced.py
   - C:\Najika_World\backend\najika_living_system.py
   - C:\Najika_World\backend\najika_battle.py

2. Document all API endpoints:
   - /api/chat (POST)
   - /api/voice_call/start (POST)
   - /api/voice_call/audio (POST)
   - /api/voice_call/end (POST)
   - /api/najika/status (GET)
   - /api/najika/feed (POST)
   - ... (liste ALLE auf!)

3. Read frontend files:
   - C:\Najika_World\digivice\index.html
   - C:\Najika_World\digivice\js\3d_scene.js
   - C:\Najika_World\digivice\js\voice_call.js
   - C:\Najika_World\digivice\js\character_animations.js

4. Document all features currently working:
   - Voice Calls ✅
   - Text Chat ✅
   - 3D World Navigation ✅
   - Tamagotchi System ✅
   - Training System ✅
   - Battle System ✅
   - ... (liste ALLE auf!)

5. Identify critical dependencies:
   - Python version: 3.10+
   - Ollama models: Llama 3.1 8B
   - Whisper model: base
   - Coqui TTS: Megumin voice
```

### **TODO 0.2: Create Full Backup**
```bash
# Backup commands:
cd C:\
tar -czf Najika_World_BACKUP_$(date +%Y%m%d).tar.gz Najika_World/

# Verify backup:
tar -tzf Najika_World_BACKUP_*.tar.gz | head -20

# Also backup to external location
robocopy C:\Najika_World D:\Backups\Najika_World_$(date +%Y%m%d) /E /COPYALL
```

### **TODO 0.3: Document Current Architecture**
```
Create document: NAJIKA_CURRENT_ARCHITECTURE.md

Include:
1. System diagram (ASCII art)
2. Data flow (User → Frontend → Backend → AI)
3. File structure tree
4. API reference (all endpoints)
5. State management (najika_state.json structure)
6. Memory system (ChromaDB schema)
7. Voice pipeline (WebRTC → Whisper → Ollama → Coqui → Audio)
```

---

## 🚀 PHASE 1: UNREAL ENGINE 5 SETUP (Week 1)

### **TODO 1.1: Install Unreal Engine 5.6**
```
1. Download Epic Games Launcher:
   https://www.epicgames.com/store/download

2. Install UE5.6 (Latest):
   - Open Epic Games Launcher
   - Library → Engine Versions
   - Install Unreal Engine 5.6.0 (or latest)
   - Select: Android Support, C++ Support, Engine Source

3. Install Android SDK/NDK:
   - Edit → Project Settings → Platforms → Android
   - Install Android SDK via UE5 (automatic)
   - Install Android NDK r25c
   - Set ANDROID_HOME environment variable

4. Install Visual Studio 2022:
   - Workloads: Desktop Development with C++
   - Components:
     - MSVC v143
     - Windows 10/11 SDK
     - C++ ATL
     - Android Game Development Extension

5. Verify installation:
   - Create test project
   - Package for Android (Test build)
   - Deploy to Xiaomi 11T Pro via USB
```

### **TODO 1.2: Create Najika Digivice Project**
```
1. Launch Unreal Engine 5.6

2. Create New Project:
   - Template: Blank (Mobile optimized)
   - Project Name: NajikaDigivice
   - Location: C:\NajikaDigivice_UE5
   - Target Platform: Mobile
   - Quality Preset: Scalable
   - With Starter Content: No
   - Raytracing: Disabled (mobile)

3. Configure Project Settings:
   Project Settings → Platforms → Android:
   - Minimum SDK: 29 (Android 10)
   - Target SDK: 34 (Android 14)
   - Package Name: com.najika.digivice
   - Orientation: Landscape or Portrait (choose!)
   - Enable Vulkan: Yes
   - Enable OpenGL ES 3.1: Yes (fallback)

4. Configure Mobile Settings:
   Project Settings → Engine → Rendering:
   - Mobile HDR: Enabled
   - Mobile MSAA: 4x
   - Dynamic Lighting: Enabled
   - Mobile Shaders: ES 3.1 + Vulkan

5. Configure Scalability:
   Project Settings → Engine → Scalability:
   - Quality Levels: Low, Medium, High, Epic
   - Default: High (Snapdragon 888 can handle it!)
   - Enable Adaptive Performance: Yes

6. Save Project Configuration
```

### **TODO 1.3: Setup Version Control**
```bash
# Initialize Git in UE5 project
cd C:\NajikaDigivice_UE5
git init
git lfs install
git lfs track "*.uasset"
git lfs track "*.umap"

# Create .gitignore for UE5
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/UnrealEngine.gitignore

# Initial commit
git add .
git commit -m "Initial UE5 project setup"

# Link to GitHub (optional)
gh repo create NajikaDigivice_UE5 --private
git remote add origin https://github.com/YOUR_USERNAME/NajikaDigivice_UE5.git
git push -u origin main
```

---

## 🎨 PHASE 2: CORE SYSTEMS (Week 2-3)

### **TODO 2.1: Create Najika Character**
```
OPTION A: Import existing VRM model (if available)
1. Get VRM model from C:\Najika_World\assets\models\
2. Convert VRM to FBX using Blender:
   - Install VRM addon for Blender
   - Import VRM
   - Export as FBX with animations
3. Import to UE5:
   - Import FBX as Skeletal Mesh
   - Create Physics Asset
   - Setup Skeleton

OPTION B: Create from scratch
1. Use MetaHuman Creator (if human-like)
2. Or import from Mixamo / Adobe Fuse
3. Customize to match Najika design

CRITICAL:
- Skeletal Mesh name: SK_Najika
- Physics Asset: PHYS_Najika
- Skeleton: SKEL_Najika
- Materials: M_Najika_Body, M_Najika_Hair, M_Najika_Eyes
```

### **TODO 2.2: Animation System**
```
1. Create Animation Blueprint:
   - Name: ABP_Najika
   - Parent: UAnimInstance
   - Skeleton: SKEL_Najika

2. State Machine:
   - Idle
   - Walk
   - Run
   - Jump
   - Talk (for voice calls!)
   - Emotes (Happy, Sad, Angry, etc.)

3. Blend Spaces:
   - BS_Najika_Locomotion (Idle → Walk → Run)
   - BS_Najika_Emotions (Happy ↔ Sad ↔ Angry)

4. Animation Sequences:
   - Import from existing animations or:
   - Download from Mixamo
   - Or create in Blender

5. Facial Animations:
   - Morph Targets for mouth (voice sync!)
   - Eye blink
   - Eyebrow movements
   - Emotion expressions

CRITICAL FOR VOICE CALLS:
- Lip sync must work with Coqui TTS audio!
- Research: Audio2Face or OVRLipSync plugin
```

### **TODO 2.3: World Setup**
```
1. Create Main Level:
   - Name: L_MainWorld
   - Based on existing digivice world

2. Import existing world geometry:
   - Check C:\Najika_World\digivice\static\models\
   - Convert GLTF/GLB to FBX if needed
   - Import to UE5

3. Lighting:
   - Directional Light (Sun)
   - Sky Light (ambient)
   - Post Process Volume (color grading)
   - Enable Lumen (mobile mode)

4. Landscape (if needed):
   - Create landscape for open world
   - Or use modular building pieces

5. Regions (from existing 9 regions):
   - Region 1: Schwarze Mühle (Home)
   - Region 2: Kristallteich (Fishing)
   - Region 3: Weltensee (Fishing)
   - Region 4: Garten (Garden)
   - Region 5: Kampfarena (Battle)
   - Region 6-9: Other locations

   Each region = separate sublevel (Level Streaming!)

6. Collision:
   - Setup collision meshes
   - Navigation mesh (for AI pathfinding)
```

### **TODO 2.4: Camera System**
```
1. Create Camera Manager:
   - Blueprint: BP_NajikaCameraManager
   - Parent: ACameraManager

2. Camera Modes:
   - Third Person (default)
   - First Person
   - Orbit (rotate around Najika)
   - Free Camera (debug)

3. Camera Controls:
   - Touch drag to rotate
   - Pinch to zoom
   - Double tap to reset

4. Camera Collision:
   - Prevent clipping through walls
   - Smooth camera movement

5. Camera Settings:
   - FOV: 90 (adjustable)
   - Near Clip: 10cm
   - Far Clip: 10000cm
```

### **TODO 2.5: Input System**
```
1. Create Input Actions:
   Content/Input/Actions/
   - IA_Move (Vector2D)
   - IA_Look (Vector2D)
   - IA_Jump (Boolean)
   - IA_Interact (Boolean)
   - IA_Menu (Boolean)

2. Create Input Mapping Context:
   Content/Input/IMC_Default
   - Touch screen bindings
   - Keyboard bindings (for PC testing)

3. Touch Controls:
   - Virtual joystick (left side)
   - Virtual buttons (right side)
   - Gesture recognition (swipe, pinch)

4. Implement in Player Controller:
   - BP_NajikaPlayerController
   - Setup Enhanced Input System
```

---

## 🔌 PHASE 3: BACKEND INTEGRATION (Week 4-5)

### **TODO 3.1: Create HTTP Client Plugin**
```
1. Create C++ Plugin:
   - Name: NajikaBackendClient
   - Type: Runtime
   - Location: Plugins/NajikaBackendClient

2. Add Dependencies (NajikaBackendClient.Build.cs):
   PublicDependencyModuleNames.AddRange(new string[] {
       "Core",
       "CoreUObject",
       "Engine",
       "HTTP",
       "Json",
       "JsonUtilities"
   });

3. Create Client Class:
   Source/NajikaBackendClient/Public/NajikaAPIClient.h:

   UCLASS()
   class UNajikaAPIClient : public UObject {
       GENERATED_BODY()
   public:
       UFUNCTION(BlueprintCallable)
       void SendChatMessage(FString Message, FOnChatResponse Callback);

       UFUNCTION(BlueprintCallable)
       void GetNajikaStatus(FOnStatusResponse Callback);

       UFUNCTION(BlueprintCallable)
       void FeedNajika(FOnActionResponse Callback);

       // Add ALL API endpoints!

   private:
       FString BaseURL = "http://127.0.0.1:8000";
       TSharedPtr<IHttpRequest> CreateRequest(FString Endpoint);
   };

4. Implement in .cpp:
   - Use FHttpModule for HTTP requests
   - Parse JSON responses
   - Handle errors gracefully
   - Implement retry logic

5. Test in Blueprint:
   - Create BP_TestBackend
   - Call all API functions
   - Verify responses
```

### **TODO 3.2: Voice Call Integration**
```
1. Create Voice Plugin:
   - Name: NajikaVoiceSystem
   - Type: Runtime
   - Dependencies: HTTP, AudioCapture, AudioMixer

2. Audio Capture (Microphone):
   Source/NajikaVoiceSystem/Private/AudioCapture.cpp:
   - Use FAudioCapture (UE5 built-in)
   - Capture raw PCM audio
   - Convert to WAV
   - Encode to Base64

3. Audio Playback (TTS Response):
   Source/NajikaVoiceSystem/Private/AudioPlayback.cpp:
   - Receive Base64 audio from server
   - Decode to WAV
   - Create USoundWave dynamically
   - Play through AudioComponent

4. Voice Call Manager:
   UCLASS()
   class UVoiceCallManager : public UObject {
       UFUNCTION(BlueprintCallable)
       void StartVoiceCall();

       UFUNCTION(BlueprintCallable)
       void EndVoiceCall();

   private:
       bool bIsCallActive;
       FAudioCapture AudioCapture;
       TArray<uint8> AudioBuffer;
   };

5. Lip Sync Integration:
   - Parse phonemes from Coqui TTS (if available)
   - Or use amplitude-based lip sync
   - Drive Najika facial animations

6. Test:
   - Start voice call in-game
   - Speak into microphone
   - Verify audio sent to backend
   - Verify TTS response played
   - Verify lip sync works
```

### **TODO 3.3: WebSocket Integration (Real-time)**
```
1. Add WebSocket Plugin:
   - Enable "Web Socket Networking" plugin in UE5

2. Create WebSocket Manager:
   UCLASS()
   class UWebSocketManager : public UObject {
       UFUNCTION(BlueprintCallable)
       void Connect(FString URL);

       UFUNCTION(BlueprintCallable)
       void SendMessage(FString Message);

       UPROPERTY(BlueprintAssignable)
       FOnMessageReceived OnMessageReceived;
   };

3. Use for:
   - Real-time state updates
   - Proactive messages from Najika
   - Live status changes
   - Multiplayer (future!)

4. Implement heartbeat (keep connection alive)
```

### **TODO 3.4: State Management**
```
1. Create Game Instance:
   - Blueprint: BP_NajikaGameInstance
   - Parent: UGameInstance
   - Persists across level changes

2. Store:
   - Najika Status (Hunger, Energy, Happiness, HP, XP)
   - User Profile
   - Chat History (recent messages)
   - Voice Call Status
   - Connection Status

3. Auto-sync with backend:
   - Poll /api/najika/status every 5 seconds
   - Update UI in real-time
   - Cache locally for offline mode

4. Save System:
   - Use USaveGame
   - Save local state
   - Sync with backend on reconnect
```

---

## 🎮 PHASE 4: GAMEPLAY SYSTEMS (Week 6-7)

### **TODO 4.1: Tamagotchi System**
```
1. Create Tamagotchi Widget:
   - UMG Widget: WBP_TamagotchiUI
   - Shows: Hunger, Energy, Happiness, HP bars
   - Shows: Level, XP progress
   - Shows: Current mood/emotion

2. Hunger/Energy System:
   - Decreases over time (synced with backend)
   - Feed button → /api/najika/feed
   - Drink button → /api/najika/drink
   - Visual feedback (particles, animation)

3. Happiness System:
   - Affected by interactions
   - Praise button → /api/najika/praise
   - Play minigames → increase happiness

4. Auto-Care (from backend):
   - Listen to backend for auto-care events
   - Show notification: "Najika hat sich selbst versorgt!"
   - Play animation

5. Death/Revival:
   - If HP reaches 0 → death state
   - Revival via item or wait time
   - Dramatic animation!
```

### **TODO 4.2: Battle System**
```
1. Battle UI:
   - WBP_BattleUI
   - Show: Player HP, Enemy HP
   - Show: Available skills
   - Show: Turn indicator

2. Battle Manager:
   - Blueprint: BP_BattleManager
   - Handles turn-based combat
   - Communicates with backend /api/battle/*

3. Skills System:
   - Load skills from backend /api/battle/skills
   - Show skill icons + descriptions
   - Implement skill animations

4. Enemy System:
   - Spawn enemies from backend data
   - 3D models or 2D sprites
   - Damage numbers (floating text)

5. Battle Flow:
   - Enter battle → transition animation
   - Turn-based combat loop
   - Win → rewards (XP, items)
   - Lose → game over or retry
```

### **TODO 4.3: Minigames**
```
1. Fishing Game:
   - Fishing rod mechanic (tap/hold)
   - Fish spawning
   - Catch animation
   - Reward system

2. Rhythm Game:
   - Note spawning
   - Hit timing
   - Score system
   - Music playback

3. Reflex Game:
   - Target spawning
   - Tap accuracy
   - Speed increase
   - High score

4. Garden Game:
   - Plant growth simulation
   - Watering mechanic
   - Harvest rewards

Each minigame:
- Separate level or mode
- UI overlay
- Backend integration (/api/minigame/*)
- Persistent progress
```

### **TODO 4.4: Scanner System (Camera)**
```
1. Camera Access:
   - Use Android Camera API plugin
   - Or UE5 built-in camera capture

2. Object Detection:
   - OPTION A: Send frame to backend YOLO API
   - OPTION B: Run TFLite model locally (mobile ML)

3. Scanner UI:
   - Camera viewfinder overlay
   - Detected objects highlighted
   - Info panel (object name, description)

4. Use Cases:
   - Scan real-world objects
   - Najika comments on what she sees
   - Collect items from scanned objects
```

---

## 🎨 PHASE 5: UI/UX POLISH (Week 8)

### **TODO 5.1: Main Menu**
```
1. Create Menu Widget:
   - WBP_MainMenu
   - Buttons:
     - Start / Continue
     - Settings
     - About
     - Exit

2. Loading Screen:
   - WBP_LoadingScreen
   - Progress bar
   - Loading tips
   - Najika animation

3. Pause Menu:
   - WBP_PauseMenu
   - Resume
   - Settings
   - Return to Menu
```

### **TODO 5.2: HUD Design**
```
1. Create Main HUD:
   - WBP_MainHUD
   - Top: Najika status bars (minimized)
   - Bottom: Action buttons
   - Center: Chat bubble (when Najika talks)

2. Chat Interface:
   - WBP_ChatUI
   - Message history (scrollable)
   - Input field (text or voice toggle)
   - Send button
   - Close button

3. Voice Call UI:
   - WBP_VoiceCallUI
   - Call status indicator
   - Audio visualizer (waveform)
   - Mute button
   - End call button
   - Transcript display

4. Notifications:
   - WBP_Notification
   - Slide in from top
   - Auto-dismiss after 3 seconds
   - Stacking support
```

### **TODO 5.3: Settings Menu**
```
1. Create Settings Widget:
   - WBP_Settings
   - Tabs: Graphics, Audio, Controls, Privacy

2. Graphics Settings:
   - Quality preset (Low/Med/High/Epic)
   - Resolution scale
   - Frame rate limit
   - VSync toggle

3. Audio Settings:
   - Master volume
   - Voice volume
   - Music volume
   - SFX volume

4. Controls Settings:
   - Virtual joystick size
   - Button layout
   - Camera sensitivity
   - Invert Y axis

5. Privacy Settings:
   - Data collection toggle
   - Camera permission
   - Microphone permission
   - Location permission
```

### **TODO 5.4: Visual Effects**
```
1. Particles (Niagara):
   - Level up effect
   - Healing effect
   - Damage effect
   - Food eating effect
   - Love hearts (when happy)

2. Post-Processing:
   - Bloom (subtle)
   - Color grading (warm tone)
   - Vignette (optional)
   - Depth of field (focus on Najika)

3. Transitions:
   - Fade in/out
   - Slide transitions
   - Battle start transition

4. Feedback:
   - Screen shake (on impact)
   - Slow motion (dramatic moments)
   - Color flash (damage/heal)
```

---

## 🔐 PHASE 6: SECURITY & OPTIMIZATION (Week 9)

### **TODO 6.1: Security Implementation**
```
1. Biometric Authentication:
   - Android Keystore integration
   - BiometricPrompt API (via JNI or plugin)
   - Protect sensitive data

2. Encrypted Storage:
   - Use EncryptedSharedPreferences (Android)
   - Encrypt save files
   - Secure API keys

3. Network Security:
   - HTTPS only (if server supports)
   - Certificate pinning
   - Request signing

4. Privacy:
   - Implement permissions system
   - Ask for camera/mic only when needed
   - Privacy policy integration
```

### **TODO 6.2: Performance Optimization**
```
1. Profiling:
   - Use UE5 built-in profiler
   - Identify bottlenecks:
     - Draw calls
     - Texture memory
     - Animation cost
     - Script execution

2. LOD (Level of Detail):
   - Create LOD chains for meshes
   - Automatic LOD generation
   - Distance-based switching

3. Texture Optimization:
   - Compress textures (ASTC)
   - Use texture streaming
   - Reduce resolution where possible

4. Lighting:
   - Bake static lighting
   - Use Lumen mobile mode
   - Limit dynamic lights

5. Culling:
   - Frustum culling
   - Occlusion culling
   - Distance culling
```

### **TODO 6.3: Battery Optimization**
```
1. Adaptive Performance:
   - Use Android Adaptive Performance API
   - Scale quality based on thermal state
   - Reduce frame rate when not focused

2. Idle Optimization:
   - Lower frame rate when idle (30 FPS)
   - Pause unnecessary updates
   - Stop animations when off-screen

3. Network Optimization:
   - Batch API calls
   - Reduce polling frequency
   - Use WebSocket for real-time (more efficient)

4. Wake Lock:
   - Only keep screen on when needed
   - Release wake lock when idle
```

### **TODO 6.4: Memory Management**
```
1. Asset Streaming:
   - Use Level Streaming
   - Load/unload levels dynamically
   - Async asset loading

2. Texture Streaming:
   - Enable texture streaming
   - Set appropriate pool sizes
   - Monitor memory usage

3. Garbage Collection:
   - Regular GC cycles
   - Unload unused assets
   - Object pooling for frequently spawned objects

4. Crash Prevention:
   - Exception handling
   - Graceful degradation
   - Fallback systems
```

---

## 📦 PHASE 7: PACKAGING & DEPLOYMENT (Week 10)

### **TODO 7.1: Build Configuration**
```
1. Shipping Build Settings:
   Project Settings → Packaging:
   - Build Configuration: Shipping
   - Compress assets: Yes
   - Exclude editor content: Yes
   - For Distribution: Yes

2. Android Settings:
   - App ID: com.najika.digivice
   - Version: 1.0.0
   - Minimum SDK: 29
   - Target SDK: 34
   - Permissions:
     - CAMERA
     - RECORD_AUDIO
     - INTERNET
     - ACCESS_NETWORK_STATE
     - VIBRATE

3. Signing:
   - Generate keystore:
     keytool -genkey -v -keystore najika-release.keystore \
     -alias najika -keyalg RSA -keysize 2048 -validity 10000
   - Configure in Project Settings → Android → Distribution Signing

4. Optimization:
   - Enable Play Asset Delivery
   - Enable App Bundle (.aab)
   - Exclude unused features
```

### **TODO 7.2: Testing on Device**
```
1. Install on Xiaomi 11T Pro:
   - USB Debugging enabled
   - Transfer APK via ADB:
     adb install NajikaDigivice.apk

2. Test Checklist:
   - [ ] App launches successfully
   - [ ] 3D world renders correctly
   - [ ] Najika character animates
   - [ ] Camera controls work
   - [ ] Touch controls responsive
   - [ ] Voice calls work (mic + speaker)
   - [ ] Chat messages send/receive
   - [ ] Backend connection stable
   - [ ] UI scales correctly
   - [ ] Performance acceptable (30+ FPS)
   - [ ] Battery drain reasonable
   - [ ] No crashes
   - [ ] Permissions work
   - [ ] Save/load works

3. Performance Testing:
   - Monitor FPS (use UE5 stat commands)
   - Monitor memory usage
   - Monitor CPU/GPU usage
   - Monitor battery drain
   - Monitor network traffic

4. Long-term Testing:
   - Leave running for 1 hour
   - Test different scenarios
   - Check for memory leaks
   - Check for crashes
```

### **TODO 7.3: Bug Fixing**
```
1. Document all bugs found:
   Create: BUGS.md
   Format:
   - Bug ID: #001
   - Severity: Critical/High/Medium/Low
   - Description: ...
   - Steps to reproduce: ...
   - Expected behavior: ...
   - Actual behavior: ...

2. Fix critical bugs first

3. Regression testing after each fix

4. Update changelog
```

### **TODO 7.4: App Store Preparation**
```
1. Create Store Listing:
   - App Name: Najika Digivice
   - Short Description: (50 chars)
   - Full Description: (4000 chars)
   - Category: Entertainment / Simulation
   - Content Rating: Teen (13+)

2. Screenshots:
   - Take 8 screenshots (1080x1920)
   - Show all major features
   - Add text overlays

3. Feature Graphic:
   - 1024x500 banner image
   - Professional design

4. Privacy Policy:
   - Create privacy policy page
   - Host on website or GitHub Pages
   - Link in app store listing

5. Closed Beta (Optional):
   - Upload to Google Play Console
   - Create closed testing track
   - Invite testers
   - Collect feedback
```

---

## 🔄 PHASE 8: ITERATIVE IMPROVEMENTS (Week 11-12)

### **TODO 8.1: User Feedback**
```
1. Implement Feedback System:
   - In-app feedback button
   - Send to server or email
   - Rate app prompt

2. Analytics (Optional):
   - Firebase Analytics
   - Track usage patterns
   - Identify popular features

3. A/B Testing:
   - Test different UI layouts
   - Test different features
```

### **TODO 8.2: Feature Additions**
```
Based on user feedback, add:
1. New minigames
2. New locations
3. New Najika outfits
4. Multiplayer features (future)
5. AR mode (using ARCore)
```

### **TODO 8.3: Content Updates**
```
1. Regular updates:
   - New dialogue lines for Najika
   - Seasonal events
   - Holiday themes
   - New items/skins

2. Backend updates:
   - New LoRA training data
   - Improved AI responses
   - New voice lines (Coqui TTS)
```

---

## 🎯 PHASE 9: UEFN PREPARATION (Future)

### **TODO 9.1: Code Audit for UEFN**
```
1. Identify Blueprints that need conversion to Verse:
   - List all Blueprint classes
   - Mark which are simple (easy to convert)
   - Mark which are complex (need refactoring)

2. Create Verse learning plan:
   - Study Verse documentation
   - Complete Verse tutorials
   - Build test projects in UEFN

3. Asset preparation:
   - Ensure all assets are Fortnite-compatible
   - Check polygon counts (optimize if needed)
   - Check texture sizes (optimize if needed)
   - Verify materials work in Fortnite
```

### **TODO 9.2: UEFN Migration Plan**
```
1. Create UEFN project structure
2. Import Najika character as Fortnite skin
3. Convert Blueprints to Verse (AI-assisted)
4. Import world as Fortnite island
5. Setup backend connection (UEFN → Python server)
6. Test in Fortnite Creative
7. Publish to Fortnite Island Code
```

---

## 📊 SUCCESS METRICS

### **Technical Metrics:**
```
✅ FPS: 30+ (minimum), 60 (target)
✅ Memory: <2GB (Xiaomi has 8GB)
✅ Battery: 4+ hours continuous use
✅ Load Time: <10 seconds
✅ Backend Latency: <500ms
✅ Voice Call Latency: <500ms STT + TTS
✅ Crash Rate: <0.1%
```

### **Feature Completion:**
```
✅ All existing features ported
✅ Voice calls working
✅ Chat working
✅ Tamagotchi system working
✅ Battle system working
✅ Minigames working
✅ Scanner working
✅ UI responsive
✅ Stable on Xiaomi 11T Pro
```

---

## 🚨 CRITICAL RULES

### **DO NOT BREAK:**
```
❌ DO NOT delete C:\Najika_World (existing system!)
❌ DO NOT modify backend without backup
❌ DO NOT commit large binary files to Git (use LFS!)
❌ DO NOT hardcode secrets (API keys, etc.)
```

### **ALWAYS:**
```
✅ Test on device after major changes
✅ Backup before risky operations
✅ Document all API changes
✅ Keep backend and frontend in sync
✅ Profile performance regularly
```

---

## 📚 RESOURCES

### **Documentation:**
```
- Unreal Engine 5 Docs: https://docs.unrealengine.com/5.6/
- Android Game Development: https://developer.android.com/games
- UE5 Mobile: https://docs.unrealengine.com/5.6/mobile/
- UEFN Docs: https://dev.epicgames.com/documentation/uefn
- Verse Language: https://dev.epicgames.com/documentation/verse
```

### **Tutorials:**
```
- UE5 Mobile Game Dev: Search YouTube
- UE5 Blueprint to C++: Official Unreal Learning
- Android Optimization: GDC talks
- Voice Integration: Search GitHub examples
```

### **Community:**
```
- Unreal Engine Forums: https://forums.unrealengine.com/
- Unreal Slackers Discord: https://unrealslackers.org/
- r/unrealengine: Reddit community
- UEFN Discord: Official Discord
```

---

## ✅ FINAL CHECKLIST

**Before starting:**
- [ ] Read this entire TODO document
- [ ] Backup existing Najika_World system
- [ ] Install all required software (UE5, VS2022, Android SDK)
- [ ] Setup development environment
- [ ] Test backend server is running

**During development:**
- [ ] Follow phases in order
- [ ] Test after each major change
- [ ] Document issues and solutions
- [ ] Regular commits to Git
- [ ] Keep TODO updated with progress

**Before deployment:**
- [ ] Full testing on Xiaomi 11T Pro
- [ ] All features working
- [ ] Performance acceptable
- [ ] No critical bugs
- [ ] Signed with release keystore
- [ ] Privacy policy created
- [ ] Store listing prepared

---

## 🎉 SUCCESS!

**When this TODO is complete, you will have:**
- ✅ Fully functional Najika Digivice app (Unreal Engine 5)
- ✅ All existing features ported and improved
- ✅ Professional graphics (Nanite, Lumen)
- ✅ Optimized for mobile (Snapdragon 888)
- ✅ Secure (Biometric, Encrypted Storage)
- ✅ Ready for UEFN port (Fortnite!)
- ✅ Deployable to Google Play Store

**Estimated Timeline:** 10-12 weeks (full-time development)

**Good luck! Najika believes in you! 💜🔥**

---

**END OF TODO**
**Version:** 1.0
**Last Updated:** 2025-11-11
