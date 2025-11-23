/**
 * World Systems Integration
 * Centralized integration point for all world systems
 *
 * This file ensures all world systems work together seamlessly:
 * - Biome System (terrain, materials, environment)
 * - Vegetation System (trees, grass, flowers)
 * - Weather System (rain, snow, fog)
 * - Day/Night Cycle (lighting, sky gradient)
 * - City Builder (buildings, roads, NPCs)
 * - LOD Manager (performance optimization)
 * - Region Streaming (chunk loading)
 */

class WorldSystemsIntegration {
    constructor(scene, camera, renderer) {
        this.scene = scene;
        this.camera = camera;
        this.renderer = renderer;

        // Initialize all world systems
        this.biomeSystem = null;
        this.vegetationSystem = null;
        this.weatherSystem = null;
        this.dayNightCycle = null;
        this.cityBuilder = null;
        this.lodManager = null;
        this.regionStreaming = null;

        // State
        this.initialized = false;
        this.currentRegion = null;
        this.activeChunks = new Set();
    }

    /**
     * Initialize all world systems
     */
    async init() {
        console.log('🌍 Initializing World Systems Integration...');

        try {
            // 1. Biome System
            this.biomeSystem = new BiomeSystem(this.scene, this.camera);
            await this.loadBiomeData();
            console.log('  ✅ Biome System initialized');

            // 2. Vegetation System
            this.vegetationSystem = new VegetationSystem(this.scene);
            this.vegetationSystem.init();
            console.log('  ✅ Vegetation System initialized');

            // 3. Weather System
            this.weatherSystem = new WeatherSystem(this.scene, this.camera);
            this.weatherSystem.init();
            console.log('  ✅ Weather System initialized');

            // 4. Day/Night Cycle
            this.dayNightCycle = new DayNightCycle(this.scene);
            this.dayNightCycle.init();
            console.log('  ✅ Day/Night Cycle initialized');

            // 5. City Builder
            this.cityBuilder = new CityBuilder(this.scene);
            this.cityBuilder.init();
            console.log('  ✅ City Builder initialized');

            // 6. LOD Manager
            this.lodManager = new LODManager(this.scene, this.camera);
            this.lodManager.init();
            console.log('  ✅ LOD Manager initialized');

            // 7. Region Streaming
            this.regionStreaming = new RegionStreaming(this.scene, this.camera);
            this.regionStreaming.init();
            console.log('  ✅ Region Streaming initialized');

            // Connect systems
            this.connectSystems();

            this.initialized = true;
            console.log('🌍 World Systems Integration complete!');

            return true;
        } catch (error) {
            console.error('❌ Failed to initialize world systems:', error);
            return false;
        }
    }

    /**
     * Connect systems to work together
     */
    connectSystems() {
        // Connect Biome System with Vegetation
        if (this.biomeSystem && this.vegetationSystem) {
            this.vegetationSystem.setBiomeSystem(this.biomeSystem);
        }

        // Connect Weather with Day/Night Cycle
        if (this.weatherSystem && this.dayNightCycle) {
            this.dayNightCycle.setWeatherSystem(this.weatherSystem);
            this.weatherSystem.setDayNightCycle(this.dayNightCycle);
        }

        // Connect LOD Manager with all renderable systems
        if (this.lodManager) {
            if (this.vegetationSystem) {
                this.lodManager.registerSystem('vegetation', this.vegetationSystem);
            }
            if (this.cityBuilder) {
                this.lodManager.registerSystem('city', this.cityBuilder);
            }
        }

        // Connect Region Streaming with all systems
        if (this.regionStreaming) {
            this.regionStreaming.onChunkLoad = (chunk) => {
                this.onChunkLoaded(chunk);
            };
            this.regionStreaming.onChunkUnload = (chunk) => {
                this.onChunkUnloaded(chunk);
            };
        }
    }

    /**
     * Load biome data from JSON
     */
    async loadBiomeData() {
        try {
            const response = await fetch('/biomes.json');
            const biomeData = await response.json();
            this.biomeSystem.loadBiomes(biomeData);
        } catch (error) {
            console.warn('⚠️ Could not load biomes.json, using defaults');
            this.biomeSystem.loadDefaultBiomes();
        }
    }

