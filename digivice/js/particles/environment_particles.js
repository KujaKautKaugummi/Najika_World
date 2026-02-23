/**
 * Environment Particle System
 * Footsteps, dust, debris, environmental effects
 */

// THREE is loaded globally

class EnvironmentParticleSystem {
    constructor(scene) {
        this.scene = scene;
        this.activeEffects = [];

        // Terrain types for different footstep effects
        this.terrainTypes = {
            GRASS: { color: 0x66aa44, particleSize: 0.2 },
            DIRT: { color: 0xaa8844, particleSize: 0.3 },
            SAND: { color: 0xffdd88, particleSize: 0.25 },
            SNOW: { color: 0xffffff, particleSize: 0.3 },
            WATER: { color: 0x4488ff, particleSize: 0.4 },
            STONE: { color: 0x888888, particleSize: 0.15 }
        };

        console.log('🌍 Environment Particle System initialized');
    }

    /**
     * Emit footstep particles
     */
    emitFootstep(position, terrain = 'GRASS', intensity = 1.0) {
        const terrainData = this.terrainTypes[terrain] || this.terrainTypes.GRASS;
        const particleCount = Math.floor(15 * intensity);

        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const velocities = [];
        const colors = new Float32Array(particleCount * 3);
        const sizes = new Float32Array(particleCount);

        const color = new THREE.Color(terrainData.color);

        for (let i = 0; i < particleCount; i++) {
            // Spread in a circle around footstep
            const angle = Math.random() * Math.PI * 2;
            const radius = Math.random() * 0.3;

            positions[i * 3] = position.x + Math.cos(angle) * radius;
            positions[i * 3 + 1] = position.y + 0.05;
            positions[i * 3 + 2] = position.z + Math.sin(angle) * radius;

            // Velocity outward and upward
            const speed = 1 + Math.random();
            velocities.push(new THREE.Vector3(
                Math.cos(angle) * speed,
                1 + Math.random() * 2,
                Math.sin(angle) * speed
            ));

            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;

            sizes[i] = terrainData.particleSize * (0.8 + Math.random() * 0.4);
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: terrainData.particleSize,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            depthWrite: false
        });

        const particles = new THREE.Points(geometry, material);
        this.scene.add(particles);

