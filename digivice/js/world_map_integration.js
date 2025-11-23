/**
 * World Map System Integration
 * Verbindet alle Map-Komponenten und integriert sie ins Hauptspiel
 *
 * Components:
 * - WorldMapAPI (Backend Integration)
 * - WorldMap3DRenderer (3D Visualization)
 * - WorldMapFullUI (Full Screen Map)
 * - Minimap (Corner Map)
 */

class WorldMapIntegration {
    constructor() {
        this.api = null;
        this.fullUI = null;
        this.minimap = null;

        // Configuration
        this.config = {
            minimapEnabled: true,
            minimapPosition: 'top-right',
            minimapSize: 200,
            minimapZoom: 20,
            autoDiscoverRegions: true,
            autoSavePosition: true
        };

        // State
        this.initialized = false;
        this.currentRegion = null;

        this.init();
    }

    async init() {
        console.log('🗺️ Initializing World Map Integration...');

        // Wait for dependencies
        await this.waitForDependencies();

        // Initialize API
        this.api = window.worldMapAPI || new WorldMapAPI();

        // Initialize Full UI
        this.fullUI = window.worldMapFullUI || new WorldMapFullUI();

        // Initialize Minimap
        if (this.config.minimapEnabled) {
            this.minimap = new Minimap({
                position: this.config.minimapPosition,
                size: this.config.minimapSize,
                zoom: this.config.minimapZoom
            });
        }

        // Connect components
        this.connectComponents();

        // Setup game integration
        this.setupGameIntegration();

        this.initialized = true;
        console.log('✅ World Map Integration complete!');

        // Show welcome message
        this.showWelcomeMessage();
    }

