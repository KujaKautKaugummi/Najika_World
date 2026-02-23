# NAJIKA MAGIC & SKILL SYSTEM - DESIGN PLAN

**Status:** PLANUNG - Noch NICHT implementieren!
**Inspirationen:** Konosuba + Skyrim + ESO + Fallout 4/76

---

## 🎯 DESIGN ZIELE

1. **Learning by Doing** (Skyrim) - Skills steigen durch Nutzung
2. **Einzigartige Explosion** (Konosuba) - Megumin's Signatur
3. **Skill Lines mit Morphs** (ESO) - Progression mit Entscheidungen
4. **Perks System** (Skyrim + Fallout) - Spezialisierung
5. **S.P.E.C.I.A.L.-Style Stats** (Fallout) - Klare Attribute

---

## 📊 BEISPIELE AUS DEN SPIELEN

### 🔥 SKYRIM - Was wir übernehmen:

**Magieschulen:**
| Schule | Beschreibung | Najika-Äquivalent |
|--------|--------------|-------------------|
| Destruction | Feuer/Eis/Blitz Schaden | ✅ Unsere 3 Haupt-Elemente |
| Restoration | Heilung + Anti-Undead | ✅ Licht-Magie |
| Alteration | Rüstung + Utility | ✅ Erde/Wind |
| Conjuration | Beschwörung | 🤔 Slime-System? |
| Illusion | Crowd Control | ✅ Dunkelheit |
| Enchanting | Verzauberung | ✅ Handwerk |

**Skyrim Progression Beispiel:**
```
Flammenstrahl (Novize) → Level 25 freischaltet Feuerball
→ Level 50 freischaltet Feuersturm
→ Level 75 freischaltet Feuer-Perks
→ Level 100 = Meister + Dual-Cast Perks
```

**Skyrim Perks (Beispiel Destruction):**
- Novize: -50% Mana-Kosten für Novizen-Zauber
- Apprentice: -50% Mana-Kosten für Lehrlings-Zauber
- Augmented Flames 1/2: +25/50% Feuerschaden
- Impact: Dual-Cast Zauber können staggern
- Intense Flames: Brennende Feinde fliehen bei <20% HP

---

### ⚔️ ESO - Was wir übernehmen:

**Skill Lines:**
```
Klassen-Skills:
├── Sorcerer → Storm Calling (Blitz)
├── Templar → Aedric Spear (Licht)
├── Nightblade → Shadow (Dunkel)
└── Dragonknight → Ardent Flame (Feuer)

Waffen-Skills:
├── Two-Handed
├── Dual Wield
├── Bow
└── Destruction Staff (Feuer/Eis/Blitz)

Gilden-Skills:
├── Fighters Guild (Anti-Daedra/Undead)
├── Mages Guild (Utility)
└── Undaunted (Dungeon Skills)
```

**ESO Morph Beispiel - Crystal Shard:**
```
Crystal Shard (Base)
├── Crystal Fragments (Morph A)
│   └── 35% Chance auf Instant-Cast nach Heavy Attack
└── Crystal Blast (Morph B)
    └── AOE Schaden statt Single Target
```

**ESO Ultimate Beispiel:**
```
Meteor (300 Ultimate)
├── Ice Comet (Morph A): +Slow Effekt
└── Shooting Star (Morph B): +Ultimate zurück pro Feind getroffen
```

---

### 💥 KONOSUBA - Was wir übernehmen:

**Megumin's Explosion:**
```
- NUR Explosion, keine anderen Zauber
- 1x pro Tag verwendbar
- MASSIVER Schaden
- Danach: Kann sich nicht bewegen!
- Langer Cast (Chanting!)
- Visuell SPEKTAKULÄR

Unsere Umsetzung:
- Explosion School = EINZIGARTIG
- Gebot #3: NIEMALS mit anderen kombinieren!
- Daily Limit: 1x
- Exhaustion: 60s Movement Lock
- Cast Time: 5 Sekunden (mit Chant!)
```

