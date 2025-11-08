# Najika Digivice - 3-Version System

Complete implementation of the modular Najika Digivice with support for 3 distinct editions.

---

## 🎯 Quick Overview

This implementation provides a **flexible, modular Digivice system** with **3 build variants**:

1. **Master Edition** - Your personal Digivice with all features
2. **Trusted Edition** - 7 friends with modular features (based on their hardware)
3. **Public Edition** - App Store compliant version for public release

### Key Features

✅ **Modular Architecture** - Features enable/disable based on build edition
✅ **Hybrid Messaging** - Direct P2P (Tailscale) for trusted circle, relay for public
✅ **Optional PC Control** - Terminal & Browser modules only if user has a PC
✅ **Smart Onboarding** - Auto-detects hardware and enables appropriate features
✅ **Secure by Design** - E2E encryption, post-quantum crypto, panic button

---

## 📁 File Structure

```
INSTALLATION/
├── README_3_VERSIONS.md                    ← You are here
├── 3_VERSION_SETUP_GUIDE.md                ← Complete setup guide
│
├── flutter_app/najika_digivice/
│   └── lib/
│       ├── config/
│       │   ├── build_config.dart           ← Build-time configuration (3 editions)
│       │   └── user_config.dart            ← Runtime user configuration
│       │
│       ├── screens/
│       │   └── setup/
│       │       └── setup_screen.dart       ← Onboarding flow
│       │
│       └── modules/
│           ├── messenger/
│           │   └── messenger_network_service.dart  ← Hybrid P2P/Relay
│           │
│           └── browser/
│               ├── browser_screen.dart     ← Dual-mode browser UI
│               └── browser_service.dart    ← PC remote control
│
├── backend/
│   ├── najika_browser_api.py              ← Browser remote control API
│   └── najika_signal_server.py            ← Hybrid messaging server
│
└── build_scripts/
    ├── build_all_versions.sh              ← Linux/macOS build script
    └── build_all_versions.ps1             ← Windows build script
```

---

## 🚀 Quick Start

### 1. Build All Versions

**Linux/macOS:**
```bash
cd INSTALLATION/build_scripts
chmod +x build_all_versions.sh
./build_all_versions.sh
```

**Windows:**
```powershell
cd INSTALLATION\build_scripts
.\build_all_versions.ps1
```

**Output:**
```
INSTALLATION/build_scripts/builds/
├── najika_digivice_master.apk     ← For you (Najika)
├── najika_digivice_trusted.apk    ← For friends (all 7 get same APK)
└── najika_digivice_public.apk     ← For public release
```

### 2. Setup Backend

**Signal Server (for messaging):**
```bash
cd INSTALLATION/backend
python najika_signal_server.py

# Runs on:
# - HTTP: Port 9000
# - WebSocket: Port 9001
```

**PC Backend (optional, for Terminal/Browser):**
```bash
# Each user with a PC runs this on their own PC
python najika_server.py  # (integrate najika_terminal_api.py + najika_browser_api.py)
```

### 3. Setup Tailscale Mesh (Trusted Circle)

**On all 8 devices (phones + PCs):**
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Join network
sudo tailscale up