    async waitForDependencies() {
        // Wait for THREE.js to load
        let attempts = 0;
        while (typeof THREE === 'undefined' && attempts < 50) {
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }

        if (typeof THREE === 'undefined') {
            console.warn('⚠️ THREE.js not loaded, 3D features may not work');
        }

        // Wait for WorldMapAPI
        attempts = 0;
        while (!window.WorldMapAPI && attempts < 50) {
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
    }

    connectComponents() {
        // Connect API to UI components
        if (this.api) {
            // Listen to position updates
            this.api.onPositionUpdate((position) => {
                if (this.fullUI) {
                    this.fullUI.updatePlayerPosition(position.x, position.z, position.rotation);
                }

                if (this.minimap) {
                    this.minimap.updatePlayerPosition(position.x, position.z, position.rotation);
                }

                // Update current region
                const region = this.api.getRegionAt(position.x, position.z);
                if (region && (!this.currentRegion || this.currentRegion.id !== region.id)) {
                    this.onRegionChanged(region);
                }
            });

            // Listen to region discoveries
            this.api.onRegionDiscovered((regionId) => {
                this.onRegionDiscovered(regionId);
            });
        }
    }

    setupGameIntegration() {
        // Integrate with 3D scene if available
        if (window.scene3D) {
            // Hook into character movement
            this.hookCharacterMovement();
        }

        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();

        // Setup periodic updates
        this.startPeriodicUpdates();
    }

    hookCharacterMovement() {
        // Store original animation function
        const originalAnimate = window.scene3D.animate;

        if (originalAnimate) {
            window.scene3D.animate = () => {
                // Call original
                originalAnimate.call(window.scene3D);

                // Update map systems
                this.updateFromGame();
            };
        }
    }

    updateFromGame() {
        if (!window.scene3D || !window.scene3D.characterGroup) return;

        // Get character position
        const pos = window.scene3D.characterGroup.position;
        const heading = window.scene3D.characterHeading || 0;

        // Convert to world coordinates (assuming scale factor of 10)
        const worldX = pos.x * 10 + 4800; // Offset to center
        const worldZ = pos.z * 10 + 4800;
        const worldY = pos.y * 10;

        // Update minimap
        if (this.minimap) {
            this.minimap.updatePlayerPosition(worldX, worldZ, heading);

            // Update nearby enemies
            if (window.scene3D.enemies) {
                const nearbyEnemies = window.scene3D.enemies
                    .filter(e => e.position)
                    .map(e => ({
                        x: e.position.x * 10 + 4800,
                        z: e.position.z * 10 + 4800
                    }));

                this.minimap.updateNearbyEnemies(nearbyEnemies);
            }

            // Update POIs (quests, NPCs, etc.)
            this.updateMinimapPOI();
        }

        // Auto-save position
        if (this.config.autoSavePosition) {
            this.throttledSavePosition(worldX, worldZ, worldY, heading);
        }

        // Auto-discover regions
        if (this.config.autoDiscoverRegions && this.api) {
            const region = this.api.getRegionAt(worldX, worldZ);
            if (region && !this.api.isRegionExplored(region.id)) {
                this.api.discoverRegion(region.id);
            }
        }
    }

    // Throttle position saving (max once per 5 seconds)
    lastSaveTime = 0;
    throttledSavePosition(x, z, y, rotation) {
        const now = Date.now();
        if (now - this.lastSaveTime > 5000) {
            this.lastSaveTime = now;
            if (this.api) {
                this.api.savePlayerPosition(x, z, y, rotation);
            }
        }
    }

    updateMinimapPOI() {
        if (!this.minimap) return;

        // Clear existing POI
        this.minimap.clearPOI();

        // Add quest markers
        if (window.questSystem && window.questSystem.activeQuests) {
            window.questSystem.activeQuests.forEach(quest => {
                if (quest.targetPosition) {
                    this.minimap.addPOI({
                        x: quest.targetPosition.x,
                        z: quest.targetPosition.z,
                        icon: '!',
                        color: '#ffff00',
                        name: quest.name
                    });
                }
            });
        }

        // Add NPC markers
        if (window.npcSystem && window.npcSystem.activeNPCs) {
            window.npcSystem.activeNPCs.forEach(npc => {
                if (npc.position) {
                    this.minimap.addPOI({
                        x: npc.position.x,
                        z: npc.position.z,
                        icon: '👤',
                        color: '#00ff00',
                        name: npc.name
                    });
                }
            });
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // 'M' key for full map (handled by WorldMapFullUI)
            // 'N' key to toggle minimap
            if (e.key === 'n' || e.key === 'N') {
                if (this.minimap) {
                    this.minimap.toggle();
                }
            }

            // 'P' key to focus on player
            if (e.key === 'p' || e.key === 'P') {
                if (this.fullUI && this.fullUI.isOpen && this.fullUI.renderer3D) {
                    this.fullUI.renderer3D.focusOnPlayer();
                }
            }
        });
    }

    startPeriodicUpdates() {
        // Update minimap every 100ms
        setInterval(() => {
            this.updateFromGame();
        }, 100);
    }

    onRegionChanged(region) {
        console.log(`🏞️ Entered region: ${region.name}`);

        this.currentRegion = region;

        // Show notification
        this.showRegionNotification(region);

        // Trigger events
        const event = new CustomEvent('regionChanged', { detail: region });
        window.dispatchEvent(event);
    }

    onRegionDiscovered(regionId) {
        const region = this.api.getRegions()?.regions[regionId];
        if (!region) return;

        console.log(`🗺️ Region discovered: ${region.name}`);

        // Show discovery notification
        this.showDiscoveryNotification(region);

        // Update fog of war in 3D renderer
        if (this.fullUI && this.fullUI.renderer3D) {
            this.fullUI.renderer3D.addExploredRegion(regionId);
        }

        // Trigger events
        const event = new CustomEvent('regionDiscovered', { detail: region });
        window.dispatchEvent(event);
    }

    showRegionNotification(region) {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 52, 96, 0.95);
            border: 2px solid #e94560;
            border-radius: 10px;
            padding: 15px 25px;
            color: #e8e8e8;
            font-size: 18px;
            font-weight: bold;
            z-index: 9998;
            animation: slideDown 0.5s ease-out;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        `;

        notification.innerHTML = `
            🏞️ ${region.name}
            <div style="font-size: 12px; font-weight: normal; margin-top: 5px;">
                ${this.getBiomeIcon(region.biome)} ${this.getBiomeName(region.biome)} Biome
            </div>
        `;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideUp 0.5s ease-in';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    showDiscoveryNotification(region) {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 140px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(233, 69, 96, 0.95);
            border: 2px solid #ffd700;
            border-radius: 10px;
            padding: 15px 25px;
            color: white;
            font-size: 16px;
            font-weight: bold;
            z-index: 9998;
            animation: slideDown 0.5s ease-out;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.5);
        `;

