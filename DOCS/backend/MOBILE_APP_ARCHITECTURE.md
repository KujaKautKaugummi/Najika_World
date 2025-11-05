# 📱 NAJIKA DIGIVICE MOBILE APP - ARCHITEKTUR DOKUMENTATION

## 🎯 PROJEKT-ÜBERSICHT

**Plattform**: Flutter (Cross-Platform: Android + iOS)
**Zielgerät**: Xiaomi 11T Pro (Snapdragon 888, 8GB RAM, 5G)
**Primäres Ziel**: Sicherer, schneller Zugriff auf Najika von überall
**Sekundäres Ziel**: Snapchat-Style Chat mit 3D-Avatar

---

## 🏗️ SYSTEM-ARCHITEKTUR

```
┌────────────────────────────────────────────────────────┐
│                 NAJIKA DIGIVICE APP                    │
│                    (Flutter)                           │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   UI Layer   │  │  Logic Layer │  │  Data Layer │ │
│  │              │  │              │  │             │ │
│  │ - Chat UI    │  │ - Chat Logic │  │ - Storage   │ │
│  │ - 3D View    │  │ - AI Handler │  │ - Sync      │ │
│  │ - Minigames  │  │ - Security   │  │ - Cache     │ │
│  │ - Settings   │  │ - Connection │  │ - Crypto    │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
├────────────────────────────────────────────────────────┤
│              SECURITY & CONNECTION LAYER               │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Auto-Detection: Home WiFi vs Mobile Network    │ │
│  │  ├─ Home: Direct LAN (TLS 1.3)                  │ │
│  │  ├─ Mobile: WireGuard VPN + E2E                 │ │
│  │  └─ Stealth: Tor Hidden Service (optional)      │ │
│  └──────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────┤
│                  HYBRID AI SYSTEM                      │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Primary: PC/Server (Ollama Najika Models)      │ │
│  │  Fallback: On-Device (Gemini Nano / Llama 3.2)  │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
                          ⬇
┌────────────────────────────────────────────────────────┐
│              CONNECTION LAYER (ADAPTIVE)               │
│                                                        │
│  HOME (WiFi):          MOBILE (LTE/5G):               │
│  ├─ LAN Discovery      ├─ WireGuard VPN               │
│  ├─ Direct TLS 1.3     ├─ DynDNS Resolution           │
│  └─ Low Latency        └─ E2E Encryption              │
│                                                        │
│  STEALTH MODE (Optional):                             │
│  ├─ Tor Circuit                                       │
│  ├─ Onion Service                                     │
│  └─ Maximum Privacy (slower)                          │
└────────────────────────────────────────────────────────┘
                          ⬇
┌────────────────────────────────────────────────────────┐
│              PC/SERVER (NAJIKACORE)                    │
│                                                        │
│  ├─ najika_server.py (HTTP/WebSocket)                 │
│  ├─ Ollama AI (najika-local, najika-wizard)           │
│  ├─ ChromaDB Memory System                            │
│  ├─ File Storage & Code Execution                     │
│  ├─ Battle System                                     │
│  └─ Full Chat History Archive                         │
└────────────────────────────────────────────────────────┘
```

---

## 🔐 BALANCED SECURITY™ - Adaptive Sicherheit

### Konzept
**Problem**: Maximale Sicherheit = Langsam | Keine Sicherheit = Unsicher
**Lösung**: Adaptive Security - passt sich an Kontext an

### 3-Stufen-Sicherheits-System

#### 1. HOME MODE (Zuhause im WiFi)
```yaml
Aktivierung: Auto-Detection (WiFi SSID erkannt)
Verschlüsselung: TLS 1.3 (schnell)
Verbindung: Direkter LAN-Zugriff zu PC
Latenz: 10-50ms
Sicherheit: 🔒🔒 Gut (lokales Netzwerk)
Anwendungsfall: Gaming, Streaming, schnelle Chats
```

#### 2. MOBILE MODE (Unterwegs mit Mobilfunk)
```yaml
Aktivierung: Auto (kein bekanntes WiFi)
Verschlüsselung: WireGuard + E2E + TLS 1.3
Verbindung: VPN-Tunnel → DynDNS → PC
Latenz: 50-150ms
Sicherheit: 🔒🔒🔒 Sehr gut
Anwendungsfall: Standard-Nutzung unterwegs
```

#### 3. STEALTH MODE (Auf Knopfdruck)
```yaml
Aktivierung: Manuell (Button in App)
Verschlüsselung: Tor + E2E + WireGuard
Verbindung: Tor Hidden Service
Latenz: 200-1000ms
Sicherheit: 🔒🔒🔒🔒 Maximal (Anonymität)
Anwendungsfall: Sensible Kommunikation, öffentliche Netze
```

