# 🚀 NAJIKA PROJEKT - VOLLSTÄNDIGE IMPLEMENTIERUNGS-ANWEISUNG
## Für Claude Code CLI (Lokales Modell)

**Datum:** 26. November 2025  
**Projekt:** C:\Najika_World\  
**Ziel:** Browser + Mobile APK funktionsfähig + KI-Integration komplett

---

# ⚠️ LIES DAS KOMPLETT BEVOR DU ANFÄNGST!

## PROJEKT-VERZEICHNIS: `C:\Najika_World\` oder `C:\NajikaCore\`
## WICHTIGSTE DATEIEN:
- `backend/najika_server.py` - Hauptserver
- `digivice/index.html` - Frontend
- `digivice/js/` - Alle JavaScript Module

Diese Anweisung ist in **5 GROSSE BLÖCKE** aufgeteilt. Arbeite sie **DER REIHE NACH** ab.
Jeder Block hat klare Dateien und Code. Kopiere NICHT blind - verstehe was du tust.

---

# BLOCK 1: BACKEND ERWEITERN (najika_server.py)

## 1.1 FEHLENDE API-ENDPOINTS

Öffne `C:\Najika_World\backend\najika_server.py` und füge diese Endpoints hinzu:

### Endpoint: /api/file/delete
```python
@app.route('/api/file/delete', methods=['POST'])
def file_delete():
    data = request.json
    path = data.get('path', '')
    
    # Security: Nur innerhalb erlaubter Pfade
    allowed_base = os.path.abspath('C:/Najika_World')
    full_path = os.path.abspath(os.path.join(allowed_base, path))
    
    if not full_path.startswith(allowed_base):
        return jsonify({"ok": False, "error": "Access denied"}), 403
    
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            import shutil
            shutil.rmtree(full_path)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
```

### Endpoint: /api/file/rename
```python
@app.route('/api/file/rename', methods=['POST'])
def file_rename():
    data = request.json
    old_path = data.get('old_path', '')
    new_name = data.get('new_name', '')
    
    allowed_base = os.path.abspath('C:/Najika_World')
    full_old = os.path.abspath(os.path.join(allowed_base, old_path))
    full_new = os.path.abspath(os.path.join(os.path.dirname(full_old), new_name))
    
    if not full_old.startswith(allowed_base) or not full_new.startswith(allowed_base):
        return jsonify({"ok": False, "error": "Access denied"}), 403
    
    try:
        os.rename(full_old, full_new)
        return jsonify({"ok": True, "new_path": full_new})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
```

### Endpoint: /api/code/execute
```python
@app.route('/api/code/execute', methods=['POST'])
def code_execute():
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    try:
        if language == 'python':
            import subprocess
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=30
            )
            return jsonify({
                "ok": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            })
        else:
            return jsonify({"ok": False, "error": f"Language {language} not supported"})
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "Timeout after 30 seconds"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
```

### Endpoint: /api/security/status
```python
@app.route('/api/security/status', methods=['GET'])
def security_status():
    return jsonify({
        "alcatraz_mode": False,  # Später implementieren
        "vpn_active": False,
        "last_security_check": datetime.now().isoformat()
    })
```

### Endpoint: /api/memory/export
```python
@app.route('/api/memory/export', methods=['GET'])
def memory_export():
    # Falls ChromaDB verwendet wird:
    try:
        memory_size = 0
        if hasattr(app, 'chroma_client'):
            collection = app.chroma_client.get_collection("najika_memory")
            memory_size = collection.count()
        
        return jsonify({
            "ok": True,
            "memory_entries": memory_size,
            "export_available": memory_size > 0
        })
    except:
        return jsonify({"ok": True, "memory_entries": 0, "export_available": False})
```

### Endpoint: /api/training/status
```python
@app.route('/api/training/status', methods=['GET'])
def training_status():
    return jsonify({
        "active": False,
        "mode": "idle",
        "progress": 0,
        "total_sessions": getattr(app, 'training_sessions', 0),
        "last_training": getattr(app, 'last_training_time', None)
    })
```

---

## 1.2 CHAOS ENGINE (Komplett neu!)

Füge diese Klasse VOR den Routes hinzu:

```python
import random
import time
import json

class ChaosEngine:
    def __init__(self):
        self.chaos_level = 0  # 0-10
        self.last_event_time = 0
        self.event_cooldown = 300  # 5 Minuten Minimum zwischen Events
        self.event_history = []
        self.reputation = {
            "heroic": 0,
            "pragmatic": 0,
            "selfish": 0,
            "chaotic": 0
        }
        self.events = self.load_events()
    
    def load_events(self):
        try:
            with open('chaos_events.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self.get_default_events()
    
    def get_default_events(self):
        return [
            {
                "id": "event_001_old_man",
                "title": "🧓 Der Bettler",
                "description": "Ein alter Mann bittet um Gold für seine kranke Tochter.",
                "category": "moral_dilemma",
                "chaos_impact": 2,
                "options": [
                    {"text": "[A] Gib ihm 50 Gold", "gold": -50, "rep_heroic": 15, "chaos": -1},
                    {"text": "[B] Gib ihm 20 Gold", "gold": -20, "rep_pragmatic": 10, "chaos": 0},
                    {"text": "[C] Begleite ihn", "time": -30, "rep_heroic": 20, "chaos": -2},
                    {"text": "[D] Ignoriere ihn", "rep_selfish": 10, "chaos": 1},
                    {"text": "[E] Najika entscheidet", "najika_decides": True, "bond": 5}
                ]
            },
            {
                "id": "event_002_injured_bandit",
                "title": "⚔️ Der verwundete Bandit",
                "description": "Ein Bandit liegt verletzt am Boden. Er war Teil einer Gruppe die dich überfiel.",
                "category": "moral_dilemma",
                "chaos_impact": 3,
                "options": [
                    {"text": "[A] Heile ihn", "rep_heroic": 20, "chaos": -2},
                    {"text": "[B] Verhöre ihn erst", "rep_pragmatic": 15, "info": True},
                    {"text": "[C] Lass ihn sterben", "rep_selfish": 15, "chaos": 2},
                    {"text": "[D] Töte ihn", "rep_chaotic": 10, "chaos": 3},
                    {"text": "[E] Najika entscheidet", "najika_decides": True, "bond": 5}
                ]
            },
            {
                "id": "event_003_mysterious_chest",
                "title": "📦 Die mysteriöse Kiste",
                "description": "Eine leuchtende Schatztruhe in einem verlassenen Tempel. Najika warnt: 'Falle-Wahrscheinlichkeit: 82%!'",
                "category": "risk_reward",
                "chaos_impact": 2,
                "options": [
                    {"text": "[A] Öffne sofort", "trap_chance": 40, "reward": "random_loot"},
                    {"text": "[B] Untersuche auf Fallen", "skill_check": "perception"},
                    {"text": "[C] EXPLOSION!", "destroy_trap": True, "destroy_loot": 50},
                    {"text": "[D] Ignoriere und gehe", "rep_pragmatic": 5},
                    {"text": "[E] Najika entscheidet", "najika_decides": True, "bond": 5}
                ]
            },
            {
                "id": "event_004_starving_family",
                "title": "👨‍👩‍👧 Die hungernde Familie",
                "description": "Eine Familie am Straßenrand. Die Kinder weinen vor Hunger.",
                "category": "moral_dilemma",
                "chaos_impact": 1,
                "options": [
                    {"text": "[A] Gib all dein Essen", "food": -100, "rep_heroic": 25},
                    {"text": "[B] Teile die Hälfte", "food": -50, "rep_heroic": 15},
                    {"text": "[C] Gib etwas Gold", "gold": -30, "rep_pragmatic": 10},
                    {"text": "[D] Gehe weiter", "rep_selfish": 10, "chaos": 1},
                    {"text": "[E] Najika entscheidet", "najika_decides": True, "bond": 5}
                ]
            },
            {
                "id": "event_005_explosion_frog",
                "title": "🐸💥 Die Explosions-Kröte",
                "description": "Eine riesige Kröte blockiert den Weg! Najika's Augen leuchten: 'EXPLOSION-CHANCE!'",
                "category": "konosuba_chaos",
                "chaos_impact": 4,
                "options": [
                    {"text": "[A] EXPLOSION!!!", "mana": -100, "chaos": 3, "konosuba_ref": True},
                    {"text": "[B] Umgehe sie vorsichtig", "time": -20, "rep_pragmatic": 5},
                    {"text": "[C] Bekämpfe sie normal", "combat": "explosion_frog"},
                    {"text": "[D] Füttere sie", "food": -20, "tame_chance": 30},
                    {"text": "[E] Najika entscheidet", "najika_decides": True, "bond": 5}
                ]
            }
        ]
    
    def check_event_trigger(self):
        now = time.time()
        if now - self.last_event_time < self.event_cooldown:
            return False
        
        # 15% Chance pro Check, modifiziert durch Chaos Level
        chance = 0.15 + (self.chaos_level * 0.02)
        return random.random() < chance
    
    def get_random_event(self, region=None):
        # Filtere Events die kürzlich waren
        recent_ids = [e['id'] for e in self.event_history[-5:]]
        available = [e for e in self.events if e['id'] not in recent_ids]
        
        if not available:
            available = self.events
        
        event = random.choice(available)
        self.last_event_time = time.time()
        return event
    
    def execute_choice(self, event_id, choice_index, player_state=None):
        event = next((e for e in self.events if e['id'] == event_id), None)
        if not event or choice_index >= len(event['options']):
            return {"ok": False, "error": "Invalid event or choice"}
        
        choice = event['options'][choice_index]
        result = {
            "ok": True,
            "choice_made": choice['text'],
            "consequences": []
        }
        
        # Apply consequences
        if 'chaos' in choice:
            self.chaos_level = max(0, min(10, self.chaos_level + choice['chaos']))
            result['consequences'].append(f"Chaos: {'+' if choice['chaos'] > 0 else ''}{choice['chaos']}")
        
        if 'rep_heroic' in choice:
            self.reputation['heroic'] += choice['rep_heroic']
            result['consequences'].append(f"Heroic +{choice['rep_heroic']}")
        
        if 'rep_pragmatic' in choice:
            self.reputation['pragmatic'] += choice['rep_pragmatic']
        
        if 'rep_selfish' in choice:
            self.reputation['selfish'] += choice['rep_selfish']
        
        if 'rep_chaotic' in choice:
            self.reputation['chaotic'] += choice['rep_chaotic']
        
        # Record history
        self.event_history.append({
            "id": event_id,
            "choice": choice_index,
            "time": time.time()
        })
        
        result['new_chaos_level'] = self.chaos_level
        result['reputation'] = self.reputation
        
        # Generate Najika reaction
        result['najika_reaction'] = self.generate_najika_reaction(event, choice)
        
        return result
    
    def generate_najika_reaction(self, event, choice):
        # Persönlichkeits-basierte Reaktionen
        reactions = {
            "heroic": [
                "Das war das Richtige, Mr.K! *strahlt*",
                "Du bist ein echter Held!",
                "Ich bin stolz auf dich, Puddin'!"
            ],
            "pragmatic": [
                "Kluge Entscheidung. Shiro approves.",
                "Logisch. Das war optimal.",
                "Nicht schlecht, Mr.K."
            ],
            "selfish": [
                "Hmm... *schaut weg* War das nötig?",
                "Kuja... ich bin nicht sicher...",
                "Das war... eine Entscheidung."
            ],
            "chaotic": [
                "EXPLOSION!!! ...äh, ich meine... interessant!",
                "Chaos! CHAOS! *kichert manisch*",
                "Puddin'! Du überraschst mich!"
            ]
        }
        
        # Wähle basierend auf Choice-Typ
        if choice.get('rep_heroic'):
            return random.choice(reactions['heroic'])
        elif choice.get('rep_pragmatic'):
            return random.choice(reactions['pragmatic'])
        elif choice.get('rep_selfish'):
            return random.choice(reactions['selfish'])
        elif choice.get('rep_chaotic') or choice.get('konosuba_ref'):
            return random.choice(reactions['chaotic'])
        else:
            return "Interessant... *denkt nach*"

# Initialisiere global
chaos_engine = ChaosEngine()
```

