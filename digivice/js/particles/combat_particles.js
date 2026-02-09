/**
 * Combat Particle Effects System
 * Digimon World style combat particles with Three.js
 */

import * as THREE from 'three';

export class CombatParticleSystem {
    constructor(scene) {
        this.scene = scene;
        this.particlePools = new Map();
        this.activeParticles = [];

        // Particle configuration
        this.config = {
            maxParticles: 10000,
            poolSize: 1000,
            gravity: -9.8,
            windStrength: 0
        };

        this.initializeParticlePools();

        console.log('🎆 Combat Particle System initialized');
    }

    /**
     * Initialize particle pools for performance
     */
    initializeParticlePools() {
        // Hit effect pool
        this.createParticlePool('hit', {
            count: 200,
            size: 0.3,
            color: 0xffaa00,
            lifetime: 0.5
        });

        // Slash effect pool
        this.createParticlePool('slash', {
            count: 150,
            size: 0.5,
            color: 0xffffff,
            lifetime: 0.4
        });

        // Blood/Impact pool
        this.createParticlePool('blood', {
            count: 300,
            size: 0.2,
            color: 0xff0000,
            lifetime: 1.0
        });

        // Shield block pool
        this.createParticlePool('shield', {
            count: 100,
            size: 0.4,
            color: 0x00ffff,
            lifetime: 0.6
        });

        // Critical hit pool
        this.createParticlePool('critical', {
            count: 200,
            size: 0.6,
            color: 0xffff00,
            lifetime: 0.8
        });

        // Dodge trail pool
        this.createParticlePool('dodge', {
            count: 150,
            size: 0.3,
            color: 0xcccccc,
            lifetime: 0.5
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
     * Emit hit effect particles
     */
    emitHit(position, direction, intensity = 1.0) {
        this.emitParticles('hit', {
            position: position,
            direction: direction,
            count: Math.floor(20 * intensity),
            speed: 5.0 * intensity,
            spread: Math.PI / 4
        });
    }

    /**
     * Emit slash effect particles
     */
    emitSlash(startPos, endPos, slashType = 'horizontal') {
        const direction = new THREE.Vector3()
            .subVectors(endPos, startPos)
            .normalize();

        // Create trail particles along slash path
        const steps = 10;
        for (let i = 0; i < steps; i++) {
            const t = i / steps;
            const pos = new THREE.Vector3().lerpVectors(startPos, endPos, t);

            this.emitParticles('slash', {
                position: pos,
                direction: direction,
                count: 15,
                speed: 8.0,
                spread: Math.PI / 6
            });
        }
    }

    /**
     * Emit blood/impact particles
     */
    emitBlood(position, direction, amount = 1.0) {
        this.emitParticles('blood', {
            position: position,
            direction: direction,
            count: Math.floor(30 * amount),
            speed: 4.0,
            spread: Math.PI / 3,
            gravity: true
        });
    }

    /**
     * Emit shield block particles
     */
    emitShieldBlock(position, impactDirection) {
        // Create expanding ring effect
        const ringCount = 3;
        for (let ring = 0; ring < ringCount; ring++) {
            setTimeout(() => {
                this.emitParticles('shield', {
                    position: position,
                    direction: impactDirection,
                    count: 30,
                    speed: 6.0 + ring * 2,
                    spread: Math.PI * 2,
                    pattern: 'ring'
                });
            }, ring * 50);
        }
    }

    /**
     * Emit critical hit particles
     */
    emitCritical(position) {
        // Star burst pattern
        const directions = 8;
        for (let i = 0; i < directions; i++) {
            const angle = (Math.PI * 2 * i) / directions;
            const dir = new THREE.Vector3(
                Math.cos(angle),
                Math.sin(angle),
                0
            );

            this.emitParticles('critical', {
                position: position,
                direction: dir,
                count: 25,
                speed: 10.0,
                spread: Math.PI / 12
            });
        }

        // Add upward burst
        this.emitParticles('critical', {
            position: position,
            direction: new THREE.Vector3(0, 1, 0),
            count: 40,
            speed: 12.0,
            spread: Math.PI / 4
        });
    }

    /**
     * Emit dodge trail particles
     */
    emitDodgeTrail(startPos, endPos) {
        const steps = 15;
        const direction = new THREE.Vector3()
            .subVectors(endPos, startPos)
            .normalize();

        for (let i = 0; i < steps; i++) {
            const t = i / steps;
            const pos = new THREE.Vector3().lerpVectors(startPos, endPos, t);

            setTimeout(() => {
                this.emitParticles('dodge', {
                    position: pos,
                    direction: direction,
                    count: 10,
                    speed: 2.0,
                    spread: Math.PI / 8
                });
            }, i * 20);
        }
    }

    /**
     * Generic particle emission
     */
    emitParticles(type, params) {
        const pool = this.particlePools.get(type);
        if (!pool) {
            console.warn(`Particle pool '${type}' not found`);
            return;
        }

        const {
            position,
            direction,
            count,
            speed,
            spread,
            pattern = 'cone',
            gravity = false
        } = params;

        const geometry = pool.system.geometry;
        const positions = geometry.attributes.position.array;
        const colors = geometry.attributes.color.array;
        const sizes = geometry.attributes.size.array;
        const lifetimes = geometry.attributes.lifetime.array;

        const baseColor = new THREE.Color(pool.config.color);

        for (let i = 0; i < count; i++) {
            const index = pool.activeCount;
            if (index >= pool.config.count) break;

            // Position
            positions[index * 3] = position.x;
            positions[index * 3 + 1] = position.y;
            positions[index * 3 + 2] = position.z;

            // Velocity (randomized within spread)
            let velocity;
            if (pattern === 'ring') {
                const angle = Math.random() * Math.PI * 2;
                velocity = new THREE.Vector3(
                    Math.cos(angle),
                    0,
                    Math.sin(angle)
                ).multiplyScalar(speed);
            } else if (pattern === 'cone') {
                const spreadAngle = (Math.random() - 0.5) * spread;
                const spreadVector = new THREE.Vector3(
                    Math.random() - 0.5,
                    Math.random() - 0.5,
                    Math.random() - 0.5
                ).normalize().multiplyScalar(Math.tan(spreadAngle));

                velocity = direction.clone()
                    .add(spreadVector)
                    .normalize()
                    .multiplyScalar(speed * (0.8 + Math.random() * 0.4));
            }

            // Color with variance
            const colorVariance = 0.2;
            colors[index * 3] = baseColor.r * (1 + (Math.random() - 0.5) * colorVariance);
            colors[index * 3 + 1] = baseColor.g * (1 + (Math.random() - 0.5) * colorVariance);
            colors[index * 3 + 2] = baseColor.b * (1 + (Math.random() - 0.5) * colorVariance);

            // Size
            sizes[index] = pool.config.size * (0.8 + Math.random() * 0.4);

            // Lifetime
            lifetimes[index] = pool.config.lifetime;

            // Store particle data
            pool.particles[index] = {
                active: true,
                velocity: velocity,
                lifetime: pool.config.lifetime,
                maxLifetime: pool.config.lifetime,
                gravity: gravity
            };

            pool.activeCount++;
        }

        geometry.attributes.position.needsUpdate = true;
        geometry.attributes.color.needsUpdate = true;
        geometry.attributes.size.needsUpdate = true;
        geometry.attributes.lifetime.needsUpdate = true;
    }

    /**
     * Update all active particles
     */
    update(deltaTime) {
        this.particlePools.forEach((pool, type) => {
            this.updateParticlePool(pool, deltaTime);
        });
    }

    /**
     * Update a specific particle pool
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

            // Apply gravity
            if (particle.gravity) {
                particle.velocity.y += this.config.gravity * deltaTime;
            }

            // Apply drag
            particle.velocity.multiplyScalar(0.98);

            // Fade out based on lifetime
            const lifetimeRatio = particle.lifetime / particle.maxLifetime;
            sizes[i] = pool.config.size * lifetimeRatio;
            lifetimes[i] = lifetimeRatio;

            needsUpdate = true;
        }

        if (needsUpdate) {
            geometry.attributes.position.needsUpdate = true;
            geometry.attributes.size.needsUpdate = true;
            geometry.attributes.lifetime.needsUpdate = true;
        }

        // Compact active particles
        this.compactParticlePool(pool);
    }

    /**
     * Compact particle pool by removing inactive particles
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
    }

    /**
     * Set wind strength for particle drift
     */
    setWind(strength, direction = new THREE.Vector3(1, 0, 0)) {
        this.config.windStrength = strength;
        this.config.windDirection = direction.normalize();
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
        this.activeParticles = [];
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
            poolStats
        };
    }
}

// Make globally available
window.CombatParticleSystem = CombatParticleSystem;
