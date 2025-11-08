# 🔐 NAJIKA SICHERHEITSMODULE

**Backend-Server, APIs und Security-Infrastruktur für Najika Digivice**

## 📦 Inhalt

### 1. Backend Server (`backend/`)

#### **Server:**
- `najika_signal_server.py` - **Hauptserver** (Signal-Protokoll, Messaging)
- `najika_messenger_server.py` - Messenger-Backend
- `najika_server_mobile.py` - Mobile-API Server
- `najika_browser_api.py` - Browser-Integration API
- `najika_terminal_api.py` - Terminal-Modul API

#### **Dependencies:**
- `requirements_mobile.txt` - Python-Pakete für Backend

### 2. Remote-Access (`remote_access/`)

#### **Cloudflare Tunnel:**
```bash
cd remote_access/cloudflare
./setup_cloudflare_tunnel.sh
```
- Sichere externe Verbindungen
- Verschlüsselte Tunnels
- Keine Port-Forwarding nötig

#### **Tailscale VPN:**
```bash
cd remote_access/tailscale
./setup_tailscale.sh
```
- Privates Netzwerk
- Peer-to-Peer Verbindungen
- WireGuard-basiert

### 3. Dokumentation

| Datei | Beschreibung |
|-------|-------------|
| `TERMINAL_MODULE_README.md` | Terminal-Modul Übersicht |
| `TERMINAL_MODULE_INTEGRATION.md` | Integration ins System |
| `IMPLEMENTATION_SUMMARY_3_VERSIONS.md` | 3-Versions-System Details |
| `IMPLEMENTATION_COMPLETE.md` | Komplette Implementation |
| `FINAL_FEATURES.md` | Finale Feature-Liste |

## 🚀 Quick Start

### Schritt 1: Dependencies installieren
```bash
cd backend
pip install -r requirements_mobile.txt
```

### Schritt 2: Server starten

#### **Option A: Signal-Server (Hauptserver)**
```bash
python najika_signal_server.py
```
**Funktionen:**
- ✅ Signal-Protokoll Messaging
- ✅ Ende-zu-Ende Verschlüsselung
- ✅ Group-Chats
- ✅ Voice Calls Koordination
- ✅ Trust-Chain Management

#### **Option B: Mobile-Server**
```bash
python najika_server_mobile.py
```
**Funktionen:**
- ✅ REST-API für Mobile App
- ✅ Verschlüsselter Storage
- ✅ User-Management
- ✅ Session-Handling

#### **Option C: Browser-API**
```bash
python najika_browser_api.py
```
**Funktionen:**
- ✅ WebSocket-Verbindungen
- ✅ Browser-Extension Support
- ✅ Sync mit Desktop-App

### Schritt 3: Remote-Access einrichten (optional)

#### **Cloudflare Tunnel:**
```bash
cd remote_access/cloudflare
chmod +x setup_cloudflare_tunnel.sh
./setup_cloudflare_tunnel.sh
```

#### **Tailscale VPN:**
```bash
cd remote_access/tailscale
chmod +x setup_tailscale.sh
./setup_tailscale.sh
```

## 🔒 Security-Features

### Verschlüsselung
- ✅ **Signal-Protokoll** - Double Ratchet, X3DH
- ✅ **Post-Quantum** - Kyber-1024 + X25519
- ✅ **TLS 1.3** - Transport-Verschlüsselung
- ✅ **AES-256-GCM** - Storage-Verschlüsselung

### Trust-System
- ✅ **Master-Key** - Root-Schlüssel (nur du)
- ✅ **Friend-Keys** - Abgeleitet vom Master
- ✅ **Public-Keys** - Für öffentliche User
- ✅ **Trust-Chain** - Hierarchische Vertrauensstruktur

### Authentifizierung
- ✅ **Multi-Factor** - 2FA/3FA Support
- ✅ **Biometric** - Fingerprint, FaceID
- ✅ **Hardware-Keys** - YubiKey Support
- ✅ **TOTP** - Time-based OTP

### Notfall-Features
- ✅ **Panic Mode** - Sofort-Löschung aller Daten
- ✅ **Dead-Man-Switch** - Auto-Löschung nach X Tagen
- ✅ **Duress-Mode** - Fake-Login bei Zwang
- ✅ **Remote-Wipe** - Fernlöschung möglich

## 📊 Backend-Architektur

### Server-Stack:
```
┌─────────────────────────────────────────┐
│  Mobile Apps (Master/Trusted/Public)    │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────▼─────────┐
        │   Signal-Server   │  ← Hauptserver
        │  (Port 8443)      │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼──┐    ┌────▼────┐   ┌───▼───┐
│ E2EE │    │ Storage │   │ Voice │
│Module│    │ Service │   │ Calls │
└──────┘    └─────────┘   └───────┘
```

### API-Endpoints:

#### **Signal-Server** (Port 8443)
- `POST /api/register` - User-Registrierung
- `POST /api/message` - Nachricht senden
- `GET /api/messages` - Nachrichten abrufen
- `POST /api/call/init` - Anruf starten
- `POST /api/trust/verify` - Trust-Chain prüfen

