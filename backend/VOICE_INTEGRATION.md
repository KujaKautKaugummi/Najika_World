# Voice & TTS Integration

**Status:** ✅ Complete (PHASE 21)
**Version:** 1.0

---

## Overview

Complete voice integration providing Speech-to-Text (Whisper AI) and Text-to-Speech (Microsoft Edge TTS) capabilities for the Najika backend.

### Features

- ✅ **Speech-to-Text** - Whisper AI transcription
- ✅ **Text-to-Speech** - Microsoft Edge Neural Voices
- ✅ **4 Personalities** - Megumin, Harley, Shiro, Melissa
- ✅ **WebSocket Voice Chat** - Real-time voice communication
- ✅ **Base64 Support** - Easy integration with web clients
- ✅ **Async Support** - Non-blocking operations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Voice API (/api/voice)                     │
│  - POST /transcribe   - POST /tts   - WebSocket /ws/{token} │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────▼────────┐
    │  Voice Service   │
    │  (Unified API)   │
    └────┬────────┬────┘
         │        │
    ┌────▼─────┐ ┌▼──────────┐
    │ Whisper  │ │ Edge TTS  │
    │ Service  │ │  Service  │
    └──────────┘ └───────────┘
        │              │
    ┌───▼───┐     ┌───▼────┐
    │Whisper│     │ Edge   │
    │  AI   │     │  TTS   │
    └───────┘     └────────┘
```

---

## Installation

### Requirements

```bash
# Whisper AI (Speech-to-Text)
pip install openai-whisper

# Edge TTS (Text-to-Speech)
pip install edge-tts

# Audio processing
pip install pydub soundfile librosa
```

### Optional: GPU Support

For faster Whisper transcription with GPU:

```bash
# CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## Usage

### 1. Speech-to-Text (Whisper AI)

#### API Endpoint

**POST** `/api/voice/transcribe`

**Request:**
```json
{
  "audio_base64": "UklGRiQ..."  // Base64 encoded audio (WAV/MP3)
}
```

**Response:**
```json
{
  "success": true,
  "transcription": "Hallo, ich bin Najika!",
  "language": "de"
}
```

#### Python Usage

```python
from backend.services.voice_service import voice_service

# From file
result = voice_service.transcribe("audio.wav", language="de")
print(result["text"])

# From base64
result = voice_service.transcribe_base64(audio_base64, language="de")
print(result["text"])
```

#### Supported Languages

- `de` - German
- `en` - English
- `ja` - Japanese
- `fr` - French
- `es` - Spanish
- Auto-detect: Set `language=None`

#### Whisper Models

- `tiny` - Fastest, least accurate (~39M parameters)
- `base` - Fast, good accuracy (~74M parameters) **[Default]**
- `small` - Balanced (~244M parameters)
- `medium` - High accuracy (~769M parameters)
- `large` - Best accuracy (~1550M parameters)

Configure in `.env`:
```env
WHISPER_MODEL=base
```

---

### 2. Text-to-Speech (Edge TTS)

#### API Endpoint

**POST** `/api/voice/tts`

**Request:**
```json
{
  "text": "EXPLOSION!",
  "language": "de"
}
```

**Response:**
```json
{
  "success": true,
  "audio_base64": "SUQzBAAAAAA...",  // MP3 audio
  "format": "mp3",
  "personality": "megumin"
}
```

#### Python Usage

```python
from backend.services.voice_service import voice_service

# Generate audio file
audio_path = voice_service.speak("Hallo, ich bin Najika!")
print(f"Audio saved to: {audio_path}")

# Get base64 (for API)
audio_base64 = voice_service.speak_base64("Hallo!")

# Async version
audio_path = await voice_service.speak_async("Hallo!")
audio_base64 = await voice_service.speak_base64_async("Hallo!")
```

#### Personalities

All personalities use the same base voice (`de-DE-AmalaNeural`) with different parameters:

##### 1. Megumin (Default)
- **Style:** Energetic, dramatic, anime-style
- **Rate:** +15% (fast, excited)
- **Volume:** +10% (loud for EXPLOSION!)
- **Pitch:** +5Hz (young, bright voice)
- **Use Case:** Main Najika personality, combat, explosions

```python
voice_service.set_tts_personality("megumin")
```

##### 2. Harley
- **Style:** Chaotic, hyperactive, unpredictable
- **Rate:** +25% (very fast)
- **Volume:** +15% (very loud)
- **Pitch:** +12Hz (high, excited)
- **Use Case:** Playful interactions, jokes, chaos mode

```python
voice_service.set_tts_personality("harley")
```

##### 3. Shiro
- **Style:** Calm, analytical, monotone
- **Rate:** -10% (slower, deliberate)
- **Volume:** +0% (normal, controlled)
- **Pitch:** -8Hz (lower, serious)
- **Use Case:** Strategy, analysis, calm moments

```python
voice_service.set_tts_personality("shiro")
```

