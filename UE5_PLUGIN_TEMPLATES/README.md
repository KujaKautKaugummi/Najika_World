# UE5 PLUGIN TEMPLATES - NAJIKA DIGIVICE
**Model 1 - P0 Priority**
**Created:** 2025-11-11

---

## 📦 AVAILABLE PLUGINS

### **1. NajikaBackendClient** ✅ READY
**Purpose:** HTTP Client for Python Backend Integration

**Features:**
- Chat with Najika (POST /api/chat)
- Get Najika Status (GET /api/najika/status)
- Feed/Drink/Wash Najika (POST /api/najika/*)
- Text-to-Speech (POST /api/tts)
- JSON parsing & serialization
- Async callbacks (delegates)

**Files:**
```
NajikaBackendClient/
├── NajikaBackendClient.uplugin    ← Plugin definition
├── Source/
│   ├── NajikaBackendClient.Build.cs   ← Build configuration
│   ├── Public/
│   │   └── NajikaAPIClient.h          ← Header file
│   └── Private/
│       └── NajikaAPIClient.cpp        ← Implementation
```

**How to use:**
1. Copy entire `NajikaBackendClient/` folder to:
   `C:\NajikaDigivice_UE5\Plugins\`

2. In UE5 Editor:
   - Edit → Plugins → Search "NajikaBackendClient"
   - Enable plugin
   - Restart editor

3. In Blueprint or C++:
   ```cpp
   // C++ Example:
   UNajikaAPIClient* Client = NewObject<UNajikaAPIClient>();
   Client->SendChatMessage("Hello Najika!", [](const FString& Response, bool bSuccess) {
       if (bSuccess) {
           UE_LOG(LogTemp, Log, TEXT("Najika says: %s"), *Response);
       }
   });
   ```

   ```
   Blueprint Example:
   Create NajikaAPIClient Object
   → Send Chat Message (Message: "Hello Najika!")
   → On Chat Response (Response, Success)
      → Print String (Response)
   ```

**API Methods:**
- `SendChatMessage(Message, Callback)`
- `GetNajikaStatus(Callback)`
- `FeedNajika(Callback)`
- `GiveWaterToNajika(Callback)`
- `WashNajika(Callback)`
- `GenerateTTS(Text, Callback)`

**Dependencies:**
- HTTP Module
- Json Module
- JsonUtilities Module

---

### **2. NajikaVoiceSystem** ⏳ TODO (Phase 3)
**Purpose:** Voice Call Integration (Whisper STT + Coqui TTS)

**Features (Planned):**
- Microphone capture (Android)
- Audio streaming to backend
- WebSocket connection
- TTS audio playback
- Lip sync integration

**Status:** Not yet implemented
**ETA:** Phase 3 (Week 4-5)

---

## 📋 INSTALLATION INSTRUCTIONS

### **Step 1: Copy Plugin to Project**
```bash
# Open PowerShell
cd C:\NajikaDigivice_UE5\
mkdir Plugins
xcopy /E /I C:\Najika_World\UE5_PLUGIN_TEMPLATES\NajikaBackendClient Plugins\NajikaBackendClient
```

### **Step 2: Regenerate Project Files**
1. Right-click on `NajikaDigivice.uproject`
2. Select "Generate Visual Studio project files"
3. Wait for completion

### **Step 3: Compile Plugin**
1. Open `NajikaDigivice.sln` in Visual Studio 2022
2. Build Solution (Ctrl+Shift+B)
3. Check for errors (should compile successfully!)

### **Step 4: Enable Plugin in UE5**
1. Open UE5 Editor
2. Edit → Plugins
3. Search "NajikaBackendClient"
4. Check "Enabled"
5. Restart Editor

### **Step 5: Test Plugin**
1. Create new Blueprint: BP_TestBackend
2. In Event Graph:
   - Begin Play
   - Create NajikaAPIClient Object
   - Send Chat Message ("Test message")
   - On Chat Response → Print String

3. Play in Editor (PIE)
4. Check Output Log for response

---

## 🧪 TESTING CHECKLIST

### **Backend Connection Test:**
```
1. [ ] Backend server is running (http://127.0.0.1:8000)
2. [ ] NajikaAPIClient can be created
3. [ ] SendChatMessage returns response
4. [ ] GetNajikaStatus returns values
5. [ ] FeedNajika updates hunger
6. [ ] GenerateTTS returns audio path
```

### **Error Handling Test:**
```
1. [ ] Stop backend server → Request fails gracefully
2. [ ] Invalid JSON → Parser returns nullptr
3. [ ] Timeout (30s) → Callback called with failure
4. [ ] Network error → Callback called with failure
```

---

## 🔧 TROUBLESHOOTING

### **Problem: Plugin not found after copy**
**Solution:**
1. Regenerate Visual Studio project files
2. Rebuild solution
3. Restart UE5 Editor

### **Problem: Compile errors**
**Solution:**
1. Check Visual Studio 2022 installed with C++ workload
2. Check all dependencies (HTTP, Json, JsonUtilities) in .Build.cs
3. Clean solution → Rebuild

### **Problem: HTTP requests fail**
**Solution:**
1. Check backend server is running:
   ```bash
   curl http://127.0.0.1:8000/health
   ```
2. Check firewall allows localhost connections
3. Check BaseURL is correct ("http://127.0.0.1:8000")

### **Problem: JSON parse errors**
**Solution:**
1. Check backend response format (should be valid JSON)
2. Check Content-Type header is "application/json"
3. Log response string to Output Log

---

## 📚 DOCUMENTATION

### **Backend API Reference:**
See: `C:\Najika_World\NAJIKA_CURRENT_ARCHITECTURE.md` (Lines 240-625)

### **UE5 HTTP Module:**
https://docs.unrealengine.com/5.6/en-US/http-module-in-unreal-engine/

### **UE5 JSON Parsing:**
https://docs.unrealengine.com/5.6/en-US/json-handling-in-unreal-engine/

---

## 🚀 NEXT STEPS

After NajikaBackendClient is working:
1. **Implement NajikaVoiceSystem plugin** (Phase 3)
2. **Create UMG Widgets** for UI (Phase 5)
3. **Integrate with Character Blueprint** (Phase 2)
4. **Add WebSocket support** for real-time updates (Phase 3)

---

**Good luck! 🔥**
**Model 1 - Digivice APK Development**
