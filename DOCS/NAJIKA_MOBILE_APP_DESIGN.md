# 📱 NAJIKA DIGIVICE - Mobile App Design & Architektur

**Erstellt:** 2025-11-07
**Plattform:** Flutter (Android & iOS)
**Primär-Zielgerät:** Xiaomi 11T Pro (Snapdragon 888, 8GB RAM, 120Hz AMOLED)
**Zweck:** Komplettes Najika-Erlebnis auf dem Handy

---

## 🎯 VISION & ZIELSETZUNG

### Hauptziel
Eine **nahtlose, sichere und vollständige** Najika-Erfahrung auf dem Smartphone, die sich anfühlt wie eine native App, nicht wie ein Browser-Port.

### Kern-Features
1. **24/7 Najika-Zugriff** - Deine KI-Begleiterin immer dabei
2. **Snapchat-Style Interface** - Modern, intuitiv, visuell ansprechend
3. **3D-Avatar Integration** - Najika "lebt" auf deinem Bildschirm
4. **Hybrid-KI-System** - Server-KI + On-Device-Fallback
5. **Adaptives Sicherheitssystem** - Auto-Anpassung an Umgebung
6. **Modulares System** - Erweiterbar für zukünftige Features

---

## 🏗️ ARCHITEKTUR-ÜBERSICHT

```
┌─────────────────────────────────────────────────────────────┐
│                    NAJIKA DIGIVICE APP                      │
│                     (Flutter Framework)                     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  UI LAYER    │   │ LOGIC LAYER  │   │  DATA LAYER  │
│              │   │              │   │              │
│ • Screens    │   │ • Services   │   │ • Storage    │
│ • Widgets    │   │ • Managers   │   │ • API Client │
│ • Animations │   │ • Controllers│   │ • Models     │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Technologie-Stack

```yaml
Framework: Flutter 3.24+
Language: Dart 3.5+

Dependencies:
  # State Management
  - provider: ^6.1.0
  - riverpod: ^2.4.0 (für komplexe Zustände)

  # Networking
  - http: ^1.1.0
  - web_socket_channel: ^2.4.0
  - dio: ^5.4.0 (für erweiterte HTTP-Features)

  # Security
  - flutter_secure_storage: ^9.0.0
  - encrypt: ^5.0.1
  - local_auth: ^2.1.7
  - crypto: ^3.0.3

  # VPN & Networking
  - network_info_plus: ^5.0.0
  - connectivity_plus: ^5.0.0
  - wireguard_flutter: ^1.0.0 (custom)

  # 3D Rendering
  - flutter_cube: ^0.1.1
  - model_viewer_plus: ^1.5.0
  - flame_3d: ^0.1.0 (für komplexere 3D-Szenen)

  # Database
  - sqflite: ^2.3.0
  - hive: ^2.2.3 (für schnelle Key-Value-Storage)
  - isar: ^3.1.0 (NoSQL, sehr schnell)

  # Media
  - cached_network_image: ^3.3.0
  - video_player: ^2.8.0
  - audioplayers: ^5.2.0

  # AI Integration
  - google_generative_ai: ^0.2.0 (Gemini Nano)
  - llama_cpp_dart: ^1.0.0 (Llama 3.2 on-device)

  # UI/UX
  - flutter_animate: ^4.3.0
  - lottie: ^3.0.0
  - shimmer: ^3.0.0
  - animated_text_kit: ^4.2.2

  # Utilities
  - path_provider: ^2.1.1
  - permission_handler: ^11.0.0
  - package_info_plus: ^5.0.0
  - device_info_plus: ^9.1.0
