// 🎨 BIOME SYSTEM - Verwaltet Biome-Konfigurationen und visuelle Eigenschaften
// Lädt Biome-Daten, erstellt Materialien, Himmel, Nebel, Beleuchtung

const THREE = window.THREE;

class BiomeSystem {
  constructor(scene, camera) {
    this.scene = scene;
    this.camera = camera;
    this.biomes = new Map();
    this.currentBiome = null;
    this.transitionSpeed = 0.02;  // Sanfter Übergang zwischen Biomes
  }

  /**
   * Lade Biome-Daten aus JSON
   * @param {Object} biomeData - Biome-Daten aus biomes.json
   */
  loadBiomes(biomeData) {
    console.log('🎨 Loading biomes...');

    for (const [biomeId, config] of Object.entries(biomeData.biomes)) {
      this.biomes.set(biomeId, this.processBiomeConfig(biomeId, config));
      console.log(`  ✅ Loaded: ${config.name}`);
    }

    console.log(`🎨 Total biomes loaded: ${this.biomes.size}`);
  }

  /**
   * Verarbeite Biome-Konfiguration
   * @param {string} biomeId - Biome ID
   * @param {Object} config - Biome Config aus JSON
   * @returns {Object} Processed biome config
   */
  processBiomeConfig(biomeId, config) {
    return {
      id: biomeId,
      name: config.name,
      colors: {
        ground: new THREE.Color(config.colors.ground),
        ambient: new THREE.Color(config.colors.ambient),
        fog: new THREE.Color(config.colors.fog),
        water: config.colors.water ? new THREE.Color(config.colors.water) : null,
        lava: config.colors.lava ? new THREE.Color(config.colors.lava) : null,
        crystal: config.colors.crystal ? new THREE.Color(config.colors.crystal) : null
      },
      vegetation: config.vegetation,
      terrain: config.terrain,
      enemies: config.enemies || [],
      weather: config.weather || [],
      waterPresence: config.waterPresence || false,
      hasOcean: config.hasOcean || false,
      lavaFlows: config.lavaFlows || false,
      requiresLight: config.requiresLight || false,
      underground: config.underground || false,
      hazardous: config.hazardous || false,
      necromancy: config.necromancy || false,
      indestructible: config.indestructible || false,
      safeZone: config.safeZone || false,
      ambientDarkness: config.ambientDarkness || 0
    };
  }

  /**
   * Erstelle Ground Material für ein Biome
   * @param {string} biomeId - Biome ID
   * @returns {THREE.Material} Ground material
   */
  createGroundMaterial(biomeId) {
    const biome = this.biomes.get(biomeId);
    if (!biome) {
      console.warn(`⚠️ Biome ${biomeId} not found! Using gray fallback.`);
      console.warn(`⚠️ Available biomes:`, Array.from(this.biomes.keys()));
      return new THREE.MeshStandardMaterial({ color: 0x808080 });
    }

    // biome.colors.ground ist bereits ein THREE.Color (von processBiomeConfig)
    // KEINE doppelte Konversion!
    const groundColor = biome.colors.ground;

    // DEBUG: Log biome color data
    console.log(`🎨 Creating material for biome "${biomeId}":`, {
      groundColor: groundColor,
      groundColorHex: '#' + groundColor.getHexString(),
      roughness: this.getTerrainRoughness(biome),
      metalness: this.getTerrainMetalness(biome)
    });

    const material = new THREE.MeshStandardMaterial({
      color: groundColor,
      roughness: this.getTerrainRoughness(biome),
      metalness: this.getTerrainMetalness(biome),
      side: THREE.DoubleSide  // WICHTIG: Beide Seiten rendern!
    });

    // Spezielle Eigenschaften pro Biome
    switch(biomeId) {
      case 'ice':
        material.roughness = 0.2;  // Glatt (Eis)
        material.metalness = 0.1;
        break;
      case 'swamp':
        material.roughness = 0.9;  // Rau (Schlamm)
        // Farbe wird bereits im Material gesetzt, nicht dunkler machen
        break;
      case 'volcano':
        material.roughness = 0.8;  // Rau (Vulkangestein)
        material.emissive = new THREE.Color(0x331100);  // Leicht glühend
        material.emissiveIntensity = 0.2;
        break;
      case 'caves':
        material.roughness = 0.7;
        // Farbe wird bereits im Material gesetzt, nicht dunkler machen
        break;
    }

    return material;
  }

