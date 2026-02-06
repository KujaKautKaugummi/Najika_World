// 📦 ASSET LOADER - Lädt 3D-Modelle (GLB, FBX) für World-System
// Verwaltet KayKit, Quaternius, JellySquish Assets


class AssetLoader {
  constructor() {
    // Use global loaders (available from CDN)
    this.gltfLoader = new THREE.GLTFLoader();

    // Cache für geladene Assets
    this.cache = new Map();

    // Asset-Pfade (Basis-URLs)
    this.paths = {
      kaykit: '/digivice/static/assets/kaykit/',
      quaternius: '/digivice/static/assets/quaternius/',
      jellysquish: '/digivice/static/assets/jellysquish/',
      misc: '/digivice/static/assets/misc/'
    };

    // Asset-Mapping (wird aus JSON geladen)
    this.assetMapping = null;

    // Loading statistics
    this.stats = {
      totalRequests: 0,
      loaded: 0,
      cached: 0,
      failed: 0,
      loadingTime: 0
    };

    console.log('📦 Asset Loader initialized');
  }

  /**
   * Lade Asset-Mapping JSON
   * @param {string} mappingPath - Pfad zu asset_mapping.json
   */
  async loadAssetMapping(mappingPath = '/data/asset_mapping.json') {
    try {
      const response = await fetch(mappingPath);
      if (!response.ok) throw new Error(`Asset mapping fetch failed: ${response.status}`);
      this.assetMapping = await response.json();
      console.log('📦 Asset mapping loaded');
      return true;
    } catch (error) {
      console.error('❌ Failed to load asset mapping:', error);
      this.assetMapping = {}; // Fallback empty mapping
      return false;
    }
  }

  /**
   * Lade ein 3D-Model (GLB oder FBX)
   * @param {string} assetPath - Pfad zum Asset (relativ zu assets/)
   * @param {Object} options - Optionen (scale, position, rotation)
   * @returns {Promise<THREE.Object3D>} Geladenes 3D-Objekt
   */
  async loadModel(assetPath, options = {}) {
    this.stats.totalRequests++;

    // Check cache
    if (this.cache.has(assetPath)) {
      this.stats.cached++;
      const cached = this.cache.get(assetPath);
      return this.applyOptions(cached.clone(), options);
    }

    const startTime = performance.now();

    try {
      let model;

      // Bestimme Loader anhand Extension
      if (assetPath.endsWith('.glb') || assetPath.endsWith('.gltf')) {
        model = await this.loadGLTF(assetPath);
      } else {
        throw new Error(`Unsupported format: ${assetPath}. Only GLB/GLTF supported.`);
      }

      // Cache das Model
      this.cache.set(assetPath, model.clone());

      // Stats
      const loadTime = performance.now() - startTime;
      this.stats.loaded++;
      this.stats.loadingTime += loadTime;

      console.log(`📦 Loaded: ${assetPath} (${loadTime.toFixed(0)}ms)`);

      return this.applyOptions(model, options);

    } catch (error) {
      this.stats.failed++;
      console.error(`❌ Failed to load: ${assetPath}`, error);

      // Return placeholder
      return this.createPlaceholder(options);
    }
  }

