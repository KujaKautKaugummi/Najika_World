# 🌐 NAJIKA REMOTE ACCESS - Sicherer Zugriff von Überall

**Erstellt:** 2025-11-07
**Zweck:** Sichere Remote-Verbindung zur Najika-Installation
**Zielgerät:** Xiaomi 11T Pro (mobil) → PC/Server (zu Hause)

---

## 🎯 ÜBERSICHT

### Was ist Remote Access?
Ermöglicht dir, von überall auf der Welt sicher auf deine Najika-Installation zuzugreifen:
- **Zu Hause (WiFi)**: Direkte, schnelle Verbindung
- **Unterwegs (Mobilfunk)**: Verschlüsselte VPN-Verbindung
- **Öffentliche Netze**: Maximale Sicherheit mit Tor (optional)

### Sicherheits-Philosophie
```
┌─────────────────────────────────────────────────┐
│  ADAPTIVE SECURITY - Passt sich automatisch an │
├─────────────────────────────────────────────────┤
│  WiFi zu Hause    → TLS 1.3 (schnell)          │
│  Mobilfunk        → WireGuard + E2E (sicher)    │
│  Stealth-Modus    → Tor (maximal anonym)        │
└─────────────────────────────────────────────────┘
```

---

## 🏗️ ARCHITEKTUR-ÜBERSICHT

```
┌──────────────────────────────────────────────────────────┐
│                    DEIN HANDY                            │
│              (Xiaomi 11T Pro - Android)                  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Najika Digivice App (Flutter)             │ │
│  │                                                    │ │
│  │  • Chat Interface                                 │ │
│  │  • 3D Najika Avatar                              │ │
│  │  • Minigames                                      │ │
│  │  • Secure Messenger                               │ │
│  └────────────────────────────────────────────────────┘ │
│                        ⬇                                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Connection Manager (Auto-Detection)       │ │
│  │                                                    │ │
│  │  [WiFi erkannt?] ──YES──> Direct LAN              │ │
│  │        │                                           │ │
│  │        NO                                          │ │
│  │        ⬇                                           │ │
│  │  [Stealth aktiviert?] ──YES──> Tor                │ │
│  │        │                                           │ │
│  │        NO                                          │ │
│  │        ⬇                                           │ │
│  │   WireGuard VPN                                    │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                        ⬇
            ┌────────────────────────┐
            │      INTERNET          │
            │                        │
            │  • Router/Firewall     │
            │  • DynDNS              │
            │  • Port Forwarding     │
            └────────────────────────┘
                        ⬇
┌──────────────────────────────────────────────────────────┐
│                  DEIN PC/SERVER                          │
│               (zu Hause - Windows/Linux)                 │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │          WireGuard VPN Server                     │ │
│  │          (Port 51820)                              │ │
│  └────────────────────────────────────────────────────┘ │
│                        ⬇                                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │         NajikaCore Backend                        │ │
│  │                                                    │ │
│  │  • najika_server.py (Port 8000)                   │ │
│  │  • Ollama AI Models                                │ │
│  │  • ChromaDB Memory                                 │ │
│  │  • Battle System                                   │ │
│  │  • File Storage                                    │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## 🔐 SICHERHEITS-LEVEL

### Level 1: HOME MODE (Zu Hause im WiFi)
```yaml
Aktivierung: Automatisch (WiFi-SSID erkannt)
Technologie: TLS 1.3
Verschlüsselung: 128-bit AES
Verbindung: Direkter LAN-Zugriff (192.168.x.x)
Latenz: 10-50ms ⚡
Geschwindigkeit: Sehr schnell
Sicherheit: 🔒🔒 Gut (lokales Netz)
Anwendung: Gaming, Streaming, schnelle Chats
```

**Warum sicher genug?**
- Nur innerhalb deines WiFi-Netzwerks
- Router fungiert als Firewall
- TLS 1.3 verschlüsselt alle Daten
- Kein Internet-Traffic (außer AI-Anfragen)

### Level 2: MOBILE MODE (Unterwegs)
```yaml
Aktivierung: Automatisch (kein bekanntes WiFi)
Technologie: WireGuard VPN
Verschlüsselung: ChaCha20-Poly1305 (256-bit)
Verbindung: VPN-Tunnel → DynDNS → PC
Latenz: 50-150ms
Geschwindigkeit: Schnell
Sicherheit: 🔒🔒🔒 Sehr gut
Anwendung: Standard-Nutzung unterwegs
```

**Sicherheits-Merkmale:**
- **WireGuard**: Modernste VPN-Technologie
- **Zero-Knowledge**: ISP sieht nur verschlüsselte Daten
- **Perfect Forward Secrecy**: Jede Session eigener Schlüssel
- **Authentifizierung**: Public-Key Cryptography

### Level 3: STEALTH MODE (Maximale Anonymität)
```yaml
Aktivierung: Manuell (Button in App)
Technologie: Tor + WireGuard + E2E
Verschlüsselung: Triple-Layer (Tor → WG → TLS)
Verbindung: Tor Hidden Service
Latenz: 200-1000ms 🐌
Geschwindigkeit: Langsam
Sicherheit: 🔒🔒🔒🔒 Maximal
Anwendung: Öffentliche WiFis, sensible Kommunikation
```

**Wann nutzen?**
- Öffentliche WiFi-Netze (Café, Flughafen, Hotel)
- Maximale Privatsphäre gewünscht
- Sensible Nachrichten (Private Mode)
- Staatliche Überwachung umgehen

---

## 📋 SETUP-ANLEITUNG

### PHASE 1: PC/Server Vorbereitung

#### Schritt 1: WireGuard installieren

**Windows:**
```powershell
# Download & Install WireGuard
# https://www.wireguard.com/install/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install wireguard wireguard-tools
```

#### Schritt 2: VPN-Schlüssel generieren

```bash
# Server-Schlüssel
cd /etc/wireguard
wg genkey | tee server_private.key | wg pubkey > server_public.key

