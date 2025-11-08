// 🌍 WORLD MANAGER - Hauptorchestrator für das 8-Regionen-System
// Koordiniert TerrainGenerator, BiomeSystem, VegetationSystem, CityBuilder, RegionStreaming, LODManager

import * as THREE from 'three';
import TerrainGenerator from './terrain_generator.js';
import BiomeSystem from './biome_system.js';
import VegetationSystem from './vegetation_system.js';
import CityBuilder from './city_builder.js';
import RegionStreaming from './region_streaming.js';
import LODManager from './lod_manager.js';
import AssetLoader from './asset_loader.js';
import AssetDiscovery from './asset_discovery.js';

class WorldManager {
  constructor(scene, camera) {
    this.scene = scene;
    this.camera = camera;

    // World configuration
    this.config = {
      worldSize: 9600,
      center: { x: 4800, z: 4800 },
      dataPath: '/entwicklung/data/'
    };

    // Initialize subsystems
    this.assetLoader = new AssetLoader();
    this.assetDiscovery = new AssetDiscovery();
    this.terrainGenerator = new TerrainGenerator();
    this.biomeSystem = new BiomeSystem(scene, camera);
    this.vegetationSystem = new VegetationSystem(scene, this.terrainGenerator);
    this.cityBuilder = new CityBuilder(scene, this.terrainGenerator);
    this.regionStreaming = new RegionStreaming(
      scene,
      this.terrainGenerator,
      this.biomeSystem,
      this.vegetationSystem,
      this.cityBuilder
    );
    this.lodManager = new LODManager(scene, camera);

    // Inject assetLoader into subsystems
    this.vegetationSystem.assetLoader = this.assetLoader;
    this.cityBuilder.assetLoader = this.assetLoader;

    // State
    this.initialized = false;
    this.playerPosition = new THREE.Vector3(4800, 0, 4800);  // Start at Götterfels

    // Performance settings
    this.enableLOD = true;
    this.enableStreaming = true;
    this.enableVegetationBatching = true;

    console.log('🌍 World Manager initialized');
  }

  /**
   * Initialize the world system
   * @param {Object} options - Initialization options
   */
  async initialize(options = {}) {
    console.log('🌍 Initializing Najika World (8 Regions)...');
    console.log(`   World Size: ${this.config.worldSize}x${this.config.worldSize}`);
    console.log(`   Center: (${this.config.center.x}, ${this.config.center.z})`);

    // Override config with options
    if (options.dataPath) this.config.dataPath = options.dataPath;
    if (options.enableLOD !== undefined) this.enableLOD = options.enableLOD;
    if (options.enableStreaming !== undefined) this.enableStreaming = options.enableStreaming;

    try {
      // Discover available assets
      console.log('🔍 Discovering assets...');
      await this.assetDiscovery.discover();
      await this.assetDiscovery.loadAssetMapping(`${this.config.dataPath}asset_mapping_v2_REAL.json`);
      this.assetDiscovery.logDiscovered();

      // Load world data
      const success = await this.regionStreaming.loadData(
        `${this.config.dataPath}regions.json`,
        `${this.config.dataPath}biomes.json`,
        `${this.config.dataPath}cities.json`
      );

      if (!success) {
        throw new Error('Failed to load world data');
      }

      // Setup lighting
      this.setupBaseLighting();

      // Load starting regions (around Götterfels)
      if (this.enableStreaming) {
        console.log('🌍 Loading starting regions (streaming enabled)...');
        this.regionStreaming.update(this.playerPosition);
      } else {
        console.log('🌍 Loading ALL regions (streaming disabled)...');
        this.regionStreaming.loadAllRegions();
      }

      // Apply LOD optimizations
      if (this.enableLOD) {
        console.log('🎯 Applying LOD optimizations...');
        this.lodManager.enableFrustumCulling(true);
        this.lodManager.setUpdateInterval(100);  // Update every 100ms
      }

      // Apply vegetation batching
      if (this.enableVegetationBatching) {
        console.log('🌿 Batching vegetation (instanced meshes)...');
        // TODO: Batch vegetation after generation
      }

      this.initialized = true;
      console.log('✅ Najika World initialized successfully!');

      // Log stats
      this.logStats();

      return true;
    } catch (error) {
      console.error('❌ Failed to initialize world:', error);
      return false;
    }
  }