##### 4. Melissa
- **Style:** Friendly, casual, warm
- **Rate:** +5% (slightly faster, conversational)
- **Volume:** +5% (slightly louder, friendly)
- **Pitch:** +2Hz (slightly higher, warm)
- **Use Case:** General conversations, friendly interactions

```python
voice_service.set_tts_personality("melissa")
```

---

### 3. WebSocket Voice Chat

#### Connection

Connect to WebSocket with JWT token:

```
ws://localhost:8000/api/voice/ws/{YOUR_JWT_TOKEN}
```

#### JavaScript Client Example

```javascript
// Get JWT token from login
const token = "eyJ0eXAiOiJKV1QiLCJhbGc...";

// Connect to voice WebSocket
const ws = new WebSocket(`ws://localhost:8000/api/voice/ws/${token}`);

ws.onopen = () => {
  console.log("Connected to voice chat");
};

// Send text message (ping, get_users, etc.)
ws.send(JSON.stringify({
  type: "ping"
}));

// Send audio data (binary)
const audioBlob = await recordAudio();
const audioBuffer = await audioBlob.arrayBuffer();
ws.send(audioBuffer);

// Receive messages
ws.onmessage = (event) => {
  if (typeof event.data === 'string') {
    const message = JSON.parse(event.data);

    if (message.type === 'audio') {
      // Play received audio
      playAudio(message.audio);  // Base64 encoded
    }
  }
};
```

#### WebSocket Message Types

##### Client → Server

**Ping:**
```json
{
  "type": "ping"
}
```

**Get Users:**
```json
{
  "type": "get_users"
}
```

**Transcription Request:**
```json
{
  "type": "transcription_request"
}
```

**Binary Audio:**
Send raw audio bytes (not JSON)

##### Server → Client

**Pong:**
```json
{
  "type": "pong",
  "timestamp": "2025-01-14T12:00:00"
}
```

**User Joined:**
```json
{
  "type": "user_joined",
  "user_id": "1",
  "username": "Alice",
  "timestamp": "2025-01-14T12:00:00"
}
```

**User Left:**
```json
{
  "type": "user_left",
  "user_id": "1",
  "username": "Alice",
  "timestamp": "2025-01-14T12:00:00"
}
```

**Audio Broadcast:**
```json
{
  "type": "audio",
  "user_id": "1",
  "username": "Alice",
  "audio": "SUQzBAAAAAA...",  // Base64
  "timestamp": "2025-01-14T12:00:00"
}
```

**Users List:**
```json
{
  "type": "users_list",
  "users": [
    {
      "user_id": "1",
      "username": "Alice",
      "connected_at": "2025-01-14T11:55:00"
    }
  ]
}
```

---

## Configuration

### Environment Variables

```.env
# Whisper AI
WHISPER_MODEL=base  # tiny, base, small, medium, large

# TTS
TTS_ENGINE=edge  # edge or coqui
VOICE_DATA_DIR=./voice_data
```

### Voice Service Configuration

```python
from backend.services.voice_service import VoiceService

# Initialize with custom settings
voice_service = VoiceService(
    whisper_model="small",     # Better accuracy
    tts_personality="megumin"  # Default personality
)
```

---

## Performance

### Whisper AI Transcription

| Model | Speed (Real-time Factor) | Accuracy | VRAM |
|-------|-------------------------|----------|------|
| tiny | ~10x | 80% | ~1GB |
| base | ~7x | 85% | ~1GB |
| small | ~4x | 90% | ~2GB |
| medium | ~2x | 95% | ~5GB |
| large | ~1x | 98% | ~10GB |

**Recommendations:**
- **Development:** `base` (good balance)
- **Production (CPU):** `base` or `small`
- **Production (GPU):** `medium` or `large`

### Edge TTS Generation

- **Speed:** ~1-2 seconds for short phrases
- **Latency:** < 500ms with caching
- **Quality:** Near-human (Microsoft Neural Voices)
- **Cost:** FREE (no API key required)

---

## Integration Examples

### Example 1: Voice Chat Bot

```python
from backend.services.voice_service import voice_service

async def voice_chat(audio_base64: str) -> str:
    # Transcribe user speech
    result = voice_service.transcribe_base64(audio_base64)

    if not result["success"]:
        return None

    user_text = result["text"]
    print(f"User said: {user_text}")

    # Generate response (example)
    response_text = f"Du hast gesagt: {user_text}"

    # Convert to speech
    response_audio = await voice_service.speak_base64_async(response_text)

    return response_audio
```

### Example 2: Personality Switcher

```python
from backend.services.voice_service import voice_service

# Switch personalities based on context
if "EXPLOSION" in text:
    voice_service.set_tts_personality("megumin")
elif "strategy" in text.lower():
    voice_service.set_tts_personality("shiro")
elif "joke" in text.lower():
    voice_service.set_tts_personality("harley")
else:
    voice_service.set_tts_personality("melissa")

# Generate speech with selected personality
audio = voice_service.speak_base64(text)
```

### Example 3: UE5 Integration

```cpp
// In UE5 C++ (NajikaVoiceSystem plugin)