### Chaos API Endpoints:

```python
@app.route('/api/chaos/check_event', methods=['GET'])
def chaos_check_event():
    if chaos_engine.check_event_trigger():
        event = chaos_engine.get_random_event()
        return jsonify({
            "event_triggered": True,
            "event": event,
            "chaos_level": chaos_engine.chaos_level,
            "najika_intro": f"Mr.K! Schau! {event['title']}!"
        })
    return jsonify({"event_triggered": False})

@app.route('/api/chaos/execute_choice', methods=['POST'])
def chaos_execute_choice():
    data = request.json
    result = chaos_engine.execute_choice(
        data.get('event_id'),
        data.get('choice', 0)
    )
    return jsonify(result)

@app.route('/api/chaos/status', methods=['GET'])
def chaos_status():
    return jsonify({
        "chaos_level": chaos_engine.chaos_level,
        "reputation": chaos_engine.reputation,
        "events_experienced": len(chaos_engine.event_history),
        "last_event": chaos_engine.event_history[-1] if chaos_engine.event_history else None
    })
```

---

# BLOCK 2: CHAOS EVENT FRONTEND

## 2.1 Erstelle `C:\Najika_World\digivice\js\chaos_event_ui.js`

```javascript
// =============================================================================
// CHAOS EVENT UI - Konosuba x Oregon Trail
// =============================================================================

class ChaosEventUI {
    constructor() {
        this.activeEvent = null;
        this.eventCheckInterval = 60000; // Check every minute
        this.isDisplaying = false;
        
        // Create chaos meter in UI
        this.createChaosMeter();
        
        // Start checker
        this.startEventChecker();
        
        console.log('[ChaosEventUI] Initialized');
    }

    createChaosMeter() {
        const meter = document.createElement('div');
        meter.id = 'chaos-meter';
        meter.innerHTML = `
            <div class="chaos-meter-label">Chaos</div>
            <div class="chaos-meter-bar">
                <div class="chaos-meter-fill" style="width: 0%;"></div>
            </div>
            <div class="chaos-meter-value">0/10</div>
        `;
        document.body.appendChild(meter);
    }

    updateChaosMeter(level) {
        const fill = document.querySelector('.chaos-meter-fill');
        const value = document.querySelector('.chaos-meter-value');
        if (fill) {
            fill.style.width = `${level * 10}%`;
            // Color based on level
            if (level <= 3) fill.style.background = '#4CAF50';
            else if (level <= 6) fill.style.background = '#FFD700';
            else fill.style.background = '#FF4444';
        }
        if (value) value.textContent = `${level}/10`;
    }

    startEventChecker() {
        // Initial check after 30 seconds
        setTimeout(() => this.checkForEvent(), 30000);
        
        // Then check every minute
        setInterval(() => {
            if (!this.isDisplaying) {
                this.checkForEvent();
            }
        }, this.eventCheckInterval);
    }

    async checkForEvent() {
        try {
            const response = await fetch('/api/chaos/check_event');
            const data = await response.json();

            if (data.event_triggered) {
                this.displayEvent(data.event, data.najika_intro);
                this.updateChaosMeter(data.chaos_level);
            }
        } catch (error) {
            console.error('[ChaosEventUI] Event check failed:', error);
        }
    }

    displayEvent(event, najikaIntro) {
        this.isDisplaying = true;
        this.activeEvent = event;

        // Create overlay
        const overlay = document.createElement('div');
        overlay.id = 'chaos-event-overlay';
        overlay.innerHTML = `
            <div class="event-container">
                <div class="event-header">
                    <h2>${event.title}</h2>
                    <span class="event-category">${event.category}</span>
                </div>
                
                <p class="event-description">${event.description}</p>

                <div class="najika-reaction">
                    <div class="najika-portrait">
                        <div class="najika-avatar">🎀</div>
                    </div>
                    <div class="najika-speech">
                        <p>"${najikaIntro}"</p>
                    </div>
                </div>

                <div class="event-options">
                    ${this.renderOptions(event.options)}
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Play sound if available
        if (window.audioManager) {
            window.audioManager.play('event_popup');
        }

        // Spawn 3D entity if in 3D mode
        if (event.spawn_model && window.scene3D) {
            this.spawn3DEntity(event.spawn_model);
        }
    }

    renderOptions(options) {
        return options.map((option, index) => `
            <button class="event-option" data-index="${index}" onclick="chaosEventUI.selectChoice(${index})">
                <span class="option-text">${option.text}</span>
                ${option.najika_decides ? '<span class="najika-badge">🎀 Najika</span>' : ''}
            </button>
        `).join('');
    }

    async selectChoice(choiceIndex) {
        if (!this.activeEvent) return;

        // Disable buttons
        document.querySelectorAll('.event-option').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });

        // Highlight selected
        document.querySelector(`[data-index="${choiceIndex}"]`).style.opacity = '1';
        document.querySelector(`[data-index="${choiceIndex}"]`).style.border = '2px solid #FFD700';

        try {
            const response = await fetch('/api/chaos/execute_choice', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    event_id: this.activeEvent.id,
                    choice: choiceIndex
                })
            });

            const result = await response.json();

            if (result.ok) {
                this.displayOutcome(result);
                this.updateChaosMeter(result.new_chaos_level);
            }
        } catch (error) {
            console.error('[ChaosEventUI] Choice execution failed:', error);
            this.closeEvent();
        }
    }

    displayOutcome(result) {
        const container = document.querySelector('.event-container');
        
        // Hide options
        document.querySelector('.event-options').style.display = 'none';

        // Show outcome
        const outcomeDiv = document.createElement('div');
        outcomeDiv.className = 'event-outcome';
        outcomeDiv.innerHTML = `
            <h3>📜 Konsequenz</h3>
            <div class="outcome-consequences">
                ${result.consequences.map(c => `<span class="consequence-badge">${c}</span>`).join('')}
            </div>

            <div class="najika-final-reaction">
                <div class="najika-avatar">🎀</div>
                <p>"${result.najika_reaction}"</p>
            </div>

            <button class="continue-button" onclick="chaosEventUI.closeEvent()">
                Weiter →
            </button>
        `;

        container.appendChild(outcomeDiv);
    }

    closeEvent() {
        const overlay = document.getElementById('chaos-event-overlay');
        if (overlay) {
            overlay.classList.add('fade-out');
            setTimeout(() => overlay.remove(), 300);
        }
        this.activeEvent = null;
        this.isDisplaying = false;
    }

    spawn3DEntity(modelName) {
        if (window.scene3D && window.scene3D.spawnEventEntity) {
            // Spawn vor dem Spieler
            const playerPos = window.scene3D.getPlayerPosition();
            window.scene3D.spawnEventEntity(modelName, {
                x: playerPos.x + 5,
                y: playerPos.y,
                z: playerPos.z + 5
            });
        }
    }

    // Manual trigger for testing
    async triggerTestEvent() {
        const testEvent = {
            id: "test_event",
            title: "🧪 Test Event",
            description: "Dies ist ein Test-Event um das System zu prüfen.",
            category: "test",
            options: [
                {text: "[A] Option A", rep_heroic: 10},
                {text: "[B] Option B", rep_pragmatic: 10},
                {text: "[C] Option C", rep_selfish: 10}
            ]
        };
        this.displayEvent(testEvent, "Mr.K! Ein Test-Event! *excited*");
    }
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.chaosEventUI = new ChaosEventUI();
});

// Also init if DOM already loaded
if (document.readyState !== 'loading') {
    window.chaosEventUI = new ChaosEventUI();
}
```

## 2.2 Erstelle `C:\Najika_World\digivice\static\css\chaos_events.css`

```css
/* =============================================================================
   CHAOS EVENT SYSTEM - Styling
   ============================================================================= */