        notification.innerHTML = `
            ⭐ NEW REGION DISCOVERED!
            <div style="font-size: 14px; margin-top: 5px;">
                ${region.name}
            </div>
        `;

        document.body.appendChild(notification);

        // Remove after 4 seconds
        setTimeout(() => {
            notification.style.animation = 'slideUp 0.5s ease-in';
            setTimeout(() => notification.remove(), 500);
        }, 4000);
    }

    showWelcomeMessage() {
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(15, 52, 96, 0.95);
            border: 2px solid #e94560;
            border-radius: 10px;
            padding: 15px 20px;
            color: #e8e8e8;
            font-size: 14px;
            z-index: 9998;
            max-width: 300px;
            animation: slideInRight 0.5s ease-out;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        `;

        message.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 10px; color: #e94560;">
                🗺️ World Map System Ready!
            </div>
            <div style="font-size: 12px; line-height: 1.4;">
                <strong>Controls:</strong><br>
                • Press <strong>M</strong> for full map<br>
                • Press <strong>N</strong> to toggle minimap<br>
                • Press <strong>P</strong> to focus on player
            </div>
        `;

        document.body.appendChild(message);

        // Remove after 8 seconds
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => message.remove(), 500);
        }, 8000);

        // Add CSS animations if not already present
        if (!document.getElementById('map-animations')) {
            const style = document.createElement('style');
            style.id = 'map-animations';
            style.textContent = `
                @keyframes slideDown {
                    from { transform: translate(-50%, -100%); opacity: 0; }
                    to { transform: translate(-50%, 0); opacity: 1; }
                }
                @keyframes slideUp {
                    from { transform: translate(-50%, 0); opacity: 1; }
                    to { transform: translate(-50%, -100%); opacity: 0; }
                }
                @keyframes slideInRight {
                    from { transform: translateX(400px); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(400px); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    getBiomeIcon(biome) {
        const icons = {
            desert: '🏜️',
            forest: '🌲',
            ice: '❄️',
            volcano: '🌋',
            coast: '🌊',
            highland: '⚡',
            swamp: '🌑',
            mountain: '🗻',
            caves: '🕳️'
        };
        return icons[biome] || '🏞️';
    }

    getBiomeName(biome) {
        const names = {
            desert: 'Desert',
            forest: 'Forest',
            ice: 'Ice',
            volcano: 'Volcanic',
            coast: 'Coastal',
            highland: 'Highland',
            swamp: 'Swamp',
            mountain: 'Mountain',
            caves: 'Caves'
        };
        return names[biome] || biome;
    }

    // Public API
    openFullMap() {
        if (this.fullUI) {
            this.fullUI.open();
        }
    }

    closeFullMap() {
        if (this.fullUI) {
            this.fullUI.close();
        }
    }

    toggleMinimap() {
        if (this.minimap) {
            this.minimap.toggle();
        }
    }

    focusOnPlayer() {
        if (this.fullUI && this.fullUI.renderer3D) {
            this.fullUI.renderer3D.focusOnPlayer();
        }
    }

    focusOnRegion(regionId) {
        if (this.fullUI) {
            this.fullUI.focusOnRegion(regionId);
        }
    }

    getCurrentRegion() {
        return this.currentRegion;
    }

    getExploredRegions() {
        return this.api ? this.api.getExploredRegions() : [];
    }

    dispose() {
        if (this.api) {
            this.api.dispose();
        }

        if (this.fullUI) {
            this.fullUI.dispose();
        }

        if (this.minimap) {
            this.minimap.dispose();
        }
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    window.worldMapIntegration = new WorldMapIntegration();
    console.log('✅ World Map Integration ready!');
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorldMapIntegration;
} else {
    window.WorldMapIntegration = WorldMapIntegration;
}
