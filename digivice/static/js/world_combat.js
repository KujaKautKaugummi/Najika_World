/**
 * WORLD COMBAT SYSTEM (Phase 3)
 * Combat-System für die offene Welt (najika_world_9regions_test.html)
 * Angepasst von dungeon_combat.js für Region-basierte Gegner
 */

class WorldCombat {
    constructor(scene, THREE) {
        this.scene = scene;
        this.THREE = THREE;

        // Combat State
        this.combatActive = false;
        this.currentEnemy = null;

        // Player Stats
        this.playerHealth = 100;
        this.playerMaxHealth = 100;
        this.playerDamage = 15;
        this.playerXP = 0;
        this.playerLevel = 1;

        // Enemies
        this.enemies = [];
        this.enemyMeshes = [];

        // Enemy Types Database (Region-spezifisch)
        this.enemyTypes = {
            // ICE Region
            ice_undead: {
                name: 'Eis-Untoter',
                hp: 40,
                damage: 8,
                xp: 15,
                loot: ['ice_shard', 'frozen_bone'],
                color: 0xaaffff,
                size: { width: 2, height: 4, depth: 2 }
            },
            ice_elemental: {
                name: 'Eis-Elemental',
                hp: 50,
                damage: 10,
                xp: 20,
                loot: ['ice_crystal', 'frozen_heart'],
                color: 0x00ffff,
                size: { width: 2.5, height: 5, depth: 2.5 }
            },

            // HIGHLAND Region
            highland_guardian: {
                name: 'Hochland-Wächter',
                hp: 60,
                damage: 12,
                xp: 25,
                loot: ['stone_blade', 'rune_fragment'],
                color: 0x8b7355,
                size: { width: 2, height: 4, depth: 2 }
            },

            // DESERT Region
            desert_bandit: {
                name: 'Wüsten-Bandit',
                hp: 45,
                damage: 10,
                xp: 18,
                loot: ['gold_coin', 'scimitar'],
                color: 0xe8d4a0,
                size: { width: 2, height: 4, depth: 2 }
            },
            desert_sandworm: {
                name: 'Sandwurm',
                hp: 80,
                damage: 15,
                xp: 35,
                loot: ['sand_pearl', 'wurm_tooth'],
                color: 0xc2b280,
                size: { width: 3, height: 2, depth: 6 }
            },

            // SWAMP Region
            swamp_witch: {
                name: 'Sumpf-Hexe',
                hp: 55,
                damage: 14,
                xp: 28,
                loot: ['poison_vial', 'witch_hat'],
                color: 0x556b2f,
                size: { width: 2, height: 4, depth: 2 }
            },
            swamp_monster: {
                name: 'Giftmonster',
                hp: 70,
                damage: 12,
                xp: 30,
                loot: ['toxic_slime', 'swamp_essence'],
                color: 0x228b22,
                size: { width: 2.5, height: 3, depth: 2.5 }
            },

            // MOUNTAIN Region
            mountain_giant: {
                name: 'Bergriese',
                hp: 100,
                damage: 20,
                xp: 50,
                loot: ['giant_club', 'mountain_stone'],
                color: 0x808080,
                size: { width: 3, height: 6, depth: 3 }
            },

            // COAST Region
            coast_pirate: {
                name: 'Pirat',
                hp: 50,
                damage: 11,
                xp: 22,
                loot: ['cutlass', 'rum_bottle'],
                color: 0xc2b280,
                size: { width: 2, height: 4, depth: 2 }
            },
            coast_seamonster: {
                name: 'Seemonster',
                hp: 90,
                damage: 18,
                xp: 45,
                loot: ['sea_pearl', 'kraken_tentacle'],
                color: 0x3498db,
                size: { width: 4, height: 3, depth: 4 }
            },

            // CAVES Region
            caves_goblin: {
                name: 'Höhlen-Goblin',
                hp: 35,
                damage: 7,
                xp: 12,
                loot: ['goblin_dagger', 'mushroom'],
                color: 0x2f2f2f,
                size: { width: 1.5, height: 3, depth: 1.5 }
            },

            // FOREST Region
            forest_druid: {
                name: 'Feindlicher Druide',
                hp: 65,
                damage: 13,
                xp: 32,
                loot: ['druid_staff', 'nature_essence'],
                color: 0x2d5016,
                size: { width: 2, height: 4, depth: 2 }
            },
            forest_spirit: {
                name: 'Waldgeist',
                hp: 45,
                damage: 9,
                xp: 20,
                loot: ['spirit_orb', 'ancient_wood'],
                color: 0x90ee90,
                size: { width: 2, height: 5, depth: 2 }
            },

            // VOLCANO Region
            volcano_elemental: {
                name: 'Feuer-Elemental',
                hp: 85,
                damage: 22,
                xp: 40,
                loot: ['lava_core', 'fire_crystal'],
                color: 0xff4500,
                size: { width: 2.5, height: 5, depth: 2.5 }
            },
            volcano_lavamonster: {
                name: 'Lava-Kreatur',
                hp: 95,
                damage: 25,
                xp: 48,
                loot: ['obsidian_shard', 'molten_heart'],
                color: 0xff6347,
                size: { width: 3, height: 4, depth: 3 }
            }
        };

        // Region-Enemy Mapping
        this.regionEnemies = {
            ice: ['ice_undead', 'ice_elemental'],
            highland: ['highland_guardian'],
            desert: ['desert_bandit', 'desert_sandworm'],
            swamp: ['swamp_witch', 'swamp_monster'],
            mountain: ['mountain_giant'],
            coast: ['coast_pirate', 'coast_seamonster'],
            caves: ['caves_goblin'],
            forest: ['forest_druid', 'forest_spirit'],
            volcano: ['volcano_elemental', 'volcano_lavamonster']
        };
    }

