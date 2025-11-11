/**
 * InteriorGenerator - Generiert Stadt-Interiors (133.32 x 133.32 Einheiten)
 *
 * Jede Stadt hat ein eigenes Layout mit Straßen, Gebäuden und NPCs.
 * Interior-Size entspricht der Größe einer Region (133.32 x 133.32).
 */

class InteriorGenerator {
    constructor(scene, THREE) {
        this.scene = scene;
        this.THREE = THREE;
        this.interiorSize = 133.32; // 4x größere Welt
        this.currentInterior = null;
        this.interiorObjects = [];
    }

    /**
     * Generiert ein Stadt-Interior basierend auf cityData
     * @param {Object} cityData - Stadt-Daten mit name, type, buildings, etc.
     * @returns {Object} Interior-Objekt mit mesh, exitPortal, buildings
     */
    generateCityInterior(cityData) {
        console.log(`🏗️ Generiere Interior für ${cityData.name}...`);

        const interior = {
            name: cityData.name,
            type: cityData.type,
            objects: [],
            exitPortal: null,
            buildings: [],
            npcs: []
        };

        // 1. Boden-Plane (133.32 x 133.32)
        const groundGeometry = new this.THREE.PlaneGeometry(this.interiorSize, this.interiorSize, 40, 40);
        const groundMaterial = new this.THREE.MeshStandardMaterial({
            color: this.getCityGroundColor(cityData.name),
            roughness: 0.8,
            metalness: 0.2
        });
        const ground = new this.THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = 0;
        ground.receiveShadow = true;
        ground.name = 'interior_ground';
        interior.objects.push(ground);

        // 2. Stadt-spezifisches Layout
        switch(cityData.name) {
            case 'Handelsfestung':
                this.generateTradingFortInterior(interior, cityData);
                break;
            case 'Dampf-Hain':
                this.generateSteamGroveInterior(interior, cityData);
                break;
            case 'Salzige Bucht':
                this.generateSaltyBayInterior(interior, cityData);
                break;
            case 'Runenheim':
                this.generateRuneheimInterior(interior, cityData);
                break;
            case 'Funken-Siedlung':
                this.generateSparkSettlementInterior(interior, cityData);
                break;
            default:
                this.generateGenericInterior(interior, cityData);
        }

        // 3. Exit-Portal platzieren (immer am Rand, bei 0, 0, -60)
        interior.exitPortal = this.createExitPortal(cityData.name);
        interior.objects.push(interior.exitPortal);

        // 4. Beleuchtung
        this.addInteriorLighting(interior, cityData);

        // 5. Wände/Grenzen (unsichtbare Collider)
        this.addInteriorBounds(interior);

        console.log(`✅ Interior für ${cityData.name} fertig: ${interior.objects.length} Objekte`);

        return interior;
    }

    /**
     * HANDELSFESTUNG - Trading Fort Interior (Fallout 76 Style)
     * 50 Gebäude: Trading Posts, Player Shops, Arena, Inn, Houses
     */
    generateTradingFortInterior(interior, cityData) {
        const gridSize = 7; // 7x7 Straßen-Grid
        const blockSize = this.interiorSize / gridSize;

        // Arena (Zentrum)
        const arena = this.createBuilding('Arena', 0, 0, 20, 20, 0xffd700);
        arena.userData.buildingType = 'arena';
        arena.userData.buildingName = 'PvP Arena';
        interior.buildings.push(arena);
        interior.objects.push(arena);

        // Player Shops (15 Stück, rund um Arena)
        for (let i = 0; i < 15; i++) {
            const angle = (i / 15) * Math.PI * 2;
            const radius = 35;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            const shop = this.createBuilding(`Player Shop ${i+1}`, x, z, 6, 6, 0xffa500);
            shop.userData.buildingType = 'player_shop';
            shop.userData.buildingName = `Player Shop ${i+1}`;
            interior.buildings.push(shop);
            interior.objects.push(shop);
        }

        // Trading Posts (8 Stück)
        for (let i = 0; i < 8; i++) {
            const x = (i % 4 - 1.5) * 25;
            const z = Math.floor(i / 4) * 50 - 25;
            const post = this.createBuilding(`Trading Post ${i+1}`, x, z, 8, 8, 0xdaa520);
            post.userData.buildingType = 'trading_post';
            post.userData.buildingName = `Trading Post ${i+1}`;
            interior.buildings.push(post);
            interior.objects.push(post);
        }

        // Inn (oben links)
        const inn = this.createBuilding('Inn', -45, -45, 12, 12, 0xcd853f);
        inn.userData.buildingType = 'inn';
        inn.userData.buildingName = 'Champions Inn';
        interior.buildings.push(inn);
        interior.objects.push(inn);

        // Houses (27 Stück, gefüllt)
        let houseCount = 0;
        for (let x = -50; x <= 50; x += 20) {
            for (let z = -50; z <= 50; z += 20) {
                // Skip center (Arena) and occupied areas
                if (Math.abs(x) < 25 && Math.abs(z) < 25) continue;
                if (houseCount >= 27) break;

                const house = this.createBuilding(`House ${houseCount+1}`, x, z, 5, 5, 0x8b4513);
                house.userData.buildingType = 'house';
                house.userData.buildingName = `House ${houseCount+1}`;
                interior.buildings.push(house);
                interior.objects.push(house);
                houseCount++;
            }
        }
    }

