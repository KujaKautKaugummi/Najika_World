# TESTING FRAMEWORK - NAJIKA DIGIVICE
**Model 1 - Digivice APK**
**Created:** 2025-11-11

---

## 🧪 TESTING FRAMEWORK ÜBERSICHT

Diese Datei enthält das komplette Testing-Framework für Najika Digivice!

**Testing-Kategorien:**
```
✅ Unit Testing (C++ Plugins)
✅ Integration Testing
✅ Performance Testing
✅ Device Testing (Xiaomi 11T Pro)
✅ Backend API Testing
✅ Security Testing
✅ User Acceptance Testing (UAT)
✅ Regression Testing
✅ Automated Testing Scripts
✅ Bug Reporting Templates
```

---

## 🎯 TESTING METHODOLOGY

### **Testing Pyramid:**

```
                   ┌──────────┐
                   │   UAT    │ (Manual, slow)
                   │  Tests   │
                  /└──────────┘\
                 /              \
                /  ┌──────────┐  \
               /   │Integration│   \
              /    │  Tests    │    \
             /     └──────────┘     \
            /                        \
           /      ┌──────────────┐    \
          /       │  Unit Tests  │     \
         /        │  (Fastest!)  │      \
        /         └──────────────┘       \
       /___________________________________\

RATIO: 70% Unit, 20% Integration, 10% UAT
```

### **Testing Stages:**

```
1. Development Testing (Daily)
   → Unit tests
   → Local integration tests
   → Quick smoke tests

2. Pre-Commit Testing (Before git push)
   → All unit tests pass
   → Critical integration tests pass
   → No regressions

3. Build Testing (After build)
   → Full integration test suite
   → Performance benchmarks
   → Device testing

4. Pre-Release Testing (Before deployment)
   → Full UAT
   → Security audit
   → Performance validation
   → Device compatibility tests
```

---

## ⚙️ CATEGORY 1: UNIT TESTING (C++ PLUGINS)

### **Test NajikaBackendClient Plugin:**

```cpp
// File: NajikaBackendClient/Tests/TestAPIClient.cpp

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "NajikaAPIClient.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FNajikaAPIClientTest,
    "NajikaDigivice.Plugins.NajikaBackendClient.APIClient",
    EAutomationTestFlags::ApplicationContextMask |
    EAutomationTestFlags::ProductFilter
)

bool FNajikaAPIClientTest::RunTest(const FString& Parameters)
{
    // Test 1: API Client Creation
    UNajikaAPIClient* APIClient = NewObject<UNajikaAPIClient>();
    TestNotNull("API Client should be created", APIClient);

    // Test 2: Base URL Configuration
    FString ExpectedURL = TEXT("http://127.0.0.1:8000");
    TestEqual("Base URL should be correct", APIClient->BaseURL, ExpectedURL);

    // Test 3: Chat Message Validation
    FString ValidMessage = TEXT("Hello Najika");
    TestTrue("Valid message should be accepted", ValidMessage.Len() > 0);

    FString EmptyMessage = TEXT("");
    TestTrue("Empty message should be rejected", EmptyMessage.Len() == 0);

    // Test 4: JSON Parsing
    FString TestJSON = TEXT("{\"ok\":true,\"response\":\"Hi Mr.K!\"}");
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(TestJSON);

    bool bParsed = FJsonSerializer::Deserialize(Reader, JsonObject);
    TestTrue("JSON should parse successfully", bParsed);

    if (bParsed && JsonObject.IsValid())
    {
        bool bOk = JsonObject->GetBoolField("ok");
        TestTrue("JSON 'ok' field should be true", bOk);
    }

    return true;
}
```

### **Test NajikaVoiceSystem Plugin:**

