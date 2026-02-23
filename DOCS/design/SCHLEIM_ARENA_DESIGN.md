# SCHLEIM-ARENA - DESIGN DOKUMENT

**Erstellt**: 2026-01-15
**Status**: Design Phase
**Location**: Handelsfeste (Heiße Dünen) - Neben der Nemesis Arena

---

## KONZEPT

Ein kleines, schäbiges Gebäude neben der großen Nemesis Arena. Von außen sieht es aus wie eine heruntergekommene Taverne, aber Eingeweihte wissen: Hier finden die legendären Schleim-Kämpfe statt.

---

## LOCATION & GEBÄUDE

### Außenansicht
- **Gebäude-Typ**: Kleines 2-stöckiges Holzgebäude
- **Zustand**: Schäbig, alte Holzplanken, schief
- **Schild**: "🍺 Zur Schlammigen Münze" (getarnt als Taverne)
- **Position**: Seitlich neben der großen Nemesis Arena
- **Ambiente**: Wüsten-Setting, Sand, Hitze

### Innenbereich - Erdgeschoss (Taverne)
- **Einrichtung**:
  - Bar mit fragwürdigem Ale
  - 3-4 wackelige Holztische
  - Dunkle Ecken, Fackeln
- **NPC**: "Schleimiger Pete" (Arena-Organisator)
  - Alter Mann mit Augenklappe
  - Kennt jeden Schleim-Kämpfer
  - Dialog: "Willkommen in der Grube, Fremder. Dein Schleim bereit für'n Kampf?"
- **Treppe nach unten**: "Nur für Stammgäste" (führt zur Keller-Arena)
- **Tür nach hinten**: Führt zum Hinterhof

### Kampfplatz - Hinterhof
- **Layout**: Offene Arena unter freiem Himmel
- **Boden**: Sand & Staub (Wüsten-Ambiente)
- **Umzäunung**: Primitive Holzzäune
- **Zuschauer**: Stehen am Rand, primitive Holzbänke
- **Größe**: 15x15 Meter Kampffläche
- **Beleuchtung**: Tagsüber Sonne, nachts Fackeln
- **Ambiente**: Hitze flimmert, gelegentliche Sandböen

### Kampfplatz - Keller (Optional)
- **Layout**: Underground Fight Club Atmosphere
- **Boden**: Gestampfter Lehm
- **Wände**: Roher Stein, Fackeln
- **Zuschauer**: Holzränge an den Seiten
- **Größe**: 12x12 Meter Kampffläche
- **Beleuchtung**: Nur Fackeln (düster)
- **Ambiente**: Enge, Hitze, Schweiß, Geschrei

---

## GAME MODES

### 1. 🥊 1v1 Normal (Classic Duel)

**Beschreibung**: Klassisches Schleim-Duell ohne Schnickschnack

**Regeln**:
- Dein Schleim vs NPC-Schleim (oder Spieler-Schleim)
- Turn-Based Combat System
- Normale Attacken, keine Finisher
- Best of 1 Runde
- Gewinner erhält: Geld + XP

**Combat-System**:
- Rundenbasiert (wie `turn_based_battle_minigame.js`)
- Jeder Zug: Angriff, Verteidigung, Item, Fliehen
- Schadens-Berechnung basierend auf Schleim-Stats
- Status-Effekte möglich (Poison, Burn, etc.)

**Rewards**:
- 100-500 Gold (abhängig von Gegner-Level)
- XP für Schleim
- Zufällige Items (10% Chance)

---

### 2. 💥 1v1 mit Finisher-System (Spectacle Duel)

**Beschreibung**: Wie normales Duell, aber mit spektakulären Finishing Moves am Ende

**Regeln**:
- Wie 1v1 Normal (rundenbasiert bis HP = 0)
- ABER: Wenn ein Schleim besiegt ist (HP = 0) → Finisher-Auswahl!
- Gewinner wählt einen Finisher aus mehreren Optionen
- **GENAU wie Nemesis Arena** - verschiedene Finisher zur Auswahl
- Finisher-Animation wird abgespielt
- Gewinner erhält: Mehr Geld + XP + Ruhm

**Combat-Control-Modi** (3 Wege - **JEDERZEIT wechselbar**):

Der Spieler kann **JEDE RUNDE NEU** entscheiden, wie er seinen Schleim steuert:

1. **🤖 KI-Kontrolle (Auto)**
   - KI entscheidet alle Aktionen automatisch
   - Spieler lehnt sich zurück und schaut zu
   - Schnell, kein Micromanagement

