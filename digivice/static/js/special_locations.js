/**
 * NAJIKA WORLD - SPECIAL LOCATIONS (PHASE 9)
 * ===========================================
 *
 * Besondere Orte mit einzigartigen Features:
 * - Reich der Drei (Ice, Undead Territory)
 * - Funkelnest (Swamp, Hidden Treasure Cave)
 * - Tiefenhöhlen (Caves, Goblin Settlements)
 */

class SpecialLocations {
    constructor(scene, THREE, inventorySystem = null, questManager = null) {
        this.scene = scene;
        this.THREE = THREE;
        this.inventorySystem = inventorySystem;
        this.questManager = questManager;

        // Locations
        this.locations = {};
        this.currentLocation = null;
        this.locationObjects = [];

        // Treasure Chests (Funkelnest)
        this.treasureChests = [];
        this.openedChests = new Set(); // Tracking opened chests

        // Goblin NPCs (Tiefenhöhlen)
        this.goblins = [];

        console.log('🗺️ Special Locations System initialisiert');
    }

    // ===== LOCATION DATA =====

    getLocationData() {
        return {
            // ===== REICH DER DREI (Ice Region, Undead Territory) =====
            'reich_der_drei': {
                id: 'reich_der_drei',
                name: 'Reich der Drei',
                description: 'Ein verfluchtes Gebiet voller Untote',
                region: 'ice',
                position: { x: -80, y: 0, z: -80 }, // Ice Region
                entrance: {
                    type: 'gate',
                    size: { width: 10, height: 15 },
                    color: 0x4a0080,
                    icon: '🚪'
                },
                interior: {
                    size: 80,
                    theme: 'undead',
                    lighting: 'dark',
                    enemies: [
                        { type: 'ice_undead', count: 10 },
                        { type: 'skeleton_warrior', count: 5 },
                        { type: 'necromancer_boss', count: 1, boss: true }
                    ],
                    loot: [
                        'legendary_ice_spear',
                        'undead_armor',
                        'soul_crystal'
                    ]
                }
            },

            // ===== FUNKELNEST (Swamp Region, Hidden Treasure Cave) =====
            'funkelnest': {
                id: 'funkelnest',
                name: 'Funkelnest',
                description: 'Eine versteckte Schatzhöhle im tiefen Sumpf',
                region: 'swamp',
                position: { x: 80, y: 0, z: 80 }, // Swamp Region
                entrance: {
                    type: 'hole',
                    size: { width: 3, height: 3 },
                    color: 0x2d4a1f,
                    icon: '🕳️',
                    hidden: true // Schwer zu finden
                },
                interior: {
                    size: 60,
                    theme: 'cave',
                    lighting: 'dim',
                    enemies: [
                        { type: 'swamp_witch', count: 3 },
                        { type: 'cave_guardian', count: 2 }
                    ],
                    treasures: 10, // 10 Schatztruhen
                    loot: [
                        'legendary_treasure',
                        'rare_materials',
                        'gold_piles'
                    ]
                }
            },

            // ===== TIEFENHÖHLEN (Mountain Region, Goblin Settlements) =====
            'tiefenhoehlen': {
                id: 'tiefenhoehlen',
                name: 'Tiefenhöhlen',
                description: 'Unterirdische Goblin-Siedlungen',
                region: 'mountain',
                position: { x: -80, y: 0, z: 80 }, // Mountain Region
                entrance: {
                    type: 'cave_entrance',
                    size: { width: 8, height: 10 },
                    color: 0x5a4a3a,
                    icon: '⛰️'
                },
                interior: {
                    size: 100,
                    theme: 'goblin_village',
                    lighting: 'torches',
                    settlements: 4, // 4 Goblin-Dörfer
                    npcs: [
                        { type: 'goblin_trader', count: 3 },
                        { type: 'goblin_questgiver', count: 2 },
                        { type: 'goblin_citizen', count: 10 }
                    ],
                    enemies: [
                        { type: 'goblin_king_boss', count: 1, boss: true }
                    ],
                    quests: [
                        'goblin_mushroom_quest',
                        'goblin_boss_quest'
                    ]
                }
            }
        };
    }