        this.activeEffects.push({
            mesh: particles,
            velocities: velocities,
            lifetime: 0.8,
            maxLifetime: 0.8,
            type: 'footstep',
            gravity: true
        });
    }

    /**
     * Emit dust cloud (running, sliding, impact)
     */
    emitDust(position, direction, intensity = 1.0) {
        const particleCount = Math.floor(30 * intensity);

        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const velocities = [];
        const colors = new Float32Array(particleCount * 3);
        const sizes = new Float32Array(particleCount);

        const color = new THREE.Color(0xccaa88);

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = position.x + (Math.random() - 0.5) * 0.5;
            positions[i * 3 + 1] = position.y + Math.random() * 0.3;
            positions[i * 3 + 2] = position.z + (Math.random() - 0.5) * 0.5;

            // Velocity in direction + randomness
            const spread = 0.5;
            velocities.push(new THREE.Vector3(
                direction.x * 3 + (Math.random() - 0.5) * spread,
                1 + Math.random() * 2,
                direction.z * 3 + (Math.random() - 0.5) * spread
            ));

            colors[i * 3] = color.r * (0.9 + Math.random() * 0.2);
            colors[i * 3 + 1] = color.g * (0.9 + Math.random() * 0.2);
            colors[i * 3 + 2] = color.b * (0.9 + Math.random() * 0.2);

            sizes[i] = 0.4 + Math.random() * 0.3;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: 0.5,
            vertexColors: true,
            transparent: true,
            opacity: 0.6,
            depthWrite: false
        });

        const particles = new THREE.Points(geometry, material);
        this.scene.add(particles);

        this.activeEffects.push({
            mesh: particles,
            velocities: velocities,
            lifetime: 1.5,
            maxLifetime: 1.5,
            type: 'dust',
            gravity: false,
            drag: 0.95
        });
    }

    /**
     * Emit debris (rocks, wood chunks, etc.)
     */
    emitDebris(position, count = 10, debrisType = 'ROCK') {
        for (let i = 0; i < count; i++) {
            const geometry = new THREE.BoxGeometry(0.15, 0.15, 0.15);
            const material = new THREE.MeshLambertMaterial({
                color: debrisType === 'ROCK' ? 0x666666 : 0x886644
            });
            const debris = new THREE.Mesh(geometry, material);

            debris.position.copy(position);
            debris.position.x += (Math.random() - 0.5) * 0.5;
            debris.position.y += Math.random() * 0.2;
            debris.position.z += (Math.random() - 0.5) * 0.5;

            this.scene.add(debris);

            const velocity = new THREE.Vector3(
                (Math.random() - 0.5) * 8,
                5 + Math.random() * 5,
                (Math.random() - 0.5) * 8
            );

            const rotationSpeed = new THREE.Vector3(
                (Math.random() - 0.5) * 10,
                (Math.random() - 0.5) * 10,
                (Math.random() - 0.5) * 10
            );

            this.activeEffects.push({
                mesh: debris,
                velocity: velocity,
                rotationSpeed: rotationSpeed,
                lifetime: 2.0,
                maxLifetime: 2.0,
                type: 'debris',
                gravity: true
            });
        }
    }

    /**
     * Emit splash effect (water, blood, liquid)
     */
    emitSplash(position, liquidColor = 0x4488ff, size = 1.0) {
        const dropletCount = Math.floor(40 * size);

        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(dropletCount * 3);
        const velocities = [];
        const colors = new Float32Array(dropletCount * 3);
        const sizes = new Float32Array(dropletCount);

        const color = new THREE.Color(liquidColor);

        for (let i = 0; i < dropletCount; i++) {
            positions[i * 3] = position.x;
            positions[i * 3 + 1] = position.y;
            positions[i * 3 + 2] = position.z;

            const angle = Math.random() * Math.PI * 2;
            const elevation = Math.random() * Math.PI / 3; // Up to 60 degrees
            const speed = 3 + Math.random() * 4;

            velocities.push(new THREE.Vector3(
                Math.cos(angle) * Math.cos(elevation) * speed,
                Math.sin(elevation) * speed,
                Math.sin(angle) * Math.cos(elevation) * speed
            ));

            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;

            sizes[i] = 0.1 + Math.random() * 0.15;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: 0.15,
            vertexColors: true,
            transparent: true,
            opacity: 0.9,
            depthWrite: false
        });

        const particles = new THREE.Points(geometry, material);
        this.scene.add(particles);

        this.activeEffects.push({
            mesh: particles,
            velocities: velocities,
            lifetime: 1.0,
            maxLifetime: 1.0,
            type: 'splash',
            gravity: true
        });
    }

    /**
     * Emit smoke/steam effect
     */
    emitSmoke(position, duration = 2.0, color = 0xaaaaaa) {
        const smokeCount = 15;

        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(smokeCount * 3);
        const velocities = [];
        const colors = new Float32Array(smokeCount * 3);
        const sizes = new Float32Array(smokeCount);

        const smokeColor = new THREE.Color(color);

        for (let i = 0; i < smokeCount; i++) {
            const offset = Math.random() * 0.3;
            positions[i * 3] = position.x + (Math.random() - 0.5) * offset;
            positions[i * 3 + 1] = position.y;
            positions[i * 3 + 2] = position.z + (Math.random() - 0.5) * offset;

            velocities.push(new THREE.Vector3(
                (Math.random() - 0.5) * 0.5,
                1 + Math.random() * 0.5,
                (Math.random() - 0.5) * 0.5
            ));

            colors[i * 3] = smokeColor.r;
            colors[i * 3 + 1] = smokeColor.g;
            colors[i * 3 + 2] = smokeColor.b;

            sizes[i] = 0.5 + Math.random() * 0.3;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: 0.8,
            vertexColors: true,
            transparent: true,
            opacity: 0.5,
            depthWrite: false
        });

        const particles = new THREE.Points(geometry, material);
        this.scene.add(particles);

        this.activeEffects.push({
            mesh: particles,
            velocities: velocities,
            lifetime: duration,
            maxLifetime: duration,
            type: 'smoke',
            gravity: false,
            expansion: 1.02
        });
    }

    /**
     * Emit leaves/petals effect
     */
    emitLeaves(position, count = 20, leafColor = 0x66aa44) {
        for (let i = 0; i < count; i++) {
            const geometry = new THREE.PlaneGeometry(0.15, 0.2);
            const material = new THREE.MeshBasicMaterial({
                color: leafColor,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.8
            });
            const leaf = new THREE.Mesh(geometry, material);

            leaf.position.copy(position);
            leaf.position.x += (Math.random() - 0.5) * 2;
            leaf.position.y += Math.random() * 3;
            leaf.position.z += (Math.random() - 0.5) * 2;

            this.scene.add(leaf);

            const velocity = new THREE.Vector3(
                (Math.random() - 0.5) * 2,
                -0.5 - Math.random(),
                (Math.random() - 0.5) * 2
            );

            const rotationSpeed = new THREE.Vector3(
                Math.random() * 5,
                Math.random() * 5,
                Math.random() * 5
            );

            this.activeEffects.push({
                mesh: leaf,
                velocity: velocity,
                rotationSpeed: rotationSpeed,
                lifetime: 3.0,
                maxLifetime: 3.0,
                type: 'leaf',
                gravity: false,
                swirl: Math.random() * Math.PI * 2
            });
        }
    }

    /**
     * Update all active effects
     */
    update(deltaTime) {
        for (let i = this.activeEffects.length - 1; i >= 0; i--) {
            const effect = this.activeEffects[i];
            effect.lifetime -= deltaTime;

            if (effect.lifetime <= 0) {
                this.removeEffect(i);
                continue;
            }

            switch (effect.type) {
                case 'footstep':
                case 'dust':
                case 'splash':
                    this.updateParticleEffect(effect, deltaTime);
                    break;
                case 'debris':
                    this.updateDebris(effect, deltaTime);
                    break;
                case 'smoke':
                    this.updateSmoke(effect, deltaTime);
                    break;
                case 'leaf':
                    this.updateLeaf(effect, deltaTime);
                    break;
            }

            // Fade out based on lifetime
            const lifetimeRatio = effect.lifetime / effect.maxLifetime;
            if (effect.mesh.material) {
                effect.mesh.material.opacity = Math.min(effect.mesh.material.opacity, lifetimeRatio);
            }
        }
    }

    /**
     * Update particle-based effects
     */
    updateParticleEffect(effect, deltaTime) {
        const positions = effect.mesh.geometry.attributes.position.array;
        const sizes = effect.mesh.geometry.attributes.size.array;

        for (let i = 0; i < effect.velocities.length; i++) {
            positions[i * 3] += effect.velocities[i].x * deltaTime;
            positions[i * 3 + 1] += effect.velocities[i].y * deltaTime;
            positions[i * 3 + 2] += effect.velocities[i].z * deltaTime;

            if (effect.gravity) {
                effect.velocities[i].y -= 9.8 * deltaTime;
            }

            if (effect.drag) {
                effect.velocities[i].multiplyScalar(effect.drag);
            }

            sizes[i] *= 0.98;
        }

        effect.mesh.geometry.attributes.position.needsUpdate = true;
        effect.mesh.geometry.attributes.size.needsUpdate = true;
    }

    /**
     * Update debris
     */
    updateDebris(effect, deltaTime) {
        effect.mesh.position.add(effect.velocity.clone().multiplyScalar(deltaTime));

        if (effect.gravity) {
            effect.velocity.y -= 9.8 * deltaTime;
        }

        effect.mesh.rotation.x += effect.rotationSpeed.x * deltaTime;
        effect.mesh.rotation.y += effect.rotationSpeed.y * deltaTime;
        effect.mesh.rotation.z += effect.rotationSpeed.z * deltaTime;

        // Bounce off ground
        if (effect.mesh.position.y < 0) {
            effect.mesh.position.y = 0;
            effect.velocity.y = -effect.velocity.y * 0.5;
            effect.velocity.x *= 0.8;
            effect.velocity.z *= 0.8;
        }
    }

    /**
     * Update smoke
     */
    updateSmoke(effect, deltaTime) {
        const positions = effect.mesh.geometry.attributes.position.array;
        const sizes = effect.mesh.geometry.attributes.size.array;

        for (let i = 0; i < effect.velocities.length; i++) {
            positions[i * 3] += effect.velocities[i].x * deltaTime;
            positions[i * 3 + 1] += effect.velocities[i].y * deltaTime;
            positions[i * 3 + 2] += effect.velocities[i].z * deltaTime;

            // Expand smoke
            if (effect.expansion) {
                sizes[i] *= effect.expansion;
            }
        }

        effect.mesh.geometry.attributes.position.needsUpdate = true;
        effect.mesh.geometry.attributes.size.needsUpdate = true;
    }

    /**
     * Update leaves with swirl
     */
    updateLeaf(effect, deltaTime) {
        effect.mesh.position.add(effect.velocity.clone().multiplyScalar(deltaTime));

        // Swirl motion
        effect.swirl += deltaTime * 2;
        effect.mesh.position.x += Math.sin(effect.swirl) * 0.02;
        effect.mesh.position.z += Math.cos(effect.swirl) * 0.02;

        effect.mesh.rotation.x += effect.rotationSpeed.x * deltaTime;
        effect.mesh.rotation.y += effect.rotationSpeed.y * deltaTime;
        effect.mesh.rotation.z += effect.rotationSpeed.z * deltaTime;
    }

    /**
     * Remove effect
     */
    removeEffect(index) {
        const effect = this.activeEffects[index];

        this.scene.remove(effect.mesh);
        if (effect.mesh.geometry) effect.mesh.geometry.dispose();
        if (effect.mesh.material) effect.mesh.material.dispose();

        this.activeEffects.splice(index, 1);
    }

    /**
     * Clear all effects
     */
    clearAll() {
        while (this.activeEffects.length > 0) {
            this.removeEffect(0);
        }
    }

    /**
     * Dispose
     */
    dispose() {
        this.clearAll();
    }
}

// Make globally available
window.EnvironmentParticleSystem = EnvironmentParticleSystem;
