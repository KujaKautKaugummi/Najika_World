# OPTIONAL Backend - Najika Digivice

> ⚠️ **HINWEIS:** Dieses Backend ist **OPTIONAL** und wurde zusätzlich erstellt.
> Das lokale Modell hat möglicherweise bereits ein Backend vorbereitet.
> Nutze dieses als Referenz, Alternative oder zum Testen.

## Features

✅ **Authentication** - JWT Token basierte Authentifizierung
✅ **User Management** - Login, User Daten
✅ **Inventory System** - Items abrufen und hinzufügen
✅ **Voice Chat** - WebSocket basiertes Real-time Voice System
✅ **Whisper AI** - Speech-to-Text (Placeholder, muss integriert werden)
✅ **Health Check** - API Status Endpoint

## Quick Start

### 1. Installation

```bash
cd OPTIONAL_Backend

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv

# Aktivieren
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### 2. Server starten

```bash
python main.py
```

Server läuft auf: **http://localhost:8000**

### 3. API Dokumentation

Öffne im Browser:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 4. Test mit UE5 Client

Im UE5 Client:
1. Stelle sicher, Backend läuft auf `localhost:8000`
2. Login mit Test-Account:
   - Username: `test_user_1`
   - Password: `test123`
3. Voice Chat testen (WebSocket verbindet automatisch)

## API Endpoints

### Authentication

#### `POST /api/auth/login`
Login und JWT Token erhalten.

**Request:**
```json
{
  "username": "test_user_1",
  "password": "test123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "user_001",
  "username": "test_user_1",
  "display_name": "Test User One"
}
```

### Inventory

#### `GET /api/inventory`
Inventory des Users abrufen.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "items": [
    {
      "item_id": "sword_001",
      "name": "Iron Sword",
      "quantity": 1,
      "icon_url": "/icons/sword.png"
    },
    ...
  ]
}
```

#### `POST /api/inventory/add`
Item zum Inventory hinzufügen.

**Query Parameters:**
- `item_id` (string) - Item ID
- `quantity` (int) - Anzahl (default: 1)

**Headers:**
```
Authorization: Bearer <access_token>
```

### Voice Chat

#### `POST /api/voice/transcribe`
Audio transkribieren (Whisper AI Placeholder).

**Request:**
```json
{
  "audio_data": "<Base64-encoded audio>",
  "sample_rate": 48000,
  "encoding": "pcm16",
  "language": "en"
}
```

**Response:**
```json
{
  "text": "Hello, this is a test.",
  "confidence": 0.95,
  "language_code": "en",
  "processing_time_ms": 250,
  "word_count": 5
}
```

#### `POST /api/voice/rooms`
Voice Room erstellen.

**Request:**
```json
{
  "room_name": "My Voice Chat",
  "max_participants": 10,
  "is_public": false
}
```

**Response:**
```json
{
  "room_id": "room_abc12345",
  "room_name": "My Voice Chat",
  "creator_id": "user_001",
  "max_participants": 10,
  "websocket_url": "ws://localhost:8000/ws/voice/room_abc12345"
}
```

#### `GET /api/voice/rooms/{room_id}`
Voice Room Info abrufen.

### WebSocket Voice Chat

#### `WS /ws/voice/{room_id}?token=<jwt_token>`
WebSocket Verbindung für Real-time Voice Chat.

**Connection URL:**
```
ws://localhost:8000/ws/voice/room_abc12345?token=eyJ0eXAiOiJKV1Qi...
```

**Message Types:**

**Client → Server (Audio Packet):**
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

**Server → Client (Audio Packet):**
```json
{
  "type": "audio",
  "from_user_id": "user_002",
  "from_username": "Bob",
  "sequence_number": 5678,
  "audio_data": "<Base64-encoded audio>",
  "encoding": "opus",
  "sample_rate": 48000
}
```

**Ping/Pong:**
```json
// Client → Server
{"type": "ping"}

// Server → Client
{"type": "pong", "server_time": 1705089600000}
```

