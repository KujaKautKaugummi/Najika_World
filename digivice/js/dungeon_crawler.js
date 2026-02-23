// DUNGEON CRAWLER - First-Person Grid-Based Dungeon (Hexen/Daggerfall Style!)
// Typ B Dungeon: Spieler bewegt sich Tile für Tile durch Korridore in First-Person
(function() {
    'use strict';

    // ==========================================
    // CONSTANTS
    // ==========================================

    const TILE_SIZE = 6;    // Jedes Tile ist 6x6 Units
    const WALL_HEIGHT = 6;  // Wandhöhe

    // Zell-Typen
    const CELL = {
        WALL: 0,
        FLOOR: 1,
        DOOR: 2,
        ENEMY: 3,
        LOOT: 4,
        ENTRANCE: 5,
        EXIT: 6
    };

    // Richtungen: 0=Nord(-Z), 1=Ost(+X), 2=Süd(+Z), 3=West(-X)
    const DIR_OFFSETS = [
        { dx: 0, dz: -1 },  // Nord
        { dx: 1, dz: 0 },   // Ost
        { dx: 0, dz: 1 },   // Süd
        { dx: -1, dz: 0 }   // West
    ];

    const DIR_ROTATIONS = [0, Math.PI / 2, Math.PI, -Math.PI / 2]; // Y-Rotation für Wände

    // KayKit Dungeon Pack Assets
    const DUNGEON_PACK = 'KayKit Dungeon Pack 1.0/Models/gltf/';
    const ASSETS = {
        wall: DUNGEON_PACK + 'wall.gltf.glb',
        wall_broken: DUNGEON_PACK + 'wall_broken.gltf.glb',
        wall_door: DUNGEON_PACK + 'wall_door.gltf.glb',
        wall_window: DUNGEON_PACK + 'wall_window.gltf.glb',
        wall_torch: DUNGEON_PACK + 'torchWall.gltf.glb',
        floor: DUNGEON_PACK + 'floorDecoration_tilesLarge.gltf.glb',
        floor_wood: DUNGEON_PACK + 'floorDecoration_wood.gltf.glb',
        pillar: DUNGEON_PACK + 'pillar.gltf.glb',
        door: DUNGEON_PACK + 'door.gltf.glb',
        stairs: DUNGEON_PACK + 'stairs.gltf.glb',
        torch: DUNGEON_PACK + 'torch.gltf.glb',
        chest: DUNGEON_PACK + 'chest_common.gltf.glb',
        chest_rare: DUNGEON_PACK + 'chest_rare.gltf.glb',
        barrel: DUNGEON_PACK + 'barrel.gltf.glb',
    };

    // ==========================================
    // STATE
    // ==========================================

    let crawlerActive = false;
    let gridMap = null;
    let gridWidth = 0;
    let gridHeight = 0;
    let dungeonGroup = null;
    let dungeonLevel = 1;

    // Player State
    let playerGridX = 1;
    let playerGridZ = 1;
    let playerFacing = 2; // Start: Süd
    let isMoving = false;
    let isRotating = false;

    // Combat encounters
    let enemiesDefeated = 0;
    let lootsCollected = 0;

    // Input handler reference
    let inputHandler = null;

    // HUD
    let crawlerHUD = null;

    // Seeded Random
    let seed = Date.now();
    function seededRandom() {
        seed = (seed * 1664525 + 1013904223) % 4294967296;
        return seed / 4294967296;
    }
    function randomInt(min, max) {
        return Math.floor(seededRandom() * (max - min + 1)) + min;
    }

    // ==========================================
    // MAZE GENERATION (Recursive Backtracker)
    // ==========================================

    function generateMaze(width, height, level) {
        // Ungerade Größen für den Algorithmus
        if (width % 2 === 0) width++;
        if (height % 2 === 0) height++;

        const grid = Array.from({ length: height }, () => Array(width).fill(CELL.WALL));

        // Recursive backtracker
        function shuffle(arr) {
            for (let i = arr.length - 1; i > 0; i--) {
                const j = randomInt(0, i);
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            return arr;
        }

        function carve(x, z) {
            grid[z][x] = CELL.FLOOR;
            const dirs = shuffle([[0, -2], [0, 2], [-2, 0], [2, 0]]);
            for (const [dx, dz] of dirs) {
                const nx = x + dx, nz = z + dz;
                if (nx > 0 && nx < width - 1 && nz > 0 && nz < height - 1 && grid[nz][nx] === CELL.WALL) {
                    grid[z + dz / 2][x + dx / 2] = CELL.FLOOR; // Passage
                    carve(nx, nz);
                }
            }
        }

        carve(1, 1);

        // Eingang und Ausgang
        grid[1][1] = CELL.ENTRANCE;

        // Ausgang: am weitesten entfernter Punkt (Bottom-Right-Ecke suchen)
        let exitX = width - 2, exitZ = height - 2;
        // Falls die Zelle WALL ist, suche nächste FLOOR-Zelle
        while (grid[exitZ][exitX] === CELL.WALL && exitZ > 1) {
            exitZ -= 2;
        }
        while (grid[exitZ][exitX] === CELL.WALL && exitX > 1) {
            exitX -= 2;
        }
        grid[exitZ][exitX] = CELL.EXIT;

        // Gegner platzieren
        const enemyCount = Math.min(3 + level * 2, 15);
        let placed = 0;
        let attempts = 0;
        while (placed < enemyCount && attempts < 500) {
            const ex = randomInt(1, width - 2);
            const ez = randomInt(1, height - 2);
            if (grid[ez][ex] === CELL.FLOOR) {
                grid[ez][ex] = CELL.ENEMY;
                placed++;
            }
            attempts++;
        }

        // Loot platzieren
        const lootCount = Math.min(1 + Math.floor(level / 2), 5);
        placed = 0;
        attempts = 0;
        while (placed < lootCount && attempts < 300) {
            const lx = randomInt(1, width - 2);
            const lz = randomInt(1, height - 2);
            if (grid[lz][lx] === CELL.FLOOR) {
                grid[lz][lx] = CELL.LOOT;
                placed++;
            }
            attempts++;
        }

        return grid;
    }

    // ==========================================
    // 3D WORLD BUILDER
    // ==========================================

    const modelCache = {};

    function loadModel(path) {
        return new Promise((resolve) => {
            if (modelCache[path]) {
                resolve(modelCache[path].clone());
                return;
            }
            if (!window.THREE || !THREE.GLTFLoader) {
                resolve(null);
                return;
            }
            const loader = new THREE.GLTFLoader();
            loader.load('/assets/' + path, (gltf) => {
                modelCache[path] = gltf.scene;
                resolve(gltf.scene.clone());
            }, undefined, () => resolve(null));
        });
    }

    function createFallbackWall() {
        const mesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SIZE, WALL_HEIGHT, 0.5),
            new THREE.MeshStandardMaterial({ color: 0x444455, roughness: 0.9 })
        );
        mesh.position.y = WALL_HEIGHT / 2;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        return mesh;
    }

    function createFallbackFloor() {
        const mesh = new THREE.Mesh(
            new THREE.PlaneGeometry(TILE_SIZE, TILE_SIZE),
            new THREE.MeshStandardMaterial({ color: 0x333340, roughness: 0.95 })
        );
        mesh.rotation.x = -Math.PI / 2;
        mesh.receiveShadow = true;
        return mesh;
    }

    function createFallbackCeiling() {
        const mesh = new THREE.Mesh(
            new THREE.PlaneGeometry(TILE_SIZE, TILE_SIZE),
            new THREE.MeshStandardMaterial({ color: 0x222230, roughness: 0.95 })
        );
        mesh.rotation.x = Math.PI / 2;
        mesh.position.y = WALL_HEIGHT;
        return mesh;
    }

    async function buildDungeonWorld(grid) {
        dungeonGroup = new THREE.Group();
        const height = grid.length;
        const width = grid[0].length;

        // Versuche KayKit Assets zu laden (mit Fallback)
        let wallTemplate = await loadModel(ASSETS.wall);
        let floorTemplate = await loadModel(ASSETS.floor);

        for (let z = 0; z < height; z++) {
            for (let x = 0; x < width; x++) {
                const cell = grid[z][x];
                if (cell === CELL.WALL) continue; // Wände sind leer

                const worldX = x * TILE_SIZE;
                const worldZ = z * TILE_SIZE;

                // BODEN
                if (floorTemplate) {
                    const floor = floorTemplate.clone();
                    floor.position.set(worldX, 0, worldZ);
                    floor.scale.set(TILE_SIZE / 2, 1, TILE_SIZE / 2);
                    dungeonGroup.add(floor);
                } else {
                    const floor = createFallbackFloor();
                    floor.position.set(worldX, 0, worldZ);
                    dungeonGroup.add(floor);
                }

                // DECKE
                const ceiling = createFallbackCeiling();
                ceiling.position.set(worldX, WALL_HEIGHT, worldZ);
                dungeonGroup.add(ceiling);

                // WÄNDE an jeder Seite wo ein WALL-Nachbar ist
                for (let d = 0; d < 4; d++) {
                    const nx = x + DIR_OFFSETS[d].dx;
                    const nz = z + DIR_OFFSETS[d].dz;

                    // Rand oder WALL-Nachbar → Wand platzieren
                    if (nz < 0 || nz >= height || nx < 0 || nx >= width || grid[nz][nx] === CELL.WALL) {
                        let wall;
                        if (wallTemplate) {
                            wall = wallTemplate.clone();
                            wall.scale.set(TILE_SIZE / 2, WALL_HEIGHT / 3, 1);
                        } else {
                            wall = createFallbackWall();
                        }

                        // Wand an der richtigen Kante positionieren
                        const wallX = worldX + DIR_OFFSETS[d].dx * TILE_SIZE / 2;
                        const wallZ = worldZ + DIR_OFFSETS[d].dz * TILE_SIZE / 2;
                        wall.position.set(wallX, wall.position.y || 0, wallZ);
                        wall.rotation.y = DIR_ROTATIONS[d];

                        dungeonGroup.add(wall);
                    }
                }

                // SPEZIAL-OBJEKTE
                if (cell === CELL.ENEMY) {
                    // Rotes Marker-Licht (Gegner-Encounter)
                    const marker = new THREE.Mesh(
                        new THREE.SphereGeometry(0.4, 8, 8),
                        new THREE.MeshStandardMaterial({
                            color: 0xff0000, emissive: 0xff0000, emissiveIntensity: 0.5,
                            transparent: true, opacity: 0.7
                        })
                    );
                    marker.position.set(worldX, 1.5, worldZ);
                    marker.userData.type = 'enemy';
                    marker.userData.gridX = x;
                    marker.userData.gridZ = z;
                    dungeonGroup.add(marker);

                    // Rotes Licht
                    const enemyLight = new THREE.PointLight(0xff2200, 0.5, 15);
                    enemyLight.position.set(worldX, 2, worldZ);
                    dungeonGroup.add(enemyLight);
                }

                if (cell === CELL.LOOT) {
                    // Truhe (versuche KayKit, sonst Fallback)
                    const chest = await loadModel(ASSETS.chest);
                    if (chest) {
                        chest.position.set(worldX, 0, worldZ);
                        chest.scale.set(2, 2, 2);
                        chest.userData.type = 'loot';
                        chest.userData.gridX = x;
                        chest.userData.gridZ = z;
                        dungeonGroup.add(chest);
                    } else {
                        const box = new THREE.Mesh(
                            new THREE.BoxGeometry(1.5, 1, 1),
                            new THREE.MeshStandardMaterial({ color: 0xffd700, emissive: 0xffd700, emissiveIntensity: 0.3 })
                        );
                        box.position.set(worldX, 0.5, worldZ);
                        box.userData.type = 'loot';
                        dungeonGroup.add(box);
                    }

                    // Goldenes Licht
                    const lootLight = new THREE.PointLight(0xffdd00, 0.4, 12);
                    lootLight.position.set(worldX, 1.5, worldZ);
                    dungeonGroup.add(lootLight);
                }

                if (cell === CELL.EXIT) {
                    // Exit Portal (grünes Leuchten)
                    const portal = new THREE.Mesh(
                        new THREE.TorusGeometry(1.5, 0.3, 8, 16),
                        new THREE.MeshStandardMaterial({
                            color: 0x00ff88, emissive: 0x00ff88, emissiveIntensity: 1.0,
                            transparent: true, opacity: 0.8
                        })
                    );
                    portal.position.set(worldX, 3, worldZ);
                    portal.rotation.x = Math.PI / 2;
                    dungeonGroup.add(portal);

                    const exitLight = new THREE.PointLight(0x00ff88, 1.0, 20);
                    exitLight.position.set(worldX, 3, worldZ);
                    dungeonGroup.add(exitLight);
                }

                if (cell === CELL.ENTRANCE) {
                    // Blaues Eingangs-Licht
                    const enterLight = new THREE.PointLight(0x4488ff, 0.8, 20);
                    enterLight.position.set(worldX, 3, worldZ);
                    dungeonGroup.add(enterLight);
                }

                // Zufällige Fackeln an manchen Wänden (20% Chance)
                if (seededRandom() < 0.2) {
                    const torchLight = new THREE.PointLight(0xff8844, 0.6, 15);
                    torchLight.position.set(worldX + randomInt(-2, 2), 3.5, worldZ + randomInt(-2, 2));
                    dungeonGroup.add(torchLight);
                }
            }
        }

        // Ambient Light für Dungeon (sehr dunkel!)
        const ambientLight = new THREE.AmbientLight(0x111122, 0.3);
        dungeonGroup.add(ambientLight);

        // Spieler-Licht (Fackel die mitgeht)
        const playerLight = new THREE.PointLight(0xff9944, 1.2, 25);
        playerLight.position.set(0, 3, 0);
        playerLight.userData.isPlayerLight = true;
        dungeonGroup.add(playerLight);

        return dungeonGroup;
    }

    // ==========================================
    // DUNGEON ENTER / EXIT
    // ==========================================

    async function enterCrawlerDungeon(level = 1, scene) {
        if (crawlerActive) return;

        dungeonLevel = level;
        seed = Date.now() + level * 777;
        enemiesDefeated = 0;
        lootsCollected = 0;

        console.log(`🏰 Crawler Dungeon Level ${level} betreten!`);

        // Grid generieren
        const size = Math.min(11 + level * 2, 25); // 11x11 bis 25x25
        gridMap = generateMaze(size, size, level);
        gridWidth = gridMap[0].length;
        gridHeight = gridMap.length;

        // Spieler-Position
        playerGridX = 1;
        playerGridZ = 1;
        playerFacing = 2; // Süd

        // 3D Welt bauen
        const group = await buildDungeonWorld(gridMap);
        scene.add(group);

        // Spieler positionieren
        if (window.character) {
            window.character.position.set(
                playerGridX * TILE_SIZE,
                0,
                playerGridZ * TILE_SIZE
            );
        }

        // First-Person Kamera aktivieren
        if (window.Scene3D && window.Scene3D.setCameraMode) {
            Scene3D.setCameraMode('first');
        }

        crawlerActive = true;
        setupInput();
        createCrawlerHUD();
        updateHUD();

        if (typeof showNotification === 'function') {
            showNotification(`🏰 Labyrinth Lv.${level} betreten! Finde den Ausgang! (${gridWidth}x${gridHeight})`, 3000);
        }
    }

    function exitCrawlerDungeon() {
        if (!crawlerActive) return;

        console.log('🚪 Crawler Dungeon verlassen!');
        crawlerActive = false;

        // Input entfernen
        if (inputHandler) {
            window.removeEventListener('keydown', inputHandler);
            inputHandler = null;
        }

        // HUD entfernen
        removeCrawlerHUD();

        // 3D Welt entfernen
        if (dungeonGroup) {
            const parentScene = dungeonGroup.parent;
            if (parentScene) parentScene.remove(dungeonGroup);

            dungeonGroup.traverse(child => {
                if (child.geometry) child.geometry.dispose();
                if (child.material) {
                    if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
                    else child.material.dispose();
                }
            });
            dungeonGroup = null;
        }

        gridMap = null;

        // Kamera zurück auf Third-Person
        if (window.Scene3D && window.Scene3D.setCameraMode) {
            Scene3D.setCameraMode('third');
        }

        // Zurück zur Overworld
        if (window.Scene3D && window.Scene3D.exitBuilding) {
            Scene3D.exitBuilding();
        }

        if (typeof showNotification === 'function') {
            showNotification(`🏰 Labyrinth geschafft! ${enemiesDefeated} Gegner besiegt, ${lootsCollected} Schätze!`, 3000);
        }
    }

    // ==========================================
    // INPUT SYSTEM (Grid-Based Movement)
    // ==========================================

    function setupInput() {
        inputHandler = (e) => {
            if (!crawlerActive || isMoving || isRotating) return;
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            switch (e.code) {
                case 'KeyW': // Vorwärts
                    tryMove(DIR_OFFSETS[playerFacing].dx, DIR_OFFSETS[playerFacing].dz);
                    e.preventDefault();
                    break;
                case 'KeyS': // Rückwärts
                    tryMove(-DIR_OFFSETS[playerFacing].dx, -DIR_OFFSETS[playerFacing].dz);
                    e.preventDefault();
                    break;
                case 'KeyA': // Strafe links
                    const leftDir = (playerFacing + 3) % 4;
                    tryMove(DIR_OFFSETS[leftDir].dx, DIR_OFFSETS[leftDir].dz);
                    e.preventDefault();
                    break;
                case 'KeyD': // Strafe rechts
                    const rightDir = (playerFacing + 1) % 4;
                    tryMove(DIR_OFFSETS[rightDir].dx, DIR_OFFSETS[rightDir].dz);
                    e.preventDefault();
                    break;
                case 'KeyQ': // Drehe links
                    playerFacing = (playerFacing + 3) % 4;
                    smoothRotate();
                    e.preventDefault();
                    break;
                case 'KeyE': // Drehe rechts
                    playerFacing = (playerFacing + 1) % 4;
                    smoothRotate();
                    e.preventDefault();
                    break;
                case 'Escape': // Dungeon verlassen
                    exitCrawlerDungeon();
                    e.preventDefault();
                    break;
            }
        };

        window.addEventListener('keydown', inputHandler);
    }

    function tryMove(dx, dz) {
        const nx = playerGridX + dx;
        const nz = playerGridZ + dz;

        // Bounds Check
        if (nz < 0 || nz >= gridHeight || nx < 0 || nx >= gridWidth) return;
        // Wall Check
        if (gridMap[nz][nx] === CELL.WALL) return;

        isMoving = true;
        const charGroup = window.Scene3D?.characterGroup;
        if (!charGroup) { isMoving = false; return; }

        const startX = charGroup.position.x;
        const startZ = charGroup.position.z;
        const targetX = nx * TILE_SIZE;
        const targetZ = nz * TILE_SIZE;
        const startTime = performance.now();
        const duration = 250; // 250ms smooth movement

        function animate() {
            const elapsed = performance.now() - startTime;
            const t = Math.min(elapsed / duration, 1);
            const eased = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // ease in-out

            charGroup.position.x = startX + (targetX - startX) * eased;
            charGroup.position.z = startZ + (targetZ - startZ) * eased;

            // Player-Licht mitbewegen
            updatePlayerLight(charGroup.position.x, charGroup.position.z);

            if (t < 1) {
                requestAnimationFrame(animate);
            } else {
                playerGridX = nx;
                playerGridZ = nz;
                isMoving = false;
                checkTileEvent(nx, nz);
                updateHUD();
            }
        }
        requestAnimationFrame(animate);
    }

    function smoothRotate() {
        isRotating = true;
        // Rotation wird vom Kamera-System in 3d_scene.js gehandled
        // Wir setzen die Blickrichtung direkt
        const targetYaw = [Math.PI, Math.PI / 2, 0, -Math.PI / 2][playerFacing]; // N, E, S, W

        if (window.Scene3D && Scene3D.setOrbitYaw) {
            Scene3D.setOrbitYaw(targetYaw);
        }

        // Kurze Verzögerung für nächste Eingabe
        setTimeout(() => {
            isRotating = false;
            updateHUD();
        }, 150);
    }

    function updatePlayerLight(x, z) {
        if (!dungeonGroup) return;
        dungeonGroup.traverse(child => {
            if (child.userData && child.userData.isPlayerLight) {
                child.position.set(x, 3, z);
            }
        });
    }

    // ==========================================
    // BIOME ENEMIES (8+ pro Biom + Götterfels)
    // ==========================================

    function getBiomeEnemies() {
        // Erkenne Biom anhand Spielerposition in der Außenwelt
        const biome = (window.OverworldProps && typeof OverworldProps.getBiomeAtPosition === 'function')
            ? OverworldProps.getBiomeAtPosition(0, 0)
            : 'samtmoos';

        return BIOME_ENEMIES[biome] || BIOME_ENEMIES['samtmoos'];
    }

    const BIOME_ENEMIES = {
        // SAMTMOOS - Sanfte Hügel, Pilzwälder
        samtmoos: [
            'pilzling',         // Kleiner Pilzkreatur
            'mooswolf',         // Wolf mit Moospelz
            'sporengeist',      // Giftiger Geist
            'wurzelkriecher',   // Kriecht aus Wurzeln
            'schleimkröte',     // Giftschlamm
            'nachtmotte',       // Riesige Motte
            'pilzgolem',        // Großer Pilz-Konstrukt
            'faulige_ranke',    // Lebende Ranke
        ],
        // REICH DER DREI - Zivilisiert, Städte
        reich_der_drei: [
            'bandit',           // Straßenräuber
            'deserteur',        // Abtrünniger Soldat
            'rattenfänger',     // Rattenbeschwörer
            'kellerspinne',     // Riesige Spinne
            'straßenhund',      // Wilder Hund
            'schatten_dieb',    // Unsichtbarer Dieb
            'söldner',          // Bezahlter Kämpfer
            'gang_anführer',    // Boss-Typ
        ],
        // HEISSE DÜNEN - Wüste, Sand
        heisse_duenen: [
            'sandwurm',         // Aus dem Boden
            'wüstenskorpion',   // Giftiger Skorpion
            'sandsturm_geist',  // Aus Sand geformt
            'dünenläufer',      // Schneller Jäger
            'oasen_sirene',     // Lockt mit Wasser
            'kaktus_golem',     // Stacheliger Golem
            'hitze_phantom',    // Fata Morgana Kreatur
            'sandräuber',       // Banditen der Wüste
        ],
        // SALZWIND - Küste, Meer
        salzwind: [
            'seemöwen_schwarm', // Aggressiver Schwarm
            'strandkrabbe',     // Riesige Krabbe
            'wellenschlag',     // Wasser-Elementar
            'piraten_geist',    // Untote Piraten
            'salzgolem',        // Kristall-Salz Golem
            'nebelsirene',      // Nebel-Kreatur
            'anker_revenant',   // Geist mit Anker
            'gezeiten_schlange',// Seeschlange
        ],
        // MAGMASTRÖME - Vulkan, Feuer
        magmastroeme: [
            'lava_schleim',     // Brennender Schleim
            'feuerkäfer',       // Explodierende Käfer
            'asche_golem',      // Aus Asche geformt
            'magma_wurm',       // Schwimmt in Lava
            'funken_elementar', // Feuer-Geist
            'obsidian_ritter',  // Steinerner Krieger
            'flammen_imp',      // Kleiner Feuerdämon
            'vulkan_drake',     // Mini-Drache
        ],
        // GRÜNSCHLAMM - Sumpf, Gift
        gruenschlamm: [
            'sumpfkröte',       // Giftige Riesenkröte
            'fäulnis_zombie',   // Sumpf-Untoter
            'giftranke',        // Giftige Pflanze
            'irrlichter',       // Locken ins Moor
            'schlamm_golem',    // Schlammkreatur
            'blutegel_schwarm', // Ekel-Schwarm
            'moor_hexe',        // Sumpfmagierin
            'faulgas_blase',    // Explodierende Gasblase
        ],
        // BLITZEBENE - Steppe, Gewitter
        blitzebene: [
            'blitz_wolf',       // Elektro-Wolf
            'donner_büffel',    // Aufgeladener Büffel
            'sturm_harpy',      // Fliegende Harpy
            'plasma_schlange',  // Elektrische Schlange
            'blitz_elementar',  // Purer Blitz
            'sturmjäger',       // Schneller Humanoider
            'kupfer_golem',     // Leitfähiger Golem
            'gewittergeist',    // Geist im Sturm
        ],
        // TIEFENHÖHLEN - Unterirdisch, Dunkel
        tiefenhoehlen: [
            'höhlen_troll',     // Klassischer Troll
            'kristall_fledermaus',// Leuchtende Fledermaus
            'tiefenwurm',       // Riesiger Wurm
            'dunkel_schleicher',// Fast unsichtbar
            'stalaktit_spinne', // Hängt von Decke
            'echo_geist',       // Schallangriff
            'minen_kobold',     // Kleiner Sprengmeister
            'steinbrecher',     // Fels-Golem
        ],
        // GÖTTERFELS - Heilig, Exklusiv, Mächtig
        goetterfels: [
            'himmels_wächter',  // Engel-ähnlich
            'zeitriss_phantom', // Zeitanomalie (→ Zeitstadt!)
            'äther_wolf',       // Ätherischer Wolf
            'götterfels_drake', // Heiliger Drake
            'kristall_seraph',  // Leuchtender Seraph
            'runen_golem',      // Antiker Wächter
            'schicksals_spinner',// Schicksal-Weber
            'nebel_titan',      // Seltener Mini-Boss
            // EXKLUSIV - Nur auf dem Götterfels!
            'zeitwandler',      // ⏰ Hinweis auf Zeitstadt
            'götterbote',       // Göttlicher Messenger
        ],
    };

    // ==========================================
    // TILE EVENTS
    // ==========================================

    function checkTileEvent(x, z) {
        const cell = gridMap[z][x];

        if (cell === CELL.ENEMY) {
            // Kampf-Encounter!
            gridMap[z][x] = CELL.FLOOR; // Gegner entfernen nach Encounter
            removeMarkerAt(x, z);

            // ⚔️ VOLLES Kampfsystem im Crawler!
            // Crawler pausiert, Real3DCombat übernimmt alle Inputs (Q/E/Space/F/Shift)
            if (window.Real3DCombat) {
                const biomeEnemies = getBiomeEnemies();
                const count = Math.min(1 + Math.floor(dungeonLevel / 3), 3);
                const enemies = [];
                for (let i = 0; i < count; i++) {
                    enemies.push(biomeEnemies[randomInt(0, biomeEnemies.length - 1)]);
                }

                // Pause Crawler-Input während Kampf
                crawlerActive = false;
                if (crawlerHUD) crawlerHUD.style.opacity = '0.3';

                const playerPos = { x: x * TILE_SIZE, y: 0, z: z * TILE_SIZE };
                Real3DCombat.startCombat(enemies, dungeonGroup.parent, playerPos);

                // Warte auf Kampf-Ende, dann Crawler-Input zurück
                const combatWatch = setInterval(() => {
                    const inCombat = Real3DCombat.isInCombat
                        ? Real3DCombat.isInCombat()
                        : (Real3DCombat.state && Real3DCombat.state.inCombat);
                    if (!inCombat) {
                        clearInterval(combatWatch);
                        crawlerActive = true;
                        if (crawlerHUD) crawlerHUD.style.opacity = '1';
                        enemiesDefeated++;
                        updateHUD();
                    }
                }, 300);
            }

            if (typeof showNotification === 'function') {
                showNotification('⚔️ Encounter! Volles Kampfsystem aktiv!', 2000);
            }
        }

        if (cell === CELL.LOOT) {
            // Schatz gefunden!
            gridMap[z][x] = CELL.FLOOR;
            removeMarkerAt(x, z);
            lootsCollected++;

            // Items ins Inventar
            const lootItems = [
                { name: 'Gold', amount: 50 + dungeonLevel * 20 },
                { name: 'Kristallsplitter', amount: randomInt(1, 3) },
                { name: 'Heiltrank', amount: 1 },
            ];

            // In localStorage speichern
            try {
                const inv = JSON.parse(localStorage.getItem('najika_inventory') || '[]');
                lootItems.forEach(item => inv.push(item));
                localStorage.setItem('najika_inventory', JSON.stringify(inv));
            } catch (e) { /* ignore */ }

            if (typeof showNotification === 'function') {
                showNotification(`💎 Schatz gefunden! +${lootItems[0].amount} Gold, +${lootItems[1].amount} Kristalle!`, 3000);
            }
        }

        if (cell === CELL.EXIT) {
            // Dungeon geschafft!
            if (typeof showNotification === 'function') {
                showNotification('🎉 DUNGEON GESCHAFFT! Ausgang gefunden!', 3000);
            }
            setTimeout(() => exitCrawlerDungeon(), 2000);
        }
    }

    function removeMarkerAt(gx, gz) {
        if (!dungeonGroup) return;
        const toRemove = [];
        dungeonGroup.traverse(child => {
            if (child.userData && (child.userData.gridX === gx && child.userData.gridZ === gz)) {
                toRemove.push(child);
            }
        });
        toRemove.forEach(obj => {
            dungeonGroup.remove(obj);
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) obj.material.dispose();
        });
    }

    // ==========================================
    // HUD
    // ==========================================

    function createCrawlerHUD() {
        removeCrawlerHUD();

        crawlerHUD = document.createElement('div');
        crawlerHUD.id = 'crawler-hud';
        crawlerHUD.style.cssText = `
            position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.85); color: #ddd; padding: 10px 20px;
            border-radius: 8px; border: 1px solid #555; z-index: 9999;
            font-family: 'Press Start 2P', monospace; font-size: 11px;
            display: flex; gap: 20px; align-items: center;
        `;
        document.body.appendChild(crawlerHUD);

        // Minimap Container
        const minimapContainer = document.createElement('div');
        minimapContainer.id = 'crawler-minimap';
        minimapContainer.style.cssText = `
            position: fixed; bottom: 10px; right: 10px;
            background: rgba(0,0,0,0.9); border: 2px solid #555;
            border-radius: 4px; z-index: 9998; padding: 4px;
        `;
        document.body.appendChild(minimapContainer);

        // Controls Hint
        const hint = document.createElement('div');
        hint.id = 'crawler-hints';
        hint.style.cssText = `
            position: fixed; bottom: 10px; left: 10px;
            background: rgba(0,0,0,0.75); color: #888; padding: 8px 12px;
            border-radius: 6px; z-index: 9998;
            font-family: monospace; font-size: 10px; line-height: 1.6;
        `;
        hint.innerHTML = `
            <b>🏰 LABYRINTH</b><br>
            W/A/S/D = Bewegen<br>
            Q/E = Drehen<br>
            ESC = Verlassen
        `;
        document.body.appendChild(hint);
    }

    function updateHUD() {
        if (!crawlerHUD || !gridMap) return;

        const facingNames = ['↑ Nord', '→ Ost', '↓ Süd', '← West'];
        const enemies = countCellType(CELL.ENEMY);
        const loots = countCellType(CELL.LOOT);

        crawlerHUD.innerHTML = `
            <span>🏰 Lv.${dungeonLevel}</span>
            <span>📍 [${playerGridX},${playerGridZ}]</span>
            <span>${facingNames[playerFacing]}</span>
            <span>👹 ${enemies}</span>
            <span>💎 ${loots}</span>
            <span>⚔️ ${enemiesDefeated}</span>
        `;

        // Minimap updaten
        updateMinimap();
    }

    function updateMinimap() {
        const container = document.getElementById('crawler-minimap');
        if (!container || !gridMap) return;

        const CELL_PX = 4;
        const VIEW_RADIUS = 5; // Zeige 5 Tiles in jede Richtung
        const mapSize = (VIEW_RADIUS * 2 + 1) * CELL_PX;

        let html = `<canvas id="crawler-minimap-canvas" width="${mapSize}" height="${mapSize}" style="display:block;"></canvas>`;
        container.innerHTML = html;

        const canvas = document.getElementById('crawler-minimap-canvas');
        const ctx = canvas.getContext('2d');

        for (let dz = -VIEW_RADIUS; dz <= VIEW_RADIUS; dz++) {
            for (let dx = -VIEW_RADIUS; dx <= VIEW_RADIUS; dx++) {
                const gx = playerGridX + dx;
                const gz = playerGridZ + dz;
                const px = (dx + VIEW_RADIUS) * CELL_PX;
                const pz = (dz + VIEW_RADIUS) * CELL_PX;

                if (gx < 0 || gx >= gridWidth || gz < 0 || gz >= gridHeight) {
                    ctx.fillStyle = '#000';
                } else {
                    const cell = gridMap[gz][gx];
                    switch (cell) {
                        case CELL.WALL: ctx.fillStyle = '#333'; break;
                        case CELL.FLOOR: ctx.fillStyle = '#666'; break;
                        case CELL.ENEMY: ctx.fillStyle = '#f00'; break;
                        case CELL.LOOT: ctx.fillStyle = '#ff0'; break;
                        case CELL.EXIT: ctx.fillStyle = '#0f8'; break;
                        case CELL.ENTRANCE: ctx.fillStyle = '#48f'; break;
                        default: ctx.fillStyle = '#555';
                    }
                }
                ctx.fillRect(px, pz, CELL_PX, CELL_PX);
            }
        }

        // Spieler-Marker (Dreieck für Richtung)
        const centerPx = VIEW_RADIUS * CELL_PX + CELL_PX / 2;
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        const arrowSize = CELL_PX * 0.8;
        const angle = [Math.PI, Math.PI / 2, 0, -Math.PI / 2][playerFacing] + Math.PI / 2;
        ctx.moveTo(centerPx + Math.cos(angle) * arrowSize, centerPx + Math.sin(angle) * arrowSize);
        ctx.lineTo(centerPx + Math.cos(angle + 2.5) * arrowSize * 0.6, centerPx + Math.sin(angle + 2.5) * arrowSize * 0.6);
        ctx.lineTo(centerPx + Math.cos(angle - 2.5) * arrowSize * 0.6, centerPx + Math.sin(angle - 2.5) * arrowSize * 0.6);
        ctx.fill();
    }

    function countCellType(type) {
        if (!gridMap) return 0;
        let count = 0;
        for (let z = 0; z < gridHeight; z++) {
            for (let x = 0; x < gridWidth; x++) {
                if (gridMap[z][x] === type) count++;
            }
        }
        return count;
    }

    function removeCrawlerHUD() {
        ['crawler-hud', 'crawler-minimap', 'crawler-hints'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.remove();
        });
        crawlerHUD = null;
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    window.DungeonCrawler = {
        enterCrawlerDungeon,
        exitCrawlerDungeon,
        get isActive() { return crawlerActive; },
        get level() { return dungeonLevel; },
        get playerPosition() { return { x: playerGridX, z: playerGridZ, facing: playerFacing }; },
        get stats() { return { enemiesDefeated, lootsCollected }; }
    };

    console.log('🏰 Dungeon Crawler System loaded (Hexen/Daggerfall Style!)');
    console.log('   WASD = Bewegen, Q/E = Drehen, ESC = Verlassen');
})();