    /**
     * DAMPF-HAIN - Steam Grove Interior (Spirited Away Style)
     * 30 Gebäude: Onsen x3, Restaurants x5, Druid Huts x8, Houses x14
     */
    generateSteamGroveInterior(interior, cityData) {
        // Onsen (Healing Zones) - 3 große Pools
        for (let i = 0; i < 3; i++) {
            const x = (i - 1) * 35;
            const z = -40;
            const onsen = this.createBuilding(`Onsen ${i+1}`, x, z, 15, 15, 0x4682b4);
            onsen.userData.buildingType = 'onsen';
            onsen.userData.buildingName = `Onsen ${i+1} - Healing Zone`;
            onsen.userData.healingZone = true;
            interior.buildings.push(onsen);
            interior.objects.push(onsen);
        }

        // Restaurants (5 Stück) - Spirited Away Style
        for (let i = 0; i < 5; i++) {
            const x = (i - 2) * 20;
            const z = 0;
            const restaurant = this.createBuilding(`Restaurant ${i+1}`, x, z, 10, 10, 0x2ecc71);
            restaurant.userData.buildingType = 'restaurant';
            restaurant.userData.buildingName = `Restaurant ${i+1}`;
            interior.buildings.push(restaurant);
            interior.objects.push(restaurant);
        }

        // Druid Huts (8 Stück)
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const radius = 50;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            const hut = this.createBuilding(`Druid Hut ${i+1}`, x, z, 6, 6, 0x228b22);
            hut.userData.buildingType = 'druid_hut';
            hut.userData.buildingName = `Druid Hut ${i+1}`;
            interior.buildings.push(hut);
            interior.objects.push(hut);
        }

