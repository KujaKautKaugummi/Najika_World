/**
 * Evolution Transformation Particle Effects
 * Digimon-style evolution sequences with dramatic particle effects
 */

import * as THREE from 'three';

export class EvolutionEffectSystem {
    constructor(scene) {
        this.scene = scene;
        this.activeEvolutions = [];
        this.particlePools = new Map();

        // Evolution configuration
        this.config = {
            maxParticles: 15000,
            evolutionDuration: 5.0, // seconds
            cocoonDuration: 2.0,
            burstDuration: 1.5,
            raysCount: 12
        };

        this.initializeParticlePools();

        console.log('✨ Evolution Effect System initialized');
    }

    /**
     * Initialize particle pools for evolution effects
     */
    initializeParticlePools() {
        // Energy spiral pool
        this.createParticlePool('spiral', {
            count: 2000,
            size: 0.4,
            color: 0x00ffff,
            lifetime: 3.0
        });

        // Cocoon shell pool
        this.createParticlePool('cocoon', {
            count: 1500,
            size: 0.3,
            color: 0xffffff,
            lifetime: 2.5
        });

        // Burst explosion pool
        this.createParticlePool('burst', {
            count: 3000,
            size: 0.6,
            color: 0xffff00,
            lifetime: 1.5
        });

        // Light rays pool
        this.createParticlePool('rays', {
            count: 1000,
            size: 1.0,
            color: 0xffffff,
            lifetime: 2.0
        });

        // Energy orbs pool
        this.createParticlePool('orbs', {
            count: 500,
            size: 0.8,
            color: 0xff00ff,
            lifetime: 4.0
        });

        // DNA helix pool
        this.createParticlePool('dna', {
            count: 800,
            size: 0.3,
            color: 0x00ff00,
            lifetime: 3.5
        });
    }

    /**
     * Create a particle pool
     */
    createParticlePool(type, config) {
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(config.count * 3);
        const colors = new Float32Array(config.count * 3);
        const sizes = new Float32Array(config.count);
        const lifetimes = new Float32Array(config.count);

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        geometry.setAttribute('lifetime', new THREE.BufferAttribute(lifetimes, 1));

        const material = new THREE.PointsMaterial({
            size: config.size,
            vertexColors: true,
            transparent: true,
            opacity: 1.0,
            blending: THREE.AdditiveBlending,
            depthWrite: false,
            sizeAttenuation: true
        });

        const particleSystem = new THREE.Points(geometry, material);
        particleSystem.frustumCulled = false;
        this.scene.add(particleSystem);

        this.particlePools.set(type, {
            system: particleSystem,
            config: config,
            activeCount: 0,
            particles: []
        });
    }

    /**
     * Start evolution sequence
     */
    startEvolution(position, evolutionType = 'champion', targetScale = 1.5) {
        const evolution = {
            id: Date.now(),
            position: position.clone(),
            startTime: performance.now() / 1000,
            phase: 'gathering', // gathering -> cocoon -> burst -> complete
            type: evolutionType,
            targetScale: targetScale,
            currentRotation: 0,
            intensity: 1.0
        };

        this.activeEvolutions.push(evolution);

        // Start gathering phase
        this.startGatheringPhase(evolution);

        console.log(`🌟 Evolution started: ${evolutionType}`);

        return evolution.id;
    }

    /**
     * Phase 1: Energy gathering spiral
     */
    startGatheringPhase(evolution) {
        const duration = 1.5;
        const startTime = performance.now() / 1000;

        // Create upward spiraling energy
        const spiralInterval = setInterval(() => {
            const elapsed = (performance.now() / 1000) - startTime;

            if (elapsed >= duration) {
                clearInterval(spiralInterval);
                evolution.phase = 'cocoon';
                this.startCocoonPhase(evolution);
                return;
            }

            // Emit spiral particles from below
            const basePos = evolution.position.clone();
            basePos.y -= 5;

            this.emitEnergySpiral(basePos, evolution.position, evolution.currentRotation);
            evolution.currentRotation += 0.3;

        }, 50);
    }

    /**
     * Phase 2: Cocoon formation
     */
    startCocoonPhase(evolution) {
        const duration = this.config.cocoonDuration;
        const startTime = performance.now() / 1000;

        // Create DNA helix effect
        this.emitDNAHelix(evolution.position);

        // Form protective cocoon
        const cocoonInterval = setInterval(() => {
            const elapsed = (performance.now() / 1000) - startTime;

            if (elapsed >= duration) {
                clearInterval(cocoonInterval);
                evolution.phase = 'burst';
                this.startBurstPhase(evolution);
                return;
            }

            // Emit cocoon shell particles
            this.emitCocoonShell(evolution.position, elapsed / duration);

            // Emit pulsing energy orbs
            if (Math.random() < 0.3) {
                this.emitEnergyOrbs(evolution.position);
            }

        }, 50);
    }

