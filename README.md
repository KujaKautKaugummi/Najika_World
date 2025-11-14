# Najika Digivice - Unreal Engine 5 Mobile Game

**Platform:** Android (ARM64)
**Engine:** Unreal Engine 5.3+
**Target Device:** Xiaomi 11T Pro (and compatible devices)
**Status:** ✅ **Ready for Development**

---

## 📋 Project Overview

Najika Digivice ist ein mobiles Action-RPG Game entwickelt mit Unreal Engine 5 für Android-Geräte. Das Projekt beinhaltet zwei C++ Plugins für Backend-Integration und Voice-Chat, sowie umfassende Dokumentation und Deployment-Tools.

### Features

✅ **Backend Integration** - HTTP REST & WebSocket Client
✅ **Voice Chat System** - Real-time Voice mit Whisper AI Transkription
✅ **Multi-User Support** - Multiplayer-ready Architektur
✅ **Mobile Optimized** - Speziell für Xiaomi 11T Pro optimiert
✅ **Complete Documentation** - 7 umfassende Guides (~8.000 Zeilen)
✅ **Production Ready** - Testing, Deployment, CI/CD vorbereitet

---

## 🚀 Quick Start

### 1. Prerequisites

Installiere folgende Software:

- **Unreal Engine 5.3+** (via Epic Games Launcher)
- **Visual Studio 2022** (mit C++ Game Development Workload)
- **Android Studio** (für SDK/NDK)
- **Git** (für Version Control)

### 2. Clone Repository

```bash
git clone https://github.com/KujaKautKaugummi/Najika_World.git
cd Najika_World
```

### 3. Deploy Plugins

Führe das PowerShell Deployment Script aus:

```powershell
cd UE5_Implementation
.\COPY_TO_UE5_PROJECT.ps1 -ProjectPath "C:\Path\To\Your\UE5\Project"
```

### 4. Open UE5 Project

1. Navigate zu deinem UE5 Projekt-Ordner
2. Öffne die `.uproject` Datei
3. Bestätige Plugin-Aktivierung
4. Warte bis Editor startet

### 5. Compile C++ Code

Öffne die `.sln` Datei in Visual Studio:

```
Right-Click auf .uproject → Generate Visual Studio project files
Öffne .sln → Build > Build Solution (Ctrl+Shift+B)
```

### 6. Start Backend (Optional)

Wenn du das optionale Backend nutzen möchtest:

```bash
cd OPTIONAL_Backend
pip install -r requirements.txt
python main.py
```

Backend läuft auf `http://localhost:8000`

---

## 📁 Repository Structure

```
Najika_World/
├── UE5_Implementation/                    # Hauptimplementierung
│   ├── Plugins/
│   │   ├── NajikaBackendClient/           # Backend Integration Plugin
│   │   └── NajikaVoiceSystem/             # Voice Chat Plugin
│   ├── BLUEPRINT_CREATION_GUIDE.md        # Blueprint Schritt-für-Schritt
│   ├── ASSET_REQUIREMENTS.md              # Asset Spezifikationen
│   ├── VISUAL_STUDIO_COMPILATION_GUIDE.md # C++ Kompilierung
│   ├── ANDROID_BUILD_GUIDE.md             # APK Building
│   ├── TESTING_CHECKLIST.md               # Test Procedures
│   ├── VOICE_BACKEND_API_SPEC.md          # Voice API Doku
│   ├── IMPLEMENTATION_SUMMARY.md          # ⭐ START HIER!
│   └── COPY_TO_UE5_PROJECT.ps1            # Deployment Script
│
├── OPTIONAL_Backend/                      # [OPTIONAL] Python Backend
│   ├── main.py                            # FastAPI Server
│   ├── requirements.txt                   # Dependencies
│   └── README.md                          # Backend Setup
│
├── WEB_MODEL_FINAL_ROUND_TODO.md          # Phase 9-15 Spezifikation
└── README.md                              # Diese Datei
```

---

## 📖 Documentation

Alle Dokumentation ist in `UE5_Implementation/` verfügbar:

| Datei | Zweck | Zeilen |
|-------|-------|--------|
| **IMPLEMENTATION_SUMMARY.md** | ⭐ **START HIER** - Kompletter Überblick | 650 |
| **BLUEPRINT_CREATION_GUIDE.md** | Blueprints erstellen (9 Blueprints) | 2.200 |
| **ASSET_REQUIREMENTS.md** | Asset-Spezifikationen & Quellen | 1.500 |
| **VISUAL_STUDIO_COMPILATION_GUIDE.md** | C++ Code kompilieren | 950 |
| **ANDROID_BUILD_GUIDE.md** | APK bauen & deployen | 1.350 |
| **TESTING_CHECKLIST.md** | Testing & Validation | 1.100 |
| **VOICE_BACKEND_API_SPEC.md** | Voice System API | 850 |

### 🎯 Empfohlene Lesereihenfolge

1. **IMPLEMENTATION_SUMMARY.md** - Überblick über alles
2. **VISUAL_STUDIO_COMPILATION_GUIDE.md** - C++ Setup
3. **BLUEPRINT_CREATION_GUIDE.md** - Blueprints erstellen
4. **ANDROID_BUILD_GUIDE.md** - APK bauen
5. **TESTING_CHECKLIST.md** - Testen

---

## 🛠️ Development Workflow

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Make changes in UE5 Editor or Visual Studio

# 3. Compile C++ (if changed)
# In Visual Studio: Ctrl+Shift+B

# 4. Test in Editor
# In UE5: Press Play (Alt+P)

# 5. Commit changes
git add .
git commit -m "Description of changes"
git push
```

### Building for Android

```bash
# 1. Package APK (Development)
# In UE5: Platforms > Android > Package Project

# 2. Deploy to device
cd <Build Output Dir>
adb install -r YourGame.apk

# 3. Test on device
adb logcat | grep "Najika"
```

---

## 🎮 Plugins

### NajikaBackendClient

**Purpose:** HTTP REST & WebSocket Client für Backend-Integration

**Features:**
- JWT Authentication
- HTTP Request Handler
- WebSocket Client
- Inventory Management
- Player Data Sync

**Usage:**
```cpp
UNajikaHttpClient* Client = GetGameInstance()->GetSubsystem<UNajikaBackendSubsystem>()->GetHttpClient();
Client->SendLoginRequest("username", "password");
```

### NajikaVoiceSystem

**Purpose:** Real-time Voice Chat & Speech-to-Text

**Features:**
- Microphone Capture mit VAD
- Noise Suppression & Echo Cancellation
- Audio Encoding (Opus/PCM16)
- WebSocket Voice Streaming
- Whisper AI Integration

**Usage:**
```cpp
UNajikaVoiceComponent* VoiceComp = Character->FindComponentByClass<UNajikaVoiceComponent>();
VoiceComp->InitializeVoiceSystem(48000);
VoiceComp->StartVoiceCall();
```

---

## 🧪 Testing

### Unit Tests

Run unit tests in UE5:

1. **Window > Test Automation**
2. Filter: `Najika`
3. Select all tests
4. Click **Start Tests**

Expected: ✅ All tests pass (20+ tests)

### Integration Tests

Follow `TESTING_CHECKLIST.md` for complete test procedures:
- ✅ Login Flow
- ✅ Inventory Retrieval
- ✅ Voice Chat
- ✅ Performance Tests

### Device Testing

Deploy to Xiaomi 11T Pro:

```bash
# Install APK
adb install -r NajikaDigivice.apk

# Monitor logs
adb logcat | findstr "Najika"

# Test backend connection
adb reverse tcp:8000 tcp:8000
```

---

## 📦 Deployment

### Development Build

```bash
# In UE5 Editor
Platforms > Android > Package Project (Development)
```

### Shipping Build

```bash
# 1. Change configuration to Shipping
# In UE5: Platforms > Android > Packaging Settings > Build Configuration = Shipping

# 2. Package
Platforms > Android > Package Project (for Distribution)

