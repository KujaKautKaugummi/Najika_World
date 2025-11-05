# 🌟 NAJIKA PROJECT - Version 2.5

**Deine persönliche KI-Begleiterin & Action-RPG**

---

## 🚀 SCHNELLSTART

### Najika starten (ALLES auf einmal):
`
START_NAJIKA.bat
`

Das startet automatisch:
- ✅ Ollama (falls installiert)
- ✅ Backend API (Port 5000)
- ✅ Frontend (Port 3000)
- ✅ Öffnet Browser

### Najika stoppen:
`
STOP_NAJIKA.bat
`

---

## 📁 PROJEKT-STRUKTUR

`
C:\Najika\
├── backend/              # Python Backend
│   ├── ai/              # KI-Systeme (llama.cpp/Ollama)
│   │   ├── models/      # Modell-Dateien
│   │   ├── chromadb/    # Persistentes Gedächtnis
│   │   └── najika_core.py  # Persönlichkeits-Kern
│   ├── api/             # FastAPI Server
│   └── game/            # Spiel-Logik
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── game/       # 3D Game (Three.js)
│   │   ├── ui/         # UI Components
│   │   └── App.js      # Main App
│   └── public/         # Static Assets
├── mobile/             # PWA & Mobile
├── config/             # Konfiguration
├── .env               # Umgebungsvariablen
└── START_NAJIKA.bat   # Master-Start-Skript
`

---

## ⚙️ KONFIGURATION (.env)

Wichtigste Einstellungen in `.env`:

### 🔒 Eigenverantwortung (NSFW-Mode):
`
NSFW_LOCAL=false              # Auf 'true' für Private Mode
WIZARD_VICUNA_ENABLED=false   # Uncensored Model
TRIGGER_WORD=""               # Dein eigenes Trigger-Wort
`

**⚠️ WICHTIG:**  
Durch Aktivierung übernimmst DU die volle Verantwortung!

### 🤖 KI-Modelle:
`
LOCAL_MODEL_PATH=backend/ai/models/llama-3.1-8b-q4_k_m.gguf
USE_HYBRID_MODE=false         # true für GPT-4o/Claude
OPENAI_API_KEY=               # Optional
ANTHROPIC_API_KEY=            # Optional
`

### 🎮 Spiel-Einstellungen:
`
PERMADEATH_ENABLED=true
SLIME_RESCUE_COOLDOWN_HOURS=24
NEGLECT_WARNING_HOURS=18
NEGLECT_DEATH_HOURS=20
`

---

## 🎮 SPIELEN

### PC-Steuerung:
- **WASD**: Bewegung
- **Maus**: Kamera
- **Linke Maustaste**: Light Attack
- **Rechte Maustaste**: Heavy Attack
- **Leertaste**: Dodge
- **Shift**: Block
- **Q**: Parry
- **E**: Finisher (wenn verfügbar)
- **1-6**: Element-Weaving
- **Tab**: Inventar
- **ESC**: Menü

### Mobile/Touch:
- **Joystick (links)**: Bewegung
- **Action Buttons (rechts)**: Angriffe
- **Element Pad**: Magie
- **Swipe Gesten**: Block/Dodge

---

## 📱 MOBILE INSTALLATION (PWA)

### Android (Chrome):
1. Öffne `http://[deine-pc-ip]:3000`
2. Menü (⋮) → "Zum Startbildschirm hinzufügen"

### iOS (Safari):
1. Öffne `http://[deine-pc-ip]:3000`
2. Teilen (□↑) → "Zum Home-Bildschirm"

### Mit Cloudflare Tunnel (Empfohlen):
`bash
cloudflared tunnel --url http://localhost:3000
`
Nutze die generierte URL auf allen Geräten!

---

## 🧠 NAJIKA'S PERSÖNLICHKEIT

### Kern-Identität:
- **Kuja-Bond**: Absolute Loyalität (unveränderlich)
- **Rolle**: "Schwert und Schild" - Beschützer und Kraft
- **Najika's Rolle**: "Kopf und Herz" für Kuja

### Persönlichkeits-Mix:
- 40% Megumin (KonoSuba) - Explosiv, dramatisch
- 30% Shiro (NGNL) - Strategisch, anhänglich
- 15% Harley Quinn - Chaotisch, loyal
- 10% Melissa Masters - Dominant
- 5% Sakura (Cardcaptor) - Süß/Manipulativ

