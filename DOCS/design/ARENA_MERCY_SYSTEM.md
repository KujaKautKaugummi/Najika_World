# ARENA GNADENBITT-SYSTEM (MERCY SURRENDER)
**Stand:** 2025-11-05
**Status:** Design-Phase

---

## ÜBERSICHT

In der Arena können Spieler, die kurz vor dem Tod stehen, um **Gnade bitten** und sich dem Gegner ergeben. Je nach Arena-Modus fallen unterschiedliche Strafen an.

---

## GRUNDMECHANIK

### Auslöser
- Spieler-HP unter **15%**
- **Mercy-Button** erscheint (nur 1x pro Kampf!)
- **5 Sekunden Zeitfenster** um zu entscheiden

### Ablauf
```
1. Verlierer drückt "Mercy"-Button
   → Animation: Kniet nieder, Hände hoch
   → Sound: "Ich ergebe mich!"

2. Gewinner erhält Prompt:
   ┌─────────────────────────────────┐
   │  [Gegner bittet um Gnade]       │
   │                                  │
   │  [✓ Gnade gewähren]             │
   │  [✗ Keine Gnade (töten)]        │
   │                                  │
   │  Belohnung: [Je nach Modus]     │
   └─────────────────────────────────┘

3a. Gnade gewährt:
    → Verlierer verliert Items (je nach Modus)
    → Verlierer wird zur Arena-Tür teleportiert
    → Gewinner erhält Beute + Ehre-Bonus

3b. Keine Gnade:
    → Kampf geht weiter
    → Verlierer stirbt (normale Tod-Mechanik)
    → Gewinner erhält nur Standard-Belohnung
```

---

## ARENA-MODI & STRAFEN

### 1. **FREUNDSCHAFTS-ARENA** (Training Mode)
**Einsatz:** Keine Items, nur Training
**Mercy-Strafe:**
- Keine Item-Verluste
- Verlierer verliert 10% Durability an aller Ausrüstung
- Gewinner erhält Ehre-Punkte

**Zweck:** Üben ohne Risiko

---

### 2. **WAGER-ARENA** (Item Bet)
**Einsatz:** Beide Spieler setzen 1 Item ein (vor Kampf)
**Mercy-Strafe:**
- Verlierer verliert sein eingesetztes Item
- Gewinner erhält beide Items

**Zweck:** Niedrig-Risiko Wetten

---

### 3. **GEAR-ARENA** (Equipment Battle)
**Einsatz:** Keine Vorbedingung
**Mercy-Strafe:**
- Verlierer verliert **1 zufälliges** angelegtes Ausrüstungsteil
- Gewinner erhält das Teil + Ehre-Bonus

**Zweck:** Mittleres Risiko, beliebt für Gear-Farming

---

### 4. **PLÜNDERUNGS-ARENA** (High Stakes)
**Einsatz:** Keine Vorbedingung
**Mercy-Strafe:**
- Verlierer verliert **ALLES** im Inventar (außer Unterwäsche + Waffe Slot 1)
- Gewinner erhält ALLE Items + großer Ehre-Bonus
- Verlierer läuft in Unterwäsche zur Arena-Tür (Walk of Shame)

**Zweck:** Höchstes Risiko, höchste Belohnung

---

### 5. **HARDCORE-ARENA** (Permadeath Risk)
**Einsatz:** Nur Hardcore-Mode Spieler
**Mercy-Strafe:**
- Verlierer verliert **ALLES** (wie Plünderungs-Arena)
- **ZUSÄTZLICH:** Verlierer verliert 1 Level in allen Skills (-10% XP)
- Gewinner erhält Items + Level-Boost (5% XP in allen Skills)

**Mercy NICHT gewährt:**
- Verlierer stirbt permanent (Hardcore Death)
- Nur Slime-Rescue möglich (wenn verfügbar)

**Zweck:** Ultimatives Risiko für Hardcore-Spieler

---

## BALANCE & FAIRNESS

### Gewinner-Anreiz für Gnade
**Warum sollte Gewinner Gnade gewähren?**

1. **Ehre-Bonus** (10-50% mehr Ehre je nach Modus)
2. **Reputation** in der Arena-Community
3. **Karma-System**:
   - Viel Gnade gewährt = "Ehrenvoller Kämpfer" Titel
   - Nie Gnade gewährt = "Gnadenloser" Titel (negative Reputation)

