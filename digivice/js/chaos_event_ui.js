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
            const response = await fetch('http://localhost:8000/api/chaos/check_event');
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
            const response = await fetch('/api/chaos/execute_choice', {
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
