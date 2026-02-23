// =============================================================================
// COMBAT INPUT HANDLER - Equipment-based Attack System
// =============================================================================

class CombatInputHandler {
    constructor(commandSystem) {
        this.cs = commandSystem;
        this.comboBuffer = [];
        this.comboTimeout = null;
        this.pressedKeys = new Set();
        this.blockHeld = false;

        // Direction Resolver starten
        if (window.DirectionResolver) {
            window.DirectionResolver.init();
        }

        this.setupKeyboardControls();
        this.setupMouseControls();

        console.log('[CombatInput] Initialized (DirectionResolver aktiv)');
    }

    setupKeyboardControls() {
        document.addEventListener('keydown', (e) => {
            // WICHTIG: Ignorieren wenn Chat-Input oder andere Input-Felder fokussiert sind
            if (window.chatInputFocused ||
                e.target.tagName === 'INPUT' ||
                e.target.tagName === 'TEXTAREA' ||
                e.target.isContentEditable) {
                return;
            }

            this.pressedKeys.add(e.code);

            switch(e.code) {
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
                    break

;

                // Parry
                case 'Space':
                    if (e.shiftKey) {
                        this.parry();
                    } else {
                        this.block();
                    }
                    break;
            }
        });

        document.addEventListener('keyup', (e) => {
            this.pressedKeys.delete(e.code);
        });
    }

    setupMouseControls() {
        document.addEventListener('mousedown', (e) => {
            if (e.button === 0) { // Linksklick = Angriff mit Richtung
                this._attackWithDirection('right', 'light');
            } else if (e.button === 2) { // Rechtsklick
                if (e.shiftKey) {
                    this._attackWithDirection('left', 'light');
                } else {
                    this.blockHeld = true;
                    this.block();
                }
            }
        });

        document.addEventListener('mouseup', (e) => {
            if (e.button === 2) {
                this.blockHeld = false;
            }
        });

        // Prevent context menu on right click
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }

    // Angriff MIT Richtungs-Erkennung (For Honor Style)
    _attackWithDirection(hand, type) {
        const DR = window.DirectionResolver;
        if (!DR) {
            // Fallback ohne DirectionResolver
            this.attack(hand, type, DR ? DR.DIR.NEUTRAL : 'neutral');
            return;
        }
        // Capture starten: sammelt Maus-Delta, gibt Richtung zurueck
        DR.startAttackCapture((direction) => {
            this.attack(hand, type, direction);
        });
    }

    isKeyPressed(keyCode) {
        return this.pressedKeys.has(keyCode);
    }

    attack(hand, type, direction = 'neutral') {
        const result = this.cs.executeAttack(hand, type);
        if (result.success) {
            this.addToCombo(type);
            this.triggerAttackAnimation(hand, type, result, direction);
            console.log(`[Combat] ${hand} ${type} [${direction.toUpperCase()}]: ${result.damage} damage (${result.weapon})`);

            // Schadenszahlen nur in Orbit-Cam anzeigen
            const camMode = window.Scene3D?.getCameraMode?.() || 'orbit';
            if (camMode === 'orbit') {
                this.showDamageNumber(result.damage, result.element);
            }
        } else {
            if (result.reason === 'cooldown') {
                console.log(`[Combat] Cooldown! Wait ${Math.ceil(result.remaining / 100) / 10}s`);
            }
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
            console.log(`[Combat] COMBO: ${combo.name}! Multiplier: x${combo.multiplier}`);
            this.showComboNotification(combo);
        }
    }

    executeWeave() {
        const result = this.cs.executeWeave();
        if (result.success) {
            console.log(`[Combat] WEAVE: ${result.weave.name}! ${result.weave.damage} damage`);
            this.showWeaveEffect(result.weave);
        } else {
            console.log(`[Combat] Weave failed: ${result.message || result.reason}`);
        }
    }

    block() {
        // ⚔️ Richtungs-Block: Maus-Richtung beim Drücken bestimmt Block-Zone
        const blockDir = this.getBlockDirection();
        const result = this.cs.executeBlock(blockDir);
        if (result && result.success) {
            console.log(`[Combat] BLOCK [${blockDir.toUpperCase()}]: ${result.type} (${result.blockValue}% reduction)`);
            this.showBlockEffect(result);
        } else if (result) {
            console.log(`[Combat] Block failed: ${result.reason}`);
        }
    }

    parry() {
        const result = this.cs.executeParry();
        if (result.success) {
            console.log(`[Combat] PARRY WINDOW: ${result.parryWindow}ms`);
            this.showParryWindow(result);
        }
    }

