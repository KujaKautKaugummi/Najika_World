/**
 * NAJIKA WORLD - Echoharp UI
 * ===========================
 * Die wandernde Bardin & Zeugen-System Frontend
 *
 * Inspiriert von: Tiny Tina's Wonderlands
 *
 * WICHTIG: "Echoharp" ist KEIN Name - es ist eine BEZEICHNUNG!
 * Sie ist die Letzte des Ordens der Chronisten aus den Wuesten-Pyramiden.
 *
 * Erstellt: 2026-02-01
 * Autor: OPUS-2 (VS Code Extension)
 */

class EchoharpUI {
    constructor() {
        this.echoharpStatus = null;
        this.witnessItem = null;
        this.currentQuest = null;
        this.stories = [];
        this.playerDeeds = [];
        this.isOpen = false;
        this.spielerId = 'player_default'; // TODO: From game state

        // Stimmungs-Emojis
        this.moodEmojis = {
            'aufgeregt': '🎉',
            'melancholisch': '😢',
            'verrückt': '🤪',
            'geheimnisvoll': '🔮',
            'betrunken': '🍺'
        };

        // Tat-Kategorie Icons
        this.categoryIcons = {
            'kampf': '⚔️',
            'boss': '👹',
            'rettung': '🛡️',
            'entdeckung': '🗺️',
            'quest': '📜',
            'crafting': '🔨',
            'handel': '💰',
            'chaos': '🌀',
            'diebstahl': '🗡️',
            'duell': '🏆'
        };

        this.init();
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================

    async init() {
        console.log('[EchoharpUI] Initialisiere Echoharp UI...');

        this.createUI();
        this.bindEvents();

        // Initial data load
        await this.refreshStatus();

        console.log('[EchoharpUI] Echoharp UI initialisiert');
    }

    // =========================================================================
    // UI CREATION
    // =========================================================================

    createUI() {
        // Haupt-Panel
        const panel = document.createElement('div');
        panel.id = 'echoharp-panel';
        panel.className = 'echoharp-panel hidden';
        panel.innerHTML = `
            <div class="echoharp-header">
                <div class="echoharp-title">
                    <span class="echoharp-icon">🎵</span>
                    <h2>Die Echoharp</h2>
                    <span class="echoharp-subtitle">Klang der Wahrheit</span>
                </div>
                <button class="echoharp-close" onclick="echoharpUI.close()">&times;</button>
            </div>

            <div class="echoharp-tabs">
                <button class="echoharp-tab active" data-tab="bard">Die Bardin</button>
                <button class="echoharp-tab" data-tab="witness">Zeugen-Item</button>
                <button class="echoharp-tab" data-tab="stories">Geschichten</button>
                <button class="echoharp-tab" data-tab="deeds">Meine Taten</button>
            </div>

            <!-- BARD TAB -->
            <div class="echoharp-content active" id="echoharp-tab-bard">
                <div id="echoharp-bard-content">
                    <div class="echoharp-loading">Lade Echoharp Status...</div>
                </div>
            </div>

            <!-- WITNESS ITEM TAB -->
            <div class="echoharp-content" id="echoharp-tab-witness">
                <div id="echoharp-witness-content">
                    <div class="echoharp-loading">Lade Item Status...</div>
                </div>
            </div>

            <!-- STORIES TAB -->
            <div class="echoharp-content" id="echoharp-tab-stories">
                <div id="echoharp-stories-content">
                    <div class="echoharp-loading">Lade Geschichten...</div>
                </div>
            </div>

            <!-- DEEDS TAB -->
            <div class="echoharp-content" id="echoharp-tab-deeds">
                <div id="echoharp-deeds-content">
                    <div class="echoharp-loading">Lade deine Taten...</div>
                </div>
            </div>
        `;
        document.body.appendChild(panel);

        // Encounter Notification (wenn Echoharp in der Naehe)
        const notification = document.createElement('div');
        notification.id = 'echoharp-notification';
        notification.className = 'echoharp-notification hidden';
        notification.innerHTML = `
            <div class="echoharp-notif-icon">🎵</div>
            <div class="echoharp-notif-text">
                <strong>Die Echoharp ist in der Naehe!</strong>
                <span>Klicke um mit ihr zu sprechen</span>
            </div>
        `;
        notification.onclick = () => this.open();
        document.body.appendChild(notification);

        this.addStyles();
    }

    addStyles() {
        if (document.getElementById('echoharp-styles')) return;

        const style = document.createElement('style');
        style.id = 'echoharp-styles';
        style.textContent = `
            /* ============================================ */
            /* ECHOHARP PANEL */
            /* ============================================ */

            .echoharp-panel {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 500px;
                max-height: 85vh;
                background: linear-gradient(135deg, #1a1a2e 0%, #2d1b4e 100%);
                border: 2px solid #9c27b0;
                border-radius: 15px;
                box-shadow: 0 0 40px rgba(156, 39, 176, 0.4);
                z-index: 10000;
                overflow: hidden;
                font-family: 'Segoe UI', sans-serif;
            }

            .echoharp-panel.hidden {
                display: none;
            }

            /* HEADER */
            .echoharp-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(90deg, rgba(156, 39, 176, 0.3) 0%, rgba(103, 58, 183, 0.3) 100%);
                border-bottom: 1px solid #9c27b0;
            }

            .echoharp-title {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .echoharp-icon {
                font-size: 28px;
                animation: echoharp-pulse 2s infinite;
            }

            @keyframes echoharp-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            .echoharp-title h2 {
                margin: 0;
                color: #e1bee7;
                font-size: 1.3em;
            }

            .echoharp-subtitle {
                color: #9c27b0;
                font-size: 0.8em;
                font-style: italic;
            }

            .echoharp-close {
                background: none;
                border: none;
                color: #ff6b6b;
                font-size: 28px;
                cursor: pointer;
            }

            /* TABS */
            .echoharp-tabs {
                display: flex;
                background: rgba(0, 0, 0, 0.4);
                border-bottom: 1px solid #333;
            }

            .echoharp-tab {
                flex: 1;
                padding: 12px 8px;
                background: none;
                border: none;
                color: #888;
                cursor: pointer;
                font-size: 13px;
                transition: all 0.3s;
            }

            .echoharp-tab:hover {
                color: #9c27b0;
                background: rgba(156, 39, 176, 0.1);
            }

            .echoharp-tab.active {
                color: #e1bee7;
                background: rgba(156, 39, 176, 0.2);
                border-bottom: 2px solid #9c27b0;
            }

            .echoharp-content {
                display: none;
                padding: 20px;
                max-height: 55vh;
                overflow-y: auto;
            }

            .echoharp-content.active {
                display: block;
            }

            /* BARD DISPLAY */
            .echoharp-bard-display {
                text-align: center;
            }

            .echoharp-bard-avatar {
                width: 100px;
                height: 100px;
                margin: 0 auto 15px;
                background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 50px;
                box-shadow: 0 0 20px rgba(156, 39, 176, 0.5);
                animation: echoharp-float 3s ease-in-out infinite;
            }

            @keyframes echoharp-float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }

            .echoharp-bard-name {
                font-size: 1.4em;
                color: #e1bee7;
                margin-bottom: 5px;
            }

            .echoharp-bard-location {
                color: #888;
                font-size: 0.9em;
                margin-bottom: 10px;
            }

            .echoharp-bard-mood {
                display: inline-block;
                padding: 5px 15px;
                background: rgba(156, 39, 176, 0.2);
                border: 1px solid #9c27b0;
                border-radius: 20px;
                color: #e1bee7;
                font-size: 0.85em;
                margin-bottom: 15px;
            }

            .echoharp-greeting {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 15px;
                margin: 15px 0;
                color: #ddd;
                font-style: italic;
                line-height: 1.5;
                border-left: 3px solid #9c27b0;
            }

            .echoharp-wildnis-badge {
                display: inline-block;
                padding: 8px 15px;
                background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
                border-radius: 20px;
                color: #000;
                font-weight: bold;
                margin: 10px 0;
            }

            .echoharp-stadt-badge {
                display: inline-block;
                padding: 8px 15px;
                background: linear-gradient(135deg, #ff9800 0%, #ffc107 100%);
                border-radius: 20px;
                color: #000;
                font-weight: bold;
                margin: 10px 0;
            }

            /* QUEST */
            .echoharp-quest-card {
                background: rgba(156, 39, 176, 0.1);
                border: 1px solid #9c27b0;
                border-radius: 10px;
                padding: 15px;
                margin: 15px 0;
            }

            .echoharp-quest-title {
                color: #e1bee7;
                font-size: 1.1em;
                margin-bottom: 10px;
            }

            .echoharp-quest-desc {
                color: #aaa;
                font-size: 0.9em;
                margin-bottom: 15px;
                line-height: 1.4;
            }

            .echoharp-quest-meta {
                display: flex;
                gap: 15px;
                font-size: 0.85em;
            }

            .echoharp-quest-meta span {
                color: #888;
            }

            .echoharp-crazy-factor {
                color: #ff6b6b !important;
            }

            /* WITNESS ITEM */
            .echoharp-witness-display {
                text-align: center;
            }

            .echoharp-crystal {
                width: 80px;
                height: 80px;
                margin: 0 auto 15px;
                background: linear-gradient(135deg, #e1bee7 0%, #9c27b0 50%, #673ab7 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                animation: crystal-glow 2s infinite;
            }

            @keyframes crystal-glow {
                0%, 100% { box-shadow: 0 0 20px rgba(156, 39, 176, 0.5); }
                50% { box-shadow: 0 0 40px rgba(225, 190, 231, 0.8); }
            }

            .echoharp-crystal.active {
                animation: crystal-active 0.5s infinite;
            }

            @keyframes crystal-active {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            .echoharp-crystal.empty {
                filter: grayscale(100%);
                animation: none;
            }

            .echoharp-charges {
                font-size: 1.2em;
                color: #e1bee7;
                margin: 10px 0;
            }

            .echoharp-item-status {
                padding: 10px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                margin: 10px 0;
            }

            .echoharp-item-status.pending {
                background: rgba(255, 193, 7, 0.2);
                border: 1px solid #ffc107;
            }

            .echoharp-activate-btns {
                display: flex;
                gap: 10px;
                justify-content: center;
                margin-top: 15px;
            }

            /* BUTTONS */
            .echoharp-btn {
                padding: 10px 20px;
                background: rgba(156, 39, 176, 0.2);
                border: 1px solid #9c27b0;
                border-radius: 8px;
                color: #e1bee7;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s;
            }

            .echoharp-btn:hover {
                background: rgba(156, 39, 176, 0.4);
                transform: scale(1.05);
            }

            .echoharp-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            .echoharp-btn-primary {
                background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
                color: #fff;
            }

            .echoharp-btn-primary:hover {
                background: linear-gradient(135deg, #ab47bc 0%, #7e57c2 100%);
            }

            /* STORIES */
            .echoharp-story {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 3px solid #9c27b0;
            }

            .echoharp-story-header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }

            .echoharp-story-player {
                color: #e1bee7;
                font-weight: bold;
            }

            .echoharp-story-time {
                color: #666;
                font-size: 0.8em;
            }

            .echoharp-story-text {
                color: #ccc;
                font-style: italic;
                line-height: 1.5;
            }

            /* DEEDS */
            .echoharp-deed {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            }

            .echoharp-deed-header {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 10px;
            }

            .echoharp-deed-category {
                font-size: 24px;
            }

            .echoharp-deed-title {
                color: #e1bee7;
                flex: 1;
            }

            .echoharp-deed-melody {
                color: #9c27b0;
                font-size: 0.85em;
            }

            .echoharp-deed-desc {
                color: #aaa;
                font-size: 0.9em;
                margin-bottom: 10px;
            }

            .echoharp-deed-meta {
                display: flex;
                gap: 15px;
                font-size: 0.8em;
                color: #666;
            }

            /* NO ITEM MESSAGE */
            .echoharp-no-item {
                text-align: center;
                padding: 30px;
                color: #888;
            }

            .echoharp-no-item p {
                margin-bottom: 15px;
            }

            /* NOTIFICATION */
            .echoharp-notification {
                position: fixed;
                bottom: 80px;
                right: 20px;
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 15px 20px;
                background: linear-gradient(135deg, #2d1b4e 0%, #1a1a2e 100%);
                border: 2px solid #9c27b0;
                border-radius: 30px;
                cursor: pointer;
                z-index: 9000;
                animation: echoharp-notif-pulse 2s infinite;
            }

            .echoharp-notification.hidden {
                display: none;
            }

            @keyframes echoharp-notif-pulse {
                0%, 100% { box-shadow: 0 0 10px rgba(156, 39, 176, 0.3); }
                50% { box-shadow: 0 0 25px rgba(156, 39, 176, 0.6); }
            }

            .echoharp-notif-icon {
                font-size: 24px;
                animation: echoharp-pulse 1s infinite;
            }

            .echoharp-notif-text {
                display: flex;
                flex-direction: column;
            }

            .echoharp-notif-text strong {
                color: #e1bee7;
                font-size: 14px;
            }

            .echoharp-notif-text span {
                color: #888;
                font-size: 12px;
            }

            /* LOADING */
            .echoharp-loading {
                text-align: center;
                padding: 30px;
                color: #888;
            }

            /* EMPTY STATE */
            .echoharp-empty {
                text-align: center;
                padding: 30px;
                color: #666;
            }

            /* MESSAGE */
            .echoharp-message {
                position: fixed;
                bottom: 100px;
                left: 50%;
                transform: translateX(-50%);
                padding: 12px 25px;
                background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
                color: #fff;
                border-radius: 25px;
                z-index: 10001;
                animation: echoharp-msg-fade 3s forwards;
            }

            @keyframes echoharp-msg-fade {
                0% { opacity: 0; transform: translateX(-50%) translateY(20px); }
                10% { opacity: 1; transform: translateX(-50%) translateY(0); }
                80% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }

    // =========================================================================
    // EVENT BINDING
    // =========================================================================

    bindEvents() {
        // Tab switching
        document.querySelectorAll('.echoharp-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                this.switchTab(tab.dataset.tab);
            });
        });

        // Keyboard shortcut (Alt+E)
        document.addEventListener('keydown', (e) => {
            if (e.altKey && e.key.toLowerCase() === 'e') {
                e.preventDefault();
                this.toggle();
            }
        });
    }

    // =========================================================================
    // DATA LOADING
    // =========================================================================

    async refreshStatus() {
        try {
            const response = await fetch('/api/echoharp/status');
            if (!response.ok) {
                // Fallback to /api/bard/status
                const bardResponse = await fetch('/api/bard/status');
                if (bardResponse.ok) {
                    this.echoharpStatus = await bardResponse.json();
                }
            } else {
                this.echoharpStatus = await response.json();
            }

            this.updateBardTab();
            this.checkEncounter();
        } catch (error) {
            console.warn('[EchoharpUI] Konnte Status nicht laden:', error);
            // Fallback test data
            this.echoharpStatus = this.getTestStatus();
            this.updateBardTab();
        }
    }

    async refreshWitnessItem() {
        try {
            const response = await fetch(`/api/echoharp/witness-item?spieler_id=${this.spielerId}`);
            if (!response.ok) {
                // Fallback
                const bardResponse = await fetch(`/api/bard/item/status?spieler_id=${this.spielerId}`);
                if (bardResponse.ok) {
                    this.witnessItem = await bardResponse.json();
                }
            } else {
                this.witnessItem = await response.json();
            }
            this.updateWitnessTab();
        } catch (error) {
            console.warn('[EchoharpUI] Konnte Item Status nicht laden:', error);
            this.witnessItem = null;
            this.updateWitnessTab();
        }
    }

    async refreshStories() {
        try {
            const response = await fetch('/api/echoharp/stories?limit=10');
            if (!response.ok) {
                const bardResponse = await fetch('/api/bard/stories?limit=10');
                if (bardResponse.ok) {
                    this.stories = await bardResponse.json();
                }
            } else {
                this.stories = await response.json();
            }
            this.updateStoriesTab();
        } catch (error) {
            console.warn('[EchoharpUI] Konnte Geschichten nicht laden:', error);
            this.stories = [];
            this.updateStoriesTab();
        }
    }

    async refreshDeeds() {
        try {
            const response = await fetch(`/api/echoharp/deeds?spieler_id=${this.spielerId}`);
            if (!response.ok) {
                const bardResponse = await fetch(`/api/bard/player/deeds?spieler_id=${this.spielerId}`);
                if (bardResponse.ok) {
                    this.playerDeeds = await bardResponse.json();
                }
            } else {
                this.playerDeeds = await response.json();
            }
            this.updateDeedsTab();
        } catch (error) {
            console.warn('[EchoharpUI] Konnte Taten nicht laden:', error);
            this.playerDeeds = [];
            this.updateDeedsTab();
        }
    }

    getTestStatus() {
        return {
            bezeichnung: "Echoharp",
            voller_titel: "Echoharp, Klang der Wahrheit",
            ort: "unterwegs",
            region: "Samtmoos-Tiefwald",
            stimmung: "verrückt",
            ist_in_wildnis: true,
            bekannte_geschichten: 42,
            begrüßung: "BWAHAHAHA! *spielt chaotische Toene* Du siehst aus wie jemand der DINGE TUT! Verrueckte Dinge! ICH MAG VERRUECKTE DINGE!"
        };
    }

    // =========================================================================
    // UI UPDATES
    // =========================================================================

    updateBardTab() {
        const container = document.getElementById('echoharp-bard-content');
        if (!container || !this.echoharpStatus) return;

        const status = this.echoharpStatus;
        const moodEmoji = this.moodEmojis[status.stimmung] || '🎵';
        const isWildnis = status.ist_in_wildnis;

        container.innerHTML = `
            <div class="echoharp-bard-display">
                <div class="echoharp-bard-avatar">🎻</div>

                <div class="echoharp-bard-name">${status.voller_titel || 'Echoharp, Klang der Wahrheit'}</div>

                <div class="echoharp-bard-location">
                    📍 ${status.ort === 'unterwegs' ? 'Unterwegs in der Wildnis' : status.ort}
                    ${status.region ? ` (${status.region})` : ''}
                </div>

                <div class="echoharp-bard-mood">
                    ${moodEmoji} ${this.formatMood(status.stimmung)}
                </div>

                ${isWildnis ? `
                    <div class="echoharp-wildnis-badge">
                        🌲 In der Wildnis - Quests verfuegbar!
                    </div>
                ` : `
                    <div class="echoharp-stadt-badge">
                        🏘️ In der Stadt - Geschichten anhoeren
                    </div>
                `}

                <div class="echoharp-greeting">
                    "${status.begrüßung || 'Hallo, Wanderer!'}"
                </div>

                <div style="color: #888; font-size: 0.85em; margin-top: 10px;">
                    📖 ${status.bekannte_geschichten || 0} Geschichten gesammelt
                </div>

                ${isWildnis ? `
                    <button class="echoharp-btn echoharp-btn-primary" onclick="echoharpUI.requestQuest()" style="margin-top: 15px;">
                        📜 Quest anfragen
                    </button>
                ` : `
                    <button class="echoharp-btn" onclick="echoharpUI.switchTab('stories')" style="margin-top: 15px;">
                        📖 Geschichten anhoeren
                    </button>
                `}

                ${this.currentQuest ? this.renderQuest(this.currentQuest) : ''}
            </div>
        `;
    }

    renderQuest(quest) {
        return `
            <div class="echoharp-quest-card">
                <div class="echoharp-quest-title">📜 ${quest.titel}</div>
                <div class="echoharp-quest-desc">${quest.beschreibung}</div>
                <div class="echoharp-quest-meta">
                    <span>Typ: ${quest.typ}</span>
                    <span>Schwierigkeit: ${'⭐'.repeat(quest.schwierigkeit)}</span>
                    <span class="echoharp-crazy-factor">Verruecktheit: ${'🌀'.repeat(Math.min(quest.crazy_faktor, 10))}</span>
                </div>
                <div style="margin-top: 15px; display: flex; gap: 10px;">
                    <button class="echoharp-btn echoharp-btn-primary" onclick="echoharpUI.acceptQuest('${quest.id}')">
                        Annehmen
                    </button>
                    <button class="echoharp-btn" onclick="echoharpUI.declineQuest()">
                        Ablehnen
                    </button>
                </div>
            </div>
        `;
    }

    updateWitnessTab() {
        const container = document.getElementById('echoharp-witness-content');
        if (!container) return;

        if (!this.witnessItem || this.witnessItem.error) {
            container.innerHTML = `
                <div class="echoharp-no-item">
                    <div style="font-size: 50px; margin-bottom: 20px;">💎</div>
                    <p>Du hast keinen <strong>Echokristall der Wahrheit</strong>!</p>
                    <p style="color: #666;">Finde die Echoharp in der Wildnis und schliesse eine Quest ab, um den Kristall zu erhalten.</p>
                    <button class="echoharp-btn" onclick="echoharpUI.switchTab('bard')">
                        Zur Echoharp
                    </button>
                </div>
            `;
            return;
        }

        const item = this.witnessItem;
        const isEmpty = item.aufladungen <= 0;
        const isPending = item.aktiv_vorher;

        container.innerHTML = `
            <div class="echoharp-witness-display">
                <div class="echoharp-crystal ${isEmpty ? 'empty' : ''} ${isPending ? 'active' : ''}">
                    💎
                </div>

                <h3 style="color: #e1bee7; margin: 10px 0;">${item.name}</h3>

                <div class="echoharp-charges">
                    Aufladungen: ${item.aufladungen} ${item.aufladungen > 0 ? '✨' : '💤'}
                </div>

                ${isPending ? `
                    <div class="echoharp-item-status pending">
                        ⚡ Aktiv! Deine NAECHSTE besondere Tat wird bezeugt!
                    </div>
                ` : ''}

                ${item.hat_letzte_tat ? `
                    <div class="echoharp-item-status">
                        📝 Du hast eine unbezeugte Tat! Aktiviere NACHHER um sie zu bezeugen.
                    </div>
                ` : ''}

                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin: 15px 0; text-align: left;">
                    <p style="color: #888; font-size: 0.9em; line-height: 1.5;">
                        ${item.beschreibung}
                    </p>
                </div>

                <div class="echoharp-activate-btns">
                    <button class="echoharp-btn ${isPending ? '' : 'echoharp-btn-primary'}"
                            onclick="echoharpUI.activateBefore()"
                            ${isEmpty || isPending ? 'disabled' : ''}>
                        ⚡ VORHER aktivieren
                    </button>
                    <button class="echoharp-btn ${item.hat_letzte_tat ? 'echoharp-btn-primary' : ''}"
                            onclick="echoharpUI.activateAfter()"
                            ${isEmpty || !item.hat_letzte_tat ? 'disabled' : ''}>
                        📝 NACHHER aktivieren
                    </button>
                </div>
            </div>
        `;
    }

    updateStoriesTab() {
        const container = document.getElementById('echoharp-stories-content');
        if (!container) return;

        if (!this.stories || this.stories.length === 0) {
            container.innerHTML = `
                <div class="echoharp-empty">
                    <p>Noch keine Geschichten erzaehlt...</p>
                    <p style="color: #666;">Wenn Spieler ihre Taten bezeugen lassen, werden sie hier erscheinen!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.stories.map(story => `
            <div class="echoharp-story">
                <div class="echoharp-story-header">
                    <span class="echoharp-story-player">Ueber: ${story.spieler || 'Unbekannt'}</span>
                    <span class="echoharp-story-time">${this.formatTime(story.zeitstempel)}</span>
                </div>
                <div class="echoharp-story-text">${story.text || story.beschreibung || 'Eine Geschichte...'}</div>
            </div>
        `).join('');
    }

    updateDeedsTab() {
        const container = document.getElementById('echoharp-deeds-content');
        if (!container) return;

        if (!this.playerDeeds || this.playerDeeds.length === 0) {
            container.innerHTML = `
                <div class="echoharp-empty">
                    <p>Du hast noch keine bezeugten Taten!</p>
                    <p style="color: #666;">Nutze den Echokristall um deine Taten bezeugen zu lassen.</p>
                    <button class="echoharp-btn" onclick="echoharpUI.switchTab('witness')">
                        Zum Kristall
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = this.playerDeeds.map(deed => `
            <div class="echoharp-deed">
                <div class="echoharp-deed-header">
                    <span class="echoharp-deed-category">${this.categoryIcons[deed.kategorie] || '🌀'}</span>
                    <span class="echoharp-deed-title">${this.formatCategory(deed.kategorie)}</span>
                    <span class="echoharp-deed-melody">🎵 ${deed.mundharmonika_melodie || 'Unbekannte Weise'}</span>
                </div>
                <div class="echoharp-deed-desc">${deed.beschreibung}</div>
                <div class="echoharp-deed-meta">
                    <span>📍 ${deed.ort || 'Unbekannt'}</span>
                    <span>🗺️ ${deed.region || 'Unbekannt'}</span>
                    <span>📅 ${this.formatTime(deed.zeitstempel)}</span>
                    ${deed.erzähl_count > 0 ? `<span>📖 ${deed.erzähl_count}x erzaehlt</span>` : ''}
                </div>
            </div>
        `).join('');
    }

    // =========================================================================
    // ACTIONS
    // =========================================================================

    async requestQuest() {
        try {
            const response = await fetch(`/api/echoharp/quests?spieler_id=${this.spielerId}`);
            let data;

            if (!response.ok) {
                const bardResponse = await fetch(`/api/bard/quest?spieler_id=${this.spielerId}`);
                data = await bardResponse.json();
            } else {
                data = await response.json();
            }

            if (data.erfolg && data.quest) {
                this.currentQuest = data.quest;
                this.showMessage(data.nachricht || 'Quest erhalten!');
            } else {
                this.showMessage(data.nachricht || data.message || 'Keine Quest verfuegbar');
            }

            this.updateBardTab();
        } catch (error) {
            this.showMessage('Fehler beim Quest-Anfragen');
        }
    }

    async acceptQuest(questId) {
        try {
            const response = await fetch('/api/echoharp/quest/accept', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    spieler_id: this.spielerId,
                    quest_id: questId
                })
            });

            const data = await response.json();
            this.showMessage(data.nachricht || 'Quest angenommen!');
            this.currentQuest = null;
            this.updateBardTab();
        } catch (error) {
            this.showMessage('Quest angenommen! (Lokal)');
            this.currentQuest = null;
            this.updateBardTab();
        }
    }

    declineQuest() {
        this.currentQuest = null;
        this.showMessage('Quest abgelehnt');
        this.updateBardTab();
    }

    async activateBefore() {
        try {
            const response = await fetch('/api/echoharp/witness/activate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    spieler_id: this.spielerId,
                    type: 'before'
                })
            });

            if (!response.ok) {
                const bardResponse = await fetch('/api/bard/item/activate/before', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ spieler_id: this.spielerId })
                });
                const data = await bardResponse.json();
                this.showMessage(data.nachricht || 'Kristall aktiviert!');
            } else {
                const data = await response.json();
                this.showMessage(data.nachricht || 'Kristall aktiviert!');
            }

            await this.refreshWitnessItem();
        } catch (error) {
            this.showMessage('Fehler beim Aktivieren');
        }
    }

    async activateAfter() {
        try {
            const response = await fetch('/api/echoharp/witness/activate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    spieler_id: this.spielerId,
                    type: 'after'
                })
            });

            if (!response.ok) {
                const bardResponse = await fetch('/api/bard/item/activate/after', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ spieler_id: this.spielerId })
                });
                const data = await bardResponse.json();
                this.showMessage(data.nachricht || 'Tat bezeugt!');
            } else {
                const data = await response.json();
                this.showMessage(data.nachricht || 'Tat bezeugt!');
            }

            await this.refreshWitnessItem();
            await this.refreshDeeds();
        } catch (error) {
            this.showMessage('Fehler beim Bezeugen');
        }
    }

    // =========================================================================
    // ENCOUNTER CHECK
    // =========================================================================

    checkEncounter() {
        const notification = document.getElementById('echoharp-notification');
        if (!notification) return;

        // Show notification if Echoharp is in wilderness (quests available)
        if (this.echoharpStatus && this.echoharpStatus.ist_in_wildnis) {
            notification.classList.remove('hidden');
        } else {
            notification.classList.add('hidden');
        }
    }

    // =========================================================================
    // HELPERS
    // =========================================================================

    formatMood(mood) {
        const moods = {
            'aufgeregt': 'Aufgeregt',
            'melancholisch': 'Melancholisch',
            'verrückt': 'Verrueckt',
            'geheimnisvoll': 'Geheimnisvoll',
            'betrunken': 'Betrunken'
        };
        return moods[mood] || mood;
    }

    formatCategory(category) {
        const categories = {
            'kampf': 'Kampf',
            'boss': 'Boss-Kampf',
            'rettung': 'Rettung',
            'entdeckung': 'Entdeckung',
            'quest': 'Quest',
            'crafting': 'Handwerk',
            'handel': 'Handel',
            'chaos': 'Chaos',
            'diebstahl': 'Diebstahl',
            'duell': 'Duell'
        };
        return categories[category] || category;
    }

    formatTime(timestamp) {
        if (!timestamp) return 'Unbekannt';
        try {
            const date = new Date(timestamp);
            return date.toLocaleString('de-DE', {
                day: '2-digit',
                month: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return timestamp;
        }
    }

    showMessage(text) {
        const msg = document.createElement('div');
        msg.className = 'echoharp-message';
        msg.textContent = text;
        document.body.appendChild(msg);

        setTimeout(() => msg.remove(), 3000);
    }

    // =========================================================================
    // PANEL CONTROL
    // =========================================================================

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.echoharp-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update content
        document.querySelectorAll('.echoharp-content').forEach(content => {
            content.classList.toggle('active', content.id === `echoharp-tab-${tabName}`);
        });

        // Load data for tab
        switch(tabName) {
            case 'bard':
                this.refreshStatus();
                break;
            case 'witness':
                this.refreshWitnessItem();
                break;
            case 'stories':
                this.refreshStories();
                break;
            case 'deeds':
                this.refreshDeeds();
                break;
        }
    }

    open() {
        document.getElementById('echoharp-panel')?.classList.remove('hidden');
        this.isOpen = true;
        this.refreshStatus();
    }

    close() {
        document.getElementById('echoharp-panel')?.classList.add('hidden');
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
        document.getElementById('echoharp-panel')?.remove();
        document.getElementById('echoharp-notification')?.remove();
        document.getElementById('echoharp-styles')?.remove();
    }
}

// =============================================================================
// GLOBAL INSTANCE
// =============================================================================

let echoharpUI = null;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        echoharpUI = new EchoharpUI();
    });
} else {
    echoharpUI = new EchoharpUI();
}

// Export for console access
window.echoharpUI = echoharpUI;
console.log('[EchoharpUI] Echoharp UI geladen. Oeffnen mit Alt+E oder echoharpUI.open()');
