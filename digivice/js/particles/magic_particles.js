/**
 * Magic Particle Effects System
 * Digimon skills and magic effects
 */

const THREE = window.THREE;

class MagicParticleSystem {
    constructor(scene) {
        this.scene = scene;
        this.activeMagicEffects = [];
        this.geometryCache = new Map();

        // Element types
        this.elements = {
            FIRE: { color: 0xff4400, glow: 0xff8800 },
            ICE: { color: 0x00ddff, glow: 0xaaffff },
            LIGHTNING: { color: 0xffff00, glow: 0xffffaa },
            EARTH: { color: 0x88aa44, glow: 0xaacc66 },
            WIND: { color: 0xccffcc, glow: 0xffffff },
            DARK: { color: 0x8800ff, glow: 0xcc66ff },
            LIGHT: { color: 0xffffaa, glow: 0xffffff },
            POISON: { color: 0x88ff00, glow: 0xaaff44 }
        };

        console.log('✨ Magic Particle System initialized');
    }

    /**
     * Cast fireball spell
     */
    castFireball(startPos, targetPos, onImpact) {
        const direction = new THREE.Vector3()
            .subVectors(targetPos, startPos)
            .normalize();

        // Create fireball mesh
        const geometry = new THREE.SphereGeometry(0.5, 16, 16);
        const material = new THREE.MeshBasicMaterial({
            color: this.elements.FIRE.color,
            transparent: true,
            opacity: 0.8
        });
        const fireball = new THREE.Mesh(geometry, material);
        fireball.position.copy(startPos);
        this.scene.add(fireball);

        // Add fire trail particles
        const trailSystem = this.createTrailSystem(this.elements.FIRE.color);
        this.scene.add(trailSystem);

        const effect = {
            mesh: fireball,
            trailSystem: trailSystem,
            velocity: direction.multiplyScalar(20),
            position: startPos.clone(),
            target: targetPos,
            lifetime: 3.0,
            onImpact: onImpact,
            type: 'projectile',
            trailPositions: []
        };

        this.activeMagicEffects.push(effect);
        return effect;
    }

    /**
     * Cast ice spike spell
     */
    castIceSpike(startPos, targetPos, onImpact) {
        const direction = new THREE.Vector3()
            .subVectors(targetPos, startPos)
            .normalize();

        // Create ice spike mesh
        const geometry = new THREE.ConeGeometry(0.3, 1.5, 8);
        const material = new THREE.MeshPhongMaterial({
            color: this.elements.ICE.color,
            transparent: true,
            opacity: 0.9,
            shininess: 100
        });
        const spike = new THREE.Mesh(geometry, material);
        spike.position.copy(startPos);

        // Orient spike towards target
        spike.lookAt(targetPos);
        spike.rotateX(Math.PI / 2);

        this.scene.add(spike);

        // Add frost trail
        const trailSystem = this.createTrailSystem(this.elements.ICE.color);
        this.scene.add(trailSystem);

        const effect = {
            mesh: spike,
            trailSystem: trailSystem,
            velocity: direction.multiplyScalar(25),
            position: startPos.clone(),
            target: targetPos,
            lifetime: 2.5,
            onImpact: onImpact,
            type: 'projectile',
            trailPositions: []
        };

        this.activeMagicEffects.push(effect);
        return effect;
    }

