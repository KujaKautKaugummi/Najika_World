# Najika Digivice - 3-Version Setup Guide

Complete guide for building and deploying all three versions of the Najika Digivice app.

---

## Table of Contents

1. [Overview](#overview)
2. [The 3 Versions](#the-3-versions)
3. [Architecture](#architecture)
4. [Prerequisites](#prerequisites)
5. [Backend Setup](#backend-setup)
6. [Building the Apps](#building-the-apps)
7. [Tailscale Mesh Network](#tailscale-mesh-network)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Najika Digivice comes in 3 distinct editions:

```
┌──────────────────────────────────────────────────────────────┐
│  MASTER EDITION (Najika's Personal Digivice)                 │
│  - All features unlocked                                      │
│  - NSFW content support                                       │
│  - Full PC control                                            │
│  - 8 devices in trusted circle                                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  TRUSTED EDITION (7 Friends)                                  │
│  - Modular features (based on user's hardware)                │
│  - Secure messenger with P2P                                  │
│  - Optional: Terminal (if user has PC)                        │
│  - Optional: Browser (mobile always, PC if available)         │
│  - Part of the trusted circle                                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  PUBLIC EDITION                                               │
│  - Basic secure messenger                                     │
│  - Signal Protocol E2E encryption                             │
│  - App Store compliant                                        │
│  - Can communicate with trusted circle (via relay)            │
└──────────────────────────────────────────────────────────────┘
```

---

## The 3 Versions

### 1. Master Edition (Najika)

**File:** `build_config.dart` → `edition = DigiviceEdition.master`

**Features:**
- ✅ Die Mühle (Secure Area)
- ✅ Terminal Module (full PC control)
- ✅ Secure Browser (Mobile + PC Remote, Tor, NSFW)
- ✅ Advanced Messenger (P2P via Tailscale)
- ✅ NSFW Features
- ✅ Post-Quantum Cryptography
- ✅ Panic Button with Duress PIN

**Use Case:** Your personal Digivice with unrestricted access

---

### 2. Trusted Edition (7 Friends)

**File:** `build_config.dart` → `edition = DigiviceEdition.trusted`

**Features:**
- ✅ Die Mühle (Secure Area)
- ⚙️ Terminal Module (optional, if user has PC)
- ⚙️ Secure Browser (mobile always, PC if available)
- ✅ Advanced Messenger (P2P via Tailscale)
- ❌ NSFW Features (can be enabled per friend if needed)
- ✅ Post-Quantum Cryptography
- ✅ Panic Button

**Use Case:** Friends in your trusted circle

**Setup:** Each friend can configure during onboarding:
- Do they have a PC? → Terminal + PC Browser enabled
- No PC? → Only mobile features available

---

### 3. Public Edition

**File:** `build_config.dart` → `edition = DigiviceEdition.public`

**Features:**
- ❌ No "Die Mühle"
- ❌ No Terminal
- ❌ No Secure Browser
- ✅ Basic Messenger (via relay server)
- ❌ No NSFW
- ✅ Signal Protocol E2E encryption

**Use Case:** Public release, App Store compatible

---

## Architecture

### Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TRUSTED CIRCLE (8 Digivices)                               │
│                                                              │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐     │
│  │Najika  │    │Friend1 │    │Friend2 │    │Friend3 │ ... │
│  │Master  │◄──►│Trusted │◄──►│Trusted │◄──►│Trusted │     │
│  └────────┘    └────────┘    └────────┘    └────────┘     │
│       │             │             │             │          │
│       └─────────────┴─────────────┴─────────────┘          │
│              TAILSCALE MESH VPN                             │
│         (Direct P2P, End-to-End Encrypted)                  │
│                                                              │
│  Each device can optionally have:                           │
│  - Own PC with najika_server.py backend                     │
│  - Terminal access to their own PC                          │
│  - Browser control of their own Firefox                     │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Can communicate via relay
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  PUBLIC USERS                                                │
│                                                              │
│  ┌────────┐    ┌────────┐    ┌────────┐                    │
│  │Public1 │    │Public2 │    │Public3 │    ...             │
│  └───┬────┘    └───┬────┘    └───┬────┘                    │
│      └─────────────┴─────────────┘                          │
│         CENTRAL SIGNAL SERVER                               │
│      (Relay, no direct P2P access)                          │
└─────────────────────────────────────────────────────────────┘
```

### Backend Architecture

```
┌──────────────────────────────────────────────────────────┐
│  YOUR MAIN SERVER (for trusted circle)                   │
│                                                           │
│  najika_signal_server.py (Port 9000/9001)                │
│  ├─ HTTP REST API                                        │
│  ├─ WebSocket Server                                     │
│  ├─ User Discovery                                       │
│  ├─ Message Routing (P2P or Relay)                       │
│  └─ Message Queue (offline delivery)                     │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  EACH USER'S PC (optional, for Terminal/Browser)         │
│                                                           │
│  najika_server.py (Port 8000)                            │
│  ├─ najika_terminal_api.py                               │
│  ├─ najika_browser_api.py                                │
│  └─ najika_tor.py (for Tor browser)                      │
│                                                           │
│  Accessible via:                                          │
│  - Tailscale IP (100.x.x.x)                              │
│  - Or Cloudflare Tunnel                                  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  PUBLIC SIGNAL SERVER (for public users)                 │
│                                                           │
│  najika_signal_server.py (Public IP)                     │
│  └─ Relay-only mode                                      │
└──────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### For App Development

1. **Flutter SDK** (3.24+)
   ```bash
   flutter --version
   # Should be 3.24 or higher
   ```

2. **Android Studio / Xcode**
   - Android: For APK building
   - iOS: For IPA building (macOS only)

3. **Dependencies**
   ```bash
   cd INSTALLATION/flutter_app/najika_digivice
   flutter pub get
   ```

### For Backend

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

   Create `requirements.txt`:
   ```
   selenium
   websockets
   pyautogui
   ```

3. **For Browser Control:**
   - Firefox installed
   - GeckoDriver (for Selenium)
   ```bash
   # Linux
   wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
   tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
   sudo mv geckodriver /usr/local/bin/
   ```

4. **Tailscale** (for trusted circle)
   ```bash
   # Install Tailscale
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```

---

## Backend Setup

### Step 1: Setup Signal Server (Central)

This server handles messaging for all devices.

```bash
cd INSTALLATION/backend

# Start Signal Server
python najika_signal_server.py
```

**Expected output:**
```
============================================================
NAJIKA HYBRID SIGNAL SERVER
============================================================
Features:
  - Direct P2P routing for trusted circle
  - Relay server for public users
  - Message queuing for offline users
============================================================
🌐 HTTP Server running on port 9000
🔌 WebSocket Server running on port 9001
```

**Configure firewall:**
```bash
# Allow ports 9000 and 9001
sudo ufw allow 9000/tcp
sudo ufw allow 9001/tcp
```

**Get your server URL:**
- If using Cloudflare Tunnel: `https://your-tunnel.trycloudflare.com`
- If using Tailscale: `https://100.x.x.x:9000`
- If public IP: `https://your-ip:9000`

---

### Step 2: Setup PC Backend (for users with Terminal/Browser)

Each user who wants Terminal or Browser features needs to run this on their PC.

```bash
cd INSTALLATION/backend

# Copy files to user's PC
scp najika_terminal_api.py user@pc:~/najika_backend/
scp najika_browser_api.py user@pc:~/najika_backend/
scp najika_tor.py user@pc:~/najika_backend/

# On user's PC:
cd ~/najika_backend

# Install dependencies
pip install selenium pyautogui websockets

# Start backend (integrate with existing najika_server.py)
python najika_server.py
```

**Backend endpoints to add to `najika_server.py`:**

See the comments in:
- `najika_terminal_api.py` (bottom of file)
- `najika_browser_api.py` (bottom of file)

---

### Step 3: Tailscale Mesh Network

For the 8 trusted Digivices to communicate directly (P2P):

**On each device (phone + PC):**

1. **Install Tailscale:**
   - Android: Play Store → "Tailscale"
   - PC: See prerequisites

2. **Join the same Tailscale network:**
   ```bash
   # On PC
   sudo tailscale up

   # Get your Tailscale IP
   tailscale ip
   # Example: 100.64.1.1
   ```

   - On Android: Open Tailscale app → Sign in → Connect

3. **Note each device's IP:**
   ```
   Najika's Phone:     100.64.1.1
   Najika's PC:        100.64.1.2
   Friend 1 Phone:     100.64.1.3
   Friend 1 PC:        100.64.1.4
   ...
   ```

4. **Update Flutter app config:**

   In `user_config.dart`, during setup:
   - Terminal Server URL: `https://100.64.1.2:8000` (PC's Tailscale IP)
   - Tailscale IP: `100.64.1.1` (Phone's Tailscale IP)

---

## Building the Apps

### Master Edition (Najika)

```bash
cd INSTALLATION/flutter_app/najika_digivice

# 1. Edit build_config.dart
# Change line: static const DigiviceEdition edition = DigiviceEdition.master;

# 2. Update server URLs in build_config.dart
# - defaultServerUrl: Your PC backend URL
# - signalServerUrl: Your Signal server URL

# 3. Build APK
flutter build apk --release

# Output: build/app/outputs/flutter-apk/app-release.apk

# 4. Install on phone
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

### Trusted Edition (Friends)

Build for each friend:

```bash
cd INSTALLATION/flutter_app/najika_digivice

# 1. Edit build_config.dart
# Change line: static const DigiviceEdition edition = DigiviceEdition.trusted;

# 2. Update signalServerUrl in build_config.dart
# Point to your Signal server

# 3. Build APK
flutter build apk --release

# 4. Rename APK for this friend
mv build/app/outputs/flutter-apk/app-release.apk \
   najika_digivice_trusted_friend1.apk

# 5. Send to friend
# Friend will configure their PC during onboarding
```

**Friend's Setup (on their phone):**

1. Install APK
2. Open app → Setup screen appears
3. **Tailscale Setup:**
   - Install Tailscale
   - Join the network
   - App auto-detects IP
4. **Die Mühle Password:**
   - Set secure password
5. **PC Backend Setup:**
   - Do you have a PC? → Yes/No
   - If Yes: Enter PC Tailscale IP (e.g., `https://100.64.1.4:8000`)
   - Test connection → ✅
6. Done!

---

### Public Edition

```bash
cd INSTALLATION/flutter_app/najika_digivice

# 1. Edit build_config.dart
# Change line: static const DigiviceEdition edition = DigiviceEdition.public;

# 2. Update signalServerUrl to public server

# 3. Build APK
flutter build apk --release

# 4. This version can go to App Store
# (after proper signing and testing)
```

---

## Tailscale Mesh Network

### Benefits

- ✅ Direct P2P encryption
- ✅ No central server needed for trusted circle
- ✅ Works with ExpressVPN
- ✅ NAT traversal (works anywhere)
- ✅ Minimal latency

### Setup for the 8 Devices

1. **Create Tailscale account** (one account for all)
2. **Install on all devices** (phones + PCs)
3. **Join network:**

   Each device:
   ```bash
   tailscale up
   ```

4. **Verify connectivity:**
   ```bash
   # From one device, ping another
   ping 100.64.1.2
   ```

5. **Document IPs:**

   Create a shared document with all IPs:
   ```
   Device          Phone IP      PC IP (if any)
   ─────────────────────────────────────────────
   Najika          100.64.1.1    100.64.1.2
   Friend 1        100.64.1.3    100.64.1.4
   Friend 2        100.64.1.5    -
   Friend 3        100.64.1.6    100.64.1.7
   ...
   ```

---

## Deployment

### Distributing to Friends

**For each friend:**

1. **Send APK:**
   ```bash
   # Via secure channel (Signal, email, etc.)
   najika_digivice_trusted_friend1.apk
   ```

2. **Send setup instructions:**
   - Install Tailscale
   - Join network (share invite link)
   - Install Digivice APK
   - Follow onboarding

3. **If they have a PC:**
   - Send backend files: `najika_terminal_api.py`, `najika_browser_api.py`
   - Help them install Python + dependencies
   - Start backend on their PC
   - They enter their PC's Tailscale IP during setup

4. **If they DON'T have a PC:**
   - Onboarding will detect this
   - Terminal module won't appear
   - Browser will be mobile-only
   - Messenger works perfectly (Tailscale on phone)

---

### Public Deployment

**For public edition:**

1. **Test thoroughly**
2. **Sign APK** (for App Store)
3. **Submit to Google Play Store**
4. **Ensure Signal server is on stable hosting**

---

## Troubleshooting

### Tailscale Issues

**Problem:** "Tailscale not detected"

**Solution:**
```bash
# On Android: Make sure Tailscale app is running
# Check: Settings → VPN → Tailscale should be active

# On PC:
sudo tailscale status
# Should show "Connected"
```

---

**Problem:** "Can't reach other devices"

**Solution:**
```bash
# Test connectivity
tailscale ping 100.64.1.2

# Check firewall
sudo ufw allow from 100.64.0.0/10
```

---

### Terminal Module Issues

**Problem:** "Terminal server not found"

**Solution:**
1. Verify PC backend is running:
   ```bash
   curl https://100.64.1.2:8000/api/health
   # Should return: {"status": "ok"}
   ```

2. Check Tailscale IP is correct in app

3. Verify firewall allows port 8000:
   ```bash
   sudo ufw allow 8000/tcp
   ```

---

### Browser Module Issues

**Problem:** "Browser won't start"

**Solution:**
1. Verify Firefox is installed on PC
2. Check GeckoDriver is in PATH:
   ```bash
   geckodriver --version
   ```
3. Test browser API manually:
   ```bash
   curl -X POST https://100.64.1.2:8000/api/browser/start \
     -H "Content-Type: application/json" \
     -d '{"session_id":"test","mode":"tor"}'
   ```

---

### Messenger Issues

**Problem:** "Messages not sending"

**Solution:**
1. Check Signal server is running:
   ```bash
   curl https://your-signal-server.com:9000/api/health
   ```

2. Check WebSocket connection (in app logs)

3. For P2P: Verify both users in Tailscale network

---

### Build Issues

**Problem:** "Build fails with dependency errors"

**Solution:**
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter build apk --release
```

---

**Problem:** "Build config not updating"

**Solution:**
1. Verify `build_config.dart` was saved
2. Run hot reload won't work - need full rebuild
3. Delete `build/` folder:
   ```bash
   rm -rf build/
   flutter build apk --release
   ```

---

## Module Availability Matrix

| Module | Master | Trusted (with PC) | Trusted (no PC) | Public |
|--------|--------|-------------------|-----------------|--------|
| Messenger | ✅ P2P | ✅ P2P | ✅ P2P | ✅ Relay |
| Terminal | ✅ | ✅ | ❌ | ❌ |
| Browser (PC) | ✅ | ✅ | ❌ | ❌ |
| Browser (Mobile) | ✅ | ✅ | ✅ | ❌ |
| Die Mühle | ✅ | ✅ | ✅ | ❌ |
| NSFW | ✅ | ❌* | ❌ | ❌ |
| Tailscale | ✅ | ✅ | ✅ | ❌ |

*Can be enabled by changing build config

---

## Security Recommendations

### For Trusted Circle

1. **Tailscale Access Control:**
   - Use ACLs to restrict who can access what
   - Each user only accesses their own PC

2. **Die Mühle Password:**
   - Use strong password (8+ characters)
   - Different for each person
   - Consider using password manager

3. **Terminal Access:**
   - Set strong terminal password (separate from Mühle)
   - Consider limiting allowed commands (in backend)
   - Monitor terminal sessions

4. **PC Backend:**
   - Keep backend updated
   - Use HTTPS (self-signed cert OK for Tailscale)
   - Consider firewall rules to only allow Tailscale IPs

### For Public Users

1. **Signal Server:**
   - Use proper HTTPS certificate
   - Rate limiting for API endpoints
   - Monitor for abuse

2. **Message Relay:**
   - Server can't read messages (E2E encrypted)
   - But can see metadata (who, when)
   - Consider logging policy

---

## Performance Optimization

### Message Delivery

- **Trusted Circle:** Direct P2P = ~10-50ms latency
- **Public Users:** Via relay = ~100-500ms latency
- **Offline Queue:** Messages delivered on next connection

### Screenshot Streaming (Browser Module)

- Default: 300ms refresh rate (3 FPS)
- Can adjust in `browser_screen.dart`:
  ```dart
  Timer.periodic(Duration(milliseconds: 300), ...);
  // Decrease for smoother (e.g., 100ms = 10 FPS)
  // Increase for less bandwidth (e.g., 500ms = 2 FPS)
  ```

---

## Congratulations!

You now have a fully functional 3-version Digivice system:

- ✅ Your Master edition with all features
- ✅ 7 Trusted editions for your friends (modular)
- ✅ Public edition for wider release

**The 8 of you form a secure, private circle with:**
- Direct P2P communication
- Optional PC control
- Complete privacy
- End-to-End encryption

**While still being able to communicate with public users via relay!**

---

*For support or questions, refer to the individual module documentation:*
- `TERMINAL_MODULE_README.md`
- `TERMINAL_MODULE_INTEGRATION.md`
- `MESSENGER_README.md` (existing)
