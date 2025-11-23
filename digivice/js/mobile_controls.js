/**
 * Mobile Controls System
 * Virtual joystick, touch controls, and mobile-specific input handling
 */

class MobileControls {
    constructor(scene, camera, player) {
        this.scene = scene;
        this.camera = camera;
        this.player = player;

        // Detection
        this.isMobile = this.detectMobile();
        this.isTablet = this.detectTablet();
        this.isTouchDevice = 'ontouchstart' in window;

        // Virtual joystick
        this.joystick = null;
        this.joystickActive = false;
        this.joystickStart = { x: 0, y: 0 };
        this.joystickCurrent = { x: 0, y: 0 };
        this.joystickDelta = { x: 0, y: 0 };

        // Touch state
        this.touches = new Map(); // {touchId: {x, y, startX, startY, startTime}}
        this.pinchDistance = 0;
        this.pinchStartDistance = 0;

        // Camera control
        this.cameraRotation = { x: 0, y: 0 };
        this.cameraSensitivity = 0.003;

        // Buttons
        this.buttons = new Map();

        // Settings
        this.joystickSize = 120;
        this.joystickDeadzone = 0.1;
        this.doubleTapDelay = 300;
        this.lastTapTime = 0;

        // Initialize if mobile
        if (this.isTouchDevice) {
            this.init();
        }
    }

