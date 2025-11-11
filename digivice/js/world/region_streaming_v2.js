// 🌍 REGION STREAMING - Load/Unload Regionen basierend auf Spieler-Position
// Optimiert Performance für die große 9600x9600 Welt

const THREE = window.THREE;

class RegionStreaming {
  constructor(scene, terrainGenerator, biomeSystem, vegetationSystem, cityBuilder) {
    this.scene = scene;
    this.terrainGenerator = terrainGenerator;
    this.biomeSystem = biomeSystem;
    this.vegetationSystem = vegetationSystem;
    this.cityBuilder = cityBuilder;

    this.loadedRegions = new Map();  // Currently loaded regions
    this.regionData = null;  // Data from regions.json
    this.biomeData = null;  // Data from biomes.json
    this.cityData = null;  // Data from cities.json

    this.loadRadius = 2;  // Load regions within this distance (in region units)
    this.playerPosition = new THREE.Vector3(4800, 0, 4800);  // Start at Götterfels

    // Performance stats
    this.stats = {
      loadedRegions: 0,
      loadedTerrain: 0,
      loadedVegetation: 0,
      loadedCities: 0,
      streamingCalls: 0
    };
  }

  /**
   * Lade JSON-Daten
   */
  async loadData(regionDataPath, biomeDataPath, cityDataPath) {
    console.log('🌍 Loading world data...');

    try {
      // Load regions.json
      const regionResponse = await fetch(regionDataPath);
      this.regionData = await regionResponse.json();
      console.log(`  ✅ Regions loaded: ${Object.keys(this.regionData.regions).length}`);

      // Load biomes.json
      const biomeResponse = await fetch(biomeDataPath);
      this.biomeData = await biomeResponse.json();
      console.log(`  ✅ Biomes loaded: ${Object.keys(this.biomeData.biomes).length}`);

      // Load cities.json
      const cityResponse = await fetch(cityDataPath);
      this.cityData = await cityResponse.json();
      console.log(`  ✅ Cities loaded: ${this.cityData.cities.length}`);

      // Initialize subsystems
      this.biomeSystem.loadBiomes(this.biomeData);
      this.vegetationSystem.initializeTemplates();
      this.cityBuilder.initializeTemplates();

      console.log('🌍 World data loaded successfully!');
      return true;
    } catch (error) {
      console.error('❌ Failed to load world data:', error);
      return false;
    }
  }

  /**
   * Update streaming (call every frame or when player moves significantly)
   * @param {THREE.Vector3} playerPosition - Current player position
   */
  update(playerPosition) {
    this.playerPosition.copy(playerPosition);
    this.stats.streamingCalls++;

    // Determine which regions should be loaded
    const regionsToLoad = this.getRegionsInRange(playerPosition);
    const regionsToUnload = this.getRegionsOutOfRange(regionsToLoad);

    // Unload distant regions
    for (const regionId of regionsToUnload) {
      this.unloadRegion(regionId);
    }

    // Load nearby regions
    for (const regionId of regionsToLoad) {
      if (!this.loadedRegions.has(regionId)) {
        this.loadRegion(regionId);
      }
    }

    // Update biome environment based on current player region
    const currentRegion = this.getCurrentRegion(playerPosition);
    if (currentRegion) {
      const biomeId = currentRegion.biome;
      if (this.biomeSystem.currentBiome !== biomeId) {
        this.biomeSystem.applyBiomeEnvironment(biomeId);
      }
    }
  }

  /**
   * Get which regions are in range of player
   * @param {THREE.Vector3} position
   * @returns {Set<string>} Region IDs to load
   */
  getRegionsInRange(position) {
    const regionsToLoad = new Set();

    if (!this.regionData) return regionsToLoad;

    for (const [regionId, region] of Object.entries(this.regionData.regions)) {
      // Check if player is within load radius of this region
      const regionCenter = new THREE.Vector3(region.position.x, 0, region.position.z);
      const distance = position.distanceTo(regionCenter);

      // Load radius in world units (approx 2400 per region, load 2 regions away)
      const loadDistance = 2400 * this.loadRadius;

      if (distance < loadDistance) {
        regionsToLoad.add(regionId);
      }
    }

    // Always load Götterfels (center mountain)
    regionsToLoad.add('goetterfels');

    return regionsToLoad;
  }

  /**
   * Get which regions are out of range and should be unloaded
   * @param {Set<string>} regionsToLoad
   * @returns {Set<string>} Region IDs to unload
   */
  getRegionsOutOfRange(regionsToLoad) {
    const regionsToUnload = new Set();

    for (const regionId of this.loadedRegions.keys()) {
      if (!regionsToLoad.has(regionId)) {
        regionsToUnload.add(regionId);
      }
    }

    return regionsToUnload;
  }

