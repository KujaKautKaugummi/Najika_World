/**
 * Touch Controls for Mobile
 * Supports: Virtual Joystick, Touch Buttons, Camera Gestures
 */

(function() {
    console.log('✅ Touch Controls module loaded');

    // Check if mobile device
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if (!isMobile) {
        console.log('Desktop detected, touch controls disabled');
        return;
    }

    console.log('📱 Mobile detected, initializing touch controls');

    // ═══════════════════════════════════════════════════════════════
    // VIRTUAL JOYSTICK
    // ═══════════════════════════════════════════════════════════════

    class VirtualJoystick {
        constructor() {
            this.active = false;
            this.startX = 0;
            this.startY = 0;
            this.currentX = 0;
            this.currentY = 0;
            this.deltaX = 0;
            this.deltaY = 0;
            this.maxDistance = 50;

            this.createJoystick();
            this.attachEvents();
        }

        createJoystick() {
            // Joystick base
            this.base = document.createElement('div');
            this.base.id = 'joystick-base';
            this.base.style.cssText = `
                position: fixed;
                bottom: 80px;
                left: 50px;
                width: 100px;
                height: 100px;
                background: rgba(100, 100, 120, 0.3);
                border: 3px solid rgba(102, 126, 234, 0.5);
                border-radius: 50%;
                z-index: 1000;
                display: none;
            `;

            // Joystick stick
            this.stick = document.createElement('div');
            this.stick.id = 'joystick-stick';
            this.stick.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                width: 40px;
                height: 40px;
                background: rgba(102, 126, 234, 0.8);
                border: 2px solid #fff;
                border-radius: 50%;
                transform: translate(-50%, -50%);
            `;

            this.base.appendChild(this.stick);
            document.body.appendChild(this.base);
        }

        attachEvents() {
            const touchArea = document.getElementById('scene');
            if (!touchArea) return;

            touchArea.addEventListener('touchstart', (e) => {
                const touch = e.touches[0];
                // Only activate if touch is in left third of screen
                if (touch.clientX < window.innerWidth / 3) {
                    this.startX = touch.clientX;
                    this.startY = touch.clientY;
                    this.active = true;

                    this.base.style.left = `${this.startX - 50}px`;
                    this.base.style.bottom = `${window.innerHeight - this.startY - 50}px`;
                    this.base.style.display = 'block';
                }
            });

            touchArea.addEventListener('touchmove', (e) => {
                if (!this.active) return;
                e.preventDefault();

                const touch = e.touches[0];
                this.currentX = touch.clientX;
                this.currentY = touch.clientY;

                let deltaX = this.currentX - this.startX;
                let deltaY = this.currentY - this.startY;

                // Clamp to max distance
                const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
                if (distance > this.maxDistance) {
                    const angle = Math.atan2(deltaY, deltaX);
                    deltaX = Math.cos(angle) * this.maxDistance;
                    deltaY = Math.sin(angle) * this.maxDistance;
                }

                this.deltaX = deltaX / this.maxDistance;
                this.deltaY = deltaY / this.maxDistance;

                // Move stick
                this.stick.style.transform = `translate(calc(-50% + ${deltaX}px), calc(-50% + ${deltaY}px))`;
            });

            const endTouch = () => {
                this.active = false;
                this.deltaX = 0;
                this.deltaY = 0;
                this.base.style.display = 'none';
                this.stick.style.transform = 'translate(-50%, -50%)';
            };

            touchArea.addEventListener('touchend', endTouch);
            touchArea.addEventListener('touchcancel', endTouch);
        }

        getInput() {
            return {
                x: this.deltaX,
                y: -this.deltaY, // Invert Y for proper forward/backward
                active: this.active
            };
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // TOUCH BUTTONS
    // ═══════════════════════════════════════════════════════════════

    class TouchButtons {
        constructor() {
            this.createButtons();
        }

        createButtons() {
            // Button container
            const container = document.createElement('div');
            container.id = 'touch-buttons';
            container.style.cssText = `
                position: fixed;
                bottom: 80px;
                right: 50px;
                display: flex;
                gap: 15px;
                z-index: 1000;
            `;

            // Jump button
            const jumpBtn = this.createButton('↑', 'touch-jump-btn');
            jumpBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.triggerAction('jump');
            });

            // Attack button
            const attackBtn = this.createButton('⚔️', 'touch-attack-btn');
            attackBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.triggerAction('attack');
            });

            // Interact button
            const interactBtn = this.createButton('💬', 'touch-interact-btn');
            interactBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.triggerAction('interact');
            });

            container.appendChild(jumpBtn);
            container.appendChild(attackBtn);
            container.appendChild(interactBtn);
            document.body.appendChild(container);
        }

        createButton(label, id) {
            const btn = document.createElement('button');
            btn.id = id;
            btn.textContent = label;
            btn.style.cssText = `
                width: 60px;
                height: 60px;
                font-size: 1.5rem;
                background: rgba(102, 126, 234, 0.8);
                border: 3px solid rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                color: white;
                cursor: pointer;
                touch-action: none;
                user-select: none;
            `;

            btn.addEventListener('touchstart', () => {
                btn.style.transform = 'scale(0.9)';
            });

            btn.addEventListener('touchend', () => {
                btn.style.transform = 'scale(1)';
            });

            return btn;
        }

        triggerAction(action) {
            // Trigger keyboard event simulation
            const event = new KeyboardEvent('keydown', {
                key: this.getKeyForAction(action),
                code: this.getKeyCodeForAction(action),
                bubbles: true
            });
            document.dispatchEvent(event);

            console.log(`Touch action: ${action}`);
        }

        getKeyForAction(action) {
            const keyMap = {
                'jump': ' ',
                'attack': 'q',
                'interact': 'e'
            };
            return keyMap[action] || '';
        }

        getKeyCodeForAction(action) {
            const codeMap = {
                'jump': 'Space',
                'attack': 'KeyQ',
                'interact': 'KeyE'
            };
            return codeMap[action] || '';
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // CAMERA TOUCH CONTROLS
    // ═══════════════════════════════════════════════════════════════

    class CameraTouchControls {
        constructor() {
            this.active = false;
            this.startX = 0;
            this.startY = 0;
            this.lastX = 0;
            this.lastY = 0;
            this.sensitivity = 0.5;

            this.attachEvents();
        }

        attachEvents() {
            const touchArea = document.getElementById('scene');
            if (!touchArea) return;

            touchArea.addEventListener('touchstart', (e) => {
                const touch = e.touches[0];
                // Only activate if touch is in right two-thirds of screen
                if (touch.clientX > window.innerWidth / 3) {
                    this.startX = touch.clientX;
                    this.startY = touch.clientY;
                    this.lastX = touch.clientX;
                    this.lastY = touch.clientY;
                    this.active = true;
                }
            });

            touchArea.addEventListener('touchmove', (e) => {
                if (!this.active) return;
                e.preventDefault();

                const touch = e.touches[0];
                const deltaX = (touch.clientX - this.lastX) * this.sensitivity;
                const deltaY = (touch.clientY - this.lastY) * this.sensitivity;

                this.lastX = touch.clientX;
                this.lastY = touch.clientY;

                // Rotate camera (if Scene3D exists)
                if (window.Scene3D && typeof window.Scene3D.rotateCamera === 'function') {
                    window.Scene3D.rotateCamera(deltaX, deltaY);
                }
            });

            const endTouch = () => {
                this.active = false;
            };

            touchArea.addEventListener('touchend', endTouch);
            touchArea.addEventListener('touchcancel', endTouch);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // MOBILE UI OPTIMIZATIONS
    // ═══════════════════════════════════════════════════════════════

    function optimizeMobileUI() {
        // Make buttons bigger on mobile
        const style = document.createElement('style');
        style.textContent = `
            @media (max-width: 768px) {
                .cloud-btn {
                    padding: 10px 15px !important;
                    font-size: 0.9rem !important;
                    margin: 3px !important;
                }

                #hud .hud-panel {
                    font-size: 0.85rem !important;
                }

                #openWorldHUD {
                    right: 10px !important;
                    top: 70px !important;
                    width: 200px !important;
                    font-size: 0.8rem !important;
                }

                /* Hide Najika-Panel on mobile in Open World mode */
                body.openworld-mode #najikaPanel {
                    display: none !important;
                }

                /* Compact inventory on mobile */
                #inventory-panel {
                    width: 90vw !important;
                    right: 5vw !important;
                }
            }

            /* Touch feedback */
            .cloud-btn:active {
                transform: scale(0.95);
                opacity: 0.8;
            }
        `;
        document.head.appendChild(style);
    }

    // ═══════════════════════════════════════════════════════════════
    // MOVEMENT INTEGRATION
    // ═══════════════════════════════════════════════════════════════

    function integrateWithMovementSystem() {
        if (!window.virtualJoystick) return;

        // Update movement system with joystick input
        setInterval(() => {
            const input = window.virtualJoystick.getInput();

            if (input.active && window.Scene3D && window.Scene3D.moveCharacter) {
                // Convert joystick to WASD-style movement
                const moveX = input.x;
                const moveZ = input.y;

                window.Scene3D.moveCharacter(moveX, moveZ);
            }
        }, 16); // ~60 FPS
    }

    // ═══════════════════════════════════════════════════════════════
    // PINCH-TO-ZOOM (for camera zoom)
    // ═══════════════════════════════════════════════════════════════

    class PinchZoom {
        constructor() {
            this.initialDistance = 0;
            this.attachEvents();
        }

        attachEvents() {
            const touchArea = document.getElementById('scene');
            if (!touchArea) return;

            touchArea.addEventListener('touchstart', (e) => {
                if (e.touches.length === 2) {
                    this.initialDistance = this.getDistance(e.touches[0], e.touches[1]);
                }
            });

            touchArea.addEventListener('touchmove', (e) => {
                if (e.touches.length === 2) {
                    e.preventDefault();
                    const currentDistance = this.getDistance(e.touches[0], e.touches[1]);
                    const delta = (currentDistance - this.initialDistance) * 0.01;

                    if (window.Scene3D && typeof window.Scene3D.zoomCamera === 'function') {
                        window.Scene3D.zoomCamera(delta);
                    }

                    this.initialDistance = currentDistance;
                }
            });
        }

        getDistance(touch1, touch2) {
            const dx = touch1.clientX - touch2.clientX;
            const dy = touch1.clientY - touch2.clientY;
            return Math.sqrt(dx * dx + dy * dy);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // INITIALIZATION
    // ═══════════════════════════════════════════════════════════════

    function init() {
        console.log('📱 Initializing mobile touch controls...');

        // Create touch controls
        window.virtualJoystick = new VirtualJoystick();
        window.touchButtons = new TouchButtons();
        window.cameraTouchControls = new CameraTouchControls();
        window.pinchZoom = new PinchZoom();

        // Optimize UI for mobile
        optimizeMobileUI();

        // Integrate with movement system (after a delay to ensure Scene3D is loaded)
        setTimeout(() => {
            integrateWithMovementSystem();
        }, 2000);

        console.log('✅ Touch controls initialized successfully');
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
