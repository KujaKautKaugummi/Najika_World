/**
 * Companion Mode Choice UI - Najika World
 * =========================================
 * Permanente Wahl zwischen Aura-Modus und Begleiter-Modus.
 * Erscheint bei Trust-Level 2 (Freund) als Story-Moment.
 *
 * Aura-Modus:   Slime verschmilzt mit Spieler → Buffs, kein physischer Kampf
 * Begleiter:    Slime reist physisch mit → Direkte Kampfteilnahme
 *
 * Die Wahl ist PERMANENT (kann nur 1x pro Playthrough geaendert werden
 * bei Trust-Level 5: Seelenbund).
 *
 * Author: Claude Code (Opus 4.6)
 * Date: 2026-02-15
 */

class CompanionModeChoice {
    constructor() {
        this.hasChosen = false;
        this.chosenMode = null;
        this.canReselect = false;
        this.isOpen = false;
        this.dialog = null;
        this.animationFrame = null;

        // Aura particle system
        this.particles = [];

        this.init();
    }

    init() {
        this.createStyles();
        this.loadState();
        console.log('[OK] Companion Mode Choice UI geladen');
    }

    // ==========================================
    // STYLES
    // ==========================================

    createStyles() {
        if (document.getElementById('companion-choice-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'companion-choice-styles';
        styles.textContent = `
            #companion-choice-overlay {
                position: fixed; top: 0; left: 0;
                width: 100vw; height: 100vh;
                background: rgba(0, 0, 0, 0);
                z-index: 2000; display: none;
                align-items: center; justify-content: center;
                font-family: 'Courier New', monospace;
                transition: background 1.5s ease;
            }
            #companion-choice-overlay.open {
                display: flex;
                background: rgba(0, 0, 0, 0.92);
            }

            .cmc-container {
                position: relative;
                width: 680px; max-width: 95vw;
                opacity: 0;
                transform: scale(0.85);
                transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);
            }
            #companion-choice-overlay.open .cmc-container {
                opacity: 1;
                transform: scale(1);
            }

            .cmc-title {
                text-align: center;
                font-size: 22px;
                color: #FFD700;
                margin-bottom: 8px;
                text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
                letter-spacing: 2px;
            }
            .cmc-subtitle {
                text-align: center;
                font-size: 12px;
                color: rgba(255, 255, 255, 0.5);
                margin-bottom: 25px;
            }

            .cmc-cards {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            @media (max-width: 600px) {
                .cmc-cards {
                    grid-template-columns: 1fr;
                }
            }

            .cmc-card {
                position: relative;
                border-radius: 15px;
                padding: 25px 20px;
                cursor: pointer;
                transition: all 0.4s ease;
                overflow: hidden;
                min-height: 320px;
                display: flex;
                flex-direction: column;
            }
            .cmc-card:hover {
                transform: translateY(-5px);
            }
            .cmc-card.selected {
                transform: translateY(-5px);
            }

            .cmc-card-aura {
                background: linear-gradient(180deg, rgba(100, 50, 200, 0.25), rgba(30, 10, 60, 0.9));
                border: 2px solid rgba(150, 100, 255, 0.3);
            }
            .cmc-card-aura:hover, .cmc-card-aura.selected {
                border-color: rgba(150, 100, 255, 0.8);
                box-shadow: 0 0 40px rgba(150, 100, 255, 0.3),
                            inset 0 0 30px rgba(150, 100, 255, 0.1);
            }

            .cmc-card-physical {
                background: linear-gradient(180deg, rgba(50, 150, 50, 0.25), rgba(10, 40, 10, 0.9));
                border: 2px solid rgba(100, 200, 100, 0.3);
            }
            .cmc-card-physical:hover, .cmc-card-physical.selected {
                border-color: rgba(100, 200, 100, 0.8);
                box-shadow: 0 0 40px rgba(100, 200, 100, 0.3),
                            inset 0 0 30px rgba(100, 200, 100, 0.1);
            }

            .cmc-card-icon {
                font-size: 48px;
                text-align: center;
                margin-bottom: 12px;
                filter: drop-shadow(0 0 10px currentColor);
            }
            .cmc-card-name {
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 6px;
                color: white;
            }
            .cmc-card-desc {
                font-size: 11px;
                text-align: center;
                color: rgba(255, 255, 255, 0.6);
                margin-bottom: 15px;
                line-height: 1.5;
            }

            .cmc-stats {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            .cmc-stat {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 11px;
                color: rgba(255, 255, 255, 0.8);
            }
            .cmc-stat-icon {
                font-size: 14px;
                width: 20px;
                text-align: center;
            }
            .cmc-stat-plus {
                color: #4CAF50;
                font-weight: bold;
            }
            .cmc-stat-minus {
                color: #F44336;
                font-weight: bold;
            }

            .cmc-confirm-area {
                text-align: center;
                opacity: 0;
                transform: translateY(10px);
                transition: all 0.5s ease;
                pointer-events: none;
            }
            .cmc-confirm-area.visible {
                opacity: 1;
                transform: translateY(0);
                pointer-events: auto;
            }

            .cmc-confirm-btn {
                background: linear-gradient(135deg, #FFD700, #FF8C00);
                border: none;
                border-radius: 10px;
                padding: 12px 40px;
                color: #000;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                cursor: pointer;
                letter-spacing: 1px;
                transition: all 0.3s ease;
            }
            .cmc-confirm-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
            }
            .cmc-confirm-btn:disabled {
                opacity: 0.4;
                cursor: not-allowed;
                transform: none;
            }

            .cmc-warning {
                font-size: 10px;
                color: rgba(255, 100, 100, 0.7);
                margin-top: 10px;
            }

            .cmc-canvas {
                position: absolute;
                top: 0; left: 0;
                width: 100%; height: 100%;
                pointer-events: none;
            }

            /* Aura preview animation */
            @keyframes aura-pulse {
                0%, 100% { opacity: 0.3; transform: scale(1); }
                50% { opacity: 0.7; transform: scale(1.1); }
            }
            .cmc-aura-preview {
                position: absolute;
                top: 50%; left: 50%;
                width: 80px; height: 80px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(150,100,255,0.4), transparent);
                transform: translate(-50%, -50%) scale(1);
                animation: aura-pulse 3s ease-in-out infinite;
                pointer-events: none;
            }

            /* Physical preview animation */
            @keyframes companion-bounce {
                0%, 100% { transform: translate(-50%, -50%) translateY(0); }
                50% { transform: translate(-50%, -50%) translateY(-8px); }
            }
            .cmc-physical-preview {
                position: absolute;
                top: 45%; left: 50%;
                font-size: 36px;
                transform: translate(-50%, -50%);
                animation: companion-bounce 2s ease-in-out infinite;
                pointer-events: none;
                filter: drop-shadow(0 5px 15px rgba(100,200,100,0.4));
            }

            /* Reselect banner */
            .cmc-reselect-banner {
                text-align: center;
                background: rgba(255, 215, 0, 0.1);
                border: 1px solid rgba(255, 215, 0, 0.3);
                border-radius: 8px;
                padding: 8px;
                margin-bottom: 15px;
                font-size: 11px;
                color: #FFD700;
            }
        `;
        document.head.appendChild(styles);
    }

    // ==========================================
    // UI RENDERING
    // ==========================================

    open(isReselect = false) {
        if (this.isOpen) return;
        if (this.hasChosen && !isReselect) {
            this.showCurrentMode();
            return;
        }

        this.canReselect = isReselect;
        this.isOpen = true;
        this.selectedMode = null;

        this.createDialog(isReselect);

        // Animate in
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                this.dialog.classList.add('open');
            });
        });
    }

    createDialog(isReselect) {
        // Remove existing
        const existing = document.getElementById('companion-choice-overlay');
        if (existing) existing.remove();

        this.dialog = document.createElement('div');
        this.dialog.id = 'companion-choice-overlay';

        const slimeName = this._getSlimeName();
        const currentForm = this._getCurrentForm();

        this.dialog.innerHTML = `
            <div class="cmc-container">
                ${isReselect ? `
                    <div class="cmc-reselect-banner">
                        Seelenbund erreicht! Du darfst deine Wahl einmalig aendern.
                    </div>
                ` : ''}

                <div class="cmc-title">WAHL DES BANDES</div>
                <div class="cmc-subtitle">
                    Wie soll ${slimeName} dich auf deiner Reise begleiten?
                </div>

                <div class="cmc-cards">
                    <!-- AURA CARD -->
                    <div class="cmc-card cmc-card-aura" id="cmc-card-aura"
                         onclick="window.companionChoice._selectMode('aura')">
                        <div class="cmc-aura-preview"></div>
                        <div class="cmc-card-icon" style="color: #B388FF;">&#10024;</div>
                        <div class="cmc-card-name">Aura-Band</div>
                        <div class="cmc-card-desc">
                            ${slimeName} verschmilzt mit deiner Seele.<br>
                            Unsichtbar, aber immer praesent.
                        </div>
                        <div class="cmc-stats">
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9876;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Alle Stats erhalten Aura-Buff</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#128737;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Passive Heilung im Kampf</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9889;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Elementar-Resistenz je nach Form</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#128161;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Erfahrungsboost +15%</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9888;</span>
                                <span class="cmc-stat-minus">-</span>
                                <span>Kein physischer Begleiter sichtbar</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9888;</span>
                                <span class="cmc-stat-minus">-</span>
                                <span>Keine direkte Kampfteilnahme</span>
                            </div>
                        </div>
                    </div>

                    <!-- PHYSICAL CARD -->
                    <div class="cmc-card cmc-card-physical" id="cmc-card-physical"
                         onclick="window.companionChoice._selectMode('physical')">
                        <div class="cmc-physical-preview">${currentForm}</div>
                        <div class="cmc-card-icon" style="color: #81C784;">&#128062;</div>
                        <div class="cmc-card-name">Koerper-Band</div>
                        <div class="cmc-card-desc">
                            ${slimeName} reist an deiner Seite.<br>
                            Sichtbar, greifbar, treu.
                        </div>
                        <div class="cmc-stats">
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9876;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Eigene Kampfaktionen (Angriff/Verteidigung)</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#128165;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Combo-Attacken mit Spieler</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#129309;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Schnellerer Trust-Aufbau</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#127968;</span>
                                <span class="cmc-stat-plus">+</span>
                                <span>Interaktionen in der Welt</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9888;</span>
                                <span class="cmc-stat-minus">-</span>
                                <span>Kann im Kampf verletzt werden</span>
                            </div>
                            <div class="cmc-stat">
                                <span class="cmc-stat-icon">&#9888;</span>
                                <span class="cmc-stat-minus">-</span>
                                <span>Keine passiven Stat-Buffs</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="cmc-confirm-area" id="cmc-confirm-area">
                    <button class="cmc-confirm-btn" id="cmc-confirm-btn"
                            onclick="window.companionChoice._confirmChoice()">
                        BAND BESIEGELN
                    </button>
                    <div class="cmc-warning">
                        Diese Wahl ist permanent${isReselect ? '' : ' (Aenderung erst bei Seelenbund moeglich)'}.
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.dialog);
    }

    _selectMode(mode) {
        this.selectedMode = mode;

        // Update card selection state
        const auraCard = document.getElementById('cmc-card-aura');
        const physicalCard = document.getElementById('cmc-card-physical');
        const confirmArea = document.getElementById('cmc-confirm-area');

        auraCard.classList.toggle('selected', mode === 'aura');
        physicalCard.classList.toggle('selected', mode === 'physical');

        // Show confirm button
        confirmArea.classList.add('visible');

        // Update button text
        const btn = document.getElementById('cmc-confirm-btn');
        if (mode === 'aura') {
            btn.textContent = 'AURA-BAND BESIEGELN';
            btn.style.background = 'linear-gradient(135deg, #B388FF, #7C4DFF)';
            btn.style.color = '#FFF';
        } else {
            btn.textContent = 'KOERPER-BAND BESIEGELN';
            btn.style.background = 'linear-gradient(135deg, #81C784, #388E3C)';
            btn.style.color = '#FFF';
        }
    }

    _confirmChoice() {
        if (!this.selectedMode) return;

        this.hasChosen = true;
        this.chosenMode = this.selectedMode;

        // Apply to slime companion
        if (window.slimeCompanion) {
            window.slimeCompanion.setCompanionMode(this.selectedMode);
        }

        // Save state
        this.saveState();

        // Notify backend
        this._notifyBackend(this.selectedMode);

        // Show confirmation animation
        this._showConfirmation(this.selectedMode);
    }

    _showConfirmation(mode) {
        const container = this.dialog.querySelector('.cmc-container');
        const isAura = mode === 'aura';
        const slimeName = this._getSlimeName();

        container.innerHTML = `
            <div style="text-align:center; padding: 40px 20px;">
                <div style="font-size:64px; margin-bottom:20px;
                    filter: drop-shadow(0 0 20px ${isAura ? 'rgba(150,100,255,0.6)' : 'rgba(100,200,100,0.6)'});">
                    ${isAura ? '&#10024;' : '&#128062;'}
                </div>
                <div style="font-size:20px; color:${isAura ? '#B388FF' : '#81C784'};
                    margin-bottom:10px; font-weight:bold;">
                    ${isAura ? 'Aura-Band' : 'Koerper-Band'} besiegelt!
                </div>
                <div style="font-size:13px; color:rgba(255,255,255,0.7);
                    margin-bottom:25px; line-height:1.6;">
                    ${isAura
                        ? `${slimeName} loest sich in tausend Lichtfunken auf...<br>
                           Du spuerst eine warme Energie durch deine Adern fliessen.<br>
                           <em style="color:#B388FF;">"Ich bin jetzt ein Teil von dir."</em>`
                        : `${slimeName} springt freudig an deine Seite!<br>
                           Ein treuer Begleiter fuer alle Abenteuer.<br>
                           <em style="color:#81C784;">"Zusammen sind wir unbesiegbar!"</em>`
                    }
                </div>
                <div style="display:flex; flex-direction:column; gap:8px; align-items:center;">
                    ${isAura ? `
                        <div style="font-size:11px; color:#B388FF;">
                            &#10003; Aura-Buffs aktiviert
                        </div>
                        <div style="font-size:11px; color:#B388FF;">
                            &#10003; Passive Heilung freigeschaltet
                        </div>
                        <div style="font-size:11px; color:#B388FF;">
                            &#10003; XP-Boost +15% aktiv
                        </div>
                    ` : `
                        <div style="font-size:11px; color:#81C784;">
                            &#10003; Begleiter-Modus aktiviert
                        </div>
                        <div style="font-size:11px; color:#81C784;">
                            &#10003; Combo-System freigeschaltet
                        </div>
                        <div style="font-size:11px; color:#81C784;">
                            &#10003; Trust-Bonus +25% aktiv
                        </div>
                    `}
                </div>
                <button onclick="window.companionChoice.close()"
                    style="margin-top:30px; background:rgba(255,255,255,0.1);
                    border:1px solid rgba(255,255,255,0.3); border-radius:8px;
                    padding:10px 30px; color:white; font-size:12px; cursor:pointer;
                    font-family:'Courier New',monospace; transition:all 0.3s;">
                    Weiter
                </button>
            </div>
        `;
    }

    close() {
        if (!this.dialog) return;
        this.isOpen = false;
        this.dialog.classList.remove('open');
        setTimeout(() => {
            if (this.dialog) {
                this.dialog.remove();
                this.dialog = null;
            }
        }, 500);
    }

    // ==========================================
    // CURRENT MODE DISPLAY (Mini-Panel)
    // ==========================================

    showCurrentMode() {
        const isAura = this.chosenMode === 'aura';
        const slimeName = this._getSlimeName();

        const existing = document.getElementById('companion-mode-info');
        if (existing) existing.remove();

        const panel = document.createElement('div');
        panel.id = 'companion-mode-info';
        panel.style.cssText = `
            position:fixed; bottom:120px; right:20px;
            background:linear-gradient(135deg,
                ${isAura ? 'rgba(60,30,120,0.95)' : 'rgba(20,60,20,0.95)'},
                rgba(10,10,20,0.98));
            border:2px solid ${isAura ? 'rgba(150,100,255,0.5)' : 'rgba(100,200,100,0.5)'};
            border-radius:12px; padding:15px; color:white;
            font-family:'Courier New',monospace; z-index:500;
            min-width:220px; max-width:260px;
            box-shadow:0 8px 32px rgba(0,0,0,0.8);
        `;

        panel.innerHTML = `
            <button onclick="document.getElementById('companion-mode-info').remove()"
                style="position:absolute;top:6px;right:8px;background:none;border:none;
                color:rgba(255,255,255,0.5);font-size:16px;cursor:pointer;">x</button>

            <div style="font-size:13px;font-weight:bold;margin-bottom:8px;
                color:${isAura ? '#B388FF' : '#81C784'};">
                ${isAura ? '&#10024;' : '&#128062;'} ${isAura ? 'Aura-Band' : 'Koerper-Band'}
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.6);margin-bottom:10px;">
                ${slimeName} &mdash; ${isAura ? 'Verschmolzen mit deiner Seele' : 'An deiner Seite'}
            </div>

            <div style="display:flex;flex-direction:column;gap:4px;font-size:10px;">
                ${isAura ? `
                    <div style="color:#B388FF;">&#10003; Aura-Buffs: Aktiv</div>
                    <div style="color:#B388FF;">&#10003; Passive Heilung: Aktiv</div>
                    <div style="color:#B388FF;">&#10003; XP-Boost: +15%</div>
                ` : `
                    <div style="color:#81C784;">&#10003; Kampf-Begleiter: Aktiv</div>
                    <div style="color:#81C784;">&#10003; Combo-System: Aktiv</div>
                    <div style="color:#81C784;">&#10003; Trust-Bonus: +25%</div>
                `}
            </div>

            ${this._canReselect() ? `
                <button onclick="window.companionChoice.open(true)"
                    style="margin-top:10px;width:100%;background:rgba(255,215,0,0.15);
                    border:1px solid rgba(255,215,0,0.3);border-radius:6px;
                    padding:6px;color:#FFD700;font-size:10px;cursor:pointer;
                    font-family:'Courier New',monospace;">
                    Band neu waehlen (Seelenbund)
                </button>
            ` : ''}
        `;

        document.body.appendChild(panel);

        // Auto-close after 8s
        setTimeout(() => {
            const el = document.getElementById('companion-mode-info');
            if (el) el.remove();
        }, 8000);
    }

    // ==========================================
    // TRUST-LEVEL TRIGGER
    // ==========================================

    checkTrustTrigger(trustLevel) {
        // Trigger bei Trust-Level 2 (Freund) wenn noch nicht gewaehlt
        if (trustLevel >= 2 && !this.hasChosen) {
            this.open(false);
            return true;
        }
        // Reselect-Option bei Trust-Level 5 (Seelenbund)
        if (trustLevel >= 5 && this.hasChosen && !this._hasReselected()) {
            this._showReselectNotification();
            return true;
        }
        return false;
    }

    _showReselectNotification() {
        if (window.slimeCompanion && window.slimeCompanion.showNotification) {
            window.slimeCompanion.showNotification(
                'Seelenbund erreicht! Du kannst dein Band mit deinem Begleiter neu waehlen.',
                5000
            );
        }
    }

    _canReselect() {
        if (!window.slimeCompanion) return false;
        const trustLevel = window.slimeCompanion.trustLevel || 0;
        return trustLevel >= 5 && !this._hasReselected();
    }

    _hasReselected() {
        try {
            return localStorage.getItem('najika_companion_reselected') === 'true';
        } catch (e) { return false; }
    }

    // ==========================================
    // BACKEND SYNC
    // ==========================================

    async _notifyBackend(mode) {
        try {
            const response = await fetch('/api/slime/set-mode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mode: mode,
                    permanent: true,
                    timestamp: Date.now()
                })
            });
            if (!response.ok) {
                console.warn('[CompanionChoice] Backend sync fehlgeschlagen:', response.status);
            }
        } catch (e) {
            console.warn('[CompanionChoice] Backend nicht erreichbar:', e.message);
        }
    }

    // ==========================================
    // HELPERS
    // ==========================================

    _getSlimeName() {
        if (window.slimeCompanion && window.slimeCompanion.slimeName) {
            return window.slimeCompanion.slimeName;
        }
        return 'Dein Begleiter';
    }

    _getCurrentForm() {
        if (window.slimeCompanion && window.slimeCompanion.currentForm) {
            const formIcons = {
                slime: '\uD83D\uDFE2',
                wolf: '\uD83D\uDC3A',
                phoenix: '\uD83D\uDD25',
                dragon: '\uD83D\uDC32',
                golem: '\uD83E\uDEA8',
                spirit: '\uD83D\uDC7B',
                serpent: '\uD83D\uDC0D',
                falcon: '\uD83E\uDD85'
            };
            return formIcons[window.slimeCompanion.currentForm] || '\uD83D\uDFE2';
        }
        return '\uD83D\uDFE2';
    }

    // ==========================================
    // PERSISTENCE
    // ==========================================

    saveState() {
        try {
            const state = {
                hasChosen: this.hasChosen,
                chosenMode: this.chosenMode,
                chosenAt: Date.now()
            };
            localStorage.setItem('najika_companion_mode_choice', JSON.stringify(state));

            if (this.canReselect) {
                localStorage.setItem('najika_companion_reselected', 'true');
            }
        } catch (e) { /* Silent */ }
    }

    loadState() {
        try {
            const raw = localStorage.getItem('najika_companion_mode_choice');
            if (raw) {
                const state = JSON.parse(raw);
                this.hasChosen = state.hasChosen || false;
                this.chosenMode = state.chosenMode || null;
            }
        } catch (e) { /* Silent */ }
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    getMode() {
        return this.chosenMode;
    }

    isAuraMode() {
        return this.chosenMode === 'aura';
    }

    isPhysicalMode() {
        return this.chosenMode === 'physical';
    }

    getAuraBuffs() {
        if (!this.isAuraMode()) return null;

        const auraLevel = (window.slimeCompanion && window.slimeCompanion.auraLevel) || 0;
        const multiplier = [1.0, 1.05, 1.10, 1.20, 1.35, 1.50][auraLevel] || 1.0;

        return {
            statMultiplier: multiplier,
            passiveHeal: 0.02 * multiplier,
            xpBoost: 0.15 * multiplier,
            elementResist: 0.10 * multiplier
        };
    }

    getPhysicalBonuses() {
        if (!this.isPhysicalMode()) return null;

        const trustLevel = (window.slimeCompanion && window.slimeCompanion.trustLevel) || 0;

        return {
            comboChance: 0.15 + (trustLevel * 0.02),
            trustGainMultiplier: 1.25,
            companionDamage: 1.0 + (trustLevel * 0.1),
            canTakeDamage: true
        };
    }

    // Fuer externes Triggering (z.B. von Chat oder Story-Events)
    triggerChoice() {
        if (!this.hasChosen) {
            this.open(false);
        }
    }

    triggerReselect() {
        if (this.hasChosen && this._canReselect()) {
            this.open(true);
        }
    }
}

// ==========================================
// GLOBAL INIT
// ==========================================

let companionChoice = null;

document.addEventListener('DOMContentLoaded', () => {
    companionChoice = new CompanionModeChoice();
});

if (document.readyState !== 'loading') {
    companionChoice = new CompanionModeChoice();
}

if (typeof window !== 'undefined') {
    window.CompanionModeChoice = CompanionModeChoice;
    window.companionChoice = companionChoice;
}