2. **🎮 Direkte Befehle (Manual)**
   - Pokemon-Style Combat
   - Spieler wählt jede Aktion:
     - [1] Angriff wählen
     - [2] Verteidigung
     - [3] Item benutzen
     - [4] Wechseln (falls mehrere Schleime)
   - Volle Kontrolle über jeden Zug

3. **📣 Digimon-Anfeuern (Cheer)**
   - Spieler feuert Schleim an:
     - [1] "Los!" (+10% DMG, 3 Runden)
     - [2] "Defend!" (+20% DEF, 3 Runden)
     - [3] "Combo!" (Next attack = Combo)
     - [4] "Focus!" (+15% Accuracy)
   - Schleim kämpft selbst, aber mit Buffs
   - Hybrid aus Auto und Manual

**Modi-Wechsel** (jede Runde):
```
╔═══════════════════════════════════════╗
║ RUNDE 3 - Dein Zug                   ║
╠═══════════════════════════════════════╣
║ Aktueller Modus: [Direkte Befehle]   ║
║                                       ║
║ Modus wechseln?                       ║
║ [F1] KI-Kontrolle                     ║
║ [F2] Direkte Befehle                  ║
║ [F3] Digimon-Anfeuern                 ║
║                                       ║
║ Oder direkt Aktion wählen:            ║
║ [1] Feuer-Angriff                     ║
║ [2] Verteidigung                      ║
║ [3] Item                              ║
╚═══════════════════════════════════════╝
```

**Finisher-System** (am Kampfende):
- **Trigger**: Wenn Gegner-HP = 0
- **Auswahl**: Gewinner wählt aus mehreren Finishern:
  - Finisher 1: "Inferno Burst" (Standard, spektakulär)
  - Finisher 2: "Mega Explosion" (Extra brutal)
  - Finisher 3: "Flame Stomp" (Demütigend)
  - Finisher 4: "Mercy" (Gnädig, nur HP-Entzug)
- **Animation**: 3-5 Sekunden pro Finisher
- **Unterschiede**: Verschiedene Animationen, gleicher Effekt (K.O.)
- **Ruhm-Bonus**: Brutale Finisher geben mehr Ruhm (+5 extra)

**Rewards**:
- 200-1000 Gold
- XP für Schleim (2x Normal)
- Ruhm-Punkte (+10)
- Bessere Item-Chance (20%)

---

### 3. 🏆 Turnier (Elimination Tournament mit Finisher-System)

**Beschreibung**: BRUTALES Single-Elimination Turnier - 1 Niederlage und du wirst GEFINISCHT!

**Regeln**:
- 8 oder 16 Teilnehmer (Spieler + NPCs)
- **Single-Elimination**: 1 Loss = Du bist RAUS
- **FINISHING RULE**: Jeder Kampf MUSS mit einem Finisher enden!
- Der Gewinner finischt den Verlierer (automatisch bei HP < 20%)
- Spektakuläre Finisher-Animationen bei jedem K.O.
- Preise für Top 3
- Turniere finden alle 7 Tage statt (in-game)

**Bracket-System** (Single-Elimination):
```
Runde 1 (Achtelfinale): 8 Kämpfe → 8 Gewinner (8 gefinischt)
Runde 2 (Viertelfinale): 4 Kämpfe → 4 Gewinner (4 gefinischt)
Runde 3 (Halbfinale):    2 Kämpfe → 2 Gewinner (2 gefinischt)
Runde 4 (FINALE):        1 Kampf  → 1 CHAMPION (1 gefinischt)

BRUTAL: Jeder Verlierer wird mit einem Finisher K.O.'d!
```

**Finishing Rule Details**:
- ❌ **NICHT bei 20% HP** - Kampf geht bis zum Ende!
- ✅ **NUR wenn HP = 0** - Dann Finisher-Auswahl
- Gewinner wählt einen von mehreren Finishern (wie Nemesis Arena)
- Finisher-Auswahl-Screen erscheint nach K.O.
- Finisher-Animation wird abgespielt (3-5 Sekunden)
- Verlierer wird spektakulär besiegt
- Zuschauer jubeln/buhen basierend auf Performance

**Combat-Control** (wie Modus 2 oben):
- Spieler kann JEDE TURNIER-RUNDE wählen:
  - KI-Kontrolle, Direkte Befehle, oder Digimon-Anfeuern
  - Modi sind pro Runde wechselbar
  - Maximale Flexibilität für jeden Kampf

**Teilnahme**:
- Einschreibung: 500 Gold (Entry Fee)
- Zeitfenster: 24 Stunden vor Turnier-Start
- Level-Beschränkungen:
  - Anfänger-Turnier: Schleim Level 1-20
  - Fortgeschrittenen-Turnier: Level 21-40
  - Meister-Turnier: Level 41+