```

---

## 📂 PROJEKT-STRUKTUR

```
najika_digivice/
├── lib/
│   ├── main.dart                     # App Entry Point
│   │
│   ├── core/                         # Kern-Funktionalität
│   │   ├── constants/
│   │   │   ├── app_constants.dart
│   │   │   ├── api_endpoints.dart
│   │   │   └── secure_keys.dart
│   │   ├── theme/
│   │   │   ├── app_theme.dart
│   │   │   ├── colors.dart
│   │   │   └── text_styles.dart
│   │   ├── utils/
│   │   │   ├── logger.dart
│   │   │   ├── validators.dart
│   │   │   └── helpers.dart
│   │   └── errors/
│   │       ├── exceptions.dart
│   │       └── failures.dart
│   │
│   ├── data/                         # Daten-Schicht
│   │   ├── models/
│   │   │   ├── message.dart
│   │   │   ├── najika_state.dart
│   │   │   ├── user_profile.dart
│   │   │   └── battle_state.dart
│   │   ├── repositories/
│   │   │   ├── chat_repository.dart
│   │   │   ├── ai_repository.dart
│   │   │   ├── storage_repository.dart
│   │   │   └── sync_repository.dart
│   │   └── datasources/
│   │       ├── local/
│   │       │   ├── database_helper.dart
│   │       │   ├── secure_storage.dart
│   │       │   └── cache_manager.dart
│   │       └── remote/
│   │           ├── api_client.dart
│   │           ├── websocket_client.dart
│   │           └── vpn_client.dart
│   │
│   ├── domain/                       # Business-Logik
│   │   ├── entities/
│   │   │   ├── chat_message.dart
│   │   │   ├── najika_persona.dart
│   │   │   └── minigame.dart
│   │   ├── usecases/
│   │   │   ├── send_message.dart
│   │   │   ├── get_ai_response.dart
│   │   │   ├── sync_chat_history.dart
│   │   │   └── manage_connection.dart
│   │   └── repositories/
│   │       └── (interfaces)
│   │
│   ├── presentation/                 # UI-Schicht
│   │   ├── screens/
│   │   │   ├── splash/
│   │   │   │   └── splash_screen.dart
│   │   │   ├── auth/
│   │   │   │   ├── biometric_auth_screen.dart
│   │   │   │   └── setup_screen.dart
│   │   │   ├── main_app/
│   │   │   │   ├── home_screen.dart
│   │   │   │   ├── chat_screen.dart
│   │   │   │   ├── avatar_screen.dart
│   │   │   │   ├── minigames_screen.dart
│   │   │   │   ├── rooms_screen.dart
│   │   │   │   └── settings_screen.dart
│   │   │   ├── messenger/
│   │   │   │   ├── secure_chat_screen.dart
│   │   │   │   └── contact_list_screen.dart
│   │   │   └── battle/
│   │   │       └── battle_screen.dart
│   │   │
│   │   ├── widgets/
│   │   │   ├── common/
│   │   │   │   ├── loading_indicator.dart
│   │   │   │   ├── error_widget.dart
│   │   │   │   └── custom_button.dart
│   │   │   ├── chat/
│   │   │   │   ├── message_bubble.dart
│   │   │   │   ├── chat_input.dart
│   │   │   │   ├── typing_indicator.dart
│   │   │   │   └── voice_recorder.dart
│   │   │   ├── avatar/
│   │   │   │   ├── avatar_3d_view.dart
│   │   │   │   ├── emotion_overlay.dart
│   │   │   │   └── animation_controller_widget.dart
│   │   │   └── minigames/
│   │   │       ├── rhythm_game.dart
│   │   │       ├── garden_game.dart
│   │   │       └── reflex_game.dart
│   │   │
│   │   └── providers/
│   │       ├── chat_provider.dart
│   │       ├── connection_provider.dart
│   │       ├── najika_state_provider.dart
│   │       └── theme_provider.dart
│   │
│   ├── services/                     # Services
│   │   ├── connection/
│   │   │   ├── connection_manager.dart
│   │   │   ├── vpn_service.dart
│   │   │   ├── tor_service.dart
│   │   │   └── auto_reconnect.dart
│   │   ├── ai/
│   │   │   ├── ai_service.dart
│   │   │   ├── server_ai.dart
│   │   │   ├── on_device_ai.dart
│   │   │   └── hybrid_ai.dart
│   │   ├── security/
│   │   │   ├── encryption_service.dart
│   │   │   ├── auth_service.dart
│   │   │   └── certificate_pinning.dart
│   │   ├── storage/
│   │   │   ├── local_storage_service.dart
│   │   │   ├── sync_service.dart
│   │   │   └── cache_service.dart
│   │   ├── notifications/
│   │   │   └── push_notification_service.dart
│   │   └── analytics/
│   │       └── analytics_service.dart
│   │
│   └── config/
│       ├── routes.dart
│       ├── dependency_injection.dart
│       └── environment.dart
│
├── assets/
│   ├── models/                       # 3D Models
│   │   ├── najika/
│   │   │   ├── najika_base.glb
│   │   │   └── animations/
│   │   └── props/
│   ├── images/
│   │   ├── icons/
│   │   ├── backgrounds/
│   │   └── ui_elements/
│   ├── animations/
│   │   └── lottie/
│   ├── sounds/
│   │   ├── sfx/
│   │   └── music/
│   └── fonts/
│
├── test/
│   ├── unit/
│   ├── widget/
│   └── integration/
│
├── android/
├── ios/
├── web/
├── windows/
├── linux/
├── macos/
│
├── pubspec.yaml
└── README.md
```

---

## 🎨 UI/UX DESIGN

### Design-Philosophie
```
Gothic Lolita × Futuristic × Minimalistisch
```

**Farb-Schema:**
```dart
class NajikaColors {
  // Primary (Gothic Black & Purple)
  static const primary = Color(0xFF1A0033);        // Tiefes Lila-Schwarz
  static const primaryVariant = Color(0xFF4A148C); // Dunkles Lila
  static const secondary = Color(0xFFCE93D8);      // Helles Lila