    /**
     * Phase 3: Dramatic burst
     */
    startBurstPhase(evolution) {
        const duration = this.config.burstDuration;
        const startTime = performance.now() / 1000;

        // Initial massive burst
        this.emitMassiveBurst(evolution.position);

        // Light rays bursting outward
        this.emitLightRays(evolution.position, this.config.raysCount);

        const burstInterval = setInterval(() => {
            const elapsed = (performance.now() / 1000) - startTime;

            if (elapsed >= duration) {
                clearInterval(burstInterval);
                evolution.phase = 'complete';
                this.completeEvolution(evolution);
                return;
            }

            // Continue emitting burst particles
            const intensity = 1 - (elapsed / duration);
            this.emitBurstRings(evolution.position, intensity);

        }, 100);
    }

    /**
     * Evolution complete
     */
    completeEvolution(evolution) {
        // Final flash effect
        this.emitFinalFlash(evolution.position);

        // Remove from active evolutions after delay
        setTimeout(() => {
            const index = this.activeEvolutions.findIndex(e => e.id === evolution.id);
            if (index !== -1) {
                this.activeEvolutions.splice(index, 1);
            }
        }, 2000);

        console.log(`✨ Evolution complete!`);
    }

    /**
     * Emit upward energy spiral
     */
    emitEnergySpiral(fromPos, toPos, rotation) {
        const pool = this.particlePools.get('spiral');
        if (!pool) return;

        const particleCount = 30;
        const height = toPos.y - fromPos.y;

        for (let i = 0; i < particleCount; i++) {
            const t = Math.random();
            const angle = rotation + t * Math.PI * 4;
            const radius = 2 * (1 - t);

            const position = new THREE.Vector3(
                fromPos.x + Math.cos(angle) * radius,
                fromPos.y + height * t,
                fromPos.z + Math.sin(angle) * radius
            );

            const velocity = new THREE.Vector3(
                -Math.sin(angle) * 2,
                5,
                Math.cos(angle) * 2
            );

            this.emitParticle(pool, position, velocity, 'spiral');
        }
    }

    /**
     * Emit DNA helix pattern
     */
    emitDNAHelix(center) {
        const pool = this.particlePools.get('dna');
        if (!pool) return;

        const helixCount = 2;
        const pointsPerHelix = 50;
        const height = 4;
        const radius = 1.5;

        for (let h = 0; h < helixCount; h++) {
            const offset = (Math.PI * 2 / helixCount) * h;

            for (let i = 0; i < pointsPerHelix; i++) {
                const t = i / pointsPerHelix;
                const angle = t * Math.PI * 4 + offset;
                const y = center.y - height / 2 + t * height;

                const position = new THREE.Vector3(
                    center.x + Math.cos(angle) * radius,
                    y,
                    center.z + Math.sin(angle) * radius
                );

                const velocity = new THREE.Vector3(
                    Math.cos(angle) * 0.5,
                    (Math.random() - 0.5) * 0.5,
                    Math.sin(angle) * 0.5
                );

                this.emitParticle(pool, position, velocity, 'helix');
            }
        }
    }

    /**
     * Emit cocoon shell particles
     */
    emitCocoonShell(center, progress) {
        const pool = this.particlePools.get('cocoon');
        if (!pool) return;

        const particleCount = 40;
        const radius = 2 - progress * 0.5;

        for (let i = 0; i < particleCount; i++) {
            const phi = Math.random() * Math.PI * 2;
            const theta = Math.random() * Math.PI;

            const position = new THREE.Vector3(
                center.x + radius * Math.sin(theta) * Math.cos(phi),
                center.y + radius * Math.cos(theta),
                center.z + radius * Math.sin(theta) * Math.sin(phi)
            );

            const velocity = new THREE.Vector3()
                .subVectors(position, center)
                .normalize()
                .multiplyScalar(0.5);

            this.emitParticle(pool, position, velocity, 'cocoon');
        }
    }

    /**
     * Emit energy orbs
     */
    emitEnergyOrbs(center) {
        const pool = this.particlePools.get('orbs');
        if (!pool) return;

        const orbCount = 5;

        for (let i = 0; i < orbCount; i++) {
            const angle = (Math.PI * 2 * i) / orbCount + Math.random() * 0.5;
            const radius = 1.5 + Math.random();

            const position = new THREE.Vector3(
                center.x + Math.cos(angle) * radius,
                center.y + (Math.random() - 0.5) * 2,
                center.z + Math.sin(angle) * radius
            );

            const velocity = new THREE.Vector3(
                (Math.random() - 0.5) * 0.5,
                0.5,
                (Math.random() - 0.5) * 0.5
            );

            this.emitParticle(pool, position, velocity, 'orbit');
        }
    }

