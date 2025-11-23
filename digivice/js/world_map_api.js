/**
 * World Map API Integration
 * Backend-Verbindung für Kartendaten und Player Tracking
 *
 * Features:
 * - Load World Data (Regions, Biomes, Cities)
 * - Player Position Tracking
 * - Travel Points Management
 * - Fast Travel API
 * - Exploration Progress
 * - Region Discovery
 */

class WorldMapAPI {
    constructor() {
        this.apiBase = '/api/world-map';
        this.playerId = null;

        // Cache
        this.cache = {
            regions: null,
            biomes: null,
            cities: null,
            travelPoints: null,
            playerPosition: null,
            exploredRegions: new Set()
        };

        // Update intervals
        this.positionUpdateInterval = 5000; // Update position every 5 seconds
        this.positionUpdateTimer = null;

        this.init();
    }

    async init() {
        console.log('🔌 Initializing World Map API...');

        // Get player ID from session
        this.playerId = await this.getPlayerId();

        // Load static world data
        await this.loadWorldData();

        // Load player-specific data
        await this.loadPlayerData();

        // Start position tracking
        this.startPositionTracking();

        console.log('✅ World Map API initialized!');
    }

    async getPlayerId() {
        try {
            // Try to get player ID from session/local storage
            const storedId = localStorage.getItem('najika_player_id');
            if (storedId) return parseInt(storedId);

            // Otherwise fetch from API
            const response = await fetch('http://localhost:8000/api/player/session');
            const data = await response.json();
            if (data.player_id) {
                localStorage.setItem('najika_player_id', data.player_id);
                return data.player_id;
            }

            // Default to player 1 for testing
            return 1;
        } catch (error) {
            console.warn('⚠️ Could not get player ID, using default:', error);
            return 1;
        }
    }

    async loadWorldData() {
        try {
            // Load regions from local JSON
            const regionsResponse = await fetch('/data/regions.json');
            this.cache.regions = await regionsResponse.json();

            // Load biomes from local JSON
            const biomesResponse = await fetch('/data/biomes.json');
            this.cache.biomes = await biomesResponse.json();

            // Load cities from local JSON
            const citiesResponse = await fetch('/data/cities.json');
            this.cache.cities = await citiesResponse.json();

            console.log('✅ World data loaded from JSON files');
        } catch (error) {
            console.error('❌ Failed to load world data:', error);
        }
    }

    async loadPlayerData() {
        try {
            // Load player position
            await this.updatePlayerPosition();

            // Load travel points
            await this.loadTravelPoints();

            // Load explored regions
            await this.loadExploredRegions();

            console.log('✅ Player data loaded');
        } catch (error) {
            console.error('❌ Failed to load player data:', error);
        }
    }

    async updatePlayerPosition() {
        try {
            // Try to get from API
            const response = await fetch(`${this.apiBase}/position/${this.playerId}`);

            if (response.ok) {
                const data = await response.json();
                this.cache.playerPosition = {
                    x: data.world_x,
                    z: data.world_z,
                    y: data.world_y,
                    rotation: data.rotation || 0,
                    region: data.region_name
                };
            } else {
                // Fallback to default position
                this.cache.playerPosition = {
                    x: 4800,
                    z: 4800,
                    y: 0,
                    rotation: 0,
                    region: 'goetterfels'
                };
            }

            // Notify listeners
            this.notifyPositionUpdate();

            return this.cache.playerPosition;
        } catch (error) {
            console.warn('⚠️ Could not fetch player position, using default:', error);

            // Use default position
            this.cache.playerPosition = {
                x: 4800,
                z: 4800,
                y: 0,
                rotation: 0,
                region: 'goetterfels'
            };

            return this.cache.playerPosition;
        }
    }

    async loadTravelPoints() {
        try {
            const response = await fetch(`${this.apiBase}/travel-points?player_id=${this.playerId}`);

            if (response.ok) {
                const data = await response.json();
                this.cache.travelPoints = data.travel_points || [];
            } else {
                // Create default travel points from cities
                this.cache.travelPoints = this.createDefaultTravelPoints();
            }

            return this.cache.travelPoints;
        } catch (error) {
            console.warn('⚠️ Could not fetch travel points, using defaults:', error);
            this.cache.travelPoints = this.createDefaultTravelPoints();
            return this.cache.travelPoints;
        }
    }

    createDefaultTravelPoints() {
        // Create travel points from cities
        if (!this.cache.cities || !this.cache.cities.cities) return [];

        return this.cache.cities.cities.map((city, index) => ({
            id: index + 1,
            name: city.name,
            type: 'city',
            icon: '🏛️',
            position: city.position,
            region: city.region,
            is_locked: false, // All cities unlocked by default for testing
            unlock_requirement: null
        }));
    }

    async loadExploredRegions() {
        try {
            const response = await fetch(`${this.apiBase}/explored-regions?player_id=${this.playerId}`);

            if (response.ok) {
                const data = await response.json();
                this.cache.exploredRegions = new Set(data.explored_regions || []);
            } else {
                // Default: only starting region explored
                this.cache.exploredRegions = new Set(['goetterfels']);
            }

            return Array.from(this.cache.exploredRegions);
        } catch (error) {
            console.warn('⚠️ Could not fetch explored regions, using defaults:', error);
            this.cache.exploredRegions = new Set(['goetterfels']);
            return Array.from(this.cache.exploredRegions);
        }
    }

