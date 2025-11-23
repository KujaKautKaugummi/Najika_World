/**
 * Boss Marker System - Najika World
 * 3D markers for regional bosses in open world
 *
 * Features:
 * - Glowing sphere markers at boss locations
 * - Particle effects around markers
 * - Proximity detection for E-prompt
 * - Integration with Nemesis Arena
 * - Boss info display on hover
 *
 * NOTE: Uses THREE from global scope
 */

(function() {
    'use strict';

    if (typeof THREE === 'undefined') {
        console.error('❌ THREE.js is required for BossMarkerSystem');
        return;
    }

class BossMarkerSystem {
    constructor(scene, worldManager) {
        this.scene = scene;
        this.worldManager = worldManager;
        this.bossData = null;
        this.activeMarkers = new Map(); // boss_id => marker mesh
        this.nearbyBoss = null;
        this.proximityDistance = 5; // meters
        this.isLoaded = false;

        console.log('🏰 Boss Marker System initializing...');
    }

    /**
     * Load boss spawn data from JSON
     * @returns {Promise<void>}
     */
    async loadBossData() {
        try {
            const response = await fetch('/digivice/data/boss_spawns.json');
            if (!response.ok) {
                throw new Error(`Failed to load boss data: ${response.status}`);
            }

            this.bossData = await response.json();
            console.log(`🏰 Loaded ${this.bossData.bosses.length} boss spawns`);
            this.isLoaded = true;
        } catch (error) {
            console.error('❌ Failed to load boss spawns:', error);
            this.bossData = { bosses: [] };
        }
    }

    /**
     * Spawn all boss markers in the world
     */
    spawnMarkers() {
        if (!this.bossData || !this.isLoaded) {
            console.warn('⚠️ Boss data not loaded yet');
            return;
        }

        console.log('🏰 Spawning boss markers...');

        this.bossData.bosses.forEach(boss => {
            const markerGroup = this.createMarker(boss);
            this.scene.add(markerGroup);
            this.activeMarkers.set(boss.id, markerGroup);
        });

        console.log(`✅ Spawned ${this.activeMarkers.size} boss markers`);
    }

    /**
     * Create a single boss marker
     * @param {Object} bossData - Boss data from JSON
     * @returns {THREE.Group} Marker group (sphere + particles + label)
     */
    createMarker(bossData) {
        const group = new THREE.Group();
        group.userData.bossData = bossData;
        group.userData.interactable = true;
        group.userData.interactText = `[E] ${bossData.name} herausfordern`;
        group.userData.markerType = 'boss';

        // Position
        group.position.set(
            bossData.position.x,
            bossData.position.y + 5, // 5m above ground
            bossData.position.z
        );

        // 1. Glowing sphere
        const sphereGeometry = new THREE.SphereGeometry(2, 16, 16);
        const sphereMaterial = new THREE.MeshStandardMaterial({
            color: bossData.markerColor,
            emissive: bossData.markerColor,
            emissiveIntensity: 0.8,
            transparent: true,
            opacity: 0.9
        });
        const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
        sphere.castShadow = false;
        sphere.receiveShadow = false;
        group.add(sphere);

        // 2. Outer glow ring
        const ringGeometry = new THREE.TorusGeometry(2.5, 0.1, 8, 24);
        const ringMaterial = new THREE.MeshBasicMaterial({
            color: bossData.markerColor,
            transparent: true,
            opacity: 0.5
        });
        const ring = new THREE.Mesh(ringGeometry, ringMaterial);
        ring.rotation.x = Math.PI / 2;
        group.add(ring);

        // 3. Point light for glow effect
        const light = new THREE.PointLight(bossData.markerColor, 2, 20);
        light.position.set(0, 0, 0);
        group.add(light);

        // 4. Boss icon/skull above sphere
        const skullGeometry = new THREE.SphereGeometry(0.8, 8, 8);
        const skullMaterial = new THREE.MeshBasicMaterial({
            color: 0xff0000,
            transparent: true,
            opacity: 0.8
        });
        const skull = new THREE.Mesh(skullGeometry, skullMaterial);
        skull.position.y = 3;
        group.add(skull);

        // 5. Particle system (simple version)
        const particleCount = 20;
        const particles = [];

        for (let i = 0; i < particleCount; i++) {
            const particleGeo = new THREE.SphereGeometry(0.1, 4, 4);
            const particleMat = new THREE.MeshBasicMaterial({
                color: bossData.markerColor,
                transparent: true,
                opacity: 0.6
            });
            const particle = new THREE.Mesh(particleGeo, particleMat);

            // Random position around marker
            const angle = (Math.PI * 2 * i) / particleCount;
            const radius = 3 + Math.random();
            particle.position.x = Math.cos(angle) * radius;
            particle.position.z = Math.sin(angle) * radius;
            particle.position.y = (Math.random() - 0.5) * 4;

            // Store animation data
            particle.userData.angle = angle;
            particle.userData.radius = radius;
            particle.userData.speed = 0.5 + Math.random() * 0.5;
            particle.userData.verticalSpeed = (Math.random() - 0.5) * 2;

            particles.push(particle);
            group.add(particle);
        }

        // Store references
        group.userData.sphere = sphere;
        group.userData.ring = ring;
        group.userData.particles = particles;
        group.userData.animationTime = 0;

        return group;
    }

    /**
     * Update boss markers (called every frame)
     * @param {Vector3} playerPosition - Player position
     * @param {number} deltaTime - Time since last frame (seconds)
     */
    update(playerPosition, deltaTime) {
        if (!playerPosition || this.activeMarkers.size === 0) return;

        this.nearbyBoss = null;
        let closestDistance = Infinity;

        // Update each marker
        this.activeMarkers.forEach((marker, bossId) => {
            // Animate marker
            marker.userData.animationTime += deltaTime;
            const time = marker.userData.animationTime;

            // Bob up and down
            marker.position.y = marker.userData.bossData.position.y + 5 + Math.sin(time * 2) * 0.5;

            // Rotate ring
            if (marker.userData.ring) {
                marker.userData.ring.rotation.z += deltaTime * 0.5;
            }

            // Pulse sphere
            if (marker.userData.sphere) {
                const scale = 1 + Math.sin(time * 3) * 0.1;
                marker.userData.sphere.scale.set(scale, scale, scale);
            }

            // Animate particles
            if (marker.userData.particles) {
                marker.userData.particles.forEach((particle, i) => {
                    particle.userData.angle += particle.userData.speed * deltaTime;

                    const radius = particle.userData.radius + Math.sin(time * 2 + i) * 0.3;
                    particle.position.x = Math.cos(particle.userData.angle) * radius;
                    particle.position.z = Math.sin(particle.userData.angle) * radius;

                    particle.position.y += particle.userData.verticalSpeed * deltaTime;

                    // Wrap vertical position
                    if (particle.position.y > 4) particle.position.y = -4;
                    if (particle.position.y < -4) particle.position.y = 4;
                });
            }

            // Check proximity
            const distance = playerPosition.distanceTo(marker.position);
            if (distance < this.proximityDistance && distance < closestDistance) {
                closestDistance = distance;
                this.nearbyBoss = marker.userData.bossData;
            }
        });
    }

    /**
     * Get nearby boss (if player is close enough)
     * @param {Vector3} playerPosition - Player position
     * @returns {Object|null} Boss data or null
     */
    getNearbyBoss(playerPosition) {
        if (!playerPosition || this.activeMarkers.size === 0) return null;

        let nearestBoss = null;
        let closestDistance = Infinity;

        this.activeMarkers.forEach((marker, bossId) => {
            const distance = playerPosition.distanceTo(marker.position);
            if (distance < this.proximityDistance && distance < closestDistance) {
                closestDistance = distance;
                nearestBoss = marker.userData.bossData;
            }
        });

        return nearestBoss;
    }

    /**
     * Interact with boss (E-key pressed)
     * @param {string} bossId - Boss ID
     */
    interactWithBoss(bossId) {
        const boss = this.bossData?.bosses.find(b => b.id === bossId);
        if (!boss) {
            console.error(`❌ Boss not found: ${bossId}`);
            return;
        }

        console.log(`🏰 Starting boss fight: ${boss.name}`);

        // Show boss intro modal
        this.showBossIntro(boss);
    }

    /**
     * Show boss introduction modal
     * @param {Object} boss - Boss data
     */
    showBossIntro(boss) {
        // Remove existing modal
        const existing = document.getElementById('boss-intro-modal');
        if (existing) existing.remove();

        const modal = document.createElement('div');
        modal.id = 'boss-intro-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 20000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s;
        `;

        modal.innerHTML = `
            <div style="
                max-width: 600px;
                background: linear-gradient(135deg, #1a1a2e, #2c2c3e);
                border: 3px solid ${boss.markerColor};
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 0 50px ${boss.markerColor}80;
                color: white;
            ">
                <div style="font-size: 64px; margin-bottom: 20px;">💀</div>
                <h2 style="font-size: 36px; margin: 0 0 10px 0; color: ${boss.markerColor};">
                    ${boss.name}
                </h2>
                <div style="font-size: 18px; color: #888; margin-bottom: 30px;">
                    Level ${boss.level} Boss
                </div>

                <p style="font-size: 16px; line-height: 1.6; color: #ccc; margin-bottom: 30px;">
                    ${boss.description}
                </p>

                <div style="
                    background: rgba(0,0,0,0.5);
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                ">
                    <h3 style="margin: 0 0 15px 0; color: #f39c12;">🏆 Rewards</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left;">
                        <div>💰 Gold: ${boss.rewards.gold}</div>
                        <div>⭐ XP: ${boss.rewards.xp}</div>
                    </div>
                    ${boss.rewards.items && boss.rewards.items.length > 0 ? `
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #333;">
                            <strong>Items:</strong><br/>
                            ${boss.rewards.items.map(item => `<span style="color: #9b59b6;">⚔️ ${item}</span>`).join('<br/>')}
                        </div>
                    ` : ''}
                </div>

                <div style="display: flex; gap: 15px; justify-content: center;">
                    <button onclick="window.bossMarkerSystem.startBossFight('${boss.id}')" style="
                        background: linear-gradient(135deg, ${boss.markerColor}, ${boss.markerColor}dd);
                        border: none;
                        color: white;
                        padding: 15px 40px;
                        border-radius: 10px;
                        cursor: pointer;
                        font-size: 18px;
                        font-weight: bold;
                    ">⚔️ Fight!</button>

                    <button onclick="document.getElementById('boss-intro-modal').remove()" style="
                        background: rgba(100, 100, 100, 0.5);
                        border: 2px solid #666;
                        color: white;
                        padding: 15px 40px;
                        border-radius: 10px;
                        cursor: pointer;
                        font-size: 18px;
                        font-weight: bold;
                    ">Cancel</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Start boss fight (called from modal)
     * @param {string} bossId - Boss ID
     */
    startBossFight(bossId) {
        const boss = this.bossData?.bosses.find(b => b.id === bossId);
        if (!boss) return;

        // Close modal
        const modal = document.getElementById('boss-intro-modal');
        if (modal) modal.remove();

        console.log(`⚔️ Starting arena: ${boss.arenaType}`);

        // Trigger Region Boss UI
        if (window.regionBossUI) {
            window.regionBossUI.show();
            // TODO: Start specific boss fight based on arenaType
        } else {
            console.warn('⚠️ RegionBossUI not available');
            alert(`Boss Fight: ${boss.name}\n\n(RegionBossUI integration pending)`);
        }
    }

    /**
     * Dispose all markers
     */
    dispose() {
        this.activeMarkers.forEach((marker, bossId) => {
            // Dispose geometries and materials
            marker.traverse(child => {
                if (child.geometry) child.geometry.dispose();
                if (child.material) {
                    if (Array.isArray(child.material)) {
                        child.material.forEach(mat => mat.dispose());
                    } else {
                        child.material.dispose();
                    }
                }
            });

            this.scene.remove(marker);
        });

        this.activeMarkers.clear();
        console.log('🏰 Boss markers disposed');
    }
}

// Export to global scope
window.BossMarkerSystem = BossMarkerSystem;

console.log('🏰 BossMarkerSystem loaded successfully');

})();
