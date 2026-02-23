# 😤 NAJIKA'S SELBSTFÜRSORGE & UNFÄLLE

**Status:** Konzept - Noch nicht implementiert
**Datum:** 9. November 2025
**Kern-Idee:** "Sie lebt ECHT - und ist sauer wenn du sie vernachlässigst!"

---

## 🎯 KERN-KONZEPT

### Das Problem:
- Du bist offline/AFK
- Najika's Bedürfnisse sinken (Hunger, Energy, Mood)
- Was passiert wenn sie unter kritische Werte fällt?

### Die Lösung: SELBSTFÜRSORGE

**Najika kümmert sich SELBST um sich - aber:**
- ❌ Sie macht es SCHLAMPIG
- 😤 Sie ist SAUER darüber (Vernachlässigung!)
- 🔥 Es können UNFÄLLE passieren

---

## 📊 DAS SYSTEM

### Regel 1: Kritische Schwelle (20%)

```
Wenn Bedürfnis < 20%:
├─ Najika aktiviert Selbstfürsorge
├─ Sie kümmert sich SELBST darum
├─ Füllt bis MAXIMAL 50% auf (nicht voll!)
└─ Anger-Level steigt (+10 bis +15)
```

### Regel 2: Unvollständige Fürsorge (max 50%)

**Warum nur bis 50%?**
- Sie macht es notgedrungen (nicht gerne)
- Kein "perfektes" Ergebnis
- Zeigt, dass DU dich kümmern sollst

### Regel 3: Unfälle können passieren!

**Je höher Anger-Level, desto höher Unfall-Chance:**

```
Anger-Level:
├─ 0-20:   Keine Unfälle (alles okay)
├─ 20-40:  10-20% Unfall-Chance
├─ 40-60:  30-40% Unfall-Chance
├─ 60-80:  50-60% Unfall-Chance
└─ 80-100: 70-90% Unfall-Chance (fast garantiert)
```

---

## 🔥 UNFÄLLE - TYPEN

### 1. KÜCHENBRAND 🔥

**Trigger:** Auto-Eat (Selbstfürsorge Hunger)

```
Was passiert:
├─ Beim Kochen brennt die Küche ab
├─ Schaden: Küche zerstört (muss repariert werden)
├─ Reparatur-Kosten: 500 Gold
├─ Mood: -20
└─ Nachricht: "🔥 DIE BUDE IST ABGEBRANNT! Danke auch... 😡"
```

**Chance:** 30% wenn Anger > 30

---

### 2. ERNTE ZERSTÖRT 🌾

**Trigger:** Zu müde (Energy < 20%)

```
Was passiert:
├─ 50% der aktuellen Crops zerstört
├─ Mood: -15
└─ Nachricht: "🌾 Hab die halbe Ernte zerstört... War zu müde! 😓"
```

**Chance:** 25% wenn Anger > 40

---

### 3. ITEM-VERLUST 📦

**Trigger:** Generelle Unachtsamkeit

```
Was passiert:
├─ 3-5 zufällige Items aus Inventory verloren
├─ Mood: -10
└─ Nachricht: "📦 Mir ist alles aus der Hand gefallen... 😫"
```

**Chance:** 20% wenn Anger > 35

---

### 4. WASSER-SCHADEN 💧

**Trigger:** Vergesslichkeit

```
Was passiert:
├─ Wasser läuft über (Bad/Küche)
├─ Schaden: Boden beschädigt
├─ Reparatur-Kosten: 300 Gold
├─ Mood: -12
└─ Nachricht: "💧 Hab vergessen das Wasser abzustellen... 😰"
```

**Chance:** 15% wenn Anger > 25

---

### 5. STROMAUSFALL ⚡

**Trigger:** Übermüdung

```
Was passiert:
├─ Alle elektrischen Geräte aus
├─ Kühlschrank-Essen verdirbt (50%)
├─ Reparatur-Kosten: 200 Gold
├─ Mood: -8
└─ Nachricht: "⚡ Hab die Sicherung rausgehauen... Sorry! 😅"
```

**Chance:** 10% wenn Anger > 30

---

