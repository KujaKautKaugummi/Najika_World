// 🌿 VEGETATION SYSTEM - Verwaltet Vegetation-Placement pro Biome
// Platziert Bäume, Pflanzen, Mushrooms, Cacti basierend auf Biome-Daten

// ============================================================================
// INSTANCED MESH INFRASTRUCTURE (Performance Optimization)
// ============================================================================

/**
 * SPATIAL GRID - Fast proximity queries
 * Divides world into grid cells for O(1) spatial lookups
 */
class SpatialGrid {
  constructor(cellSize = 50) {
    this.cellSize = cellSize;
    this.grid = new Map(); // cellKey → Set<instanceId>
  }

  getCellKey(x, z) {
    const cx = Math.floor(x / this.cellSize);
    const cz = Math.floor(z / this.cellSize);
    return `${cx},${cz}`;
  }

  insert(instanceId, position) {
    const key = this.getCellKey(position.x, position.z);
    if (!this.grid.has(key)) {
      this.grid.set(key, new Set());
    }
    this.grid.get(key).add(instanceId);
  }

  remove(instanceId, position) {
    const key = this.getCellKey(position.x, position.z);
    const cell = this.grid.get(key);
    if (cell) {
      cell.delete(instanceId);
      if (cell.size === 0) {
        this.grid.delete(key);
      }
    }
  }

  queryRadius(position, radius) {
    const results = [];
    const minCellX = Math.floor((position.x - radius) / this.cellSize);
    const maxCellX = Math.floor((position.x + radius) / this.cellSize);
    const minCellZ = Math.floor((position.z - radius) / this.cellSize);
    const maxCellZ = Math.floor((position.z + radius) / this.cellSize);

    for (let cx = minCellX; cx <= maxCellX; cx++) {
      for (let cz = minCellZ; cz <= maxCellZ; cz++) {
        const key = `${cx},${cz}`;
        const cell = this.grid.get(key);
        if (cell) {
          results.push(...cell);
        }
      }
    }
    return results;
  }

  clear() {
    this.grid.clear();
  }
}

/**
 * INSTANCE METADATA - Stores per-instance data
 */
class InstanceMetadata {
  constructor(instanceId, type, position, rotation, scale) {
    this.id = instanceId;
    this.type = type;
    this.position = position.clone();
    this.rotation = rotation;
    this.scale = scale;
    this.visible = true;
  }
}

/**
 * INSTANCED MESH DATA - Manages one instanced mesh (one vegetation type)
 */
class InstancedMeshData {
  constructor(geometry, material, maxInstances) {
    this.mesh = new THREE.InstancedMesh(geometry, material, maxInstances);
    this.count = 0; // Current active count
    this.maxCount = maxInstances;

    // Visibility tracking (for dynamic removal)
    this.visibilityArray = new Float32Array(maxInstances);
    this.visibilityArray.fill(1.0); // All visible by default

    // Free slots (for reuse after removal)
    this.freeSlots = [];

    // Instance ID mapping
    this.indexToId = new Map(); // instanceIndex → instanceId
    this.idToIndex = new Map(); // instanceId → instanceIndex
  }

  allocateInstance(instanceId) {
    let index;
    if (this.freeSlots.length > 0) {
      // Reuse freed slot
      index = this.freeSlots.pop();
    } else if (this.count < this.maxCount) {
      // Allocate new slot
      index = this.count++;
    } else {
      // Buffer full
      return null;
    }

    this.indexToId.set(index, instanceId);
    this.idToIndex.set(instanceId, index);
    this.visibilityArray[index] = 1.0; // Visible
    return index;
  }

  freeInstance(instanceId) {
    const index = this.idToIndex.get(instanceId);
    if (index !== undefined) {
      this.visibilityArray[index] = 0.0; // Hide
      this.freeSlots.push(index);
      this.indexToId.delete(index);
      this.idToIndex.delete(instanceId);
      return true;
    }
    return false;
  }

  dispose() {
    this.mesh.geometry.dispose();
    if (Array.isArray(this.mesh.material)) {
      this.mesh.material.forEach(m => m.dispose());
    } else {
      this.mesh.material.dispose();
    }
  }
}

/**
 * REGION INSTANCED VEGETATION - Manages all instanced meshes for one region
 */
class RegionInstancedVegetation {
  constructor(regionId) {
    this.regionId = regionId;

    // Map<vegetationType, InstancedMeshData>
    this.instancedMeshes = new Map();

    // Spatial index for fast queries
    this.spatialGrid = new SpatialGrid(50);

    // Instance metadata tracking
    // Map<instanceId, InstanceMetadata>
    this.instanceMetadata = new Map();

    this.nextInstanceId = 0;
  }

