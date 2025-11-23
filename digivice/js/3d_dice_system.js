/**
 * 3D Dice System - Najika World
 * Physically-animated 3D dice rolling system
 *
 * Features:
 * - Realistic dice rolling with rotation animations
 * - Canvas-based face textures (1-6 pips)
 * - Physics-lite simulation (easing-based)
 * - Multiple dice support
 * - Auto-cleanup after animation
 *
 * Integration with dice_monsters_ui.js
 *
 * NOTE: Uses THREE from global scope (loaded via CDN in index.html)
 */

(function() {
    'use strict';

    // Check if THREE.js is loaded
    if (typeof THREE === 'undefined') {
        console.error('❌ THREE.js is required for DiceSystem3D');
        return;
    }

class DiceSystem3D {
    constructor(scene, camera) {
        this.scene = scene;
        this.camera = camera;
        this.activeDice = [];
        this.animatingDice = [];
        this.results = [];

        // Animation settings
        this.rollDuration = 2000; // 2 seconds
        this.rollStartTime = 0;
        this.isRolling = false;

        // Spawn position (in front of player)
        this.spawnPosition = new THREE.Vector3(0, 2, -5);

        console.log('🎲 3D Dice System initialized');
    }

    /**
     * Create canvas texture for dice face
     * @param {number} number - Pip count (1-6)
     * @returns {THREE.CanvasTexture}
     */
    createDiceFaceTexture(number) {
        const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');

        // Background (white)
        ctx.fillStyle = '#f0f0f0';
        ctx.fillRect(0, 0, 128, 128);

        // Border
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 4;
        ctx.strokeRect(4, 4, 120, 120);

        // Pips (black dots)
        ctx.fillStyle = '#000';
        const pipRadius = 10;
        const positions = this.getPipPositions(number);

        positions.forEach(pos => {
            ctx.beginPath();
            ctx.arc(pos[0], pos[1], pipRadius, 0, Math.PI * 2);
            ctx.fill();
        });

        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        return texture;
    }

    /**
     * Get pip positions for dice face number
     * @param {number} num - Face number (1-6)
     * @returns {Array} Array of [x, y] positions
     */
    getPipPositions(num) {
        const center = 64;
        const offset = 30;

        switch(num) {
            case 1:
                return [[center, center]];
            case 2:
                return [[center - offset, center - offset], [center + offset, center + offset]];
            case 3:
                return [[center - offset, center - offset], [center, center], [center + offset, center + offset]];
            case 4:
                return [
                    [center - offset, center - offset],
                    [center + offset, center - offset],
                    [center - offset, center + offset],
                    [center + offset, center + offset]
                ];
            case 5:
                return [
                    [center - offset, center - offset],
                    [center + offset, center - offset],
                    [center, center],
                    [center - offset, center + offset],
                    [center + offset, center + offset]
                ];
            case 6:
                return [
                    [center - offset, center - offset],
                    [center + offset, center - offset],
                    [center - offset, center],
                    [center + offset, center],
                    [center - offset, center + offset],
                    [center + offset, center + offset]
                ];
            default:
                return [[center, center]];
        }
    }

    /**
     * Create a single die mesh
     * @param {Vector3} position - Spawn position
     * @param {number} finalValue - Resulting face (1-6)
     * @returns {THREE.Mesh}
     */
    createDie(position, finalValue) {
        // Create box geometry
        const geometry = new THREE.BoxGeometry(1, 1, 1);

        // Create materials with face textures
        const materials = [
            new THREE.MeshStandardMaterial({ map: this.createDiceFaceTexture(1) }), // right
            new THREE.MeshStandardMaterial({ map: this.createDiceFaceTexture(2) }), // left
            new THREE.MeshStandardMaterial({ map: this.createDiceFaceTexture(3) }), // top
            new THREE.MeshStandardMaterial({ map: this.createDiceFaceTexture(4) }), // bottom
            new THREE.MeshStandardMaterial({ map: this.createDiceFaceTexture(5) }), // front
            new THREE.MeshStandardMaterial({ map: this.createDiceFaceTexture(6) })  // back
        ];

        const die = new THREE.Mesh(geometry, materials);
        die.position.copy(position);
        die.castShadow = true;
        die.receiveShadow = true;

        // Store animation data
        die.userData.finalValue = finalValue;
        die.userData.startRotation = new THREE.Euler(
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2,
            Math.random() * Math.PI * 2
        );
        die.userData.targetRotation = this.getRotationForFace(finalValue);
        die.userData.velocity = new THREE.Vector3(
            (Math.random() - 0.5) * 5,
            Math.random() * 2 + 3,
            (Math.random() - 0.5) * 5
        );
        die.userData.angularVelocity = new THREE.Vector3(
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 10
        );

        return die;
    }

    /**
     * Calculate rotation to show specific face on top
     * @param {number} face - Face number (1-6)
     * @returns {THREE.Euler}
     */
    getRotationForFace(face) {
        switch(face) {
            case 1: return new THREE.Euler(0, 0, 0); // face 1 on top
            case 2: return new THREE.Euler(0, 0, Math.PI); // face 2 on top
            case 3: return new THREE.Euler(0, 0, -Math.PI / 2); // face 3 on top
            case 4: return new THREE.Euler(0, 0, Math.PI / 2); // face 4 on top
            case 5: return new THREE.Euler(-Math.PI / 2, 0, 0); // face 5 on top
            case 6: return new THREE.Euler(Math.PI / 2, 0, 0); // face 6 on top
            default: return new THREE.Euler(0, 0, 0);
        }
    }

    /**
     * Roll multiple dice
     * @param {number} count - Number of dice
     * @param {Vector3} playerPosition - Player position for spawn location
     * @returns {Promise<Array<number>>} Array of results (1-6)
     */
    rollDice(count, playerPosition = null) {
        return new Promise((resolve) => {
            // Clear any existing dice
            this.clearDice();

            // Set spawn position
            if (playerPosition) {
                this.spawnPosition.copy(playerPosition);
                this.spawnPosition.y = 2;
                this.spawnPosition.z -= 3; // In front of player
            }

            // Generate random results
            this.results = [];
            for (let i = 0; i < count; i++) {
                this.results.push(Math.floor(Math.random() * 6) + 1);
            }

            // Create dice meshes
            for (let i = 0; i < count; i++) {
                const offset = new THREE.Vector3(
                    (i - count / 2) * 1.5, // Spread horizontally
                    0,
                    0
                );
                const position = this.spawnPosition.clone().add(offset);
                const die = this.createDie(position, this.results[i]);

                this.scene.add(die);
                this.activeDice.push(die);
                this.animatingDice.push(die);
            }

            // Start animation
            this.isRolling = true;
            this.rollStartTime = Date.now();

            // Resolve with results after animation
            setTimeout(() => {
                this.isRolling = false;
                resolve(this.results);
            }, this.rollDuration + 500); // Extra 0.5s for settling
        });
    }

    /**
     * Update animation (called every frame)
     * @param {number} deltaTime - Time since last frame (seconds)
     */
    update(deltaTime) {
        if (!this.isRolling || this.animatingDice.length === 0) return;

        const elapsed = Date.now() - this.rollStartTime;
        const progress = Math.min(elapsed / this.rollDuration, 1);
        const easeProgress = this.easeOutCubic(progress);

        this.animatingDice.forEach(die => {
            if (progress < 0.7) {
                // Physics phase (first 70% of animation)
                // Apply gravity
                die.userData.velocity.y -= 9.8 * deltaTime;

                // Update position
                die.position.x += die.userData.velocity.x * deltaTime;
                die.position.y += die.userData.velocity.y * deltaTime;
                die.position.z += die.userData.velocity.z * deltaTime;

                // Bounce on ground
                if (die.position.y < 0.5) {
                    die.position.y = 0.5;
                    die.userData.velocity.y = Math.abs(die.userData.velocity.y) * 0.6; // Bounce with damping
                    die.userData.velocity.x *= 0.8; // Friction
                    die.userData.velocity.z *= 0.8;
                }

                // Angular velocity (spinning)
                die.rotation.x += die.userData.angularVelocity.x * deltaTime;
                die.rotation.y += die.userData.angularVelocity.y * deltaTime;
                die.rotation.z += die.userData.angularVelocity.z * deltaTime;

                // Damping
                die.userData.angularVelocity.multiplyScalar(0.98);

            } else {
                // Settling phase (last 30% of animation)
                // Smoothly rotate to final face
                const settleProgress = (progress - 0.7) / 0.3;
                const settleEase = this.easeInOutQuad(settleProgress);

                die.rotation.x = THREE.MathUtils.lerp(
                    die.rotation.x,
                    die.userData.targetRotation.x,
                    settleEase * 0.5
                );
                die.rotation.y = THREE.MathUtils.lerp(
                    die.rotation.y,
                    die.userData.targetRotation.y,
                    settleEase * 0.5
                );
                die.rotation.z = THREE.MathUtils.lerp(
                    die.rotation.z,
                    die.userData.targetRotation.z,
                    settleEase * 0.5
                );

                // Settle position to ground
                die.position.y = THREE.MathUtils.lerp(die.position.y, 0.5, settleEase * 0.3);
            }
        });
    }

    /**
     * Easing function: ease out cubic
     * @param {number} t - Progress (0-1)
     * @returns {number} Eased value
     */
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    /**
     * Easing function: ease in-out quad
     * @param {number} t - Progress (0-1)
     * @returns {number} Eased value
     */
    easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    }

    /**
     * Clear all dice from scene
     */
    clearDice() {
        this.activeDice.forEach(die => {
            // Dispose geometries and materials
            if (die.geometry) die.geometry.dispose();
            if (die.material) {
                if (Array.isArray(die.material)) {
                    die.material.forEach(mat => {
                        if (mat.map) mat.map.dispose();
                        mat.dispose();
                    });
                } else {
                    if (die.material.map) die.material.map.dispose();
                    die.material.dispose();
                }
            }

            this.scene.remove(die);
        });

        this.activeDice = [];
        this.animatingDice = [];
        this.results = [];
        this.isRolling = false;
    }

    /**
     * Get current results
     * @returns {Array<number>} Array of dice results
     */
    getResults() {
        return this.results;
    }

    /**
     * Check if dice are currently rolling
     * @returns {boolean}
     */
    isAnimating() {
        return this.isRolling;
    }
}

// Export to global scope
window.DiceSystem3D = DiceSystem3D;

console.log('🎲 DiceSystem3D loaded successfully');

})();
