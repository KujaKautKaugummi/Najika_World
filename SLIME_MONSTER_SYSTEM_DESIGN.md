# NAJIKA WORLD - SLIME/MONSTER COMPANION SYSTEM
## Design-Dokument basierend auf: Dragon Quest Monsters + Digimon V-Pet + Fortnite Begleiter

**Erstellt:** 2026-01-28
**Grundsatz:** FREIHEIT! Monster-Kaempfe OPTIONAL, nicht zwingend!

---

# KERN-PHILOSOPHIE

## Skyrim-Prinzip (HEILIG!)
- **Keine Klassen** - Jeder kann alles sein (Bauer, Haendler, Bandit, Krieger, Magier, Mix)
- **Learning by Doing** - Skills verbessern sich durch Nutzung
- **Monster = OPTIONAL** - Man KANN Monster sammeln, MUSS aber nicht
- Monster-Kampf ist EIN Spielstil von VIELEN

## Balance: Freiheit vs. Monster-System
```
ERLAUBT:
- Spieler ignoriert Monster komplett → Trotzdem volles Spiel
- Spieler fokussiert NUR auf Monster → Trotzdem volles Spiel
- Spieler mischt beides → Optimales Erlebnis

VERBOTEN:
- "Du MUSST Monster haben fuer X"
- "Ohne Monster kein Endgame"
- Monster-Gates die Progression blockieren
```

---

# SLIME COMPANION SYSTEM

## Basis: Digimon V-Pet Mechanik

### Evolution-Stufen (6 Stufen)
| Stufe | Name | Zeit | Beispiel |
|-------|------|------|----------|
| 1 | Schleim-Ei | Start | Farbiges Ei |
| 2 | Baby-Schleim | 1h | Winziger Blob |
| 3 | Kind-Schleim | 24h | Kleiner Schleim |
| 4 | Reifer Schleim | 3 Tage | Normal-Groesse |
| 5 | Champion-Schleim | 7 Tage | Spezial-Form |
| 6 | Ultimativ | 14 Tage | Legendaere Form |

### Evolution-Bedingungen (Digimon-Style)
```python
EVOLUTION_CONDITIONS = {
    "care_mistakes": {
        # Wie oft Hunger/Thirst auf 0 gefallen
        "good_path": 0-2,    # Beste Evolution
        "normal_path": 3-5,  # Normale Evolution
        "bad_path": 6+       # Schlechte/Sonder-Evolution
    },
    "training": {
        # Wie oft trainiert (egal ob erfolgreich)
        "effort_heart": "Alle 4 Trainings = 1 Effort Heart",
        "requirement": "X Effort Hearts fuer bestimmte Evolution"
    },
    "battles": {
        # NUR wenn Spieler kaempft (OPTIONAL!)
        "count": "Anzahl Kaempfe (Win oder Loss)",
        "win_rate": "80%+ fuer beste Evolutionen"
    },
    "region_bonus": {
        # Wo der Schleim aufgewachsen ist
        "samtmoos": "Natur-Typen",
        "magmastroeme": "Feuer-Typen",
        "reich_der_drei": "Eis/Nekro-Typen",
        "salzwind": "Wasser-Typen"
    }
}
```

### Pflege-System (V-Pet Style)
- **Hunger-Herzen**: Fuettern bevor leer (10 Min Toleranz)
- **Kraft-Herzen**: Training/Spielen
- **Schlaf**: Licht aus wenn muede (20 Min Toleranz)
- **Care Mistake**: Wenn Ruf-Licht ausgeht ohne Reaktion

### Tod-Bedingungen
- 20 Verletzungen angesammelt
- 6 Stunden verletzt ohne Heilung
- 12 Stunden ohne Essen
- **ABER**: Najika warnt vorher MEHRFACH!

---

# DRAGON QUEST MONSTERS: SYNTHESE/FUSION

## Basis-Mechanik
- 2 Monster Level 10+ → 1 neues Monster
- **Originale sind WEG** (wichtige Entscheidung!)
- Neues Monster startet Level 1
- Erbt 3 Talente von Eltern

## Plus-Wert System (+N)
```
Synthese-Ergebnis Plus-Wert:
  +9 Monster + +5 Monster = +10 Monster
  (Hoechster Eltern-Wert + 1)

Plus-Wert bedeutet:
  - Hoeheres Stat-Potential
  - Bessere Wachstumsrate
  - Zeigt "Generationen" an
```

## Synthese-Typen