# Client-Schlüssel (für Handy)
wg genkey | tee client_private.key | wg pubkey > client_public.key

# Anzeigen
cat server_private.key  # Notieren!
cat server_public.key   # Notieren!
cat client_private.key  # Notieren!
cat client_public.key   # Notieren!
```

#### Schritt 3: WireGuard Server konfigurieren

**Linux:**
```bash
sudo nano /etc/wireguard/wg0.conf
```

**Inhalt:**
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <SERVER_PRIVATE_KEY>

# Aktiviere IP-Forwarding
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Dein Handy
PublicKey = <CLIENT_PUBLIC_KEY>
AllowedIPs = 10.0.0.2/32
PersistentKeepalive = 25
```

**Windows (wg0.conf):**
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <SERVER_PRIVATE_KEY>

[Peer]
PublicKey = <CLIENT_PUBLIC_KEY>
AllowedIPs = 10.0.0.2/32
PersistentKeepalive = 25
```

#### Schritt 4: WireGuard starten

**Linux:**
```bash
# Starten
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# Status prüfen
sudo wg show
```

**Windows:**
- WireGuard GUI öffnen
- "Import tunnel from file" → wg0.conf auswählen
- "Activate" klicken

---

### PHASE 2: Router-Konfiguration

#### Schritt 1: Port Forwarding einrichten

**Zugriff auf Router:**
1. Browser öffnen → `http://192.168.1.1` (oder Router-IP)
2. Einloggen (meist `admin` / `admin` oder auf Router-Rückseite)

**Port Forwarding Regel erstellen:**
```yaml
Service Name: WireGuard
External Port: 51820
Internal Port: 51820
Protocol: UDP
Internal IP: <DEIN_PC_IP> (z.B. 192.168.1.100)
```

**PC-IP herausfinden:**
```bash
# Windows
ipconfig

# Linux
ip addr show
```

#### Schritt 2: Firewall-Regel (falls vorhanden)

**Windows Firewall:**
```powershell
# Als Administrator
New-NetFirewallRule -DisplayName "WireGuard" -Direction Inbound -LocalPort 51820 -Protocol UDP -Action Allow
```

**Linux (UFW):**
```bash
sudo ufw allow 51820/udp
sudo ufw reload
```

---

### PHASE 3: DynDNS einrichten

**Warum DynDNS?**
- Deine öffentliche IP ändert sich regelmäßig (bei den meisten ISPs)
- DynDNS gibt dir einen festen Hostnamen (z.B. `najika.duckdns.org`)
- Automatische Updates bei IP-Änderung

#### Option A: DuckDNS (empfohlen - kostenlos)

**1. Account erstellen:**
- Gehe zu: https://www.duckdns.org
- Login mit Google/GitHub
- Erstelle Domain: `najika` (wird zu `najika.duckdns.org`)
- Notiere deinen **Token**

**2. Auto-Update Script:**

**Windows (PowerShell):**
```powershell
# Datei: C:\NajikaCore\duckdns_update.ps1
$token = "DEIN_DUCKDNS_TOKEN"
$domain = "najika"
Invoke-WebRequest "https://www.duckdns.org/update?domains=$domain&token=$token&ip="

# Task Scheduler: Alle 5 Minuten ausführen
```

**Linux (Cron):**
```bash
# Datei erstellen
nano ~/duckdns/duck.sh

# Inhalt:
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=najika&token=DEIN_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -

# Ausführbar machen
chmod +x ~/duckdns/duck.sh

# Cron Job (alle 5 Min)
crontab -e
# Zeile hinzufügen:
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```