    // Animation Trigger - jetzt MIT Richtung
    triggerAttackAnimation(hand, type, result, direction = 'neutral') {
        if (window.Scene3D && window.Scene3D.triggerAttackAnimation) {
            window.Scene3D.triggerAttackAnimation({
                hand:      hand,
                type:      type,
                weapon:    result.weapon,
                element:   result.element,
                direction: direction   // NEU: OBEN/UNTEN/LINKS/RECHTS/neutral
            });
        }
    }

    // Block-Richtung abfragen (fuer Directional Block)
    getBlockDirection() {
        if (window.DirectionResolver) {
            return window.DirectionResolver.getBlockDirection();
        }
        return 'neutral';
    }

    // UI Feedback
    showDamageNumber(damage, element) {
        const dmgNum = document.createElement('div');
        dmgNum.className = 'damage-number';
        dmgNum.textContent = damage;
        dmgNum.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 48px;
            font-weight: bold;
            color: ${element === 'fire' ? '#FF4444' : element === 'ice' ? '#4444FF' : '#FFD700'};
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
            pointer-events: none;
            z-index: 10000;
            animation: damageFloat 0.8s ease-out forwards;
        `;
        document.body.appendChild(dmgNum);
        setTimeout(() => dmgNum.remove(), 800);
    }

    showComboNotification(combo) {
        const notification = document.createElement('div');
        notification.className = 'combo-notification';
        notification.innerHTML = `
            <span class="combo-name">${combo.name}</span>
            <span class="combo-bonus">x${combo.multiplier}</span>
        `;
        notification.style.cssText = `
            position: fixed;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(90deg, #FFD700, #FFA500);
            color: #000;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            z-index: 10000;
            animation: comboSlide 1.5s ease-out forwards;
        `;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 1500);
    }

    showWeaveEffect(weave) {
        const effect = document.createElement('div');
        effect.className = 'weave-effect';
        effect.innerHTML = `⚡ ${weave.name} ⚡`;
        effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 36px;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 0 0 20px #FFD700;
            z-index: 10000;
            animation: weaveExplosion 2s ease-out forwards;
        `;
        document.body.appendChild(effect);
        setTimeout(() => effect.remove(), 2000);
    }

    showBlockEffect(result) {
        const effect = document.createElement('div');
        effect.className = 'block-effect';
        effect.textContent = '🛡️ BLOCK';
        effect.style.cssText = `
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translateX(-50%);
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
            text-shadow: 0 0 10px #4CAF50;
            z-index: 10000;
            animation: blockFlash 0.5s ease-out forwards;
        `;
        document.body.appendChild(effect);
        setTimeout(() => effect.remove(), 500);
    }

    showParryWindow(result) {
        const effect = document.createElement('div');
        effect.className = 'parry-window';
        effect.textContent = '⚡ PARRY READY';
        effect.style.cssText = `
            position: fixed;
            top: 35%;
            left: 50%;
            transform: translateX(-50%);
            font-size: 28px;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 0 0 15px #FFD700;
            z-index: 10000;
            animation: parryPulse ${result.parryWindow}ms ease-out forwards;
        `;
        document.body.appendChild(effect);
        setTimeout(() => effect.remove(), result.parryWindow);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes damageFloat {
        0% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(0.5);
        }
        50% {
            opacity: 1;
            transform: translate(-50%, -70%) scale(1.2);
        }
        100% {
            opacity: 0;
            transform: translate(-50%, -100%) scale(0.8);
        }
    }

    @keyframes comboSlide {
        0% {
            opacity: 0;
            transform: translateX(-50%) translateY(-50px);
        }
        20% {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        80% {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        100% {
            opacity: 0;
            transform: translateX(-50%) translateY(30px);
        }
    }

    @keyframes weaveExplosion {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.3);
        }
        20% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.5);
        }
        80% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.2);
        }
        100% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(2);
        }
    }

    @keyframes blockFlash {
        0% {
            opacity: 1;
            transform: translateX(-50%) scale(1);
        }
        50% {
            opacity: 1;
            transform: translateX(-50%) scale(1.2);
        }
        100% {
            opacity: 0;
            transform: translateX(-50%) scale(0.8);
        }
    }

    @keyframes parryPulse {
        0%, 100% {
            opacity: 0;
            transform: translateX(-50%) scale(0.9);
        }
        50% {
            opacity: 1;
            transform: translateX(-50%) scale(1.1);
        }
    }
`;
document.head.appendChild(style);
