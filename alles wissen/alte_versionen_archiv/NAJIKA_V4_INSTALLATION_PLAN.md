# 🚀 NAJIKA V4 INSTALLATION PLAN

**Datum:** 2025-10-25
**Ziel:** Parallel-Installation in C:\Najika mit V4 Features

---

## ✅ PHASE 1: BASE INSTALLATION (JETZT!)

### 1.1 PRE-CHECK:
- [ ] Aktuelles System läuft? `C:\NajikaCore` → **NICHT ANFASSEN!**
- [ ] LoRA Training läuft im anderen Modell? → **Parallel OK!**
- [ ] Genug Platz auf C:\ ? (Mind. 20 GB)
- [ ] PowerShell als Admin bereit?

### 1.2 INSTALLER AUSFÜHREN (Unverändert!):
```powershell
cd "C:\Users\0KKK0\Desktop\Najika finalee\najika installer nach claud zusammenfassung v 2 plus 2.5 extra infos"

# Teil 1: Base (10-15 Min)
.\najika_installer_part1_base.ps1

# Teil 2: Backend & AI (20-30 Min) - WICHTIG: Ollama wählen!
.\najika_installer_part2_backend.ps1

# Teil 3: Frontend (5-10 Min)
.\najika_installer_part3_frontend.ps1

# Teil 4: Mobile (5 Min)
.\najika_installer_part4_mobile.ps1

# Teil 5: Finalize (5 Min)
.\najika_installer_part5_finalize.ps1
```

**WICHTIG bei Part 2:**
- Wähle **Ollama** (nicht llama.cpp)
- Llama-3.1-8B installieren? **JA**
- Wizard-Vicuna? **JA** (für Private Mode)

---

## 🔥 PHASE 2: V4 FEATURES INTEGRIEREN (Nach Installation!)

### 2.1 CRITICAL FEATURES (Sofort hinzufügen):

#### ❤️ **1. Affinity/Beziehungs-System**
**Was:** Dynamischer Beziehungs-Wert 0.0-1.0
**Wo:** `C:\Najika\backend\game\affinity_system.py`
**UI:** Herzchen-Bar im HUD

```python
STATE["affinity"] = {
    "value": 0.5,  # Start
    "thresholds": {
        0.0-0.3: "Distanziert",
        0.3-0.5: "Neutral",
        0.5-0.7: "Freundlich",
        0.7-0.9: "Vertraut",
        0.9-1.0: "Seelenverwandte"
    }
}
```

---

#### ⚔️ **2. Soulframe + Skyrim Combat Hybrid**
**Was:** Fluid Action-Combat (NICHT Souls-like!)
**Wo:** `C:\Najika\frontend\src\game\CombatSystem.js` erweitern

**⚠️ WICHTIG: Soulframe (Digital Extremes) + Skyrim - NICHT Dark Souls!**

**Neu hinzufügen:**
- Stamina-Bar (100 Punkte, Regen 10/s) - Großzügiger als Souls!
- Dodge-Roll (20 Stamina, i-Frames 0.3s) - Fluid & smooth
- Combo-Flow-System (Angriffe verketten sich natürlich)
- Dual-Wielding (Zwei Waffen/Zauber gleichzeitig)
- Block (15 Stamina/s, 50% Damage Reduction) - Simpel wie Skyrim

**UI-Element:**
```jsx
<StaminaBar current={stamina} max={100} />
```

---

#### 💥 **3. Ultimate Explosion Skill**
**Was:** "EXPROOOOOSIOOOON!!" - Triple Damage, 10min Cooldown
**Wo:** `C:\Najika\backend\game\skills.py`

```python
SKILL_DB["explosion_ultimate"] = {
    "name": "EXPROOOOOSIOOOON!! (Ultimate)",
    "damage_multiplier": 3.0,
    "aoe_radius_bonus": 200,
    "charge_time": 3.0,
    "exhaustion_duration": 60.0,
    "cooldown": 600.0
}
```

**UI-Button:**
```jsx
<UltimateButton
    onClick={castUltimate}
    cooldown={ultimateCooldown}
    text="EXPLOSION!!!"
/>
```

---