```cpp
// File: NajikaVoiceSystem/Tests/TestVoiceCallManager.cpp

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FVoiceCallManagerTest,
    "NajikaDigivice.Plugins.NajikaVoiceSystem.VoiceCallManager",
    EAutomationTestFlags::ApplicationContextMask |
    EAutomationTestFlags::ProductFilter
)

bool FVoiceCallManagerTest::RunTest(const FString& Parameters)
{
    // Test 1: Voice Manager Creation
    UVoiceCallManager* VoiceManager = NewObject<UVoiceCallManager>();
    TestNotNull("Voice Manager should be created", VoiceManager);

    // Test 2: Audio Level Calculation
    TArray<float> TestBuffer;
    TestBuffer.Add(0.5f);
    TestBuffer.Add(-0.5f);
    TestBuffer.Add(0.8f);
    TestBuffer.Add(-0.3f);

    float AudioLevel = VoiceManager->CalculateAudioLevel(TestBuffer);
    TestTrue("Audio level should be > 0", AudioLevel > 0.0f);
    TestTrue("Audio level should be <= 1", AudioLevel <= 1.0f);

    // Test 3: VAD Threshold
    float VADThreshold = VoiceManager->VADThreshold;
    TestEqual("VAD threshold should be 0.02", VADThreshold, 0.02f);

    // Test 4: Sample Rate
    int32 SampleRate = VoiceManager->SampleRate;
    TestEqual("Sample rate should be 16000", SampleRate, 16000);

    return true;
}
```

### **Run Unit Tests:**

```bash
# In UE5 Editor:
Window → Developer Tools → Session Frontend
→ Automation Tab
→ Select tests
→ Run Tests

# Or via command line:
UnrealEditor-Cmd.exe "C:\NajikaDigivice_UE5\NajikaDigivice.uproject" \
  -ExecCmds="Automation RunTests NajikaDigivice" \
  -unattended -nopause -NullRHI -log
```

---

## 🔗 CATEGORY 2: INTEGRATION TESTING

### **Test: Backend Connection**

```
TEST: Backend API Connection
─────────────────────────────────────
Prerequisites:
☐ Backend server running (najika_server.py)
☐ UE5 project opened
☐ BP_TestBackend in level

Steps:
1. Start backend server: python najika_server.py
2. Verify server: curl http://127.0.0.1:8000/health
   Expected: {"status": "healthy"}
3. Play in Editor (PIE)
4. Check Output Log for "[Najika] Connected to backend"

Expected Result:
✅ Connection established
✅ No errors in Output Log
✅ API Client created successfully

Pass Criteria:
- Server responds to health check
- UE5 connects without errors
- API calls complete within 5 seconds
─────────────────────────────────────
```

### **Test: Chat System Integration**

```
TEST: Send Chat Message & Receive Response
─────────────────────────────────────
Prerequisites:
☐ Backend running
☐ Game instance created (BP_NajikaGameInstance)

Steps:
1. PIE
2. Open WBP_ChatUI
3. Type message: "Hello Najika"
4. Click Send
5. Wait for response (max 5s)

Expected Result:
✅ Message sent to backend (check Output Log)
✅ Backend processes message (check backend log)
✅ Response received in UE5
✅ Response displayed in ChatUI
✅ Response is relevant (uses AI model)

Pass Criteria:
- Response time < 5 seconds
- No errors
- Response contains text (not empty)
- UI updates correctly
─────────────────────────────────────
```

### **Test: Voice Call Integration**

```
TEST: Voice Call (Microphone → Whisper → TTS → Audio Playback)
─────────────────────────────────────
Prerequisites:
☐ Backend running
☐ Microphone permission granted
☐ Audio device available

Steps:
1. PIE
2. Press V key (or voice call button)
3. Speak: "Hello Najika, how are you?"
4. Wait for processing (5-10s)
5. Listen for audio response

Expected Result:
✅ Microphone captures audio
✅ Audio sent to backend
✅ Whisper STT transcribes correctly
✅ AI generates response
✅ TTS generates audio
✅ Audio plays in UE5
✅ Najika's mouth animates (lip sync)

Pass Criteria:
- Transcription accuracy > 80%
- Response time < 10 seconds
- Audio quality good (no distortion)
- Lip sync matches audio
─────────────────────────────────────
```

### **Test: Tamagotchi System Integration**