    /**
     * Cast lightning bolt
     */
    castLightning(startPos, targetPos, branches = 3) {
        const segments = 20;
        const points = [];
        const direction = new THREE.Vector3()
            .subVectors(targetPos, startPos);

        // Generate jagged lightning path
        for (let i = 0; i <= segments; i++) {
            const t = i / segments;
            const point = new THREE.Vector3()
                .lerpVectors(startPos, targetPos, t);

            // Add randomness for jagged effect
            if (i > 0 && i < segments) {
                point.x += (Math.random() - 0.5) * 2;
                point.y += (Math.random() - 0.5) * 2;
                point.z += (Math.random() - 0.5) * 2;
            }

            points.push(point);
        }

        // Create lightning geometry
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({
            color: this.elements.LIGHTNING.color,
            linewidth: 3,
            transparent: true,
            opacity: 1.0
        });
        const lightning = new THREE.Line(geometry, material);
        this.scene.add(lightning);

        // Add branches
        for (let b = 0; b < branches; b++) {
            const branchStart = Math.floor(segments * (0.3 + Math.random() * 0.4));
            const branchPoints = [points[branchStart]];

            for (let i = 0; i < 5; i++) {
                const lastPoint = branchPoints[branchPoints.length - 1];
                const branchPoint = lastPoint.clone();
                branchPoint.x += (Math.random() - 0.5) * 3;
                branchPoint.y += (Math.random() - 0.5) * 3;
                branchPoint.z += (Math.random() - 0.5) * 3;
                branchPoints.push(branchPoint);
            }

            const branchGeometry = new THREE.BufferGeometry().setFromPoints(branchPoints);
            const branchMaterial = new THREE.LineBasicMaterial({
                color: this.elements.LIGHTNING.color,
                linewidth: 2,
                transparent: true,
                opacity: 0.8
            });
            const branch = new THREE.Line(branchGeometry, branchMaterial);
            this.scene.add(branch);

            setTimeout(() => {
                this.scene.remove(branch);
                branch.geometry.dispose();
                branch.material.dispose();
            }, 200);
        }

        const effect = {
            mesh: lightning,
            lifetime: 0.2,
            type: 'instant'
        };

        this.activeMagicEffects.push(effect);

        // Create impact flash
        this.createImpactFlash(targetPos, this.elements.LIGHTNING.color);

        return effect;
    }

    /**
     * Cast healing spell
     */
    castHeal(position, amount = 50) {
        const particleCount = 50;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        const sizes = new Float32Array(particleCount);

        const color = new THREE.Color(this.elements.LIGHT.color);

        for (let i = 0; i < particleCount; i++) {
            // Start particles in a sphere around position
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.random() * Math.PI;
            const radius = 2 + Math.random();

            positions[i * 3] = position.x + radius * Math.sin(phi) * Math.cos(theta);
            positions[i * 3 + 1] = position.y + radius * Math.sin(phi) * Math.sin(theta);
            positions[i * 3 + 2] = position.z + radius * Math.cos(phi);

            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;

            sizes[i] = 0.3 + Math.random() * 0.2;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: 0.3,
            vertexColors: true,
            transparent: true,
            opacity: 1.0,
            blending: THREE.AdditiveBlending
        });

        const particles = new THREE.Points(geometry, material);
        this.scene.add(particles);

        const velocities = [];
        for (let i = 0; i < particleCount; i++) {
            // Particles move towards center
            const vel = new THREE.Vector3(
                position.x - positions[i * 3],
                position.y - positions[i * 3 + 1] + 1, // Slight upward bias
                position.z - positions[i * 3 + 2]
            ).normalize().multiplyScalar(2);
            velocities.push(vel);
        }

        const effect = {
            mesh: particles,
            velocities: velocities,
            lifetime: 2.0,
            type: 'heal',
            amount: amount
        };

