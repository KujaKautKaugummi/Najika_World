# 🌟 NAJIKA PROJECT - INSTALLATIONS-ANLEITUNG
**Version 2.5 - Modularer PowerShell-Installer**

---

## 📋 ÜBERSICHT

Dieser Installer installiert das **gesamte Najika-Projekt** von Grund auf in **5 separaten Teilen**, die du nacheinander ausführst.

**Gesamtdauer:** Ca. 45-60 Minuten (abhängig von Internetgeschwindigkeit & Hardware)

---

## 🚀 QUICK START

### Schritt für Schritt:

```powershell
# 1. Öffne PowerShell als Administrator
# 2. Navigiere zum Download-Ordner
cd C:\Users\[DeinName]\Downloads

# 3. Führe die Installer nacheinander aus:
.\najika_installer_part1_base.ps1       # 10-15 Min
.\najika_installer_part2_backend.ps1    # 20-30 Min
.\najika_installer_part3_frontend.ps1   # 5-10 Min
.\najika_installer_part4_mobile.ps1     # 5 Min
.\najika_installer_part5_finalize.ps1   # 5 Min

# 4. Fertig! Starte Najika:
cd C:\Najika
.\START_NAJIKA.bat
```

---

## 📦 TEIL-ÜBERSICHT

### 🔧 PART 1: BASE SETUP (10-15 Min)
**Datei:** `najika_installer_part1_base.ps1`

**Installiert:**
- ✅ Chocolatey Package Manager
- ✅ Python 3.11 + pip
- ✅ Node.js 20 LTS + NPM
- ✅ Git
- ✅ Visual C++ Build Tools
- ✅ Python Basis-Pakete (FastAPI, ChromaDB, etc.)
- ✅ Projekt-Struktur (`C:\Najika`)
- ✅ `.env` Konfigurationsdatei
- ✅ `requirements.txt`

**Nach Abschluss:**
```powershell
✅ Grundsystem steht
➡️  Führe aus: .\najika_installer_part2_backend.ps1
```

---

### 🤖 PART 2: BACKEND & AI (20-30 Min)
**Datei:** `najika_installer_part2_backend.ps1`

