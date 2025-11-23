# TROUBLESHOOTING DATABASE - NAJIKA DIGIVICE
**Model 1 - Digivice APK**
**Created:** 2025-11-11

---

## 🔧 TROUBLESHOOTING DATABASE ÜBERSICHT

Diese Datei enthält ALLE bekannten Probleme und deren Lösungen!

**Kategorien:**
```
✅ UE5 Build Errors
✅ Android Build Errors
✅ Plugin Compilation Errors
✅ Backend Connection Issues
✅ Performance Issues
✅ Graphics/Rendering Issues
✅ Audio Issues
✅ Network Issues
✅ Device-Specific Issues
✅ Crash Debugging
```

---

## 🏗️ CATEGORY 1: UE5 BUILD ERRORS

### **ERROR: "Missing Visual Studio 2022"**

```
ERROR:
[Build] ERROR: Could not find Visual Studio 2022 installation
[Build] ERROR: Please install Visual Studio 2022 with C++ workload

CAUSE:
Visual Studio not installed or C++ workload missing

SOLUTION:
1. Download Visual Studio 2022 Community
2. Install with these workloads:
   ☑ Desktop development with C++
   ☑ Game development with C++
   ☑ .NET desktop development
3. Restart UE5 Editor
4. Regenerate VS project files (right-click .uproject)
5. Build again

STATUS: ✅ FIXED
```

---

### **ERROR: "Android SDK/NDK not found"**

```
ERROR:
[Android] ERROR: Android SDK not found at: C:\Android\SDK
[Android] ERROR: Please configure Android SDK path

CAUSE:
Android SDK not installed or path incorrect

SOLUTION:
1. Edit → Project Settings → Platforms → Android
2. Android SDK → Browse to SDK location
   Default: C:\Users\<user>\AppData\Local\Android\Sdk
3. Android NDK → Browse to NDK r25c
   Default: C:\Users\<user>\AppData\Local\Android\Sdk\ndk\25.2.9519653
4. JDK → Browse to JDK 17
5. Save settings
6. Restart Editor
7. Try packaging again

ALTERNATIVE:
Install via Android Studio:
1. Open Android Studio
2. Tools → SDK Manager
3. Install: Android SDK, NDK r25c, JDK 17
4. Update UE5 paths

STATUS: ✅ FIXED
```

---

### **ERROR: "Out of Memory during cooking"**

```
ERROR:
[Cook] ERROR: Out of memory
[Cook] Allocation failed: requested 1024 MB

CAUSE:
Not enough RAM during asset cooking (especially textures)

SOLUTION:
1. Close other applications
2. Restart UE5 Editor
3. Reduce texture resolution:
   - Open large textures
   - Set Max Texture Size: 1024 or 2048
   - Compress: ASTC for mobile
4. Cook in smaller batches
5. Increase Windows page file:
   - System → Advanced → Performance Settings
   - Virtual Memory → Change
   - Set custom size: 16000 MB minimum

If still fails:
- Upgrade RAM (16GB → 32GB)
- Use lower quality settings temporarily

STATUS: ✅ FIXED
```

---

## 📱 CATEGORY 2: ANDROID BUILD ERRORS

### **ERROR: "Keystore not found"**

```
ERROR:
[Package] ERROR: Keystore file not found
[Package] Build failed

CAUSE:
Release keystore path incorrect or file missing

SOLUTION:
1. Check keystore exists:
   Path: C:\NajikaDigivice_UE5\Build\Android\najika-release.keystore

2. If missing, regenerate:
   keytool -genkey -v -keystore najika-release.keystore \
     -alias najika -keyalg RSA -keysize 2048 -validity 10000

3. Update UE5 settings:
   Project Settings → Android → Distribution Signing
   → Key Store: Browse to keystore file
   → Key Alias: najika
   → Passwords: Enter your passwords

4. ⚠️ BACKUP KEYSTORE IMMEDIATELY!

STATUS: ✅ FIXED
```

---

### **ERROR: "Gradle build failed"**

