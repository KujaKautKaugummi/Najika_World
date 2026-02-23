# PHASE 3: BACKEND INTEGRATION - COMPLETE GUIDE
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**Phase:** 3 - Backend Integration (Woche 4-5)
**Dauer:** 2 Wochen

---

## 🎯 PHASE 3 ÜBERSICHT

### **Was wird gebaut:**
```
✅ NajikaBackendClient Plugin (HTTP Client) - FERTIG!
✅ NajikaVoiceSystem Plugin (Voice Calls) - FERTIG!
✅ WebSocketManager (Real-time Updates) - FERTIG!
✅ State Management (Game Instance)
✅ Testing & Debugging
```

---

## 🔌 TODO 3.1: HTTP CLIENT PLUGIN (✅ FERTIG!)

### **Plugin Installation:**

```bash
# 1. Kopiere Plugin
xcopy /E /I C:\Najika_World\UE5_PLUGIN_TEMPLATES\NajikaBackendClient C:\NajikaDigivice_UE5\Plugins\NajikaBackendClient

# 2. Regenerate Visual Studio project files
# (Rechtsklick auf .uproject → "Generate Visual Studio project files")

# 3. Öffne Visual Studio Solution
# 4. Build Solution (Ctrl+Shift+B)
# 5. Sollte ohne Fehler kompilieren!
```

### **Plugin Enable in UE5:**

```
1. Öffne UE5 Editor
2. Edit → Plugins
3. Suche "NajikaBackendClient"
4. Enable checkbox
5. Restart Editor
```

### **Test das Plugin:**

```
1. Create Blueprint: BP_TestBackend (Actor)

2. Event BeginPlay:
   → Create NajikaAPIClient Object
   → Store in variable: APIClient

   → SendChatMessage
      Message: "Hello Najika!"
      Callback: OnChatResponse

3. OnChatResponse Event:
   → PrintString: Response

4. Place BP_TestBackend in Level
5. Play in Editor (PIE)
6. Check Output Log für Response
```

### **Erwartetes Ergebnis:**
```
Output Log:
[Najika] Chat response: Hi Mr.K! 💜 What can I do for you?
```

✅ **Wenn Response kommt: Plugin funktioniert perfekt!**

---

## 🎤 TODO 3.2: VOICE SYSTEM PLUGIN (✅ FERTIG!)

### **Plugin Installation:**

```bash
# 1. Kopiere Plugin
xcopy /E /I C:\Najika_World\UE5_PLUGIN_TEMPLATES\NajikaVoiceSystem C:\NajikaDigivice_UE5\Plugins\NajikaVoiceSystem

# 2. Regenerate VS project files
# 3. Build Solution
# 4. Enable in UE5 Editor
```

### **Test Voice System:**

```
1. Create Blueprint: BP_TestVoice (Actor)

2. Variables:
   - VoiceManager (VoiceCallManager Object Reference)

3. Event BeginPlay:
   → Create VoiceCallManager Object
   → Store in VoiceManager variable
   → Initialize

4. Custom Event: StartCall
   → VoiceManager->StartVoiceCall()

5. Bind Events:
   → OnVoiceCallStarted → PrintString "Call Started"
   → OnSpeechRecognized → PrintString "You said: {Text}"
   → OnNajikaResponse → Play Sound 2D
   → OnVoiceCallError → PrintString "Error: {Error}"

6. Input Action:
   → V-Taste → StartCall

7. Place in Level, PIE
8. Press V
9. Speak into microphone
```

### **Erwartetes Ergebnis:**
```
1. "Call Started" in Output Log
2. Deine Sprache wird erkannt → "You said: Hello"
3. Najika antwortet mit Audio
4. Audio wird abgespielt
```

### **Android Microphone Permission:**

Füge zu `Config/DefaultEngine.ini` hinzu:
```ini
[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]
PackageForOculusMobile=()
bPackageDataInsideApk=True
bEnableMicrophonePermissionByDefault=True
```

Füge zu `AndroidManifest.xml` (wird automatisch generiert):
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS"/>
```

---

## 🌐 TODO 3.3: WEBSOCKET INTEGRATION (✅ FERTIG!)

### **WebSocket Plugin Enable:**

```
1. Edit → Plugins
2. Suche "WebSockets"
3. Enable "Web Socket Networking"
4. Restart Editor
```

### **WebSocket Manager Setup:**

```
1. Create Blueprint: BP_TestWebSocket (Actor)

2. Variables:
   - WSManager (WebSocketManager Object Reference)