**Async-System** (Optional):
- NPCs werden automatisch generiert wenn nicht genug Spieler
- Spieler-Kämpfe können asynchron sein (KI übernimmt Gegner-Kontrolle)
- Ergebnisse werden gespeichert und Bracket aktualisiert

**Rewards**:
- **1. Platz (Champion)**:
  - 5000 Gold
  - Titel: "Schleim-Champion" (7 Tage)
  - Spezielles Item: "Goldener Schleim-Pokal" (Display-Item)
  - Ruhm: +100 Punkte
  - Statue in der Arena (temporär)
- **2. Platz**:
  - 2000 Gold
  - Titel: "Silber-Kämpfer" (7 Tage)
  - Ruhm: +50 Punkte
- **3. Platz**:
  - 1000 Gold
  - Ruhm: +25 Punkte

**Turnier-Kalender**:
- Jeden Montag (in-game): Anfänger-Turnier
- Jeden Donnerstag (in-game): Fortgeschrittenen-Turnier
- Jeden Samstag (in-game): Meister-Turnier
- Monatlich: Grand Championship (alle Levels, höhere Preise)

---

## UI-INTEGRATION

### Hauptmenü (beim Betreten der Schleim-Arena)

```
╔══════════════════════════════════════════╗
║     🟢 SCHLEIM-ARENA - DIE GRUBE 🟢     ║
╚══════════════════════════════════════════╝

"Willkommen, Kämpfer! Was darf's sein?"
  - Schleimiger Pete

┌──────────────────────────────────────────┐
│ [1] 🥊 1v1 Normal                        │
│     Klassisches Duell                    │
│     Reward: 100-500 Gold + XP            │
├──────────────────────────────────────────┤
│ [2] 💥 1v1 mit Finisher                  │
│     Spektakuläre Finishing Moves!        │
│     Reward: 200-1000 Gold + Ruhm         │
├──────────────────────────────────────────┤
│ [3] 🏆 Turnier                           │
│     Nächstes: Montag 18:00 Uhr           │
│     Entry Fee: 500 Gold                  │
│     Teilnehmer: 4/8                      │
├──────────────────────────────────────────┤
│ [4] 📊 Rangliste                         │
│     Top Schleim-Kämpfer                  │
├──────────────────────────────────────────┤
│ [X] Verlassen                            │
└──────────────────────────────────────────┘
```

### In-Combat UI (1v1 mit Finisher)

```
╔══════════════════════════════════════════╗
║  Dein Schleim (Feuer)    VS    Pete's Eis-Schleim  ║
╠══════════════════════════════════════════╣
║  HP: ████████░░ 80/100   HP: ██████████ 100/100   ║
║  Finisher: ██████░░░░ 60%     Finisher: ███░░░░░░░ 30%    ║
╚══════════════════════════════════════════╝

┌──────────────────────────────────────────┐
│ [1] 🔥 Feuer-Angriff (15 DMG)            │
│ [2] 🛡️ Verteidigung (+50% DEF)          │
│ [3] 💊 Item benutzen                     │
│ [4] 💥 FINISHER! (nur wenn 100%)         │
└──────────────────────────────────────────┘

Log:
> Dein Schleim greift an! (15 DMG)
> Pete's Schleim verteidigt sich!
> Finisher +5%
```

### Turnier-Bracket UI

```
╔══════════════════════════════════════════╗
║       🏆 SCHLEIM-TURNIER - BRACKET       ║
║         Anfänger-Turnier (Level 1-20)    ║
╚══════════════════════════════════════════╝

HALBFINALE:
┌─────────────────────┐
│ Kuja's Feuer-Schleim│───┐
│       vs            │   │
│ Pete's Eis-Schleim  │   │  FINALE:
└─────────────────────┘   ├──────► ???
                          │
┌─────────────────────┐   │
│ Anna's Blitz-Schleim│───┘
│       vs            │
│ Tom's Wald-Schleim  │
└─────────────────────┘

Dein nächster Kampf:
[▶ Kampf starten]
```

---

## BACKEND-INTEGRATION

### API-Endpoints (Game Server - Port 8001)

```python
# /api/slime-arena/modes
GET - Liste aller Modi + Status

# /api/slime-arena/duel/start
POST - Starte 1v1 Duell (normal oder finisher)
Body: { "mode": "normal" | "finisher", "opponent_id": int }

# /api/slime-arena/duel/action
POST - Führe Action aus (attack, defend, item, finisher)
Body: { "duel_id": int, "action": string, "target": int }

# /api/slime-arena/tournament/join
POST - Turnier beitreten
Body: { "tournament_id": int, "entry_fee": 500 }

# /api/slime-arena/tournament/bracket
GET - Hole aktuelles Bracket
Params: tournament_id

# /api/slime-arena/leaderboard
GET - Top Schleim-Kämpfer
Params: limit (default 10)
```