  /**
   * Setup base lighting (sun, ambient)
   */
  setupBaseLighting() {
    console.log('☀️ Setting up base lighting...');

    // Remove old lights
    const lightsToRemove = [];
    this.scene.traverse(obj => {
      if (obj.isLight && obj.name !== 'biome_ambient') {
        lightsToRemove.push(obj);
      }
    });
    lightsToRemove.forEach(light => this.scene.remove(light));

    // Directional Light (Sun)
    const sun = new THREE.DirectionalLight(0xffffff, 1.5);
    sun.position.set(100, 200, 100);
    sun.castShadow = true;
    sun.shadow.mapSize.width = 2048;
    sun.shadow.mapSize.height = 2048;
    sun.shadow.camera.near = 0.5;
    sun.shadow.camera.far = 1000;
    sun.shadow.camera.left = -500;
    sun.shadow.camera.right = 500;
    sun.shadow.camera.top = 500;
    sun.shadow.camera.bottom = -500;
    sun.name = 'sun';
    this.scene.add(sun);

    // Ambient Light (will be modified by biome system)
    const ambient = new THREE.AmbientLight(0xffffff, 0.4);
    ambient.name = 'base_ambient';
    this.scene.add(ambient);

    // Hemisphere Light (sky/ground)
    const hemisphere = new THREE.HemisphereLight(0x87ceeb, 0x8b7355, 0.6);
    hemisphere.name = 'hemisphere';
    this.scene.add(hemisphere);

    console.log('  ✅ Base lighting setup complete');
  }

  /**
   * Update world (call every frame)
   * @param {number} deltaTime - Time since last frame
   */
  update(deltaTime) {
    if (!this.initialized) return;

    // Update region streaming
    if (this.enableStreaming) {
      this.regionStreaming.update(this.playerPosition);
    }

    // Update LOD
    if (this.enableLOD) {
      this.lodManager.update();
    }

    // Update vegetation system
    this.vegetationSystem.update(this.camera.position);
  }

  /**
   * Set player position (for streaming)
   * @param {THREE.Vector3} position
   */
  setPlayerPosition(position) {
    this.playerPosition.copy(position);

    // Update streaming immediately on large position changes
    const distance = this.playerPosition.distanceTo(this.camera.position);
    if (distance > 100) {
      this.regionStreaming.update(this.playerPosition);
    }
  }

  /**
   * Get current region player is in
   * @returns {Object|null} Region data
   */
  getCurrentRegion() {
    return this.regionStreaming.getCurrentRegion(this.playerPosition);
  }

  /**
   * Get nearby regions
   * @param {number} radius - Search radius in world units
   * @returns {Array<Object>} Nearby regions
   */
  getNearbyRegions(radius = 5000) {
    return this.regionStreaming.getRegionsNearPosition(this.playerPosition, radius);
  }

  /**
   * Teleport player to position (with immediate region loading)
   * @param {THREE.Vector3} position
   */
  teleportTo(position) {
    console.log(`🌍 Teleporting to (${position.x.toFixed(0)}, ${position.z.toFixed(0)})...`);

    this.playerPosition.copy(position);
    this.camera.position.set(position.x, position.y + 50, position.z + 50);
    this.camera.lookAt(position);

    // Force immediate region streaming update
    this.regionStreaming.update(this.playerPosition);

    const currentRegion = this.getCurrentRegion();
    if (currentRegion) {
      console.log(`  📍 Now in: ${currentRegion.name}`);
    }
  }

  /**
   * Teleport to city by name
   * @param {string} cityName
   */
  teleportToCity(cityName) {
    const cityData = this.regionStreaming.cityData.cities.find(
      city => city.name.toLowerCase() === cityName.toLowerCase()
    );

    if (cityData) {
      const position = new THREE.Vector3(cityData.position.x, 0, cityData.position.z);
      this.teleportTo(position);
      console.log(`  🏘️ Arrived at: ${cityData.name}`);
    } else {
      console.warn(`❌ City not found: ${cityName}`);
    }
  }

  /**
   * Teleport to region by name
   * @param {string} regionName
   */
  teleportToRegion(regionName) {
    const region = Object.values(this.regionStreaming.regionData.regions).find(
      r => r.name.toLowerCase() === regionName.toLowerCase() || r.id.toLowerCase() === regionName.toLowerCase()
    );

    if (region) {
      const position = new THREE.Vector3(region.position.x, 0, region.position.z);
      this.teleportTo(position);
      console.log(`  🗺️ Arrived at: ${region.name}`);
    } else {
      console.warn(`❌ Region not found: ${regionName}`);
    }
  }

  /**
   * Get height at position (terrain height)
   * @param {number} x
   * @param {number} z
   * @returns {number} Height
   */
  getHeightAt(x, z) {
    return this.terrainGenerator.getHeightAt(x, z);
  }

  /**
   * Get vegetation near position
   * @param {THREE.Vector3} position
   * @param {number} radius
   * @returns {Array<THREE.Object3D>} Nearby vegetation
   */
  getVegetationNear(position, radius = 5) {
    return this.vegetationSystem.getVegetationNear(position, radius);
  }

  /**
   * Remove vegetation at position (harvesting)
   * @param {THREE.Vector3} position
   * @param {number} radius
   * @returns {number} Count of removed vegetation
   */
  removeVegetationAt(position, radius = 2) {
    return this.vegetationSystem.removeVegetationAt(position, radius);
  }

  /**
   * Spawn vegetation at position (replanting)
   * @param {string} type - Vegetation type
   * @param {THREE.Vector3} position
   */
  spawnVegetationAt(type, position) {
    return this.vegetationSystem.spawnVegetationAt(type, position);
  }