    /**
     * Detect if device is mobile
     */
    detectMobile() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        return /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent.toLowerCase());
    }

    /**
     * Detect if device is tablet
     */
    detectTablet() {
        const userAgent = navigator.userAgent.toLowerCase();
        return /(ipad|tablet|playbook|silk)|(android(?!.*mobile))/i.test(userAgent);
    }

    /**
     * Initialize mobile controls
     */
    init() {
        console.log('📱 Initializing mobile controls...');

        // Create UI elements
        this.createJoystick();
        this.createActionButtons();

        // Add touch event listeners
        this.addTouchListeners();

        // Add orientation change listener
        window.addEventListener('orientationchange', () => this.onOrientationChange());

        // Hide mouse cursor on mobile
        document.body.style.cursor = 'none';

        console.log('✅ Mobile controls initialized');
    }

    /**
     * Create virtual joystick
     */
    createJoystick() {
        // Create joystick container
        const container = document.createElement('div');
        container.id = 'joystick-container';
        container.style.cssText = `
            position: fixed;
            bottom: 30px;
            left: 30px;
            width: ${this.joystickSize}px;
            height: ${this.joystickSize}px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            z-index: 1000;
            touch-action: none;
        `;

        // Create joystick stick
        const stick = document.createElement('div');
        stick.id = 'joystick-stick';
        stick.style.cssText = `
            position: absolute;
            width: ${this.joystickSize * 0.5}px;
            height: ${this.joystickSize * 0.5}px;
            background: rgba(255, 255, 255, 0.5);
            border: 2px solid rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            transition: all 0.1s ease;
        `;

        container.appendChild(stick);
        document.body.appendChild(container);

        this.joystick = {
            container,
            stick
        };
    }

    /**
     * Create action buttons
     */
    createActionButtons() {
        const buttonsData = [
            { id: 'jump', label: '↑', bottom: 120, right: 30 },
            { id: 'attack', label: '⚔️', bottom: 30, right: 120 },
            { id: 'interact', label: '✋', bottom: 30, right: 30 }
        ];

        buttonsData.forEach(data => {
            const button = document.createElement('button');
            button.id = `btn-${data.id}`;
            button.textContent = data.label;
            button.style.cssText = `
                position: fixed;
                bottom: ${data.bottom}px;
                right: ${data.right}px;
                width: 70px;
                height: 70px;
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                color: white;
                font-size: 24px;
                z-index: 1000;
                touch-action: none;
                user-select: none;
            `;

            // Touch events for button
            button.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.onButtonPress(data.id);
                button.style.background = 'rgba(255, 255, 255, 0.5)';
            });

            button.addEventListener('touchend', (e) => {
                e.preventDefault();
                this.onButtonRelease(data.id);
                button.style.background = 'rgba(255, 255, 255, 0.2)';
            });

            document.body.appendChild(button);
            this.buttons.set(data.id, button);
        });
    }

    /**
     * Add touch event listeners
     */
    addTouchListeners() {
        // Joystick touch
        this.joystick.container.addEventListener('touchstart', (e) => this.onJoystickTouchStart(e), { passive: false });
        this.joystick.container.addEventListener('touchmove', (e) => this.onJoystickTouchMove(e), { passive: false });
        this.joystick.container.addEventListener('touchend', (e) => this.onJoystickTouchEnd(e), { passive: false });

        // Camera control (right side of screen)
        const cameraArea = document.createElement('div');
        cameraArea.id = 'camera-control-area';
        cameraArea.style.cssText = `
            position: fixed;
            top: 0;
            left: 50%;
            right: 0;
            bottom: 200px;
            z-index: 999;
            touch-action: none;
        `;

        cameraArea.addEventListener('touchstart', (e) => this.onCameraTouchStart(e), { passive: false });
        cameraArea.addEventListener('touchmove', (e) => this.onCameraTouchMove(e), { passive: false });
        cameraArea.addEventListener('touchend', (e) => this.onCameraTouchEnd(e), { passive: false });

        document.body.appendChild(cameraArea);

        // Pinch to zoom
        document.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
        document.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
        document.addEventListener('touchend', (e) => this.onTouchEnd(e), { passive: false });
    }

    /**
     * Joystick touch start
     */
    onJoystickTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const rect = this.joystick.container.getBoundingClientRect();

        this.joystickActive = true;
        this.joystickStart = {
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2
        };
        this.joystickCurrent = {
            x: touch.clientX,
            y: touch.clientY
        };
    }

    /**
     * Joystick touch move
     */
    onJoystickTouchMove(e) {
        if (!this.joystickActive) return;
        e.preventDefault();

        const touch = e.touches[0];
        this.joystickCurrent = {
            x: touch.clientX,
            y: touch.clientY
        };

        // Calculate delta
        const dx = this.joystickCurrent.x - this.joystickStart.x;
        const dy = this.joystickCurrent.y - this.joystickStart.y;

        // Limit to joystick radius
        const maxDistance = this.joystickSize / 2;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > maxDistance) {
            const angle = Math.atan2(dy, dx);
            this.joystickCurrent.x = this.joystickStart.x + Math.cos(angle) * maxDistance;
            this.joystickCurrent.y = this.joystickStart.y + Math.sin(angle) * maxDistance;
        }

        // Normalize delta (-1 to 1)
        this.joystickDelta.x = (this.joystickCurrent.x - this.joystickStart.x) / maxDistance;
        this.joystickDelta.y = (this.joystickCurrent.y - this.joystickStart.y) / maxDistance;

        // Apply deadzone
        if (Math.abs(this.joystickDelta.x) < this.joystickDeadzone) this.joystickDelta.x = 0;
        if (Math.abs(this.joystickDelta.y) < this.joystickDeadzone) this.joystickDelta.y = 0;

        // Update stick position
        this.updateJoystickVisual();
    }

    /**
     * Joystick touch end
     */
    onJoystickTouchEnd(e) {
        e.preventDefault();
        this.joystickActive = false;
        this.joystickDelta = { x: 0, y: 0 };
        this.updateJoystickVisual();
    }

    /**
     * Update joystick visual
     */
    updateJoystickVisual() {
        if (this.joystickActive) {
            const offsetX = this.joystickDelta.x * (this.joystickSize / 2) * 0.5;
            const offsetY = this.joystickDelta.y * (this.joystickSize / 2) * 0.5;

            this.joystick.stick.style.transform = `translate(-50%, -50%) translate(${offsetX}px, ${offsetY}px)`;
        } else {
            this.joystick.stick.style.transform = 'translate(-50%, -50%)';
        }
    }

    /**
     * Camera touch start
     */
    onCameraTouchStart(e) {
        if (e.touches.length !== 1) return;
        e.preventDefault();

        const touch = e.touches[0];
        this.cameraTouchStart = {
            x: touch.clientX,
            y: touch.clientY
        };
    }

    /**
     * Camera touch move
     */
    onCameraTouchMove(e) {
        if (e.touches.length !== 1 || !this.cameraTouchStart) return;
        e.preventDefault();

        const touch = e.touches[0];
        const dx = touch.clientX - this.cameraTouchStart.x;
        const dy = touch.clientY - this.cameraTouchStart.y;

        // Rotate camera
        this.cameraRotation.y -= dx * this.cameraSensitivity;
        this.cameraRotation.x -= dy * this.cameraSensitivity;

        // Clamp X rotation
        this.cameraRotation.x = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.cameraRotation.x));

        // Update touch start
        this.cameraTouchStart = {
            x: touch.clientX,
            y: touch.clientY
        };
    }

    /**
     * Camera touch end
     */
    onCameraTouchEnd(e) {
        this.cameraTouchStart = null;
    }

    /**
     * General touch start (for pinch zoom)
     */
    onTouchStart(e) {
        Array.from(e.touches).forEach(touch => {
            this.touches.set(touch.identifier, {
                x: touch.clientX,
                y: touch.clientY,
                startX: touch.clientX,
                startY: touch.clientY,
                startTime: Date.now()
            });
        });

        // Detect pinch start
        if (e.touches.length === 2) {
            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            this.pinchStartDistance = this.getDistance(touch1, touch2);
            this.pinchDistance = this.pinchStartDistance;
        }
    }

    /**
     * General touch move (for pinch zoom)
     */
    onTouchMove(e) {
        // Update touch positions
        Array.from(e.touches).forEach(touch => {
            if (this.touches.has(touch.identifier)) {
                const t = this.touches.get(touch.identifier);
                t.x = touch.clientX;
                t.y = touch.clientY;
            }
        });

        // Handle pinch zoom
        if (e.touches.length === 2) {
            e.preventDefault();

            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            const currentDistance = this.getDistance(touch1, touch2);

            const scale = currentDistance / this.pinchStartDistance;
            this.onPinchZoom(scale);

            this.pinchDistance = currentDistance;
        }
    }

    /**
     * General touch end
     */
    onTouchEnd(e) {
        // Check for double tap
        const now = Date.now();
        if (now - this.lastTapTime < this.doubleTapDelay) {
            this.onDoubleTap(e);
        }
        this.lastTapTime = now;

        // Remove ended touches
        Array.from(e.changedTouches).forEach(touch => {
            this.touches.delete(touch.identifier);
        });

        // Reset pinch
        if (e.touches.length < 2) {
            this.pinchStartDistance = 0;
            this.pinchDistance = 0;
        }
    }

    /**
     * Get distance between two touches
     */
    getDistance(touch1, touch2) {
        const dx = touch2.clientX - touch1.clientX;
        const dy = touch2.clientY - touch1.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    /**
     * Handle pinch zoom
     */
    onPinchZoom(scale) {
        // Implement zoom logic (adjust camera distance)
        if (this.camera) {
            const zoomSpeed = 0.5;
            const delta = (scale - 1) * zoomSpeed;

            // Adjust camera zoom or distance
            if (this.camera.isPerspectiveCamera) {
                this.camera.zoom = Math.max(0.5, Math.min(3, this.camera.zoom + delta));
                this.camera.updateProjectionMatrix();
            }
        }
    }

    /**
     * Handle double tap
     */
    onDoubleTap(e) {
        console.log('Double tap detected');
        // Implement double tap action (e.g., auto-center camera)
    }

    /**
     * Button press handler
     */
    onButtonPress(buttonId) {
        console.log(`Button pressed: ${buttonId}`);

        // Trigger corresponding action
        switch (buttonId) {
            case 'jump':
                this.onJump();
                break;
            case 'attack':
                this.onAttack();
                break;
            case 'interact':
                this.onInteract();
                break;
        }
    }

    /**
     * Button release handler
     */
    onButtonRelease(buttonId) {
        console.log(`Button released: ${buttonId}`);
    }

    /**
     * Jump action
     */
    onJump() {
        if (this.player && this.player.jump) {
            this.player.jump();
        }
    }

    /**
     * Attack action
     */
    onAttack() {
        if (this.player && this.player.attack) {
            this.player.attack();
        }
    }

    /**
     * Interact action
     */
    onInteract() {
        if (this.player && this.player.interact) {
            this.player.interact();
        }
    }

    /**
     * Handle orientation change
     */
    onOrientationChange() {
        console.log('Orientation changed');

        // Adjust UI positions if needed
        setTimeout(() => {
            // Recalculate positions after orientation settles
            window.scrollTo(0, 1); // Hide address bar
        }, 100);
    }

    /**
     * Update (call every frame)
     */
    update(deltaTime) {
        if (!this.isTouchDevice) return;

        // Apply joystick movement to player
        if (this.player && (this.joystickDelta.x !== 0 || this.joystickDelta.y !== 0)) {
            // Convert joystick delta to movement
            const moveSpeed = 5 * deltaTime;

            // Forward/backward
            const forward = -this.joystickDelta.y * moveSpeed;
            // Left/right
            const strafe = this.joystickDelta.x * moveSpeed;

            // Apply to player
            if (this.player.moveForward) {
                this.player.moveForward(forward);
            }
            if (this.player.moveRight) {
                this.player.moveRight(strafe);
            }
        }

        // Apply camera rotation
        if (this.camera && this.player) {
            this.camera.rotation.y = this.cameraRotation.y;
            this.camera.rotation.x = this.cameraRotation.x;
        }
    }

    /**
     * Show/hide mobile controls
     */
    setVisible(visible) {
        const display = visible ? 'block' : 'none';

        if (this.joystick) {
            this.joystick.container.style.display = display;
        }

        this.buttons.forEach(button => {
            button.style.display = display;
        });
    }

    /**
     * Cleanup
     */
    dispose() {
        // Remove joystick
        if (this.joystick) {
            this.joystick.container.remove();
        }

        // Remove buttons
        this.buttons.forEach(button => button.remove());

        // Remove camera area
        const cameraArea = document.getElementById('camera-control-area');
        if (cameraArea) {
            cameraArea.remove();
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileControls;
}