### Datenbank-Schema

```sql
-- Schleim-Arena Duelle
CREATE TABLE slime_duels (
    id INTEGER PRIMARY KEY,
    player1_id INTEGER,
    player2_id INTEGER,
    slime1_id INTEGER,
    slime2_id INTEGER,
    mode VARCHAR(20), -- 'normal', 'finisher'
    winner_id INTEGER,
    rounds_data JSON, -- Combat log
    rewards JSON,
    created_at TIMESTAMP,
    finished_at TIMESTAMP
);

-- Turniere
CREATE TABLE slime_tournaments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    level_min INTEGER,
    level_max INTEGER,
    entry_fee INTEGER,
    max_participants INTEGER,
    status VARCHAR(20), -- 'registration', 'active', 'finished'
    bracket JSON,
    rewards JSON,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- Turnier-Teilnahmen
CREATE TABLE tournament_participants (
    id INTEGER PRIMARY KEY,
    tournament_id INTEGER,
    player_id INTEGER,
    slime_id INTEGER,
    placement INTEGER, -- 1st, 2nd, 3rd, etc.
    prize_claimed BOOLEAN
);

-- Rangliste
CREATE TABLE slime_arena_stats (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    slime_id INTEGER,
    total_fights INTEGER,
    wins INTEGER,
    losses INTEGER,
    finishers_used INTEGER,
    tournaments_won INTEGER,
    fame_points INTEGER,
    current_title VARCHAR(50)
);
```

---

## FRONTEND-INTEGRATION

### Neue Dateien

**1. `digivice/js/slime_arena.js`** - Hauptlogik
- Arena-Menü
- Modus-Auswahl
- Backend-API-Calls

**2. `digivice/js/slime_arena_combat.js`** - Kampf-System
- Turn-Based Combat
- Finisher-System
- Animations

**3. `digivice/js/slime_arena_tournament.js`** - Turnier-System
- Bracket-Verwaltung
- Teilnahme-Logic
- Async-Kampf-Simulation

**4. `digivice/css/slime_arena.css`** - Styling
- Arena UI
- Kampf-Overlays
- Bracket-Display

### Integration in World

**3D-Scene Integration** (`3d_scene.js`):
```javascript
// Beim Betreten des Gebäudes neben Nemesis Arena
if (buildingName === "Schleim-Arena") {
    if (window.SlimeArena && typeof window.SlimeArena.open === 'function') {
        window.SlimeArena.open();
    }
}
```

**Building hinzufügen** (`city_builder.js` oder `custom_buildings.js`):
```javascript
// Position neben Nemesis Arena in Handelsfeste
const slimeArenaPos = [arenaX + 50, 0, arenaZ + 30]; // Seitlich versetzt
CustomBuildings.buildSlimeArena(slimeArenaPos, 0.5, scene);
```

---

## SCHLEIM-STATS FÜR COMBAT

Jeder Schleim hat Stats für Arena:

```javascript
{
    "id": 1,
    "name": "Mein Feuer-Schleim",
    "color": "molten_red",
    "level": 15,
    "stats": {
        "hp": 120,
        "attack": 25,
        "defense": 15,
        "speed": 18,
        "luck": 10
    },
    "moves": [
        { "name": "Tackle", "power": 10, "type": "physical" },
        { "name": "Ember", "power": 15, "type": "fire", "element": "fire" },
        { "name": "Flame Burst", "power": 25, "type": "fire", "element": "fire", "finisher": true }
    ],
    "finisher": {
        "name": "Inferno Burst",
        "power": 100,
        "animation": "fire_explosion",
        "description": "Massive Feuer-Explosion die alles verbrennt!"
    }
}
```

---

## FINISHER-ANIMATIONEN

### Visual Effects (pro Element)

**Feuer** (Inferno Burst):
- Screen Flash (orange/rot)
- Particle Explosion (Flammen)
- Screen Shake (stark)
- Sound: Explosion + Feuer-Whoosh

**Eis** (Glacial Spike):
- Screen Flash (blau/weiß)
- Eis-Speer erscheint von oben
- Splitter-Partikel
- Sound: Glas-Zerbrechen + Eis-Knacken

**Blitz** (Thunder Strike):
- Screen Flash (gelb/violett)
- Blitz vom Himmel
- Elektrische Partikel
- Sound: Donner + Elektro-Zischen