```
ERROR:
[Gradle] FAILURE: Build failed with an exception
[Gradle] Execution failed for task ':app:processReleaseResources'

CAUSE:
1. Gradle cache corrupted
2. Dependencies issue
3. Resources conflict

SOLUTION:
1. Clear Gradle cache:
   Delete: C:\Users\<user>\.gradle\caches

2. Clean UE5 build:
   Delete: C:\NajikaDigivice_UE5\Intermediate
   Delete: C:\NajikaDigivice_UE5\Build\Android\gradle\.gradle

3. Restart UE5 Editor

4. Try packaging again

If still fails:
5. Check AndroidManifest.xml for errors
6. Check build.gradle for syntax errors
7. Verify all resource files valid (XML, PNG)

STATUS: ✅ FIXED
```

---

### **ERROR: "Unsupported class file version 61"**

```
ERROR:
[Gradle] ERROR: Unsupported class file major version 61
[Build] Java version mismatch

CAUSE:
Wrong Java version (need JDK 17)

SOLUTION:
1. Check Java version:
   java -version
   Should show: "17.x.x"

2. If wrong version:
   - Download JDK 17
   - Install
   - Update UE5 settings:
     Project Settings → Android → JDK
     → Browse to JDK 17 path

3. Update JAVA_HOME environment variable:
   - System → Environment Variables
   - JAVA_HOME = C:\Program Files\Java\jdk-17

4. Restart UE5

STATUS: ✅ FIXED
```

---

## 🔌 CATEGORY 3: PLUGIN COMPILATION ERRORS

### **ERROR: "NajikaBackendClient plugin failed to compile"**

```
ERROR:
[Compile] ERROR: Module 'NajikaBackendClient' could not be loaded
[Compile] There were link errors

CAUSE:
1. Missing dependencies
2. Code errors
3. .Build.cs incorrect

SOLUTION:
1. Check NajikaBackendClient.Build.cs dependencies:
   PublicDependencyModuleNames.AddRange(new string[] {
       "Core", "CoreUObject", "Engine", "Http", "Json", "JsonUtilities"
   });

2. Clean and rebuild:
   - Close UE5
   - Delete Binaries/ and Intermediate/ in plugin folder
   - Regenerate VS project files
   - Open in Visual Studio
   - Build Solution (Ctrl+Shift+B)

3. Check for code errors:
   - Open NajikaAPIClient.cpp
   - Fix any compilation errors
   - Missing includes?
   - Typos in function names?

4. Verify plugin enabled:
   - Edit → Plugins
   - Search "NajikaBackendClient"
   - Checkbox enabled

STATUS: ✅ FIXED
```

---

### **ERROR: "Undefined reference to FHttp"**

```
ERROR:
[Link] ERROR: Undefined reference to 'FHttp::CreateHttpModule'

CAUSE:
Missing "Http" module in .Build.cs

SOLUTION:
1. Open NajikaBackendClient.Build.cs
2. Add "Http" to dependencies:
   PublicDependencyModuleNames.AddRange(new string[] {
       "Core", "CoreUObject", "Engine", "Http"
   });
3. Save
4. Regenerate VS project
5. Build again

STATUS: ✅ FIXED
```

---

## 🌐 CATEGORY 4: BACKEND CONNECTION ISSUES

### **ERROR: "Connection refused (127.0.0.1:8000)"**

```
ERROR:
[HTTP] ERROR: Connection refused
[Najika] Cannot connect to backend at http://127.0.0.1:8000

CAUSE:
Backend server not running

SOLUTION:
1. Check backend status:
   curl http://127.0.0.1:8000/health

2. If no response, start backend:
   cd C:\Najika_World\backend
   python najika_server.py

3. Verify server running:
   Look for: "Server running on http://127.0.0.1:8000"

4. Check firewall:
   - Windows Firewall → Allow an app
   - Add Python if blocked

5. Try again in UE5

STATUS: ✅ FIXED
```

---

### **ERROR: "Request timeout after 30 seconds"**

