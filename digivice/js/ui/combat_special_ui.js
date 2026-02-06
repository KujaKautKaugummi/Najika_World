/**
 * COMBAT SPECIAL UI - Grab, TIDS, Infuse, Weapon Glow & Keybindings
 * ===================================================================
 *
 * UI fuer die Combat-Systeme:
 * 1. GRAB - Wrestling-Griff mit Move-Auswahl-Popup (5s Timer)
 * 2. TIDS - Tritt In Den Schritt (GAG-Move mit lustiger Reaktion)
 * 3. INFUSE - Aktive Waffen-Buffs mit Timer-Countdown + Waffen-Glow
 * 4. WEAPON GLOW - Waffen-Slots im HUD gluehen in Element-Farbe
 * 5. TIDS SOUND - Synthesized "OUCH" Sound via Web Audio API
 * 6. KEYBINDINGS OVERLAY - Alle Combat-Tasten als Hilfe-Popup (H/F1)
 *
 * Keybindings: G=Grab, T=TIDS, H/F1=Keybindings
 * API: POST /api/combat-magic/grab, /api/combat-magic/tids
 */

(function() {
    'use strict';

    const API_BASE = 'http://127.0.0.1:8000';

    // ==========================================
    // ELEMENT FARBEN (fuer Infuse Glow)
    // ==========================================
    const ELEMENT_COLORS = {
        feuer: '#ff4400',
        eis: '#88ddff',
        blitz: '#ffff00',
        licht: '#ffffaa',
        dunkel: '#9933ff',
        natur: '#00aa00',
        erde: '#8b4513',
        wind: '#aaffaa',
        wasser: '#0066ff',
        fire: '#ff4400',
        ice: '#88ddff',
        lightning: '#ffff00',
        light: '#ffffaa',
        dark: '#9933ff',
        nature: '#00aa00',
        earth: '#8b4513',
        water: '#0066ff'
    };

    const ELEMENT_NAMES = {
        feuer: 'Feuer', fire: 'Feuer',
        eis: 'Frost', ice: 'Frost',
        blitz: 'Blitz', lightning: 'Blitz',
        licht: 'Licht', light: 'Licht',
        dunkel: 'Schatten', dark: 'Schatten',
        natur: 'Natur', nature: 'Natur',
        erde: 'Stein', earth: 'Stein',
        wind: 'Wind',
        wasser: 'Wasser', water: 'Wasser'
    };

    const ELEMENT_ICONS = {
        feuer: '🔥', fire: '🔥',
        eis: '❄️', ice: '❄️',
        blitz: '⚡', lightning: '⚡',
        licht: '✨', light: '✨',
        dunkel: '🌑', dark: '🌑',
        natur: '🌿', nature: '🌿',
        erde: '🪨', earth: '🪨',
        wind: '🌪️',
        wasser: '💧', water: '💧'
    };

    // ==========================================
    // STATE
    // ==========================================
    const uiState = {
        grabPopupVisible: false,
        grabTimer: null,
        grabTimeLeft: 5,
        tidsPopupVisible: false,
        tidsPopupTimer: null,
        infuseUpdateInterval: null,
        keybindingsVisible: false,
        audioContext: null,
        initialized: false
    };

    // ==========================================
    // INITIALIZATION
    // ==========================================

    function init() {
        if (uiState.initialized) return;
        uiState.initialized = true;

        console.log('🎮 Combat Special UI V2 initializing...');

        injectStyles();
        createCombatSpecialButtons();
        createGrabPopup();
        createTIDSPopup();
        createInfuseDisplay();
        createKeybindingsOverlay();
        setupKeybindings();
        startInfuseUpdateLoop();
        initAudio();

        // Inject Grab/TIDS into unified combat HUD when it appears
        injectIntoUnifiedHUD();
        // Retry injection after HUD might be created
        setTimeout(injectIntoUnifiedHUD, 1500);
        setTimeout(injectIntoUnifiedHUD, 3000);

        console.log('✅ Combat Special UI V2 ready! (G=Grab, T=TIDS, H=Hilfe)');
    }

    // ==========================================
    // AUDIO SYSTEM (Web Audio API Synthesizer)
    // ==========================================

    function initAudio() {
        try {
            uiState.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('⚠️ Web Audio API nicht verfuegbar');
        }
    }

    function ensureAudioContext() {
        if (!uiState.audioContext) {
            try {
                uiState.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            } catch (e) { return null; }
        }
        if (uiState.audioContext.state === 'suspended') {
            uiState.audioContext.resume();
        }
        return uiState.audioContext;
    }

    function playTIDSSound() {
        const ctx = ensureAudioContext();
        if (!ctx) return;

        const now = ctx.currentTime;

        // 1. Impact "THWACK" - kurzer tiefer Schlag
        const impactOsc = ctx.createOscillator();
        const impactGain = ctx.createGain();
        impactOsc.type = 'sine';
        impactOsc.frequency.setValueAtTime(150, now);
        impactOsc.frequency.exponentialRampToValueAtTime(40, now + 0.15);
        impactGain.gain.setValueAtTime(0.6, now);
        impactGain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
        impactOsc.connect(impactGain);
        impactGain.connect(ctx.destination);
        impactOsc.start(now);
        impactOsc.stop(now + 0.2);

        // 2. "OUCH" - hoher Quietscher (lustig!)
        const ouchOsc = ctx.createOscillator();
        const ouchGain = ctx.createGain();
        ouchOsc.type = 'sawtooth';
        ouchOsc.frequency.setValueAtTime(800, now + 0.05);
        ouchOsc.frequency.linearRampToValueAtTime(1200, now + 0.15);
        ouchOsc.frequency.linearRampToValueAtTime(600, now + 0.4);
        ouchGain.gain.setValueAtTime(0, now);
        ouchGain.gain.linearRampToValueAtTime(0.3, now + 0.08);
        ouchGain.gain.linearRampToValueAtTime(0.15, now + 0.25);
        ouchGain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        ouchOsc.connect(ouchGain);
        ouchGain.connect(ctx.destination);
        ouchOsc.start(now + 0.05);
        ouchOsc.stop(now + 0.5);

        // 3. Comic "Boing" - Feder-Effekt
        const boingOsc = ctx.createOscillator();
        const boingGain = ctx.createGain();
        boingOsc.type = 'sine';
        boingOsc.frequency.setValueAtTime(300, now + 0.1);
        boingOsc.frequency.exponentialRampToValueAtTime(900, now + 0.2);
        boingOsc.frequency.exponentialRampToValueAtTime(200, now + 0.5);
        boingGain.gain.setValueAtTime(0.2, now + 0.1);
        boingGain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
        boingOsc.connect(boingGain);
        boingGain.connect(ctx.destination);
        boingOsc.start(now + 0.1);
        boingOsc.stop(now + 0.6);

        // 4. Noise burst (Knall)
        const bufferSize = ctx.sampleRate * 0.1;
        const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
        }
        const noiseSource = ctx.createBufferSource();
        const noiseGain = ctx.createGain();
        noiseSource.buffer = noiseBuffer;
        noiseGain.gain.setValueAtTime(0.25, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        noiseSource.connect(noiseGain);
        noiseGain.connect(ctx.destination);
        noiseSource.start(now);
    }

    function playGrabSound() {
        const ctx = ensureAudioContext();
        if (!ctx) return;

        const now = ctx.currentTime;

        // "Whoosh" grab sound
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.exponentialRampToValueAtTime(80, now + 0.3);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.3);
    }

    function playInfuseExpiredSound() {
        const ctx = ensureAudioContext();
        if (!ctx) return;

        const now = ctx.currentTime;

        // Absteigender Ton = "puff, weg"
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.exponentialRampToValueAtTime(100, now + 0.4);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.5);
    }

    // ==========================================
    // CSS INJECTION
    // ==========================================

    function injectStyles() {
        if (document.getElementById('combat-special-styles')) return;

        const style = document.createElement('style');
        style.id = 'combat-special-styles';
        style.textContent = `
            /* ========== COMBAT SPECIAL BUTTONS (Floating Fallback) ========== */
            #combat-special-buttons {
                position: fixed;
                bottom: 320px;
                right: 20px;
                display: flex;
                flex-direction: column;
                gap: 8px;
                z-index: 14999;
            }

            /* Verstecke Floating Buttons wenn HUD-Integration aktiv */
            #combat-special-buttons.hud-integrated {
                display: none;
            }

            .combat-special-btn {
                width: 60px;
                height: 60px;
                border-radius: 12px;
                border: 2px solid rgba(255,255,255,0.3);
                color: white;
                font-weight: bold;
                font-size: 13px;
                cursor: pointer;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
                position: relative;
                text-shadow: 1px 1px 2px black;
                font-family: 'Segoe UI', sans-serif;
            }

            .combat-special-btn:hover {
                transform: scale(1.1);
                border-color: white;
            }

            .combat-special-btn:active {
                transform: scale(0.95);
            }

            .combat-special-btn .btn-icon {
                font-size: 20px;
                line-height: 1;
            }

            .combat-special-btn .btn-label {
                font-size: 10px;
                margin-top: 2px;
                opacity: 0.9;
            }

            #btn-grab, .hud-btn-grab {
                background: linear-gradient(135deg, #e67e22, #d35400);
            }

            #btn-tids, .hud-btn-tids {
                background: linear-gradient(135deg, #e74c3c, #c0392b);
            }

            #btn-tids.on-cooldown, .hud-btn-tids.on-cooldown {
                background: linear-gradient(135deg, #555, #333);
                opacity: 0.6;
                cursor: not-allowed;
            }

            #btn-tids .cooldown-overlay, .hud-btn-tids .cooldown-overlay {
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.6);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 11px;
                color: #aaa;
            }

            .combat-special-btn .keyhint {
                position: absolute;
                top: -6px;
                right: -6px;
                background: #333;
                color: #fff;
                font-size: 9px;
                padding: 1px 5px;
                border-radius: 4px;
                border: 1px solid #666;
            }

            /* ========== HUD-INTEGRIERTE Grab/TIDS Buttons ========== */
            .hud-special-row {
                display: flex;
                gap: 10px;
                margin: 8px 0;
                justify-content: center;
                flex-wrap: wrap;
            }

            .hud-special-btn {
                padding: 12px 18px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 13px;
                font-weight: bold;
                transition: all 0.2s;
                min-width: 100px;
                color: white;
                position: relative;
            }

            .hud-special-btn:hover {
                transform: scale(1.05);
            }

            .hud-btn-grab { background: linear-gradient(135deg, #e67e22, #d35400); }
            .hud-btn-tids { background: linear-gradient(135deg, #e74c3c, #c0392b); }
            .hud-btn-help { background: linear-gradient(135deg, #3498db, #2980b9); }

            .hud-btn-tids.on-cooldown {
                opacity: 0.5;
                cursor: not-allowed;
            }

            .hud-special-btn .key-badge {
                display: inline-block;
                background: rgba(0,0,0,0.3);
                padding: 1px 6px;
                border-radius: 3px;
                font-size: 10px;
                margin-left: 6px;
                vertical-align: middle;
            }

            /* ========== WEAPON HAND DISPLAY (Infuse Glow) ========== */
            .weapon-hands-display {
                display: flex;
                gap: 8px;
                align-items: center;
                margin: 6px 0;
            }

            .weapon-hand-slot {
                display: flex;
                align-items: center;
                gap: 6px;
                background: rgba(255,255,255,0.08);
                border: 2px solid rgba(255,255,255,0.15);
                border-radius: 8px;
                padding: 5px 10px;
                min-width: 120px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                color: #ccc;
                position: relative;
                transition: all 0.3s;
            }

            .weapon-hand-slot .hand-label {
                font-size: 10px;
                color: #888;
                font-weight: bold;
                min-width: 14px;
            }

            .weapon-hand-slot .weapon-icon {
                font-size: 18px;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px;
                transition: all 0.3s;
            }

            .weapon-hand-slot .weapon-name {
                font-size: 12px;
                font-weight: bold;
                color: #ddd;
                flex: 1;
            }

            /* Infuse Glow State */
            .weapon-hand-slot.infused {
                border-color: var(--infuse-color, #fff);
                box-shadow: 0 0 12px var(--infuse-color, #fff),
                            inset 0 0 8px rgba(255,255,255,0.1);
                animation: weaponGlow 2s ease-in-out infinite;
            }

            .weapon-hand-slot.infused .weapon-icon {
                background: var(--infuse-color, #fff);
                box-shadow: 0 0 10px var(--infuse-color, #fff);
                animation: iconPulse 1.5s ease-in-out infinite;
            }

            .weapon-hand-slot .infuse-badge {
                display: none;
                position: absolute;
                bottom: -5px;
                right: -5px;
                background: var(--infuse-color, #fff);
                border-radius: 50%;
                padding: 2px 6px;
                font-size: 10px;
                font-weight: bold;
                color: #000;
                animation: pulse 1s infinite;
                border: 1px solid rgba(0,0,0,0.3);
            }

            .weapon-hand-slot.infused .infuse-badge {
                display: block;
            }

            @keyframes weaponGlow {
                0%, 100% { box-shadow: 0 0 8px var(--infuse-color, #fff), inset 0 0 6px rgba(255,255,255,0.05); }
                50% { box-shadow: 0 0 20px var(--infuse-color, #fff), 0 0 30px var(--infuse-color, #fff), inset 0 0 10px rgba(255,255,255,0.1); }
            }

            @keyframes iconPulse {
                0%, 100% { box-shadow: 0 0 5px var(--infuse-color, #fff); }
                50% { box-shadow: 0 0 15px var(--infuse-color, #fff), 0 0 25px var(--infuse-color, #fff); }
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.7; transform: scale(1.1); }
            }

            /* ========== GRAB POPUP ========== */
            #grab-popup {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #2c3e50, #34495e);
                border: 3px solid #e67e22;
                border-radius: 16px;
                padding: 24px 32px;
                z-index: 20000;
                min-width: 340px;
                text-align: center;
                font-family: 'Segoe UI', sans-serif;
                color: white;
                box-shadow: 0 0 40px rgba(230, 126, 34, 0.5);
                animation: grabPopIn 0.3s ease-out;
            }

            #grab-popup.visible { display: block; }

            @keyframes grabPopIn {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            }

            #grab-popup .grab-title {
                font-size: 22px;
                font-weight: bold;
                color: #e67e22;
                margin-bottom: 6px;
            }

            #grab-popup .grab-timer {
                font-size: 14px;
                color: #e74c3c;
                margin-bottom: 16px;
            }

            #grab-popup .grab-timer .timer-bar {
                width: 100%;
                height: 6px;
                background: #444;
                border-radius: 3px;
                margin-top: 6px;
                overflow: hidden;
            }

            #grab-popup .grab-timer .timer-fill {
                height: 100%;
                background: linear-gradient(90deg, #e74c3c, #e67e22);
                transition: width 0.1s linear;
                border-radius: 3px;
            }

            .grab-move-btn {
                display: block;
                width: 100%;
                padding: 12px 16px;
                margin: 6px 0;
                border: 2px solid rgba(255,255,255,0.2);
                border-radius: 10px;
                background: rgba(255,255,255,0.08);
                color: white;
                font-size: 15px;
                font-weight: bold;
                cursor: pointer;
                text-align: left;
                transition: all 0.15s;
                font-family: 'Segoe UI', sans-serif;
            }

            .grab-move-btn:hover {
                background: rgba(230, 126, 34, 0.3);
                border-color: #e67e22;
                transform: translateX(4px);
            }

            .grab-move-btn .move-key {
                display: inline-block;
                background: #555;
                color: #fff;
                padding: 1px 8px;
                border-radius: 4px;
                font-size: 12px;
                margin-right: 8px;
                min-width: 24px;
                text-align: center;
            }

            .grab-move-btn .move-req {
                float: right;
                font-size: 11px;
                color: #aaa;
                font-weight: normal;
            }

            .grab-move-btn.disabled {
                opacity: 0.4;
                cursor: not-allowed;
            }

            .grab-move-btn.disabled:hover {
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.2);
                transform: none;
            }

            /* ========== TIDS GAG POPUP ========== */
            #tids-popup {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #ff6b6b, #feca57);
                border: 4px solid #fff;
                border-radius: 24px;
                padding: 32px 40px;
                z-index: 20001;
                min-width: 400px;
                max-width: 500px;
                text-align: center;
                font-family: 'Segoe UI', sans-serif;
                color: #333;
                box-shadow: 0 0 60px rgba(255, 107, 107, 0.6), 0 0 120px rgba(254, 202, 87, 0.3);
                animation: tidsBounce 0.5s ease;
            }

            #tids-popup.visible { display: block; }

            @keyframes tidsBounce {
                0% { transform: translate(-50%, -50%) scale(0); }
                50% { transform: translate(-50%, -50%) scale(1.15); }
                70% { transform: translate(-50%, -50%) scale(0.95); }
                100% { transform: translate(-50%, -50%) scale(1); }
            }

            #tids-popup .tids-icon {
                font-size: 48px;
                margin-bottom: 8px;
            }

            #tids-popup .tids-title {
                font-size: 28px;
                font-weight: 900;
                color: #c0392b;
                text-shadow: 2px 2px 0 rgba(255,255,255,0.5);
                margin-bottom: 12px;
            }

            #tids-popup .tids-gag {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                margin: 16px 0;
                padding: 12px;
                background: rgba(255,255,255,0.5);
                border-radius: 12px;
                font-style: italic;
                line-height: 1.4;
            }

            #tids-popup .tids-stats {
                display: flex;
                justify-content: center;
                gap: 16px;
                margin-top: 12px;
            }

            #tids-popup .tids-stat {
                background: rgba(0,0,0,0.15);
                padding: 6px 14px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }

            /* ========== INFUSE DISPLAY ========== */
            #infuse-display {
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 14999;
                display: flex;
                flex-direction: column;
                gap: 6px;
                pointer-events: none;
            }

            .infuse-buff {
                display: flex;
                align-items: center;
                gap: 10px;
                background: rgba(0, 0, 0, 0.8);
                border-radius: 10px;
                padding: 8px 14px;
                border-left: 4px solid var(--infuse-color, #fff);
                min-width: 220px;
                animation: infuseSlideIn 0.3s ease-out;
                box-shadow: 0 0 15px var(--infuse-glow, transparent);
            }

            @keyframes infuseSlideIn {
                0% { transform: translateX(100px); opacity: 0; }
                100% { transform: translateX(0); opacity: 1; }
            }

            .infuse-buff .infuse-icon {
                font-size: 24px;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 8px;
                background: rgba(255,255,255,0.1);
                animation: infuseGlow 1.5s ease-in-out infinite;
            }

            @keyframes infuseGlow {
                0%, 100% { box-shadow: 0 0 5px var(--infuse-color, #fff); }
                50% { box-shadow: 0 0 20px var(--infuse-color, #fff), 0 0 30px var(--infuse-color, #fff); }
            }

            .infuse-buff .infuse-info {
                flex: 1;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }

            .infuse-buff .infuse-name {
                font-size: 13px;
                font-weight: bold;
            }

            .infuse-buff .infuse-bonus {
                font-size: 11px;
                color: #aaa;
            }

            .infuse-buff .infuse-timer {
                font-size: 18px;
                font-weight: bold;
                color: var(--infuse-color, #fff);
                min-width: 32px;
                text-align: right;
            }

            .infuse-buff .infuse-timer.low {
                color: #e74c3c;
                animation: timerPulse 0.5s infinite;
            }

            @keyframes timerPulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.4; }
            }

            /* ========== INFUSE EXPIRED NOTIFICATION ========== */
            .infuse-expired-notif {
                position: fixed;
                top: 35%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.85);
                border: 2px solid #e74c3c;
                border-radius: 12px;
                padding: 16px 28px;
                color: #e74c3c;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                z-index: 19000;
                animation: expiredFade 2s ease-out forwards;
                pointer-events: none;
            }

            @keyframes expiredFade {
                0% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
                70% { opacity: 1; }
                100% { opacity: 0; transform: translate(-50%, -70%); }
            }

            /* ========== GRAB FAIL POPUP ========== */
            .grab-fail-notif {
                position: fixed;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.8);
                border: 2px solid #e67e22;
                border-radius: 10px;
                padding: 12px 24px;
                color: #e67e22;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                z-index: 19000;
                animation: expiredFade 1.5s ease-out forwards;
                pointer-events: none;
            }

            /* ========== KEYBINDINGS OVERLAY ========== */
            #keybindings-overlay {
                display: none;
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.85);
                z-index: 25000;
                font-family: 'Segoe UI', sans-serif;
                color: white;
                overflow-y: auto;
            }

            #keybindings-overlay.visible { display: flex; align-items: center; justify-content: center; }

            .keybindings-panel {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 2px solid #667eea;
                border-radius: 20px;
                padding: 30px 40px;
                max-width: 700px;
                width: 90%;
                max-height: 85vh;
                overflow-y: auto;
                box-shadow: 0 0 60px rgba(102, 126, 234, 0.3);
                animation: keybindSlideIn 0.3s ease-out;
            }

            @keyframes keybindSlideIn {
                0% { transform: translateY(-30px); opacity: 0; }
                100% { transform: translateY(0); opacity: 1; }
            }

            .keybindings-panel .kb-title {
                font-size: 24px;
                font-weight: 900;
                text-align: center;
                color: #667eea;
                margin-bottom: 20px;
            }

            .keybindings-panel .kb-close-hint {
                text-align: center;
                font-size: 12px;
                color: #666;
                margin-bottom: 16px;
            }

            .kb-section {
                margin-bottom: 18px;
            }

            .kb-section-title {
                font-size: 16px;
                font-weight: bold;
                color: #feca57;
                margin-bottom: 8px;
                padding-bottom: 4px;
                border-bottom: 1px solid rgba(254, 202, 87, 0.3);
            }

            .kb-row {
                display: flex;
                align-items: center;
                padding: 4px 0;
                gap: 12px;
            }

            .kb-key {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 36px;
                height: 28px;
                padding: 0 8px;
                background: linear-gradient(180deg, #444, #333);
                border: 1px solid #666;
                border-bottom: 3px solid #555;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                color: #fff;
                text-align: center;
                font-family: monospace;
            }

            .kb-desc {
                font-size: 13px;
                color: #bbb;
            }

            .kb-divider {
                border: none;
                border-top: 1px solid rgba(255,255,255,0.1);
                margin: 12px 0;
            }
        `;
        document.head.appendChild(style);
    }

    // ==========================================
    // HUD BUTTONS (Floating Fallback - Grab + TIDS)
    // ==========================================

    function createCombatSpecialButtons() {
        if (document.getElementById('combat-special-buttons')) return;

        const container = document.createElement('div');
        container.id = 'combat-special-buttons';
        container.innerHTML = `
            <button id="btn-grab" class="combat-special-btn" title="Greifen (G)">
                <span class="keyhint">G</span>
                <span class="btn-icon">🤼</span>
                <span class="btn-label">Grab</span>
            </button>
            <button id="btn-tids" class="combat-special-btn" title="TIDS - Tritt In Den Schritt (T)">
                <span class="keyhint">T</span>
                <span class="btn-icon">🦵</span>
                <span class="btn-label">TIDS</span>
            </button>
        `;
        document.body.appendChild(container);

        document.getElementById('btn-grab').addEventListener('click', handleGrab);
        document.getElementById('btn-tids').addEventListener('click', handleTIDS);

        // Initial cooldown check fuer TIDS
        updateTIDSCooldownDisplay();
    }

    // ==========================================
    // HUD INTEGRATION (Grab/TIDS/Help in Unified Combat HUD)
    // ==========================================

    function injectIntoUnifiedHUD() {
        const manualActions = document.getElementById('manual-actions');
        if (!manualActions) return;

        // Schon injiziert?
        if (manualActions.querySelector('.hud-special-row')) return;

        // Neue Zeile mit Grab, TIDS, Help Buttons
        const row = document.createElement('div');
        row.className = 'hud-special-row';
        row.innerHTML = `
            <button class="hud-special-btn hud-btn-grab" id="hud-btn-grab" title="Greifen (G)">
                🤼 Grab <span class="key-badge">G</span>
            </button>
            <button class="hud-special-btn hud-btn-tids" id="hud-btn-tids" title="TIDS (T)">
                🦵 TIDS <span class="key-badge">T</span>
            </button>
            <button class="hud-special-btn hud-btn-help" id="hud-btn-help" title="Keybindings (H)">
                📋 Keys <span class="key-badge">H</span>
            </button>
        `;
        manualActions.appendChild(row);

        // Event Listeners
        document.getElementById('hud-btn-grab').addEventListener('click', handleGrab);
        document.getElementById('hud-btn-tids').addEventListener('click', handleTIDS);
        document.getElementById('hud-btn-help').addEventListener('click', toggleKeybindings);

        // Floating Buttons verstecken
        const floating = document.getElementById('combat-special-buttons');
        if (floating) floating.classList.add('hud-integrated');

        // Weapon Hands in Header einfuegen
        injectWeaponHandsIntoHUD();

        console.log('✅ Grab/TIDS/Help in Unified Combat HUD integriert');
    }

    // ==========================================
    // WEAPON HAND DISPLAY (Infuse Glow im HUD)
    // ==========================================

    function injectWeaponHandsIntoHUD() {
        const playerInfo = document.querySelector('.unified-combat-ui .player-info');
        if (!playerInfo) return;

        // Schon da?
        if (playerInfo.querySelector('.weapon-hands-display')) return;

        const handsDiv = document.createElement('div');
        handsDiv.className = 'weapon-hands-display';
        handsDiv.id = 'weapon-hands-display';
        handsDiv.innerHTML = `
            <div class="weapon-hand-slot" id="weapon-hand-L" data-hand="left">
                <span class="hand-label">L</span>
                <span class="weapon-icon">⚔️</span>
                <span class="weapon-name">Leer</span>
                <span class="infuse-badge" id="infuse-badge-L"></span>
            </div>
            <div class="weapon-hand-slot" id="weapon-hand-R" data-hand="right">
                <span class="hand-label">R</span>
                <span class="weapon-icon">⚔️</span>
                <span class="weapon-name">Leer</span>
                <span class="infuse-badge" id="infuse-badge-R"></span>
            </div>
        `;

        // Nach den combat-meters einfuegen
        const meters = playerInfo.querySelector('.combat-meters');
        if (meters) {
            meters.after(handsDiv);
        } else {
            playerInfo.appendChild(handsDiv);
        }
    }

    function updateWeaponHandsDisplay() {
        const leftSlot = document.getElementById('weapon-hand-L');
        const rightSlot = document.getElementById('weapon-hand-R');
        if (!leftSlot || !rightSlot) return;

        // Aktuelle Waffen von EquipmentCombat holen
        let leftWeapon = null;
        let rightWeapon = null;

        if (window.EquipmentCombat) {
            const equip = window.EquipmentCombat.getEquipped ? window.EquipmentCombat.getEquipped() : null;
            if (equip) {
                leftWeapon = equip.leftHand || equip.left_hand || null;
                rightWeapon = equip.rightHand || equip.right_hand || null;
            }
        }

        // Auch von UnifiedCombat pruefen
        if (window.UnifiedCombat) {
            if (!leftWeapon && window.UnifiedCombat.getHand) {
                leftWeapon = window.UnifiedCombat.getHand('left');
            }
            if (!rightWeapon && window.UnifiedCombat.getHand) {
                rightWeapon = window.UnifiedCombat.getHand('right');
            }
        }

        // Infuse-Daten holen
        let infuses = [];
        if (window.UnifiedCombat && typeof window.UnifiedCombat.getActiveInfuses === 'function') {
            infuses = window.UnifiedCombat.getActiveInfuses();
        }

        // Linke Hand updaten
        updateSingleHand(leftSlot, leftWeapon, infuses, 'left', 'L');
        // Rechte Hand updaten
        updateSingleHand(rightSlot, rightWeapon, infuses, 'right', 'R');
    }

    function updateSingleHand(slot, weapon, infuses, handKey, badgeId) {
        const nameEl = slot.querySelector('.weapon-name');
        const iconEl = slot.querySelector('.weapon-icon');
        const badgeEl = document.getElementById(`infuse-badge-${badgeId}`);

        // Waffen-Name
        if (weapon) {
            const wName = typeof weapon === 'string' ? weapon : (weapon.name || weapon.id || 'Waffe');
            nameEl.textContent = wName;
            iconEl.textContent = getWeaponIcon(weapon);
        } else {
            nameEl.textContent = 'Leer';
            iconEl.textContent = '✋';
        }

        // Infuse-Glow pruefen
        const weaponId = weapon ? (typeof weapon === 'string' ? weapon : (weapon.id || weapon.name || '')) : '';
        const infuse = infuses.find(i =>
            i.weapon === weaponId ||
            i.hand === handKey ||
            i.weapon === handKey
        );

        if (infuse) {
            const color = ELEMENT_COLORS[infuse.element] || '#ffffff';
            slot.classList.add('infused');
            slot.style.setProperty('--infuse-color', color);
            if (badgeEl) {
                badgeEl.textContent = `${infuse.remaining}s`;
                badgeEl.style.background = color;
            }
        } else {
            slot.classList.remove('infused');
            slot.style.removeProperty('--infuse-color');
            if (badgeEl) badgeEl.textContent = '';
        }
    }

    function getWeaponIcon(weapon) {
        if (!weapon) return '✋';
        const type = typeof weapon === 'string' ? weapon.toLowerCase() : (weapon.type || weapon.id || '').toLowerCase();
        if (type.includes('sword') || type.includes('schwert')) return '⚔️';
        if (type.includes('dagger') || type.includes('dolch')) return '🗡️';
        if (type.includes('axe') || type.includes('axt')) return '🪓';
        if (type.includes('hammer')) return '🔨';
        if (type.includes('spear') || type.includes('speer') || type.includes('lance')) return '🔱';
        if (type.includes('staff') || type.includes('stab')) return '🪄';
        if (type.includes('shield') || type.includes('schild')) return '🛡️';
        if (type.includes('bow') || type.includes('bogen')) return '🏹';
        if (type.includes('gun') || type.includes('pistol')) return '🔫';
        if (type.includes('fist') || type.includes('faust') || type.includes('gauntlet')) return '🥊';
        return '⚔️';
    }

    // ==========================================
    // GRAB SYSTEM UI
    // ==========================================

    function createGrabPopup() {
        if (document.getElementById('grab-popup')) return;

        const popup = document.createElement('div');
        popup.id = 'grab-popup';
        popup.innerHTML = `
            <div class="grab-title">🤼 GEGNER GEGRIFFEN!</div>
            <div class="grab-timer">
                <span id="grab-timer-text">5s</span>
                <div class="timer-bar">
                    <div class="timer-fill" id="grab-timer-fill" style="width:100%"></div>
                </div>
            </div>
            <button class="grab-move-btn" data-move="suplex">
                <span class="move-key">1</span> Suplex
                <span class="move-req">Skill 15</span>
            </button>
            <button class="grab-move-btn" data-move="chokeslam">
                <span class="move-key">2</span> Chokeslam
                <span class="move-req">Skill 10</span>
            </button>
            <button class="grab-move-btn" data-move="throw_object">
                <span class="move-key">3</span> In Objekt werfen
                <span class="move-req"></span>
            </button>
            <button class="grab-move-btn" data-move="release">
                <span class="move-key">4</span> Loslassen
                <span class="move-req"></span>
            </button>
        `;
        document.body.appendChild(popup);

        // Click Handler fuer Move-Buttons
        popup.querySelectorAll('.grab-move-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (btn.classList.contains('disabled')) return;
                executeGrabMoveUI(btn.dataset.move);
            });
        });
    }

    function handleGrab() {
        playGrabSound();

        // Versuche ueber Backend API
        tryGrabAPI().then(result => {
            if (result && result.success) {
                showGrabPopup(result.available_moves, result.time_limit || 5);
            } else if (result && !result.success) {
                showGrabFailNotification(result.message || 'Griff verfehlt!');
            }
        }).catch(() => {
            // Fallback: Lokales System
            if (window.EquipmentCombat) {
                const result = window.EquipmentCombat.grab();
                if (result && result.grabbed) {
                    showGrabPopup(result.options, 5);
                } else {
                    showGrabFailNotification('Griff verfehlt!');
                }
            }
        });
    }

    async function tryGrabAPI() {
        try {
            const resp = await fetch(`${API_BASE}/api/combat-magic/grab`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player_id: 'kuja', target_id: 'current_target' })
            });
            if (resp.ok) return await resp.json();
        } catch (e) {
            // API nicht erreichbar
        }
        return null;
    }

    function showGrabPopup(availableMoves, timeLimit) {
        const popup = document.getElementById('grab-popup');
        if (!popup) return;

        uiState.grabPopupVisible = true;
        uiState.grabTimeLeft = timeLimit;
        popup.classList.add('visible');

        // Skill-Requirements pruefen und Buttons disablen
        const skills = window.EquipmentCombat ? window.EquipmentCombat.getSkills() : {};
        const suplexBtn = popup.querySelector('[data-move="suplex"]');
        const chokeslamBtn = popup.querySelector('[data-move="chokeslam"]');

        if (suplexBtn) {
            const suplexLevel = skills.suplex ? skills.suplex.level : 1;
            if (suplexLevel < 15) {
                suplexBtn.classList.add('disabled');
                suplexBtn.querySelector('.move-req').textContent = `Skill ${suplexLevel}/15`;
            } else {
                suplexBtn.classList.remove('disabled');
                suplexBtn.querySelector('.move-req').textContent = `Skill ${suplexLevel}`;
            }
        }

        if (chokeslamBtn) {
            const throwLevel = skills.throw ? skills.throw.level : 1;
            if (throwLevel < 10) {
                chokeslamBtn.classList.add('disabled');
                chokeslamBtn.querySelector('.move-req').textContent = `Skill ${throwLevel}/10`;
            } else {
                chokeslamBtn.classList.remove('disabled');
                chokeslamBtn.querySelector('.move-req').textContent = `Skill ${throwLevel}`;
            }
        }

        // Timer starten
        startGrabTimer(timeLimit);
    }

    function startGrabTimer(seconds) {
        if (uiState.grabTimer) clearInterval(uiState.grabTimer);

        const startTime = Date.now();
        const totalMs = seconds * 1000;

        const timerText = document.getElementById('grab-timer-text');
        const timerFill = document.getElementById('grab-timer-fill');

        uiState.grabTimer = setInterval(() => {
            const elapsed = Date.now() - startTime;
            const remaining = Math.max(0, totalMs - elapsed);
            const sec = Math.ceil(remaining / 1000);

            if (timerText) timerText.textContent = `${sec}s`;
            if (timerFill) timerFill.style.width = `${(remaining / totalMs) * 100}%`;

            if (remaining <= 0) {
                // Zeit abgelaufen - automatisch loslassen
                executeGrabMoveUI('release');
            }
        }, 50);
    }

    function executeGrabMoveUI(move) {
        hideGrabPopup();

        // Versuche Backend API
        fetch(`${API_BASE}/api/combat-magic/grab/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: 'kuja', move: move })
        }).then(r => r.json()).then(result => {
            if (result.success && result.message) {
                console.log(`🤼 ${result.message}`);
            }
        }).catch(() => {
            // Fallback lokal
            if (window.EquipmentCombat) {
                window.EquipmentCombat.executeGrabMove(move);
            }
        });
    }

    function hideGrabPopup() {
        const popup = document.getElementById('grab-popup');
        if (popup) popup.classList.remove('visible');
        uiState.grabPopupVisible = false;
        if (uiState.grabTimer) {
            clearInterval(uiState.grabTimer);
            uiState.grabTimer = null;
        }
    }

    function showGrabFailNotification(message) {
        const notif = document.createElement('div');
        notif.className = 'grab-fail-notif';
        notif.textContent = `🤼 ${message}`;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 1500);
    }

    // ==========================================
    // TIDS SYSTEM UI
    // ==========================================

    function createTIDSPopup() {
        if (document.getElementById('tids-popup')) return;

        const popup = document.createElement('div');
        popup.id = 'tids-popup';
        popup.innerHTML = `
            <div class="tids-icon">🦵🎯</div>
            <div class="tids-title">TIDS! TRITT IN DEN SCHRITT!</div>
            <div class="tids-gag" id="tids-gag-text"></div>
            <div class="tids-stats">
                <span class="tids-stat" id="tids-stat-damage">Schaden: 0</span>
                <span class="tids-stat" id="tids-stat-stun">Stun: 0s</span>
                <span class="tids-stat" id="tids-stat-tag">GAG!</span>
            </div>
        `;
        document.body.appendChild(popup);

        // Klick zum Schliessen
        popup.addEventListener('click', hideTIDSPopup);
    }

    function handleTIDS() {
        // Cooldown Check (lokal)
        if (window.EquipmentCombat) {
            const cooldown = window.EquipmentCombat.getTIDSCooldown();
            if (cooldown > 0) {
                const hours = Math.ceil(cooldown / 3600000);
                showGrabFailNotification(`TIDS Cooldown! Noch ${hours}h`);
                return;
            }
        }

        // Versuche Backend API (hat lustige gag_messages!)
        tryTIDSAPI().then(result => {
            if (result && result.success) {
                showTIDSPopup(result);
            } else if (result && !result.success) {
                showGrabFailNotification(result.message || 'TIDS fehlgeschlagen!');
            }
        }).catch(() => {
            // Fallback: Lokales System
            if (window.EquipmentCombat) {
                const result = window.EquipmentCombat.useTIDS('humanoid');
                if (result) {
                    showTIDSPopup({
                        damage: result.damage,
                        stun_duration: result.stun / 1000,
                        gag_message: 'Der Gegner greift sich zwischen die Beine und taumelt verwirrt!',
                        flee_bonus: result.fleeBonus
                    });
                }
            }
        });
    }

    async function tryTIDSAPI() {
        try {
            const resp = await fetch(`${API_BASE}/api/combat-magic/tids`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: 'kuja',
                    target_type: 'humanoid',
                    target_name: 'Gegner',
                    is_boss: false
                })
            });
            if (resp.ok) return await resp.json();
        } catch (e) {
            // API nicht erreichbar
        }
        return null;
    }

    function showTIDSPopup(data) {
        // TIDS Sound abspielen!
        playTIDSSound();

        const popup = document.getElementById('tids-popup');
        if (!popup) return;

        const gagText = document.getElementById('tids-gag-text');
        const dmgStat = document.getElementById('tids-stat-damage');
        const stunStat = document.getElementById('tids-stat-stun');

        if (gagText) gagText.textContent = `"${data.gag_message || 'AUTSCH!'}"`;
        if (dmgStat) dmgStat.textContent = `Schaden: ${data.damage || 0}`;
        if (stunStat) stunStat.textContent = `Stun: ${data.stun_duration || 0}s`;

        popup.classList.add('visible');
        uiState.tidsPopupVisible = true;

        // TIDS Cooldown-Button updaten
        updateTIDSCooldownDisplay();

        // Auto-Close nach 4 Sekunden
        if (uiState.tidsPopupTimer) clearTimeout(uiState.tidsPopupTimer);
        uiState.tidsPopupTimer = setTimeout(() => {
            hideTIDSPopup();
        }, 4000);
    }

    function hideTIDSPopup() {
        const popup = document.getElementById('tids-popup');
        if (popup) popup.classList.remove('visible');
        uiState.tidsPopupVisible = false;
    }

    function updateTIDSCooldownDisplay() {
        // Floating Button
        updateSingleTIDSButton(document.getElementById('btn-tids'));
        // HUD-integrierter Button
        updateSingleTIDSButton(document.getElementById('hud-btn-tids'));
    }

    function updateSingleTIDSButton(btn) {
        if (!btn) return;

        let cooldown = 0;
        if (window.EquipmentCombat) {
            cooldown = window.EquipmentCombat.getTIDSCooldown();
        }

        // Bestehende Overlay entfernen
        const existing = btn.querySelector('.cooldown-overlay');
        if (existing) existing.remove();

        if (cooldown > 0) {
            btn.classList.add('on-cooldown');
            const hours = Math.ceil(cooldown / 3600000);
            const overlay = document.createElement('span');
            overlay.className = 'cooldown-overlay';
            overlay.textContent = `${hours}h`;
            btn.appendChild(overlay);
        } else {
            btn.classList.remove('on-cooldown');
        }
    }

    // ==========================================
    // INFUSE DISPLAY
    // ==========================================

    function createInfuseDisplay() {
        if (document.getElementById('infuse-display')) return;

        const display = document.createElement('div');
        display.id = 'infuse-display';
        document.body.appendChild(display);
    }

    function startInfuseUpdateLoop() {
        if (uiState.infuseUpdateInterval) clearInterval(uiState.infuseUpdateInterval);

        uiState.infuseUpdateInterval = setInterval(() => {
            updateInfuseDisplay();
            updateWeaponHandsDisplay();
        }, 500);

        // TIDS seltener updaten
        setInterval(updateTIDSCooldownDisplay, 60000);
    }

    // Merke vorherige Infuses um Ablauf zu erkennen
    let previousInfuseWeapons = new Set();

    function updateInfuseDisplay() {
        const display = document.getElementById('infuse-display');
        if (!display) return;

        let infuses = [];

        // Von UnifiedCombat holen
        if (window.UnifiedCombat && typeof window.UnifiedCombat.getActiveInfuses === 'function') {
            infuses = window.UnifiedCombat.getActiveInfuses();
        }

        // Ablauf-Check
        const currentWeapons = new Set(infuses.map(i => i.weapon));
        for (const prev of previousInfuseWeapons) {
            if (!currentWeapons.has(prev)) {
                showInfuseExpiredNotification(prev);
                playInfuseExpiredSound();
            }
        }
        previousInfuseWeapons = currentWeapons;

        // Keine Infuses -> Display verstecken
        if (infuses.length === 0) {
            display.innerHTML = '';
            return;
        }

        // Infuse-Buffs rendern
        display.innerHTML = infuses.map(infuse => {
            const color = ELEMENT_COLORS[infuse.element] || '#ffffff';
            const name = ELEMENT_NAMES[infuse.element] || infuse.element;
            const icon = ELEMENT_ICONS[infuse.element] || '⚔️';
            const bonusPct = Math.round(infuse.bonus * 100);
            const isLow = infuse.remaining <= 5;

            return `
                <div class="infuse-buff" style="--infuse-color: ${color}; --infuse-glow: ${color}40;">
                    <div class="infuse-icon" style="--infuse-color: ${color}">${icon}</div>
                    <div class="infuse-info">
                        <div class="infuse-name">${name}-${infuse.weapon}</div>
                        <div class="infuse-bonus">+${bonusPct}% ${name}-Schaden</div>
                    </div>
                    <div class="infuse-timer ${isLow ? 'low' : ''}">${infuse.remaining}s</div>
                </div>
            `;
        }).join('');
    }

    function showInfuseExpiredNotification(weaponId) {
        const notif = document.createElement('div');
        notif.className = 'infuse-expired-notif';
        notif.textContent = `⏱️ Infuse abgelaufen! (${weaponId})`;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 2000);
    }

    // ==========================================
    // KEYBINDINGS OVERLAY (H / F1)
    // ==========================================

    function createKeybindingsOverlay() {
        if (document.getElementById('keybindings-overlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'keybindings-overlay';
        overlay.innerHTML = `
            <div class="keybindings-panel">
                <div class="kb-title">🎮 COMBAT KEYBINDINGS</div>
                <div class="kb-close-hint">Druecke H, F1 oder Escape zum Schliessen</div>

                <div class="kb-section">
                    <div class="kb-section-title">⚔️ Nahkampf</div>
                    <div class="kb-row"><span class="kb-key">Q</span> <span class="kb-desc">Leichter Angriff (Links)</span></div>
                    <div class="kb-row"><span class="kb-key">E</span> <span class="kb-desc">Leichter Angriff (Rechts)</span></div>
                    <div class="kb-row"><span class="kb-key">R</span> <span class="kb-desc">Leichter Angriff (Beide)</span></div>
                    <div class="kb-row"><span class="kb-key">A</span> <span class="kb-desc">Schwerer Angriff (Links)</span></div>
                    <div class="kb-row"><span class="kb-key">D</span> <span class="kb-desc">Schwerer Angriff (Rechts)</span></div>
                    <div class="kb-row"><span class="kb-key">F</span> <span class="kb-desc">Schwerer Angriff (Beide)</span></div>
                </div>

                <hr class="kb-divider">

                <div class="kb-section">
                    <div class="kb-section-title">🛡️ Defensive</div>
                    <div class="kb-row"><span class="kb-key">Space</span> <span class="kb-desc">Ausweichen (Dodge)</span></div>
                    <div class="kb-row"><span class="kb-key">Shift</span> <span class="kb-desc">Parieren (Parry)</span></div>
                </div>

                <hr class="kb-divider">

                <div class="kb-section">
                    <div class="kb-section-title">🔮 Magie</div>
                    <div class="kb-row"><span class="kb-key">1</span> <span class="kb-desc">Spell Slot 1 (Feuer)</span></div>
                    <div class="kb-row"><span class="kb-key">2</span> <span class="kb-desc">Spell Slot 2 (Eis)</span></div>
                    <div class="kb-row"><span class="kb-key">3</span> <span class="kb-desc">Spell Slot 3 (Heilung)</span></div>
                    <div class="kb-row"><span class="kb-key">4</span> <span class="kb-desc">Spell Slot 4 (EXPLOSION!)</span></div>
                </div>

                <hr class="kb-divider">

                <div class="kb-section">
                    <div class="kb-section-title">🤼 Spezial-Moves</div>
                    <div class="kb-row"><span class="kb-key">G</span> <span class="kb-desc">Grab (Gegner greifen)</span></div>
                    <div class="kb-row"><span class="kb-key">T</span> <span class="kb-desc">TIDS - Tritt In Den Schritt (24h CD)</span></div>
                    <div class="kb-row"><span class="kb-key">X</span> <span class="kb-desc">Finisher (wenn Leiste voll)</span></div>
                    <div class="kb-row"><span class="kb-key">V</span> <span class="kb-desc">Wall Jump</span></div>
                    <div class="kb-row"><span class="kb-key">B</span> <span class="kb-desc">Barrel Throw</span></div>
                </div>

                <hr class="kb-divider">

                <div class="kb-section">
                    <div class="kb-section-title">🤼 Grab-Moves (im Grab-Popup)</div>
                    <div class="kb-row"><span class="kb-key">1</span> <span class="kb-desc">Suplex (Skill 15+)</span></div>
                    <div class="kb-row"><span class="kb-key">2</span> <span class="kb-desc">Chokeslam (Skill 10+)</span></div>
                    <div class="kb-row"><span class="kb-key">3</span> <span class="kb-desc">In Objekt werfen</span></div>
                    <div class="kb-row"><span class="kb-key">4</span> <span class="kb-desc">Loslassen</span></div>
                    <div class="kb-row"><span class="kb-key">Esc</span> <span class="kb-desc">Grab-Popup schliessen</span></div>
                </div>

                <hr class="kb-divider">

                <div class="kb-section">
                    <div class="kb-section-title">📋 UI</div>
                    <div class="kb-row"><span class="kb-key">H</span> <span class="kb-desc">Diese Hilfe anzeigen/verstecken</span></div>
                    <div class="kb-row"><span class="kb-key">F1</span> <span class="kb-desc">Diese Hilfe anzeigen/verstecken</span></div>
                    <div class="kb-row"><span class="kb-key">Esc</span> <span class="kb-desc">Popups schliessen</span></div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // Klick auf Background schliesst Overlay
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) toggleKeybindings();
        });
    }

    function toggleKeybindings() {
        const overlay = document.getElementById('keybindings-overlay');
        if (!overlay) return;

        uiState.keybindingsVisible = !uiState.keybindingsVisible;
        overlay.classList.toggle('visible', uiState.keybindingsVisible);
    }

    // ==========================================
    // KEYBINDINGS (G=Grab, T=TIDS, H=Help)
    // ==========================================

    function setupKeybindings() {
        document.addEventListener('keydown', (e) => {
            // Ignoriere wenn Input fokussiert
            if (window.chatInputFocused) return;
            const active = document.activeElement;
            if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.isContentEditable)) return;

            // Keybindings Overlay Toggle
            if (e.code === 'KeyH' || e.code === 'F1') {
                // Nicht wenn Grab-Popup offen (H koennte ungewollt sein)
                if (!uiState.grabPopupVisible) {
                    toggleKeybindings();
                    e.preventDefault();
                    return;
                }
            }

            // Escape schliesst alles
            if (e.code === 'Escape') {
                if (uiState.keybindingsVisible) {
                    toggleKeybindings();
                    e.preventDefault();
                    return;
                }
                if (uiState.grabPopupVisible) {
                    hideGrabPopup();
                    e.preventDefault();
                    return;
                }
                if (uiState.tidsPopupVisible) {
                    hideTIDSPopup();
                    e.preventDefault();
                    return;
                }
                return;
            }

            // Keybindings-Overlay offen? Keine weiteren Actions
            if (uiState.keybindingsVisible) return;

            // Grab Popup Move-Auswahl (1-4)
            if (uiState.grabPopupVisible) {
                switch (e.code) {
                    case 'Digit1': executeGrabMoveUI('suplex'); e.preventDefault(); return;
                    case 'Digit2': executeGrabMoveUI('chokeslam'); e.preventDefault(); return;
                    case 'Digit3': executeGrabMoveUI('throw_object'); e.preventDefault(); return;
                    case 'Digit4': executeGrabMoveUI('release'); e.preventDefault(); return;
                }
            }

            // G = Grab (nur wenn kein Grab-Popup offen)
            if (e.code === 'KeyG' && !uiState.grabPopupVisible) {
                handleGrab();
                e.preventDefault();
                return;
            }

            // T = TIDS
            if (e.code === 'KeyT' && !uiState.tidsPopupVisible) {
                handleTIDS();
                e.preventDefault();
                return;
            }
        });
    }

    // ==========================================
    // INIT
    // ==========================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // Kurz warten damit andere Systeme zuerst laden
        setTimeout(init, 500);
    }

    // Public API
    window.CombatSpecialUI = {
        showGrabPopup,
        hideGrabPopup,
        showTIDSPopup,
        hideTIDSPopup,
        updateInfuseDisplay,
        updateTIDSCooldownDisplay,
        updateWeaponHandsDisplay,
        toggleKeybindings,
        playTIDSSound,
        playGrabSound,
        injectIntoUnifiedHUD
    };

    console.log('🎮 Combat Special UI V2 loaded (Grab/TIDS/Infuse/Glow/Sound/Keys)');
})();
