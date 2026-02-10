/**
 * DUNGEON ENEMY SYSTEM
 * Spawnt & animiert Gegner im Dungeon
 * Nutzt KayKit Skeletons + Animations
 */

(function() {
    'use strict';

    // Enemy Database - ERWEITERT mit verschiedenen KayKit Packs!
    const ENEMY_TYPES = {
        // === SKELETONS (Undead, Easy) ===
        skeleton_warrior: {
            name: 'Skelett-Krieger',
            model: 'KayKit_Skeletons_1.0_FREE/KayKit_Skeletons_1.0_FREE/assets/gltf/Skeleton_Blade.gltf',
            hp: 30,
            damage: 5,
            speed: 1.2,
            attackRange: 2.0,
            scale: 1.8,
            xp: 10,
            loot: ['bone', 'sword_rusty'],
            color: 0xcccccc,
            tier: 1 // Easy
        },
        skeleton_archer: {
            name: 'Skelett-Bogenschütze',
            model: 'KayKit_Skeletons_1.0_FREE/KayKit_Skeletons_1.0_FREE/assets/gltf/Skeleton_Crossbow.gltf',
            hp: 20,
            damage: 8,
            speed: 0.8,
            attackRange: 8.0,
            scale: 1.8,
            xp: 15,
            loot: ['bone', 'crossbow_broken'],
            color: 0xcccccc,
            tier: 1
        },
        skeleton_mage: {
            name: 'Skelett-Magier',
            model: 'KayKit_Skeletons_1.0_FREE/KayKit_Skeletons_1.0_FREE/assets/gltf/Skeleton_Staff.gltf',
            hp: 25,
            damage: 12,
            speed: 0.9,
            attackRange: 6.0,
            scale: 1.8,
            xp: 20,
            loot: ['bone', 'magic_crystal'],
            color: 0x8844ff,
            tier: 2
        },
        skeleton_tank: {
            name: 'Skelett-Wächter',
            model: 'KayKit_Skeletons_1.0_FREE/KayKit_Skeletons_1.0_FREE/assets/gltf/Skeleton_Shield_Large_A.gltf',
            hp: 50,
            damage: 3,
            speed: 0.6,
            attackRange: 1.5,
            scale: 2.0,
            xp: 25,
            loot: ['bone', 'shield_heavy'],
            color: 0xffcc00,
            tier: 2
        },
        skeleton_axe: {
            name: 'Skelett-Henker',
            model: 'KayKit_Skeletons_1.0_FREE/KayKit_Skeletons_1.0_FREE/assets/gltf/Skeleton_Axe.gltf',
            hp: 40,
            damage: 10,
            speed: 1.0,
            attackRange: 2.5,
            scale: 1.9,
            xp: 18,
            loot: ['bone', 'axe_rusty'],
            color: 0xff4444,
            tier: 2
        },

        // === CORRUPTED HEROES (KayKit Adventurers - Medium) ===
        corrupted_knight: {
            name: 'Verfluchter Ritter',
            model: 'KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Characters/gltf/Knight.glb',
            hp: 80,
            damage: 15,
            speed: 0.9,
            attackRange: 2.5,
            scale: 2.0,
            xp: 50,
            loot: ['cursed_sword', 'plate_armor_broken'],
            color: 0x440044,
            tier: 3
        },
        corrupted_rogue: {
            name: 'Schattendieb',
            model: 'KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Characters/gltf/Rogue_Hooded.glb',
            hp: 60,
            damage: 20,
            speed: 1.5,
            attackRange: 3.0,
            scale: 1.8,
            xp: 60,
            loot: ['poison_dagger', 'shadow_cloak'],
            color: 0x222266,
            tier: 3
        },
        corrupted_barbarian: {
            name: 'Berserker-Untoter',
            model: 'KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Characters/gltf/Barbarian.glb',
            hp: 120,
            damage: 25,
            speed: 0.7,
            attackRange: 2.0,
            scale: 2.2,
            xp: 80,
            loot: ['great_axe', 'berserker_helm'],
            color: 0xff0000,
            tier: 4
        },
        dark_sorcerer: {
            name: 'Dunkler Hexenmeister',
            model: 'KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Characters/gltf/Mage.glb',
            hp: 70,
            damage: 30,
            speed: 0.8,
            attackRange: 10.0,
            scale: 1.9,
            xp: 100,
            loot: ['dark_staff', 'spell_tome'],
            color: 0x6600ff,
            tier: 4
        },

        // === HALLOWEEN ENEMIES (Spooky Props as enemies) ===
        haunted_pumpkin: {
            name: 'Verfluchter Kürbis',
            model: 'KayKit Spooktober Seasonal Pack 1.1/Models/gltf/jackolantern_big.gltf.glb',
            hp: 15,
            damage: 3,
            speed: 0.5,
            attackRange: 1.0,
            scale: 2.5,
            xp: 8,
            loot: ['pumpkin_seed', 'candle'],
            color: 0xff8800,
            tier: 1,
            isStatic: true // Doesn't move much
        },
        cursed_coffin: {
            name: 'Verfluchter Sarg',
            model: 'KayKit_HalloweenBits_1.0_FREE/KayKit_HalloweenBits_1.0_FREE/Assets/gltf/coffin.gltf',
            hp: 50,
            damage: 0,
            speed: 0,
            attackRange: 0,
            scale: 2.0,
            xp: 5,
            loot: ['ancient_gold', 'mystery_item'],
            color: 0x8844ff,
            tier: 1,
            isStatic: true, // Spawns enemies when opened!
            spawner: true
        },

        // === DUNGEON PROPS als Gegner (Creative!) ===
        barrel_mimic: {
            name: 'Fass-Mimik',
            model: 'KayKit_DungeonRemastered_1.1_FREE/KayKit_DungeonRemastered_1.1_FREE/Assets/gltf/barrel.gltf',
            hp: 25,
            damage: 8,
            speed: 0.3,
            attackRange: 1.5,
            scale: 2.0,
            xp: 12,
            loot: ['barrel_wood', 'mystery_item'],
            color: 0x996633,
            tier: 2,
            surprise: true // Looks like normal prop!
        },
        crate_golem: {
            name: 'Kisten-Golem',
            model: 'KayKit_DungeonRemastered_1.1_FREE/KayKit_DungeonRemastered_1.1_FREE/Assets/gltf/crate_small_A.gltf',
            hp: 35,
            damage: 6,
            speed: 0.5,
            attackRange: 2.0,
            scale: 2.5,
            xp: 15,
            loot: ['wooden_plank', 'nails'],
            color: 0x886644,
            tier: 2
        }
    };

    // Enemy AI States
    const AI_STATE = {
        IDLE: 'idle',
        PATROL: 'patrol',
        CHASE: 'chase',
        ATTACK: 'attack',
        HURT: 'hurt',
        DEAD: 'dead'
    };

    // Active enemies in scene
    let activeEnemies = [];

    // Animation mixer for all enemies
    let enemyMixers = [];
    const clock = new THREE.Clock();

    /**
     * Enemy Class
     */
    class Enemy {
        constructor(type, position, level = 1, scene) {
            this.type = type;
            this.data = ENEMY_TYPES[type];
            this.level = level;
            this.scene = scene;

            // Stats (skaliert mit Level)
            this.maxHp = Math.floor(this.data.hp * (1 + level * 0.3));
            this.hp = this.maxHp;
            this.damage = Math.floor(this.data.damage * (1 + level * 0.2));
            this.speed = this.data.speed;
            this.attackRange = this.data.attackRange;
            this.xp = Math.floor(this.data.xp * (1 + level * 0.5));

            // Position & Movement
            this.position = new THREE.Vector3(...position);
            this.rotation = Math.random() * Math.PI * 2;
            this.velocity = new THREE.Vector3();
            this.target = null; // Player or patrol point

            // AI State
            this.state = AI_STATE.IDLE;
            this.stateTimer = 0;
            this.patrolPoints = this.generatePatrolPoints(position);
            this.currentPatrolIndex = 0;
            this.attackCooldown = 0;

            // 3D Objects
            this.group = null;
            this.model = null;
            this.healthBar = null;
            this.mixer = null;
            this.animations = {};

            // Flags
            this.isDead = false;
            this.isLoaded = false;
        }

        async load() {
            try {
                // Load model via KayKitLoader
                const modelPath = this.data.model;
                const gltf = await this.loadGLTF('/assets/' + modelPath);

                this.group = new THREE.Group();
                this.model = gltf.scene.clone();
                this.model.scale.setScalar(this.data.scale);

                // Add subtle glow effect
                this.model.traverse(child => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                        // Emissive glow für Skelette
                        if (child.material) {
                            child.material = child.material.clone();
                            child.material.emissive = new THREE.Color(this.data.color);
                            child.material.emissiveIntensity = 0.2;
                        }
                    }
                });

                this.group.add(this.model);
                this.group.position.copy(this.position);
                this.group.rotation.y = this.rotation;

                // Health Bar
                this.createHealthBar();

                // Animations (wenn vorhanden)
                if (gltf.animations && gltf.animations.length > 0) {
                    this.mixer = new THREE.AnimationMixer(this.model);
                    enemyMixers.push(this.mixer);

                    gltf.animations.forEach(clip => {
                        this.animations[clip.name] = this.mixer.clipAction(clip);
                    });

                    // Play idle animation
                    if (this.animations['Idle']) {
                        this.animations['Idle'].play();
                    }
                }

                this.scene.add(this.group);
                this.isLoaded = true;

                console.log(`✅ Enemy loaded: ${this.data.name} (Lv ${this.level})`);
            } catch (error) {
                console.error('❌ Enemy load failed:', error);
            }
        }

        loadGLTF(url) {
            return new Promise((resolve, reject) => {
                const loader = new THREE.GLTFLoader();
                loader.load(url, resolve, undefined, reject);
            });
        }

        createHealthBar() {
            // Simple 3D health bar above enemy
            const barWidth = 2;
            const barHeight = 0.2;

            const barGeometry = new THREE.PlaneGeometry(barWidth, barHeight);
            const barMaterial = new THREE.MeshBasicMaterial({
                color: 0x00ff00,
                side: THREE.DoubleSide
            });

            this.healthBar = new THREE.Mesh(barGeometry, barMaterial);
            this.healthBar.position.y = 3; // Above model
            this.healthBar.renderOrder = 999; // Always on top

            this.group.add(this.healthBar);
        }

        updateHealthBar() {
            if (!this.healthBar) return;

            const healthPercent = Math.max(0, this.hp / this.maxHp);

            // Color: Green -> Yellow -> Red
            let color;
            if (healthPercent > 0.5) {
                color = new THREE.Color(0x00ff00); // Green
            } else if (healthPercent > 0.2) {
                color = new THREE.Color(0xffff00); // Yellow
            } else {
                color = new THREE.Color(0xff0000); // Red
            }

            this.healthBar.material.color = color;
            this.healthBar.scale.x = healthPercent;
        }

        generatePatrolPoints(center) {
            // Generate 3-5 random patrol points around spawn
            const points = [];
            const count = 3 + Math.floor(Math.random() * 3);
            const radius = 5;

            for (let i = 0; i < count; i++) {
                const angle = (i / count) * Math.PI * 2;
                const x = center[0] + Math.cos(angle) * radius;
                const z = center[2] + Math.sin(angle) * radius;
                points.push(new THREE.Vector3(x, 0, z));
            }

            return points;
        }

        update(delta, playerPosition) {
            if (this.isDead || !this.isLoaded) return;

            this.stateTimer += delta;
            this.attackCooldown = Math.max(0, this.attackCooldown - delta);

            // Update AI based on state
            switch (this.state) {
                case AI_STATE.IDLE:
                    this.updateIdle(delta);
                    break;
                case AI_STATE.PATROL:
                    this.updatePatrol(delta);
                    break;
                case AI_STATE.CHASE:
                    this.updateChase(delta, playerPosition);
                    break;
                case AI_STATE.ATTACK:
                    this.updateAttack(delta, playerPosition);
                    break;
            }

            // Check if player in range -> chase
            if (playerPosition && this.state !== AI_STATE.ATTACK) {
                const distToPlayer = this.position.distanceTo(playerPosition);
                if (distToPlayer < 15) { // Aggro range
                    this.state = AI_STATE.CHASE;
                }
            }

            // Apply velocity
            this.position.add(this.velocity);
            this.group.position.copy(this.position);
            this.group.rotation.y = this.rotation;

            // Billboard health bar towards camera
            if (this.healthBar && window.Scene3D && Scene3D.camera) {
                this.healthBar.lookAt(Scene3D.camera.position);
            }
        }

        updateIdle(delta) {
            this.velocity.set(0, 0, 0);

            // Nach 2-5 Sekunden -> Patrol
            if (this.stateTimer > 2 + Math.random() * 3) {
                this.state = AI_STATE.PATROL;
                this.stateTimer = 0;
            }
        }

        updatePatrol(delta) {
            const target = this.patrolPoints[this.currentPatrolIndex];
            const direction = target.clone().sub(this.position);
            const distance = direction.length();

            if (distance < 0.5) {
                // Reached patrol point -> next
                this.currentPatrolIndex = (this.currentPatrolIndex + 1) % this.patrolPoints.length;
                this.state = AI_STATE.IDLE;
                this.stateTimer = 0;
            } else {
                // Move towards patrol point
                direction.normalize();
                this.velocity.set(direction.x * this.speed * delta, 0, direction.z * this.speed * delta);
                this.rotation = Math.atan2(direction.x, direction.z);
            }
        }

        updateChase(delta, playerPosition) {
            if (!playerPosition) {
                this.state = AI_STATE.PATROL;
                return;
            }

            const direction = playerPosition.clone().sub(this.position);
            const distance = direction.length();

            if (distance > 20) {
                // Player zu weit -> zurück zu Patrol
                this.state = AI_STATE.PATROL;
                this.stateTimer = 0;
            } else if (distance < this.attackRange) {
                // In Attack Range -> Attack
                this.state = AI_STATE.ATTACK;
                this.stateTimer = 0;
                this.velocity.set(0, 0, 0);
            } else {
                // Chase player
                direction.normalize();
                this.velocity.set(direction.x * this.speed * delta * 2, 0, direction.z * this.speed * delta * 2);
                this.rotation = Math.atan2(direction.x, direction.z);
            }
        }

        updateAttack(delta, playerPosition) {
            if (!playerPosition) {
                this.state = AI_STATE.CHASE;
                return;
            }

            const distance = this.position.distanceTo(playerPosition);

            if (distance > this.attackRange * 1.5) {
                // Player escaped -> chase
                this.state = AI_STATE.CHASE;
            } else {
                // Face player
                const direction = playerPosition.clone().sub(this.position);
                this.rotation = Math.atan2(direction.x, direction.z);

                // Attack every 1-2 seconds
                if (this.attackCooldown <= 0) {
                    this.performAttack(playerPosition);
                    this.attackCooldown = 1 + Math.random();
                }
            }
        }

        performAttack(playerPosition) {
            let damage = this.damage;
            let isCrit = false;

            // 💥 CRIT MECHANIC: Wenn Player staggered ist, 50% Crit Chance!
            if (window.DungeonEnemies && window.DungeonEnemies.playerIsStaggered) {
                if (Math.random() < 0.5) {
                    isCrit = true;
                    console.log(`💀 ${this.data.name} CRITICAL HIT! Player is staggered!`);
                }
            }

            console.log(`⚔️ ${this.data.name} attacks! Damage: ${damage}${isCrit ? ' (CRIT!)' : ''}`);

            // Play attack animation
            if (this.animations['Attack']) {
                this.animations['Attack'].reset().play();
            }

            // Damage Player via COMBAT_SYSTEM
            if (window.Scene3D && window.Scene3D.COMBAT_SYSTEM) {
                const actualDamage = window.Scene3D.COMBAT_SYSTEM.takeDamage(damage, isCrit);
                console.log(`💥 Player took ${actualDamage} damage!`);
            }

            // Legacy event trigger
            if (typeof window.onEnemyAttack === 'function') {
                window.onEnemyAttack(damage, this.position, isCrit);
            }
        }

        takeDamage(amount) {
            if (this.isDead) return;

            this.hp = Math.max(0, this.hp - amount);
            this.updateHealthBar();

            console.log(`💥 ${this.data.name} took ${amount} damage! HP: ${this.hp}/${this.maxHp}`);

            if (this.hp <= 0) {
                this.die();
            } else {
                // Play hurt animation
                if (this.animations['Hit']) {
                    this.animations['Hit'].reset().play();
                }
                this.state = AI_STATE.HURT;
                setTimeout(() => {
                    if (!this.isDead) this.state = AI_STATE.CHASE;
                }, 500);
            }
        }

        die() {
            this.isDead = true;
            this.state = AI_STATE.DEAD;

            console.log(`💀 ${this.data.name} defeated! +${this.xp} XP`);

            // Play death animation
            if (this.animations['Death']) {
                this.animations['Death'].reset().play();
            }

            // Fade out and remove
            setTimeout(() => {
                if (this.group) {
                    this.scene.remove(this.group);
                    const index = activeEnemies.indexOf(this);
                    if (index > -1) activeEnemies.splice(index, 1);
                }
            }, 2000);

            // Drop loot
            this.dropLoot();

            // Trigger death event
            if (typeof window.onEnemyKilled === 'function') {
                window.onEnemyKilled(this.xp, this.data.loot, this.position);
            }
        }

        dropLoot() {
            const loot = this.data.loot;
            if (!loot || loot.length === 0) return;

            // Gold-Loot direkt an Player
            loot.forEach(item => {
                if (item.type === 'gold' && window.player) {
                    const amount = item.amount || 10;
                    window.player.gold += amount;
                    if (typeof notify === 'function') notify(`💰 +${amount}G Beute!`, 'success');
                } else {
                    // Item ins Inventar legen
                    if (window.InventorySystem?.addItem) {
                        window.InventorySystem.addItem(item.id || item.type, item.amount || 1);
                        if (typeof notify === 'function') notify(`💎 ${item.name || item.type} erhalten!`, 'info');
                    } else {
                        // Fallback: localStorage
                        try {
                            const inv = JSON.parse(localStorage.getItem('najika_inventory') || '{}');
                            const key = item.id || item.type;
                            inv[key] = (inv[key] || 0) + (item.amount || 1);
                            localStorage.setItem('najika_inventory', JSON.stringify(inv));
                            if (typeof notify === 'function') notify(`💎 ${item.name || item.type} erhalten!`, 'info');
                        } catch(e) { console.error('Loot save error:', e); }
                    }
                }
            });

            // Event emittieren für andere Systeme
            if (window.GameEvents) {
                window.GameEvents.emit('lootDropped', { items: loot, position: this.position });
            }
        }

        dispose() {
            if (this.group) {
                this.scene.remove(this.group);
            }
            if (this.mixer) {
                const index = enemyMixers.indexOf(this.mixer);
                if (index > -1) enemyMixers.splice(index, 1);
            }
        }
    }

    /**
     * Wählt Enemy-Typ basierend auf Dungeon-Level & Schwierigkeit
     */
    function getEnemyTypeForLevel(level) {
        const tier = Math.ceil(level / 3); // Level 1-3 = Tier 1, 4-6 = Tier 2, etc.

        // Pool von Enemies nach Tier
        const tierPools = {
            1: ['skeleton_warrior', 'skeleton_archer', 'haunted_pumpkin'],
            2: ['skeleton_mage', 'skeleton_tank', 'skeleton_axe', 'barrel_mimic', 'crate_golem'],
            3: ['corrupted_knight', 'corrupted_rogue'],
            4: ['corrupted_barbarian', 'dark_sorcerer']
        };

        const pool = tierPools[Math.min(tier, 4)] || tierPools[1];
        return pool[Math.floor(Math.random() * pool.length)];
    }

    /**
     * Spawn enemies from dungeon data - ERWEITERT!
     */
    function spawnEnemies(dungeon, scene) {
        if (!dungeon || !dungeon.enemies) return;

        console.log(`🧟 Spawning ${dungeon.enemies.length} enemies (Level ${dungeon.level})...`);

        dungeon.enemies.forEach((enemyData, index) => {
            // Intelligente Enemy-Auswahl basierend auf Level
            let enemyType;

            if (dungeon.level <= 2) {
                // Early levels: Nur Skelette & Pumpkins
                const earlyPool = ['skeleton_warrior', 'skeleton_archer', 'haunted_pumpkin'];
                enemyType = earlyPool[index % earlyPool.length];
            } else if (dungeon.level <= 5) {
                // Mid levels: Skelette + Mimics
                const midPool = ['skeleton_mage', 'skeleton_tank', 'skeleton_axe', 'barrel_mimic', 'crate_golem'];
                enemyType = midPool[index % midPool.length];
            } else if (dungeon.level <= 8) {
                // High levels: Corrupted Heroes
                const highPool = ['corrupted_knight', 'corrupted_rogue', 'skeleton_mage', 'skeleton_axe'];
                enemyType = highPool[index % highPool.length];
            } else {
                // End-game: Bosses & Elite
                const bossPool = ['corrupted_barbarian', 'dark_sorcerer', 'corrupted_knight'];
                enemyType = bossPool[index % bossPool.length];
            }

            // Fallback: Generic mapping
            if (!ENEMY_TYPES[enemyType]) {
                enemyType = getEnemyTypeForLevel(dungeon.level);
            }

            const enemy = new Enemy(enemyType, enemyData.position, enemyData.level || dungeon.level, scene);
            enemy.load();
            activeEnemies.push(enemy);
        });
    }

    /**
     * Update all active enemies
     */
    function updateEnemies(playerPosition) {
        const delta = clock.getDelta();

        // Update animation mixers
        enemyMixers.forEach(mixer => {
            mixer.update(delta);
        });

        // Update each enemy AI
        activeEnemies.forEach(enemy => {
            enemy.update(delta, playerPosition);
        });
    }

    /**
     * Clear all enemies (on room change)
     */
    function clearAllEnemies() {
        activeEnemies.forEach(enemy => enemy.dispose());
        activeEnemies = [];
        enemyMixers = [];
        console.log('🧹 All enemies cleared');
    }

    /**
     * Damage nearest enemy (player attack)
     */
    function damageNearestEnemy(playerPosition, damage, range = 3) {
        if (!playerPosition) return null;

        let nearest = null;
        let nearestDist = Infinity;

        activeEnemies.forEach(enemy => {
            if (enemy.isDead) return;
            const dist = enemy.position.distanceTo(playerPosition);
            if (dist < range && dist < nearestDist) {
                nearest = enemy;
                nearestDist = dist;
            }
        });

        if (nearest) {
            nearest.takeDamage(damage);
            return nearest;
        }

        return null;
    }

    /**
     * Get all living enemies
     */
    function getLivingEnemies() {
        return activeEnemies.filter(e => !e.isDead);
    }

    // Public API
    window.DungeonEnemies = {
        spawnEnemies,
        updateEnemies,
        clearAllEnemies,
        damageNearestEnemy,
        getLivingEnemies,
        getActiveEnemies: () => activeEnemies,
        damageEnemy: (enemyId, damage) => {
            const enemy = activeEnemies.find(e => e.group && e.group.userData.enemyId === enemyId);
            if (enemy) {
                enemy.takeDamage(damage);
                return true;
            }
            return false;
        },
        playerIsStaggered: false,  // Flag für CRIT Mechanic
        Enemy,
        ENEMY_TYPES,
        AI_STATE
    };

    console.log('🧟 Dungeon Enemy System initialized');
})();
