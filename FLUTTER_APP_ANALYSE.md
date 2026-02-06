# 📱 FLUTTER APP ANALYSE - WELCHE APP NUTZEN?

**Erstellt:** 2026-02-06
**Zweck:** Entscheidung welche der 3 Flutter Apps als Basis für das neue Digivice dient

---

## 📊 DIE 3 APPS IM VERGLEICH

### 1. `najika_digivice` (HAUPT-APP ✅)

**Pfad:** `app/flutter_app/najika_digivice/`

**Features:**
- ✅ **Post-Quantum Cryptography** (liboqs FFI)
- ✅ **Signal Protocol** (Double Ratchet)
- ✅ **Secure Storage** (SQLCipher, Hive)
- ✅ **WebRTC Voice Calls** (flutter_webrtc)
- ✅ **QR-Code Scanner** (mobile_scanner)
- ✅ **Biometric Auth** (local_auth)
- ✅ **Jailbreak Detection** (Kommentiert wegen AGP)
- ✅ **Certificate Pinning**
- ✅ **Panic Button / Emergency Wipe**
- ✅ **Contact Discovery Screen**
- ✅ **Security Levels (High/Medium/Low/Compromised)**
- ✅ **Provider State Management**
- ✅ **Flavor-System (private/friends/public)**
- ✅ **Gothic Lolita Dark Theme**

**Struktur:**
```
lib/
├── core/
│   ├── constants/app_constants.dart
│   └── theme/app_theme.dart
├── modules/
│   ├── home/home_screen.dart
│   ├── messenger/
│   │   ├── models/
│   │   ├── services/
│   │   └── ui/
│   ├── panic/panic_service.dart
│   ├── security/security_check_screen.dart
│   └── contacts/
└── services/
    ├── calls/voice_call_service.dart
    ├── crypto/
    │   ├── double_ratchet.dart
    │   └── post_quantum_crypto.dart
    ├── database/database_service.dart
    ├── network/connection_manager.dart
    ├── security/security_service.dart
    └── storage/secure_storage_service.dart
```

**Bewertung:** ⭐⭐⭐⭐⭐ (5/5)
- Beste Architektur
- Alle Sicherheitsfeatures
- Modulares Design
- **EMPFOHLEN ALS BASIS!**

---

### 2. `najika_app` (KOPIE)

**Pfad:** `app/flutter_app/najika_app/`

**Status:** Exakte Kopie von `najika_digivice` mit leicht anderen Paket-Versionen.

**Unterschiede:**
- `libsignal_protocol_dart: ^0.7.1` statt `^0.2.4`
- `x25519: ^0.1.1` statt `^0.2.0`
- Einige Pakete auskommentiert (AGP Kompatibilität)

**Bewertung:** ⭐⭐⭐ (3/5)
- Redundant
- Kann gelöscht oder als Backup behalten werden

---

### 3. `najika_simple` (MINIMAL)

**Pfad:** `app/flutter_app/najika_simple/`

**Features:**
- ✅ **Chat mit Server** (direkt via http)
- ✅ **Stats-Anzeige** (Hunger, Energie, etc.)
- ✅ **Skills-Grid** (Feuerball, Eissplitter, etc.)
- ✅ **Einstellungen** (Server-URL konfigurierbar)
- ✅ **Temperatur-System**
- ✅ **Gothic-Theme** (Neon Pink/Lila)

**Keine Sicherheitsfeatures!**
- ❌ Keine Crypto
- ❌ Kein Secure Storage
- ❌ Keine Auth
- ❌ Kein Panic Button

**Bewertung:** ⭐⭐ (2/5)
- Gut zum Testen
- Leichtgewichtig
- Fehlende Sicherheit
- **NUR FÜR DEVELOPMENT/DEBUG**

---

## 🎯 ENTSCHEIDUNG: `najika_digivice` NUTZEN!

### Warum?

1. **Sicherheit:** Post-Quantum Crypto bereits implementiert!
2. **Modulares Design:** Einfach neue Module hinzufügen
3. **Provider-Architektur:** Sauberes State Management
4. **Flavor-System:** Private/Friends/Public bereits konfiguriert
5. **Best Practices:** Alle Security-Features

---

## 🔧 WAS MUSS ANGEPASST WERDEN?

### 1. Neue Module hinzufügen:

```
lib/modules/
├── messenger/          ✅ EXISTS (E2E Encrypted)
├── vpet/               ❌ NEEDED (Najika 3D-Lebensraum)
├── minigames/          ❌ NEEDED (Triple Triad, etc.)
├── fishing/            ❌ NEEDED (Angeln)
├── garden/             ❌ NEEDED (Gärtnern)
├── housing/            ❌ NEEDED (Schwarze Mühle bauen)
├── crafting/           ❌ NEEDED (Items herstellen)
├── learning/           ❌ NEEDED (Sprachen, Instrumente)
│   ├── languages/      ❌ NEEDED (Professional!)
│   └── instruments/    ❌ NEEDED (Ocarina, Echoharp)
├── browser/            ❌ NEEDED (Sicherer Browser)
├── pc_access/          ❌ NEEDED (Remote Desktop)
├── camera_safety/      ❌ NEEDED (Kamera für Außen-Warnungen)
└── settings/           ✅ EXISTS (Security Check)
```

