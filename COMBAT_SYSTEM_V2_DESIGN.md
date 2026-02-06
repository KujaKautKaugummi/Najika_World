# ⚔️ NAJIKA WORLD - COMBAT SYSTEM V2 DESIGN

**Aktualisiert:** 2026-02-06

## 🎯 GRUNDPRINZIP

**Der Spieler ist IMMER im manuellen Modus** (außer in der Schleim-Arena).
Die 3 Kampfmodi (AUTO, MANUAL, CHEER) gelten für den **COMPANION**, nicht den Spieler!

**WICHTIG:** In der **Schleim-Arena** sind ALLE 3 Modi (AUTO, MANUAL, CHEER)
**JEDERZEIT WECHSELBAR** während des Kampfes!

---

## 📍 KONTEXT-UNTERSCHIEDE

### 🌍 GAME WORLD / SPIELER-ARENA

```
┌─────────────────────────────────────────────────────┐
│                    KAMPF                            │
│                                                     │
│  ┌─────────────┐         ┌─────────────────────┐   │
│  │   SPIELER   │         │     COMPANION       │   │
│  │  (MANUAL)   │         │ (AUTO/MANUAL/CHEER) │   │
│  │             │         │                     │   │
│  │ - Angriff   │         │ KÖRPERLICH:         │   │
│  │ - Skill     │         │ → Kämpft neben dir  │   │
│  │ - Item      │         │                     │   │
│  │ - Verteidig │         │ AURA:               │   │
│  └─────────────┘         │ → Passive Buffs     │   │
│                          └─────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Spieler-Arena Modi:**
| Modus | Beschreibung |
|-------|-------------|
| ☠️ HARDCORE | Echter Tod möglich! |
| ⚔️ NORMAL | Standard PvP/PvE |
| 🎓 SOFTY | Training, kein echter Tod |
| 🌊 WELLE | 15 Wellen überleben |

### 🐾 SCHLEIM-ARENA

```
┌─────────────────────────────────────────────────────┐
│              SCHLEIM-ARENA KAMPF                    │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │             DEIN SLIME                       │   │
│  │                                              │   │
│  │  🤖 AUTO: KI kämpft selbstständig           │   │
│  │  🎮 MANUAL: DU steuerst den Slime DIREKT!   │   │
│  │  📣 CHEER: Feuere an für Buffs              │   │
│  │                                              │   │
│  │  ↕️ JEDERZEIT WECHSELBAR WÄHREND KAMPF! ↕️   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  WICHTIG: In MANUAL übernimmst DU die Kontrolle!   │
└─────────────────────────────────────────────────────┘
```

**Schleim-Arena Modi:**
| Modus | Beschreibung |
|-------|-------------|
| ⚔️ NORMAL | Standard Slime-Kampf |
| 🌊 WELLE | Slime-Wellen-Überleben |

---

## 💀 FINISHER-SYSTEM

**Das Finisher-System ist in BEIDEN Arenen verfügbar!**

### Wie es funktioniert:

1. **Spieler gibt Wörter/Kategorie:**
   - 3-5 Wörter (z.B. "Feuer", "Katze", "Explosion")
   - Eine Kategorie (z.B. "Lustiger Tod", "Ehrenvoller Tod")

2. **Najika baut daraus einen Finisher:**
   - Kombiniert die Wörter kreativ
   - Passt zur gewählten Kategorie
   - In IHREM Megumin-Stil!

### Kategorien (BrutalityCategory):

| Kategorie | Beschreibung | Brutality | Humor |
|-----------|-------------|-----------|-------|
| Ehrenvoller Tod | Sauber, respektvoll | 3 | 2 |
| Lustiger Tod | Komisch, absurd | 5 | 10 |
| Grausamer Tod | Dunkel, sadistisch | 8 | 1 |
| Tod Tod Blut Blut | EXTREME Brutalität | 10 | 0 |
| Sinnloser Tod | Anti-klimaktisch | 4 | 7 |

### Finisher-Styles (automatisch basierend auf Wörtern):

| Style | Keywords | Beispiel |
|-------|----------|----------|
| EXPLOSION! | explosion, dynamit, bombe, feuer | Megumin-Style |
| Niedlich-Brutal | kuschel, plüsch, kawaii, cute | Happy Tree Friends |
| Chaotisch | chaos, anarchie, verrückt, wild | Harley Quinn |
| Berechnet | strategie, plan, logik, analyse | Shiro |
| Dominant | macht, herrsch, stark, überlegen | Melissa |

### Beispiel-Ablauf:

```
Spieler: ["Feuer", "Katze", "Explosion"], Kategorie: "Lustiger Tod"

