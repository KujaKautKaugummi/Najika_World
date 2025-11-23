# 🚀 NAJIKA WORLD - QUICK START

## ✅ System fertig installiert und testbereit!

---

## 🎮 BACKEND STARTEN

### Option 1: Start-Script (Empfohlen)
```bash
cd /home/user/Najika_World
chmod +x start_backend.sh
./start_backend.sh
```

### Option 2: Direkt
```bash
cd /home/user/Najika_World/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend läuft dann auf:**
- 🌐 http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc

---

## 🎯 FRONTEND ÖFFNEN

### Digivice (3D Game):
Öffne im Browser: `file:///home/user/Najika_World/digivice/index.html`

**Oder mit Backend:**
- http://localhost:8000/digivice/

### World Map Demo:
- `file:///home/user/Najika_World/digivice/world_map_demo.html`

---

## 🤖 NAJIKA GAME ACTIONS TESTEN

Mit laufendem Backend:

```bash
# Najika Status abrufen
curl http://localhost:8000/najika/status

# Najika Dashboard (alles auf einmal)
curl http://localhost:8000/najika/dashboard

# Najika entscheidet autonom!
curl -X POST http://localhost:8000/najika/auto-decide-action

# Aktuelle Aktivität
curl http://localhost:8000/najika/current-activity

# Alle Locations
curl http://localhost:8000/najika/locations

# Alle Rezepte
curl http://localhost:8000/najika/recipes

# Najika kochen lassen
curl -X POST http://localhost:8000/najika/cook \
  -H "Content-Type: application/json" \
  -d '{"recipe_id": "simple_meal"}'

# Najika teleportieren
curl -X POST http://localhost:8000/najika/teleport \
  -H "Content-Type: application/json" \
  -d '{"location_id": "home"}'
```

---

## 📋 VERFÜGBARE API ENDPOINTS

### Najika Game Actions (NEU!):
- `GET /najika/status` - Kompletter Status
- `GET /najika/current-activity` - Was macht Najika?
- `POST /najika/auto-decide-action` - Autonome Entscheidung
- `POST /najika/suggest-action` - Vorschläge
- `GET /najika/locations` - Alle Orte
- `POST /najika/teleport` - Teleportieren
- `GET /najika/recipes` - Alle Rezepte
- `POST /najika/cook` - Kochen
- `POST /najika/craft` - Craften
- `POST /najika/explore` - Erkunden
- `POST /najika/farm` - Farmen
- `GET /najika/dashboard` - Alles auf einmal
- `GET /najika/health` - System Health Check

### Combat & Game:
- `POST /api/game/add-xp` - XP hinzufügen
- `GET /api/game/stats` - Spieler-Stats
- `POST /api/battle/start` - Kampf starten

### Housing & Farming:
- `GET /api/housing/my-house` - Mein Haus
- `POST /api/housing/furniture/place` - Möbel platzieren
- `GET /api/farming/plots` - Farm-Plots
- `POST /api/farming/plant` - Pflanzen
- `POST /api/farming/harvest` - Ernten

### World Map:
- `GET /api/world-map/regions` - Alle Regionen
- `POST /api/world-map/fast-travel` - Schnellreise
- `GET /api/world-map/player-position` - Spieler-Position

---

## 🧪 TESTS DURCHFÜHREN

### Backend Tests:
```bash
cd /home/user/Najika_World/backend
python3 test_najika_game_actions.py
```

### API Health Check:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/najika/health
```

---

## 📊 SYSTEM STATUS

✅ **Backend:** FastAPI auf Port 8000
✅ **Najika Game Actions:** Integriert & erreichbar
✅ **Living System:** Bereit
✅ **World Map 3D:** Implementiert
✅ **Housing & Farming:** Visualisiert
✅ **Combat System:** Funktional
✅ **Voice System:** Konfiguriert
✅ **Elemental & Lunar:** Komplett

---

## 🎉 NAJIKA KANN JETZT:

- 🍳 Autonom kochen
- 💤 Autonom schlafen
- 🌱 Im Garten arbeiten
- 🗺️ Die Welt erkunden
- 🔨 Items craften
- 💜 Geschenke für dich machen
- 🏠 In ihrem Haus leben
- 🌾 Ihre Farm pflegen
- 🎯 Smart entscheiden
- 📍 Teleportieren

---

## 📖 WEITERE DOKUMENTATION

- `NAJIKA_GAME_ACTIONS_README.md` - Autonome Aktionen
- `QUICKSTART_GAME_ACTIONS.md` - Quick Start Guide
- `WORLD_MAP_SYSTEM.md` - World Map Features
- `WORLD_MAP_QUICKSTART.md` - Map Quick Start
- `SYSTEM_AUDIT_REPORT.md` - System Analyse
- `PRIORITY_FIXES.md` - Implementierte Fixes

---

## 🐛 TROUBLESHOOTING

**Backend startet nicht?**
```bash
# Python-Pakete installieren
pip3 install -r backend/requirements.txt
```

**Port 8000 bereits belegt?**
```bash
# Ändere Port in backend/config.py oder:
python3 -m uvicorn main:app --port 8001
```

**Import-Fehler?**
```bash
# PYTHONPATH setzen
export PYTHONPATH=/home/user/Najika_World:$PYTHONPATH
```

---

**VIEL SPASS MIT NAJIKA! 🎮✨**