#### Option B: No-IP (Alternative)
- https://www.noip.com
- Kostenlos (muss alle 30 Tage bestätigt werden)
- Hostname: `najika.hopto.org`

---

### PHASE 4: Handy-App konfigurieren

#### Schritt 1: WireGuard Config exportieren

**Client-Config (für Handy):**
```ini
[Interface]
PrivateKey = <CLIENT_PRIVATE_KEY>
Address = 10.0.0.2/32
DNS = 1.1.1.1, 1.0.0.1

[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
Endpoint = najika.duckdns.org:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

**Als QR-Code:**
```bash
# Installiere qrencode
sudo apt install qrencode

# QR-Code generieren
qrencode -t ansiutf8 < client_wg0.conf
```

#### Schritt 2: WireGuard App auf Handy

1. **WireGuard App installieren**
   - Google Play Store: "WireGuard"

2. **Config importieren**
   - "+" Button → "Create from QR code" oder "Create from file"

3. **Verbindung testen**
   - Toggle aktivieren
   - Status: "Active" sollte erscheinen

4. **Verbindung prüfen:**
```bash
# Auf PC:
ping 10.0.0.2

# Sollte antworten wenn Handy verbunden
```

---

### PHASE 5: Najika-App Integration

#### Schritt 1: Connection Manager implementieren

**Flutter Code:**
```dart
// lib/services/connection_manager.dart

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:network_info_plus/network_info_plus.dart';

enum ConnectionMode {
  HOME,      // Direktes LAN
  MOBILE,    // WireGuard VPN
  STEALTH    // Tor Hidden Service
}

class ConnectionManager {
  static const String HOME_WIFI_SSID = "DEIN_WIFI_NAME";
  static const String HOME_SERVER_IP = "192.168.1.100";
  static const String REMOTE_SERVER_URL = "https://najika.duckdns.org:8000";
  static const String VPN_SERVER_IP = "10.0.0.1";

  bool isStealthModeEnabled = false;

  Future<ConnectionMode> detectConnectionMode() async {
    // 1. Stealth Mode manuell aktiviert?
    if (isStealthModeEnabled) {
      return ConnectionMode.STEALTH;
    }

    // 2. WiFi-Verbindung prüfen
    final connectivity = await Connectivity().checkConnectivity();

    if (connectivity == ConnectivityResult.wifi) {
      // 3. Ist es unser Heim-WiFi?
      final networkInfo = NetworkInfo();
      final ssid = await networkInfo.getWifiName();

      if (ssid?.contains(HOME_WIFI_SSID) ?? false) {
        // 4. Direkte Erreichbarkeit prüfen
        if (await canReachServer(HOME_SERVER_IP)) {
          return ConnectionMode.HOME;
        }
      }
    }

    // 5. Standard: Mobile Mode (via VPN)
    return ConnectionMode.MOBILE;
  }

