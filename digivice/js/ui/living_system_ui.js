/**
 * Living System UI - Najika World
 * ================================
 * Zeigt Najikas Lebenszustand an:
 * - Hunger, Energy, Mood, Anger
 * - Self-Care Buttons (Feed, Drink, Sleep)
 * - Activity Status
 * - Proactive Messages
 *
 * API Endpoints (Port 8000 - Flask):
 * - GET /api/living/state
 * - GET /api/living/proactive
 * - GET /api/living/activity/check
 * - POST /api/living/activity/start
 * - POST /api/najika/feed
 * - POST /api/najika/drink
 * - POST /api/najika/sleep
 *
 * Author: Claude Code
 * Date: 2026-02-05
 */

class LivingSystemUI {
    constructor() {
        this.apiBase = 'http://127.0.0.1:8000';
        this.isOpen = false;
        this.state = {
            hunger: 80,
            energy: 70,
            mood: 'normal',
            moodValue: 75,
            anger: 0,
            activity: null
        };
        this.pollInterval = null;

        this.init();
    }

    init() {
        this.createUI();
        this.createMiniBars();
        this.loadState();
        this.startPolling();
        console.log('[OK] Living System UI geladen');
    }

    // ==========================================
    // UI CREATION
    // ==========================================

    createMiniBars() {
        // Mini Status-Bars im HUD (immer sichtbar)
        const miniContainer = document.createElement('div');
        miniContainer.id = 'living-mini-bars';
        miniContainer.innerHTML = `
            <style>
                #living-mini-bars {
                    position: fixed;
                    top: 10px;
                    right: 10px;
                    background: rgba(0, 0, 0, 0.8);
                    border: 1px solid #444;
                    border-radius: 8px;
                    padding: 10px;
                    z-index: 9000;
                    font-family: 'Consolas', monospace;
                    color: #fff;
                    min-width: 180px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                #living-mini-bars:hover {
                    background: rgba(0, 0, 0, 0.95);
                    border-color: #f0a;
                }
                .living-mini-bar {
                    display: flex;
                    align-items: center;
                    margin-bottom: 6px;
                    font-size: 12px;
                }
                .living-mini-bar:last-child {
                    margin-bottom: 0;
                }
                .living-mini-icon {
                    width: 18px;
                    text-align: center;
                    margin-right: 6px;
                }
                .living-mini-label {
                    width: 50px;
                    color: #888;
                }
                .living-mini-track {
                    flex: 1;
                    height: 8px;
                    background: #333;
                    border-radius: 4px;
                    overflow: hidden;
                    margin-right: 6px;
                }
                .living-mini-fill {
                    height: 100%;
                    transition: width 0.5s ease, background 0.3s ease;
                    border-radius: 4px;
                }
                .living-mini-value {
                    width: 35px;
                    text-align: right;
                    font-size: 11px;
                }
                .living-activity {
                    margin-top: 8px;
                    padding-top: 8px;
                    border-top: 1px solid #333;
                    font-size: 11px;
                    color: #f0a;
                }
                .living-click-hint {
                    font-size: 9px;
                    color: #555;
                    text-align: center;
                    margin-top: 6px;
                }
            </style>
            <div class="living-mini-bar">
                <span class="living-mini-icon">🍖</span>
                <span class="living-mini-label">Hunger</span>
                <div class="living-mini-track">
                    <div class="living-mini-fill" id="mini-hunger-fill" style="width: 80%; background: #4a4;"></div>
                </div>
                <span class="living-mini-value" id="mini-hunger-value">80%</span>
            </div>
            <div class="living-mini-bar">
                <span class="living-mini-icon">⚡</span>
                <span class="living-mini-label">Energy</span>
                <div class="living-mini-track">
                    <div class="living-mini-fill" id="mini-energy-fill" style="width: 70%; background: #4af;"></div>
                </div>
                <span class="living-mini-value" id="mini-energy-value">70%</span>
            </div>
            <div class="living-mini-bar">
                <span class="living-mini-icon">😊</span>
                <span class="living-mini-label">Mood</span>
                <div class="living-mini-track">
                    <div class="living-mini-fill" id="mini-mood-fill" style="width: 75%; background: #fa0;"></div>
                </div>
                <span class="living-mini-value" id="mini-mood-value">75%</span>
            </div>
            <div class="living-mini-bar">
                <span class="living-mini-icon">😤</span>
                <span class="living-mini-label">Anger</span>
                <div class="living-mini-track">
                    <div class="living-mini-fill" id="mini-anger-fill" style="width: 0%; background: #f44;"></div>
                </div>
                <span class="living-mini-value" id="mini-anger-value">0%</span>
            </div>
            <div class="living-activity" id="mini-activity" style="display: none;">
                <span id="mini-activity-text">Aktivitaet...</span>
            </div>
            <div class="living-click-hint">Klicke fuer Details</div>
        `;

        miniContainer.addEventListener('click', () => this.toggle());
        document.body.appendChild(miniContainer);
    }

