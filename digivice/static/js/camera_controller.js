/**
 * Kamera-Controller für Najika World 3D-Szenen
 * Unterstützt drei Modi: ORBIT, THIRD-PERSON, FIRST-PERSON
 */

class CameraController {
    constructor(camera, scene, renderer) {
        this.camera = camera;
        this.scene = scene;
        this.renderer = renderer;

        // Kamera-Modi
        this.MODES = {
            ORBIT: 'orbit',
            THIRD: 'third',
            FIRST: 'first'
        };

        this.currentMode = this.MODES.ORBIT;

        // Orbit-Parameter
        this.orbitYaw = Math.PI;  // 180° = hinten
        this.orbitPitch = 0.3;
        this.orbitDistance = 14;

        // Orbit-Limits
        this.ORBIT_MIN_DIST = 5;
        this.ORBIT_MAX_DIST = 50;
        this.ORBIT_MIN_PITCH = -Math.PI / 2 + 0.1;
        this.ORBIT_MAX_PITCH = Math.PI / 2 - 0.1;

        // Target (Fokuspunkt)
        this.target = new THREE.Vector3(0, 0, 0);

        // Character (optional für THIRD/FIRST Person)
        this.character = null;
        this.characterHeight = 3;

        // Interaktion
        this.activePointers = new Map();
        this.pointerMode = null;
        this.dragStartYaw = this.orbitYaw;
        this.dragStartPitch = this.orbitPitch;
        this.pinchBaseDistance = this.orbitDistance;

        this.setupEventListeners();
    }