  /**
   * Enable/disable streaming (load all or stream)
   */
  setStreaming(enabled) {
    this.enableStreaming = enabled;

    if (enabled) {
      console.log('🌍 Streaming enabled');
      this.regionStreaming.unloadAllRegions();
      this.regionStreaming.update(this.playerPosition);
    } else {
      console.log('🌍 Streaming disabled, loading all regions');
      this.regionStreaming.loadAllRegions();
    }
  }

  /**
   * Set streaming radius
   * @param {number} radius - In region units (default 2)
   */
  setStreamingRadius(radius) {
    this.regionStreaming.setLoadRadius(radius);
  }

  /**
   * Enable/disable LOD
   */
  setLOD(enabled) {
    this.enableLOD = enabled;
    console.log(`🎯 LOD ${enabled ? 'enabled' : 'disabled'}`);
  }

  /**
   * Debug: Visualize LOD levels
   */
  debugLOD(enabled = true) {
    this.lodManager.debugVisualizeLOD(enabled);
  }

  /**
   * Debug: Log all loaded regions
   */
  debugRegions() {
    this.regionStreaming.debugLogLoadedRegions();
  }

  /**
   * Get comprehensive stats
   */
  getStats() {
    return {
      world: {
        size: this.config.worldSize,
        center: this.config.center,
        initialized: this.initialized
      },
      player: {
        position: this.playerPosition.toArray(),
        currentRegion: this.getCurrentRegion()?.name || 'Unknown'
      },
      streaming: this.regionStreaming.getStats(),
      lod: this.lodManager.getStats(),
      vegetation: this.vegetationSystem.getStats(),
      cities: this.cityBuilder.getStats()
    };
  }

  /**
   * Log statistics to console
   */
  logStats() {
    console.log('📊 === NAJIKA WORLD STATISTICS ===');

    const stats = this.getStats();

    console.log('🌍 World:');
    console.log(`   Size: ${stats.world.size}x${stats.world.size}`);
    console.log(`   Initialized: ${stats.world.initialized}`);

    console.log('📍 Player:');
    console.log(`   Position: (${stats.player.position[0].toFixed(0)}, ${stats.player.position[2].toFixed(0)})`);
    console.log(`   Current Region: ${stats.player.currentRegion}`);

    console.log('🗺️ Streaming:');
    console.log(`   Loaded Regions: ${stats.streaming.loadedRegions} / ${stats.streaming.totalRegions}`);
    console.log(`   Load Radius: ${stats.streaming.loadRadiusRegions} regions (${stats.streaming.loadRadiusWorldUnits} units)`);

    console.log('🌿 Vegetation:');
    console.log(`   Regions: ${stats.vegetation.regionsLoaded}`);
    console.log(`   Total Items: ${stats.vegetation.totalVegetation}`);
    console.log(`   Templates: ${stats.vegetation.templatesLoaded}`);

    console.log('🏘️ Cities:');
    console.log(`   Loaded: ${stats.cities.citiesLoaded}`);
    console.log(`   Total Buildings: ${stats.cities.totalBuildings}`);

    console.log('🎯 LOD:');
    console.log(`   High Detail: ${stats.lod.highDetail}`);
    console.log(`   Medium Detail: ${stats.lod.mediumDetail}`);
    console.log(`   Low Detail: ${stats.lod.lowDetail}`);
    console.log(`   Culled: ${stats.lod.culled}`);

    console.log('===================================');
  }

  /**
   * List all cities
   */
  listCities() {
    console.log('🏘️ === CITIES IN NAJIKA WORLD ===');
    this.regionStreaming.cityData.cities.forEach((city, i) => {
      console.log(`${i + 1}. ${city.name} (${city.region})`);
      console.log(`   Position: (${city.position.x}, ${city.position.z})`);
      console.log(`   Size: ${city.size}, Population: ${city.population}`);
      if (city.isCapital) console.log('   ⭐ CAPITAL');
      if (city.foodSpeciality) {
        console.log(`   🍖 Specialty: ${city.foodSpeciality.name}`);
      }
    });
    console.log('===================================');
  }

  /**
   * List all regions
   */
  listRegions() {
    console.log('🗺️ === REGIONS IN NAJIKA WORLD ===');
    Object.values(this.regionStreaming.regionData.regions).forEach((region, i) => {
      console.log(`${i + 1}. ${region.name} (${region.id})`);
      console.log(`   Biome: ${region.biome}`);
      console.log(`   Position: (${region.position.x}, ${region.position.z})`);
      console.log(`   Level: ${region.level}`);
      if (region.city) console.log(`   🏘️ City: ${region.city.name}`);
      if (region.underground) console.log('   🕳️ Underground');
    });
    console.log('===================================');
  }

  /**
   * Cleanup (dispose all resources)
   */
  dispose() {
    console.log('🌍 Disposing world...');

    this.regionStreaming.unloadAllRegions();
    this.vegetationSystem.clearAllVegetation();
    this.lodManager.clear();

    this.initialized = false;

    console.log('✅ World disposed');
  }
}

export default WorldManager;