    createUI() {
        // Vollstaendiges Panel (auf Klick oeffnen)
        const container = document.createElement('div');
        container.id = 'living-system-panel';
        container.innerHTML = `
            <style>
                #living-system-panel {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 500px;
                    max-height: 80vh;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    border: 2px solid #f0a;
                    border-radius: 15px;
                    z-index: 10000;
                    display: none;
                    overflow: hidden;
                    box-shadow: 0 0 30px rgba(255, 0, 170, 0.3);
                    font-family: 'Segoe UI', sans-serif;
                    color: #fff;
                }
                #living-system-panel.open {
                    display: block;
                    animation: slideIn 0.3s ease;
                }
                @keyframes slideIn {
                    from { opacity: 0; transform: translate(-50%, -50%) scale(0.9); }
                    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                }
                .living-header {
                    background: linear-gradient(90deg, #f0a 0%, #a0f 100%);
                    padding: 15px 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .living-header h2 {
                    margin: 0;
                    font-size: 20px;
                    font-weight: bold;
                }
                .living-close {
                    background: none;
                    border: none;
                    color: #fff;
                    font-size: 24px;
                    cursor: pointer;
                    padding: 0;
                    line-height: 1;
                }
                .living-content {
                    padding: 20px;
                    overflow-y: auto;
                    max-height: 60vh;
                }
                .living-stat-row {
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                    padding: 10px;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                }
                .living-stat-icon {
                    font-size: 28px;
                    width: 40px;
                    text-align: center;
                }
                .living-stat-info {
                    flex: 1;
                    margin-left: 10px;
                }
                .living-stat-name {
                    font-size: 14px;
                    color: #888;
                    margin-bottom: 4px;
                }
                .living-stat-bar {
                    height: 12px;
                    background: #333;
                    border-radius: 6px;
                    overflow: hidden;
                }
                .living-stat-fill {
                    height: 100%;
                    transition: width 0.5s ease;
                    border-radius: 6px;
                }
                .living-stat-value {
                    width: 50px;
                    text-align: right;
                    font-size: 18px;
                    font-weight: bold;
                }
                .living-actions {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 10px;
                    margin-top: 20px;
                }
                .living-action-btn {
                    background: linear-gradient(135deg, #333 0%, #222 100%);
                    border: 1px solid #555;
                    border-radius: 10px;
                    padding: 15px 10px;
                    color: #fff;
                    cursor: pointer;
                    text-align: center;
                    transition: all 0.2s ease;
                }
                .living-action-btn:hover {
                    background: linear-gradient(135deg, #444 0%, #333 100%);
                    border-color: #f0a;
                    transform: scale(1.02);
                }
                .living-action-btn:active {
                    transform: scale(0.98);
                }
                .living-action-icon {
                    font-size: 28px;
                    display: block;
                    margin-bottom: 5px;
                }
                .living-action-text {
                    font-size: 12px;
                    color: #aaa;
                }
                .living-status {
                    margin-top: 15px;
                    padding: 10px;
                    background: rgba(255, 0, 170, 0.1);
                    border-radius: 8px;
                    font-size: 13px;
                }
                .living-status-label {
                    color: #888;
                }
                .living-warning {
                    color: #f44;
                    animation: pulse 1s infinite;
                }
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
            <div class="living-header">
                <h2>💖 Najika's Zustand</h2>
                <button class="living-close" id="living-close-btn">&times;</button>
            </div>
            <div class="living-content">
                <!-- Hunger -->
                <div class="living-stat-row">
                    <span class="living-stat-icon">🍖</span>
                    <div class="living-stat-info">
                        <div class="living-stat-name">Hunger</div>
                        <div class="living-stat-bar">
                            <div class="living-stat-fill" id="full-hunger-fill" style="width: 80%; background: linear-gradient(90deg, #4a4, #8f8);"></div>
                        </div>
                    </div>
                    <span class="living-stat-value" id="full-hunger-value">80%</span>
                </div>

                <!-- Energy -->
                <div class="living-stat-row">
                    <span class="living-stat-icon">⚡</span>
                    <div class="living-stat-info">
                        <div class="living-stat-name">Energy</div>
                        <div class="living-stat-bar">
                            <div class="living-stat-fill" id="full-energy-fill" style="width: 70%; background: linear-gradient(90deg, #4af, #8ff);"></div>
                        </div>
                    </div>
                    <span class="living-stat-value" id="full-energy-value">70%</span>
                </div>

                <!-- Mood -->
                <div class="living-stat-row">
                    <span class="living-stat-icon" id="mood-emoji">😊</span>
                    <div class="living-stat-info">
                        <div class="living-stat-name">Stimmung (<span id="mood-name">Normal</span>)</div>
                        <div class="living-stat-bar">
                            <div class="living-stat-fill" id="full-mood-fill" style="width: 75%; background: linear-gradient(90deg, #fa0, #ff0);"></div>
                        </div>
                    </div>
                    <span class="living-stat-value" id="full-mood-value">75%</span>
                </div>

                <!-- Anger -->
                <div class="living-stat-row">
                    <span class="living-stat-icon">😤</span>
                    <div class="living-stat-info">
                        <div class="living-stat-name">Wut-Level <span id="anger-warning" class="living-warning" style="display: none;">(GEFAHR!)</span></div>
                        <div class="living-stat-bar">
                            <div class="living-stat-fill" id="full-anger-fill" style="width: 0%; background: linear-gradient(90deg, #f44, #f00);"></div>
                        </div>
                    </div>
                    <span class="living-stat-value" id="full-anger-value">0%</span>
                </div>

                <!-- Action Buttons -->
                <div class="living-actions">
                    <button class="living-action-btn" id="btn-feed">
                        <span class="living-action-icon">🍜</span>
                        <span class="living-action-text">Fuettern</span>
                    </button>
                    <button class="living-action-btn" id="btn-drink">
                        <span class="living-action-icon">🥤</span>
                        <span class="living-action-text">Trinken</span>
                    </button>
                    <button class="living-action-btn" id="btn-sleep">
                        <span class="living-action-icon">😴</span>
                        <span class="living-action-text">Schlafen</span>
                    </button>
                    <button class="living-action-btn" id="btn-play">
                        <span class="living-action-icon">🎮</span>
                        <span class="living-action-text">Spielen</span>
                    </button>
                    <button class="living-action-btn" id="btn-praise">
                        <span class="living-action-icon">💕</span>
                        <span class="living-action-text">Loben</span>
                    </button>
                    <button class="living-action-btn" id="btn-refresh">
                        <span class="living-action-icon">🔄</span>
                        <span class="living-action-text">Aktualisieren</span>
                    </button>
                </div>

                <!-- Current Activity -->
                <div class="living-status" id="activity-status" style="display: none;">
                    <span class="living-status-label">Aktuelle Aktivitaet:</span>
                    <strong id="activity-name">...</strong>
                </div>

                <!-- Proactive Message -->
                <div class="living-status" id="proactive-message" style="display: none;">
                    <span class="living-status-label">Najika sagt:</span>
                    <em id="proactive-text">...</em>
                </div>
            </div>
        `;

        document.body.appendChild(container);
        this.panel = container;

        // Event Listeners
        document.getElementById('living-close-btn').addEventListener('click', () => this.close());
        document.getElementById('btn-feed').addEventListener('click', () => this.doAction('feed'));
        document.getElementById('btn-drink').addEventListener('click', () => this.doAction('drink'));
        document.getElementById('btn-sleep').addEventListener('click', () => this.doAction('sleep'));
        document.getElementById('btn-play').addEventListener('click', () => this.doAction('play'));
        document.getElementById('btn-praise').addEventListener('click', () => this.doAction('praise'));
        document.getElementById('btn-refresh').addEventListener('click', () => this.loadState());

        // ESC to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    // ==========================================
    // TOGGLE / OPEN / CLOSE
    // ==========================================

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.panel.classList.add('open');
        this.isOpen = true;
        this.loadState();
    }

