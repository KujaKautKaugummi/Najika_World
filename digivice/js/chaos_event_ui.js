// =============================================================================
// CHAOS EVENT UI - Konosuba x Oregon Trail
// =============================================================================

// API Base URL - Backend auf Port 8000
const CHAOS_API_BASE = window.API_BASE_URL || 'http://localhost:8000';

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
            const response = await fetch(`${CHAOS_API_BASE}/api/chaos/check_event`);
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
                    <span class="event-category">${event.category || 'Event'}</span>
                </div>

                <p class="event-description">${event.description}</p>

                <div class="najika-reaction">
                    <div class="najika-portrait">
                        <div class="najika-avatar">🎀</div>
                    </div>
                    <div class="najika-speech">
                        <p>"${najikaIntro || 'Mr.K! Was machen wir?'}"</p>
                    </div>
                </div>

                <div class="event-options">
                    ${this.renderOptions(event.choices || event.options || [])}
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
            const response = await fetch(`${CHAOS_API_BASE}/api/chaos/execute_choice`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    event_id: this.activeEvent.id,
                    choice_index: choiceIndex
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
                ${(result.consequences || []).map(c => `<span class="consequence-badge">${c}</span>`).join('')}
            </div>

            <div class="najika-final-reaction">
                <div class="najika-avatar">🎀</div>
                <p>"${result.najika_reaction || 'Interessant...'}"</p>
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

// =============================================================================
// OREGON TRAIL EVENT UI - Separate Journey System
// =============================================================================

class OregonTrailUI {
    constructor() {
        // Player ID (should be passed from game state)
        this.playerId = 1;

        // Current Journey
        this.currentJourney = null;
        this.currentEvent = null;

        // UI State
        this.uiVisible = false;
        this.eventActive = false;

        // API Base URL
        this.apiBase = (window.API_BASE_URL || 'http://127.0.0.1:8000') + '/api/oregon';

        console.log('[OregonTrailUI] Initialized');
    }

    // ===== UI CREATION =====

    createUI() {
        // Check if already exists
        if (document.getElementById('oregon-trail-ui')) {
            return document.getElementById('oregon-trail-ui');
        }

        // Create main container
        const container = document.createElement('div');
        container.id = 'oregon-trail-ui';
        container.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            width: 450px;
            max-height: 80vh;
            background: rgba(20, 20, 30, 0.95);
            border: 3px solid #ff6b35;
            border-radius: 12px;
            padding: 20px;
            color: white;
            font-family: 'Courier New', monospace;
            z-index: 9999;
            display: none;
            overflow-y: auto;
            box-shadow: 0 8px 32px rgba(255, 107, 53, 0.4);
        `;

        container.innerHTML = `
            <div class="oregon-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h2 style="margin: 0; color: #ff6b35; font-size: 18px;">🚗 Oregon Trail</h2>
                <button id="oregon-close" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0;">×</button>
            </div>

            <!-- Journey Status -->
            <div id="oregon-journey-status" style="background: rgba(255, 107, 53, 0.1); border: 2px solid #ff6b35; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h3 style="margin: 0 0 10px 0; color: #ff6b35; font-size: 14px;">📊 Journey Status</h3>
                <div id="journey-stats" style="font-size: 12px; line-height: 1.6;">
                    <div>📍 Location: <span id="stat-location">-</span></div>
                    <div>🛣️ Distance: <span id="stat-distance">0</span> / 2000 miles</div>
                    <div>📅 Days: <span id="stat-days">0</span></div>
                    <div>❤️ Health: <span id="stat-health">100</span>%</div>
                    <div>😊 Morale: <span id="stat-morale">100</span>%</div>
                    <div>🍖 Food: <span id="stat-food">200</span> lbs</div>
                    <div>💧 Water: <span id="stat-water">50</span> gal</div>
                    <div>💰 Money: <span id="stat-money">100</span>$</div>
                    <div>👥 Party: <span id="stat-party">4</span> alive</div>
                </div>
            </div>

            <!-- Progress Bar -->
            <div style="background: rgba(0, 0, 0, 0.3); border-radius: 8px; height: 20px; margin-bottom: 15px; overflow: hidden;">
                <div id="progress-bar" style="background: linear-gradient(90deg, #ff6b35, #ffa500); height: 100%; width: 0%; transition: width 0.5s;"></div>
            </div>

            <!-- Control Buttons -->
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <button id="oregon-trigger-event" style="flex: 1; background: #ff6b35; border: none; color: white; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 12px;">
                    🎲 Trigger Event
                </button>
                <button id="oregon-add-progress" style="flex: 1; background: #00aaff; border: none; color: white; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 12px;">
                    ➡️ Travel +10mi
                </button>
            </div>

            <!-- Current Event -->
            <div id="oregon-current-event" style="display: none; background: rgba(255, 107, 53, 0.15); border: 2px solid #ff6b35; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h3 style="margin: 0 0 10px 0; color: #ff6b35; font-size: 14px;" id="event-title">Event Title</h3>
                <p style="margin: 0 0 10px 0; font-size: 12px; line-height: 1.5;" id="event-description">Event description...</p>
                <p style="margin: 0 0 15px 0; font-size: 11px; font-style: italic; color: #ffa500;" id="event-najika-quote">"Najika quote..."</p>

                <!-- Choices -->
                <div id="event-choices" style="display: flex; flex-direction: column; gap: 8px;">
                    <!-- Choices will be inserted here -->
                </div>
            </div>

            <!-- Event Outcome -->
            <div id="oregon-event-outcome" style="display: none; background: rgba(0, 170, 255, 0.1); border: 2px solid #00aaff; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h3 style="margin: 0 0 10px 0; color: #00aaff; font-size: 14px;">📝 Outcome</h3>
                <p style="margin: 0 0 10px 0; font-size: 12px;" id="outcome-text">Outcome text...</p>
                <div id="outcome-impact" style="font-size: 11px; line-height: 1.6; color: #aaa;">
                    <!-- Impact will be shown here -->
                </div>
                <button id="outcome-continue" style="background: #00aaff; border: none; color: white; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-top: 10px; font-size: 11px;">
                    Continue
                </button>
            </div>

            <!-- Event History -->
            <div style="margin-top: 15px;">
                <h3 style="margin: 0 0 10px 0; color: #ff6b35; font-size: 14px;">📜 Recent Events</h3>
                <div id="event-history" style="max-height: 200px; overflow-y: auto; font-size: 11px; line-height: 1.6;">
                    <!-- Event history will be shown here -->
                </div>
            </div>
        `;

        document.body.appendChild(container);

        // Bind Events
        this.bindEvents();

        return container;
    }

    bindEvents() {
        // Close Button
        document.getElementById('oregon-close').addEventListener('click', () => {
            this.hideUI();
        });

        // Trigger Event
        document.getElementById('oregon-trigger-event').addEventListener('click', () => {
            this.triggerEvent();
        });

        // Add Progress
        document.getElementById('oregon-add-progress').addEventListener('click', () => {
            this.addProgress();
        });

        // Continue from Outcome
        document.getElementById('outcome-continue').addEventListener('click', () => {
            this.hideOutcome();
        });
    }

    // ===== UI VISIBILITY =====

    showUI() {
        if (!document.getElementById('oregon-trail-ui')) {
            this.createUI();
        }

        document.getElementById('oregon-trail-ui').style.display = 'block';
        this.uiVisible = true;
        this.loadJourneyStatus();
    }

    hideUI() {
        const ui = document.getElementById('oregon-trail-ui');
        if (ui) {
            ui.style.display = 'none';
        }
        this.uiVisible = false;
    }

    toggleUI() {
        if (this.uiVisible) {
            this.hideUI();
        } else {
            this.showUI();
        }
    }

    // ===== API CALLS =====

    async loadJourneyStatus() {
        try {
            const response = await fetch(`${this.apiBase}/journey/status?player_id=${this.playerId}`);
            const data = await response.json();

            if (data.journey) {
                this.currentJourney = data.journey;
                this.updateJourneyDisplay();
                this.loadEventHistory();
            }

        } catch (error) {
            console.error('[OregonTrailUI] Failed to load journey:', error);
        }
    }

    async triggerEvent() {
        try {
            const response = await fetch(`${this.apiBase}/trigger`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    location: 'any',
                    player_class: null
                })
            });

            const data = await response.json();

            if (data.triggered && data.event) {
                this.currentEvent = data.event;
                this.currentEvent.event_id = data.event_id;
                this.displayEvent();
            } else {
                console.log('[OregonTrailUI] No event triggered');
            }

        } catch (error) {
            console.error('[OregonTrailUI] Failed to trigger event:', error);
        }
    }

    async executeChoice(choiceIndex) {
        if (!this.currentEvent || !this.currentEvent.event_id) {
            console.error('[OregonTrailUI] No active event');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/choice`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    event_id: this.currentEvent.event_id,
                    choice_index: choiceIndex
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showOutcome(data);
                this.currentJourney = data.journey;
                this.updateJourneyDisplay();
                this.loadEventHistory();
            }

        } catch (error) {
            console.error('[OregonTrailUI] Failed to execute choice:', error);
        }
    }

    async addProgress() {
        try {
            const response = await fetch(`${this.apiBase}/progress`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    distance: 10,
                    days: 1
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentJourney = data.journey;
                this.updateJourneyDisplay();

                if (data.completed) {
                    alert('🎉 Congratulations! You reached Oregon!');
                }
            }

        } catch (error) {
            console.error('[OregonTrailUI] Failed to add progress:', error);
        }
    }

    async loadEventHistory() {
        try {
            const response = await fetch(`${this.apiBase}/events?player_id=${this.playerId}&limit=5`);
            const data = await response.json();

            if (data.events) {
                this.displayEventHistory(data.events);
            }

        } catch (error) {
            console.error('[OregonTrailUI] Failed to load event history:', error);
        }
    }

    // ===== DISPLAY METHODS =====

    updateJourneyDisplay() {
        if (!this.currentJourney) return;

        const j = this.currentJourney;

        const els = {
            location: document.getElementById('stat-location'),
            distance: document.getElementById('stat-distance'),
            days: document.getElementById('stat-days'),
            health: document.getElementById('stat-health'),
            morale: document.getElementById('stat-morale'),
            food: document.getElementById('stat-food'),
            water: document.getElementById('stat-water'),
            money: document.getElementById('stat-money'),
            party: document.getElementById('stat-party')
        };

        if (els.location) els.location.textContent = j.current_location || 'Unknown';
        if (els.distance) els.distance.textContent = j.distance_traveled || 0;
        if (els.days) els.days.textContent = j.days_elapsed || 0;
        if (els.health) els.health.textContent = Math.round(j.party_health || 100);
        if (els.morale) els.morale.textContent = Math.round(j.party_morale || 100);
        if (els.food) els.food.textContent = j.food || 0;
        if (els.water) els.water.textContent = j.water || 0;
        if (els.money) els.money.textContent = j.money || 0;
        if (els.party) els.party.textContent = j.alive_members || 0;

        // Update Progress Bar
        const progress = ((j.distance_traveled || 0) / 2000) * 100;
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
    }

    displayEvent() {
        if (!this.currentEvent) return;

        const eventDiv = document.getElementById('oregon-current-event');
        if (!eventDiv) return;

        eventDiv.style.display = 'block';

        const titleEl = document.getElementById('event-title');
        const descEl = document.getElementById('event-description');
        const quoteEl = document.getElementById('event-najika-quote');

        if (titleEl) titleEl.textContent = this.currentEvent.title || 'Unknown Event';
        if (descEl) descEl.textContent = this.currentEvent.description || '';
        if (quoteEl) quoteEl.textContent = `"${this.currentEvent.najika_quote || ''}"`;

        // Display Choices
        const choicesDiv = document.getElementById('event-choices');
        if (!choicesDiv) return;

        choicesDiv.innerHTML = '';

        const choices = this.currentEvent.choices || [];
        choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.style.cssText = `
                background: rgba(255, 107, 53, 0.2);
                border: 2px solid #ff6b35;
                color: white;
                padding: 10px;
                border-radius: 6px;
                cursor: pointer;
                text-align: left;
                font-size: 11px;
                transition: all 0.2s;
            `;
            button.textContent = `${String.fromCharCode(65 + index)}) ${choice}`;
            button.addEventListener('click', () => this.executeChoice(index));
            button.addEventListener('mouseenter', () => {
                button.style.background = 'rgba(255, 107, 53, 0.4)';
                button.style.transform = 'translateX(5px)';
            });
            button.addEventListener('mouseleave', () => {
                button.style.background = 'rgba(255, 107, 53, 0.2)';
                button.style.transform = 'translateX(0)';
            });

            choicesDiv.appendChild(button);
        });
    }

    showOutcome(data) {
        // Hide Event
        const eventDiv = document.getElementById('oregon-current-event');
        if (eventDiv) eventDiv.style.display = 'none';

        // Show Outcome
        const outcomeDiv = document.getElementById('oregon-event-outcome');
        if (!outcomeDiv) return;

        outcomeDiv.style.display = 'block';

        const outcomeText = document.getElementById('outcome-text');
        if (outcomeText) {
            outcomeText.textContent = `${data.choice}\n\n${data.outcome}`;
        }

        // Display Impact
        const impactDiv = document.getElementById('outcome-impact');
        if (impactDiv && data.impact) {
            impactDiv.innerHTML = '';

            const impacts = [];
            for (const [key, value] of Object.entries(data.impact)) {
                const sign = value >= 0 ? '+' : '';
                const color = value >= 0 ? '#4CAF50' : '#ff4444';
                impacts.push(`<div style="color: ${color};">${key}: ${sign}${value}</div>`);
            }
            impactDiv.innerHTML = impacts.join('');
        }
    }

    hideOutcome() {
        const outcomeDiv = document.getElementById('oregon-event-outcome');
        if (outcomeDiv) {
            outcomeDiv.style.display = 'none';
        }
        this.currentEvent = null;
    }

    displayEventHistory(events) {
        const historyDiv = document.getElementById('event-history');
        if (!historyDiv) return;

        historyDiv.innerHTML = '';

        if (events.length === 0) {
            historyDiv.innerHTML = '<div style="color: #888;">No events yet...</div>';
            return;
        }

        events.forEach(event => {
            const item = document.createElement('div');
            item.style.cssText = `
                background: rgba(255, 107, 53, 0.1);
                border-left: 3px solid #ff6b35;
                padding: 8px;
                margin-bottom: 8px;
                border-radius: 4px;
            `;
            item.innerHTML = `
                <div style="font-weight: bold; color: #ff6b35;">${event.event_name}</div>
                <div style="color: #aaa; font-size: 10px; margin-top: 4px;">
                    ${event.player_choice || 'No choice made'} → ${event.outcome || 'Pending'}
                </div>
            `;
            historyDiv.appendChild(item);
        });
    }

    // ===== EXTERNAL INTEGRATION =====

    startNewJourney() {
        fetch(`${this.apiBase}/journey/start?player_id=${this.playerId}`)
            .then(res => res.json())
            .then(data => {
                console.log('[OregonTrailUI] New Journey Started:', data);
                this.loadJourneyStatus();
            })
            .catch(error => {
                console.error('[OregonTrailUI] Error starting journey:', error);
            });
    }
}

// Initialize Oregon Trail UI
window.oregonTrailUI = new OregonTrailUI();