#### **Mobile-Server** (Port 8080)
- `POST /api/auth/login` - Login
- `GET /api/user/profile` - Profil abrufen
- `POST /api/sync` - Daten synchronisieren
- `GET /api/contacts` - Kontakte laden

#### **Browser-API** (Port 9000)
- `WS /ws/chat` - WebSocket für Chat
- `GET /api/extension/status` - Extension-Status
- `POST /api/browser/sync` - Browser-Sync

## 🔧 Terminal-Modul

**Vollständig dokumentiert in:** `TERMINAL_MODULE_README.md`

### Features:
- ✅ Shell-Zugriff über verschlüsselte Verbindung
- ✅ Remote-Commands via App
- ✅ Sichere File-Transfers
- ✅ Zugriffskontrolle (nur Master-Version)

### Integration:
```python
# Siehe TERMINAL_MODULE_INTEGRATION.md
from najika_terminal_api import TerminalSession

session = TerminalSession(master_key=YOUR_KEY)
result = session.execute("ls -la /secure/path")
```

## 🌐 Remote-Access

### Cloudflare Tunnel
**Setup:**
```bash
cd remote_access/cloudflare
./setup_cloudflare_tunnel.sh
```

**Vorteile:**
- ✅ Keine Portfreigabe
- ✅ DDoS-Schutz
- ✅ Automatische SSL-Zertifikate
- ✅ Global verteilt (CDN)

### Tailscale VPN
**Setup:**
```bash
cd remote_access/tailscale
./setup_tailscale.sh
```

**Vorteile:**
- ✅ Peer-to-Peer
- ✅ WireGuard-Protokoll
- ✅ Zero-Config
- ✅ NAT-Traversal

## 📚 Dokumentation

### Für Entwickler:
1. **IMPLEMENTATION_SUMMARY_3_VERSIONS.md**
   - Details zum 3-Versions-System
   - Key-Management
   - Trust-Chain Implementierung

2. **IMPLEMENTATION_COMPLETE.md**
   - Vollständige Feature-Liste
   - Architektur-Details
   - Code-Beispiele

3. **FINAL_FEATURES.md**
   - Abgeschlossene Features
   - Testing-Status
   - Deployment-Infos

### Für Terminal-Modul:
1. **TERMINAL_MODULE_README.md**
   - Übersicht über Terminal-Features
   - Sicherheitskonzepte
   - API-Referenz

2. **TERMINAL_MODULE_INTEGRATION.md**
   - Integration in Apps
   - Code-Beispiele
   - Best Practices

## 🎯 Production-Deployment

### Server-Requirements:
- **OS:** Linux (Ubuntu 22.04+ empfohlen)
- **RAM:** Min. 2GB (4GB empfohlen)
- **CPU:** 2+ Cores
- **Storage:** 20GB+ SSD
- **Python:** 3.9+

### Deployment-Schritte:

1. **Server vorbereiten:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```

2. **Backend installieren:**
```bash
cd sicherheitsmodule/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_mobile.txt
```

3. **Systemd-Service erstellen:**
```bash
sudo nano /etc/systemd/system/najika-signal.service
```

4. **Service starten:**
```bash
sudo systemctl enable najika-signal
sudo systemctl start najika-signal
sudo systemctl status najika-signal
```

5. **SSL-Zertifikate (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Monitoring:
```bash
# Logs checken
sudo journalctl -u najika-signal -f

# Status prüfen
sudo systemctl status najika-signal

# Resource-Usage
htop
```

## 🛡️ Security-Checklist

Vor Production-Deployment:

- [ ] Alle Secrets in Environment-Variables
- [ ] Firewall konfiguriert (nur nötige Ports offen)
- [ ] SSL/TLS aktiviert (Let's Encrypt)
- [ ] Database-Backups eingerichtet
- [ ] Rate-Limiting aktiv
- [ ] Intrusion-Detection (fail2ban)
- [ ] Log-Rotation konfiguriert
- [ ] Monitoring aufgesetzt
- [ ] Alerting konfiguriert
- [ ] Backup-Strategy definiert

## 📞 Support & Debugging

### Logs:
```bash
# Signal-Server Logs
tail -f /var/log/najika/signal.log

# Mobile-Server Logs
tail -f /var/log/najika/mobile.log

# Nginx Access-Logs
tail -f /var/log/nginx/access.log
```

### Debugging:
```python
# Debug-Modus aktivieren
export NAJIKA_DEBUG=1
python najika_signal_server.py
```

### Common Issues:
- **Port blocked:** Check Firewall (`sudo ufw status`)
- **SSL errors:** Check certificates (`sudo certbot certificates`)
- **Database errors:** Check permissions (`ls -la /var/lib/najika`)
- **Connection timeout:** Check Remote-Access setup

---

**Viel Erfolg! 🚀🔒**

*Für detaillierte Infos siehe die einzelnen Dokumentations-Dateien.*