    close() {
        this.panel.classList.remove('open');
        this.isOpen = false;
    }

    // ==========================================
    // DATA LOADING
    // ==========================================

    async loadState() {
        try {
            const response = await fetch(`${this.apiBase}/api/living/state`);
            if (!response.ok) throw new Error('API Error');

            const data = await response.json();

            // Parse state
            this.state.hunger = data.hunger || data.satiation || 80;
            this.state.energy = data.energy || 70;
            this.state.moodValue = data.mood_value || data.happiness || 75;
            this.state.mood = data.mood || 'normal';
            this.state.anger = data.anger || 0;
            this.state.activity = data.current_activity;

            this._apiErrors = 0; // Reset error count on success
            this.updateUI();
            this.checkProactiveMessage();

        } catch (error) {
            this._apiErrors = (this._apiErrors || 0) + 1;
            if (this._apiErrors <= 2) {
                console.warn('[Living UI] Konnte State nicht laden:', error.message);
            }
            if (this._apiErrors >= 3) {
                console.warn('[Living UI] API nicht erreichbar - Polling gestoppt. Nutze Default-Werte.');
                this.stopPolling();
            }
            // Zeige trotzdem Default-Werte
            this.updateUI();
        }
    }

    async checkProactiveMessage() {
        try {
            const response = await fetch(`${this.apiBase}/api/living/proactive`);
            if (!response.ok) return;

            const data = await response.json();

            if (data.should_send && data.message) {
                const msgDiv = document.getElementById('proactive-message');
                const msgText = document.getElementById('proactive-text');
                msgText.textContent = data.message;
                msgDiv.style.display = 'block';

                // Nach 10s ausblenden
                setTimeout(() => {
                    msgDiv.style.display = 'none';
                }, 10000);
            }
        } catch (error) {
            // Ignorieren
        }
    }