### 1. Gleiche Monster
```
Schleim A + Schleim A = Schleim (mit +1)
Garantiert gleiches Monster, aber staerker
```

### 2. Familien-Kombination
```
Feuer-Typ + Beliebig = Feuer-Hybrid moeglich
Wasser-Typ + Beliebig = Wasser-Hybrid moeglich
```

### 3. Spezial-Synthese (4-Eltern)
```
Grosseltern muessen spezifisch sein:
  [A + B] = Elter1    [C + D] = Elter2
           \              /
            [Elter1 + Elter2] = LEGENDAER

Gold-Rahmen zeigt Spezial-Synthese an
```

## Skill-Vererbung
- Kind erbt Skills von BEIDEN Eltern
- Plus eigene angeborene Skills
- Skill-Punkte investieren fuer Traits

---

# NAJIKA WORLD IMPLEMENTATION

## Slime-Typen (basierend auf 9 Regionen)

| Region | Slime-Typ | Farbe | Spezial |
|--------|-----------|-------|---------|
| Samtmoos-Tiefwald | Moos-Schleim | Gruen | Heilung, Gift-Immun |
| Reich der Drei | Frost-Schleim | Weiss/Blau | Eis-Magie, Untot-Freund |
| Salzwind-Kueste | Wasser-Schleim | Blau | Schwimmen, Fisch-Locken |
| Blitzebene | Blitz-Schleim | Lila | Elektro-Schock, Schnell |
| Gruenschlamm-Sumpf | Gift-Schleim | Schwarz | Gift-Angriff, Unsichtbar |
| Magmastroeme | Magma-Schleim | Rot/Orange | Feuer-Immun, Schmieden-Hilfe |
| Heisse Duenen | Sand-Schleim | Gold | Graben, Schatz-Finder |
| Goetterfels | Goetter-Schleim | Regenbogen | Alle Elemente (SELTEN!) |
| Tiefenhoehlen | Kristall-Schleim | Transparent | Licht-Quelle, Erz-Finder |

## Nicht-Kampf Nutzen (WICHTIG!)

### Fuer Nicht-Kaempfer
```
Slime kann helfen bei:
- Farming: Bewaessern, Schaedlinge fressen
- Crafting: Materialien finden
- Trading: Waren tragen
- Exploration: Verstecktes finden
- Social: Einfach niedlich sein!
```

### Passive Boni (ohne Kampf)
```python
PASSIVE_BONUSES = {
    "moos_schleim": {
        "farming_speed": +20%,
        "herb_quality": +10%
    },
    "wasser_schleim": {
        "fishing_luck": +30%,
        "swimming_speed": +15%
    },
    "sand_schleim": {
        "treasure_find": +25%,
        "trade_discount": +5%
    },
    "kristall_schleim": {
        "mining_speed": +20%,
        "light_radius": +50%
    }
}
```

## Kampf-System (OPTIONAL!)

### Nur wenn Spieler WILL
```
Aktivierung:
- Spieler muss bewusst "Monster-Kampf" waehlen
- Normaler Kampf = Spieler kaempft selbst
- Monster-Kampf = Slime kaempft (Pokemon/DQM Style)

NIEMALS:
- Automatischer Monster-Kampf
- "Dein Slime muss kaempfen"
- Zwangs-Battles
```

### Kampf-Mechanik (wenn aktiviert)
```
Turn-Based oder Real-Time (Spieler-Wahl):
1. Slime hat 4 Skills
2. Typ-Effektivitaet (Feuer > Pflanze > Wasser > Feuer)
3. Synthese-Plus beeinflusst Stats
4. Win-Rate beeinflusst naechste Evolution
```

---

# FORTNITE BEGLEITER INSPIRATION

## Was wir uebernehmen:
- Begleiter folgt Spieler
- Kann Gegner angreifen (wenn Spieler will)
- Kann Items aufheben
- Hat eigene Persoenlichkeit/Animationen

## Was wir NICHT uebernehmen:
- Kein Zwang zum Begleiter
- Keine Pay2Win Monster
- Keine "Meta" Monster die man BRAUCHT

---

# SYNTHESE-REZEPTE (Beispiele)

## Basis-Synthesen
```
Moos-Schleim + Wasser-Schleim = Sumpf-Schleim
Frost-Schleim + Magma-Schleim = Dampf-Schleim
Blitz-Schleim + Sand-Schleim = Glas-Schleim
Gift-Schleim + Kristall-Schleim = Toxin-Kristall
```

