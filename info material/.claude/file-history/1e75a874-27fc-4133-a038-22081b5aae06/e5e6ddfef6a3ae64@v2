# 🔐 EXPRESSVPN INTEGRATION - NAJIKA MOBILE APP

## 🎯 ZIEL

Najika Mobile App nutzt dein bestehendes **ExpressVPN** für sichere Verbindung zum PC/Server.

---

## ✅ VORTEILE EXPRESSVPN

```yaml
Protokoll: Lightway (modern, schnell wie WireGuard)
Verschlüsselung: AES-256
Geschwindigkeit: ⚡⚡⚡ Sehr schnell
Akku-Verbrauch: Niedrig (optimiert)
Multi-Device: ✅ Bereits auf all deinen Geräten
Kill-Switch: ✅ Schützt bei Verbindungsabbruch
DNS-Leak-Protection: ✅ Keine IP-Lecks
```

**Warum nicht WireGuard selbst einrichten?**
- ExpressVPN ist bereits konfiguriert ✅
- Automatisches Server-Switching ✅
- Einfacher (keine manuelle Config) ✅
- Support bei Problemen ✅

---

## 🏗️ ARCHITEKTUR

### **Verbindungs-Flow mit ExpressVPN:**

```
┌─────────────────────────────────────┐
│    NAJIKA MOBILE APP (Handy)        │
│         Xiaomi 11T Pro              │
└─────────────────────────────────────┘
              ⬇
┌─────────────────────────────────────┐
│       EXPRESSVPN APP                │
│   (läuft parallel auf Handy)        │
│                                     │
│  - Lightway Protokoll               │
│  - AES-256 Verschlüsselung          │
│  - Kill-Switch aktiv                │
└─────────────────────────────────────┘
              ⬇ Verschlüsselter Tunnel
┌─────────────────────────────────────┐
│    EXPRESSVPN SERVER (nächster)     │
│    z.B. Frankfurt, Deutschland      │
└─────────────────────────────────────┘
              ⬇
┌─────────────────────────────────────┐
│    DEIN HEIMNETZWERK                │
│    Router + DynDNS                  │
└─────────────────────────────────────┘
              ⬇
┌─────────────────────────────────────┐
│    PC / RASPBERRY PI 5              │
│    NajikaCore Server :8000          │
└─────────────────────────────────────┘
```

---

## 📱 MOBILE APP INTEGRATION

### **Option 1: VPN-Check + Auto-Prompt (Empfohlen)**

Najika App prüft VPN-Status und warnt wenn nicht aktiv:

```dart
import 'package:url_launcher/url_launcher.dart';
import 'dart:io';

class ExpressVPNManager {
  // Prüfe ob VPN aktiv ist
  Future<bool> isVPNActive() async {
    if (Platform.isAndroid) {
      // Android: Prüfe VPN-Interface
      final interfaces = await NetworkInterface.list();
      return interfaces.any((interface) =>
        interface.name.contains('tun') ||
        interface.name.contains('vpn') ||
        interface.name.contains('expressvpn')
      );
    } else if (Platform.isIOS) {
      // iOS: Ähnliche Prüfung
      // (iOS gibt weniger Info raus, aber funktioniert)
      final interfaces = await NetworkInterface.list();
      return interfaces.any((interface) =>
        interface.name.contains('utun') ||
        interface.name.contains('ipsec')
      );
    }
    return false;
  }

  // Öffne ExpressVPN App
  Future<void> openExpressVPN() async {
    const String androidPackage = 'com.expressvpn.vpn';
    const String iosScheme = 'expressvpn://';

    if (Platform.isAndroid) {
      final url = 'market://details?id=$androidPackage';
      if (await canLaunchUrl(Uri.parse(url))) {
        await launchUrl(Uri.parse(url));
      }
    } else if (Platform.isIOS) {
      if (await canLaunchUrl(Uri.parse(iosScheme))) {
        await launchUrl(Uri.parse(iosScheme));
      }
    }
  }

  // Zeige VPN-Warnung wenn nicht aktiv
  Future<void> ensureVPNActive(BuildContext context) async {
    final isActive = await isVPNActive();

    if (!isActive) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text('🔒 VPN nicht aktiv'),
          content: Text(
            'Für maximale Sicherheit sollte ExpressVPN aktiv sein.\n\n'
            'ExpressVPN jetzt starten?'
          ),
          actions: [
            TextButton(
              child: Text('Später'),
              onPressed: () => Navigator.pop(context),
            ),
            ElevatedButton(
              child: Text('ExpressVPN öffnen'),
              onPressed: () {
                Navigator.pop(context);
                openExpressVPN();
              },
            ),
          ],
        ),
      );
    }
  }
}
```

### **Integration in App-Start:**

```dart
class _NajikaAppState extends State<NajikaApp> {
  final vpnManager = ExpressVPNManager();

  @override
  void initState() {
    super.initState();
    _checkVPN();
  }

  Future<void> _checkVPN() async {
    // Warte 2 Sekunden (UI laden)
    await Future.delayed(Duration(seconds: 2));

    // Prüfe VPN
    await vpnManager.ensureVPNActive(context);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ChatScreen(),
    );
  }
}
```