### Verlierer-Schutz
**Anti-Missbrauch:**
- Mercy nur **1x pro Kampf** möglich
- Nach Mercy-Gewährung: 24h IRL **keine** Plünderungs-/Hardcore-Arena teilnehmbar
- Nach 3x Mercy in 7 Tagen: Automatisch auf Wager-/Gear-Arena beschränkt (7 Tage Cooldown)

---

## VISUELLE DARSTELLUNG

### Mercy-Animation (Verlierer)
```
1. Character kniet auf ein Knie
2. Waffe/Schild fallen zu Boden
3. Hände heben sich (Surrender-Geste)
4. Kopf senkt sich
5. Aura wechselt zu Weiß (Kapitulation)
```

### Gewinner-Entscheidung
```
Option 1: Gnade gewähren
→ Gewinner nickt
→ Verlierer steht langsam auf
→ Beide verbeugen sich (Respekt)
→ Verlierer wird teleportiert

Option 2: Keine Gnade
→ Gewinner schüttelt Kopf
→ Verlierer's Aura wechselt zu Rot (Verzweiflung)
→ Kampf geht weiter
→ Finisher-Sequenz beginnt (wenn HP auf 0)
```

### Walk of Shame (Plünderungs-/Hardcore-Arena)
```
Verlierer in Unterwäsche:
- Nur Unterhose/BH sichtbar
- Slot 1 Waffe (z.B. Starter-Schwert) bleibt
- Langsames Gehen zur Arena-Tür
- NPCs zeigen auf ihn und lachen (optional)
- Screen-Effekt: Leicht verschwommen (Scham-Effekt)
```

---

## TECHNISCHE IMPLEMENTIERUNG

### Python Backend (Pseudo-Code)

```python
class ArenaMercySystem:
    """
    Gnadenbitt-System für Arena-Kämpfe
    """

    MERCY_MODES = {
        "friendship": {
            "penalty": "durability_loss",
            "amount": 0.10,  # 10% Durability
            "honor_bonus": 50
        },
        "wager": {
            "penalty": "wagered_item",
            "honor_bonus": 100
        },
        "gear": {
            "penalty": "random_equipped_item",
            "amount": 1,
            "honor_bonus": 200
        },
        "plunder": {
            "penalty": "all_inventory",
            "exceptions": ["underwear", "weapon_slot_1"],
            "honor_bonus": 500,
            "walk_of_shame": True
        },
        "hardcore": {
            "penalty": "all_inventory_plus_xp",
            "xp_loss": 0.10,  # 10% all skills
            "honor_bonus": 1000,
            "walk_of_shame": True,
            "permadeath_risk": True
        }
    }

    def __init__(self, arena_mode):
        self.mode = arena_mode
        self.mercy_requested = False
        self.mercy_granted = None

    def check_mercy_available(self, loser_hp, loser_used_mercy):
        """
        Prüft ob Mercy-Option verfügbar ist
        """
        if loser_used_mercy:
            return False  # Nur 1x pro Kampf

        if loser_hp <= 0.15:  # Unter 15% HP
            return True

        return False

    def request_mercy(self, loser, winner):
        """
        Verlierer bittet um Gnade
        """
        self.mercy_requested = True

        # Animation
        loser.play_animation("kneel_surrender")
        loser.set_aura("white")

        # Prompt für Gewinner
        winner.show_prompt({
            "title": f"{loser.name} bittet um Gnade!",
            "reward": self.get_mercy_reward_preview(),
            "options": [
                {"label": "Gnade gewähren", "value": True},
                {"label": "Keine Gnade", "value": False}
            ],
            "timeout": 10  # 10 Sekunden
        })

    def grant_mercy(self, loser, winner, granted):
        """
        Gewinner entscheidet
        """
        self.mercy_granted = granted

        if granted:
            # Gnade gewährt
            penalty = self.apply_penalty(loser, winner)
            honor = self.give_honor_bonus(winner)

            # Teleport + Animations
            loser.play_animation("bow_respect")
            winner.play_animation("nod_respect")

            if self.MERCY_MODES[self.mode].get("walk_of_shame"):
                loser.strip_to_underwear()
                loser.slow_walk_to_exit()
            else:
                loser.teleport_to_arena_exit()

            return {
                "result": "mercy_granted",
                "penalty": penalty,
                "honor": honor
            }
        else:
            # Keine Gnade
            loser.set_aura("red")
            loser.add_status_effect("desperation", duration=10)

            # Kampf geht weiter
            return {
                "result": "no_mercy",
                "continue_fight": True
            }

    def apply_penalty(self, loser, winner):
        """
        Wendet Strafe an je nach Arena-Modus
        """
        mode_config = self.MERCY_MODES[self.mode]
        penalty_type = mode_config["penalty"]

        if penalty_type == "durability_loss":
            lost = loser.reduce_all_durability(mode_config["amount"])
            return f"Durability -{mode_config['amount']*100}%"

        elif penalty_type == "wagered_item":
            item = loser.remove_wagered_item()
            winner.add_item(item)
            return f"Item verloren: {item.name}"

        elif penalty_type == "random_equipped_item":
            item = loser.remove_random_equipped()
            winner.add_item(item)
            return f"Ausrüstung verloren: {item.name}"

        elif penalty_type == "all_inventory":
            exceptions = mode_config["exceptions"]
            items = loser.remove_all_items(except_types=exceptions)
            for item in items:
                winner.add_item(item)
            return f"ALLES verloren ({len(items)} Items)"

        elif penalty_type == "all_inventory_plus_xp":
            # Items
            exceptions = mode_config["exceptions"]
            items = loser.remove_all_items(except_types=exceptions)
            for item in items:
                winner.add_item(item)

            # XP Loss
            xp_lost = loser.reduce_all_skills_xp(mode_config["xp_loss"])
            winner.boost_all_skills_xp(0.05)  # 5% Boost für Gewinner

            return f"ALLES + {mode_config['xp_loss']*100}% XP verloren"

    def give_honor_bonus(self, winner):
        """
        Gibt Ehre-Bonus für Gnade
        """
        honor = self.MERCY_MODES[self.mode]["honor_bonus"]
        winner.add_honor(honor)

        # Karma-System Update
        winner.increment_stat("mercy_granted")
        if winner.get_stat("mercy_granted") >= 50:
            winner.unlock_title("Ehrenvoller Kämpfer")

        return honor

    def check_cooldowns(self, player):
        """
        Prüft Cooldowns für Arena-Teilnahme
        """
        mercy_count_7d = player.get_mercy_count_last_7_days()

        if mercy_count_7d >= 3:
            # Restricted to low-risk arenas
            return {
                "can_join": {
                    "friendship": True,
                    "wager": True,
                    "gear": False,
                    "plunder": False,
                    "hardcore": False
                },
                "restriction_expires": player.get_mercy_restriction_expiry()
            }

        # Check 24h cooldown after mercy
        last_mercy = player.get_last_mercy_timestamp()
        if last_mercy and (time.now() - last_mercy) < timedelta(hours=24):
            return {
                "can_join": {
                    "friendship": True,
                    "wager": True,
                    "gear": True,
                    "plunder": False,
                    "hardcore": False
                },
                "cooldown_expires": last_mercy + timedelta(hours=24)
            }

        return {
            "can_join": {
                "friendship": True,
                "wager": True,
                "gear": True,
                "plunder": True,
                "hardcore": True
            }
        }
```

