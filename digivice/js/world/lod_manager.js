// 🎯 LOD MANAGER - Level of Detail Management für Performance-Optimierung
// Passt Mesh-Details basierend auf Kamera-Distanz an


class LODManager {
  constructor(scene, camera) {
    this.scene = scene;
    this.camera = camera;

    // LOD levels and their distances
    this.lodLevels = {
      high: { distance: 0, maxDistance: 100 },      // Full detail
      medium: { distance: 100, maxDistance: 300 },  // Reduced detail
      low: { distance: 300, maxDistance: 800 },     // Very low detail
      culled: { distance: 800, maxDistance: Infinity } // Not rendered
    };

    // Objects to manage
    this.managedObjects = new Map();  // uuid -> LOD config
    this.lodGroups = new Map();  // uuid -> THREE.LOD

    // Performance tracking
    this.stats = {
      totalObjects: 0,
      highDetail: 0,
      mediumDetail: 0,
      lowDetail: 0,
      culled: 0,
      lastUpdate: 0
    };

    // Update frequency (don't check every frame)
    this.updateInterval = 100;  // ms
    this.lastUpdateTime = 0;
  }

  /**
   * Create LOD group for a mesh
   * @param {THREE.Mesh} highDetailMesh - Full detail mesh
   * @param {Object} options - LOD options
   * @returns {THREE.LOD} LOD group
   */
  createLOD(highDetailMesh, options = {}) {
    const lod = new THREE.LOD();

    // Add high detail level
    lod.addLevel(highDetailMesh, this.lodLevels.high.distance);

    // Create medium detail version (reduce geometry)
    if (options.generateMedium !== false) {
      const mediumMesh = this.createReducedMesh(highDetailMesh, 0.5);
      lod.addLevel(mediumMesh, this.lodLevels.medium.distance);
    }

    // Create low detail version (simple geometry or billboard)
    if (options.generateLow !== false) {
      const lowMesh = this.createReducedMesh(highDetailMesh, 0.2);
      lod.addLevel(lowMesh, this.lodLevels.low.distance);
    }

    // Track this LOD group
    this.lodGroups.set(lod.uuid, {
      lod: lod,
      currentLevel: 0,
      options: options
    });

    this.stats.totalObjects++;

    return lod;
  }

  /**
   * Create reduced detail mesh
   * @param {THREE.Mesh} originalMesh
   * @param {number} factor - Reduction factor (0.0 - 1.0)
   * @returns {THREE.Mesh} Reduced mesh
   */
  createReducedMesh(originalMesh, factor) {
    // Simple reduction: use less detailed geometry
    const reducedMesh = originalMesh.clone();

    if (originalMesh.geometry) {
      // For now: just reuse geometry (later: implement real decimation)
      // TODO: Implement SimplifyModifier for geometry reduction
      reducedMesh.geometry = originalMesh.geometry.clone();
    }

    // Reduce shadow quality for low-detail meshes
    if (factor < 0.5) {
      reducedMesh.castShadow = false;
      reducedMesh.receiveShadow = false;
    }

    return reducedMesh;
  }

  /**
   * Create simple billboard for distant objects
   * @param {THREE.Mesh} mesh
   * @returns {THREE.Sprite} Billboard sprite
   */
  createBillboard(mesh) {
    // Create a simple sprite that always faces camera
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');

    // Draw simple representation
    ctx.fillStyle = '#8b4513';
    ctx.fillRect(0, 0, 64, 64);

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(material);

    return sprite;
  }

  /**
   * Add object to LOD management
   * @param {THREE.Object3D} object
   * @param {Object} config - LOD configuration
   */
  addObject(object, config = {}) {
    const lodConfig = {
      object: object,
      distances: config.distances || this.lodLevels,
      enableCulling: config.enableCulling !== false,
      currentLevel: 'high',
      visible: true
    };

    this.managedObjects.set(object.uuid, lodConfig);
    this.stats.totalObjects++;
  }

  /**
   * Remove object from LOD management
   * @param {THREE.Object3D} object
   */
  removeObject(object) {
    this.managedObjects.delete(object.uuid);
    this.lodGroups.delete(object.uuid);
    this.stats.totalObjects--;
  }