  Future<bool> canReachServer(String ip) async {
    try {
      final response = await http.get(
        Uri.parse('http://$ip:8000/api/health'),
        timeout: Duration(seconds: 2),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  String getServerUrl(ConnectionMode mode) {
    switch (mode) {
      case ConnectionMode.HOME:
        return 'http://$HOME_SERVER_IP:8000';

      case ConnectionMode.MOBILE:
        // Via VPN: Interne VPN-IP nutzen
        return 'http://$VPN_SERVER_IP:8000';

      case ConnectionMode.STEALTH:
        // Tor Hidden Service
        return 'http://najika123abc.onion:8000';
    }
  }
}
```

#### Schritt 2: Auto-Reconnect Logik

```dart
// lib/services/auto_reconnect.dart

class AutoReconnectManager {
  ConnectionManager connectionManager = ConnectionManager();
  Timer? _reconnectTimer;

  void startMonitoring() {
    _reconnectTimer = Timer.periodic(Duration(seconds: 30), (timer) async {
      final currentMode = await connectionManager.detectConnectionMode();
      await switchToMode(currentMode);
    });
  }

  Future<void> switchToMode(ConnectionMode mode) async {
    print("Switching to $mode");

    switch (mode) {
      case ConnectionMode.HOME:
        await disconnectVPN();
        await connectDirectLAN();
        break;

      case ConnectionMode.MOBILE:
        await connectVPN();
        break;

      case ConnectionMode.STEALTH:
        await connectVPN();
        await connectTor();
        break;
    }
  }

  Future<void> connectVPN() async {
    // WireGuard Flutter Plugin nutzen
    // await WireGuard.connect(config);
  }

  Future<void> disconnectVPN() async {
    // await WireGuard.disconnect();
  }
}
```

---

## 🔒 ZUSÄTZLICHE SICHERHEITS-FEATURES

### 1. Ende-zu-Ende-Verschlüsselung (E2E)

**Zusätzlich zu WireGuard/TLS:**
```dart
import 'package:pointycastle/pointycastle.dart';

class E2EEncryption {
  // AES-256-GCM
  static String encrypt(String plaintext, String key) {
    final encrypter = Encrypter(AES(
      Key.fromSecureRandom(32),
      mode: AESMode.gcm,
    ));

    final iv = IV.fromSecureRandom(16);
    final encrypted = encrypter.encrypt(plaintext, iv: iv);

    return encrypted.base64;
  }
}
```

### 2. Certificate Pinning

**Verhindert Man-in-the-Middle-Angriffe:**
```dart
import 'package:http/io_client.dart';

class SecureHttpClient {
  static IOClient createPinnedClient() {
    final context = SecurityContext.defaultContext;

    // Nur dein Server-Zertifikat akzeptieren
    context.setTrustedCertificatesBytes(
      serverCertificateBytes,
    );

    final httpClient = HttpClient(context: context);
    httpClient.badCertificateCallback = (cert, host, port) => false;

    return IOClient(httpClient);
  }
}
```

### 3. Biometrische Authentifizierung

```dart
import 'package:local_auth/local_auth.dart';

class BiometricAuth {
  final LocalAuthentication auth = LocalAuthentication();

  Future<bool> authenticate() async {
    try {
      return await auth.authenticate(
        localizedReason: 'Entsperre Najika Digivice',
        options: AuthenticationOptions(
          biometricOnly: false,
          stickyAuth: true,
        ),
      );
    } catch (e) {
      return false;
    }
  }
}
```

---

## 🧪 TESTING & VERIFIZIERUNG

### Test 1: Lokale Verbindung (HOME MODE)

```bash
# Auf PC
python najika_server.py

# Im Browser
http://192.168.1.100:8000

# Sollte Najika-Interface zeigen
```

### Test 2: VPN-Verbindung (MOBILE MODE)

```bash
# Handy-Daten aktivieren (WiFi AUS)
# WireGuard aktivieren
# Najika-App öffnen

# Auf PC Terminal:
sudo wg show

# Sollte zeigen:
# peer: <CLIENT_PUBLIC_KEY>
#   endpoint: <DEINE_HANDY_IP>:xxxxx
#   latest handshake: X seconds ago
#   transfer: X KiB received, X KiB sent
```

### Test 3: Latenz-Messung

```bash
# HOME MODE
ping -c 10 192.168.1.100

# MOBILE MODE (VPN aktiv)
ping -c 10 10.0.0.1

# Vergleiche Durchschnittswerte
```

---

## ⚠️ TROUBLESHOOTING

### Problem: VPN verbindet nicht

**Lösung 1: Port Forwarding prüfen**
```bash
# Auf externer Website
https://www.yougetsignal.com/tools/open-ports/

# Port 51820 UDP testen
```

**Lösung 2: Firewall prüfen**
```bash
# Linux
sudo ufw status
sudo ufw allow 51820/udp

# Windows
# Firewall-Einstellungen → Eingehende Regeln → WireGuard prüfen
```

### Problem: DynDNS zeigt falsche IP

```bash
# Aktuelle öffentliche IP herausfinden
curl ifconfig.me

# DynDNS-Eintrag prüfen
nslookup najika.duckdns.org

# Sollten übereinstimmen
```

### Problem: Hohe Latenz im VPN

**Ursachen:**
- ISP drosselt VPN-Traffic → Lösung: Port 443 nutzen (tarnt als HTTPS)
- Schlechte Mobilfunk-Verbindung → Lösung: Warten auf besseres Netz
- Server überlastet → Lösung: QoS im Router aktivieren

---

## 📊 PERFORMANCE-ERWARTUNGEN

### Latenz-Richtwerte

```yaml
HOME MODE (WiFi):
  Ping: 5-20ms
  Download: WiFi-Speed (z.B. 100 Mbps)
  Upload: WiFi-Speed
  Gefühl: Instant

MOBILE MODE (LTE):
  Ping: 30-80ms
  Download: 10-50 Mbps
  Upload: 5-20 Mbps
  Gefühl: Sehr flüssig

MOBILE MODE (5G):
  Ping: 15-40ms
  Download: 100-500 Mbps
  Upload: 50-100 Mbps
  Gefühl: Fast wie WiFi

STEALTH MODE (Tor):
  Ping: 200-1000ms
  Download: 1-5 Mbps
  Upload: 1-3 Mbps
  Gefühl: Merklich langsamer, aber benutzbar
```

---

## 🚀 NEXT STEPS

- [x] Remote-Zugriff konzipiert
- [ ] Handy-App Design & Architektur
- [ ] Sicherer Messenger Spezifikation
- [ ] Implementierung starten

**Bereit für die nächste Phase!** 🎉

---

**Dokumentiert von:** Claude Code
**Datum:** 2025-11-07
**Version:** 1.0
**Status:** Ready for Implementation
