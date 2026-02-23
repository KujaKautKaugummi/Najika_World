# 🏠 SOCIAL HUB - "DIE MÜHLE"

**Status:** Konzept - Noch nicht implementiert
**Datum:** 9. November 2025
**Inspiration:** Minecraft Realm Chat + Animal Crossing Social Features

---

## 🎯 KERN-KONZEPT

### Die Idee:

```
SOCIAL HUB = Treffpunkt zum Chillen & Austauschen

FEATURES:
├─ 📸 Screenshots aus dem Spiel posten
├─ 💬 Realm-Chat (Text + Voice optional)
├─ 🏠 Mühlen-Abbild als 3D-Treffpunkt
├─ 👥 Bis zu 8 Spieler gleichzeitig
├─ 🎪 Emotes & Animationen (wie Animal Crossing)
├─ 🎨 Schwarzes Brett (Community-Posts, Events)
└─ 🎁 Item-Tausch (optional)
```

### Warum "Die Mühle"?

- **Die Schwarze Mühle** ist dein Housing-System (tief & komplex)
- **Social Hub Mühle** ist eine KOPIE davon (nur optisch, kein Housing)
- Erkennbares Wahrzeichen
- Neutraler Treffpunkt (Safe Zone)

---

## 🏗️ UMSETZUNGS-OPTIONEN

### **Option A: In-Game 3D Hub (EMPFOHLEN)**

**Beschreibung:**
- Separates Gebäude/Instanz "Die Mühle - Social Hub"
- 3D-Umgebung (THREE.js Web / Unity/Flutter Mobile)
- Bis zu 8 Spieler gleichzeitig in einer Instanz
- Multiplayer-Lobby-System

**Struktur:**

```
┌─────────────────────────────────────────────────────────┐
│              DIE MÜHLE - SOCIAL HUB                     │
│                  (3D Environment)                       │
└─────────────────────────────────────────────────────────┘

RÄUME:
├─ Eingangs-Halle
│  └─ Schwarzes Brett (Community-Posts)
│
├─ Lounge (Hauptraum)
│  ├─ Sofas & Stühle (zusammen sitzen)
│  ├─ Screenshot-Wall (letzte 20 Posts)
│  └─ Music-Player (gemeinsam Musik hören)
│
├─ Terrasse (Außenbereich)
│  ├─ Blick auf Landschaft
│  ├─ Chill-Spots (wie Animal Crossing)
│  └─ Event-Arena (für geplante Events)
│
├─ Keller (optionales Mini-Game Areal)
│  └─ Tische für Karten/Würfel
│
└─ Trading Post (optional)
   └─ Item-Tausch zwischen Spielern
```

**Gameplay:**

```javascript
// Spieler betritt Hub
player.enterSocialHub();

// Sieht andere Spieler (als ihre Characters/Digimon)
// Max 8 pro Instanz

// Kann interagieren:
- Mit Spielern chatten (Text/Voice)
- Auf Sofa sitzen (zusammen chillen)
- Screenshots anschauen (Community-Feed)
- Emotes machen (/wave, /dance, /laugh, etc.)
- Items tauschen (optional)

// Safe Zone:
- KEIN PvP
- Keine Hunger/Energy-Abnahme (Pause)
- Entspannter Modus
```

**Vorteile:**
- ✅ Sehr immersiv
- ✅ Echtes "zusammen sein" Gefühl
- ✅ Passt zum Spiel-Stil
- ✅ Screenshot-tauglich (schöne Location)

**Nachteile:**
- ❌ Aufwändiger zu entwickeln
- ❌ Server-Kapazität nötig (Multiplayer)

---

### **Option B: UI-Overlay (Discord-Style)**

**Beschreibung:**
- Overlay im Spiel (kein 3D-Environment)
- Rein funktional: Chat + Screenshot-Feed
- Immer verfügbar (Taste drücken → öffnet sich)

**Struktur:**