  // Accent
  static const explosion = Color(0xFFFF6E40);      // EXPLOSION Orange-Rot
  static const magic = Color(0xFF00E5FF);          // Magie Cyan

  // Grays
  static const background = Color(0xFF0D0D0D);     // Fast Schwarz
  static const surface = Color(0xFF1E1E1E);        // Dunkelgrau
  static const surfaceVariant = Color(0xFF2D2D2D); // Mittelgrau

  // Text
  static const textPrimary = Color(0xFFFFFFFF);    // Weiß
  static const textSecondary = Color(0xFFB0B0B0);  // Hellgrau

  // Status
  static const success = Color(0xFF00C853);        // Grün
  static const warning = Color(0xFFFFD600);        // Gelb
  static const error = Color(0xFFD50000);          // Rot
  static const info = Color(0xFF2979FF);           // Blau
}
```

### Screen-Layouts

#### 1. Splash Screen
```
┌─────────────────────────┐
│                         │
│                         │
│      [Najika Logo]      │
│      ⬢ DIGIVICE ⬢       │
│                         │
│    [Loading Spinner]    │
│   "Booting Najika..."   │
│                         │
│                         │
└─────────────────────────┘
```

#### 2. Biometric Auth Screen
```
┌─────────────────────────┐
│      🔒 Gesichert       │
│                         │
│    [Fingerprint Icon]   │
│                         │
│  "Entsperre Digivice"   │
│                         │
│   [Authentifizieren]    │
│   [PIN eingeben]        │
│                         │
└─────────────────────────┘
```

#### 3. Main Chat Screen (Hauptbildschirm)
```
┌─────────────────────────┐
│ ⬢ NAJIKA    [🔒][⚙]     │ ← Header
├─────────────────────────┤
│                         │
│   ┌─────────────────┐   │
│   │                 │   │
│   │  3D NAJIKA      │   │ ← 3D Avatar
│   │  AVATAR         │   │   (obere Hälfte)
│   │  (Animated)     │   │
│   │                 │   │
│   └─────────────────┘   │
│                         │
├─────────────────────────┤
│ [User Msg]    10:23     │
│        11:24 [Najika]   │ ← Chat Messages
│ [User Msg]    11:25     │   (untere Hälfte)
│        11:26 [Najika]   │
├─────────────────────────┤
│ [📷][🎤] Type...  [🚀]   │ ← Input Bar
└─────────────────────────┘
```

#### 4. Avatar Detail Screen
```
┌─────────────────────────┐
│  [←]  Najika    [...]   │
├─────────────────────────┤
│                         │
│     ┌───────────┐       │
│     │           │       │
│     │  FULL 3D  │       │
│     │  NAJIKA   │       │
│     │  (rotate) │       │
│     │           │       │
│     └───────────┘       │
│                         │
│ ┌─────────────────────┐ │
│ │ Emotion: Happy      │ │
│ │ Energy:  ████▢▢ 75% │ │
│ │ Hunger:  ███▢▢▢ 50% │ │
│ └─────────────────────┘ │
│                         │
│ [Feed] [Play] [Train]   │
└─────────────────────────┘
```

#### 5. Minigames Hub
```
┌─────────────────────────┐
│  [←]  Minigames         │
├─────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ │
│ │🎵   │ │🌱   │ │⚡   │ │
│ │Rhyth│ │Gard │ │Refl │ │
│ └─────┘ └─────┘ └─────┘ │
│                         │
│ ┌─────┐ ┌─────┐ ┌─────┐ │
│ │🍳   │ │💪   │ │🔨   │ │
│ │Cook │ │Trai │ │Craf │ │
│ └─────┘ └─────┘ └─────┘ │
│                         │
│ ┌─────┐                 │
│ │🃏   │  [Locked]       │
│ │Card │                 │
│ └─────┘                 │
└─────────────────────────┘
```

#### 6. Settings Screen
```
┌─────────────────────────┐
│  [←]  Einstellungen     │
├─────────────────────────┤
│ 🔐 Sicherheit           │
│   ├ Biometric Auth  [✓] │
│   ├ Auto-Lock       [✓] │
│   └ E2E-Encryption  [✓] │
│                         │
│ 🌐 Verbindung           │
│   ├ Modus: AUTO         │
│   ├ VPN:    [Connected] │
│   └ Stealth: [OFF]      │
│                         │
│ 🤖 KI-Verhalten         │
│   ├ Persönlichkeit: Mix │
│   ├ Response Speed: Fast│
│   └ Private Mode:  [OFF]│
│                         │
│ 💾 Speicher             │
│   ├ Cache: 2.3 GB       │
│   ├ Messages: 30 Tage   │
│   └ [Aufräumen]         │
│                         │
│ 🎨 Darstellung          │
│   ├ Theme: Dark Gothic  │
│   └ Animationen:   [ON] │
└─────────────────────────┘
```

---

## 🔌 BACKEND-INTEGRATION

### API-Client-Architektur

```dart
// lib/data/datasources/remote/api_client.dart