    // ==========================================
    // UI UPDATE
    // ==========================================

    updateUI() {
        const { hunger, energy, moodValue, mood, anger, activity } = this.state;

        // Mini-Bars
        this.updateBar('mini-hunger', hunger);
        this.updateBar('mini-energy', energy);
        this.updateBar('mini-mood', moodValue);
        this.updateBar('mini-anger', anger, true);

        // Full Panel Bars
        this.updateBar('full-hunger', hunger);
        this.updateBar('full-energy', energy);
        this.updateBar('full-mood', moodValue);
        this.updateBar('full-anger', anger, true);

        // Mood Emoji & Name
        const moodEmojis = {
            'happy': '😄',
            'excited': '🤩',
            'normal': '😊',
            'tired': '😴',
            'sad': '😢',
            'angry': '😠',
            'scared': '😨',
            'love': '😍'
        };
        const moodEmoji = document.getElementById('mood-emoji');
        const moodName = document.getElementById('mood-name');
        if (moodEmoji) moodEmoji.textContent = moodEmojis[mood] || '😊';
        if (moodName) moodName.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);

        // Anger Warning
        const angerWarning = document.getElementById('anger-warning');
        if (angerWarning) {
            angerWarning.style.display = anger > 50 ? 'inline' : 'none';
        }

