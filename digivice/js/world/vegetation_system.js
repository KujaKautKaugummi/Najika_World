// 🌿 VEGETATION SYSTEM - Verwaltet Vegetation-Placement pro Biome
// Platziert Bäume, Pflanzen, Mushrooms, Cacti basierend auf Biome-Daten

const THREE = window.THREE;

class VegetationSystem {
  constructor(scene, terrainGenerator) {
    this.scene = scene;
    this.terrainGenerator = terrainGenerator;
    this.vegetationGroups = new Map();  // Per-region vegetation groups
    this.vegetationTemplates = new Map();  // Reusable geometries
    this.instancedMeshes = new Map();  // For performance optimization
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
   * Populate Region mit Vegetation
   * @param {string} regionId - Region ID
   * @param {Object} regionData - Region data from regions.json
   * @param {Object} biomeData - Biome data from biomes.json
   */
  populateRegion(regionId, regionData, biomeData) {
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
   * Remove vegetation for a region (for streaming)
   */
  removeRegionVegetation(regionId) {
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
    // TODO: Implement LOD switching based on distance
    // TODO: Implement frustum culling for performance

    // For now: Simple distance-based visibility
    for (const [regionId, group] of this.vegetationGroups.entries()) {
      const distance = group.position.distanceTo(cameraPosition);
      group.visible = distance < 3000;  // Hide if > 3000 units away
    }
  }

  /**
   * Get vegetation at position (for collision, interaction)
   * @param {THREE.Vector3} position
   * @param {number} radius
   * @returns {Array<THREE.Object3D>} Nearby vegetation
   */
  getVegetationNear(position, radius = 5) {
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
   * Remove vegetation at position (for harvesting, destruction)
   */
  removeVegetationAt(position, radius = 2) {
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
   * Spawn vegetation at position (for replanting, growth)
   */
  spawnVegetationAt(type, position) {
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
}

export default VegetationSystem;
