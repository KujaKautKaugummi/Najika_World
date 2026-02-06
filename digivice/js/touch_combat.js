/**
 * NAJIKA TOUCH COMBAT CONTROLS
 * Mobile-optimierte Touch-Steuerung für Combat
 *
 * Features:
 * - Virtueller Joystick (links) für Bewegung
 * - Virtuelle Buttons (rechts) für Angriffe
 * - Swipe für Dodge
 * - Hold für Block
 * - Double-Tap für Heavy Attack
 */

(function() {
    'use strict';

    // ===== CONFIGURATION =====
    const CONFIG = {
        joystick: {
            size: 120,
            innerSize: 50,
            deadzone: 0.1,
            position: { bottom: 80, left: 40 }
        },
        buttons: {
            size: 70,
            spacing: 15,
            position: { bottom: 80, right: 40 }
        },
        swipe: {
            minDistance: 50,
            maxTime: 300
        },
        doubleTap: {
            maxDelay: 300
        }
    };

    // ===== STATE =====
    const state = {
        joystick: {
            active: false,
            startX: 0,
            startY: 0,
            currentX: 0,
            currentY: 0,
            angle: 0,
            magnitude: 0
        },
        buttons: {
            attackLeft: false,
            attackRight: false,
            magic: false,
            block: false,
            dodge: false,
            grab: false,
            parry: false
        },
        combinedAttack: {
            leftPressed: false,
            rightPressed: false,
            timeWindow: 100 // ms für gleichzeitige Erkennung
        },
        lastTap: {
            attackLeft: 0,
            attackRight: 0,
            magic: 0
        },
        swipeStart: null
    };

    // ===== UI ELEMENTS =====
    let joystickOuter = null;
    let joystickInner = null;
    let attackLeftBtn = null;
    let attackRightBtn = null;
    let magicBtn = null;
    let blockBtn = null;
    let dodgeBtn = null;
    let grabBtn = null;
    let parryBtn = null;
    let controlsContainer = null;

    // ===== INITIALIZATION =====

    function init() {
        // Nur auf Touch-Geräten aktivieren
        if (!isTouchDevice()) {
            console.log('📱 Touch Controls: Desktop erkannt, überspringe');
            return;
        }

        createTouchUI();
        setupEventListeners();
        console.log('📱 Touch Combat Controls initialized');
    }

    function isTouchDevice() {
        return ('ontouchstart' in window) ||
               (navigator.maxTouchPoints > 0) ||
               (navigator.msMaxTouchPoints > 0) ||
               window.innerWidth <= 1024; // Auch für kleine Screens
    }

    function createTouchUI() {
        // Container
        controlsContainer = document.createElement('div');
        controlsContainer.id = 'touch-controls';
        controlsContainer.innerHTML = `
            <!-- JOYSTICK (Links) -->
            <div class="joystick-container" id="joystick-container">
                <div class="joystick-outer" id="joystick-outer">
                    <div class="joystick-inner" id="joystick-inner"></div>
                </div>
            </div>

            <!-- BUTTONS (Rechts) -->
            <div class="touch-buttons" id="touch-buttons">
                <button class="touch-btn attack-left" id="btn-attack-left">⚔️<span class="hand-label">L</span></button>
                <button class="touch-btn attack-right" id="btn-attack-right">⚔️<span class="hand-label">R</span></button>
                <button class="touch-btn magic" id="btn-magic">🔮</button>
                <button class="touch-btn block" id="btn-block">🛡️</button>
                <button class="touch-btn grab" id="btn-grab">👊</button>
                <button class="touch-btn parry" id="btn-parry">⚡</button>
            </div>

            <!-- SWIPE AREA (Mitte) -->
            <div class="swipe-area" id="swipe-area"></div>
        `;

        // Styles
        const style = document.createElement('style');
        style.id = 'touch-controls-style';
        style.textContent = `
            #touch-controls {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
                touch-action: none;
            }

            /* JOYSTICK */
            .joystick-container {
                position: absolute;
                bottom: ${CONFIG.joystick.position.bottom}px;
                left: ${CONFIG.joystick.position.left}px;
                pointer-events: auto;
            }

            .joystick-outer {
                width: ${CONFIG.joystick.size}px;
                height: ${CONFIG.joystick.size}px;
                background: rgba(255, 255, 255, 0.2);
                border: 3px solid rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                touch-action: none;
            }

            .joystick-inner {
                width: ${CONFIG.joystick.innerSize}px;
                height: ${CONFIG.joystick.innerSize}px;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 50%;
                transition: transform 0.05s ease-out;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            }

            /* BUTTONS */
            .touch-buttons {
                position: absolute;
                bottom: ${CONFIG.buttons.position.bottom}px;
                right: ${CONFIG.buttons.position.right}px;
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                grid-template-rows: repeat(3, 1fr);
                gap: ${CONFIG.buttons.spacing}px;
                pointer-events: auto;
            }

            /* Grab and Parry buttons in bottom row */
            #btn-grab,
            #btn-parry {
                /* Normal size, no spanning */
            }

            .touch-btn {
                width: ${CONFIG.buttons.size}px;
                height: ${CONFIG.buttons.size}px;
                border-radius: 50%;
                border: 3px solid rgba(255, 255, 255, 0.6);
                background: rgba(0, 0, 0, 0.4);
                font-size: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                touch-action: manipulation;
                user-select: none;
                -webkit-user-select: none;
                transition: transform 0.1s, background 0.1s;
            }

            .touch-btn:active, .touch-btn.active {
                transform: scale(0.9);
                background: rgba(255, 255, 255, 0.3);
            }

            .touch-btn.attack-left,
            .touch-btn.attack-right {
                border-color: #ff6b6b;
                background: rgba(255, 107, 107, 0.3);
                position: relative;
            }

            .hand-label {
                position: absolute;
                bottom: 2px;
                right: 4px;
                font-size: 10px;
                font-weight: bold;
                color: rgba(255, 255, 255, 0.8);
                text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
            }

            .touch-btn.magic {
                border-color: #4ecdc4;
                background: rgba(78, 205, 196, 0.3);
            }

            .touch-btn.block {
                border-color: #ffe66d;
                background: rgba(255, 230, 109, 0.3);
            }

            .touch-btn.grab {
                border-color: #ff9f43;
                background: rgba(255, 159, 67, 0.3);
            }

            .touch-btn.parry {
                border-color: #f368e0;
                background: rgba(243, 104, 224, 0.3);
            }

            /* SWIPE AREA */
            .swipe-area {
                position: absolute;
                top: 20%;
                left: 25%;
                width: 50%;
                height: 60%;
                pointer-events: auto;
                /* Debug: border: 1px dashed red; */
            }

            /* Mobile Optimizations */
            @media (max-width: 600px) {
                .joystick-outer {
                    width: 100px;
                    height: 100px;
                }
                .joystick-inner {
                    width: 40px;
                    height: 40px;
                }
                .touch-btn {
                    width: 60px;
                    height: 60px;
                    font-size: 24px;
                }
            }

            /* Landscape Mode */
            @media (orientation: landscape) and (max-height: 500px) {
                .joystick-container {
                    bottom: 20px;
                    left: 20px;
                }
                .touch-buttons {
                    bottom: 20px;
                    right: 20px;
                }
                .joystick-outer {
                    width: 80px;
                    height: 80px;
                }
                .touch-btn {
                    width: 50px;
                    height: 50px;
                    font-size: 20px;
                }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(controlsContainer);

        // Get element references
        joystickOuter = document.getElementById('joystick-outer');
        joystickInner = document.getElementById('joystick-inner');
        attackLeftBtn = document.getElementById('btn-attack-left');
        attackRightBtn = document.getElementById('btn-attack-right');
        magicBtn = document.getElementById('btn-magic');
        blockBtn = document.getElementById('btn-block');
        dodgeBtn = document.getElementById('btn-dodge');
        grabBtn = document.getElementById('btn-grab');
        parryBtn = document.getElementById('btn-parry');
    }

    // ===== EVENT LISTENERS =====

    function setupEventListeners() {
        // Joystick Events
        joystickOuter.addEventListener('touchstart', onJoystickStart, { passive: false });
        joystickOuter.addEventListener('touchmove', onJoystickMove, { passive: false });
        joystickOuter.addEventListener('touchend', onJoystickEnd, { passive: false });

        // Button Events
        setupButtonEvents(attackLeftBtn, 'attackLeft', onAttackLeft, onAttackLeftRelease);
        setupButtonEvents(attackRightBtn, 'attackRight', onAttackRight, onAttackRightRelease);
        setupButtonEvents(magicBtn, 'magic', onMagic);
        setupButtonEvents(blockBtn, 'block', onBlockStart, onBlockEnd);
        setupButtonEvents(dodgeBtn, 'dodge', onDodge);
        setupButtonEvents(grabBtn, 'grab', onGrab);
        setupButtonEvents(parryBtn, 'parry', onParry);

        // Swipe Area Events
        const swipeArea = document.getElementById('swipe-area');
        swipeArea.addEventListener('touchstart', onSwipeStart, { passive: false });
        swipeArea.addEventListener('touchend', onSwipeEnd, { passive: false });
    }

    function setupButtonEvents(btn, name, onPress, onRelease = null) {
        btn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            btn.classList.add('active');
            state.buttons[name] = true;
            if (onPress) onPress(e);
        }, { passive: false });

        btn.addEventListener('touchend', (e) => {
            e.preventDefault();
            btn.classList.remove('active');
            state.buttons[name] = false;
            if (onRelease) onRelease(e);
        }, { passive: false });
    }

    // ===== JOYSTICK HANDLERS =====

    function onJoystickStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const rect = joystickOuter.getBoundingClientRect();

        state.joystick.active = true;
        state.joystick.startX = rect.left + rect.width / 2;
        state.joystick.startY = rect.top + rect.height / 2;

        updateJoystick(touch.clientX, touch.clientY);
    }

    function onJoystickMove(e) {
        e.preventDefault();
        if (!state.joystick.active) return;

        const touch = e.touches[0];
        updateJoystick(touch.clientX, touch.clientY);
    }

    function onJoystickEnd(e) {
        e.preventDefault();
        state.joystick.active = false;
        state.joystick.currentX = 0;
        state.joystick.currentY = 0;
        state.joystick.magnitude = 0;

        joystickInner.style.transform = 'translate(0, 0)';

        // Emit stop movement event
        emitEvent('touchMove', { x: 0, y: 0, magnitude: 0 });
    }

    function updateJoystick(touchX, touchY) {
        const maxDistance = CONFIG.joystick.size / 2 - CONFIG.joystick.innerSize / 2;

        let deltaX = touchX - state.joystick.startX;
        let deltaY = touchY - state.joystick.startY;

        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        const angle = Math.atan2(deltaY, deltaX);

        // Clamp to circle
        if (distance > maxDistance) {
            deltaX = Math.cos(angle) * maxDistance;
            deltaY = Math.sin(angle) * maxDistance;
        }

        state.joystick.currentX = deltaX / maxDistance;
        state.joystick.currentY = deltaY / maxDistance;
        state.joystick.angle = angle;
        state.joystick.magnitude = Math.min(distance / maxDistance, 1);

        // Apply deadzone
        if (state.joystick.magnitude < CONFIG.joystick.deadzone) {
            state.joystick.magnitude = 0;
            state.joystick.currentX = 0;
            state.joystick.currentY = 0;
        }

        // Update visual
        joystickInner.style.transform = `translate(${deltaX}px, ${deltaY}px)`;

        // Emit movement event
        emitEvent('touchMove', {
            x: state.joystick.currentX,
            y: state.joystick.currentY,
            magnitude: state.joystick.magnitude,
            angle: state.joystick.angle
        });
    }

    // ===== BUTTON HANDLERS =====

    function onAttackLeft(e) {
        state.combinedAttack.leftPressed = Date.now();

        // Check if right button is also pressed (within time window)
        if (state.combinedAttack.rightPressed &&
            (state.combinedAttack.leftPressed - state.combinedAttack.rightPressed) < state.combinedAttack.timeWindow) {
            // COMBINED ATTACK!
            onCombinedAttack();
            return;
        }

        const now = Date.now();
        const isDoubleTap = (now - state.lastTap.attackLeft) < CONFIG.doubleTap.maxDelay;
        state.lastTap.attackLeft = now;

        if (isDoubleTap) {
            // Heavy Attack Left Hand
            emitEvent('touchAttack', { type: 'heavy', hand: 'left' });
            console.log('⚔️ Heavy Attack LEFT (Double Tap)');
        } else {
            // Light Attack Left Hand
            emitEvent('touchAttack', { type: 'light', hand: 'left' });
            console.log('⚔️ Light Attack LEFT');
        }
    }

    function onAttackLeftRelease(e) {
        state.combinedAttack.leftPressed = false;
    }

    function onAttackRight(e) {
        state.combinedAttack.rightPressed = Date.now();

        // Check if left button is also pressed (within time window)
        if (state.combinedAttack.leftPressed &&
            (state.combinedAttack.rightPressed - state.combinedAttack.leftPressed) < state.combinedAttack.timeWindow) {
            // COMBINED ATTACK!
            onCombinedAttack();
            return;
        }

        const now = Date.now();
        const isDoubleTap = (now - state.lastTap.attackRight) < CONFIG.doubleTap.maxDelay;
        state.lastTap.attackRight = now;

        if (isDoubleTap) {
            // Heavy Attack Right Hand
            emitEvent('touchAttack', { type: 'heavy', hand: 'right' });
            console.log('⚔️ Heavy Attack RIGHT (Double Tap)');
        } else {
            // Light Attack Right Hand
            emitEvent('touchAttack', { type: 'light', hand: 'right' });
            console.log('⚔️ Light Attack RIGHT');
        }
    }

    function onAttackRightRelease(e) {
        state.combinedAttack.rightPressed = false;
    }

    function onCombinedAttack() {
        // Reset states to prevent double-triggering
        state.combinedAttack.leftPressed = false;
        state.combinedAttack.rightPressed = false;

        // SPACE equivalent - BOTH HANDS ATTACK!
        emitEvent('touchAttack', { type: 'combined', hand: 'both' });
        console.log('💥 COMBINED ATTACK! (BOTH HANDS)');

        // Visual feedback
        attackLeftBtn.classList.add('active');
        attackRightBtn.classList.add('active');
        setTimeout(() => {
            attackLeftBtn.classList.remove('active');
            attackRightBtn.classList.remove('active');
        }, 200);
    }

    function onMagic(e) {
        const now = Date.now();
        const isDoubleTap = (now - state.lastTap.magic) < CONFIG.doubleTap.maxDelay;
        state.lastTap.magic = now;

        if (isDoubleTap) {
            // Heavy Magic
            emitEvent('touchAttack', { type: 'heavy', hand: 'left' });
            console.log('🔮 Heavy Magic (Double Tap)');
        } else {
            // Light Magic
            emitEvent('touchAttack', { type: 'light', hand: 'left' });
            console.log('🔮 Light Magic');
        }
    }

    function onBlockStart(e) {
        emitEvent('touchBlock', { active: true });
        console.log('🛡️ Block Start');
    }

    function onBlockEnd(e) {
        emitEvent('touchBlock', { active: false });
        console.log('🛡️ Block End');
    }

    function onDodge(e) {
        emitEvent('touchDodge', { direction: 'back' });
        console.log('🌀 Dodge');
    }

    function onGrab(e) {
        // Emit grab event with context
        // Backend will determine: item pickup, enemy throw, or enemy lift (based on stats)
        emitEvent('touchGrab', {
            action: 'grab',
            context: 'auto' // Backend determines context
        });
        console.log('👊 Grab/Throw');
    }

    function onParry(e) {
        // Parry is timing-based - requires precise timing
        emitEvent('touchParry', {
            action: 'parry',
            timestamp: Date.now() // For timing verification
        });
        console.log('⚡ Parry!');

        // Visual feedback
        parryBtn.style.boxShadow = '0 0 20px rgba(243, 104, 224, 1)';
        setTimeout(() => {
            parryBtn.style.boxShadow = '';
        }, 300);
    }

    // ===== SWIPE HANDLERS =====

    function onSwipeStart(e) {
        const touch = e.touches[0];
        state.swipeStart = {
            x: touch.clientX,
            y: touch.clientY,
            time: Date.now()
        };
    }

    function onSwipeEnd(e) {
        if (!state.swipeStart) return;

        const touch = e.changedTouches[0];
        const deltaX = touch.clientX - state.swipeStart.x;
        const deltaY = touch.clientY - state.swipeStart.y;
        const deltaTime = Date.now() - state.swipeStart.time;

        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

        if (distance >= CONFIG.swipe.minDistance && deltaTime <= CONFIG.swipe.maxTime) {
            // Determine direction
            const angle = Math.atan2(deltaY, deltaX) * 180 / Math.PI;
            let direction = 'back';

            if (angle > -45 && angle <= 45) direction = 'right';
            else if (angle > 45 && angle <= 135) direction = 'back';
            else if (angle > -135 && angle <= -45) direction = 'forward';
            else direction = 'left';

            emitEvent('touchDodge', { direction });
            console.log(`🌀 Swipe Dodge: ${direction}`);
        }

        state.swipeStart = null;
    }

    // ===== EVENT EMISSION =====

    function emitEvent(type, detail) {
        window.dispatchEvent(new CustomEvent(type, { detail }));

        // Direct integration with EquipmentCombat if available
        if (window.EquipmentCombat) {
            switch (type) {
                case 'touchAttack':
                    if (detail.type === 'combined') {
                        // SPACE equivalent - both hands attack
                        window.EquipmentCombat.attackCombined();
                    } else if (detail.type === 'light') {
                        window.EquipmentCombat.attackLight(detail.hand);
                    } else if (detail.type === 'heavy') {
                        window.EquipmentCombat.attackHeavy(detail.hand);
                    }
                    break;
                case 'touchBlock':
                    if (detail.active) {
                        window.EquipmentCombat.block();
                    } else {
                        window.EquipmentCombat.releaseBlock();
                    }
                    break;
                case 'touchDodge':
                    window.EquipmentCombat.dodge(detail.direction);
                    break;
                case 'touchGrab':
                    // Grab/Throw/Lift based on context
                    window.EquipmentCombat.grab(detail);
                    break;
                case 'touchParry':
                    window.EquipmentCombat.parry(detail);
                    break;
            }
        }

        // Integration with Realtime Combat if available
        if (window.realtimeCombat) {
            switch (type) {
                case 'touchAttack':
                    if (detail.type === 'combined') {
                        window.realtimeCombat.combineAttack();
                    } else if (detail.hand === 'left') {
                        window.realtimeCombat.attackLeft(detail.type === 'heavy');
                    } else if (detail.hand === 'right') {
                        window.realtimeCombat.attackRight(detail.type === 'heavy');
                    }
                    break;
                case 'touchGrab':
                    window.realtimeCombat.grab();
                    break;
                case 'touchParry':
                    window.realtimeCombat.parry();
                    break;
            }
        }
    }

    // ===== PUBLIC API =====

    function show() {
        if (controlsContainer) controlsContainer.style.display = 'block';
    }

    function hide() {
        if (controlsContainer) controlsContainer.style.display = 'none';
    }

    function toggle() {
        if (controlsContainer) {
            controlsContainer.style.display =
                controlsContainer.style.display === 'none' ? 'block' : 'none';
        }
    }

    window.TouchCombat = {
        init,
        show,
        hide,
        toggle,
        getState: () => ({ ...state }),
        isTouch: isTouchDevice
    };

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    console.log('✅ Touch Combat Controls loaded');
})();