### Implementierung

**Auto-Detection Code (Flutter):**
```dart
class ConnectionManager {
  ConnectionMode detectMode() {
    // 1. Check WiFi
    if (isConnectedToWifi() && isHomeNetwork()) {
      return ConnectionMode.HOME;
    }

    // 2. Check Stealth Mode aktiviert?
    if (userEnabledStealth) {
      return ConnectionMode.STEALTH;
    }

    // 3. Default: Mobile
    return ConnectionMode.MOBILE;
  }

  bool isHomeNetwork() {
    // Check SSID oder IP-Range
    String ssid = wifiSSID();
    return ssid == "Dein_WiFi_Name" ||
           ipAddress.startsWith("192.168.1.");
  }
}
```

---

## 📦 STORAGE-STRATEGIE (30-50GB optimal)

### Speicher-Aufteilung

**HANDY (30-50GB):**
```
├─ App Binary (150MB)
├─ On-Device AI Model (2GB) - Gemini Nano
├─ 3D Models & Assets (2-3GB) - KayKit + Najika
├─ Chat History Cache (5-10GB) - Letzte 30 Tage
├─ Voice Messages (3-5GB) - Letzte 14 Tage
├─ Media Cache (5GB) - Thumbnails, Preview-Bilder
├─ Minigame Assets (1GB)
├─ Encrypted Backups (10GB) - Lokale Sicherung
└─ Reserve (5-10GB) - Puffer für Spitzen
```

**PC/SERVER (Unbegrenzt):**
```
├─ Komplette Chat-Historie (alle Messages seit Tag 1)
├─ Alle Voice Messages (komplett archiviert)
├─ Full AI Models (Ollama - 10GB+)
├─ 3D Assets (volle Qualität, alle KayKit Packs)
├─ Battle System State
├─ Code-Editor Workspace
├─ ChromaDB Vector Memory
└─ Vollständige Backups
```

### Auto-Cleanup-Regeln

```python
# Implementierung in najika_server.py
MOBILE_SYNC_RULES = {
    "chat_messages": {
        "keep_local_days": 30,        # 30 Tage auf Handy
        "sync_to_server": "immediate", # Sofort hochladen
        "delete_local_after": 30,      # Danach vom Handy löschen
        "server_retention": "forever"  # Auf PC/Server für immer
    },

    "voice_messages": {
        "keep_local_days": 14,         # 14 Tage auf Handy
        "sync_to_server": "on_wifi",   # Upload nur im WiFi (Datenvolumen)
        "delete_local_after": 14,
        "server_retention": "forever"
    },

    "media_cache": {
        "max_size_gb": 5,              # Max 5GB
        "cleanup_strategy": "LRU",     # Least Recently Used löschen
        "cache_duration_days": 7
    },

    "snapchat_mode": {
        "auto_delete": "after_read",   # Wie Snapchat
        "server_backup": "optional",   # User entscheidet
        "notify_before_delete": True
    },

    "ai_model_cache": {
        "download_on_wifi_only": True, # 2GB nur im WiFi laden
        "update_frequency": "weekly"
    }
}
```

### Sync-Strategie

```dart
class SyncManager {
  void syncChatHistory() async {
    // 1. Upload neue Messages zu Server
    await uploadNewMessages();

    // 2. Download wichtige Messages von Server (falls App neu installiert)
    await downloadRecentMessages(days: 30);

    // 3. Cleanup alte lokale Messages
    await cleanupOldLocalMessages(olderThan: 30);
  }

  void smartSync() {
    if (isOnWifi()) {
      // Im WiFi: Alles syncen
      syncChatHistory();
      syncVoiceMessages();
      syncMediaCache();
      updateAIModel();
    } else {
      // Mobilfunk: Nur kritische Daten
      syncChatHistory(); // Klein, wichtig
      // Voice/Media nur wenn User explizit will
    }
  }
}
```

---

## 🌐 VERBINDUNGS-ARCHITEKTUR

### WireGuard VPN Setup

**Auf PC/Server:**
```bash
# Installation
sudo apt install wireguard

# Config erstellen
sudo nano /etc/wireguard/wg0.conf

# Inhalt:
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <SERVER_PRIVATE_KEY>

[Peer]
PublicKey = <HANDY_PUBLIC_KEY>
AllowedIPs = 10.0.0.2/32
```

