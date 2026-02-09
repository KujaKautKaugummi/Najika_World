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
            attack: false,
            magic: false,
            block: false,
            dodge: false
        },
        lastTap: {
            attack: 0,
            magic: 0
        },
        swipeStart: null
    };

    // ===== UI ELEMENTS =====
    let joystickOuter = null;
    let joystickInner = null;
    let attackBtn = null;
    let magicBtn = null;
    let blockBtn = null;
    let dodgeBtn = null;
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
                <button class="touch-btn attack" id="btn-attack">⚔️</button>
                <button class="touch-btn magic" id="btn-magic">🔮</button>
                <button class="touch-btn block" id="btn-block">🛡️</button>
                <button class="touch-btn dodge" id="btn-dodge">🌀</button>
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
                gap: ${CONFIG.buttons.spacing}px;
                pointer-events: auto;
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

            .touch-btn.attack {
                border-color: #ff6b6b;
                background: rgba(255, 107, 107, 0.3);
            }

            .touch-btn.magic {
                border-color: #4ecdc4;
                background: rgba(78, 205, 196, 0.3);
            }

            .touch-btn.block {
                border-color: #ffe66d;
                background: rgba(255, 230, 109, 0.3);
            }

            .touch-btn.dodge {
                border-color: #95e1d3;
                background: rgba(149, 225, 211, 0.3);
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
        attackBtn = document.getElementById('btn-attack');
        magicBtn = document.getElementById('btn-magic');
        blockBtn = document.getElementById('btn-block');
        dodgeBtn = document.getElementById('btn-dodge');
    }

    // ===== EVENT LISTENERS =====

    function setupEventListeners() {
        // Joystick Events
        joystickOuter.addEventListener('touchstart', onJoystickStart, { passive: false });
        joystickOuter.addEventListener('touchmove', onJoystickMove, { passive: false });
        joystickOuter.addEventListener('touchend', onJoystickEnd, { passive: false });

        // Button Events
        setupButtonEvents(attackBtn, 'attack', onAttack);
        setupButtonEvents(magicBtn, 'magic', onMagic);
        setupButtonEvents(blockBtn, 'block', onBlockStart, onBlockEnd);
        setupButtonEvents(dodgeBtn, 'dodge', onDodge);

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

    function onAttack(e) {
        const now = Date.now();
        const isDoubleTap = (now - state.lastTap.attack) < CONFIG.doubleTap.maxDelay;
        state.lastTap.attack = now;

        if (isDoubleTap) {
            // Heavy Attack
            emitEvent('touchAttack', { type: 'heavy', hand: 'right' });
            console.log('⚔️ Heavy Attack (Double Tap)');
        } else {
            // Light Attack
            emitEvent('touchAttack', { type: 'light', hand: 'right' });
            console.log('⚔️ Light Attack');
        }
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
                    if (detail.type === 'light') {
                        window.EquipmentCombat.attackLight(detail.hand);
                    } else {
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