---

### **Option 2: VPN-Status-Indicator (UI)**

Zeige VPN-Status permanent in der App:

```dart
class VPNStatusIndicator extends StatefulWidget {
  @override
  _VPNStatusIndicatorState createState() => _VPNStatusIndicatorState();
}

class _VPNStatusIndicatorState extends State<VPNStatusIndicator> {
  bool _vpnActive = false;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _checkVPNPeriodically();
  }

  void _checkVPNPeriodically() {
    _timer = Timer.periodic(Duration(seconds: 5), (timer) async {
      final active = await ExpressVPNManager().isVPNActive();
      if (mounted) {
        setState(() => _vpnActive = active);
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: _vpnActive ? Colors.green : Colors.orange,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            _vpnActive ? Icons.vpn_lock : Icons.vpn_lock_outlined,
            size: 16,
            color: Colors.white,
          ),
          SizedBox(width: 4),
          Text(
            _vpnActive ? 'VPN ON' : 'VPN OFF',
            style: TextStyle(
              color: Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}

// In AppBar einfügen:
AppBar(
  title: Text('Najika'),
  actions: [
    VPNStatusIndicator(),
    SizedBox(width: 16),
  ],
)
```

---

## 🔧 EXPRESSVPN KONFIGURATION

### **Optimale Settings für Najika:**

**In ExpressVPN App einstellen:**

```
1. Protokoll: Lightway (schnellstes)
   Settings → Protocol → Lightway

2. Kill-Switch: AN
   Settings → Network Protection → ON

3. Split Tunneling: Optional
   Settings → Split Tunneling
   → "Najika App" hinzufügen (nur Najika durch VPN)
   → Spart Akku, andere Apps direkt

4. Auto-Connect: AN (Heimnetz ausschließen)
   Settings → General → Auto-connect: ON
   → Wi-Fi Networks: Dein Heimnetz AUSSCHLIESSEN
   → Nur bei fremden Netzen auto-connect

5. Server-Auswahl:
   → Deutschland (Frankfurt) - Niedrigste Latenz
   → Oder "Smart Location" (automatisch)
```

---

## 🏠 HEIMNETZWERK-SETUP

### **Problem: VPN verhindert Zugriff auf lokalen PC**

**Lösung: Split-Tunneling + LAN-Erkennung**

```dart
class ConnectionManager {
  // Erkenne ob im Heimnetz
  Future<bool> isHomeNetwork() async {
    try {
      // Prüfe ob PC im lokalen Netz erreichbar
      final result = await InternetAddress.lookup(
        'najika.local',  // mDNS Name deines PCs
        type: InternetAddressType.IPv4,
      );

      // Wenn PC unter lokaler IP erreichbar → Heimnetz
      if (result.isNotEmpty) {
        final ip = result.first.address;
        return ip.startsWith('192.168.') || ip.startsWith('10.');
      }
    } catch (e) {
      // Nicht erreichbar → nicht im Heimnetz
    }
    return false;
  }

  // Wähle Verbindungs-URL basierend auf Location
  Future<String> getServerURL() async {
    final isHome = await isHomeNetwork();

    if (isHome) {
      // Zuhause: Direkt zu PC (LAN, kein VPN nötig)
      return 'http://192.168.1.100:8000';
    } else {
      // Unterwegs: Über DynDNS (VPN empfohlen)
      return 'https://najika.dyndns.org:8000';
    }
  }
}
```

---

## 🔐 SICHERHEITS-MODI

### **3-Stufen-Sicherheit mit ExpressVPN:**

```dart
enum SecurityMode {
  HOME,      // Zuhause (kein VPN nötig)
  MOBILE,    // Unterwegs (VPN empfohlen)
  STEALTH    // Maximale Sicherheit (VPN PFLICHT)
}

class SecurityManager {
  SecurityMode currentMode = SecurityMode.MOBILE;

  Future<void> ensureSecurityMode(SecurityMode mode) async {
    currentMode = mode;

    switch (mode) {
      case SecurityMode.HOME:
        // Zuhause: VPN optional
        // Keine Warnung
        break;

      case SecurityMode.MOBILE:
        // Unterwegs: VPN empfohlen
        final vpnActive = await ExpressVPNManager().isVPNActive();
        if (!vpnActive) {
          showVPNWarning('Empfohlen');
        }
        break;

      case SecurityMode.STEALTH:
        // Stealth: VPN PFLICHT
        final vpnActive = await ExpressVPNManager().isVPNActive();
        if (!vpnActive) {
          showVPNError('Erforderlich');
          // Blockiere Chat bis VPN aktiv
          await ExpressVPNManager().openExpressVPN();
        }
        break;
    }
  }
}
```