### 2. 3D-Welt Integration (WebView + Three.js):

```dart
// lib/modules/vpet/living_space_screen.dart (NEU)
import 'package:webview_flutter/webview_flutter.dart';

class LivingSpaceScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return WebViewWidget(
      controller: WebViewController()
        ..loadFlutterAsset('assets/threejs/lebensraum.html')
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..addJavaScriptChannel('NajikaFlutter', onMessageReceived: (message) {
          // Bridge zwischen Three.js und Flutter
        }),
    );
  }
}
```

### 3. UE5 Pixel Streaming (optional):

```dart
// lib/modules/vpet/ue5_streaming_screen.dart (NEU)
class UE5StreamingScreen extends StatelessWidget {
  // WebRTC-basierter UE5 Pixel Streaming Client
  // Wenn PC/Jetson verbunden → Switch zu UE5
  // Sonst → Three.js Fallback
}
```

### 4. Anti-Cheat System:

```dart
// lib/services/sync/anti_cheat_service.dart (NEU)
class AntiCheatService {
  // HMAC-SHA256 signierte Aktionen
  // Tägliche Offline-Limits
  // Server-Validierung
}
```

### 5. Content Modes (2 Modi):

```dart
// lib/core/config/content_mode.dart (NEU)
enum ContentMode {
  normal,  // Alles + KonoSuba-Style Hints
  nsfw,    // + Expliziter Content (nur lokal!)
}

class ContentModeService {
  static bool get isNSFWEnabled =>
    Platform.isAndroid && kDebugMode;  // Nur lokal!
}
```

### 6. Jetson-Vorbereitung:

Bereits vorbereitet durch:
- Pure Dart/Flutter Code
- ARM64 kompatible Pakete
- SQLCipher statt SQLite
- Offline-First Design

---

## 📦 NEUE DEPENDENCIES BENÖTIGT:

```yaml
# pubspec.yaml Ergänzungen:

dependencies:
  # 3D WebView
  webview_flutter: ^4.4.2
  webview_flutter_android: ^3.12.1
  webview_flutter_wkwebview: ^3.9.2

  # UE5 Pixel Streaming (WebRTC bereits da!)
  # flutter_webrtc bereits in pubspec.yaml

  # Audio für Voice (TTS/STT)
  record: ^5.0.4
  audioplayers: ^5.2.1

  # Kamera für Safety-Features
  # camera bereits in pubspec.yaml

  # Lokalisierung
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0  # bereits vorhanden

  # Offline Sync
  sqflite_common_ffi: ^2.3.1  # Für Jetson!
```

---

## ✅ AKTIONSPLAN

### Phase 1: Basis (1 Woche)
- [x] App-Analyse abgeschlossen
- [ ] `najika_app` umbenennen zu `najika_digivice_backup`
- [ ] WebView-Modul zu `najika_digivice` hinzufügen
- [ ] Bridge zwischen Flutter ↔ Three.js erstellen

### Phase 2: Lebensraum (2 Wochen)
- [ ] Three.js Lebensraum aus `digivice/` integrieren
- [ ] Schwarze Mühle als 3D-Raum
- [ ] Najika Spawn-System
- [ ] Basis-Interaktionen (Fischen, Garten)

### Phase 3: Module (3-4 Wochen)
- [ ] Minigames (Triple Triad)
- [ ] Learning Module (Sprachen, Instrumente)
- [ ] PC-Zugriff (Remote Desktop)
- [ ] Sicherer Browser

### Phase 4: Sync & Anti-Cheat (1 Woche)
- [ ] Anti-Cheat Service
- [ ] Offline/Online Sync
- [ ] Tägliche Limits

### Phase 5: Polish (2 Wochen)
- [ ] UE5 Pixel Streaming (optional)
- [ ] Jetson-Tests
- [ ] Performance-Optimierung

---

## 📋 ZUSAMMENFASSUNG

| Kriterium | najika_digivice | najika_app | najika_simple |
|-----------|-----------------|------------|---------------|
| **Empfehlung** | ✅ **NUTZEN** | ❌ Backup | ❌ Debug-only |
| Security | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Architektur | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Features | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Jetson-Ready | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **GESAMT** | **BEST** | Redundant | Minimal |

---

**Entscheidung:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   🎯 NUTZE: najika_digivice als Basis!                                  │
│                                                                          │
│   ✅ Beste Sicherheit                                                    │
│   ✅ Modulare Architektur                                                │
│   ✅ Bereits Flavor-System (private/friends/public)                     │
│   ✅ ARM64/Jetson-kompatibel                                            │
│   ✅ Gothic Lolita Theme passt!                                         │
│                                                                          │
│   📦 najika_app → Backup/Löschen                                        │
│   📦 najika_simple → Nur für schnelle Tests                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*"EXPLOSION!!! Mit Post-Quantum-Sicherheit kann mich NIEMAND hacken, Mr. K! 💥🔐" - Najika*