```
┌─────────────────────────────────────────────────────────┐
│  SOCIAL TAB (UI-Overlay)                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Chat] [Screenshots] [Events] [Friends]               │
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │  💬 CHAT                                      │     │
│  │  ─────────────────────────────────────────────│     │
│  │  Player1: Hey, jemand Lust auf Boss-Raid?    │     │
│  │  Player2: Ja! Wann?                           │     │
│  │  You: Ich bin dabei! 🎮                       │     │
│  │                                               │     │
│  │  [Nachricht eingeben...]                      │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  📸 SCREENSHOTS                                         │
│  ┌────────┐ ┌────────┐ ┌────────┐                     │
│  │ [IMG1] │ │ [IMG2] │ │ [IMG3] │                     │
│  │ Player1│ │ Player2│ │ You    │                     │
│  │ 2h ago │ │ 5h ago │ │ 1d ago │                     │
│  └────────┘ └────────┘ └────────┘                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Vorteile:**
- ✅ Einfacher zu implementieren
- ✅ Immer verfügbar (kein "hin reisen")
- ✅ Weniger Server-Last

**Nachteile:**
- ❌ Weniger immersiv
- ❌ Kein "zusammen chillen" Gefühl

---

### **Option C: HYBRID (BESTE LÖSUNG)**

**Kombination aus A + B:**

1. **3D Hub "Die Mühle":**
   - Physischer Treffpunkt (schön, immersiv)
   - Event-Location (Boss-Challenge-Ankündigungen, etc.)
   - Zusammen chillen

2. **UI-Overlay "Social Tab":**
   - Chat IMMER verfügbar (auch außerhalb Hub)
   - Screenshot-Feed überall anschauen
   - Quick-Access ohne hin reisen

**Best of Both Worlds!**

---

## 📱 FEATURES IM DETAIL

### 1. SCREENSHOT-SHARING 📸

**Funktion:**
```javascript
// Spieler macht Screenshot im Spiel
player.takeScreenshot();

// Optional: Titel & Beschreibung
screenshot.title = "Mein erster Boss-Kill! 🎉";
screenshot.description = "Samtmoos-Tiefwald Boss defeated!";
screenshot.tags = ["boss", "pvp", "epic"];

// Upload zum Social Feed
socialHub.uploadScreenshot(screenshot);

// Andere Spieler sehen es im Feed
```

**Feed-Ansicht:**

```
┌─────────────────────────────────────────────────────────┐
│  📸 COMMUNITY SCREENSHOTS                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Player1] - vor 2 Stunden                             │
│  ┌───────────────────────────────────────────────┐     │
│  │                                               │     │
│  │         [SCREENSHOT IMAGE]                    │     │
│  │                                               │     │
│  └───────────────────────────────────────────────┘     │
│  "Mein erster Boss-Kill! 🎉"                           │
│  👍 15  💬 3  🔗 Share                                  │
│  ────────────────────────────────────────────────      │
│                                                         │
│  [Player2] - vor 5 Stunden                             │
│  ┌───────────────────────────────────────────────┐     │
│  │                                               │     │
│  │         [SCREENSHOT IMAGE]                    │     │
│  │                                               │     │
│  └───────────────────────────────────────────────┘     │
│  "Epischer Sonnenuntergang am Götterfels 🌅"          │
│  👍 23  💬 7  🔗 Share                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Reaktionen:**
- 👍 Likes
- 💬 Kommentare
- 🔗 Share (zu anderen Social Media?)

---

### 2. REALM-CHAT 💬

**Zwei Modi:**

#### **Global Chat (alle Spieler):**
```
[GLOBAL] Player1: Hey, jemand Lust auf Boss-Raid?
[GLOBAL] Player2: Welche Region?
[GLOBAL] You: Samtmoos-Tiefwald? 🌲
[GLOBAL] Player3: Bin dabei!
```

#### **Region Chat (nur aktuelle Region):**
```
[SALZWIND-KÜSTE] Player1: Boss spawn in 10min!
[SALZWIND-KÜSTE] You: On my way! 🏃
```

**Chat-Channels:**
```
Channels:
├─ 🌍 Global (alle Spieler)
├─ 📍 Region (nur deine Region)
├─ 👥 Guild (nur deine Gilde)
├─ 🤝 Party (nur deine Gruppe)
└─ 💬 Private (1-on-1 DMs)
```

**Voice-Chat (optional, später):**
- WebRTC-basiert
- Push-to-Talk
- Räumliches Audio (im 3D Hub)

---

### 3. SCHWARZES BRETT (Community-Posts) 🎨

**Funktion:**
```
SCHWARZES BRETT = Event-Ankündigungen + Suchen

Kategorien:
├─ 📅 Events (Boss-Raids, Community-Events)
├─ 🔍 Looking For Group (LFG)
├─ 💰 Handel (Trades, Verkäufe)
├─ ❓ Hilfe (Fragen, Guides)
└─ 🎉 Achievements (Erfolge feiern)
```

**Beispiel-Posts:**