## Legendaere 4-Eltern-Synthesen
```
[Frost + Magma] = Dampf    [Blitz + Wasser] = Sturm
         \                        /
          [Dampf + Sturm] = WETTER-GOTT-SCHLEIM

[Moos + Gift] = Pilz    [Kristall + Sand] = Juwel
        \                      /
         [Pilz + Juwel] = NATUR-GEIST-SCHLEIM
```

## Goetter-Schleim (Geheim)
```
Voraussetzung: Alle 9 Basis-Typen gesammelt
Dann: Spezial-Quest in Goetterfels
Ergebnis: Goetter-Schleim (Regenbogen, alle Elemente)
```

---

# TECHNISCHE IMPLEMENTATION

## Neue Backend-Dateien benoetigt:
```
backend/
├── najika_slime_system.py      # Haupt-Slime-Logik
├── najika_slime_evolution.py   # Evolution-Bedingungen
├── najika_slime_synthesis.py   # Fusion/Synthese
├── najika_slime_care.py        # Pflege (V-Pet Style)
└── api/
    └── slime_companion.py      # API Endpoints
```

## Datenbank-Schema
```python
SLIME_STATE = {
    "id": "uuid",
    "name": "Spieler-gewaehlter Name",
    "type": "moos_schleim",
    "stage": 3,  # 1-6
    "level": 15,
    "plus_value": 2,  # Synthese-Generationen

    # V-Pet Stats
    "hunger_hearts": 4,  # Max 4
    "strength_hearts": 4,
    "care_mistakes": 1,
    "effort_hearts": 8,
    "battles": 12,
    "win_rate": 0.75,

    # Evolution Timer
    "birth_time": timestamp,
    "evolution_time": timestamp,  # Wann naechste Evolution moeglich

    # Vererbte Skills
    "skills": ["heal", "poison_spit", "camouflage"],
    "inherited_from": ["parent1_id", "parent2_id"],

    # Passive Boni
    "passive_bonus": {
        "farming_speed": 0.2,
        "herb_quality": 0.1
    }
}
```

## API Endpoints
```
GET  /api/slime/status          # Aktueller Slime-Status
POST /api/slime/feed            # Fuettern
POST /api/slime/train           # Trainieren
POST /api/slime/play            # Spielen
POST /api/slime/sleep           # Schlafen legen
GET  /api/slime/evolution-check # Pruefe ob Evolution moeglich
POST /api/slime/evolve          # Evolution durchfuehren
POST /api/slime/synthesize      # Zwei Slimes fusionieren
GET  /api/slime/recipes         # Synthese-Rezepte anzeigen
```

---

# BALANCE-REGELN

## Monster-Spieler vs. Nicht-Monster-Spieler
```
GLEICH STARK:
- Krieger ohne Slime = Krieger mit Slime (im Spieler-Kampf)
- Slime gibt Boni, aber nicht OP

UNTERSCHIEDLICH:
- Monster-Kaempfe = Slime-Stats entscheidend
- Spieler-Kaempfe = Spieler-Stats entscheidend

BEIDE WEGE FUEHREN ZUM ZIEL:
- Endgame-Bosse: Solo ODER mit Monster
- Keine "Monster-Only" Barrieren
```

## Anti-Grind Massnahmen
```
- Evolution basiert auf ZEIT + PFLEGE, nicht Grind
- Synthese braucht Level 10, nicht Level 99
- Legendaere Slimes = Dedication, nicht No-Life
- Care > Battles fuer beste Evolutionen
```

---

# ZUSAMMENFASSUNG

## Was wir von jedem System nehmen:

### Dragon Quest Monsters:
- Synthese/Fusion (2 Monster → 1 neues)
- Plus-Wert System (+N Generationen)
- Skill-Vererbung
- 4-Eltern Spezial-Synthesen

### Digimon V-Pet:
- 6 Evolution-Stufen
- Care Mistakes beeinflussen Evolution
- Hunger/Kraft-Herzen
- Zeit-basierte Evolution
- Effort Hearts durch Training

### Fortnite Begleiter:
- Folgt Spieler
- Kann helfen im Kampf
- Items aufheben
- Niedliche Animationen

### Skyrim (HEILIG!):
- ALLES OPTIONAL
- Keine Zwangs-Mechaniken
- Freiheit uber alles

---

*"Dein Schleim, deine Regeln. Oder kein Schleim - auch okay!"*