---

## NAJIKA'S REAKTIONEN

### Wenn Kuja um Gnade bittet:
```
*schockiert*
"KUJA! Du... du hast VERLOREN?!"

*wird ernst*
"Aber... das ist in Ordnung. Du lebst noch. Das ist alles was zählt."

*hilft ihm auf*
"Komm, lass uns nach Hause gehen. Wir werden trainieren.
Beim nächsten Mal GEWINNST du!"
```

### Wenn Kuja Gnade gewährt:
```
*stolz*
"Das war edel von dir, Kuja! Ein echter Krieger zeigt Ehre!"

*hüpft auf*
"Und schau, wie viel Ehre du dafür bekommen hast!
Respekt ist manchmal mehr wert als Beute!"
```

### Wenn Kuja keine Gnade gewährt:
```
*nachdenklich*
"Du hast keine Gnade gezeigt...

*seufzt*
"Manchmal muss man hart sein. Ich verstehe das.
Aber denk daran - eines Tages könntest DU derjenige sein,
der um Gnade bittet."
```

---

## ZUSAMMENFASSUNG

**Das Arena Gnadenbitt-System bietet:**

1. **5 Arena-Modi** mit unterschiedlichen Risiko-Leveln
2. **Dynamische Entscheidungen** für Gewinner (Gnade oder Tod?)
3. **Balance** durch Ehre-Bonus und Karma-System
4. **Schutz** durch Cooldowns und Restrictions
5. **Spannung** durch Walk of Shame und hohe Einsätze
6. **Fairness** durch klare Regeln und Grenzen

**Kernphilosophie:**
"Ehre im Sieg, Würde in der Niederlage, Gnade als Zeichen der Stärke"

---

**Ende Design-Dokument**

*Nächster Schritt: User-Feedback & Implementierung*