    async savePlayerPosition(x, z, y, rotation) {
        try {
            const response = await fetch(`${this.apiBase}/position`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    world_x: x,
                    world_z: z,
                    world_y: y,
                    rotation: rotation
                })
            });

            if (response.ok) {
                this.cache.playerPosition = { x, z, y, rotation };
                this.notifyPositionUpdate();
                return true;
            }

            return false;
        } catch (error) {
            console.warn('⚠️ Could not save player position:', error);
            return false;
        }
    }

    async discoverRegion(regionId) {
        if (this.cache.exploredRegions.has(regionId)) {
            return true; // Already discovered
        }

        try {
            const response = await fetch(`${this.apiBase}/discover-region`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    region_id: regionId
                })
            });

            if (response.ok) {
                this.cache.exploredRegions.add(regionId);
                this.notifyRegionDiscovered(regionId);
                console.log(`🗺️ Region discovered: ${regionId}`);
                return true;
            }

            return false;
        } catch (error) {
            console.warn('⚠️ Could not save region discovery:', error);
            // Still add to local cache
            this.cache.exploredRegions.add(regionId);
            this.notifyRegionDiscovered(regionId);
            return true;
        }
    }

    async fastTravel(travelPointId) {
        try {
            const response = await fetch(`${this.apiBase}/travel`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    travel_point_id: travelPointId
                })
            });

            if (response.ok) {
                const data = await response.json();

                // Update player position
                if (data.new_position) {
                    this.cache.playerPosition = {
                        x: data.new_position.x,
                        z: data.new_position.z,
                        y: data.new_position.y || 0,
                        rotation: data.new_position.rotation || 0,
                        region: data.region_id
                    };
                    this.notifyPositionUpdate();
                }

                return data;
            }

            return null;
        } catch (error) {
            console.error('❌ Fast travel failed:', error);
            return null;
        }
    }

    startPositionTracking() {
        // Periodically update player position from game state
        this.positionUpdateTimer = setInterval(() => {
            this.updatePlayerPositionFromGame();
        }, this.positionUpdateInterval);
    }

    stopPositionTracking() {
        if (this.positionUpdateTimer) {
            clearInterval(this.positionUpdateTimer);
            this.positionUpdateTimer = null;
        }
    }

    updatePlayerPositionFromGame() {
        // Get position from game's 3D scene
        if (window.scene3D && window.scene3D.characterGroup) {
            const pos = window.scene3D.characterGroup.position;
            const rotation = window.scene3D.characterHeading || 0;

            // Convert 3D scene coordinates to world coordinates
            const worldX = pos.x * 10; // Scale factor
            const worldZ = pos.z * 10;

            // Check if position changed significantly
            if (this.cache.playerPosition) {
                const dx = Math.abs(worldX - this.cache.playerPosition.x);
                const dz = Math.abs(worldZ - this.cache.playerPosition.z);

                if (dx > 10 || dz > 10) {
                    // Position changed, save it
                    this.savePlayerPosition(worldX, worldZ, pos.y * 10, rotation);

                    // Check for region discovery
                    const region = this.getRegionAt(worldX, worldZ);
                    if (region && !this.cache.exploredRegions.has(region.id)) {
                        this.discoverRegion(region.id);
                    }
                }
            }
        }
    }

    getRegionAt(x, z) {
        if (!this.cache.regions) return null;

        for (const region of Object.values(this.cache.regions.regions)) {
            const bounds = region.bounds;
            if (x >= bounds.minX && x <= bounds.maxX &&
                z >= bounds.minZ && z <= bounds.maxZ) {
                return region;
            }
        }

        return null;
    }

    // Event listeners
    positionListeners = [];
    regionDiscoveredListeners = [];

    onPositionUpdate(callback) {
        this.positionListeners.push(callback);
    }

    onRegionDiscovered(callback) {
        this.regionDiscoveredListeners.push(callback);
    }

    notifyPositionUpdate() {
        this.positionListeners.forEach(callback => {
            callback(this.cache.playerPosition);
        });
    }

    notifyRegionDiscovered(regionId) {
        this.regionDiscoveredListeners.forEach(callback => {
            callback(regionId);
        });
    }

    // Public getters
    getRegions() {
        return this.cache.regions;
    }

    getBiomes() {
        return this.cache.biomes;
    }

    getCities() {
        return this.cache.cities;
    }

    getTravelPoints() {
        return this.cache.travelPoints;
    }

    getPlayerPosition() {
        return this.cache.playerPosition;
    }

    getExploredRegions() {
        return Array.from(this.cache.exploredRegions);
    }

    isRegionExplored(regionId) {
        return this.cache.exploredRegions.has(regionId);
    }

    // Cleanup
    dispose() {
        this.stopPositionTracking();
        this.positionListeners = [];
        this.regionDiscoveredListeners = [];
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    window.worldMapAPI = new WorldMapAPI();
    console.log('✅ World Map API ready!');
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorldMapAPI;
} else {
    window.WorldMapAPI = WorldMapAPI;
}