# 3. Sign APK (see ANDROID_BUILD_GUIDE.md)
```

---

## 🔧 Troubleshooting

### Common Issues

#### Plugin Not Loading

```
Error: Plugin 'NajikaBackendClient' failed to load
```

**Solution:**
1. Close UE5 Editor
2. Delete `Binaries/`, `Intermediate/`, `Saved/`
3. Rebuild in Visual Studio
4. Reopen UE5

#### Compilation Errors

```
Error LNK2019: unresolved external symbol
```

**Solution:**
- Check `.Build.cs` has all required modules
- Verify function implementation exists in `.cpp`
- Clean and rebuild solution

#### APK Not Installing

```
Installation failed with error: INSTALL_FAILED_INSUFFICIENT_STORAGE
```

**Solution:**
- Free up device storage
- Or install to SD card (change Install Location in Project Settings)

Für mehr Solutions siehe **VISUAL_STUDIO_COMPILATION_GUIDE.md** und **ANDROID_BUILD_GUIDE.md**.

---

## 🤝 Contributing

Dieses Projekt wurde für ein spezifisches Ziel entwickelt, aber Contributions sind willkommen:

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit deine Changes (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

---

## 📊 Project Status

### Phases Completed

| Phase | Deliverable | Status |
|-------|-------------|--------|
| Phase 0-8 | NajikaBackendClient Plugin | ✅ Complete |
| **Phase 9** | NajikaVoiceSystem Plugin | ✅ Complete |
| **Phase 10** | Blueprint Creation Guide | ✅ Complete |
| **Phase 11** | Asset Requirements | ✅ Complete |
| **Phase 12** | Copy & Setup Scripts | ✅ Complete |
| **Phase 13** | VS Compilation Guide | ✅ Complete |
| **Phase 14** | Android Build Guide | ✅ Complete |
| **Phase 15** | Testing Checklist | ✅ Complete |
| **Bonus** | Voice API Spec, Tests, Summary | ✅ Complete |
| **Optional** | Backend, Fixes, Utils | ✅ Complete |

**Total Lines:** 12.000+ lines of code & documentation

### Next Steps

- [ ] Acquire/Import Assets (see ASSET_REQUIREMENTS.md)
- [ ] Create Blueprints (see BLUEPRINT_CREATION_GUIDE.md)
- [ ] Implement Gameplay Logic
- [ ] Performance Optimization
- [ ] User Acceptance Testing

---

## 📝 License

Dieses Projekt ist Teil der Najika Development Arbeit.

---

## 📞 Support

### Documentation

Alle Guides sind in `UE5_Implementation/` verfügbar. Start mit:
- **IMPLEMENTATION_SUMMARY.md** - Kompletter Überblick

### Issues

Bei Problemen oder Fragen:
1. Check Documentation (TROUBLESHOOTING Sektionen)
2. Search Unreal Engine AnswerHub
3. Open ein Issue auf GitHub

### Resources

- **UE5 Documentation:** https://docs.unrealengine.com/5.3/
- **Android Development:** https://developer.android.com/guide
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

## 🎯 Architecture

```
┌─────────────────────────────────────────────────┐
│          UE5 Client (Xiaomi 11T Pro)            │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │   Blueprints     │  │   C++ Plugins    │   │
│  │                  │  │                  │   │
│  │ - BP_Character   │  │ - Backend Client │   │
│  │ - BP_Controller  │  │ - Voice System   │   │
│  │ - WBP_HUD        │  │                  │   │
│  └────────┬─────────┘  └────────┬─────────┘   │
│           │                     │             │
│           └─────────┬───────────┘             │
│                     ▼                         │
└─────────────────────┼─────────────────────────┘
                      │
            HTTP / WebSocket
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│         Backend Server (localhost:8000)         │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │   FastAPI        │  │  WebSocket       │   │
│  │                  │  │                  │   │
│  │ - Auth           │  │ - Voice Rooms    │   │
│  │ - Inventory      │  │ - Audio Forward  │   │
│  │ - User Data      │  │                  │   │
│  └──────────────────┘  └──────────────────┘   │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │   Database       │  │   Whisper AI     │   │
│  │   (SQLite)       │  │   (Speech-to-Text)│   │
│  └──────────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

**Made with ❤️ for Najika Development**

*Letztes Update: Januar 2025*
