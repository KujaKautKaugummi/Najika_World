# 📱 NAJIKA DIGIVICE - MOBILE APP

**Flutter-basierte Mobile App für das Najika World Projekt**

## 📦 Inhalt

### 1. Flutter App (`flutter_app/`)
Die komplette Flutter-App mit allen Modulen:
- **Messenger** - Signal-Protokoll verschlüsselte Kommunikation
- **Voice Calls** - Verschlüsselte Sprachanrufe
- **Panic Mode** - Notzerstörungs-Mechanismus
- **Security Checks** - Integritätsprüfungen
- **Post-Quantum Crypto** - Zukunftssichere Verschlüsselung

### 2. Build-Scripts (`build_scripts/`)
Scripts zum Bauen der 3 App-Versionen:

#### **3 Versionen:**
```bash
# 1. Master-Version (nur für dich)
./build_scripts/build_private.sh
# → Vollzugriff, alle Features, keine Beschränkungen

# 2. Trusted-Version (für 7 Freunde)
./build_scripts/build_friends.sh
# → Verschlüsselte Kommunikation untereinander
# → Trust-Chain basiert auf deinem Master-Key

# 3. Public-Version (für alle anderen)
./build_scripts/build_public.sh
# → Normale Funktionen
# → Keine Trust-Features
```

#### **Alle Versionen bauen:**
```bash
# Linux/macOS:
chmod +x build_scripts/build_all_versions.sh
./build_scripts/build_all_versions.sh

# Windows:
.\build_scripts\build_all_versions.ps1
```

**Erstellt:**
```
builds/
├── najika_digivice_master.apk      ← Für dich
├── najika_digivice_trusted.apk     ← Für alle 7 Freunde
└── najika_digivice_public.apk      ← Für öffentlich
```

### 3. Dokumentation

| Datei | Beschreibung |
|-------|-------------|
| `MASTER_OVERVIEW.md` | Komplette Übersicht über ALLES |
| `README_3_VERSIONS.md` | Quick Start für 3 Versionen |
| `3_VERSION_SETUP_GUIDE.md` | 60-Seiten Komplettanleitung |

## 🚀 Quick Start

### Schritt 1: Dokumentation lesen
```bash
cat MASTER_OVERVIEW.md
```

### Schritt 2: Apps bauen
```bash
cd build_scripts
./build_all_versions.sh
```

### Schritt 3: Backend starten
```bash
# Backend im sicherheitsmodule/ Ordner starten
cd ../sicherheitsmodule/backend
python najika_signal_server.py
```

### Schritt 4: App installieren
```bash
# Master-Version (nur für dich)
adb install builds/najika_digivice_master.apk

# Oder Trusted-Version (für Freunde)
adb install builds/najika_digivice_trusted.apk
```

## 🔑 Wichtige Features

### Security-First Design
- ✅ **Signal-Protokoll** - Ende-zu-Ende Verschlüsselung
- ✅ **Double Ratchet** - Forward Secrecy
- ✅ **Post-Quantum Crypto** - Kyber-1024 + X25519
- ✅ **Panic Mode** - Sofort-Zerstörung aller Daten

### Trust-Chain System
- ✅ **Master-Key** - Dein Root-Schlüssel
- ✅ **Friend-Keys** - Abgeleitet vom Master-Key
- ✅ **Trust-Levels** - Unterschiedliche Zugriffsstufen

### Messenger-Funktionen
- ✅ **1-zu-1 Chats** - Verschlüsselte Nachrichten
- ✅ **Gruppenchats** - Bis zu 8 Personen
- ✅ **Voice Calls** - Verschlüsselte Anrufe
- ✅ **Datei-Sharing** - Verschlüsselt, bis 100MB

## 📊 App-Struktur

```
flutter_app/najika_digivice/lib/
├── core/
│   ├── constants/      ← App-Konstanten
│   └── theme/          ← UI-Theme
├── modules/
│   ├── home/           ← Home-Screen
│   ├── messenger/      ← Chat & Messaging
│   ├── panic/          ← Panic-Mode
│   └── security/       ← Security-Checks
└── services/
    ├── calls/          ← Voice Calls
    ├── crypto/         ← Verschlüsselung
    ├── network/        ← Netzwerk
    ├── security/       ← Security-Service
    └── storage/        ← Secure Storage
```

## 🔧 Requirements

### Development:
- Flutter SDK >= 3.0
- Dart >= 3.0
- Android Studio / Xcode
- Android SDK / iOS SDK

### Backend:
- Python >= 3.9
- (Siehe `sicherheitsmodule/backend/requirements_mobile.txt`)

## 📚 Weitere Ressourcen

**Im `app/` Ordner:**
- `MASTER_OVERVIEW.md` - Übersicht über ALLES
- `README_3_VERSIONS.md` - 3-Versions-System erklärt
- `3_VERSION_SETUP_GUIDE.md` - Komplettanleitung (60 Seiten)
- `MASTER_INSTALLER.sh` - Automatisches Setup-Script

**Im `sicherheitsmodule/` Ordner:**
- Backend-Server und APIs
- Remote-Access (Cloudflare, Tailscale)
- Terminal-Modul Dokumentation

## 🎯 Nächste Schritte

1. **Lies die Docs:**
   ```bash
   cat MASTER_OVERVIEW.md
   ```

2. **Baue die Apps:**
   ```bash
   cd build_scripts
   ./build_all_versions.sh
   ```

3. **Starte das Backend:**
   ```bash
   cd ../sicherheitsmodule/backend
   python najika_signal_server.py
   ```

4. **Installiere & Teste:**
   ```bash
   adb install builds/najika_digivice_master.apk
   ```

---

**Viel Erfolg! 🚀**

*Für Fragen siehe `MASTER_OVERVIEW.md` oder die anderen Docs.*