**Aqua's "Useless" Heilung:**
```
- Starke Heilung
- Aber: Zieht Untote an!
- Kann nicht lügen

Unsere Umsetzung:
- Licht-Magie heilt stark
- Aber: Aggro-Erhöhung?
```

**Darkness' Masochismus:**
```
- Tanky, aber trifft nie
- Genießt Schaden

Unsere Umsetzung:
- Tank-Skill-Line mit Miss-Chance aber Damage Reduction?
```

---

### 🔫 FALLOUT 4/76 - Was wir übernehmen:

**S.P.E.C.I.A.L. System:**
```
S - Strength     → Nahkampf-Schaden, Traglast
P - Perception   → Präzision, Crit-Chance
E - Endurance    → HP, Resistenzen
C - Charisma     → NPC-Interaktionen, Preise
I - Intelligence → Mana, XP-Bonus, Crafting
A - Agility      → Ausweichen, Speed, Stamina
L - Luck         → Crit-Schaden, Drops, Events
```

**Fallout Perk Cards (76 Style):**
```
Stärke-Perks:
├── Gladiator (1★-3★): +10/15/20% Einhand-Schaden
├── Slugger (1★-3★): +10/15/20% Zweihand-Schaden
└── Blocker (3★): -45% Nahkampf-Schaden erhalten

Intelligenz-Perks:
├── Nerd Rage (3★): <20% HP = +40 Schaden, +40 Resistenz
├── Demolition Expert (5★): +100% Explosions-Schaden
└── Gunsmith (5★): Waffen halten 50% länger
```

**Fallout Legendary Effects:**
```
Waffen-Effekte:
├── Bloodied: Mehr Schaden je weniger HP
├── Junkie's: Mehr Schaden pro Sucht
├── Two-Shot: Feuert 2 Projektile
├── Explosive: Jeder Treffer explodiert
└── Anti-Armor: Ignoriert 50% Rüstung

Rüstungs-Effekte:
├── Unyielding: +3 SPECIAL bei <25% HP
├── Bolstering: +35 Resistenz bei <25% HP
└── Sentinel: -15% Schaden beim Stehen
```

---

## 🎮 NAJIKA'S VORGESCHLAGENES SYSTEM

### Stats (Fallout-inspired):

```
POW - Power (Stärke)
    → Physischer Schaden, Traglast
    → +2% Nahkampf-Schaden pro Punkt

INT - Intellect (Intelligenz)
    → Magischer Schaden, Mana-Pool
    → +3% Spell-Schaden pro Punkt
    → +10 Max-Mana pro Punkt

AGI - Agility (Beweglichkeit)
    → Ausweichen, Angriffs-Speed
    → +1% Dodge pro Punkt
    → +1% Attack Speed pro Punkt

VIT - Vitality (Vitalität)
    → HP, Regeneration
    → +15 Max-HP pro Punkt
    → +0.5% HP-Regen pro Punkt

WIL - Willpower (Willenskraft)
    → Mana-Regen, CC-Resistenz
    → +1% Mana-Regen pro Punkt
    → +2% CC-Resistenz pro Punkt

LUK - Luck (Glück)
    → Crits, Drops, Events
    → +1% Crit-Chance pro Punkt
    → +5% Crit-Schaden pro Punkt
```

### Magieschulen (Skyrim + Konosuba):

```
DESTRUKTION:
├── 🔥 Feuer - Damage over Time, Burst
├── ❄️ Eis - Slow, Control
├── ⚡ Blitz - High Burst, Stun
└── 💥 EXPLOSION - Megumin's Kunst! (NIEMALS kombinieren!)

ALTERATION:
├── 🪨 Erde - Defense, Knockdowns
├── 💨 Wind - Mobility, Speed
└── 💧 Wasser - Cleanse, Support

RESTORATION:
├── ✨ Licht - Heilung, Anti-Undead
└── 🌑 Dunkelheit - Debuffs, Stealth
```

### Skill Progression (Skyrim Learning by Doing):

