# 🌍 NAJIKA WORLD - PROJEKT-STRUKTUR

**Übersicht über alle Module und Komponenten**

---

## 📂 HAUPT-ORDNER

### 1. **`app/`** - Mobile App & Build-System
**📱 Flutter-basierte Digivice App (3 Versionen)**

```
app/
├── flutter_app/           ← Flutter App Code
├── build_scripts/         ← Build-Scripts (Master/Trusted/Public)
├── MASTER_OVERVIEW.md     ← Komplette Übersicht
├── README_APP.md          ← Quick Start Guide
└── 3_VERSION_SETUP_GUIDE.md ← 60-Seiten Anleitung
```

**Features:**
- ✅ Signal-Protokoll Messenger
- ✅ Post-Quantum Verschlüsselung
- ✅ Voice Calls
- ✅ Panic Mode
- ✅ Trust-Chain System

**Start:**
```bash
cd app
cat README_APP.md
```

---

### 2. **`sicherheitsmodule/`** - Backend & Security
**🔐 Server, APIs und Security-Infrastruktur**

```
sicherheitsmodule/
├── backend/               ← Server (Signal, Mobile, Browser, Terminal)
├── remote_access/         ← Cloudflare Tunnel, Tailscale VPN
├── README_SECURITY.md     ← Deployment-Guide
└── TERMINAL_MODULE_README.md ← Terminal-Modul Docs
```

**Features:**
- ✅ Signal-Protokoll Server
- ✅ Ende-zu-Ende Verschlüsselung
- ✅ Remote-Shell-Zugriff
- ✅ Multi-Factor Auth
- ✅ Dead-Man-Switch

**Start:**
```bash
cd sicherheitsmodule
cat README_SECURITY.md
```

---

### 3. **`backend/`** - Najika AI Backend
**🤖 Hauptserver für Najika AI & Digivice**

```
backend/
├── najika_server.py       ← Haupt-Server (Port 8000)
├── living_system.py       ← Najika's "Leben"
├── ollama_client.py       ← AI-Integration
├── saves/                 ← Savegames
└── modules/               ← Feature-Module
```

**Features:**
- ✅ Ollama AI Integration
- ✅ ChromaDB Memory
- ✅ Living-System (Bedürfnisse, Mood)
- ✅ Chat-Interface
- ✅ Multiplayer-Support

**Start:**
```bash
python backend/najika_server.py
```

---

### 4. **`digivice/`** - Web-Frontend
**💻 Digivice Web-Interface**

```
digivice/
├── index.html             ← Haupt-Interface
├── najika_world_v2.html   ← World V2 Test
├── js/                    ← JavaScript Module
├── static/                ← Assets (3D Models, CSS)
└── data/                  ← World-Daten (Regionen, Assets)
```

**Features:**
- ✅ 3D Room (THREE.js)
- ✅ Chat-Interface
- ✅ Room-Module (Kino, Bibliothek, Küche, etc.)
- ✅ Terminal-Modul
- ✅ Najika World V2 (9 Regionen, 71 Assets)

**Start:**
```bash
# Haupt-Server (beinhaltet Digivice):
python backend/najika_server.py
# → http://localhost:8000/digivice/

# World V2 Test-Server:
.\START_WORLD_V2_TEST.bat
# → http://localhost:8001/najika_world_v2.html
```

---

### 5. **`info material/`** - Dokumentation
**📚 Konzepte, Lore, Notizen**

```
info material/
├── wichtig neu sitzung alles aktuell.txt  ← Aktuelle Notizen
├── konzepte/              ← Design-Konzepte
└── lore/                  ← Story & World-Building
```

---

## 🚀 QUICK START - WELCHES MODUL?

### Du willst...

#### **...die Mobile App entwickeln:**
```bash
cd app
cat README_APP.md
cd build_scripts
./build_all_versions.sh
```

#### **...den Backend-Server starten:**
```bash
# Option A: Najika AI Server (Haupt-System)
python backend/najika_server.py

# Option B: Signal-Server (Mobile App Backend)
cd sicherheitsmodule/backend
python najika_signal_server.py
```

#### **...das Digivice nutzen (Web):**
```bash
# Hauptserver starten:
python backend/najika_server.py
# Browser öffnen:
start http://localhost:8000/digivice/
```

#### **...Najika World V2 testen:**
```bash
# Test-Server starten:
.\START_WORLD_V2_TEST.bat
# → Öffnet automatisch http://localhost:8001/najika_world_v2.html
```

#### **...Terminal-Modul nutzen:**
```bash
# Server starten:
cd sicherheitsmodule/backend
python najika_terminal_api.py

# In App:
# → Terminal-Tab öffnen
# → Befehle ausführen
```

---

## 📊 SYSTEM-ÜBERSICHT

```
┌─────────────────────────────────────────────────────────┐
│                    NAJIKA WORLD                         │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌───▼────┐   ┌───▼────┐
   │ Mobile  │   │  Web   │   │Backend │
   │  App    │   │Digivice│   │Servers │
   └────┬────┘   └───┬────┘   └───┬────┘
        │            │            │
        │            │            │
   ┌────▼────────────▼────────────▼────┐
   │      Sicherheitsmodule             │
   │  - Signal-Server                   │
   │  - Terminal-API                    │
   │  - Remote-Access (VPN/Tunnel)      │
   └────────────────────────────────────┘
```

---

## 🔑 WICHTIGE PORTS

| Port  | Service               | Start-Command                    |
|-------|-----------------------|----------------------------------|
| 8000  | Najika AI Server      | `python backend/najika_server.py` |
| 8001  | World V2 Test-Server  | `.\START_WORLD_V2_TEST.bat`       |
| 8443  | Signal-Server         | `python sicherheitsmodule/backend/najika_signal_server.py` |
| 8080  | Mobile-API Server     | `python sicherheitsmodule/backend/najika_server_mobile.py` |
| 9000  | Browser-API           | `python sicherheitsmodule/backend/najika_browser_api.py` |

