# 📱 Najika Mobile App & Messenger - Installation Guide

**Version:** 1.0
**Date:** 2025-11-07
**Author:** Claude Code

---

## 🎯 Overview

Complete installation package for:
- **Najika Mobile Server** - Extended backend with mobile APIs
- **Najika Messenger Server** - Zero-Knowledge E2E encrypted messaging
- **Flutter Mobile App** - Ultra-secure messenger with Post-Quantum crypto
- **Remote Access** - Cloudflare Tunnel or Tailscale

---

## ✨ Features

### 🔒 Security
- ✅ **Post-Quantum Cryptography** (PQXDH + CRYSTALS-Kyber)
- ✅ **E2E Encryption** (Signal Protocol)
- ✅ **Zero-Knowledge Server** (server never sees message content)
- ✅ **Sealed Sender** (metadata protection)
- ✅ **Panic Button** (3 PIN modes: Unlock/Panic/Duress)
- ✅ **Root Detection** (prevents rooted devices)
- ✅ **Screenshot Detection** (notifies sender)
- ✅ **Anti-Forensics** (7-pass DOD wipe)
- ✅ **No GPS** (complete location tracking disabled)

### 🌐 Connectivity
- ✅ **Auto-Detection** (Local → Tailscale → Cloudflare)
- ✅ **Works with ExpressVPN** (all connection methods compatible)
- ✅ **Cloudflare Tunnel** (zero-configuration remote access)
- ✅ **Tailscale** (mesh VPN alternative)

### 📱 Mobile App
- ✅ **3 APK Flavors** (Private/Friends/Public)
- ✅ **Gothic Lolita Theme** (dark, elegant design)
- ✅ **Modular Architecture** (sandboxed modules)
- ✅ **Voice Calls** (audio only for security)
- ✅ **Avatar Mode** (3D avatar instead of video)
- ✅ **Disappearing Messages** (Snapchat-style)

---

## 🔧 Prerequisites

