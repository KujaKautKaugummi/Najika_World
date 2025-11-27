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

            // Maus nach rechts = Kamera dreht nach rechts (positive rotation)
            this.orbitYaw = this.dragStartYaw + dx * 0.005;
            // Maus nach unten = Kamera schaut nach unten (negative pitch)
            this.orbitPitch = this.clamp(
                this.dragStartPitch + dy * 0.003,
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
            // Kamera ist frei drehbar (nur orbitYaw/Pitch), UNABHÄNGIG von Character-Rotation

            const distance = 8;  // Näher für Fortnite-Feeling
            const heightOffset = 2.5;  // Über Schulter
            const shoulderOffset = 1.5;  // Seitlich (rechte Schulter)

            // Verwende NUR orbitYaw/Pitch (NICHT character.rotation.y!)
            const cos = Math.cos(this.orbitPitch);
            const sin = Math.sin(this.orbitPitch);
            const cosYaw = Math.cos(this.orbitYaw);
            const sinYaw = Math.sin(this.orbitYaw);

            // Kamera-Position: Hinter Character + Schulter-Offset + Höhe
            const offset = new THREE.Vector3(
                sinYaw * cos * distance + shoulderOffset * Math.cos(this.orbitYaw + Math.PI/2),
                heightOffset + sin * distance * 0.5,
                cosYaw * cos * distance + shoulderOffset * Math.sin(this.orbitYaw + Math.PI/2)
            );

            const charTarget = this.character.position.clone();
            charTarget.y += 1.5;  // Blick auf Oberkörper, nicht Füße
            this.camera.position.copy(charTarget).add(offset);
            this.camera.lookAt(charTarget);

        } else if (this.currentMode === this.MODES.FIRST) {
            // FIRST-PERSON: Ego-Perspektive
            // Kamera auf Augenhöhe (nicht im Kopf!)

            const eyeHeight = this.characterHeight * 0.85;  // 85% = echte Augenhöhe

            // WICHTIG: Verwende character.rotation.y als Basis-Blickrichtung (Fortnite-Style)
            const characterYaw = this.character.rotation.y;

            // Kamera-Position an den Augen des Charakters
            this.camera.position.set(
                this.character.position.x,
                this.character.position.y + eyeHeight,
                this.character.position.z
            );

            // Blickrichtung: Charakter-Rotation + Maus-Pitch für hoch/runter schauen
            const lookDistance = 10;
            const charCos = Math.cos(characterYaw);
            const charSin = Math.sin(characterYaw);

            const lookTarget = new THREE.Vector3(
                this.camera.position.x + charSin * cosPitch * lookDistance,
                this.camera.position.y + sinPitch * lookDistance,
                this.camera.position.z + charCos * cosPitch * lookDistance
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

    // Für Fortnite-Style kamera-relative Bewegung
    getCameraYaw() {
        // Gibt die horizontale Blickrichtung der Kamera zurück
        if (this.currentMode === this.MODES.ORBIT) {
            return this.orbitYaw;
        } else if (this.currentMode === this.MODES.THIRD) {
            // In Third-Person: NUR Kamera-Rotation (NICHT Character-Rotation!)
            // Sonst gibt es einen Feedback-Loop!
            return this.orbitYaw;
        } else if (this.currentMode === this.MODES.FIRST) {
            // In First-Person: Character-Rotation ist die Kamera-Richtung
            return this.character ? this.character.rotation.y : 0;
        }
        return 0;
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
