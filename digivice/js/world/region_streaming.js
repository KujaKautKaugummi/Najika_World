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

    // GLTFLoader for special locations
    this.gltfLoader = new THREE.GLTFLoader();

    // Special location meshes
    this.specialMeshes = new Map();

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
        this.cityBuilder.buildCity(cityData);
        this.stats.loadedCities++;
      }
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

    // WICHTIG: +Math.PI / 2 (nicht -Math.PI / 2)!
    // Sonst sind Normalen invertiert und Beleuchtung trifft Unterseite!
    terrainMesh.rotation.x = +Math.PI / 2;

    return terrainMesh;
  }

  /**
   * Load region-specific features
   */
  loadRegionFeatures(region, regionGroup) {
    // Special locations (Funkelnest, Leuchtturm, etc.)
    if (region.specialLocation) {
      console.log(`  🎯 Adding special location: ${region.specialLocation.name || region.specialLocation}`);
      // TODO: Add special location markers/buildings
    }

    // Götterfels special handling
    if (region.id === 'goetterfels') {
      this.loadGoetterfelsFeatures(region, regionGroup);
    }

    // Tiefenhöhlen entrance
    if (region.id === 'tiefenhoehlen') {
      console.log(`  🕳️ Adding cave entrance at (${region.entrance.x}, ${region.entrance.z})`);
      this.loadCaveEntrance(region, regionGroup);
    }
  }

  /**
   * Load Götterfels special features
   */
  loadGoetterfelsFeatures(region, regionGroup) {
    console.log('  ⛰️ Loading Götterfels features...');

    // Schwarze Mühle (on peak)
    if (region.specialLocations && region.specialLocations.peak) {
      const peak = region.specialLocations.peak;
      console.log(`    🏠 ${peak.name} - ${peak.rooms} rooms (Safe Zone)`);
      this.loadSchwarzeMuehle(peak, regionGroup);
    }

    // Fluss (river)
    console.log('    🌊 River flowing down the mountain');
    this.loadRiver(region, regionGroup);

    // Kleines Dorf (small village)
    console.log('    🏘️ Small village');
    this.loadVillage(region, regionGroup);
  }

  /**
   * Load Schwarze Mühle (Najika's Home)
   */
  async loadSchwarzeMuehle(peakData, regionGroup) {
    try {
      const gltf = await new Promise((resolve, reject) => {
        this.gltfLoader.load('static/assets/kaykit/medieval/building_windmill_red.gltf', resolve, undefined, reject);
      });

      const schwarzeMuehle = gltf.scene;
      schwarzeMuehle.position.set(peakData.position.x, 5, peakData.position.z);
      schwarzeMuehle.scale.set(2.5, 2.5, 2.5);

      // Make it BLACK (Schwarze Mühle)
      schwarzeMuehle.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
          child.material = new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            roughness: 0.6,
            metalness: 0.3,
            emissive: 0x0a0a0a,
            emissiveIntensity: 0.2
          });
        }
      });

      // UserData for interaction system
      schwarzeMuehle.userData.buildingType = 'schwarze_muehle';
      schwarzeMuehle.userData.buildingName = 'Schwarze Windmühle';
      schwarzeMuehle.userData.proximityRadius = 15;
      schwarzeMuehle.userData.safeZone = peakData.safeZone;
      schwarzeMuehle.userData.rooms = peakData.rooms;

      regionGroup.add(schwarzeMuehle);
      this.specialMeshes.set('schwarze_muehle', schwarzeMuehle);

      // Add glowing marker above
      const markerGeometry = new THREE.SphereGeometry(1, 16, 16);
      const markerMaterial = new THREE.MeshStandardMaterial({
        color: 0x8b00ff,
        emissive: 0x8b00ff,
        emissiveIntensity: 1,
        transparent: true,
        opacity: 0.8
      });
      const marker = new THREE.Mesh(markerGeometry, markerMaterial);
      marker.position.set(peakData.position.x, 18, peakData.position.z);
      regionGroup.add(marker);

      // Pulsing animation
      marker.userData.animateMarker = (time) => {
        marker.scale.setScalar(1 + Math.sin(time * 0.003) * 0.3);
      };

      this.specialMeshes.set('schwarze_muehle_marker', marker);

      console.log('    ✅ Schwarze Mühle loaded successfully!');
    } catch (error) {
      console.error('    ❌ Failed to load Schwarze Mühle:', error);
    }
  }

  /**
   * Load River mesh flowing down the mountain
   */
  loadRiver(region, regionGroup) {
    // Create simple river using planes
    const riverGeometry = new THREE.PlaneGeometry(20, 300);
    const riverMaterial = new THREE.MeshStandardMaterial({
      color: 0x2a5f9e,
      transparent: true,
      opacity: 0.7,
      roughness: 0.1,
      metalness: 0.3,
      emissive: 0x1a3f6e,
      emissiveIntensity: 0.2
    });

    const river = new THREE.Mesh(riverGeometry, riverMaterial);
    river.rotation.x = -Math.PI / 2;
    river.position.set(4800, 0.1, 4650);
    river.userData.type = 'river';

    regionGroup.add(river);
    this.specialMeshes.set('goetterfels_river', river);

    console.log('    ✅ River mesh added');
  }

  /**
   * Load cave entrance mesh
   */
  loadCaveEntrance(region, regionGroup) {
    if (!region.entrance) return;

    const entranceX = region.entrance.x;
    const entranceZ = region.entrance.z;

    // Create cave entrance structure
    const entranceGroup = new THREE.Group();

    // Cave opening (dark tunnel)
    const tunnelGeometry = new THREE.CylinderGeometry(8, 10, 15, 16);
    const tunnelMaterial = new THREE.MeshStandardMaterial({
      color: 0x1a1a1a,
      roughness: 0.9,
      metalness: 0.1,
      emissive: 0x000000
    });
    const tunnel = new THREE.Mesh(tunnelGeometry, tunnelMaterial);
    tunnel.rotation.z = Math.PI / 2; // Horizontal tunnel
    tunnel.position.set(entranceX, 5, entranceZ);
    tunnel.castShadow = true;
    tunnel.receiveShadow = true;
    entranceGroup.add(tunnel);

    // Rocky arch around entrance
    const rockGeometry = new THREE.DodecahedronGeometry(6, 1);
    const rockMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a4a4a,
      roughness: 0.95,
      metalness: 0.05
    });

    // Left rock
    const leftRock = new THREE.Mesh(rockGeometry, rockMaterial);
    leftRock.position.set(entranceX - 8, 6, entranceZ);
    leftRock.scale.set(1.2, 1.5, 0.8);
    leftRock.rotation.set(0.2, 0.5, 0.1);
    leftRock.castShadow = true;
    leftRock.receiveShadow = true;
    entranceGroup.add(leftRock);

    // Right rock
    const rightRock = new THREE.Mesh(rockGeometry.clone(), rockMaterial.clone());
    rightRock.position.set(entranceX + 8, 6, entranceZ);
    rightRock.scale.set(1.2, 1.5, 0.8);
    rightRock.rotation.set(-0.2, -0.5, -0.1);
    rightRock.castShadow = true;
    rightRock.receiveShadow = true;
    entranceGroup.add(rightRock);

    // Top rock
    const topRock = new THREE.Mesh(rockGeometry.clone(), rockMaterial.clone());
    topRock.position.set(entranceX, 12, entranceZ);
    topRock.scale.set(2, 0.8, 1);
    topRock.rotation.set(0, 0.3, 0);
    topRock.castShadow = true;
    topRock.receiveShadow = true;
    entranceGroup.add(topRock);

    // Glowing crystals at entrance
    const crystalGeometry = new THREE.ConeGeometry(0.5, 2, 6);
    const crystalMaterial = new THREE.MeshStandardMaterial({
      color: 0x9370db,
      roughness: 0.2,
      metalness: 0.3,
      emissive: 0x9370db,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.8
    });

    // Place crystals around entrance
    const crystalPositions = [
      { x: entranceX - 6, y: 2, z: entranceZ + 3 },
      { x: entranceX + 6, y: 2, z: entranceZ - 3 },
      { x: entranceX - 4, y: 3, z: entranceZ - 5 },
      { x: entranceX + 5, y: 2, z: entranceZ + 4 }
    ];

    crystalPositions.forEach(pos => {
      const crystal = new THREE.Mesh(crystalGeometry.clone(), crystalMaterial.clone());
      crystal.position.set(pos.x, pos.y, pos.z);
      crystal.rotation.set(
        Math.random() * 0.5,
        Math.random() * Math.PI * 2,
        Math.random() * 0.5
      );
      crystal.castShadow = true;
      entranceGroup.add(crystal);
    });

    // Point light inside cave (spooky glow)
    const caveLight = new THREE.PointLight(0x9370db, 2, 30);
    caveLight.position.set(entranceX, 5, entranceZ);
    caveLight.castShadow = true;
    entranceGroup.add(caveLight);

    // Fog/mist effect at entrance
    const mistGeometry = new THREE.SphereGeometry(8, 16, 16);
    const mistMaterial = new THREE.MeshBasicMaterial({
      color: 0x444444,
      transparent: true,
      opacity: 0.3,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    const mist = new THREE.Mesh(mistGeometry, mistMaterial);
    mist.position.set(entranceX, 5, entranceZ);
    entranceGroup.add(mist);

    // Animate mist (pulsing effect)
    mist.userData.animateMist = (time) => {
      mist.scale.setScalar(1 + Math.sin(time * 0.001) * 0.2);
      mist.material.opacity = 0.2 + Math.sin(time * 0.002) * 0.1;
    };

    // Sign: "Tiefenhöhlen - Level 15+"
    const signCanvas = document.createElement('canvas');
    signCanvas.width = 512;
    signCanvas.height = 128;
    const ctx = signCanvas.getContext('2d');

    // Sign background
    ctx.fillStyle = 'rgba(80, 50, 30, 0.9)';
    ctx.fillRect(0, 0, signCanvas.width, signCanvas.height);
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 4;
    ctx.strokeRect(0, 0, signCanvas.width, signCanvas.height);

    // Sign text
    ctx.fillStyle = '#ffcc00';
    ctx.font = 'bold 48px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('⚠️ TIEFENHÖHLEN ⚠️', signCanvas.width / 2, 40);
    ctx.font = 'bold 32px Arial';
    ctx.fillStyle = '#ff4444';
    ctx.fillText('LEVEL 15+ REQUIRED', signCanvas.width / 2, 90);

    const signTexture = new THREE.CanvasTexture(signCanvas);
    const signSpriteMaterial = new THREE.SpriteMaterial({
      map: signTexture,
      transparent: true
    });
    const sign = new THREE.Sprite(signSpriteMaterial);
    sign.scale.set(10, 2.5, 1);
    sign.position.set(entranceX, 15, entranceZ - 12);
    entranceGroup.add(sign);

    // UserData for interaction system
    entranceGroup.userData.buildingType = 'cave_entrance';
    entranceGroup.userData.buildingName = 'Tiefenhöhlen Eingang';
    entranceGroup.userData.proximityRadius = 20;
    entranceGroup.userData.minLevel = 15;
    entranceGroup.userData.teleportTo = {
      region: 'tiefenhoehlen',
      x: region.entrance.x,
      y: -20, // Underground
      z: region.entrance.z
    };

    regionGroup.add(entranceGroup);
    this.specialMeshes.set('cave_entrance', entranceGroup);

    console.log('    ✅ Cave entrance mesh created');
  }

  /**
   * Load Village buildings
   */
  async loadVillage(region, regionGroup) {
    const villagePositions = [
      { x: 4750, z: 4750 },
      { x: 4770, z: 4760 },
      { x: 4730, z: 4770 }
    ];

    for (let i = 0; i < villagePositions.length; i++) {
      try {
        const gltf = await new Promise((resolve, reject) => {
          this.gltfLoader.load('static/assets/kaykit/medieval/building_home_A_red.gltf', resolve, undefined, reject);
        });

        const house = gltf.scene.clone();
        house.position.set(villagePositions[i].x, 0, villagePositions[i].z);
        house.scale.set(1.5, 1.5, 1.5);

        house.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });

        house.userData.buildingType = 'village_house';
        house.userData.buildingName = `Village House ${i + 1}`;

        regionGroup.add(house);
        this.specialMeshes.set(`village_house_${i}`, house);
      } catch (error) {
        console.error(`    ❌ Failed to load village house ${i}:`, error);
      }
    }

    console.log('    ✅ Village buildings loaded');
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