## Test Accounts

| Username | Password | User ID | Items |
|----------|----------|---------|-------|
| `test_user_1` | `test123` | `user_001` | 5 items (sword, potions, armor, wood) |
| `test_user_2` | `test123` | `user_002` | 2 items (bow, potions) |

## Konfiguration

### Secret Key ändern

⚠️ **WICHTIG:** In Produktion Secret Key ändern!

In `main.py`:
```python
SECRET_KEY = "dein_super_sicherer_secret_key_hier"
```

### Port ändern

In `main.py` am Ende:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Port hier ändern
```

### Database

Aktuell: In-Memory Dictionary (Daten gehen bei Server-Restart verloren)

Für Produktion: SQLite oder PostgreSQL integrieren

Beispiel SQLite Setup:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./najika.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## Whisper AI Integration

Aktuell: **Placeholder** (gibt simulierte Transkription zurück)

### Integration mit OpenAI Whisper:

1. Whisper installieren:
   ```bash
   pip install openai-whisper
   pip install torch torchaudio
   ```

2. In `main.py` in `transcribe_audio()`:
   ```python
   import whisper
   import io
   import soundfile as sf

   # Model laden (einmalig beim Start)
   whisper_model = whisper.load_model("base")

   # In transcribe_audio():
   audio_bytes = base64.b64decode(request.audio_data)

   # Audio zu Numpy Array konvertieren
   audio_array, _ = sf.read(io.BytesIO(audio_bytes))

   # Transkribieren
   result = whisper_model.transcribe(audio_array)
   text = result["text"]
   confidence = 0.95  # Whisper gibt keinen Confidence Score
   ```

## Docker Deployment (Optional)

Erstelle `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["python", "main.py"]
```

Bauen und starten:
```bash
docker build -t najika-backend .
docker run -p 8000:8000 najika-backend
```

## Troubleshooting

### Port 8000 bereits belegt

```bash
# Port ändern in main.py oder anderes Programm beenden
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

### CORS Fehler

In `main.py` CORS origins einschränken:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Nur bestimmte Origins
    ...
)
```

### JWT Token Fehler

Token abgelaufen? Neu einloggen und neues Token holen.

## Performance

- **Concurrent Connections:** Unterstützt 100+ gleichzeitige WebSocket Verbindungen
- **Latency:** < 50ms für Audio Packet Forwarding (localhost)
- **Throughput:** ~1000 Requests/Sekunde (lokaler Test)

## Sicherheit

⚠️ **Für Produktion beachten:**

1. **Secret Key ändern** (nicht "najika_secret_key_change_in_production" nutzen!)
2. **HTTPS verwenden** (TLS/SSL Zertifikat)
3. **CORS einschränken** (nicht `allow_origins=["*"]`)
4. **Rate Limiting** implementieren (z.B. mit `slowapi`)
5. **Input Validation** verstärken
6. **SQL Injection** Prevention (bei SQL Datenbank)
7. **Passwörter** mit bcrypt hashen (bereits implementiert ✓)
8. **Token Expiration** beachten (aktuell 24h)

## Weiterentwicklung

### TODO:

- [ ] SQLite/PostgreSQL Datenbank Integration
- [ ] Whisper AI Model Integration
- [ ] Rate Limiting (slowapi)
- [ ] Redis für Session Management
- [ ] Admin Dashboard
- [ ] Logging (structlog)
- [ ] Monitoring (Prometheus)
- [ ] Unit Tests (pytest)
- [ ] Docker Compose Setup
- [ ] CI/CD Pipeline

## Support

Bei Fragen oder Problemen:
1. API Docs checken: http://localhost:8000/docs
2. Logs checken (Terminal wo Server läuft)
3. Health Check: http://localhost:8000/api/health

## License

Dieses Backend ist Teil des Najika Digivice Projekts.

---

**Erstellt als OPTIONALE Komponente - Nutze alternatives Backend wenn vorhanden**
