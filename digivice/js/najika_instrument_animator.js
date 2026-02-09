/**
 * Najika Instrument Animator - 3D Animation for Music Playing
 * Animates Najika character when playing instruments
 *
 * Features:
 * - Hand movement animation
 * - Head bobbing to rhythm
 * - Note particle effects
 * - Integration with instrument_player.js
 *
 * NOTE: Uses THREE from global scope
 */

(function() {
    'use strict';

    if (typeof THREE === 'undefined') {
        console.error('❌ THREE.js is required for InstrumentAnimator');
        return;
    }

class InstrumentAnimator {
    constructor(scene, characterGroup) {
        this.scene = scene;
        this.characterGroup = characterGroup;
        this.isPlaying = false;
        this.animationTime = 0;
        this.currentNote = null;
        this.particles = [];
        this.maxParticles = 30;

        // Animation states
        this.headBobAmplitude = 0.1;
        this.headBobSpeed = 2;
        this.handWaveSpeed = 3;

        // Store original character pose
        this.originalPose = {
            headRotation: null,
            leftHandPosition: null,
            rightHandPosition: null
        };

        console.log('🎵 Instrument Animator initialized');
    }

    /**
     * Start playing animation
     * @param {string} instrument - Instrument type (harmonica, flute, etc.)
     */
    startPlaying(instrument = 'harmonica') {
        if (!this.characterGroup) {
            console.warn('⚠️ No character to animate');
            return;
        }

        this.isPlaying = true;
        this.animationTime = 0;
        this.currentInstrument = instrument;

        // Save original pose
        this.saveOriginalPose();

        console.log(`🎵 Started ${instrument} animation`);
    }

    /**
     * Stop playing animation
     */
    stopPlaying() {
        if (!this.isPlaying) return;

        this.isPlaying = false;

        // Restore original pose
        this.restoreOriginalPose();

        // Clear particles
        this.clearParticles();

        console.log('🎵 Stopped instrument animation');
    }

    /**
     * Save original character pose
     */
    saveOriginalPose() {
        if (!this.characterGroup) return;

        // Find head and hands (if they exist)
        this.characterGroup.traverse(child => {
            if (child.name === 'head' || child.name === 'Head') {
                this.originalPose.headRotation = child.rotation.clone();
            }
            if (child.name === 'leftHand' || child.name === 'LeftHand') {
                this.originalPose.leftHandPosition = child.position.clone();
            }
            if (child.name === 'rightHand' || child.name === 'RightHand') {
                this.originalPose.rightHandPosition = child.position.clone();
            }
        });
    }

    /**
     * Restore original character pose
     */
    restoreOriginalPose() {
        if (!this.characterGroup) return;

        this.characterGroup.traverse(child => {
            if ((child.name === 'head' || child.name === 'Head') && this.originalPose.headRotation) {
                child.rotation.copy(this.originalPose.headRotation);
            }
            if ((child.name === 'leftHand' || child.name === 'LeftHand') && this.originalPose.leftHandPosition) {
                child.position.copy(this.originalPose.leftHandPosition);
            }
            if ((child.name === 'rightHand' || child.name === 'RightHand') && this.originalPose.rightHandPosition) {
                child.position.copy(this.originalPose.rightHandPosition);
            }
        });
    }

    /**
     * Play a note (trigger particle effect)
     * @param {string} note - Note name (C4, D4, etc.)
     * @param {string} color - Note color (hex)
     */
    playNote(note, color = '#3498db') {
        if (!this.characterGroup || !this.scene) return;

        this.currentNote = note;

        // Spawn note particles
        this.spawnNoteParticles(color);
    }

    /**
     * Spawn musical note particles
     * @param {string} color - Particle color
     */
    spawnNoteParticles(color) {
        if (!this.characterGroup || !this.scene) return;

        // Spawn 3-5 particles per note
        const count = 3 + Math.floor(Math.random() * 3);

        for (let i = 0; i < count; i++) {
            // Create note particle (simple sphere or text)
            const particleGeo = new THREE.SphereGeometry(0.15, 8, 8);
            const particleMat = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.9
            });
            const particle = new THREE.Mesh(particleGeo, particleMat);

            // Position near character's head
            const headPosition = this.characterGroup.position.clone();
            headPosition.y += 2; // Above head
            headPosition.x += (Math.random() - 0.5) * 0.5;
            headPosition.z += (Math.random() - 0.5) * 0.5;

            particle.position.copy(headPosition);

            // Animation data
            particle.userData.velocity = new THREE.Vector3(
                (Math.random() - 0.5) * 2,
                1 + Math.random() * 2, // Upward
                (Math.random() - 0.5) * 2
            );
            particle.userData.lifetime = 1.5; // 1.5 seconds
            particle.userData.age = 0;

            this.scene.add(particle);
            this.particles.push(particle);

            // Limit particle count
            if (this.particles.length > this.maxParticles) {
                const old = this.particles.shift();
                if (old.geometry) old.geometry.dispose();
                if (old.material) old.material.dispose();
                this.scene.remove(old);
            }
        }
    }

    /**
     * Update animation (called every frame)
     * @param {number} deltaTime - Time since last frame (seconds)
     */
    update(deltaTime) {
        if (!this.isPlaying || !this.characterGroup) {
            // Still update particles even when not playing
            this.updateParticles(deltaTime);
            return;
        }

        this.animationTime += deltaTime;

        // Animate character
        this.animateCharacter(deltaTime);

        // Update particles
        this.updateParticles(deltaTime);
    }

    /**
     * Animate character body parts
     * @param {number} deltaTime - Time delta
     */
    animateCharacter(deltaTime) {
        if (!this.characterGroup) return;

        const time = this.animationTime;

        // Head bobbing
        this.characterGroup.traverse(child => {
            if (child.name === 'head' || child.name === 'Head') {
                // Bob up and down
                child.rotation.x = Math.sin(time * this.headBobSpeed) * this.headBobAmplitude;
                child.rotation.z = Math.cos(time * this.headBobSpeed * 0.5) * this.headBobAmplitude * 0.5;
            }

            // Hand wave (for harmonica)
            if (this.currentInstrument === 'harmonica') {
                if (child.name === 'leftHand' || child.name === 'LeftHand') {
                    child.position.x = (this.originalPose.leftHandPosition?.x || 0) + Math.sin(time * this.handWaveSpeed) * 0.2;
                }
                if (child.name === 'rightHand' || child.name === 'RightHand') {
                    child.position.x = (this.originalPose.rightHandPosition?.x || 0) - Math.sin(time * this.handWaveSpeed) * 0.2;
                }
            }
        });
    }

    /**
     * Update note particles
     * @param {number} deltaTime - Time delta
     */
    updateParticles(deltaTime) {
        const particlesToRemove = [];

        this.particles.forEach((particle, index) => {
            // Age particle
            particle.userData.age += deltaTime;

            // Update position
            particle.position.add(particle.userData.velocity.clone().multiplyScalar(deltaTime));

            // Fade out
            const lifetime = particle.userData.lifetime;
            const age = particle.userData.age;
            const opacity = 1 - (age / lifetime);

            if (particle.material) {
                particle.material.opacity = Math.max(0, opacity);
            }

            // Slow down
            particle.userData.velocity.multiplyScalar(0.95);

            // Remove if dead
            if (age >= lifetime) {
                particlesToRemove.push({ particle, index });
            }
        });

        // Remove dead particles
        particlesToRemove.reverse().forEach(({ particle, index }) => {
            if (particle.geometry) particle.geometry.dispose();
            if (particle.material) particle.material.dispose();
            this.scene.remove(particle);
            this.particles.splice(index, 1);
        });
    }

    /**
     * Clear all particles
     */
    clearParticles() {
        this.particles.forEach(particle => {
            if (particle.geometry) particle.geometry.dispose();
            if (particle.material) particle.material.dispose();
            this.scene.remove(particle);
        });
        this.particles = [];
    }

    /**
     * Set character reference (if character loads late)
     * @param {THREE.Group} characterGroup - Character group
     */
    setCharacter(characterGroup) {
        this.characterGroup = characterGroup;
        console.log('🎵 Character set for instrument animator');
    }

    /**
     * Dispose animator
     */
    dispose() {
        this.stopPlaying();
        this.clearParticles();
        console.log('🎵 Instrument Animator disposed');
    }
}

// Export to global scope
window.InstrumentAnimator = InstrumentAnimator;

console.log('🎵 InstrumentAnimator loaded successfully');

})();