3. Event BeginPlay:
   → Create WebSocketManager Object
   → Connect("ws://127.0.0.1:8000/ws")

4. Bind Events:
   → OnConnected → PrintString "WebSocket Connected!"
   → OnDisconnected → PrintString "WebSocket Disconnected"
   → OnMessageReceived → HandleMessage

5. HandleMessage Function:
   Input: Message (String)
   → Parse JSON
   → Check "type" field
   → Handle based on type:
      - "proactive_message" → Show Najika speech bubble
      - "status_update" → Update UI
      - "battle_start" → Switch to battle mode
```

### **Backend WebSocket Endpoint:**

Der Python-Backend hat bereits einen WebSocket-Endpoint:
```python
# In najika_server.py:
@socketio.on('connect')
def handle_connect():
    print('[WebSocket] Client connected')

@socketio.on('message')
def handle_message(data):
    # Handle incoming messages
    pass

# Proactive messages from Najika:
socketio.emit('proactive_message', {
    'message': 'Mr.K, ich habe etwas Neues gelernt!',
    'emotion': 'excited'
})
```

### **Use Cases für WebSocket:**

1. **Proactive Messages:**
   - Najika spricht dich von selbst an
   - "Mr.K, mir ist langweilig!"
   - "Schau mal was ich gefunden habe!"

2. **Real-time State Updates:**
   - Hunger/Energy/Happiness changes
   - Level-up notifications
   - Achievement unlocks

3. **Living System Events:**
   - Auto-care messages
   - Mood changes
   - Activity updates

4. **Multiplayer (Future):**
   - Other players in world
   - Co-op battles
   - Trading system

---

## 💾 TODO 3.4: STATE MANAGEMENT

### **Create Game Instance:**

```
1. Create Blueprint: BP_NajikaGameInstance
   Parent: GameInstance

2. Variables:
   - APIClient (NajikaAPIClient)
   - WSManager (WebSocketManager)
   - VoiceManager (VoiceCallManager)
   - NajikaState (Struct):
      * Hunger (Int 0-100)
      * Energy (Int 0-100)
      * Happiness (Int 0-100)
      * Level (Int)
      * XP (Int)
   - UserProfile (Struct):
      * Username (String)
      * Level (Int)
      * Points (Int)
      * Inventory (Array of Items)
   - ChatHistory (Array of ChatMessage)
   - ConnectionStatus (Enum): Connected/Disconnected/Reconnecting

3. Functions:
   - Init (Event Init)
      → Create APIClient
      → Create WSManager
      → Create VoiceManager
      → Connect WebSocket
      → Load State from Backend

   - LoadStateFromBackend
      → GET /api/state
      → Parse JSON
      → Update NajikaState
      → Update UserProfile

   - SaveStateToBackend (Auto-save every 30 seconds)
      → POST /api/save
      → Send current state

   - OnWebSocketMessage
      → Parse message
      → Update state
      → Broadcast to UI

   - GetAPIClient → APIClient
   - GetWSManager → WSManager
   - GetVoiceManager → VoiceManager
```

### **Set Game Instance in Project Settings:**

```
1. Edit → Project Settings
2. Project → Maps & Modes
3. Game Instance Class: BP_NajikaGameInstance
4. Save
```

### **Access Game Instance from Blueprints:**

```
Any Blueprint:
→ Get Game Instance
→ Cast to BP_NajikaGameInstance
→ Now you can access APIClient, WSManager, etc.
```

### **Auto-Sync mit Backend:**

```
1. In BP_NajikaGameInstance:
   - Event Init
      → Set Timer by Function Name
         Function: "UpdateStateFromBackend"
         Time: 5.0 (every 5 seconds)
         Looping: True

2. UpdateStateFromBackend Function:
   → APIClient->GetNajikaStatus()
   → OnStatusReceived:
      * Update NajikaState
      * Broadcast Event: OnStateUpdated
      * Update UI