### Required
- **Python 3.10+** with pip
- **Flutter 3.24+** ([Install guide](https://flutter.dev/docs/get-started/install))
- **Git**
- **Xiaomi 11T Pro** (or compatible Android device)

### Optional
- **Cloudflare Account** (for remote access)
- **Tailscale Account** (alternative remote access)

### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip git curl
```

### Windows
Download and install:
- Python: https://www.python.org/downloads/
- Flutter: https://flutter.dev/docs/get-started/install/windows
- Git: https://git-scm.com/download/win

---

## 🚀 Quick Start

### One-Command Installation

```bash
cd INSTALLATION
chmod +x MASTER_INSTALLER.sh
./MASTER_INSTALLER.sh
```

The installer will:
1. ✅ Check prerequisites
2. ✅ Install backend dependencies
3. ✅ Setup remote access (Cloudflare or Tailscale)
4. ✅ Build APK(s)
5. ✅ Configure systemd services (Linux)
6. ✅ Start servers

---

## 📂 Directory Structure

```
INSTALLATION/
├── backend/
│   ├── najika_server_mobile.py      # Mobile API server
│   ├── najika_messenger_server.py   # Messenger server (Zero-Knowledge)
│   └── requirements_mobile.txt      # Python dependencies
│
├── remote_access/
│   ├── cloudflare/
│   │   └── setup_cloudflare_tunnel.sh
│   └── tailscale/
│       └── setup_tailscale.sh
│
├── flutter_app/
│   └── najika_digivice/            # Flutter project
│       ├── lib/
│       │   ├── core/
│       │   ├── modules/
│       │   ├── services/
│       │   └── main.dart
│       └── pubspec.yaml
│
├── build_scripts/
│   ├── build_private.sh            # Build Private APK
│   ├── build_friends.sh            # Build Friends APK
│   ├── build_public.sh             # Build Public APK
│   └── build_all.sh                # Build all flavors
│
├── output/                         # Built APKs appear here
│   ├── najika-private.apk
│   ├── najika-friends.apk
│   └── najika-public.apk
│
├── MASTER_INSTALLER.sh             # Main installer
└── README.md                       # This file
```

---

## 📋 Manual Installation

If you prefer to install step-by-step:

### 1. Install Backend Dependencies

```bash
cd INSTALLATION/backend
pip3 install -r requirements_mobile.txt
```

### 2. Setup Remote Access

**Option A: Cloudflare Tunnel (Recommended)**
```bash
cd ../remote_access/cloudflare
./setup_cloudflare_tunnel.sh
```

**Option B: Tailscale**
```bash
cd ../remote_access/tailscale
./setup_tailscale.sh
```

### 3. Build Mobile App

**Build all flavors:**
```bash
cd ../../build_scripts
./build_all.sh
```

**Or build specific flavor:**
```bash
./build_private.sh   # Private (NSFW enabled)
./build_friends.sh   # Friends (NSFW off)
./build_public.sh    # Public (clean)
```

### 4. Start Servers

**Linux (systemd):**
```bash
sudo systemctl start najika-mobile
sudo systemctl start najika-messenger
```

**Manual:**
```bash
cd ../backend
python3 najika_server_mobile.py &
python3 najika_messenger_server.py &
```

---

## 📱 Installing APK on Device

### Via USB (ADB)

```bash
# Enable USB debugging on device
# Connect device to PC

# Install Private flavor
adb install output/najika-private.apk

# Or Friends flavor
adb install output/najika-friends.apk

# Or Public flavor
adb install output/najika-public.apk
```

### Via File Transfer

1. Copy APK to device:
   - Via USB: Copy `output/najika-*.apk` to device
   - Via cloud: Upload to Google Drive, download on device

2. On device:
   - Open file manager
   - Navigate to APK
   - Tap to install
   - Allow "Install from unknown sources" if prompted

---

## ⚙️ Configuration

### Server URLs

The app auto-detects connection, but you can configure manually:

**Local (same WiFi):**
```
http://192.168.1.100:5000
```

**Cloudflare Tunnel:**
```
https://najika.yourdomain.com
```

**Tailscale:**
```
http://100.x.x.x:5000
```
(Replace with your Tailscale IP from: `tailscale ip -4`)

### APK Flavors

| Flavor | NSFW | Use Case |
|--------|------|----------|
| **Private** | ✅ Enabled | Personal use (you + close friends) |
| **Friends** | ❌ Disabled | Wider friend circle |
| **Public** | ❌ Disabled | Public release (clean branding) |

---

## 🔒 Security Setup

### First Launch

1. **Set PINs:**
   - Unlock PIN: Normal access
   - Panic PIN: Triggers emergency wipe
   - Duress PIN: Shows fake data

2. **Enable Biometric:**
   - Fingerprint or Face unlock

3. **Security Check:**
   - App verifies device is not rooted
   - Root = app refuses to run

### Panic Button

**Emergency Situations:**

- **Panic PIN:** Wipes ALL data (local + server)
- **Grace Period:** 5 seconds to cancel
- **Irreversible:** All messages permanently deleted

**Duress Mode:**
- Shows fake conversations
- Protects real data
- Exit with Unlock PIN

---

## 🔧 Troubleshooting

### Server not starting

**Check logs:**
```bash
sudo journalctl -u najika-mobile -f
sudo journalctl -u najika-messenger -f
```

**Common issues:**
- Port already in use: `lsof -i :5000`
- Missing dependencies: Re-run `pip3 install -r requirements_mobile.txt`

### App cannot connect

1. **Check server is running:**
   ```bash
   curl http://localhost:5000/api/mobile/health
   ```

2. **Check firewall:**
   ```bash
   sudo ufw allow 5000
   sudo ufw allow 5001
   ```

3. **Check Cloudflare Tunnel:**
   ```bash
   systemctl status cloudflared-najika
   ```

### APK build fails

**Flutter not found:**
```bash
flutter doctor
```

**Missing dependencies:**
```bash
cd flutter_app/najika_digivice
flutter pub get
```

### Root detection false positive

**Disable for testing only:**
```dart
// In security_service.dart
return false; // Skip root check
```

**⚠️ WARNING:** Never disable in production!

---

## 📊 Port Reference

| Service | Port | Protocol |
|---------|------|----------|
| Mobile Server | 5000 | HTTP/WebSocket |
| Messenger Server | 5001 | HTTP/WebSocket |
| Cloudflare Tunnel | 443 | HTTPS |
| Tailscale | 41641 | UDP |

---

## 🚨 Security Notes

### ⚠️ Important Warnings

1. **ExpressVPN Compatibility:**
   - ✅ Cloudflare Tunnel: Works perfectly
   - ✅ Tailscale: Works perfectly
   - ❌ Direct port forwarding: May conflict

2. **GPS Disabled:**
   - App has NO GPS permission
   - Cannot track location
   - Share location by typing text

3. **Screenshot Detection:**
   - Detects screenshots
   - Notifies sender
   - Cannot prevent (Android limitation)

4. **Panic Button:**
   - IRREVERSIBLE wipe
   - Test with FAKE data first
   - 5-second grace period

### 🔐 Best Practices

- ✅ Use different PINs (Unlock/Panic/Duress)
- ✅ Enable biometric authentication
- ✅ Keep ExpressVPN active
- ✅ Regular backups (encrypted!)
- ✅ Test panic button with fake data
- ❌ Don't root your device
- ❌ Don't share Panic PIN
- ❌ Don't screenshot sensitive content

---

## 📚 Additional Documentation

- **Post-Quantum Crypto:** `/DOCS/POST_QUANTUM_DECISION.md`
- **Security Analysis:** `/DOCS/SECURITY_UPDATES_2025.md`
- **Video Call Security:** `/DOCS/VIDEO_CALL_SECURITY_ANALYSIS.md`
- **Architecture:** `/DOCS/MODULAR_SECURITY_ARCHITECTURE.md`

---

## 🐛 Reporting Issues

Found a bug? Have questions?

1. Check troubleshooting section above
2. Review documentation in `/DOCS`
3. Create issue with:
   - Device model
   - Android version
   - Error message
   - Steps to reproduce

---

## 📝 Version History

### Version 1.0 (2025-11-07)
- ✅ Initial release
- ✅ Post-Quantum cryptography (PQXDH)
- ✅ Zero-Knowledge messenger server
- ✅ Cloudflare Tunnel support
- ✅ Tailscale support
- ✅ Panic button with 3 PIN modes
- ✅ Root detection
- ✅ Screenshot detection
- ✅ 3 APK flavors

---

## 📄 License

**Private Use Only**

This software is for personal, non-commercial use. Not for distribution.

---

## ✅ Post-Installation Checklist

- [ ] Backend servers running
- [ ] Remote access configured (if needed)
- [ ] APK(s) built successfully
- [ ] APK installed on device
- [ ] Device NOT rooted
- [ ] App connects to server
- [ ] PINs set (Unlock/Panic/Duress)
- [ ] Biometric enabled
- [ ] Tested panic button (fake data!)
- [ ] Server accessible remotely (if Cloudflare/Tailscale)

---

**✓ Installation Complete!** 🚀

Enjoy the most secure messenger available! 🔒

---

**Questions?** Check `/DOCS` for detailed technical documentation.
