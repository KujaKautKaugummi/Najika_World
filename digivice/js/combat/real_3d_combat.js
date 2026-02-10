/**
 * REAL 3D COMBAT SYSTEM - Najika World
 * =====================================
 *
 * ERSETZT den Text-basierten Kampf mit ECHTEN 3D Gegnern!
 *
 * Nutzt:
 * - KayKit 3D Models (Skelette, Adventurers, etc.)
 * - Echte Hitboxen und Kollisionen
 * - Visuelle Angriffs-Animationen
 *
 * MODES:
 * - MANUAL: Q/E für Angriffe, Q+E für Dual-Attack, Space für Dodge
 * - AUTO: KI kämpft
 * - CHEER: Anfeuern (Digimon Style)
 */

(function() {
    'use strict';

    // ==========================================
    // COMBAT STATE
    // ==========================================

    let combatActive = false;
    let combatMode = 'MANUAL'; // MANUAL, AUTO, CHEER
    let currentEnemies = [];
    let playerStats = {
        hp: 100,
        maxHp: 100,
        stamina: 100,
        maxStamina: 100,
        mana: 100,
        maxMana: 100
    };

    // Combo System
    let comboCount = 0;
    let lastAttackTime = 0;
    const COMBO_WINDOW = 1500; // 1.5 seconds

    // Cooldowns
    let attackCooldown = 0;
    let dodgeCooldown = 0;
    let skillCooldowns = {};

    // Animation
    let animationFrame = null;
    const clock = new THREE.Clock();

    // AUTO Mode AI
    let autoModeInterval = null;
    let autoAttackTimer = 0;

    // CHEER Mode Buffs
    let cheerBuffs = {
        attack: 0,   // Rounds remaining
        defend: 0,
        combo: 0,
        focus: 0
    };

    // Dual-Attack System (Q+E gleichzeitig)
    let dualAttackState = {
        qPressed: false,
        ePressed: false,
        qTime: 0,
        eTime: 0,
        dualWindow: 120,  // ms Fenster für "gleichzeitig"
        dualPending: null  // Timer für verzögertes Single-Attack
    };

    // Finisher System
    let finisherMeter = 0;
    const FINISHER_MAX = 100;
    let lastFinisherTime = 0;
    const FINISHER_COOLDOWN = 24 * 60 * 60 * 1000; // 24h
    let finisherQTEActive = false;
    let finisherQTESequence = [];
    let finisherQTEIndex = 0;
    let finisherQTETimer = null;
    let finisherTarget = null;

    // Loot Collection
    let collectedLoot = [];
    let totalXPEarned = 0;

    // Damage Number pool
    let damageNumbers = [];

    // ==========================================
    // KAYKIT ENEMY MODELS MAPPING
    // ==========================================

    const KAYKIT_MODELS = {
        // Skeletons
        skeleton_warrior: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_warrior.gltf',
        skeleton_archer: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_archer.gltf',
        skeleton_mage: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_mage.gltf',
        skeleton_minion: 'KayKit Character Pack - Skeletons 1.0/Models/characters/gltf/character_skeleton_minion.gltf',

        // Dungeon Pack Characters
        knight: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf',
        barbarian: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_barbarian.gltf',
        mage: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_mage.gltf',
        rogue: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_rogue.gltf',

        // Halloween
        witch: 'KayKit Spooktober Seasonal Pack 1.1/Models/Characters/Witch/gltf/character_witch.gltf',

        // Generic fallback
        default: 'KayKit Dungeon Pack 1.0/Models/Characters/gltf/character_knight.gltf'
    };

    // ==========================================
    // ENEMY TYPES WITH STATS
    // ==========================================

    const ENEMY_TYPES = {
        // === TIER 1: Easy ===
        bat: {
            name: 'Höhlenfledermaus',
            model: 'skeleton_minion',
            hp: 15, damage: 3, speed: 2.0,
            attackRange: 2, xp: 5, tier: 1,
            loot: ['bat_wing']
        },
        slime: {
            name: 'Schleim',
            model: 'default',
            hp: 20, damage: 2, speed: 0.5,
            attackRange: 1.5, xp: 8, tier: 1,
            loot: ['slime_goo'],
            color: 0x00ff00
        },
        skeleton_warrior: {
            name: 'Skelett-Krieger',
            model: 'skeleton_warrior',
            hp: 30, damage: 8, speed: 1.2,
            attackRange: 2.5, xp: 15, tier: 1,
            loot: ['bone', 'sword_rusty']
        },
        skeleton_archer: {
            name: 'Skelett-Bogenschütze',
            model: 'skeleton_archer',
            hp: 20, damage: 10, speed: 1.0,
            attackRange: 10, xp: 18, tier: 1,
            loot: ['bone', 'arrow']
        },

        // === TIER 2: Medium ===
        wolf: {
            name: 'Wolf',
            model: 'skeleton_minion',
            hp: 40, damage: 12, speed: 2.5,
            attackRange: 2, xp: 25, tier: 2,
            loot: ['wolf_pelt', 'wolf_fang'],
            color: 0x888888
        },
        goblin: {
            name: 'Goblin',
            model: 'rogue',
            hp: 35, damage: 10, speed: 1.8,
            attackRange: 2, xp: 22, tier: 2,
            loot: ['gold_coin', 'dagger_crude'],
            color: 0x00aa00
        },
        skeleton_mage: {
            name: 'Skelett-Magier',
            model: 'skeleton_mage',
            hp: 25, damage: 18, speed: 0.8,
            attackRange: 8, xp: 30, tier: 2,
            loot: ['bone', 'magic_crystal']
        },

        // === TIER 3: Hard ===
        corrupted_knight: {
            name: 'Verfluchter Ritter',
            model: 'knight',
            hp: 80, damage: 20, speed: 1.0,
            attackRange: 3, xp: 60, tier: 3,
            loot: ['cursed_sword', 'plate_armor_broken'],
            color: 0x440044
        },
        witch: {
            name: 'Hexe',
            model: 'witch',
            hp: 60, damage: 25, speed: 0.9,
            attackRange: 10, xp: 70, tier: 3,
            loot: ['witch_hat', 'potion_empty', 'spell_scroll']
        },

        // === TIER 4: Boss ===
        barbarian_boss: {
            name: 'Berserker-Untoter',
            model: 'barbarian',
            hp: 200, damage: 35, speed: 0.7,
            attackRange: 3, xp: 150, tier: 4,
            loot: ['great_axe', 'berserker_helm', 'rare_gem'],
            isBoss: true
        }
    };

    // ==========================================
    // BIOME -> ENEMY MAPPING (Fixes null biome bug!)
    // ==========================================

    const BIOME_ENEMIES = {
        // === NAJIKA WORLD BIOME NAMES (from overworld_enemies.js) ===
        'samtmoos': ['wolf', 'skeleton_warrior', 'goblin', 'bat'],
        'reich_der_drei': ['skeleton_warrior', 'skeleton_mage', 'wolf'],
        'heisse_duenen': ['skeleton_archer', 'skeleton_mage', 'goblin'],
        'salzwind': ['slime', 'skeleton_warrior', 'bat'],
        'magmastroeme': ['skeleton_warrior', 'corrupted_knight', 'bat', 'skeleton_mage'],
        'gruenschlamm': ['witch', 'slime', 'skeleton_mage', 'bat'],
        'blitzebene': ['wolf', 'goblin', 'corrupted_knight'],
        'tiefenhoehlen': ['bat', 'goblin', 'skeleton_mage', 'slime'],
        'goetterfels': [], // Safe zone - no enemies!

        // === GENERIC BIOME ALIASES ===
        'forest': ['wolf', 'skeleton_warrior', 'goblin', 'bat'],
        'desert': ['skeleton_archer', 'skeleton_mage', 'goblin'],
        'coast': ['slime', 'skeleton_warrior', 'bat'],
        'swamp': ['witch', 'slime', 'skeleton_mage', 'bat'],
        'ice': ['skeleton_warrior', 'skeleton_mage', 'wolf'],
        'volcano': ['skeleton_warrior', 'corrupted_knight', 'bat'],
        'highland': ['wolf', 'goblin', 'corrupted_knight'],
        'caves': ['bat', 'goblin', 'skeleton_mage', 'slime'],
        'mountain': ['wolf', 'skeleton_archer', 'corrupted_knight'],

        // Fallback for null/undefined biome
        'null': ['skeleton_warrior', 'bat', 'slime'],
        'undefined': ['skeleton_warrior', 'bat', 'slime'],
        'default': ['skeleton_warrior', 'bat', 'slime']
    };

    // ==========================================
    // 3D ENEMY CLASS
    // ==========================================

    class Enemy3D {
        constructor(type, position, level = 1, scene) {
            this.type = type;
            this.data = ENEMY_TYPES[type] || ENEMY_TYPES.skeleton_warrior;
            this.level = level;
            this.scene = scene;

            // Stats scaled by level
            this.maxHp = Math.floor(this.data.hp * (1 + level * 0.25));
            this.hp = this.maxHp;
            this.damage = Math.floor(this.data.damage * (1 + level * 0.15));
            this.speed = this.data.speed;
            this.xp = Math.floor(this.data.xp * (1 + level * 0.4));

            // Position
            this.position = new THREE.Vector3(position.x, position.y || 0, position.z);
            this.rotation = Math.random() * Math.PI * 2;

            // AI State
            this.state = 'idle'; // idle, patrol, chase, attack, hurt, dead
            this.target = null;
            this.attackCooldown = 0;

            // 3D Model
            this.group = null;
            this.model = null;
            this.mixer = null;
            this.healthBar = null;
            this.isLoaded = false;
            this.isDead = false;

            // Hitbox for collision
            this.hitbox = null;
        }

        async load() {
            const modelKey = this.data.model || 'default';
            const modelPath = KAYKIT_MODELS[modelKey] || KAYKIT_MODELS.default;

            try {
                const loader = new THREE.GLTFLoader();
                const gltf = await new Promise((resolve, reject) => {
                    loader.load(
                        `static/assets/${modelPath}`,
                        resolve,
                        undefined,
                        reject
                    );
                });

                this.group = new THREE.Group();
                this.model = gltf.scene.clone();
                this.model.scale.setScalar(1.5);

                // Color tint if specified
                if (this.data.color) {
                    this.model.traverse(child => {
                        if (child.isMesh && child.material) {
                            child.material = child.material.clone();
                            child.material.emissive = new THREE.Color(this.data.color);
                            child.material.emissiveIntensity = 0.3;
                        }
                    });
                }

                this.group.add(this.model);
                this.group.position.copy(this.position);
                this.group.rotation.y = this.rotation;

                // Health bar
                this.createHealthBar();

                // Hitbox (invisible sphere for collision)
                const hitboxGeom = new THREE.SphereGeometry(1.5, 8, 8);
                const hitboxMat = new THREE.MeshBasicMaterial({
                    visible: false,
                    transparent: true,
                    opacity: 0
                });
                this.hitbox = new THREE.Mesh(hitboxGeom, hitboxMat);
                this.hitbox.userData.enemy = this;
                this.group.add(this.hitbox);

                // Animations
                if (gltf.animations && gltf.animations.length > 0) {
                    this.mixer = new THREE.AnimationMixer(this.model);
                    this.animations = {};
                    gltf.animations.forEach(clip => {
                        const name = clip.name.toLowerCase().replace(/\s+/g, '');
                        this.animations[name] = this.mixer.clipAction(clip);
                    });
                    this.currentAnim = '';
                    this.playEnemyAnim('idle');
                }

                this.scene.add(this.group);
                this.isLoaded = true;

                console.log(`✅ 3D Enemy loaded: ${this.data.name} (Lv${this.level})`);
                return true;
            } catch (error) {
                console.error(`❌ Failed to load enemy ${this.type}:`, error);
                // Fallback: Create colored cube
                this.createFallbackModel();
                return false;
            }
        }

        createFallbackModel() {
            this.group = new THREE.Group();

            const geometry = new THREE.BoxGeometry(1, 2, 1);
            const material = new THREE.MeshLambertMaterial({
                color: this.data.color || 0xff0000
            });
            this.model = new THREE.Mesh(geometry, material);
            this.model.position.y = 1;

            this.group.add(this.model);
            this.group.position.copy(this.position);

            this.createHealthBar();

            // Hitbox
            const hitboxGeom = new THREE.SphereGeometry(1.5, 8, 8);
            const hitboxMat = new THREE.MeshBasicMaterial({ visible: false });
            this.hitbox = new THREE.Mesh(hitboxGeom, hitboxMat);
            this.hitbox.userData.enemy = this;
            this.group.add(this.hitbox);

            this.scene.add(this.group);
            this.isLoaded = true;
        }

        createHealthBar() {
            const barWidth = 2;
            const barGeometry = new THREE.PlaneGeometry(barWidth, 0.2);
            const barMaterial = new THREE.MeshBasicMaterial({
                color: 0x00ff00,
                side: THREE.DoubleSide
            });

            this.healthBar = new THREE.Mesh(barGeometry, barMaterial);
            this.healthBar.position.y = 3;
            this.group.add(this.healthBar);
        }

        updateHealthBar() {
            if (!this.healthBar) return;

            const percent = this.hp / this.maxHp;
            this.healthBar.scale.x = Math.max(0, percent);

            if (percent > 0.5) {
                this.healthBar.material.color.setHex(0x00ff00);
            } else if (percent > 0.25) {
                this.healthBar.material.color.setHex(0xffff00);
            } else {
                this.healthBar.material.color.setHex(0xff0000);
            }
        }

        update(delta, playerPosition) {
            if (this.isDead || !this.isLoaded) return;

            this.attackCooldown = Math.max(0, this.attackCooldown - delta);

            if (this.mixer) {
                this.mixer.update(delta);
            }

            // AI
            if (playerPosition) {
                const distance = this.position.distanceTo(playerPosition);
                const prevState = this.state;

                if (distance < this.data.attackRange) {
                    // Attack!
                    if (this.attackCooldown <= 0) {
                        this.attack(playerPosition);
                        this.attackCooldown = 1 + Math.random() * 0.5;
                    }
                    this.state = 'attack';
                } else if (distance < 15) {
                    // Chase
                    this.state = 'chase';
                    const direction = playerPosition.clone().sub(this.position).normalize();
                    this.position.add(direction.multiplyScalar(this.speed * delta));
                    this.rotation = Math.atan2(direction.x, direction.z);
                } else {
                    this.state = 'idle';
                }

                // State-basierte Animation (nur bei State-Wechsel)
                if (this.mixer && prevState !== this.state) {
                    if (this.state === 'chase') {
                        this.playEnemyAnim('run');
                    } else if (this.state === 'idle') {
                        this.playEnemyAnim('idle');
                    }
                    // 'attack' wird in attack() direkt getriggert
                }
            }

            this.group.position.copy(this.position);
            this.group.rotation.y = this.rotation;

            // Billboard healthbar
            if (this.healthBar && window.Scene3D?.camera) {
                this.healthBar.lookAt(Scene3D.camera.position);
            }
        }

        playEnemyAnim(name, loop = true, fadeTime = 0.2) {
            if (!this.mixer || !this.animations) return;
            name = name.toLowerCase();

            // Name mapping for KayKit animations
            const MAP = {
                'attack': 'attack(1h)', 'cast': 'shoot(1h)',
                'dodge': 'roll', 'block': 'block',
                'die': 'defeat', 'death': 'defeat',
                'hurt': 'hit', 'damage': 'hit'
            };
            const mapped = MAP[name] || name;
            const action = this.animations[mapped] || this.animations[name];
            if (!action) return;
            if (this.currentAnim === name) return;

            // Fade out all running
            Object.values(this.animations).forEach(a => {
                if (a.isRunning()) a.fadeOut(fadeTime);
            });

            action.reset();
            action.fadeIn(fadeTime);
            action.setLoop(loop ? THREE.LoopRepeat : THREE.LoopOnce);
            if (!loop) action.clampWhenFinished = true;
            action.play();
            this.currentAnim = name;
        }

        attack(playerPosition) {
            console.log(`⚔️ ${this.data.name} greift an! -${this.damage} HP`);
            this.playEnemyAnim('attack', false);

            // Damage player
            takeDamage(this.damage, this.data.name);

            // Notify UnifiedCombat if it exists
            if (typeof UnifiedCombat !== 'undefined' && UnifiedCombat.notify) {
                UnifiedCombat.notify(`${this.data.name} greift an! -${this.damage} HP`);
            }
        }

        takeDamage(amount, isCrit = false) {
            if (this.isDead) return;

            this.hp -= amount;
            this.updateHealthBar();

            // Hit animation (kurz, dann zurück zum vorherigen State)
            if (this.mixer && this.state !== 'dead') {
                this.playEnemyAnim('hurt', false);
                setTimeout(() => {
                    if (!this.isDead) {
                        this.playEnemyAnim(this.state === 'chase' ? 'run' : 'idle');
                    }
                }, 400);
            }

            // Visual feedback - flash red
            if (this.model) {
                this.model.traverse(child => {
                    if (child.isMesh && child.material) {
                        const origColor = child.material.emissive?.clone() || new THREE.Color(0);
                        child.material.emissive = new THREE.Color(0xff0000);
                        setTimeout(() => {
                            if (child.material) child.material.emissive = origColor;
                        }, 100);
                    }
                });
            }

            // Floating Damage Number
            spawnDamageNumber(amount, this.position, isCrit);

            // Finisher Meter gain
            gainFinisher('normalAttack');

            console.log(`💥 ${this.data.name}: -${amount} HP (${this.hp}/${this.maxHp})`);

            if (this.hp <= 0) {
                this.die();
            }
        }

        die() {
            this.isDead = true;
            this.state = 'dead';

            // Death animation
            this.playEnemyAnim('die', false);

            console.log(`💀 ${this.data.name} besiegt! +${this.xp} XP`);

            // Collect loot
            if (this.data.loot && this.data.loot.length > 0) {
                this.data.loot.forEach(item => collectedLoot.push(item));
                console.log(`💎 Loot: ${this.data.loot.join(', ')}`);
                spawnLootDrop(this.position, this.data.loot);
            }

            // Track XP
            totalXPEarned += this.xp;

            // Notify systems
            if (typeof UnifiedCombat !== 'undefined' && UnifiedCombat.notify) {
                UnifiedCombat.notify(`💀 ${this.data.name} besiegt! +${this.xp} XP`);
            }

            // Add XP
            addXP(this.xp);

            // Track kill in Bestiary
            if (window.bestiaryTrackKill) {
                window.bestiaryTrackKill(this.type);
            }

            // Finisher meter bonus for kill
            gainFinisher('combo5');

            // Fade out
            if (this.group) {
                const fadeOut = () => {
                    if (!this.group) return;
                    this.group.scale.multiplyScalar(0.9);
                    this.group.position.y -= 0.1;
                    if (this.group.scale.x > 0.1) {
                        requestAnimationFrame(fadeOut);
                    } else {
                        this.dispose();
                    }
                };
                setTimeout(fadeOut, 500);
            }

            // Remove from enemies list
            const index = currentEnemies.indexOf(this);
            if (index > -1) currentEnemies.splice(index, 1);

            // Check victory
            checkVictory();
        }

        dispose() {
            if (this.group && this.scene) {
                this.scene.remove(this.group);
            }
            this.group = null;
            this.model = null;
        }
    }

    // ==========================================
    // PLAYER FUNCTIONS
    // ==========================================

    function takeDamage(amount, source = 'Unknown') {
        // Cheer defense buff
        let finalAmount = amount;
        if (cheerBuffs.defend > 0) {
            finalAmount = Math.floor(amount * 0.8); // -20% damage
            cheerBuffs.defend--;
        }

        // Equipment armor reduction
        if (window.EquipmentCombat) {
            const ecResult = EquipmentCombat.takeDamage(finalAmount);
            if (ecResult === 0) return; // Dodged
            if (ecResult === -1) return; // Parried
            finalAmount = ecResult;
        }

        playerStats.hp = Math.max(0, playerStats.hp - finalAmount);

        // Player Hit Animation
        if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
            window.CharacterAnimations.playHit();
        }

        updateCombatHUD();

        // Screen flash
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed; inset: 0;
            background: rgba(255, 0, 0, 0.3);
            pointer-events: none;
            z-index: 9999;
            animation: fadeOut 0.3s forwards;
        `;
        document.body.appendChild(flash);
        setTimeout(() => flash.remove(), 300);

        if (playerStats.hp <= 0) {
            gameOver();
        }
    }

    function heal(amount) {
        playerStats.hp = Math.min(playerStats.maxHp, playerStats.hp + amount);
        updateCombatHUD();
    }

    function addXP(amount) {
        console.log(`+${amount} XP`);
        if (window.GameEvents) {
            window.GameEvents.emit('xpGained', { amount, source: 'combat' });
        }
        // Connect to skill system
        if (window.skillSystem && window.skillSystem.addXP) {
            window.skillSystem.addXP('combat', amount);
        }
    }

    // ==========================================
    // COMBAT FUNCTIONS
    // ==========================================

    function startCombat(enemyList, scene, position) {
        combatActive = true;
        currentEnemies = [];
        collectedLoot = [];
        totalXPEarned = 0;
        finisherMeter = 0;
        comboCount = 0;
        cheerBuffs = { attack: 0, defend: 0, combo: 0, focus: 0 };

        enemyList.forEach((enemyType, i) => {
            const offset = {
                x: position.x + (Math.random() - 0.5) * 10,
                y: 0,
                z: position.z + (Math.random() - 0.5) * 10
            };

            const level = 1 + Math.floor(Math.random() * 3);
            const enemy = new Enemy3D(enemyType, offset, level, scene);
            enemy.load();
            currentEnemies.push(enemy);
            // Track encounter in Bestiary
            if (window.bestiaryTrackEncounter) window.bestiaryTrackEncounter(enemyType);
        });

        combatMode = 'MANUAL'; // Immer im manuellen Modus starten
        createCombatHUD();
        startCombatLoop();

        console.log(`⚔️ Combat started: ${enemyList.length} enemies! Mode: ${combatMode}`);

        // Emit GameEvent
        if (window.GameEvents) {
            window.GameEvents.emit('combatStarted', {
                type: 'real3d',
                enemyCount: currentEnemies.length,
                enemies: currentEnemies.map(e => ({ id: e.type, name: e.name, level: e.level }))
            });
        }
    }

    function attackNearestEnemy(damage, range = 5, hand = 'right', isHeavy = false) {
        if (!combatActive) return null;

        const playerPos = getPlayerPosition();
        if (!playerPos) return null;

        // Player Attack Animation
        if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
            window.CharacterAnimations.playAttack(isHeavy ? 'heavy' : 'light');
        }
        // Companion Animation (Najika greift mit an)
        if (window.Companion3D) {
            window.Companion3D.playAttack();
        }

        // Try to get equipment-based damage
        let finalDamage = damage;
        let weaponRange = range;
        let isCrit = false;
        let element = null;

        if (window.EquipmentCombat) {
            const ec = EquipmentCombat;
            const result = isHeavy ? ec.attackHeavy(hand) : ec.attackLight(hand);
            if (result) {
                finalDamage = result.damage;
                weaponRange = result.range || range;
                isCrit = result.combo > 2;
                element = result.element;
            }
        }

        let nearest = null;
        let nearestDist = Infinity;

        currentEnemies.forEach(enemy => {
            if (enemy.isDead) return;
            const dist = enemy.position.distanceTo(playerPos);
            if (dist < weaponRange && dist < nearestDist) {
                nearest = enemy;
                nearestDist = dist;
            }
        });

        if (nearest) {
            // Combo bonus
            const now = Date.now();
            if (now - lastAttackTime < COMBO_WINDOW) {
                comboCount++;
            } else {
                comboCount = 1;
            }
            lastAttackTime = now;

            // Cheer buff bonus
            let cheerMultiplier = 1.0;
            if (cheerBuffs.attack > 0) { cheerMultiplier *= 1.1; cheerBuffs.attack--; }
            if (cheerBuffs.combo > 0) { cheerMultiplier *= 1.3; cheerBuffs.combo--; }
            if (cheerBuffs.focus > 0 && Math.random() < 0.15) {
                isCrit = true;
                cheerBuffs.focus--;
            }

            const comboDamage = Math.floor(finalDamage * (1 + comboCount * 0.1) * cheerMultiplier * (isCrit ? 2.0 : 1.0));
            nearest.takeDamage(comboDamage, isCrit);

            if (isCrit) {
                console.log(`💥 KRITISCH! ${comboDamage} Schaden!`);
            }
            if (comboCount > 1) {
                console.log(`🔥 ${comboCount}-Hit Combo! ${comboDamage} Schaden!`);
            }

            // Check finisher availability
            if (canUseFinisher(nearest)) {
                showFinisherPrompt();
            }

            return nearest;
        }

        return null;
    }

    // ==========================================
    // DUAL-ATTACK (Beide Hände gleichzeitig!)
    // ==========================================

    function dualAttackNearestEnemy(isHeavy = false) {
        if (!combatActive) return null;

        const playerPos = getPlayerPosition();
        if (!playerPos) return null;

        // Dual-Attack Animation (spinning attack)
        if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
            window.CharacterAnimations.playAttack('spin');
        }
        if (window.Companion3D) {
            window.Companion3D.playAttack();
        }

        // Equipment-based Dual-Attack
        let finalDamage = 30; // Base Dual Damage
        let weaponRange = 5;
        let isCrit = false;
        let element = null;
        let isDual = true;

        if (window.EquipmentCombat && EquipmentCombat.attackDual) {
            const result = EquipmentCombat.attackDual(isHeavy);
            if (result) {
                finalDamage = result.damage;
                weaponRange = result.range || 5;
                isCrit = result.isCrit || false;
                element = result.element;
            } else {
                // Fallback: kein Dual möglich (z.B. nur eine Waffe) → normaler Angriff
                console.log('⚠️ Dual-Attack nicht möglich, normaler Angriff!');
                return attackNearestEnemy(15, 4, 'right', isHeavy);
            }
        } else {
            // Ohne EquipmentCombat: einfacher Dual-Bonus
            finalDamage = isHeavy ? 50 : 30;
        }

        // Nächsten Gegner finden
        let nearest = null;
        let nearestDist = Infinity;

        currentEnemies.forEach(enemy => {
            if (enemy.isDead) return;
            const dist = enemy.position.distanceTo(playerPos);
            if (dist < weaponRange && dist < nearestDist) {
                nearest = enemy;
                nearestDist = dist;
            }
        });

        if (nearest) {
            // Combo - Dual zählt als 2 Hits!
            const now = Date.now();
            if (now - lastAttackTime < COMBO_WINDOW) {
                comboCount += 2;
            } else {
                comboCount = 2;
            }
            lastAttackTime = now;

            // Cheer Buffs
            let cheerMultiplier = 1.0;
            if (cheerBuffs.attack > 0) { cheerMultiplier *= 1.1; cheerBuffs.attack--; }
            if (cheerBuffs.combo > 0) { cheerMultiplier *= 1.3; cheerBuffs.combo--; }
            if (cheerBuffs.focus > 0 && Math.random() < 0.15) {
                isCrit = true;
                cheerBuffs.focus--;
            }

            const totalDamage = Math.floor(finalDamage * cheerMultiplier * (isCrit ? 2.0 : 1.0));
            nearest.takeDamage(totalDamage, isCrit);

            // Finisher Meter - Dual gibt extra!
            gainFinisher('normalAttack');
            gainFinisher('normalAttack'); // Doppelt!

            // Visuals
            if (isCrit) {
                console.log(`💥💥 DUAL KRIT! ${totalDamage} Schaden!`);
            } else {
                console.log(`⚔️⚔️ DUAL-ATTACK! ${totalDamage} Schaden! (${comboCount}-Hit Combo)`);
            }

            // Show dual notification
            showDualAttackNotification(isHeavy, totalDamage, isCrit);

            if (canUseFinisher(nearest)) {
                showFinisherPrompt();
            }

            return nearest;
        }

        return null;
    }

    function showDualAttackNotification(isHeavy, damage, isCrit) {
        const notif = document.createElement('div');
        notif.style.cssText = `
            position: fixed; top: 30%; left: 50%; transform: translateX(-50%);
            font-size: ${isCrit ? '42px' : '32px'}; font-weight: bold; z-index: 10001;
            color: ${isCrit ? '#ff00ff' : '#ff8800'}; text-shadow: 0 0 20px ${isCrit ? '#ff00ff' : '#ff4400'}, 0 0 40px rgba(0,0,0,0.8);
            pointer-events: none; font-family: 'Press Start 2P', monospace;
            animation: dualAttackPulse 0.8s ease-out forwards;
        `;
        notif.textContent = isCrit
            ? `💥💥 DUAL KRIT! ${damage} 💥💥`
            : `⚔️⚔️ ${isHeavy ? 'DUAL HEAVY' : 'DUAL STRIKE'}! ${damage}`;
        document.body.appendChild(notif);

        // CSS Animation injizieren (falls noch nicht da)
        if (!document.getElementById('dual-attack-styles')) {
            const style = document.createElement('style');
            style.id = 'dual-attack-styles';
            style.textContent = `
                @keyframes dualAttackPulse {
                    0% { opacity: 1; transform: translateX(-50%) scale(1.5); }
                    50% { opacity: 1; transform: translateX(-50%) scale(1.0); }
                    100% { opacity: 0; transform: translateX(-50%) scale(0.8) translateY(-40px); }
                }
            `;
            document.head.appendChild(style);
        }

        setTimeout(() => notif.remove(), 800);
    }

    function getPlayerPosition() {
        if (window.Scene3D?.characterGroup) {
            return Scene3D.characterGroup.position.clone();
        }
        return null;
    }

    function checkVictory() {
        const living = currentEnemies.filter(e => !e.isDead);
        if (living.length === 0 && combatActive) {
            victory();
        }
    }

    function victory() {
        combatActive = false;
        combatMode = 'MANUAL'; // Modus zurücksetzen
        stopCombatLoop();
        stopAutoMode();

        // Victory Animation (Cheer!)
        if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
            window.CharacterAnimations.playCheer();
        }

        console.log('🎉 SIEG!');

        if (typeof notify === 'function') {
            notify('🎉 Alle Gegner besiegt!', 'success');
        }

        // Show loot summary
        showLootSummary(totalXPEarned, collectedLoot);

        // Notify game systems
        if (typeof window.onCombatVictory === 'function') {
            window.onCombatVictory({
                type: 'real3d',
                xp: totalXPEarned,
                loot: collectedLoot
            });
        }

        // Add loot to inventory
        addLootToInventory(collectedLoot);

        removeCombatHUD();

        // Emit GameEvent
        if (window.GameEvents) {
            window.GameEvents.emit('combatEnded', {
                type: 'real3d',
                result: 'victory',
                xp: totalXPEarned,
                loot: collectedLoot,
                enemies: currentEnemies.map(e => ({ id: e.type, name: e.name, level: e.level }))
            });
        }
    }

    function gameOver() {
        combatActive = false;
        stopCombatLoop();
        stopAutoMode();
        hideFinisherQTE();

        // Defeat Animation
        if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
            window.CharacterAnimations.playDefeat();
        }

        console.log('💀 GAME OVER');

        if (typeof notify === 'function') {
            notify('💀 Du wurdest besiegt!', 'error');
        }

        // Notify game systems
        if (typeof window.onCombatDefeat === 'function') {
            window.onCombatDefeat({ type: 'real3d' });
        }

        // Show defeat overlay, then respawn
        showDefeatScreen();

        // Emit GameEvent
        if (window.GameEvents) {
            window.GameEvents.emit('combatEnded', {
                type: 'real3d',
                result: 'defeat',
                enemies: currentEnemies.map(e => ({ id: e.type, name: e.name, level: e.level }))
            });
        }

        setTimeout(() => {
            playerStats.hp = Math.floor(playerStats.maxHp / 2);
            removeCombatHUD();
            damageNumbers.forEach(dn => dn.element?.remove());
            damageNumbers = [];
        }, 2000);
    }

    // ==========================================
    // COMBAT LOOP
    // ==========================================

    function startCombatLoop() {
        const loop = () => {
            if (!combatActive) return;

            const delta = clock.getDelta();
            const playerPos = getPlayerPosition();

            currentEnemies.forEach(enemy => {
                enemy.update(delta, playerPos);
            });

            // Update floating damage numbers
            updateDamageNumbers(delta);

            // AUTO mode AI
            if (combatMode === 'AUTO') {
                autoAttackTimer -= delta;
                if (autoAttackTimer <= 0) {
                    performAutoAction();
                    autoAttackTimer = 0.6 + Math.random() * 0.4; // 0.6-1.0s interval
                }
            }

            // CHEER mode - KI fights automatically
            if (combatMode === 'CHEER') {
                autoAttackTimer -= delta;
                if (autoAttackTimer <= 0) {
                    performAutoAction();
                    autoAttackTimer = 0.8 + Math.random() * 0.5; // Slightly slower
                }
            }

            updateCombatHUD();

            animationFrame = requestAnimationFrame(loop);
        };

        loop();
    }

    function stopCombatLoop() {
        if (animationFrame) {
            cancelAnimationFrame(animationFrame);
            animationFrame = null;
        }
    }

    // ==========================================
    // COMBAT HUD
    // ==========================================

    function createCombatHUD() {
        let hud = document.getElementById('real-combat-hud');
        if (hud) return;

        hud = document.createElement('div');
        hud.id = 'real-combat-hud';
        hud.style.cssText = `
            position: fixed;
            bottom: 70px;
            left: 0; right: 0;
            background: rgba(0,0,0,0.9);
            padding: 10px 20px;
            color: white;
            font-family: monospace;
            z-index: 900;
            border-top: 2px solid #ff4444;
        `;
        document.body.appendChild(hud);

        updateCombatHUD();
    }

    function updateCombatHUD() {
        const hud = document.getElementById('real-combat-hud');
        if (!hud) return;

        const hpPercent = Math.floor((playerStats.hp / playerStats.maxHp) * 100);
        let hpColor = '#00ff00';
        if (hpPercent < 60) hpColor = '#ffff00';
        if (hpPercent < 30) hpColor = '#ff0000';

        const enemyCount = currentEnemies.filter(e => !e.isDead).length;

        // Mode display
        const modeIcons = { 'MANUAL': '🎮', 'AUTO': '🤖', 'CHEER': '📣' };
        const modeColors = { 'MANUAL': '#00ff00', 'AUTO': '#00aaff', 'CHEER': '#ffaa00' };

        // Finisher meter bar
        const finisherPercent = Math.floor((finisherMeter / FINISHER_MAX) * 100);
        const finisherColor = finisherMeter >= FINISHER_MAX ? '#ff00ff' : '#8844ff';
        const finisherReady = canUseFinisherAny();

        // Controls text based on mode
        let controlsText = '';
        if (combatMode === 'MANUAL') {
            controlsText = 'Q/E = Angriff | Space = Dodge | M = Modus';
        } else if (combatMode === 'AUTO') {
            controlsText = 'KI kämpft automatisch | M = Modus';
        } else if (combatMode === 'CHEER') {
            controlsText = '1=💪 2=🛡️ 3=💥 4=🎯 | M = Modus';
        }

        hud.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 4px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <span style="font-weight: bold; color: ${modeColors[combatMode]};">${modeIcons[combatMode]} ${combatMode}</span>
                        <span style="color: ${hpColor};">❤️ ${playerStats.hp}/${playerStats.maxHp}</span>
                        <span style="color: #ff8888;">⚔️ ${enemyCount}</span>
                        ${comboCount > 1 ? `<span style="color: #ffaa00; font-weight: bold;">🔥 ${comboCount}x</span>` : ''}
                        ${finisherReady ? '<span style="color: #ff00ff; animation: pulse 0.5s infinite alternate; font-weight: bold;">💀 X = FINISHER!</span>' : ''}
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span style="color: #aaa; font-size: 11px;">${controlsText}</span>
                        <button id="exit-real-combat" style="background: #ff4444; color: white; border: none; padding: 3px 8px; cursor: pointer; border-radius: 3px; font-size: 11px;">✕</button>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <div style="flex: 1; background: #333; height: 6px; border-radius: 3px; overflow: hidden;" title="Finisher Meter: ${finisherPercent}%">
                        <div style="width: ${finisherPercent}%; height: 100%; background: ${finisherColor}; transition: width 0.3s;${finisherReady ? ' animation: pulse 0.5s infinite alternate;' : ''}"></div>
                    </div>
                    <span style="color: #8844ff; font-size: 10px; min-width: 30px;">${finisherPercent}%</span>
                </div>
                ${combatMode === 'CHEER' ? `
                <div style="display: flex; gap: 8px; justify-content: center; padding-top: 2px;">
                    <button onclick="Real3DCombat.cheer('attack')" style="background: #ff4444; color: white; border: none; padding: 4px 12px; cursor: pointer; border-radius: 4px; font-size: 12px;">1: 💪 LOS!</button>
                    <button onclick="Real3DCombat.cheer('defend')" style="background: #4444ff; color: white; border: none; padding: 4px 12px; cursor: pointer; border-radius: 4px; font-size: 12px;">2: 🛡️ DEFEND!</button>
                    <button onclick="Real3DCombat.cheer('combo')" style="background: #ff8800; color: white; border: none; padding: 4px 12px; cursor: pointer; border-radius: 4px; font-size: 12px;">3: 💥 COMBO!</button>
                    <button onclick="Real3DCombat.cheer('focus')" style="background: #44ff44; color: black; border: none; padding: 4px 12px; cursor: pointer; border-radius: 4px; font-size: 12px;">4: 🎯 FOCUS!</button>
                </div>
                ` : ''}
            </div>
        `;

        const exitBtn = document.getElementById('exit-real-combat');
        if (exitBtn) {
            exitBtn._confirmPending = false;
            exitBtn.addEventListener('click', () => {
                if (!exitBtn._confirmPending) {
                    exitBtn._confirmPending = true;
                    exitBtn.textContent = '⚠️ Sicher?';
                    exitBtn.style.background = '#c0392b';
                    setTimeout(() => {
                        exitBtn._confirmPending = false;
                        exitBtn.textContent = '🚪 Exit';
                        exitBtn.style.background = '';
                    }, 3000);
                } else {
                    endCombat();
                }
            });
        }
    }

    function removeCombatHUD() {
        const hud = document.getElementById('real-combat-hud');
        if (hud) hud.remove();
    }

    function endCombat() {
        combatActive = false;
        combatMode = 'MANUAL'; // Modus zurücksetzen
        stopCombatLoop();
        stopAutoMode();
        hideFinisherQTE();

        currentEnemies.forEach(e => e.dispose());
        currentEnemies = [];
        damageNumbers = [];
        collectedLoot = [];
        totalXPEarned = 0;
        finisherMeter = 0;

        removeCombatHUD();
        console.log('🚪 Combat beendet');
    }

    // ==========================================
    // KEYBOARD CONTROLS
    // ==========================================

    function setupControls() {
        document.addEventListener('keydown', (e) => {
            // Skip if typing
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            if (!combatActive) return;

            // Handle finisher QTE input
            if (finisherQTEActive) {
                handleFinisherQTEInput(e.key.toUpperCase());
                e.preventDefault();
                return;
            }

            const key = e.key.toLowerCase();

            switch(key) {
                case 'q':
                    if (combatMode === 'MANUAL') {
                        const now = Date.now();
                        dualAttackState.qPressed = true;
                        dualAttackState.qTime = now;

                        // Check: wurde E kürzlich gedrückt? → DUAL!
                        if (dualAttackState.ePressed && (now - dualAttackState.eTime) < dualAttackState.dualWindow) {
                            // DUAL ATTACK! Cancel pending single
                            if (dualAttackState.dualPending) {
                                clearTimeout(dualAttackState.dualPending);
                                dualAttackState.dualPending = null;
                            }
                            dualAttackNearestEnemy(e.shiftKey);
                            dualAttackState.qPressed = false;
                            dualAttackState.ePressed = false;
                        } else {
                            // Warte kurz ob E noch kommt
                            dualAttackState.dualPending = setTimeout(() => {
                                if (dualAttackState.qPressed) {
                                    attackNearestEnemy(15, 4, 'left', e.shiftKey);
                                    dualAttackState.qPressed = false;
                                }
                                dualAttackState.dualPending = null;
                            }, dualAttackState.dualWindow);
                        }
                    }
                    break;
                case 'e':
                    if (combatMode === 'MANUAL') {
                        if (window.nearBuilding) return;
                        const now2 = Date.now();
                        dualAttackState.ePressed = true;
                        dualAttackState.eTime = now2;

                        // Check: wurde Q kürzlich gedrückt? → DUAL!
                        if (dualAttackState.qPressed && (now2 - dualAttackState.qTime) < dualAttackState.dualWindow) {
                            // DUAL ATTACK! Cancel pending single
                            if (dualAttackState.dualPending) {
                                clearTimeout(dualAttackState.dualPending);
                                dualAttackState.dualPending = null;
                            }
                            dualAttackNearestEnemy(e.shiftKey);
                            dualAttackState.qPressed = false;
                            dualAttackState.ePressed = false;
                        } else {
                            // Warte kurz ob Q noch kommt
                            dualAttackState.dualPending = setTimeout(() => {
                                if (dualAttackState.ePressed) {
                                    attackNearestEnemy(12, 4, 'right', e.shiftKey);
                                    dualAttackState.ePressed = false;
                                }
                                dualAttackState.dualPending = null;
                            }, dualAttackState.dualWindow);
                        }
                    }
                    break;
                case ' ':
                    e.preventDefault();
                    if (combatMode === 'MANUAL') {
                        // Dodge
                        if (window.EquipmentCombat) {
                            EquipmentCombat.dodge('back');
                        }
                        // Player Dodge Animation
                        if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
                            window.CharacterAnimations.playDodge();
                        }
                        gainFinisher('perfectDodge');
                        console.log('🌀 Dodge!');
                    }
                    break;
                case 'm':
                    // Toggle mode
                    const modes = ['MANUAL', 'AUTO', 'CHEER'];
                    const idx = modes.indexOf(combatMode);
                    combatMode = modes[(idx + 1) % modes.length];
                    console.log(`Combat Mode: ${combatMode}`);

                    // Start/stop auto mode
                    if (combatMode === 'AUTO' || combatMode === 'CHEER') {
                        startAutoMode();
                    } else {
                        stopAutoMode();
                    }

                    updateCombatHUD();
                    break;
                case 'x':
                    // Finisher trigger
                    triggerFinisher();
                    break;

                // CHEER Mode buttons (1-4)
                case '1':
                    if (combatMode === 'CHEER') {
                        cheer('attack');
                        e.preventDefault();
                    }
                    break;
                case '2':
                    if (combatMode === 'CHEER') {
                        cheer('defend');
                        e.preventDefault();
                    }
                    break;
                case '3':
                    if (combatMode === 'CHEER') {
                        cheer('combo');
                        e.preventDefault();
                    }
                    break;
                case '4':
                    if (combatMode === 'CHEER') {
                        cheer('focus');
                        e.preventDefault();
                    }
                    break;
            }
        });

        // Keyup - Dual-Attack State resetten
        document.addEventListener('keyup', (e) => {
            const key = e.key.toLowerCase();
            if (key === 'q') dualAttackState.qPressed = false;
            if (key === 'e') dualAttackState.ePressed = false;
        });
    }

    // ==========================================
    // BIOME ENEMY SPAWNER (Fixes null biome!)
    // ==========================================

    function getEnemiesForBiome(biome) {
        const normalizedBiome = (biome || 'default').toLowerCase();
        const enemies = BIOME_ENEMIES[normalizedBiome] || BIOME_ENEMIES.default;
        return enemies;
    }

    function spawnBiomeEnemies(biome, position, scene, count = 3) {
        const enemyTypes = getEnemiesForBiome(biome);
        if (enemyTypes.length === 0) {
            console.log(`⚔️ Safe Zone: ${biome} - keine Gegner`);
            return;
        }

        const toSpawn = [];
        for (let i = 0; i < count; i++) {
            const type = enemyTypes[Math.floor(Math.random() * enemyTypes.length)];
            toSpawn.push(type);
        }

        startCombat(toSpawn, scene, position);
    }

    // ==========================================
    // INIT
    // ==========================================

    setupControls();

    // ==========================================
    // AUTO MODE AI
    // ==========================================

    function startAutoMode() {
        autoAttackTimer = 0.5;
    }

    function stopAutoMode() {
        if (autoModeInterval) {
            clearInterval(autoModeInterval);
            autoModeInterval = null;
        }
    }

    function performAutoAction() {
        if (!combatActive) return;

        const playerPos = getPlayerPosition();
        if (!playerPos) return;

        // Find nearest living enemy
        let nearest = null;
        let nearestDist = Infinity;
        currentEnemies.forEach(enemy => {
            if (enemy.isDead) return;
            const dist = enemy.position.distanceTo(playerPos);
            if (dist < nearestDist) {
                nearest = enemy;
                nearestDist = dist;
            }
        });

        if (!nearest) return;

        // AI Decision
        const hpPercent = playerStats.hp / playerStats.maxHp;

        // Dodge if enemy is attacking and close
        if (nearest.state === 'attack' && nearestDist < 3 && Math.random() < 0.4) {
            if (window.EquipmentCombat) EquipmentCombat.dodge('back');
            if (window.CharacterAnimations && window.CharacterAnimations.isReady()) {
                window.CharacterAnimations.playDodge();
            }
            gainFinisher('perfectDodge');
            return;
        }

        // If in range, attack
        if (nearestDist < 5) {
            // Heavy attack occasionally (20% chance)
            if (Math.random() < 0.2) {
                attackNearestEnemy(25, 5, 'right', true);
            } else {
                // Alternate hands
                const hand = Math.random() < 0.5 ? 'left' : 'right';
                attackNearestEnemy(15, 5, hand, false);
            }
        }

        // Try finisher if available
        if (canUseFinisherAny()) {
            triggerFinisher();
        }
    }

    // ==========================================
    // CHEER SYSTEM (Digimon World Style!)
    // ==========================================

    function cheer(type) {
        if (combatMode !== 'CHEER') return false;

        const effects = {
            attack: { buff: 'attack', rounds: 3, msg: '💪 "GIB IHM!" - Angriff +10%!', color: '#ff4444' },
            defend: { buff: 'defend', rounds: 3, msg: '🛡️ "HALTE DURCH!" - Verteidigung +20%!', color: '#4444ff' },
            combo: { buff: 'combo', rounds: 1, msg: '💥 "COMBO!" - Nächster x1.3 Schaden!', color: '#ff8800' },
            focus: { buff: 'focus', rounds: 2, msg: '🎯 "FOCUS!" - +15% Crit Chance!', color: '#44ff44' }
        };

        const effect = effects[type];
        if (!effect) return false;

        // Don't stack if already active
        if (cheerBuffs[effect.buff] > 0) {
            showCheerNotification('⏳ Buff noch aktiv!', '#888');
            return false;
        }

        cheerBuffs[effect.buff] = effect.rounds;
        showCheerNotification(effect.msg, effect.color);

        console.log(`📣 Cheer: ${effect.msg}`);
        return true;
    }

    function showCheerNotification(msg, color) {
        const notif = document.createElement('div');
        notif.style.cssText = `
            position: fixed; top: 30%; left: 50%; transform: translateX(-50%);
            background: ${color}; color: white; padding: 12px 24px;
            border-radius: 8px; font-size: 18px; font-weight: bold;
            font-family: monospace; z-index: 9999;
            animation: cheerBounce 0.5s ease-out;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            pointer-events: none;
        `;
        notif.textContent = msg;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 1500);
    }

    // ==========================================
    // FINISHER SYSTEM (QTE)
    // ==========================================

    function gainFinisher(action) {
        const gains = {
            perfectDodge: 30,
            combo5: 25,
            parryRiposte: 20,
            chargedAttack: 15,
            normalAttack: 5
        };
        finisherMeter = Math.min(FINISHER_MAX, finisherMeter + (gains[action] || 5));
    }

    function canUseFinisher(enemy) {
        if (finisherMeter < FINISHER_MAX) return false;
        if (!enemy || enemy.isDead) return false;
        if (enemy.hp > enemy.maxHp * 0.2) return false;
        const timeSince = Date.now() - lastFinisherTime;
        if (timeSince < FINISHER_COOLDOWN) return false;
        return true;
    }

    function canUseFinisherAny() {
        if (finisherMeter < FINISHER_MAX) return false;
        const timeSince = Date.now() - lastFinisherTime;
        if (timeSince < FINISHER_COOLDOWN) return false;
        return currentEnemies.some(e => !e.isDead && e.hp <= e.maxHp * 0.2);
    }

    function showFinisherPrompt() {
        // Already showing
        if (document.getElementById('finisher-prompt')) return;

        const prompt = document.createElement('div');
        prompt.id = 'finisher-prompt';
        prompt.style.cssText = `
            position: fixed; top: 40%; left: 50%; transform: translateX(-50%);
            background: rgba(100,0,100,0.9); color: #ff00ff; padding: 10px 20px;
            border-radius: 8px; font-size: 16px; font-weight: bold;
            font-family: monospace; z-index: 9999;
            border: 2px solid #ff00ff;
            animation: pulse 0.5s infinite alternate;
        `;
        prompt.textContent = '💀 Drücke X für FINISHER!';
        document.body.appendChild(prompt);

        // Auto-remove after 5 seconds
        setTimeout(() => prompt.remove(), 5000);
    }

    function triggerFinisher() {
        if (!canUseFinisherAny()) return;

        // Find target
        finisherTarget = currentEnemies.find(e => !e.isDead && e.hp <= e.maxHp * 0.2);
        if (!finisherTarget) return;

        // Remove prompt
        document.getElementById('finisher-prompt')?.remove();

        // Start QTE
        startFinisherQTE();
    }

    function startFinisherQTE() {
        finisherQTEActive = true;
        finisherQTEIndex = 0;

        // Generate random key sequence (4 keys)
        const possibleKeys = ['Q', 'W', 'E', 'A', 'S', 'D'];
        finisherQTESequence = [];
        for (let i = 0; i < 4; i++) {
            finisherQTESequence.push(possibleKeys[Math.floor(Math.random() * possibleKeys.length)]);
        }

        showFinisherQTE();

        // Timer - 4 seconds to complete
        finisherQTETimer = setTimeout(() => {
            finisherQTEFail();
        }, 4000);
    }

    function showFinisherQTE() {
        let overlay = document.getElementById('finisher-qte-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'finisher-qte-overlay';
            overlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.6);
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                z-index: 10000; font-family: monospace;
            `;
            document.body.appendChild(overlay);
        }

        const keysHtml = finisherQTESequence.map((key, i) => {
            let color = '#555';
            let border = '#888';
            if (i < finisherQTEIndex) { color = '#00ff00'; border = '#00ff00'; }
            else if (i === finisherQTEIndex) { color = '#ffaa00'; border = '#ffaa00'; }
            return `<div style="width: 60px; height: 60px; background: ${color}; border: 3px solid ${border};
                border-radius: 10px; display: flex; align-items: center; justify-content: center;
                font-size: 28px; font-weight: bold; color: white;
                ${i === finisherQTEIndex ? 'animation: pulse 0.3s infinite alternate; transform: scale(1.2);' : ''}">${key}</div>`;
        }).join('');

        overlay.innerHTML = `
            <div style="color: #ff00ff; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-shadow: 0 0 10px #ff00ff;">
                💀 FINISHER! 💀
            </div>
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                ${keysHtml}
            </div>
            <div style="color: #ffaa00; font-size: 14px;">Drücke die Tasten in Reihenfolge!</div>
            <div style="width: 200px; height: 6px; background: #333; border-radius: 3px; margin-top: 10px; overflow: hidden;">
                <div id="finisher-qte-timer" style="width: 100%; height: 100%; background: #ff00ff; transition: width 4s linear;"></div>
            </div>
        `;

        // Start timer animation
        requestAnimationFrame(() => {
            const timerBar = document.getElementById('finisher-qte-timer');
            if (timerBar) timerBar.style.width = '0%';
        });
    }

    function handleFinisherQTEInput(key) {
        if (!finisherQTEActive) return;

        if (key === finisherQTESequence[finisherQTEIndex]) {
            finisherQTEIndex++;

            // Play success sound
            if (window.CombatSpecialUI?.playSound) {
                CombatSpecialUI.playSound('whoosh');
            }

            if (finisherQTEIndex >= finisherQTESequence.length) {
                // QTE Complete!
                finisherQTESuccess();
            } else {
                // Update display
                showFinisherQTE();
            }
        } else {
            // Wrong key!
            finisherQTEFail();
        }
    }

    function finisherQTESuccess() {
        clearTimeout(finisherQTETimer);
        finisherQTEActive = false;
        finisherMeter = 0;
        lastFinisherTime = Date.now();

        hideFinisherQTE();

        // MASSIVE DAMAGE to target
        if (finisherTarget && !finisherTarget.isDead) {
            const finisherDamage = finisherTarget.maxHp * 5; // Overkill!
            finisherTarget.takeDamage(finisherDamage, true);

            // Screen effect
            const flash = document.createElement('div');
            flash.style.cssText = `
                position: fixed; inset: 0;
                background: radial-gradient(circle, rgba(255,0,255,0.8), rgba(100,0,100,0.3));
                pointer-events: none; z-index: 9999;
                animation: fadeOut 1s forwards;
            `;
            document.body.appendChild(flash);
            setTimeout(() => flash.remove(), 1000);

            // Victory text
            const text = document.createElement('div');
            text.style.cssText = `
                position: fixed; top: 35%; left: 50%; transform: translateX(-50%);
                color: #ff00ff; font-size: 48px; font-weight: bold;
                font-family: monospace; z-index: 10001;
                text-shadow: 0 0 20px #ff00ff, 0 0 40px #ff00ff;
                animation: finisherText 2s ease-out forwards;
                pointer-events: none;
            `;
            text.textContent = '💀 FINISHER! 💀';
            document.body.appendChild(text);
            setTimeout(() => text.remove(), 2000);

            console.log(`💀 FINISHER! ${finisherDamage} Schaden an ${finisherTarget.data.name}!`);
        }

        finisherTarget = null;
    }

    function finisherQTEFail() {
        clearTimeout(finisherQTETimer);
        finisherQTEActive = false;
        finisherMeter = Math.floor(FINISHER_MAX * 0.5); // Lose half meter
        finisherTarget = null;

        hideFinisherQTE();

        showCheerNotification('❌ Finisher verfehlt!', '#ff4444');
        console.log('❌ Finisher QTE failed!');
    }

    function hideFinisherQTE() {
        document.getElementById('finisher-qte-overlay')?.remove();
        document.getElementById('finisher-prompt')?.remove();
    }

    // ==========================================
    // FLOATING DAMAGE NUMBERS
    // ==========================================

    function spawnDamageNumber(amount, position, isCrit) {
        const dmgNum = {
            value: Math.floor(amount),
            x: position.x + (Math.random() - 0.5) * 1.5,
            y: position.y + 3.5,
            z: position.z + (Math.random() - 0.5) * 1.5,
            vy: 2.0, // upward velocity
            life: 1.2, // seconds to live
            maxLife: 1.2,
            isCrit: isCrit,
            sprite: null
        };

        // Create 2D overlay element (more reliable than 3D text)
        const el = document.createElement('div');
        el.className = 'damage-number';
        el.style.cssText = `
            position: fixed;
            font-family: monospace;
            font-weight: bold;
            pointer-events: none;
            z-index: 950;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            transition: none;
            ${isCrit ?
                'font-size: 28px; color: #ff00ff;' :
                'font-size: 20px; color: #ffdd00;'
            }
        `;
        el.textContent = isCrit ? `💥${amount}` : `-${amount}`;
        document.body.appendChild(el);

        dmgNum.element = el;
        damageNumbers.push(dmgNum);
    }

    function updateDamageNumbers(delta) {
        const camera = window.Scene3D?.camera;
        if (!camera) return;

        damageNumbers = damageNumbers.filter(dn => {
            dn.life -= delta;
            dn.y += dn.vy * delta;
            dn.vy *= 0.95; // slow down

            if (dn.life <= 0) {
                dn.element?.remove();
                return false;
            }

            // Project 3D position to screen
            const pos = new THREE.Vector3(dn.x, dn.y, dn.z);
            pos.project(camera);

            const hw = window.innerWidth / 2;
            const hh = window.innerHeight / 2;
            const screenX = pos.x * hw + hw;
            const screenY = -pos.y * hh + hh;

            // Only show if in front of camera
            if (pos.z > 0 && pos.z < 1) {
                const opacity = Math.min(1, dn.life / (dn.maxLife * 0.3));
                const scale = dn.isCrit ? 1.0 + (1 - dn.life / dn.maxLife) * 0.3 : 1.0;
                dn.element.style.left = `${screenX}px`;
                dn.element.style.top = `${screenY}px`;
                dn.element.style.opacity = opacity;
                dn.element.style.transform = `translate(-50%, -50%) scale(${scale})`;
                dn.element.style.display = 'block';
            } else {
                dn.element.style.display = 'none';
            }

            return true;
        });
    }

    // ==========================================
    // LOOT SYSTEM
    // ==========================================

    function spawnLootDrop(position, items) {
        // Visual loot notification
        items.forEach((item, i) => {
            setTimeout(() => {
                const el = document.createElement('div');
                el.style.cssText = `
                    position: fixed; bottom: ${120 + i * 35}px; right: 20px;
                    background: rgba(80, 50, 0, 0.9); color: #ffcc00;
                    padding: 6px 14px; border-radius: 6px;
                    font-family: monospace; font-size: 14px;
                    border: 1px solid #ffcc00;
                    z-index: 960;
                    animation: lootSlide 0.3s ease-out;
                    pointer-events: none;
                `;
                el.textContent = `💎 +${formatLootName(item)}`;
                document.body.appendChild(el);
                setTimeout(() => el.remove(), 2500);
            }, i * 200);
        });
    }

    function showLootSummary(xp, loot) {
        if (xp === 0 && loot.length === 0) return;

        const overlay = document.createElement('div');
        overlay.id = 'loot-summary';
        overlay.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7);
            display: flex; align-items: center; justify-content: center;
            z-index: 10000; font-family: monospace;
            cursor: pointer;
        `;

        // Count loot items
        const lootCounts = {};
        loot.forEach(item => {
            lootCounts[item] = (lootCounts[item] || 0) + 1;
        });

        const lootHtml = Object.entries(lootCounts).map(([item, count]) =>
            `<div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #333;">
                <span style="color: #ffcc00;">💎 ${formatLootName(item)}</span>
                <span style="color: #aaa;">x${count}</span>
            </div>`
        ).join('');

        overlay.innerHTML = `
            <div style="background: rgba(30, 20, 10, 0.95); border: 2px solid #ffcc00; border-radius: 12px;
                        padding: 24px; min-width: 300px; max-width: 400px;">
                <div style="text-align: center; color: #00ff00; font-size: 24px; font-weight: bold; margin-bottom: 16px;">
                    🎉 SIEG!
                </div>
                <div style="text-align: center; color: #88ff88; font-size: 18px; margin-bottom: 16px;">
                    +${xp} XP
                </div>
                ${loot.length > 0 ? `
                    <div style="color: #ffcc00; font-size: 14px; margin-bottom: 8px; font-weight: bold;">LOOT:</div>
                    <div style="max-height: 200px; overflow-y: auto;">
                        ${lootHtml}
                    </div>
                ` : '<div style="color: #888; text-align: center;">Kein Loot</div>'}
                <div style="text-align: center; color: #666; font-size: 12px; margin-top: 16px;">
                    Klicke zum Schließen
                </div>
            </div>
        `;

        overlay.addEventListener('click', () => overlay.remove());
        document.body.appendChild(overlay);

        // Auto-close after 8 seconds
        setTimeout(() => overlay.remove(), 8000);
    }

    function showDefeatScreen() {
        const overlay = document.createElement('div');
        overlay.id = 'defeat-screen';
        overlay.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(80, 0, 0, 0.85);
            display: flex; align-items: center; justify-content: center;
            z-index: 10000; font-family: monospace;
            animation: fadeIn 0.5s;
        `;

        overlay.innerHTML = `
            <div style="background: rgba(40, 0, 0, 0.95); border: 2px solid #ff4444; border-radius: 12px;
                        padding: 30px; min-width: 320px; max-width: 420px; text-align: center;">
                <div style="color: #ff4444; font-size: 28px; font-weight: bold; margin-bottom: 12px;">
                    💀 BESIEGT! 💀
                </div>
                <div style="color: #cc8888; font-size: 14px; margin-bottom: 20px;">
                    Du wurdest im Kampf niedergestreckt...
                </div>
                <div style="color: #ffaa00; font-size: 13px; margin-bottom: 16px;">
                    Wiederbelebung mit halber Gesundheit
                </div>
                <div style="color: #666; font-size: 11px;">Klicke zum Fortfahren</div>
            </div>
        `;

        overlay.addEventListener('click', () => overlay.remove());
        document.body.appendChild(overlay);

        // Auto-close after 5 seconds
        setTimeout(() => { if (overlay.parentNode) overlay.remove(); }, 5000);
    }

    function formatLootName(itemId) {
        return itemId
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    function addLootToInventory(loot) {
        // Try to add to game inventory system
        if (window.InventorySystem?.addItem) {
            loot.forEach(item => InventorySystem.addItem(item, 1));
        } else {
            // Fallback: Save to localStorage
            const inventory = JSON.parse(localStorage.getItem('najika_inventory') || '{}');
            loot.forEach(item => {
                inventory[item] = (inventory[item] || 0) + 1;
            });
            localStorage.setItem('najika_inventory', JSON.stringify(inventory));
        }
    }

    // CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        @keyframes pulse {
            from { opacity: 0.7; }
            to { opacity: 1; }
        }
        @keyframes cheerBounce {
            0% { transform: translateX(-50%) scale(0.5); opacity: 0; }
            50% { transform: translateX(-50%) scale(1.2); }
            100% { transform: translateX(-50%) scale(1); opacity: 1; }
        }
        @keyframes lootSlide {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes finisherText {
            0% { transform: translateX(-50%) scale(0.5); opacity: 0; }
            30% { transform: translateX(-50%) scale(1.3); opacity: 1; }
            70% { opacity: 1; }
            100% { transform: translateX(-50%) scale(1) translateY(-50px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    // ==========================================
    // PUBLIC API
    // ==========================================

    window.Real3DCombat = {
        startCombat,
        endCombat,
        attackNearestEnemy,
        dualAttackNearestEnemy,
        takeDamage,
        heal,

        // Biome system
        getEnemiesForBiome,
        spawnBiomeEnemies,

        // State
        isActive: () => combatActive,
        getMode: () => combatMode,
        setMode: (mode) => {
            combatMode = mode;
            if (mode === 'AUTO' || mode === 'CHEER') startAutoMode();
            else stopAutoMode();
            updateCombatHUD();
        },
        getPlayerStats: () => ({ ...playerStats }),
        getEnemies: () => currentEnemies,

        // Combat Modes
        cheer,
        getCheerBuffs: () => ({ ...cheerBuffs }),

        // Finisher
        getFinisherMeter: () => finisherMeter,
        triggerFinisher,

        // Loot
        getCollectedLoot: () => [...collectedLoot],
        getInventory: () => JSON.parse(localStorage.getItem('najika_inventory') || '{}'),

        // Enemy types for reference
        ENEMY_TYPES,
        BIOME_ENEMIES
    };

    console.log('✅ Real 3D Combat System V2 loaded!');
    console.log('   🎮 MANUAL: Q/E = Attack, Q+E = Dual Attack!, Shift+Q+E = Dual Heavy!, Space = Dodge');
    console.log('   🤖 AUTO: KI kämpft automatisch');
    console.log('   📣 CHEER: 1-4 Anfeuern (Digimon Style!)');
    console.log('   💀 X = Finisher (wenn Meter voll + Gegner < 20% HP)');
    console.log('   💎 Loot-System + Damage Numbers aktiv!');

})();
