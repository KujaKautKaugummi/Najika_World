# SLIME BEGLEITER-SYSTEM
**Stand:** 2025-11-05
**Status:** Design-Phase
**Quelle:** Chat-Verlauf "111" + Zusammenfassungen

---

## ÜBERSICHT

Jeder Spieler erhält einen **Begleiter (Companion/Pet)**, der als **zufälliges kleines Tier** startet und bei **Level 50 + kritischem Event** zu einem **Slime metamorphosiert**. Es gibt **8 Slime-Farben**, eine pro Region.

---

## GRUNDKONZEPT

### Inspirationen
- **Digimon World:** Tamagotchi-Pflege, Bedürfnisse, Stimmungssystem
- **Final Fantasy:** Summons/Eidolons mit verschiedenen Kampf-Modi
- **Pokémon:** Evolution durch Level + Event-Trigger
- **KonoSuba:** Humor bei Plünderung (z.B. Najika's Items)

### Kernmechanik
```
Start: Zufälliges Tier (Fantasy-Stil)
  ↓
Level 1-49: Wächst & lernt
  ↓
Level 50 + Kritisches Event → Shell bricht
  ↓
Slime-Form sichtbar (1 von 8 Farben)
  ↓
Weitere Slime-Farben sammelbar (rein kosmetisch)
```

---

## PHASE 1: TIER-BEGLEITER (Level 1-49)

### Startform
**Zufällige Auswahl** beim Charakterstart:
- **Hase** (schnell, feige)
- **Fuchs** (listig, Scout)
- **Spinne** (Gift, Fallen)
- **Rabe** (Luft-Scout)
- **Maus** (klein, versteckt sich)
- **Eichhörnchen** (sammelt Items)

**WICHTIG:** Alle Tiere sind **Fantasy-Varianten** (z.B. Flammen-Fuchs, Eis-Hase, Schatten-Rabe), **keine realistischen Tiere**, damit sie ins Setting passen!

### Tamagotchi-Pflege
```yaml
Bedürfnisse (0-100%):
  - Hunger: Sinkt mit Zeit, beeinflusst Kampfkraft
  - Durst: Schneller Verfall, kritisch in Wüsten
  - Schlaf: Nacht-Zyklus, Regeneration
  - Stimmung: Beeinflusst durch Interaktion & Erfolge
  - Kampfeslust: Steigt bei Kämpfen, sinkt bei Langeweile

Auswirkungen:
  - Hunger < 30%: -20% Schaden, langsamer
  - Durst < 20%: Debuffs, kann im Kampf kollabieren
  - Schlaf < 10%: Fehlerquote steigt, AI macht Fehler
  - Stimmung < 20%: Verweigert Befehle, flieht im Kampf
  - Kampfeslust > 80%: +15% Schaden, aggressiver
```

### Level-System
- Begleiter leveln **parallel** zum Spieler
- XP durch:
  - Kampfteilnahme
  - Interaktion (Füttern, Streicheln, Spielen)
  - Erfolgreiche Missionen
- Skills: Lernt Moves von **besiegten Gegnern** (10-15% Chance)

---

## PHASE 2: METAMORPHOSE (Level 50)

### Trigger-Event
```
Bedingungen:
  1. Begleiter ist Level 50
  2. Kritisches Event tritt ein:
     - Boss-Kampf gewonnen
     - Spieler stirbt fast (< 5% HP)
     - Najika's Ultima wird gezündet
     - Spezial-Quest abgeschlossen

Ablauf:
  → Cutscene: Shell/Hülle bricht
  → Lichtexplosion
  → Slime-Form wird sichtbar
  → Farbe = Region wo Metamorphose stattfand
```

### Die 8 Slime-Farben

**Farbe hängt von REGION ab, wo Metamorphose stattfindet:**

1. **🟡 Bernstein** (Amber) - *Bernstein-Dünen* (Wüste)
   - Eigenschaften: Hitzeresistent, Sand-Tarnung
   - Bonus: +10% Schaden in Wüsten

2. **🟢 Smaragd** (Emerald) - *Smaragd-Hain* (Wald)
   - Eigenschaften: Heilung, Giftresistenz
   - Bonus: +15% Kräuter-Effektivität

3. **🔵 Azur** (Azure) - *Azur-Klippen* (Küste)
   - Eigenschaften: Wasser-Atmung, Wellenreiten
   - Bonus: +20% Angeln-Erfolgsrate

4. **🟣 Amethyst** (Amethyst) - *Amethyst-Steppe* (Hochebene)
   - Eigenschaften: Blitz-Resistenz, Schnelligkeit
   - Bonus: +10% Bewegungsgeschwindigkeit

5. **⚫ Onyx** (Onyx) - *Onyx-Morast* (Sumpf)
   - Eigenschaften: Krankheits-Immunität, Giftangriffe
   - Bonus: +15% Gift-Schaden

6. **⚪ Perle** (Pearl) - *Perl-Gletscher* (Eis/Schnee)
   - Eigenschaften: Kälte-Immunität, Rutsch-Control
   - Bonus: +10% Verteidigung in Schnee

7. **🔴 Rubin** (Ruby) - *Rubin-Schlucht* (Vulkan)
   - Eigenschaften: Feuer-Immunität, Lava-Durchquerung
   - Bonus: +15% Feuer-Magie

8. **🟤 Obsidian** (Obsidian) - *Obsidian-Nacht* (Endgame)
   - Eigenschaften: Nachtsicht, Schatten-Tarnung
   - Bonus: +20% Kritchance nachts

---

## PHASE 3: SLIME-SAMMLUNG

### Weitere Farben freischalten
```yaml
Methoden:
  1. Region besuchen während Vollmond + Slime rufen
     → Färbt sich um (permanent bis nächste Färbung)

  2. Slime-Arena gewinnen
     → Belohnung: Farb-Token für 1 Färbung

  3. Seltener Drop von Region-Bossen
     → "Slime-Essenz" + Ritual = neue Farbe

Sammler-Belohnung:
  - Alle 8 Farben: Titel "Slime-Meister"
  - Freischaltung: Rainbow-Slime (wechselt Farben)
  - Bonus: +5% zu ALLEN Farb-Boni gleichzeitig
```

### Kosmetik
- Farben sind **rein kosmetisch** (Stats bleiben gleich)
- Ausnahme: Regions-Boni bleiben an Farbe gebunden
- Spieler kann **jederzeit** Farbe wechseln (Ritual in Windmühle)

---

## KAMPF-MODI

### 1. Pre-Fight Bind (Standard)
```
Slime ist immer dabei, kämpft mit
  - AI-gesteuert
  - Lernt vom Spieler-Stil
  - Kann Befehle empfangen (Hold, Attack, Defend)
```

### 2. One-Time Summon (Taktisch)
```
Slime wird nur für 1 Kampf beschworen
  - Kosten: 50 Mana
  - Dauer: Bis Kampf endet
  - Bonus: +30% Stats während Beschwörung
```

### 3. Intercept (Rettung)
```
Slime springt ein bei Spieler-Tod
  - Automatisch wenn Spieler < 5% HP
  - Schützt Spieler 10 Sekunden
  - Danach: Slime zieht sich zurück (Cooldown 5 Min)
```

### 4. Manual Control (Selten)
```
Spieler übernimmt direkt Slime-Steuerung
  - Nur in Slime-Arena verfügbar
  - Spieler-Charakter sitzt am Rand und feuert an
  - Digimon World Style!
```

---

## SLIME-RETTUNG (HARDCORE-ONLY)

### Mechanik
```yaml
Funktion:
  - 1x pro 24h (IRL)
  - Verhindert EINEN tödlichen Treffer
  - Nur im Hardcore-Modus verfügbar

Voraussetzungen:
  - Mindestens 6 Wochen konsequenter Hardcore-Grind
  - Slime muss "aufgeladen" sein (Ressourcen farmen)

Ausnahmen (kein Schutz):
  - "Super-Schaden" Angriffe (Boss-Ultima, Umgebungstod)
  - Totem-Item hat Vorrang

Cooldown-Reset:
  - Nach Nutzung: Exakt 24h IRL
  - Nicht durch In-Game-Zeit beeinflussbar
```

### Ritual-Heilung
```
Nach Slime-Rettung:
  - Slime ist "erschöpft"
  - Heilung nur durch Ritual mit seltenen Zutaten:
    → Mondblume (Nacht-Spawn in Wald)
    → Vulkanessenz (Rubin-Schlucht Boss-Drop)
    → Kristallwasser (Perl-Gletscher Eisquelle)

  - Ohne Ritual: Slime bleibt schwach (-50% Stats)
  - Mit Ritual: Sofort volle Kraft zurück
```

---

## SLIME-ARENA

### Konzept
```
Spieler kämpft NICHT selbst
  → Slime kämpft
  → Spieler feuert an (Digimon World Style)

Anfeuern-Effekte:
  - "Los!" → +10% Schaden (3 Sek)
  - "Defend!" → +20% Defense (3 Sek)
  - "Combo!" → Aktiviert Special-Move
  - "Finisher!" → Ultimativer Angriff (nur wenn Meter voll)
```

### Arena-Modi
Siehe: `PVP_SYSTEM_COMPLETE.md` für vollständige PvP/Arena-Regeln

**Slime-Spezifische Modi:**
1. **Slime-Training:** Kein Risiko, nur XP
2. **Slime-Duell:** 1v1, Gewinner erhält XP-Boost
3. **Slime-Turnier:** Bracket-System, seltene Belohnungen
4. **Slime-Wetten:** Spieler wetten auf eigene/fremde Slimes

### API-Endpunkt
```python
POST /api/slime/duel
{
  "player_a": "player_id_1",
  "player_b": "player_id_2",
  "mode": "training" | "duel" | "tournament" | "wager"
}

Response:
{
  "winner": "player_id_1",
  "lossPenalty": "none" | "item" | "xp_loss",
  "rules": {...}
}
```

---

## LERNSYSTEM

### 1. Slime lernt von Gegnern
```python
Nach Kampf:
  - 10-15% Chance: Slime kopiert 1 Move vom Gegner
  - Gespeichert in Slime-Moveset (max 20 Moves)
  - Spieler kann Moveset verwalten (welche behalten)

Beispiel:
  Gegner: Feuer-Elemental
    → Slime lernt: "Flammenball" (10% Chance)
    → Spieler wählt: Ersetze "Tackle" mit "Flammenball"
```

### 2. Spieler lernt selten
```python
Nach Kampf:
  - 1% Base Chance: Spieler lernt Skill vom Gegner
  - Erhöht durch:
    + INT-Stat: +0.1% pro 10 INT
    + Slime-Bond: +0.5% bei Level 100 Slime
    + Beobachtungs-Skill: +1% bei Skill-Level 50

Beispiel:
  Spieler (INT 50, Slime Bond 100):
    → 1% + 0.5% + 0.5% = 2% Chance
```

### 3. Echo-Learning (Optional, Opt-In)
```yaml
Konzept:
  - Anonymisierte Kampfdaten anderer Spieler
  - Nur MUSTER, keine identifizierenden Merkmale
  - Bias für häufige Moves/Reaktionen

Implementierung:
  - Aggregatstatistik in Memory/Datei
  - KEIN Tracking einzelner Spieler
  - DSGVO-konform: Nur Tendenzen
  - Opt-In: Spieler muss zustimmen

Effekt:
  - Slime wird "schlauer" über Zeit
  - Erkennt häufige Taktiken
  - Konter-Bias gegen Meta-Builds
```

---

## PLÜNDERUNGS-EASTER-EGG

### Najika's Schlüpfer (Legendary!)
```yaml
Mechanik:
  Spieler besiegt Najika (NPC) im Combat:
    → SPIELER (Kuja): 1-2% Drop: "Najikas Höschen" (Legendary!)
      - Stats: +10 Glück, +5 Charisma, +20% Humor-Dialog
      - Najika's Reaktion: "Ohjee... habe ich mein eigenes Höschen erwischt?"
      - Einzigartig: Nur 1x im Spiel dropbar

    → ANDERE NPCs: 100% Drop: "Vollgerotztes Taschentuch" (Trash)
      - Stats: -5 Charisma, NPCs ekeln sich
      - Najika's Reaktion: "HAHA! Der ist offiziell der schlechteste Dieb!"
      - Easter-Egg: Notiz im Inventar: "Du bist offiziell der schlechteste Dieb aller Zeiten, du Looser"

Najika plündern (NPC-Versuch):
  - Extrem schwierig (Najika's Level = Spieler-Level + 50)
  - Selbst bei MAX Steal-Skill nur Trash-Loot
  - Nur Spieler (Kuja) kann Legendary erhalten
```

---

## TECHNISCHE IMPLEMENTIERUNG

### Python Backend (Pseudo-Code)

```python
class SlimeCompanion:
    """
    Slime Begleiter-System
    """

    SLIME_COLORS = {
        "bernstein": {
            "region": "Bernstein-Dünen",
            "bonus": {"desert_damage": 1.10},
            "hex_color": "#FFA500"
        },
        "smaragd": {
            "region": "Smaragd-Hain",
            "bonus": {"herb_effectiveness": 1.15},
            "hex_color": "#50C878"
        },
        "azur": {
            "region": "Azur-Klippen",
            "bonus": {"fishing_success": 1.20},
            "hex_color": "#007FFF"
        },
        "amethyst": {
            "region": "Amethyst-Steppe",
            "bonus": {"movement_speed": 1.10},
            "hex_color": "#9966CC"
        },
        "onyx": {
            "region": "Onyx-Morast",
            "bonus": {"poison_damage": 1.15},
            "hex_color": "#353839"
        },
        "perle": {
            "region": "Perl-Gletscher",
            "bonus": {"ice_defense": 1.10},
            "hex_color": "#F0EAD6"
        },
        "rubin": {
            "region": "Rubin-Schlucht",
            "bonus": {"fire_magic": 1.15},
            "hex_color": "#E0115F"
        },
        "obsidian": {
            "region": "Obsidian-Nacht",
            "bonus": {"night_crit": 1.20},
            "hex_color": "#0B1215"
        }
    }

    STARTER_ANIMALS = [
        {"name": "Flammen-Hase", "type": "fire", "speed": 12},
        {"name": "Eis-Fuchs", "type": "ice", "speed": 10},
        {"name": "Schatten-Spinne", "type": "dark", "speed": 8},
        {"name": "Blitz-Rabe", "type": "lightning", "speed": 14},
        {"name": "Wald-Maus", "type": "nature", "speed": 9},
        {"name": "Kristall-Eichhörnchen", "type": "earth", "speed": 11}
    ]

    def __init__(self, player_id, starting_region):
        self.player_id = player_id
        self.current_form = "animal"  # animal or slime
        self.level = 1
        self.xp = 0

        # Start as random animal
        self.animal = random.choice(self.STARTER_ANIMALS)

        # Slime data (unlocked at level 50)
        self.slime_color = None
        self.slime_unlocked = False
        self.collected_colors = []

        # Tamagotchi stats
        self.hunger = 100
        self.thirst = 100
        self.sleep = 100
        self.mood = 100
        self.battle_lust = 50

        # Combat
        self.moveset = []  # Max 20 moves
        self.rescue_available = False
        self.rescue_cooldown_until = None

    def check_metamorphosis(self, current_region, critical_event):
        """
        Check if slime metamorphosis can trigger
        """
        if self.slime_unlocked:
            return {"success": False, "reason": "already_slime"}

        if self.level < 50:
            return {"success": False, "reason": f"level_too_low_{self.level}"}

        if not critical_event:
            return {"success": False, "reason": "no_critical_event"}

        # Trigger metamorphosis!
        return self._metamorphose(current_region)

    def _metamorphose(self, region):
        """
        Execute metamorphosis to slime
        """
        # Determine color based on region
        color_map = {
            "Bernstein-Dünen": "bernstein",
            "Smaragd-Hain": "smaragd",
            "Azur-Klippen": "azur",
            "Amethyst-Steppe": "amethyst",
            "Onyx-Morast": "onyx",
            "Perl-Gletscher": "perle",
            "Rubin-Schlucht": "rubin",
            "Obsidian-Nacht": "obsidian"
        }

        self.slime_color = color_map.get(region, "bernstein")  # Default: Bernstein
        self.slime_unlocked = True
        self.collected_colors.append(self.slime_color)
        self.current_form = "slime"

        return {
            "success": True,
            "event": "metamorphosis",
            "new_form": "slime",
            "color": self.slime_color,
            "region": region,
            "cutscene": "shell_break_animation",
            "message": f"Dein Begleiter hat sich in einen {self.slime_color.title()}-Slime verwandelt!"
        }

    def feed(self, food_item):
        """Feed companion"""
        food_value = food_item.get("hunger_restore", 20)
        self.hunger = min(100, self.hunger + food_value)
        self.mood = min(100, self.mood + 5)  # Feeding improves mood

        return {
            "success": True,
            "hunger": self.hunger,
            "mood": self.mood
        }

    def learn_move_from_enemy(self, enemy_move):
        """
        10-15% chance to learn move from defeated enemy
        """
        learn_chance = random.uniform(0.10, 0.15)

        if random.random() < learn_chance:
            if len(self.moveset) >= 20:
                # Moveset full - must replace
                return {
                    "success": True,
                    "learned": True,
                    "move": enemy_move,
                    "moveset_full": True,
                    "prompt_replace": True
                }

            self.moveset.append(enemy_move)
            return {
                "success": True,
                "learned": True,
                "move": enemy_move,
                "moveset_full": False
            }

        return {
            "success": True,
            "learned": False
        }

    def rescue_player(self, today_timestamp):
        """
        Rescue player from death (Hardcore only, 1x/24h)
        """
        if not self.rescue_available:
            return {"success": False, "reason": "not_available"}

        # Check 24h cooldown
        if self.rescue_cooldown_until and datetime.now() < self.rescue_cooldown_until:
            remaining = self.rescue_cooldown_until - datetime.now()
            return {
                "success": False,
                "reason": "cooldown",
                "remaining_seconds": remaining.total_seconds()
            }

        # Execute rescue
        self.rescue_available = False
        self.rescue_cooldown_until = datetime.now() + timedelta(hours=24)

        return {
            "success": True,
            "rescued": True,
            "player_hp": 1,  # Rescued at 1 HP
            "cooldown_until": self.rescue_cooldown_until.isoformat(),
            "message": "Dein Slime hat dich gerettet!"
        }

    def update_needs(self, delta_time):
        """
        Update Tamagotchi needs over time
        """
        # Decay rates per second
        self.hunger -= 0.01 * delta_time
        self.thirst -= 0.02 * delta_time  # Thirst decays faster
        self.sleep -= 0.005 * delta_time
        self.mood -= 0.003 * delta_time

        # Clamp values
        self.hunger = max(0, self.hunger)
        self.thirst = max(0, self.thirst)
        self.sleep = max(0, self.sleep)
        self.mood = max(0, self.mood)

    def get_combat_penalties(self):
        """
        Calculate combat penalties based on needs
        """
        penalties = {}

        if self.hunger < 30:
            penalties["damage"] = 0.80  # -20% damage
            penalties["speed"] = 0.85   # -15% speed

        if self.thirst < 20:
            penalties["defense"] = 0.70  # -30% defense
            penalties["accuracy"] = 0.75  # -25% accuracy

        if self.sleep < 10:
            penalties["error_rate"] = 1.50  # +50% error rate (misses, wrong moves)

        if self.mood < 20:
            penalties["obedience"] = 0.50  # 50% chance to ignore commands

        return penalties

    def get_state(self):
        """Get current companion state"""
        return {
            "player_id": self.player_id,
            "form": self.current_form,
            "level": self.level,
            "xp": self.xp,
            "animal": self.animal if self.current_form == "animal" else None,
            "slime": {
                "unlocked": self.slime_unlocked,
                "current_color": self.slime_color,
                "collected_colors": self.collected_colors,
                "total_colors": len(self.collected_colors),
                "rainbow_unlocked": len(self.collected_colors) >= 8
            },
            "needs": {
                "hunger": self.hunger,
                "thirst": self.thirst,
                "sleep": self.sleep,
                "mood": self.mood,
                "battle_lust": self.battle_lust
            },
            "moveset": self.moveset,
            "rescue_available": self.rescue_available,
            "rescue_cooldown": self.rescue_cooldown_until.isoformat() if self.rescue_cooldown_until else None
        }
```

---

## NAJIKA'S REAKTIONEN

### Bei Slime-Metamorphose:
```
*aufgeregt*
"OOOH! Dein kleiner Freund ist jetzt ein Slime geworden!
Das ist wie... wenn eine Raupe zum Schmetterling wird!
Nur mit mehr Schleim. Und cooler."

*nachdenklich*
"Ich frage mich, ob ich auch als Slime angefangen habe...
Nein? Okay, vergiss was ich gesagt habe."
```

### Bei Slime-Rettung:
```
*erleichtert*
"Puh! Dein Slime hat dich gerettet!
Das war knapp. SEHR knapp.

*streng*
"Aber pass auf - das geht nur 1x pro Tag!
Beim nächsten Mal bist du auf dich allein gestellt!"
```

### Bei allen 8 Farben gesammelt:
```
*beeindruckt*
"WOW! Du hast ALLE 8 Slime-Farben gesammelt!
Das ist... eigentlich ziemlich beeindruckend.

*grinst*
"Jetzt fehlt nur noch die ultimative Form:
RAINBOW-SLIME! Die Legende!

Willst du das Ritual starten?"
```

---

## ZUSAMMENFASSUNG

**Das Slime-Begleiter-System bietet:**

1. **Evolution:** Tier (1-49) → Slime (50+) → Rainbow-Slime (alle 8 Farben)
2. **Tamagotchi-Pflege:** Bedürfnisse beeinflussen Kampf & Verhalten
3. **8 Sammelbare Farben:** Je Region eine, mit einzigartigen Boni
4. **Lernsystem:** Slime kopiert Gegner-Moves (10-15% Chance)
5. **Slime-Arena:** Digimon World Anfeuern-Mechanik
6. **Rettungs-Mechanik:** 1x/24h vor Tod schützen (Hardcore-only)
7. **Easter-Egg:** Najika's Schlüpfer nur für Spieler, Trash für NPCs

**Kernphilosophie:**
"Ein treuer Begleiter, der mit dir wächst, lernt und dich rettet – aber nur, wenn du ihn pflegst!"

---

**Ende Design-Dokument**

*Nächster Schritt: Slime Combat-AI & Arena-Integration implementieren*