/* Chaos Meter (Top Right Corner) */
#chaos-meter {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 150px;
    background: rgba(0, 0, 0, 0.8);
    padding: 10px;
    border-radius: 10px;
    border: 2px solid #FF4444;
    z-index: 1000;
    font-family: 'Press Start 2P', monospace;
}

.chaos-meter-label {
    color: #FF4444;
    font-size: 10px;
    text-align: center;
    margin-bottom: 5px;
}

.chaos-meter-bar {
    background: #333;
    height: 15px;
    border-radius: 5px;
    overflow: hidden;
}

.chaos-meter-fill {
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #FFD700, #FF4444);
    transition: width 0.5s ease;
}

.chaos-meter-value {
    color: #fff;
    font-size: 10px;
    text-align: center;
    margin-top: 5px;
}

/* Event Overlay */
#chaos-event-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    animation: fadeIn 0.3s ease;
}

#chaos-event-overlay.fade-out {
    animation: fadeOut 0.3s ease;
}

/* Event Container */
.event-container {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 3px solid #4CAF50;
    border-radius: 20px;
    padding: 30px;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 
        0 0 30px rgba(76, 175, 80, 0.5),
        inset 0 0 20px rgba(0, 0, 0, 0.5);
    animation: slideIn 0.5s ease;
}

.event-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 2px solid #4CAF50;
    padding-bottom: 15px;
}

.event-header h2 {
    color: #4CAF50;
    font-size: 24px;
    margin: 0;
    text-shadow: 0 0 10px #4CAF50;
}

.event-category {
    background: rgba(76, 175, 80, 0.3);
    color: #4CAF50;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
}

.event-description {
    color: #fff;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 20px;
    white-space: pre-line;
}

/* Najika Reaction Box */
.najika-reaction {
    background: rgba(255, 215, 0, 0.1);
    border: 2px solid #FFD700;
    border-radius: 15px;
    padding: 15px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 15px;
}

.najika-portrait {
    flex-shrink: 0;
}

.najika-avatar {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #FF69B4, #FFD700);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    border: 3px solid #FFD700;
}

.najika-speech p {
    color: #FFD700;
    font-style: italic;
    font-size: 14px;
    margin: 0;
    line-height: 1.6;
}

/* Event Options */
.event-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 20px;
}