  /**
   * Get current region player is in
   * @param {THREE.Vector3} position
   * @returns {Object|null} Region data
   */
  getCurrentRegion(position) {
    if (!this.regionData) return null;

    for (const region of Object.values(this.regionData.regions)) {
      const { bounds } = region;
      if (
        position.x >= bounds.minX &&
        position.x <= bounds.maxX &&
        position.z >= bounds.minZ &&
        position.z <= bounds.maxZ
      ) {
        return region;
      }
    }

    return null;
  }

  /**
   * Load a region
   * @param {string} regionId
   */
  loadRegion(regionId) {
    if (this.loadedRegions.has(regionId)) {
      console.warn(`🌍 Region already loaded: ${regionId}`);
      return;
    }

    const region = this.regionData.regions[regionId];
    if (!region) {
      console.error(`❌ Region not found: ${regionId}`);
      return;
    }

    console.log(`🌍 Loading region: ${region.name}`);

    const regionGroup = new THREE.Group();
    regionGroup.name = `region_${regionId}`;

    // 1. Generate Terrain
    const terrainMesh = this.loadRegionTerrain(region);
    if (terrainMesh) {
      regionGroup.add(terrainMesh);
      this.stats.loadedTerrain++;
    }

    // 2. Populate Vegetation
    this.vegetationSystem.populateRegion(regionId, region, this.biomeData);
    this.stats.loadedVegetation++;

    // 3. Build City (if exists)
    if (region.city && region.city.name) {
      const cityData = this.getCityData(region.city.name);
      if (cityData) {
        console.log(`  🏘️ Building city: ${cityData.name} at (${cityData.position.x}, ${cityData.position.z})`);
        this.cityBuilder.buildCity(cityData);
        this.stats.loadedCities++;
      }
    } else if (region.city === null) {
      console.log(`  ℹ️  No city in this region (${region.name}) - this is intentional`);
    }

    // 4. Add special features
    this.loadRegionFeatures(region, regionGroup);

    // Mark as loaded
    this.loadedRegions.set(regionId, {
      group: regionGroup,
      region: region,
      loadTime: Date.now()
    });

    this.scene.add(regionGroup);
    this.stats.loadedRegions++;

    console.log(`  ✅ Region loaded: ${region.name}`);
  }

  /**
   * Load region terrain
   */
  loadRegionTerrain(region) {
    const biome = this.biomeData.biomes[region.biome];
    if (!biome) {
      console.error(`❌ Biome not found: ${region.biome}`);
      return null;
    }

    // Generate terrain geometry
    const terrainGeometry = this.terrainGenerator.generateRegionTerrain(region, this.biomeData);

    // Create ground material
    const groundMaterial = this.biomeSystem.createGroundMaterial(region.biome);

    // DEBUG: Log material color
    console.log(`🎨 TERRAIN MATERIAL - ${region.name}:`, {
      biome: region.biome,
      colorHex: '#' + groundMaterial.color.getHexString(),
      roughness: groundMaterial.roughness,
      metalness: groundMaterial.metalness
    });

    // Create mesh
    const terrainMesh = new THREE.Mesh(terrainGeometry, groundMaterial);
    terrainMesh.receiveShadow = true;
    terrainMesh.castShadow = false;  // Terrain wirft keine Schatten
    terrainMesh.name = `terrain_${region.id}`;

    // Position terrain at region center
    // Y-Position MUSS über Character-Spawn sein!
    terrainMesh.position.set(region.position.x, 0, region.position.z);

    // Simple rotation - Three.js handles normals automatically!
    // (wie in der alten funktionierenden Version najika_world.html)
    terrainMesh.rotation.x = -Math.PI / 2;

    return terrainMesh;
  }

  /**
   * Load region-specific features
   */
  loadRegionFeatures(region, regionGroup) {
    // Special locations (Funkelnest, Leuchtturm, etc.)
    if (region.specialLocation) {
      console.log(`  🎯 Special location in region: ${region.specialLocation.name || region.specialLocation}`);
      // Note: Special locations currently don't load physical assets to avoid placeholder boxes
    }

    // Götterfels special handling
    if (region.id === 'goetterfels') {
      this.loadGoetterfelsFeatures(region, regionGroup);
    }

    // Tiefenhöhlen entrance
    if (region.id === 'tiefenhoehlen') {
      console.log(`  🕳️ Cave entrance marked at (${region.entrance.x}, ${region.entrance.z})`);
      // Note: Cave entrance currently doesn't load to avoid placeholder boxes
    }
  }