    setupEventListeners() {
        const canvas = this.renderer.domElement;

        // Maus-Events
        canvas.addEventListener('pointerdown', (e) => this.onPointerDown(e));
        canvas.addEventListener('pointermove', (e) => this.onPointerMove(e));
        canvas.addEventListener('pointerup', (e) => this.onPointerUp(e));
        canvas.addEventListener('pointercancel', (e) => this.onPointerUp(e));

        // Mausrad (Zoom)
        canvas.addEventListener('wheel', (e) => this.onWheel(e), { passive: false });

        // Touch-Gesten verhindern Standard-Verhalten
        canvas.addEventListener('touchstart', (e) => e.preventDefault(), { passive: false });
        canvas.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });
    }

    onPointerDown(e) {
        this.activePointers.set(e.pointerId, {
            x: e.clientX,
            y: e.clientY,
            startX: e.clientX,
            startY: e.clientY
        });

        if (this.activePointers.size === 1) {
            this.pointerMode = 'drag';
            this.dragStartYaw = this.orbitYaw;
            this.dragStartPitch = this.orbitPitch;
        } else if (this.activePointers.size === 2 && this.currentMode === this.MODES.ORBIT) {
            this.pointerMode = 'pinch';
            this.pinchBaseDistance = this.orbitDistance;
        }
    }

    onPointerMove(e) {
        if (!this.activePointers.has(e.pointerId)) return;

        const pointer = this.activePointers.get(e.pointerId);
        const startX = pointer.startX;
        const startY = pointer.startY;

        this.activePointers.set(e.pointerId, {
            x: e.clientX,
            y: e.clientY,
            startX: startX,
            startY: startY
        });

        if (this.pointerMode === 'drag' && this.activePointers.size === 1) {
            // Berechne Delta seit Start
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;

            this.orbitYaw = this.dragStartYaw - dx * 0.005;
            this.orbitPitch = this.clamp(
                this.dragStartPitch - dy * 0.003,
                this.ORBIT_MIN_PITCH,
                this.ORBIT_MAX_PITCH
            );
        } else if (this.pointerMode === 'pinch' && this.activePointers.size === 2 && this.currentMode === this.MODES.ORBIT) {
            // Pinch-to-Zoom
            const pointers = [...this.activePointers.values()];
            const dx = pointers[0].x - pointers[1].x;
            const dy = pointers[0].y - pointers[1].y;
            const currentDist = Math.sqrt(dx * dx + dy * dy);

            if (!this.initialPinchDist) {
                this.initialPinchDist = currentDist;
            }

            const ratio = this.initialPinchDist / currentDist;
            this.orbitDistance = this.clamp(
                this.pinchBaseDistance * ratio,
                this.ORBIT_MIN_DIST,
                this.ORBIT_MAX_DIST
            );
        }
    }

    onPointerUp(e) {
        this.activePointers.delete(e.pointerId);

        if (this.activePointers.size === 0) {
            this.pointerMode = null;
            this.initialPinchDist = null;
        } else if (this.activePointers.size === 1 && this.pointerMode === 'pinch') {
            // Zurück zu Drag-Mode
            this.pointerMode = 'drag';
            this.dragStartYaw = this.orbitYaw;
            this.dragStartPitch = this.orbitPitch;

            // Aktualisiere Start-Position des verbleibenden Pointers
            const [pointerId, pointer] = [...this.activePointers.entries()][0];
            this.activePointers.set(pointerId, {
                x: pointer.x,
                y: pointer.y,
                startX: pointer.x,
                startY: pointer.y
            });
        }
    }

    onWheel(e) {
        e.preventDefault();

        // Zoom funktioniert in allen Modi
        const delta = e.deltaY > 0 ? 1 : -1;
        this.orbitDistance = this.clamp(
            this.orbitDistance + delta,
            this.ORBIT_MIN_DIST,
            this.ORBIT_MAX_DIST
        );
    }

    update(delta) {
        if (!this.camera) return;

        const cosPitch = Math.cos(this.orbitPitch);
        const sinPitch = Math.sin(this.orbitPitch);
        const cosYaw = Math.cos(this.orbitYaw);
        const sinYaw = Math.sin(this.orbitYaw);

        if (this.currentMode === this.MODES.ORBIT || !this.character) {
            // ORBIT Mode: Freie Kamera-Steuerung
            // Auto-Track Character wenn vorhanden
            if (this.character) {
                this.target.copy(this.character.position);
            }

            const offset = new THREE.Vector3(
                sinYaw * cosPitch,
                sinPitch,
                cosYaw * cosPitch
            ).multiplyScalar(this.orbitDistance);

            this.camera.position.copy(this.target).add(offset);
            this.camera.lookAt(this.target);

        } else if (this.currentMode === this.MODES.THIRD) {
            // THIRD-PERSON: Fortnite-Style
            const distance = 12;
            const height = 4;
            const offset = new THREE.Vector3(
                sinYaw * cosPitch * distance,
                height + sinPitch * distance * 0.5,
                cosYaw * cosPitch * distance
            );

            const charTarget = this.character.position.clone();
            this.camera.position.copy(charTarget).add(offset);
            this.camera.lookAt(charTarget);

        } else if (this.currentMode === this.MODES.FIRST) {
            // FIRST-PERSON: Ego-Perspektive (Kamera VOR dem Kopf, nicht IM Kopf)
            // Character position.y ist bereits die Körpermitte
            // Augenhöhe bei ~40% über Mitte = realistische Augenhöhe
            const eyeHeight = this.characterHeight * 0.40;  // ~40% über Mitte = Augenhöhe
            const forwardOffset = 1.5;  // Kamera 1.5 Einheiten VOR dem Kopf

            // Kamera-Position: VOR dem Character, in Blickrichtung
            this.camera.position.set(
                this.character.position.x + sinYaw * cosPitch * forwardOffset,
                this.character.position.y + eyeHeight,
                this.character.position.z + cosYaw * cosPitch * forwardOffset
            );

            const lookDistance = 10;
            const lookTarget = new THREE.Vector3(
                this.camera.position.x + sinYaw * cosPitch * lookDistance,
                this.camera.position.y + sinPitch * lookDistance,
                this.camera.position.z + cosYaw * cosPitch * lookDistance
            );

            this.camera.lookAt(lookTarget);
        }
    }

    setMode(mode) {
        if (!Object.values(this.MODES).includes(mode)) {
            console.warn('Ungültiger Kamera-Modus:', mode);
            return;
        }

        this.currentMode = mode;

        // Clear pointer state when leaving Orbit mode
        if (this.currentMode !== this.MODES.ORBIT) {
            this.activePointers.clear();
            this.pointerMode = null;
        }

        console.log('Kamera-Modus:', this.currentMode);
    }

    getMode() {
        return this.currentMode;
    }

    setTarget(x, y, z) {
        this.target.set(x, y, z);
    }

    setCharacter(character, height = 3) {
        this.character = character;
        this.characterHeight = height;
    }

    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }
}

// Export für Browser (window.CameraController)
if (typeof window !== 'undefined') {
    window.CameraController = CameraController;
}

// Export für Node.js (optional)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CameraController;
}