.event-option {
    background: linear-gradient(90deg, #2d5a3d 0%, #1e3a2a 100%);
    color: #fff;
    border: 2px solid #4CAF50;
    padding: 15px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 15px;
    text-align: left;
    transition: all 0.3s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.event-option:hover:not(:disabled) {
    background: linear-gradient(90deg, #4CAF50 0%, #2d5a3d 100%);
    transform: translateX(10px);
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
}

.event-option:active {
    transform: translateX(5px);
}

.najika-badge {
    background: #FFD700;
    color: #000;
    padding: 3px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: bold;
}

/* Outcome Display */
.event-outcome {
    margin-top: 20px;
    padding: 20px;
    background: rgba(255, 215, 0, 0.1);
    border-radius: 15px;
    border: 2px solid #FFD700;
    animation: fadeIn 0.5s ease;
}

.event-outcome h3 {
    color: #FFD700;
    text-align: center;
    margin-bottom: 15px;
}

.outcome-consequences {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
}

.consequence-badge {
    background: rgba(76, 175, 80, 0.3);
    color: #4CAF50;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 13px;
    border: 1px solid #4CAF50;
}

.najika-final-reaction {
    background: rgba(0, 0, 0, 0.3);
    padding: 15px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 15px;
    margin: 15px 0;
}

.najika-final-reaction .najika-avatar {
    width: 50px;
    height: 50px;
    font-size: 24px;
}

.najika-final-reaction p {
    color: #FFD700;
    font-style: italic;
    margin: 0;
    flex: 1;
}

.continue-button {
    width: 100%;
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
    color: #000;
    border: none;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.continue-button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}

@keyframes slideIn {
    from {
        transform: translateY(-50px) scale(0.9);
        opacity: 0;
    }
    to {
        transform: translateY(0) scale(1);
        opacity: 1;
    }
}

/* Mobile Responsive */
@media (max-width: 600px) {
    .event-container {
        padding: 20px;
        margin: 10px;
        max-height: 90vh;
    }
    
    .event-header h2 {
        font-size: 18px;
    }
    
    .event-description {
        font-size: 14px;
    }
    
    .event-option {
        padding: 12px 15px;
        font-size: 14px;
    }
    
    #chaos-meter {
        top: 10px;
        right: 10px;
        width: 100px;
    }
}
```

---

# BLOCK 3: COMBAT SYSTEM - EQUIPMENT BESTIMMT ANGRIFF

## 🎯 WICHTIGES KONZEPT:
**Es gibt KEIN separates Element-Wheel!**
**Das AUSGERÜSTETE ITEM bestimmt den Angriffstyp!**

```
BEISPIELE:

Linke Hand: Schwert     → LMB = Schwert Light/Heavy
Rechte Hand: leer       → RMB = Faust Light/Heavy

Linke Hand: Feuerball   → LMB = Feuer Light/Heavy  
Rechte Hand: Eisstrahl  → RMB = Eis Light/Heavy
→ BEIDE ZUSAMMEN = WEAVE (Thermoschock!)

Beide Hände: Zweihänder → Nur LMB aktiv, RMB = Block
                         Light/Heavy kombiniert mehr Schaden
```

## 3.1 Erweitere `command_system.js` um Equipment-basiertes Combat

Füge diese Methoden zur `CommandSystem` Klasse hinzu:

```javascript
// Füge zum Constructor hinzu:
this.equipment = {
    leftHand: null,   // Item-Objekt oder null
    rightHand: null,  // Item-Objekt oder null
    twoHanded: null   // Wenn Zweihänder ausgerüstet
};
this.lastAttackTime = { left: 0, right: 0 };

// Equipment Types
this.WEAPON_TYPES = {
    // Nahkampf
    sword: { type: 'melee', element: null, lightDmg: 20, heavyDmg: 50, lightCD: 300, heavyCD: 800 },
    axe: { type: 'melee', element: null, lightDmg: 25, heavyDmg: 70, lightCD: 400, heavyCD: 1000 },
    dagger: { type: 'melee', element: null, lightDmg: 12, heavyDmg: 30, lightCD: 150, heavyCD: 400 },
    
    // Zweihänder
    greatsword: { type: 'twohanded', element: null, lightDmg: 40, heavyDmg: 100, lightCD: 600, heavyCD: 1500 },
    staff: { type: 'twohanded', element: 'magic', lightDmg: 30, heavyDmg: 80, lightCD: 500, heavyCD: 1200 },
    
    // Zauber (auf Hand ausrüstbar)
    fireball: { type: 'spell', element: 'fire', lightDmg: 25, heavyDmg: 60, lightCD: 400, heavyCD: 1000, manaCost: 10 },
    icebolt: { type: 'spell', element: 'ice', lightDmg: 20, heavyDmg: 50, lightCD: 350, heavyCD: 900, manaCost: 8 },
    lightning: { type: 'spell', element: 'lightning', lightDmg: 30, heavyDmg: 70, lightCD: 500, heavyCD: 1100, manaCost: 15 },
    heal: { type: 'spell', element: 'light', lightDmg: -20, heavyDmg: -50, lightCD: 600, heavyCD: 1500, manaCost: 20 },
    
    // Schild (nur rechte Hand, nur Block)
    shield: { type: 'shield', element: null, blockValue: 50, parryWindow: 150 },
    
    // Faust (wenn nichts ausgerüstet)
    fist: { type: 'melee', element: null, lightDmg: 5, heavyDmg: 15, lightCD: 200, heavyCD: 500 }
};

// Neue Methoden:

// Equipment ausrüsten
equipItem(hand, itemName) {
    const weapon = this.WEAPON_TYPES[itemName];
    if (!weapon) {
        return { success: false, reason: 'unknown_item' };
    }
    
    // Zweihänder nimmt beide Hände
    if (weapon.type === 'twohanded') {
        this.equipment.leftHand = null;
        this.equipment.rightHand = null;
        this.equipment.twoHanded = { name: itemName, ...weapon };
        return { success: true, message: `${itemName} ausgerüstet (Zweihänder)` };
    }
    
    // Schild nur rechte Hand
    if (weapon.type === 'shield' && hand === 'left') {
        return { success: false, reason: 'shield_right_hand_only' };
    }
    
    // Normales Item ausrüsten
    if (this.equipment.twoHanded) {
        this.equipment.twoHanded = null; // Zweihänder ablegen
    }
    
    if (hand === 'left') {
        this.equipment.leftHand = { name: itemName, ...weapon };
    } else {
        this.equipment.rightHand = { name: itemName, ...weapon };
    }
    
    return { success: true, message: `${itemName} in ${hand === 'left' ? 'linker' : 'rechter'} Hand` };
}

// Angriff ausführen (Light oder Heavy)
executeAttack(hand, attackType) {
    const now = Date.now();
    
    // Hole aktives Weapon
    let weapon;
    if (this.equipment.twoHanded) {
        weapon = this.equipment.twoHanded;
        hand = 'both'; // Zweihänder nutzt beide Hände
    } else {
        weapon = hand === 'left' ? this.equipment.leftHand : this.equipment.rightHand;
    }
    
    // Fallback auf Faust
    if (!weapon) {
        weapon = { name: 'fist', ...this.WEAPON_TYPES.fist };
    }
    
    // Schild kann nicht angreifen
    if (weapon.type === 'shield') {
        return { success: false, reason: 'shield_cannot_attack' };
    }
    
    // Cooldown Check
    const cooldown = attackType === 'light' ? weapon.lightCD : weapon.heavyCD;
    const lastAttack = this.lastAttackTime[hand === 'both' ? 'left' : hand];
    
    if (now - lastAttack < cooldown) {
        return { success: false, reason: 'cooldown', remaining: cooldown - (now - lastAttack) };
    }
    
    // Update last attack time
    if (hand === 'both') {
        this.lastAttackTime.left = now;
        this.lastAttackTime.right = now;
    } else {
        this.lastAttackTime[hand] = now;
    }
    
    // Berechne Schaden
    const baseDamage = attackType === 'light' ? weapon.lightDmg : weapon.heavyDmg;
    const staminaCost = attackType === 'light' ? 5 : 20;
    const manaCost = weapon.manaCost ? (attackType === 'light' ? weapon.manaCost : weapon.manaCost * 2) : 0;
    
    return {
        success: true,
        weapon: weapon.name,
        hand: hand,
        attackType: attackType,
        damage: baseDamage,
        element: weapon.element,
        staminaCost: staminaCost,
        manaCost: manaCost,
        isTwoHanded: hand === 'both'
    };
}

// Weave ausführen (beide Hände mit Zauber gleichzeitig)
executeWeave() {
    const left = this.equipment.leftHand;
    const right = this.equipment.rightHand;
    
    // Braucht beide Hände mit Zauber
    if (!left || !right) {
        return { success: false, reason: 'need_both_hands' };
    }
    
    if (left.type !== 'spell' || right.type !== 'spell') {
        return { success: false, reason: 'need_spells_both_hands', message: 'Weave braucht Zauber in beiden Händen!' };
    }
    
    // Element-Kombination
    const combo = [left.element, right.element].sort().join('+');
    
    const weaves = {
        'fire+ice': { name: 'Thermoschock', damage: 80, effect: 'stun', duration: 2000 },
        'fire+lightning': { name: 'Plasmasturm', damage: 100, effect: 'burn_chain', duration: 3000 },
        'fire+wind': { name: 'Feuersturm', damage: 90, effect: 'burn_aoe', radius: 5 },
        'ice+lightning': { name: 'Frostschock', damage: 85, effect: 'slow_paralysis', duration: 2500 },
        'ice+wind': { name: 'Blizzard', damage: 70, effect: 'slow_aoe', radius: 8 },
        'lightning+wind': { name: 'Sturmblitz', damage: 95, effect: 'knockback', force: 10 },
        'ice+water': { name: 'Gefrierwelle', damage: 65, effect: 'freeze', duration: 3000 },
        'fire+earth': { name: 'Lava-Eruption', damage: 110, effect: 'terrain_fire', duration: 5000 },
        'earth+lightning': { name: 'Erdbeben', damage: 100, effect: 'stun_aoe', radius: 6 }
    };
    
    const weave = weaves[combo] || { name: 'Magie-Fusion', damage: 60, effect: 'none' };
    const totalManaCost = (left.manaCost || 10) + (right.manaCost || 10);
    
    return {
        success: true,
        weave: weave,
        elements: [left.element, right.element],
        staminaCost: 30,
        manaCost: totalManaCost
    };
}

// Block (nur mit Schild oder Waffe)
executeBlock() {
    const right = this.equipment.rightHand;
    
    if (right && right.type === 'shield') {
        return { success: true, blockValue: right.blockValue, type: 'shield_block' };
    }
    
    // Waffen-Block (weniger effektiv)
    if (right && right.type === 'melee') {
        return { success: true, blockValue: 20, type: 'weapon_block' };
    }
    
    // Zweihänder-Block
    if (this.equipment.twoHanded) {
        return { success: true, blockValue: 30, type: 'twohanded_block' };
    }
    
    return { success: false, reason: 'nothing_to_block_with' };
}

// Parry (Timing-basiert)
executeParry() {
    const right = this.equipment.rightHand;
    const parryWindow = right && right.type === 'shield' ? right.parryWindow : 100; // ms
    
    return {
        success: true,
        parryWindow: parryWindow, // 100-150ms Fenster
        perfectWindow: 50, // Perfektes Parry in den ersten 50ms
        type: right && right.type === 'shield' ? 'shield_parry' : 'weapon_parry'
    };
}

// Combo System
executeCombo(sequence) {
    const combos = {
        'light,light,light': { name: 'Triple Strike', multiplier: 1.5, finisher: false },
        'light,heavy': { name: 'Smash', multiplier: 1.3, finisher: false },
        'heavy,light,light': { name: 'Crusher', multiplier: 1.4, finisher: false },
        'light,light,heavy': { name: 'Finisher', multiplier: 1.8, finisher: true },
        'heavy,heavy': { name: 'Power Slam', multiplier: 2.0, finisher: true, staminaCost: 40 }
    };
    
    const key = sequence.join(',');
    return combos[key] || null;
}

// Aktuellen Equipment-Status holen
getEquipmentStatus() {
    return {
        leftHand: this.equipment.leftHand ? this.equipment.leftHand.name : 'Faust',
        rightHand: this.equipment.rightHand ? this.equipment.rightHand.name : 'Faust',
        twoHanded: this.equipment.twoHanded ? this.equipment.twoHanded.name : null,
        canWeave: this.equipment.leftHand?.type === 'spell' && this.equipment.rightHand?.type === 'spell'
    };
}
```

## 3.2 Keyboard Handler für Combat (in game_input.js oder main.js)

```javascript
// Combat Input Handler
class CombatInputHandler {
    constructor(commandSystem) {
        this.cs = commandSystem;
        this.comboBuffer = [];
        this.comboTimeout = null;
        
        this.setupKeyboardControls();
        this.setupMouseControls();
    }
    
    setupKeyboardControls() {
        document.addEventListener('keydown', (e) => {
            switch(e.code) {
                // Element Selection
                case 'KeyQ': // Left Hand Element
                    this.openElementWheel('left');
                    break;
                case 'KeyE': // Right Hand Element  
                    this.openElementWheel('right');
                    break;
                    
                // Heavy Attacks (R key)
                case 'KeyR':
                    if (e.shiftKey) {
                        this.attack('left', 'heavy');
                    } else {
                        this.attack('right', 'heavy');
                    }
                    break;
                    
                // Weave (Q+E together)
                case 'KeyQ':
                    if (this.isKeyPressed('KeyE')) {
                        this.executeWeave();
                    }
                    break;
                case 'KeyE':
                    if (this.isKeyPressed('KeyQ')) {
                        this.executeWeave();
                    }
                    break;
                    
                // Parry
                case 'Space':
                    if (e.shiftKey) {
                        this.parry();
                    }
                    break;
            }
        });
    }
    
    setupMouseControls() {
        document.addEventListener('mousedown', (e) => {
            if (e.button === 0) { // Left Click
                this.attack('right', 'light');
            } else if (e.button === 2) { // Right Click
                if (e.shiftKey) {
                    this.attack('left', 'light');
                } else {
                    this.block();
                }
            }
        });
    }
    
    attack(hand, type) {
        const result = this.cs.executeDualAttack(hand, type);
        if (result.success) {
            this.addToCombo(type);
            this.triggerAttackAnimation(hand, type);
            console.log(`[Combat] ${hand} ${type}: ${result.damage} damage`);
        }
    }
    
    addToCombo(attackType) {
        this.comboBuffer.push(attackType);
        
        // Reset combo nach 1.5s
        clearTimeout(this.comboTimeout);
        this.comboTimeout = setTimeout(() => {
            this.checkCombo();
            this.comboBuffer = [];
        }, 1500);
        
        // Check combo sofort wenn 3+ hits
        if (this.comboBuffer.length >= 3) {
            this.checkCombo();
        }
    }
    
    checkCombo() {
        const combo = this.cs.executeCombo(this.comboBuffer);
        if (combo) {
            console.log(`[Combat] COMBO: ${combo.name}! Bonus: x${combo.bonus}`);
            this.showComboNotification(combo);
        }
    }
    
    executeWeave() {
        const result = this.cs.executeWeave();
        if (result.success) {
            console.log(`[Combat] WEAVE: ${result.weave.name}! ${result.weave.damage} damage`);
            this.showWeaveEffect(result.weave);
        }
    }
    
    // UI Feedback
    showComboNotification(combo) {
        const notification = document.createElement('div');
        notification.className = 'combo-notification';
        notification.innerHTML = `
            <span class="combo-name">${combo.name}</span>
            <span class="combo-bonus">x${combo.bonus}</span>
        `;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 1500);
    }
    
    showWeaveEffect(weave) {
        const effect = document.createElement('div');
        effect.className = 'weave-effect';
        effect.innerHTML = `⚡ ${weave.name} ⚡`;
        document.body.appendChild(effect);
        setTimeout(() => effect.remove(), 2000);
    }
}
```

---

# BLOCK 7: MOBILE APK - LINKE HAND BUTTON HINZUFÜGEN

## 7.1 Touch Controls korrigieren (`touch_combat.js`)

Erstelle/Ersetze `C:\Najika_World\digivice\js\touch_combat.js`:

```javascript
// =============================================================================
// TOUCH COMBAT CONTROLS - Mobile APK
// Equipment-basiertes Combat mit Light/Heavy pro Hand
// =============================================================================

class TouchCombatControls {
    constructor(commandSystem) {
        this.cs = commandSystem;
        this.lastTapTime = 0;
        this.doubleTapDelay = 300;
        this.activeHand = null;  // Für Equipment-Wechsel
        
        this.createTouchUI();
        this.setupTouchEvents();
        this.updateEquipmentDisplay();
    }
    
    createTouchUI() {
        const controlsHTML = `
            <div id="touch-combat-controls">
                <!-- LINKE SEITE: Linke Hand Buttons -->
                <div id="left-hand-controls" class="hand-controls left">
                    <div class="hand-label">Linke Hand</div>
                    <div class="equipped-item" id="left-equipped">Faust</div>
                    <button id="btn-left-light" class="attack-btn light">
                        <span>⚔️</span>
                        <small>Light</small>
                    </button>
                    <button id="btn-left-heavy" class="attack-btn heavy">
                        <span>💥</span>
                        <small>Heavy</small>
                    </button>
                </div>
                
                <!-- MITTE: Utility Buttons -->
                <div id="center-controls">
                    <button id="btn-dodge" class="utility-btn">
                        <span>💨</span>
                        <small>Dodge</small>
                    </button>
                    <button id="btn-weave" class="utility-btn weave hidden">
                        <span>✨</span>
                        <small>WEAVE</small>
                    </button>
                    <button id="btn-block" class="utility-btn">
                        <span>🛡️</span>
                        <small>Block</small>
                    </button>
                </div>
                
                <!-- RECHTE SEITE: Rechte Hand Buttons -->
                <div id="right-hand-controls" class="hand-controls right">
                    <div class="hand-label">Rechte Hand</div>
                    <div class="equipped-item" id="right-equipped">Faust</div>
                    <button id="btn-right-light" class="attack-btn light">
                        <span>⚔️</span>
                        <small>Light</small>
                    </button>
                    <button id="btn-right-heavy" class="attack-btn heavy">
                        <span>💥</span>
                        <small>Heavy</small>
                    </button>
                </div>
                
                <!-- Equipment Quick-Select (Long-Press öffnet) -->
                <div id="equipment-wheel" class="hidden">
                    <div class="wheel-title">Ausrüstung wählen</div>
                    <div class="wheel-items" id="wheel-items">
                        <!-- Wird dynamisch gefüllt -->
                    </div>
                    <button class="wheel-close" onclick="touchCombat.closeEquipmentWheel()">✕</button>
                </div>
                
                <!-- Combo Anzeige -->
                <div id="combo-display" class="hidden">
                    <span id="combo-count">0</span>
                    <span id="combo-name"></span>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', controlsHTML);
    }
    
    setupTouchEvents() {
        // ===== LINKE HAND =====
        // Light Attack Links
        this.setupAttackButton('btn-left-light', 'left', 'light');
        // Heavy Attack Links (Hold für Charge)
        this.setupChargeButton('btn-left-heavy', 'left', 'heavy');
        
        // ===== RECHTE HAND =====
        // Light Attack Rechts
        this.setupAttackButton('btn-right-light', 'right', 'light');
        // Heavy Attack Rechts (Hold für Charge)
        this.setupChargeButton('btn-right-heavy', 'right', 'heavy');
        
        // ===== UTILITY =====
        // Dodge
        document.getElementById('btn-dodge').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.handleDodge();
        });
        
        // Block (Hold)
        const blockBtn = document.getElementById('btn-block');
        blockBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startBlock();
        });
        blockBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.endBlock();
        });
        
        // Weave (wenn beide Hände Zauber haben)
        document.getElementById('btn-weave').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.handleWeave();
        });
        
        // ===== EQUIPMENT WECHSEL (Long Press auf Hand-Label) =====
        ['left', 'right'].forEach(hand => {
            const label = document.querySelector(`#${hand}-hand-controls .hand-label`);
            let longPressTimer;
            
            label.addEventListener('touchstart', (e) => {
                longPressTimer = setTimeout(() => {
                    this.openEquipmentWheel(hand);
                }, 500);
            });
            
            label.addEventListener('touchend', () => {
                clearTimeout(longPressTimer);
            });
            
            label.addEventListener('touchmove', () => {
                clearTimeout(longPressTimer);
            });
        });
        
        // Double-Tap für Parry (irgendwo auf Screen)
        document.addEventListener('touchstart', (e) => {
            if (e.target.closest('#touch-combat-controls')) return;
            
            const now = Date.now();
            if (now - this.lastTapTime < this.doubleTapDelay) {
                this.handleParry();
            }
            this.lastTapTime = now;
        });
    }
    
    setupAttackButton(btnId, hand, type) {
        const btn = document.getElementById(btnId);
        btn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.handleAttack(hand, type);
            btn.classList.add('pressed');
        });
        btn.addEventListener('touchend', () => {
            btn.classList.remove('pressed');
        });
    }
    
    setupChargeButton(btnId, hand, type) {
        const btn = document.getElementById(btnId);
        let chargeStart = 0;
        let chargeInterval;
        
        btn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            chargeStart = Date.now();
            btn.classList.add('charging');
            
            // Visuelles Feedback während Charge
            let chargeLevel = 0;
            chargeInterval = setInterval(() => {
                chargeLevel = Math.min(100, (Date.now() - chargeStart) / 10);
                btn.style.setProperty('--charge-level', chargeLevel + '%');
            }, 50);
        });
        
        btn.addEventListener('touchend', (e) => {
            e.preventDefault();
            clearInterval(chargeInterval);
            const chargeTime = Date.now() - chargeStart;
            btn.classList.remove('charging');
            btn.style.setProperty('--charge-level', '0%');
            
            // Charged Heavy = mehr Schaden
            const isCharged = chargeTime > 500;
            this.handleAttack(hand, type, isCharged);
        });
    }
    
    handleAttack(hand, type, charged = false) {
        const result = this.cs.executeAttack(hand, type);
        
        if (result.success) {
            // Schaden berechnen (Charged = 1.5x)
            const finalDamage = charged ? Math.floor(result.damage * 1.5) : result.damage;
            
            // Visuelles Feedback
            this.showDamageNumber(finalDamage, result.element);
            this.vibrateDevice(type === 'heavy' ? 100 : 30);
            
            // Combo tracking
            this.addToCombo(hand, type);
            
            // Animation trigger
            if (window.characterAnimation) {
                window.characterAnimation.playAttack(hand, type);
            }
            
            console.log(`[Combat] ${hand} ${type}${charged ? ' (CHARGED)' : ''}: ${finalDamage} ${result.element || ''} damage`);
        } else {
            // Cooldown Feedback
            if (result.reason === 'cooldown') {
                this.showCooldownFeedback(hand);
            }
        }
    }
    
    handleDodge() {
        // i-Frames: 200ms
        this.vibrateDevice(20);
        console.log('[Combat] Dodge! i-Frames active');
        
        // Visual feedback
        document.getElementById('btn-dodge').classList.add('active');
        setTimeout(() => {
            document.getElementById('btn-dodge').classList.remove('active');
        }, 200);
    }
    
    startBlock() {
        const result = this.cs.executeBlock();
        if (result.success) {
            document.getElementById('btn-block').classList.add('blocking');
            console.log(`[Combat] Block START (${result.type}, value: ${result.blockValue})`);
        }
    }
    
    endBlock() {
        document.getElementById('btn-block').classList.remove('blocking');
        console.log('[Combat] Block END');
    }
    
    handleParry() {
        const result = this.cs.executeParry();
        this.vibrateDevice(50);
        console.log(`[Combat] PARRY! Window: ${result.parryWindow}ms`);
        
        // Show parry indicator
        this.showParryIndicator();
    }
    
    handleWeave() {
        const result = this.cs.executeWeave();
        
        if (result.success) {
            this.showWeaveAnimation(result.weave);
            this.vibrateDevice(200);
            console.log(`[Combat] WEAVE: ${result.weave.name}! ${result.weave.damage} damage, effect: ${result.weave.effect}`);
        } else {
            this.showMessage(result.message || 'Weave nicht möglich!');
        }
    }
    
    // ===== EQUIPMENT =====
    
    openEquipmentWheel(hand) {
        this.activeHand = hand;
        const wheel = document.getElementById('equipment-wheel');
        const itemsContainer = document.getElementById('wheel-items');
        
        // Hole verfügbare Items (aus Inventory)
        const availableItems = this.getAvailableEquipment(hand);
        
        itemsContainer.innerHTML = availableItems.map(item => `
            <button class="wheel-item" data-item="${item.id}" onclick="touchCombat.equipItem('${item.id}')">
                <span class="item-icon">${item.icon}</span>
                <span class="item-name">${item.name}</span>
                <span class="item-type">${item.type}</span>
            </button>
        `).join('');
        
        wheel.classList.remove('hidden');
        this.vibrateDevice(30);
    }
    
    closeEquipmentWheel() {
        document.getElementById('equipment-wheel').classList.add('hidden');
        this.activeHand = null;
    }
    
    equipItem(itemId) {
        if (!this.activeHand) return;
        
        const result = this.cs.equipItem(this.activeHand, itemId);
        
        if (result.success) {
            this.updateEquipmentDisplay();
            this.showMessage(result.message);
            this.closeEquipmentWheel();
        }
    }
    
    getAvailableEquipment(hand) {
        // TODO: Aus echtem Inventory laden
        // Für jetzt: Hardcoded Liste
        const items = [
            { id: 'fist', name: 'Faust', icon: '👊', type: 'melee' },
            { id: 'sword', name: 'Schwert', icon: '⚔️', type: 'melee' },
            { id: 'dagger', name: 'Dolch', icon: '🗡️', type: 'melee' },
            { id: 'fireball', name: 'Feuerball', icon: '🔥', type: 'spell' },
            { id: 'icebolt', name: 'Eisblitz', icon: '❄️', type: 'spell' },
            { id: 'lightning', name: 'Blitz', icon: '⚡', type: 'spell' }
        ];
        
        // Schild nur rechte Hand
        if (hand === 'right') {
            items.push({ id: 'shield', name: 'Schild', icon: '🛡️', type: 'shield' });
        }
        
        return items;
    }
    
    updateEquipmentDisplay() {
        const status = this.cs.getEquipmentStatus();
        
        document.getElementById('left-equipped').textContent = status.leftHand;
        document.getElementById('right-equipped').textContent = status.rightHand;
        
        // Weave Button zeigen wenn beide Hände Zauber haben
        const weaveBtn = document.getElementById('btn-weave');
        if (status.canWeave) {
            weaveBtn.classList.remove('hidden');
        } else {
            weaveBtn.classList.add('hidden');
        }
        
        // Zweihänder: Disable andere Hand
        if (status.twoHanded) {
            document.getElementById('left-equipped').textContent = status.twoHanded;
            document.getElementById('right-equipped').textContent = '(Zweihänder)';
        }
    }
    
    // ===== COMBO SYSTEM =====
    
    comboBuffer = [];
    comboTimeout = null;
    
    addToCombo(hand, type) {
        this.comboBuffer.push(`${hand}_${type}`);
        
        clearTimeout(this.comboTimeout);
        this.comboTimeout = setTimeout(() => {
            this.evaluateCombo();
            this.comboBuffer = [];
        }, 1500);
        
        // Update Combo Display
        document.getElementById('combo-display').classList.remove('hidden');
        document.getElementById('combo-count').textContent = this.comboBuffer.length;
    }
    
    evaluateCombo() {
        if (this.comboBuffer.length < 2) {
            document.getElementById('combo-display').classList.add('hidden');
            return;
        }
        
        // Vereinfache zu light/heavy
        const simplified = this.comboBuffer.map(c => c.split('_')[1]);
        const combo = this.cs.executeCombo(simplified);
        
        if (combo) {
            document.getElementById('combo-name').textContent = combo.name;
            this.showComboAnimation(combo);
        }
        
        setTimeout(() => {
            document.getElementById('combo-display').classList.add('hidden');
        }, 2000);
    }
    
    // ===== UI FEEDBACK =====
    
    showDamageNumber(damage, element) {
        const colors = {
            fire: '#FF4444',
            ice: '#44AAFF',
            lightning: '#FFFF44',
            null: '#FFFFFF'
        };
        
        const dmg = document.createElement('div');
        dmg.className = 'floating-damage';
        dmg.textContent = damage;
        dmg.style.color = colors[element] || colors[null];
        dmg.style.left = `${Math.random() * 40 + 30}%`;
        dmg.style.top = '40%';
        document.body.appendChild(dmg);
        setTimeout(() => dmg.remove(), 1000);
    }
    
    showCooldownFeedback(hand) {
        const side = hand === 'left' ? 'left-hand-controls' : 'right-hand-controls';
        const controls = document.getElementById(side);
        controls.classList.add('on-cooldown');
        setTimeout(() => controls.classList.remove('on-cooldown'), 300);
    }
    
    showParryIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'parry-indicator';
        indicator.textContent = 'PARRY!';
        document.body.appendChild(indicator);
        setTimeout(() => indicator.remove(), 500);
    }
    
    showWeaveAnimation(weave) {
        const anim = document.createElement('div');
        anim.className = 'weave-animation';
        anim.innerHTML = `
            <div class="weave-name">${weave.name}</div>
            <div class="weave-damage">${weave.damage} DMG</div>
            <div class="weave-effect">${weave.effect}</div>
        `;
        document.body.appendChild(anim);
        setTimeout(() => anim.remove(), 2000);
    }
    
    showComboAnimation(combo) {
        const anim = document.createElement('div');
        anim.className = 'combo-animation';
        anim.innerHTML = `
            <div class="combo-title">COMBO!</div>
            <div class="combo-combo-name">${combo.name}</div>
            <div class="combo-multiplier">x${combo.multiplier}</div>
        `;
        document.body.appendChild(anim);
        this.vibrateDevice(100);
        setTimeout(() => anim.remove(), 1500);
    }
    
    showMessage(text) {
        const msg = document.createElement('div');
        msg.className = 'combat-message';
        msg.textContent = text;
        document.body.appendChild(msg);
        setTimeout(() => msg.remove(), 2000);
    }
    
    vibrateDevice(duration) {
        if (navigator.vibrate) {
            navigator.vibrate(duration);
        }
    }
}

