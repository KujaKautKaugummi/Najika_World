/**
 * OVERWORLD ENEMY SYSTEM - Najika World
 * ======================================
 *
 * Spawnt und verwaltet Gegner auf der Overworld-Map
 * Basiert auf Region/Biome und nutzt das Unified Combat System
 *
 * Features:
 * - Regionbasierte Gegner-Typen
 * - Skalierung nach Spieler-Level
 * - Day/Night Unterschiede
 * - Respawn System
 * - Integration mit 3D Scene
 */

const OverworldEnemies = (function() {
    'use strict';

    // ==========================================
    // ASSET PFADE (KayKit Character-Modelle)
    // ==========================================
    const ASSET_BASE = '/static/assets/';
    const MODELS = {
        rogue:      'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_rogue.gltf',
        barbarian:  'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
        knight:     'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf',
        mage:       'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_mage.gltf',
        skeleton_warrior: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_warrior.gltf',
        skeleton_archer:  'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_archer.gltf',
        skeleton_mage:    'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_mage.gltf',
        skeleton_minion:  'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_minion.gltf',
        bear:       'KayKit Mini-Game Variety Pack 1.2/Models/Characters/Bear/gltf/character_bear.gltf',
        dog:        'KayKit Mini-Game Variety Pack 1.2/Models/Characters/Dog/gltf/character_dog.gltf',
        duck:       'KayKit Mini-Game Variety Pack 1.2/Models/Characters/Duck/gltf/character_duck.gltf',
        jack:       'KayKit Spooktober Seasonal Pack 1.1/Models/Characters/Jack/gltf/character_jack.gltf',
        witch:      'KayKit Spooktober Seasonal Pack 1.1/Models/Characters/Witch/gltf/character_witch.gltf'
    };

    // Model-Cache (damit nicht jeder Enemy neu lädt)
    const modelCache = {};
    let gltfLoader = null;

    // ==========================================
    // ENEMY DATABASE (per Biome)
    // ==========================================

    const BIOME_ENEMIES = {
        // SAMTMOOS-TIEFWALD (Wald)
        'samtmoos': {
            common: [
                {
                    id: 'wolf', name: 'Wolf', hp: 40, attack: 8, defense: 3, speed: 1.3,
                    xp: 15, loot: ['wolf_pelt', 'fang'], tier: 1,
                    model: MODELS.dog, color: 0x666666, modelScale: 3.0
                },
                {
                    id: 'forest_spider', name: 'Waldspinne', hp: 25, attack: 12, defense: 2, speed: 1.5,
                    xp: 12, loot: ['spider_silk', 'venom_sac'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0x332211, modelScale: 2.0
                },
                {
                    id: 'boar', name: 'Wildschwein', hp: 50, attack: 10, defense: 5, speed: 0.8,
                    xp: 18, loot: ['boar_tusk', 'meat'], tier: 1,
                    model: MODELS.bear, color: 0x8B4513, modelScale: 2.5
                }
            ],
            rare: [
                {
                    id: 'bear', name: 'Bär', hp: 120, attack: 20, defense: 10, speed: 0.9,
                    xp: 50, loot: ['bear_pelt', 'bear_claw', 'honey'], tier: 2,
                    model: MODELS.bear, color: 0x4a3728, modelScale: 4.0
                },
                {
                    id: 'treant', name: 'Baumwächter', hp: 150, attack: 15, defense: 20, speed: 0.4,
                    xp: 75, loot: ['ancient_bark', 'life_sap'], tier: 3,
                    model: MODELS.barbarian, color: 0x228B22, modelScale: 5.0
                }
            ],
            boss: {
                id: 'sporax', name: 'Sporax der Pilzfürst', hp: 500, attack: 35, defense: 15, speed: 0.6,
                xp: 300, loot: ['sporax_spore', 'fungal_crown', 'rare_mushroom'], tier: 4,
                element: 'poison', traits: ['Giftwolke', 'Sporenexplosion']
            }
        },

        // REICH DER DREI (Eis/Schnee)
        'reich_der_drei': {
            common: [
                {
                    id: 'ice_wolf', name: 'Eiswolf', hp: 45, attack: 10, defense: 4, speed: 1.4,
                    xp: 18, loot: ['frost_pelt', 'ice_fang'], tier: 1, element: 'ice',
                    model: MODELS.dog, color: 0xadd8e6, modelScale: 3.0
                },
                {
                    id: 'snow_hare', name: 'Schneehase', hp: 20, attack: 5, defense: 1, speed: 2.0,
                    xp: 8, loot: ['soft_fur', 'rabbit_foot'], tier: 1,
                    model: MODELS.duck, color: 0xffffff, modelScale: 1.5
                }
            ],
            rare: [
                {
                    id: 'frost_giant', name: 'Frostriese', hp: 200, attack: 30, defense: 15, speed: 0.5,
                    xp: 100, loot: ['giant_ice', 'frozen_heart'], tier: 3, element: 'ice',
                    model: MODELS.knight, color: 0x4169e1, modelScale: 6.0
                },
                {
                    id: 'yeti', name: 'Yeti', hp: 180, attack: 25, defense: 12, speed: 0.7,
                    xp: 90, loot: ['yeti_fur', 'yeti_tooth'], tier: 3,
                    model: MODELS.bear, color: 0xeeeeee, modelScale: 5.0
                }
            ],
            boss: {
                id: 'ice_queen', name: 'Eiskönigin Crystalia', hp: 600, attack: 40, defense: 20, speed: 0.8,
                xp: 400, loot: ['eternal_ice', 'frost_crown', 'diamond_dust'], tier: 5,
                element: 'ice', traits: ['Frostschild', 'Blizzard', 'Eissplitter']
            }
        },

        // HEISSE DÜNEN (Wüste)
        'heisse_duenen': {
            common: [
                {
                    id: 'sand_scorpion', name: 'Sandskorpion', hp: 35, attack: 15, defense: 8, speed: 1.2,
                    xp: 15, loot: ['scorpion_tail', 'venom'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0xc2b280, modelScale: 2.5
                },
                {
                    id: 'desert_snake', name: 'Wüstenschlange', hp: 30, attack: 12, defense: 2, speed: 1.6,
                    xp: 12, loot: ['snake_skin', 'snake_venom'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0xdaa520, modelScale: 2.0
                },
                {
                    id: 'sand_beetle', name: 'Sandkäfer', hp: 40, attack: 8, defense: 12, speed: 0.8,
                    xp: 14, loot: ['chitin_shell', 'beetle_horn'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0x8b7355, modelScale: 2.5
                }
            ],
            rare: [
                {
                    id: 'sand_wurm', name: 'Sandwurm', hp: 180, attack: 35, defense: 5, speed: 1.0,
                    xp: 120, loot: ['wurm_scale', 'wurm_tooth', 'sand_crystal'], tier: 3,
                    model: MODELS.barbarian, color: 0xd2b48c, modelScale: 5.0
                }
            ],
            boss: {
                id: 'fire_lord', name: 'Feuerfürst Ignis', hp: 550, attack: 45, defense: 18, speed: 0.9,
                xp: 350, loot: ['flame_essence', 'fire_crown', 'molten_core'], tier: 4,
                element: 'fire', traits: ['Flammenaura', 'Meteorregen', 'Feueratem']
            }
        },

        // SALZWIND-KÜSTE (Küste/Strand)
        'salzwind': {
            common: [
                {
                    id: 'crab', name: 'Riesenkrabbe', hp: 45, attack: 10, defense: 15, speed: 0.6,
                    xp: 14, loot: ['crab_shell', 'crab_meat'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0xff6347, modelScale: 2.5
                },
                {
                    id: 'seagull', name: 'Aggressiver Seevogel', hp: 20, attack: 8, defense: 1, speed: 2.0,
                    xp: 8, loot: ['feather', 'beak'], tier: 1,
                    model: MODELS.duck, color: 0xffffff, modelScale: 2.0
                }
            ],
            rare: [
                {
                    id: 'sea_serpent', name: 'Seeschlange', hp: 160, attack: 28, defense: 10, speed: 1.2,
                    xp: 85, loot: ['sea_scale', 'serpent_fang', 'pearl'], tier: 3, element: 'water',
                    model: MODELS.skeleton_archer, color: 0x20b2aa, modelScale: 4.0
                }
            ],
            boss: {
                id: 'kraken', name: 'Kraken Tidelord', hp: 700, attack: 50, defense: 25, speed: 0.5,
                xp: 500, loot: ['kraken_ink', 'tentacle', 'sea_crown'], tier: 5,
                element: 'water', traits: ['Tentakelschlag', 'Tintenwolke', 'Gezeitenruf']
            }
        },

        // MAGMASTRÖME (Vulkan)
        'magmastroeme': {
            common: [
                {
                    id: 'fire_imp', name: 'Feuerteufel', hp: 30, attack: 18, defense: 3, speed: 1.4,
                    xp: 16, loot: ['fire_essence', 'imp_horn'], tier: 1, element: 'fire',
                    model: MODELS.jack, color: 0xff4500, modelScale: 2.5
                },
                {
                    id: 'lava_slug', name: 'Lavaschnecke', hp: 50, attack: 12, defense: 8, speed: 0.3,
                    xp: 15, loot: ['molten_slime', 'obsidian_shard'], tier: 1, element: 'fire',
                    model: MODELS.skeleton_minion, color: 0xff6600, modelScale: 2.0
                }
            ],
            rare: [
                {
                    id: 'magma_golem', name: 'Magmagolem', hp: 220, attack: 35, defense: 25, speed: 0.4,
                    xp: 130, loot: ['golem_core', 'living_stone', 'lava_crystal'], tier: 3, element: 'fire',
                    model: MODELS.knight, color: 0x8b0000, modelScale: 5.0
                },
                {
                    id: 'fire_drake', name: 'Feuerdrache', hp: 250, attack: 40, defense: 20, speed: 1.0,
                    xp: 150, loot: ['drake_scale', 'dragon_fang', 'fire_gem'], tier: 4, element: 'fire',
                    model: MODELS.barbarian, color: 0xdc143c, modelScale: 5.5
                }
            ],
            boss: {
                id: 'volcano_titan', name: 'Vulkantitan Pyroclast', hp: 800, attack: 60, defense: 30, speed: 0.3,
                xp: 600, loot: ['titan_core', 'volcanic_crown', 'primordial_flame'], tier: 5,
                element: 'fire', traits: ['Erdbeben', 'Lavawelle', 'Vulkanausbruch']
            }
        },

        // GRÜNSCHLAMM-SUMPF
        'gruenschlamm': {
            common: [
                {
                    id: 'swamp_slime', name: 'Sumpfschleim', hp: 35, attack: 8, defense: 5, speed: 0.6,
                    xp: 10, loot: ['slime_gel', 'swamp_moss'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0x6b8e23, modelScale: 2.0
                },
                {
                    id: 'poison_frog', name: 'Giftfrosch', hp: 25, attack: 15, defense: 2, speed: 1.3,
                    xp: 12, loot: ['frog_skin', 'poison_gland'], tier: 1, element: 'poison',
                    model: MODELS.duck, color: 0x00ff00, modelScale: 2.0
                },
                {
                    id: 'swamp_leech', name: 'Riesenegel', hp: 40, attack: 10, defense: 3, speed: 0.8,
                    xp: 11, loot: ['leech_blood', 'anticoagulant'], tier: 1,
                    model: MODELS.skeleton_minion, color: 0x2f4f4f, modelScale: 2.5
                }
            ],
            rare: [
                {
                    id: 'bog_horror', name: 'Sumpfschrecken', hp: 170, attack: 28, defense: 12, speed: 0.7,
                    xp: 95, loot: ['horror_essence', 'swamp_heart'], tier: 3,
                    model: MODELS.witch, color: 0x3d5c3d, modelScale: 4.5
                }
            ],
            boss: {
                id: 'swamp_queen', name: 'Sumpfkönigin Morbia', hp: 550, attack: 38, defense: 16, speed: 0.6,
                xp: 380, loot: ['miasma_orb', 'bog_crown', 'essence_of_decay'], tier: 4,
                element: 'poison', traits: ['Giftnebel', 'Parasitenschwarm', 'Fäulnisaura']
            }
        },

        // BLITZEBENE
        'blitzebene': {
            common: [
                {
                    id: 'lightning_hawk', name: 'Blitzfalke', hp: 30, attack: 14, defense: 2, speed: 2.0,
                    xp: 14, loot: ['charged_feather', 'hawk_talon'], tier: 1, element: 'lightning',
                    model: MODELS.duck, color: 0xffff00, modelScale: 2.5
                },
                {
                    id: 'plains_runner', name: 'Steppenläufer', hp: 45, attack: 10, defense: 4, speed: 1.8,
                    xp: 15, loot: ['swift_hide', 'horn'], tier: 1,
                    model: MODELS.dog, color: 0xdeb887, modelScale: 3.0
                }
            ],
            rare: [
                {
                    id: 'storm_elemental', name: 'Sturmelementar', hp: 150, attack: 32, defense: 8, speed: 1.5,
                    xp: 100, loot: ['storm_essence', 'lightning_crystal'], tier: 3, element: 'lightning',
                    model: MODELS.mage, color: 0x1e90ff, modelScale: 4.0
                }
            ],
            boss: {
                id: 'thunder_lord', name: 'Donnerfürst Voltaris', hp: 580, attack: 48, defense: 15, speed: 1.2,
                xp: 420, loot: ['thunder_core', 'storm_crown', 'bolt_essence'], tier: 4,
                element: 'lightning', traits: ['Kettenblitz', 'Donnerschlag', 'Sturmruf']
            }
        },

        // TIEFENHÖHLEN (Unterirdisch)
        'tiefenhoehlen': {
            common: [
                {
                    id: 'cave_bat', name: 'Höhlenfledermaus', hp: 20, attack: 8, defense: 1, speed: 1.8,
                    xp: 8, loot: ['bat_wing', 'echo_crystal'], tier: 1,
                    model: MODELS.duck, color: 0x4a4a4a, modelScale: 1.5
                },
                {
                    id: 'rock_golem', name: 'Steingolem', hp: 80, attack: 15, defense: 20, speed: 0.3,
                    xp: 25, loot: ['stone_core', 'ore_vein'], tier: 2, element: 'earth',
                    model: MODELS.knight, color: 0x808080, modelScale: 4.0
                },
                {
                    id: 'mushroom_creature', name: 'Pilzwesen', hp: 35, attack: 10, defense: 5, speed: 0.7,
                    xp: 12, loot: ['glowing_spore', 'cave_mushroom'], tier: 1,
                    model: MODELS.jack, color: 0x9370db, modelScale: 2.5
                }
            ],
            rare: [
                {
                    id: 'crystal_dragon', name: 'Kristalldrache', hp: 280, attack: 42, defense: 28, speed: 0.8,
                    xp: 180, loot: ['dragon_crystal', 'prismatic_scale', 'gem_heart'], tier: 4, element: 'earth',
                    model: MODELS.skeleton_mage, color: 0x00ced1, modelScale: 6.0
                }
            ],
            boss: {
                id: 'deep_king', name: 'Tiefenkönig Abyssal', hp: 750, attack: 55, defense: 35, speed: 0.5,
                xp: 550, loot: ['abyss_core', 'deep_crown', 'void_essence'], tier: 5,
                element: 'dark', traits: ['Schattenruf', 'Erderschütterung', 'Abgrundblick']
            }
        }
    };

    // ==========================================
    // STATE
    // ==========================================

    const state = {
        activeEnemies: [],      // Aktuell gespawnte Gegner
        maxEnemies: 15,         // Max gleichzeitig auf Map
        spawnRadius: 50,        // Spawn-Radius um Spieler
        despawnRadius: 100,     // Despawn wenn weiter weg
        respawnTime: 30000,     // 30 Sekunden bis Respawn
        lastSpawnCheck: 0,
        playerLevel: 1,
        currentBiome: 'samtmoos',
        scene: null,
        isNight: false,
        activeCombat: false     // Combat-Queue: Nur 1 Combat gleichzeitig!
    };

    // ==========================================
    // INITIALIZATION
    // ==========================================

    function init(scene) {
        state.scene = scene;
        console.log('🐺 Overworld Enemies System initializing...');

        // Spawn-Check Loop
        setInterval(checkSpawns, 2000);

        // Despawn-Check Loop
        setInterval(checkDespawns, 5000);

        console.log('✅ Overworld Enemies System ready!');
    }

    // ==========================================
    // SPAWNING LOGIC
    // ==========================================

    function checkSpawns() {
        if (!state.scene) return;
        if (state.activeEnemies.length >= state.maxEnemies) return;

        // Get player position
        const playerPos = getPlayerPosition();
        if (!playerPos) return;

        // Determine current biome
        const biome = getCurrentBiome(playerPos);
        if (biome !== state.currentBiome) {
            state.currentBiome = biome;
            console.log(`🌍 Entered biome: ${biome}`);
        }

        // Spawn chance based on time since last spawn
        const now = Date.now();
        if (now - state.lastSpawnCheck < 5000) return;
        state.lastSpawnCheck = now;

        // Spawn 1-3 enemies
        const spawnCount = Math.floor(Math.random() * 3) + 1;

        for (let i = 0; i < spawnCount && state.activeEnemies.length < state.maxEnemies; i++) {
            spawnEnemy(playerPos, biome);
        }
    }

    function spawnEnemy(playerPos, biome) {
        // Safe Zone: Keine Spawns in Götterfels
        if (biome === 'goetterfels') return null;

        const biomeData = BIOME_ENEMIES[biome];
        if (!biomeData) {
            return null;  // Kein Warn-Spam für unbekannte Biomes
        }

        // Decide rarity (90% common, 9% rare, 1% boss)
        const roll = Math.random();
        let enemyList;
        let rarity;

        if (roll < 0.01 && biomeData.boss) {
            // Boss spawn (very rare, only if not already spawned)
            if (!state.activeEnemies.find(e => e.data.tier >= 4)) {
                enemyList = [biomeData.boss];
                rarity = 'boss';
            } else {
                enemyList = biomeData.rare || biomeData.common;
                rarity = 'rare';
            }
        } else if (roll < 0.10 && biomeData.rare) {
            enemyList = biomeData.rare;
            rarity = 'rare';
        } else {
            enemyList = biomeData.common;
            rarity = 'common';
        }

        // Pick random enemy from list
        const enemyTemplate = enemyList[Math.floor(Math.random() * enemyList.length)];

        // Calculate spawn position (random direction from player)
        const angle = Math.random() * Math.PI * 2;
        const distance = state.spawnRadius * (0.5 + Math.random() * 0.5);
        const spawnPos = {
            x: playerPos.x + Math.cos(angle) * distance,
            y: playerPos.y || 0,
            z: playerPos.z + Math.sin(angle) * distance
        };

        // Scale stats based on player level
        const levelScale = 1 + (state.playerLevel - 1) * 0.1;

        // Create enemy instance
        const enemy = {
            id: `enemy_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            data: {
                ...enemyTemplate,
                hp: Math.floor(enemyTemplate.hp * levelScale),
                maxHp: Math.floor(enemyTemplate.hp * levelScale),
                attack: Math.floor(enemyTemplate.attack * levelScale),
                defense: Math.floor(enemyTemplate.defense * levelScale),
                xp: Math.floor(enemyTemplate.xp * levelScale)
            },
            position: spawnPos,
            mesh: null,
            spawnTime: Date.now(),
            rarity: rarity,
            isAggro: false,
            aggroRange: rarity === 'boss' ? 30 : (rarity === 'rare' ? 20 : 12),
            lastAttack: 0
        };

        // Create 3D representation
        createEnemyMesh(enemy);

        state.activeEnemies.push(enemy);

        console.log(`🐺 Spawned ${rarity} enemy: ${enemy.data.name} at (${spawnPos.x.toFixed(0)}, ${spawnPos.z.toFixed(0)})`);

        return enemy;
    }

    function createEnemyMesh(enemy) {
        if (!state.scene) return;
        if (!window.THREE) return;

        // GLTFLoader initialisieren (einmalig)
        if (!gltfLoader && THREE.GLTFLoader) {
            gltfLoader = new THREE.GLTFLoader();
        }

        const modelPath = enemy.data.model;

        // Versuche 3D-Modell zu laden
        if (modelPath && gltfLoader) {
            const fullPath = ASSET_BASE + modelPath;
            const cacheKey = modelPath;

            // Gruppe für Enemy (Model + Label)
            const group = new THREE.Group();
            group.position.set(enemy.position.x, enemy.position.y, enemy.position.z);
            group.userData.enemyId = enemy.id;
            group.userData.isEnemy = true;

            // Name-Label sofort erstellen
            createNameLabel(enemy, group);

            state.scene.add(group);
            enemy.mesh = group;

            // Aus Cache klonen oder neu laden
            if (modelCache[cacheKey]) {
                const clone = modelCache[cacheKey].clone();
                applyEnemyModelSettings(clone, enemy);
                group.add(clone);
            } else {
                gltfLoader.load(
                    fullPath,
                    (gltf) => {
                        // In Cache speichern
                        modelCache[cacheKey] = gltf.scene.clone();

                        const model = gltf.scene;
                        applyEnemyModelSettings(model, enemy);
                        group.add(model);
                        console.log(`✅ Enemy model loaded: ${enemy.data.name}`);
                    },
                    undefined,
                    (error) => {
                        console.warn(`⚠️ Model load failed for ${enemy.data.name}, using fallback:`, error.message || error);
                        // Fallback: Farbige Box statt Sphere
                        const fallback = createFallbackShape(enemy);
                        group.add(fallback);
                    }
                );
            }

            // Pulsing Animation für rare/boss
            if (enemy.rarity !== 'common') {
                animateEnemyMesh(enemy);
            }
        } else {
            // Kein Model verfügbar → Fallback
            createFallbackMesh(enemy);
        }
    }

    function applyEnemyModelSettings(model, enemy) {
        const scale = enemy.data.modelScale || 3.0;
        model.scale.set(scale, scale, scale);

        // Farbe/Tint anwenden
        const color = enemy.data.color;
        if (color) {
            model.traverse(node => {
                if (node.isMesh) {
                    node.castShadow = true;
                    node.receiveShadow = true;
                    // Material klonen um Original nicht zu ändern
                    if (node.material) {
                        node.material = node.material.clone();
                        // Emissive-Tint für Farbgebung
                        node.material.emissive = new THREE.Color(color);
                        node.material.emissiveIntensity = 0.3;
                    }
                }
            });
        }

        // Boss-Glow
        if (enemy.rarity === 'boss') {
            model.traverse(node => {
                if (node.isMesh && node.material) {
                    node.material.emissiveIntensity = 0.6;
                }
            });
        }

        // Füße auf Boden
        const box = new THREE.Box3().setFromObject(model);
        model.position.y = -box.min.y;
    }

    function createNameLabel(enemy, parentGroup) {
        // Canvas für Text-Sprite
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');

        // Hintergrund
        ctx.fillStyle = enemy.rarity === 'boss' ? 'rgba(180,0,0,0.8)' :
                         enemy.rarity === 'rare' ? 'rgba(128,0,128,0.8)' :
                         'rgba(0,0,0,0.7)';
        ctx.roundRect(4, 4, 248, 56, 8);
        ctx.fill();

        // Text
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 22px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(enemy.data.name, 128, 30);

        // HP-Bar
        ctx.fillStyle = '#333';
        ctx.fillRect(30, 40, 196, 12);
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(30, 40, 196, 12);

        // Level/Tier
        ctx.fillStyle = '#FFD700';
        ctx.font = '14px Arial';
        ctx.fillText(`Lv${enemy.data.tier || 1}`, 128, 54);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(spriteMat);

        // Label über dem Enemy
        const height = (enemy.data.modelScale || 3.0) * 1.5 + 2;
        sprite.position.set(0, height, 0);
        sprite.scale.set(5, 1.25, 1);

        parentGroup.add(sprite);
        enemy.nameSprite = sprite;
    }

    function createFallbackShape(enemy) {
        // Stylisierte Box statt langweilige Sphere
        const size = enemy.rarity === 'boss' ? 3 : (enemy.rarity === 'rare' ? 2 : 1.2);
        const geometry = new THREE.BoxGeometry(size, size * 1.5, size);
        const material = new THREE.MeshStandardMaterial({
            color: enemy.data.color || 0xff0000,
            emissive: enemy.rarity === 'boss' ? 0x330000 : 0x000000,
            emissiveIntensity: enemy.rarity === 'boss' ? 0.5 : 0.1
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.castShadow = true;
        mesh.position.y = size * 0.75;
        return mesh;
    }

    function createFallbackMesh(enemy) {
        if (!window.THREE) return;

        const group = new THREE.Group();
        group.position.set(enemy.position.x, enemy.position.y, enemy.position.z);
        group.userData.enemyId = enemy.id;
        group.userData.isEnemy = true;

        const fallback = createFallbackShape(enemy);
        group.add(fallback);

        // Name-Label
        createNameLabel(enemy, group);

        state.scene.add(group);
        enemy.mesh = group;

        if (enemy.rarity !== 'common') {
            animateEnemyMesh(enemy);
        }
    }

    function animateEnemyMesh(enemy) {
        if (!enemy.mesh) return;

        const originalScale = enemy.mesh.scale.x;
        let phase = 0;

        const animate = () => {
            if (!enemy.mesh || !state.activeEnemies.includes(enemy)) return;

            phase += 0.05;
            const scale = originalScale + Math.sin(phase) * 0.1;
            enemy.mesh.scale.set(scale, scale, scale);

            requestAnimationFrame(animate);
        };

        animate();
    }

    // ==========================================
    // DESPAWNING
    // ==========================================

    function checkDespawns() {
        const playerPos = getPlayerPosition();
        if (!playerPos) return;

        state.activeEnemies = state.activeEnemies.filter(enemy => {
            const dist = distance2D(playerPos, enemy.position);

            if (dist > state.despawnRadius) {
                despawnEnemy(enemy);
                return false;
            }

            return true;
        });
    }

    function despawnEnemy(enemy) {
        if (enemy.mesh && state.scene) {
            state.scene.remove(enemy.mesh);
            // Rekursiv alle Meshes/Materials/Geometries disposen
            enemy.mesh.traverse(node => {
                if (node.isMesh) {
                    if (node.geometry) node.geometry.dispose();
                    if (node.material) {
                        if (Array.isArray(node.material)) {
                            node.material.forEach(m => m.dispose());
                        } else {
                            node.material.dispose();
                        }
                    }
                }
                if (node.isSprite && node.material) {
                    if (node.material.map) node.material.map.dispose();
                    node.material.dispose();
                }
            });
        }
        console.log(`👋 Despawned: ${enemy.data.name}`);
    }

    // ==========================================
    // COMBAT INTEGRATION
    // ==========================================

    /**
     * Prüft ob Spieler in Aggro-Range eines Gegners ist
     */
    function checkAggro() {
        const playerPos = getPlayerPosition();
        if (!playerPos) return;

        // Safe Zone: Keine Aggro in Götterfels (Schwarze Mühle)
        const dxCenter = playerPos.x - 4800;
        const dzCenter = playerPos.z - 4800;
        if (Math.sqrt(dxCenter * dxCenter + dzCenter * dzCenter) < 500) return;

        state.activeEnemies.forEach(enemy => {
            if (enemy.isAggro || enemy.inCombat) return; // Skip if already aggro or in combat

            const dist = distance2D(playerPos, enemy.position);
            if (dist < enemy.aggroRange) {
                enemy.isAggro = true;
                triggerEncounter(enemy);
            }
        });
    }

    /**
     * Startet Kampf mit Gegner
     */
    function triggerEncounter(enemy) {
        console.log(`⚔️ Encounter triggered: ${enemy.data.name}`);

        // COMBAT-QUEUE: Nur 1 Combat gleichzeitig!
        if (state.activeCombat) {
            console.warn(`⚠️ Combat bereits aktiv! ${enemy.data.name} wird übersprungen.`);
            enemy.isAggro = false;
            return;
        }

        // GameEvent emittieren
        if (window.GameEvents) {
            window.GameEvents.emit('combatStarted', {
                enemyId: enemy.data.id,
                enemyName: enemy.data.name,
                biome: state.currentBiome,
                rarity: enemy.rarity
            });
        }

        let combatStarted = false;

        // Use REAL 3D Combat (Tastatur-Controls: Q/E/Space)
        if (window.Real3DCombat && window.Real3DCombat.startCombat) {
            const scene = window.getScene ? window.getScene() : (state.scene || window.scene);
            const playerPos = window.getPlayerPosition ? window.getPlayerPosition() :
                (window.Scene3D?.characterGroup?.position || { x: 4800, y: 0, z: 4800 });

            if (scene) {
                // Store current enemy reference (wichtig für Callbacks!)
                const currentEnemy = enemy;

                // Setup Callbacks BEFORE starting combat
                window.onCombatVictory = (result) => {
                    if (result.type === 'real3d') {
                        console.log('✅ Combat Victory! XP:', result.xp, 'Loot:', result.loot);
                        onEnemyDefeated(currentEnemy);
                        state.activeCombat = false; // Combat beendet!
                        if (window.GameEvents) {
                            window.GameEvents.emit('combatEnded', { won: true, enemyData: currentEnemy.data });
                        }
                    }
                };

                window.onCombatDefeat = (result) => {
                    if (result.type === 'real3d') {
                        console.log('💀 Combat Defeat!');
                        // Spieler verloren - Gegner wieder sichtbar machen
                        if (currentEnemy.mesh) {
                            currentEnemy.mesh.visible = true;
                        }
                        currentEnemy.inCombat = false;
                        currentEnemy.isAggro = false;
                        state.activeCombat = false; // Combat beendet!
                        if (window.GameEvents) {
                            window.GameEvents.emit('combatEnded', { won: false, enemyData: currentEnemy.data });
                        }
                    }
                };

                // Real3DCombat erwartet: (enemyList, scene, position)
                window.Real3DCombat.startCombat([enemy.data.id], scene, playerPos);
                combatStarted = true;
                state.activeCombat = true; // Markiere Combat als aktiv!
                console.log(`⚔️ Real3D Combat gestartet: ${enemy.data.name}`);
            } else {
                console.warn('Scene nicht verfügbar für Real3DCombat, versuche Fallback...');
            }
        }

        if (!combatStarted && window.UnifiedCombat) {
            // Fallback: Unified Combat (UI-Buttons)
            const currentEnemy = enemy; // Store reference
            window.UnifiedCombat.startCombat({
                type: 'overworld',
                enemy: enemy.data,
                location: state.currentBiome,
                isHardcore: false,
                onWin: () => {
                    onEnemyDefeated(currentEnemy);
                    state.activeCombat = false;
                },
                onLose: () => {
                    if (currentEnemy.mesh) {
                        currentEnemy.mesh.visible = true;
                    }
                    currentEnemy.inCombat = false;
                    currentEnemy.isAggro = false;
                    state.activeCombat = false;
                    if (window.GameEvents) {
                        window.GameEvents.emit('combatEnded', { won: false, enemyData: currentEnemy.data });
                    }
                }
            });
            combatStarted = true;
            state.activeCombat = true;
        }

        if (!combatStarted) {
            // Kein Combat-System verfügbar - Gegner NICHT entfernen!
            console.error('Kein Combat-System geladen! Gegner bleibt auf der Map.');
            enemy.isAggro = false; // Reset aggro so player can try again
            return;
        }

        // Verstecke Gegner während Combat (statt ihn zu entfernen!)
        if (enemy.mesh) {
            enemy.mesh.visible = false;
        }

        // Markiere als "in combat" damit er nicht doppelt getriggert wird
        enemy.inCombat = true;
    }

    // ==========================================
    // FAIRES LOOT-SYSTEM
    // ==========================================
    //
    // DESIGN-PRINZIP: Kampf-Aufwand = Belohnung!
    //
    // - BOSSE: GARANTIERTER guter Loot (alle ihre Items + Bonus-Würfel)
    // - RARE: Garantiert 1-2 Items + Bonus-Chance auf seltenes Item
    // - COMMON: 1 garantiertes Item + Würfel auf 2. Item
    // - Bonus-Würfel kann VERBESSERN aber NIEMALS das Basis-Loot WEGNEHMEN
    // - "Pity System": Nach 5 Kills ohne Rare-Drop → nächster Drop GARANTIERT Rare
    //
    // Kein "ich lege Boss und krieg nichts"-Frust!

    let killsWithoutRareDrop = 0;

    // Bonus-Loot-Tabelle (extra Würfel-Items)
    const BONUS_LOOT = {
        common: ['health_potion', 'bread', 'torch', 'crystal_shard'],
        rare:   ['mana_potion', 'stamina_potion', 'antidote', 'steel_ingot', 'crystal_shard'],
        epic:   ['fire_sword', 'ice_dagger', 'lightning_staff', 'vitality_amulet', 'strength_ring'],
        legendary: ['champion_keule', 'frost_crown', 'volcanic_crown', 'storm_crown']
    };

    function onEnemyDefeated(enemy) {
        console.log(`💀 Enemy defeated: ${enemy.data.name}`);

        const rarity = enemy.rarity || 'common';
        const tier = enemy.data.tier || 1;
        const baseLoot = enemy.data.loot || [];
        const actualLoot = [];

        // ===== GARANTIERTER BASIS-LOOT =====
        // Bosse: ALLE ihre Items (IMMER)
        // Rare: 1-2 Items garantiert
        // Common: 1 Item garantiert
        if (rarity === 'boss') {
            // Boss → ALLE Items garantiert
            actualLoot.push(...baseLoot);
        } else if (rarity === 'rare') {
            // Rare → 1-2 Items garantiert
            const count = Math.min(baseLoot.length, 1 + (Math.random() < 0.6 ? 1 : 0));
            const shuffled = [...baseLoot].sort(() => Math.random() - 0.5);
            actualLoot.push(...shuffled.slice(0, count));
        } else {
            // Common → 1 Item garantiert
            if (baseLoot.length > 0) {
                actualLoot.push(baseLoot[Math.floor(Math.random() * baseLoot.length)]);
            }
        }

        // ===== BONUS-WÜRFEL (nur VERBESSERN, nie verschlechtern!) =====
        // Boss: 80% Chance auf Epic-Bonus + 30% Legendary
        // Rare: 50% Chance auf Rare-Bonus + 15% Epic
        // Common: 30% Chance auf Common-Bonus

        if (rarity === 'boss') {
            if (Math.random() < 0.8) {
                actualLoot.push(pickRandom(BONUS_LOOT.epic));
            }
            if (Math.random() < 0.3) {
                actualLoot.push(pickRandom(BONUS_LOOT.legendary));
            }
            // Boss droppt IMMER mindestens ein Rare-Bonus
            actualLoot.push(pickRandom(BONUS_LOOT.rare));
        } else if (rarity === 'rare') {
            if (Math.random() < 0.5) {
                actualLoot.push(pickRandom(BONUS_LOOT.rare));
            }
            if (Math.random() < 0.15) {
                actualLoot.push(pickRandom(BONUS_LOOT.epic));
            }
        } else {
            if (Math.random() < 0.3) {
                actualLoot.push(pickRandom(BONUS_LOOT.common));
            }
        }

        // ===== PITY SYSTEM =====
        // Nach 5 Common-Kills ohne Rare-Loot → GARANTIERT Rare-Bonus
        if (rarity === 'common') {
            killsWithoutRareDrop++;
            if (killsWithoutRareDrop >= 5) {
                actualLoot.push(pickRandom(BONUS_LOOT.rare));
                killsWithoutRareDrop = 0;
                console.log('🍀 Pity-System: Rare Bonus-Drop!');
            }
        } else {
            killsWithoutRareDrop = 0;  // Reset bei Rare/Boss Kill
        }

        // ===== LOOT INS INVENTAR =====
        actualLoot.forEach(itemId => {
            if (window.inventorySystem) {
                window.inventorySystem.addItem(itemId, 1);
            }
            if (window.GameEvents) {
                window.GameEvents.emit('itemCollected', { itemId, quantity: 1, source: 'combat_loot' });
            }
        });

        // ===== XP (Tier-basiert, Boss = Extra) =====
        let xp = enemy.data.xp || 10;
        if (rarity === 'boss') xp = Math.floor(xp * 1.5);  // 50% Bonus für Bosse

        // ===== GOLD (fair, Tier-basiert) =====
        const goldBase = tier * 10;
        const goldMultiplier = rarity === 'boss' ? 5 : (rarity === 'rare' ? 2 : 1);
        const goldDrop = Math.floor(goldBase * goldMultiplier * (0.8 + Math.random() * 0.4));
        if (goldDrop > 0 && window.inventorySystem && window.inventorySystem.addGold) {
            window.inventorySystem.addGold(goldDrop);
        }

        // ===== GAME EVENTS =====
        if (window.GameEvents) {
            window.GameEvents.emit('combatEnded', {
                won: true, enemyData: enemy.data,
                loot: actualLoot, xp, biome: state.currentBiome
            });
            window.GameEvents.emit('enemyKilled', {
                enemyId: enemy.data.id, enemyType: enemy.data.id,
                biome: state.currentBiome, loot: actualLoot,
                xp, rarity, gold: goldDrop,
                isBoss: rarity === 'boss'
            });
        }

        // ===== LOOT NOTIFICATION =====
        showLootNotification(enemy, actualLoot, goldDrop, xp);

        console.log(`💰 +${goldDrop}g | 📦 ${actualLoot.length} Items | ⭐ ${xp}XP`);

        // Entferne Gegner NACH Kampf
        removeEnemy(enemy.id);
    }

    function showLootNotification(enemy, loot, gold, xp) {
        const rarity = enemy.rarity || 'common';
        const borderColor = rarity === 'boss' ? '#FFD700' : (rarity === 'rare' ? '#9b59b6' : '#4CAF50');
        const bgColor = rarity === 'boss' ? 'rgba(80,60,0,0.95)' : (rarity === 'rare' ? 'rgba(60,0,80,0.95)' : 'rgba(0,60,0,0.9)');

        const notif = document.createElement('div');
        notif.style.cssText = `
            position:fixed; top:120px; right:20px; z-index:5000;
            background:${bgColor}; color:#fff; padding:12px 18px;
            border-radius:10px; border:2px solid ${borderColor};
            font-family:Arial; min-width:200px; max-width:300px;
        `;

        const itemList = loot.slice(0, 4).map(id => `📦 ${id.replace(/_/g, ' ')}`).join('<br>');
        const moreText = loot.length > 4 ? `<div style="color:#aaa; font-size:11px;">+${loot.length - 4} weitere...</div>` : '';

        notif.innerHTML = `
            <div style="font-weight:bold; color:${borderColor}; font-size:14px;">
                💀 ${enemy.data.name} besiegt!
            </div>
            <div style="font-size:12px; margin-top:5px; line-height:1.6;">
                ${itemList}
                ${moreText}
                <div style="margin-top:5px; color:#FFD700;">💰 ${gold} Gold | ⭐ ${xp} XP</div>
            </div>
        `;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 5000);
    }

    function pickRandom(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function removeEnemy(enemyId) {
        const index = state.activeEnemies.findIndex(e => e.id === enemyId);
        if (index !== -1) {
            const enemy = state.activeEnemies[index];
            despawnEnemy(enemy);
            state.activeEnemies.splice(index, 1);
        }
    }

    // ==========================================
    // UTILITY
    // ==========================================

    function getPlayerPosition() {
        // 1. Scene3D characterGroup (Hauptquelle!)
        if (window.Scene3D && window.Scene3D.characterGroup && window.Scene3D.characterGroup.position) {
            return {
                x: window.Scene3D.characterGroup.position.x,
                y: window.Scene3D.characterGroup.position.y,
                z: window.Scene3D.characterGroup.position.z
            };
        }

        // 2. Legacy: window.character
        if (window.character && window.character.position) {
            return {
                x: window.character.position.x,
                y: window.character.position.y,
                z: window.character.position.z
            };
        }

        // 3. Fallback
        if (window.playerPosition) {
            return window.playerPosition;
        }

        // 4. Letzte Rettung: Welt-Mitte
        return { x: 4800, y: 0, z: 4800 };
    }

    function getCurrentBiome(pos) {
        // Basierend auf Position das Biom bestimmen
        // (vereinfachte Version - sollte von world_system.py kommen)

        const centerX = 4800;
        const centerZ = 4800;
        const dx = pos.x - centerX;
        const dz = pos.z - centerZ;
        const angle = Math.atan2(dz, dx);
        const dist = Math.sqrt(dx * dx + dz * dz);

        // Götterfels (Mitte) - Safe Zone, keine Gegner
        if (dist < 500) return 'goetterfels';

        // 8 Regionen im Uhrzeigersinn
        const sector = Math.floor(((angle + Math.PI) / (Math.PI * 2)) * 8);

        // WICHTIG: Diese Namen MUESSEN mit BIOME_ENEMIES Keys übereinstimmen!
        const biomes = [
            'samtmoos',       // N - Wald
            'reich_der_drei', // NE - Eis
            'blitzebene',     // E - Highland (fallback: samtmoos)
            'heisse_duenen',  // SE - Wüste
            'magmastroeme',   // S - Vulkan (fallback: heisse_duenen)
            'gruenschlamm',   // SW - Sumpf (fallback: samtmoos)
            'salzwind',       // W - Küste (fallback: samtmoos)
            'tiefenhoehlen'   // NW - Höhlen (fallback: reich_der_drei)
        ];

        const biome = biomes[sector] || 'samtmoos';

        // Fallback zu existierenden Biomes wenn nicht definiert
        const biomeMapping = {
            'blitzebene': 'samtmoos',
            'magmastroeme': 'heisse_duenen',
            'gruenschlamm': 'samtmoos',
            'salzwind': 'samtmoos',
            'tiefenhoehlen': 'reich_der_drei',
            'goetterfels': null  // Safe Zone
        };

        // Wenn Biome in BIOME_ENEMIES existiert, nutze es direkt
        if (BIOME_ENEMIES[biome]) {
            return biome;
        }

        // Sonst nutze das Mapping
        return biomeMapping[biome] !== undefined ? biomeMapping[biome] : 'samtmoos';
    }

    function distance2D(a, b) {
        const dx = a.x - b.x;
        const dz = a.z - b.z;
        return Math.sqrt(dx * dx + dz * dz);
    }

    // ==========================================
    // UPDATE LOOP (call from main game loop)
    // ==========================================

    function update(playerPosition) {
        if (playerPosition) {
            window.playerPosition = playerPosition;
        }

        checkAggro();

        // Update enemy positions (move towards player if aggro)
        state.activeEnemies.forEach(enemy => {
            if (enemy.isAggro && enemy.mesh) {
                // Move towards player
                const playerPos = getPlayerPosition();
                const dx = playerPos.x - enemy.position.x;
                const dz = playerPos.z - enemy.position.z;
                const dist = Math.sqrt(dx * dx + dz * dz);

                if (dist > 3) {  // Don't get too close
                    const speed = enemy.data.speed * 0.1;
                    enemy.position.x += (dx / dist) * speed;
                    enemy.position.z += (dz / dist) * speed;
                    enemy.mesh.position.set(enemy.position.x, enemy.position.y + 1, enemy.position.z);
                }
            }
        });
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    return {
        init,
        update,
        spawnEnemy,
        removeEnemy,
        triggerEncounter,

        // Getters
        getActiveEnemies: () => state.activeEnemies,
        getCurrentBiome: () => state.currentBiome,
        getEnemyById: (id) => state.activeEnemies.find(e => e.id === id),

        // Setters
        setPlayerLevel: (level) => { state.playerLevel = level; },
        setMaxEnemies: (max) => { state.maxEnemies = max; },
        setNightMode: (isNight) => { state.isNight = isNight; },

        // Debug
        debugSpawn: (biome) => spawnEnemy(getPlayerPosition(), biome || state.currentBiome),
        clearAll: () => {
            state.activeEnemies.forEach(despawnEnemy);
            state.activeEnemies = [];
        }
    };
})();

// Global access
window.OverworldEnemies = OverworldEnemies;

console.log('🐺 Overworld Enemies System loaded!');