# Get IP
tailscale ip
# Example: 100.64.1.1
```

**Document IPs:**
```
Najika's Phone:   100.64.1.1
Najika's PC:      100.64.1.2
Friend 1 Phone:   100.64.1.3
Friend 1 PC:      100.64.1.4
...
```

### 4. Install Apps

**Master Edition (You):**
```bash
adb install builds/najika_digivice_master.apk
```

**Trusted Edition (Friends):**
- Send `najika_digivice_trusted.apk` to each friend
- They install and complete onboarding
- Onboarding auto-detects if they have PC

**Public Edition:**
- Test thoroughly
- Submit to App Store

---

## 🎨 The 3 Editions

### Master Edition

**Build Config:**
```dart
static const DigiviceEdition edition = DigiviceEdition.master;
```

**Features:**
- ✅ All modules (Terminal, Browser, Messenger)
- ✅ NSFW features
- ✅ Die Mühle secure area
- ✅ Tailscale direct P2P
- ✅ Post-Quantum crypto

**Use Case:** Your personal Digivice

---

### Trusted Edition

**Build Config:**
```dart
static const DigiviceEdition edition = DigiviceEdition.trusted;
```

**Features:**
- ⚙️ Terminal (optional, if has PC)
- ⚙️ Browser PC-Remote (optional, if has PC)
- ✅ Browser Mobile (always available)
- ✅ Messenger (P2P via Tailscale)
- ✅ Die Mühle secure area
- ❌ NSFW (can enable per friend)

**Use Case:** Friends in trusted circle

**Onboarding Flow:**
1. **Tailscale Setup** - Install and connect
2. **Die Mühle Password** - Set secure password
3. **PC Backend** (optional):
   - Do you have a PC? → Yes/No
   - If Yes: Enter Tailscale IP → Test connection
   - If No: Skip (only mobile features)
4. **Done!** - Modules auto-enable based on setup

---

### Public Edition

**Build Config:**
```dart
static const DigiviceEdition edition = DigiviceEdition.public;
```

**Features:**
- ✅ Basic Messenger (via relay server)
- ✅ Signal Protocol E2E encryption
- ❌ No Terminal
- ❌ No Browser
- ❌ No Die Mühle
- ❌ No Tailscale

**Use Case:** App Store release

---

## 🔒 Security Architecture

### Trusted Circle (8 Digivices)

```
┌─────────────────────────────────────────┐
│  TRUSTED CIRCLE                         │
│                                          │
│  All 8 devices in Tailscale mesh        │
│  ├─ Direct P2P encryption               │
│  ├─ No central server needed            │
│  └─ Works with ExpressVPN               │
│                                          │
│  Messaging:                              │
│  ├─ Attempt direct P2P first            │
│  └─ Fallback to relay if P2P fails      │
│                                          │
│  Terminal/Browser:                       │
│  ├─ Each user controls ONLY their PC    │
│  ├─ Via Tailscale IP                    │
│  └─ No cross-user access                │
└─────────────────────────────────────────┘
```

### Public Users

```
┌─────────────────────────────────────────┐
│  PUBLIC USERS                            │
│                                          │
│  Connect via central Signal server      │
│  ├─ E2E encryption (server can't read)  │
│  ├─ Server only relays messages         │
│  └─ Can message trusted circle          │
│                                          │
│  Features:                               │
│  └─ Basic messenger only                │
└─────────────────────────────────────────┘
```

---

## 📊 Feature Matrix

| Feature | Master | Trusted (PC) | Trusted (No PC) | Public |
|---------|--------|--------------|-----------------|--------|
| **Messenger** | ✅ P2P | ✅ P2P | ✅ P2P | ✅ Relay |
| **Terminal** | ✅ | ✅ | ❌ | ❌ |
| **Browser (PC)** | ✅ | ✅ | ❌ | ❌ |
| **Browser (Mobile)** | ✅ | ✅ | ✅ | ❌ |
| **Die Mühle** | ✅ | ✅ | ✅ | ❌ |
| **NSFW** | ✅ | ❌* | ❌ | ❌ |
| **Tailscale** | ✅ | ✅ | ✅ | ❌ |
| **PQ Crypto** | ✅ | ✅ | ✅ | ❌ |

*Can be enabled by changing `hasNSFW` in build_config.dart

---

## 🛠️ Key Components

### 1. Build Configuration System

**File:** `lib/config/build_config.dart`

Controls compile-time features:
```dart
class BuildConfig {
  static const edition = DigiviceEdition.master; // ← Change this

  // Auto-computed feature flags
  static bool get hasMuehle => isTrustedCircle;
  static bool get hasTerminal => isTrustedCircle;
  static bool get hasNSFW => isMaster;
  // ...
}
```

### 2. User Configuration System

**File:** `lib/config/user_config.dart`

Runtime configuration (set during onboarding):
```dart
class UserConfig {
  bool hasPersonalPC = false;           // User has PC?
  String? terminalServerUrl;            // PC Tailscale IP

  // Computed:
  bool get canUseTerminal => hasPersonalPC && terminalServerUrl != null;
  List<SecureModule> get availableModules { ... }
}
```

### 3. Hybrid Messenger Network

**File:** `lib/modules/messenger/messenger_network_service.dart`

Automatic routing:
```dart
enum MessageDeliveryMode {
  directP2P,      // Tailscale (trusted circle)
  relayServer,    // Signal server (public or fallback)
  offline,        // Queue for later
}

// Auto-selects best mode per recipient
Future<bool> sendMessage(recipientId, message) {
  if (both_in_trusted_circle && tailscale_connected) {
    return _sendDirectP2P();
  } else {
    return _sendViaRelay();
  }
}
```

### 4. Dual-Mode Browser

**File:** `lib/modules/browser/browser_screen.dart`

Two modes:
```dart
enum BrowserMode {
  mobile,      // Native WebView (always available)
  pcRemote,    // Stream from PC Firefox (if PC available)
}

// User can switch with toggle button
```

### 5. Smart Onboarding

**File:** `lib/screens/setup/setup_screen.dart`

Multi-step flow:
1. Welcome
2. Tailscale setup (if trusted edition)
3. Die Mühle password (if trusted edition)
4. PC backend setup (optional)
5. Complete

Auto-skips steps not relevant to edition.

### 6. Backend Components

**Browser Control:** `backend/najika_browser_api.py`
- Start/stop Firefox
- Screenshot streaming
- Mouse/keyboard input
- Uses Selenium + pyautogui

**Signal Server:** `backend/najika_signal_server.py`
- HTTP REST API + WebSocket
- Message routing (P2P or relay)
- User discovery
- Offline message queue

---

## 📝 Documentation

| File | Purpose |
|------|---------|
| `README_3_VERSIONS.md` | This file - Quick overview |
| `3_VERSION_SETUP_GUIDE.md` | Complete setup guide (60+ pages) |
| `TERMINAL_MODULE_README.md` | Terminal module documentation |
| `TERMINAL_MODULE_INTEGRATION.md` | Terminal integration guide |

---

## 🔧 Configuration Checklist

### Before Building

**1. Update Server URLs** in `build_config.dart`:
```dart
static String get defaultServerUrl {
  switch (edition) {
    case DigiviceEdition.master:
      return 'https://your-pc-tailscale-ip:8000';  // ← Your PC
    case DigiviceEdition.trusted:
      return '';  // Configured per user during onboarding
    case DigiviceEdition.public:
      return 'https://api.najika-public.com';      // ← Your public server
  }
}

static String get signalServerUrl {
  if (isTrustedCircle) {
    return 'https://your-signal-server:9000';      // ← Your Signal server
  } else {
    return 'https://signal-public.najika.com';     // ← Public Signal server
  }
}
```

**2. Set Build Edition:**
```dart
static const DigiviceEdition edition = DigiviceEdition.master;  // ← Change this
```

**3. Build:**
```bash
./build_all_versions.sh
```

---

## 🚦 Testing Checklist

### Master Edition
- [ ] Die Mühle password works
- [ ] Terminal connects to PC
- [ ] Browser PC-Remote works
- [ ] Messenger sends to friend (P2P)
- [ ] Tailscale IP detected

### Trusted Edition (with PC)
- [ ] Onboarding detects Tailscale
- [ ] PC backend test succeeds
- [ ] Terminal module appears
- [ ] Browser has PC mode
- [ ] Messenger P2P works

### Trusted Edition (without PC)
- [ ] Onboarding skips PC setup
- [ ] Terminal module NOT shown
- [ ] Browser has Mobile mode only
- [ ] Messenger P2P works
- [ ] Die Mühle accessible

### Public Edition
- [ ] No Die Mühle
- [ ] Only basic messenger
- [ ] Messages via relay server
- [ ] No Tailscale prompts

---

## 🎁 What's Included

### Flutter App Components
```
✅ Build configuration system (3 editions)
✅ User configuration system (runtime)
✅ Setup/Onboarding screen
✅ Hybrid messenger network service
✅ Dual-mode browser (Mobile + PC Remote)
✅ Terminal module (from previous implementation)
✅ Die Mühle secure area
```

### Backend Components
```
✅ Browser control API (najika_browser_api.py)
✅ Hybrid Signal server (najika_signal_server.py)
✅ Terminal API (najika_terminal_api.py) - already done
✅ Tor integration (najika_tor.py) - already exists
```

### Documentation
```
✅ 3-Version Setup Guide (comprehensive)
✅ This README
✅ Terminal module docs (previous)
✅ Build scripts (Linux + Windows)
```

---

## 💡 Usage Scenarios

### Scenario 1: You + 7 Friends (All with PCs)

1. Build Master edition for yourself
2. Build Trusted edition × 7 for friends
3. Setup Tailscale mesh (all 16 devices: 8 phones + 8 PCs)
4. Each friend installs their PC backend
5. Everyone has full features

**Result:** 8 fully-featured Digivices with P2P messaging

---

### Scenario 2: You + 7 Friends (Mixed)

- You: PC ✅
- Friend 1: PC ✅
- Friend 2: PC ✅
- Friend 3-7: No PC ❌

1. Same APK for all friends (Trusted edition)
2. Onboarding auto-detects during setup
3. Friends 3-7 get mobile-only features
4. Messaging works for everyone (P2P)

**Result:** Flexible deployment based on hardware

---

### Scenario 3: Private Circle + Public Release

1. You + 7 friends: Trusted circle with Tailscale
2. Public users: Via relay server
3. Public users can message you (via relay)
4. You can message them back

**Result:** Private circle + public compatibility

---

## 🔐 Security Best Practices

1. **Tailscale ACLs:**
   - Restrict PC backend to owner's phone only
   - No cross-user PC access

2. **Die Mühle Password:**
   - Unique per user
   - 8+ characters
   - Store in password manager

3. **Terminal Password:**
   - Separate from Mühle password
   - Required for command execution

4. **Backend Security:**
   - HTTPS only (self-signed OK for Tailscale)
   - Firewall rules: Only Tailscale IPs
   - Keep Python dependencies updated

5. **Signal Server:**
   - Rate limiting
   - Log message metadata only (not content - E2E encrypted)
   - Monitor for abuse

---

## 🆘 Troubleshooting

See `3_VERSION_SETUP_GUIDE.md` → "Troubleshooting" section

Common issues:
- Tailscale not detected → Install Tailscale app
- Terminal not connecting → Check PC backend is running
- Messages not sending → Check Signal server
- Build fails → Run `flutter clean`

---

## 🎉 Congratulations!

You now have:

✅ **3 distinct app editions** from a single codebase
✅ **Modular architecture** that adapts to user's hardware
✅ **Secure P2P messaging** for trusted circle
✅ **Optional PC control** (Terminal + Browser)
✅ **Public compatibility** for wider release

The **8 of you** form a **secure, private mesh network** while still being able to communicate with public users!

---

## 📞 Support

For questions or issues:
1. Check `3_VERSION_SETUP_GUIDE.md` (comprehensive guide)
2. Review module-specific docs (Terminal, Messenger)
3. Test each edition thoroughly before deployment

---

## 🚀 Next Steps

1. **Build all 3 versions** using provided scripts
2. **Setup Tailscale mesh** for trusted circle
3. **Deploy Signal server** on your infrastructure
4. **Test Master edition** on your device
5. **Distribute Trusted edition** to friends
6. **Optional: Prepare Public edition** for App Store

Enjoy your secure Digivice network! 🎯