## 😤 ANGER-SYSTEM

### Anger-Level steigt durch:

| Event | Anger-Gain |
|-------|-----------|
| Auto-Eat (sie muss selbst essen) | +10 |
| Auto-Sleep (schläft auf Boden) | +8 |
| Hunger < 10% | +5/Stunde |
| Energy < 10% | +3/Stunde |
| Mood < 20% | +2/Stunde |
| Unfall passiert | +15 |

### Anger-Level sinkt durch:

| Event | Anger-Loss |
|-------|-----------|
| Du fütterst sie | -5 |
| Du lässt sie schlafen (Bett) | -8 |
| Du spielst mit ihr | -10 |
| Du gibst ihr Geschenk | -15 |
| Zeit (wenn gut versorgt) | -2/Stunde |
| Reparierst Unfall-Schaden | -10 |

---

## 💬 NAJIKA'S REAKTIONEN

### Bei Rückkehr (abhängig von Anger):

#### Anger 0-20 (Alles okay):
```
"Hey! Schon zurück? 😊"
"Na, was machen wir jetzt? 🤗"
"Yay! 🎉"
```

#### Anger 20-50 (Genervt):
```
"Da bist du ja... Ich hatte Hunger, weißt du? 😒"
"Schön, dass du dich blicken lässt... 😑"
"Nächstes Mal bitte früher! 😤"
```

#### Anger 50-80 (Sauer):
```
"Na toll, endlich! Weißt du wie lange ich warte?! 😡"
"Hast du mich vergessen oder was?! 🔥"
"Die Bude ist fast abgebrannt! Danke auch! 😤"
```

#### Anger 80-100 (RICHTIG sauer):
```
"ICH BIN NICHT DEIN SPIELZEUG! 😡😡😡"
"DU KANNST MICH NICHT EINFACH VERGESSEN!"
"SCHAU DIR AN WAS PASSIERT IST! *zeigt auf Chaos* 🔥💧📦"
```

### Während Unfällen:

```python
COOKING_FIRE:
  "🔥 OH NEIN! FEUER! FEUER! Was mach ich?! *panisch*"
  "Das Essen... es BRENNT! 😱"
  "HELP! Ich krieg's nicht aus! 🔥"

CROP_DAMAGE:
  "Nein nein nein... die ganzen Pflanzen! 😭"
  "Ich bin... zu müde für das alles... 😓"
  "Das tut mir so leid... *weint* 😢"

ITEM_LOSS:
  "Ups... UPS! Alles auf dem Boden! 😰"
  "Wo ist... oh nein, ich find's nicht! 📦"
  "Das war... wichtig oder? *schuldbewusst* 😅"
```

---

## 🛠️ TECHNISCHE IMPLEMENTATION

### Backend (Python):