        // Activity Status
        const activityDiv = document.getElementById('activity-status');
        const activityName = document.getElementById('activity-name');
        const miniActivity = document.getElementById('mini-activity');
        const miniActivityText = document.getElementById('mini-activity-text');

        if (activity) {
            if (activityDiv) activityDiv.style.display = 'block';
            if (activityName) activityName.textContent = activity;
            if (miniActivity) miniActivity.style.display = 'block';
            if (miniActivityText) miniActivityText.textContent = activity;
        } else {
            if (activityDiv) activityDiv.style.display = 'none';
            if (miniActivity) miniActivity.style.display = 'none';
        }
    }

    updateBar(prefix, value, isAnger = false) {
        const fill = document.getElementById(`${prefix}-fill`);
        const valueEl = document.getElementById(`${prefix}-value`);

        if (fill) {
            fill.style.width = `${Math.min(100, Math.max(0, value))}%`;

            // Farbe basierend auf Wert
            if (!isAnger) {
                if (value > 70) {
                    fill.style.background = fill.id.includes('hunger') ? 'linear-gradient(90deg, #4a4, #8f8)' :
                                            fill.id.includes('energy') ? 'linear-gradient(90deg, #4af, #8ff)' :
                                            'linear-gradient(90deg, #fa0, #ff0)';
                } else if (value > 30) {
                    fill.style.background = '#fa0';
                } else {
                    fill.style.background = '#f44';
                }
            }
        }

        if (valueEl) {
            valueEl.textContent = `${Math.round(value)}%`;
        }
    }

    // ==========================================
    // ACTIONS
    // ==========================================

    async doAction(action) {
        try {
            let endpoint = '';

            switch (action) {
                case 'feed':
                    endpoint = '/api/najika/feed';
                    break;
                case 'drink':
                    endpoint = '/api/najika/drink';
                    break;
                case 'sleep':
                    endpoint = '/api/najika/sleep';
                    break;
                case 'play':
                    endpoint = '/api/living/activity/start';
                    break;
                case 'praise':
                    endpoint = '/api/najika/praise';
                    break;
                default:
                    return;
            }

            const response = await fetch(`${this.apiBase}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action })
            });

            if (response.ok) {
                console.log(`[Living UI] ${action} erfolgreich!`);
                // Reload state after action
                setTimeout(() => this.loadState(), 500);
            }

        } catch (error) {
            console.warn(`[Living UI] ${action} fehlgeschlagen:`, error.message);
        }
    }

    // ==========================================
    // POLLING
    // ==========================================

    startPolling() {
        // Update alle 30 Sekunden
        this.pollInterval = setInterval(() => {
            this.loadState();
        }, 30000);
    }

    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }
}

// ==========================================
// GLOBAL INITIALIZATION
// ==========================================

let livingSystemUI = null;

document.addEventListener('DOMContentLoaded', () => {
    livingSystemUI = new LivingSystemUI();
});

// Falls DOM schon geladen ist
if (document.readyState !== 'loading') {
    livingSystemUI = new LivingSystemUI();
}

// Export fuer andere Module
if (typeof window !== 'undefined') {
    window.LivingSystemUI = LivingSystemUI;
    window.livingSystemUI = livingSystemUI;
}