        // Houses (14 Stück)
        for (let i = 0; i < 14; i++) {
            const x = (i % 7 - 3) * 15;
            const z = Math.floor(i / 7) * 30 + 20;
            const house = this.createBuilding(`House ${i+1}`, x, z, 5, 5, 0x8b4513);
            house.userData.buildingType = 'house';
            house.userData.buildingName = `House ${i+1}`;
            interior.buildings.push(house);
            interior.objects.push(house);
        }
    }

    /**
     * SALZIGE BUCHT - Salty Bay Interior (Harbor Town)
     * 35 Gebäude: Harbor Buildings x8, Fish Market, Lighthouse, Ships x5, Houses x20
     */
    generateSaltyBayInterior(interior, cityData) {
        // Leuchtturm (Climbable) - Zentrum
        const lighthouse = this.createBuilding('Leuchtturm', 0, -50, 8, 30, 0x3498db);
        lighthouse.userData.buildingType = 'lighthouse';
        lighthouse.userData.buildingName = 'Leuchtturm';
        lighthouse.userData.climbable = true;
        interior.buildings.push(lighthouse);
        interior.objects.push(lighthouse);

        // Harbor Buildings (8 Stück)
        for (let i = 0; i < 8; i++) {
            const x = (i % 4 - 1.5) * 20;
            const z = Math.floor(i / 4) * 25 + 20;
            const harbor = this.createBuilding(`Harbor Building ${i+1}`, x, z, 10, 10, 0x4169e1);
            harbor.userData.buildingType = 'harbor_building';
            harbor.userData.buildingName = `Harbor Building ${i+1}`;
            interior.buildings.push(harbor);
            interior.objects.push(harbor);
        }

        // Fish Market (groß)
        const market = this.createBuilding('Fish Market', -40, 0, 15, 15, 0x00ced1);
        market.userData.buildingType = 'market';
        market.userData.buildingName = 'Fish Market';
        interior.buildings.push(market);
        interior.objects.push(market);

        // Ships (5 Stück) - große Objekte am Hafen
        for (let i = 0; i < 5; i++) {
            const x = (i - 2) * 25;
            const z = 55;
            const ship = this.createBuilding(`Ship ${i+1}`, x, z, 12, 20, 0x1e90ff);
            ship.userData.buildingType = 'ship';
            ship.userData.buildingName = `Ship ${i+1}`;
            interior.buildings.push(ship);
            interior.objects.push(ship);
        }

        // Houses (20 Stück)
        let houseCount = 0;
        for (let x = -50; x <= 50; x += 20) {
            for (let z = -40; z <= -10; z += 15) {
                if (houseCount >= 20) break;
                const house = this.createBuilding(`House ${houseCount+1}`, x, z, 5, 5, 0x8b4513);
                house.userData.buildingType = 'house';
                house.userData.buildingName = `House ${houseCount+1}`;
                interior.buildings.push(house);
                interior.objects.push(house);
                houseCount++;
            }
        }
    }

    /**
     * RUNENHEIM - Runeheim Interior (Magic Academy)
     * 20 Gebäude: Magic Academy, Rune Shops x3, Totems x5, Houses x11
     */
    generateRuneheimInterior(interior, cityData) {
        // Magic Academy (Zentrum) - groß
        const academy = this.createBuilding('Magic Academy', 0, 0, 25, 25, 0x9b59b6);
        academy.userData.buildingType = 'magic_academy';
        academy.userData.buildingName = 'Magic Academy';
        interior.buildings.push(academy);
        interior.objects.push(academy);

        // Rune Shops (3 Stück)
        for (let i = 0; i < 3; i++) {
            const angle = (i / 3) * Math.PI * 2;
            const radius = 40;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            const shop = this.createBuilding(`Rune Shop ${i+1}`, x, z, 10, 10, 0x8b008b);
            shop.userData.buildingType = 'rune_shop';
            shop.userData.buildingName = `Rune Shop ${i+1}`;
            interior.buildings.push(shop);
            interior.objects.push(shop);
        }

        // Totems (5 Stück) - hohe dünne Strukturen
        for (let i = 0; i < 5; i++) {
            const angle = (i / 5) * Math.PI * 2 + Math.PI / 5;
            const radius = 55;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            const totem = this.createBuilding(`Totem ${i+1}`, x, z, 2, 15, 0xff00ff);
            totem.userData.buildingType = 'totem';
            totem.userData.buildingName = `Totem ${i+1}`;
            interior.buildings.push(totem);
            interior.objects.push(totem);
        }

        // Houses (11 Stück)
        for (let i = 0; i < 11; i++) {
            const angle = (i / 11) * Math.PI * 2;
            const radius = 60;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            const house = this.createBuilding(`House ${i+1}`, x, z, 5, 5, 0x8b4513);
            house.userData.buildingType = 'house';
            house.userData.buildingName = `House ${i+1}`;
            interior.buildings.push(house);
            interior.objects.push(house);
        }
    }

    /**
     * FUNKEN-SIEDLUNG - Spark Settlement Interior (Forge Town)
     * 25 Gebäude: Forges x5, Blacksmith, Lava Docks x2, Fireproof Houses x17
     */
    generateSparkSettlementInterior(interior, cityData) {
        // Master Blacksmith (Zentrum)
        const blacksmith = this.createBuilding('Master Blacksmith', 0, 0, 18, 18, 0xe74c3c);
        blacksmith.userData.buildingType = 'master_blacksmith';
        blacksmith.userData.buildingName = 'Master Blacksmith - Legendary Crafting';
        interior.buildings.push(blacksmith);
        interior.objects.push(blacksmith);

        // Forges (5 Stück)
        for (let i = 0; i < 5; i++) {
            const angle = (i / 5) * Math.PI * 2;
            const radius = 35;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            const forge = this.createBuilding(`Forge ${i+1}`, x, z, 12, 12, 0xff4500);
            forge.userData.buildingType = 'forge';
            forge.userData.buildingName = `Forge ${i+1}`;
            interior.buildings.push(forge);
            interior.objects.push(forge);
        }

        // Lava Docks (2 Stück) - groß
        for (let i = 0; i < 2; i++) {
            const x = (i - 0.5) * 50;
            const z = 50;
            const dock = this.createBuilding(`Lava Dock ${i+1}`, x, z, 20, 15, 0xff6347);
            dock.userData.buildingType = 'lava_dock';
            dock.userData.buildingName = `Lava Dock ${i+1}`;
            interior.buildings.push(dock);
            interior.objects.push(dock);
        }

        // Fireproof Houses (17 Stück)
        let houseCount = 0;
        for (let x = -55; x <= 55; x += 20) {
            for (let z = -50; z <= 30; z += 20) {
                // Skip center (Blacksmith) and forge areas
                if (Math.abs(x) < 20 && Math.abs(z) < 20) continue;
                if (houseCount >= 17) break;

                const house = this.createBuilding(`Fireproof House ${houseCount+1}`, x, z, 6, 6, 0x8b0000);
                house.userData.buildingType = 'house';
                house.userData.buildingName = `Fireproof House ${houseCount+1}`;
                interior.buildings.push(house);
                interior.objects.push(house);
                houseCount++;
            }
        }
    }

    /**
     * Generic Interior (Fallback)
     */
    generateGenericInterior(interior, cityData) {
        // Einfaches Grid mit 10 Gebäuden
        for (let i = 0; i < 10; i++) {
            const x = (i % 5 - 2) * 20;
            const z = Math.floor(i / 5) * 20;
            const building = this.createBuilding(`Building ${i+1}`, x, z, 8, 8, 0x888888);
            building.userData.buildingType = 'generic';
            building.userData.buildingName = `Building ${i+1}`;
            interior.buildings.push(building);
            interior.objects.push(building);
        }
    }

    /**
     * Erstellt ein Gebäude-Mesh
     */
    createBuilding(name, x, z, width, height, color) {
        const geometry = new this.THREE.BoxGeometry(width, height, width);
        const material = new this.THREE.MeshStandardMaterial({
            color: color,
            roughness: 0.7,
            metalness: 0.3
        });
        const building = new this.THREE.Mesh(geometry, material);
        building.position.set(x, height / 2, z);
        building.castShadow = true;
        building.receiveShadow = true;
        building.name = name;
        return building;
    }

    /**
     * Erstellt Exit-Portal
     */
    createExitPortal(cityName) {
        const geometry = new this.THREE.BoxGeometry(10, 15, 2);
        const material = new this.THREE.MeshStandardMaterial({
            color: 0x00ff00,
            emissive: 0x00ff00,
            emissiveIntensity: 0.5,
            transparent: true,
            opacity: 0.7
        });
        const portal = new this.THREE.Mesh(geometry, material);
        portal.position.set(0, 7.5, -60); // Am Rand
        portal.name = 'exit_portal';
        portal.userData.isExitPortal = true;
        portal.userData.cityName = cityName;

        // Pulsing Animation (später in Animation-Loop)
        portal.userData.animationOffset = Math.random() * Math.PI * 2;

        return portal;
    }

    /**
     * Fügt Interior-Beleuchtung hinzu
     */
    addInteriorLighting(interior, cityData) {
        // Ambient Light (heller für Interior)
        const ambientLight = new this.THREE.AmbientLight(0xffffff, 0.8);
        ambientLight.name = 'interior_ambient';
        interior.objects.push(ambientLight);

        // Directional Light (von oben)
        const dirLight = new this.THREE.DirectionalLight(0xffffff, 0.6);
        dirLight.position.set(50, 100, 50);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 1024;
        dirLight.shadow.mapSize.height = 1024;
        dirLight.shadow.camera.left = -70;
        dirLight.shadow.camera.right = 70;
        dirLight.shadow.camera.top = 70;
        dirLight.shadow.camera.bottom = -70;
        dirLight.name = 'interior_directional';
        interior.objects.push(dirLight);

        // Point Lights bei wichtigen Gebäuden
        interior.buildings.slice(0, 10).forEach((building, i) => {
            const pointLight = new this.THREE.PointLight(0xffa500, 0.5, 30);
            pointLight.position.copy(building.position);
            pointLight.position.y += 15;
            pointLight.castShadow = true;
            pointLight.name = `interior_pointlight_${i}`;
            interior.objects.push(pointLight);
        });
    }

    /**
     * Fügt unsichtbare Wände/Grenzen hinzu
     */
    addInteriorBounds(interior) {
        // Unsichtbare Box um Interior herum (für Collision Detection)
        const boundSize = this.interiorSize / 2;
        const bounds = [
            { x: 0, z: boundSize, width: this.interiorSize, depth: 1 },  // Nord
            { x: 0, z: -boundSize, width: this.interiorSize, depth: 1 }, // Süd
            { x: boundSize, z: 0, width: 1, depth: this.interiorSize },  // Ost
            { x: -boundSize, z: 0, width: 1, depth: this.interiorSize }  // West
        ];

        bounds.forEach((bound, i) => {
            const geometry = new this.THREE.BoxGeometry(bound.width, 20, bound.depth);
            const material = new this.THREE.MeshBasicMaterial({
                color: 0xff0000,
                transparent: true,
                opacity: 0, // Unsichtbar
                wireframe: false
            });
            const wall = new this.THREE.Mesh(geometry, material);
            wall.position.set(bound.x, 10, bound.z);
            wall.name = `interior_bound_${i}`;
            wall.userData.isWall = true;
            interior.objects.push(wall);
        });
    }

    /**
     * Gibt Boden-Farbe für Stadt zurück
     */
    getCityGroundColor(cityName) {
        const colors = {
            'Handelsfestung': 0xd2b48c,   // Tan (Arena-Sand)
            'Dampf-Hain': 0x90ee90,       // Light Green (Gras)
            'Salzige Bucht': 0xffd700,    // Gold (Sand am Strand)
            'Runenheim': 0x9370db,        // Medium Purple (Magic)
            'Funken-Siedlung': 0x8b4513   // Saddle Brown (Vulkan-Stein)
        };
        return colors[cityName] || 0x808080; // Default: Gray
    }

    /**
     * Lädt Interior in Szene
     */
    loadInterior(interior) {
        interior.objects.forEach(obj => {
            this.scene.add(obj);
            this.interiorObjects.push(obj);
        });
        this.currentInterior = interior;
    }

    /**
     * Entfernt Interior aus Szene
     */
    unloadInterior() {
        if (!this.currentInterior) return;

        this.interiorObjects.forEach(obj => {
            this.scene.remove(obj);
            // Dispose materials and geometries
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) {
                if (Array.isArray(obj.material)) {
                    obj.material.forEach(mat => mat.dispose());
                } else {
                    obj.material.dispose();
                }
            }
        });

        this.interiorObjects = [];
        this.currentInterior = null;
    }

    /**
     * Spawnt NPCs im aktuellen Interior
     * @param {NPCSystem} npcSystem - NPC System Instance
     * @param {string} cityId - City ID (handelsfestung, dampf_hain, etc.)
     * @param {Object} cityData - City Data
     */
    spawnNPCsInInterior(npcSystem, cityId, cityData) {
        if (!this.currentInterior) {
            console.warn('⚠️ Kein aktives Interior, NPCs können nicht gespawned werden');
            return [];
        }

        const interiorBounds = {
            width: this.interiorSize,
            depth: this.interiorSize
        };

        const npcs = npcSystem.spawnNPCsForCity(cityId, cityData, interiorBounds);
        this.currentInterior.npcs = npcs;

        console.log(`🧑 ${npcs.length} NPCs gespawned in ${cityData.name}`);
        return npcs;
    }

    /**
     * Gibt aktuelles Interior zurück
     */
    getCurrentInterior() {
        return this.currentInterior;
    }
}

// Export für Module (falls verwendet)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InteriorGenerator;
}
