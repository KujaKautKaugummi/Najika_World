/**
 * NAJIKA WORLD - Slime Companion UI
 * ==================================
 * V-Pet Style UI fuer Slime Begleiter
 *
 * Basiert auf: Digimon V-Pet + Dragon Quest Monsters + Fortnite Begleiter
 *
 * Erstellt: 2026-02-01
 * Autor: OPUS-2 (VS Code Extension)
 */

class SlimeCompanionUI {
    constructor() {
        this.activeSlime = null;
        this.allSlimes = [];
        this.slimeTypes = [];
        this.updateInterval = null;
        this.isOpen = false;

        // Slime Farben (vom Backend)
        this.slimeColors = {
            'moos_schleim': '#4CAF50',
            'frost_schleim': '#81D4FA',
            'wasser_schleim': '#2196F3',
            'blitz_schleim': '#9C27B0',
            'gift_schleim': '#1B5E20',
            'magma_schleim': '#FF5722',
            'sand_schleim': '#FFD54F',
            'kristall_schleim': '#E0E0E0',
            'goetter_schleim': 'rainbow'
        };

        // Stage Namen
        this.stageNames = {
            1: 'Ei',
            2: 'Baby',
            3: 'Kind',
            4: 'Reif',
            5: 'Champion',
            6: 'Ultimativ'
        };

        this.init();
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================

    async init() {
        console.log('[SlimeUI] Initialisiere Slime Companion UI...');

        // UI erstellen
        this.createUI();
        this.createWidget();
        this.bindEvents();

        // Daten laden
        await this.loadSlimeTypes();
        await this.refreshSlimes();

        // Periodisches Update (alle 30 Sekunden)
        this.updateInterval = setInterval(() => this.periodicUpdate(), 30000);

        console.log('[SlimeUI] Slime Companion UI initialisiert');
    }

    // =========================================================================
    // UI CREATION
    // =========================================================================

    createUI() {
        // Haupt-Panel
        const panel = document.createElement('div');
        panel.id = 'slime-companion-panel';
        panel.className = 'slime-panel hidden';
        panel.innerHTML = `
            <div class="slime-panel-header">
                <h2>Schleim-Begleiter</h2>
                <button class="slime-close-btn" onclick="slimeUI.close()">&times;</button>
            </div>

            <div class="slime-panel-tabs">
                <button class="slime-tab active" data-tab="active">Aktiv</button>
                <button class="slime-tab" data-tab="collection">Sammlung</button>
                <button class="slime-tab" data-tab="create">Neu</button>
            </div>

            <!-- ACTIVE TAB -->
            <div class="slime-tab-content active" id="slime-tab-active">
                <div id="slime-active-container">
                    <div class="slime-no-active">
                        <p>Kein aktiver Begleiter</p>
                        <button class="slime-btn" onclick="slimeUI.switchTab('collection')">
                            Waehle einen Slime
                        </button>
                    </div>
                </div>
            </div>

            <!-- COLLECTION TAB -->
            <div class="slime-tab-content" id="slime-tab-collection">
                <div id="slime-collection-list"></div>
            </div>

            <!-- CREATE TAB -->
            <div class="slime-tab-content" id="slime-tab-create">
                <div class="slime-create-form">
                    <h3>Neues Schleim-Ei</h3>
                    <div class="slime-form-group">
                        <label>Slime-Typ:</label>
                        <select id="slime-create-type"></select>
                    </div>
                    <div class="slime-form-group">
                        <label>Name (optional):</label>
                        <input type="text" id="slime-create-name" placeholder="Gib deinem Slime einen Namen">
                    </div>
                    <button class="slime-btn slime-btn-primary" onclick="slimeUI.createSlime()">
                        Ei erstellen
                    </button>
                </div>
                <div class="slime-type-preview" id="slime-type-preview"></div>
            </div>
        `;
        document.body.appendChild(panel);

        // Styles hinzufuegen
        this.addStyles();
    }

    createWidget() {
        // Mini-Widget fuer HUD (immer sichtbar wenn Slime aktiv)
        const widget = document.createElement('div');
        widget.id = 'slime-widget';
        widget.className = 'slime-widget hidden';
        widget.innerHTML = `
            <div class="slime-widget-avatar" id="slime-widget-avatar"></div>
            <div class="slime-widget-info">
                <div class="slime-widget-name" id="slime-widget-name">-</div>
                <div class="slime-widget-hearts">
                    <span class="slime-hearts-hunger" id="slime-widget-hunger"></span>
                    <span class="slime-hearts-strength" id="slime-widget-strength"></span>
                </div>
            </div>
            <div class="slime-widget-status" id="slime-widget-status"></div>
        `;
        widget.onclick = () => this.open();
        document.body.appendChild(widget);
    }

    addStyles() {
        if (document.getElementById('slime-companion-styles')) return;

        const style = document.createElement('style');
        style.id = 'slime-companion-styles';
        style.textContent = `
            /* ============================================ */
            /* SLIME COMPANION PANEL */
            /* ============================================ */

            .slime-panel {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 450px;
                max-height: 80vh;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 2px solid #4CAF50;
                border-radius: 15px;
                box-shadow: 0 0 30px rgba(76, 175, 80, 0.3);
                z-index: 10000;
                overflow: hidden;
                font-family: 'Segoe UI', sans-serif;
            }

            .slime-panel.hidden {
                display: none;
            }

            .slime-panel-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: rgba(76, 175, 80, 0.2);
                border-bottom: 1px solid #4CAF50;
            }

            .slime-panel-header h2 {
                margin: 0;
                color: #4CAF50;
                font-size: 1.3em;
            }

            .slime-close-btn {
                background: none;
                border: none;
                color: #ff6b6b;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                line-height: 1;
            }

            .slime-close-btn:hover {
                color: #ff4757;
            }

            /* TABS */
            .slime-panel-tabs {
                display: flex;
                background: rgba(0, 0, 0, 0.3);
                border-bottom: 1px solid #333;
            }

            .slime-tab {
                flex: 1;
                padding: 12px;
                background: none;
                border: none;
                color: #888;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s;
            }

            .slime-tab:hover {
                color: #4CAF50;
                background: rgba(76, 175, 80, 0.1);
            }

            .slime-tab.active {
                color: #4CAF50;
                background: rgba(76, 175, 80, 0.2);
                border-bottom: 2px solid #4CAF50;
            }

            .slime-tab-content {
                display: none;
                padding: 20px;
                max-height: 50vh;
                overflow-y: auto;
            }

            .slime-tab-content.active {
                display: block;
            }

            /* ACTIVE SLIME VIEW */
            .slime-active-display {
                text-align: center;
            }

            .slime-avatar-large {
                width: 120px;
                height: 120px;
                margin: 0 auto 15px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 60px;
                animation: slime-bounce 2s infinite;
            }

            @keyframes slime-bounce {
                0%, 100% { transform: translateY(0) scale(1); }
                50% { transform: translateY(-10px) scale(1.05); }
            }

            .slime-name-display {
                font-size: 1.5em;
                color: #fff;
                margin-bottom: 5px;
            }

            .slime-stage-display {
                color: #888;
                font-size: 0.9em;
                margin-bottom: 15px;
            }

            /* HEARTS */
            .slime-hearts-row {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 15px;
            }

            .slime-hearts-group {
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .slime-hearts-group label {
                font-size: 0.8em;
                color: #888;
                margin-bottom: 5px;
            }

            .slime-hearts {
                font-size: 20px;
            }

            .heart-full { color: #ff6b6b; }
            .heart-empty { color: #444; }
            .strength-full { color: #ffd93d; }
            .strength-empty { color: #444; }

            /* CARE BUTTONS */
            .slime-care-buttons {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin: 15px 0;
            }

            .slime-care-btn {
                padding: 12px 8px;
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid #4CAF50;
                border-radius: 8px;
                color: #4CAF50;
                cursor: pointer;
                font-size: 12px;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 5px;
                transition: all 0.3s;
            }

            .slime-care-btn:hover {
                background: rgba(76, 175, 80, 0.4);
                transform: scale(1.05);
            }

            .slime-care-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            .slime-care-btn .icon {
                font-size: 20px;
            }

            /* STATS */
            .slime-stats {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 10px;
                margin: 15px 0;
            }

            .slime-stat-row {
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
                border-bottom: 1px solid #333;
                font-size: 0.9em;
            }

            .slime-stat-row:last-child {
                border-bottom: none;
            }

            .slime-stat-label {
                color: #888;
            }

            .slime-stat-value {
                color: #4CAF50;
            }

            /* BONUSES */
            .slime-bonuses {
                background: rgba(76, 175, 80, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin-top: 15px;
            }

            .slime-bonuses h4 {
                margin: 0 0 10px 0;
                color: #4CAF50;
                font-size: 0.9em;
            }

            .slime-bonus-item {
                display: flex;
                justify-content: space-between;
                padding: 3px 0;
                font-size: 0.85em;
            }

            .slime-bonus-name {
                color: #aaa;
            }

            .slime-bonus-value {
                color: #ffd93d;
            }

            /* EVOLUTION */
            .slime-evolution-ready {
                background: linear-gradient(135deg, #ffd93d 0%, #ff6b6b 100%);
                color: #000;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                text-align: center;
                animation: evolution-glow 1.5s infinite;
            }

            @keyframes evolution-glow {
                0%, 100% { box-shadow: 0 0 10px rgba(255, 217, 61, 0.5); }
                50% { box-shadow: 0 0 25px rgba(255, 107, 107, 0.8); }
            }

            .slime-evolution-ready h4 {
                margin: 0 0 10px 0;
            }

            /* COLLECTION */
            .slime-collection-item {
                display: flex;
                align-items: center;
                padding: 12px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                margin-bottom: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .slime-collection-item:hover {
                background: rgba(76, 175, 80, 0.2);
            }

            .slime-collection-item.active {
                border: 1px solid #4CAF50;
            }

            .slime-collection-avatar {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                margin-right: 12px;
            }

            .slime-collection-info {
                flex: 1;
            }

            .slime-collection-name {
                color: #fff;
                font-weight: bold;
            }

            .slime-collection-stage {
                color: #888;
                font-size: 0.85em;
            }

            .slime-collection-actions {
                display: flex;
                gap: 8px;
            }

            /* CREATE FORM */
            .slime-create-form {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 8px;
            }

            .slime-create-form h3 {
                margin: 0 0 15px 0;
                color: #4CAF50;
            }

            .slime-form-group {
                margin-bottom: 15px;
            }

            .slime-form-group label {
                display: block;
                color: #888;
                margin-bottom: 5px;
                font-size: 0.9em;
            }

            .slime-form-group select,
            .slime-form-group input {
                width: 100%;
                padding: 10px;
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid #444;
                border-radius: 5px;
                color: #fff;
                font-size: 14px;
            }

            .slime-form-group select:focus,
            .slime-form-group input:focus {
                border-color: #4CAF50;
                outline: none;
            }

            .slime-type-preview {
                margin-top: 20px;
                padding: 15px;
                background: rgba(76, 175, 80, 0.1);
                border-radius: 8px;
            }

            .slime-type-preview h4 {
                margin: 0 0 10px 0;
                color: #4CAF50;
            }

            /* BUTTONS */
            .slime-btn {
                padding: 10px 20px;
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid #4CAF50;
                border-radius: 5px;
                color: #4CAF50;
                cursor: pointer;
                transition: all 0.3s;
            }

            .slime-btn:hover {
                background: rgba(76, 175, 80, 0.4);
            }

            .slime-btn-primary {
                background: #4CAF50;
                color: #000;
            }

            .slime-btn-primary:hover {
                background: #66BB6A;
            }

            .slime-btn-small {
                padding: 5px 10px;
                font-size: 12px;
            }

            /* WIDGET */
            .slime-widget {
                position: fixed;
                bottom: 20px;
                left: 20px;
                display: flex;
                align-items: center;
                padding: 10px 15px;
                background: rgba(26, 26, 46, 0.95);
                border: 2px solid #4CAF50;
                border-radius: 30px;
                cursor: pointer;
                z-index: 9000;
                transition: all 0.3s;
            }

            .slime-widget.hidden {
                display: none;
            }

            .slime-widget:hover {
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
            }

            .slime-widget-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                margin-right: 10px;
            }

            .slime-widget-info {
                margin-right: 10px;
            }

            .slime-widget-name {
                color: #fff;
                font-weight: bold;
                font-size: 14px;
            }

            .slime-widget-hearts {
                display: flex;
                gap: 5px;
                font-size: 12px;
            }

            .slime-hearts-hunger { color: #ff6b6b; }
            .slime-hearts-strength { color: #ffd93d; }

            .slime-widget-status {
                font-size: 16px;
            }

            /* NO ACTIVE */
            .slime-no-active {
                text-align: center;
                padding: 40px;
                color: #888;
            }

            .slime-no-active p {
                margin-bottom: 20px;
            }

            /* SLEEPING */
            .slime-sleeping {
                opacity: 0.7;
            }

            .slime-sleeping .slime-avatar-large {
                animation: slime-sleep 3s infinite;
            }

            @keyframes slime-sleep {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(0.95); }
            }

            /* MESSAGE */
            .slime-message {
                position: fixed;
                bottom: 80px;
                left: 20px;
                padding: 10px 20px;
                background: rgba(76, 175, 80, 0.9);
                color: #000;
                border-radius: 20px;
                z-index: 10001;
                animation: slime-message-fade 3s forwards;
            }

            @keyframes slime-message-fade {
                0% { opacity: 0; transform: translateY(20px); }
                10% { opacity: 1; transform: translateY(0); }
                80% { opacity: 1; }
                100% { opacity: 0; }
            }

            /* DEAD SLIME */
            .slime-dead {
                filter: grayscale(100%);
            }

            .slime-dead .slime-avatar-large {
                animation: none;
            }
        `;
        document.head.appendChild(style);
    }

    // =========================================================================
    // EVENT BINDING
    // =========================================================================

    bindEvents() {
        // Tab switching
        document.querySelectorAll('.slime-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                this.switchTab(tab.dataset.tab);
            });
        });

        // Create type preview
        const typeSelect = document.getElementById('slime-create-type');
        if (typeSelect) {
            typeSelect.addEventListener('change', () => this.updateTypePreview());
        }

        // Keyboard shortcut (Alt+S)
        document.addEventListener('keydown', (e) => {
            if (e.altKey && e.key.toLowerCase() === 's') {
                e.preventDefault();
                this.toggle();
            }
        });
    }

    // =========================================================================
    // DATA LOADING
    // =========================================================================

    async loadSlimeTypes() {
        try {
            const response = await fetch('/api/slime/types');
            if (!response.ok) throw new Error('Failed to load slime types');

            const data = await response.json();
            this.slimeTypes = data.types || [];

            // Populate create dropdown
            const typeSelect = document.getElementById('slime-create-type');
            if (typeSelect) {
                typeSelect.innerHTML = this.slimeTypes.map(type =>
                    `<option value="${type.id}">${type.name} - ${type.description}</option>`
                ).join('');
            }

            this.updateTypePreview();
        } catch (error) {
            console.warn('[SlimeUI] Konnte Slime-Typen nicht laden:', error);
            // Fallback types
            this.slimeTypes = [
                { id: 'moos_schleim', name: 'MOOS', description: 'Hilft beim Gaertnern' },
                { id: 'frost_schleim', name: 'FROST', description: 'Haelt Essen frisch' },
                { id: 'wasser_schleim', name: 'WASSER', description: 'Mehr Glueck beim Angeln' },
                { id: 'blitz_schleim', name: 'BLITZ', description: 'Schnellere Bewegung' },
                { id: 'gift_schleim', name: 'GIFT', description: 'Gift-Resistenz' },
                { id: 'magma_schleim', name: 'MAGMA', description: 'Besseres Schmieden' },
                { id: 'sand_schleim', name: 'SAND', description: 'Findet Schaetze' },
                { id: 'kristall_schleim', name: 'KRISTALL', description: 'Leuchtet im Dunkeln' },
                { id: 'goetter_schleim', name: 'GOETTER', description: 'Bonus auf ALLES!' }
            ];
        }
    }

    async refreshSlimes() {
        try {
            const response = await fetch('/api/slime/all');
            if (!response.ok) throw new Error('Failed to load slimes');

            const data = await response.json();
            this.allSlimes = data.slimes || [];

            // Find active slime
            if (data.active_id) {
                this.activeSlime = this.allSlimes.find(s => s.id === data.active_id) || null;
            } else {
                this.activeSlime = null;
            }

            this.updateUI();
        } catch (error) {
            console.warn('[SlimeUI] Konnte Slimes nicht laden:', error);
        }
    }

    async periodicUpdate() {
        if (!this.activeSlime) return;

        try {
            // Trigger server-side update
            await fetch('/api/slime/update', { method: 'POST' });

            // Refresh data
            await this.refreshSlimes();
        } catch (error) {
            console.warn('[SlimeUI] Periodic update fehlgeschlagen:', error);
        }
    }

    // =========================================================================
    // UI UPDATES
    // =========================================================================

    updateUI() {
        this.updateActiveTab();
        this.updateCollectionTab();
        this.updateWidget();
    }

    updateActiveTab() {
        const container = document.getElementById('slime-active-container');
        if (!container) return;

        if (!this.activeSlime) {
            container.innerHTML = `
                <div class="slime-no-active">
                    <p>Kein aktiver Begleiter</p>
                    <button class="slime-btn" onclick="slimeUI.switchTab('collection')">
                        Waehle einen Slime
                    </button>
                </div>
            `;
            return;
        }

        const slime = this.activeSlime;
        const color = this.slimeColors[slime.slime_type] || '#888';
        const isRainbow = color === 'rainbow';
        const bgStyle = isRainbow
            ? 'background: linear-gradient(45deg, red, orange, yellow, green, blue, purple);'
            : `background: ${color};`;

        const isSleeping = slime.is_sleeping;
        const isDead = !slime.is_alive;

        container.innerHTML = `
            <div class="slime-active-display ${isSleeping ? 'slime-sleeping' : ''} ${isDead ? 'slime-dead' : ''}">
                <div class="slime-avatar-large" style="${bgStyle}">
                    ${this.getSlimeEmoji(slime)}
                </div>

                <div class="slime-name-display">${slime.name}</div>
                <div class="slime-stage-display">
                    ${this.stageNames[slime.stage] || 'Unbekannt'} • Lv.${slime.level}
                    ${slime.plus_value > 0 ? ` • +${slime.plus_value}` : ''}
                    ${isSleeping ? ' • zzZ' : ''}
                    ${isDead ? ' • Tot' : ''}
                </div>

                <div class="slime-hearts-row">
                    <div class="slime-hearts-group">
                        <label>Hunger</label>
                        <div class="slime-hearts">
                            ${this.renderHearts(slime.hunger_hearts, 4, 'heart')}
                        </div>
                    </div>
                    <div class="slime-hearts-group">
                        <label>Energie</label>
                        <div class="slime-hearts">
                            ${this.renderHearts(slime.strength_hearts, 4, 'strength')}
                        </div>
                    </div>
                </div>

                ${slime.can_evolve ? `
                    <div class="slime-evolution-ready">
                        <h4>Evolution bereit!</h4>
                        <button class="slime-btn slime-btn-primary" onclick="slimeUI.evolve()">
                            Jetzt entwickeln!
                        </button>
                    </div>
                ` : ''}

                ${!isDead ? `
                    <div class="slime-care-buttons">
                        <button class="slime-care-btn" onclick="slimeUI.feed()" ${slime.hunger_hearts >= 4 || isSleeping ? 'disabled' : ''}>
                            <span class="icon">🍖</span>
                            <span>Fuettern</span>
                        </button>
                        <button class="slime-care-btn" onclick="slimeUI.train()" ${slime.strength_hearts < 1 || isSleeping ? 'disabled' : ''}>
                            <span class="icon">💪</span>
                            <span>Training</span>
                        </button>
                        <button class="slime-care-btn" onclick="slimeUI.play()" ${slime.strength_hearts >= 4 || isSleeping ? 'disabled' : ''}>
                            <span class="icon">🎮</span>
                            <span>Spielen</span>
                        </button>
                        <button class="slime-care-btn" onclick="slimeUI.sleep(${isSleeping})">
                            <span class="icon">${isSleeping ? '☀️' : '💤'}</span>
                            <span>${isSleeping ? 'Aufwecken' : 'Schlafen'}</span>
                        </button>
                        <button class="slime-care-btn" onclick="slimeUI.heal()" ${slime.injuries === 0 ? 'disabled' : ''}>
                            <span class="icon">💊</span>
                            <span>Heilen</span>
                        </button>
                        <button class="slime-care-btn" onclick="slimeUI.rename()">
                            <span class="icon">✏️</span>
                            <span>Umbenennen</span>
                        </button>
                    </div>
                ` : ''}

                <div class="slime-stats">
                    <div class="slime-stat-row">
                        <span class="slime-stat-label">Alter</span>
                        <span class="slime-stat-value">${this.formatAge(slime.age_hours)}</span>
                    </div>
                    <div class="slime-stat-row">
                        <span class="slime-stat-label">Effort Hearts</span>
                        <span class="slime-stat-value">${slime.effort_hearts}</span>
                    </div>
                    <div class="slime-stat-row">
                        <span class="slime-stat-label">Care Mistakes</span>
                        <span class="slime-stat-value">${slime.care_mistakes}/10</span>
                    </div>
                    ${slime.battles > 0 ? `
                        <div class="slime-stat-row">
                            <span class="slime-stat-label">Kaempfe</span>
                            <span class="slime-stat-value">${slime.wins}/${slime.battles} (${Math.round(slime.win_rate * 100)}%)</span>
                        </div>
                    ` : ''}
                    ${slime.injuries > 0 ? `
                        <div class="slime-stat-row">
                            <span class="slime-stat-label">Verletzungen</span>
                            <span class="slime-stat-value" style="color: #ff6b6b;">${slime.injuries}/20</span>
                        </div>
                    ` : ''}
                </div>

                ${Object.keys(slime.passive_bonuses || {}).length > 0 ? `
                    <div class="slime-bonuses">
                        <h4>Passive Boni</h4>
                        ${Object.entries(slime.passive_bonuses)
                            .filter(([key]) => key !== 'description')
                            .map(([key, value]) => `
                                <div class="slime-bonus-item">
                                    <span class="slime-bonus-name">${this.formatBonusName(key)}</span>
                                    <span class="slime-bonus-value">+${Math.round(value * 100)}%</span>
                                </div>
                            `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }

    updateCollectionTab() {
        const list = document.getElementById('slime-collection-list');
        if (!list) return;

        if (this.allSlimes.length === 0) {
            list.innerHTML = `
                <div class="slime-no-active">
                    <p>Noch keine Slimes</p>
                    <button class="slime-btn" onclick="slimeUI.switchTab('create')">
                        Erstes Ei erstellen
                    </button>
                </div>
            `;
            return;
        }

        list.innerHTML = this.allSlimes.map(slime => {
            const color = this.slimeColors[slime.slime_type] || '#888';
            const isRainbow = color === 'rainbow';
            const bgStyle = isRainbow
                ? 'background: linear-gradient(45deg, red, orange, yellow, green, blue, purple);'
                : `background: ${color};`;
            const isActive = this.activeSlime && slime.id === this.activeSlime.id;

            return `
                <div class="slime-collection-item ${isActive ? 'active' : ''} ${!slime.is_alive ? 'slime-dead' : ''}"
                     onclick="slimeUI.selectSlime('${slime.id}')">
                    <div class="slime-collection-avatar" style="${bgStyle}">
                        ${this.getSlimeEmoji(slime)}
                    </div>
                    <div class="slime-collection-info">
                        <div class="slime-collection-name">${slime.name}</div>
                        <div class="slime-collection-stage">
                            ${this.stageNames[slime.stage]} • Lv.${slime.level}
                            ${slime.is_sleeping ? ' • zzZ' : ''}
                            ${!slime.is_alive ? ' • Tot' : ''}
                        </div>
                    </div>
                    <div class="slime-collection-actions">
                        ${!isActive && slime.is_alive ? `
                            <button class="slime-btn slime-btn-small" onclick="event.stopPropagation(); slimeUI.activate('${slime.id}')">
                                Aktivieren
                            </button>
                        ` : ''}
                        ${isActive ? '<span style="color: #4CAF50;">Aktiv</span>' : ''}
                    </div>
                </div>
            `;
        }).join('');
    }

    updateWidget() {
        const widget = document.getElementById('slime-widget');
        if (!widget) return;

        if (!this.activeSlime || !this.activeSlime.is_alive) {
            widget.classList.add('hidden');
            return;
        }

        widget.classList.remove('hidden');

        const slime = this.activeSlime;
        const color = this.slimeColors[slime.slime_type] || '#888';
        const isRainbow = color === 'rainbow';
        const bgStyle = isRainbow
            ? 'background: linear-gradient(45deg, red, orange, yellow, green, blue, purple);'
            : `background: ${color};`;

        document.getElementById('slime-widget-avatar').style.cssText = bgStyle;
        document.getElementById('slime-widget-avatar').textContent = this.getSlimeEmoji(slime);
        document.getElementById('slime-widget-name').textContent = slime.name;
        document.getElementById('slime-widget-hunger').textContent = '❤️'.repeat(slime.hunger_hearts);
        document.getElementById('slime-widget-strength').textContent = '⚡'.repeat(slime.strength_hearts);

        // Status icon
        let status = '';
        if (slime.is_sleeping) status = '💤';
        else if (slime.hunger_hearts <= 1) status = '😫';
        else if (slime.can_evolve) status = '✨';
        else if (slime.injuries > 0) status = '🤕';

        document.getElementById('slime-widget-status').textContent = status;
    }

    updateTypePreview() {
        const preview = document.getElementById('slime-type-preview');
        const typeSelect = document.getElementById('slime-create-type');
        if (!preview || !typeSelect) return;

        const selectedType = this.slimeTypes.find(t => t.id === typeSelect.value);
        if (!selectedType) {
            preview.innerHTML = '';
            return;
        }

        const color = this.slimeColors[selectedType.id] || '#888';
        const isRainbow = color === 'rainbow';
        const bgStyle = isRainbow
            ? 'background: linear-gradient(45deg, red, orange, yellow, green, blue, purple);'
            : `background: ${color};`;

        preview.innerHTML = `
            <h4>Vorschau: ${selectedType.name}</h4>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 60px; height: 60px; ${bgStyle} border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px;">
                    🥚
                </div>
                <div>
                    <p style="margin: 0; color: #fff;">${selectedType.description || ''}</p>
                    ${selectedType.passive_bonuses ? `
                        <p style="margin: 5px 0 0 0; color: #888; font-size: 0.85em;">
                            ${Object.entries(selectedType.passive_bonuses)
                                .filter(([key]) => key !== 'description')
                                .map(([key, value]) => `${this.formatBonusName(key)}: +${Math.round(value * 100)}%`)
                                .join(', ')}
                        </p>
                    ` : ''}
                </div>
            </div>
        `;
    }

    // =========================================================================
    // HELPER FUNCTIONS
    // =========================================================================

    getSlimeEmoji(slime) {
        if (!slime.is_alive) return '💀';
        if (slime.is_sleeping) return '😴';

        switch(slime.stage) {
            case 1: return '🥚';
            case 2: return '🫧';
            case 3: return '🟢';
            case 4: return '💧';
            case 5: return '⭐';
            case 6: return '👑';
            default: return '🫧';
        }
    }

    renderHearts(current, max, type) {
        let html = '';
        for (let i = 0; i < max; i++) {
            if (i < current) {
                html += type === 'heart' ? '❤️' : '⚡';
            } else {
                html += type === 'heart' ? '🖤' : '⚫';
            }
        }
        return html;
    }

    formatAge(hours) {
        if (hours < 1) return `${Math.round(hours * 60)} Min`;
        if (hours < 24) return `${Math.round(hours)} Std`;
        if (hours < 168) return `${Math.round(hours / 24)} Tage`;
        return `${Math.round(hours / 168)} Wochen`;
    }

    formatBonusName(key) {
        const names = {
            'farming_speed': 'Farming',
            'herb_quality': 'Kraeuter',
            'food_preservation': 'Frische',
            'cold_resistance': 'Kaelte-Schutz',
            'fishing_luck': 'Angel-Glueck',
            'swimming_speed': 'Schwimmen',
            'movement_speed': 'Bewegung',
            'crafting_speed': 'Crafting',
            'poison_immunity': 'Gift-Schutz',
            'stealth': 'Tarnung',
            'smithing_bonus': 'Schmieden',
            'fire_resistance': 'Feuer-Schutz',
            'treasure_find': 'Schaetze',
            'trade_discount': 'Handel',
            'mining_speed': 'Mining',
            'light_radius': 'Licht',
            'all_bonus': 'Alles',
            'luck': 'Glueck'
        };
        return names[key] || key;
    }

    showMessage(text) {
        const msg = document.createElement('div');
        msg.className = 'slime-message';
        msg.textContent = text;
        document.body.appendChild(msg);

        setTimeout(() => msg.remove(), 3000);
    }

    // =========================================================================
    // ACTIONS
    // =========================================================================

    async feed() {
        try {
            const response = await fetch('/api/slime/feed', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const data = await response.json();
            this.showMessage(data.message || 'Gefuettert!');
            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler beim Fuettern');
        }
    }

    async train() {
        try {
            const response = await fetch('/api/slime/train', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const data = await response.json();
            this.showMessage(data.message || 'Trainiert!');
            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler beim Training');
        }
    }

    async play() {
        try {
            const response = await fetch('/api/slime/play', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const data = await response.json();
            this.showMessage(data.message || 'Gespielt!');
            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler beim Spielen');
        }
    }

    async sleep(isCurrentlySleeping) {
        try {
            const response = await fetch('/api/slime/sleep', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ wake: isCurrentlySleeping })
            });

            const data = await response.json();
            this.showMessage(data.message || (isCurrentlySleeping ? 'Aufgewacht!' : 'Schlaeft jetzt!'));
            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler');
        }
    }

    async heal() {
        try {
            const response = await fetch('/api/slime/heal', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const data = await response.json();
            this.showMessage(data.message || 'Geheilt!');
            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler beim Heilen');
        }
    }

    async evolve() {
        try {
            const response = await fetch('/api/slime/evolve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage(`${this.activeSlime.name} hat sich entwickelt!`);
            } else {
                this.showMessage(data.message || 'Evolution fehlgeschlagen');
            }

            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler bei Evolution');
        }
    }

    async rename() {
        const newName = prompt('Neuer Name:', this.activeSlime?.name || '');
        if (!newName || !newName.trim()) return;

        try {
            const response = await fetch('/api/slime/rename', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: newName.trim() })
            });

            const data = await response.json();
            this.showMessage(data.message || 'Umbenannt!');
            await this.refreshSlimes();
        } catch (error) {
            this.showMessage('Fehler beim Umbenennen');
        }
    }

    async activate(slimeId) {
        try {
            const response = await fetch('/api/slime/activate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: slimeId })
            });

            const data = await response.json();
            this.showMessage(data.message || 'Aktiviert!');
            await this.refreshSlimes();
            this.switchTab('active');
        } catch (error) {
            this.showMessage('Fehler beim Aktivieren');
        }
    }

    async createSlime() {
        const typeSelect = document.getElementById('slime-create-type');
        const nameInput = document.getElementById('slime-create-name');

        if (!typeSelect) return;

        const slimeType = typeSelect.value;
        const name = nameInput?.value?.trim() || null;

        try {
            const response = await fetch('/api/slime/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: slimeType, name: name })
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage(data.message || 'Ei erstellt!');
                if (nameInput) nameInput.value = '';
                await this.refreshSlimes();
                this.switchTab('active');
            } else {
                this.showMessage(data.error || 'Fehler beim Erstellen');
            }
        } catch (error) {
            this.showMessage('Fehler beim Erstellen');
        }
    }

    selectSlime(slimeId) {
        // Just show details - actual activation via button
        const slime = this.allSlimes.find(s => s.id === slimeId);
        if (slime && slime.is_alive) {
            this.activate(slimeId);
        }
    }

    // =========================================================================
    // PANEL CONTROL
    // =========================================================================

    switchTab(tabName) {
        document.querySelectorAll('.slime-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        document.querySelectorAll('.slime-tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `slime-tab-${tabName}`);
        });
    }

    open() {
        document.getElementById('slime-companion-panel')?.classList.remove('hidden');
        this.isOpen = true;
        this.refreshSlimes();
    }

    close() {
        document.getElementById('slime-companion-panel')?.classList.add('hidden');
        this.isOpen = false;
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    // =========================================================================
    // CLEANUP
    // =========================================================================

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }

        document.getElementById('slime-companion-panel')?.remove();
        document.getElementById('slime-widget')?.remove();
        document.getElementById('slime-companion-styles')?.remove();
    }
}

// =============================================================================
// GLOBAL INSTANCE
// =============================================================================

let slimeUI = null;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        slimeUI = new SlimeCompanionUI();
    });
} else {
    slimeUI = new SlimeCompanionUI();
}

// Export for console access
window.slimeUI = slimeUI;
console.log('[SlimeUI] Slime Companion UI geladen. Oeffnen mit Alt+S oder slimeUI.open()');