  /**
   * Load Götterfels special features
   */
  loadGoetterfelsFeatures(region, regionGroup) {
    console.log('  ⛰️ Götterfels features noted (assets disabled to prevent placeholder boxes):');

    // Schwarze Mühle (on peak)
    if (region.specialLocations && region.specialLocations.peak) {
      const peak = region.specialLocations.peak;
      console.log(`    🏠 ${peak.name} - ${peak.rooms} rooms (Safe Zone) - Asset loading disabled`);
    }

    // Fluss (river)
    console.log('    🌊 River flowing down the mountain - Asset loading disabled');

    // Kleines Dorf (small village)
    console.log('    🏘️ Small village - Asset loading disabled');

    // NOTE: Physical assets for these features are disabled to prevent magenta placeholder boxes
    // Re-enable when proper GLB models are available
  }

  /**
   * Unload a region
   * @param {string} regionId
   */
  unloadRegion(regionId) {
    const loadedRegion = this.loadedRegions.get(regionId);
    if (!loadedRegion) return;

    console.log(`🌍 Unloading region: ${loadedRegion.region.name}`);

    // Remove terrain mesh
    this.scene.remove(loadedRegion.group);
    loadedRegion.group.traverse(obj => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) {
          obj.material.forEach(mat => mat.dispose());
        } else {
          obj.material.dispose();
        }
      }
    });
    loadedRegion.group.clear();

    // Remove vegetation
    this.vegetationSystem.removeRegionVegetation(regionId);

    // Remove city (if exists)
    const cityData = this.getCityData(loadedRegion.region.city?.name);
    if (cityData) {
      this.cityBuilder.removeCity(cityData.id);
    }

    this.loadedRegions.delete(regionId);
    this.stats.loadedRegions--;

    console.log(`  ✅ Region unloaded: ${loadedRegion.region.name}`);
  }

  /**
   * Get city data by name
   */
  getCityData(cityName) {
    if (!this.cityData || !cityName) return null;
    return this.cityData.cities.find(city => city.name === cityName);
  }

  /**
   * Force load all regions (for testing, not recommended for production)
   */
  loadAllRegions() {
    console.log('🌍 Loading ALL regions (this may impact performance)...');

    for (const regionId of Object.keys(this.regionData.regions)) {
      this.loadRegion(regionId);
    }

    console.log('🌍 All regions loaded!');
  }

  /**
   * Unload all regions
   */
  unloadAllRegions() {
    console.log('🌍 Unloading all regions...');

    const regionIds = Array.from(this.loadedRegions.keys());
    for (const regionId of regionIds) {
      this.unloadRegion(regionId);
    }

    console.log('🌍 All regions unloaded');
  }

  /**
   * Get regions near position (for UI, minimap, etc.)
   * @param {THREE.Vector3} position
   * @param {number} radius - In world units
   * @returns {Array<Object>} Region data
   */
  getRegionsNearPosition(position, radius = 5000) {
    const nearbyRegions = [];

    if (!this.regionData) return nearbyRegions;

    for (const region of Object.values(this.regionData.regions)) {
      const regionCenter = new THREE.Vector3(region.position.x, 0, region.position.z);
      const distance = position.distanceTo(regionCenter);

      if (distance < radius) {
        nearbyRegions.push({
          ...region,
          distance: distance,
          isLoaded: this.loadedRegions.has(region.id)
        });
      }
    }

    // Sort by distance
    nearbyRegions.sort((a, b) => a.distance - b.distance);

    return nearbyRegions;
  }

  /**
   * Set load radius (in region units, default 2)
   */
  setLoadRadius(radius) {
    this.loadRadius = Math.max(1, radius);
    console.log(`🌍 Load radius set to: ${this.loadRadius} regions`);
  }

  /**
   * Get statistics
   */
  getStats() {
    return {
      ...this.stats,
      loadedRegions: this.loadedRegions.size,
      totalRegions: this.regionData ? Object.keys(this.regionData.regions).length : 0,
      loadRadiusRegions: this.loadRadius,
      loadRadiusWorldUnits: this.loadRadius * 2400
    };
  }

  /**
   * Debug: Log all loaded regions
   */
  debugLogLoadedRegions() {
    console.log('🌍 Currently loaded regions:');
    for (const [regionId, data] of this.loadedRegions.entries()) {
      const timeLoaded = ((Date.now() - data.loadTime) / 1000).toFixed(1);
      console.log(`  - ${data.region.name} (${regionId}) - loaded ${timeLoaded}s ago`);
    }
  }
}

export default RegionStreaming;