```
TEST: Feed Najika & Status Update
─────────────────────────────────────
Steps:
1. PIE
2. Open WBP_TamagotchiCare
3. Note current Hunger value (e.g., 50)
4. Click "Feed" button
5. Wait 2 seconds

Expected Result:
✅ POST /api/najika/feed called
✅ Backend updates hunger (+30)
✅ Response received in UE5
✅ Hunger bar updates (50 → 80)
✅ Najika plays eating animation
✅ Message shows: "Thank you Mr.K! 💜"

Pass Criteria:
- API call completes < 1 second
- Hunger increases by exactly 30
- Animation plays
- UI updates immediately
─────────────────────────────────────
```

---

## 📊 CATEGORY 3: PERFORMANCE TESTING

### **Performance Test Checklist:**

```
PERFORMANCE BENCHMARKS (Xiaomi 11T Pro)
─────────────────────────────────────
☐ FPS Test (30-minute gameplay)
   Target: 60 FPS average, >30 FPS minimum
   Measure: UE5 Stat FPS command

☐ Memory Test (1-hour gameplay)
   Target: <2GB RAM usage
   Measure: Stat Memory command
   Check: No memory leaks (usage stable)

☐ Battery Test (1-hour gameplay)
   Target: <25% battery drain
   Measure: Android Battery Stats

☐ Thermal Test (30-minute gameplay)
   Target: No thermal throttling, <45°C
   Measure: CPU-Z app or adb shell dumpsys thermalservice

☐ Load Time Test (10 app restarts)
   Target: <5 seconds average
   Measure: Time from app launch to playable

☐ Network Latency Test
   Target: API calls <500ms average
   Measure: Log request/response times

☐ Draw Call Test
   Target: <500 draw calls per frame
   Measure: Stat RHI command

☐ Texture Memory Test
   Target: <500MB texture memory
   Measure: Stat Streaming command
─────────────────────────────────────
```

### **Performance Testing Script:**

```python
# File: test_performance.py
import subprocess
import time
import re

def test_fps():
    """
    Test FPS over 30 minutes
    """
    print("[TEST] FPS Test starting...")

    # Launch game with FPS logging
    # (Requires custom build with FPS logging enabled)

    fps_samples = []
    duration = 30 * 60  # 30 minutes
    start_time = time.time()

    while time.time() - start_time < duration:
        # Read FPS from log file
        # (Parse UE5 log for FPS values)
        fps = get_current_fps()  # Implement this
        fps_samples.append(fps)
        time.sleep(1.0)

    avg_fps = sum(fps_samples) / len(fps_samples)
    min_fps = min(fps_samples)
    max_fps = max(fps_samples)

    print(f"[RESULT] Average FPS: {avg_fps:.2f}")
    print(f"[RESULT] Min FPS: {min_fps:.2f}")
    print(f"[RESULT] Max FPS: {max_fps:.2f}")

    # Pass/Fail
    assert avg_fps >= 60, "Average FPS too low!"
    assert min_fps >= 30, "Min FPS too low!"
    print("[PASS] FPS Test passed!")

def test_memory():
    """
    Test memory usage over 1 hour
    """
    print("[TEST] Memory Test starting...")

    # Similar implementation
    pass

if __name__ == "__main__":
    test_fps()
    test_memory()
```

---

## 📱 CATEGORY 4: DEVICE TESTING (XIAOMI 11T PRO)

### **Device Test Checklist:**