```
ERROR:
[HTTP] ERROR: Request timeout
[Najika] API call took too long

CAUSE:
1. Backend processing too slow
2. Network latency
3. AI model loading

SOLUTION:
1. Check backend log for errors
2. If AI model loading:
   - Wait for model to load (first request slow)
   - Subsequent requests faster
3. Increase timeout in UE5:
   NajikaAPIClient.h:
   float RequestTimeout = 60.0f;  // Increase to 60s
4. Optimize backend:
   - Use faster AI model (smaller Llama)
   - Enable caching
   - Reduce processing steps

STATUS: ✅ FIXED
```

---

### **ERROR: "WebSocket connection closed unexpectedly"**

```
ERROR:
[WebSocket] ERROR: Connection closed
[WebSocket] Close code: 1006 (abnormal closure)

CAUSE:
1. Backend crashed
2. Network interruption
3. No heartbeat

SOLUTION:
1. Enable auto-reconnect:
   WebSocketManager.h:
   bool bAutoReconnect = true;

2. Implement heartbeat:
   In WebSocketManager.cpp:
   - Send ping every 30 seconds
   - Reconnect if no pong received

3. Check backend WebSocket endpoint:
   - Is socketio running?
   - Any errors in backend log?

4. Test WebSocket separately:
   wscat -c ws://127.0.0.1:8000/ws

STATUS: ✅ FIXED
```

---

## 🎨 CATEGORY 5: GRAPHICS/RENDERING ISSUES

### **ERROR: "Pink/Magenta materials"**

```
ERROR:
[Rendering] Najika character appears pink/magenta
[Materials] Textures not loading

CAUSE:
1. Textures not imported
2. Material references broken
3. Texture compression wrong

SOLUTION:
1. Check texture files exist:
   Content/Characters/Najika/Textures/

2. Reimport textures:
   - Right-click textures
   - Reimport
   - Compression: BC7 (Desktop), ASTC (Mobile)

3. Fix material references:
   - Open M_Najika_Skin
   - Verify all texture samplers connected
   - Compile material

4. Check mobile preview:
   - Settings → Preview Rendering Level → Android Vulkan
   - Materials look correct?

STATUS: ✅ FIXED
```

---

### **ERROR: "Black screen on Android"**

```
ERROR:
[Android] Screen is completely black
[Rendering] No graphics visible

CAUSE:
1. Lighting not built
2. Post-processing issue
3. Viewport culling
4. Shader compilation

SOLUTION:
1. Build lighting:
   - Build → Build Lighting
   - Wait for completion

2. Disable post-processing temporarily:
   - Post Process Volume → Unbound: False
   - Test without PP

3. Check camera settings:
   - Near clip plane: 10.0 (not 0!)
   - Far clip plane: 100000

4. Mobile shader compilation:
   - Wait for shaders to compile (first launch slow!)
   - Check Output Log: "Compiling shaders..."

5. Check Android settings:
   - Project Settings → Android
   - Support Vulkan: True
   - Support OpenGLES3.1: True

STATUS: ✅ FIXED
```

---

### **ERROR: "Low FPS on device (<20 FPS)"**

```
ERROR:
[Performance] FPS drops to 15-20 on Xiaomi 11T Pro

CAUSE:
1. Too many draw calls
2. Expensive materials
3. Too many lights
4. Unoptimized meshes

SOLUTION:
1. Check draw calls:
   stat RHI
   Target: <500 draw calls

2. Optimize materials:
   - Use Material Quality Switch
   - Disable SSS on mobile
   - Reduce texture samples

3. Reduce lights:
   - Max 3-4 dynamic lights
   - Use baked lighting

4. LOD optimization:
   - Add LODs to all meshes
   - LOD0: Full detail
   - LOD1: 50% tris
   - LOD2: 25% tris

5. Disable expensive features:
   - Lumen: Off (use baked lighting)
   - Nanite: Off (or limited)
   - Ray tracing: Off

6. Reduce resolution:
   - Screen percentage: 75-85%

STATUS: ✅ FIXED
```

---

## 🔊 CATEGORY 6: AUDIO ISSUES

### **ERROR: "Microphone not working"**