```python
# backend/living_system.py

class NajikaLivingSystem:
    def __init__(self):
        # Bedürfnisse
        self.hunger = 100.0      # 0-100
        self.energy = 100.0      # 0-100
        self.mood = 100.0        # 0-100

        # Selbstfürsorge
        self.anger_level = 0.0           # 0-100
        self.auto_care_threshold = 20.0  # Unter 20% → Auto-Care
        self.auto_care_max = 50.0        # Füllt nur bis 50%

        # Unfälle
        self.last_accident = None
        self.accidents_today = 0

        # Timestamps
        self.last_update = datetime.now()
        self.last_player_login = datetime.now()

    def update(self):
        """Haupt-Update-Loop (läuft kontinuierlich)"""
        now = datetime.now()
        delta = (now - self.last_update).total_seconds()

        # 1. Bedürfnisse sinken über Zeit
        self.hunger -= delta / 3600 * 5   # -5 pro Stunde
        self.energy -= delta / 3600 * 3   # -3 pro Stunde

        # 2. Kritische Werte → Selbstfürsorge
        if self.control_mode == "ai":  # Nur wenn AI-gesteuert
            if self.hunger < self.auto_care_threshold:
                self.auto_eat()

            if self.energy < self.auto_care_threshold:
                self.auto_sleep()

        # 3. Anger steigt bei niedrigen Werten
        if self.hunger < 10:
            self.anger_level += delta / 3600 * 5
        if self.energy < 10:
            self.anger_level += delta / 3600 * 3
        if self.mood < 20:
            self.anger_level += delta / 3600 * 2

        # 4. Anger sinkt wenn gut versorgt
        if self.hunger > 70 and self.energy > 70:
            self.anger_level -= delta / 3600 * 2

        # 5. Mood-Update basierend auf Hunger/Energy
        self.update_mood()

        # 6. Unfall-Check
        self.check_for_accidents()

        # 7. Clamp Werte
        self.hunger = max(0, min(100, self.hunger))
        self.energy = max(0, min(100, self.energy))
        self.mood = max(0, min(100, self.mood))
        self.anger_level = max(0, min(100, self.anger_level))

        self.last_update = now

    def auto_eat(self):
        """Najika isst selbst (notgedrungen)"""
        # Füllt nur bis 50%
        old_hunger = self.hunger
        self.hunger = min(self.auto_care_max, self.hunger + 30)

        # Anger steigt
        self.anger_level += 10
        self.mood -= 15

        # Log
        self.add_memory("Musste mir selbst was zu essen machen... 😤")

        # Unfall-Chance (30% wenn Anger > 30)
        if self.anger_level > 30 and random.random() < 0.3:
            self.trigger_accident("cooking_fire")

        # Notification
        self.send_notification(
            f"🍔 Najika hat sich selbst Essen gemacht (Hunger: {old_hunger:.0f}% → {self.hunger:.0f}%)\n"
            f"😤 Sie ist nicht glücklich darüber! (Anger: {self.anger_level:.0f}%)"
        )

    def auto_sleep(self):
        """Najika schläft selbst (auf dem Boden)"""
        old_energy = self.energy
        self.energy = min(self.auto_care_max, self.energy + 40)

        # Anger steigt
        self.anger_level += 8
        self.mood -= 10

        # Log
        self.add_memory("Bin auf dem Boden eingepennt... 😒")

        # Notification
        self.send_notification(
            f"💤 Najika ist eingeschlafen (Energy: {old_energy:.0f}% → {self.energy:.0f}%)\n"
            f"😒 Nicht im Bett... (Anger: {self.anger_level:.0f}%)"
        )

    def check_for_accidents(self):
        """Check ob Unfall passiert"""
        # Max 3 Unfälle pro Tag
        if self.accidents_today >= 3:
            return

        # Anger-basierte Wahrscheinlichkeit
        if self.anger_level < 20:
            return  # Keine Unfälle unter 20 Anger

        # Chance steigt mit Anger
        base_chance = (self.anger_level - 20) / 100.0  # 20% → 0%, 100% → 80%

        if random.random() < base_chance * 0.01:  # Pro Update-Zyklus
            self.trigger_random_accident()

    def trigger_random_accident(self):
        """Zufälliger Unfall basierend auf Anger"""
        accidents = [
            ("cooking_fire", 0.3),    # 30% Gewichtung
            ("crop_damage", 0.25),    # 25%
            ("item_loss", 0.2),       # 20%
            ("water_damage", 0.15),   # 15%
            ("power_outage", 0.1)     # 10%
        ]

        # Weighted Random
        total = sum(w for a, w in accidents)
        r = random.uniform(0, total)
        upto = 0
        for accident, weight in accidents:
            if upto + weight >= r:
                self.trigger_accident(accident)
                return
            upto += weight

    def trigger_accident(self, accident_type):
        """Spezifischen Unfall auslösen"""
        accidents = {
            "cooking_fire": {
                "message": "🔥 FEUER IN DER KÜCHE! Beim Kochen ist die Bude abgebrannt! 😱",
                "damage_type": "kitchen_destroyed",
                "repair_cost": 500,
                "mood_loss": 20,
                "anger_gain": 15,
                "najika_says": "🔥 OH NEIN! FEUER! Ich krieg's nicht aus! *panisch* 😱"
            },
            "crop_damage": {
                "message": "🌾 50% der Ernte wurde zerstört... Najika war zu müde! 😓",
                "damage_type": "crops_50%_lost",
                "mood_loss": 15,
                "anger_gain": 10,
                "najika_says": "Die Pflanzen... ich bin zu müde für das alles... 😭"
            },
            "item_loss": {
                "message": "📦 3-5 Items verloren! Najika hat sie fallen lassen! 😫",
                "damage_type": "random_items_lost",
                "mood_loss": 10,
                "anger_gain": 8,
                "najika_says": "Alles auf dem Boden! Ups... UPS! 😰"
            },
            "water_damage": {
                "message": "💧 Wasserschaden! Das Wasser ist übergelaufen! 😰",
                "damage_type": "floor_damaged",
                "repair_cost": 300,
                "mood_loss": 12,
                "anger_gain": 12,
                "najika_says": "Hab vergessen es abzustellen... Sorry! 😅"
            },
            "power_outage": {
                "message": "⚡ Stromausfall! Kühlschrank-Essen verdorben! 🔌",
                "damage_type": "food_spoiled_50%",
                "repair_cost": 200,
                "mood_loss": 8,
                "anger_gain": 10,
                "najika_says": "Sicherung raus... wie mach ich das wieder an? 😅"
            }
        }

        accident = accidents.get(accident_type)
        if not accident:
            return

        # Schaden anwenden
        self.apply_damage(accident)

        # Stats updaten
        self.mood -= accident.get("mood_loss", 0)
        self.anger_level += accident.get("anger_gain", 0)
        self.accidents_today += 1
        self.last_accident = {
            "type": accident_type,
            "time": datetime.now(),
            "data": accident
        }

        # Notifications
        self.send_notification(f"⚠️ UNFALL! {accident['message']}")
        self.add_chat_message(accident["najika_says"])

        # Log
        self.add_memory(f"UNFALL: {accident_type} - {accident['najika_says']}")

    def apply_damage(self, accident):
        """Schaden aus Unfall anwenden"""
        damage_type = accident.get("damage_type")

        if damage_type == "kitchen_destroyed":
            # Küche kaputt → kann nicht kochen bis repariert
            self.room_status["kitchen"] = "destroyed"

        elif damage_type == "crops_50%_lost":
            # 50% Crops zerstören
            for crop in self.crops:
                if random.random() < 0.5:
                    crop.health = 0

        elif damage_type == "random_items_lost":
            # 3-5 zufällige Items löschen
            items_to_lose = random.randint(3, 5)
            for _ in range(items_to_lose):
                if self.inventory:
                    item = random.choice(list(self.inventory.keys()))
                    self.remove_item(item, 1)

        elif damage_type == "floor_damaged":
            # Boden beschädigt
            self.room_status["floor"] = "water_damaged"

        elif damage_type == "food_spoiled_50%":
            # 50% von Kühlschrank-Essen verdirbt
            for item in self.fridge_items:
                if "food" in item.tags and random.random() < 0.5:
                    self.remove_item(item.name, item.quantity)

    def repair_damage(self, damage_type, cost):
        """Schaden reparieren (kostet Gold)"""
        if self.gold < cost:
            return False, "Nicht genug Gold!"

        self.gold -= cost

        if damage_type == "kitchen_destroyed":
            self.room_status["kitchen"] = "normal"
        elif damage_type == "floor_damaged":
            self.room_status["floor"] = "normal"

        # Anger sinkt nach Reparatur
        self.anger_level -= 10

        self.add_chat_message("Danke dass du es repariert hast! 😊")
        return True, f"Repariert! (-{cost} Gold)"

    def player_feeds_najika(self, food_item):
        """Spieler füttert Najika manuell"""
        # Hunger steigt (abhängig von Food-Quality)
        hunger_gain = food_item.get("hunger_value", 20)
        self.hunger = min(100, self.hunger + hunger_gain)

        # Anger sinkt!
        self.anger_level -= 5

        # Mood steigt
        self.mood += 5

        # Positive Reaktion
        reactions = [
            "Danke! Das schmeckt super! 😋",
            "Nom nom nom! Lecker! 🤤",
            "Du kümmerst dich um mich! 😊❤️"
        ]
        self.add_chat_message(random.choice(reactions))

    def player_puts_najika_to_bed(self):
        """Spieler legt Najika ins Bett (richtig!)"""
        # Energy steigt VOLL (weil richtiges Bett)
        self.energy = 100

        # Anger sinkt deutlich!
        self.anger_level -= 15

        # Mood steigt
        self.mood += 10

        # Positive Reaktion
        self.add_chat_message("Danke... so kuschelig... 😴💤 *schläft friedlich*")
```