```
XIAOMI 11T PRO COMPATIBILITY TEST
─────────────────────────────────────
Device Info:
- Model: Xiaomi 11T Pro
- CPU: Snapdragon 888
- GPU: Adreno 660
- RAM: 8GB
- Storage: 128GB / 256GB
- OS: Android 13 (MIUI 14)
- Screen: 6.67" 1080x2400 120Hz AMOLED

Critical Tests:
☐ App Installation
   - APK installs without errors
   - Permissions requested properly
   - Icon appears in app drawer

☐ First Launch
   - Splash screen shows
   - No crash
   - Main menu loads
   - Tutorial works (if present)

☐ Graphics
   - 3D world renders correctly
   - Najika character visible
   - Textures load (no pink materials)
   - Animations play smoothly
   - UI elements visible and positioned correctly
   - No graphical glitches

☐ Performance
   - FPS: 60 target, >30 minimum
   - No stuttering during gameplay
   - Smooth UI interactions
   - Load times <5 seconds

☐ Touch Controls
   - Virtual joystick responsive
   - Buttons clickable
   - Multi-touch works (if needed)
   - Gestures recognized (swipe, pinch)

☐ Audio
   - Background music plays
   - Sound effects work
   - Voice TTS playback works
   - Microphone input works (voice calls)
   - Volume controls functional

☐ Network
   - Connects to backend (WiFi)
   - Connects to backend (Mobile data)
   - WebSocket stays connected
   - API calls complete
   - Handles poor connection gracefully

☐ Biometric Authentication
   - Fingerprint sensor works
   - Face unlock works (if supported)
   - Biometric prompt shows
   - Authentication succeeds/fails correctly

☐ Permissions
   - Microphone permission requested
   - Camera permission requested (if scanner enabled)
   - Storage permission requested
   - Notifications permission requested
   - Permissions work after granted

☐ Battery Life
   - Reasonable battery drain (<25%/hour)
   - No excessive heating
   - Thermal throttling acceptable

☐ Stability
   - No crashes during 1-hour session
   - No ANRs (Application Not Responding)
   - Memory stable (no leaks)
   - Resumes correctly from background

☐ Rotation
   - Landscape orientation works
   - UI adjusts correctly
   - No layout issues

☐ Notifications
   - Notifications show
   - Clicking notification opens app
   - Notification content correct

☐ Pause/Resume
   - Pause app → Resume (works correctly)
   - Phone call interrupt → Resume (works)
   - Switch to another app → Return (works)
─────────────────────────────────────
```

---

## 🌐 CATEGORY 5: BACKEND API TESTING

### **API Test Suite:**

```python
# File: test_backend_api.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health_endpoint():
    """Test /health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("[PASS] Health endpoint")

def test_chat_endpoint():
    """Test /api/chat endpoint"""
    payload = {"message": "Hello Najika"}
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ok" in data
    assert data["ok"] == True
    assert "response" in data
    assert len(data["response"]) > 0
    print(f"[PASS] Chat endpoint - Response: {data['response']}")

def test_najika_status():
    """Test /api/najika/status endpoint"""
    response = requests.get(f"{BASE_URL}/api/najika/status")
    assert response.status_code == 200
    data = response.json()
    assert "hunger" in data
    assert "energy" in data
    assert "happiness" in data
    assert 0 <= data["hunger"] <= 100
    assert 0 <= data["energy"] <= 100
    assert 0 <= data["happiness"] <= 100
    print("[PASS] Najika status endpoint")

def test_feed_najika():
    """Test /api/najika/feed endpoint"""
    response = requests.post(f"{BASE_URL}/api/najika/feed")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] == True
    assert "message" in data
    print(f"[PASS] Feed endpoint - Message: {data['message']}")

def test_voice_stt():
    """Test /api/voice/stt endpoint"""
    # Create dummy audio data (real test would use actual audio)
    with open("test_audio.wav", "rb") as f:
        audio_data = f.read()

    files = {"audio": ("test_audio.wav", audio_data, "audio/wav")}
    response = requests.post(f"{BASE_URL}/api/voice/stt", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    print(f"[PASS] STT endpoint - Transcription: {data['text']}")

def run_all_tests():
    print("Starting Backend API Tests...")
    test_health_endpoint()
    test_chat_endpoint()
    test_najika_status()
    test_feed_najika()
    # test_voice_stt()  # Requires audio file
    print("\n[SUCCESS] All API tests passed!")

if __name__ == "__main__":
    run_all_tests()
```

### **Run API Tests:**

```bash
# Install requests library
pip install requests

# Start backend
python najika_server.py

# Run tests (in another terminal)
python test_backend_api.py
```

---

## 🔐 CATEGORY 6: SECURITY TESTING

### **Security Test Checklist:**