Najika: "Ohoho! *dramatische Pose*
        Sieh diese unheilige Kombination!
        Eine BRENNENDE KATZEN-EXPLOSION!!!
        ...warte, das klingt gemein zur Katze...
        NEIN! Die Katze ist aus FEUER!
        EXPLOSIONS-KÄTZCHEN DES VERDERBENS!!! 💥🐱🔥
        *der Gegner explodiert in Konfetti-Flammen*
        Aww~ Das war niedlich! Hehe! 😇"
```

### Arena-Unterschiede:

| Aspekt | Spieler-Arena | Schleim-Arena |
|--------|---------------|---------------|
| Style | Episch, dramatisch | Lustig, cute |
| Narrator | Najika in Megumin-Style | Najika kommentiert |
| Verfügbar wenn | Gegner < 20% HP + Meter voll | Gegner < 20% HP |
| Belohnung | Fame + XP + Gold | Extra Fame |

### API Endpoints:

**Unified Battle API (Spieler-Arena + Game World):**
```http
POST /api/battle/finisher
{
  "player_id": "player_123",
  "words": ["Feuer", "Katze", "Explosion"],
  "category": "lustig",
  "target_index": 0
}
```

**Slime Arena API:**
```http
POST /api/slime-arena/finisher
{
  "duel_id": 123,
  "finisher_name": "Explosive Katzen-Doom",
  "target": "opponent"
}
```

**Kategorien abrufen:**
```http
GET /api/battle/finisher/categories
```

---

## 🐾 COMPANION-FORMEN

### KÖRPERLICH 🐾
Der Companion ist ein **physisches Wesen** neben dir.

**Eigenschaften:**
- Kämpft eigenständig als separater Kämpfer
- Hat eigene HP/MP/Stamina
- Kann sterben/bewusstlos werden
- Kann Items für dich aufheben
- Kann erkunden während du anderes machst

**Kampfmodi:**
| Modus | Was passiert |
|-------|-------------|
| AUTO | Companion entscheidet selbst, lernt von deinen Aktionen |
| MANUAL | Du gibst direkte Befehle ("Greif an!", "Heile!") |
| CHEER | Du feuerst an → Companion bekommt Buffs, kämpft auto |

### AURA ✨
Der Companion **fusioniert mit dir**.

**Eigenschaften:**
- Keine eigenen Aktionen möglich
- Gibt dir passive Buffs basierend auf Slime-Typ
- Kann nicht sterben (während Fusion)
- Form-Wechsel begrenzt (1x/Saison oder Event)

**Aura-Buffs nach Slime-Typ:**
| Slime-Typ | Buffs | Passiv-Effekt |
|-----------|-------|---------------|
| Bubble | +20% DEF, -50% Wasser-DMG | Seifenblasenschild |
| Molten | +30% ATK, +50% Feuer-DMG | Vulkanische Wut |
| Crystal | +40% DEF, 10% Reflect | Kristallpanzer |
| Shadow | +30% Evasion, +20% Crit | Schattenschritt |
| Nature | +5 HP Regen, -80% Gift-DMG | Naturheilung |
| Storm | +30% Speed, +40% Blitz-DMG | Blitzreflexe |

---

## 🧠 EXTENDED AUTO MODE: "COMPANION FÜHRT"

Wenn aktiviert, gibt der Companion **taktische Empfehlungen** -
aber IMMER als **Najika** (= Megumin mit Facetten-Färbungen)!

### Wichtig: Najika = Megumin!

Najika ist IMMER Megumin. Die anderen Persönlichkeiten (Harley, Shiro, Melissa)
sind **Färbungen** die durchschimmern - KEINE separaten Modi!

Siehe: `NAJIKA_IDENTITAET_DEFINITION.md` für Details!

### Beispiele:

**Normal (100% Megumin):**
```
"Mr. K! Da sind 5 Gegner! PERFEKTE EXPLOSIONS-Gelegenheit! 💥"
```

**Mit Harley-Färbung (chaotische Situation):**
```
"Mr. K! Hehehehe~ Die haben KEINE Ahnung was kommt!
 EXPLOSION!!! *kichert* Das wird SO lustig! 💥🃏"