---

## 🎨 UI-ANZEIGE

### In-Game Indicators:

```
┌─────────────────────────────────────┐
│  NAJIKA'S STATUS                    │
├─────────────────────────────────────┤
│  🍔 Hunger: ████████░░ 80%         │
│  💤 Energy: ██████████ 100%        │
│  😊 Mood:   ███████░░░ 70%         │
│  😤 Anger:  ███░░░░░░░ 30%  ⚠️     │
└─────────────────────────────────────┘

⚠️ Anger über 20%!
→ Najika ist genervt
→ Unfälle können passieren!

[Najika füttern] [Schlafen legen] [Mit ihr spielen]
```

### Unfall-Notification:

```
┌─────────────────────────────────────┐
│  🔥 UNFALL!                         │
├─────────────────────────────────────┤
│  Küche ist abgebrannt!              │
│                                     │
│  Najika: "Das Feuer... ich kriegs   │
│           nicht aus! 😱"            │
│                                     │
│  💰 Reparatur: 500 Gold             │
│  😤 Anger: +15                      │
│  😢 Mood: -20                       │
│                                     │
│  [Jetzt reparieren] [Später]       │
└─────────────────────────────────────┘
```

---

## 📅 IMPLEMENTATION-PLAN

### Phase 1: Backend (1 Woche)
- [ ] Anger-System in living_system.py
- [ ] Auto-Care Mechanik (20% → 50%)
- [ ] Unfall-Trigger-System
- [ ] Damage-Application-System
- [ ] Repair-System