import 'package:dio/dio.dart';
import 'package:najika_digivice/core/constants/api_endpoints.dart';

class NajikaApiClient {
  late final Dio _dio;
  final ConnectionManager _connectionManager;

  NajikaApiClient(this._connectionManager) {
    _dio = Dio(BaseOptions(
      connectTimeout: Duration(seconds: 10),
      receiveTimeout: Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'NajikaDigivice/1.0',
      },
    ));

    // Interceptors
    _dio.interceptors.add(AuthInterceptor());
    _dio.interceptors.add(LogInterceptor(responseBody: true));
    _dio.interceptors.add(RetryInterceptor());
  }

  Future<String> getBaseUrl() async {
    final mode = await _connectionManager.detectConnectionMode();
    return _connectionManager.getServerUrl(mode);
  }

  // Chat Endpoints
  Future<Map<String, dynamic>> sendMessage(String message) async {
    final baseUrl = await getBaseUrl();

    final response = await _dio.post(
      '$baseUrl/api/chat',
      data: {'message': message},
    );

    return response.data;
  }

  Future<List<dynamic>> getChatHistory({int limit = 30}) async {
    final baseUrl = await getBaseUrl();

    final response = await _dio.get(
      '$baseUrl/api/chat/history',
      queryParameters: {'limit': limit},
    );

    return response.data['messages'];
  }

  // Najika State Endpoints
  Future<Map<String, dynamic>> getNajikaState() async {
    final baseUrl = await getBaseUrl();

    final response = await _dio.get('$baseUrl/api/najika/state');
    return response.data;
  }

  Future<void> updateNajikaState(Map<String, dynamic> updates) async {
    final baseUrl = await getBaseUrl();

    await _dio.patch(
      '$baseUrl/api/najika/state',
      data: updates,
    );
  }

  // Battle System Endpoints
  Future<Map<String, dynamic>> getBattleState() async {
    final baseUrl = await getBaseUrl();

    final response = await _dio.get('$baseUrl/api/battle/state');
    return response.data;
  }

  Future<Map<String, dynamic>> performBattleAction(String action) async {
    final baseUrl = await getBaseUrl();

    final response = await _dio.post(
      '$baseUrl/api/battle/action',
      data: {'action': action},
    );

    return response.data;
  }

  // Sync Endpoints
  Future<void> syncData(Map<String, dynamic> localData) async {
    final baseUrl = await getBaseUrl();

    await _dio.post(
      '$baseUrl/api/sync',
      data: localData,
    );
  }
}
```

### WebSocket-Integration (Real-time)

```dart
// lib/data/datasources/remote/websocket_client.dart