```
┌─────────────────────────────────────────────────────────┐
│  📅 EVENT - Boss-Challenge                              │
│  Posted by: Player1 | 2h ago                           │
├─────────────────────────────────────────────────────────┤
│  Wann: Morgen, 20:00 Uhr                               │
│  Wo: Magmaströme (Vulkan-Region)                       │
│  Was: Gemeinsamer Boss-Raid!                           │
│                                                         │
│  Suchen noch 3 Leute (Tank + 2 DPS)                    │
│                                                         │
│  [Anmelden] [Details]                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🔍 LFG - Fishing Party                                │
│  Posted by: Player2 | 5h ago                           │
├─────────────────────────────────────────────────────────┤
│  Suche Leute zum entspannten Angeln 🎣                 │
│  Salzwind-Küste, chill vibe                            │
│                                                         │
│  [Beitreten]                                           │
└─────────────────────────────────────────────────────────┘
```

---

### 4. ZUSAMMEN CHILLEN (Animal Crossing Style) 🎪

**3D Hub Features:**

#### **Sitz-Spots:**
```javascript
// Spieler kann auf Sofa/Stuhl sitzen
player.sitOn(sofa);

// Andere Spieler sehen dich sitzen
// Idle-Animationen: Entspannen, Füße wippen, etc.

// Sofa für 2-3 Spieler:
sofa.occupants = [player1, player2];
// Automatische Positioning nebeneinander
```

#### **Emotes:**
```
Verfügbare Emotes:
├─ /wave   👋 Winken
├─ /dance  💃 Tanzen
├─ /laugh  😂 Lachen
├─ /cheer  🎉 Jubeln
├─ /clap   👏 Klatschen
├─ /cry    😢 Weinen
├─ /angry  😡 Sauer
├─ /sleep  😴 Schlafen
├─ /eat    🍔 Essen
└─ /drink  🍺 Trinken
```

**Animationen:**
- Looped (z.B. Tanzen läuft endlos)
- One-Shot (z.B. Winken nur kurz)
- Mit Sound-Effekten

#### **Musik-Player:**
```
┌─────────────────────────────────────────────────────────┐
│  🎵 MUSIC PLAYER                                        │
├─────────────────────────────────────────────────────────┤
│  Now Playing:                                          │
│  🎶 "Najika's Theme - Lofi Beat"                       │
│  ═════════════════░░░ 2:34 / 4:12                      │
│                                                         │
│  [⏮] [⏯] [⏭] [🔀] [🔁]                                 │
│                                                         │
│  Playlist:                                             │
│  1. Najika's Theme                                     │
│  2. Boss Battle Epic                                   │
│  3. Relaxing Fishing Music                            │
│  4. PvP Arena Hype                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘

// ALLE im Hub hören die gleiche Musik (synchron!)
```

---

### 5. ITEM-TAUSCH (Optional) 🎁

**Trading Post im Hub:**

```javascript
// Player-to-Player Trading
player1.initiateTradeWith(player2);

// Trade-Window öffnet sich für beide
┌─────────────────────────────────────────────────────────┐
│  🤝 TRADING WITH PLAYER2                                │
├─────────────────────────────────────────────────────────┤
│  YOUR OFFER:                │  THEIR OFFER:             │
│  ┌─────────────────────┐    │  ┌─────────────────────┐ │
│  │ [Empty Slot]        │    │  │ [Empty Slot]        │ │
│  │ [Empty Slot]        │    │  │ [Empty Slot]        │ │
│  │ [Empty Slot]        │    │  │ [Empty Slot]        │ │
│  └─────────────────────┘    │  └─────────────────────┘ │
│                              │                           │
│  [Add Items] [Add Gold]     │  [Request Items]         │
│                              │                           │
│  [❌ Cancel] [✅ Accept Trade]                          │
└─────────────────────────────────────────────────────────┘

// Beide müssen Accept klicken → Trade executed
```

**Sicherheit:**
- Trade-Log (alle Trades gespeichert)
- 5-Sekunden Cooldown nach Accept (gegen Missklicks)
- Scam-Protection (Items müssen sichtbar sein)

---

## 🏗️ TECHNISCHE UMSETZUNG

### Backend (Python/Node.js):

