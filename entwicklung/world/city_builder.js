// 🏘️ CITY BUILDER - Erstellt Städte mit Gebäuden und Features
// Platziert: Handelsfestung, Dampf-Hain, Salzige Bucht, Runenheim, Funken-Siedlung

import * as THREE from 'three';

class CityBuilder {
  constructor(scene, terrainGenerator) {
    this.scene = scene;
    this.terrainGenerator = terrainGenerator;
    this.cities = new Map();
    this.buildingTemplates = new Map();
  }

  /**
   * Initialisiere Building-Templates (Placeholder)
   * TODO: Replace with KayKit Medieval assets
   */
  initializeTemplates() {
    console.log('🏘️ Initializing building templates...');

    // BASIC BUILDINGS
    this.createHouseTemplate('house', { width: 6, depth: 6, height: 4 });
    this.createHouseTemplate('large_house', { width: 8, depth: 8, height: 5 });

    // CITY-SPECIFIC BUILDINGS
    this.createTradingPostTemplate('trading_post');
    this.createPlayerShopTemplate('player_shop');
    this.createArenaTemplate('pvp_arena');
    this.createInnTemplate('inn');
    this.createOnsenTemplate('onsen');
    this.createRestaurantTemplate('restaurant');
    this.createDruidHutTemplate('druid_hut');
    this.createHarborBuildingTemplate('harbor_building');
    this.createLighthouseTemplate('lighthouse');
    this.createShipTemplate('ship');
    this.createMagicAcademyTemplate('magic_academy');
    this.createRuneShopTemplate('rune_shop');
    this.createTotemTemplate('totem');
    this.createForgeTemplate('forge');
    this.createBlacksmithTemplate('blacksmith');
    this.createLavaDockTemplate('lava_dock');
    this.createFireproofHouseTemplate('fireproof_house');

    console.log(`🏘️ Templates initialized: ${this.buildingTemplates.size} types`);
  }