**Etc.** für alle 9 Schleim-Farben

---

## PROGRESSION & REWARDS

### Fame-System (Ruhm-Punkte)

**Punkte sammeln durch**:
- 1v1 Normal Sieg: +5 Fame
- 1v1 Finisher Sieg: +10 Fame
- Turnier Top 3: +25/50/100 Fame
- Perfekte Siege (kein Damage genommen): +15 Fame Bonus

**Fame-Titel** (automatisch vergeben):
- 0-99: Anfänger
- 100-499: Kämpfer
- 500-999: Veteran
- 1000-2499: Champion
- 2500+: Legende

**Fame-Belohnungen**:
- 500 Fame: Zugang zu Fortgeschrittenen-Turnieren
- 1000 Fame: Spezial-Move "Rage Mode" (Damage +20% für 3 Runden)
- 2500 Fame: Goldene Schleim-Rüstung (Cosmetic für Schleim)

---

## PHASE 1 IMPLEMENTATION (MVP)

**Minimum Viable Product** für erste Version:

✅ **MUST HAVE**:
1. Gebäude in Handelsfeste (neben Arena)
2. NPC "Schleimiger Pete"
3. 1v1 Normal Modus (funktionsfähig)
4. Turn-Based Combat System
5. Basic UI (Menü + Combat)
6. Backend API (Duel Start/Action)
7. Rewards (Gold + XP)

⏳ **LATER** (Phase 2):
1. Finisher-System (Animations + Meter)
2. Turnier-System (Bracket + Async)
3. Rangliste + Fame
4. Hinterhof/Keller 3D-Models
5. Sound Effects
6. Advanced Animations

---

## TECHNISCHE NOTIZEN

**Combat-System basiert auf**:
- `turn_based_battle_minigame.js` (bereits vorhanden)
- Anpassung für Schleim-vs-Schleim

**Finisher-System ähnlich zu**:
- `realtime_combat.js` Cheer-System
- Aber rundenbasiert statt Echtzeit

**Turnier-System inspiriert von**:
- Pokemon Tournaments
- Fighting Game Brackets
- Async-Processing möglich

---

## BALANCING

### Combat-Balancing

**Damage-Formel**:
```
Base Damage = Move Power
Attack Modifier = (Attacker Attack / Defender Defense)
Critical = Random(1-20) == 20 ? 2x : 1x
Element Bonus = Element Advantage ? 1.5x : 1.0x

Final Damage = Base * Attack Modifier * Critical * Element Bonus
```

**Element-System** (Rock-Paper-Scissors):
- Feuer > Eis > Blitz > Wasser > Feuer
- Natur > Wasser, Erde > Blitz
- Licht <-> Dunkel (neutral)

**Level-Scaling**:
- Stats steigen mit Level
- Level 1: HP 50, ATK 10, DEF 5
- Level 50: HP 250, ATK 50, DEF 25
- Formel: Base + (Level * Wachstum)

---

## ZUKUNFTS-FEATURES (Post-Launch)

**Mögliche Erweiterungen**:
1. **2v2 Team-Kämpfe** - Zwei Schleime pro Seite
2. **Zuschauer-Wetten** - NPCs/Spieler wetten auf Kämpfe
3. **Schleim-Training** - Mini-Games zum Stats-Boost
4. **Arena-Customization** - Spieler können Arena dekorieren
5. **Saison-System** - Saisonale Turniere mit exklusiven Preisen
6. **Replay-System** - Kämpfe aufzeichnen & anschauen
7. **Commentary** - Pete kommentiert Kämpfe

---

## ZUSAMMENFASSUNG

**Schleim-Arena** ist ein kleines, charmantes Nebengebäude zur großen Nemesis Arena. Es bietet fokussiertes Schleim-vs-Schleim Combat in 3 Modi:

1. **1v1 Normal** - Schnell, einfach, Geld verdienen
2. **1v1 Finisher** - Spektakulär, mehr Rewards, Ruhm
3. **Turnier** - Kompetitiv, große Preise, Titel

Das System ist **modular** aufgebaut und kann schrittweise erweitert werden. Phase 1 (MVP) fokussiert auf funktionierendes Combat, spätere Phasen fügen Finisher, Turniere und Features hinzu.

**Zielgruppe**: Spieler die ihre Schleime trainieren wollen, kompetitiv spielen möchten, oder einfach nur Spaß an Turn-Based Combat haben.

---

**STATUS**: ✅ Design Complete - Ready for Implementation
**NEXT**: Warten auf Najika's 2. Durchgang (~3h), dann Implementierung starten