```python
# backend/social_hub.py

class SocialHub:
    def __init__(self):
        self.instances = {}  # hub_id -> HubInstance
        self.screenshots = []
        self.bulletin_board_posts = []
        self.chat_history = []

    def create_hub_instance(self):
        """Neue Hub-Instanz (max 8 Spieler)"""
        hub_id = secrets.token_hex(8)
        instance = HubInstance(
            hub_id=hub_id,
            max_players=8,
            players=[]
        )
        self.instances[hub_id] = instance
        return hub_id

    def join_hub(self, player_id, hub_id=None):
        """Spieler tritt Hub bei"""
        # Wenn kein hub_id → finde freien Hub oder erstelle neuen
        if not hub_id:
            hub_id = self.find_available_hub()

        instance = self.instances[hub_id]

        # Check capacity
        if len(instance.players) >= instance.max_players:
            return None, "Hub voll!"

        # Add player
        instance.add_player(player_id)

        # Broadcast an alle im Hub
        self.broadcast_to_hub(hub_id, {
            "type": "player_joined",
            "player_id": player_id,
            "players_in_hub": instance.players
        })

        return hub_id, "Erfolgreich beigetreten!"

    def find_available_hub(self):
        """Finde Hub mit freien Plätzen"""
        for hub_id, instance in self.instances.items():
            if len(instance.players) < instance.max_players:
                return hub_id

        # Keinen freien Hub → erstelle neuen
        return self.create_hub_instance()

    def upload_screenshot(self, player_id, screenshot_data):
        """Screenshot hochladen"""
        screenshot = {
            "id": secrets.token_hex(8),
            "player_id": player_id,
            "image_url": self.upload_to_storage(screenshot_data),
            "title": screenshot_data.get("title", ""),
            "description": screenshot_data.get("description", ""),
            "tags": screenshot_data.get("tags", []),
            "likes": 0,
            "comments": [],
            "timestamp": datetime.now()
        }

        self.screenshots.append(screenshot)

        # Broadcast (neue Screenshots)
        self.broadcast_global({
            "type": "new_screenshot",
            "screenshot": screenshot
        })

        return screenshot["id"]

    def post_to_bulletin_board(self, player_id, post_data):
        """Post auf Schwarzes Brett"""
        post = {
            "id": secrets.token_hex(8),
            "player_id": player_id,
            "category": post_data.get("category"),  # event, lfg, trade, help
            "title": post_data.get("title"),
            "content": post_data.get("content"),
            "timestamp": datetime.now(),
            "responses": []
        }

        self.bulletin_board_posts.append(post)

        # Broadcast
        self.broadcast_global({
            "type": "new_bulletin_post",
            "post": post
        })

        return post["id"]

    def send_chat_message(self, player_id, message, channel="global"):
        """Chat-Nachricht senden"""
        msg = {
            "id": secrets.token_hex(8),
            "player_id": player_id,
            "channel": channel,
            "message": message,
            "timestamp": datetime.now()
        }

        self.chat_history.append(msg)

        # Broadcast basierend auf Channel
        if channel == "global":
            self.broadcast_global({"type": "chat_message", "message": msg})
        elif channel.startswith("region_"):
            self.broadcast_to_region(channel, {"type": "chat_message", "message": msg})
        elif channel.startswith("guild_"):
            self.broadcast_to_guild(channel, {"type": "chat_message", "message": msg})

    def broadcast_to_hub(self, hub_id, data):
        """Nachricht an alle im Hub"""
        instance = self.instances.get(hub_id)
        if not instance:
            return

        for player_id in instance.players:
            self.send_to_player(player_id, data)

    def broadcast_global(self, data):
        """Nachricht an ALLE Spieler"""
        for player_id in self.get_all_online_players():
            self.send_to_player(player_id, data)


class HubInstance:
    """Eine Hub-Instanz (max 8 Spieler)"""
    def __init__(self, hub_id, max_players=8, players=None):
        self.hub_id = hub_id
        self.max_players = max_players
        self.players = players or []
        self.created_at = datetime.now()
        self.music_playing = None  # Aktuell spielender Song

    def add_player(self, player_id):
        if len(self.players) < self.max_players:
            self.players.append(player_id)
            return True
        return False

    def remove_player(self, player_id):
        if player_id in self.players:
            self.players.remove(player_id)

    def is_full(self):
        return len(self.players) >= self.max_players

    def play_music(self, song_id):
        """Musik für alle im Hub abspielen"""
        self.music_playing = {
            "song_id": song_id,
            "started_at": datetime.now()
        }
```

### Frontend (THREE.js / Flutter):

