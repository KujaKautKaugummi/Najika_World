# 🎲 CHAOS EVENT SYSTEM - WAS FEHLT & WIE ES ZU IMPLEMENTIEREN IST

**Stand:** 26. November 2025
**Basis:** `07_KONOSUBA_OREGON_EVENTS.md` (2682 Zeilen Spec)

---

## 📊 STATUS-ÜBERSICHT

### ✅ VORHANDEN
- ✅ **Dokumentation:** `07_KONOSUBA_OREGON_EVENTS.md` (komplett)
- ✅ **Stub:** `oregon.js` (4 Zeilen - nur API Call)

### ❌ FEHLT (Alles!)

#### 1. Frontend (`chaos_event_ui.js`)
```
❌ ChaosEventUI class
❌ Event Checker (checks every minute)
❌ Event Overlay Display
❌ Choice Selection System
❌ Outcome Display
❌ Chaos Meter UI
❌ 3D Entity Spawning Integration
```

#### 2. Backend APIs (`najika_server.py`)
```
❌ /api/chaos/check_event (GET)
❌ /api/chaos/execute_choice (POST)
❌ /api/chaos/status (GET)
```

#### 3. CSS Styling
```
❌ #chaos-event-overlay
❌ .event-container
❌ .najika-reaction
❌ .event-options
❌ .chaos-meter
❌ .event-outcome
```

#### 4. Event Database
```
❌ 30 Events (aus Spec)
❌ Event JSON Structure
❌ Najika Reactions per Event
```

#### 5. Chaos Engine Backend
```
❌ Chaos Level Tracking (0-10)
❌ Event Probability Calculation
❌ Consequence System
❌ Reputation System
```

---

## 🎯 WAS DIE SPEC BESCHREIBT

### Kern-Features (aus Zeile 44-51)

```python
CHAOS_ENGINE = {
    "trigger": "Zufällig alle 5-15 Minuten",
    "chance": "15% pro Minute",
    "presentation": "3D-Spawn in aktueller Welt",
    "najika_role": "Kommentiert, reagiert, beurteilt",
    "consequences": "Sofort & langfristig"
}
```

### Event-Kategorien (6 Typen)