// CSS für Touch Controls
const touchCombatCSS = `
#touch-combat-controls {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 180px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 10px;
    pointer-events: none;
    z-index: 5000;
}

.hand-controls {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    pointer-events: auto;
}

.hand-controls.left { align-items: flex-start; }
.hand-controls.right { align-items: flex-end; }

.hand-label {
    color: #4CAF50;
    font-size: 12px;
    font-weight: bold;
    padding: 5px 10px;
    background: rgba(0,0,0,0.7);
    border-radius: 5px;
    cursor: pointer;
}

.equipped-item {
    color: #FFD700;
    font-size: 11px;
    background: rgba(0,0,0,0.5);
    padding: 3px 8px;
    border-radius: 3px;
}

.attack-btn {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.7);
    border: 3px solid #4CAF50;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    transition: all 0.1s;
    pointer-events: auto;
}

.attack-btn.heavy {
    border-color: #FF4444;
    position: relative;
    overflow: hidden;
}

.attack-btn.heavy::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: var(--charge-level, 0%);
    height: 100%;
    background: rgba(255, 68, 68, 0.3);
    transition: width 0.05s;
}

.attack-btn.charging {
    animation: pulse 0.3s infinite;
    box-shadow: 0 0 20px #FF4444;
}

.attack-btn.pressed {
    transform: scale(0.9);
    background: rgba(76, 175, 80, 0.5);
}

.attack-btn small {
    font-size: 10px;
    margin-top: 2px;
}

#center-controls {
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: auto;
}

.utility-btn {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.7);
    border: 2px solid #00BCD4;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.utility-btn.weave {
    border-color: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    background: linear-gradient(135deg, rgba(255,107,107,0.3), rgba(78,205,196,0.3));
}

.utility-btn.blocking {
    background: rgba(255, 215, 0, 0.5);
    box-shadow: 0 0 15px #FFD700;
}

.utility-btn.active {
    background: rgba(0, 188, 212, 0.5);
}

.on-cooldown {
    opacity: 0.5;
}

#equipment-wheel {
    position: fixed;
    bottom: 200px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.95);
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #4CAF50;
    z-index: 6000;
    pointer-events: auto;
}

.wheel-title {
    color: #4CAF50;
    text-align: center;
    margin-bottom: 15px;
    font-weight: bold;
}

.wheel-items {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.wheel-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    background: rgba(255,255,255,0.1);
    border: 1px solid #4CAF50;
    border-radius: 10px;
    color: white;
}

.wheel-item .item-icon { font-size: 24px; }
.wheel-item .item-name { font-size: 12px; margin-top: 5px; }
.wheel-item .item-type { font-size: 10px; color: #888; }

.wheel-close {
    position: absolute;
    top: 5px;
    right: 10px;
    background: none;
    border: none;
    color: #FF4444;
    font-size: 20px;
}

#combo-display {
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.8);
    padding: 10px 20px;
    border-radius: 10px;
    border: 2px solid #FFD700;
    color: #FFD700;
    font-weight: bold;
    z-index: 5500;
}

#combo-count { font-size: 24px; }
#combo-name { font-size: 14px; margin-left: 10px; }

.floating-damage {
    position: fixed;
    font-size: 36px;
    font-weight: bold;
    text-shadow: 2px 2px 4px black;
    animation: floatUp 1s ease-out forwards;
    pointer-events: none;
    z-index: 6000;
}

.parry-indicator {
    position: fixed;
    top: 30%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 32px;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 0 0 10px #FFD700;
    animation: flash 0.5s ease-out;
    pointer-events: none;
}

.weave-animation, .combo-animation {
    position: fixed;
    top: 25%;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    padding: 20px 40px;
    border-radius: 15px;
    animation: popIn 0.3s ease-out;
    pointer-events: none;
    z-index: 6000;
}

.weave-animation {
    background: linear-gradient(135deg, rgba(255,107,107,0.9), rgba(78,205,196,0.9));
}

.combo-animation {
    background: linear-gradient(135deg, rgba(255,215,0,0.9), rgba(255,165,0,0.9));
}

.weave-name, .combo-title { font-size: 24px; font-weight: bold; color: white; }
.weave-damage, .combo-multiplier { font-size: 18px; color: white; margin-top: 5px; }
.weave-effect, .combo-combo-name { font-size: 14px; color: rgba(255,255,255,0.8); }

.combat-message {
    position: fixed;
    bottom: 220px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.8);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    animation: fadeInOut 2s ease-out;
    pointer-events: none;
}

@keyframes floatUp {
    0% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(-100px); }
}

@keyframes flash {
    0%, 100% { opacity: 1; transform: translateX(-50%) scale(1); }
    50% { opacity: 0.5; transform: translateX(-50%) scale(1.2); }
}

@keyframes popIn {
    0% { opacity: 0; transform: translateX(-50%) scale(0.5); }
    100% { opacity: 1; transform: translateX(-50%) scale(1); }
}

@keyframes fadeInOut {
    0% { opacity: 0; }
    20% { opacity: 1; }
    80% { opacity: 1; }
    100% { opacity: 0; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.hidden { display: none !important; }
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = touchCombatCSS;
document.head.appendChild(style);

// Global instance
window.touchCombat = null;

// Initialize when ready
document.addEventListener('DOMContentLoaded', () => {
    if ('ontouchstart' in window && window.commandSystem) {
        window.touchCombat = new TouchCombatControls(window.commandSystem);
        console.log('[TouchCombat] Initialized with equipment-based combat');
    }
});
```