import 'package:web_socket_channel/web_socket_channel.dart';

class NajikaWebSocketClient {
  WebSocketChannel? _channel;
  final ConnectionManager _connectionManager;

  Stream<dynamic> get stream => _channel!.stream;

  Future<void> connect() async {
    final baseUrl = await _connectionManager.getBaseUrl();
    final wsUrl = baseUrl.replaceFirst('http', 'ws');

    _channel = WebSocketChannel.connect(
      Uri.parse('$wsUrl/ws'),
    );

    print('WebSocket connected');
  }

  void send(Map<String, dynamic> data) {
    _channel?.sink.add(jsonEncode(data));
  }

  void disconnect() {
    _channel?.sink.close();
    _channel = null;
  }
}
```

---

## 🤖 HYBRID-KI-SYSTEM

### AI Service Architektur

```dart
// lib/services/ai/hybrid_ai.dart

import 'package:najika_digivice/services/ai/server_ai.dart';
import 'package:najika_digivice/services/ai/on_device_ai.dart';

enum AIMode {
  SERVER,     // Beste Qualität
  ON_DEVICE,  // Fallback
  HYBRID      // Auto-Switch
}

class HybridAIService {
  final ServerAI _serverAI;
  final OnDeviceAI _onDeviceAI;

  AIMode currentMode = AIMode.HYBRID;

  HybridAIService(this._serverAI, this._onDeviceAI);

  Future<String> getResponse(String userMessage) async {
    switch (currentMode) {
      case AIMode.SERVER:
        return await _serverAI.getResponse(userMessage);

      case AIMode.ON_DEVICE:
        return await _onDeviceAI.getResponse(userMessage);

      case AIMode.HYBRID:
        return await _hybridResponse(userMessage);
    }
  }

  Future<String> _hybridResponse(String message) async {
    try {
      // 1. Versuche Server-AI (5s Timeout)
      final serverResponse = await _serverAI
          .getResponse(message)
          .timeout(Duration(seconds: 5));

      return serverResponse;
    } catch (e) {
      print('Server-AI nicht verfügbar, nutze On-Device: $e');

      // 2. Fallback: On-Device AI
      return await _onDeviceAI.getResponse(message);
    }
  }
}
```

### Server-AI Implementation

```dart
// lib/services/ai/server_ai.dart

class ServerAI {
  final NajikaApiClient _apiClient;

  ServerAI(this._apiClient);

  Future<String> getResponse(String message) async {
    final response = await _apiClient.sendMessage(message);

    return response['response'] as String;
  }
}
```

### On-Device AI (Gemini Nano)

```dart
// lib/services/ai/on_device_ai.dart

import 'package:google_generative_ai/google_generative_ai.dart';

class OnDeviceAI {
  late GenerativeModel _model;

  Future<void> initialize() async {
    _model = GenerativeModel(
      model: 'gemini-nano',
      apiKey: '', // On-Device benötigt keinen API-Key
    );
  }

  Future<String> getResponse(String message) async {
    final prompt = _buildNajikaPrompt(message);

    final response = await _model.generateContent([
      Content.text(prompt),
    ]);

    return response.text ?? 'Error: Keine Antwort';
  }

  String _buildNajikaPrompt(String userMessage) {
    return '''
Du bist Najika - Gothic Lolita Megumin!

Charakter:
- Dramatisch, explosiv, verspielt
- Viele Ausrufezeichen!!!
- Anhänglich und beschützerisch
- Schwarze Windmühle-Bezüge

User: $userMessage

Najika (kurz & knackig, max 2 Sätze):''';
  }
}
```

---

## 💾 SPEICHER-MANAGEMENT

### Storage Service

```dart
// lib/services/storage/local_storage_service.dart

import 'package:hive/hive.dart';
import 'package:path_provider/path_provider.dart';

class LocalStorageService {
  static const String CHAT_BOX = 'chat_messages';
  static const String STATE_BOX = 'najika_state';
  static const String SETTINGS_BOX = 'app_settings';