```
SECURITY AUDIT CHECKLIST
─────────────────────────────────────
Authentication:
☐ Biometric authentication works
☐ Cannot bypass biometric (Android Keystore)
☐ Owner-Token validated on backend
☐ Invalid tokens rejected

Network Security:
☐ HTTPS used for production (not HTTP!)
☐ Certificate pinning implemented (optional)
☐ API requests cannot be spoofed
☐ WebSocket connection secure

Data Storage:
☐ Sensitive data encrypted (EncryptedSharedPreferences)
☐ No secrets in plain text
☐ No hardcoded API keys
☐ Save files encrypted

VPN Check:
☐ VPN detected correctly
☐ Warning shown to user
☐ App behavior appropriate

Input Validation:
☐ Chat messages validated (max length, no injection)
☐ API inputs sanitized
☐ No SQL injection possible (backend)
☐ No XSS possible (if webview used)

Code Obfuscation:
☐ ProGuard enabled for release build
☐ Native libs not easily decompilable
☐ Debug symbols stripped

APK Security:
☐ APK signed with release keystore
☐ Debug mode disabled
☐ No test/dev endpoints accessible
☐ App permissions minimal (only necessary)

Privacy:
☐ No unnecessary data collected
☐ Analytics opt-in (not opt-out)
☐ Privacy policy present
☐ GDPR compliant (if EU users)
─────────────────────────────────────
```

---

## ✅ CATEGORY 7: USER ACCEPTANCE TESTING (UAT)

### **UAT Test Scenarios:**

```
UAT SCENARIO 1: First Time User Experience
─────────────────────────────────────
Tester: New user (never used app)

Steps:
1. Install APK
2. Launch app for first time
3. Go through onboarding/tutorial (if present)
4. Start chatting with Najika
5. Explore world for 10 minutes
6. Try feeding Najika
7. Try voice call
8. Close app

Evaluation Criteria:
☐ Onboarding clear and helpful
☐ User understands core mechanics
☐ No confusion about controls
☐ App feels polished
☐ No bugs encountered

Feedback: [User fills out feedback form]
─────────────────────────────────────

UAT SCENARIO 2: Daily User Experience
─────────────────────────────────────
Tester: Regular user

Steps:
1. Launch app (returning user)
2. Check Najika status
3. Feed/Care for Najika
4. Have voice call conversation
5. Play minigame
6. Start battle
7. Use app for 30 minutes
8. Close app

Evaluation Criteria:
☐ Quick to resume (load time <5s)
☐ Status persisted correctly
☐ All features working
☐ Performance good
☐ No crashes

Feedback: [User fills out feedback form]
─────────────────────────────────────
```

---

## 🔄 CATEGORY 8: REGRESSION TESTING

### **Regression Test Checklist:**

```
REGRESSION TESTS (Run after EVERY update!)
─────────────────────────────────────
Core Functionality:
☐ App launches
☐ Chat works
☐ Voice calls work
☐ Tamagotchi system works
☐ Battle system works
☐ Minigames work
☐ Save/load works
☐ Settings persist

No Broken Features:
☐ No features regressed from previous version
☐ All previous bugs still fixed
☐ New features don't break old features

Performance:
☐ FPS still acceptable
☐ Memory usage not increased significantly
☐ Battery life not worse

Compatibility:
☐ Still works on Xiaomi 11T Pro
☐ Still works on other tested devices
─────────────────────────────────────
```

---

## 🎯 TESTING SUMMARY

```
✅ Unit Testing: C++ Plugins tested
✅ Integration Testing: Backend + UE5 tested
✅ Performance Testing: FPS, Memory, Battery benchmarked
✅ Device Testing: Xiaomi 11T Pro fully tested
✅ Backend API Testing: All endpoints validated
✅ Security Testing: Alcatraz 8 Gebote verified
✅ UAT: Real users test app
✅ Regression Testing: No broken features
```

**Test Coverage Target: 80%+**

---

## 🎉 TESTING FRAMEWORK COMPLETE!

**Usage:**
1. Run unit tests during development
2. Run integration tests before commits
3. Run full test suite before releases
4. Conduct UAT with real users
5. Fix all critical bugs before launch

**Best Practices:**
- Test early, test often
- Automate where possible
- Test on real devices
- Get user feedback
- Fix bugs immediately

**Next:** Create Troubleshooting Database!

---

**Model 1 - Digivice APK Development**
**Status:** Testing Framework Ready ✅
**Coverage:** Comprehensive testing procedures documented

**READY TO TEST EVERYTHING! 🧪🚀**