  /**
   * Update LOD for all managed objects
   */
  update() {
    const now = Date.now();

    // Throttle updates
    if (now - this.lastUpdateTime < this.updateInterval) {
      return;
    }

    this.lastUpdateTime = now;

    // Reset stats
    this.stats.highDetail = 0;
    this.stats.mediumDetail = 0;
    this.stats.lowDetail = 0;
    this.stats.culled = 0;

    const cameraPosition = this.camera.position;

    // Update THREE.LOD groups (automatic)
    for (const lodData of this.lodGroups.values()) {
      lodData.lod.update(this.camera);
    }

    // Update manual LOD objects
    for (const config of this.managedObjects.values()) {
      this.updateObjectLOD(config, cameraPosition);
    }

    this.stats.lastUpdate = now;
  }

  /**
   * Update LOD for single object
   */
  updateObjectLOD(config, cameraPosition) {
    const distance = config.object.position.distanceTo(cameraPosition);

    let newLevel = 'culled';

    if (distance < this.lodLevels.high.maxDistance) {
      newLevel = 'high';
      this.stats.highDetail++;
    } else if (distance < this.lodLevels.medium.maxDistance) {
      newLevel = 'medium';
      this.stats.mediumDetail++;
    } else if (distance < this.lodLevels.low.maxDistance) {
      newLevel = 'low';
      this.stats.lowDetail++;
    } else {
      this.stats.culled++;
    }

    // Apply culling
    if (config.enableCulling) {
      const shouldBeVisible = newLevel !== 'culled';
      if (config.visible !== shouldBeVisible) {
        config.object.visible = shouldBeVisible;
        config.visible = shouldBeVisible;
      }
    }

    config.currentLevel = newLevel;
  }

  /**
   * Set LOD distances
   * @param {Object} levels - Custom LOD levels
   */
  setLODLevels(levels) {
    this.lodLevels = {
      ...this.lodLevels,
      ...levels
    };
    console.log('🎯 LOD levels updated:', this.lodLevels);
  }

  /**
   * Enable/disable frustum culling for scene
   */
  enableFrustumCulling(enabled = true) {
    this.scene.traverse(obj => {
      if (obj.isMesh) {
        obj.frustumCulled = enabled;
      }
    });
    console.log(`🎯 Frustum culling ${enabled ? 'enabled' : 'disabled'}`);
  }

  /**
   * Optimize vegetation LOD (special handling)
   */
  optimizeVegetation(vegetationGroup) {
    console.log('🎯 Optimizing vegetation LOD...');

    vegetationGroup.traverse(obj => {
      if (obj.isMesh) {
        // Vegetation-specific LOD (simpler than buildings)
        const lod = new THREE.LOD();

        // High detail (close)
        lod.addLevel(obj.clone(), 0);

        // Medium detail (reduce geometry)
        const mediumGeometry = obj.geometry.clone();
        const mediumMesh = new THREE.Mesh(mediumGeometry, obj.material);
        mediumMesh.castShadow = false;  // No shadows at medium distance
        lod.addLevel(mediumMesh, 50);

        // Low detail (simple billboard)
        const billboard = this.createSimpleVegetationBillboard(obj);
        lod.addLevel(billboard, 150);

        // Replace original with LOD
        obj.parent.add(lod);
        lod.position.copy(obj.position);
        obj.parent.remove(obj);

        this.lodGroups.set(lod.uuid, {
          lod: lod,
          currentLevel: 0,
          type: 'vegetation'
        });
      }
    });

    console.log('  ✅ Vegetation LOD optimized');
  }

  /**
   * Create simple vegetation billboard
   */
  createSimpleVegetationBillboard(mesh) {
    const geometry = new THREE.PlaneGeometry(2, 2);
    const material = new THREE.MeshBasicMaterial({
      color: 0x228b22,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.8
    });
    const billboard = new THREE.Mesh(geometry, material);
    billboard.renderOrder = 999;  // Render last
    return billboard;
  }

  /**
   * Optimize city buildings LOD
   */
  optimizeCityBuildings(cityGroup) {
    console.log('🎯 Optimizing city buildings LOD...');

    cityGroup.traverse(obj => {
      if (obj.isMesh) {
        const lod = new THREE.LOD();

        // High detail
        lod.addLevel(obj.clone(), 0);

        // Medium detail
        const mediumMesh = this.createReducedMesh(obj, 0.5);
        lod.addLevel(mediumMesh, 100);

        // Low detail (very simple box)
        const lowGeometry = new THREE.BoxGeometry(5, 5, 5);
        const lowMaterial = new THREE.MeshBasicMaterial({ color: obj.material.color });
        const lowMesh = new THREE.Mesh(lowGeometry, lowMaterial);
        lod.addLevel(lowMesh, 300);

        // Replace
        obj.parent.add(lod);
        lod.position.copy(obj.position);
        obj.parent.remove(obj);

        this.lodGroups.set(lod.uuid, {
          lod: lod,
          currentLevel: 0,
          type: 'building'
        });
      }
    });

    console.log('  ✅ City buildings LOD optimized');
  }

