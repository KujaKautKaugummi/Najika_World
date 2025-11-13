# Voice Backend API Specification - Najika Voice System

**Version:** 1.0
**Last Updated:** 2025-01-13
**Protocol:** HTTP REST + WebSocket
**Base URL:** `http://localhost:8000` (Development)

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [HTTP REST Endpoints](#http-rest-endpoints)
4. [WebSocket Protocol](#websocket-protocol)
5. [Data Formats](#data-formats)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Implementation Examples](#implementation-examples)

---

## Overview

### Architecture

```
UE5 Client (NajikaVoiceSystem)
    ↓
    ├─ HTTP → /api/voice/* (Transcription, Config)
    └─ WebSocket → /ws/voice (Real-time Audio Streaming)
         ↓
    Backend Server (localhost:8000)
         ↓
    ├─ Whisper AI (Speech-to-Text)
    └─ Voice Room Manager (Multi-user Voice Chat)
```

### Features

- **Real-time Voice Chat:** WebSocket-based audio streaming
- **Speech-to-Text:** Whisper AI integration via HTTP
- **Voice Rooms:** Multi-user voice channels
- **Push-to-Talk & VAD:** Client-controlled transmission modes

---

## Authentication

### JWT Token Authentication

All API requests require a valid JWT token obtained from the login endpoint.

**Header Format:**
```
Authorization: Bearer <access_token>
```

**Token Payload Example:**
```json
{
  "user_id": "12345",
  "username": "test_user_1",
  "exp": 1705176000,  // Expiration timestamp
  "iat": 1705089600   // Issued at timestamp
}
```

### Authentication Flow

1. Client logs in via `/api/auth/login` (see NajikaBackendClient plugin)
2. Backend returns `access_token`
3. Client stores token
4. Client includes token in `Authorization` header for all subsequent requests

**Unauthenticated requests receive:**
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authentication token",
  "status": 401
}
```

---

## HTTP REST Endpoints

### 1. Transcribe Audio (Whisper AI)

**Endpoint:** `POST /api/voice/transcribe`

**Description:** Transcribe audio to text using Whisper AI

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "audio_data": "<Base64-encoded audio data>",
  "sample_rate": 48000,
  "encoding": "pcm16",
  "language": "en",
  "auto_detect_language": false
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audio_data` | string | Yes | Base64-encoded audio (WAV, PCM16, Opus) |
| `sample_rate` | integer | Yes | Sample rate in Hz (16000, 48000) |
| `encoding` | string | Yes | Audio encoding (`pcm16`, `opus`, `wav`) |
| `language` | string | No | ISO 639-1 language code (`en`, `de`, `ja`) |
| `auto_detect_language` | boolean | No | Auto-detect language (default: `false`) |

**Response (Success - 200 OK):**
```json
{
  "text": "Hello, this is a test message.",
  "confidence": 0.95,
  "language_code": "en",
  "processing_time_ms": 342,
  "word_count": 6
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Transcribed text |
| `confidence` | float | Confidence score (0.0 - 1.0) |
| `language_code` | string | Detected or specified language |
| `processing_time_ms` | integer | Server processing time in milliseconds |
| `word_count` | integer | Number of words in transcription |

**Response (Error - 400 Bad Request):**
```json
{
  "error": "Invalid Audio Data",
  "message": "Could not decode Base64 audio data",
  "status": 400
}
```

**Response (Error - 500 Internal Server Error):**
```json
{
  "error": "Transcription Failed",
  "message": "Whisper AI processing error",
  "status": 500
}
```

**Example Usage (UE5 C++):**
```cpp
// In UNajikaWhisperClient
void UNajikaWhisperClient::TranscribeAudio(const TArray<uint8>& AudioData, int32 SampleRate, const FString& LanguageCode)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject());

    // Encode audio to Base64
    FString AudioDataBase64 = FBase64::Encode(AudioData);
    JsonObject->SetStringField(TEXT("audio_data"), AudioDataBase64);
    JsonObject->SetNumberField(TEXT("sample_rate"), SampleRate);
    JsonObject->SetStringField(TEXT("encoding"), TEXT("pcm16"));
    JsonObject->SetStringField(TEXT("language"), LanguageCode);

    // Send HTTP POST
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(BackendURL + TEXT("/api/voice/transcribe"));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Authorization"), TEXT("Bearer ") + AccessToken);
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(SerializeJson(JsonObject));
    Request->OnProcessRequestComplete().BindUObject(this, &UNajikaWhisperClient::OnTranscribeResponse);
    Request->ProcessRequest();
}
```

---

### 2. Get Voice Room Info

**Endpoint:** `GET /api/voice/rooms/{room_id}`

**Description:** Get information about a voice room

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `room_id` | string | Voice room ID |

**Response (Success - 200 OK):**
```json
{
  "room_id": "room_12345",
  "room_name": "Party Voice Chat",
  "participants": [
    {
      "user_id": "user_001",
      "username": "Alice",
      "is_speaking": true,
      "is_muted": false
    },
    {
      "user_id": "user_002",
      "username": "Bob",
      "is_speaking": false,
      "is_muted": false
    }
  ],
  "max_participants": 10,
  "created_at": "2025-01-13T10:30:00Z"
}
```

---

### 3. Create Voice Room

**Endpoint:** `POST /api/voice/rooms`

**Description:** Create a new voice room

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "room_name": "My Party Voice Chat",
  "max_participants": 10,
  "is_public": false,
  "password": "optional_password"
}
```