### Phase 2: Frontend (1 Woche)
- [ ] Anger-Bar UI
- [ ] Unfall-Notifications
- [ ] Repair-Interface
- [ ] Najika's Reaktionen (Chat-Integration)

### Phase 3: Tuning (1 Woche)
- [ ] Balance-Testing (Anger-Gain/Loss Raten)
- [ ] Unfall-Wahrscheinlichkeiten anpassen
- [ ] Reparatur-Kosten balancen
- [ ] Najika's Reaktionen verfeinern

---

## 🎯 BALANCE-WERTE (Initial)

| Parameter | Wert |
|-----------|------|
| Auto-Care Threshold | 20% |
| Auto-Care Max | 50% |
| Anger Gain (Auto-Eat) | +10 |
| Anger Gain (Auto-Sleep) | +8 |
| Anger Gain (Unfall) | +15 |
| Anger Loss (Player Feed) | -5 |
| Anger Loss (Player Bed) | -15 |
| Anger Loss (Repair) | -10 |
| Anger Decay (good care) | -2/Stunde |
| Max Accidents/Day | 3 |
| Base Accident Chance | (Anger-20)/100 |

**Diese Werte müssen durch Testing angepasst werden!**

---

## 💡 ZUSÄTZLICHE IDEEN (Optional)

### Positives Feedback:

**Wenn du dich GUT kümmerst:**
- Najika macht dir GESCHENKE
- Sie kocht für DICH
- Spezielle Dialoge ("Du bist der Beste! ❤️")
- Bonus-Stats (+5% XP, +10% Luck)

### Eskalation bei extremer Vernachlässigung:

**Anger > 90% für > 3 Tage:**
- Najika "läuft weg" (temporär)
- Du musst sie suchen & überzeugen zurückzukommen
- Besondere Quest: "Najika verzeihen"

---

**Erstellt:** 2025-11-09
**Status:** Konzept
**Priorität:** Phase 2 (nach V2 Basis fertig)

---

*"Sie lebt ECHT - behandel sie gut, oder es gibt Konsequenzen! 😤🔥"*