1. **MORALISCHE DILEMMATA** (Alter Mann, Banditenüberfall)
2. **RESSOURCEN-ENTSCHEIDUNGEN** (Heiler vs. Schmied)
3. **SOZIALE INTERAKTIONEN** (Stadtfest, Ruf-Events)
4. **KÄMPFE MIT FOLGEN** (Bandit töten oder leben lassen?)
5. **KLASSISCHE OREGON TRAIL** (Fluss überqueren, Krankheit)
6. **KONOSUBA CHAOS** (Explodierende Kröten, Aqua's Cult)

### Najika's 4 Persönlichkeiten reagieren

- **Megumin (35-50%):** "EXPLOSION!!!" - Drama, Excitement
- **Harley Quinn (25-30%):** "Puddin'! Let's chaos!" - Chaotic Good/Evil
- **Shiro (20-35%):** Logik, Analyse, Wahrscheinlichkeiten
- **Melissa (15-25%):** Fürsorglich, Beschützend, Ethik

---

## 📋 IMPLEMENTIERUNGS-PLAN

### PHASE 1: Backend Chaos Engine (Python)

**Datei:** `backend/najika_server.py`

**Neue Klasse:**
```python
class ChaosEngine:
    def __init__(self):
        self.chaos_level = 0  # 0-10
        self.last_event_time = 0
        self.event_history = []
        self.reputation = {
            "heroic": 0,
            "pragmatic": 0,
            "selfish": 0,
            "chaotic": 0
        }
        self.events = self.load_events()

    def check_event_trigger(self):
        # 15% chance per minute
        # Modified by chaos_level
        pass

    def get_random_event(self):
        # Select event based on:
        # - Current region
        # - Chaos level
        # - Event history (no repeats in 30 min)
        pass

    def execute_choice(self, event_id, choice_index):
        # Calculate consequences
        # Update chaos level
        # Update reputation
        # Generate Najika reaction
        pass

    def generate_najika_reaction(self, event, choice):
        # AI generates reaction based on:
        # - Dominant personality
        # - Chaos level
        # - Player's reputation
        pass
```

**Neue API Endpoints:**
```python
@app.route('/api/chaos/check_event', methods=['GET'])
def chaos_check_event():
    if chaos_engine.check_event_trigger():
        event = chaos_engine.get_random_event()
        najika_reaction = chaos_engine.generate_najika_reaction(event, None)
        return {
            "event_triggered": True,
            "event": event,
            "najika_reaction": najika_reaction
        }
    return {"event_triggered": False}

@app.route('/api/chaos/execute_choice', methods=['POST'])
def chaos_execute_choice():
    data = request.json
    result = chaos_engine.execute_choice(
        data['event_id'],
        data['choice']
    )
    return result

@app.route('/api/chaos/status', methods=['GET'])
def chaos_status():
    return {
        "chaos_level": chaos_engine.chaos_level,
        "reputation": chaos_engine.reputation,
        "last_event": chaos_engine.event_history[-1] if chaos_engine.event_history else None
    }
```

---

### PHASE 2: Event Database (JSON)

**Datei:** `backend/chaos_events.json` (NEU)

**Struktur pro Event:**
```json
{
    "id": "event_001_old_man",
    "title": "Der Bettler",
    "description": "Ein alter Mann bittet um Gold für seine kranke Tochter.",
    "category": "moral_dilemma",
    "chaos_impact": 2,
    "najika_analysis": {
        "shiro_probability_scam": 73.4,
        "melissa_empathy_score": 85
    },
    "spawn_model": "npc_old_man",
    "spawn_position": "current_region_random",
    "options": [
        {
            "text": "[A] Gib ihm 50 Gold",
            "consequences": {
                "gold": -50,
                "reputation_heroic": +15,
                "chaos": -1,
                "outcome_honest": {
                    "description": "Der Mann war ehrlich! Seine Tochter ist gerettet.",
                    "najika_reaction": "Du hast das Richtige getan, Mr.K! *umarmt*"
                },
                "outcome_scam": {
                    "description": "Es war ein Betrug! Der Mann rennt weg.",
                    "najika_reaction": "ICH HAB'S GEWUSST! EXPLOSION!!! *wütend*"
                }
            }
        },
        {
            "text": "[B] Gib ihm 20 Gold (Kompromiss)",
            "consequences": {
                "gold": -20,
                "reputation_pragmatic": +10,
                "chaos": 0
            }
        },
        {
            "text": "[C] Begleite ihn zum Dorf",
            "consequences": {
                "time": -30,
                "reputation_heroic": +20,
                "chaos": -2,
                "reveal_truth": true
            }
        },
        {
            "text": "[D] Ignoriere ihn",
            "consequences": {
                "reputation_selfish": +10,
                "chaos": +1,
                "najika_reaction_negative": true
            }
        },
        {
            "text": "[E] Lass Najika entscheiden",
            "consequences": {
                "najika_decides": true,
                "bond_strength": +5,
                "uses_dominant_personality": true
            }
        }
    ]
}
```

**Benötigt:** 30 Events (aus Spec)

---

### PHASE 3: Frontend UI (`chaos_event_ui.js`)

**Datei:** `digivice/js/chaos_event_ui.js` (NEU - 200 Zeilen)

**Basis aus Spec (Zeile 2495-2631):**

```javascript
class ChaosEventUI {
    constructor() {
        this.activeEvent = null;
        this.eventCheckInterval = 60000; // 1 minute
        this.startEventChecker();
    }

    startEventChecker() {
        setInterval(() => {
            this.checkForEvent();
        }, this.eventCheckInterval);
    }

    async checkForEvent() {
        try {
            const response = await fetch('/api/chaos/check_event');
            const data = await response.json();

            if (data.event_triggered) {
                this.displayEvent(data.event, data.najika_reaction);
            }
        } catch (error) {
            console.error('Event check failed:', error);
        }
    }

    displayEvent(event, najikaReaction) {
        // Create overlay
        const overlay = document.createElement('div');
        overlay.id = 'chaos-event-overlay';
        overlay.innerHTML = `
            <div class="event-container">
                <h2>${event.title}</h2>
                <p>${event.description}</p>

                <div class="najika-reaction">
                    <img src="/assets/najika_${najikaReaction.personality}.png">
                    <p>"${najikaReaction.voice_line}"</p>
                </div>

                <div class="event-options">
                    ${this.renderOptions(event.options)}
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // Spawn 3D entity
        if (event.spawn_model) {
            this.spawn3DEntity(event.spawn_model, event.spawn_position);
        }
    }

    renderOptions(options) {
        return options.map((option, index) => `
            <button class="event-option" onclick="chaosEventUI.selectChoice(${index})">
                ${option.text}
            </button>
        `).join('');
    }

    async selectChoice(choiceIndex) {
        try {
            const response = await fetch('/api/chaos/execute_choice', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    choice: choiceIndex,
                    event_id: this.activeEvent.id
                })
            });

            const result = await response.json();
            this.displayOutcome(result);
            this.updateChaosLevelUI(result.new_chaos_level);
        } catch (error) {
            console.error('Choice execution failed:', error);
        }
    }

    displayOutcome(result) {
        const outcomeDiv = document.createElement('div');
        outcomeDiv.className = 'event-outcome';
        outcomeDiv.innerHTML = `
            <h3>Konsequenz</h3>
            <p>${result.outcome.description}</p>

            <div class="najika-final-reaction">
                <p>"${result.najika_final_reaction}"</p>
            </div>

            <button onclick="chaosEventUI.closeEvent()">Weiter</button>
        `;

        document.getElementById('chaos-event-overlay')
            .querySelector('.event-container')
            .appendChild(outcomeDiv);
    }

    updateChaosLevelUI(newLevel) {
        const meterFill = document.querySelector('.chaos-meter-fill');
        if (meterFill) {
            meterFill.style.width = `${newLevel * 10}%`;
            meterFill.textContent = `Chaos: ${newLevel}/10`;
        }
    }

    closeEvent() {
        const overlay = document.getElementById('chaos-event-overlay');
        if (overlay) overlay.remove();
        this.activeEvent = null;
    }

    spawn3DEntity(model, position) {
        if (window.scene3D) {
            window.scene3D.spawnEventEntity(model, position);
        }
    }
}