    /**
     * Spawnt Gegner in allen 9 Regionen
     */
    spawnEnemiesInAllRegions(regions) {
        console.log('👾 Spawning enemies in all regions...');

        regions.forEach(region => {
            this.spawnEnemiesInRegion(region);
        });

        console.log(`✅ Spawned ${this.enemies.length} enemies total!`);
    }

    /**
     * Spawnt Gegner in einer Region
     */
    spawnEnemiesInRegion(region) {
        const enemyTypesForRegion = this.regionEnemies[region.name];
        if (!enemyTypesForRegion) {
            console.warn(`⚠️  No enemies defined for region: ${region.name}`);
            return;
        }

        // Spawn 3-5 zufällige Gegner pro Region
        const enemyCount = Math.floor(Math.random() * 3) + 3; // 3-5

        for (let i = 0; i < enemyCount; i++) {
            // Zufälliger Enemy-Typ für diese Region
            const randomType = enemyTypesForRegion[Math.floor(Math.random() * enemyTypesForRegion.length)];
            const enemyData = this.enemyTypes[randomType];

            // Zufällige Position in Region (nicht zu nah am Zentrum)
            const offsetX = (Math.random() - 0.5) * 100; // ±50 units
            const offsetZ = (Math.random() - 0.5) * 100;
            const x = region.x + offsetX;
            const z = region.z + offsetZ;

            this.spawnEnemy(randomType, x, region.y, z);
        }
    }

    /**
     * Spawnt einen einzelnen Gegner
     */
    spawnEnemy(type, x, y, z) {
        const enemyData = this.enemyTypes[type];
        if (!enemyData) {
            console.error(`❌ Unknown enemy type: ${type}`);
            return;
        }

        // Erstelle Enemy Mesh (Box)
        const geometry = new this.THREE.BoxGeometry(
            enemyData.size.width,
            enemyData.size.height,
            enemyData.size.depth
        );
        const material = new this.THREE.MeshStandardMaterial({
            color: enemyData.color,
            emissive: enemyData.color,
            emissiveIntensity: 0.3
        });
        const mesh = new this.THREE.Mesh(geometry, material);
        mesh.position.set(x, y + enemyData.size.height / 2, z);
        mesh.castShadow = true;
        mesh.receiveShadow = true;

        // Enemy Data
        const enemy = {
            type: type,
            data: enemyData,
            mesh: mesh,
            health: enemyData.hp,
            maxHealth: enemyData.hp,
            alive: true
        };

        this.enemies.push(enemy);
        this.enemyMeshes.push(mesh);
        this.scene.add(mesh);
    }

    /**
     * Update Enemies (Animationen, KI, etc.)
     */
    updateEnemies(playerPosition) {
        this.enemies.forEach(enemy => {
            if (!enemy.alive) return;

            // Simple KI: Drehe dich zum Spieler wenn nah
            const distance = playerPosition.distanceTo(enemy.mesh.position);
            if (distance < 20) {
                const direction = new this.THREE.Vector3();
                direction.subVectors(playerPosition, enemy.mesh.position);
                const angle = Math.atan2(direction.x, direction.z);
                enemy.mesh.rotation.y = angle;

                // Leuchte rot wenn sehr nah (Aggro)
                if (distance < 5) {
                    enemy.mesh.material.emissive.setHex(0xff0000);
                    enemy.mesh.material.emissiveIntensity = 0.6;
                } else {
                    enemy.mesh.material.emissive.setHex(enemy.data.color);
                    enemy.mesh.material.emissiveIntensity = 0.3;
                }
            }
        });
    }