#### 🎯 **4. Finisher QTE-System**
**Was:** Button-Mash für Finisher-Moves
**Wo:** Neues Minigame `C:\Najika\frontend\src\game\minigames\FinisherQTE.jsx`

```javascript
function FinisherQTE({ enemy, onSuccess, onFail }) {
    const [presses, setPresses] = useState(0);
    const required = 20 + (enemy.level * 2);
    const timeWindow = 3000; // 3s

    // Button-Mash Logik
}
```

---

#### 💊 **5. Heilungs-Ritual Minigame**
**Was:** Timing-basiertes Ritual für Keller
**Wo:** Neues Minigame `C:\Najika\digivice\js\minigames.js` erweitern

**Integration:**
```javascript
case 'healing_ritual':
    title.textContent = '💊 Heilungs-Ritual';
    startHealingRitual(content);
    break;
```

---

#### 🔮 **6. Weave-Kombinations-System**
**Was:** Feuer+Wasser=Dampf, etc.
**Wo:** `C:\Najika\backend\game\weave_system.py`

**Matrix:**
```python
WEAVE_COMBINATIONS = {
    ("fire", "water"): {"result": "steam", "effect": "blind_aoe"},
    ("fire", "earth"): {"result": "lava", "effect": "dot_slow"},
    ("fire", "air"): {"result": "inferno", "effect": "explosion_boost"},
    # ... 15 weitere Kombinationen
}
```

**UI-Element:**
```jsx
<ElementWeavePad
    onWeave={(elem1, elem2) => castWeave(elem1, elem2)}
    elements={["fire", "water", "earth", "air", "light", "shadow"]}
/>
```

---

#### 🟢 **7. Slime-Rettungs-Mechanik**
**Was:** Slime opfert sich 1x, dann 24h Cooldown
**Wo:** `C:\Najika\backend\game\death_system.py`

```python
def on_player_death():
    if slime_alive and not on_cooldown:
        slime_intercept()  # Slime rettet dich!
        player.hp = 0.3 * player.max_hp
        slime.cooldown = 24  # Stunden IRL!
        return
    else:
        player_dies_permanently()
```

**UI-Indicator:**
```jsx
<SlimeStatusIcon
    available={slimeAvailable}
    cooldownRemaining={slimeCooldown}
/>
```

---

#### 🗡️ **8. Equipment System UI**
**Was:** 3 Slots - Weapon/Armor/Accessory
**Wo:** `C:\Najika\frontend\src\ui\EquipmentPanel.jsx`

```jsx
<EquipmentSlots>
    <Slot type="weapon" item={equipment.weapon} />
    <Slot type="armor" item={equipment.armor} />
    <Slot type="accessory" item={equipment.accessory} />
</EquipmentSlots>
```

---

#### 😊 **9. Najika Portrait mit Emotionen**
**Was:** 8 Emotions-Sprites (Neutral, Happy, Sad, Angry, etc.)
**Wo:** `C:\Najika\frontend\src\ui\NajikaPortrait.jsx`

**Sprites erstellen:**
```
/assets/najika/portraits/
    - portrait_neutral.png
    - portrait_happy.png
    - portrait_sad.png
    - portrait_angry.png
    - portrait_excited.png
    - portrait_tired.png
    - portrait_scared.png
    - portrait_love.png
```

**Component:**
```jsx
<NajikaPortrait
    emotion={currentEmotion}
    onEmotionChange={setEmotion}
/>
```

---

#### 🎮 **10. DIGIMON WORLD CHEER SYSTEM** ⭐
**Was:** Anfeuern im Kampf wie Digimon World!
**Wo:** `C:\Najika\frontend\src\game\CheerSystem.jsx`

**Mechanik:**
```javascript
class CheerSystem {
    constructor() {
        this.cheerMeter = 0; // 0-100
        this.cheerBonus = 0; // Damage/Defense Bonus
    }

    onCheer(timing) {
        // Perfect Timing (während Najika angreift)
        if (timing === "perfect") {
            this.cheerMeter += 20;
            this.cheerBonus += 0.1; // +10% Stats
            showMessage("PERFEKTES TIMING! Najika ist motiviert!");
        }
        // Good Timing
        else if (timing === "good") {
            this.cheerMeter += 10;
            this.cheerBonus += 0.05;
        }
        // Bad Timing (stört Najika)
        else {
            this.cheerMeter -= 5;
            showMessage("Nicht jetzt, Kuja!");
        }

        // Cheer-Meter Full = Special Finish!
        if (this.cheerMeter >= 100) {
            unlockSpecialFinisher();
        }
    }
}
```