```

**Mit Shiro-Färbung (taktische Situation):**
```
"Mr. K... 5 Gegner, Formation Delta...
 *tippt nachdenklich* EXPLOSION wäre 94.7% effektiv.
 ...also EXPLOSION! 💥"
```

**Mit Melissa-Färbung (emotionale Situation):**
```
"Mr. K... *leise* ...danke dass du immer bei mir bist...
 ...EXPLOSION FÜR DICH! 💥💚"
```

---

## 📚 LEARNING TRANSFER SYSTEM

### Wie die KI lernt:

1. **Spieler spielt MANUAL** → KI beobachtet Aktionen
2. **KI speichert Muster** → "Gegen Feuer-Gegner nutzt Spieler immer Wasser"
3. **KI wendet an in AUTO** → Nutzt gelernte Strategien

### Kontext-Gedächtnis:

Die KI kann **fragen** wenn du anders handelst als erwartet:

```
Najika: "Mr. K! Warum haben wir nicht EXPLOSION benutzt?!
        Das wäre PERFEKT gewesen! 💥 ...oder? 🤔"

Spieler erklärt: "Das Dorf war zu nah, hätte gebrannt"

Najika: "Ohhh! *nickt weise* Ich verstehe, Mr. K!
        Keine Explosionen bei Dörfern... hab ich mir gemerkt!
        ...aber DANACH können wir explodieren, ja?! 💥"