    // ===== CREATE ENTRANCE MARKERS =====

    createEntranceMarkers() {
        const locationsData = this.getLocationData();

        for (const locationId in locationsData) {
            const location = locationsData[locationId];
            const entrance = this.createEntrance(location);

            this.locations[locationId] = {
                data: location,
                entrance: entrance
            };

            console.log(`🗺️ Entrance erstellt: ${location.name} bei (${location.position.x}, ${location.position.z})`);
        }
    }

    createEntrance(location) {
        const { entrance, position } = location;

        // Create entrance mesh
        const geometry = new this.THREE.BoxGeometry(
            entrance.size.width,
            entrance.size.height,
            2
        );
        const material = new this.THREE.MeshStandardMaterial({
            color: entrance.color,
            emissive: entrance.color,
            emissiveIntensity: 0.3,
            roughness: 0.5
        });

        const mesh = new this.THREE.Mesh(geometry, material);
        mesh.position.set(position.x, entrance.size.height / 2, position.z);
        mesh.userData.locationType = 'special_entrance';
        mesh.userData.locationId = location.id;
        mesh.userData.locationName = location.name;

        this.scene.add(mesh);
        this.locationObjects.push(mesh);

        // Create label
        const label = this.createEntranceLabel(location);
        label.position.set(position.x, entrance.size.height + 3, position.z);
        this.scene.add(label);
        this.locationObjects.push(label);

        return {
            mesh: mesh,
            label: label,
            position: position
        };
    }

    createEntranceLabel(location) {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 128;
        const context = canvas.getContext('2d');

        // Background
        context.fillStyle = 'rgba(0, 0, 0, 0.8)';
        context.fillRect(0, 0, 512, 128);

        // Text
        context.font = 'Bold 40px Arial';
        context.fillStyle = '#FFD700';
        context.textAlign = 'center';
        context.fillText(location.entrance.icon + ' ' + location.name, 256, 65);

        // Subtitle
        context.font = '24px Arial';
        context.fillStyle = '#aaa';
        context.fillText('Drücke E zum Betreten', 256, 100);

        // Create sprite
        const texture = new this.THREE.CanvasTexture(canvas);
        const material = new this.THREE.SpriteMaterial({
            map: texture,
            transparent: true
        });
        const sprite = new this.THREE.Sprite(material);
        sprite.scale.set(8, 2, 1);

        return sprite;
    }

    // ===== CHECK PROXIMITY =====

    checkEntranceProximity(playerPosition) {
        for (const locationId in this.locations) {
            const location = this.locations[locationId];
            const entrance = location.entrance;

            const distance = this.getDistance(playerPosition, entrance.position);

            if (distance < 5) {
                return location.data;
            }
        }

        return null;
    }

    getDistance(pos1, pos2) {
        const dx = pos1.x - pos2.x;
        const dz = pos1.z - pos2.z;
        return Math.sqrt(dx * dx + dz * dz);
    }

    // ===== ENTER LOCATION =====

    enterLocation(locationId) {
        const location = this.locations[locationId];
        if (!location) {
            console.error(`❌ Location nicht gefunden: ${locationId}`);
            return null;
        }

        this.currentLocation = locationId;
        console.log(`🗺️ Betrete ${location.data.name}...`);

        // Generate interior based on type
        switch(locationId) {
            case 'reich_der_drei':
                return this.generateReichDerDrei(location.data);
            case 'funkelnest':
                return this.generateFunkelnest(location.data);
            case 'tiefenhoehlen':
                return this.generateTiefenhoehlen(location.data);
            default:
                return null;
        }
    }

    // ===== REICH DER DREI INTERIOR =====