  getTerrainRoughness(biome) {
    const roughnessMap = {
      'desert': 0.9,
      'forest': 0.8,
      'coast': 0.7,
      'highland': 0.85,
      'swamp': 0.95,
      'ice': 0.2,
      'volcano': 0.9,
      'mountain': 0.8,
      'caves': 0.7
    };
    return roughnessMap[biome.id] || 0.8;
  }

  getTerrainMetalness(biome) {
    const metalnessMap = {
      'ice': 0.3,      // Etwas reflektierend
      'water': 0.5,    // Reflektierend
      'default': 0.0   // Nicht-metallisch
    };
    return metalnessMap[biome.id] || 0.0;
  }

  /**
   * Wende Biome-Umgebung an (Himmel, Nebel, Licht)
   * @param {string} biomeId - Biome ID
   */
  applyBiomeEnvironment(biomeId) {
    const biome = this.biomes.get(biomeId);
    if (!biome) return;

    console.log(`🎨 Applying environment: ${biome.name}`);

    // Background Color (Himmel)
    this.scene.background = biome.colors.fog;

    // Nebel
    this.applyFog(biome);

    // Beleuchtung
    this.applyLighting(biome);

    // Spezielle Effekte
    if (biome.underground) {
      this.applyUndergroundEffects(biome);
    }

    if (biome.lavaFlows) {
      this.applyLavaEffects(biome);
    }

    this.currentBiome = biomeId;
  }

  /**
   * Nebel anwenden
   */
  applyFog(biome) {
    const fogColor = biome.colors.fog;
    const fogDensity = this.getFogDensity(biome);
    const fogDistance = this.getFogDistance(biome);

    // Exponential Fog (dichter Nebel) oder Linear Fog
    if (biome.id === 'swamp' || biome.id === 'caves') {
      // Dichter Nebel
      this.scene.fog = new THREE.FogExp2(fogColor, fogDensity);
    } else {
      // Normaler Nebel
      this.scene.fog = new THREE.Fog(
        fogColor,
        fogDistance.near,
        fogDistance.far
      );
    }
  }

  getFogDensity(biome) {
    const densityMap = {
      'swamp': 0.008,      // Sehr dichter Nebel
      'caves': 0.01,       // Extrem dichter Nebel
      'ice': 0.003,        // Leichter Nebel
      'default': 0.001
    };
    return densityMap[biome.id] || densityMap.default;
  }

  getFogDistance(biome) {
    const distanceMap = {
      'desert': { near: 500, far: 2000 },    // Weit sichtbar
      'forest': { near: 200, far: 800 },     // Eingeschränkt durch Bäume
      'coast': { near: 300, far: 1500 },     // Gute Sicht
      'highland': { near: 400, far: 2000 },  // Sehr weit
      'ice': { near: 300, far: 1200 },       // Schnee reduziert Sicht
      'volcano': { near: 250, far: 1000 },   // Asche reduziert Sicht
      'mountain': { near: 400, far: 2500 },  // Extrem weit
      'default': { near: 300, far: 1000 }
    };
    return distanceMap[biome.id] || distanceMap.default;
  }