  /**
   * Lade GLTF/GLB Model
   */
  loadGLTF(path) {
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        path,
        (gltf) => {
          const model = gltf.scene;
          model.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          resolve(model);
        },
        undefined,
        reject
      );
    });
  }

  // FBX loading removed - only GLTF/GLB supported via CDN loader

  /**
   * Wende Optionen auf Model an
   */
  applyOptions(model, options) {
    if (options.scale) {
      if (typeof options.scale === 'number') {
        model.scale.setScalar(options.scale);
      } else {
        model.scale.set(options.scale.x, options.scale.y, options.scale.z);
      }
    }

    if (options.position) {
      model.position.set(options.position.x, options.position.y, options.position.z);
    }

    if (options.rotation) {
      model.rotation.set(options.rotation.x, options.rotation.y, options.rotation.z);
    }

    return model;
  }

  /**
   * Erstelle Placeholder (falls Model nicht geladen werden kann)
   */
  createPlaceholder(options = {}) {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({ color: 0xff00ff });
    const placeholder = new THREE.Mesh(geometry, material);

    return this.applyOptions(placeholder, options);
  }

  /**
   * Lade Asset basierend auf Biome und Typ
   * @param {string} biome - Biome ID (z.B. 'desert', 'forest')
   * @param {string} type - Asset Type (z.B. 'tree', 'rock', 'building')
   * @param {Object} options - Optionen
   */
  async loadBiomeAsset(biome, type, options = {}) {
    if (!this.assetMapping) {
      console.warn('⚠️ Asset mapping not loaded, using placeholder');
      return this.createPlaceholder(options);
    }

    const biomeAssets = this.assetMapping.biomes[biome];
    if (!biomeAssets) {
      console.warn(`⚠️ No assets defined for biome: ${biome}`);
      return this.createPlaceholder(options);
    }

    const assetInfo = biomeAssets[type];
    if (!assetInfo) {
      console.warn(`⚠️ No asset defined for ${biome}/${type}`);
      return this.createPlaceholder(options);
    }

    // Falls mehrere Varianten verfügbar, wähle zufällig
    let assetPath;
    if (Array.isArray(assetInfo)) {
      assetPath = assetInfo[Math.floor(Math.random() * assetInfo.length)];
    } else {
      assetPath = assetInfo;
    }

    // Lade das Asset
    return await this.loadModel(assetPath, options);
  }

  /**
   * Lade City-Building Asset
   * @param {string} buildingType - Building type (z.B. 'house', 'inn', 'forge')
   */
  async loadCityBuilding(buildingType, options = {}) {
    if (!this.assetMapping) {
      return this.createPlaceholder(options);
    }

    const buildingAssets = this.assetMapping.buildings[buildingType];
    if (!buildingAssets) {
      console.warn(`⚠️ No building asset for: ${buildingType}`);
      return this.createPlaceholder(options);
    }

    let assetPath;
    if (Array.isArray(buildingAssets)) {
      assetPath = buildingAssets[Math.floor(Math.random() * buildingAssets.length)];
    } else {
      assetPath = buildingAssets;
    }

    return await this.loadModel(assetPath, options);
  }

  /**
   * Batch-Load mehrerer Assets (parallel)
   * @param {Array<string>} assetPaths - Array von Asset-Pfaden
   * @returns {Promise<Array<THREE.Object3D>>} Array von geladenen Models
   */
  async loadBatch(assetPaths, options = {}) {
    console.log(`📦 Batch loading ${assetPaths.length} assets...`);

    const startTime = performance.now();

    const promises = assetPaths.map(path => this.loadModel(path, options));
    const models = await Promise.all(promises);

    const totalTime = performance.now() - startTime;
    console.log(`✅ Batch loaded ${models.length} assets in ${totalTime.toFixed(0)}ms`);

    return models;
  }

  /**
   * Preload häufig genutzte Assets
   * @param {Array<string>} assetPaths - Assets zum Vorabladen
   */
  async preloadAssets(assetPaths) {
    console.log(`📦 Preloading ${assetPaths.length} assets...`);

    for (const path of assetPaths) {
      await this.loadModel(path);
    }

    console.log('✅ Preload complete');
  }

  /**
   * Preload Assets für ein spezifisches Biome
   */
  async preloadBiomeAssets(biome) {
    if (!this.assetMapping) {
      console.warn('⚠️ Asset mapping not loaded');
      return;
    }

    const biomeAssets = this.assetMapping.biomes[biome];
    if (!biomeAssets) return;

    const assetPaths = [];

    // Sammle alle Asset-Pfade für dieses Biome
    for (const assetInfo of Object.values(biomeAssets)) {
      if (Array.isArray(assetInfo)) {
        assetPaths.push(...assetInfo);
      } else {
        assetPaths.push(assetInfo);
      }
    }

    console.log(`📦 Preloading ${assetPaths.length} assets for biome: ${biome}`);
    await this.preloadAssets(assetPaths);
  }

  /**
   * Lösche Cache (für Memory Management)
   */
  clearCache() {
    for (const model of this.cache.values()) {
      model.traverse((child) => {
        if (child.isMesh) {
          if (child.geometry) child.geometry.dispose();
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(mat => mat.dispose());
            } else {
              child.material.dispose();
            }
          }
        }
      });
    }

    this.cache.clear();
    console.log('📦 Asset cache cleared');
  }

  /**
   * Entferne spezifisches Asset aus Cache
   */
  uncache(assetPath) {
    if (this.cache.has(assetPath)) {
      const model = this.cache.get(assetPath);
      model.traverse((child) => {
        if (child.isMesh) {
          if (child.geometry) child.geometry.dispose();
          if (child.material) child.material.dispose();
        }
      });
      this.cache.delete(assetPath);
      console.log(`📦 Uncached: ${assetPath}`);
    }
  }

  /**
   * Get loading statistics
   */
  getStats() {
    return {
      ...this.stats,
      cacheSize: this.cache.size,
      avgLoadTime: this.stats.loaded > 0 ? (this.stats.loadingTime / this.stats.loaded).toFixed(2) : 0,
      successRate: this.stats.totalRequests > 0
        ? ((this.stats.loaded / this.stats.totalRequests) * 100).toFixed(1)
        : 0
    };
  }

  /**
   * Log statistics
   */
  logStats() {
    const stats = this.getStats();
    console.log('📊 === ASSET LOADER STATS ===');
    console.log(`Total Requests: ${stats.totalRequests}`);
    console.log(`Loaded: ${stats.loaded}`);
    console.log(`From Cache: ${stats.cached}`);
    console.log(`Failed: ${stats.failed}`);
    console.log(`Cache Size: ${stats.cacheSize}`);
    console.log(`Avg Load Time: ${stats.avgLoadTime}ms`);
    console.log(`Success Rate: ${stats.successRate}%`);
    console.log('============================');
  }

  /**
   * List alle gecachten Assets
   */
  listCached() {
    console.log('📦 Cached Assets:');
    for (const path of this.cache.keys()) {
      console.log(`  - ${path}`);
    }
  }
}

// export default AssetLoader; // Converted to global
window.AssetLoader = AssetLoader;