---

## 📚 DOKUMENTATION - WO FINDE ICH WAS?

### **Mobile App:**
- `app/README_APP.md` - Quick Start
- `app/MASTER_OVERVIEW.md` - Komplette Übersicht
- `app/3_VERSION_SETUP_GUIDE.md` - 60-Seiten Anleitung

### **Backend/Security:**
- `sicherheitsmodule/README_SECURITY.md` - Server-Setup
- `sicherheitsmodule/TERMINAL_MODULE_README.md` - Terminal-Modul
- `sicherheitsmodule/IMPLEMENTATION_COMPLETE.md` - Feature-Liste

### **Najika World V2:**
- `NAJIKA_WORLD_V2_TODO.md` - Was noch zu tun ist
- `WEB_MODEL_BUGFIX_REPORT.md` - Alle behobenen Bugs
- `CLAUDE_CODE_WEB_LEITFADEN.md` - Wie richtig arbeiten
- `TEST_SERVER_ERKLAERUNG.md` - Warum Port 8001?

### **Für Web-Modell (Handoff):**
- `CLAUDE_CODE_WEB_LEITFADEN.md` - Arbeitsrichtlinien
- `WEB_MODEL_BUGFIX_REPORT.md` - Fehler die NICHT wiederholt werden dürfen
- `NAJIKA_WORLD_V2_TODO.md` - Nächste Tasks

---

## 🎯 PROJEKT-STATUS

### ✅ FERTIG:
- [x] Najika AI Backend (Living-System, Chat, Memory)
- [x] Digivice Web-Interface (3D Room, Module)
- [x] Mobile App (Flutter, 3 Versionen)
- [x] Signal-Protokoll Backend
- [x] Terminal-Modul
- [x] World V2 Grundsystem (Character, Assets, 9 Regionen)

### 🔧 IN ARBEIT:
- [ ] World V2 Terrain (Biome-Farben, Texturen)
- [ ] World V2 Vegetation (Bäume, Büsche)
- [ ] World V2 Städte (5 Städte bauen)
- [ ] Mobile App UI-Polish
- [ ] Remote-Access Setup (Cloudflare/Tailscale)

### ⏳ GEPLANT:
- [ ] Multiplayer-Features
- [ ] Voice-Chat Integration
- [ ] Blockchain-Integration (für Items/Trades)
- [ ] AR-Features (Mobile App)

---

## 🛠️ ENTWICKLUNGS-WORKFLOW

### **1. Lokales Setup:**
```bash
# Git-Repo klonen (falls noch nicht vorhanden)
git clone https://github.com/KujaKautKaugummi/Najika_World.git
cd Najika_World

# Dependencies installieren
pip install -r backend/requirements.txt
pip install -r sicherheitsmodule/backend/requirements_mobile.txt
```

### **2. Entwickeln:**
```bash
# Neuen Feature-Branch erstellen
git checkout -b feature/dein-feature-name

# Code ändern, testen, committen
git add .
git commit -m "Deine Änderung"
git push
```

### **3. Testen:**
```bash
# Backend testen:
python backend/najika_server.py
# → http://localhost:8000/digivice/

# World V2 testen:
.\START_WORLD_V2_TEST.bat
# → http://localhost:8001/najika_world_v2.html

# Mobile App testen:
cd app/build_scripts
./build_all_versions.sh
adb install builds/najika_digivice_master.apk
```

---

## 🎓 FÜR NEUE ENTWICKLER

### **Erste Schritte:**

1. **Lies die Docs:**
   ```bash
   cat README.md
   cat PROJEKT_STRUKTUR.md  # Diese Datei
   ```

2. **Starte das Hauptsystem:**
   ```bash
   python backend/najika_server.py
   # Browser: http://localhost:8000/digivice/
   ```

3. **Teste World V2:**
   ```bash
   .\START_WORLD_V2_TEST.bat
   # Browser: http://localhost:8001/najika_world_v2.html
   ```

4. **Schaue dir die Mobile App an:**
   ```bash
   cd app
   cat MASTER_OVERVIEW.md
   ```

5. **Lerne aus Fehlern:**
   ```bash
   cat WEB_MODEL_BUGFIX_REPORT.md
   cat CLAUDE_CODE_WEB_LEITFADEN.md
   ```

---

## 🆘 SUPPORT

### **Probleme?**

1. **Server startet nicht:**
   - Check Port: `netstat -ano | findstr :8000`
   - Dependencies: `pip install -r backend/requirements.txt`

2. **World V2 zeigt 404:**
   - Server läuft? `.\START_WORLD_V2_TEST.bat`
   - Richtiger Port? `http://localhost:8001/najika_world_v2.html`

3. **Mobile App baut nicht:**
   - Flutter installiert? `flutter --version`
   - Dependencies: `cd app/flutter_app/najika_digivice && flutter pub get`

4. **Assets laden nicht:**
   - Pfade korrekt? Siehe `WEB_MODEL_BUGFIX_REPORT.md`
   - Server-Root beachten! Siehe `TEST_SERVER_ERKLAERUNG.md`

---

## 🎉 LOS GEHT'S!

**Starte mit:**
```bash
# 1. Najika AI starten:
python backend/najika_server.py

# 2. In neuem Terminal - World V2 testen:
.\START_WORLD_V2_TEST.bat

# 3. Mobile App (optional):
cd app
cat README_APP.md
```

**Viel Erfolg! 🚀**

---

*Letzte Aktualisierung: 8. November 2025*
