# 🚀 NAJIKA MOBILE & MESSENGER - Implementierungs-Roadmap

**Erstellt:** 2025-11-07
**Zweck:** Schritt-für-Schritt Plan zur Umsetzung
**Geschätzte Gesamtdauer:** 10-12 Wochen
**Ziel:** Vollständige Mobile-App mit sicherem Messenger

---

## 📋 PROJEKT-ÜBERSICHT

### Komponenten

```
┌────────────────────────────────────────────────────────┐
│                NAJIKA COMPLETE SYSTEM                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. REMOTE ACCESS                                      │
│     ├─ WireGuard VPN Server                           │
│     ├─ DynDNS Setup                                    │
│     └─ Router Configuration                            │
│                                                        │
│  2. MOBILE APP (Flutter)                               │
│     ├─ Chat Interface (Najika-KI)                     │
│     ├─ 3D Avatar Integration                          │
│     ├─ Minigames                                       │
│     ├─ Connection Manager                              │
│     └─ Hybrid AI System                                │
│                                                        │
│  3. SECURE MESSENGER                                   │
│     ├─ Signal Protocol (E2E)                          │
│     ├─ Self-Destructing Messages                      │
│     ├─ Zero-Knowledge Server                          │
│     └─ Safety Number Verification                      │
│                                                        │
│  4. BACKEND (Server)                                   │
│     ├─ najika_server.py (erweitert)                   │
│     ├─ najika_messenger_server.py (neu)               │
│     └─ Ollama AI Integration                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📅 ZEITPLAN

### PHASE 1: Infrastruktur & Setup (Woche 1-2)

#### Woche 1: Remote Access Setup

**Tag 1-2: PC/Server Vorbereitung**
```bash
# Tasks:
□ WireGuard installieren (Windows/Linux)
□ VPN-Schlüssel generieren
□ wg0.conf konfigurieren
□ WireGuard-Service starten
□ Firewall-Regeln einrichten
```

**Tag 3-4: Router-Konfiguration**
```bash
□ Port Forwarding (51820 UDP)
□ DynDNS einrichten (DuckDNS)
□ Auto-Update-Script (Cron/Task Scheduler)
□ Verbindung testen (extern)
```

**Tag 5-7: Flutter Projekt Setup**
```bash
□ Flutter installieren (falls nicht vorhanden)
□ Projekt erstellen: flutter create najika_digivice
□ Dependencies hinzufügen (siehe MOBILE_APP_DESIGN.md)
□ Ordnerstruktur aufbauen
□ Git Repository initialisieren
```

#### Woche 2: Backend-Erweiterung

**Tag 1-3: najika_server.py erweitern**
```python
# Tasks:
□ WebSocket-Support hinzufügen
□ Mobile-API-Endpoints erstellen:
  ├─ /api/mobile/chat
  ├─ /api/mobile/state
  └─ /api/mobile/sync