  /**
   * Use instanced meshes for repeated objects (performance boost)
   * @param {Array<THREE.Mesh>} meshes - Meshes to instance
   * @returns {THREE.InstancedMesh} Instanced mesh
   */
  createInstancedMesh(meshes) {
    if (meshes.length === 0) return null;

    const referenceMesh = meshes[0];
    const instancedMesh = new THREE.InstancedMesh(
      referenceMesh.geometry,
      referenceMesh.material,
      meshes.length
    );

    const matrix = new THREE.Matrix4();

    meshes.forEach((mesh, i) => {
      matrix.setPosition(mesh.position);
      instancedMesh.setMatrixAt(i, matrix);
    });

    instancedMesh.instanceMatrix.needsUpdate = true;
    instancedMesh.castShadow = true;
    instancedMesh.receiveShadow = true;

    console.log(`🎯 Created instanced mesh with ${meshes.length} instances`);

    return instancedMesh;
  }

  /**
   * Batch similar vegetation into instanced meshes
   * @param {THREE.Group} vegetationGroup
   */
  batchVegetation(vegetationGroup) {
    console.log('🎯 Batching vegetation into instanced meshes...');

    const vegetationByType = new Map();

    // Group by geometry + material
    vegetationGroup.traverse(obj => {
      if (obj.isMesh) {
        const key = `${obj.geometry.uuid}_${obj.material.uuid}`;
        if (!vegetationByType.has(key)) {
          vegetationByType.set(key, []);
        }
        vegetationByType.get(key).push(obj);
      }
    });

    let totalBatched = 0;

    // Create instanced meshes
    for (const [key, meshes] of vegetationByType.entries()) {
      if (meshes.length > 10) {  // Only batch if >10 instances
        const instancedMesh = this.createInstancedMesh(meshes);

        if (instancedMesh) {
          vegetationGroup.add(instancedMesh);

          // Remove originals
          meshes.forEach(mesh => {
            if (mesh.parent) mesh.parent.remove(mesh);
          });

          totalBatched += meshes.length;
        }
      }
    }

    console.log(`  ✅ Batched ${totalBatched} vegetation items`);
  }

  /**
   * Get current LOD statistics
   */
  getStats() {
    return {
      ...this.stats,
      totalManaged: this.managedObjects.size,
      totalLODGroups: this.lodGroups.size,
      updateInterval: this.updateInterval
    };
  }

  /**
   * Debug: Visualize LOD levels with color coding
   */
  debugVisualizeLOD(enabled = true) {
    if (!enabled) {
      // Reset colors
      for (const config of this.managedObjects.values()) {
        if (config.object.material && config.object.material.emissive) {
          config.object.material.emissive.setHex(0x000000);
        }
      }
      return;
    }

    // Color code by LOD level
    const colors = {
      high: 0x00ff00,    // Green
      medium: 0xffff00,  // Yellow
      low: 0xff9900,     // Orange
      culled: 0xff0000   // Red (invisible)
    };

    for (const config of this.managedObjects.values()) {
      if (config.object.material && config.object.material.emissive) {
        config.object.material.emissive.setHex(colors[config.currentLevel] || 0x000000);
        config.object.material.emissiveIntensity = 0.3;
      }
    }

    console.log('🎯 LOD visualization enabled (Green=High, Yellow=Medium, Orange=Low, Red=Culled)');
  }

  /**
   * Set update interval (ms)
   */
  setUpdateInterval(interval) {
    this.updateInterval = Math.max(16, interval);  // Min 16ms (60fps)
    console.log(`🎯 LOD update interval set to ${this.updateInterval}ms`);
  }

  /**
   * Clear all LOD management
   */
  clear() {
    this.managedObjects.clear();
    this.lodGroups.clear();
    this.stats = {
      totalObjects: 0,
      highDetail: 0,
      mediumDetail: 0,
      lowDetail: 0,
      culled: 0,
      lastUpdate: 0
    };
    console.log('🎯 LOD manager cleared');
  }
}

// export default LODManager; // Converted to global
window.LODManager = LODManager;