  /**
   * Beleuchtung anwenden
   */
  applyLighting(biome) {
    // Entferne alte Lichter (außer Directional Light für Sonne)
    const lightsToRemove = [];
    this.scene.traverse(obj => {
      if (obj.isLight && obj.name === 'biome_ambient') {
        lightsToRemove.push(obj);
      }
    });
    lightsToRemove.forEach(light => this.scene.remove(light));

    // Ambient Light (Grundbeleuchtung)
    const ambientIntensity = this.getAmbientIntensity(biome);
    const ambientLight = new THREE.AmbientLight(
      biome.colors.ambient,
      ambientIntensity
    );
    ambientLight.name = 'biome_ambient';
    this.scene.add(ambientLight);

    // Spezielle Beleuchtung pro Biome
    switch(biome.id) {
      case 'volcano':
        this.addVolcanoLighting();
        break;
      case 'caves':
        this.addCaveLighting();
        break;
      case 'ice':
        this.addIceLighting();
        break;
    }
  }

  getAmbientIntensity(biome) {
    if (biome.underground) return 0.2 * (1 - biome.ambientDarkness);
    if (biome.id === 'volcano') return 0.6;  // Lava-Glühen
    if (biome.id === 'ice') return 0.8;      // Schnee reflektiert
    return 0.5;  // Standard
  }

  addVolcanoLighting() {
    // Rötliches Lava-Glühen
    const lavaGlow = new THREE.PointLight(0xff4500, 1.5, 200);
    lavaGlow.position.set(0, 50, 0);
    lavaGlow.name = 'biome_ambient';
    this.scene.add(lavaGlow);
  }

  addCaveLighting() {
    // Schwaches bläuliches Kristall-Licht
    const crystalGlow = new THREE.PointLight(0x9370db, 0.3, 150);
    crystalGlow.position.set(0, 20, 0);
    crystalGlow.name = 'biome_ambient';
    this.scene.add(crystalGlow);
  }

  addIceLighting() {
    // Helles, kühles Licht
    const iceLight = new THREE.HemisphereLight(0xb0e0e6, 0xffffff, 0.7);
    iceLight.name = 'biome_ambient';
    this.scene.add(iceLight);
  }

  /**
   * Unterirdische Effekte
   */
  applyUndergroundEffects(biome) {
    // Sehr dunkle Umgebung
    this.scene.background = new THREE.Color(0x000000);

    // Sehr dichter Nebel
    this.scene.fog = new THREE.FogExp2(0x000000, 0.015);
  }

  /**
   * Lava-Effekte
   */
  applyLavaEffects(biome) {
    // TODO: Später - Lava-Fluss Partikel-System
    // Für jetzt: Nur Farbanpassungen
    console.log('  🌋 Lava effects applied');
  }

  /**
   * Smooth transition zwischen Biomes
   * @param {string} fromBiomeId - Current biome
   * @param {string} toBiomeId - Target biome
   */
  transitionToBiome(fromBiomeId, toBiomeId) {
    const from = this.biomes.get(fromBiomeId);
    const to = this.biomes.get(toBiomeId);

    if (!from || !to) return;

    console.log(`🎨 Transitioning: ${from.name} → ${to.name}`);

    // Smooth color transition (implementiere später mit GSAP oder ähnlich)
    // Für jetzt: Direkter Wechsel
    this.applyBiomeEnvironment(toBiomeId);
  }

  /**
   * Get biome at position (für Region-Streaming)
   * @param {THREE.Vector3} position - World position
   * @param {Object} regionData - Region data from regions.json
   * @returns {string} Biome ID
   */
  getBiomeAtPosition(position, regionData) {
    // Find which region the position is in
    for (const [regionId, region] of Object.entries(regionData.regions)) {
      const { bounds } = region;
      if (position.x >= bounds.minX && position.x <= bounds.maxX &&
          position.z >= bounds.minZ && position.z <= bounds.maxZ) {
        return region.biome;
      }
    }
    return 'forest';  // Default fallback
  }

  /**
   * Get biome config
   * @param {string} biomeId - Biome ID
   * @returns {Object} Biome config
   */
  getBiome(biomeId) {
    return this.biomes.get(biomeId);
  }

  /**
   * Get all biomes
   * @returns {Map} All biomes
   */
  getAllBiomes() {
    return this.biomes;
  }
}

export default BiomeSystem;
