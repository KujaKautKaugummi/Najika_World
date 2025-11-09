// 🏔️ TERRAIN GENERATOR - Najikas 9600x9600 Welt
// Generiert Terrain für alle 8 Regionen mit Biome-spezifischen Höhenprofilen

const THREE = window.THREE;

class TerrainGenerator {
  constructor(worldSize = 9600) {
    this.worldSize = worldSize;
    this.segments = 200;  // Mehr Detail für größere Welt
    this.regionTerrains = new Map();  // Map<regionId, {geometry, region}>
  }

  /**
   * Generiert Terrain für eine gesamte Region
   * @param {Object} regionData - Region-Daten aus regions.json
   * @param {Object} biomeData - Biome-Daten aus biomes.json
   * @returns {THREE.PlaneGeometry} Terrain-Geometrie
   */
  generateRegionTerrain(regionData, biomeData) {
    const { bounds, biome, id } = regionData;
    const config = biomeData.biomes[biome];

    console.log(`🏔️ Generating terrain for ${regionData.name} (${biome})`);

    // Calculate region size
    const width = bounds.maxX - bounds.minX;
    const height = bounds.maxZ - bounds.minZ;

    // Create plane geometry
    const geometry = new THREE.PlaneGeometry(
      width,
      height,
      this.segments,
      this.segments
    );

    // Get vertices
    const vertices = geometry.attributes.position.array;

    // Apply biome-specific terrain
    switch(biome) {
      case 'desert':
        this.applyDesertTerrain(vertices, width, height, config);
        break;
      case 'forest':
        this.applyForestTerrain(vertices, width, height, config);
        break;
      case 'coast':
        this.applyCoastalTerrain(vertices, width, height, config, bounds);
        break;
      case 'highland':
        this.applyHighlandTerrain(vertices, width, height, config);
        break;
      case 'swamp':
        this.applySwampTerrain(vertices, width, height, config);
        break;
      case 'ice':
        this.applyIceTerrain(vertices, width, height, config);
        break;
      case 'volcano':
        this.applyVolcanoTerrain(vertices, width, height, config);
        break;
      case 'mountain':
        this.applyMountainTerrain(vertices, width, height, config, regionData);
        break;
      case 'caves':
        this.applyCaveTerrain(vertices, width, height, config);
        break;
      default:
        console.warn(`Unknown biome: ${biome}`);
    }

    // Compute normals for proper lighting
    geometry.computeVertexNormals();

    // Store terrain with region data (needed for world→local coordinate conversion)
    this.regionTerrains.set(id, {
      geometry: geometry,
      region: regionData
    });

    return geometry;
  }

  /**
   * DESERT - Sanfte Dünen mit Perlin Noise
   */
  applyDesertTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Layered Perlin noise für organische Dünen
      const noise1 = this.perlin2D(x * noiseScale, z * noiseScale);
      const noise2 = this.perlin2D(x * noiseScale * 2, z * noiseScale * 2) * 0.5;
      const noise3 = this.perlin2D(x * noiseScale * 4, z * noiseScale * 4) * 0.25;

      const combined = (noise1 + noise2 + noise3) / 1.75;
      const height_val = combined * heightVariation;