**Response (Success - 201 Created):**
```json
{
  "room_id": "room_12345",
  "room_name": "My Party Voice Chat",
  "creator_id": "user_001",
  "max_participants": 10,
  "websocket_url": "ws://localhost:8000/ws/voice/room_12345"
}
```

---

## WebSocket Protocol

### Connection

**WebSocket URL:** `ws://localhost:8000/ws/voice/{room_id}`

**Connection Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `room_id` | string | Yes | Voice room ID (from create/join room) |
| `token` | string | Yes | JWT access token (query param or header) |

**Connection Example:**
```
ws://localhost:8000/ws/voice/room_12345?token=eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Connection Handshake

**Client → Server (Connect):**
```json
{
  "type": "join",
  "user_id": "user_001",
  "username": "Alice",
  "audio_config": {
    "sample_rate": 48000,
    "encoding": "opus",
    "channels": 1
  }
}
```

**Server → Client (Welcome):**
```json
{
  "type": "welcome",
  "room_id": "room_12345",
  "your_user_id": "user_001",
  "participants": [
    {"user_id": "user_002", "username": "Bob"}
  ]
}
```

---

### Message Types

#### 1. Audio Packet (Client → Server)

**Description:** Send audio data to server for distribution

**Message Format:**
```json
{
  "type": "audio",
  "user_id": "user_001",
  "sequence_number": 1234,
  "timestamp": 1705089600000,
  "audio_data": "<Base64-encoded audio>",
  "encoding": "opus",
  "sample_rate": 48000,
  "contains_voice": true
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Always `"audio"` |
| `user_id` | string | Yes | Sender's user ID |
| `sequence_number` | integer | Yes | Packet sequence (for ordering) |
| `timestamp` | integer | Yes | Unix timestamp in milliseconds |
| `audio_data` | string | Yes | Base64-encoded audio chunk |
| `encoding` | string | Yes | Audio encoding (`opus`, `pcm16`) |
| `sample_rate` | integer | Yes | Sample rate in Hz |
| `contains_voice` | boolean | Yes | VAD result (true if voice detected) |

**UE5 C++ Example:**
```cpp
void UNajikaVoiceComponent::SendAudioPacket(const FNajikaAudioPacket& Packet)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject());
    JsonObject->SetStringField(TEXT("type"), TEXT("audio"));
    JsonObject->SetStringField(TEXT("user_id"), UserID);
    JsonObject->SetNumberField(TEXT("sequence_number"), Packet.SequenceNumber);
    JsonObject->SetNumberField(TEXT("timestamp"), Packet.Timestamp);
    JsonObject->SetStringField(TEXT("audio_data"), FBase64::Encode(Packet.AudioData));
    JsonObject->SetStringField(TEXT("encoding"), TEXT("opus"));
    JsonObject->SetNumberField(TEXT("sample_rate"), Packet.SampleRate);
    JsonObject->SetBoolField(TEXT("contains_voice"), Packet.bContainsVoice);

    FString JsonString = SerializeJson(JsonObject);
    WebSocket->Send(JsonString);
}
```

---

#### 2. Audio Packet (Server → Client)

**Description:** Receive audio from other participants

**Message Format:**
```json
{
  "type": "audio",
  "from_user_id": "user_002",
  "from_username": "Bob",
  "sequence_number": 5678,
  "timestamp": 1705089600100,
  "audio_data": "<Base64-encoded audio>",
  "encoding": "opus",
  "sample_rate": 48000
}
```

**UE5 C++ Example (Receive & Playback):**
```cpp
void UNajikaVoiceComponent::OnWebSocketMessage(const FString& Message)
{
    TSharedPtr<FJsonObject> JsonObject = ParseJson(Message);

    FString Type = JsonObject->GetStringField(TEXT("type"));

    if (Type == TEXT("audio"))
    {
        FString FromUserID = JsonObject->GetStringField(TEXT("from_user_id"));
        FString AudioDataBase64 = JsonObject->GetStringField(TEXT("audio_data"));
        int32 SampleRate = JsonObject->GetIntegerField(TEXT("sample_rate"));

        // Decode Base64
        TArray<uint8> AudioData;
        FBase64::Decode(AudioDataBase64, AudioData);

        // Play audio
        VoicePlayback->PlayAudioChunk(AudioData, SampleRate);
    }
}
```

---

#### 3. User Joined

**Description:** Notification when a user joins the room

**Server → Client:**
```json
{
  "type": "user_joined",
  "user_id": "user_003",
  "username": "Charlie",
  "joined_at": "2025-01-13T10:35:00Z"
}
```

---

#### 4. User Left

**Description:** Notification when a user leaves the room

**Server → Client:**
```json
{
  "type": "user_left",
  "user_id": "user_003",
  "username": "Charlie",
  "reason": "disconnect",
  "left_at": "2025-01-13T10:40:00Z"
}
```

---

#### 5. Mute/Unmute

**Description:** Mute or unmute a participant (server-side)

**Client → Server:**
```json
{
  "type": "set_mute",
  "user_id": "user_001",
  "is_muted": true
}
```

**Server → All Clients:**
```json
{
  "type": "user_muted",
  "user_id": "user_001",
  "is_muted": true
}
```

---

#### 6. Speaking Status

**Description:** Notify when a user starts/stops speaking (VAD)

**Server → All Clients:**
```json
{
  "type": "speaking_status",
  "user_id": "user_002",
  "is_speaking": true
}
```

---

#### 7. Ping/Pong (Heartbeat)

**Description:** Keep connection alive

**Client → Server (every 30 seconds):**
```json
{
  "type": "ping"
}
```

**Server → Client:**
```json
{
  "type": "pong",
  "server_time": 1705089600000
}
```

---

### Disconnection

**Client Disconnect (Graceful):**
```json
{
  "type": "leave",
  "user_id": "user_001"
}
```

**Server Response:**
```json
{
  "type": "goodbye",
  "message": "You have left the voice room"
}
```

**Server closes WebSocket with code `1000` (Normal Closure).**

---

## Data Formats

### Audio Encoding

**Supported Encodings:**

| Encoding | Bitrate | Sample Rate | Use Case |
|----------|---------|-------------|----------|
| **Opus** | 24-32 kbps | 48000 Hz | Recommended for production (best quality/bandwidth) |
| **PCM16** | ~1536 kbps | 48000 Hz | Development/testing (uncompressed) |

**Opus Encoding Parameters:**
- **Bitrate:** 24000 bps (adjustable 16k-32k)
- **Frame Size:** 960 samples (20ms at 48kHz)
- **Channels:** 1 (mono)
- **Complexity:** 5 (balance quality/CPU)

### Audio Chunk Size

**Recommended chunk size:** 960 samples (20ms at 48kHz)

**Calculation:**
```
Chunk Duration = 20ms
Sample Rate = 48000 Hz
Samples per Chunk = 48000 * 0.02 = 960 samples
```

**PCM16 Data Size:**
```
960 samples × 2 bytes (16-bit) = 1920 bytes per chunk
```

**Opus Compressed Size:**
```
~60-80 bytes per chunk (variable)
```

---

## Error Handling

### HTTP Error Codes

| Code | Error | Description |
|------|-------|-------------|
| `400` | Bad Request | Invalid request format or parameters |
| `401` | Unauthorized | Missing or invalid authentication token |
| `403` | Forbidden | User lacks permission for this resource |
| `404` | Not Found | Room or resource does not exist |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server-side processing error |

### WebSocket Error Codes

| Code | Error | Description |
|------|-------|-------------|
| `1000` | Normal Closure | Clean disconnect |
| `1001` | Going Away | Server shutting down |
| `1002` | Protocol Error | Invalid message format |
| `1003` | Unsupported Data | Unsupported audio encoding |
| `1008` | Policy Violation | Violation of server rules (spam, abuse) |
| `1011` | Internal Error | Server-side error |

### Error Response Format

**HTTP Error Response:**
```json
{
  "error": "Error Name",
  "message": "Detailed error message",
  "status": 400,
  "timestamp": "2025-01-13T10:30:00Z",
  "details": {
    "field": "audio_data",
    "reason": "Invalid Base64 encoding"
  }
}
```

**WebSocket Error Message:**
```json
{
  "type": "error",
  "error_code": "INVALID_FORMAT",
  "message": "Audio packet missing required field: sequence_number",
  "severity": "warning"
}
```

---

## Rate Limiting

### HTTP Endpoints

| Endpoint | Rate Limit | Window |
|----------|------------|--------|
| `/api/voice/transcribe` | 10 requests | 1 minute |
| `/api/voice/rooms` (GET) | 30 requests | 1 minute |
| `/api/voice/rooms` (POST) | 5 requests | 1 minute |

**Rate Limit Exceeded Response (429):**
```json
{
  "error": "Rate Limit Exceeded",
  "message": "You have exceeded the rate limit for this endpoint",
  "status": 429,
  "retry_after": 60
}
```

### WebSocket

**Audio Packet Rate Limit:**
- Maximum: 50 packets/second (for 20ms chunks, this is normal)
- Burst: 100 packets/second (temporary spikes allowed)

**If exceeded, server sends warning:**
```json
{
  "type": "warning",
  "message": "Sending audio packets too fast. Throttling.",
  "recommended_rate": "50 packets/second"
}
```

---

## Implementation Examples

### Complete Voice Call Flow (UE5 Client)

#### 1. Create Voice Room

```cpp
// HTTP Request
UNajikaHttpClient* HttpClient = GetGameInstance()->GetSubsystem<UNajikaBackendSubsystem>()->GetHttpClient();

TSharedPtr<FJsonObject> Request = MakeShareable(new FJsonObject());
Request->SetStringField(TEXT("room_name"), TEXT("My Party"));
Request->SetNumberField(TEXT("max_participants"), 10);

HttpClient->SendRequest(TEXT("/api/voice/rooms"), Request, OnRoomCreated);
```

#### 2. Join Voice Room (WebSocket)

```cpp
// WebSocket Connection
void UNajikaVoiceComponent::JoinVoiceRoom(const FString& RoomID)
{
    FString WebSocketURL = FString::Printf(TEXT("ws://localhost:8000/ws/voice/%s?token=%s"), *RoomID, *AccessToken);

    WebSocket = FWebSocketsModule::Get().CreateWebSocket(WebSocketURL, TEXT("ws"));

    WebSocket->OnConnected().AddLambda([this]()
    {
        UE_LOG(LogNajikaVoice, Log, TEXT("WebSocket connected"));

        // Send join message
        TSharedPtr<FJsonObject> JoinMessage = MakeShareable(new FJsonObject());
        JoinMessage->SetStringField(TEXT("type"), TEXT("join"));
        JoinMessage->SetStringField(TEXT("user_id"), UserID);
        JoinMessage->SetStringField(TEXT("username"), Username);

        WebSocket->Send(SerializeJson(JoinMessage));
    });

    WebSocket->OnMessage().AddUObject(this, &UNajikaVoiceComponent::OnWebSocketMessage);
    WebSocket->Connect();
}
```

#### 3. Send Audio

```cpp
void UNajikaVoiceComponent::OnAudioPacketReady(const FNajikaAudioPacket& Packet)
{
    if (!WebSocket || !WebSocket->IsConnected())
        return;

    TSharedPtr<FJsonObject> AudioMessage = MakeShareable(new FJsonObject());
    AudioMessage->SetStringField(TEXT("type"), TEXT("audio"));
    AudioMessage->SetStringField(TEXT("user_id"), UserID);
    AudioMessage->SetNumberField(TEXT("sequence_number"), Packet.SequenceNumber);
    AudioMessage->SetNumberField(TEXT("timestamp"), FDateTime::UtcNow().ToUnixTimestamp() * 1000);
    AudioMessage->SetStringField(TEXT("audio_data"), FBase64::Encode(Packet.AudioData));
    AudioMessage->SetStringField(TEXT("encoding"), TEXT("opus"));
    AudioMessage->SetNumberField(TEXT("sample_rate"), 48000);
    AudioMessage->SetBoolField(TEXT("contains_voice"), Packet.bContainsVoice);

    WebSocket->Send(SerializeJson(AudioMessage));
}
```

#### 4. Receive Audio

```cpp
void UNajikaVoiceComponent::OnWebSocketMessage(const FString& Message)
{
    TSharedPtr<FJsonObject> JsonObject = ParseJson(Message);
    FString Type = JsonObject->GetStringField(TEXT("type"));

    if (Type == TEXT("audio"))
    {
        FString FromUserID = JsonObject->GetStringField(TEXT("from_user_id"));
        FString AudioDataBase64 = JsonObject->GetStringField(TEXT("audio_data"));
        int32 SequenceNumber = JsonObject->GetIntegerField(TEXT("sequence_number"));

        TArray<uint8> AudioData;
        FBase64::Decode(AudioDataBase64, AudioData);

        // Decode and play
        VoicePlayback->EnqueueAudioPacket(AudioData, SequenceNumber);
    }
    else if (Type == TEXT("user_joined"))
    {
        FString Username = JsonObject->GetStringField(TEXT("username"));
        UE_LOG(LogNajikaVoice, Log, TEXT("User joined: %s"), *Username);
    }
}
```

---

## Backend Implementation Notes

### Technology Stack (Recommended)

- **Framework:** FastAPI (Python) or Node.js (Express + Socket.io)
- **WebSocket:** Socket.io or native WebSocket
- **Whisper AI:** OpenAI Whisper (whisper-cpp for C++ backend, or openai-whisper for Python)
- **Audio Processing:** FFmpeg or libopus

### Voice Room Management

**Room State (In-Memory or Redis):**
```python
# Example Python structure
voice_rooms = {
    "room_12345": {
        "room_id": "room_12345",
        "room_name": "Party Chat",
        "participants": {
            "user_001": {
                "user_id": "user_001",
                "username": "Alice",
                "websocket": <WebSocket object>,
                "is_muted": False,
                "is_speaking": False
            },
            "user_002": { ... }
        },
        "created_at": "2025-01-13T10:30:00Z"
    }
}
```

### Audio Forwarding Logic

```python
# Pseudo-code
async def handle_audio_packet(room_id, from_user_id, audio_packet):
    room = voice_rooms[room_id]

    # Broadcast to all participants except sender
    for user_id, participant in room["participants"].items():
        if user_id != from_user_id and not participant["is_muted"]:
            await participant["websocket"].send_json({
                "type": "audio",
                "from_user_id": from_user_id,
                "from_username": room["participants"][from_user_id]["username"],
                **audio_packet
            })
```

---

## Security Considerations

### 1. Audio Data Validation

- **Size Limit:** Reject packets > 10 KB (prevents DoS)
- **Rate Limiting:** Max 50 packets/second per user
- **Format Validation:** Verify Base64 encoding and audio format

### 2. Room Access Control

- **Private Rooms:** Require password or invitation
- **Max Participants:** Enforce room capacity limits
- **User Verification:** Verify JWT token for each WebSocket message

### 3. Content Moderation

- **Transcription Logging:** Store transcriptions for moderation
- **Abuse Detection:** Flag users sending excessive/spam audio
- **Mute/Ban:** Allow room moderators to mute/kick users

---

## Summary

This API provides:

- ✅ **Real-time voice chat** via WebSocket with audio packet streaming
- ✅ **Speech-to-text** via HTTP REST using Whisper AI
- ✅ **Multi-user voice rooms** with participant management
- ✅ **Flexible audio encoding** (Opus, PCM16)
- ✅ **Comprehensive error handling** and rate limiting

**For full implementation, refer to:**
- `NajikaVoiceSystem` plugin (UE5_Implementation/Plugins/NajikaVoiceSystem/)
- `TESTING_CHECKLIST.md` (Integration tests for voice system)

---

**End of Voice Backend API Specification**

*This specification is part of the Najika UE5 Implementation documentation suite.*