        this.activeMagicEffects.push(effect);
        return effect;
    }

    /**
     * Cast area of effect spell (AOE)
     */
    castAOE(position, radius, element = 'FIRE') {
        const elementData = this.elements[element];

        // Create expanding ring
        const geometry = new THREE.RingGeometry(0.1, radius, 32);
        const material = new THREE.MeshBasicMaterial({
            color: elementData.color,
            transparent: true,
            opacity: 0.6,
            side: THREE.DoubleSide
        });
        const ring = new THREE.Mesh(geometry, material);
        ring.position.copy(position);
        ring.rotation.x = -Math.PI / 2; // Flat on ground
        this.scene.add(ring);

        // Create upward particle burst
        const particleCount = 100;
        const particleGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        const sizes = new Float32Array(particleCount);

        const color = new THREE.Color(elementData.color);

        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * radius;

            positions[i * 3] = position.x + Math.cos(angle) * distance;
            positions[i * 3 + 1] = position.y;
            positions[i * 3 + 2] = position.z + Math.sin(angle) * distance;

            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;

            sizes[i] = 0.4 + Math.random() * 0.3;
        }

        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        particleGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const particleMaterial = new THREE.PointsMaterial({
            size: 0.4,
            vertexColors: true,
            transparent: true,
            opacity: 1.0,
            blending: THREE.AdditiveBlending
        });

        const particles = new THREE.Points(particleGeometry, particleMaterial);
        this.scene.add(particles);

        const velocities = [];
        for (let i = 0; i < particleCount; i++) {
            velocities.push(new THREE.Vector3(0, 5 + Math.random() * 3, 0));
        }

        const effect = {
            mesh: ring,
            particles: particles,
            velocities: velocities,
            lifetime: 1.5,
            type: 'aoe',
            radius: radius
        };

        this.activeMagicEffects.push(effect);
        return effect;
    }

    /**
     * Cast buff effect (floating runes around character)
     */
    castBuff(position, buffType = 'POWER') {
        const elementData = this.elements[buffType] || this.elements.LIGHT;
        const runeCount = 6;
        const runes = [];

        for (let i = 0; i < runeCount; i++) {
            const angle = (Math.PI * 2 * i) / runeCount;
            const geometry = new THREE.PlaneGeometry(0.5, 0.5);
            const material = new THREE.MeshBasicMaterial({
                color: elementData.color,
                transparent: true,
                opacity: 0.7,
                side: THREE.DoubleSide
            });
            const rune = new THREE.Mesh(geometry, material);

            const radius = 2;
            rune.position.set(
                position.x + Math.cos(angle) * radius,
                position.y + 1 + Math.sin(i * 0.5),
                position.z + Math.sin(angle) * radius
            );

            this.scene.add(rune);
            runes.push({
                mesh: rune,
                angle: angle,
                radius: radius,
                baseY: position.y + 1
            });
        }

        const effect = {
            runes: runes,
            center: position.clone(),
            lifetime: 10.0,
            type: 'buff',
            rotationSpeed: 1.0
        };

        this.activeMagicEffects.push(effect);
        return effect;
    }

    /**
     * Create trail system for projectiles
     */
    createTrailSystem(color) {
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(100 * 3);
        const colors = new Float32Array(100 * 3);
        const sizes = new Float32Array(100);

        const col = new THREE.Color(color);

        for (let i = 0; i < 100; i++) {
            colors[i * 3] = col.r;
            colors[i * 3 + 1] = col.g;
            colors[i * 3 + 2] = col.b;
            sizes[i] = 0.3;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: 0.3,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });

        return new THREE.Points(geometry, material);
    }

    /**
     * Create impact flash effect
     */
    createImpactFlash(position, color) {
        const geometry = new THREE.SphereGeometry(1, 16, 16);
        const material = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 1.0
        });
        const flash = new THREE.Mesh(geometry, material);
        flash.position.copy(position);
        this.scene.add(flash);

        const effect = {
            mesh: flash,
            lifetime: 0.3,
            type: 'flash',
            maxScale: 3
        };

        this.activeMagicEffects.push(effect);
    }

    /**
     * Update all active magic effects
     */
    update(deltaTime) {
        for (let i = this.activeMagicEffects.length - 1; i >= 0; i--) {
            const effect = this.activeMagicEffects[i];
            effect.lifetime -= deltaTime;

            if (effect.lifetime <= 0) {
                this.removeEffect(effect, i);
                continue;
            }

            // Update based on effect type
            switch (effect.type) {
                case 'projectile':
                    this.updateProjectile(effect, deltaTime);
                    break;
                case 'heal':
                    this.updateHeal(effect, deltaTime);
                    break;
                case 'aoe':
                    this.updateAOE(effect, deltaTime);
                    break;
                case 'buff':
                    this.updateBuff(effect, deltaTime);
                    break;
                case 'flash':
                    this.updateFlash(effect, deltaTime);
                    break;
                case 'instant':
                    // Just fade out
                    if (effect.mesh.material) {
                        effect.mesh.material.opacity = effect.lifetime / 0.2;
                    }
                    break;
            }
        }
    }

    /**
     * Update projectile effects
     */
    updateProjectile(effect, deltaTime) {
        // Move projectile
        effect.position.add(effect.velocity.clone().multiplyScalar(deltaTime));
        effect.mesh.position.copy(effect.position);

        // Update trail
        if (effect.trailSystem) {
            effect.trailPositions.push(effect.position.clone());
            if (effect.trailPositions.length > 20) {
                effect.trailPositions.shift();
            }

            const positions = effect.trailSystem.geometry.attributes.position.array;
            for (let i = 0; i < effect.trailPositions.length; i++) {
                const pos = effect.trailPositions[i];
                positions[i * 3] = pos.x;
                positions[i * 3 + 1] = pos.y;
                positions[i * 3 + 2] = pos.z;
            }
            effect.trailSystem.geometry.attributes.position.needsUpdate = true;
        }

        // Check if reached target
        if (effect.position.distanceTo(effect.target) < 1) {
            if (effect.onImpact) {
                effect.onImpact(effect.position);
            }
            effect.lifetime = 0;
        }
    }

    /**
     * Update heal effects
     */
    updateHeal(effect, deltaTime) {
        const positions = effect.mesh.geometry.attributes.position.array;
        const sizes = effect.mesh.geometry.attributes.size.array;

        for (let i = 0; i < effect.velocities.length; i++) {
            positions[i * 3] += effect.velocities[i].x * deltaTime;
            positions[i * 3 + 1] += effect.velocities[i].y * deltaTime;
            positions[i * 3 + 2] += effect.velocities[i].z * deltaTime;

            // Fade out
            sizes[i] *= 0.98;
        }

        effect.mesh.geometry.attributes.position.needsUpdate = true;
        effect.mesh.geometry.attributes.size.needsUpdate = true;
        effect.mesh.material.opacity = effect.lifetime / 2.0;
    }

    /**
     * Update AOE effects
     */
    updateAOE(effect, deltaTime) {
        // Fade ring
        effect.mesh.material.opacity = effect.lifetime / 1.5 * 0.6;

        // Update particles
        if (effect.particles) {
            const positions = effect.particles.geometry.attributes.position.array;
            const sizes = effect.particles.geometry.attributes.size.array;

            for (let i = 0; i < effect.velocities.length; i++) {
                positions[i * 3 + 1] += effect.velocities[i].y * deltaTime;
                sizes[i] *= 0.97;
            }

            effect.particles.geometry.attributes.position.needsUpdate = true;
            effect.particles.geometry.attributes.size.needsUpdate = true;
            effect.particles.material.opacity = effect.lifetime / 1.5;
        }
    }

    /**
     * Update buff effects
     */
    updateBuff(effect, deltaTime) {
        const time = Date.now() * 0.001;

        effect.runes.forEach((rune, i) => {
            rune.angle += effect.rotationSpeed * deltaTime;

            rune.mesh.position.x = effect.center.x + Math.cos(rune.angle) * rune.radius;
            rune.mesh.position.y = rune.baseY + Math.sin(time * 2 + i) * 0.3;
            rune.mesh.position.z = effect.center.z + Math.sin(rune.angle) * rune.radius;

            rune.mesh.rotation.y = rune.angle + Math.PI / 2;
        });

        // Fade out near end
        if (effect.lifetime < 1.0) {
            effect.runes.forEach(rune => {
                rune.mesh.material.opacity = effect.lifetime * 0.7;
            });
        }
    }

    /**
     * Update flash effects
     */
    updateFlash(effect, deltaTime) {
        const scale = 1 + (1 - effect.lifetime / 0.3) * effect.maxScale;
        effect.mesh.scale.set(scale, scale, scale);
        effect.mesh.material.opacity = effect.lifetime / 0.3;
    }

    /**
     * Remove effect and cleanup
     */
    removeEffect(effect, index) {
        if (effect.mesh) {
            this.scene.remove(effect.mesh);
            if (effect.mesh.geometry) effect.mesh.geometry.dispose();
            if (effect.mesh.material) effect.mesh.material.dispose();
        }

        if (effect.trailSystem) {
            this.scene.remove(effect.trailSystem);
            effect.trailSystem.geometry.dispose();
            effect.trailSystem.material.dispose();
        }

        if (effect.particles) {
            this.scene.remove(effect.particles);
            effect.particles.geometry.dispose();
            effect.particles.material.dispose();
        }

        if (effect.runes) {
            effect.runes.forEach(rune => {
                this.scene.remove(rune.mesh);
                rune.mesh.geometry.dispose();
                rune.mesh.material.dispose();
            });
        }

        this.activeMagicEffects.splice(index, 1);
    }

    /**
     * Clear all active effects
     */
    clearAll() {
        while (this.activeMagicEffects.length > 0) {
            this.removeEffect(this.activeMagicEffects[0], 0);
        }
    }

    /**
     * Dispose of all resources
     */
    dispose() {
        this.clearAll();
        this.geometryCache.forEach(geometry => geometry.dispose());
        this.geometryCache.clear();
    }
}

// Make globally available
window.MagicParticleSystem = MagicParticleSystem;