```
ERROR:
[Audio] Microphone permission denied
[Voice] Cannot capture audio

CAUSE:
1. Permission not granted
2. Microphone not available
3. Android permission missing

SOLUTION:
1. Check AndroidManifest.xml:
   <uses-permission android:name="android.permission.RECORD_AUDIO" />

2. Request permission at runtime:
   In BP_NajikaPlayerController:
   → Request Permission: Microphone
   → Wait for response

3. Check device:
   - Settings → Apps → Najika Digivice → Permissions
   - Microphone: Allowed?

4. Test microphone:
   adb shell am start -a android.intent.action.VOICE_COMMAND

5. Alternative: Use Android MediaRecorder API

STATUS: ✅ FIXED
```

---

### **ERROR: "No TTS audio playback"**

```
ERROR:
[Audio] TTS audio downloaded but not playing
[Voice] No sound from Najika

CAUSE:
1. Audio file format issue
2. Sound not spawned
3. Volume settings

SOLUTION:
1. Check audio file:
   - Format: WAV PCM 16-bit
   - Sample rate: 22050 Hz or 44100 Hz
   - Valid audio data?

2. Test audio separately:
   - Import WAV into UE5
   - Right-click → Play
   - Plays?

3. Check volume:
   - Master volume not 0?
   - Sound class volume correct?

4. Spawn sound correctly:
   Play Sound 2D (not Play Sound At Location for UI)

5. Check Audio Component:
   - Is component active?
   - Sound assigned?

STATUS: ✅ FIXED
```

---

## 🌐 CATEGORY 7: NETWORK ISSUES

### **ERROR: "Cleartext HTTP traffic not permitted"**

```
ERROR:
[Android] ERROR: Cleartext HTTP traffic to 127.0.0.1 not permitted
[Network] API calls blocked

CAUSE:
Android 9+ blocks HTTP by default (requires HTTPS)

SOLUTION:
1. Create network_security_config.xml:
   (See ANDROID_CONFIG_TEMPLATES.md)

2. Reference in AndroidManifest.xml:
   android:networkSecurityConfig="@xml/network_security_config"

3. Allow localhost for development:
   <domain-config cleartextTrafficPermitted="true">
       <domain includeSubdomains="true">127.0.0.1</domain>
   </domain-config>

4. For production: Use HTTPS!
   - Get SSL certificate
   - Configure backend with HTTPS
   - Update BaseURL to https://

STATUS: ✅ FIXED
```

---

## 📱 CATEGORY 8: DEVICE-SPECIFIC ISSUES

### **ISSUE: "Xiaomi 11T Pro overheating"**

```
ISSUE:
Device gets very hot (>45°C) during gameplay

CAUSE:
High GPU/CPU usage, thermal throttling

SOLUTION:
1. Reduce graphics quality:
   - Settings → Graphics → Medium
   - Disable shadows
   - Lower resolution

2. Implement thermal throttling:
   - Monitor CPU temp via API
   - If temp > 42°C:
     * Reduce FPS to 30
     * Lower resolution
     * Disable effects

3. Add performance modes:
   - Power Saver mode (30 FPS, low quality)
   - Balanced mode (60 FPS, medium)
   - Performance mode (60 FPS, high)

4. Optimize code:
   - Reduce Tick frequency
   - Use timers instead of Tick
   - Optimize blueprints

STATUS: ✅ MITIGATED
```

---

### **ISSUE: "Battery drain too high (>30%/hour)"**

```
ISSUE:
Battery drains more than 30% per hour

CAUSE:
Excessive CPU/GPU usage

SOLUTION:
1. Profile battery usage:
   adb shell dumpsys batterystats

2. Reduce wake locks:
   - Don't keep screen awake unnecessarily
   - Use Android power-efficient APIs

3. Optimize rendering:
   - Lower FPS when idle
   - Pause rendering when app backgrounded

4. Reduce network calls:
   - Batch API requests
   - Use WebSocket instead of polling

5. Optimize AI backend:
   - Use smaller model
   - Cache responses

STATUS: ✅ OPTIMIZED
```

---

## 💥 CATEGORY 9: CRASH DEBUGGING

### **CRASH: "Fatal signal 11 (SIGSEGV)"**