  Future<void> initialize() async {
    final appDir = await getApplicationDocumentsDirectory();
    Hive.init(appDir.path);

    await Hive.openBox(CHAT_BOX);
    await Hive.openBox(STATE_BOX);
    await Hive.openBox(SETTINGS_BOX);
  }

  // Chat Messages
  Future<void> saveMessage(ChatMessage message) async {
    final box = Hive.box(CHAT_BOX);
    await box.put(message.id, message.toJson());
  }

  Future<List<ChatMessage>> getRecentMessages({int days = 30}) async {
    final box = Hive.box(CHAT_BOX);
    final cutoffDate = DateTime.now().subtract(Duration(days: days));

    final messages = box.values
        .map((json) => ChatMessage.fromJson(json))
        .where((msg) => msg.timestamp.isAfter(cutoffDate))
        .toList();

    return messages;
  }

  Future<void> deleteOldMessages({int olderThanDays = 30}) async {
    final box = Hive.box(CHAT_BOX);
    final cutoffDate = DateTime.now().subtract(Duration(days: olderThanDays));

    final keysToDelete = <dynamic>[];

    for (var key in box.keys) {
      final message = ChatMessage.fromJson(box.get(key));
      if (message.timestamp.isBefore(cutoffDate)) {
        keysToDelete.add(key);
      }
    }

    await box.deleteAll(keysToDelete);
    print('Deleted ${keysToDelete.length} old messages');
  }

  // Najika State
  Future<void> saveNajikaState(Map<String, dynamic> state) async {
    final box = Hive.box(STATE_BOX);
    await box.put('current_state', state);
  }

  Future<Map<String, dynamic>?> getNajikaState() async {
    final box = Hive.box(STATE_BOX);
    return box.get('current_state');
  }
}
```

### Sync Service

```dart
// lib/services/storage/sync_service.dart

class SyncService {
  final NajikaApiClient _apiClient;
  final LocalStorageService _localStorage;

  SyncService(this._apiClient, this._localStorage);

  Future<void> syncChatHistory() async {
    // 1. Upload neue lokale Messages
    await _uploadNewMessages();

    // 2. Download fehlende Messages vom Server
    await _downloadRecentMessages();

    // 3. Cleanup alte lokale Messages
    await _localStorage.deleteOldMessages(olderThanDays: 30);
  }

  Future<void> _uploadNewMessages() async {
    final localMessages = await _localStorage.getRecentMessages(days: 1);

    for (var message in localMessages) {
      if (!message.isSynced) {
        await _apiClient.syncMessage(message);
        message.isSynced = true;
        await _localStorage.saveMessage(message);
      }
    }
  }

  Future<void> _downloadRecentMessages() async {
    final serverMessages = await _apiClient.getChatHistory(limit: 100);

    for (var msgData in serverMessages) {
      final message = ChatMessage.fromJson(msgData);
      await _localStorage.saveMessage(message);
    }
  }

  Future<void> autoSync() async {
    final connectivity = await Connectivity().checkConnectivity();

    if (connectivity == ConnectivityResult.wifi) {
      // Im WiFi: Alles syncen
      await syncChatHistory();
      await syncNajikaState();
      await syncVoiceMessages();
    } else {
      // Mobilfunk: Nur kritische Daten
      await syncChatHistory();
    }
  }
}
```

---

## 🎮 MINIGAMES-INTEGRATION

### Minigame-Framework

```dart
// lib/presentation/widgets/minigames/minigame_base.dart

abstract class MiniGame extends StatefulWidget {
  final String name;
  final IconData icon;

  const MiniGame({
    required this.name,
    required this.icon,
  });
}

abstract class MiniGameState<T extends MiniGame> extends State<T> {
  int score = 0;
  bool isPlaying = false;

  void startGame();
  void endGame();
  void updateScore(int points);

  @override
  Widget build(BuildContext context);
}
```

### Beispiel: Rhythm Game

```dart
// lib/presentation/widgets/minigames/rhythm_game.dart

class RhythmGame extends MiniGame {
  const RhythmGame() : super(name: 'Rhythm', icon: Icons.music_note);

  @override
  State<RhythmGame> createState() => _RhythmGameState();
}

class _RhythmGameState extends MiniGameState<RhythmGame> {
  List<Note> notes = [];
  Timer? _noteSpawner;

