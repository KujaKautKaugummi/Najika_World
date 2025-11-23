# Testing & Validation Checklist - Najika UE5 Project

**Version:** 1.0
**Last Updated:** 2025-01-13
**Project:** Najika Digivice (UE5 Mobile Game)
**Test Target:** Xiaomi 11T Pro (Android 11+)

---

## Table of Contents

1. [Overview](#overview)
2. [Pre-Testing Setup](#pre-testing-setup)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [Functional Testing](#functional-testing)
6. [Performance Testing](#performance-testing)
7. [Platform-Specific Testing](#platform-specific-testing)
8. [User Acceptance Testing](#user-acceptance-testing)
9. [Security Testing](#security-testing)
10. [Regression Testing](#regression-testing)
11. [Sign-Off Checklist](#sign-off-checklist)

---

## Overview

### Testing Philosophy

**Najika Testing Pyramid:**

```
              / \
             /UAT \          User Acceptance (5%)
            /-------\
           /Security \       Security & Compliance (10%)
          /-----------\
         / Platform   \     Platform-Specific (15%)
        /  Performance \   Performance & Stress (20%)
       /-----------------\
      /   Functional      \   Functional Tests (30%)
     /  Integration Tests  \  Integration Tests (20%)
    /-----------------------\
```

### Test Environments

| Environment | Purpose | Backend | Device | Configuration |
|-------------|---------|---------|--------|---------------|
| **Local Development** | Daily testing | localhost:8000 | PC (PIE) | DebugGame Editor |
| **Device Testing** | Mobile validation | localhost:8000 (forwarded) | Xiaomi 11T Pro | Development |
| **Staging** | Pre-release | Staging server | Xiaomi 11T Pro | Shipping |
| **Production** | Final validation | Production server | Multiple devices | Shipping |

### Test Coverage Goals

- **Code Coverage:** 70%+ (C++ plugins)
- **Blueprint Coverage:** 90%+ (game logic)
- **Critical Path Coverage:** 100% (login, gameplay, voice chat)
- **Platform Coverage:** 100% (Android ARM64)

---

## Pre-Testing Setup

### 1. Environment Preparation

#### ✅ Development PC Setup

- [ ] Visual Studio 2022 installed and configured
- [ ] UE5.3+ installed with Android support
- [ ] All plugins compiled successfully
- [ ] No compilation errors or warnings
- [ ] Git repository is clean (no uncommitted changes)

#### ✅ Android Device Setup (Xiaomi 11T Pro)

- [ ] Developer options enabled
- [ ] USB debugging enabled
- [ ] Device connected via ADB (`adb devices` shows device)
- [ ] Latest APK installed (`Development` configuration)
- [ ] Port forwarding configured (`adb reverse tcp:8000 tcp:8000`)
- [ ] All permissions granted (Internet, Microphone, etc.)

#### ✅ Backend Setup

- [ ] Backend server running on `localhost:8000`
- [ ] Database initialized with test data
- [ ] Health check endpoint responding: `curl http://localhost:8000/api/health`
- [ ] Test accounts created:
  - Username: `test_user_1`, Password: `test123`
  - Username: `test_user_2`, Password: `test123`
  - Username: `admin_test`, Password: `admin123`

### 2. Test Data Preparation

#### Create Test Accounts (Backend)

Run backend script to create test users:

```bash
# Example
python manage.py create_test_users
```

**Required test accounts:**
- 10 regular users (`test_user_1` through `test_user_10`)
- 2 admin users (`admin_test_1`, `admin_test_2`)
- 5 users with pre-existing inventory/progress

#### Prepare Test Assets

- [ ] Test images for avatar uploads (1 MB, 5 MB, 10 MB files)
- [ ] Test audio files for voice chat (WAV, 16kHz, mono)
- [ ] Corrupted files for negative testing (invalid JSON, malformed images)

### 3. Logging Configuration

#### Enable Verbose Logging in UE5

In **Project Settings > Engine > Logging**:

Set log verbosity for:
- `LogNajikaBackend`: `Verbose`
- `LogNajikaVoice`: `Verbose`
- `LogTemp`: `Verbose`

#### Enable ADB Logging

Terminal 1 (Backend logs):
```bash
# Backend server logs
tail -f backend/logs/server.log
```

Terminal 2 (Android logcat):
```bash
adb logcat | findstr "Najika"
```

Terminal 3 (Test execution):
```bash
# Your test commands
```

---

## Unit Testing

### C++ Unit Tests

#### NajikaBackendClient Plugin Tests

**Test File:** `Plugins/NajikaBackendClient/Source/Tests/NajikaBackendClientTests.cpp`

##### Test 1: HTTP Client Construction

```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaHttpClientConstruction,
    "Najika.Backend.HttpClient.Construction",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaHttpClientConstruction::RunTest(const FString& Parameters)
{
    UNajikaHttpClient* Client = NewObject<UNajikaHttpClient>();

    TestNotNull(TEXT("HttpClient should be created"), Client);
    TestEqual(TEXT("BaseURL should default to localhost"),
        Client->GetBaseURL(),
        TEXT("http://localhost:8000"));

    return true;
}
```

**Run in UE5:**
1. **Window > Test Automation**
2. Filter: `Najika.Backend`
3. Select all tests
4. Click **Start Tests**

**Expected Result:** ✅ All tests pass

---

##### Test 2: JSON Serialization

```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaJsonSerialization,
    "Najika.Backend.HttpClient.JsonSerialization",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaJsonSerialization::RunTest(const FString& Parameters)
{
    FNajikaLoginRequest Request;
    Request.Username = TEXT("test_user");
    Request.Password = TEXT("test_pass");

    FString JsonString = Request.ToJsonString();

    TestTrue(TEXT("JSON should contain username"),
        JsonString.Contains(TEXT("\"username\":\"test_user\"")));
    TestTrue(TEXT("JSON should contain password"),
        JsonString.Contains(TEXT("\"password\":\"test_pass\"")));

    return true;
}
```

**Expected Result:** ✅ Pass

---

#### NajikaVoiceSystem Plugin Tests

##### Test 3: Voice Capture Initialization

```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceCaptureInit,
    "Najika.Voice.Capture.Initialization",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceCaptureInit::RunTest(const FString& Parameters)
{
    UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

    FNajikaVoiceCaptureConfig Config;
    Config.SampleRate = 48000;
    Config.bEnableVAD = true;

    bool bSuccess = Capture->Initialize(Config);

    TestTrue(TEXT("Capture should initialize successfully"), bSuccess);
    TestEqual(TEXT("Sample rate should be set"),
        Capture->GetSampleRate(), 48000);

    return true;
}
```

**Expected Result:** ✅ Pass

---

##### Test 4: VAD (Voice Activity Detection)

```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVAD,
    "Najika.Voice.VAD.Detection",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVAD::RunTest(const FString& Parameters)
{
    UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

    // Test with silence (low energy)
    TArray<float> SilenceBuffer;
    SilenceBuffer.Init(0.001f, 1024);  // Very quiet
    bool bVoiceInSilence = Capture->DetectVoiceActivity(SilenceBuffer.GetData(), 1024);
    TestFalse(TEXT("VAD should not detect voice in silence"), bVoiceInSilence);

    // Test with loud audio (high energy)
    TArray<float> LoudBuffer;
    LoudBuffer.Init(0.8f, 1024);  // Loud
    bool bVoiceInLoud = Capture->DetectVoiceActivity(LoudBuffer.GetData(), 1024);
    TestTrue(TEXT("VAD should detect voice in loud audio"), bVoiceInLoud);

    return true;
}
```

**Expected Result:** ✅ Pass

---

### Unit Test Checklist

Run all unit tests and verify:

- [ ] ✅ `Najika.Backend.HttpClient.Construction` - PASS
- [ ] ✅ `Najika.Backend.HttpClient.JsonSerialization` - PASS
- [ ] ✅ `Najika.Backend.WebSocket.Connection` - PASS
- [ ] ✅ `Najika.Voice.Capture.Initialization` - PASS
- [ ] ✅ `Najika.Voice.VAD.Detection` - PASS
- [ ] ✅ `Najika.Voice.Encoding.OpusEncoding` - PASS
- [ ] ✅ `Najika.Voice.Playback.AudioPlayback` - PASS

**Total Unit Tests:** 15+
**Required Pass Rate:** 100%

---

## Integration Testing

### Backend Integration Tests

#### Test 5: Login Flow (HTTP)

**Objective:** Verify login request → backend → response → token storage

**Test Steps:**

1. **Setup:**
   - Backend running on `localhost:8000`
   - Test account exists: `test_user_1` / `test123`

2. **Execution (Blueprint or C++):**
   ```cpp
   // In test Blueprint or C++ test
   UNajikaHttpClient* Client = GetGameInstance()->GetSubsystem<UNajikaBackendSubsystem>()->GetHttpClient();

   Client->SendLoginRequest(TEXT("test_user_1"), TEXT("test123"));

   // Wait for response (use latent action in tests)
   ```

3. **Verification:**
   - [ ] HTTP request sent to `/api/auth/login`
   - [ ] Backend responds with `200 OK`
   - [ ] Response contains `access_token`
   - [ ] Response contains `user_id`
   - [ ] Token stored in `UNajikaGameInstance`
   - [ ] `OnLoginSuccess` delegate broadcasts
   - [ ] No errors in logcat

**Expected Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "12345",
  "username": "test_user_1",
  "display_name": "Test User One"
}
```

**Pass Criteria:** ✅ All verifications pass

---

#### Test 6: Login Failure (Invalid Credentials)

**Objective:** Verify error handling for invalid login

**Test Steps:**

1. **Execution:**
   ```cpp
   Client->SendLoginRequest(TEXT("test_user_1"), TEXT("WRONG_PASSWORD"));
   ```

2. **Verification:**
   - [ ] Backend responds with `401 Unauthorized`
   - [ ] `OnLoginFailure` delegate broadcasts with error message
   - [ ] Error message displayed to user: "Invalid username or password"
   - [ ] No token stored

**Pass Criteria:** ✅ Error handled gracefully

---

#### Test 7: Inventory Retrieval

**Objective:** Verify inventory fetch after login

**Test Steps:**

1. **Setup:**
   - Login successful (from Test 5)
   - Test account has 5 items in inventory

2. **Execution:**
   ```cpp
   Client->SendGetInventoryRequest();
   ```

3. **Verification:**
   - [ ] Request includes `Authorization: Bearer <token>` header
   - [ ] Backend responds with `200 OK`
   - [ ] Response contains array of inventory items
   - [ ] Item count matches backend data (5 items)
   - [ ] Each item has: `item_id`, `name`, `quantity`, `icon_url`

**Expected Response:**
```json
{
  "items": [
    {"item_id": "sword_001", "name": "Iron Sword", "quantity": 1, "icon_url": "/icons/sword.png"},
    {"item_id": "potion_hp", "name": "HP Potion", "quantity": 10, "icon_url": "/icons/potion_hp.png"},
    ...
  ]
}
```

**Pass Criteria:** ✅ Inventory data correctly parsed and stored

---

### Voice System Integration Tests

#### Test 8: Voice Call Establishment (WebSocket)

**Objective:** Verify WebSocket connection for voice chat

**Test Steps:**

1. **Setup:**
   - Two clients logged in: `test_user_1` and `test_user_2`
   - Both in same "room" or "party"

2. **Execution (Client 1):**
   ```cpp
   UNajikaVoiceComponent* VoiceComp = GetCharacter()->FindComponentByClass<UNajikaVoiceComponent>();
   VoiceComp->StartVoiceCall();
   ```

3. **Verification (Client 1):**
   - [ ] WebSocket connects to `ws://localhost:8000/ws/voice`
   - [ ] Connection established (`OnConnectionEstablished` callback)
   - [ ] Microphone capture starts
   - [ ] Voice call state = `Connected`

4. **Verification (Client 2):**
   - [ ] Receives notification of Client 1 joining voice call
   - [ ] Audio playback component ready

**Pass Criteria:** ✅ WebSocket connection established, both clients aware

---

#### Test 9: Voice Transmission (Audio Packets)

**Objective:** Verify audio data flows from Client 1 → Backend → Client 2

**Test Steps:**

1. **Setup:**
   - Voice call established (from Test 8)

2. **Execution (Client 1):**
   - Speak into microphone for 5 seconds
   - Or play test audio file

3. **Verification (Client 1):**
   - [ ] VAD detects voice activity
   - [ ] Audio captured and encoded (Opus or PCM16)
   - [ ] Packets sent via WebSocket
   - [ ] `OnAudioPacketSent` delegate broadcasts

4. **Verification (Client 2):**
   - [ ] Receives audio packets via WebSocket
   - [ ] Packets decoded
   - [ ] Audio played back through speakers/headphones
   - [ ] Playback is clear (no excessive distortion/lag)

5. **Verification (Backend Logs):**
   - [ ] Backend logs show audio packets received from Client 1
   - [ ] Backend logs show audio packets forwarded to Client 2

**Pass Criteria:** ✅ Audio transmitted and played back successfully

---

#### Test 10: Whisper AI Transcription

**Objective:** Verify speech-to-text integration

**Test Steps:**

1. **Setup:**
   - Voice component initialized
   - Auto-transcribe enabled

2. **Execution:**
   ```cpp
   VoiceComp->SetAutoTranscribeEnabled(true);
   ```
   - Speak clearly: "Hello, this is a test message"

3. **Verification:**
   - [ ] Audio captured
   - [ ] Sent to backend `/api/voice/transcribe`
   - [ ] Backend processes with Whisper AI
   - [ ] Transcription result received
   - [ ] Text approximately matches spoken words: "Hello, this is a test message"
   - [ ] `OnWhisperTranscriptionComplete` delegate broadcasts
   - [ ] Transcribed text displayed in chat UI

**Expected Result:**
```json
{
  "text": "Hello, this is a test message.",
  "confidence": 0.95,
  "language_code": "en"
}
```

**Pass Criteria:** ✅ Transcription accuracy ≥ 80%

---

### Integration Test Checklist

- [ ] ✅ Test 5: Login Flow (HTTP) - PASS
- [ ] ✅ Test 6: Login Failure (Invalid Credentials) - PASS
- [ ] ✅ Test 7: Inventory Retrieval - PASS
- [ ] ✅ Test 8: Voice Call Establishment (WebSocket) - PASS
- [ ] ✅ Test 9: Voice Transmission (Audio Packets) - PASS
- [ ] ✅ Test 10: Whisper AI Transcription - PASS
- [ ] ✅ Test 11: Session Management - PASS
- [ ] ✅ Test 12: Token Refresh - PASS

**Total Integration Tests:** 10+
**Required Pass Rate:** 100%

---

## Functional Testing

### Gameplay Feature Tests

#### Test 13: Character Movement

**Objective:** Verify player can move in all directions

**Test Steps (On Device):**

1. Launch game on Xiaomi 11T Pro
2. Login with test account
3. Enter main gameplay level

**Test Cases:**

| Input | Expected Result | Status |
|-------|-----------------|--------|
| Touch joystick left | Character moves left | [ ] PASS |
| Touch joystick right | Character moves right | [ ] PASS |
| Touch joystick up | Character moves forward | [ ] PASS |
| Touch joystick down | Character moves backward | [ ] PASS |
| Diagonal input | Character moves diagonally | [ ] PASS |
| Release joystick | Character stops moving | [ ] PASS |
| Swipe screen | Camera rotates | [ ] PASS |
| Double tap | Character jumps | [ ] PASS |

**Pass Criteria:** ✅ All movement inputs respond correctly, no lag

---

#### Test 14: Inventory Management

**Objective:** Verify inventory UI and item interactions

**Test Steps:**

1. Open inventory (tap inventory button)
2. Verify items display correctly

**Test Cases:**

| Action | Expected Result | Status |
|--------|-----------------|--------|
| Open inventory | UI appears with all items | [ ] PASS |
| Tap item | Item details shown (name, description, stats) | [ ] PASS |
| Use consumable | Item count decreases, effect applied | [ ] PASS |
| Equip weapon | Character's weapon changes visually | [ ] PASS |
| Unequip weapon | Weapon removed from character | [ ] PASS |
| Drop item | Confirmation prompt appears | [ ] PASS |
| Confirm drop | Item removed from inventory | [ ] PASS |
| Close inventory | UI closes, returns to gameplay | [ ] PASS |

**Pass Criteria:** ✅ All inventory actions work, UI responsive

---

#### Test 15: Combat System

**Objective:** Verify attack mechanics

**Test Steps:**

1. Encounter enemy NPC
2. Engage in combat

**Test Cases:**

| Action | Expected Result | Status |
|--------|-----------------|--------|
| Tap attack button | Character performs attack animation | [ ] PASS |
| Hit enemy | Enemy takes damage, health bar decreases | [ ] PASS |
| Enemy counterattacks | Player takes damage, health bar decreases | [ ] PASS |
| Use skill | Skill animation plays, MP consumed | [ ] PASS |
| Dodge button | Character dodges, i-frames active | [ ] PASS |
| Block button | Damage reduced | [ ] PASS |
| Defeat enemy | Enemy dies, loot drops, XP gained | [ ] PASS |
| Player dies | Death screen shown, respawn option | [ ] PASS |

**Pass Criteria:** ✅ All combat mechanics functional

---

#### Test 16: Quest System

**Objective:** Verify quest acceptance and completion

**Test Steps:**

1. Talk to NPC quest giver
2. Accept quest

**Test Cases:**

| Action | Expected Result | Status |
|--------|-----------------|--------|
| Talk to NPC | Quest dialogue appears | [ ] PASS |
| Accept quest | Quest added to journal | [ ] PASS |
| Open quest journal | Quest details shown (objectives, rewards) | [ ] PASS |
| Complete objective | Quest tracker updates (1/3 → 2/3) | [ ] PASS |
| All objectives done | Quest marked as "Turn In" | [ ] PASS |
| Return to NPC | Turn-in option available | [ ] PASS |
| Turn in quest | Rewards received (XP, gold, items) | [ ] PASS |

**Pass Criteria:** ✅ Quest flow works end-to-end

---

### UI/UX Tests

#### Test 17: Main Menu Navigation

**Test Cases:**

| Action | Expected Result | Status |
|--------|-----------------|--------|
| Launch app | Splash screen → Main menu | [ ] PASS |
| Tap "Play" | Login screen appears | [ ] PASS |
| Tap "Settings" | Settings UI opens | [ ] PASS |
| Tap "Credits" | Credits screen shown | [ ] PASS |
| Tap "Exit" | App closes or confirmation prompt | [ ] PASS |
| Back button (Android) | Navigate back or exit | [ ] PASS |

---

#### Test 18: HUD Display

**Test Cases:**

| Element | Expected Result | Status |
|---------|-----------------|--------|
| Health bar | Displays current/max HP, updates in real-time | [ ] PASS |
| MP/Stamina bar | Displays current/max, updates in real-time | [ ] PASS |
| XP bar | Displays progress to next level | [ ] PASS |
| Minimap | Shows player position and nearby entities | [ ] PASS |
| Quest tracker | Shows active quest objectives | [ ] PASS |
| Gold/Currency | Displays current gold amount | [ ] PASS |
| Notification icons | Shows buff/debuff icons | [ ] PASS |

**Pass Criteria:** ✅ All HUD elements visible, no overlap

---

### Functional Test Checklist

- [ ] ✅ Test 13: Character Movement - PASS
- [ ] ✅ Test 14: Inventory Management - PASS
- [ ] ✅ Test 15: Combat System - PASS
- [ ] ✅ Test 16: Quest System - PASS
- [ ] ✅ Test 17: Main Menu Navigation - PASS
- [ ] ✅ Test 18: HUD Display - PASS
- [ ] ✅ Test 19: Social Features (Friends, Chat) - PASS
- [ ] ✅ Test 20: In-App Purchases (if applicable) - PASS

**Total Functional Tests:** 12+
**Required Pass Rate:** 95%+

---

## Performance Testing

### Frame Rate Tests

#### Test 21: Target Frame Rate (120 FPS)

**Objective:** Verify game runs at 60+ FPS (ideally 120 FPS on Xiaomi 11T Pro)

**Test Steps:**

1. Launch game on device
2. Enable FPS counter:
   - Open console (3-finger tap)
   - Type: `stat fps`

3. **Test Scenarios:**

| Scenario | Target FPS | Measured FPS | Status |
|----------|-----------|--------------|--------|
| Main menu (idle) | 120 | _______ | [ ] PASS |
| Character idle in empty scene | 120 | _______ | [ ] PASS |
| Character walking (no enemies) | 100+ | _______ | [ ] PASS |
| Combat with 3 enemies | 80+ | _______ | [ ] PASS |
| Combat with 5 enemies | 60+ | _______ | [ ] PASS |
| Dense forest area (many trees) | 60+ | _______ | [ ] PASS |
| Particle effects (spells, explosions) | 60+ | _______ | [ ] PASS |

**Pass Criteria:** ✅ Minimum 60 FPS in all scenarios, 80+ FPS in normal gameplay

**If Failed:**
- Check `stat unit` to identify bottleneck (Game/Draw/GPU)
- Reduce graphics quality or optimize assets
- Profile with Unreal Insights

---

### Memory Usage Tests

#### Test 22: Memory Consumption

**Objective:** Verify app stays within device RAM limits

**Test Steps:**

1. Enable memory stats:
   ```
   stat memory
   ```

2. **Test Scenarios:**

| Scenario | Expected Memory | Measured Memory | Status |
|----------|-----------------|-----------------|--------|
| Main menu | < 500 MB | _______ MB | [ ] PASS |
| Gameplay (small level) | < 1.5 GB | _______ MB | [ ] PASS |
| Gameplay (large level) | < 2.5 GB | _______ MB | [ ] PASS |
| After 30 minutes | < 3 GB | _______ MB | [ ] PASS |
| After 1 hour | < 3.5 GB | _______ MB | [ ] PASS |

**Pass Criteria:** ✅ Memory stays below 3.5 GB (Xiaomi 11T Pro has 8-12 GB total)

**Memory Leak Detection:**
- [ ] Memory does not continuously increase over time
- [ ] After returning to main menu, memory returns to baseline

**If Failed:**
- Profile with Unreal Insights → Memory Insights
- Check for unreleased textures, audio, or objects

---

### Battery & Thermal Tests

#### Test 23: Battery Drain

**Objective:** Verify reasonable battery consumption

**Test Steps:**

1. Charge device to 100%
2. Disconnect charger
3. Play game continuously for 1 hour
4. Record battery percentage

**Expected Results:**

| Duration | Battery Drain | Status |
|----------|---------------|--------|
| 1 hour | ≤ 25% | [ ] PASS |
| 2 hours | ≤ 50% | [ ] PASS |

**Pass Criteria:** ✅ Battery lasts at least 3-4 hours of continuous gameplay

---

#### Test 24: Thermal Performance

**Objective:** Verify device doesn't overheat

**Test Steps:**

1. Play game continuously for 30 minutes
2. Monitor device temperature (use thermal measurement app or infrared thermometer)

**Expected Results:**

| Duration | Temperature | Throttling | Status |
|----------|-------------|------------|--------|
| 10 minutes | < 40°C | None | [ ] PASS |
| 20 minutes | < 45°C | None | [ ] PASS |
| 30 minutes | < 48°C | Minimal | [ ] PASS |

**Pass Criteria:** ✅ Device stays below 50°C, no severe throttling

---

### Network Performance Tests

#### Test 25: Backend Latency

**Objective:** Verify backend response times are acceptable

**Test Steps:**

1. Enable network profiling
2. Perform actions that trigger backend requests

**Expected Response Times:**

| Action | Endpoint | Target Latency | Measured Latency | Status |
|--------|----------|----------------|------------------|--------|
| Login | `/api/auth/login` | < 200ms | _______ ms | [ ] PASS |
| Get Inventory | `/api/inventory` | < 150ms | _______ ms | [ ] PASS |
| Update Profile | `/api/user/profile` | < 200ms | _______ ms | [ ] PASS |
| Send Chat Message | `/api/chat/send` | < 100ms | _______ ms | [ ] PASS |
| Voice Packet | WebSocket | < 50ms | _______ ms | [ ] PASS |

**Pass Criteria:** ✅ All requests within target latency

---

### Load Testing

#### Test 26: Concurrent Voice Calls

**Objective:** Verify system handles multiple voice participants

**Test Steps:**

1. Setup: 5 devices (or simulated clients) in same voice room
2. All speak simultaneously for 1 minute

**Expected Results:**

- [ ] No audio distortion
- [ ] No packet loss > 5%
- [ ] Latency < 100ms
- [ ] No crashes or disconnections

**Pass Criteria:** ✅ All clients maintain voice call without issues

---

### Performance Test Checklist

- [ ] ✅ Test 21: Target Frame Rate (120 FPS) - PASS
- [ ] ✅ Test 22: Memory Consumption - PASS
- [ ] ✅ Test 23: Battery Drain - PASS
- [ ] ✅ Test 24: Thermal Performance - PASS
- [ ] ✅ Test 25: Backend Latency - PASS
- [ ] ✅ Test 26: Concurrent Voice Calls - PASS

**Total Performance Tests:** 8+
**Required Pass Rate:** 100%

---

## Platform-Specific Testing

### Xiaomi 11T Pro Specific Tests

#### Test 27: Display Modes

**Objective:** Verify game works with different display settings

**Test Cases:**

| Setting | Expected Result | Status |
|---------|-----------------|--------|
| 60Hz refresh rate | Game runs at 60 FPS | [ ] PASS |
| 120Hz refresh rate | Game runs at 120 FPS | [ ] PASS |
| Dark mode (system) | UI uses dark theme | [ ] PASS |
| Light mode (system) | UI uses light theme | [ ] PASS |
| Auto-brightness | Game visible in all lighting conditions | [ ] PASS |
| Notch display | UI elements avoid notch area | [ ] PASS |

---

#### Test 28: MIUI Features

**Objective:** Verify compatibility with MIUI Android skin

**Test Cases:**

| Feature | Expected Result | Status |
|---------|-----------------|--------|
| Notification shade | Game pauses when notification shade opened | [ ] PASS |
| Recent apps | Game visible in recent apps, screenshot shown | [ ] PASS |
| Split screen | Game pauses or displays error (if not supported) | [ ] PASS |
| Floating windows | Game handles floating windows gracefully | [ ] PASS |
| Game Turbo mode | Game runs with enhanced performance | [ ] PASS |
| Battery saver | Game notifies user if performance affected | [ ] PASS |

---

### Android System Tests

#### Test 29: Permissions

**Objective:** Verify permission requests and handling

**Test Cases:**

| Permission | When Requested | Expected Result | Status |
|------------|----------------|-----------------|--------|
| Internet | App launch | Auto-granted (no prompt) | [ ] PASS |
| Microphone | First voice call | Permission prompt, explain usage | [ ] PASS |
| Microphone denied | First voice call | Error message, voice features disabled | [ ] PASS |
| Microphone granted later | Settings → Grant | Voice features enabled | [ ] PASS |
| Notification | App launch or settings | Permission prompt (Android 13+) | [ ] PASS |

---

#### Test 30: Lifecycle Events

**Objective:** Verify app handles Android lifecycle correctly

**Test Cases:**

| Event | Action | Expected Result | Status |
|-------|--------|-----------------|--------|
| Pause (Home button) | Press Home | Game pauses, music stops | [ ] PASS |
| Resume | Tap app icon | Game resumes, state preserved | [ ] PASS |
| Incoming call | Receive phone call | Game pauses, voice call muted | [ ] PASS |
| After call | End phone call | Game resumes | [ ] PASS |
| Low battery warning | System low battery prompt | Game shows warning, reduces performance | [ ] PASS |
| Orientation change | Rotate device | Game locks to landscape (or handles rotation) | [ ] PASS |
| Backgrounded for 10 minutes | Wait 10 min | Game state preserved on resume | [ ] PASS |

---

### Platform Test Checklist

- [ ] ✅ Test 27: Display Modes - PASS
- [ ] ✅ Test 28: MIUI Features - PASS
- [ ] ✅ Test 29: Permissions - PASS
- [ ] ✅ Test 30: Lifecycle Events - PASS
- [ ] ✅ Test 31: Hardware Buttons (Volume, Power) - PASS
- [ ] ✅ Test 32: External Audio Devices (Bluetooth headphones) - PASS

**Total Platform Tests:** 8+
**Required Pass Rate:** 100%

---

## User Acceptance Testing

### UAT Test Group

**Test Users:** 10-15 external testers (not part of development team)

**Test Period:** 1-2 weeks

**Test Environment:** Shipping build on real devices

### UAT Scenarios

#### Scenario 1: New Player Experience

**Objective:** Verify new players can understand and enjoy the game

**Test Steps:**

1. Install APK (first time)
2. Complete tutorial
3. Play for 30 minutes

**Feedback Questions:**

- [ ] Was the tutorial clear and helpful? (1-5 rating: ______)
- [ ] Were you able to navigate menus easily? (1-5 rating: ______)
- [ ] Did you understand the combat system? (1-5 rating: ______)
- [ ] Were there any confusing elements? (Free text: _____________)
- [ ] How likely are you to continue playing? (1-5 rating: ______)

**Pass Criteria:** ✅ Average rating ≥ 4.0

---

#### Scenario 2: Multiplayer Experience

**Objective:** Verify voice chat and multiplayer work intuitively

**Test Steps:**

1. Create party with another player
2. Use voice chat for 10 minutes
3. Complete a quest together

**Feedback Questions:**

- [ ] Was it easy to create/join a party? (1-5 rating: ______)
- [ ] Did voice chat work clearly? (1-5 rating: ______)
- [ ] Any lag or audio issues? (Yes/No: ______)
- [ ] Would you use voice chat regularly? (Yes/No: ______)

**Pass Criteria:** ✅ Average rating ≥ 4.0, < 20% report audio issues

---

### Bug Reporting

**UAT Testers should report:**

- Crashes (with steps to reproduce)
- UI/UX issues (screenshots)
- Performance problems (FPS drops, stuttering)
- Content errors (typos, missing textures)
- Gameplay balance issues

**Bug Tracking:** Use issue tracker (GitHub Issues, Jira, etc.)

### UAT Checklist

- [ ] ✅ 10+ testers recruited
- [ ] ✅ Test builds distributed
- [ ] ✅ Scenario 1 feedback collected (avg ≥ 4.0)
- [ ] ✅ Scenario 2 feedback collected (avg ≥ 4.0)
- [ ] ✅ Critical bugs fixed (P0, P1)
- [ ] ✅ 80%+ of P2 bugs addressed
- [ ] ✅ Final feedback review meeting held

---

## Security Testing

### Data Security Tests

#### Test 33: Password Security

**Objective:** Verify passwords are handled securely

**Test Steps:**

1. Login with test account
2. Inspect network traffic (use Wireshark or Charles Proxy)

**Verification:**

- [ ] Password is NOT sent in plain text
- [ ] HTTPS is used (or password is hashed)
- [ ] Password is not logged in logcat
- [ ] Password is not stored in SharedPreferences (only token)

**Pass Criteria:** ✅ No password leaks

---

#### Test 34: Token Security

**Objective:** Verify access tokens are protected

**Test Steps:**

1. Login successfully
2. Check token storage

**Verification:**

- [ ] Token is stored securely (EncryptedSharedPreferences or Keychain)
- [ ] Token includes expiration time
- [ ] Expired tokens are rejected by backend
- [ ] Token refresh flow works correctly

**Pass Criteria:** ✅ Tokens handled securely

---

### Network Security Tests

#### Test 35: Man-in-the-Middle (MITM) Protection

**Objective:** Verify network traffic is encrypted

**Test Steps:**

1. Setup MITM proxy (e.g., mitmproxy, Charles Proxy)
2. Attempt to intercept game traffic

**Verification:**

- [ ] HTTPS/WSS used for all backend communication
- [ ] Certificate pinning implemented (optional but recommended)
- [ ] Traffic cannot be read without certificate

**Pass Criteria:** ✅ All traffic encrypted

---

### Security Checklist

- [ ] ✅ Test 33: Password Security - PASS
- [ ] ✅ Test 34: Token Security - PASS
- [ ] ✅ Test 35: MITM Protection - PASS
- [ ] ✅ Test 36: Input Validation (SQL injection, XSS prevention) - PASS
- [ ] ✅ Test 37: Rate Limiting (prevent spam/DoS) - PASS

**Total Security Tests:** 6+
**Required Pass Rate:** 100%

---

## Regression Testing

### What is Regression Testing?

After fixing bugs or adding features, re-run previous tests to ensure nothing broke.

### Regression Test Suite

**Run these tests after ANY code change:**

1. **Core Functional Tests:**
   - [ ] Login flow
   - [ ] Character movement
   - [ ] Inventory management
   - [ ] Combat system

2. **Critical Path Tests:**
   - [ ] New player can create account → login → complete tutorial → save progress
   - [ ] Player can join voice call → speak → be heard by others

3. **Performance Baseline:**
   - [ ] Frame rate remains ≥ 60 FPS
   - [ ] Memory usage < 3 GB
   - [ ] Backend latency < 200ms

### Automated Regression Tests

**Setup CI/CD Pipeline:**

Example using GitHub Actions:

```yaml
# .github/workflows/regression-tests.yml
name: Regression Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run Unit Tests
        run: |
          "C:\Program Files\Epic Games\UE_5.3\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" `
            "NajikaDigivice.uproject" `
            -ExecCmds="Automation RunTests Najika;Quit" `
            -TestExit="Automation Test Queue Empty" `
            -log

      - name: Parse Test Results
        run: |
          # Parse test output for failures
```

### Regression Checklist

- [ ] ✅ All unit tests pass (re-run Test Automation)
- [ ] ✅ Critical functional tests pass (Login, Movement, Combat)
- [ ] ✅ Performance metrics within acceptable range
- [ ] ✅ No new crashes introduced
- [ ] ✅ Previously fixed bugs do not reappear

---

## Sign-Off Checklist

### Pre-Release Final Validation

**Before releasing to production, ALL items must be ✅:**

#### Code Quality

- [ ] ✅ All C++ code compiles without errors
- [ ] ✅ All Blueprints compile without errors
- [ ] ✅ No critical warnings in Output Log
- [ ] ✅ Code reviewed by at least one other developer
- [ ] ✅ No debug code or test accounts in Shipping build

#### Testing

- [ ] ✅ All unit tests pass (100%)
- [ ] ✅ All integration tests pass (100%)
- [ ] ✅ All functional tests pass (≥ 95%)
- [ ] ✅ All performance tests pass (100%)
- [ ] ✅ All platform-specific tests pass (100%)
- [ ] ✅ UAT completed with avg rating ≥ 4.0
- [ ] ✅ Security tests pass (100%)
- [ ] ✅ Regression tests pass (100%)

#### Assets & Content

- [ ] ✅ All required assets present (see ASSET_REQUIREMENTS.md)
- [ ] ✅ No missing textures (pink materials)
- [ ] ✅ No missing audio files
- [ ] ✅ All UI text finalized (no "TODO" or placeholder text)
- [ ] ✅ All icons and splash screens implemented

#### Documentation

- [ ] ✅ User manual created (if applicable)
- [ ] ✅ Known issues documented
- [ ] ✅ Privacy policy finalized
- [ ] ✅ Terms of service finalized
- [ ] ✅ Credits complete

#### Build & Deployment

- [ ] ✅ APK built in Shipping configuration
- [ ] ✅ APK signed with release keystore
- [ ] ✅ APK size < 500 MB (or OBB split configured)
- [ ] ✅ Version number updated correctly
- [ ] ✅ App icon and name correct
- [ ] ✅ Permissions declared in manifest

#### Legal & Compliance

- [ ] ✅ App rated appropriately (ESRB, PEGI, etc.)
- [ ] ✅ COPPA compliance (if target audience includes children)
- [ ] ✅ GDPR compliance (if EU users)
- [ ] ✅ Third-party licenses included (for plugins, assets)

#### Marketing

- [ ] ✅ Google Play Store listing ready (description, screenshots, video)
- [ ] ✅ App store screenshots prepared (at least 4)
- [ ] ✅ Feature graphic created (1024x500)
- [ ] ✅ Promotional video uploaded (optional but recommended)

---

## Final Sign-Off

**Sign-Off Authority:** Project Lead, QA Lead, Technical Lead

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Project Lead** | _____________ | _____________ | ______ |
| **QA Lead** | _____________ | _____________ | ______ |
| **Technical Lead** | _____________ | _____________ | ______ |

**Upon all signatures, the project is approved for release.**

---

## Post-Release Monitoring

### Week 1 Metrics

Monitor these metrics in the first week after release:

- [ ] Crash rate < 1%
- [ ] ANR (App Not Responding) rate < 0.5%
- [ ] Average session duration > 10 minutes
- [ ] User retention (Day 1) > 40%
- [ ] User retention (Day 7) > 20%
- [ ] Average app rating > 4.0 stars
- [ ] Backend error rate < 1%

**If any metric fails, investigate immediately and consider hotfix.**

---

## Support

### Documentation References

- `VISUAL_STUDIO_COMPILATION_GUIDE.md` - C++ compilation
- `ANDROID_BUILD_GUIDE.md` - APK building
- `BLUEPRINT_CREATION_GUIDE.md` - Blueprint setup
- `ASSET_REQUIREMENTS.md` - Asset specifications

### Testing Tools

- **Unreal Engine Test Automation:** Window > Test Automation
- **ADB (Android Debug Bridge):** Device communication and logging
- **Unreal Insights:** Performance profiling
- **Charles Proxy / mitmproxy:** Network traffic analysis
- **Android Profiler:** Memory, CPU, network profiling

---

**End of Testing & Validation Checklist**

*This checklist is part of the Najika UE5 Implementation documentation suite.*