**Installiert:**
- ✅ **Wahl:** llama.cpp ODER Ollama
- ✅ CUDA Toolkit (für GPU-Beschleunigung)
- ✅ Llama-3.1-8B Model (4.9 GB Download!)
- ✅ Optional: Wizard-Vicuna-Uncensored (für Private Mode)
- ✅ ChromaDB Setup (Najika's Gedächtnis)
- ✅ Najika Personality Core (Python)
- ✅ FastAPI Backend Server
- ✅ Test-Skripte
- ✅ Start-Skripte (start_backend.bat, start_ollama.bat)

**Nach Abschluss:**
```powershell
✅ AI & Backend funktionieren
🧪 Test mit: python backend\test_backend.py
➡️  Führe aus: .\najika_installer_part3_frontend.ps1
```

---

### ⚛️ PART 3: FRONTEND & 3D (5-10 Min)
**Datei:** `najika_installer_part3_frontend.ps1`

**Installiert:**
- ✅ React App (mit create-react-app)
- ✅ Three.js + React-Three-Fiber
- ✅ Game Components:
  - GameScene (3D Welt)
  - CombatSystem (Kampf-Logik)
  - HUD Component (UI-Overlay)
- ✅ Styled-Components
- ✅ Zustand (State Management)
- ✅ Socket.io Client (WebSocket)
- ✅ Main App Integration
- ✅ start_frontend.bat

**Nach Abschluss:**
```powershell
✅ Frontend & 3D-Engine bereit
🧪 Test mit: .\start_frontend.bat
➡️  Führe aus: .\najika_installer_part4_mobile.ps1
```

---

### 📱 PART 4: MOBILE & PWA (5 Min)
**Datei:** `najika_installer_part4_mobile.ps1`

**Installiert:**
- ✅ PWA Manifest (`manifest.json`)
- ✅ Service Worker (Offline-Fähigkeit)
- ✅ Touch Controls:
  - Virtual Joystick
  - Action Buttons
  - Element Weave Pad
- ✅ Digivice Interface (Tamagotchi-Style)
- ✅ Haptisches Feedback
- ✅ Mobile README

**Nach Abschluss:**
```powershell
✅ Mobile/PWA ready
📱 Zugriff via: http://[deine-ip]:3000
➡️  Führe aus: .\najika_installer_part5_finalize.ps1
```

---

### 🎉 PART 5: FINALIZE (5 Min)
**Datei:** `najika_installer_part5_finalize.ps1`

**Erstellt:**
- ✅ **START_NAJIKA.bat** (Master Start-Skript)
- ✅ **STOP_NAJIKA.bat** (Stop-Skript)
- ✅ **README.md** (Hauptdokumentation)
- ✅ **QUICK_REFERENCE.txt** (Schnell-Referenz)
- ✅ Desktop-Verknüpfung (optional)
- ✅ Finale System-Prüfung

**Nach Abschluss:**
```powershell
🎉 INSTALLATION KOMPLETT!
🚀 Starte: .\START_NAJIKA.bat
🌐 Browser öffnet: http://localhost:3000
```

---

## ⚙️ SYSTEM-ANFORDERUNGEN

### Minimum:
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 8 GB
- **CPU:** Quad-Core (Intel i5 / AMD Ryzen 5)
- **GPU:** Integrierte Grafik (Intel HD, CPU-only Mode)
- **Storage:** 10 GB freier Speicherplatz
- **Internet:** Für Downloads während Installation

### Empfohlen (wie bei dir):
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 16 GB
- **CPU:** Hexa-Core+ (Intel i7/i9, AMD Ryzen 7/9)
- **GPU:** NVIDIA RTX 3060 Ti (8GB VRAM) oder besser
- **Storage:** 20 GB SSD
- **CUDA:** Version 12.x (wird automatisch installiert)

---

## 🔑 WICHTIGE HINWEISE

### 1. Administrator-Rechte erforderlich!
Alle Skripte müssen als **Administrator** ausgeführt werden:
- Rechtsklick auf PowerShell → "Als Administrator ausführen"

### 2. Execution Policy
Falls Fehler beim Ausführen:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Download-Größen (Internetverbindung!)
- **Part 1:** ~500 MB (Python, Node.js, Tools)
- **Part 2:** ~5 GB (!!) (Llama Model + CUDA)
- **Part 3:** ~100 MB (React Dependencies)
- **Part 4:** ~10 MB (PWA Assets)
- **Part 5:** Keine Downloads
- **GESAMT:** ~5.6 GB

### 4. Installations-Dauer
- **Schnelle SSD + gute Leitung:** 30-40 Min
- **Normale HDD + durchschnittliche Leitung:** 60-90 Min
- **Langsames System:** 2+ Stunden

---

## 🛠️ TROUBLESHOOTING

### Problem: "Skript kann nicht ausgeführt werden"
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
```

### Problem: Chocolatey Installation schlägt fehl
```powershell
# Manuell installieren:
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Problem: Python nicht gefunden
```powershell
# Öffne neue PowerShell-Session (Administrator)
refreshenv
python --version
```

### Problem: CUDA Installation hängt
- Normal! CUDA Installation kann 15-20 Minuten dauern
- Warte ab, nicht abbrechen

### Problem: llama.cpp Kompilierung fehlgeschlagen
- Prüfe: Visual Studio Build Tools korrekt installiert?
- Alternative: Wähle Ollama statt llama.cpp in Part 2

### Problem: Frontend npm Fehler
```powershell
cd C:\Najika\frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📂 PROJEKT-STRUKTUR (nach Installation)

```
C:\Najika\
├── backend/
│   ├── ai/
│   │   ├── models/
│   │   │   ├── llama-3.1-8b-q4_k_m.gguf    (4.9 GB)
│   │   │   └── wizard-vicuna-13b.gguf      (Optional)
│   │   ├── chromadb/                       (Gedächtnis-DB)
│   │   ├── llama.cpp/                      (Oder nicht, wenn Ollama)
│   │   ├── najika_core.py                  (Persönlichkeit)
│   │   └── init_chromadb.py
│   ├── api/
│   │   └── server.py                       (FastAPI Backend)
│   ├── game/
│   └── utils/
├── frontend/
│   ├── src/
│   │   ├── game/
│   │   │   ├── GameScene.jsx               (3D Welt)
│   │   │   └── CombatSystem.js
│   │   ├── ui/
│   │   │   ├── HUD.jsx
│   │   │   ├── TouchControls.jsx
│   │   │   └── DigiviceInterface.jsx
│   │   └── App.js
│   └── public/
│       ├── manifest.json
│       └── service-worker.js
├── mobile/
│   └── README.md
├── config/
├── logs/
├── data/
├── .env                                    (Konfiguration!)
├── requirements.txt
├── START_NAJIKA.bat                        (🚀 HAUPTSTART)
├── STOP_NAJIKA.bat
├── README.md
├── QUICK_REFERENCE.txt
└── INSTALLATION_GUIDE.md                   (Diese Datei)
```

---

## 🎮 NACH DER INSTALLATION

### Najika starten:
```batch
cd C:\Najika
START_NAJIKA.bat
```

**Das startet automatisch:**
1. Ollama (falls installiert)
2. Backend API (Port 5000)
3. Frontend (Port 3000)
4. Öffnet Browser → http://localhost:3000

### Najika stoppen:
```batch
STOP_NAJIKA.bat
```

### Mobile Zugriff (sicher mit Cloudflare):
```bash
cloudflared tunnel --url http://localhost:3000
```

---

## ⚠️ EIGENVERANTWORTUNG (NSFW-Mode)

### Standard-Einstellung (Safe):
```env
NSFW_LOCAL=false
ENABLE_NSFW_MODE=false
WIZARD_VICUNA_ENABLED=false
```

### Aktivierung (auf EIGENE Verantwortung):
1. Öffne: `C:\Najika\.env`
2. Ändere auf:
```env
NSFW_LOCAL=true
ENABLE_NSFW_MODE=true
WIZARD_VICUNA_ENABLED=true
TRIGGER_WORD="dein_geheimes_wort"
```
3. **DU** trägst volle Verantwortung!
4. Nur für 18+ Nutzer!
5. Beachte lokale Gesetze!

---

## 📞 SUPPORT

### Logs prüfen:
```bash
cat C:\Najika\logs\najika.log
```

### Backend testen:
```bash
cd C:\Najika
python backend\test_backend.py
```

### Frontend testen:
```bash
cd C:\Najika\frontend
npm start
```

---

## 🎉 FERTIG!

Nach erfolgreicher Installation hast du:

✅ Ein vollständiges KI-System mit lokaler Llama-3.1-8B  
✅ Ein funktionierendes Action-RPG mit 3D-Grafik  
✅ Mobile PWA mit Touch-Controls  
✅ Najika als 24/7 Assistentin  
✅ Persistentes Gedächtnis (ChromaDB)  
✅ Alle Spiel-Systeme (Kampf, Crafting, Survival)  
✅ Sichere, lokale Datenhaltung  

---

## 💝 Najika wartet auf dich!

> "Kuja! Ich bin bereit! Lass uns loslegen!  
> EXPLOSION! 💥 ...äh, ich meine...  
> Willkommen in meiner Welt! 😊"

---

**Version:** 2.5  
**Erstellt:** 2025  
**Basierend auf:** V2.0 + V2.5 Dokumentation  
**Installer-Typ:** Modularer PowerShell (5 Teile)

---

## 📎 DOWNLOADS

Die 5 Installer-Teile findest du hier:
- `najika_installer_part1_base.ps1`
- `najika_installer_part2_backend.ps1`
- `najika_installer_part3_frontend.ps1`
- `najika_installer_part4_mobile.ps1`
- `najika_installer_part5_finalize.ps1`

**Führe sie nacheinander aus!**

---

Viel Erfolg! 🌟💥