    /**
     * Emit massive burst explosion
     */
    emitMassiveBurst(center) {
        const pool = this.particlePools.get('burst');
        if (!pool) return;

        const particleCount = 500;

        for (let i = 0; i < particleCount; i++) {
            const phi = Math.random() * Math.PI * 2;
            const theta = Math.random() * Math.PI;

            const direction = new THREE.Vector3(
                Math.sin(theta) * Math.cos(phi),
                Math.sin(theta) * Math.sin(phi),
                Math.cos(theta)
            );

            const speed = 8 + Math.random() * 4;
            const velocity = direction.multiplyScalar(speed);

            this.emitParticle(pool, center.clone(), velocity, 'burst');
        }
    }

    /**
     * Emit light rays
     */
    emitLightRays(center, count) {
        const pool = this.particlePools.get('rays');
        if (!pool) return;

        for (let i = 0; i < count; i++) {
            const angle = (Math.PI * 2 * i) / count;

            const direction = new THREE.Vector3(
                Math.cos(angle),
                0.2,
                Math.sin(angle)
            ).normalize();

            // Create ray particles along the direction
            for (let j = 0; j < 20; j++) {
                const distance = j * 0.5;
                const position = center.clone().add(
                    direction.clone().multiplyScalar(distance)
                );

                const velocity = direction.clone().multiplyScalar(10);

                this.emitParticle(pool, position, velocity, 'ray');
            }
        }
    }

    /**
     * Emit burst rings
     */
    emitBurstRings(center, intensity) {
        const pool = this.particlePools.get('burst');
        if (!pool) return;

        const particleCount = Math.floor(60 * intensity);
        const radius = 3 * (1 - intensity);

        for (let i = 0; i < particleCount; i++) {
            const angle = (Math.PI * 2 * i) / particleCount;

            const position = new THREE.Vector3(
                center.x + Math.cos(angle) * radius,
                center.y + (Math.random() - 0.5) * 0.5,
                center.z + Math.sin(angle) * radius
            );

            const velocity = new THREE.Vector3(
                Math.cos(angle) * 5,
                2,
                Math.sin(angle) * 5
            );

            this.emitParticle(pool, position, velocity, 'ring');
        }
    }

    /**
     * Emit final flash effect
     */
    emitFinalFlash(center) {
        const pool = this.particlePools.get('burst');
        if (!pool) return;

        // Create expanding sphere
        const particleCount = 300;

        for (let i = 0; i < particleCount; i++) {
            const phi = Math.random() * Math.PI * 2;
            const theta = Math.random() * Math.PI;

            const direction = new THREE.Vector3(
                Math.sin(theta) * Math.cos(phi),
                Math.sin(theta) * Math.sin(phi),
                Math.cos(theta)
            );

            const speed = 15;
            const velocity = direction.multiplyScalar(speed);

            this.emitParticle(pool, center.clone(), velocity, 'flash');
        }
    }

    /**
     * Generic particle emission helper
     */
    emitParticle(pool, position, velocity, particleType = 'default') {
        const index = pool.activeCount;
        if (index >= pool.config.count) return;

        const geometry = pool.system.geometry;
        const positions = geometry.attributes.position.array;
        const colors = geometry.attributes.color.array;
        const sizes = geometry.attributes.size.array;
        const lifetimes = geometry.attributes.lifetime.array;

        // Position
        positions[index * 3] = position.x;
        positions[index * 3 + 1] = position.y;
        positions[index * 3 + 2] = position.z;

        // Color with variance
        const baseColor = new THREE.Color(pool.config.color);
        const colorVariance = 0.3;

        colors[index * 3] = Math.min(1, baseColor.r * (1 + (Math.random() - 0.5) * colorVariance));
        colors[index * 3 + 1] = Math.min(1, baseColor.g * (1 + (Math.random() - 0.5) * colorVariance));
        colors[index * 3 + 2] = Math.min(1, baseColor.b * (1 + (Math.random() - 0.5) * colorVariance));

        // Size
        sizes[index] = pool.config.size * (0.7 + Math.random() * 0.6);

        // Lifetime
        lifetimes[index] = pool.config.lifetime;

        // Store particle data
        pool.particles[index] = {
            active: true,
            velocity: velocity.clone(),
            lifetime: pool.config.lifetime,
            maxLifetime: pool.config.lifetime,
            type: particleType
        };

        pool.activeCount++;

        geometry.attributes.position.needsUpdate = true;
        geometry.attributes.color.needsUpdate = true;
        geometry.attributes.size.needsUpdate = true;
        geometry.attributes.lifetime.needsUpdate = true;
    }

    /**
     * Update all evolution effects
     */
    update(deltaTime) {
        // Update particle pools
        this.particlePools.forEach((pool) => {
            this.updateParticlePool(pool, deltaTime);
        });
    }