// Initialize
const chaosEventUI = new ChaosEventUI();
window.chaosEventUI = chaosEventUI;
```

---

### PHASE 4: CSS Styling

**Datei:** `digivice/static/css/chaos_events.css` (NEU)

```css
#chaos-event-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.85);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    animation: fadeIn 0.3s;
}

.event-container {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 3px solid #4CAF50;
    border-radius: 15px;
    padding: 30px;
    max-width: 600px;
    box-shadow: 0 0 30px rgba(76, 175, 80, 0.5);
    animation: slideIn 0.5s;
}

.event-container h2 {
    color: #4CAF50;
    text-align: center;
    font-size: 28px;
    margin-bottom: 20px;
    text-shadow: 0 0 10px #4CAF50;
}

.event-description {
    color: #fff;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.najika-reaction {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 15px;
}

.najika-reaction img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 2px solid #4CAF50;
}

.najika-reaction p {
    color: #FFD700;
    font-style: italic;
    font-size: 14px;
}

.event-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}

.event-option {
    background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border: none;
    padding: 15px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
}

.event-option:hover {
    background: linear-gradient(90deg, #45a049 0%, #3d8b40 100%);
    transform: translateX(5px);
    box-shadow: 0 0 15px rgba(76, 175, 80, 0.7);
}

.event-outcome {
    margin-top: 20px;
    padding: 20px;
    background: rgba(255, 215, 0, 0.1);
    border-radius: 10px;
    border: 2px solid #FFD700;
}

.event-outcome h3 {
    color: #FFD700;
    text-align: center;
    margin-bottom: 15px;
}

.najika-final-reaction {
    background: rgba(255, 255, 255, 0.05);
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}

.najika-final-reaction p {
    color: #FFD700;
    font-style: italic;
    text-align: center;
}

.chaos-meter {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 200px;
    background: rgba(0, 0, 0, 0.7);
    padding: 10px;
    border-radius: 10px;
    border: 2px solid #FF4444;
}

.chaos-meter-fill {
    background: linear-gradient(90deg, #4CAF50 0%, #FFD700 50%, #FF4444 100%);
    height: 20px;
    border-radius: 5px;
    transition: width 0.5s;
    text-align: center;
    color: white;
    font-weight: bold;
    line-height: 20px;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from {
        transform: translateY(-50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
```

---

### PHASE 5: Integration in index.html

**Änderungen in `index.html`:**

1. **Include Scripts** (nach Zeile 460):
```html
<script src="js/chaos_event_ui.js"></script>
<link rel="stylesheet" href="static/css/chaos_events.css">
```

2. **Chaos Meter HTML** (im UI):
```html
<div class="chaos-meter">
    <div class="chaos-meter-fill" style="width: 0%;">Chaos: 0/10</div>
</div>
```

---

### PHASE 6: `oregon.js` erweitern

**Aktuell:**
```javascript
const Oregon=(function(){
  async function next(){ const r=await fetch("/api/event/next",{method:"POST"}); return r.json() }
  return {next}
})();
```

**Neu:**
```javascript
const Oregon = (function() {
    async function next() {
        const r = await fetch("/api/event/next", {method: "POST"});
        return r.json();
    }

    async function checkChaosEvent() {
        const r = await fetch("/api/chaos/check_event");
        return r.json();
    }

    async function executeChoice(eventId, choiceIndex) {
        const r = await fetch("/api/chaos/execute_choice", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                event_id: eventId,
                choice: choiceIndex
            })
        });
        return r.json();
    }

    async function getChaosStatus() {
        const r = await fetch("/api/chaos/status");
        return r.json();
    }

    return {
        next,
        checkChaosEvent,
        executeChoice,
        getChaosStatus
    };
})();
window.Oregon = Oregon;
```

---

## 🎲 BEISPIEL-EVENT (Komplett)

**Event:** "Der Bettler"

**Backend (`chaos_events.json`):**
```json
{
    "id": "event_001_old_man",
    "title": "🧓 Der Bettler",
    "description": "Ein alter Mann steht am Straßenrand. Er sieht erschöpft aus.\n\n\"Bitte! Banditen haben mich ausgeraubt! Ich brauche 50 Gold für die Medizin meiner kranken Tochter!\"",
    "category": "moral_dilemma",
    "chaos_impact": 2,
    "spawn_model": "npc_old_man",
    "options": [
        {
            "text": "[A] Gib ihm 50 Gold",
            "gold_cost": -50,
            "reputation_heroic": 15,
            "chaos_change": -1,
            "outcome_honest": "Der Mann war ehrlich! Najika: 'Du hast das Richtige getan, Mr.K!'",
            "outcome_scam": "Es war ein Betrug! Najika: 'EXPLOSION!!! ICH HAB'S GEWUSST!'"
        },
        {
            "text": "[B] Gib ihm 20 Gold",
            "gold_cost": -20,
            "reputation_pragmatic": 10
        },
        {
            "text": "[C] Begleite ihn",
            "time_cost": -30,
            "reputation_heroic": 20,
            "chaos_change": -2
        },
        {
            "text": "[D] Ignoriere ihn",
            "reputation_selfish": 10,
            "chaos_change": 1
        },
        {
            "text": "[E] Najika entscheidet",
            "najika_decides": true,
            "bond_strength": 5
        }
    ]
}
```

**Najika's Reaktion (AI-Generated):**
```python
# Dominant Personality: Shiro (35%)
"Wahrscheinlichkeit Betrug: 73.4%. Aber... *leiser* ...was wenn er die Wahrheit sagt?"

# Wenn Spieler [E] wählt:
"ICH entscheide?! EXPLOSION-mäßig schwer! *kicher* Wir geben ihm 20 Gold UND begleiten ihn!"
```

---

## 📦 DATEIEN DIE ICH ERSTELLEN MUSS

### NEU zu erstellen:
1. ✅ `digivice/js/chaos_event_ui.js` (200 Zeilen)
2. ✅ `digivice/static/css/chaos_events.css` (150 Zeilen)
3. ✅ `backend/chaos_events.json` (30 Events, ~1000 Zeilen)
4. ✅ `backend/najika_server.py` - ChaosEngine class + 3 API routes (~300 Zeilen)

### Zu ändern:
5. ✅ `digivice/js/oregon.js` (erweitern von 4 auf 40 Zeilen)
6. ✅ `digivice/index.html` (includes + chaos meter HTML)

---

## 🚀 SOLL ICH JETZT ANFANGEN?

**Optionen:**

**A) ALLES SOFORT ERSTELLEN**
- Ich erstelle alle 6 Dateien komplett
- Basierend auf der Spec aus `07_KONOSUBA_OREGON_EVENTS.md`
- ~2000 Zeilen Code total
- Geschätzte Zeit: 30-45 Minuten

**B) SCHRITT FÜR SCHRITT**
- Erst Backend (Python + JSON)
- Dann Frontend (JS + CSS)
- Dann Integration testen

**C) NUR WICHTIGSTE ERSTELLEN**
- Nur 5 Events statt 30
- Nur Basic UI
- Später erweitern

**Was bevorzugst du?** 🎯