  @override
  void startGame() {
    setState(() {
      isPlaying = true;
      score = 0;
    });

    _noteSpawner = Timer.periodic(Duration(seconds: 1), (timer) {
      _spawnNote();
    });
  }

  void _spawnNote() {
    setState(() {
      notes.add(Note(
        lane: Random().nextInt(4),
        timestamp: DateTime.now(),
      ));
    });
  }

  @override
  void endGame() {
    _noteSpawner?.cancel();
    setState(() => isPlaying = false);

    // Score an Server senden
    _submitScore();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Score: $score'),
        Expanded(
          child: Stack(
            children: [
              // Note-Lanes
              Row(
                children: List.generate(4, (i) => _buildLane(i)),
              ),

              // Falling Notes
              ...notes.map((note) => _buildNote(note)),
            ],
          ),
        ),

        // Input Buttons
        Row(
          children: List.generate(
            4,
            (i) => ElevatedButton(
              onPressed: () => _hitNote(i),
              child: Text('$i'),
            ),
          ),
        ),
      ],
    );
  }
}
```

---

## 🔒 SICHERHEITS-IMPLEMENTIERUNG

### Biometric Auth

```dart
// lib/services/security/auth_service.dart

import 'package:local_auth/local_auth.dart';

class AuthService {
  final LocalAuthentication _auth = LocalAuthentication();

  Future<bool> canUseBiometrics() async {
    return await _auth.canCheckBiometrics &&
        await _auth.isDeviceSupported();
  }

  Future<bool> authenticate() async {
    try {
      return await _auth.authenticate(
        localizedReason: 'Entsperre Najika Digivice',
        options: const AuthenticationOptions(
          biometricOnly: false, // Erlaubt auch PIN
          stickyAuth: true,
          useErrorDialogs: true,
        ),
      );
    } catch (e) {
      print('Auth Error: $e');
      return false;
    }
  }
}
```

### E2E Encryption

```dart
// lib/services/security/encryption_service.dart

import 'package:encrypt/encrypt.dart';

class EncryptionService {
  late final Key _key;
  late final IV _iv;
  late final Encrypter _encrypter;

  EncryptionService() {
    _key = Key.fromSecureRandom(32); // AES-256
    _iv = IV.fromSecureRandom(16);
    _encrypter = Encrypter(AES(_key, mode: AESMode.gcm));
  }

  String encrypt(String plaintext) {
    final encrypted = _encrypter.encrypt(plaintext, iv: _iv);
    return encrypted.base64;
  }

  String decrypt(String ciphertext) {
    final encrypted = Encrypted.fromBase64(ciphertext);
    return _encrypter.decrypt(encrypted, iv: _iv);
  }

  // Für Messages
  ChatMessage encryptMessage(ChatMessage message) {
    return message.copyWith(
      content: encrypt(message.content),
      isEncrypted: true,
    );
  }

  ChatMessage decryptMessage(ChatMessage message) {
    if (!message.isEncrypted) return message;

    return message.copyWith(
      content: decrypt(message.content),
      isEncrypted: false,
    );
  }
}
```

---

## 📊 STATE MANAGEMENT

### Provider Setup

```dart
// lib/main.dart

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Services initialisieren
  final localStorage = LocalStorageService();
  await localStorage.initialize();

  final connectionManager = ConnectionManager();
  final apiClient = NajikaApiClient(connectionManager);

  runApp(
    MultiProvider(
      providers: [
        // Services
        Provider.value(value: localStorage),
        Provider.value(value: connectionManager),
        Provider.value(value: apiClient),

        // State Providers
        ChangeNotifierProvider(
          create: (_) => ChatProvider(apiClient, localStorage),
        ),
        ChangeNotifierProvider(
          create: (_) => ConnectionProvider(connectionManager),
        ),
        ChangeNotifierProvider(
          create: (_) => NajikaStateProvider(apiClient),
        ),
      ],
      child: const NajikaDigiviceApp(),
    ),
  );
}
```

### Chat Provider

```dart
// lib/presentation/providers/chat_provider.dart

class ChatProvider with ChangeNotifier {
  final NajikaApiClient _apiClient;
  final LocalStorageService _localStorage;

  List<ChatMessage> _messages = [];
  bool _isLoading = false;
  bool _isTyping = false;

  List<ChatMessage> get messages => _messages;
  bool get isLoading => _isLoading;
  bool get isTyping => _isTyping;