    /**
     * Update particle pool
     */
    updateParticlePool(pool, deltaTime) {
        const geometry = pool.system.geometry;
        const positions = geometry.attributes.position.array;
        const sizes = geometry.attributes.size.array;
        const lifetimes = geometry.attributes.lifetime.array;

        let needsUpdate = false;

        for (let i = 0; i < pool.activeCount; i++) {
            const particle = pool.particles[i];
            if (!particle || !particle.active) continue;

            // Update lifetime
            particle.lifetime -= deltaTime;

            if (particle.lifetime <= 0) {
                particle.active = false;
                sizes[i] = 0;
                needsUpdate = true;
                continue;
            }

            // Update position
            positions[i * 3] += particle.velocity.x * deltaTime;
            positions[i * 3 + 1] += particle.velocity.y * deltaTime;
            positions[i * 3 + 2] += particle.velocity.z * deltaTime;

            // Apply type-specific behavior
            switch (particle.type) {
                case 'spiral':
                    // Spirals slow down and fade
                    particle.velocity.multiplyScalar(0.95);
                    break;

                case 'orbit':
                    // Orbs float and pulse
                    particle.velocity.y += Math.sin(performance.now() / 200) * 0.1;
                    break;

                case 'helix':
                    // DNA particles maintain course
                    particle.velocity.multiplyScalar(0.99);
                    break;

                case 'burst':
                case 'flash':
                    // Burst particles slow down with drag
                    particle.velocity.multiplyScalar(0.90);
                    break;

                case 'ray':
                    // Rays maintain speed longer
                    particle.velocity.multiplyScalar(0.98);
                    break;

                default:
                    particle.velocity.multiplyScalar(0.96);
            }

            // Fade out based on lifetime
            const lifetimeRatio = particle.lifetime / particle.maxLifetime;
            sizes[i] = pool.config.size * lifetimeRatio * (0.7 + Math.random() * 0.6);
            lifetimes[i] = lifetimeRatio;

            needsUpdate = true;
        }

        if (needsUpdate) {
            geometry.attributes.position.needsUpdate = true;
            geometry.attributes.size.needsUpdate = true;
            geometry.attributes.lifetime.needsUpdate = true;
        }

        // Compact pool
        this.compactParticlePool(pool);
    }

    /**
     * Compact particle pool
     */
    compactParticlePool(pool) {
        let writeIndex = 0;
        const geometry = pool.system.geometry;
        const positions = geometry.attributes.position.array;
        const colors = geometry.attributes.color.array;
        const sizes = geometry.attributes.size.array;
        const lifetimes = geometry.attributes.lifetime.array;

        for (let i = 0; i < pool.activeCount; i++) {
            const particle = pool.particles[i];
            if (particle && particle.active) {
                if (writeIndex !== i) {
                    // Copy particle data
                    positions[writeIndex * 3] = positions[i * 3];
                    positions[writeIndex * 3 + 1] = positions[i * 3 + 1];
                    positions[writeIndex * 3 + 2] = positions[i * 3 + 2];

                    colors[writeIndex * 3] = colors[i * 3];
                    colors[writeIndex * 3 + 1] = colors[i * 3 + 1];
                    colors[writeIndex * 3 + 2] = colors[i * 3 + 2];

                    sizes[writeIndex] = sizes[i];
                    lifetimes[writeIndex] = lifetimes[i];

                    pool.particles[writeIndex] = particle;
                }
                writeIndex++;
            }
        }

        pool.activeCount = writeIndex;
    }

    /**
     * Clear all particles
     */
    clearAll() {
        this.particlePools.forEach((pool) => {
            pool.activeCount = 0;
            pool.particles = [];

            const geometry = pool.system.geometry;
            const sizes = geometry.attributes.size.array;
            for (let i = 0; i < sizes.length; i++) {
                sizes[i] = 0;
            }
            geometry.attributes.size.needsUpdate = true;
        });

        this.activeEvolutions = [];
    }

    /**
     * Dispose of all resources
     */
    dispose() {
        this.particlePools.forEach((pool) => {
            this.scene.remove(pool.system);
            pool.system.geometry.dispose();
            pool.system.material.dispose();
        });
        this.particlePools.clear();
        this.activeEvolutions = [];
    }

    /**
     * Get statistics
     */
    getStats() {
        let totalActive = 0;
        const poolStats = {};

        this.particlePools.forEach((pool, type) => {
            poolStats[type] = pool.activeCount;
            totalActive += pool.activeCount;
        });

        return {
            totalActive,
            maxParticles: this.config.maxParticles,
            poolStats,
            activeEvolutions: this.activeEvolutions.length
        };
    }
}

// Make globally available
window.EvolutionEffectSystem = EvolutionEffectSystem;