□ Token-basierte Authentifizierung
□ CORS für Mobile-App konfigurieren
□ TLS/HTTPS einrichten (Let's Encrypt)
```

**Tag 4-7: najika_messenger_server.py erstellen**
```python
□ Flask-Server aufsetzen (Port 8001)
□ Datenbank initialisieren (SQLite)
□ PreKey-Endpunkte implementieren
□ Message-Queue-System
□ WebSocket für Real-time
□ Test-Suite schreiben
```

---

### PHASE 2: Mobile App Basis (Woche 3-4)

#### Woche 3: Core Funktionalität

**Tag 1-2: Navigation & Struktur**
```dart
□ main.dart Setup
□ Routing-System (named routes)
□ Bottom Navigation Bar
□ Screens erstellen:
  ├─ SplashScreen
  ├─ AuthScreen
  ├─ HomeScreen
  └─ SettingsScreen
```

**Tag 3-5: Connection Manager**
```dart
□ ConnectionManager-Service implementieren
□ Auto-Detection (WiFi/Mobile)
□ VPN-Integration (WireGuard Flutter Plugin)
□ API-Client (Dio)
□ WebSocket-Client
□ Connection-Status UI
```

**Tag 6-7: Biometric Auth & Security**
```dart
□ local_auth Integration
□ Secure Storage Setup
□ PIN-Backup-System
□ Auto-Lock implementieren
```

#### Woche 4: Chat-Interface (Najika-KI)

**Tag 1-3: Chat UI**
```dart
□ ChatScreen Layout
□ MessageBubble Widget
□ ChatInput Widget
□ TypingIndicator
□ ScrollController (Auto-Scroll)
```

**Tag 4-5: AI Integration**
```dart
□ HybridAI-Service implementieren
□ ServerAI (API-Calls)
□ OnDeviceAI (Gemini Nano)
□ Fallback-Logik
□ Response-Caching
```

**Tag 6-7: State Management**
```dart
□ ChatProvider Setup
□ Message-Speicherung (Hive)
□ Sync-Service (WiFi-basiert)
□ Offline-Modus
```

---

### PHASE 3: 3D Avatar & Minigames (Woche 5-6)

#### Woche 5: 3D Avatar Integration

**Tag 1-3: 3D Rendering**
```dart
□ flutter_cube Setup
□ Skeleton_Mage laden (temporär)
□ Avatar3DView Widget
□ Rotation/Zoom/Pan Controls
□ Animation-System
```

**Tag 4-5: Avatar-Emotionen**
```dart
□ Emotion-Detection (aus Najika-Response)
□ Animation-Mapping:
  ├─ happy → idle_happy
  ├─ explosion → cast_spell
  ├─ tired → sit
  └─ default → idle
□ Smooth Transitions
```

**Tag 6-7: Avatar Detail Screen**
```dart
□ AvatarScreen Layout
□ Stats-Anzeige (Hunger, Energy, etc.)
□ Care-Buttons (Feed, Play, Train)
□ State-Sync mit Backend
```

#### Woche 6: Minigames

**Tag 1-2: Minigame-Framework**
```dart
□ MiniGame Base-Klasse
□ Score-System
□ Minigames Hub Screen
□ Navigation zu einzelnen Games
```

**Tag 3-7: Minigames implementieren**
```dart
□ Rhythm Game
  ├─ Note-Spawning
  ├─ Hit-Detection
  └─ Score-Tracking

□ Garden Game
  ├─ Pflanzen-System
  ├─ Wachstums-Mechanik
  └─ Ernte-System

□ Reflex Game
  ├─ Reaction-Time-Test
  └─ Highscore-System

□ (Optional) Weitere Games
```

---

### PHASE 4: Secure Messenger (Woche 7-9)

#### Woche 7: Krypto-Grundlage

**Tag 1-3: Signal Protocol**
```dart
□ X3DH Key Exchange implementieren
□ Double Ratchet Algorithm
□ HKDF (Key Derivation)
□ AES-256-GCM Encryption
□ Key-Storage (Secure)
```

**Tag 4-5: PreKey-Management**
```dart
□ Identity Key generieren
□ Signed PreKey generieren
□ One-Time PreKeys (100x) generieren
□ PreKey-Upload zu Server
□ PreKey-Rotation (monatlich)
```

**Tag 6-7: Safety Numbers**
```dart
□ Safety Number generieren
□ QR-Code-Display
□ Verification-UI
□ Verified-Status speichern
```

#### Woche 8: Messenger-UI

**Tag 1-3: Chat List & Chat Screen**
```dart
□ Messenger-Tab in App
□ Chat-Liste (mit Unread-Count)
□ Chat-Screen (E2E-verschlüsselt)
□ Message-Verschlüsselung/-Entschlüsselung
□ Send/Receive-Logik
```

**Tag 4-5: Media-Messages**
```dart
□ Sprachnachrichten
  ├─ Audio-Recorder
  ├─ Waveform-Visualisierung
  └─ Playback-Player

□ Bilder/Videos
  ├─ Kamera-Integration
  ├─ Galerie-Auswahl
  ├─ Verschlüsselter Upload
  └─ Thumbnail-Generation
```

**Tag 6-7: Self-Destructing Messages**
```dart
□ DisappearingMessage-Typ
□ Countdown-UI
□ Auto-Delete-Timer
□ Screenshot-Erkennung
□ Sender-Benachrichtigung
```

#### Woche 9: Messenger-Server & Sync

**Tag 1-3: Server-Integration**
```python
□ /api/messenger/send
□ /api/messenger/fetch
□ /api/messenger/prekeys/upload
□ /api/messenger/prekeys/fetch
□ WebSocket-Channels
```

**Tag 4-5: Message Queue**
```dart
□ Offline-Message-Queue
□ Auto-Retry bei Verbindungsverlust
□ Message-Status-Updates
  ├─ Sending
  ├─ Sent
  ├─ Delivered
  └─ Read
```

**Tag 6-7: Sealed Sender**
```dart
□ Double-Encryption-Logik
□ Server-Key-Management
□ Metadata-Protection
□ Testing
```

---

### PHASE 5: Polish & Features (Woche 10)

#### Woche 10: UI/UX & Features

**Tag 1-2: Theme & Design**
```dart
□ Gothic-Lolita Theme finalisieren
□ Dark Mode (primary)
□ Animationen (flutter_animate)
□ Lottie-Integrationen
□ Custom Fonts
```

**Tag 3-4: Notifications**
```dart
□ Push-Notifications Setup (FCM)
□ Verschlüsselte Payloads
□ Notification-Handler
□ In-App-Notifications
□ Badge-Count
```

**Tag 5-7: Settings & Preferences**
```dart
□ Einstellungen-Screen erweitern:
  ├─ Sicherheit (Biometric, Auto-Lock)
  ├─ Verbindung (Mode-Selection)
  ├─ KI-Verhalten (Personality, Speed)
  ├─ Speicher (Cache-Management)
  ├─ Darstellung (Theme, Animationen)
  └─ Messenger (Safety Numbers, Backups)
```

---

### PHASE 6: Testing & Optimierung (Woche 11)

#### Woche 11: Testing

**Tag 1-2: Unit Tests**
```dart
□ Connection Manager Tests
□ Crypto-Service Tests
□ AI-Service Tests
□ Storage-Service Tests
□ Message-Encryption Tests
```

**Tag 3-4: Widget Tests**
```dart
□ Chat-Screen Tests
□ Avatar-Screen Tests
□ Minigames Tests
□ Settings-Screen Tests
```

**Tag 5-7: Integration Tests**
```dart
□ End-to-End Chat-Flow
□ E2E Messenger-Flow
□ VPN-Connection Tests
□ Offline-Mode Tests
□ Sync-Tests
```

---

### PHASE 7: Deployment & Finalisierung (Woche 12)

#### Woche 12: Build & Deploy

**Tag 1-2: Android Build**
```bash
□ Release-Build konfigurieren
□ App-Icons hinzufügen
□ Splash-Screen finalisieren
□ Proguard-Regeln
□ APK bauen: flutter build apk --release
□ Sideload-Test auf Xiaomi 11T Pro
```

**Tag 3-4: Performance-Optimierung**
```dart
□ Image-Caching optimieren
□ 3D-Model Lazy Loading
□ Database-Query-Optimierung
□ Memory-Leak-Check
□ Battery-Usage-Optimierung
```

**Tag 5-7: Dokumentation & Übergabe**
```markdown
□ User-Guide schreiben
□ Admin-Guide (Server-Setup)
□ API-Dokumentation
□ Troubleshooting-Guide
□ Changelog erstellen
```

---

## 🛠️ ENTWICKLUNGS-TOOLS

### Erforderliche Software

```yaml
Entwicklung:
  - Flutter SDK 3.24+
  - Android Studio / VS Code
  - Dart DevTools
  - Git

Server:
  - Python 3.11+
  - WireGuard
  - SQLite / PostgreSQL (optional)
  - Let's Encrypt (für TLS)

Testing:
  - Android Device (Xiaomi 11T Pro)
  - WiFi-Netzwerk
  - VPN-Test-Tool (z.B. ping, speedtest)

Design:
  - Figma (für UI-Mockups)
  - Blender (für 3D-Assets, später)
```

---

## 📊 MEILENSTEINE & DELIVERABLES

### Meilenstein 1: Infrastruktur (Ende Woche 2)
```
✅ VPN-Server läuft
✅ DynDNS funktioniert
✅ Flutter-Projekt aufgesetzt
✅ Backend erweitert
```

### Meilenstein 2: MVP Mobile App (Ende Woche 4)
```
✅ Chat mit Najika funktioniert
✅ Biometric Auth implementiert
✅ Connection Manager aktiv
✅ Sync-System läuft
```

### Meilenstein 3: Feature-Complete (Ende Woche 6)
```
✅ 3D Avatar integriert
✅ Minigames spielbar
✅ Avatar-Care-System
```

### Meilenstein 4: Secure Messenger (Ende Woche 9)
```
✅ E2E-Verschlüsselung funktioniert
✅ Self-Destructing Messages
✅ Messenger-Server läuft
✅ Safety Number Verification
```

### Meilenstein 5: Production-Ready (Ende Woche 12)
```
✅ Alle Tests bestanden
✅ Performance optimiert
✅ APK gebaut
✅ Dokumentation komplett
```

---

## 🎯 PRIORITÄTEN

### Must-Have (P0)
```
1. Remote Access (VPN)
2. Chat mit Najika (Hybrid AI)
3. Biometric Auth
4. E2E Messenger
5. Self-Destructing Messages
```

### Should-Have (P1)
```
6. 3D Avatar (mit Platzhalter-Model)
7. Minigames (mindestens 3)
8. Sealed Sender
9. Push Notifications
10. Settings-Screen
```

### Nice-to-Have (P2)
```
11. Custom Najika 3D Model
12. AR-Modus
13. Tor-Integration
14. Voice/Video Calls
15. Group Chats
```

---

## ⚠️ RISIKEN & MITIGATION

### Risiko 1: VPN-Verbindung instabil
**Mitigation:**
- Fallback auf Direct-Server-Connection (mit TLS)
- Cloudflare Tunnel als Alternative
- Auto-Reconnect-Logik

### Risiko 2: On-Device AI zu langsam
**Mitigation:**
- Response-Caching
- Kürzere Prompts
- Fallback auf Server-AI bevorzugen

### Risiko 3: Krypto-Implementierung fehlerhaft
**Mitigation:**
- Nutze bewährte Libraries (cryptography Package)
- Code-Review durch Experten
- Penetration Testing

### Risiko 4: Speicherplatz-Probleme
**Mitigation:**
- Aggressives Auto-Cleanup (>30 Tage)
- Kompression für Medien
- User-Warnungen bei <5GB frei

---

## 📈 SUCCESS METRICS

### Funktionale Metriken
```
□ App startet in <3 Sekunden
□ Chat-Response in <2 Sekunden (WiFi)
□ VPN-Verbindung in <5 Sekunden
□ Message-Verschlüsselung in <100ms
□ 3D Avatar läuft bei 60 FPS
```

### Sicherheits-Metriken
```
□ 100% E2E-Verschlüsselung
□ Keine Plaintext-Messages auf Server
□ Safety Numbers verifizierbar
□ Zero-Knowledge-Server (auditiert)
```

### User-Experience-Metriken
```
□ Intuitive Navigation (<5 Min Einarbeitung)
□ Keine Crashes
□ Battery-Usage <10%/Stunde
□ Daten-Usage <50MB/Tag (Mobile)
```

---

## 🔄 POST-LAUNCH ROADMAP

### Version 1.1 (1 Monat nach Launch)
```
□ Group Chats (Messenger)
□ Voice/Video Calls (verschlüsselt)
□ Custom Najika 3D Model
□ AR-Modus (Najika in deinem Raum)
```

### Version 1.2 (2 Monate nach Launch)
```
□ iOS-Version
□ Tablet-Support
□ Backup-System (verschlüsselt)
□ Multi-Device-Sync
```

### Version 2.0 (6 Monate nach Launch)
```
□ Öffentlicher Release (Messenger)
□ Modulares Plugin-System
□ Community-Features
□ Educational Modules (Sprachen, Musik, etc.)
```

---

## 📞 SUPPORT & WARTUNG

### Wöchentliche Tasks
```
□ Server-Updates prüfen
□ DynDNS-Status checken
□ Backup-Integrity verifizieren
□ Logs durchsehen
```

### Monatliche Tasks
```
□ PreKeys rotieren (Messenger)
□ Security-Audits
□ Performance-Analyse
□ User-Feedback auswerten
```

---

## ✅ CHECKLISTE - READY FOR IMPLEMENTATION

### Vor dem Start
- [x] Dokumentation komplett gelesen
- [x] Entwicklungs-Umgebung vorbereitet
- [ ] Flutter installiert & getestet
- [ ] Git Repository erstellt
- [ ] Server/PC bereit

### Phase 1 Ready?
- [ ] WireGuard installiert
- [ ] DynDNS konfiguriert
- [ ] Flutter-Projekt erstellt
- [ ] Backend-Server läuft

---

**Nächster Schritt:**
👉 **Beginne mit Phase 1, Tag 1: WireGuard Installation**

Oder möchtest du mit einer anderen Phase starten?

---

**Dokumentiert von:** Claude Code
**Datum:** 2025-11-07
**Version:** 1.0
**Status:** Ready to Execute 🚀