    /**
     * Enter a specific region/biome
     */
    enterRegion(regionId, biomeId) {
        console.log(`🌍 Entering region: ${regionId} (biome: ${biomeId})`);

        this.currentRegion = regionId;

        // Apply biome environment
        if (this.biomeSystem) {
            this.biomeSystem.applyBiomeEnvironment(biomeId);
        }

        // Update vegetation for this biome
        if (this.vegetationSystem) {
            this.vegetationSystem.setBiome(biomeId);
        }

        // Update weather for this biome
        if (this.weatherSystem) {
            const weatherTypes = this.biomeSystem.biomes.get(biomeId)?.weather || ['clear'];
            this.weatherSystem.setWeatherOptions(weatherTypes);
        }

        // Start streaming this region
        if (this.regionStreaming) {
            this.regionStreaming.setActiveRegion(regionId);
        }

        // Generate city if applicable
        if (this.cityBuilder && ['city', 'village'].includes(biomeId)) {
            this.cityBuilder.generateCity(regionId, biomeId);
        }
    }

    /**
     * Handle chunk loaded
     */
    onChunkLoaded(chunk) {
        this.activeChunks.add(chunk.id);

        // Generate vegetation for this chunk
        if (this.vegetationSystem && chunk.biome) {
            this.vegetationSystem.generateForChunk(chunk);
        }

        // Register with LOD manager
        if (this.lodManager) {
            this.lodManager.registerChunk(chunk);
        }

        console.log(`📦 Chunk loaded: ${chunk.id} (total active: ${this.activeChunks.size})`);
    }

    /**
     * Handle chunk unloaded
     */
    onChunkUnloaded(chunk) {
        this.activeChunks.delete(chunk.id);

        // Clean up vegetation
        if (this.vegetationSystem) {
            this.vegetationSystem.cleanupChunk(chunk);
        }

        // Unregister from LOD manager
        if (this.lodManager) {
            this.lodManager.unregisterChunk(chunk);
        }

        console.log(`🗑️ Chunk unloaded: ${chunk.id} (remaining: ${this.activeChunks.size})`);
    }

    /**
     * Update all systems (call every frame)
     */
    update(deltaTime) {
        if (!this.initialized) return;

        // Update Day/Night Cycle
        if (this.dayNightCycle) {
            this.dayNightCycle.update(deltaTime);
        }

        // Update Weather
        if (this.weatherSystem) {
            this.weatherSystem.update(deltaTime);
        }

        // Update LOD based on camera position
        if (this.lodManager) {
            this.lodManager.update(this.camera.position);
        }

        // Update Region Streaming
        if (this.regionStreaming) {
            this.regionStreaming.update(this.camera.position);
        }

        // Update Vegetation (wind animation, etc.)
        if (this.vegetationSystem) {
            this.vegetationSystem.update(deltaTime);
        }
    }

    /**
     * Change time of day
     */
    setTimeOfDay(hour) {
        if (this.dayNightCycle) {
            this.dayNightCycle.setTime(hour);
        }
    }

    /**
     * Change weather
     */
    setWeather(weatherType, intensity = 1.0) {
        if (this.weatherSystem) {
            this.weatherSystem.setWeather(weatherType, intensity);
        }
    }

    /**
     * Enable/disable a system
     */
    toggleSystem(systemName, enabled) {
        switch(systemName) {
            case 'weather':
                if (this.weatherSystem) {
                    this.weatherSystem.enabled = enabled;
                }
                break;
            case 'daynight':
                if (this.dayNightCycle) {
                    this.dayNightCycle.enabled = enabled;
                }
                break;
            case 'lod':
                if (this.lodManager) {
                    this.lodManager.enabled = enabled;
                }
                break;
            case 'streaming':
                if (this.regionStreaming) {
                    this.regionStreaming.enabled = enabled;
                }
                break;
        }
    }

    /**
     * Get system stats
     */
    getStats() {
        return {
            activeChunks: this.activeChunks.size,
            vegetation: this.vegetationSystem?.getStats() || {},
            weather: this.weatherSystem?.getCurrentWeather() || 'none',
            timeOfDay: this.dayNightCycle?.getCurrentTime() || 0,
            lodLevels: this.lodManager?.getStats() || {},
            streamingDistance: this.regionStreaming?.streamingDistance || 0
        };
    }

    /**
     * Cleanup
     */
    dispose() {
        console.log('🌍 Cleaning up World Systems...');

        if (this.vegetationSystem) {
            this.vegetationSystem.dispose();
        }

        if (this.weatherSystem) {
            this.weatherSystem.dispose();
        }

        if (this.cityBuilder) {
            this.cityBuilder.dispose();
        }

        if (this.regionStreaming) {
            this.regionStreaming.dispose();
        }

        this.activeChunks.clear();
        this.initialized = false;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorldSystemsIntegration;
}