  dispose() {
    // Dispose all instanced meshes
    for (const instancedMeshData of this.instancedMeshes.values()) {
      instancedMeshData.dispose();
    }
    this.instancedMeshes.clear();
    this.instanceMetadata.clear();
    this.spatialGrid.clear();
  }
}

// ============================================================================
// VEGETATION SYSTEM (Main Class)
// ============================================================================

class VegetationSystem {
  constructor(scene, terrainGenerator) {
    this.scene = scene;
    this.terrainGenerator = terrainGenerator;

    // Legacy implementation (kept for compatibility during migration)
    this.vegetationGroups = new Map();  // Per-region vegetation groups
    this.vegetationTemplates = new Map();  // Reusable geometries
    this.instancedMeshes = new Map();  // For performance optimization (unused)

    // NEW: Instanced mesh implementation
    this.instancedRegions = new Map();  // regionId → RegionInstancedVegetation
    this.useInstancing = true;  // Feature flag (set to false to use legacy)
    this.bufferOverhead = 1.3;  // Allocate 30% extra for dynamic spawning

    console.log('[VEGETATION SYSTEM] 🌿 Initialized (Instancing: ' + this.useInstancing + ')');
  }

  /**
   * Initialisiere Vegetation-Templates (Placeholder geometries)
   * TODO: Later replace with KayKit/Quaternius models
   */
  initializeTemplates() {
    console.log('🌿 Initializing vegetation templates...');

    // TREES
    this.createTreeTemplate('tree', { trunkHeight: 8, trunkRadius: 0.5, crownRadius: 3 });
    this.createTreeTemplate('palm_tree', { trunkHeight: 10, trunkRadius: 0.3, crownRadius: 2 });
    this.createTreeTemplate('frozen_tree', { trunkHeight: 6, trunkRadius: 0.4, crownRadius: 2 });
    this.createTreeTemplate('dead_tree', { trunkHeight: 5, trunkRadius: 0.3, crownRadius: 1 });

    // MUSHROOMS
    this.createMushroomTemplate('mushroom', { stemHeight: 1, capRadius: 1, color: 0xcd5c5c });
    this.createMushroomTemplate('glowing_mushroom', { stemHeight: 2, capRadius: 1.5, color: 0x9370db, glowing: true });

    // PLANTS
    this.createPlantTemplate('bush', { radius: 1, height: 1.5, color: 0x228b22 });
    this.createPlantTemplate('fern', { radius: 0.8, height: 1, color: 0x2e8b57 });
    this.createPlantTemplate('cactus', { height: 3, radius: 0.5, color: 0x6b8e23 });
    this.createPlantTemplate('dry_bush', { radius: 0.8, height: 1, color: 0x8b7355 });
    this.createPlantTemplate('beach_grass', { radius: 0.3, height: 1.5, color: 0x9acd32 });
    this.createPlantTemplate('swamp_grass', { radius: 0.4, height: 1.2, color: 0x556b2f });
    this.createPlantTemplate('tough_grass', { radius: 0.3, height: 1, color: 0x8b7355 });
    this.createPlantTemplate('mountain_grass', { radius: 0.3, height: 0.8, color: 0x6b8e23 });
    this.createPlantTemplate('alpine_flower', { radius: 0.2, height: 0.5, color: 0xff69b4 });
    this.createPlantTemplate('highland_flower', { radius: 0.3, height: 0.6, color: 0xdda0dd });
    this.createPlantTemplate('seaweed', { radius: 0.5, height: 2, color: 0x2e8b57 });
    this.createPlantTemplate('poison_plant', { radius: 0.6, height: 1, color: 0x9370db });
    this.createPlantTemplate('vines', { radius: 0.2, height: 3, color: 0x228b22 });
    this.createPlantTemplate('snow_bush', { radius: 0.7, height: 1, color: 0xf0f8ff });
    this.createPlantTemplate('fire_flower', { radius: 0.4, height: 0.8, color: 0xff4500 });
    this.createPlantTemplate('lava_moss', { radius: 0.5, height: 0.3, color: 0x8b4513 });
    this.createPlantTemplate('cave_moss', { radius: 0.4, height: 0.2, color: 0x2f4f4f });

    // SPECIAL
    this.createCrystalTemplate('crystal', { height: 4, radius: 0.8, color: 0x9370db });
    this.createCrystalTemplate('ice_crystal', { height: 3, radius: 0.6, color: 0xb0e0e6 });
    this.createRockTemplate('volcanic_rock', { radius: 2, height: 1.5, color: 0x8b4513 });
    this.createTotemTemplate('totem', { height: 5, radius: 0.5 });

    console.log(`🌿 Templates initialized: ${this.vegetationTemplates.size} types`);
  }