---

# BLOCK 8: ABSCHLUSS & CHECKLISTE

## 📋 NACH DER IMPLEMENTIERUNG - ALLES TESTEN!

### 1. Backend starten:
```bash
cd C:\Najika_World\backend
python najika_server.py
```

### 2. API-Endpoints testen (im Browser oder curl):
```
✅ http://localhost:8000/api/status
✅ http://localhost:8000/api/chaos/status
✅ http://localhost:8000/api/chaos/check_event
✅ http://localhost:8000/api/najika/status
✅ http://localhost:8000/api/file/list?path=/
✅ http://localhost:8000/api/training/status
✅ http://localhost:8000/api/security/status
```

### 3. Frontend testen:
```
1. Öffne http://localhost:8000/ im Browser
2. F12 → Console → sollte zeigen:
   "[Najika] ✓ Command System"
   "[Najika] ✓ Chaos Event UI"
   "[Najika] All systems initialized!"
3. Chaos Meter rechts oben sichtbar?
4. Nach 30 Sekunden eventuell Event?
5. Terminal-Module wechselbar (1-4 Keys)?
```

### 4. Combat testen (Desktop):
```
LMB → Light Attack (rechte Hand)
R → Heavy Attack (rechte Hand)
RMB (Hold) → Block
Space → Dodge
Q+E → Weave (wenn beide Hände Zauber)
```