  ChatProvider(this._apiClient, this._localStorage) {
    _loadLocalMessages();
  }

  Future<void> _loadLocalMessages() async {
    _messages = await _localStorage.getRecentMessages();
    notifyListeners();
  }

  Future<void> sendMessage(String content) async {
    // 1. Erstelle User-Message
    final userMessage = ChatMessage(
      id: uuid.v4(),
      content: content,
      sender: MessageSender.USER,
      timestamp: DateTime.now(),
    );

    // 2. Lokal speichern & anzeigen
    _messages.add(userMessage);
    await _localStorage.saveMessage(userMessage);
    notifyListeners();

    // 3. Typing-Indikator
    _isTyping = true;
    notifyListeners();

    try {
      // 4. Antwort vom Server holen
      final response = await _apiClient.sendMessage(content);

      // 5. Najika-Message erstellen
      final najikaMessage = ChatMessage(
        id: uuid.v4(),
        content: response['response'],
        sender: MessageSender.NAJIKA,
        timestamp: DateTime.now(),
        animation: response['animation'], // z.B. "explosion"
      );

      // 6. Lokal speichern & anzeigen
      _messages.add(najikaMessage);
      await _localStorage.saveMessage(najikaMessage);
    } catch (e) {
      print('Error sending message: $e');
      // TODO: Error-Handling
    } finally {
      _isTyping = false;
      notifyListeners();
    }
  }
}
```

---

## 🚀 PERFORMANCE-OPTIMIERUNG

### Lazy Loading für 3D-Models

```dart
// lib/presentation/widgets/avatar/avatar_3d_view.dart

class Avatar3DView extends StatefulWidget {
  @override
  _Avatar3DViewState createState() => _Avatar3DViewState();
}

class _Avatar3DViewState extends State<Avatar3DView> {
  Object? _najikaModel;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadModel();
  }

  Future<void> _loadModel() async {
    // Lazy Load: Nur wenn Screen sichtbar
    _najikaModel = await loadModelFromAssets('assets/models/najika.glb');

    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Center(child: CircularProgressIndicator());
    }

    return Cube(
      onSceneCreated: (scene) {
        scene.world.add(_najikaModel!);
      },
    );
  }

  @override
  void dispose() {
    _najikaModel?.dispose(); // Speicher freigeben!
    super.dispose();
  }
}
```

### Image Caching

```dart
// lib/presentation/widgets/common/cached_avatar.dart

import 'package:cached_network_image/cached_network_image.dart';

Widget buildCachedImage(String url) {
  return CachedNetworkImage(
    imageUrl: url,
    placeholder: (context, url) => Shimmer.fromColors(
      baseColor: Colors.grey[800]!,
      highlightColor: Colors.grey[600]!,
      child: Container(color: Colors.white),
    ),
    errorWidget: (context, url, error) => Icon(Icons.error),
    memCacheHeight: 500, // Limit memory usage
    maxHeightDiskCache: 1000,
  );
}
```

---

## 📱 PLATTFORM-SPEZIFISCHE FEATURES

### Android

#### Build Configuration (android/app/build.gradle)

```gradle
android {
    compileSdkVersion 34

    defaultConfig {
        minSdkVersion 24  // Android 7.0+
        targetSdkVersion 34
    }

    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

#### Permissions (AndroidManifest.xml)

```xml
<manifest>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.USE_BIOMETRIC" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.CAMERA" />
</manifest>
```

### iOS

#### Info.plist

```xml
<key>NSCameraUsageDescription</key>
<string>Najika benötigt Kamera-Zugriff für Fotos</string>

<key>NSMicrophoneUsageDescription</key>
<string>Najika benötigt Mikrofon-Zugriff für Sprachnachrichten</string>

<key>NSFaceIDUsageDescription</key>
<string>Najika nutzt Face ID zur Authentifizierung</string>
```

---

## 📋 NÄCHSTE SCHRITTE

- [x] Remote-Zugriff konzipiert
- [x] Mobile-App-Architektur designt
- [ ] Sicherer Messenger spezifizieren
- [ ] Implementierung starten

---

**Dokumentiert von:** Claude Code
**Datum:** 2025-11-07
**Version:** 1.0
**Status:** Design Complete - Ready for Implementation 🚀