  /**
   * Tree Template (Cylinder trunk + Sphere crown)
   */
  createTreeTemplate(type, { trunkHeight, trunkRadius, crownRadius }) {
    const group = new THREE.Group();

    // Trunk
    const trunkGeometry = new THREE.CylinderGeometry(trunkRadius, trunkRadius * 1.2, trunkHeight, 8);
    const trunkMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513, roughness: 0.9 });
    const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
    trunk.position.y = trunkHeight / 2;
    trunk.castShadow = true;
    group.add(trunk);

    // Crown (Foliage)
    const crownGeometry = new THREE.SphereGeometry(crownRadius, 8, 8);
    const crownColor = type === 'dead_tree' ? 0x3d2817 : (type === 'frozen_tree' ? 0xe0ffff : 0x228b22);
    const crownMaterial = new THREE.MeshStandardMaterial({ color: crownColor, roughness: 0.8 });
    const crown = new THREE.Mesh(crownGeometry, crownMaterial);
    crown.position.y = trunkHeight + crownRadius * 0.5;
    crown.castShadow = true;
    group.add(crown);

    this.vegetationTemplates.set(type, group);
  }

  /**
   * Mushroom Template
   */
  createMushroomTemplate(type, { stemHeight, capRadius, color, glowing = false }) {
    const group = new THREE.Group();

    // Stem
    const stemGeometry = new THREE.CylinderGeometry(capRadius * 0.2, capRadius * 0.25, stemHeight, 8);
    const stemMaterial = new THREE.MeshStandardMaterial({ color: 0xfaf0e6, roughness: 0.6 });
    const stem = new THREE.Mesh(stemGeometry, stemMaterial);
    stem.position.y = stemHeight / 2;
    group.add(stem);

    // Cap
    const capGeometry = new THREE.SphereGeometry(capRadius, 8, 8, 0, Math.PI * 2, 0, Math.PI / 2);
    const capMaterial = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.5,
      emissive: glowing ? color : 0x000000,
      emissiveIntensity: glowing ? 0.3 : 0
    });
    const cap = new THREE.Mesh(capGeometry, capMaterial);
    cap.position.y = stemHeight + capRadius * 0.3;
    cap.rotation.x = Math.PI;
    group.add(cap);

    this.vegetationTemplates.set(type, group);
  }

  /**
   * Plant Template (Simple sphere or cone)
   */
  createPlantTemplate(type, { radius, height, color }) {
    const group = new THREE.Group();

    const geometry = type === 'cactus'
      ? new THREE.CylinderGeometry(radius, radius * 0.8, height, 8)
      : new THREE.SphereGeometry(radius, 6, 6);

    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: type === 'cactus' ? 0.9 : 0.7
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.y = type === 'cactus' ? height / 2 : radius;
    mesh.castShadow = true;
    group.add(mesh);

    this.vegetationTemplates.set(type, group);
  }

  /**
   * Crystal Template
   */
  createCrystalTemplate(type, { height, radius, color }) {
    const group = new THREE.Group();

    const geometry = new THREE.ConeGeometry(radius, height, 6);
    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.2,
      metalness: 0.3,
      emissive: color,
      emissiveIntensity: 0.2,
      transparent: true,
      opacity: 0.8
    });

    const crystal = new THREE.Mesh(geometry, material);
    crystal.position.y = height / 2;
    crystal.rotation.y = Math.random() * Math.PI * 2;
    crystal.castShadow = true;
    group.add(crystal);

    this.vegetationTemplates.set(type, group);
  }

  /**
   * Rock Template
   */
  createRockTemplate(type, { radius, height, color }) {
    const group = new THREE.Group();

    const geometry = new THREE.DodecahedronGeometry(radius);
    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.9,
      metalness: 0.1
    });

    const rock = new THREE.Mesh(geometry, material);
    rock.position.y = height / 2;
    rock.rotation.set(
      Math.random() * Math.PI,
      Math.random() * Math.PI,
      Math.random() * Math.PI
    );
    rock.castShadow = true;
    group.add(rock);

    this.vegetationTemplates.set(type, group);
  }

  /**
   * Totem Template (Highland)
   */
  createTotemTemplate(type, { height, radius }) {
    const group = new THREE.Group();

    // Base
    const baseGeometry = new THREE.CylinderGeometry(radius * 1.5, radius * 1.5, height * 0.2, 8);
    const baseMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const base = new THREE.Mesh(baseGeometry, baseMaterial);
    base.position.y = height * 0.1;
    group.add(base);

    // Pole
    const poleGeometry = new THREE.CylinderGeometry(radius, radius, height * 0.8, 4);
    const poleMaterial = new THREE.MeshStandardMaterial({ color: 0x654321 });
    const pole = new THREE.Mesh(poleGeometry, poleMaterial);
    pole.position.y = height * 0.5;
    pole.castShadow = true;
    group.add(pole);

    this.vegetationTemplates.set(type, group);
  }

  /**
   * Populate Region mit Vegetation (Wrapper with feature flag)
   * @param {string} regionId - Region ID
   * @param {Object} regionData - Region data from regions.json
   * @param {Object} biomeData - Biome data from biomes.json
   */
  populateRegion(regionId, regionData, biomeData) {
    if (this.useInstancing) {
      return this.populateRegionInstanced(regionId, regionData, biomeData);
    } else {
      return this.populateRegionLegacy(regionId, regionData, biomeData);
    }
  }

  /**
   * Populate Region mit Vegetation (LEGACY - individual meshes)
   * @param {string} regionId - Region ID
   * @param {Object} regionData - Region data from regions.json
   * @param {Object} biomeData - Biome data from biomes.json
   */
  populateRegionLegacy(regionId, regionData, biomeData) {
    console.log(`🌿 Populating vegetation: ${regionData.name}`);

    const biome = biomeData.biomes[regionData.biome];
    if (!biome || !biome.vegetation) {
      console.warn(`  ⚠️ No vegetation config for ${regionData.biome}`);
      return;
    }

    const { types, density } = biome.vegetation;
    const { bounds } = regionData;

    // Create group for this region's vegetation
    const vegetationGroup = new THREE.Group();
    vegetationGroup.name = `vegetation_${regionId}`;

    // Calculate number of vegetation items based on area and density
    const width = bounds.maxX - bounds.minX;
    const height = bounds.maxZ - bounds.minZ;
    const area = width * height;
    const vegetationCount = Math.floor(area * density);

    console.log(`  📊 Area: ${area}, Density: ${density}, Count: ${vegetationCount}`);

    // Place vegetation randomly within bounds
    for (let i = 0; i < vegetationCount; i++) {
      const x = bounds.minX + Math.random() * width;
      const z = bounds.minZ + Math.random() * height;

      // Get terrain height at this position
      const y = this.terrainGenerator.getHeightAt(regionId, x, z);

      // Skip if underwater or too steep
      if (y < 0.5 || this.isPositionTooSteep(regionId, x, z)) continue;

      // Select random vegetation type from biome's types
      const type = types[Math.floor(Math.random() * types.length)];

      // Create vegetation instance
      const vegetation = this.createVegetationInstance(type, x, y, z);
      if (vegetation) {
        vegetationGroup.add(vegetation);
      }
    }

    console.log(`  ✅ Placed ${vegetationGroup.children.length} vegetation items`);

    this.vegetationGroups.set(regionId, vegetationGroup);
    this.scene.add(vegetationGroup);
  }

  /**
   * Create single vegetation instance
   */
  createVegetationInstance(type, x, y, z) {
    const template = this.vegetationTemplates.get(type);
    if (!template) {
      console.warn(`  ⚠️ Template not found: ${type}`);
      return null;
    }

    const instance = template.clone();
    instance.position.set(x, y, z);

    // Random rotation
    instance.rotation.y = Math.random() * Math.PI * 2;

    // Random scale variation (±20%)
    const scaleVariation = 0.8 + Math.random() * 0.4;
    instance.scale.multiplyScalar(scaleVariation);

    return instance;
  }

  /**
   * Check if position is too steep for vegetation
   */
  isPositionTooSteep(regionId, x, z) {
    const sampleDist = 2;
    const h1 = this.terrainGenerator.getHeightAt(regionId, x, z);
    const h2 = this.terrainGenerator.getHeightAt(regionId, x + sampleDist, z);
    const h3 = this.terrainGenerator.getHeightAt(regionId, x, z + sampleDist);

    const slope = Math.max(
      Math.abs(h2 - h1) / sampleDist,
      Math.abs(h3 - h1) / sampleDist
    );

    return slope > 0.5;  // Too steep if slope > 50%
  }

  /**
   * Remove vegetation for a region (Wrapper with feature flag)
   */
  removeRegionVegetation(regionId) {
    if (this.useInstancing) {
      return this.removeRegionVegetationInstanced(regionId);
    } else {
      return this.removeRegionVegetationLegacy(regionId);
    }
  }

  /**
   * Remove vegetation for a region (LEGACY)
   */
  removeRegionVegetationLegacy(regionId) {
    const vegetationGroup = this.vegetationGroups.get(regionId);
    if (vegetationGroup) {
      this.scene.remove(vegetationGroup);
      vegetationGroup.clear();
      this.vegetationGroups.delete(regionId);
      console.log(`🌿 Removed vegetation: ${regionId}`);
    }
  }

  /**
   * Clear all vegetation
   */
  clearAllVegetation() {
    for (const [regionId, group] of this.vegetationGroups.entries()) {
      this.scene.remove(group);
      group.clear();
    }
    this.vegetationGroups.clear();
    console.log('🌿 All vegetation cleared');
  }

  /**
   * Update vegetation (for LOD, culling, etc.)
   */
  update(cameraPosition) {
    // Implement LOD switching based on distance
    for (const [regionId, group] of this.vegetationGroups.entries()) {
      const distance = group.position.distanceTo(cameraPosition);

      // LOD levels:
      // < 500: High detail (original meshes)
      // 500-1500: Medium detail (simplified meshes)
      // 1500-3000: Low detail (billboards/impostors)
      // > 3000: Hidden

      if (distance > 3000) {
        group.visible = false;
      } else {
        group.visible = true;

        // Apply LOD to each vegetation item
        group.children.forEach(vegetation => {
          if (distance < 500) {
            // High detail - show all geometry
            vegetation.traverse(child => {
              if (child.isMesh) {
                child.visible = true;
              }
            });
            vegetation.userData.currentLOD = 'high';
          } else if (distance < 1500) {
            // Medium detail - simplify some geometry
            vegetation.traverse(child => {
              if (child.isMesh) {
                // Hide smaller details but keep main structure
                child.visible = child.geometry.parameters?.radius > 0.3 ||
                               child.geometry.parameters?.height > 0.5;
              }
            });
            vegetation.userData.currentLOD = 'medium';
          } else {
            // Low detail - show only as simple billboard
            this.convertToBillboard(vegetation);
            vegetation.userData.currentLOD = 'low';
          }
        });
      }
    }

    // Implement frustum culling for performance
    this.performFrustumCulling(cameraPosition);
  }

  /**
   * Convert vegetation to billboard for distant LOD
   */
  convertToBillboard(vegetation) {
    if (vegetation.userData.billboard) {
      // Already converted, just make sure billboard is visible
      vegetation.userData.billboard.visible = true;
      vegetation.children.forEach(child => {
        if (!child.isSprite) child.visible = false;
      });
      return;
    }

    // Create billboard texture from vegetation
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');

    // Simple colored square as billboard
    ctx.fillStyle = '#228b22'; // Green color for vegetation
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({
      map: texture,
      transparent: true
    });
    const billboard = new THREE.Sprite(spriteMaterial);
    billboard.scale.set(2, 2, 1);

    vegetation.add(billboard);
    vegetation.userData.billboard = billboard;

    // Hide original meshes
    vegetation.children.forEach(child => {
      if (!child.isSprite) child.visible = false;
    });
  }

  /**
   * Perform frustum culling
   */
  performFrustumCulling(cameraPosition) {
    // Get camera frustum
    const frustum = new THREE.Frustum();
    const matrix = new THREE.Matrix4();

    if (window.camera) {
      matrix.multiplyMatrices(
        window.camera.projectionMatrix,
        window.camera.matrixWorldInverse
      );
      frustum.setFromProjectionMatrix(matrix);

      // Check each vegetation group
      for (const group of this.vegetationGroups.values()) {
        if (!group.visible) continue;

        // Check if group bounding box intersects frustum
        const boundingBox = new THREE.Box3().setFromObject(group);
        const inFrustum = frustum.intersectsBox(boundingBox);

        // Hide if outside frustum
        if (!inFrustum) {
          group.visible = false;
        }
      }
    }
  }

  /**
   * Batch vegetation using InstancedMesh for performance
   */
  batchVegetation() {
    console.log('🌿 Batching vegetation with InstancedMesh...');

    let batchedCount = 0;

    // Group vegetation by type
    const vegetationByType = new Map();

    for (const [regionId, group] of this.vegetationGroups.entries()) {
      group.children.forEach(vegetation => {
        const type = vegetation.userData?.type || 'unknown';

        if (!vegetationByType.has(type)) {
          vegetationByType.set(type, []);
        }

        vegetationByType.get(type).push({
          regionId,
          vegetation,
          position: vegetation.position.clone(),
          rotation: vegetation.rotation.clone(),
          scale: vegetation.scale.clone()
        });
      });
    }

    // Create InstancedMesh for each type
    for (const [type, instances] of vegetationByType.entries()) {
      if (instances.length < 10) continue; // Only batch if enough instances

      const template = this.vegetationTemplates.get(type);
      if (!template || !template.children[0]) continue;

      const geometry = template.children[0].geometry;
      const material = template.children[0].material;

      // Create InstancedMesh
      const instancedMesh = new THREE.InstancedMesh(
        geometry,
        material,
        instances.length
      );

      const matrix = new THREE.Matrix4();
      const dummy = new THREE.Object3D();

      // Set transform for each instance
      instances.forEach((instance, i) => {
        dummy.position.copy(instance.position);
        dummy.rotation.copy(instance.rotation);
        dummy.scale.copy(instance.scale);
        dummy.updateMatrix();
        instancedMesh.setMatrixAt(i, dummy.matrix);

        // Remove original mesh
        const regionGroup = this.vegetationGroups.get(instance.regionId);
        if (regionGroup) {
          regionGroup.remove(instance.vegetation);
        }
      });

      instancedMesh.instanceMatrix.needsUpdate = true;
      instancedMesh.castShadow = true;
      instancedMesh.receiveShadow = true;
      instancedMesh.name = `instanced_${type}`;

      // Add to first region group (or create new batched group)
      if (this.vegetationGroups.size > 0) {
        const firstGroup = this.vegetationGroups.values().next().value;
        firstGroup.add(instancedMesh);
      }

      this.instancedMeshes.set(type, instancedMesh);
      batchedCount += instances.length;
    }

    console.log(`  ✅ Batched ${batchedCount} vegetation items into ${this.instancedMeshes.size} InstancedMeshes`);
  }

  /**
   * Get vegetation at position (Wrapper with feature flag)
   * @param {THREE.Vector3} position
   * @param {number} radius
   * @returns {Array<THREE.Object3D|Object>} Nearby vegetation
   */
  getVegetationNear(position, radius = 5) {
    if (this.useInstancing) {
      return this.getVegetationNearInstanced(position, radius);
    } else {
      return this.getVegetationNearLegacy(position, radius);
    }
  }

  /**
   * Get vegetation at position (LEGACY)
   * @param {THREE.Vector3} position
   * @param {number} radius
   * @returns {Array<THREE.Object3D>} Nearby vegetation
   */
  getVegetationNearLegacy(position, radius = 5) {
    const nearby = [];

    for (const group of this.vegetationGroups.values()) {
      for (const vegetation of group.children) {
        const dist = vegetation.position.distanceTo(position);
        if (dist <= radius) {
          nearby.push(vegetation);
        }
      }
    }

    return nearby;
  }

  /**
   * Remove vegetation at position (Wrapper with feature flag)
   */
  removeVegetationAt(position, radius = 2) {
    if (this.useInstancing) {
      return this.removeVegetationAtInstanced(position, radius);
    } else {
      return this.removeVegetationAtLegacy(position, radius);
    }
  }

  /**
   * Remove vegetation at position (LEGACY)
   */
  removeVegetationAtLegacy(position, radius = 2) {
    let removedCount = 0;

    for (const group of this.vegetationGroups.values()) {
      const toRemove = [];

      for (const vegetation of group.children) {
        const dist = vegetation.position.distanceTo(position);
        if (dist <= radius) {
          toRemove.push(vegetation);
        }
      }

      toRemove.forEach(v => {
        group.remove(v);
        removedCount++;
      });
    }

    if (removedCount > 0) {
      console.log(`🌿 Removed ${removedCount} vegetation items`);
    }

    return removedCount;
  }

  /**
   * Spawn vegetation at position (Wrapper with feature flag)
   */
  spawnVegetationAt(type, position) {
    if (this.useInstancing) {
      return this.spawnVegetationAtInstanced(type, position);
    } else {
      return this.spawnVegetationAtLegacy(type, position);
    }
  }

  /**
   * Spawn vegetation at position (LEGACY)
   */
  spawnVegetationAtLegacy(type, position) {
    // Find which region this position belongs to
    for (const [regionId, group] of this.vegetationGroups.entries()) {
      // Simple bounds check (TODO: proper region lookup)
      const vegetation = this.createVegetationInstance(
        type,
        position.x,
        position.y,
        position.z
      );

      if (vegetation) {
        group.add(vegetation);
        console.log(`🌿 Spawned ${type} at (${position.x.toFixed(0)}, ${position.z.toFixed(0)})`);
        return vegetation;
      }
    }

    return null;
  }

  /**
   * Get statistics
   */
  getStats() {
    let totalVegetation = 0;
    for (const group of this.vegetationGroups.values()) {
      totalVegetation += group.children.length;
    }

    return {
      regionsLoaded: this.vegetationGroups.size,
      totalVegetation: totalVegetation,
      templatesLoaded: this.vegetationTemplates.size
    };
  }

  // ========================================================================
  // INSTANCED MESH IMPLEMENTATION (New Performance-Optimized Methods)
  // ========================================================================

  /**
   * Populate Region with INSTANCED vegetation (Performance-optimized)
   */
  populateRegionInstanced(regionId, regionData, biomeData) {
    console.log(`🌿 Populating vegetation (INSTANCED): ${regionData.name}`);

    const biome = biomeData.biomes[regionData.biome];
    if (!biome || !biome.vegetation) {
      console.warn(`  ⚠️ No vegetation config for ${regionData.biome}`);
      return;
    }

    const { types, density } = biome.vegetation;
    const { bounds } = regionData;

    // Create instanced vegetation manager for region
    const regionInstanced = new RegionInstancedVegetation(regionId);
    this.instancedRegions.set(regionId, regionInstanced);

    // Group vegetation by type DURING generation
    const vegetationByType = new Map();

    // Calculate and pre-generate positions
    const width = bounds.maxX - bounds.minX;
    const height = bounds.maxZ - bounds.minZ;
    const area = width * height;
    const vegetationCount = Math.floor(area * density);

    for (let i = 0; i < vegetationCount; i++) {
      const x = bounds.minX + Math.random() * width;
      const z = bounds.minZ + Math.random() * height;
      const y = this.terrainGenerator.getHeightAt(regionId, x, z);

      if (y < 0.5 || this.isPositionTooSteep(regionId, x, z)) continue;

      const type = types[Math.floor(Math.random() * types.length)];

      if (!vegetationByType.has(type)) {
        vegetationByType.set(type, []);
      }

      vegetationByType.get(type).push({
        position: new THREE.Vector3(x, y, z),
        rotation: Math.random() * Math.PI * 2,
        scale: 0.8 + Math.random() * 0.4
      });
    }

    // Create instanced mesh for each type
    let totalPlaced = 0;
    for (const [type, instances] of vegetationByType.entries()) {
      this.createInstancedVegetationGroup(
        regionId,
        regionInstanced,
        type,
        instances
      );
      totalPlaced += instances.length;
    }

    console.log(`  ✅ Placed ${totalPlaced} vegetation items (${regionInstanced.instancedMeshes.size} instanced meshes)`);
  }

  /**
   * Create instanced mesh group for one vegetation type
   */
  createInstancedVegetationGroup(regionId, regionInstanced, type, instances) {
    const template = this.vegetationTemplates.get(type);
    if (!template) {
      console.warn(`  ⚠️ Template not found: ${type}`);
      return;
    }

    // Calculate buffer size with overhead for dynamic spawning
    const bufferSize = Math.ceil(instances.length * this.bufferOverhead);

    // Extract geometry and material from template
    let geometry, material;
    template.traverse(obj => {
      if (obj.isMesh && !geometry) {
        geometry = obj.geometry;
        material = obj.material.clone(); // Clone to avoid shared materials
      }
    });

    if (!geometry || !material) {
      console.warn(`  ⚠️ Cannot extract geometry/material from template: ${type}`);
      return;
    }

    // Create instanced mesh data
    const instancedMeshData = new InstancedMeshData(geometry, material, bufferSize);
    const mesh = instancedMeshData.mesh;

    // Populate instances
    const matrix = new THREE.Matrix4();
    for (let i = 0; i < instances.length; i++) {
      const { position, rotation, scale } = instances[i];

      // Allocate instance
      const instanceId = `${regionId}_${regionInstanced.nextInstanceId++}`;
      const index = instancedMeshData.allocateInstance(instanceId);

      // Set transform
      matrix.compose(
        position,
        new THREE.Quaternion().setFromEuler(new THREE.Euler(0, rotation, 0)),
        new THREE.Vector3(scale, scale, scale)
      );
      mesh.setMatrixAt(index, matrix);

      // Store metadata
      const metadata = new InstanceMetadata(instanceId, type, position, rotation, scale);
      regionInstanced.instanceMetadata.set(instanceId, metadata);

      // Add to spatial grid
      regionInstanced.spatialGrid.insert(instanceId, position);
    }

    mesh.instanceMatrix.needsUpdate = true;
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    // Add to scene
    this.scene.add(mesh);

    // Store in region
    regionInstanced.instancedMeshes.set(type, instancedMeshData);
  }

  /**
   * Remove instanced vegetation for a region
   */
  removeRegionVegetationInstanced(regionId) {
    const regionInstanced = this.instancedRegions.get(regionId);
    if (!regionInstanced) return;

    // Remove all instanced meshes from scene
    for (const instancedMeshData of regionInstanced.instancedMeshes.values()) {
      this.scene.remove(instancedMeshData.mesh);
      instancedMeshData.dispose();
    }

    // Clean up data structures
    regionInstanced.dispose();
    this.instancedRegions.delete(regionId);

    console.log(`🌿 Removed instanced vegetation: ${regionId}`);
  }

  /**
   * Get vegetation near position (INSTANCED)
   */
  getVegetationNearInstanced(position, radius = 5) {
    const nearby = [];
    const radiusSq = radius * radius;

    // Query all loaded regions
    for (const regionInstanced of this.instancedRegions.values()) {
      // Use spatial grid for fast broad-phase
      const candidateIds = regionInstanced.spatialGrid.queryRadius(position, radius);

      // Narrow-phase: check exact distance
      for (const instanceId of candidateIds) {
        const metadata = regionInstanced.instanceMetadata.get(instanceId);
        if (metadata && metadata.visible) {
          const distSq = metadata.position.distanceToSquared(position);
          if (distSq <= radiusSq) {
            nearby.push({
              instanceId: instanceId,
              type: metadata.type,
              position: metadata.position,
              distance: Math.sqrt(distSq)
            });
          }
        }
      }
    }

    return nearby;
  }

  /**
   * Remove vegetation at position (INSTANCED)
   */
  removeVegetationAtInstanced(position, radius = 2) {
    let removedCount = 0;

    for (const regionInstanced of this.instancedRegions.values()) {
      const candidateIds = regionInstanced.spatialGrid.queryRadius(position, radius);

      for (const instanceId of candidateIds) {
        const metadata = regionInstanced.instanceMetadata.get(instanceId);
        if (metadata && metadata.visible) {
          const dist = metadata.position.distanceTo(position);
          if (dist <= radius) {
            // Hide instance
            const instancedMeshData = regionInstanced.instancedMeshes.get(metadata.type);
            if (instancedMeshData) {
              // Get index BEFORE freeing
              const index = instancedMeshData.idToIndex.get(instanceId);

              if (index !== undefined && instancedMeshData.freeInstance(instanceId)) {
                metadata.visible = false;

                // Scale to zero for GPU culling
                const matrix = new THREE.Matrix4();
                matrix.makeScale(0, 0, 0);
                instancedMeshData.mesh.setMatrixAt(index, matrix);
                instancedMeshData.mesh.instanceMatrix.needsUpdate = true;

                // Remove from spatial grid
                regionInstanced.spatialGrid.remove(instanceId, metadata.position);

                removedCount++;
              }
            }
          }
        }
      }
    }

    if (removedCount > 0) {
      console.log(`🌿 Removed ${removedCount} vegetation items (instanced)`);
    }

    return removedCount;
  }

  /**
   * Spawn vegetation at position (INSTANCED)
   */
  spawnVegetationAtInstanced(type, position) {
    // Find which region this position belongs to (simple heuristic)
    let targetRegion = null;
    for (const regionInstanced of this.instancedRegions.values()) {
      // If region has any instances, assume it covers this area
      // TODO: proper region bounds check
      targetRegion = regionInstanced;
      break;
    }

    if (!targetRegion) {
      console.warn('Cannot find region for position');
      return null;
    }

    let instancedMeshData = targetRegion.instancedMeshes.get(type);

    // Create instanced mesh for this type if it doesn't exist
    if (!instancedMeshData) {
      this.createInstancedVegetationGroup(
        targetRegion.regionId,
        targetRegion,
        type,
        [] // Empty, will add below
      );
      instancedMeshData = targetRegion.instancedMeshes.get(type);
    }

    // Allocate instance
    const instanceId = `${targetRegion.regionId}_${targetRegion.nextInstanceId++}`;
    const instanceIndex = instancedMeshData.allocateInstance(instanceId);

    if (instanceIndex === null) {
      console.warn(`  ⚠️ Buffer full for type ${type}`);
      return null;
    }

    // Set transform
    const matrix = new THREE.Matrix4();
    const rotation = Math.random() * Math.PI * 2;
    const scale = 0.8 + Math.random() * 0.4;
    matrix.compose(
      position,
      new THREE.Quaternion().setFromEuler(new THREE.Euler(0, rotation, 0)),
      new THREE.Vector3(scale, scale, scale)
    );
    instancedMeshData.mesh.setMatrixAt(instanceIndex, matrix);
    instancedMeshData.mesh.instanceMatrix.needsUpdate = true;

    // Store metadata
    const metadata = new InstanceMetadata(instanceId, type, position, rotation, scale);
    targetRegion.instanceMetadata.set(instanceId, metadata);

    // Add to spatial grid
    targetRegion.spatialGrid.insert(instanceId, position);

    console.log(`🌿 Spawned ${type} at (${position.x.toFixed(0)}, ${position.z.toFixed(0)})`);
    return instanceId;
  }
}

// export default VegetationSystem; // Converted to global
window.VegetationSystem = VegetationSystem;