### 5. Mobile APK testen:
```
1. Build APK (existierendes Build-Script nutzen)
2. Installiere auf Android
3. Linke Hand Buttons links sichtbar?
4. Rechte Hand Buttons rechts sichtbar?
5. Long-Press auf "Linke Hand" → Equipment Wheel?
6. Weave Button erscheint wenn beide Hände Zauber haben?
```

### 6. KI/Najika testen:
```
POST http://localhost:8000/api/chat
Body: {"message": "Hallo Najika!"}
→ Sollte Megumin-Style Antwort geben

POST http://localhost:8000/api/najika/command
Body: {"input": "zeig mir die dateien", "authorized": true}
→ Sollte "dir" ausführen und Ergebnis zeigen
```

---

## ⚠️ WICHTIGE HINWEISE FÜR DAS LOKALE CLAUDE CODE CLI

1. **Arbeite in kleinen Schritten!** 
   - Ein BLOCK nach dem anderen
   - Nach jedem Block: Server neu starten und testen

2. **Backup VORHER machen:**
   ```powershell
   xcopy C:\Najika_World C:\Najika_World_Backup /E /I /Y
   ```

3. **Bei Fehlern:**
   - Console-Log prüfen (F12 im Browser)
   - Python-Fehler im Terminal lesen
   - NIEMALS blind weitermachen

4. **Existierende Dateien:**
   - NICHT komplett überschreiben
   - NUR die angegebenen Teile ergänzen/ersetzen
   - Bei Unsicherheit: Frag nach!

5. **Encoding:**
   - Alle Python-Dateien: UTF-8
   - Alle JS-Dateien: UTF-8
   - PowerShell-Befehle: Vorsicht mit Umlauten!

---

## 📊 ZUSAMMENFASSUNG DER ÄNDERUNGEN

| Datei | Änderung |
|-------|----------|
| `najika_server.py` | +6 API Endpoints, +ChaosEngine Klasse, +PC Orchestrator |
| `chaos_event_ui.js` | NEU - Komplettes Event-UI |
| `chaos_events.css` | NEU - Event Styling |
| `command_system.js` | +Equipment-basiertes Combat |
| `touch_combat.js` | NEU/ERSETZT - Mit linker Hand Button |
| `najika_pc_orchestrator.py` | NEU - Natural Language → Commands |
| `index.html` | +Script-Tags, +CSS-Links |

---

## 🎯 PRIORITÄTEN

**MUSS funktionieren:**
1. ✅ Server startet ohne Fehler
2. ✅ Frontend lädt im Browser
3. ✅ Chat mit Najika funktioniert
4. ✅ Combat-System reagiert auf Input
5. ✅ Mobile Touch Controls sichtbar

**SOLLTE funktionieren:**
1. Chaos Events triggern
2. PC Orchestrator versteht Befehle
3. Weave-System funktioniert
4. Equipment-Wechsel funktioniert

**KANN später:**
1. Voice Integration
2. Training System
3. Advanced Combos
4. 3D Entity Spawning bei Events

---

**VIEL ERFOLG!** 🚀

Wenn Probleme auftreten: Lies die Error-Messages genau und frage nach!
Najika sagt: "Gemeinsam schaffen wir das, Kuja! EXPLOSION!!! ✨"

## 5.1 Script-Tags hinzufügen

Öffne `C:\Najika_World\digivice\index.html` und füge VOR `</body>` hinzu:

```html
<!-- ============================================ -->
<!-- TERMINAL MODULES -->
<!-- ============================================ -->
<script src="js/terminal_modules.js"></script>
<script src="js/code_editor.js"></script>
<script src="js/secure_messenger.js"></script>
<script src="js/system_monitor.js"></script>
<script src="js/file_manager.js"></script>
<script src="js/voice_call.js"></script>

<!-- ============================================ -->
<!-- CHAOS EVENT SYSTEM -->
<!-- ============================================ -->
<script src="js/chaos_event_ui.js"></script>
<script src="js/oregon.js"></script>

<!-- ============================================ -->
<!-- COMBAT SYSTEM -->
<!-- ============================================ -->
<script src="js/command_system.js"></script>
<script src="js/battle_core.js"></script>
<script src="js/battle_api.js"></script>

<!-- ============================================ -->
<!-- TOUCH CONTROLS (Mobile) -->
<!-- ============================================ -->
<script src="js/touch_combat.js"></script>

<!-- ============================================ -->
<!-- WORLD SYSTEM -->
<!-- ============================================ -->
<script src="js/terrain_generator.js"></script>
<script src="js/biome_system.js"></script>
<script src="js/vegetation_system.js"></script>
<script src="js/region_streaming.js"></script>
<script src="js/lod_manager.js"></script>
<script src="js/asset_loader.js"></script>
<script src="js/dungeon_generator.js"></script>

<!-- ============================================ -->
<!-- INIT ALL SYSTEMS -->
<!-- ============================================ -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    console.log('[Najika] Initializing all systems...');
    
    // Command System
    if (typeof CommandSystem !== 'undefined') {
        window.commandSystem = new CommandSystem();
        console.log('[Najika] ✓ Command System');
    }
    
    // Chaos Events
    if (typeof ChaosEventUI !== 'undefined') {
        window.chaosEventUI = new ChaosEventUI();
        console.log('[Najika] ✓ Chaos Event UI');
    }
    
    // Touch Controls (nur wenn Mobile)
    if ('ontouchstart' in window && typeof TouchCombatControls !== 'undefined') {
        window.touchCombat = new TouchCombatControls(window.commandSystem);
        console.log('[Najika] ✓ Touch Combat Controls');
    }
    
    // Combat Input (Desktop)
    if (typeof CombatInputHandler !== 'undefined') {
        window.combatInput = new CombatInputHandler(window.commandSystem);
        console.log('[Najika] ✓ Combat Input Handler');
    }
    
    console.log('[Najika] All systems initialized!');
});
</script>
```

## 5.2 CSS-Links hinzufügen (im `<head>`)

```html
<!-- Terminal Module Styles -->
<link rel="stylesheet" href="static/css/terminal_modules.css">
<link rel="stylesheet" href="static/css/code_editor.css">
<link rel="stylesheet" href="static/css/secure_messenger.css">
<link rel="stylesheet" href="static/css/system_monitor.css">
<link rel="stylesheet" href="static/css/file_manager.css">

<!-- Chaos Events -->
<link rel="stylesheet" href="static/css/chaos_events.css">

<!-- Combat UI -->
<link rel="stylesheet" href="static/css/combat_ui.css">
```

---

# 📋 CHECKLISTE NACH DER IMPLEMENTIERUNG

## Backend testen:
```bash
cd C:\Najika_World\backend
python najika_server.py
```

Dann im Browser testen:
- `http://localhost:5000/api/chaos/check_event` → sollte JSON zurückgeben
- `http://localhost:5000/api/chaos/status` → sollte chaos_level zeigen
- `http://localhost:5000/api/file/list?path=/` → sollte Dateien listen

## Frontend testen:
- Öffne `http://localhost:5000/` im Browser
- Console öffnen (F12) → sollte "[Najika] All systems initialized!" zeigen
- Chaos Meter sollte rechts oben sichtbar sein
- Nach 30 Sekunden sollte evtl. ein Event erscheinen

## Mobile APK testen:
- Build die APK mit dem existierenden Build-Script
- Installiere auf Android
- Touch Controls sollten unten rechts erscheinen
- Element-Auswahl durch langes Drücken auf L/R

---

# ⚠️ WICHTIGE HINWEISE

1. **NICHT** die existierenden Dateien komplett überschreiben - nur ergänzen!
2. Backup machen BEVOR du anfängst: `xcopy C:\Najika_World C:\Najika_World_Backup /E /I`
3. Bei Fehlern: Console-Log prüfen (F12 im Browser)
4. Server neu starten nach Backend-Änderungen
5. Browser-Cache leeren nach Frontend-Änderungen (Ctrl+F5)

---

**VIEL ERFOLG!** 🚀

---

# BLOCK 6: NAJIKA KI-INTEGRATION & PC ORCHESTRATOR

## 6.1 Das existiert bereits (aus 10_SERVER_CODE.py):
- `najika_enhanced_personality.py` → Persönlichkeits-System (4 Facetten)
- `najika_living_system.py` → Autonomes Verhalten
- `najika_memory_enhanced.py` → ChromaDB Memory
- `najika_search.py` → Web-Suche
- `najika_tor.py` → Tor Browser Integration
- `najika_security.py` → Alcatraz Security
- `najika_tts_edge.py` → Edge-TTS Voice
- `najika_claude_code.py` → Claude Code Integration

## 6.2 PC Orchestrator erweitern

Die Whitelist in `/api/system/command` ist zu restriktiv. Erweitere sie:

```python
# In najika_server.py - Ersetze die allowed_commands Liste

# ERWEITERTE WHITELIST für PC Orchestration
ALLOWED_COMMANDS = {
    # System Info
    "systeminfo": True,
    "hostname": True,
    "whoami": True,
    "date": True,
    "time": True,
    
    # Dateisystem (READ-ONLY)
    "dir": True,
    "ls": True,
    "pwd": True,
    "cd": True,
    "type": True,  # Windows cat
    "cat": True,   # Linux cat
    "find": True,
    "where": True,
    
    # Prozesse (READ-ONLY)
    "tasklist": True,
    "ps": True,
    "netstat": True,
    
    # Netzwerk (READ-ONLY)
    "ipconfig": True,
    "ifconfig": True,
    "ping": True,
    "nslookup": True,
    
    # Python/Dev
    "python --version": True,
    "python -c": True,  # Kurze Python-Befehle
    "pip list": True,
    "git status": True,
    "git log --oneline -10": True,
    
    # Najika-spezifisch
    "ollama list": True,
    "ollama ps": True,
    
    # Apps öffnen (GEFÄHRLICH - nur mit Authorization)
    "start": "requires_auth",
    "open": "requires_auth",
    "explorer": "requires_auth",
    "notepad": "requires_auth",
    "code": "requires_auth",  # VS Code
    
    # VERBOTEN (niemals erlauben)
    "rm": False,
    "del": False,
    "format": False,
    "shutdown": False,
    "restart": False,
    "taskkill": False,
    "reg": False,
    "regedit": False
}

def is_command_allowed(command, authorized=False):
    """Prüft ob Befehl erlaubt ist"""
    cmd_lower = command.lower().strip()
    
    # Prüfe gegen Whitelist
    for allowed_cmd, permission in ALLOWED_COMMANDS.items():
        if cmd_lower.startswith(allowed_cmd.lower()):
            if permission == True:
                return True
            elif permission == "requires_auth":
                return authorized
            else:
                return False
    
    # Prüfe gegen Blacklist (Sicherheit!)
    dangerous_patterns = ['rm -rf', 'del /s', 'format', 'shutdown', '>', '>>', '|', '&', ';']
    for pattern in dangerous_patterns:
        if pattern in cmd_lower:
            return False
    
    return False  # Default: Nicht erlaubt
```

## 6.3 Natural Language PC Control (Hacker-Modus)

Erstelle `backend/najika_pc_orchestrator.py`:

```python
"""
NAJIKA PC ORCHESTRATOR
Natürliche Sprache → System-Befehle
"""

import subprocess
import os
import json
import re

class NajikaPCOrchestrator:
    def __init__(self):
        self.command_mappings = {
            # Dateien
            "zeig mir die dateien": "dir",
            "liste dateien": "dir",
            "was ist in diesem ordner": "dir",
            "öffne ordner": "explorer .",
            
            # System
            "welche programme laufen": "tasklist",
            "zeig prozesse": "tasklist",
            "wie viel speicher": "systeminfo | findstr Memory",
            "system info": "systeminfo",
            
            # Netzwerk
            "meine ip": "ipconfig",
            "netzwerk status": "netstat -an",
            "ping google": "ping -n 4 google.com",
            
            # Entwicklung
            "git status": "git status",
            "welche python version": "python --version",
            "installierte pakete": "pip list",
            
            # Ollama/KI
            "welche modelle habe ich": "ollama list",
            "läuft ollama": "ollama ps",
            
            # Apps öffnen
            "öffne notepad": "start notepad",
            "öffne browser": "start chrome",
            "öffne vs code": "start code",
            "öffne explorer": "explorer",
            "öffne terminal": "start cmd"
        }
        
        self.intent_patterns = [
            # Datei-Operationen
            (r"(zeig|liste|was ist in).*(datei|ordner|verzeichnis)", "dir"),
            (r"öffne ordner (.+)", "explorer {0}"),
            
            # System
            (r"(welche|liste).*(programme|prozesse|apps)", "tasklist"),
            (r"(system|computer).*(info|status)", "systeminfo"),
            (r"(speicher|ram|memory)", "systeminfo | findstr Memory"),
            
            # Netzwerk
            (r"(meine|lokale).*(ip|adresse)", "ipconfig"),
            (r"ping (.+)", "ping -n 4 {0}"),
            
            # Suche
            (r"such.* datei.* (.+)", 'dir /s /b "*{0}*"'),
            (r"find.* (.+)", 'dir /s /b "*{0}*"')
        ]
    
    def parse_natural_language(self, text):
        """Konvertiert natürliche Sprache zu System-Befehl"""
        text_lower = text.lower().strip()
        
        # Direkte Mappings
        for phrase, command in self.command_mappings.items():
            if phrase in text_lower:
                return {
                    "understood": True,
                    "command": command,
                    "confidence": 0.95,
                    "explanation": f"Ich führe '{command}' aus."
                }
        
        # Regex Patterns
        for pattern, cmd_template in self.intent_patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Ersetze Platzhalter
                command = cmd_template
                for i, group in enumerate(match.groups()):
                    if group:
                        command = command.replace(f"{{{i}}}", group)
                
                return {
                    "understood": True,
                    "command": command,
                    "confidence": 0.8,
                    "explanation": f"Ich verstehe das als '{command}'."
                }
        
        return {
            "understood": False,
            "command": None,
            "confidence": 0,
            "explanation": "Ich verstehe nicht was du möchtest. Kannst du es anders formulieren?"
        }
    
    def execute_safe(self, command, authorized=False):
        """Führt Befehl sicher aus"""
        if not is_command_allowed(command, authorized):
            return {
                "success": False,
                "error": "Befehl nicht erlaubt",
                "output": ""
            }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='cp850',  # Windows Codepage
                errors='replace'
            )
            
            return {
                "success": True,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout nach 30 Sekunden",
                "output": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": ""
            }
    
    def process_request(self, user_input, authorized=False):
        """Hauptfunktion: User Input → Ausführung → Ergebnis"""
        # 1. Parse natürliche Sprache
        parsed = self.parse_natural_language(user_input)
        
        if not parsed["understood"]:
            return {
                "success": False,
                "najika_response": parsed["explanation"],
                "command_executed": None,
                "output": None
            }
        
        # 2. Führe Befehl aus
        result = self.execute_safe(parsed["command"], authorized)
        
        # 3. Generiere Najika-Antwort
        if result["success"]:
            najika_response = f"{parsed['explanation']}\n\nErgebnis:\n```\n{result['output'][:2000]}\n```"
        else:
            najika_response = f"Hmm, das hat nicht geklappt... {result['error']}"
        
        return {
            "success": result["success"],
            "najika_response": najika_response,
            "command_executed": parsed["command"],
            "output": result["output"],
            "error": result.get("error")
        }

# Globale Instanz
PC_ORCHESTRATOR = NajikaPCOrchestrator()
```

## 6.4 API Endpoint für Natural Language Control

Füge zu `najika_server.py` hinzu:

```python
# Import am Anfang
from najika_pc_orchestrator import PC_ORCHESTRATOR

# Neuer Endpoint
@app.route('/api/najika/command', methods=['POST'])
def najika_natural_command():
    """Natural Language → PC Command"""
    data = request.json
    user_input = data.get('input', '')
    authorized = data.get('authorized', False)
    
    result = PC_ORCHESTRATOR.process_request(user_input, authorized)
    
    # Log für Lernen
    log("INFO", f"PC Command: '{user_input}' → {result.get('command_executed')}", "ORCHESTRATOR")
    
    return jsonify(result)
```

## 6.5 Frontend Integration (Terminal Modul)

In `terminal_modules.js` oder `code_editor.js`, füge Natural Language Input hinzu:

```javascript
// Natural Language Command Input
async function executeNaturalCommand(userInput) {
    try {
        const response = await fetch('/api/najika/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                input: userInput,
                authorized: window.isOwnerAuthorized || false
            })
        });
        
        const result = await response.json();
        
        // Zeige Najika's Antwort
        displayNajikaResponse(result.najika_response);
        
        // Zeige Command Output im Terminal
        if (result.output) {
            appendToTerminal(result.output);
        }
        
        return result;
    } catch (error) {
        console.error('[Terminal] Natural command failed:', error);
        displayNajikaResponse("Ups! Da ist was schiefgelaufen...");
    }
}

// Chat-Input kann auch System-Befehle sein
function handleChatInput(input) {
    // Check ob es ein System-Befehl sein könnte
    const systemKeywords = ['zeig', 'öffne', 'liste', 'such', 'ping', 'system', 'datei', 'ordner'];
    const isSystemCommand = systemKeywords.some(kw => input.toLowerCase().includes(kw));
    
    if (isSystemCommand) {
        // Frage Najika ob sie den Befehl ausführen soll
        showConfirmDialog(
            `Soll ich "${input}" auf deinem PC ausführen?`,
            () => executeNaturalCommand(input),
            () => sendToChat(input)  // Normaler Chat
        );
    } else {
        sendToChat(input);
    }
}
```

## 6.6 Najika Personality in allen Responses

Stelle sicher dass ALLE API-Responses die Najika-Persönlichkeit nutzen:

```python
# In najika_server.py - Helper Funktion

def najika_format_response(data, mood="neutral"):
    """Formatiert Response mit Najika-Persönlichkeit"""
    
    # Mood-basierte Prefixe
    prefixes = {
        "excited": ["EXPLOSION!!! ", "*hüpft aufgeregt* ", "Kuja! Schau! "],
        "happy": ["*strahlt* ", "Yay! ", "*kichert* "],
        "neutral": ["", "Also... ", "Hmm, "],
        "thinking": ["*denkt nach* ", "*Shiro-Modus* ", "Interessant... "],
        "worried": ["*schaut besorgt* ", "Uhm... ", "Kuja... "],
        "angry": ["*funkelt wütend* ", "HEY! ", "Das gefällt mir nicht! "]
    }
    
    # Mood-basierte Suffixe
    suffixes = {
        "excited": [" ✨", " 🎆", " *macht Siegespose*"],
        "happy": [" 💕", " *lächelt*", ""],
        "neutral": ["", "", ""],
        "thinking": [" 🤔", " *tippt an Kinn*", ""],
        "worried": [" 😟", " *zieht an Ärmel*", ""],
        "angry": [" 😤", " *stampft mit Fuß*", " EXPLOSION-bereit!"]
    }
    
    import random
    prefix = random.choice(prefixes.get(mood, prefixes["neutral"]))
    suffix = random.choice(suffixes.get(mood, suffixes["neutral"]))
    
    if isinstance(data, str):
        return f"{prefix}{data}{suffix}"
    elif isinstance(data, dict) and "message" in data:
        data["message"] = f"{prefix}{data['message']}{suffix}"
        return data
    else:
        return data
```

---

# BLOCK 7: MOBILE APK - LINKE HAND BUTTON HINZUFÜGEN