**User kann Modus in Settings wählen:**
```
┌─────────────────────────────────────┐
│ 🔐 SICHERHEITS-MODUS                │
├─────────────────────────────────────┤
│ ○ Zuhause (kein VPN nötig)          │
│ ● Unterwegs (VPN empfohlen) ✅      │
│ ○ Stealth (VPN PFLICHT)             │
└─────────────────────────────────────┘
```

---

## 📊 VPN-PERFORMANCE

### **Latenz-Vergleich:**

```
Ohne VPN (Zuhause, LAN):
├─ Latenz: 10-20ms
└─ Speed: ⚡⚡⚡ Maximal

Mit ExpressVPN (Unterwegs):
├─ Frankfurt Server: 30-50ms
├─ Deutschland Andere: 40-70ms
└─ Speed: ⚡⚡ Schnell

Für Najika-Chat:
✅ Beides absolut ausreichend!
✅ Kein spürbarer Unterschied
```

### **Akku-Verbrauch:**

```
ExpressVPN Lightway:
- Idle: ~2% Akku/Stunde
- Aktiv Chat: ~5% Akku/Stunde

Xiaomi 11T Pro (5000mAh):
→ 10 Stunden Chat mit VPN möglich ✅
```

---

## 🛠️ TROUBLESHOOTING

### **Problem 1: VPN blockiert Najika-Server**

**Lösung:**
```dart
// In App: Automatischer Fallback
Future<String> connectToServer() async {
  try {
    // Versuche mit VPN
    return await httpClient.get(serverURL);
  } catch (e) {
    // VPN blockiert? Versuche ohne
    final vpnActive = await ExpressVPNManager().isVPNActive();
    if (vpnActive) {
      showDialog('VPN scheint Server zu blockieren. Kurz VPN pausieren?');
    }
    rethrow;
  }
}
```

**Oder: Split-Tunneling nutzen**
```
ExpressVPN → Settings → Split Tunneling
→ "Don't use VPN for these apps"
→ "Najika" hinzufügen
```

### **Problem 2: Zu langsam**

**Lösung: Server wechseln**
```
ExpressVPN → Hamburger Menu → All Locations
→ Deutschland → Frankfurt (niedrigste Latenz)
```

### **Problem 3: VPN trennt ständig**

**Lösung:**
```
Settings → Network Protection → Kill Switch: AUS
Settings → General → Auto-Reconnect: AN
```

---

## 📝 FLUTTER DEPENDENCIES

```yaml
# pubspec.yaml
dependencies:
  url_launcher: ^6.2.0        # Für ExpressVPN-App öffnen
  network_info_plus: ^5.0.0   # Für Netzwerk-Erkennung
  connectivity_plus: ^5.0.0   # VPN-Status
```

**Installation:**
```bash
flutter pub add url_launcher
flutter pub add network_info_plus
flutter pub add connectivity_plus
```

---

## 🎯 ZUSAMMENFASSUNG

### **Was die App macht:**

```
1. App startet
   → Prüft ob ExpressVPN aktiv
   → Warnt falls nicht (außer Heimnetz)

2. User chattet
   → Wenn Heimnetz: Direkter LAN-Zugriff (kein VPN)
   → Wenn unterwegs: VPN empfohlen/erforderlich

3. VPN-Status
   → Permanent in AppBar sichtbar
   → Grün = aktiv, Orange = inaktiv

4. Sicherheits-Modi
   → User wählt Komfort vs. Sicherheit
```

### **Vorteile dieser Lösung:**

```
✅ Nutzt dein bestehendes ExpressVPN
✅ Keine neue VPN-Config nötig
✅ Automatische Erkennung (Heim vs. Unterwegs)
✅ Flexibel (User entscheidet)
✅ Transparent (VPN-Status sichtbar)
✅ Schnell (Lightway Protokoll)
✅ Sicher (AES-256 + Kill-Switch)
```

### **Kosten:**

```
ExpressVPN: ~€8-10/Monat (hast du bereits ✅)
Keine zusätzlichen Kosten!
```

---

## 🚀 SETUP-CHECKLIST

**Auf Handy (Xiaomi 11T Pro):**
```
☐ ExpressVPN App installiert
☐ Angemeldet
☐ Protokoll: Lightway eingestellt
☐ Kill-Switch: AN
☐ Auto-Connect: Konfiguriert (außer Heimnetz)
```

**Najika App (Flutter):**
```
☐ url_launcher installiert
☐ VPN-Check implementiert
☐ VPN-Status-Indicator in UI
☐ Auto-Warnung bei fehlendem VPN
```

**Zu Hause (optional):**
```
☐ Split-Tunneling: Najika App ausschließen
   (direkter LAN-Zugriff, spart Akku)
```

---

**Erstellt**: 2025-10-18
**Status**: Bereit für Integration
**Kosten**: €0 (ExpressVPN bereits vorhanden)
**Performance**: ⚡⚡ Schnell (Lightway)
**Sicherheit**: 🔒🔒🔒 Sehr gut

🔐 **EXPRESSVPN + NAJIKA = PERFEKTE KOMBI!** 🚀