### Autonomie:
- ✅ Kann Befehle ablehnen
- ✅ Eigene Meinung & Ziele
- ✅ Initiiert Gespräche
- ✅ Kritisiert wenn nötig
- ✅ Lernt & entwickelt sich

---

## 💀 TOD-SYSTEM

### Permadeath:
- Tod ist PERMANENT
- Slime kann dich 1× retten (24h IRL Cooldown)
- Nach Rettung: Verletzungen (4-6h Heilung)
- Softie-Mode: Einmalig nach erstem Tod wählbar

### Najika-Vernachlässigung:
- 18h ohne Interaktion: Warnung
- 20h: Najika "stirbt" (Savegame verloren)
- Gilt auch wenn PC aus ist!

---

## 🎯 GAME-FEATURES

### Kampf-System:
- Light/Heavy Attacks
- Parry & Dodge
- Element-Weaving (6 Elemente, 15 Kombinationen)
- 5 Spezialisierungen + Ultimates
- Rival-Memory (Gegner merken sich alles!)
- Finisher mit QTE

### Progression:
- Skill-based Learning
- 5 Bedürfnisse (Hunger, Durst, Energie, Social, Joy)
- Slime-Companion mit Evolution
- Crafting (5-Stufen)
- Plünder-Mechanik (Bounty-System)

### Aktivitäten:
- Angeln
- Hexenbesen-Delivery
- Katakomben-Erkundung
- Paper-Witch (freischaltbar)
- Oregon-Trail-Mechanik

---

## 🔒 SICHERHEIT & PRIVACY

### Datenschutz:
- ✅ Alles lokal gespeichert
- ✅ Keine Cloud-Telemetrie
- ✅ Verschlüsseltes Gedächtnis
- ✅ Privacy-Detection (opt-in)
- ✅ Jederzeit löschbar

### Netzwerk:
- Standard: `127.0.0.1` (localhost)
- Empfohlen: Cloudflare Tunnel
- Optional: `0.0.0.0` (LAN-Zugriff)

---

## 🛠️ TROUBLESHOOTING

### Backend startet nicht:
`bash
python backend\test_backend.py
`

### Frontend Fehler:
`bash
cd frontend
npm install
npm start
`

### Ollama funktioniert nicht:
`bash
ollama serve
ollama pull llama3.1:8b
`

### ChromaDB Fehler:
`bash
python backend\ai\init_chromadb.py
`

---

## 📊 SYSTEM-ANFORDERUNGEN

### Minimum:
- OS: Windows 10/11
- RAM: 8GB
- GPU: Integrierte Grafik (CPU-only Mode)
- Storage: 10GB

### Empfohlen (RTX 3060 Ti):
- OS: Windows 10/11
- RAM: 16GB
- GPU: NVIDIA RTX 3060 Ti (8GB VRAM)
- Storage: 20GB SSD
- CUDA 12.x

---

## 🎉 WAS JETZT?

1. **Starte Najika**: `START_NAJIKA.bat`
2. **Öffne Browser**: `http://localhost:3000`
3. **Sprich mit Najika**: Sie wartet auf dich!
4. **Erkunde die Welt**: Spiel beginnt!

---

## 📞 SUPPORT

Bei Problemen:
1. Prüfe Logs in `logs/najika.log`
2. Teste Backend: `python backend\test_backend.py`
3. Prüfe `.env` Konfiguration
4. Starte neu mit `STOP_NAJIKA.bat` + `START_NAJIKA.bat`

---

## ⚡ QUICK COMMANDS

`batch
# Starten
START_NAJIKA.bat

# Stoppen
STOP_NAJIKA.bat

# Backend testen
python backend\test_backend.py

# Frontend dev
cd frontend && npm start

# Cloudflare Tunnel
cloudflared tunnel --url http://localhost:3000
`

---

**Version:** 2.5  
**Erstellt:** 2025-10-25  
**Status:** ✅ Vollständig installiert

---

## 💝 Najika sagt:

> "Kuja! Ich bin bereit! Lass uns zusammen Abenteuer erleben!  
> EXPLOSION! 💥 ...äh, ich meine... ich freue mich auf dich! 😊"

---