      vertices[i + 2] = height_val;  // Y-coordinate
    }
  }

  /**
   * FOREST - Hügelig mit dichter Vegetation
   */
  applyForestTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Sanfte Hügel
      const noise = this.perlin2D(x * noiseScale, z * noiseScale);
      const height_val = noise * heightVariation;

      vertices[i + 2] = height_val;
    }
  }

  /**
   * COAST - Strand mit Wassernähe
   */
  applyCoastalTerrain(vertices, width, height, config, bounds) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Distanz zur Küstenlinie (westliche Kante)
      const distToCoast = Math.abs(x - bounds.minX);
      const beachFactor = Math.min(1, distToCoast / 200);  // Strand 200m breit

      const noise = this.perlin2D(x * noiseScale, z * noiseScale);
      const base_height = noise * heightVariation * beachFactor;

      // Strand ist flach, dann steigt es an
      vertices[i + 2] = base_height;
    }
  }

  /**
   * HIGHLAND - Felsige Hochebene
   */
  applyHighlandTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Rauere Noise für felsiges Terrain
      const noise1 = this.perlin2D(x * noiseScale, z * noiseScale);
      const noise2 = Math.abs(this.perlin2D(x * noiseScale * 5, z * noiseScale * 5)) * 0.3;

      const combined = noise1 + noise2;
      const height_val = combined * heightVariation + 30;  // Base elevation

      vertices[i + 2] = height_val;
    }
  }

  /**
   * SWAMP - Flach und sumpfig
   */
  applySwampTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Sehr sanfte Variationen (Sumpf ist fast flach)
      const noise = this.perlin2D(x * noiseScale, z * noiseScale);
      const height_val = noise * heightVariation - 2;  // Leicht unter Meeresspiegel

      vertices[i + 2] = height_val;
    }
  }

  /**
   * ICE - Gletscher und Eis
   */
  applyIceTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Glatte Gletscher mit scharfen Kanten
      const noise = this.perlin2D(x * noiseScale, z * noiseScale);
      const ridges = Math.abs(this.perlin2D(x * noiseScale * 3, z * noiseScale * 3)) * 0.4;

      const height_val = (noise + ridges) * heightVariation;

      vertices[i + 2] = height_val;
    }
  }

  /**
   * VOLCANO - Raues Vulkangestein
   */
  applyVolcanoTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Sehr raues Terrain mit Lavakanälen
      const noise1 = this.perlin2D(x * noiseScale, z * noiseScale);
      const noise2 = Math.abs(this.perlin2D(x * noiseScale * 4, z * noiseScale * 4)) * 0.5;
      const channels = Math.sin(x * 0.02) * Math.cos(z * 0.02) * 5;  // Lavakanäle

      const combined = noise1 + noise2 + channels;
      const height_val = combined * heightVariation;

      vertices[i + 2] = height_val;
    }
  }

  /**
   * MOUNTAIN - GÖTTERFELS (Steiler Berg in der Mitte!)
   */
  applyMountainTerrain(vertices, width, height, config, regionData) {
    const centerX = 0;  // Relative zum Geometrie-Zentrum
    const centerZ = 0;
    const maxHeight = config.terrain.peakHeight || 500;
    const baseRadius = 1200;  // Berg-Basis

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Distanz vom Berg-Zentrum
      const dist = Math.sqrt(x * x + z * z);

      if (dist < baseRadius) {
        // Innerhalb des Berges
        const factor = 1 - (dist / baseRadius);
        let mountainHeight = factor * factor * maxHeight;  // Quadratischer Abfall

        // Füge Noise für Rocky Details hinzu
        const noise = this.perlin2D(x * 0.01, z * 0.01) * 20;
        mountainHeight += noise;

        vertices[i + 2] = Math.max(0, mountainHeight);
      } else {
        // Außerhalb des Berges (flaches Vorland)
        const noise = this.perlin2D(x * 0.005, z * 0.005);
        vertices[i + 2] = noise * 10;
      }
    }
  }

  /**
   * CAVES - Unterirdisches Terrain (für später)
   */
  applyCaveTerrain(vertices, width, height, config) {
    const { heightVariation, noiseScale } = config.terrain;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Wellenförmiges Höhlendach
      const noise = this.perlin2D(x * noiseScale, z * noiseScale);
      const height_val = noise * heightVariation - 100;  // Unterirdisch bei Y=-100

      vertices[i + 2] = height_val;
    }
  }

  /**
   * Simplified 2D Perlin Noise
   * (In production, use proper noise library like simplex-noise)
   */
  perlin2D(x, y) {
    // Very simplified Perlin - replace with real implementation
    const value = Math.sin(x * 1.5) * Math.cos(y * 1.5) +
                  Math.sin(x * 3) * Math.cos(y * 3) * 0.5 +
                  Math.sin(x * 6) * Math.cos(y * 6) * 0.25;

    return (value + 1.75) / 3.5;  // Normalize to 0-1
  }

  /**
   * Hole Terrain-Höhe an einer Position (für Vegetation/Objekte)
   * @param {string} regionId - Region ID
   * @param {number} x - World X coordinate
   * @param {number} z - World Z coordinate
   * @returns {number} Height at position
   */
  getHeightAt(regionId, x, z) {
    const terrainData = this.regionTerrains.get(regionId);
    if (!terrainData) return 0;

    const { geometry, region } = terrainData;
    const vertices = geometry.attributes.position.array;

    // Convert world coordinates to local coordinates
    // (Terrain mesh is positioned at region.position)
    const localX = x - region.position.x;
    const localZ = z - region.position.z;

    // Find closest vertex (simplified)
    // NOTE: PlaneGeometry vertices are in X-Y plane, rotated to X-Z
    // Before rotation: vertices[i]=X, vertices[i+1]=Y(height), vertices[i+2]=Z
    let closestHeight = 0;
    let minDist = Infinity;

    for (let i = 0; i < vertices.length; i += 3) {
      const vx = vertices[i];       // Local X
      const vz = vertices[i + 1];   // Local Z (becomes Z after rotation)
      const vy = vertices[i + 2];   // Height (becomes Y after rotation)

      const dist = Math.sqrt((vx - localX) ** 2 + (vz - localZ) ** 2);

      if (dist < minDist) {
        minDist = dist;
        closestHeight = vy;
      }
    }

    return closestHeight;
  }
}

export default TerrainGenerator;