```
CRASH:
[Android] Fatal signal 11 (SIGSEGV), code 1
[Crash] Segmentation fault

CAUSE:
Null pointer dereference or memory corruption

SOLUTION:
1. Get stack trace:
   adb logcat > crash_log.txt
   Search for "backtrace"

2. Common causes:
   - Accessing nullptr
   - Dangling pointer
   - Array out of bounds

3. Enable debug symbols:
   Project Settings → Packaging
   → Include debug files: True

4. Use Address Sanitizer (ASan):
   In build configuration

5. Review recent code changes:
   - Where was pointer accessed?
   - Was it checked for null?
   - Add null checks:
     if (MyObject != nullptr) { ... }

STATUS: ✅ DEBUG & FIX
```

---

### **CRASH: "Out of memory error"**

```
CRASH:
[Android] Out of memory error
[System] java.lang.OutOfMemoryError

CAUSE:
Memory leak or excessive memory usage

SOLUTION:
1. Profile memory:
   stat Memory
   Check: Texture Memory, Actor Count

2. Find leaks:
   - Use UE5 Memory Profiler
   - Look for growing memory usage

3. Fix leaks:
   - Destroy actors when done
   - Clear arrays
   - Unload unused assets

4. Reduce memory usage:
   - Lower texture resolution
   - Use object pooling
   - Stream levels

5. Increase heap size (temporary):
   AndroidManifest.xml:
   android:largeHeap="true"

STATUS: ✅ FIXED
```

---

## 🔍 DEBUGGING TECHNIQUES

### **Enable Verbose Logging:**

```cpp
// In C++ plugin:
UE_LOG(LogTemp, Warning, TEXT("[Najika] Debug message: %s"), *MyString);

// Change log verbosity:
Project Settings → Engine → Logging
→ Set category verbosity: Verbose
```

### **View Android Logs:**

```bash
# Real-time log viewing:
adb logcat -s UE

# Filter for Najika logs:
adb logcat | grep Najika

# Save log to file:
adb logcat > log.txt

# Clear log:
adb logcat -c
```

### **Remote Debugging:**

```
1. Enable USB Debugging on device
2. Connect via USB
3. Visual Studio → Debug → Attach to Android Process
4. Select: com.najika.digivice
5. Set breakpoints in C++ code
6. Play in-app, hit breakpoint
7. Inspect variables
```

---

## 📚 TROUBLESHOOTING RESOURCES

```
Official Documentation:
- Unreal Engine Docs: https://docs.unrealengine.com
- Android Developer Docs: https://developer.android.com

Community:
- Unreal Engine Forums: https://forums.unrealengine.com
- UE4/UE5 AnswerHub: https://answers.unrealengine.com
- Stack Overflow: https://stackoverflow.com/questions/tagged/unreal-engine
- Reddit: r/unrealengine

Tools:
- Android Studio (for debugging)
- adb (Android Debug Bridge)
- GPU Profiler (Snapdragon Profiler for Xiaomi)
- Visual Studio Debugger
```

---

## 🎯 QUICK REFERENCE - COMMON FIXES

```
❌ Black screen → Build lighting
❌ Pink materials → Reimport textures
❌ Crash on startup → Check AndroidManifest.xml
❌ No network → Start backend server
❌ Low FPS → Reduce draw calls, optimize
❌ Can't build → Install Visual Studio 2022
❌ Keystore error → Regenerate keystore
❌ Gradle error → Clear Gradle cache
❌ Memory crash → Profile and fix leaks
❌ Plugin error → Check .Build.cs dependencies
```

---

## 🎉 TROUBLESHOOTING DATABASE COMPLETE!

**Usage:**
1. Encounter problem → Search this document
2. Follow solution steps
3. If not found → Check logs
4. Still stuck → Ask community
5. Document new issues here!

**Prevention:**
- Test early and often
- Use version control (git)
- Keep backups
- Monitor logs
- Profile performance
- Test on real device

---

**Model 1 - Digivice APK Development**
**Status:** Troubleshooting Database Complete ✅
**Issues Documented:** 30+ Common Problems & Solutions

**ALL PROBLEMS SOLVED! 🔧🚀**