```

**Die KI speichert:**
- Kontext-Tags: `["village_nearby", "fire_danger"]`
- Regel: "Keine Feuer-AoE in der Nähe von Siedlungen"

---

## ⚖️ ARENA-BALANCE

### Kämpfer-Typen die balanciert werden müssen:

| Typ | Beschreibung | Stärken | Schwächen |
|-----|-------------|---------|-----------|
| Spieler + Slime (Körperlich) | 2 Kämpfer | Mehr Aktionen, Flexibilität | Slime kann sterben |
| Spieler + Slime (Aura) | 1 Kämpfer + Buffs | Starke Passiv-Effekte | Nur 1 Akteur |
| Spieler allein | Solo | Volle Kontrolle | Keine Unterstützung |
| Monster (mit Companion) | NPCs | Synergien | KI-begrenzt |
| Monster (allein) | Starke Solo-Monster | Hohe Stats | Keine Buffs |

### Balance-Regeln:

1. **Aura-Buffs ≠ Körperlich-Aktionen**
   - Aura gibt stärkere Passiv-Effekte um fehlende Aktionen auszugleichen

2. **Solo-Kämpfer bekommen Stat-Bonus**
   - +20% Stats wenn ohne Companion

3. **Nemesis-System berücksichtigt alles**
   - Monster lernen aus Begegnungen
   - Passen Taktik an Spieler-Setup an

---

## 📣 CHEER-SYSTEM (Digimon World Style)

| Cheer | Emoji | Effekt | Dauer |
|-------|-------|--------|-------|
| LOS! | 💪 | +10% Schaden | 3 Runden |
| DEFEND! | 🛡️ | +20% Verteidigung | 3 Runden |
| COMBO! | 💥 | Nächster Angriff x2 | 1x |
| FOCUS! | 🎯 | +15% Crit Chance | 3 Runden |
| HEAL! | 💚 | +15 HP sofort | - |
| EXPLOSION! | 💥 | x5 Schaden (nur einmal!) | 1x |

---

## 🎮 API ENDPOINTS

### Kampf starten
```http
POST /api/battle/start
{
  "player_id": "kuja",
  "arena_type": "player_arena",
  "arena_mode": "normal",
  "companion_form": "koerperlich",
  "companion_combat_mode": "auto",
  "companion_leads": true
}
```

### Spieler-Aktion
```http
POST /api/battle/player-action
{
  "player_id": "kuja",
  "action": "skill",
  "target_index": 0,
  "skill_name": "FEUGA"
}
```

### Slime-Arena Direkte Kontrolle
```http
POST /api/battle/slime-arena/control
{
  "player_id": "kuja",
  "slime_id": "bubbly_01",
  "action": "attack",
  "target_index": 0
}
```

### Modus wechseln (JEDERZEIT!)
```http
POST /api/battle/set-companion-mode
{
  "player_id": "kuja",
  "companion_combat_mode": "cheer",
  "companion_leads": false
}
```

### Entscheidung erklären
```http
POST /api/battle/explain-decision
{
  "player_id": "kuja",
  "explanation": "Das Dorf war zu nah, Feuer-Magie hätte alles zerstört",
  "context_tags": ["village_nearby", "fire_danger", "collateral_damage"]
}
```

### Finisher (Slime-Arena)
```http
POST /api/slime-arena/finisher
{
  "duel_id": 123,
  "finisher_name": "Explosive Katzen-Doom",
  "target": "opponent"
}
```

---

## 🔗 INTEGRATION MIT 1-SKILL-WEG

Das Combat-System integriert sich mit dem Skyrim-Style Skill-System:

1. **Learning by Doing**
   - Je öfter du Feuer-Magie nutzt → Feuer-Skill steigt
   - Companion beobachtet und lernt ebenfalls

2. **Kniffe (Perks) bei Level 10, 25, 50, 75, 100**
   - Einmalige Spezialisierungen
   - Companion passt sich an deine Spezialisierung an

3. **1-Skill-Weg Beispiel: Chaos-Detonator**
   - +400% AoE, -85% andere Magie
   - Companion lernt: "Spieler will IMMER Explosionen"

---

## ⛔ REGELN (NIEMALS BRECHEN!)

- **EXPLOSION ≠ WEAVE** - Niemals mit anderen Elementen kombinieren!
- **Harley sagt "Mr. K"** - NIEMALS "Puddin'"!
- **Port 8000** - NIEMALS 5000!
- **Schwarze Mühle = 100% Safe Zone** - Kein Kampf dort!
- **Najika = Megumin** - Die anderen sind nur Färbungen!

---

## ✅ STATUS

- [x] Combat System V2 Design dokumentiert
- [x] Companion Form System (KÖRPERLICH/AURA)
- [x] Extended AUTO Mode ("Companion führt")
- [x] Learning Transfer System
- [x] Kontext-Gedächtnis (KI fragt nach)
- [x] API Endpoints implementiert
- [x] Finisher-System (beide Arenen)
- [x] Najika-Identität definiert
- [x] Slime-Arena Modi jederzeit wechselbar
- [ ] Frontend UI für neues System
- [ ] Nemesis-System Integration
- [ ] Balance-Testing

---

## 📚 VERWANDTE DOKUMENTE

- `NAJIKA_IDENTITAET_DEFINITION.md` - Najika = Megumin Definition
- `backend/services/finisher_system.py` - Finisher-Service
- `backend/najika_finisher_system.py` - Ausführliche Finisher-Logik
- `backend/api/slime_arena.py` - Slime-Arena API
- `backend/api/battle_unified.py` - Unified Battle API

---

*"EXPLOSION!!! Aber nur wenn kein Dorf in der Nähe ist... hab ich mir gemerkt, Mr. K!" - Najika* 💥