// Send audio to backend
FString AudioBase64 = EncodeAudioToBase64(AudioData);
FString URL = "http://localhost:8000/api/voice/transcribe";

// POST request
TSharedRef<IHttpRequest> Request = Http->CreateRequest();
Request->SetURL(URL);
Request->SetVerb("POST");
Request->SetHeader("Content-Type", "application/json");
Request->SetContentAsString(FString::Printf(TEXT("{\"audio_base64\": \"%s\"}"), *AudioBase64));

Request->OnProcessRequestComplete().BindLambda([](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess) {
    if (bSuccess) {
        FString Transcription = Response->GetContentAsString();
        UE_LOG(LogTemp, Log, TEXT("Transcription: %s"), *Transcription);
    }
});

Request->ProcessRequest();
```

---

## Testing

### Test Whisper Transcription

```python
from backend.services.voice_service import voice_service

# Test with audio file
result = voice_service.transcribe("test_audio.wav")

print(f"Success: {result['success']}")
print(f"Text: {result['text']}")
print(f"Language: {result['language']}")
```

### Test Edge TTS

```python
from backend.services.voice_service import voice_service

# Test all personalities
personalities = ["megumin", "harley", "shiro", "melissa"]

for personality in personalities:
    voice_service.set_tts_personality(personality)
    audio_path = voice_service.speak(f"Hallo, ich bin {personality}!")
    print(f"Generated: {audio_path}")
```

### Test WebSocket

```bash
# Install websocat for testing
cargo install websocat

# Connect to WebSocket
websocat "ws://localhost:8000/api/voice/ws/YOUR_JWT_TOKEN"

# Send ping
{"type": "ping"}

# Get users
{"type": "get_users"}
```

---

## Troubleshooting

### Whisper AI Issues

#### Problem: "Model not found"
```
Solution: Download model manually
python -c "import whisper; whisper.load_model('base')"
```

#### Problem: "Out of memory"
```
Solution: Use smaller model
WHISPER_MODEL=tiny
```

#### Problem: "Slow transcription (CPU)"
```
Solutions:
1. Use GPU (install torch with CUDA)
2. Use smaller model (tiny/base)
3. Use shorter audio clips
```

### Edge TTS Issues

#### Problem: "edge-tts not installed"
```bash
pip install edge-tts
```

#### Problem: "Network error"
```
Edge TTS requires internet connection
Check firewall/proxy settings
```

#### Problem: "Audio quality issues"
```
Try different voice or personality
Check audio output format (MP3 default)
```

### WebSocket Issues

#### Problem: "Connection refused"
```
1. Check backend is running
2. Verify JWT token is valid
3. Check CORS settings
```

#### Problem: "Audio not playing"
```
1. Check audio format (MP3)
2. Decode base64 correctly
3. Verify audio codec support in browser
```

---

## API Reference

### WhisperService

```python
class WhisperService:
    def __init__(self, model_size: str = "base")
    def transcribe(self, audio_path: str, language: str = "de") -> Dict
    def transcribe_from_base64(self, audio_base64: str, language: str = "de") -> Dict
```

### EdgeTTSService

```python
class EdgeTTSService:
    def __init__(self, personality: str = "megumin")
    async def speak_async(self, text: str, output_path: Optional[str] = None) -> str
    def speak(self, text: str, output_path: Optional[str] = None) -> str
    async def speak_to_base64_async(self, text: str) -> str
    def speak_to_base64(self, text: str) -> str
    def set_personality(self, personality: str)
```

### VoiceService (Unified)

```python
class VoiceService:
    def __init__(self, whisper_model: str = "base", tts_personality: str = "megumin")
    def transcribe(self, audio_path: str, language: str = "de") -> Dict
    def transcribe_base64(self, audio_base64: str, language: str = "de") -> Dict
    def speak(self, text: str, output_path: Optional[str] = None) -> str
    def speak_base64(self, text: str) -> str
    async def speak_async(self, text: str, output_path: Optional[str] = None) -> str
    async def speak_base64_async(self, text: str) -> str
    def set_tts_personality(self, personality: str)
    def get_info() -> Dict
```

---

## Summary

**PHASE 21: Voice & TTS Integration** successfully completed:

- ✅ Created VoiceService with Whisper AI and Edge TTS
- ✅ Integrated with existing voice scripts
- ✅ Updated voice API endpoints with real implementations
- ✅ Added 4 personality profiles for TTS
- ✅ WebSocket voice chat ready
- ✅ Base64 support for easy web integration
- ✅ Async/await support for performance

**Total Lines:** ~500 (VoiceService) + API updates

**Ready for:**
- UE5 mobile game voice chat
- Digivice web game voice integration
- Frontend dashboard with voice controls
- Real-time voice communication

**Next Phase:** PHASE 25 - Documentation Consolidation or PHASE 22 - Frontend Dashboard

---

**Created:** PHASE 21
**Author:** Web Model (Claude Sonnet 4.5)