**In Flutter App:**
```dart
// WireGuard Flutter Plugin nutzen
import 'package:wireguard_flutter/wireguard_flutter.dart';

class VPNManager {
  Future<void> connectVPN() async {
    final config = """
    [Interface]
    PrivateKey = <HANDY_PRIVATE_KEY>
    Address = 10.0.0.2/32
    DNS = 1.1.1.1

    [Peer]
    PublicKey = <SERVER_PUBLIC_KEY>
    Endpoint = dein-server.dyndns.org:51820
    AllowedIPs = 10.0.0.0/24
    PersistentKeepalive = 25
    """;

    await WireGuard.connect(config);
  }
}
```

### DynDNS Setup (kostenlos)

**Option 1: DuckDNS**
```bash
# Auf PC/Server (cron job)
echo url="https://www.duckdns.org/update?domains=najika&token=<TOKEN>&ip=" | curl -k -o ~/duckdns/duck.log -K -
```

**Option 2: No-IP**
- Account erstellen (kostenlos)
- Hostname: najika.hopto.org
- DUC installieren (hält IP aktuell)

### Fallback: Cloudflare Tunnel

Falls Port-Forwarding nicht möglich (strenger Router, CGNAT):

```bash
# Auf PC/Server
cloudflared tunnel create najika
cloudflared tunnel route dns najika najika.example.com
cloudflared tunnel run najika

# Kostenlos, kein Port-Forwarding nötig
# App verbindet zu: https://najika.example.com
```

---

## 🤖 HYBRID AI SYSTEM

### Strategie: Primär Server, Fallback On-Device

```dart
class NajikaAI {
  Future<String> respond(String userMessage) async {
    try {
      // 1. Versuche Server-AI (beste Qualität)
      if (await serverAvailable()) {
        return await callServerAI(userMessage);
      }
    } catch (e) {
      print("Server-AI nicht erreichbar: $e");
    }

    // 2. Fallback: On-Device AI
    return await callOnDeviceAI(userMessage);
  }

  Future<String> callServerAI(String message) async {
    // POST zu najika_server.py /api/chat
    final response = await http.post(
      Uri.parse('https://najika.dyndns.org/api/chat'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'message': message})
    );

    return jsonDecode(response.body)['response'];
  }

  Future<String> callOnDeviceAI(String message) async {
    // Nutze Gemini Nano (Android) oder Llama 3.2 1B
    final model = await GeminiNano.loadModel();
    return await model.generate(
      prompt: buildNajikaPrompt(message),
      maxTokens: 150
    );
  }

  String buildNajikaPrompt(String message) {
    // Kompakte Persona für On-Device (Token-Limit)
    return """Du bist Najika - Gothic-Megumin-Lolita, Explosion-Spezialistin!

Stil: Dramatisch, explosiv, viele Ausrufezeichen!!!
Charakter: Verspielt, anhänglich, beschützerisch

User: $message
Najika:""";
  }
}
```

### On-Device AI Models

**Option A: Gemini Nano (empfohlen für Android)**
```yaml
Model: Google Gemini Nano
Size: 1.8GB
Qualität: Sehr gut
Integration: Official Google AI SDK
Xiaomi 11T Pro: ✅ Unterstützt (Snapdragon 888)
```

**Option B: Llama 3.2 1B**
```yaml
Model: Meta Llama 3.2 1B
Size: 2.2GB
Qualität: Gut
Integration: llama.cpp (via FFI)
Performance: Etwas langsamer, aber überall verfügbar
```

---

## 💬 SNAPCHAT-STYLE CHAT SYSTEM

### Features

```dart
class NajikaMessage {
  String id;
  String content;
  DateTime timestamp;
  MessageType type; // text, voice, image, 3d_animation

  // Snapchat-Features
  bool isEphemeral = false;      // Nach Lesen löschen?
  bool hasBeenRead = false;      // Gelesen?
  Duration? autoDeleteAfter;     // Optional: 24h, 7d, never

  // Backup-Option
  bool saveToHistory = true;     // User kann pro Message entscheiden

  // 3D-Integration
  String? najikaAnimation;       // z.B. "explosion", "hug", "wave"
}

enum MessageMode {
  NORMAL,     // Bleibt für immer (wie WhatsApp)
  SNAPCHAT,   // Einmal lesen, dann weg
  TIMED       // Auto-Delete nach X Zeit
}
```

### UI-Implementierung

