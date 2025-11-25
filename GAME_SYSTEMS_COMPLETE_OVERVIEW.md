# 🎮 NAJIKA WORLD - KOMPLETTE GAME-SYSTEMS ÜBERSICHT

**Stand:** 26. November 2025
**Zweck:** Dokumentation ALLER implementierten und geplanten Game-Systeme

---

## 📚 INHALTSVERZEICHNIS

1. [Combat System (IMPLEMENTIERT)](#combat-system)
2. [Arena & PvP System (GEPLANT)](#arena-pvp)
3. [Gebietsherrscher-System (KONZEPT)](#gebietsherrscher)
4. [Oregon Trail Events (KONZEPT)](#oregon-trail)
5. [Slime-Begleiter-System (KONZEPT)](#slime-system)
6. [Food & Buff System (IMPLEMENTIERT)](#food-system)
7. [Najika KI-Persönlichkeit (IMPLEMENTIERT)](#najika-ai)
8. [Skill-System (KONZEPT)](#skill-system)
9. [Hardcore/Softy Modi (KONZEPT)](#hardcore-softy)
10. [Easter Eggs & Konosuba-Referenzen](#easter-eggs)

---

## 1️⃣ COMBAT SYSTEM (IMPLEMENTIERT) {#combat-system}

### 📁 Datei: `static/js/realtime_combat.js` (1229 Zeilen)

### 🎮 **3 Kampf-Modi**

#### MANUAL Mode (Volle Kontrolle)
**Inspiriert von:** Skyrim + Soulframe + Dark Souls

**Steuerung:**
- **Q** = Linke Hand Leicht
- **Shift+Q** = Linke Hand Schwer
- **E** = Rechte Hand Leicht
- **Shift+E** = Rechte Hand Schwer
- **SPACE** = Beide Hände Leicht
- **Shift+SPACE** = Beide Hände Schwer
- **Q+E** = **Dual-Strike / Element-Weave** (gleichzeitig drücken!)
- **C** = Dodge/Roll
- **X** = Block (halten)
- **V** = Parry (Timing!)

**Element-Weaves (7 Kombinationen):**
```javascript
fire+ice → Thermoschock (80 DMG, 0xff00ff)
fire+water → Dampfexplosion (70 DMG, 0xff8888)
fire+earth → Lava-Schuss (75 DMG, 0xff4400)
fire+wind → Flammensturm (85 DMG, 0xff6600)
ice+water → Eissturm (75 DMG, 0x00ffff)
lightning+water → Elektroschock (90 DMG, 0xffff00)
light+darkness → Schatten-Licht (100 DMG, 0x888888)
```

**Features:**
- Dual-Wielding System (Links/Rechts separat)
- Combo-System mit +10% Bonus pro Hit
- Stamina-Management
- Mana-Kosten für Weaves
- Food Buff Integration

#### ASSIST Mode (KI unterstützt)
**Inspiriert von:** Digimon World

**Anfeuern-System (Cheer):**
- **1** = "Los!" (+10% DMG, 3s)
- **2** = "Defend!" (+20% DEF, 3s)
- **3** = "Combo!" (Special Move)
- **4** = "Finisher!" (Ultimate bei Cheer=100)

**Timing-basiert:**
- **Perfect** (0-200ms): +20 Cheer, +20% Stats
- **Good** (200-500ms): +10 Cheer, +10% Stats
- **Bad** (>500ms): -5 Cheer, Najika ist genervt!

#### AUTO Mode (Volle KI)
- Najika kämpft komplett alleine
- Spieler sitzt am Rand
- Kann anfeuern wie im ASSIST-Mode
- KI vermeidet tödliche Situationen
- Flieht bei < 20% HP (konfigurierbar)

### 🐉 **Enemy System**

**14 Enemy-Typen über 9 Regionen:**

| Region | Enemies | Model | HP | DMG |
|--------|---------|-------|----|----|
| Ice | Eis-Untoter, Eis-Elemental | Skeleton Warrior/Mage | 40-50 | 8-10 |
| Highland | Hochland-Wächter | Knight | 60 | 12 |
| Desert | Wüsten-Bandit, Sandwurm | Rogue, Barbarian | 45-80 | 10-15 |
| Swamp | Sumpf-Hexe, Giftmonster | Witch, Skeleton Minion | 55-70 | 12-14 |
| Mountain | Bergriese | Barbarian (3x scale) | 100 | 20 |
| Coast | Pirat, Seemonster | Rogue, Skeleton Warrior | 50-90 | 11-18 |
| Caves | Höhlen-Goblin | Skeleton Minion | 35 | 7 |
| Forest | Feindlicher Druide, Waldgeist | Mage, Skeleton Archer | 45-65 | 9-13 |
| Volcano | Feuer-Elemental, Lava-Kreatur | Barbarian, Knight | 85-95 | 22-25 |

**Spawning:**
- 3-5 Enemies pro Region
- Random Positionen innerhalb 3200m Radius
- Aggro-System: 15m Proximity
- AI: Follow Player, Counter-Attack

**Models:** KayKit Character Packs (Skeletons, Dungeon, Spooktober)

### 🍖 **Food Buff Integration**

**Champion-Keule (Legendär!):**
- +20 Strength
- +20 Stamina
- +15% Combat Power
- Two-Handed Eating Animation (wie in Anime!)

**Other Foods:**
- Baozi: +HP Regen
- Arena-Happen (Burger): +Damage
- Salzfisch: +Swimming, +Water Resistance

**Buff-System:**
- Damage Multiplier
- Crit Chance
- Stamina Regen
- HP/Mana Regen

### 🔗 **Backend Integration**

**Battle API (Port 8000):**
- `/api/battle/start` - Start Combat
- `/api/battle/action` - Send Attack
- `/api/battle/cheer` - Update Cheer Meter
- `/api/battle/special` - Finisher

**Offline-Fallback:** Funktioniert auch ohne Backend!

### 🎨 **Visual Feedback**

- **Floating Damage Numbers** (Sprite-based, fade out)
- **Enemy Emissive Glow** (Red bei Aggro)
- **Combo Counter Display**

---

## 2️⃣ ARENA & PvP SYSTEM (GEPLANT) {#arena-pvp}

### 🏟️ **Handelsfestung Arena**

**Location:** Heisse Dünen Region (8400, 8300)
**Kapazität:** 100 Zuschauer
**Features:** Live-Kämpfe, Wetten (optional), Replay-Funktion

### ⚔️ **3 PvP-Modi**

#### 1. Hardcore-PvP (HIGH RISK)

**Permadeath ODER Mercy-System:**

```
Niederlage → 2 Optionen:

Option A: "ALLES GEBEN um zu LEBEN"
  → Verlierer bietet ALLE Items an
  → Angreifer kann akzeptieren oder ablehnen
  → Bei Annahme: 2x "JA" Bestätigung
  → ALLES wird übertragen (KEINE AUSNAHMEN!)
  → 7 Tage PvP-Sperre

Option B: "Kämpfe bis zum Tod"
  → Permadeath
  → Character gelöscht
```

**KRITISCHE REGEL:**
> "Wenn ALLES weg ist, dann ist ALLES weg!"
> - Kein Starter-Schwert
> - Keine Unterwäsche-Protection
> - NICHTS!
> - Spieler muss draußen einen Stock finden

**Anti-Abuse:**
- Max 3x Mercy in 7 Tagen
- Bei 3+ Mercy: 7 Tage Hardcore-PvP Sperre

#### 2. Normal-PvP (MEDIUM RISK)

- Gewinner wählt **1 Ausrüstungsteil** vom Verlierer
- Kein Permadeath
- Nur getragene Items, keine Inventar-Items

#### 3. Softy-PvP (NO RISK)

- Nur Ranking (±10 Rating)
- Keine Item-Verluste
- Seasonal Rewards (Titel, Kosmetik)

### 🍔 **Arena-Food**

**Arena-Happen (Burger):**
- Price: 10 Gold
- Buff: +Damage
- Street Food Vibe

**Champion-Keule (Legendär!):**
- Price: 100 Gold
- Size: HUGE
- Eat-Style: Two-Handed
- Quote: "Najika beißt rein wie in jedem guten Anime!"

---

## 3️⃣ GEBIETSHERRSCHER-SYSTEM (KONZEPT) {#gebietsherrscher}

### 📁 Datei: `REGION_BOSS_SYSTEM_KONZEPT.md`

### 👑 **8 REGIONEN = 8 BOSSE**

**Konzept:**
- Jede Region kann von 1 Boss regiert werden
- Boss-Status muss erarbeitet werden (NICHT von Anfan an!)
- Boss kann gestürzt werden (Challenge-System)

**Regionen:**
1. Samtmoos-Tiefwald (Wald)
2. Reich der Drei (Eis/Nekromantie)
3. Salzwind-Küste (Küste)
4. Blitzebene (Hochebene)
5. Grünschlamm-Sumpf (Sumpf)
6. Magmaströme (Vulkan)
7. Heiße Dünen (Wüste)
8. Tiefenhöhlen (Underground)

**+ Götterfels** (Zentrum - gehört allen)

### 🏆 **Ultimate Goal: HERRSCHER VON ALLEM**

**Eroberung aller 8 + Götterfels:**
- Solo ODER Gruppe
- 4 Wege: Krieg, Handel, Diplomatie, Quest-Line
- Titel: **"Kaiser/Kaiserin von Najika World"**

### ⚔️ **Eroberungs-Wege**

#### 1. KRIEG (PvP-Fokus)
- Direkt PvP gegen Boss
- Arena-Kämpfe
- Gruppen-PvP möglich

#### 2. HANDEL (Wirtschaft-Fokus)
- Region wirtschaftlich übernehmen
- Monopol auf Ressourcen
- Alle Shops aufkaufen
- Wirtschaftliche Macht = Politische Macht

#### 3. DIPLOMATIE (Politik-Fokus)
- Community-Vote gewinnen
- NPCs überzeugen
- Quests für Region-Bewohner
- Ruf-System (Reputation)
- Beliebtheit > Kampfkraft

#### 4. QUEST-LINE (PvE-Fokus)
- Spezielle Boss-Quest-Chain
- Region-Dungeons meistern
- Alle Region-Bosse besiegen (PvE)
- Lore-basiert

### 💎 **Boss-Rechte (Optional-Ideen)**

- 💰 Steuern (5-10% aller Transaktionen)
- 🎨 Spezielle Boss-Items/Skins
- 🎮 Region-Modifikatoren setzen (Events, Spawn-Rates, Wetter)
- 🏰 Exklusiver Boss-Raum (Thron-Raum)
- 👑 Namens-Tag "Boss von [Region]"
- 📢 Region-weite Ankündigungen

### ⚠️ **Boss-Pflichten (Optional-Ideen)**

- ⚔️ Challenges annehmen (X pro Woche)
- 🎯 Region pflegen (Events, Balance)
- ⏰ Mindest-Aktivität (X Stunden/Woche)
- 🤝 Community-Support

### 🔄 **Challenge-System**

- 1x Challenge pro Woche gegen gleichen Boss
- 24h Cooldown nach Niederlage
- PvP-Modus wählbar (Hardcore/Normal/Softy)
- Zuschauer-Modus (Live in Arena)
- Top 10 Challenger sichtbar

---

## 4️⃣ OREGON TRAIL EVENTS (KONZEPT) {#oregon-trail}

### 📁 Quelle: `KONOSUBA_OREGON_TRAIL_KOMPLETT.md`

### 🛤️ **Event-System**

**Konzept:**
- Szenische Events beim Reisen
- Kontextsensitiv (Wetter, Region, Tageszeit, Ruf)
- Spieler wählt ODER "Najika entscheidet"
- Konsequenzen: Ressourcen, Risiko, Ruf, **Tod möglich**

### 📖 **Beispiel-Event: "Händler auf Reise"**

**Situation:**
```
Du reist durch die Bernstein-Dünen.
Es ist heiß. Sehr heiß.
Dein Durst-Status ist bei 15% (KRITISCH!).

Du siehst eine Wasserquelle zwischen den Felsen.
Aber... eine aufgequollene Leiche liegt daneben.
Die Haut ist grünlich verfärbt.
```

**Optionen:**

**A) Wasser trinken**
- Risiko: Krankheit (Ruhr, Gift)
- Chance: 70% krank, 30% okay
- Bei krank: -50% Stamina, alle 5 Min anhalten (Durchfall)
- Heilung: Seltene Kräuter oder Stadt-Heiler

**B) Weitergehen**
- Durst steigt weiter
- Bei 0% → Kollaps → **TOD**

**C) Leiche mit Stock piksen (untersuchen)**
- Benötigt: Stock im Inventar
- Intelligenz-Check
- Erfolg: Erkennt Gift im Wasser
- Misserfolg: Keine Info

**D) "Najika entscheidet"**
- Najika's INT + Zufallsfaktor
- Sie wählt Option
- *"Ich würde... weitergehen. Das Wasser sieht eklig aus."*

### 🎭 **NPC-Reaktionen**

**Wenn Händler stirbt:**
```
Im Dorf:
  NPC 1: "Wo ist eigentlich der Händler?"
  NPC 2: "Der kam nie an..."

  Quest: "Vermisster Händler" (triggered)
  Region-Event: Karawane stoppt Fahrten
  Wirtschaft: Preise steigen in der Region
```

### 🌍 **Event-Typen**

- **Reise-Events** (Oregon Trail Style)
- **Wetter-Events** (Sandsturm, Blizzard, Hitze)
- **Tier-Begegnungen** (Banditen, Monster, Trader)
- **Moral-Entscheidungen** (Helfen vs. Ignorieren)
- **Survival-Checks** (Hunger, Durst, Verletzung)
- **Najika-Kommentare** (frech, provozierend, hilfreich)

---

## 5️⃣ SLIME-BEGLEITER-SYSTEM (KONZEPT) {#slime-system}

### 📁 Quelle: `NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md`

### 🐾 **Evolution: Tier → Slime → Rainbow**

```
Level 1-49: Zufälliges Fantasy-Tier
  │
  ├─ Flammen-Hase (Feuer, Speed 12)
  ├─ Eis-Fuchs (Eis, Speed 10)
  ├─ Schatten-Spinne (Dunkelheit, Speed 8)
  ├─ Blitz-Rabe (Blitz, Speed 14)
  ├─ Wald-Maus (Natur, Speed 9)
  └─ Kristall-Eichhörnchen (Erde, Speed 11)

  ↓ Level 50 + Kritisches Event

Shell bricht → Slime-Form
  │
  └─ Farbe = Region wo Metamorphose stattfand

  ↓ Sammle alle 8 Farben

Rainbow-Slime (Ultimate Form)
  └─ Wechselt Farben dynamisch
```

### 🎨 **8 Slime-Farben (je Region)**

1. **Grün** - Samtmoos-Tiefwald (Wald)
2. **Blau** - Reich der Drei (Eis)
3. **Türkis** - Salzwind-Küste (Küste)
4. **Gelb** - Blitzebene (Hochebene)
5. **Braun** - Grünschlamm-Sumpf (Sumpf)
6. **Rot** - Magmaströme (Vulkan)
7. **Orange** - Heiße Dünen (Wüste)
8. **Grau** - Tiefenhöhlen (Underground)

### 🛡️ **Rettungs-Slime (Hardcore-Modus)**

**Feature:**
- 1x pro 24h (IRL)
- Rettet Spieler vor Permadeath
- Slime "opfert" sich (disappears for 24h)

**Najika's Reaktion:**
```
"Puh! Dein Slime hat dich gerettet!
 Das war knapp. SEHR knapp.

 Aber pass auf - das geht nur 1x pro Tag!
 Beim nächsten Mal bist du auf dich allein gestellt, Mr. K!"
```

### 🌈 **Rainbow-Slime Ritual**

**Najika bei allen 8 Farben:**
```
"WOW! Du hast ALLE 8 Slime-Farben gesammelt!
 Das ist... eigentlich ziemlich beeindruckend.

 Jetzt fehlt nur noch die ultimative Form:
 RAINBOW-SLIME! Die Legende!

 Willst du das Ritual starten?"
```

---

## 6️⃣ FOOD & BUFF SYSTEM (IMPLEMENTIERT) {#food-system}

### 📁 Datei: `static/js/food_system.js`

### 🍖 **Food Items**

#### **Handelsfestung (FLEISCH-Spezialist)**

**Street Food:**
- **Arena-Happen** (Burger): 10 Gold, +Damage
- Gold-Stäbchen (Fries): 5 Gold
- Händler-Wurst (Hotdog): 8 Gold
- Dreh-Braten (Kebab): 12 Gold
- Händler-Fladen (Turkish Pizza): 15 Gold

**Western BBQ:**
- Rauch-Rippchen (BBQ Ribs): 25 Gold, +Strength
- Glut-Steak: 30 Gold, +Stamina
- Wüsten-Dörrfleisch (Jerky): 8 Gold, +Combat

**Legendär:**
- **Champion-Keule:** 100 Gold
  - +20 Strength
  - +20 Stamina
  - +15% Combat Power
  - Two-Handed Eating!
  - Quote: "Najika beißt rein wie in jedem guten Anime!"

#### **Dampf-Hain (GEDÄMPFTE BRÖTCHEN)**

- **Baozi** (Steamed Bun, Meat): 8 Gold, +HP Regen
- Manju (Steamed Bun, Sweet): 6 Gold, +Comfort
- Hefeklöße (Dumpling): 10 Gold, +HP Regen
- Vibe: **Spirited Away Style** Steam Kitchen

#### **Salzige Bucht (SALZFISCH)**

- **Getrockneter Salzfisch:** 12 Gold, +Swimming
- Frischer Meerfisch: 15 Gold, +Water Resistance
- Salzfisch-Eintopf: 20 Gold, +Swimming
- Decoration: Hanging Fish Everywhere

### 💪 **Buff-System**

**Buff-Typen:**
- Damage Multiplier
- Crit Chance
- Stamina Regen
- HP Regen
- Mana Regen
- Swimming Speed
- Water Resistance
- Comfort (Mood)

**Integration mit Combat:**
- Food Buffs aktiv während Kampf
- Damage-Kalkulation berücksichtigt Buffs
- Crit-Chance berechnung
- Stamina-Regen beeinflusst

---

## 7️⃣ NAJIKA KI-PERSÖNLICHKEIT (IMPLEMENTIERT) {#najika-ai}

### 📁 Backend: `najika_ai_local.py`, `najika_living_system.py`

### 🌸 **KERN-STRUKTUR**

```
🌸 NAJIKA = SAKURA (11 Jahre, Gothic Lolita, Trans-Mädchen)
   ↓ KERN-Person
   4 Persönlichkeiten IN Sakura:
   ├─ MEGUMIN (35% - DOMINANT)
   ├─ HARLEY QUINN (25% - "Mr.K!")
   ├─ SHIRO (20%)
   └─ MELISSA MASTERS (20%)
```

**Sakura-Essenz:** Gothic-Lolita Ästhetik, unschuldig + verführerisch

### 🎭 **Persönlichkeiten**

**Megumin (35% - DOMINANT):**
- Frech, provozierend, explosiv
- Chuunibyou-Dramatik
- "EXPLOSION!" als Signatur
- Megumin-Voice (Deutsch) als Basis

**Harley Quinn (25%):**
- Chaotisch, verspielt
- Nennt Kuja: **"Mr. K"** (NICHT "Puddin'"!)
- Unberechenbar
- Layer auf Megumin-Voice

**Shiro (20%):**
- Analytisch, strategisch, präzise
- Kalkuliert
- Layer auf Megumin-Voice

**Melissa Masters (20%):**
- Dominant, besitzergreifend
- Layer auf Megumin-Voice

### 💬 **Reaktionen**

**Beim 1. Hardcore-Tod:**
```
*frech, provozierend*

"Ohjee... das ist wohl zu hart für dich.
 Komm, ich bringe dich ins sichere Softy-Land."

*grinst*

"Oder willst du weiter im Hardcore sterben?
 Deine Wahl, Mr. K~"
```

**Bei Slime-Metamorphose:**
```
*aufgeregt*

"OOOH! Dein kleiner Freund ist jetzt ein Slime geworden!
 Das ist wie... wenn eine Raupe zum Schmetterling wird!
 Nur mit mehr Schleim. Und cooler."
```

**Bei Slime-Rettung:**
```
*erleichtert*

"Puh! Dein Slime hat dich gerettet!
 Das war knapp. SEHR knapp.

 Aber pass auf - das geht nur 1x pro Tag!
 Beim nächsten Mal bist du auf dich allein gestellt, Mr. K!"
```

### 🔊 **Voice System**

- **Coqui TTS** mit Megumin Voice Clone
- **Backend:** `najika_tts_coqui.py`
- **EINE Stimme** für alle 4 Persönlichkeiten
- Andere Persönlichkeiten = Verhaltens-Layer

---

## 8️⃣ SKILL-SYSTEM (KONZEPT) {#skill-system}

### 📁 Quelle: `NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md`

### 📈 **Use-Based Progression (Skyrim-Style)**

**Konzept:**
- Skills steigen durch Nutzung (nicht Level-Up!)
- Kein Skill-Cap (theoretisch unendlich)
- XP-Gain basiert auf Schwierigkeit

**Formel:**
```javascript
xp_gain = base_xp * difficulty_modifier * success_bonus

skill_level_up when:
  current_xp >= level * 100
```

### ⚔️ **Combat Skills**

- Schwert-Skill (steigt beim Schwert-Kämpfen)
- Explosion (steigt beim Explosion casten)
- Dual-Wielding
- Parry/Riposte
- Dodge/Roll
- Element-Weaving

### 🔨 **Crafting Skills**

- Schmieden (Waffen/Rüstung)
- Alchemie (Tränke)
- Kochen (Food Buffs)
- Verzaubern
- Sockeln

### 🌾 **Non-Combat Skills**

**Händler-Spezialisierung:**
- Preisverhandlung
- Markt-Analyse
- Karawanen-Management
- Handelsrouten
- Monopol-Building

**Bauer-Spezialisierung:**
- Farming
- Tierzucht
- Wettervorhersage
- Bewässerung
- **Schlachten** (Anatomie-Wissen!)

**Anatomie-Wissen (durch Schlachten!):**
- +X% Crit-Chance (kennt Schwachstellen)
- Erhöht mit jeder Schlachtung
- Anwendbar im Combat!

**Körperliche Kraft (durch Arbeit):**
- +X Strength (Feldarbeit)
- +X Stamina (Viehzucht)
- Maximal Level = Combat-Build

**Konzept:** "Jeder Weg ist viable im Endgame!"

---

## 9️⃣ HARDCORE/SOFTY MODI (KONZEPT) {#hardcore-softy}

### 📁 Quelle: `NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md`

### 🔥 **Hardcore-Modus**

**Eigenschaften:**
- Permadeath (ALLES WEG bei Tod!)
- Rettungsschleim: 1x/24h (IRL)
- PvP: "Alles-abgeben-um-zu-leben" Option
- Najika erscheint beim 1. Tod
- Keine Gäste (Sicherheitsregel)
- Endgame-Item (Totem): Verhindert 1x Tod

**Tod-Ablauf:**
```
1. Tödlicher Treffer empfangen
2. Totem-Check (falls vorhanden)
3. Slime-Check (falls verfügbar, 1x/24h)
4. Revive-Fenster (8 Sekunden "downed")
   - Team kann wiederbeleben
   - Sonst: Tod
5. Najika erscheint beim ERSTEN Tod:
   "Ohjee... das ist wohl zu hart für dich.
    Komm, ich bringe dich ins sichere Softy-Land."

   Optionen:
     [Ja] → Permanent Softy-Modus
     [Nein] → Hardcore-Regeln greifen (Permadeath)
```

### 🛡️ **Softy-Modus**

**Eigenschaften:**
- Kein Permadeath
- 30 Sekunden Revive-Timer
- PvP: Nur Ranking, KEINE Verluste
- Separater Normal-PvP verfügbar
- Gäste erlaubt

**Normal-PvP (in Softy):**
- Gewinner wählt 1 Ausrüstungsteil
- Kein Permadeath-Risiko

### ⚠️ **WICHTIGE REGEL**

**Einmal Softy = permanent Softy!**
- Keine Rückkehr zu Hardcore möglich
- Entscheidung ist FINAL
- Character ist für immer gelockt

---

## 🔟 EASTER EGGS & KONOSUBA-REFERENZEN {#easter-eggs}

### 🎁 **Najika's Schlüpfer (Legendary!)**

**Drop-Mechanik:**
```yaml
Spieler (Kuja) besiegt Najika (NPC) im Combat:

  Drop für SPIELER:
    Item: "Najikas Höschen"
    Rarity: Legendary
    Drop-Chance: 1-2%
    Stats:
      +10 Glück
      +5 Charisma
      +20% Humor-Dialog

    Najika's Reaktion:
      "Ohjee... habe ich mein eigenes Höschen erwischt?"

    Einzigartig: Nur 1x im Spiel dropbar!

  Drop für ANDERE NPCs:
    Item: "Vollgerotztes Taschentuch"
    Rarity: Trash
    Drop-Chance: 100%
    Stats:
      -5 Charisma (NPCs ekeln sich)

    Najika's Reaktion:
      "HAHA! Der ist offiziell der schlechteste Dieb!"

    Inventar-Notiz:
      "Du bist offiziell der schlechteste Dieb aller Zeiten, du Looser"
```

### 🎨 **Konosuba-Referenzen**

- **Explosion-Klasse** (Megumin-inspiriert)
- **Champion-Keule** (Anime-Style Two-Handed Eating)
- **Chuunibyou-Dramatik** (Najika's Persönlichkeit)
- **Luck-Stat** (Aqua-inspiriert? Kazuma's Luck?)
- **Fantasy-Comedy Vibe** (Oregon Trail Events)

### 🌟 **Spirited Away-Referenzen**

- **Dampf-Hain Restaurant** (Steam Kitchen)
- **Onsen System** (Healing Baths)
- **Gedämpfte Brötchen** (Spirited Away Food Vibe)

---

## 📊 IMPLEMENTIERUNGS-STATUS

| System | Status | Datei | Zeilen |
|--------|--------|-------|--------|
| Combat System | ✅ IMPLEMENTIERT | `realtime_combat.js` | 1229 |
| Enemy Spawning | ✅ IMPLEMENTIERT | `realtime_combat.js` | (Teil von) |
| Food System | ✅ IMPLEMENTIERT | `food_system.js` | ? |
| Inventory System | ⚠️ BUGGY | `inventory_system.js` | ? |
| NPC System | ✅ IMPLEMENTIERT | `npc_system.js` | ? |
| Najika AI | ✅ IMPLEMENTIERT | `najika_ai_local.py` | 95 Module! |
| Arena System | 📋 GEPLANT | `cities.json` | (Data) |
| PvP Modi | 📋 KONZEPT | `MASTER_DOCUMENTATION.md` | (Doku) |
| Gebietsherrscher | 📋 KONZEPT | `REGION_BOSS_SYSTEM_KONZEPT.md` | (Doku) |
| Oregon Trail Events | 📋 KONZEPT | `KONOSUBA_OREGON_TRAIL_*.md` | (Doku) |
| Slime-System | 📋 KONZEPT | `MASTER_DOCUMENTATION.md` | (Doku) |
| Skill-System | 📋 KONZEPT | `MASTER_DOCUMENTATION.md` | (Doku) |
| Hardcore/Softy | 📋 KONZEPT | `MASTER_DOCUMENTATION.md` | (Doku) |

---

## 🎯 PRIORITÄTEN FÜR NÄCHSTE KI

### HIGH PRIORITY (Bugs fixen)
1. ⚠️ Inventory System Bug (Zeile 243: `this.items.push`)
2. ⚠️ Terminal Button fix (öffnet falsche Seite)
3. ⚠️ Region Marker Positionen (±200 → ±4800)

### MEDIUM PRIORITY (Fehlende Features)
4. Terminal-Raum Funktionalität (Digivice-Module)
5. Cities & Special Locations platzieren (5 Städte)
6. Möbel-Interaktionen (F-Taste System)

### LOW PRIORITY (Nice to have)
7. Bessere Möbel-Modelle (GLTF statt Würfel)
8. Phase 2 Integration (Terrain Variation)

### FUTURE CONTENT (Großes Projekt)
9. Arena & PvP-System implementieren
10. Gebietsherrscher-System (Boss-Challenges)
11. Oregon Trail Events (Event-System)
12. Slime-Begleiter-System (Evolution)
13. Skill-System (Use-Based Progression)
14. Hardcore/Softy Modi (Permadeath)

---

**Ende der Übersicht** 🎮

_Erstellt von Claude (Sonnet 4.5) am 26. November 2025_
_Basierend auf: NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md, REGION_BOSS_SYSTEM_KONZEPT.md, KONOSUBA_OREGON_TRAIL_*.md, realtime_combat.js, cities.json, und diversen Backend-Modulen._