```

### **UI Binding:**

```
Any UI Widget:
1. Get Game Instance
2. Cast to BP_NajikaGameInstance
3. Bind to OnStateUpdated event
4. Update UI elements when state changes
```

---

## 🧪 TODO 3.5: INTEGRATION TESTING

### **Test Checklist:**

#### **HTTP Client Tests:**
```
1. [ ] Chat mit Najika funktioniert
2. [ ] Get Najika Status gibt korrekte Werte
3. [ ] Feed/Drink/Wash aktualisieren Status
4. [ ] TTS Audio wird generiert
5. [ ] Fehlerbehandlung bei Backend Disconnect
6. [ ] Timeout nach 30 Sekunden
```

#### **Voice System Tests:**
```
1. [ ] Microphone Permission wird requested (Android)
2. [ ] Audio wird captured
3. [ ] Audio wird an Backend gesendet
4. [ ] Whisper STT erkennt Sprache
5. [ ] TTS Audio wird empfangen
6. [ ] Audio wird abgespielt
7. [ ] Lip Sync funktioniert (falls implementiert)
8. [ ] Call kann beendet werden
```

#### **WebSocket Tests:**
```
1. [ ] WebSocket verbindet beim Start
2. [ ] Proactive Messages werden empfangen
3. [ ] State Updates in Real-time
4. [ ] Heartbeat funktioniert (Connection bleibt offen)
5. [ ] Auto-Reconnect bei Disconnect
6. [ ] Nachrichten senden funktioniert
```

#### **State Management Tests:**
```
1. [ ] Game Instance erstellt APIs beim Start
2. [ ] State wird vom Backend geladen
3. [ ] Auto-Save alle 30 Sekunden
4. [ ] State bleibt über Level-Wechsel erhalten
5. [ ] UI aktualisiert bei State-Changes
```

---

## 🔧 DEBUGGING TIPPS

### **Backend-Verbindung testen:**

```bash
# 1. Prüfe ob Backend läuft:
curl http://127.0.0.1:8000/health

# Erwartete Antwort:
# {"status": "healthy", "uptime": 12345}

# 2. Test Chat API:
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Test\"}"

# 3. Test WebSocket:
# Benutze Tool wie "wscat" oder Browser Console:
# ws = new WebSocket("ws://127.0.0.1:8000/ws");
# ws.onmessage = (e) => console.log(e.data);
```

### **UE5 Output Log Monitoring:**

```
Im UE5 Editor:
Window → Developer Tools → Output Log

Filter nach:
- [Najika] → Alle Najika-bezogenen Logs
- [HTTP] → HTTP-Requests
- [WebSocket] → WebSocket-Events

Enable "Verbose" für detaillierte Logs
```

### **Common Issues:**

**Problem: "Connection refused"**
```
Lösung:
1. Backend Server läuft nicht → Starte najika_server.py
2. Falsche URL → Prüfe BaseURL (http://127.0.0.1:8000)
3. Firewall blockt → Temporär deaktivieren für Test
```

**Problem: "JSON Parse Error"**
```
Lösung:
1. Backend sendet invalides JSON → Check Backend Log
2. Encoding Problem → UTF-8 verwenden
3. Log Raw Response String → Debuggen
```

**Problem: "Microphone not working"**
```
Lösung:
1. Permission nicht granted → Request Permission
2. Android Manifest fehlt → Add RECORD_AUDIO permission
3. Audio Device nicht gefunden → Check FAudioCapture
```

**Problem: "WebSocket keeps disconnecting"**
```
Lösung:
1. Heartbeat nicht aktiv → Enable Heartbeat (30s)
2. Backend Timeout → Erhöhe Backend Timeout
3. Network issues → Check Connection
```

---

## 📊 SUCCESS CRITERIA

**Phase 3 ist komplett wenn:**

```
✅ NajikaBackendClient Plugin funktioniert
   - Chat messages senden/empfangen
   - Status abfragen
   - Feed/Drink/Wash funktioniert
   - TTS Audio generieren

✅ NajikaVoiceSystem Plugin funktioniert
   - Microphone Capture
   - Audio zu Backend senden
   - STT Recognition
   - TTS Playback

✅ WebSocket funktioniert
   - Verbindung bleibt offen
   - Proactive Messages empfangen
   - Real-time Updates
   - Auto-Reconnect

✅ State Management funktioniert
   - Game Instance lädt State beim Start
   - Auto-Save alle 30s
   - UI updated bei State-Changes
   - State bleibt über Sessions erhalten

✅ Integration Tests bestanden
   - Alle Checklisten-Items ✅
   - Keine kritischen Bugs
   - Performance akzeptabel (<500ms Latency)
```

---

## 🎉 PHASE 3 COMPLETE!

Wenn alle Success Criteria erfüllt sind, ist **Phase 3 abgeschlossen!**

**Nächster Schritt:** Phase 4 - Gameplay Systems

**Geschätzte Dauer Phase 3:** 2 Wochen
**Nach Abschluss:** Create Progress Report + Git Commit + Push

---

**Model 1 - Digivice APK Development**
**Phase:** 3/9 - Backend Integration
**Status:** Ready to Execute (Plugins already created!)