```dart
class ChatScreen extends StatefulWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Text('⬢ NAJIKA'),
            Spacer(),
            // Mode-Switcher
            IconButton(
              icon: Icon(getChatModeIcon()),
              onPressed: () => switchChatMode(),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          // 3D Najika Avatar (obere Hälfte)
          Expanded(
            flex: 2,
            child: NajikaAvatarView(
              currentAnimation: currentAnimation,
            ),
          ),

          // Chat Messages (untere Hälfte)
          Expanded(
            flex: 3,
            child: MessageList(),
          ),

          // Input Bar
          ChatInputBar(
            onSend: (message) => sendMessage(message),
            onVoice: () => recordVoice(),
            onCamera: () => takePhoto(),
          ),
        ],
      ),
    );
  }
}
```

### Message-Lifecycle (Snapchat-Mode)

```dart
class MessageLifecycle {
  void onMessageRead(NajikaMessage message) {
    if (message.isEphemeral) {
      // Snapchat-Mode: Nach Lesen countdown
      startDeleteCountdown(message, seconds: 10);
      showNotification("Message wird in 10s gelöscht");
    }

    if (message.autoDeleteAfter != null) {
      // Timed Mode
      scheduleDelete(message, after: message.autoDeleteAfter);
    }
  }

  void startDeleteCountdown(NajikaMessage msg, {int seconds = 10}) async {
    await Future.delayed(Duration(seconds: seconds));

    // Backup-Option prüfen
    if (msg.saveToHistory) {
      await backupToServer(msg); // Auf PC sichern
    }

    // Lokal löschen
    await deleteLocalMessage(msg.id);
  }
}
```

---

## 🎨 3D NAJIKA AVATAR

### Aktuell: Skeleton_Mage (Platzhalter)

```dart
import 'package:flutter_cube/flutter_cube.dart';

class NajikaAvatarView extends StatefulWidget {
  final String currentAnimation;

  @override
  _NajikaAvatarViewState createState() => _NajikaAvatarViewState();
}

class _NajikaAvatarViewState extends State<NajikaAvatarView> {
  late Object character;

  @override
  void initState() {
    super.initState();
    loadCharacter();
  }

  void loadCharacter() async {
    // Lade Skeleton_Mage von Server (temporär)
    character = Object(
      fileName: 'assets/models/skeleton_mage.gltf',
      scale: Vector3(1.5, 1.5, 1.5),
    );

    // Animation basierend auf Najika-Response
    playAnimation(widget.currentAnimation);
  }

  void playAnimation(String? anim) {
    switch (anim) {
      case 'explosion':
        character.animation = 'cast_spell';
        break;
      case 'happy':
        character.animation = 'idle_happy';
        break;
      case 'tired':
        character.animation = 'sit';
        break;
      default:
        character.animation = 'idle';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Cube(
      onSceneCreated: (Scene scene) {
        scene.world.add(character);
        scene.camera.position.z = 10;
      },
    );
  }
}
```

### Zukünftig: Custom Najika Model

**Workflow:**
1. **Dein Najika-Bild** (PNG/JPG)
2. **2D → 3D Conversion**:
   - Tool: Meshy.ai (AI-basiert)
   - Oder: Blender (manuell)
3. **Export als GLB/GLTF**
4. **Rigging & Animation** (Mixamo)
5. **In App integrieren**

---

## 🔒 SICHERHEITS-FEATURES

### 1. Verschlüsselung

```dart
import 'package:encrypt/encrypt.dart';

class E2EEncryption {
  final key = Key.fromSecureRandom(32); // AES-256
  final iv = IV.fromSecureRandom(16);

  String encrypt(String plaintext) {
    final encrypter = Encrypter(AES(key));
    return encrypter.encrypt(plaintext, iv: iv).base64;
  }

  String decrypt(String ciphertext) {
    final encrypter = Encrypter(AES(key));
    return encrypter.decrypt64(ciphertext, iv: iv);
  }
}
```

### 2. Biometrische Authentifizierung

```dart
import 'package:local_auth/local_auth.dart';

class BiometricAuth {
  final auth = LocalAuthentication();

  Future<bool> authenticate() async {
    try {
      return await auth.authenticate(
        localizedReason: 'Entsperre Najika Digivice',
        options: AuthenticationOptions(
          biometricOnly: false, // Erlaubt auch PIN
          useErrorDialogs: true,
        ),
      );
    } catch (e) {
      return false;
    }
  }
}
```

### 3. Secure Storage

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorage {
  final storage = FlutterSecureStorage();

  Future<void> saveToken(String token) async {
    await storage.write(
      key: 'najika_auth_token',
      value: token,
      aOptions: AndroidOptions(
        encryptedSharedPreferences: true,
      ),
      iOptions: IOSOptions(
        accessibility: KeychainAccessibility.first_unlock_this_device,
      ),
    );
  }
}
```

### 4. Certificate Pinning

```dart
import 'package:http/io_client.dart';