  /**
   * Standard House Template
   */
  createHouseTemplate(type, { width, depth, height }) {
    const group = new THREE.Group();

    // Walls
    const wallsGeometry = new THREE.BoxGeometry(width, height, depth);
    const wallsMaterial = new THREE.MeshStandardMaterial({
      color: 0xd2b48c,
      roughness: 0.8
    });
    const walls = new THREE.Mesh(wallsGeometry, wallsMaterial);
    walls.position.y = height / 2;
    walls.castShadow = true;
    walls.receiveShadow = true;
    group.add(walls);

    // Roof (pyramid)
    const roofGeometry = new THREE.ConeGeometry(width * 0.8, height * 0.5, 4);
    const roofMaterial = new THREE.MeshStandardMaterial({
      color: 0x8b4513,
      roughness: 0.9
    });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = height + height * 0.25;
    roof.rotation.y = Math.PI / 4;
    roof.castShadow = true;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width, depth } });
  }

  /**
   * Trading Post (Handelsfestung)
   */
  createTradingPostTemplate(type) {
    const group = new THREE.Group();

    // Main building (larger)
    const mainGeometry = new THREE.BoxGeometry(10, 6, 10);
    const mainMaterial = new THREE.MeshStandardMaterial({ color: 0xdaa520 });
    const main = new THREE.Mesh(mainGeometry, mainMaterial);
    main.position.y = 3;
    main.castShadow = true;
    group.add(main);

    // Flat roof
    const roofGeometry = new THREE.BoxGeometry(11, 0.5, 11);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 6.25;
    roof.castShadow = true;
    group.add(roof);

    // Shop sign
    const signGeometry = new THREE.BoxGeometry(0.2, 2, 3);
    const signMaterial = new THREE.MeshStandardMaterial({ color: 0xff6347 });
    const sign = new THREE.Mesh(signGeometry, signMaterial);
    sign.position.set(0, 4, 5.5);
    group.add(sign);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 10, depth: 10 } });
  }

  /**
   * Player Shop (Fallout 76 style camp)
   */
  createPlayerShopTemplate(type) {
    const group = new THREE.Group();

    // Simple tent/stand structure
    const baseGeometry = new THREE.BoxGeometry(4, 0.5, 4);
    const baseMaterial = new THREE.MeshStandardMaterial({ color: 0x8b7355 });
    const base = new THREE.Mesh(baseGeometry, baseMaterial);
    base.position.y = 0.25;
    group.add(base);

    // Canopy (tent roof)
    const canopyGeometry = new THREE.ConeGeometry(3, 2, 4);
    const canopyMaterial = new THREE.MeshStandardMaterial({ color: 0xffa500 });
    const canopy = new THREE.Mesh(canopyGeometry, canopyMaterial);
    canopy.position.y = 2;
    canopy.rotation.y = Math.PI / 4;
    group.add(canopy);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 4, depth: 4 } });
  }

  /**
   * PvP Arena (Handelsfestung)
   */
  createArenaTemplate(type) {
    const group = new THREE.Group();

    // Arena floor (large circle)
    const floorGeometry = new THREE.CylinderGeometry(30, 30, 0.5, 32);
    const floorMaterial = new THREE.MeshStandardMaterial({ color: 0xcd853f });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.position.y = 0.25;
    floor.receiveShadow = true;
    group.add(floor);

    // Arena walls (ring)
    const wallGeometry = new THREE.TorusGeometry(30, 2, 8, 32);
    const wallMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const wall = new THREE.Mesh(wallGeometry, wallMaterial);
    wall.rotation.x = Math.PI / 2;
    wall.position.y = 2;
    wall.castShadow = true;
    group.add(wall);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 64, depth: 64 } });
  }

  /**
   * Inn/Tavern
   */
  createInnTemplate(type) {
    const group = new THREE.Group();

    // Building
    const buildingGeometry = new THREE.BoxGeometry(12, 7, 10);
    const buildingMaterial = new THREE.MeshStandardMaterial({ color: 0xdeb887 });
    const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
    building.position.y = 3.5;
    building.castShadow = true;
    group.add(building);

    // Roof
    const roofGeometry = new THREE.ConeGeometry(10, 3, 4);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x8b0000 });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 8.5;
    roof.rotation.y = Math.PI / 4;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 12, depth: 10 } });
  }

  /**
   * Onsen (Hot Spring - Dampf-Hain)
   */
  createOnsenTemplate(type) {
    const group = new THREE.Group();

    // Pool (cylinder)
    const poolGeometry = new THREE.CylinderGeometry(6, 6, 1, 16);
    const poolMaterial = new THREE.MeshStandardMaterial({
      color: 0x4682b4,
      transparent: true,
      opacity: 0.6,
      roughness: 0.1
    });
    const pool = new THREE.Mesh(poolGeometry, poolMaterial);
    pool.position.y = 0.5;
    group.add(pool);

    // Rocks around pool
    const rockGeometry = new THREE.DodecahedronGeometry(1);
    const rockMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
    for (let i = 0; i < 8; i++) {
      const rock = new THREE.Mesh(rockGeometry, rockMaterial);
      const angle = (i / 8) * Math.PI * 2;
      rock.position.set(Math.cos(angle) * 6, 0.5, Math.sin(angle) * 6);
      rock.castShadow = true;
      group.add(rock);
    }

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 14, depth: 14 } });
  }

  /**
   * Restaurant (Spirited Away style - Dampf-Hain)
   */
  createRestaurantTemplate(type) {
    const group = new THREE.Group();

    // Main building (Japanese style)
    const buildingGeometry = new THREE.BoxGeometry(14, 6, 12);
    const buildingMaterial = new THREE.MeshStandardMaterial({ color: 0xdc143c });
    const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
    building.position.y = 3;
    building.castShadow = true;
    group.add(building);

    // Japanese-style roof (wide and flat)
    const roofGeometry = new THREE.BoxGeometry(16, 1, 14);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x8b0000 });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 6.5;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 14, depth: 12 } });
  }

  /**
   * Druid Hut (Samtmoos-Tiefwald)
   */
  createDruidHutTemplate(type) {
    const group = new THREE.Group();

    // Round hut
    const hutGeometry = new THREE.CylinderGeometry(3, 3.5, 4, 8);
    const hutMaterial = new THREE.MeshStandardMaterial({ color: 0x8b7355 });
    const hut = new THREE.Mesh(hutGeometry, hutMaterial);
    hut.position.y = 2;
    hut.castShadow = true;
    group.add(hut);

    // Thatched roof
    const roofGeometry = new THREE.ConeGeometry(4, 2, 8);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0xdaa520 });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 5;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 7, depth: 7 } });
  }

  /**
   * Harbor Building (Salzige Bucht)
   */
  createHarborBuildingTemplate(type) {
    const group = new THREE.Group();

    // Warehouse
    const warehouseGeometry = new THREE.BoxGeometry(12, 8, 15);
    const warehouseMaterial = new THREE.MeshStandardMaterial({ color: 0xa0522d });
    const warehouse = new THREE.Mesh(warehouseGeometry, warehouseMaterial);
    warehouse.position.y = 4;
    warehouse.castShadow = true;
    group.add(warehouse);

    // Simple flat roof
    const roofGeometry = new THREE.BoxGeometry(13, 0.5, 16);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 8.25;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 12, depth: 15 } });
  }

  /**
   * Lighthouse (Salzige Bucht)
   */
  createLighthouseTemplate(type) {
    const group = new THREE.Group();

    // Tower
    const towerGeometry = new THREE.CylinderGeometry(2, 3, 30, 8);
    const towerMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const tower = new THREE.Mesh(towerGeometry, towerMaterial);
    tower.position.y = 15;
    tower.castShadow = true;
    group.add(tower);

    // Light room
    const lightRoomGeometry = new THREE.CylinderGeometry(2.5, 2.5, 3, 8);
    const lightRoomMaterial = new THREE.MeshStandardMaterial({
      color: 0xffff00,
      emissive: 0xffff00,
      emissiveIntensity: 0.5
    });
    const lightRoom = new THREE.Mesh(lightRoomGeometry, lightRoomMaterial);
    lightRoom.position.y = 31.5;
    group.add(lightRoom);

    // Point light
    const light = new THREE.PointLight(0xffff00, 2, 100);
    light.position.y = 32;
    group.add(light);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 6, depth: 6 } });
  }

  /**
   * Ship (Salzige Bucht)
   */
  createShipTemplate(type) {
    const group = new THREE.Group();

    // Hull
    const hullGeometry = new THREE.BoxGeometry(8, 4, 20);
    const hullMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const hull = new THREE.Mesh(hullGeometry, hullMaterial);
    hull.position.y = 2;
    hull.castShadow = true;
    group.add(hull);

    // Mast
    const mastGeometry = new THREE.CylinderGeometry(0.3, 0.3, 15, 8);
    const mastMaterial = new THREE.MeshStandardMaterial({ color: 0xdeb887 });
    const mast = new THREE.Mesh(mastGeometry, mastMaterial);
    mast.position.y = 11.5;
    group.add(mast);

    // Sail
    const sailGeometry = new THREE.PlaneGeometry(6, 10);
    const sailMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      side: THREE.DoubleSide
    });
    const sail = new THREE.Mesh(sailGeometry, sailMaterial);
    sail.position.set(3, 12, 0);
    group.add(sail);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 8, depth: 20 } });
  }

  /**
   * Magic Academy (Runenheim)
   */
  createMagicAcademyTemplate(type) {
    const group = new THREE.Group();

    // Tower
    const towerGeometry = new THREE.CylinderGeometry(5, 6, 20, 8);
    const towerMaterial = new THREE.MeshStandardMaterial({ color: 0x9370db });
    const tower = new THREE.Mesh(towerGeometry, towerMaterial);
    tower.position.y = 10;
    tower.castShadow = true;
    group.add(tower);

    // Roof (cone)
    const roofGeometry = new THREE.ConeGeometry(6, 5, 8);
    const roofMaterial = new THREE.MeshStandardMaterial({
      color: 0x4b0082,
      emissive: 0x4b0082,
      emissiveIntensity: 0.2
    });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 22.5;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 12, depth: 12 } });
  }

  /**
   * Rune Shop (Runenheim)
   */
  createRuneShopTemplate(type) {
    const group = new THREE.Group();

    // Building
    const buildingGeometry = new THREE.BoxGeometry(6, 5, 6);
    const buildingMaterial = new THREE.MeshStandardMaterial({ color: 0x8b7355 });
    const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
    building.position.y = 2.5;
    building.castShadow = true;
    group.add(building);

    // Glowing rune symbol
    const runeGeometry = new THREE.RingGeometry(1, 1.5, 6);
    const runeMaterial = new THREE.MeshStandardMaterial({
      color: 0x9370db,
      emissive: 0x9370db,
      emissiveIntensity: 0.5,
      side: THREE.DoubleSide
    });
    const rune = new THREE.Mesh(runeGeometry, runeMaterial);
    rune.position.set(0, 4, 3.5);
    group.add(rune);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 6, depth: 6 } });
  }

  /**
   * Totem (Runenheim)
   */
  createTotemTemplate(type) {
    const group = new THREE.Group();

    const totemGeometry = new THREE.CylinderGeometry(0.5, 0.5, 8, 4);
    const totemMaterial = new THREE.MeshStandardMaterial({ color: 0x654321 });
    const totem = new THREE.Mesh(totemGeometry, totemMaterial);
    totem.position.y = 4;
    totem.castShadow = true;
    group.add(totem);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 1, depth: 1 } });
  }

  /**
   * Forge (Funken-Siedlung)
   */
  createForgeTemplate(type) {
    const group = new THREE.Group();

    // Building
    const buildingGeometry = new THREE.BoxGeometry(10, 6, 10);
    const buildingMaterial = new THREE.MeshStandardMaterial({ color: 0x2f4f4f });
    const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
    building.position.y = 3;
    building.castShadow = true;
    group.add(building);

    // Chimney
    const chimneyGeometry = new THREE.CylinderGeometry(1, 1, 8, 8);
    const chimneyMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
    const chimney = new THREE.Mesh(chimneyGeometry, chimneyMaterial);
    chimney.position.set(3, 10, 3);
    group.add(chimney);

    // Glow from forge
    const glowLight = new THREE.PointLight(0xff4500, 2, 20);
    glowLight.position.set(0, 2, 0);
    group.add(glowLight);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 10, depth: 10 } });
  }

  /**
   * Blacksmith (Funken-Siedlung)
   */
  createBlacksmithTemplate(type) {
    const group = new THREE.Group();

    // Building
    const buildingGeometry = new THREE.BoxGeometry(8, 5, 8);
    const buildingMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
    building.position.y = 2.5;
    building.castShadow = true;
    group.add(building);

    // Anvil sign
    const anvilGeometry = new THREE.BoxGeometry(0.5, 1, 1);
    const anvilMaterial = new THREE.MeshStandardMaterial({ color: 0x708090 });
    const anvil = new THREE.Mesh(anvilGeometry, anvilMaterial);
    anvil.position.set(0, 4, 4.5);
    group.add(anvil);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 8, depth: 8 } });
  }

  /**
   * Lava Dock (Funken-Siedlung)
   */
  createLavaDockTemplate(type) {
    const group = new THREE.Group();

    // Platform
    const platformGeometry = new THREE.BoxGeometry(15, 1, 8);
    const platformMaterial = new THREE.MeshStandardMaterial({ color: 0x696969 });
    const platform = new THREE.Mesh(platformGeometry, platformMaterial);
    platform.position.y = 0.5;
    group.add(platform);

    // Lava underneath (glowing)
    const lavaGeometry = new THREE.PlaneGeometry(15, 8);
    const lavaMaterial = new THREE.MeshStandardMaterial({
      color: 0xff4500,
      emissive: 0xff4500,
      emissiveIntensity: 0.8
    });
    const lava = new THREE.Mesh(lavaGeometry, lavaMaterial);
    lava.rotation.x = -Math.PI / 2;
    lava.position.y = -1;
    group.add(lava);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 15, depth: 8 } });
  }

  /**
   * Fireproof House (Funken-Siedlung)
   */
  createFireproofHouseTemplate(type) {
    const group = new THREE.Group();

    // Obsidian-like walls
    const wallsGeometry = new THREE.BoxGeometry(6, 5, 6);
    const wallsMaterial = new THREE.MeshStandardMaterial({
      color: 0x2f2f2f,
      roughness: 0.3,
      metalness: 0.5
    });
    const walls = new THREE.Mesh(wallsGeometry, wallsMaterial);
    walls.position.y = 2.5;
    walls.castShadow = true;
    group.add(walls);

    // Metal roof
    const roofGeometry = new THREE.ConeGeometry(5, 2, 4);
    const roofMaterial = new THREE.MeshStandardMaterial({
      color: 0x708090,
      metalness: 0.8
    });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 6;
    roof.rotation.y = Math.PI / 4;
    group.add(roof);

    this.buildingTemplates.set(type, { geometry: group, footprint: { width: 6, depth: 6 } });
  }

  /**
   * Build a city from cities.json data
   * @param {Object} cityData - City data from cities.json
   */
  buildCity(cityData) {
    console.log(`🏘️ Building city: ${cityData.name}`);

    const cityGroup = new THREE.Group();
    cityGroup.name = `city_${cityData.id}`;

    const { position, buildings } = cityData;
    const centerX = position.x;
    const centerZ = position.z;

    // Place buildings in a grid around the city center
    let placedCount = 0;
    let gridX = -20;
    let gridZ = -20;

    for (const buildingType of buildings.types) {
      for (let i = 0; i < buildingType.count; i++) {
        const building = this.createBuilding(buildingType.type, centerX + gridX, centerZ + gridZ);

        if (building) {
          cityGroup.add(building);
          placedCount++;

          // Move to next grid position
          gridX += 12;
          if (gridX > 20) {
            gridX = -20;
            gridZ += 12;
          }
        }
      }
    }

    console.log(`  ✅ Placed ${placedCount} buildings`);

    this.cities.set(cityData.id, cityGroup);
    this.scene.add(cityGroup);

    return cityGroup;
  }

  /**
   * Create single building
   */
  createBuilding(type, x, z) {
    const template = this.buildingTemplates.get(type);
    if (!template) {
      console.warn(`  ⚠️ Building template not found: ${type}`);
      return null;
    }

    const building = template.geometry.clone();
    const y = this.terrainGenerator.getHeightAt(x, z);
    building.position.set(x, y, z);

    // Random rotation (90° increments)
    building.rotation.y = (Math.floor(Math.random() * 4) * Math.PI) / 2;

    return building;
  }

  /**
   * Get city
   */
  getCity(cityId) {
    return this.cities.get(cityId);
  }

  /**
   * Remove city
   */
  removeCity(cityId) {
    const city = this.cities.get(cityId);
    if (city) {
      this.scene.remove(city);
      city.clear();
      this.cities.delete(cityId);
      console.log(`🏘️ Removed city: ${cityId}`);
    }
  }

  /**
   * Get stats
   */
  getStats() {
    let totalBuildings = 0;
    for (const city of this.cities.values()) {
      totalBuildings += city.children.length;
    }

    return {
      citiesLoaded: this.cities.size,
      totalBuildings: totalBuildings
    };
  }
}

export default CityBuilder;