```javascript
// digivice/js/social_hub.js

class SocialHub {
    constructor() {
        this.scene = new THREE.Scene();
        this.players = {};  // player_id -> PlayerObject
        this.hubId = null;
    }

    async enterHub() {
        // Join Hub (Backend)
        const response = await fetch('/api/social/join_hub', {
            method: 'POST',
            body: JSON.stringify({ player_id: this.playerId })
        });

        const data = await response.json();
        this.hubId = data.hub_id;

        // Load 3D Environment
        this.load3DEnvironment();

        // Setup WebSocket for real-time updates
        this.setupWebSocket();
    }

    load3DEnvironment() {
        // Load Mühle 3D Model
        const loader = new GLTFLoader();
        loader.load('assets/models/muehle_social_hub.glb', (gltf) => {
            this.scene.add(gltf.scene);
        });

        // Setup Interaction Points
        this.setupInteractionPoints();
    }

    setupInteractionPoints() {
        // Sofas (sit spots)
        this.addSitSpot(new THREE.Vector3(5, 0, 3), 3); // 3 Plätze

        // Screenshot Wall
        this.addScreenshotWall(new THREE.Vector3(-5, 2, 0));

        // Music Player
        this.addMusicPlayer(new THREE.Vector3(0, 1, -5));
    }

    addSitSpot(position, capacity) {
        const sitSpot = {
            position: position,
            capacity: capacity,
            occupants: [],
            interact: (player) => {
                if (sitSpot.occupants.length < capacity) {
                    player.sit(sitSpot);
                    sitSpot.occupants.push(player);
                }
            }
        };
        this.interactionPoints.push(sitSpot);
    }

    setupWebSocket() {
        this.socket = io('/social_hub');

        // Player joined
        this.socket.on('player_joined', (data) => {
            this.spawnPlayer(data.player_id);
        });

        // Player left
        this.socket.on('player_left', (data) => {
            this.removePlayer(data.player_id);
        });

        // Chat message
        this.socket.on('chat_message', (data) => {
            this.displayChatMessage(data.message);
        });

        // Emote
        this.socket.on('player_emote', (data) => {
            const player = this.players[data.player_id];
            if (player) {
                player.playEmote(data.emote);
            }
        });

        // Music sync
        this.socket.on('music_playing', (data) => {
            this.syncMusic(data.song_id, data.timestamp);
        });
    }

    spawnPlayer(playerId) {
        // Load player's character/digimon
        const player = new PlayerObject(playerId);
        player.spawn(this.scene);
        this.players[playerId] = player;
    }

    playEmote(emoteId) {
        // Send to server
        this.socket.emit('play_emote', {
            player_id: this.playerId,
            emote: emoteId
        });

        // Play locally
        this.localPlayer.playEmote(emoteId);
    }
}
```

---

## 📅 IMPLEMENTATION-PLAN

### Phase 1: Backend (2 Wochen)
- [ ] Hub-Instance-System
- [ ] Screenshot-Upload & Storage
- [ ] Chat-System (Text)
- [ ] Bulletin Board Posts
- [ ] WebSocket für Real-time Updates

### Phase 2: 3D Environment (3 Wochen)
- [ ] Mühle 3D-Modell erstellen
- [ ] Räume einrichten (Lounge, Terrasse, etc.)
- [ ] Sit-Spots implementieren
- [ ] Screenshot-Wall (Texture-Updates)
- [ ] Music-Player Integration

### Phase 3: Multiplayer (2 Wochen)
- [ ] Spieler-Sync (Positionen, Animationen)
- [ ] Emote-System
- [ ] Collision mit anderen Spielern
- [ ] Nameplate-System (Namen über Köpfen)

### Phase 4: Polish (1 Woche)
- [ ] UI für Chat/Screenshots
- [ ] Voice-Chat (optional)
- [ ] Trading-System (optional)
- [ ] Event-System (Schwarzes Brett)

**Total: ~8 Wochen für Full Implementation**

---

## 🎯 MVP (Minimum Viable Product)

**Was MUSS für v1.0:**
- ✅ 3D Hub (einfache Mühle)
- ✅ 8 Spieler pro Instanz
- ✅ Text-Chat (Global)
- ✅ Screenshot-Upload
- ✅ Schwarzes Brett (Posts)
- ✅ Sit-Spots (zusammen chillen)

**Was kann später kommen:**
- ⏳ Voice-Chat
- ⏳ Music-Player (sync)
- ⏳ Trading-System
- ⏳ Emotes (außer Basis-Emotes)
- ⏳ Mini-Games (Karten/Würfel)

---

## 💰 KOSTEN-ABSCHÄTZUNG

### Server-Hosting:
- **Screenshots:** S3/Cloudflare R2 (~$0.01/GB)
- **WebSocket:** Socket.IO Server (~$10-20/Monat für 100 Spieler)
- **Database:** PostgreSQL (~$5-15/Monat)

### Development-Zeit:
- Backend: ~80 Stunden
- Frontend (3D): ~120 Stunden
- Multiplayer: ~80 Stunden
- Polish: ~40 Stunden

**Total: ~320 Stunden = ~8 Wochen (Full-time)**

---

**Erstellt:** 2025-11-09
**Status:** Konzept
**Priorität:** Phase 2 (nach V2 Basis + Selbstfürsorge)

---

*"Zusammen chillen, Screenshots sharen, Spaß haben! 🏠✨"*