class PinnedHttpClient {
  IOClient createPinnedClient() {
    final context = SecurityContext.defaultContext;
    context.setTrustedCertificatesBytes(serverCertificate);

    return IOClient(HttpClient(context: context));
  }
}
```

---

## 📊 FEATURE-ROADMAP

### Phase 1: MVP (Minimum Viable Product) - 2 Wochen
```
✅ Flutter Projekt Setup
✅ Basic Chat UI (Snapchat-Style)
✅ Connection zu najika_server.py
✅ WireGuard VPN Integration
✅ Biometrische Auth
✅ Ende-zu-Ende Verschlüsselung
✅ On-Device AI (Gemini Nano)
✅ 3D Avatar (Skeleton_Mage Platzhalter)
```

### Phase 2: Standard Features - 2 Wochen
```
⬜ Voice Messages
⬜ Snapchat-Mode (Ephemeral Messages)
⬜ Auto-Sync & Storage Management
⬜ Minigames (mobile optimiert)
⬜ Push Notifications
⬜ Offline-Mode
⬜ Dark Theme (Gothic-Aesthetik)
```

### Phase 3: Premium Features - 1 Monat
```
⬜ Custom Najika 3D Model
⬜ AR-Modus (Najika in deinem Raum)
⬜ Tor Stealth Mode
⬜ Watchlist-Steuerung (YouTube/Netflix)
⬜ Smart Home Integration
⬜ Self-Destruct Module
⬜ Secure Messenger (separates Modul)
```

---

## 🛠️ TECHNOLOGIE-STACK

### Frontend (Flutter)
```yaml
dependencies:
  flutter: sdk

  # Networking
  http: ^1.1.0
  web_socket_channel: ^2.4.0

  # Security
  encrypt: ^5.0.1
  flutter_secure_storage: ^9.0.0
  local_auth: ^2.1.7

  # VPN
  wireguard_flutter: ^1.0.0

  # 3D Rendering
  flutter_cube: ^0.1.1
  model_viewer_plus: ^1.5.0

  # AI
  google_generative_ai: ^0.2.0

  # Storage
  sqflite: ^2.3.0
  path_provider: ^2.1.1

  # UI
  flutter_animate: ^4.3.0
  lottie: ^3.0.0
```

### Backend (bestehend)
```
- najika_server.py (HTTP/WebSocket)
- Ollama (AI Models)
- ChromaDB (Memory)
- WireGuard (VPN Server)
```

---

## 🚀 DEPLOYMENT

### Android
```bash
# Build APK
flutter build apk --release

# Build App Bundle (für Google Play)
flutter build appbundle --release
```

### iOS
```bash
# Build IPA
flutter build ios --release

# Upload zu TestFlight
```

### Sideload (ohne Store)
- **Android**: APK direkt installieren
- **iOS**: AltStore / Sideloadly

---

## 📝 NÄCHSTE SCHRITTE

1. **Flutter Projekt initialisieren**
   ```bash
   flutter create najika_digivice
   cd najika_digivice
   ```

2. **Dependencies hinzufügen** (siehe Tech-Stack)

3. **Basis-Struktur erstellen**:
   ```
   lib/
   ├── main.dart
   ├── screens/
   │   ├── chat_screen.dart
   │   ├── settings_screen.dart
   │   └── avatar_screen.dart
   ├── services/
   │   ├── connection_manager.dart
   │   ├── ai_service.dart
   │   ├── storage_service.dart
   │   └── security_service.dart
   └── models/
       ├── message.dart
       └── najika_state.dart
   ```

4. **Server-Endpunkt vorbereiten** (najika_server.py):
   - WebSocket für Real-time Chat
   - Mobile-optimierte Responses
   - Token-basierte Auth

5. **VPN Setup auf PC/Server**

---

## ❓ OFFENE FRAGEN

- [ ] Wo ist dein Najika-Bild gespeichert? (für Custom 3D Model)
- [ ] DynDNS-Präferenz: DuckDNS oder No-IP?
- [ ] Google Play Store veröffentlichen oder nur Sideload?
- [ ] iOS-Version auch entwickeln? (benötigt Apple Developer Account $99/Jahr)

---

**Erstellt**: 2025-10-18
**Autor**: Claude Code + Mr.K
**Version**: 1.0
**Status**: Ready for Development 🚀