    /**
     * Check Combat Proximity (startet Combat wenn zu nah)
     */
    checkCombatProximity(playerPosition) {
        if (this.combatActive) return null;

        // Finde nächsten lebenden Gegner
        let closestEnemy = null;
        let closestDistance = Infinity;

        this.enemies.forEach(enemy => {
            if (!enemy.alive) return;

            const distance = playerPosition.distanceTo(enemy.mesh.position);
            if (distance < 3 && distance < closestDistance) {
                closestEnemy = enemy;
                closestDistance = distance;
            }
        });

        return closestEnemy;
    }

    /**
     * Startet Combat mit Gegner
     */
    startCombat(enemy) {
        this.combatActive = true;
        this.currentEnemy = enemy;

        console.log(`⚔️ Combat started with ${enemy.data.name}!`);

        // Visual: Gegner rot leuchten lassen
        enemy.mesh.material.emissive.setHex(0xff0000);
        enemy.mesh.material.emissiveIntensity = 1.0;

        return enemy;
    }

    /**
     * Player Angriff
     */
    playerAttack() {
        if (!this.combatActive || !this.currentEnemy) return null;

        const enemy = this.currentEnemy;
        enemy.health -= this.playerDamage;

        console.log(`⚔️ Hit ${enemy.data.name} for ${this.playerDamage} damage! (${enemy.health}/${enemy.maxHealth} HP)`);

        if (enemy.health <= 0) {
            return this.killEnemy(enemy);
        }

        // Enemy schlägt zurück
        this.enemyAttack(enemy);

        return { type: 'hit', enemy, damage: this.playerDamage };
    }

    /**
     * Enemy Angriff
     */
    enemyAttack(enemy) {
        const damage = enemy.data.damage;
        this.playerHealth -= damage;

        console.log(`💥 ${enemy.data.name} hit you for ${damage} damage! (${this.playerHealth}/${this.playerMaxHealth} HP)`);

        if (this.playerHealth <= 0) {
            this.gameOver();
        }

        return damage;
    }

    /**
     * Töte Gegner
     */
    killEnemy(enemy) {
        enemy.alive = false;

        console.log(`💀 ${enemy.data.name} defeated! +${enemy.data.xp} XP, Loot: ${enemy.data.loot.join(', ')}`);

        // XP geben
        this.playerXP += enemy.data.xp;

        // Check Level Up
        const xpForNextLevel = this.playerLevel * 100;
        if (this.playerXP >= xpForNextLevel) {
            this.levelUp();
        }

        // Entferne Mesh
        this.scene.remove(enemy.mesh);

        // Combat beenden
        this.combatActive = false;
        this.currentEnemy = null;

        return {
            type: 'kill',
            enemy,
            xp: enemy.data.xp,
            loot: enemy.data.loot
        };
    }

    /**
     * Level Up
     */
    levelUp() {
        this.playerLevel++;
        this.playerMaxHealth += 20;
        this.playerHealth = this.playerMaxHealth; // Full heal
        this.playerDamage += 5;

        console.log(`🎉 LEVEL UP! Now Level ${this.playerLevel}!`);
        console.log(`   HP: ${this.playerMaxHealth} | Damage: ${this.playerDamage}`);
    }

    /**
     * Game Over
     */
    gameOver() {
        this.combatActive = false;
        this.currentEnemy = null;

        console.log('💀 GAME OVER - You died!');

        // Respawn mit vollem HP
        setTimeout(() => {
            this.playerHealth = this.playerMaxHealth;
            console.log('⚕️ Respawned with full HP!');
        }, 2000);
    }

    /**
     * Beende Combat vorzeitig (Flucht)
     */
    exitCombat() {
        if (!this.combatActive) return;

        console.log('🏃 Fled from combat!');

        // Reset enemy emissive
        if (this.currentEnemy) {
            this.currentEnemy.mesh.material.emissive.setHex(this.currentEnemy.data.color);
            this.currentEnemy.mesh.material.emissiveIntensity = 0.3;
        }

        this.combatActive = false;
        this.currentEnemy = null;
    }

    /**
     * Entferne alle Enemies (Cleanup)
     */
    clearAllEnemies() {
        this.enemies.forEach(enemy => {
            this.scene.remove(enemy.mesh);
        });

        this.enemies = [];
        this.enemyMeshes = [];
        this.combatActive = false;
        this.currentEnemy = null;

        console.log('🧹 All enemies cleared');
    }

    /**
     * Get Stats
     */
    getStats() {
        return {
            health: this.playerHealth,
            maxHealth: this.playerMaxHealth,
            damage: this.playerDamage,
            xp: this.playerXP,
            level: this.playerLevel,
            combatActive: this.combatActive,
            enemiesAlive: this.enemies.filter(e => e.alive).length,
            currentEnemy: this.currentEnemy ? this.currentEnemy.data.name : null
        };
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorldCombat;
}