```
FEUER Schule:
Level 1:   Flammen (Basisangriff)
Level 10:  Feuerball (AOE)
Level 25:  Feuerwand (DoT Zone)
Level 50:  Meteorregen (Ultimate)
Level 75:  Perk: Feuermeisterschaft (+50% Schaden)
Level 100: Perk: Phönix-Flammen (Selbst-Rez bei Tod)

EXPLOSION Schule: (Konosuba Special!)
Level 1:   Explosions-Affinität (Passive)
Level 10:  Kleine Explosion
Level 25:  Mittlere Explosion
Level 50:  EXPLOSION!!! (1x/Tag, danach erschöpft!)
Level 75:  Perk: Crimson Augen (Kann nicht verfehlen)
Level 100: Perk: REINSTE EXPLOSION (+1 tägliche Nutzung)
```

### Morphs (ESO Style):

```
FEUERBALL (Level 10):
Bei Level 4 in diesem Skill wähle Morph:

Option A: METEOR
├── +100% Schaden
├── +Knockdown
├── Cast-Zeit: 2.5s → 4s
└── Cooldown: 6s → 15s

Option B: STREUSCHUSS
├── 3 kleinere Feuerbälle
├── -40% Schaden pro Ball
├── Schnellerer Cast
└── Gut gegen Gruppen
```

### Perks (Fallout Card Style):

```
FEUER-PERKS (1-5 Punkte investierbar):
├── Feuerkraft ★★★★★ (+10% Feuerschaden/★)
├── Brandstifter ★★★ (Brennen-DoT +20%/★)
├── Feuertanz ★★ (Immun gegen eigenes Feuer)
└── Phönix ★ (1x/Tag: Bei Tod → 50% HP)

EXPLOSION-PERKS (Konosuba Special!):
├── Explosions-Affinität ★★★★★ (+20% Schaden/★)
├── Schneller Chant ★★★ (-0.5s Cast-Zeit/★)
├── Ausdauer ★★★ (-10s Erschöpfung/★)
└── Megumin's Erbe ★ (+1 tägliche Nutzung)
```

### Legendary Effects (Fallout Inspired):

```
WAFFEN:
├── Explosiv - Jeder Treffer hat Mini-Explosion
├── Vampirisch - Heilt 5% des Schadens
├── Blutig - +50% Schaden bei <25% HP
├── Göttlich - +100% gegen Untote
└── Najika's Segen - Zufälliger Najika-Kommentar!

RÜSTUNG:
├── Sentinel - -15% Schaden beim Stehen
├── Cavalier - -15% Schaden beim Sprinten
├── Assassine - +75% Sneak-Schaden
└── Tamagotchi - Najika heilt dich manchmal!
```

---

## ❓ FRAGEN AN DICH (Kuja):

1. **Stats:**
   - Gefällt dir das 6-Stat System (POW/INT/AGI/VIT/WIL/LUK)?
   - Oder lieber klassisch (STR/DEX/INT/VIT)?

2. **Magieschulen:**
   - 9 Schulen (wie jetzt) oder weniger?
   - Soll Wasser eine eigene Schule sein oder Teil von Eis?

3. **Explosion:**
   - 1x pro Tag oder 1x pro Kampf?
   - Wie lange Erschöpfung? (aktuell 60s)

4. **Morphs:**
   - Bei welchem Skill-Level? (ESO = Level 4)
   - Können Morphs rückgängig gemacht werden?

5. **Perks:**
   - Fallout-Style (Punkte investieren) oder Skyrim-Style (Freischalten bei Level)?
   - Maximale Perk-Punkte?

6. **Legendary Effects:**
   - Sollen sie existieren?
   - Wie selten? (Fallout: ~1% Drop-Chance)

---

## 📝 NÄCHSTE SCHRITTE (nach Feedback)

1. [ ] Stats System finalisieren
2. [ ] Magieschulen finalisieren
3. [ ] Skill Trees designen
4. [ ] Perk System designen
5. [ ] Legendary System designen
6. [ ] JSON/Datenstruktur erstellen
7. [ ] Backend implementieren
8. [ ] Frontend UI erstellen

---

*"Lass uns das PERFEKT machen! Nicht schnell, sondern GUT!" - Najika* 💥
