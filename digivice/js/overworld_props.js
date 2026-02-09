// OVERWORLD PROP GENERATOR - Biome-aware random props for living world
// Jedes Verlassen von Gebäuden/Städten generiert neue Außenwelt!
(function() {
    'use strict';

    // ==========================================
    // SEEDED RANDOM (gleich wie dungeon_generator.js)
    // ==========================================
    let seed = Date.now();

    function seededRandom() {
        seed = (seed * 1664525 + 1013904223) % 4294967296;
        return seed / 4294967296;
    }

    function randomInt(min, max) {
        return Math.floor(seededRandom() * (max - min + 1)) + min;
    }

    function randomFloat(min, max) {
        return seededRandom() * (max - min) + min;
    }

    function pickRandom(array) {
        return array[randomInt(0, array.length - 1)];
    }

    function weightedPick(items) {
        const totalWeight = items.reduce((sum, item) => sum + (item.weight || 1), 0);
        let roll = seededRandom() * totalWeight;
        for (const item of items) {
            roll -= (item.weight || 1);
            if (roll <= 0) return item;
        }
        return items[items.length - 1];
    }

    // ==========================================
    // ASSET PFADE (verifiziert vorhanden!)
    // ==========================================

    // Medieval Props (KayKit_Medieval_Hexagon_Pack)
    const MEDIEVAL_PROPS = 'KayKit_Medieval_Hexagon_Pack_1.0_FREE/Assets/gltf/decoration/props/';
    // Medieval Buildings
    const MEDIEVAL_BUILD = 'kaykit/medieval/';
    // Nature
    const NATURE = 'kaykit/nature/';

    // ==========================================
    // BIOME-SPEZIFISCHE PROP-TABELLEN
    // ==========================================

    const BIOME_PROPS = {
        // === SAMTMOOS-TIEFWALD (Wald) ===
        samtmoos: {
            singles: [
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 3, scale: [2.5, 4.0] },
                { path: MEDIEVAL_PROPS + 'barrel.gltf', weight: 2, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'sack.gltf', weight: 2, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'weaponrack.gltf', weight: 1, scale: [2.0, 3.0] },
                { path: MEDIEVAL_PROPS + 'crate_A_big.gltf', weight: 2, scale: [1.5, 2.5] },
                { path: NATURE + 'Tree_1_A_Color1.gltf', weight: 4, scale: [3.0, 6.0] },
                { path: NATURE + 'Tree_2_A_Color1.gltf', weight: 3, scale: [3.0, 5.0] },
                { path: NATURE + 'Bush_1_A_Color1.gltf', weight: 3, scale: [2.0, 4.0] },
                { path: NATURE + 'Rock_1_A_Color1.gltf', weight: 2, scale: [2.0, 5.0] },
            ],
            clusters: [
                { name: 'Banditenlager', items: ['tent.gltf', 'barrel.gltf', 'weaponrack.gltf', 'sack.gltf'], chance: 0.25 },
                { name: 'Haendler-Camp', items: ['tent.gltf', 'crate_A_big.gltf', 'crate_A_small.gltf', 'sack.gltf'], chance: 0.2 },
                { name: 'Waldlichtung', items: ['tent.gltf', 'barrel.gltf', 'ladder.gltf'], chance: 0.15 },
            ],
            density: 0.4,
            maxProps: 50
        },

        // === HEISSE DÜNEN (Wüste) ===
        heisse_duenen: {
            singles: [
                { path: MEDIEVAL_BUILD + 'building_destroyed.gltf', weight: 3, scale: [3.0, 5.0] },
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 3, scale: [2.5, 4.0] },
                { path: NATURE + 'Rock_1_C_Color1.gltf', weight: 4, scale: [3.0, 7.0] },
                { path: NATURE + 'Rock_1_F_Color1.gltf', weight: 3, scale: [2.0, 5.0] },
                { path: MEDIEVAL_PROPS + 'wheelbarrow.gltf', weight: 2, scale: [2.0, 3.0] },
                { path: MEDIEVAL_PROPS + 'barrel.gltf', weight: 1, scale: [1.5, 2.5] },
            ],
            clusters: [
                { name: 'Wuestenruine', items: ['building_destroyed.gltf', 'barrel.gltf', 'crate_open.gltf'], chance: 0.3 },
                { name: 'Nomadenlager', items: ['tent.gltf', 'wheelbarrow.gltf', 'sack.gltf'], chance: 0.25 },
            ],
            density: 0.15,
            maxProps: 25
        },

        // === SALZWIND (Küste) ===
        salzwind: {
            singles: [
                { path: MEDIEVAL_PROPS + 'barrel.gltf', weight: 4, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'crate_long_A.gltf', weight: 3, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'pallet.gltf', weight: 2, scale: [2.0, 3.0] },
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 2, scale: [2.5, 4.0] },
                { path: NATURE + 'Rock_1_B_Color1.gltf', weight: 3, scale: [2.0, 5.0] },
                { path: NATURE + 'Bush_2_A_Color1.gltf', weight: 2, scale: [2.0, 3.0] },
            ],
            clusters: [
                { name: 'Fischer-Camp', items: ['tent.gltf', 'barrel.gltf', 'barrel.gltf', 'crate_long_A.gltf'], chance: 0.3 },
                { name: 'Strandgut', items: ['pallet.gltf', 'barrel.gltf', 'crate_open.gltf'], chance: 0.25 },
            ],
            density: 0.2,
            maxProps: 30
        },

        // === MAGMASTRÖME (Vulkan) ===
        magmastroeme: {
            singles: [
                { path: MEDIEVAL_BUILD + 'building_destroyed.gltf', weight: 3, scale: [3.0, 5.0] },
                { path: NATURE + 'Rock_1_D_Color1.gltf', weight: 5, scale: [3.0, 8.0] },
                { path: NATURE + 'Rock_1_E_Color1.gltf', weight: 4, scale: [2.0, 6.0] },
                { path: MEDIEVAL_PROPS + 'barrel.gltf', weight: 1, scale: [1.5, 2.5] },
            ],
            clusters: [
                { name: 'Schmiedelager', items: ['barrel.gltf', 'crate_A_big.gltf', 'weaponrack.gltf'], chance: 0.2 },
                { name: 'Verbrannte-Ruine', items: ['building_destroyed.gltf', 'barrel.gltf'], chance: 0.3 },
            ],
            density: 0.12,
            maxProps: 20
        },

        // === GRÜNSCHLAMM (Sumpf) ===
        gruenschlamm: {
            singles: [
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 2, scale: [2.0, 3.5] },
                { path: NATURE + 'Bush_1_C_Color1.gltf', weight: 4, scale: [2.0, 4.0] },
                { path: NATURE + 'Bush_1_E_Color1.gltf', weight: 3, scale: [2.0, 4.0] },
                { path: NATURE + 'Tree_3_A_Color1.gltf', weight: 3, scale: [3.0, 5.0] },
                { path: NATURE + 'Rock_1_G_Color1.gltf', weight: 2, scale: [2.0, 5.0] },
                { path: MEDIEVAL_PROPS + 'barrel.gltf', weight: 1, scale: [1.5, 2.5] },
            ],
            clusters: [
                { name: 'Druidenlager', items: ['tent.gltf', 'barrel.gltf', 'sack.gltf'], chance: 0.2 },
                { name: 'Sumpfhuette', items: ['tent.gltf', 'crate_A_small.gltf', 'ladder.gltf'], chance: 0.15 },
            ],
            density: 0.25,
            maxProps: 35
        },

        // === BLITZEBENE (Steppe/Plains) ===
        blitzebene: {
            singles: [
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 3, scale: [2.5, 4.0] },
                { path: MEDIEVAL_PROPS + 'wheelbarrow.gltf', weight: 3, scale: [2.0, 3.5] },
                { path: MEDIEVAL_PROPS + 'flag_red.gltf', weight: 2, scale: [2.0, 3.0] },
                { path: MEDIEVAL_PROPS + 'flag_yellow.gltf', weight: 2, scale: [2.0, 3.0] },
                { path: NATURE + 'Rock_1_H_Color1.gltf', weight: 3, scale: [2.0, 5.0] },
                { path: NATURE + 'Bush_2_B_Color1.gltf', weight: 2, scale: [2.0, 3.0] },
            ],
            clusters: [
                { name: 'Planwagen-Camp', items: ['wheelbarrow.gltf', 'tent.gltf', 'barrel.gltf', 'sack.gltf'], chance: 0.3 },
                { name: 'Nomaden-Rast', items: ['tent.gltf', 'flag_red.gltf', 'barrel.gltf'], chance: 0.25 },
            ],
            density: 0.2,
            maxProps: 30
        },

        // === TIEFENHÖHLEN (Caves/Mountains) ===
        tiefenhoehlen: {
            singles: [
                { path: NATURE + 'Rock_1_I_Color1.gltf', weight: 5, scale: [3.0, 8.0] },
                { path: NATURE + 'Rock_1_J_Color1.gltf', weight: 4, scale: [2.0, 6.0] },
                { path: MEDIEVAL_PROPS + 'barrel.gltf', weight: 1, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'crate_B_big.gltf', weight: 1, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'ladder.gltf', weight: 1, scale: [2.0, 3.0] },
            ],
            clusters: [
                { name: 'Bergbau-Camp', items: ['tent.gltf', 'barrel.gltf', 'crate_B_big.gltf', 'ladder.gltf'], chance: 0.2 },
            ],
            density: 0.15,
            maxProps: 20
        },

        // === REICH DER DREI (Eis/Schnee) ===
        reich_der_drei: {
            singles: [
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 2, scale: [2.5, 4.0] },
                { path: MEDIEVAL_BUILD + 'building_destroyed.gltf', weight: 2, scale: [3.0, 5.0] },
                { path: NATURE + 'Tree_1_B_Color1.gltf', weight: 3, scale: [3.0, 5.0] },
                { path: NATURE + 'Rock_1_A_Color1.gltf', weight: 3, scale: [2.0, 6.0] },
                { path: MEDIEVAL_PROPS + 'flag_blue.gltf', weight: 2, scale: [2.0, 3.0] },
            ],
            clusters: [
                { name: 'Winterlager', items: ['tent.gltf', 'barrel.gltf', 'flag_blue.gltf', 'sack.gltf'], chance: 0.25 },
                { name: 'Verschneite-Ruine', items: ['building_destroyed.gltf', 'barrel.gltf', 'crate_A_small.gltf'], chance: 0.2 },
            ],
            density: 0.15,
            maxProps: 25
        },

        // === GÖTTERFELS (Safe Zone - Händler & Leben) ===
        goetterfels: {
            singles: [
                { path: MEDIEVAL_PROPS + 'tent.gltf', weight: 3, scale: [2.5, 4.0] },
                { path: MEDIEVAL_PROPS + 'crate_A_big.gltf', weight: 2, scale: [1.5, 2.5] },
                { path: MEDIEVAL_PROPS + 'wheelbarrow.gltf', weight: 2, scale: [2.0, 3.0] },
                { path: MEDIEVAL_PROPS + 'target.gltf', weight: 1, scale: [2.0, 3.0] },
                { path: NATURE + 'Bush_1_B_Color1.gltf', weight: 2, scale: [2.0, 3.0] },
                { path: NATURE + 'Tree_2_C_Color1.gltf', weight: 2, scale: [3.0, 5.0] },
            ],
            clusters: [
                { name: 'Marktstand', items: ['tent.gltf', 'crate_A_big.gltf', 'barrel.gltf', 'sack.gltf'], chance: 0.3 },
                { name: 'Uebungsplatz', items: ['target.gltf', 'weaponrack.gltf', 'barrel.gltf'], chance: 0.2 },
            ],
            density: 0.3,
            maxProps: 40
        }
    };

    // Fallback
    BIOME_PROPS['default'] = BIOME_PROPS.samtmoos;

    // ==========================================
    // BIOME-ERKENNUNG (Position → Biome)
    // ==========================================

    function getBiomeAtPosition(x, z) {
        // Nutze overworld_enemies.js getCurrentBiome() wenn vorhanden
        if (window.OverworldEnemies && window.OverworldEnemies.getCurrentBiome) {
            return window.OverworldEnemies.getCurrentBiome({ x, z });
        }

        // Fallback: Winkel-basierte Sektoren (gleich wie overworld_enemies.js)
        const cx = 4800, cz = 4800; // World center
        const dx = x - cx, dz = z - cz;
        const dist = Math.sqrt(dx * dx + dz * dz);

        // Götterfels = Zentrum (< 500 radius)
        if (dist < 500) return 'goetterfels';

        const angle = (Math.atan2(dz, dx) * 180 / Math.PI + 360) % 360;

        if (angle < 45) return 'samtmoos';
        if (angle < 90) return 'reich_der_drei';
        if (angle < 135) return 'heisse_duenen';
        if (angle < 180) return 'salzwind';
        if (angle < 225) return 'magmastroeme';
        if (angle < 270) return 'gruenschlamm';
        if (angle < 315) return 'blitzebene';
        return 'tiefenhoehlen';
    }

    // ==========================================
    // GEBÄUDE-AUSSCHLUSS (keine Props auf Gebäuden)
    // ==========================================

    const BUILDING_POSITIONS = [
        { x: 0, z: 0, radius: 150 },          // Schwarze Mühle
        { x: -2000, z: -2000, radius: 120 },   // Kampfarena
        { x: 2000, z: 2000, radius: 100 },     // Gartenhaus + Garten
        { x: -3000, z: -3000, radius: 100 },   // Dungeon 1
        { x: 3000, z: -3000, radius: 100 },    // Dungeon 2
        { x: 0, z: 3000, radius: 100 },        // Dungeon 3
        { x: 2500, z: 2500, radius: 120 },     // Kristallteich
        { x: -2500, z: -2500, radius: 170 },   // Weltensee
    ];

    function isNearBuilding(x, z) {
        for (const b of BUILDING_POSITIONS) {
            const dist = Math.sqrt((x - b.x) ** 2 + (z - b.z) ** 2);
            if (dist < b.radius) return true;
        }
        return false;
    }

    // ==========================================
    // CAMPFIRE BUILDER (kein Asset vorhanden → Primitives)
    // ==========================================

    function createCampfire(scale = 1.0) {
        const group = new THREE.Group();

        // Steinring
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const stone = new THREE.Mesh(
                new THREE.SphereGeometry(0.3 * scale, 6, 4),
                new THREE.MeshStandardMaterial({ color: 0x666666, roughness: 0.9 })
            );
            stone.position.set(Math.cos(angle) * 0.8 * scale, 0.15 * scale, Math.sin(angle) * 0.8 * scale);
            stone.castShadow = true;
            group.add(stone);
        }

        // Holzscheite
        for (let i = 0; i < 3; i++) {
            const log = new THREE.Mesh(
                new THREE.CylinderGeometry(0.12 * scale, 0.12 * scale, 1.2 * scale),
                new THREE.MeshStandardMaterial({ color: 0x8B4513 })
            );
            log.rotation.z = Math.PI / 2;
            log.rotation.y = (i / 3) * Math.PI;
            log.position.y = 0.2 * scale;
            group.add(log);
        }

        // Feuer (Glow)
        const fire = new THREE.Mesh(
            new THREE.ConeGeometry(0.4 * scale, 1.0 * scale, 8),
            new THREE.MeshStandardMaterial({
                color: 0xff4400,
                emissive: 0xff6600,
                emissiveIntensity: 2.0,
                transparent: true,
                opacity: 0.85
            })
        );
        fire.position.y = 0.5 * scale;
        group.add(fire);

        // Licht
        const light = new THREE.PointLight(0xff6633, 1.5, 30 * scale);
        light.position.y = 1.0 * scale;
        group.add(light);

        return group;
    }

    // ==========================================
    // HAUPT-GENERATOR
    // ==========================================

    const GLTF_CACHE = {}; // Gecachte Templates
    let loadingCount = 0;

    function loadModelCached(path, callback) {
        if (GLTF_CACHE[path]) {
            callback(GLTF_CACHE[path].clone());
            return;
        }

        if (!window.THREE || !THREE.GLTFLoader) {
            callback(null);
            return;
        }

        const loader = new THREE.GLTFLoader();
        loadingCount++;

        loader.load('/assets/' + path, (gltf) => {
            GLTF_CACHE[path] = gltf.scene;
            callback(gltf.scene.clone());
            loadingCount--;
        }, undefined, (err) => {
            // console.warn('Prop load failed:', path);
            callback(null);
            loadingCount--;
        });
    }

    /**
     * Hauptfunktion: Generiere Overworld-Props
     * @param {THREE.Group} worldGroup - roomGroup aus buildRoom()
     * @param {number} worldSize - 9600
     * @returns {number} Anzahl platzierter Props
     */
    function generateOverworldProps(worldGroup, worldSize = 9600) {
        seed = Date.now(); // Neuer Seed = neue Welt!
        let totalPlaced = 0;
        const MAX_TOTAL = 200; // Performance-Limit

        const CHUNK_SIZE = 400;
        const PROP_RADIUS = 2400; // 2.4km Radius

        console.log(`🌍 Generating overworld props (seed: ${seed})...`);

        for (let cx = -PROP_RADIUS; cx < PROP_RADIUS; cx += CHUNK_SIZE) {
            for (let cz = -PROP_RADIUS; cz < PROP_RADIUS; cz += CHUNK_SIZE) {
                if (totalPlaced >= MAX_TOTAL) break;

                const biome = getBiomeAtPosition(cx + CHUNK_SIZE / 2, cz + CHUNK_SIZE / 2);
                const config = BIOME_PROPS[biome] || BIOME_PROPS['default'];

                // Einzelne Props
                const propsInChunk = Math.floor(config.density * (CHUNK_SIZE / 100) * (CHUNK_SIZE / 100));

                for (let i = 0; i < propsInChunk && totalPlaced < MAX_TOTAL; i++) {
                    const x = cx + randomFloat(20, CHUNK_SIZE - 20);
                    const z = cz + randomFloat(20, CHUNK_SIZE - 20);

                    if (isNearBuilding(x, z)) continue;

                    const propDef = weightedPick(config.singles);
                    const scale = randomFloat(propDef.scale[0], propDef.scale[1]);
                    const rotation = randomFloat(0, Math.PI * 2);

                    placeProp(worldGroup, propDef.path, x, z, scale, rotation);
                    totalPlaced++;
                }

                // Cluster (Camps, Ruinen etc.)
                for (const cluster of config.clusters) {
                    if (seededRandom() < cluster.chance && totalPlaced < MAX_TOTAL - cluster.items.length) {
                        const clusterX = cx + randomFloat(50, CHUNK_SIZE - 50);
                        const clusterZ = cz + randomFloat(50, CHUNK_SIZE - 50);

                        if (isNearBuilding(clusterX, clusterZ)) continue;

                        placeCluster(worldGroup, cluster, clusterX, clusterZ);
                        totalPlaced += cluster.items.length + 1; // +1 für Campfire

                        console.log(`🏕️ ${cluster.name} bei [${Math.round(clusterX)}, ${Math.round(clusterZ)}] (${biome})`);
                    }
                }

                // Zufällige Lagerfeuer (10% Chance pro Chunk)
                if (seededRandom() < 0.1 && totalPlaced < MAX_TOTAL) {
                    const fx = cx + randomFloat(50, CHUNK_SIZE - 50);
                    const fz = cz + randomFloat(50, CHUNK_SIZE - 50);
                    if (!isNearBuilding(fx, fz)) {
                        const campfire = createCampfire(randomFloat(1.0, 2.0));
                        campfire.position.set(fx, 0, fz);
                        worldGroup.add(campfire);
                        totalPlaced++;
                    }
                }
            }
        }

        console.log(`🌍 Overworld Props generiert: ${totalPlaced} (Seed: ${seed})`);
        return totalPlaced;
    }

    function placeProp(group, assetPath, x, z, scale, rotation) {
        loadModelCached(assetPath, (model) => {
            if (model) {
                model.scale.set(scale, scale, scale);
                model.position.set(x, 0, z);
                model.rotation.y = rotation;
                model.traverse(n => {
                    if (n.isMesh) {
                        n.castShadow = true;
                        n.receiveShadow = true;
                    }
                });
                group.add(model);
            } else {
                // Fallback: Farbige Box
                const colors = [0x8B4513, 0x556B2F, 0x696969, 0x4682B4];
                const geo = new THREE.BoxGeometry(
                    randomFloat(1, 3) * scale * 0.3,
                    randomFloat(1, 4) * scale * 0.3,
                    randomFloat(1, 3) * scale * 0.3
                );
                const mat = new THREE.MeshStandardMaterial({
                    color: pickRandom(colors),
                    roughness: 0.9
                });
                const mesh = new THREE.Mesh(geo, mat);
                mesh.position.set(x, geo.parameters.height / 2, z);
                mesh.rotation.y = rotation;
                mesh.castShadow = true;
                group.add(mesh);
            }
        });
    }

    function placeCluster(group, cluster, cx, cz) {
        const spacing = 8;

        // Items im Kreis um das Zentrum
        cluster.items.forEach((itemName, i) => {
            const angle = (i / cluster.items.length) * Math.PI * 2 + randomFloat(-0.3, 0.3);
            const dist = spacing + randomFloat(-2, 2);
            const x = cx + Math.cos(angle) * dist;
            const z = cz + Math.sin(angle) * dist;
            const scale = randomFloat(2.0, 3.5);
            const rotation = randomFloat(0, Math.PI * 2);

            // Bestimme vollen Pfad
            const path = itemName.includes('/') ? itemName : MEDIEVAL_PROPS + itemName;
            placeProp(group, path, x, z, scale, rotation);
        });

        // Lagerfeuer in der Mitte des Clusters
        const campfire = createCampfire(randomFloat(1.0, 1.8));
        campfire.position.set(cx, 0, cz);
        group.add(campfire);
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    window.OverworldProps = {
        generateOverworldProps,
        getBiomeAtPosition,
        createCampfire,
        clearCache: () => { Object.keys(GLTF_CACHE).forEach(k => delete GLTF_CACHE[k]); }
    };

    console.log('🌍 Overworld Props System loaded - Lebendige Welt bei jedem Verlassen!');
})();