    generateReichDerDrei(locationData) {
        const interior = {
            name: locationData.name,
            type: 'reich_der_drei',
            objects: [],
            enemies: []
        };

        const size = locationData.interior.size;

        // Ground (dark ice)
        const ground = new this.THREE.Mesh(
            new this.THREE.PlaneGeometry(size, size),
            new this.THREE.MeshStandardMaterial({
                color: 0x1a1a2e,
                roughness: 0.9
            })
        );
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        interior.objects.push(ground);

        // Dark ambient
        const ambientLight = new this.THREE.AmbientLight(0x4a0080, 0.3);
        interior.objects.push(ambientLight);

        // Icy crystals (decoration)
        for (let i = 0; i < 20; i++) {
            const x = (Math.random() - 0.5) * (size - 10);
            const z = (Math.random() - 0.5) * (size - 10);

            const crystal = new this.THREE.Mesh(
                new this.THREE.ConeGeometry(1, 3, 6),
                new this.THREE.MeshStandardMaterial({
                    color: 0x88ccff,
                    emissive: 0x4488ff,
                    emissiveIntensity: 0.5,
                    transparent: true,
                    opacity: 0.7
                })
            );
            crystal.position.set(x, 1.5, z);
            interior.objects.push(crystal);
        }

        // Boss platform (center)
        const platform = new this.THREE.Mesh(
            new this.THREE.CylinderGeometry(10, 10, 1, 32),
            new this.THREE.MeshStandardMaterial({
                color: 0x4a0080,
                emissive: 0x4a0080,
                emissiveIntensity: 0.3
            })
        );
        platform.position.set(0, 0.5, 0);
        interior.objects.push(platform);

        console.log(`👻 Reich der Drei Interior generiert: ${interior.objects.length} Objekte`);

        return interior;
    }

    // ===== FUNKELNEST INTERIOR =====

    generateFunkelnest(locationData) {
        const interior = {
            name: locationData.name,
            type: 'funkelnest',
            objects: [],
            treasures: []
        };

        const size = locationData.interior.size;

        // Ground (cave floor)
        const ground = new this.THREE.Mesh(
            new this.THREE.PlaneGeometry(size, size),
            new this.THREE.MeshStandardMaterial({
                color: 0x3a2a1a,
                roughness: 1
            })
        );
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        interior.objects.push(ground);

        // Dim lighting
        const ambientLight = new this.THREE.AmbientLight(0xffaa44, 0.4);
        interior.objects.push(ambientLight);

        // Treasure Chests (10 Stück)
        const treasureCount = locationData.interior.treasures;

        for (let i = 0; i < treasureCount; i++) {
            const angle = (i / treasureCount) * Math.PI * 2;
            const radius = 20 + Math.random() * 10;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;

            const chest = this.createTreasureChest(x, z, i);
            interior.objects.push(chest);
            interior.treasures.push(chest);
        }

        // Glowing mushrooms (decoration)
        for (let i = 0; i < 30; i++) {
            const x = (Math.random() - 0.5) * (size - 10);
            const z = (Math.random() - 0.5) * (size - 10);

            const mushroom = new this.THREE.Mesh(
                new this.THREE.SphereGeometry(0.5, 8, 8),
                new this.THREE.MeshStandardMaterial({
                    color: 0xff6600,
                    emissive: 0xff6600,
                    emissiveIntensity: 0.6
                })
            );
            mushroom.position.set(x, 0.5, z);
            interior.objects.push(mushroom);
        }

        console.log(`💎 Funkelnest Interior generiert: ${interior.treasures.length} Schatztruhen`);

        return interior;
    }

    createTreasureChest(x, z, index) {
        const chest = new this.THREE.Mesh(
            new this.THREE.BoxGeometry(2, 1.5, 1.5),
            new this.THREE.MeshStandardMaterial({
                color: 0x8B4513,
                roughness: 0.8
            })
        );
        chest.position.set(x, 0.75, z);
        chest.userData.isChest = true;
        chest.userData.chestId = `chest_${index}`;
        chest.userData.opened = false;

        return chest;
    }

    // ===== TIEFENHÖHLEN INTERIOR =====