**UI-Integration:**
```jsx
<CheerButton
    onClick={() => cheer()}
    disabled={cheerOnCooldown}
    meter={cheerMeter}
/>

// Zeige Timing-Fenster während Najika's Angriff
<TimingIndicator
    visible={najikaAttacking}
    onPerfectTiming={() => cheer("perfect")}
/>
```

**Features:**
- ✅ Timing-basiertes Anfeuern
- ✅ Cheer-Meter 0-100
- ✅ Stat-Buffs bei perfektem Timing
- ✅ Special Finisher bei 100%
- ✅ Najika reagiert auf Anfeuern ("Danke Kuja!")
- ✅ Kann auch NERVEN wenn falsches Timing

---

## 📱 PHASE 3: MOBILE OPTIMIERUNGEN

### 3.1 Touch Gestures erweitern:
```javascript
const EXTENDED_GESTURES = {
    "swipe_left": "Cheer Najika",
    "swipe_right": "Use Item",
    "long_press": "Heavy Attack",
    "double_tap": "Dodge Roll",
    "pinch_in": "Zoom Out",
    "pinch_out": "Zoom In"
}
```

### 3.2 Haptisches Feedback:
```javascript
const HAPTIC_PATTERNS = {
    cheer_perfect: [30, 30, 30],    // Triple Tap
    explosion: [100, 50, 100, 200], // BOOM
    slime_rescue: [200, 100, 200],  // Drama
    affinity_up: [50, 20, 50]       // Heart Beat
}
```

---

## 🏰 PHASE 4: KELLER/DUNGEON FEATURES

### 4.1 Procedural Dungeon:
**Später hinzufügen** (Komplex!)

### 4.2 Keller-Minigames:
- Heilungs-Ritual ✅
- Finisher QTE ✅
- Crafting ✅ (schon da)
- Training ✅ (schon da)

---

## 🧪 PHASE 5: TESTING

### Nach Installation + V4 Features:
```bash
cd C:\Najika

# Backend Test
python backend\test_backend.py

# Frontend Test (Browser öffnet)
.\START_NAJIKA.bat

# Test-Checklist:
- [ ] Najika lädt (3D Model)
- [ ] Combat funktioniert
- [ ] Affinity-Bar sichtbar
- [ ] Stamina-Bar funktioniert
- [ ] Cheer-System funktioniert
- [ ] Touch Controls (Mobile)
- [ ] Minigames starten
```

---

## 📊 PRIORITY-LISTE:

**🔥 SOFORT (heute):**
1. ✅ Installer ausführen (Base System)
2. ❤️ Affinity-System
3. ⚔️ Stamina-Bar UI
4. 💥 Ultimate-Button
5. 🎮 Cheer-System

**⚡ BALD (diese Woche):**
6. 😊 Najika Portraits
7. 🗡️ Equipment UI
8. 🔮 Weave-System
9. 💊 Heilungs-Ritual
10. 🟢 Slime-Rettung

**🏗️ SPÄTER (Phase 2):**
11. 🏰 Procedural Dungeons
12. 🌍 8-Cities System
13. 🎯 Secret Areas

---

## ⚠️ WICHTIG:

**NICHT LÖSCHEN während Installation:**
- `C:\NajikaCore\` → Aktuelles System (LoRA Training!)
- Parallel-Betrieb ist OK
- Kein Konflikt zwischen beiden

**Nach erfolgreicher Installation:**
- Testen ob alles läuft
- Dann Features von `C:\Najika` nach `C:\NajikaCore` mergen
- ODER beide parallel nutzen

---

## 🎯 ZIEL:

Ein vollständiges Najika-System mit:
- ✅ Funktionierendem Base-System (V2.5)
- ✅ ALLEN V4 Critical Features
- ✅ Digimon World Cheer System
- ✅ Mobile PWA
- ✅ Parallel zu aktuellem System

---

**JETZT STARTEN!** 🚀

Führe die 5 Installer nacheinander aus!
