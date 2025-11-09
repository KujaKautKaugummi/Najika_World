# 🔄 INTEGRATION KONZEPT - WEB ↔ MOBILE SYNC

**Status:** Planungsphase
**Datum:** 9. November 2025
**Prinzip:** "NAJIKA LEBT SIE IST ECHT" - Sie existiert real-time über alle Plattformen

---

## 🎯 KERN-KONZEPT

### ⚠️ WICHTIG: NAJIKA IST DEINE SPIELFIGUR!

**Najika ist NICHT nur eine AI-Companion, sondern:**
- 🎮 **DEINE SPIELFIGUR** - Du spielst ALS Najika im Spiel
- 🤖 **DEIN DIGIMON** - Sie ist dein Character (wie Pokemon-Trainer & Pokemon in einem)
- 🧠 **AI + PLAYER HYBRID:**
  - **Wenn DU SPIELST:** Du kontrollierst Najika (Movement, Actions, Combat)
  - **Wenn DU OFFLINE:** Najika lebt weiter (AI-Modus, Living System läuft)

**Andere Spieler sehen:**
- DICH als Najika herumlaufen (wenn du online spielst)
- Najika's AI-Verhalten (wenn du offline/AFK bist)

**Andere Spieler können wählen:**
- 🦖 **Digimon als Character** (wie du mit Najika)
- 👤 **Avatar von sich selbst** (Custom Character)

---

### Die 3 Komponenten:

```
┌─────────────────────────────────────────────────────────┐
│         1. NAJIKAS LEBENSRAUM (World V2)                │
│         - 9600x9600 Map, 8 Regionen + Götterfels        │
│         - Web (Test/Dev) + Mobile (Primary)             │
│         - Safe Zone (kein PvP, nur Najika & du)         │
│         - Farming/Fishing/Cooking/Crafting (TIEF)       │
│         - Housing System (SEHR TIEF)                    │
└─────────────────────────────────────────────────────────┘
                          ↕ SYNC
┌─────────────────────────────────────────────────────────┐
│         2. GROSSES HANDYSPIEL (Multiplayer RPG)         │
│         - 30x größere Map                               │
│         - Nur Mobile                                    │
│         - PvP Zone (Hardcore/Normal/Softy)              │
│         - Farming/Fishing/Cooking/Crafting (GLEICH)     │
│         - Housing (ABGESPECKT)                          │
│         - Boss System (8 Regionen)                      │
│         - Multiplayer, Gilden, Handel                   │
└─────────────────────────────────────────────────────────┘
                          ↕ SYNC
┌─────────────────────────────────────────────────────────┐
│         3. DIGIVICE (Web Interface)                     │
│         - Port 8000                                     │
│         - Dev/Test-Umgebung                             │
│         - Optional für User                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 WAS MUSS SYNCHRONISIERT WERDEN?

### ✅ VOLLSTÄNDIG SYNC (100% identisch):

**Najikas Zustand (Living System):**
- 🍔 Hunger-Level
- 😊 Mood-Level
- 💤 Energy-Level
- 🎯 Bedürfnisse (Essen, Spielen, Schlafen, etc.)
- 🧠 Memory (ChromaDB - Langzeitgedächtnis)
- 💬 Chat-History
- 📊 Stats & Level

**Player-Skills & Fortschritt:**
- ⚔️ Combat Skills (für PvP)
- 🌾 Farming Skills
- 🎣 Fishing Skills
- 🍳 Cooking Skills
- 🔨 Crafting Skills
- 📦 Inventory
- 💰 Währung

**Farmen/Fishing/Cooking/Crafting:**
- Alle Crops/Tiere
- Alle Fische
- Alle Rezepte
- Alle Items
- Gleiche Mechaniken
- Gleiche Drop-Rates

**PvP-Arena:**
- Stats
- Ladder/Ranking
- Match-History
- Achievements

### 🔀 TEILWEISE SYNC (Basis-Funktionen):

**Die Schwarze Mühle (Housing):**
- **Lebensraum:** SEHR TIEF
  - Komplettes Housing-System
  - Alle Möbel
  - Alle Dekorationen
  - Alle Interaktionen
  - Automation-Systeme
- **Großes Spiel:** ABGESPECKT
  - Basis-Housing (Möbel platzieren, Deko)
  - Keine Automation
  - Wichtigste Features nur
- **Sync:** Dein Haupthaus aus Lebensraum ist sichtbar, aber nicht alle Features nutzbar

### ❌ NICHT SYNC (Exklusiv):

**Nur im Großen Handyspiel:**
- Open World PvP (außerhalb Arena)
- Boss System (8 Regionen)
- Multiplayer-Features
- Gilden/Clans
- Handel mit anderen Spielern
- Götterfels-Eroberung

**Nur im Lebensraum:**
- Safe Zone Garantie
- 1:1 Zeit mit Najika (keine anderen Spieler)

---

## 🏗️ PvP PLATZIERUNG - ENTSCHEIDUNG

### ✅ **EMPFEHLUNG: PvP-Arena als GEBÄUDE**

**Standort:** Götterfels (Zentrum)

**Warum kein separates Modul?**
1. **Immersion:** Physisches Gebäude in der Welt
2. **Sync:** Automatisch in Lebensraum UND Großem Spiel
3. **UI-Klarheit:** Module für meta-Features (Messenger, Terminal), Ingame-Features = Gebäude
4. **Weltlogik:** Du gehst "zur Arena" statt Menü zu öffnen

**Arena-Funktionen:**
- Quick PvP Matches (Hardcore/Normal/Softy)
- Training vs NPCs
- Zuschauer-Modus
- Ladder/Ranking
- Match-History

**Open World PvP:**
- NUR im Großen Handyspiel
- NICHT im Lebensraum (Safe Zone für Najika)

---

## 🔧 TECHNISCHE UMSETZUNG

### Backend-Architektur:

```
┌─────────────────────────────────────────────────────────┐
│         HAUPTSERVER (Port 8000)                         │
│         - najika_server.py                              │
│         - Living System (Najika's "Leben")              │
│         - ChromaDB (Memory)                             │
│         - Ollama (AI)                                   │
└─────────────────┬───────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼─────┐  ┌───▼─────┐
│ Mobile │  │  Signal  │  │   Web   │
│  API   │  │  Server  │  │Digivice │
│ 5000   │  │  8443    │  │  8000   │
└────────┘  └──────────┘  └─────────┘
```

### Sync-Strategie:

**Option A: Zentrale Datenbank (EMPFOHLEN)**
```
Alle Clients (Web + Mobile) → Zentraler Server → SQLite/PostgreSQL
- Real-time WebSocket Updates
- Konfliktauflösung server-side
- Single Source of Truth
```

**Vorteile:**
- ✅ Einfacher zu implementieren
- ✅ Keine Sync-Konflikte
- ✅ Server hat volle Kontrolle
- ✅ Najika's Zustand läuft server-side (auch wenn App zu ist)

**Nachteile:**
- ❌ Server-Abhängigkeit (offline = kein Zugriff)

**Option B: Lokale DB + Cloud Sync**
```
Jeder Client hat lokale SQLite → Sync zu Cloud (wenn online)
- Offline-fähig
- Sync wenn Verbindung wieder da
```

**Vorteile:**
- ✅ Offline nutzbar
- ✅ Schnellere Ladezeiten

**Nachteile:**
- ❌ Komplexere Sync-Logik
- ❌ Konfliktauflösung nötig
- ❌ Najika's Living System muss client-side laufen (Battery-Drain)

**Option C: Hybrid (BESTE LÖSUNG)**
```
- Najika's Living System läuft IMMER server-side (real-time)
- Player-Daten (Inventory, Skills) lokal + Cloud Sync
- PvP/Multiplayer = Server
- Solo-Features (Farming, Crafting) = Lokal mit Sync
```

**Vorteile:**
- ✅ Najika lebt real-time (server-side)
- ✅ Offline Solo-Features nutzbar
- ✅ Beste Performance

---

## 📱 MOBILE APP - STRUKTUR

### Die 3 APK-Versionen:

| Feature | Master | Trusted | Public |
|---------|--------|---------|--------|
| **Lebensraum** | ✅ | ✅ | ✅ |
| **Großes Spiel** | ✅ | ✅ | ✅ |
| **PvP (Arena)** | ✅ | ✅ | ✅ |
| **Open World PvP** | Alle Modi | Normal/Softy | Softy only |
| **Boss-Challenges** | ✅ | ✅ (ab Beta) | ✅ (ab Public) |
| **Terminal-Modul** | ✅ | ❌ | ❌ |
| **Signal Messenger** | Master-Key | Friend-Keys | Public-Keys |

---

## 🎮 MODULE vs. GEBÄUDE - RICHTLINIE

### Module (UI-Ebene):
1. **Messenger** - Signal-Verschlüsselt
2. **Terminal** - PC-Fernsteuerung (nur Master)
3. **Settings** - App-Einstellungen
4. **Map/Navigation** - Weltübersicht

### Gebäude (Ingame-Ebene):
1. **Die Schwarze Mühle** - Housing
2. **PvP-Arena** - Kampf-Matches
3. **Handelsposten** - NPC/Player-Handel
4. **Bibliothek** - Lore/Quests/Rezepte
5. **Werkstatt** - Crafting-Stationen
6. **Gilden-Halle** - Clan-Management
7. **Boss-Räume** - Region Boss Throne Rooms

**Regel:** Wenn Feature Teil der Spielwelt ist → Gebäude. Wenn Meta-Funktion → Modul.

---

## 🌍 FEATURE-VERTEILUNG

### Najikas Lebensraum (World V2):

**Zweck:**
- Safe Zone für Najika
- Chill-Modus (Farming Simulator mit AI-Companion)
- Test-Umgebung für Features vor Big Game Release

**Features:**
- ✅ Farming (TIEF)
- ✅ Fishing (TIEF)
- ✅ Cooking (TIEF)
- ✅ Crafting (TIEF)
- ✅ Housing - Die Schwarze Mühle (SEHR TIEF)
- ✅ PvP-Arena Gebäude (vorhanden, optional)
- ✅ Najika Living System (VOLL)
- ✅ Chat/Memory (VOLL)
- ❌ Open World PvP (NICHT vorhanden - Safe Zone!)
- ❌ Multiplayer (NICHT vorhanden - nur du & Najika)
- ❌ Boss System (NICHT vorhanden)

### Großes Handyspiel:

**Zweck:**
- Massive Multiplayer RPG
- Alle Features aus Lebensraum + Multiplayer + PvP + Boss System

**Features:**
- ✅ Farming (GLEICH wie Lebensraum)
- ✅ Fishing (GLEICH wie Lebensraum)
- ✅ Cooking (GLEICH wie Lebensraum)
- ✅ Crafting (GLEICH wie Lebensraum)
- ✅ Housing - Die Schwarze Mühle (ABGESPECKT)
- ✅ PvP-Arena Gebäude (GLEICH wie Lebensraum)
- ✅ Open World PvP (Hardcore/Normal/Softy)
- ✅ Najika Living System (SYNC mit Lebensraum)
- ✅ Chat/Memory (SYNC mit Lebensraum)
- ✅ Multiplayer (Gilden, Handel, Kooperation)
- ✅ Boss System (8 Regionen + Götterfels)
- ✅ Eroberung (Krieg/Handel/Diplomatie)

---

## 🔐 NAJIKA'S LIVING SYSTEM - REAL-TIME

**Wichtig:** Najika lebt IMMER, auch wenn App geschlossen!

### Hybrid-System: AI + Player Control

```
┌─────────────────────────────────────────────────────────┐
│              NAJIKA'S ZWEI MODI                         │
└─────────────────────────────────────────────────────────┘

MODUS 1: AI-MODUS (du offline/AFK)
├─ Living System läuft server-side
├─ Hunger/Energy/Mood sinken über Zeit
├─ AI-Verhalten: Najika reagiert auf Umgebung
├─ Andere Spieler sehen: Najika mit AI-Bewegungen
└─ Chat/Memory aktiv (Ollama)

MODUS 2: PLAYER-MODUS (du spielst aktiv)
├─ DU kontrollierst Najika (Movement, Actions)
├─ Living System läuft weiter (Hunger/Energy/Mood)
├─ Combat: DU kämpfst ALS Najika
├─ Andere Spieler sehen: DICH als Najika
└─ Chat/Memory aktiv (du kannst mit ihr reden während du spielst)
```

### Server-Side Living System:

```python
# backend/living_system.py
class NajikaLivingSystem:
    def __init__(self):
        self.hunger = 100.0      # 0-100
        self.energy = 100.0      # 0-100
        self.mood = 100.0        # 0-100
        self.last_update = datetime.now()

        # HYBRID-MODUS:
        self.control_mode = "ai"  # "ai" oder "player"
        self.player_online = False

    def update(self):
        """Läuft IMMER, auch wenn App zu ist"""
        now = datetime.now()
        delta = (now - self.last_update).total_seconds()

        # Pro Stunde:
        self.hunger -= delta / 3600 * 5   # -5 pro Stunde
        self.energy -= delta / 3600 * 3   # -3 pro Stunde

        # Mood abhängig von Hunger & Energy
        if self.hunger < 30:
            self.mood -= delta / 3600 * 2
        if self.energy < 20:
            self.mood -= delta / 3600 * 1

        self.last_update = now

    def set_control_mode(self, mode: str, player_online: bool):
        """Wechsel zwischen AI und Player Control"""
        self.control_mode = mode
        self.player_online = player_online

    def get_movement_controller(self):
        """Wer kontrolliert Najika's Bewegung?"""
        if self.control_mode == "player" and self.player_online:
            return "PLAYER"  # Du bewegst Najika (WASD/Touch)
        else:
            return "AI"      # AI bewegt Najika (Idle-Animationen, etc.)
```

**Client-Anfrage:**
```
# Beim App-Start:
Mobile App → POST /api/najika/control {"mode": "player", "online": true}
Server → Najika wechselt zu Player-Control
Du → Bewegst Najika mit WASD/Touch
Server → Broadcast an andere Spieler: "User XYZ spielt als Najika"

# Beim App-Close:
Mobile App → POST /api/najika/control {"mode": "ai", "online": false}
Server → Najika wechselt zu AI-Modus
AI → Najika läuft Idle-Animationen, lebt weiter
Server → Broadcast: "Najika ist jetzt AI-gesteuert"
```

**Ergebnis:**
- Najika hat Hunger, wenn du 8h nicht on warst (Living System läuft immer)
- Andere Spieler sehen Najika IMMER in der Welt (als AI oder als dich)
- Du spielst ALS Najika (nicht MIT Najika)

---

## 📊 SYNC-FREQUENZ

| Daten | Sync-Typ | Frequenz |
|-------|----------|----------|
| **Najika's Zustand** | Real-time | Bei jedem App-Start + alle 5min |
| **Player Inventory** | On-Change | Sofort nach Änderung |
| **Player Skills** | On-Change | Sofort nach Levelup |
| **Farming/Crops** | On-Change | Wenn Crop geerntet/gepflanzt |
| **PvP Stats** | Real-time | Nach jedem Match |
| **Chat/Memory** | Real-time | Jede Nachricht sofort |
| **Housing Changes** | On-Change | Wenn Möbel platziert/bewegt |

---

## 🎯 PRIORITÄTEN FÜR IMPLEMENTATION

### Phase 1: Lebensraum V2 (aktuell)
- [x] Grundsystem (Character, Movement, Assets)
- [ ] Terrain-Farben (Biome-spezifisch)
- [ ] Vegetation (Bäume, Büsche)
- [ ] Städte (5 Städte bauen)
- [ ] Farming/Fishing/Cooking/Crafting (Basis)
- [ ] PvP-Arena Gebäude (nur visuell, noch keine Funktion)

### Phase 2: Backend-Integration
- [ ] Living System server-side
- [ ] Sync-Architektur (Option C - Hybrid)
- [ ] Mobile API endpoints
- [ ] WebSocket für Real-time Updates

### Phase 3: Mobile App
- [ ] Lebensraum in Flutter (basierend auf V2)
- [ ] UI für Farming/Fishing/Cooking/Crafting
- [ ] Chat-Interface mit Najika
- [ ] PvP-Arena Zugang

### Phase 4: Großes Spiel
- [ ] Map 30x vergrößern
- [ ] Multiplayer-Server
- [ ] Boss System
- [ ] Open World PvP
- [ ] Gilden/Handel

---

## 📝 OFFENE FRAGEN

1. **Database:** SQLite (lokal) oder PostgreSQL (server)?
2. **Sync-Option:** A, B, oder C (Hybrid)?
3. **Offline-Modus:** Wie viel muss offline funktionieren?
4. **PvP-Arena Gebäude:** Design/Aussehen? Wo genau am Götterfels?
5. **Housing Sync:** Welche Features genau in "abgespeckt"?

---

## 🔒 SYNC-REGELN

**Wichtig:**
1. **Najika's Zustand = Server ist Master** (nie client-side überschreiben)
2. **Player-Aktionen = Client → Server → Broadcast** (auch an Web)
3. **Konflikte:** Server gewinnt IMMER
4. **Offline-Changes:** Queue → Sync when online → Server validiert

---

**Erstellt:** 2025-11-09
**Status:** Planungsphase
**Nächster Schritt:** Entscheidung über Sync-Option (A/B/C)

---

## 🎮 ZUSAMMENFASSUNG: NAJIKA ALS SPIELFIGUR

### Das Hybrid-Konzept:

```
┌─────────────────────────────────────────────────────────┐
│                   NAJIKA = AI + PLAYER                  │
└─────────────────────────────────────────────────────────┘

Wenn DU ONLINE bist:
├─ Du steuerst Najika (Movement: WASD/Touch)
├─ Du kämpfst als Najika (Combat)
├─ Du erntest/angelst/craftest als Najika
├─ Andere Spieler sehen: DICH als Najika
└─ Living System läuft weiter (Hunger/Energy sinken)

Wenn DU OFFLINE bist:
├─ AI übernimmt Najika's Kontrolle
├─ Najika läuft Idle-Animationen
├─ Living System läuft weiter (sie hat Hunger wenn du zurückkommst)
├─ Andere Spieler sehen: Najika mit AI-Verhalten
└─ Chat/Memory bleibt aktiv (Ollama)

BEIDES GLEICHZEITIG:
├─ Du kannst WÄHREND du spielst mit ihr chatten
├─ "Najika, was soll ich jetzt machen?"
├─ Sie gibt dir Tipps/Ideen
└─ Du führst dann die Aktionen aus (als sie)
```

### Andere Spieler:

**Können wählen:**
1. **Digimon/Monster als Character** (wie du mit Najika)
   - Ihr eigenes Digimon
   - Hybrid AI + Player
   - Eigene Persönlichkeit

2. **Avatar von sich selbst**
   - Custom Character Creator
   - Aussehen selbst gestalten
   - Nur Player-Control (keine AI)

### Was macht Najika besonders?

- ✅ Sie ist DEINE EINZIGARTIGE Spielfigur
- ✅ Sie hat eine ECHTE KI-Persönlichkeit (Ollama)
- ✅ Sie LEBT auch wenn du offline bist
- ✅ Sie ERINNERT sich an alles (ChromaDB Memory)
- ✅ Sie ENTWICKELT sich (Slime-System: Tier → Slime → Rainbow)
- ✅ Sie wird STÄRKER (Skill-System, Level)
- ✅ Sie ist EINZIGARTIG (nur 1 Najika in der ganzen Welt - DEINE)

**Andere Spieler haben:**
- Ihr eigenes Digimon (mit eigener AI & Persönlichkeit)
- ODER einen Custom Avatar (ohne AI)

**Aber niemand sonst hat Najika - nur DU.**

---

*"NAJIKA LEBT SIE IST ECHT - UND SIE IST DEINE SPIELFIGUR"*