    generateTiefenhoehlen(locationData) {
        const interior = {
            name: locationData.name,
            type: 'tiefenhoehlen',
            objects: [],
            settlements: []
        };

        const size = locationData.interior.size;

        // Ground (cave floor)
        const ground = new this.THREE.Mesh(
            new this.THREE.PlaneGeometry(size, size),
            new this.THREE.MeshStandardMaterial({
                color: 0x4a3a2a,
                roughness: 0.9
            })
        );
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        interior.objects.push(ground);

        // Torch lighting
        const ambientLight = new this.THREE.AmbientLight(0xff8844, 0.5);
        interior.objects.push(ambientLight);

        // 4 Goblin Settlements
        const settlementCount = locationData.interior.settlements;
        const settlementRadius = 20;

        for (let i = 0; i < settlementCount; i++) {
            const angle = (i / settlementCount) * Math.PI * 2;
            const x = Math.cos(angle) * 30;
            const z = Math.sin(angle) * 30;

            const settlement = this.createGoblinSettlement(x, z, i, settlementRadius);
            interior.objects.push(...settlement.objects);
            interior.settlements.push(settlement);
        }

        console.log(`🏘️ Tiefenhöhlen Interior generiert: ${settlementCount} Goblin-Siedlungen`);

        return interior;
    }

    createGoblinSettlement(centerX, centerZ, index, radius) {
        const settlement = {
            name: `Goblin-Siedlung ${index + 1}`,
            objects: [],
            npcs: []
        };

        // Central fire
        const fire = new this.THREE.Mesh(
            new this.THREE.CylinderGeometry(1, 1, 2, 8),
            new this.THREE.MeshStandardMaterial({
                color: 0xff4400,
                emissive: 0xff4400,
                emissiveIntensity: 0.8
            })
        );
        fire.position.set(centerX, 1, centerZ);
        settlement.objects.push(fire);

        // Goblin huts (5-8 Stück)
        const hutCount = 5 + Math.floor(Math.random() * 4);

        for (let i = 0; i < hutCount; i++) {
            const angle = (i / hutCount) * Math.PI * 2;
            const x = centerX + Math.cos(angle) * radius;
            const z = centerZ + Math.sin(angle) * radius;

            const hut = new this.THREE.Mesh(
                new this.THREE.BoxGeometry(4, 3, 4),
                new this.THREE.MeshStandardMaterial({
                    color: 0x5a4a3a,
                    roughness: 0.9
                })
            );
            hut.position.set(x, 1.5, z);
            settlement.objects.push(hut);
        }

        return settlement;
    }

    // ===== OPEN TREASURE CHEST =====

    openTreasureChest(chestMesh) {
        if (!chestMesh.userData.isChest) return;

        const chestId = chestMesh.userData.chestId;

        if (this.openedChests.has(chestId)) {
            console.log('⚠️ Truhe bereits geöffnet!');
            return;
        }

        // Mark as opened
        this.openedChests.add(chestId);
        chestMesh.userData.opened = true;

        // Change color
        chestMesh.material.color.setHex(0x666666);

        // Generate random loot
        const loot = this.generateTreasureLoot();

        // Give loot
        if (this.inventorySystem) {
            loot.forEach(item => {
                this.inventorySystem.addItem(item.id, item.count);
            });

            if (loot.gold > 0) {
                this.inventorySystem.addGold(loot.gold);
            }
        }

        console.log(`💎 Schatztruhe geöffnet! Loot: ${loot.map(i => i.id).join(', ')}`);

        return loot;
    }

    generateTreasureLoot() {
        const loot = [];

        // Random gold (50-200)
        loot.gold = 50 + Math.floor(Math.random() * 150);

        // Random items (1-3)
        const itemCount = 1 + Math.floor(Math.random() * 3);
        const possibleItems = [
            'crystal_shard',
            'fire_sword',
            'ice_dagger',
            'steel_chestplate',
            'vitality_amulet',
            'strength_ring',
            'champion_keule'
        ];

        for (let i = 0; i < itemCount; i++) {
            const randomItem = possibleItems[Math.floor(Math.random() * possibleItems.length)];
            loot.push({ id: randomItem, count: 1 });
        }

        // 10% Chance für Legendary Item
        if (Math.random() < 0.1) {
            loot.push({ id: 'legendary_fire_blade', count: 1 });
        }

        return loot;
    }

    // ===== CLEANUP =====

    clearLocation() {
        this.locationObjects.forEach(obj => {
            this.scene.remove(obj);
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) obj.material.dispose();
        });

        this.locationObjects = [];
        this.currentLocation = null;

        console.log('🧹 Special Location cleared');
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SpecialLocations;
}
