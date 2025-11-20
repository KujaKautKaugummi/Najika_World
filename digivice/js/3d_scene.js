// Najika Digivice – Three.js scene manager with KayKit rooms, character controls and camera modes
(function () {
    const CAMERA_MODES = {
        ORBIT: 'orbit',
        THIRD: 'third',
        FIRST: 'first'
    };

    const DEFAULT_PALETTE = {
        background: 0x1a1a2e,
        fog: 0x1a1a2e,
        ambient: 0.45,
        dir: 0xffffff,
        dirIntensity: 0.9,
        primary: 0xff6b6b,
        secondary: 0x667eea,
        floor: 0x2a2a3e
    };

    const PRIVATE_PALETTE = {
        background: 0x240008,
        fog: 0x240008,
        ambient: 0.25,
        dir: 0xff5500,
        dirIntensity: 0.6,
        primary: 0xaa1111,
        secondary: 0x330033,
        floor: 0x240008
    };

    const FALLBACK_DEFAULTS = {
        span: 24,
        wallHeight: 6
    };

    const CHARACTER_SPEED = 7.5;
    const CHARACTER_HEIGHT = 3.8;
    const CLAMP_PADDING = 2;

    let scene;
    let camera;
    let renderer;
    let ambientLight;
    let dirLight;
    let pointLight1;
    let pointLight2;
    let baseFloor;
    let gridHelper;
    const fallbackWalls = [];

    let roomGroup = null;
    let currentRoomName = 'Wohnzimmer';
    let currentRoomSpan = FALLBACK_DEFAULTS.span;
    let privateModeActive = false;
    let usingFallbackRoom = true;
    let pendingRoomBuild = false;

    let clock;
    let animationHandle = null;

    let characterGroup = null;
    let characterReady = false;
    let characterHeading = 0;
    const activeKeys = new Set();

    // 🌍 World Manager for 9600×9600 Open World
    let worldManager = null;
    let useWorldManager = true;  // Toggle for testing

    // 🗡️ DUAL-WIELD KAMPFSYSTEM (Skyrim + Dark Souls + Dark Messiah)
    const COMBAT_SYSTEM = {
        leftHand: null,     // Zauber, Schild, Zweithwaffe
        rightHand: null,    // Hauptwaffe (Schwert, Axt, etc.)
        stamina: 100,
        maxStamina: 100,
        health: 100,
        maxHealth: 100,
        mana: 100,
        maxMana: 100,
        manaRegen: 5,  // Mana/sec

        // 🪄 Skills System
        skillSystem: null,  // Wird in init() initialisiert
        skillCooldowns: {},  // skill_id => endTime

        // 🎒 Inventory System
        inventorySystem: null,  // Wird in init() initialisiert

        // 🎯 Target System (Skyrim/Fortnite Style)
        currentTarget: null,
        targetLockOn: false,  // Tab zum Togglen
        targetDistance: 0,

        // 🥊 Attack States
        isAttacking: false,
        attackStartTime: 0,
        attackDuration: 0,
        isStaggered: false,
        staggerEndTime: 0,

        // 🎲 Hit Chance (abhängig von Distanz & Typ)
        hitChance: {
            light: 0.85,      // 85% Light Attack Hit Chance (kein Stagger bei miss!)
            heavy: 0.65,      // 65% Heavy Attack Hit Chance (kein Stagger bei miss!)
            both: 0.50        // 50% Beide gleichzeitig (STAGGER bei miss!)
        },

        // 🎯 Lock-On Toggle (Tab-Taste)
        toggleLockOn() {
            this.targetLockOn = !this.targetLockOn;

            if (this.targetLockOn) {
                console.log('🎯 Lock-On AKTIVIERT - Auto-Targeting an');
                if (typeof notify === 'function') {
                    notify('🎯 Lock-On aktiviert', 'info');
                }
            } else {
                console.log('🎯 Lock-On DEAKTIVIERT - Freies Zielen');
                this.currentTarget = null;
                if (typeof notify === 'function') {
                    notify('🎯 Freies Zielen', 'info');
                }
            }
            return this.targetLockOn;
        },

        // Parry-System (Dark Souls Style)
        parryWindow: { start: 80, end: 200 },  // ms
        lastParryTime: 0,
        isParrying: false,

        // Dodge Roll (i-frames)
        dodgeRoll: {
            active: false,
            iFrames: 12,  // Frames of invincibility
            staminaCost: 20,
            cooldown: 500  // ms
        },
        lastDodgeTime: 0,

        // Combo-System
        combo: {
            hits: 0,
            lastHitTime: 0,
            timeout: 1000,  // ms
            multiplier: 1.0
        },

        // Dual-Wield Combos (erweitert)
        dualWieldCombos: {
            'LL': { damage: 25, stamina: 12, name: 'Doppel-Leicht', speed: 'fast' },
            'LH': { damage: 45, stamina: 18, name: 'Leicht→Schwer Mix', speed: 'medium' },
            'HL': { damage: 45, stamina: 18, name: 'Schwer→Leicht Mix', speed: 'medium' },
            'HH': { damage: 80, stamina: 35, name: 'Doppel-Schwer Crush', speed: 'slow' },
            'LLL': { damage: 40, stamina: 20, name: 'Zauber-Salve', speed: 'fast' },
            'HHH': { damage: 120, stamina: 50, name: 'Vernichtung', speed: 'very_slow' },
            'LHLH': { damage: 90, stamina: 40, name: 'Todestanz', speed: 'medium' }
        },
        comboBuffer: '',
        lastComboTime: 0,

        // 🎒 Equipment Helper Methods (uses InventorySystem)
        getWeaponDamage(hand) {
            if (!this.inventorySystem) return hand === 'left' ? 15 : 20; // Fallback

            const slot = hand === 'left' ? 'weapon_left' : 'weapon_right';
            const weapon = this.inventorySystem.equipment[slot];

            if (weapon && weapon.data && weapon.data.stats) {
                return weapon.data.stats.damage || 10;
            }

            // Fallback unarmed damage
            return hand === 'left' ? 10 : 15;
        },

        getArmorDefense() {
            if (!this.inventorySystem) return 10; // Fallback

            const totalStats = this.inventorySystem.getTotalStats();
            return totalStats.defense || 0;
        },

        // 🗡️ Equipment Management
        equipWeapon(hand, weaponData) {
            if (hand === 'left') {
                this.leftHand = weaponData;
                console.log(`⚔️ Linke Hand: ${weaponData.type} (${weaponData.damage} DMG) ausgerüstet`);
            } else if (hand === 'right') {
                this.rightHand = weaponData;
                console.log(`⚔️ Rechte Hand: ${weaponData.type} (${weaponData.damage} DMG) ausgerüstet`);
            }
        },

        unequipWeapon(hand) {
            if (hand === 'left') {
                this.leftHand = null;
                console.log('🔓 Linke Hand: Waffe abgelegt');
            } else if (hand === 'right') {
                this.rightHand = null;
                console.log('🔓 Rechte Hand: Waffe abgelegt');
            }
        },

        // ⚔️ ATTACK FUNCTIONS (erweitert)

        // Linke Hand - Light Attack
        attackLeftLight() {
            if (this.stamina < 8 || this.isStaggered || this.isAttacking) return false;

            this.stamina -= 8;
            this.isAttacking = true;
            this.attackDuration = 300; // 300ms schnell
            this.attackStartTime = Date.now();

            const damage = this.getWeaponDamage('left') * 0.7; // 70% für Light
            const hit = this.performAttack('left', 'light', damage);

            this.comboBuffer += 'L';
            this.checkCombo();

            setTimeout(() => { this.isAttacking = false; }, this.attackDuration);
            return hit;
        },

        // Linke Hand - Heavy Attack
        attackLeftHeavy() {
            if (this.stamina < 20 || this.isStaggered || this.isAttacking) return false;

            this.stamina -= 20;
            this.isAttacking = true;
            this.attackDuration = 800; // 800ms langsam, nicht abbrechbar!
            this.attackStartTime = Date.now();

            const damage = this.getWeaponDamage('left') * 1.5; // 150% für Heavy
            const hit = this.performAttack('left', 'heavy', damage);

            this.comboBuffer += 'H';
            this.checkCombo();

            setTimeout(() => { this.isAttacking = false; }, this.attackDuration);
            return hit;
        },

        // Rechte Hand - Light Attack
        attackRightLight() {
            if (this.stamina < 10 || this.isStaggered || this.isAttacking) return false;

            this.stamina -= 10;
            this.isAttacking = true;
            this.attackDuration = 350;
            this.attackStartTime = Date.now();

            const damage = this.getWeaponDamage('right') * 0.7;
            const hit = this.performAttack('right', 'light', damage);

            this.comboBuffer += 'L';
            this.checkCombo();

            setTimeout(() => { this.isAttacking = false; }, this.attackDuration);
            return hit;
        },

        // Rechte Hand - Heavy Attack
        attackRightHeavy() {
            if (this.stamina < 25 || this.isStaggered || this.isAttacking) return false;

            this.stamina -= 25;
            this.isAttacking = true;
            this.attackDuration = 900; // Sehr langsam, hoher Schaden
            this.attackStartTime = Date.now();

            const damage = this.getWeaponDamage('right') * 1.5;
            const hit = this.performAttack('right', 'heavy', damage);

            this.comboBuffer += 'H';
            this.checkCombo();

            setTimeout(() => { this.isAttacking = false; }, this.attackDuration);
            return hit;
        },

        // Beide Hände GLEICHZEITIG (riskant!)
        attackBoth(leftType = 'light', rightType = 'heavy') {
            const leftCost = leftType === 'light' ? 8 : 20;
            const rightCost = rightType === 'light' ? 10 : 25;
            const totalCost = leftCost + rightCost;

            if (this.stamina < totalCost || this.isStaggered || this.isAttacking) return false;

            this.stamina -= totalCost;
            this.isAttacking = true;
            this.attackDuration = 600; // Mittlere Dauer
            this.attackStartTime = Date.now();

            const leftDamage = this.getWeaponDamage('left') * (leftType === 'light' ? 0.7 : 1.5);
            const rightDamage = this.getWeaponDamage('right') * (rightType === 'light' ? 0.7 : 1.5);
            const totalDamage = leftDamage + rightDamage;

            // Beide gleichzeitig = niedrigere Hit Chance!
            const hit = this.performAttack('both', 'mixed', totalDamage, this.hitChance.both);

            this.comboBuffer += 'B'; // 'B' für Both

            setTimeout(() => { this.isAttacking = false; }, this.attackDuration);
            return hit;
        },

        // 🎯 Angriff ausführen mit Hit Detection
        performAttack(hand, type, damage, customHitChance = null) {
            if (!this.currentTarget) {
                console.log('⚠️ Kein Ziel!');
                return { hit: false, reason: 'no_target' };
            }

            // Hit Chance berechnen
            let hitChance = customHitChance || this.hitChance[type] || 0.75;

            // Distanz zum Ziel beeinflusst Hit Chance
            if (this.targetDistance > 5) {
                hitChance *= 0.7; // 30% Penalty bei großer Distanz
            }

            // Roll für Hit/Miss
            const roll = Math.random();
            const isHit = roll < hitChance;

            if (isHit) {
                // HIT! Schaden anwenden
                console.log(`💥 HIT! ${hand} ${type} - ${Math.round(damage)} Schaden`);

                // Damage an Gegner (DungeonEnemies System)
                if (window.DungeonEnemies && this.currentTarget.userData && this.currentTarget.userData.enemyId) {
                    const enemyId = this.currentTarget.userData.enemyId;
                    window.DungeonEnemies.damageEnemy(enemyId, damage);
                }

                // Combo-Counter erhöhen
                this.combo.hits++;
                this.combo.lastHitTime = Date.now();
                this.combo.multiplier = Math.min(2.0, 1.0 + (this.combo.hits * 0.1));

                if (typeof notify === 'function') {
                    notify(`💥 ${Math.round(damage)} DMG (${this.combo.hits}x Combo!)`, 'success');
                }

                return { hit: true, damage, comboHits: this.combo.hits };

            } else {
                // MISS! NUR bei simultanen Angriffen (both) wird getaumelt!
                if (hand === 'both') {
                    // BEIDE HÄNDE VERFEHLT = TAUMELN!
                    console.log(`❌ MIX-ANGRIFF VERFEHLT! Taumeln für 500ms...`);
                    this.triggerStagger(500); // 500ms Stagger

                    if (typeof notify === 'function') {
                        notify('❌ MIX VERFEHLT! TAUMELN!', 'error');
                    }

                    return { hit: false, reason: 'miss', staggered: true };
                } else {
                    // Einzelangriff verfehlt = NUR miss, KEIN Taumeln (wie Skyrim)
                    console.log(`❌ Verfehlt (${hand})`);
                    if (typeof notify === 'function') {
                        notify(`❌ Verfehlt`, 'warning');
                    }
                    return { hit: false, reason: 'miss', staggered: false };
                }
            }
        },

        // 😵 Taumeln (Stagger) - Spieler ist verletzlich!
        triggerStagger(duration = 500) {
            this.isStaggered = true;
            this.staggerEndTime = Date.now() + duration;
            this.combo.hits = 0; // Combo unterbrochen!

            // Gegner können CRIT machen während Stagger
            // Das wird in DungeonEnemies.updateCombat() geprüft
            if (window.DungeonEnemies) {
                window.DungeonEnemies.playerIsStaggered = true;
                setTimeout(() => {
                    if (window.DungeonEnemies) {
                        window.DungeonEnemies.playerIsStaggered = false;
                    }
                }, duration);
            }

            setTimeout(() => {
                this.isStaggered = false;
                console.log('✅ Taumeln beendet');
            }, duration);
        },

        parry() {
            const now = Date.now();
            if (now - this.lastParryTime < 1000) return false;  // Cooldown
            this.isParrying = true;
            this.lastParryTime = now;
            setTimeout(() => { this.isParrying = false; }, this.parryWindow.end);
            return true;
        },

        dodge() {
            const now = Date.now();
            if (now - this.lastDodgeTime < this.dodgeRoll.cooldown) return false;
            if (this.stamina < this.dodgeRoll.staminaCost) return false;

            this.stamina -= this.dodgeRoll.staminaCost;
            this.dodgeRoll.active = true;
            this.lastDodgeTime = now;

            // i-frames für 200ms
            setTimeout(() => { this.dodgeRoll.active = false; }, 200);
            return true;
        },

        checkCombo() {
            const now = Date.now();
            if (now - this.lastComboTime > 800) {
                this.comboBuffer = this.comboBuffer.slice(-1);  // Reset wenn zu langsam
            }
            this.lastComboTime = now;

            // Check for Combo-Match
            for (const [sequence, combo] of Object.entries(this.dualWieldCombos)) {
                if (this.comboBuffer === sequence) {
                    console.log(`💥 COMBO: ${combo.name} (${combo.damage} DMG)`);
                    this.executeCombo(combo);
                    this.comboBuffer = '';
                    return combo;
                }
            }
            return null;
        },

        executeCombo(combo) {
            // Combo-Schaden anwenden
            if (this.currentTarget && window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, combo.damage);
            }

            if (typeof notify === 'function') {
                notify(`🌟 ${combo.name}! ${combo.damage} DMG`, 'success');
            }
        },

        takeDamage(amount, isCrit = false) {
            if (this.dodgeRoll.active) return 0;  // i-frames

            // STAGGER = 2x Schaden von Crits!
            if (this.isStaggered && isCrit) {
                amount *= 2.0;
                if (typeof notify === 'function') {
                    notify(`💀 CRITICAL HIT! ${Math.round(amount)} DMG`, 'error');
                }
            }

            if (this.isParrying) {
                // Parry successful - kein Schaden + Stamina zurück
                this.stamina = Math.min(this.maxStamina, this.stamina + 20);
                if (typeof notify === 'function') {
                    notify('🛡️ PARRY!', 'success');
                }
                return 0;
            }

            const defense = this.getArmorDefense();
            const damage = Math.max(1, amount - defense);
            this.health = Math.max(0, this.health - damage);
            return damage;
        },

        // 🪄 Cast Skill (Zauber/Abilities)
        castSkill(slotIndex) {
            if (!this.skillSystem) {
                console.warn('⚠️ Skill System nicht initialisiert!');
                return false;
            }

            const equippedSkills = this.skillSystem.getEquippedSkills();
            if (slotIndex >= equippedSkills.length) {
                console.warn(`⚠️ Kein Skill in Slot ${slotIndex + 1}`);
                return false;
            }

            const skillId = equippedSkills[slotIndex];
            const skill = this.skillSystem.learnedSkills[skillId];

            if (!skill) {
                console.warn(`⚠️ Skill nicht gefunden: ${skillId}`);
                return false;
            }

            // Check cooldown
            const now = Date.now();
            if (this.skillCooldowns[skillId] && now < this.skillCooldowns[skillId]) {
                const remaining = ((this.skillCooldowns[skillId] - now) / 1000).toFixed(1);
                console.log(`⏰ Skill auf Cooldown: ${remaining}s`);
                if (typeof notify === 'function') {
                    notify(`⏰ ${skill.name}: ${remaining}s`, 'warning');
                }
                return false;
            }

            // Check mana
            const manaCost = skill.getManaCostAtLevel();
            if (this.mana < manaCost) {
                console.log(`⚠️ Nicht genug Mana! (${manaCost} benötigt, ${Math.floor(this.mana)} verfügbar)`);
                if (typeof notify === 'function') {
                    notify(`⚠️ Nicht genug Mana für ${skill.name}`, 'error');
                }
                return false;
            }

            // Cast spell!
            this.mana -= manaCost;
            const cooldownMs = skill.getCooldownAtLevel() * 1000;
            this.skillCooldowns[skillId] = now + cooldownMs;

            console.log(`✨ ${skill.icon} ${skill.name} gewirkt! (Power: ${skill.getPowerAtLevel()}, Mana: -${manaCost})`);
            if (typeof notify === 'function') {
                notify(`✨ ${skill.icon} ${skill.name}`, 'success');
            }

            // Add XP
            skill.addXP(10);

            // Save progress
            this.skillSystem.save();

            // Trigger visual effect
            this.triggerSkillEffect(skill);

            return true;
        },

        // 🎨 Trigger Skill Visual Effect
        triggerSkillEffect(skill) {
            if (!scene || !characterGroup) return;

            const damage = skill.getPowerAtLevel();

            switch(skill.id) {
                case 'rune_fireball':
                    this.createFireballProjectile(damage);
                    break;
                case 'lightning_bolt':
                    this.createLightningBolt(damage);
                    break;
                case 'nature_heal':
                    this.createHealEffect();
                    break;
                case 'rune_ice_lance':
                    this.createIceLanceProjectile(damage);
                    break;
                case 'chain_lightning':
                    this.createChainLightning(damage);
                    break;
                case 'nature_roots':
                    this.createRootsEffect(damage);
                    break;
                case 'rune_lightning':
                    this.createLightningStrike(damage);
                    break;
                default:
                    console.log(`🎨 No visual effect for ${skill.name}`);
            }
        },

        // 🔥 Fireball Projectile
        createFireballProjectile(damage) {
            if (!this.currentTarget) {
                if (typeof notify === 'function') notify('⚠️ Kein Ziel!', 'warning');
                return;
            }

            const startPos = characterGroup.position.clone();
            startPos.y += 1.5;
            const targetPos = this.currentTarget.position.clone();
            targetPos.y += 1;

            const fireball = new THREE.Mesh(
                new THREE.SphereGeometry(0.3, 16, 16),
                new THREE.MeshBasicMaterial({ color: 0xff6600, emissive: 0xff3300 })
            );
            fireball.position.copy(startPos);
            scene.add(fireball);

            const direction = targetPos.clone().sub(startPos).normalize();
            const distance = startPos.distanceTo(targetPos);
            const duration = distance / 20; // 20 units/sec
            const startTime = Date.now();

            const animateFireball = () => {
                const elapsed = (Date.now() - startTime) / 1000;
                if (elapsed >= duration) {
                    // Impact!
                    scene.remove(fireball);
                    if (window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                        window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, damage);
                        console.log(`🔥 Fireball hit for ${damage} damage!`);
                    }
                    return;
                }

                fireball.position.addScaledVector(direction, 20 * 0.016);
                requestAnimationFrame(animateFireball);
            };
            animateFireball();
        },

        // ⚡ Lightning Bolt
        createLightningBolt(damage) {
            if (!this.currentTarget) {
                if (typeof notify === 'function') notify('⚠️ Kein Ziel!', 'warning');
                return;
            }

            const targetPos = this.currentTarget.position.clone();
            const points = [
                new THREE.Vector3(targetPos.x, targetPos.y + 10, targetPos.z),
                new THREE.Vector3(targetPos.x, targetPos.y, targetPos.z)
            ];

            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({ color: 0x00aaff, linewidth: 5 });
            const lightning = new THREE.Line(geometry, material);
            scene.add(lightning);

            // Damage enemy
            if (window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, damage);
                console.log(`⚡ Lightning hit for ${damage} damage!`);
            }

            setTimeout(() => scene.remove(lightning), 150);
        },

        // 🌿 Heal Effect
        createHealEffect() {
            const healAmount = Math.min(20, this.maxHealth - this.health);
            this.health = Math.min(this.maxHealth, this.health + healAmount);

            const ring = new THREE.Mesh(
                new THREE.RingGeometry(0.5, 1, 32),
                new THREE.MeshBasicMaterial({ color: 0x00ff00, side: THREE.DoubleSide, transparent: true, opacity: 0.6 })
            );
            ring.position.copy(characterGroup.position);
            ring.rotation.x = -Math.PI / 2;
            scene.add(ring);

            console.log(`🌿 Healed ${healAmount} HP!`);
            if (typeof notify === 'function') notify(`🌿 +${healAmount} HP`, 'success');

            let scale = 1;
            const animateHeal = () => {
                scale += 0.1;
                ring.scale.set(scale, scale, 1);
                ring.material.opacity -= 0.02;
                if (ring.material.opacity <= 0) {
                    scene.remove(ring);
                    return;
                }
                requestAnimationFrame(animateHeal);
            };
            animateHeal();
        },

        // ❄️ Ice Lance Projectile
        createIceLanceProjectile(damage) {
            if (!this.currentTarget) {
                if (typeof notify === 'function') notify('⚠️ Kein Ziel!', 'warning');
                return;
            }

            const startPos = characterGroup.position.clone();
            startPos.y += 1.5;
            const targetPos = this.currentTarget.position.clone();

            const iceLance = new THREE.Mesh(
                new THREE.ConeGeometry(0.15, 1, 8),
                new THREE.MeshBasicMaterial({ color: 0x00ccff, emissive: 0x0066cc })
            );
            iceLance.position.copy(startPos);

            const direction = targetPos.clone().sub(startPos).normalize();
            iceLance.lookAt(targetPos);
            iceLance.rotateX(Math.PI / 2);

            scene.add(iceLance);

            const distance = startPos.distanceTo(targetPos);
            const duration = distance / 25;
            const startTime = Date.now();

            const animateIce = () => {
                const elapsed = (Date.now() - startTime) / 1000;
                if (elapsed >= duration) {
                    scene.remove(iceLance);
                    if (window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                        window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, damage);
                        console.log(`❄️ Ice Lance hit for ${damage} damage!`);
                    }
                    return;
                }
                iceLance.position.addScaledVector(direction, 25 * 0.016);
                requestAnimationFrame(animateIce);
            };
            animateIce();
        },

        // ⚡⚡ Chain Lightning
        createChainLightning(damage) {
            if (!this.currentTarget) {
                if (typeof notify === 'function') notify('⚠️ Kein Ziel!', 'warning');
                return;
            }

            const playerPos = characterGroup.position.clone();
            playerPos.y += 1.5;
            const targetPos = this.currentTarget.position.clone();
            targetPos.y += 1;

            const points = [playerPos, targetPos];
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({ color: 0xffff00, linewidth: 3 });
            const chain = new THREE.Line(geometry, material);
            scene.add(chain);

            if (window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, damage);
                console.log(`⚡⚡ Chain Lightning hit for ${damage} damage!`);
            }

            setTimeout(() => scene.remove(chain), 200);
        },

        // 🌳 Roots Effect
        createRootsEffect(damage) {
            if (!this.currentTarget) {
                if (typeof notify === 'function') notify('⚠️ Kein Ziel!', 'warning');
                return;
            }

            const targetPos = this.currentTarget.position.clone();
            const roots = new THREE.Mesh(
                new THREE.CylinderGeometry(0.8, 0.8, 0.2, 8),
                new THREE.MeshBasicMaterial({ color: 0x8b4513, transparent: true, opacity: 0.7 })
            );
            roots.position.copy(targetPos);
            roots.position.y += 0.1;
            scene.add(roots);

            if (window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, damage);
                console.log(`🌳 Roots snared for ${damage} damage!`);
            }

            setTimeout(() => scene.remove(roots), 3000);
        },

        // ⚡ Lightning Strike (from sky)
        createLightningStrike(damage) {
            if (!this.currentTarget) {
                if (typeof notify === 'function') notify('⚠️ Kein Ziel!', 'warning');
                return;
            }

            const targetPos = this.currentTarget.position.clone();
            const points = [
                new THREE.Vector3(targetPos.x, targetPos.y + 15, targetPos.z),
                new THREE.Vector3(targetPos.x, targetPos.y, targetPos.z)
            ];

            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 8 });
            const strike = new THREE.Line(geometry, material);
            scene.add(strike);

            if (window.DungeonEnemies && this.currentTarget.userData.enemyId) {
                window.DungeonEnemies.damageEnemy(this.currentTarget.userData.enemyId, damage);
                console.log(`⚡ Lightning Strike hit for ${damage} damage!`);
            }

            setTimeout(() => scene.remove(strike), 100);
        },

        update(delta) {
            // Stamina regeneriert sich
            this.stamina = Math.min(this.maxStamina, this.stamina + 10 * delta);

            // Mana regeneriert sich
            this.mana = Math.min(this.maxMana, this.mana + this.manaRegen * delta);

            // Combo-Buffer timeout
            if (Date.now() - this.lastComboTime > 800) {
                this.comboBuffer = '';
            }

            // Combo timeout (kein Hit = Reset)
            if (Date.now() - this.combo.lastHitTime > this.combo.timeout) {
                this.combo.hits = 0;
                this.combo.multiplier = 1.0;
            }

            // Update Target Distance
            if (this.currentTarget && characterGroup) {
                this.targetDistance = characterGroup.position.distanceTo(this.currentTarget.position);
            }
        }
    };

    let webcamStream = null;
    let webcamElement = null;

    // ⚔️ Combat Stats UI
    let combatStatsUI = null;

    // 🚪 Building Interaction
    let nearBuilding = null;
    let buildingPromptUI = null;

    // Orbit Camera Controls - Start HINTER dem Charakter
    let orbitYaw = Math.PI;  // 180° = HINTEN (nicht 45° = rechts-vorne!)
    let orbitPitch = 0.3;
    let orbitDistance = 14;
    const ORBIT_MIN_DIST = 6;
    const ORBIT_MAX_DIST = 40;
    const ORBIT_MIN_PITCH = -Math.PI / 2 + 0.12;
    const ORBIT_MAX_PITCH = Math.PI / 2 - 0.12;

    const activePointers = new Map();
    let pointerMode = null;
    let dragStartPos = { x: 0, y: 0 };
    let dragStartYaw = orbitYaw;
    let dragStartPitch = orbitPitch;
    let pinchStartDist = 0;
    let pinchBaseDistance = orbitDistance;
    let orbitCanvas = null;

    let cameraMode = CAMERA_MODES.ORBIT;

    // 💎 GROUND LOOT SYSTEM
    let groundLoot = []; // Active loot items on the ground
    let nearestLoot = null;

    function getContainer() {
        return document.getElementById('scene');
    }

    function init() {
        if (scene || typeof THREE === 'undefined') {
            if (typeof THREE === 'undefined') {
                console.warn('Scene3D: THREE.js not yet available.');
            }
            return;
        }

        const container = getContainer();
        if (!container) {
            console.warn('Scene3D: container element #scene not found.');
            return;
        }

        scene = new THREE.Scene();
        scene.background = new THREE.Color(DEFAULT_PALETTE.background);
        scene.fog = new THREE.Fog(DEFAULT_PALETTE.fog, 12, 160);

        camera = new THREE.PerspectiveCamera(
            65,
            container.clientWidth / container.clientHeight,
            0.1,
            2000
        );
        camera.position.set(0, 12, 28);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(window.devicePixelRatio || 1);
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.innerHTML = '';
        container.appendChild(renderer.domElement);

        clock = new THREE.Clock();

        setupLights();
        installEventHandlers();
        ensureKayKitLoader();
        loadCharacter();
        createCombatStatsUI();
        createBuildingPromptUI();
        createSkillHotbarUI();
        createInventoryUI();

        // 🪄 Initialize Skill System
        if (typeof SkillSystem !== 'undefined') {
            COMBAT_SYSTEM.skillSystem = new SkillSystem();

            // DEV: Lerne ein paar Skills zum Testen
            COMBAT_SYSTEM.skillSystem.learnSkill('rune_fireball');
            COMBAT_SYSTEM.skillSystem.learnSkill('lightning_bolt');
            COMBAT_SYSTEM.skillSystem.learnSkill('nature_heal');

            // Equip skills to hotbar
            COMBAT_SYSTEM.skillSystem.equipSkill('rune_fireball');    // Slot 1
            COMBAT_SYSTEM.skillSystem.equipSkill('lightning_bolt');   // Slot 2
            COMBAT_SYSTEM.skillSystem.equipSkill('nature_heal');      // Slot 3

            console.log('🪄 Skill System initialisiert mit 3 Skills');
        }

        // 🎒 Initialize Inventory System
        if (typeof InventorySystem !== 'undefined') {
            COMBAT_SYSTEM.inventorySystem = new InventorySystem(null, COMBAT_SYSTEM);

            // DEV: Add starter equipment
            COMBAT_SYSTEM.inventorySystem.addItem('fire_sword', 1);
            COMBAT_SYSTEM.inventorySystem.addItem('ice_dagger', 1);
            COMBAT_SYSTEM.inventorySystem.addItem('leather_armor', 1);
            COMBAT_SYSTEM.inventorySystem.addItem('iron_helmet', 1);

            // Auto-equip starter items
            COMBAT_SYSTEM.inventorySystem.equipItem('fire_sword');
            COMBAT_SYSTEM.inventorySystem.equipItem('ice_dagger');
            COMBAT_SYSTEM.inventorySystem.equipItem('leather_armor');
            COMBAT_SYSTEM.inventorySystem.equipItem('iron_helmet');

            console.log('🎒 Inventory System initialisiert mit Starter-Equipment');

            // 💎 DEV: Spawn test loot items
            setTimeout(() => {
                if (characterGroup) {
                    const playerPos = characterGroup.position;
                    spawnLootItem('lightning_staff', new THREE.Vector3(playerPos.x + 3, 0, playerPos.z + 2));
                    spawnLootItem('crystal_shard', new THREE.Vector3(playerPos.x - 3, 0, playerPos.z + 2));
                    spawnLootItem('vitality_amulet', new THREE.Vector3(playerPos.x, 0, playerPos.z + 5));
                    spawnLootItem('', new THREE.Vector3(playerPos.x + 5, 0, playerPos.z), 100); // 100g
                    console.log('💎 DEV Test Loot spawned');
                }
            }, 2000);
        }

        // 📜 Initialize Quest System
        if (typeof QuestManager !== 'undefined') {
            window.questManager = new QuestManager(COMBAT_SYSTEM.inventorySystem);
            console.log('📜 Quest System initialized');
        }

        // 🎭 Initialize NPC System
        if (typeof NPCSystem !== 'undefined' && scene) {
            window.npcSystem = new NPCSystem(scene, THREE);
            console.log('🎭 NPC System initialized');
        }

        // 🔨 Initialize Crafting System
        if (typeof CraftingSystem !== 'undefined') {
            window.craftingSystem = new CraftingSystem(COMBAT_SYSTEM.inventorySystem);
            console.log('🔨 Crafting System initialized');
        }

        // 🏠 Initialize Housing System
        if (typeof HousingSystem !== 'undefined' && scene) {
            HousingSystem.init(scene, 1); // Player ID 1 for now
            HousingSystem.setScene(scene);
            console.log('🏠 Housing System 3D initialized');
        }

        // 🌾 Initialize Farming System
        if (typeof FarmingSystem !== 'undefined' && scene) {
            FarmingSystem.init(scene, 1); // Player ID 1 for now
            FarmingSystem.setScene(scene);
            console.log('🌾 Farming System 3D initialized');
        }

        // 🌍 Initialize World Manager (9600×9600 Grid World)
        if (useWorldManager && window.WorldManager) {
            initWorldManager();
        } else {
            // Fallback to old 2400×2400 map
            setupFallbackRoom();
            scheduleRoomBuild();
        }

        startAnimationLoop();

        document.dispatchEvent(new CustomEvent('scene3d:ready'));
        console.log('Scene3D initialised.');
    }

    async function initWorldManager() {
        console.log('🌍 Initializing WorldManager for 9600×9600 Open World...');

        try {
            // Create WorldManager instance
            worldManager = new window.WorldManager(scene, camera);

            // Initialize with backend data
            await worldManager.initialize({
                dataPath: '/entwicklung/data/',
                enableLOD: true,
                enableStreaming: true
            });

            // Set player starting position (Götterfels - Schwarze Mühle)
            if (characterGroup) {
                characterGroup.position.set(4800, 0, 4800);
            }

            // Update world based on player position
            worldManager.setPlayerPosition(characterGroup ? characterGroup.position : new THREE.Vector3(4800, 0, 4800));

            // Disable old room system
            usingFallbackRoom = false;
            currentRoomSpan = 9600;  // Full world size

            console.log('✅ WorldManager initialized successfully!');
            console.log(`   World Size: 9600×9600`);
            console.log(`   Starting Position: Götterfels (4800, 4800)`);

        } catch (error) {
            console.error('❌ Failed to initialize WorldManager:', error);
            console.error('Error details:', error.message);
            console.error('Stack trace:', error.stack);

            // Show user-friendly error
            alert('⚠️ WorldManager konnte nicht geladen werden!\n\n' +
                  'Fehler: ' + error.message + '\n\n' +
                  'Fallback: Lade altes 2400×2400 System...\n\n' +
                  'Für Open World, nutze: najika_world_9regions_test.html');

            console.log('⚠️ Falling back to old 2400×2400 map...');

            // Fallback to old system
            useWorldManager = false;
            setupFallbackRoom();
            scheduleRoomBuild();
        }
    }

    function createCombatStatsUI() {
        combatStatsUI = document.createElement('div');
        combatStatsUI.id = 'combat-stats-ui';
        combatStatsUI.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.85);
            border: 3px solid #ff6b9d;
            border-radius: 12px;
            padding: 15px;
            color: white;
            font-family: monospace;
            font-size: 13px;
            z-index: 1000;
            min-width: 220px;
        `;

        combatStatsUI.innerHTML = `
            <h3 style="display: flex; justify-content: space-between; align-items: center; cursor: pointer; margin: 0 0 12px 0; font-size: 15px; font-weight: bold;" id="combat-header">
                <span>⚔️ COMBAT</span>
                <button id="combat-toggle" style="background: none; border: none; color: #ff6b9d; font-size: 1.2rem; cursor: pointer; padding: 0; margin: 0;">▼</button>
            </h3>
            <div id="combat-content">
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                        <span>❤️ HP:</span>
                        <span id="combat-hp-text">100/100</span>
                    </div>
                    <div style="background: #333; height: 16px; border-radius: 5px; overflow: hidden;">
                        <div id="combat-hp-bar" style="background: linear-gradient(90deg, #ff1744, #ff6b9d); height: 100%; width: 100%; transition: width 0.3s;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                        <span>⚡ Stamina:</span>
                        <span id="combat-stamina-text">100/100</span>
                    </div>
                    <div style="background: #333; height: 16px; border-radius: 5px; overflow: hidden;">
                        <div id="combat-stamina-bar" style="background: linear-gradient(90deg, #4a90e2, #50c878); height: 100%; width: 100%; transition: width 0.3s;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                        <span>🪄 Mana:</span>
                        <span id="combat-mana-text">100/100</span>
                    </div>
                    <div style="background: #333; height: 16px; border-radius: 5px; overflow: hidden;">
                        <div id="combat-mana-bar" style="background: linear-gradient(90deg, #9c27b0, #e91e63); height: 100%; width: 100%; transition: width 0.3s;"></div>
                    </div>
                </div>
                <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #444; font-size: 11px;">
                    <div><strong>⚔️ Equipment:</strong></div>
                    <div id="combat-equipment" style="margin-top: 5px; line-height: 1.4;">
                        <div>L: <span id="equip-left">Najika Staff</span></div>
                        <div>R: <span id="equip-right">Eisenschwert</span></div>
                        <div>🛡️: <span id="equip-armor">10 DEF</span></div>
                    </div>
                </div>
                <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #444; font-size: 10px; color: #aaa;">
                    J/K: Attack | Tab: Lock-On | 1-9: Skills
                </div>
            </div>
        `;

        document.body.appendChild(combatStatsUI);

        // Toggle collapse handler
        const header = combatStatsUI.querySelector('#combat-header');
        const toggle = combatStatsUI.querySelector('#combat-toggle');
        if (header && toggle) {
            const toggleCombat = () => {
                const content = combatStatsUI.querySelector('#combat-content');
                if (content.style.display === 'none') {
                    content.style.display = 'block';
                    toggle.textContent = '▼';
                } else {
                    content.style.display = 'none';
                    toggle.textContent = '▶';
                }
            };
            header.addEventListener('click', toggleCombat);
            toggle.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleCombat();
            });
        }
    }

    function updateCombatStatsUI() {
        if (!combatStatsUI) return;

        // HP
        const hpBar = combatStatsUI.querySelector('#combat-hp-bar');
        const hpText = combatStatsUI.querySelector('#combat-hp-text');
        if (hpBar && hpText) {
            const hpPercent = (COMBAT_SYSTEM.health / COMBAT_SYSTEM.maxHealth) * 100;
            hpBar.style.width = `${hpPercent}%`;
            hpText.textContent = `${Math.round(COMBAT_SYSTEM.health)}/${COMBAT_SYSTEM.maxHealth}`;
        }

        // Stamina
        const staminaBar = combatStatsUI.querySelector('#combat-stamina-bar');
        const staminaText = combatStatsUI.querySelector('#combat-stamina-text');
        if (staminaBar && staminaText) {
            const staminaPercent = (COMBAT_SYSTEM.stamina / COMBAT_SYSTEM.maxStamina) * 100;
            staminaBar.style.width = `${staminaPercent}%`;
            staminaText.textContent = `${Math.round(COMBAT_SYSTEM.stamina)}/${COMBAT_SYSTEM.maxStamina}`;
        }

        // Mana
        const manaBar = combatStatsUI.querySelector('#combat-mana-bar');
        const manaText = combatStatsUI.querySelector('#combat-mana-text');
        if (manaBar && manaText) {
            const manaPercent = (COMBAT_SYSTEM.mana / COMBAT_SYSTEM.maxMana) * 100;
            manaBar.style.width = `${manaPercent}%`;
            manaText.textContent = `${Math.round(COMBAT_SYSTEM.mana)}/${COMBAT_SYSTEM.maxMana}`;
        }

        // Equipment
        const equipLeft = combatStatsUI.querySelector('#equip-left');
        const equipRight = combatStatsUI.querySelector('#equip-right');
        const equipArmor = combatStatsUI.querySelector('#equip-armor');

        if (COMBAT_SYSTEM.inventorySystem) {
            const leftWeapon = COMBAT_SYSTEM.inventorySystem.equipment.weapon_left;
            const rightWeapon = COMBAT_SYSTEM.inventorySystem.equipment.weapon_right;
            const armorChest = COMBAT_SYSTEM.inventorySystem.equipment.armor_chest;
            const armorHead = COMBAT_SYSTEM.inventorySystem.equipment.armor_head;

            if (equipLeft) {
                equipLeft.textContent = leftWeapon ? `${leftWeapon.data.icon} ${leftWeapon.data.name}` : 'Unarmed';
            }
            if (equipRight) {
                equipRight.textContent = rightWeapon ? `${rightWeapon.data.icon} ${rightWeapon.data.name}` : 'Unarmed';
            }
            if (equipArmor) {
                const totalDef = COMBAT_SYSTEM.getArmorDefense();
                const armorName = armorChest ? armorChest.data.name : (armorHead ? armorHead.data.name : 'None');
                equipArmor.textContent = `${armorName} (${totalDef} DEF)`;
            }
        }
    }

    // 🎯 Find Nearest Enemy für Auto-Targeting
    function findNearestEnemy() {
        if (!window.DungeonEnemies || !characterGroup) return null;

        const enemies = window.DungeonEnemies.getActiveEnemies();
        if (!enemies || enemies.length === 0) return null;

        let nearest = null;
        let minDistance = Infinity;

        enemies.forEach(enemy => {
            if (!enemy.mesh || enemy.isDead) return;

            const distance = characterGroup.position.distanceTo(enemy.mesh.position);
            if (distance < minDistance) {
                minDistance = distance;
                nearest = { enemy: enemy.mesh, distance };
            }
        });

        return nearest;
    }

    function createBuildingPromptUI() {
        buildingPromptUI = document.createElement('div');
        buildingPromptUI.id = 'building-prompt-ui';
        buildingPromptUI.style.cssText = `
            position: fixed;
            bottom: 150px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.9);
            border: 3px solid #ffffff;
            border-radius: 15px;
            padding: 15px 30px;
            color: white;
            font-family: monospace;
            font-size: 16px;
            font-weight: bold;
            display: none;
            z-index: 1000;
            animation: pulse 1.5s infinite;
            box-shadow: 0 6px 12px rgba(0,0,0,0.6);
        `;

        buildingPromptUI.innerHTML = `
            <div style="text-align: center;">
                <div id="building-prompt-text">E - Betreten</div>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { transform: translateX(-50%) scale(1); }
                    50% { transform: translateX(-50%) scale(1.05); }
                }
            </style>
        `;

        document.body.appendChild(buildingPromptUI);
    }

    function showBuildingPrompt(building) {
        if (!buildingPromptUI || !building) return;
        const textEl = buildingPromptUI.querySelector('#building-prompt-text');
        if (textEl) {
            textEl.textContent = `E - ${building.userData.buildingName} betreten`;
        }
        buildingPromptUI.style.display = 'block';
    }

    function hideBuildingPrompt() {
        if (!buildingPromptUI) return;
        buildingPromptUI.style.display = 'none';
    }

    // 🪄 SKILL HOTBAR UI
    let skillHotbarUI = null;

    function createSkillHotbarUI() {
        skillHotbarUI = document.createElement('div');
        skillHotbarUI.id = 'skill-hotbar-ui';
        skillHotbarUI.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            z-index: 1000;
        `;
        document.body.appendChild(skillHotbarUI);
        updateSkillHotbarUI();
    }

    function updateSkillHotbarUI() {
        if (!skillHotbarUI || !COMBAT_SYSTEM.skillSystem) return;

        const equippedSkills = COMBAT_SYSTEM.skillSystem.getEquippedSkills();
        const maxSlots = 9;

        let html = '';
        for (let i = 0; i < maxSlots; i++) {
            const skillId = equippedSkills[i];
            const skill = skillId ? COMBAT_SYSTEM.skillSystem.learnedSkills[skillId] : null;

            // Check cooldown
            const now = Date.now();
            const cooldownEnd = COMBAT_SYSTEM.skillCooldowns[skillId] || 0;
            const onCooldown = now < cooldownEnd;
            const cooldownPercent = onCooldown ? ((cooldownEnd - now) / (skill.getCooldownAtLevel() * 1000)) * 100 : 0;
            const cooldownSec = onCooldown ? ((cooldownEnd - now) / 1000).toFixed(1) : '';

            // Check mana
            const manaCost = skill ? skill.getManaCostAtLevel() : 0;
            const canAfford = skill ? COMBAT_SYSTEM.mana >= manaCost : false;

            html += `
                <div style="
                    width: 60px;
                    height: 60px;
                    background: ${skill ? 'rgba(0,0,0,0.9)' : 'rgba(0,0,0,0.5)'};
                    border: 2px solid ${skill ? (onCooldown ? '#666' : (canAfford ? '#9c27b0' : '#ff4444')) : '#333'};
                    border-radius: 8px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-family: monospace;
                    position: relative;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.5);
                    ${onCooldown ? 'opacity: 0.5;' : ''}
                ">
                    ${skill ? `
                        <div style="font-size: 24px;">${skill.icon}</div>
                        <div style="font-size: 9px; margin-top: 2px;">${i + 1}</div>
                        <div style="font-size: 8px; color: #e91e63;">${manaCost}M</div>
                        ${onCooldown ? `
                            <div style="
                                position: absolute;
                                bottom: 0;
                                left: 0;
                                right: 0;
                                height: ${cooldownPercent}%;
                                background: rgba(255,0,0,0.6);
                                border-radius: 0 0 6px 6px;
                            "></div>
                            <div style="
                                position: absolute;
                                top: 50%;
                                left: 50%;
                                transform: translate(-50%, -50%);
                                font-size: 14px;
                                font-weight: bold;
                                text-shadow: 0 0 4px black;
                            ">${cooldownSec}</div>
                        ` : ''}
                    ` : `
                        <div style="font-size: 18px; color: #666;">-</div>
                        <div style="font-size: 9px; color: #666;">${i + 1}</div>
                    `}
                </div>
            `;
        }

        skillHotbarUI.innerHTML = html;
    }

    // 🎒 INVENTORY UI MODAL
    let inventoryUI = null;
    let draggedItem = null;

    function createInventoryUI() {
        inventoryUI = document.createElement('div');
        inventoryUI.id = 'inventory-ui';
        inventoryUI.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 900px;
            max-width: 95vw;
            height: 700px;
            max-height: 90vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 3px solid #667eea;
            border-radius: 15px;
            padding: 20px;
            display: none;
            z-index: 2000;
            color: white;
            font-family: monospace;
            overflow-y: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        `;

        inventoryUI.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0; font-size: 24px;">🎒 INVENTORY</h2>
                <div style="display: flex; align-items: center; gap: 20px;">
                    <span style="font-size: 18px; color: #ffd700;">💰 <span id="inv-gold">100</span>g</span>
                    <button id="inv-close" style="
                        background: #ff4444;
                        border: none;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-weight: bold;
                    ">✕ Close</button>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
                <!-- Left: Inventory Grid -->
                <div>
                    <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #aaa;">Items (50 slots)</h3>
                    <div id="inv-grid" style="
                        display: grid;
                        grid-template-columns: repeat(10, 1fr);
                        gap: 5px;
                        background: rgba(0,0,0,0.3);
                        padding: 10px;
                        border-radius: 8px;
                        min-height: 400px;
                    "></div>
                </div>

                <!-- Right: Equipment Paperdoll -->
                <div>
                    <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #aaa;">Equipment</h3>
                    <div id="inv-equipment" style="
                        background: rgba(0,0,0,0.3);
                        padding: 15px;
                        border-radius: 8px;
                    ">
                        <div style="display: flex; flex-direction: column; gap: 10px;"></div>
                    </div>

                    <h3 style="margin: 20px 0 10px 0; font-size: 16px; color: #aaa;">Stats</h3>
                    <div id="inv-stats" style="
                        background: rgba(0,0,0,0.3);
                        padding: 15px;
                        border-radius: 8px;
                        font-size: 12px;
                        line-height: 1.6;
                    "></div>
                </div>
            </div>
        `;

        document.body.appendChild(inventoryUI);

        // Close button
        inventoryUI.querySelector('#inv-close').addEventListener('click', () => toggleInventoryUI());

        updateInventoryUI();
    }

    function toggleInventoryUI() {
        if (!inventoryUI) createInventoryUI();

        if (inventoryUI.style.display === 'none') {
            inventoryUI.style.display = 'block';
            updateInventoryUI();
        } else {
            inventoryUI.style.display = 'none';
        }
    }

    function updateInventoryUI() {
        if (!inventoryUI || !COMBAT_SYSTEM.inventorySystem) return;

        const inv = COMBAT_SYSTEM.inventorySystem;

        // Update gold
        const goldEl = inventoryUI.querySelector('#inv-gold');
        if (goldEl) goldEl.textContent = inv.gold;

        // Update inventory grid
        const gridEl = inventoryUI.querySelector('#inv-grid');
        if (gridEl) {
            gridEl.innerHTML = '';

            // Create 50 slots
            for (let i = 0; i < inv.maxSlots; i++) {
                const item = inv.items[i];
                const slot = createInventorySlot(item, i, 'inventory');
                gridEl.appendChild(slot);
            }
        }

        // Update equipment slots
        const equipEl = inventoryUI.querySelector('#inv-equipment > div');
        if (equipEl) {
            equipEl.innerHTML = '';

            const equipSlots = [
                { key: 'weapon_left', label: '🗡️ Left Hand' },
                { key: 'weapon_right', label: '⚔️ Right Hand' },
                { key: 'armor_head', label: '⛑️ Head' },
                { key: 'armor_chest', label: '🛡️ Chest' },
                { key: 'armor_legs', label: '👖 Legs' },
                { key: 'accessory_1', label: '💍 Accessory 1' },
                { key: 'accessory_2', label: '💍 Accessory 2' }
            ];

            equipSlots.forEach(({ key, label }) => {
                const item = inv.equipment[key];
                const slotContainer = document.createElement('div');
                slotContainer.style.cssText = 'display: flex; align-items: center; gap: 10px; margin-bottom: 8px;';

                const labelEl = document.createElement('span');
                labelEl.textContent = label;
                labelEl.style.cssText = 'min-width: 120px; font-size: 11px;';

                const slot = createInventorySlot(item, key, 'equipment');
                slot.style.width = '50px';
                slot.style.height = '50px';

                slotContainer.appendChild(labelEl);
                slotContainer.appendChild(slot);
                equipEl.appendChild(slotContainer);
            });
        }

        // Update stats
        const statsEl = inventoryUI.querySelector('#inv-stats');
        if (statsEl) {
            const stats = inv.getTotalStats();
            statsEl.innerHTML = `
                <div>⚔️ Damage: <strong>${stats.damage}</strong></div>
                <div>🛡️ Defense: <strong>${stats.defense}</strong></div>
                <div>💪 Strength: <strong>${stats.strength}%</strong></div>
                <div>❤️ Max HP: <strong>+${stats.max_hp}</strong></div>
                <div>💚 HP Regen: <strong>+${stats.hp_regen}/s</strong></div>
                <div>⚡ Speed: <strong>×${stats.speed_modifier.toFixed(2)}</strong></div>
                <div>⚖️ Weight: <strong>${stats.weight}</strong></div>
            `;
        }
    }

    function createInventorySlot(item, index, slotType) {
        const slot = document.createElement('div');
        slot.className = 'inv-slot';
        slot.dataset.index = index;
        slot.dataset.slotType = slotType;

        const rarityColors = {
            common: '#aaa',
            uncommon: '#1eff00',
            rare: '#0070dd',
            legendary: '#a335ee',
            quest: '#ffd700'
        };

        if (item) {
            const rarity = item.data.rarity || 'common';
            const borderColor = rarityColors[rarity];

            slot.style.cssText = `
                width: 60px;
                height: 60px;
                background: rgba(0,0,0,0.6);
                border: 2px solid ${borderColor};
                border-radius: 5px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: grab;
                position: relative;
                transition: transform 0.1s, box-shadow 0.1s;
            `;

            slot.innerHTML = `
                <div style="font-size: 28px;">${item.data.icon || '📦'}</div>
                ${item.quantity > 1 ? `<div style="position: absolute; bottom: 2px; right: 4px; font-size: 10px; font-weight: bold; text-shadow: 0 0 2px black;">${item.quantity}</div>` : ''}
            `;

            // Tooltip
            slot.title = `${item.data.name}\n${item.data.description || ''}\nRarity: ${rarity}`;

            // Drag events
            slot.draggable = true;
            slot.addEventListener('dragstart', onDragStart);
            slot.addEventListener('dragover', onDragOver);
            slot.addEventListener('drop', onDrop);
            slot.addEventListener('dragend', onDragEnd);

            // Right-click to use/equip
            slot.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                if (slotType === 'inventory') {
                    if (item.data.type === 'weapon' || item.data.type === 'armor' || item.data.type === 'accessory') {
                        COMBAT_SYSTEM.inventorySystem.equipItem(item.id);
                        updateInventoryUI();
                    } else if (item.data.type === 'food') {
                        COMBAT_SYSTEM.inventorySystem.useItem(item.id);
                        updateInventoryUI();
                    }
                } else if (slotType === 'equipment') {
                    COMBAT_SYSTEM.inventorySystem.unequipItem(index);
                    updateInventoryUI();
                }
            });

            // Hover effect
            slot.addEventListener('mouseenter', () => {
                slot.style.transform = 'scale(1.1)';
                slot.style.boxShadow = `0 0 15px ${borderColor}`;
            });
            slot.addEventListener('mouseleave', () => {
                slot.style.transform = 'scale(1)';
                slot.style.boxShadow = 'none';
            });
        } else {
            // Empty slot
            slot.style.cssText = `
                width: 60px;
                height: 60px;
                background: rgba(0,0,0,0.3);
                border: 2px solid #333;
                border-radius: 5px;
                display: flex;
                align-items: center;
                justify-content: center;
            `;

            // Can still drop items here
            slot.addEventListener('dragover', onDragOver);
            slot.addEventListener('drop', onDrop);
        }

        return slot;
    }

    function onDragStart(e) {
        draggedItem = {
            slotType: e.target.dataset.slotType,
            index: e.target.dataset.index
        };
        e.target.style.opacity = '0.5';
    }

    function onDragOver(e) {
        e.preventDefault(); // Allow drop
        e.dataTransfer.dropEffect = 'move';
    }

    function onDrop(e) {
        e.preventDefault();
        if (!draggedItem) return;

        const targetSlotType = e.currentTarget.dataset.slotType;
        const targetIndex = e.currentTarget.dataset.index;

        // TODO: Implement drag & drop logic
        // This would move items between inventory slots
        // Or equip/unequip items by dragging to equipment slots
        console.log(`Drop: ${draggedItem.slotType}[${draggedItem.index}] → ${targetSlotType}[${targetIndex}]`);

        updateInventoryUI();
    }

    function onDragEnd(e) {
        e.target.style.opacity = '1';
        draggedItem = null;
    }

    // 💎 GROUND LOOT SYSTEM

    function spawnLootItem(itemId, position, gold = 0) {
        if (!scene || !COMBAT_SYSTEM.inventorySystem) return null;

        const itemData = COMBAT_SYSTEM.inventorySystem.itemDatabase[itemId];
        if (!itemData && gold === 0) {
            console.warn(`⚠️ Unknown item: ${itemId}`);
            return null;
        }

        // Create loot object (golden sphere for now, can be replaced with models)
        const geometry = new THREE.SphereGeometry(0.3, 16, 16);
        const rarityColors = {
            common: 0xaaaaaa,
            uncommon: 0x1eff00,
            rare: 0x0070dd,
            legendary: 0xa335ee,
            quest: 0xffd700
        };

        const rarity = itemData ? itemData.rarity : 'common';
        const color = gold > 0 ? 0xffd700 : (rarityColors[rarity] || 0xaaaaaa);

        const material = new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.5,
            metalness: 0.8,
            roughness: 0.2
        });

        const lootMesh = new THREE.Mesh(geometry, material);
        lootMesh.position.copy(position);
        lootMesh.position.y += 0.5; // Slightly above ground

        // Add floating animation
        lootMesh.userData.startY = lootMesh.position.y;
        lootMesh.userData.floatTime = 0;

        // Store loot data
        lootMesh.userData.itemId = itemId;
        lootMesh.userData.gold = gold;
        lootMesh.userData.rarity = rarity;
        lootMesh.userData.isLoot = true;

        scene.add(lootMesh);

        // Create loot beam effect
        const beamHeight = gold > 0 ? 15 : (rarity === 'legendary' ? 20 : (rarity === 'rare' ? 12 : 8));
        createLootBeam(lootMesh.position, color, beamHeight, rarity);

        const lootObj = {
            mesh: lootMesh,
            itemId: itemId,
            gold: gold,
            position: position.clone()
        };

        groundLoot.push(lootObj);

        console.log(`💎 Loot spawned: ${itemData ? itemData.name : `${gold}g`} at`, position);
        return lootObj;
    }

    function createLootBeam(position, color, height = 10, rarity = 'common') {
        // Create vertical beam of light
        const beamGeometry = new THREE.CylinderGeometry(0.05, 0.2, height, 8);
        const beamMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: rarity === 'legendary' ? 0.8 : (rarity === 'rare' ? 0.6 : 0.4)
        });

        const beam = new THREE.Mesh(beamGeometry, beamMaterial);
        beam.position.copy(position);
        beam.position.y += height / 2;

        scene.add(beam);

        // Animate and remove after 5 seconds
        let elapsed = 0;
        const animateBeam = () => {
            elapsed += 0.016;
            if (elapsed > 5) {
                scene.remove(beam);
                return;
            }

            beam.material.opacity = (1 - elapsed / 5) * (rarity === 'legendary' ? 0.8 : 0.5);
            beam.rotation.y += 0.02;
            requestAnimationFrame(animateBeam);
        };
        animateBeam();
    }

    function updateGroundLoot(delta) {
        if (!characterGroup) return;

        groundLoot.forEach(loot => {
            // Floating animation
            loot.mesh.userData.floatTime += delta * 2;
            loot.mesh.position.y = loot.mesh.userData.startY + Math.sin(loot.mesh.userData.floatTime) * 0.1;

            // Rotation
            loot.mesh.rotation.y += delta * 1.5;
        });

        // Check nearest loot
        nearestLoot = null;
        let minDist = Infinity;

        groundLoot.forEach(loot => {
            const dist = characterGroup.position.distanceTo(loot.mesh.position);
            if (dist < 3 && dist < minDist) { // Within 3 units
                minDist = dist;
                nearestLoot = loot;
            }
        });

        // Show pickup prompt
        if (nearestLoot) {
            showLootPickupPrompt(nearestLoot);
        } else {
            hideLootPickupPrompt();
        }
    }

    let lootPickupPromptUI = null;

    function showLootPickupPrompt(loot) {
        if (!lootPickupPromptUI) {
            lootPickupPromptUI = document.createElement('div');
            lootPickupPromptUI.style.cssText = `
                position: fixed;
                bottom: 100px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.9);
                border: 2px solid #ffd700;
                border-radius: 10px;
                padding: 10px 20px;
                color: white;
                font-family: monospace;
                font-size: 14px;
                font-weight: bold;
                z-index: 1000;
                display: none;
            `;
            document.body.appendChild(lootPickupPromptUI);
        }

        const itemData = COMBAT_SYSTEM.inventorySystem.itemDatabase[loot.itemId];
        const text = loot.gold > 0 ? `💰 ${loot.gold}g` : `${itemData.icon} ${itemData.name}`;

        lootPickupPromptUI.innerHTML = `E - Pick up ${text}`;
        lootPickupPromptUI.style.display = 'block';
    }

    function hideLootPickupPrompt() {
        if (lootPickupPromptUI) {
            lootPickupPromptUI.style.display = 'none';
        }
    }

    function pickupLoot() {
        if (!nearestLoot || !COMBAT_SYSTEM.inventorySystem) return false;

        const loot = nearestLoot;

        // Add to inventory
        if (loot.gold > 0) {
            COMBAT_SYSTEM.inventorySystem.gold += loot.gold;
            if (typeof notify === 'function') {
                notify(`💰 +${loot.gold}g`, 'success');
            }
            console.log(`💰 Picked up ${loot.gold}g`);
        } else {
            const success = COMBAT_SYSTEM.inventorySystem.addItem(loot.itemId, 1);
            if (success) {
                const itemData = COMBAT_SYSTEM.inventorySystem.itemDatabase[loot.itemId];
                if (typeof notify === 'function') {
                    notify(`${itemData.icon} ${itemData.name}`, 'success');
                }
                console.log(`💎 Picked up ${itemData.name}`);
            } else {
                if (typeof notify === 'function') {
                    notify('⚠️ Inventory full!', 'error');
                }
                return false;
            }
        }

        // Remove from scene
        scene.remove(loot.mesh);

        // Remove from array
        const index = groundLoot.indexOf(loot);
        if (index > -1) {
            groundLoot.splice(index, 1);
        }

        nearestLoot = null;
        hideLootPickupPrompt();

        return true;
    }

    // Hook into dungeon_enemies onEnemyKilled
    window.onEnemyKilled = function(xp, loot, position) {
        console.log(`💀 Enemy defeated! +${xp} XP, Loot:`, loot);

        if (typeof notify === 'function') {
            notify(`+${xp} XP | ${loot.length} items`, 'success');
        }

        // Spawn loot items on ground
        if (loot && loot.length > 0 && position) {
            const pos = new THREE.Vector3(position.x, position.y, position.z);

            loot.forEach((itemId, index) => {
                // Spread items in circle
                const angle = (index / loot.length) * Math.PI * 2;
                const offset = new THREE.Vector3(
                    Math.cos(angle) * 1.5,
                    0,
                    Math.sin(angle) * 1.5
                );

                spawnLootItem(itemId, pos.clone().add(offset));
            });
        }

        // TODO: Add XP to player level system
    };

    function checkNearBuilding() {
        if (!characterGroup || !roomGroup) {
            nearBuilding = null;
            hideBuildingPrompt();
            return;
        }

        let closestBuilding = null;
        let minDist = Infinity;

        roomGroup.traverse(obj => {
            if (obj.userData && obj.userData.buildingName && obj.userData.buildingRadius) {
                const dist = Math.sqrt(
                    Math.pow(characterGroup.position.x - obj.position.x, 2) +
                    Math.pow(characterGroup.position.z - obj.position.z, 2)
                );

                if (dist < obj.userData.buildingRadius + 30 && dist < minDist) {
                    closestBuilding = obj;
                    minDist = dist;
                }
            }
        });

        if (closestBuilding) {
            nearBuilding = closestBuilding;
            showBuildingPrompt(closestBuilding);
        } else {
            nearBuilding = null;
            hideBuildingPrompt();
        }
    }

    // 🏠 BUILDING INTERIOR SYSTEM
    let currentInterior = null;
    window.currentInterior = null; // Expose to other modules (garden.js)
    let exteriorPosition = null;
    let roomConfigs = null;

    // Load room configs from JSON
    async function loadRoomConfigs() {
        if (roomConfigs) return roomConfigs;
        try {
            const response = await fetch('/digivice/config/room_config_detailed.json');
            roomConfigs = await response.json();
            console.log('✅ Room configs loaded:', roomConfigs.rooms.length, 'rooms');
            return roomConfigs;
        } catch (err) {
            console.error('❌ Failed to load room configs:', err);
            return null;
        }
    }

    function enterBuilding() {
        if (!nearBuilding) return false;

        const buildingName = nearBuilding.userData.buildingName;
        console.log(`🚪 Betrete Gebäude: ${buildingName}`);

        if (typeof notify === 'function') {
            notify(`🚪 ${buildingName} betreten!`, 'info');
        }

        // Speichere Position draußen
        exteriorPosition = {
            x: characterGroup.position.x,
            y: characterGroup.position.y,
            z: characterGroup.position.z
        };

        // Lade Interior
        loadBuildingInterior(buildingName);
        return true;
    }

    // Schwarze Mühle Stockwerke
    let currentFloor = 0;
    const muehleFloors = [
        {
            name: 'Erdgeschoss',
            rooms: [
                { name: 'Wohnzimmer', position: [0, 0, 0] },
                { name: 'Küche', position: [60, 0, 0] },
                { name: 'Badezimmer', position: [-60, 0, 0] }
            ]
        },
        { name: 'Obergeschoss', rooms: [{ name: 'Schlafzimmer', position: [0, 0, 0] }] },
        { name: 'Turm', rooms: [{ name: 'Terminal', position: [0, 0, 0] }] },
        { name: 'Keller', rooms: [{ name: 'Studieren & Crafting', position: [0, 0, 0] }] }
    ];

    async function loadBuildingInterior(buildingName) {
        // Lade Room Configs
        const configs = await loadRoomConfigs();
        if (!configs) {
            console.error('❌ No room configs available');
            return;
        }

        // Entferne Open World
        if (roomGroup) {
            scene.remove(roomGroup);
        }

        currentInterior = buildingName;
        window.currentInterior = buildingName; // Sync to window

        // Schwarze Mühle hat mehrere Stockwerke
        if (buildingName === 'Schwarze Mühle') {
            currentFloor = 0; // Start im Erdgeschoss
            await loadMuehleFloor(currentFloor);
            showFloorSwitchUI();
            showExitBuildingPrompt();
            return;
        }

        // Check if this is a dungeon - start combat instead of loading room
        const dungeonMappings = {
            'Dungeon des Schattens': { level: 1, name: 'Dungeon des Schattens' },
            'Dungeon der Explosion': { level: 5, name: 'Dungeon der Explosion' },
            'Dungeon des Chaos': { level: 10, name: 'Dungeon des Chaos' }
        };

        if (dungeonMappings[buildingName]) {
            const dungeon = dungeonMappings[buildingName];
            console.log(`🏰 Starting dungeon combat: ${dungeon.name} Level ${dungeon.level}`);

            // Start dungeon combat system
            if (window.DungeonCombat && typeof window.DungeonCombat.startDungeonCombat === 'function') {
                window.DungeonCombat.startDungeonCombat(dungeon.level, scene, dungeon.name);
                if (typeof notify === 'function') {
                    notify(`⚔️ ${dungeon.name} gestartet!`, 'warning');
                }
            } else {
                console.error('❌ DungeonCombat system not available');
            }
            return;
        }

        // Mapping: Gebäude → Raum (für nicht-Dungeons)
        const buildingToRoom = {
            'Kampfarena': 'Kampfarena',
            'Garten': 'Garten'
        };

        const roomName = buildingToRoom[buildingName] || 'Wohnzimmer';
        let roomConfig = configs.rooms.find(r => r.name === roomName);

        if (!roomConfig) {
            console.error(`❌ Room config not found for: ${roomName}`);
            return;
        }

        console.log(`🏠 Loading interior: ${roomName}`);

        // Baue Raum aus Config
        await buildRoomFromConfig(roomConfig);

        // Zeige Exit-Button
        showExitBuildingPrompt();

        // Load room actions
        if (typeof window.renderActions === 'function') {
            console.log(`🎯 Loading actions for room: ${roomName}`);
            try {
                await window.renderActions(roomName);
            } catch (error) {
                console.warn('Failed to load room actions:', error);
            }
        }
    }

    async function loadMuehleFloor(floorIndex) {
        const configs = await loadRoomConfigs();
        const floor = muehleFloors[floorIndex];

        console.log(`🏠 Loading Mühle ${floor.name}`);

        // Entferne alten Raum
        if (roomGroup) {
            scene.remove(roomGroup);
        }

        // Clear interactive objects when switching floors
        interactiveObjects.length = 0;
        currentInteractable = null;
        hideInteractionPrompt();

        // Erstelle neue Gruppe für alle Räume auf dieser Etage
        const floorGroup = new THREE.Group();

        // Lade alle Räume auf dieser Etage
        for (const roomDef of floor.rooms) {
            let roomConfig = configs.rooms.find(r => r.name === roomDef.name);

            if (!roomConfig) {
                console.error(`❌ Room config not found: ${roomDef.name}`);
                continue;
            }

            // Clone config und setze span auf 48 (Wohnzimmer-Größe)
            roomConfig = JSON.parse(JSON.stringify(roomConfig));
            roomConfig.floor.span = 48;
            if (roomConfig.walls) roomConfig.walls.span = 48;
            roomConfig.wallHeight = 6;

            console.log(`  📐 Building room: ${roomDef.name} at position`, roomDef.position);

            // Baue Raum in eigener Gruppe
            const roomSubGroup = new THREE.Group();
            roomSubGroup.position.set(...roomDef.position);

            // Lade Floor
            if (roomConfig.floor && roomConfig.floor.model) {
                await loadRoomFloor(roomSubGroup, roomConfig.floor, 48);
            }

            // Lade Walls
            if (roomConfig.walls && roomConfig.walls.model) {
                await loadRoomWalls(roomSubGroup, roomConfig.walls, 48, 6);
            }

            // Lade Props (mit korrigierter Position relativ zum Raum)
            if (roomConfig.props && roomConfig.props.length > 0) {
                for (const prop of roomConfig.props) {
                    // Clone prop config und addiere roomDef.position
                    const propCopy = JSON.parse(JSON.stringify(prop));
                    propCopy.position = [
                        propCopy.position[0] + roomDef.position[0],
                        propCopy.position[1] + roomDef.position[1],
                        propCopy.position[2] + roomDef.position[2]
                    ];
                    await loadRoomProp(floorGroup, propCopy);
                }
            }

            // Füge Raum zur Etage hinzu
            floorGroup.add(roomSubGroup);
        }

        // Verwende Palette vom ersten Raum
        const firstRoomConfig = configs.rooms.find(r => r.name === floor.rooms[0].name);
        if (firstRoomConfig && firstRoomConfig.palette) {
            applyRoomPalette(firstRoomConfig.palette);
        }

        // Spawn Position im Zentrum
        resetCharacterPosition([0, 0, 0]);

        roomGroup = floorGroup;
        scene.add(roomGroup);

        console.log(`✅ Floor loaded: ${floor.name} with ${floor.rooms.length} room(s)`);

        // Update Floor UI
        updateFloorSwitchUI();

        // Update Exit Prompt (zeigt Terminal-Hinweis im Turm)
        showExitBuildingPrompt();

        // Load room actions for the first room on this floor
        if (floor.rooms && floor.rooms.length > 0 && typeof window.renderActions === 'function') {
            const firstRoomName = floor.rooms[0].name;
            console.log(`🎯 Loading actions for room: ${firstRoomName}`);
            try {
                await window.renderActions(firstRoomName);
            } catch (error) {
                console.warn('Failed to load room actions:', error);
            }
        }
    }

    function exitBuilding() {
        if (!currentInterior) return;

        console.log(`🚪 Verlasse Gebäude: ${currentInterior}`);

        // Entferne Interior
        if (roomGroup) {
            scene.remove(roomGroup);
        }

        // Hide Floor UI if in Mühle
        hideFloorSwitchUI();

        // Clear interactive objects
        interactiveObjects.length = 0;
        currentInteractable = null;
        hideInteractionPrompt();

        currentInterior = null;
        window.currentInterior = null; // Sync to window
        currentFloor = 0;

        // Lade Open World zurück
        buildRoom();

        // Restore Position draußen
        if (exteriorPosition) {
            characterGroup.position.set(
                exteriorPosition.x,
                exteriorPosition.y,
                exteriorPosition.z
            );
        }

        hideExitBuildingPrompt();
    }

    // === BUILD ROOM FROM CONFIG ===

    async function buildRoomFromConfig(roomConfig) {
        const group = new THREE.Group();
        const span = roomConfig.floor.span || 48;
        const wallHeight = roomConfig.wallHeight || 6;
        const defaults = roomConfigs.defaults || {};

        console.log(`📐 Building room: ${roomConfig.name} (span: ${span}, wallHeight: ${wallHeight})`);

        // 1. BODEN (Floor)
        if (roomConfig.floor && roomConfig.floor.model) {
            await loadRoomFloor(group, roomConfig.floor, span);
        }

        // 2. WÄNDE (Walls)
        if (roomConfig.walls && roomConfig.walls.model) {
            await loadRoomWalls(group, roomConfig.walls, span, wallHeight);
        }

        // 3. PROPS (Möbel, Dekoration)
        if (roomConfig.props && roomConfig.props.length > 0) {
            for (const prop of roomConfig.props) {
                await loadRoomProp(group, prop);
            }
        }

        // 4. PALETTE (Farben, Beleuchtung)
        if (roomConfig.palette) {
            applyRoomPalette(roomConfig.palette);
        }

        // 5. SPAWN POSITION
        const spawnPos = roomConfig.spawn || [0, 0, span * 0.3];
        resetCharacterPosition(spawnPos);

        roomGroup = group;
        scene.add(roomGroup);

        console.log(`✅ Room built: ${roomConfig.name}`);
    }

    async function loadRoomFloor(group, floorConfig, span) {
        if (!THREE.GLTFLoader) {
            console.warn('GLTFLoader not available');
            return;
        }

        const loader = new THREE.GLTFLoader();
        return new Promise((resolve) => {
            loader.load(
                `/assets/${floorConfig.model}`,
                (gltf) => {
                    const instance = gltf.scene;

                    // ORIGINAL METHODE: Skaliere auf volle Größe (EIN STÜCK!)
                    const box = new THREE.Box3().setFromObject(instance);
                    const size = new THREE.Vector3();
                    box.getSize(size);
                    const max = Math.max(size.x, size.z);
                    if (max && isFinite(max)) {
                        const factor = span / max;
                        instance.scale.multiplyScalar(factor);
                    }

                    // Mache EXTREM flach (nur 5% Höhe)
                    instance.scale.y *= 0.05;

                    // Positioniere korrekt
                    const floorBox = new THREE.Box3().setFromObject(instance);
                    const floorHeight = floorBox.max.y - floorBox.min.y;
                    instance.position.y = -floorBox.min.y - floorHeight;

                    // Tint & Material
                    instance.traverse(node => {
                        if (node.isMesh) {
                            node.receiveShadow = true;
                            node.castShadow = true;
                            if (floorConfig.tint) {
                                if (node.material) {
                                    node.material = node.material.clone();
                                    node.material.color.setStyle(floorConfig.tint);
                                    node.material.roughness = floorConfig.roughness || 0.8;
                                    node.material.metalness = floorConfig.metalness || 0.1;
                                }
                            }
                        }
                    });

                    group.add(instance);
                    resolve();
                },
                undefined,
                (error) => {
                    console.error('Error loading floor:', error);
                    resolve();
                }
            );
        });
    }

    async function loadRoomWalls(group, wallConfig, span, wallHeight) {
        if (!THREE.GLTFLoader) return;

        const loader = new THREE.GLTFLoader();
        const halfSpan = span / 2;

        // Lade BASE Wand-Model nur EINMAL
        return new Promise((resolve) => {
            loader.load(
                `/assets/${wallConfig.model}`,
                (gltf) => {
                    const base = gltf.scene;

                    // ORIGINAL METHODE: Skaliere auf span-Breite (EIN STÜCK pro Wand!)
                    const box = new THREE.Box3().setFromObject(base);
                    const size = new THREE.Vector3();
                    box.getSize(size);
                    const axisSize = size.x;
                    if (axisSize && isFinite(axisSize)) {
                        const factor = span / axisSize;
                        base.scale.x *= factor;
                    }

                    const wallGroup = new THREE.Group();

                    // Nord-Wand
                    const north = base.clone(true);
                    north.position.set(0, 0, -halfSpan);
                    wallGroup.add(north);

                    // Süd-Wand
                    const south = base.clone(true);
                    south.rotation.y = Math.PI;
                    south.position.set(0, 0, halfSpan);
                    wallGroup.add(south);

                    // Ost-Wand
                    const east = base.clone(true);
                    east.rotation.y = -Math.PI / 2;
                    east.position.set(halfSpan, 0, 0);
                    wallGroup.add(east);

                    // West-Wand
                    const west = base.clone(true);
                    west.rotation.y = Math.PI / 2;
                    west.position.set(-halfSpan, 0, 0);
                    wallGroup.add(west);

                    // Shadows & Tint
                    wallGroup.traverse(node => {
                        if (node.isMesh) {
                            node.castShadow = true;
                            node.receiveShadow = true;
                            if (wallConfig.tint && node.material) {
                                node.material = node.material.clone();
                                node.material.color.setStyle(wallConfig.tint);
                            }
                        }
                    });

                    // Skaliere Höhe
                    const wallBox = new THREE.Box3().setFromObject(wallGroup);
                    const wallSize = new THREE.Vector3();
                    wallBox.getSize(wallSize);
                    const currentHeight = wallSize.y;
                    const scaleFactor = wallHeight / Math.max(currentHeight, 0.0001);
                    wallGroup.scale.y *= scaleFactor;

                    // Positioniere mit UNTERSEITE auf Y=0
                    const finalBox = new THREE.Box3().setFromObject(wallGroup);
                    wallGroup.position.y = -finalBox.min.y;

                    group.add(wallGroup);
                    resolve();
                },
                undefined,
                (error) => {
                    console.error('Error loading walls:', error);
                    resolve();
                }
            );
        });
    }

    // Interactive Objects System
    const interactiveObjects = [];
    let currentInteractable = null;
    let interactionPromptUI = null;

    async function loadRoomProp(group, propConfig) {
        if (!THREE.GLTFLoader) return;

        const loader = new THREE.GLTFLoader();
        return new Promise((resolve) => {
            loader.load(
                `/assets/${propConfig.model}`,
                (gltf) => {
                    const prop = gltf.scene;
                    prop.position.set(...propConfig.position);
                    if (propConfig.rotation) {
                        prop.rotation.set(...propConfig.rotation);
                    }
                    if (propConfig.scale) {
                        const scale = propConfig.scale;
                        prop.scale.set(scale, scale, scale);
                    }
                    prop.traverse(node => {
                        if (node.isMesh) {
                            node.castShadow = true;
                            node.receiveShadow = true;
                        }
                    });

                    // Register as interactive object if it has an interaction type
                    if (propConfig.interaction) {
                        const interactObj = {
                            mesh: prop,
                            position: new THREE.Vector3(...propConfig.position),
                            type: propConfig.interaction,
                            radius: propConfig.interactionRadius || 4
                        };
                        interactiveObjects.push(interactObj);
                        console.log('✅ Registered interactive object:', propConfig.interaction, 'at', propConfig.position);
                    }

                    group.add(prop);
                    resolve();
                },
                undefined,
                (error) => {
                    console.error('Error loading prop:', error);
                    resolve();
                }
            );
        });
    }

    function checkInteractables() {
        if (!characterGroup) return;

        const charPos = new THREE.Vector3();
        characterGroup.getWorldPosition(charPos);

        let closest = null;
        let closestDist = Infinity;

        for (const obj of interactiveObjects) {
            const dist = charPos.distanceTo(obj.position);
            if (dist < obj.radius && dist < closestDist) {
                closest = obj;
                closestDist = dist;
            }
        }

        if (closest !== currentInteractable) {
            currentInteractable = closest;
            if (closest) {
                showInteractionPrompt(closest.type);
            } else {
                hideInteractionPrompt();
            }
        }
    }

    function showInteractionPrompt(interactionType) {
        if (!interactionPromptUI) {
            interactionPromptUI = document.createElement('div');
            interactionPromptUI.id = 'interaction-prompt-ui';
            interactionPromptUI.style.cssText = `
                position: fixed;
                bottom: 140px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.9);
                border: 2px solid #50c878;
                border-radius: 10px;
                padding: 15px 25px;
                color: white;
                font-family: monospace;
                font-size: 16px;
                z-index: 1500;
                text-align: center;
            `;
            document.body.appendChild(interactionPromptUI);
        }

        const prompts = {
            'bed': '🛏️ Drücke [E] zum Schlafen',
            'stove': '🍳 Drücke [E] zum Kochen',
            'shower': '🚿 Drücke [E] zum Duschen',
            'toilet': '🚽 Drücke [E] für Toilette',
            'sink': '🚰 Drücke [E] zum Waschen',
            'table': '🪑 Drücke [E] zum Essen'
        };

        interactionPromptUI.innerHTML = prompts[interactionType] || `✨ Drücke [E] für ${interactionType}`;
        interactionPromptUI.style.display = 'block';
    }

    function hideInteractionPrompt() {
        if (interactionPromptUI) {
            interactionPromptUI.style.display = 'none';
        }
    }

    function handleInteraction() {
        if (!currentInteractable) return;

        const type = currentInteractable.type;
        console.log('🎮 Interacting with:', type);

        switch (type) {
            case 'bed':
                handleBedInteraction();
                break;
            case 'stove':
                handleStoveInteraction();
                break;
            case 'shower':
                handleShowerInteraction();
                break;
            case 'toilet':
                handleToiletInteraction();
                break;
            case 'sink':
                handleSinkInteraction();
                break;
            case 'table':
                handleTableInteraction();
                break;
            default:
                console.log('⚠️ No handler for interaction type:', type);
        }
    }

    async function handleBedInteraction() {
        console.log('💤 Najika geht schlafen...');
        showFloatingMessage('💤 Najika schläft und regeneriert Energie...', '#7a8bff');

        try {
            const response = await fetch('/api/najika/sleep', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log('✅ Sleep API response:', data);

            // Refresh Najika status display
            if (typeof window.fetchNajikaStatus === 'function') {
                window.fetchNajikaStatus();
            }
        } catch (error) {
            console.error('❌ Sleep API error:', error);
        }
    }

    async function handleStoveInteraction() {
        console.log('🍳 Najika kocht Essen...');
        showFloatingMessage('🍳 Najika bereitet eine Mahlzeit zu...', '#ffb74d');

        try {
            const response = await fetch('/api/najika/feed', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log('✅ Feed API response:', data);

            if (typeof window.refreshNajikaStatus === 'function') {
                window.refreshNajikaStatus();
            }
        } catch (error) {
            console.error('❌ Feed API error:', error);
        }
    }

    async function handleShowerInteraction() {
        console.log('🚿 Najika duscht...');
        showFloatingMessage('🚿 Najika wird sauber und erfrischt...', '#8be6ff');

        try {
            const response = await fetch('/api/najika/wash', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log('✅ Wash API response:', data);

            if (typeof window.refreshNajikaStatus === 'function') {
                window.refreshNajikaStatus();
            }
        } catch (error) {
            console.error('❌ Wash API error:', error);
        }
    }

    async function handleToiletInteraction() {
        console.log('🚽 Najika benutzt die Toilette...');
        showFloatingMessage('🚽 Najika fühlt sich erleichtert...', '#c7f3f7');

        // Toilet increases happiness slightly
        try {
            const response = await fetch('/api/najika/wash', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log('✅ Toilet API response:', data);

            if (typeof window.refreshNajikaStatus === 'function') {
                window.refreshNajikaStatus();
            }
        } catch (error) {
            console.error('❌ Toilet API error:', error);
        }
    }

    async function handleSinkInteraction() {
        console.log('🚰 Najika wäscht sich...');
        showFloatingMessage('🚰 Najika wäscht die Hände...', '#81d4fa');

        try {
            const response = await fetch('/api/najika/wash', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log('✅ Wash API response:', data);

            if (typeof window.refreshNajikaStatus === 'function') {
                window.refreshNajikaStatus();
            }
        } catch (error) {
            console.error('❌ Wash API error:', error);
        }
    }

    async function handleTableInteraction() {
        console.log('🪑 Najika setzt sich zum Essen...');
        showFloatingMessage('🪑 Najika isst am Tisch...', '#ff9b71');

        try {
            const response = await fetch('/api/najika/feed', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log('✅ Feed API response:', data);

            if (typeof window.refreshNajikaStatus === 'function') {
                window.refreshNajikaStatus();
            }
        } catch (error) {
            console.error('❌ Feed API error:', error);
        }
    }

    function showFloatingMessage(text, color) {
        const msg = document.createElement('div');
        msg.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.95);
            border: 3px solid ${color};
            border-radius: 15px;
            padding: 25px 40px;
            color: ${color};
            font-family: monospace;
            font-size: 20px;
            font-weight: bold;
            z-index: 2000;
            text-align: center;
            animation: fadeInOut 2s ease-in-out;
        `;
        msg.textContent = text;
        document.body.appendChild(msg);

        setTimeout(() => {
            document.body.removeChild(msg);
        }, 2000);
    }

    function applyRoomPalette(palette) {
        const bg = parseInt(palette.background.replace('#', ''), 16);
        const fg = parseInt(palette.fog.replace('#', ''), 16);
        applyPalette({
            background: bg,
            fog: fg,
            ambient: palette.ambient,
            primary: parseInt(palette.primary.replace('#', ''), 16),
            secondary: parseInt(palette.secondary.replace('#', ''), 16),
            floor: parseInt(palette.floor.replace('#', ''), 16)
        });
    }

    // Exit Building Prompt
    let exitBuildingPromptUI = null;

    function showExitBuildingPrompt() {
        if (!exitBuildingPromptUI) {
            exitBuildingPromptUI = document.createElement('div');
            exitBuildingPromptUI.id = 'exit-building-prompt-ui';
            exitBuildingPromptUI.style.cssText = `
                position: fixed;
                bottom: 100px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.9);
                border: 2px solid #ff6b9d;
                border-radius: 10px;
                padding: 15px 25px;
                color: white;
                font-family: monospace;
                font-size: 16px;
                z-index: 1500;
                text-align: center;
            `;
            document.body.appendChild(exitBuildingPromptUI);
        }

        // Check if we're in Terminal room (Turm, Floor 2)
        if (currentInterior === 'Schwarze Mühle' && currentFloor === 2) {
            exitBuildingPromptUI.innerHTML = `
                🚪 Drücke [Q] um Gebäude zu verlassen<br>
                💻 Drücke [T] um Terminal zu öffnen
            `;
        } else {
            exitBuildingPromptUI.innerHTML = `
                🚪 Drücke [Q] um Gebäude zu verlassen
            `;
        }

        exitBuildingPromptUI.style.display = 'block';
    }

    function hideExitBuildingPrompt() {
        if (exitBuildingPromptUI) {
            exitBuildingPromptUI.style.display = 'none';
        }
    }

    // Floor Switch UI (Schwarze Mühle Stockwerke)
    let floorSwitchUI = null;

    function showFloorSwitchUI() {
        if (!floorSwitchUI) {
            floorSwitchUI = document.createElement('div');
            floorSwitchUI.id = 'floor-switch-ui';
            floorSwitchUI.style.cssText = `
                position: fixed;
                top: 20px;
                right: 250px;
                background: rgba(0,0,0,0.9);
                border: 2px solid #ff9b71;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-family: monospace;
                font-size: 14px;
                z-index: 1000;
                min-width: 200px;
            `;
            floorSwitchUI.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 10px; text-align: center;">
                    🏰 Schwarze Mühle
                </div>
                <div id="floor-buttons" style="display: flex; flex-direction: column; gap: 8px;">
                    ${muehleFloors.map((floor, index) => `
                        <button
                            id="floor-btn-${index}"
                            onclick="window.switchToFloor(${index})"
                            style="
                                padding: 8px;
                                background: ${index === 0 ? '#ff9b71' : '#444'};
                                color: white;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                font-family: monospace;
                                font-size: 13px;
                            "
                        >${floor.name}</button>
                    `).join('')}
                </div>
                <div style="margin-top: 10px; font-size: 11px; color: #aaa; text-align: center;">
                    [1-4] Schnellwahl
                </div>
            `;
            document.body.appendChild(floorSwitchUI);

            // Global function for onclick
            window.switchToFloor = (index) => {
                currentFloor = index;
                loadMuehleFloor(currentFloor);
            };

            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (currentInterior === 'Schwarze Mühle') {
                    if (e.code === 'Digit1' || e.code === 'Numpad1') window.switchToFloor(0);
                    if (e.code === 'Digit2' || e.code === 'Numpad2') window.switchToFloor(1);
                    if (e.code === 'Digit3' || e.code === 'Numpad3') window.switchToFloor(2);
                    if (e.code === 'Digit4' || e.code === 'Numpad4') window.switchToFloor(3);
                }
            });
        }
        floorSwitchUI.style.display = 'block';
        updateFloorSwitchUI();
    }

    function updateFloorSwitchUI() {
        if (!floorSwitchUI) return;
        muehleFloors.forEach((floor, index) => {
            const btn = document.getElementById(`floor-btn-${index}`);
            if (btn) {
                btn.style.background = index === currentFloor ? '#ff9b71' : '#444';
            }
        });
    }

    function hideFloorSwitchUI() {
        if (floorSwitchUI) {
            floorSwitchUI.style.display = 'none';
        }
    }

    function setupLights() {
        ambientLight = new THREE.AmbientLight(DEFAULT_PALETTE.dir, DEFAULT_PALETTE.ambient);
        scene.add(ambientLight);

        dirLight = new THREE.DirectionalLight(DEFAULT_PALETTE.dir, DEFAULT_PALETTE.dirIntensity);
        dirLight.position.set(12, 25, 12);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 2048;
        dirLight.shadow.mapSize.height = 2048;
        dirLight.shadow.camera.near = 0.1;
        dirLight.shadow.camera.far = 120;
        scene.add(dirLight);

        pointLight1 = new THREE.PointLight(DEFAULT_PALETTE.primary, 1.1, 80);
        pointLight1.position.set(-14, 6, -14);
        scene.add(pointLight1);

        pointLight2 = new THREE.PointLight(DEFAULT_PALETTE.secondary, 1.1, 80);
        pointLight2.position.set(14, 6, 14);
        scene.add(pointLight2);
    }

    function setupFallbackRoom() {
        const floorGeometry = new THREE.PlaneGeometry(120, 120);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: DEFAULT_PALETTE.floor,
            roughness: 0.85,
            metalness: 0.1
        });
        baseFloor = new THREE.Mesh(floorGeometry, floorMaterial);
        baseFloor.rotation.x = -Math.PI / 2;
        baseFloor.receiveShadow = true;
        scene.add(baseFloor);

        gridHelper = new THREE.GridHelper(120, 60, DEFAULT_PALETTE.secondary, 0x1d1d30);
        gridHelper.material.opacity = 0.25;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);

        const wallMaterial = new THREE.MeshStandardMaterial({
            color: 0x36364a,
            roughness: 0.7,
            metalness: 0.2
        });
        const wallThickness = 1;
        const wallHeight = FALLBACK_DEFAULTS.wallHeight;
        const wallSpan = FALLBACK_DEFAULTS.span;
        const positions = [
            { pos: [0, wallHeight / 2, -wallSpan], size: [wallSpan * 2, wallHeight, wallThickness] },
            { pos: [0, wallHeight / 2, wallSpan], size: [wallSpan * 2, wallHeight, wallThickness] },
            { pos: [-wallSpan, wallHeight / 2, 0], size: [wallThickness, wallHeight, wallSpan * 2] },
            { pos: [wallSpan, wallHeight / 2, 0], size: [wallThickness, wallHeight, wallSpan * 2] }
        ];
        positions.forEach(info => {
            const wall = new THREE.Mesh(new THREE.BoxGeometry(...info.size), wallMaterial);
            wall.position.set(info.pos[0], info.pos[1], info.pos[2]);
            wall.castShadow = true;
            wall.receiveShadow = true;
            scene.add(wall);
            fallbackWalls.push(wall);
        });
    }

    function installEventHandlers() {
        window.addEventListener('resize', onWindowResize, false);
        window.addEventListener('keydown', onKeyDown, false);
        window.addEventListener('keyup', onKeyUp, false);

        const canvas = renderer.domElement;
        orbitCanvas = canvas;
        canvas.style.touchAction = 'none';
        canvas.addEventListener('pointerdown', onPointerDown, { passive: false });
        canvas.addEventListener('pointermove', onPointerMove, { passive: false });
        canvas.addEventListener('pointerup', onPointerUp, { passive: false });
        canvas.addEventListener('pointerleave', onPointerUp, { passive: false });
        canvas.addEventListener('pointercancel', onPointerUp, { passive: false });
        canvas.addEventListener('wheel', onWheel, { passive: false });
    }

    function ensureKayKitLoader() {
        // 🌍 OPEN WORLD MODE - KayKit Loader deaktiviert
        // Wir brauchen keine room configs mehr, nur Character Model
        if (!window.KayKitLoader) {
            return;
        }
        // NICHT mehr auf configReady warten - würde Open World überschreiben!
        // document.addEventListener('kaykit:configReady', scheduleRoomBuild, false);
        document.addEventListener('kaykit:modelLoaded', onKayKitModelLoaded, false);
        // KayKit init() lädt room_config_detailed.json - überspringen!
        // if (typeof KayKitLoader.init === 'function') {
        //     KayKitLoader.init();
        // }
    }

    function startAnimationLoop() {
        const loop = () => {
            animationHandle = requestAnimationFrame(loop);
            const delta = clock ? clock.getDelta() : 0.016;
            updateCharacter(delta);
            updateCamera(delta);
            // ⚔️ Update Combat System (Stamina regeneration, combos)
            COMBAT_SYSTEM.update(delta);
            updateCombatStatsUI();
            updateSkillHotbarUI();

            // 💎 Update Ground Loot System
            updateGroundLoot(delta);

            // 🎯 Auto-Targeting: Finde nächsten Gegner wenn keiner ausgewählt (nur wenn Lock-On aktiv!)
            if (COMBAT_SYSTEM.targetLockOn && !COMBAT_SYSTEM.currentTarget && characterGroup && window.DungeonEnemies) {
                const nearestEnemy = findNearestEnemy();
                if (nearestEnemy && nearestEnemy.distance < 15) {
                    COMBAT_SYSTEM.currentTarget = nearestEnemy.enemy;
                    console.log(`🎯 Auto-Target: ${nearestEnemy.enemy.userData.enemyId} (${Math.round(nearestEnemy.distance)}m)`);
                }
            }

            // 🎯 Target verloren wenn zu weit weg oder tot
            if (COMBAT_SYSTEM.currentTarget) {
                if (COMBAT_SYSTEM.targetDistance > 20) {
                    console.log('🎯 Target zu weit weg - verloren');
                    COMBAT_SYSTEM.currentTarget = null;
                }
                // Prüfe ob Target noch existiert
                if (COMBAT_SYSTEM.currentTarget.userData && COMBAT_SYSTEM.currentTarget.userData.isDead) {
                    console.log('🎯 Target eliminated - suche neues');
                    COMBAT_SYSTEM.currentTarget = null;
                }
            }
            // 🎣 Update Fishing System
            if (typeof window.FishingSystem !== 'undefined') {
                FishingSystem.updateFishing(delta);
                // Check if player near fishing spot
                if (characterGroup && !FishingSystem.isFishing) {
                    const spot = FishingSystem.checkNearSpot(characterGroup.position);
                    // Show UI prompt when near spot (later)
                }
            }
            // 🌱 Update Garden System
            if (typeof window.GardenSystem !== 'undefined') {
                GardenSystem.updateGarden(delta);
                // Check if player near plot
                if (characterGroup) {
                    const plot = GardenSystem.getNearestPlot(characterGroup.position);
                    if (plot) {
                        GardenSystem.setSelectedPlot(plot);
                        GardenSystem.showGardenUI();
                        GardenSystem.updateGardenUI();
                    } else {
                        GardenSystem.setSelectedPlot(null);
                        GardenSystem.hideGardenUI();
                    }
                }
            }

            // 🏠 Update Housing System
            if (typeof window.HousingSystem !== 'undefined' && characterGroup) {
                HousingSystem.updateHousing(delta, characterGroup.position);
                // Check if player near house
                const nearHouse = HousingSystem.checkNearHouse(characterGroup.position);
                // Show UI prompt when near house (later)
            }

            // 🌾 Update Farming System
            if (typeof window.FarmingSystem !== 'undefined' && characterGroup) {
                FarmingSystem.updateFarming(delta, characterGroup.position);
                // Proximity check and UI updates handled inside updateFarming
            }

            // 🌍 Update World Manager (Streaming, LOD, Weather, Day/Night)
            if (worldManager && characterGroup) {
                worldManager.update(delta, characterGroup.position);
            }

            // 🚪 Check Building Proximity (works in both modes)
            if (!currentInterior) {
                checkNearBuilding();
            }
            // ✨ Check Interactive Objects
            checkInteractables();
            // Only rebuild room if not in an interior
            if (pendingRoomBuild && !useWorldManager && !currentInterior) {
                buildRoom();
            }
            // Update Dungeon Combat (enemies & combat logic)
            if (typeof window.DungeonCombat !== 'undefined' && DungeonCombat.isActive()) {
                DungeonCombat.updateCombat();
            }
            renderer.render(scene, camera);
        };
        loop();
    }

    function onWindowResize() {
        const container = getContainer();
        if (!container || !camera || !renderer) {
            return;
        }
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function onKeyDown(event) {
        activeKeys.add(event.code);

        // 🎯 Tab: Lock-On Toggle (Skyrim/Fortnite Style)
        if (event.code === 'Tab') {
            event.preventDefault(); // Verhindere Browser-Tab-Switch
            COMBAT_SYSTEM.toggleLockOn();
            return;
        }

        // 🪄 SKILL HOTBAR (1-9 für Skills/Zauber)
        if (event.code === 'Digit1') { COMBAT_SYSTEM.castSkill(0); return; }
        if (event.code === 'Digit2') { COMBAT_SYSTEM.castSkill(1); return; }
        if (event.code === 'Digit3') { COMBAT_SYSTEM.castSkill(2); return; }
        if (event.code === 'Digit4') { COMBAT_SYSTEM.castSkill(3); return; }
        if (event.code === 'Digit5') { COMBAT_SYSTEM.castSkill(4); return; }
        if (event.code === 'Digit6') { COMBAT_SYSTEM.castSkill(5); return; }
        if (event.code === 'Digit7') { COMBAT_SYSTEM.castSkill(6); return; }
        if (event.code === 'Digit8') { COMBAT_SYSTEM.castSkill(7); return; }
        if (event.code === 'Digit9') { COMBAT_SYSTEM.castSkill(8); return; }

        // 🎒 I-Taste: Inventory Toggle
        if (event.code === 'KeyI') {
            toggleInventoryUI();
            return;
        }

        // F-Taste: Najika dreht sich zum Spieler
        if (event.code === 'KeyF') {
            faceCharacter();
        }

        // 🚪 E-Taste: Loot Pickup, Interaktion, oder Gebäude betreten
        if (event.code === 'KeyE') {
            // Priorität 1: Loot Pickup
            if (nearestLoot) {
                pickupLoot();
                return;
            }
            // Priorität 2: Interaktion mit Objekten (wenn drinnen)
            if (currentInterior && currentInteractable) {
                handleInteraction();
                return;
            }
            // Priorität 3: Gebäude betreten
            if (nearBuilding && !currentInterior) {
                enterBuilding();
                return;
            }
        }

        // ⚔️ KAMPF-TASTEN (Light/Heavy System)
        // J: Linke Hand Light/Heavy (kein Stagger bei miss!)
        if (event.code === 'KeyJ') {
            if (event.shiftKey) {
                // Shift+J = Heavy Attack Links
                const result = COMBAT_SYSTEM.attackLeftHeavy();
                if (result && result.hit) {
                    console.log('💥 Linke Hand HEAVY! ' + Math.round(result.damage) + ' Schaden');
                } else if (result && !result.hit) {
                    console.log('❌ Linke Hand Heavy verfehlt');
                }
            } else {
                // J = Light Attack Links
                const result = COMBAT_SYSTEM.attackLeftLight();
                if (result && result.hit) {
                    console.log(`🔮 Linke Hand LIGHT! ${Math.round(result.damage)} Schaden`);
                } else if (result && !result.hit) {
                    console.log('❌ Linke Hand Light verfehlt');
                }
            }
        }

        // K: Rechte Hand Light/Heavy (kein Stagger bei miss!)
        if (event.code === 'KeyK') {
            if (event.shiftKey) {
                // Shift+K = Heavy Attack Rechts
                const result = COMBAT_SYSTEM.attackRightHeavy();
                if (result && result.hit) {
                    console.log('💥 Rechte Hand HEAVY! ' + Math.round(result.damage) + ' Schaden');
                } else if (result && !result.hit) {
                    console.log('❌ Rechte Hand Heavy verfehlt');
                }
            } else {
                // K = Light Attack Rechts
                const result = COMBAT_SYSTEM.attackRightLight();
                if (result && result.hit) {
                    console.log(`⚔️ Rechte Hand LIGHT! ${result.damage} Schaden`);
                } else if (result && !result.hit) {
                    console.log('❌ Verfehlt! TAUMELN!');
                }
            }
        }

        // B: Beide Hände gleichzeitig (riskanter Mix-Angriff!)
        if (event.code === 'KeyB') {
            const leftType = event.shiftKey ? 'heavy' : 'light';
            const rightType = event.shiftKey ? 'heavy' : 'light';
            const result = COMBAT_SYSTEM.attackBoth(leftType, rightType);
            if (result && result.hit) {
                console.log(`💫 BEIDE HÄNDE! ${result.damage} Schaden!`);
            } else if (result && !result.hit) {
                console.log('❌ Mix-Angriff VERFEHLT! Schweres Taumeln!');
            }
        }
        // Q: Exit Building ODER Parry
        if (event.code === 'KeyQ') {
            // Wenn im Gebäude, verlasse es
            if (currentInterior) {
                exitBuilding();
                return;
            }
            // Ansonsten: Parry
            if (COMBAT_SYSTEM.parry()) {
                console.log('🛡️ PARRY bereit!');
            }
        }
        // Space: Dodge Roll (Ausweichen mit i-frames)
        if (event.code === 'Space') {
            if (COMBAT_SYSTEM.dodge()) {
                console.log('🌀 DODGE ROLL!');
                // Ausweichen in Bewegungsrichtung
                if (characterGroup) {
                    const rollDistance = 15;
                    const moveX = Math.sin(characterHeading) * rollDistance;
                    const moveZ = Math.cos(characterHeading) * rollDistance;
                    characterGroup.position.x += moveX;
                    characterGroup.position.z += moveZ;
                    clampCharacterToRoom(characterGroup.position);
                }
            }
        }
        // T-Taste: Terminal öffnen (nur im Terminal-Raum = Turm = Floor 2)
        if (event.code === 'KeyT') {
            if (currentInterior === 'Schwarze Mühle' && currentFloor === 2) {
                console.log('💻 Terminal wird geöffnet...');
                if (window.CodeEditor && typeof window.CodeEditor.open === 'function') {
                    window.CodeEditor.open();
                } else {
                    console.error('❌ CodeEditor nicht geladen!');
                }
            }
        }
    }

    function onKeyUp(event) {
        activeKeys.delete(event.code);
    }

    function onPointerDown(event) {
        if (!orbitCanvas) {
            return;
        }
        event.preventDefault();

        // FIX: Blur ANY focused input element to enable WASD controls
        // This prevents inputs from chat, terminal modules, etc. from stealing keyboard events
        if (document.activeElement && (
            document.activeElement.tagName === 'INPUT' ||
            document.activeElement.tagName === 'TEXTAREA' ||
            document.activeElement.tagName === 'SELECT'
        )) {
            document.activeElement.blur();
        }

        activePointers.set(event.pointerId, { x: event.clientX, y: event.clientY });

        if (activePointers.size === 1) {
            // Single touch/click: Rotate
            pointerMode = 'rotate';
            dragStartPos = { x: event.clientX, y: event.clientY };
            dragStartYaw = orbitYaw;
            dragStartPitch = orbitPitch;
        } else if (activePointers.size === 2 && cameraMode === CAMERA_MODES.ORBIT) {
            // Two touches: Pinch to zoom (nur in Orbit)
            pointerMode = 'pinch';
            pinchStartDist = computePointerDistance();
            pinchBaseDistance = orbitDistance;
        }
    }

    function onPointerMove(event) {
        if (!activePointers.has(event.pointerId)) {
            return;
        }
        activePointers.set(event.pointerId, { x: event.clientX, y: event.clientY });

        if (pointerMode === 'pinch' && activePointers.size === 2 && cameraMode === CAMERA_MODES.ORBIT) {
            const dist = computePointerDistance();
            if (pinchStartDist > 0) {
                const ratio = dist / pinchStartDist;
                if (ratio > 0) {
                    orbitDistance = clamp(pinchBaseDistance / ratio, ORBIT_MIN_DIST, ORBIT_MAX_DIST);
                }
            }
        } else if (pointerMode === 'rotate' && activePointers.size === 1) {
            const dx = event.clientX - dragStartPos.x;
            const dy = event.clientY - dragStartPos.y;
            orbitYaw = dragStartYaw - dx * 0.005;
            orbitPitch = clamp(dragStartPitch - dy * 0.003, ORBIT_MIN_PITCH, ORBIT_MAX_PITCH);
        }
    }

    function onPointerUp(event) {
        activePointers.delete(event.pointerId);
        if (activePointers.size === 0) {
            pointerMode = null;
        } else if (activePointers.size === 1 && pointerMode === 'pinch') {
            // Switched from pinch back to rotate
            pointerMode = 'rotate';
            const remaining = Array.from(activePointers.values())[0];
            dragStartPos = { x: remaining.x, y: remaining.y };
            dragStartYaw = orbitYaw;
            dragStartPitch = orbitPitch;
        }
    }

    function onWheel(event) {
        if (cameraMode !== CAMERA_MODES.ORBIT) {
            return;
        }
        event.preventDefault();
        const delta = Math.sign(event.deltaY) * 1.5;
        orbitDistance = clamp(orbitDistance + delta, ORBIT_MIN_DIST, ORBIT_MAX_DIST);
    }

    function computePointerDistance() {
        const ptrs = Array.from(activePointers.values());
        if (ptrs.length < 2) return 0;
        const dx = ptrs[0].x - ptrs[1].x;
        const dy = ptrs[0].y - ptrs[1].y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    function onKayKitModelLoaded(event) {
        const modelName = event && event.detail && event.detail.name;
        if (!characterReady && modelName && modelName.includes('wand')) {
            attachStaffToCharacter();
        }
        scheduleRoomBuild();
    }

    function scheduleRoomBuild() {
        pendingRoomBuild = true;
    }

    function buildRoom() {
        pendingRoomBuild = false;

        if (roomGroup) {
            scene.remove(roomGroup);
            disposeHierarchy(roomGroup);
            roomGroup = null;
        }

        // 🌍 OPEN WORLD MODE - Großer Raum statt einzelner Room
        const OPEN_WORLD_SIZE = 2400;
        usingFallbackRoom = false;
        showFallbackRoom(false);
        currentRoomSpan = OPEN_WORLD_SIZE;

        const group = new THREE.Group();

        // 🌍 BUILD OPEN WORLD FLOOR (große grüne Fläche)
        const floorGeo = new THREE.PlaneGeometry(OPEN_WORLD_SIZE, OPEN_WORLD_SIZE, 100, 100);
        const floorMat = new THREE.MeshStandardMaterial({
            color: 0x3f7a2c, // Grasgrün
            roughness: 0.95,
            metalness: 0.0
        });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        group.add(floor);

        // 🏠 BUILD GEBÄUDE (6 Stück mit GLTF-Modellen)
        const buildings = [
            {
                name: 'Schwarze Mühle',
                pos: [0, 0, 0],
                model: 'KayKit_Platformer_Pack_1.0_FREE/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf/neutral/structure_C.gltf',
                scale: 12.0,
                radius: 80
            },
            {
                name: 'Kampfarena',
                pos: [-600, 0, -600],
                model: 'KayKit_Platformer_Pack_1.0_FREE/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf/red/arch_tall_red.gltf',
                scale: 10.0,
                radius: 50
            },
            {
                name: 'Garten',
                pos: [600, 0, 600],
                model: 'KayKit_Platformer_Pack_1.0_FREE/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf/neutral/structure_A.gltf',
                scale: 5.0,
                radius: 60
            },
            {
                name: 'Dungeon des Schattens',
                pos: [-720, 0, -720],
                model: 'KayKit_Platformer_Pack_1.0_FREE/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf/blue/arch_tall_blue.gltf',
                scale: 6.0,
                radius: 70
            },
            {
                name: 'Dungeon der Explosion',
                pos: [720, 0, -720],
                model: 'KayKit_Platformer_Pack_1.0_FREE/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf/green/arch_tall_green.gltf',
                scale: 6.0,
                radius: 70
            },
            {
                name: 'Dungeon des Chaos',
                pos: [0, 0, 720],
                model: 'KayKit_Platformer_Pack_1.0_FREE/KayKit_Platformer_Pack_1.0_FREE/Assets/gltf/yellow/arch_tall_yellow.gltf',
                scale: 6.0,
                radius: 70
            }
        ];

        // 🏗️ CUSTOM BUILDINGS - Baue echte Gebäude aus THREE.js Primitives

        // Schwarze Mühle (Position [0,0,0])
        if (window.CustomBuildings) {
            window.CustomBuildings.buildWindmill([0, 0, 0], 1.0, group);
        }

        // Kampfarena (Position [-600,0,-600])
        if (window.CustomBuildings) {
            window.CustomBuildings.buildArena([-600, 0, -600], 0.8, group);
        }

        // Garten-Haus (Position [600,0,600])
        if (window.CustomBuildings) {
            window.CustomBuildings.buildHouse([600, 0, 600], 0.6, 0x90EE90, 'Gartenhaus', 60, group);
        }

        // Dungeons als kleine dunkle Häuser
        if (window.CustomBuildings) {
            window.CustomBuildings.buildHouse([-720, 0, -720], 0.7, 0x4169E1, 'Dungeon 1', 70, group);
            window.CustomBuildings.buildHouse([720, 0, -720], 0.7, 0x228B22, 'Dungeon 2', 70, group);
            window.CustomBuildings.buildHouse([0, 0, 720], 0.7, 0xFFD700, 'Dungeon 3', 70, group);
        }

        // 🌱 9 GARTEN-BEETE (3x3 Grid nahe Garten-Gebäude bei [600,0,600])
        const gardenPlots = [
            { id: 1, position: [550, 0, 550], size: 20 },
            { id: 2, position: [600, 0, 550], size: 20 },
            { id: 3, position: [650, 0, 550], size: 20 },
            { id: 4, position: [550, 0, 600], size: 20 },
            { id: 5, position: [600, 0, 600], size: 20 },
            { id: 6, position: [650, 0, 600], size: 20 },
            { id: 7, position: [550, 0, 650], size: 20 },
            { id: 8, position: [600, 0, 650], size: 20 },
            { id: 9, position: [650, 0, 650], size: 20 }
        ];

        gardenPlots.forEach(plot => {
            // Boden (braune Erde)
            const plotGeo = new THREE.BoxGeometry(plot.size, 2, plot.size);
            const plotMat = new THREE.MeshStandardMaterial({
                color: 0x8B4513,  // Braune Erde
                roughness: 0.9
            });
            const plotMesh = new THREE.Mesh(plotGeo, plotMat);
            plotMesh.position.set(plot.position[0], 1, plot.position[2]);
            plotMesh.castShadow = true;
            plotMesh.receiveShadow = true;
            plotMesh.userData.gardenPlotId = plot.id;
            group.add(plotMesh);

            // Holz-Rahmen um das Beet
            const frameThickness = 1;
            const frameHeight = 3;
            const frameMat = new THREE.MeshStandardMaterial({
                color: 0x654321,  // Dunkleres Holz
                roughness: 0.8
            });

            // 4 Seiten des Rahmens
            const frameSides = [
                { pos: [0, 0, -plot.size/2], rot: 0, w: plot.size + 2, d: frameThickness },
                { pos: [0, 0, plot.size/2], rot: 0, w: plot.size + 2, d: frameThickness },
                { pos: [-plot.size/2, 0, 0], rot: Math.PI/2, w: plot.size, d: frameThickness },
                { pos: [plot.size/2, 0, 0], rot: Math.PI/2, w: plot.size, d: frameThickness }
            ];

            frameSides.forEach(side => {
                const frameGeo = new THREE.BoxGeometry(side.w, frameHeight, side.d);
                const frame = new THREE.Mesh(frameGeo, frameMat);
                frame.position.set(
                    plot.position[0] + side.pos[0],
                    frameHeight/2,
                    plot.position[2] + side.pos[2]
                );
                frame.rotation.y = side.rot;
                frame.castShadow = true;
                frame.receiveShadow = true;
                group.add(frame);
            });
        });

        // 🎣 WASSER-PLANES für Fishing Spots
        const fishingSpots = [
            { name: 'Kristallteich', position: [800, 0, 800], radius: 100 },
            { name: 'Weltensee', position: [-800, 0, -800], radius: 150 }  // Weg von der Mühle!
        ];

        fishingSpots.forEach(spot => {
            // Wasser-Circle
            const waterGeo = new THREE.CircleGeometry(spot.radius, 64);
            const waterMat = new THREE.MeshStandardMaterial({
                color: 0x0077be,  // Schönes Blau
                transparent: true,
                opacity: 0.7,
                roughness: 0.1,
                metalness: 0.3,
                side: THREE.DoubleSide
            });
            const water = new THREE.Mesh(waterGeo, waterMat);
            water.rotation.x = -Math.PI / 2;  // Horizontal legen
            water.position.set(spot.position[0], 0.5, spot.position[2]);  // Leicht über Boden
            water.receiveShadow = true;
            water.userData.fishingSpot = spot.name;
            group.add(water);

            // Reflektions-Effekt (zweite Layer leicht höher)
            const reflectionGeo = new THREE.CircleGeometry(spot.radius * 0.95, 64);
            const reflectionMat = new THREE.MeshStandardMaterial({
                color: 0x4da6ff,  // Helleres Blau
                transparent: true,
                opacity: 0.3,
                roughness: 0.05,
                metalness: 0.5,
                side: THREE.DoubleSide
            });
            const reflection = new THREE.Mesh(reflectionGeo, reflectionMat);
            reflection.rotation.x = -Math.PI / 2;
            reflection.position.set(spot.position[0], 0.6, spot.position[2]);
            group.add(reflection);
        });

        roomGroup = group;
        scene.add(roomGroup);

        // Palette für Open World (blauer Himmel)
        applyPalette({ background: 0x87CEEB, fog: 0xb5d8e0, ambient: 0.6 });

        // Character spawnt in Mitte
        resetCharacterPosition([0, 0, 0]);
    }


    function loadBuildingModel(building, parentGroup) {
        if (!THREE.GLTFLoader) {
            console.warn('GLTFLoader not available, using fallback cube');
            // Fallback: Cube
            const geo = new THREE.BoxGeometry(building.radius, 50, building.radius);
            const mat = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
            const mesh = new THREE.Mesh(geo, mat);
            mesh.position.set(building.pos[0], 25, building.pos[2]);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            mesh.userData.buildingName = building.name;
            mesh.userData.buildingRadius = building.radius;
            parentGroup.add(mesh);
            return;
        }

        const loader = new THREE.GLTFLoader();
        loader.load(
            `/assets/${building.model}`,
            gltf => {
                const model = gltf.scene;
                model.traverse(node => {
                    if (node.isMesh) {
                        node.castShadow = true;
                        node.receiveShadow = true;
                    }
                });

                // Scale model
                model.scale.set(building.scale, building.scale, building.scale);

                // Position mit Füßen auf Boden
                const box = new THREE.Box3().setFromObject(model);
                const offsetY = box.min.y;
                model.position.set(building.pos[0], -offsetY, building.pos[2]);

                model.userData.buildingName = building.name;
                model.userData.buildingRadius = building.radius;

                parentGroup.add(model);
                console.log(`✅ Gebäude geladen: ${building.name}`);
            },
            undefined,
            error => {
                console.warn(`Failed to load building ${building.name}:`, error);
                // Fallback cube
                const geo = new THREE.BoxGeometry(building.radius, 50, building.radius);
                const mat = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
                const mesh = new THREE.Mesh(geo, mat);
                mesh.position.set(building.pos[0], 25, building.pos[2]);
                mesh.castShadow = true;
                mesh.receiveShadow = true;
                mesh.userData.buildingName = building.name;
                mesh.userData.buildingRadius = building.radius;
                parentGroup.add(mesh);
            }
        );
    }

    function showFallbackRoom(visible) {
        if (baseFloor) baseFloor.visible = visible;
        if (gridHelper) gridHelper.visible = visible;
        fallbackWalls.forEach(w => (w.visible = visible));
    }

    function getRoomConfig(name) {
        if (!name || !window.KayKitLoader || typeof KayKitLoader.getRoomConfig !== 'function') {
            return null;
        }
        try {
            return KayKitLoader.getRoomConfig(name);
        } catch (error) {
            console.warn('Scene3D: failed to read room config', error);
            return null;
        }
    }

    function getKayKitDefaults() {
        if (!window.KayKitLoader || typeof KayKitLoader.getConfig !== 'function') {
            return { ...FALLBACK_DEFAULTS };
        }
        const cfg = KayKitLoader.getConfig();
        if (!cfg || !cfg.defaults) {
            return { ...FALLBACK_DEFAULTS };
        }
        return { ...FALLBACK_DEFAULTS, ...cfg.defaults };
    }

    function resolveSpan(config) {
        if (typeof config.span === 'number') {
            return config.span;
        }
        if (config.floor && typeof config.floor.span === 'number') {
            return config.floor.span;
        }
        if (config.walls && typeof config.walls.span === 'number') {
            return config.walls.span;
        }
        const defaults = getKayKitDefaults();
        return defaults.span;
    }

    function resolveWallHeight(config) {
        if (config.walls && typeof config.walls.height === 'number') {
            return config.walls.height;
        }
        if (typeof config.wallHeight === 'number') {
            return config.wallHeight;
        }
        const defaults = getKayKitDefaults();
        return defaults.wallHeight;
    }

    function roomAssetsAvailable(config) {
        if (!window.KayKitLoader) {
            return false;
        }
        const required = new Set();
        if (config.floor && config.floor.model) required.add(config.floor.model);
        if (config.walls && config.walls.model) required.add(config.walls.model);
        if (Array.isArray(config.props)) {
            config.props.forEach(prop => {
                if (prop && prop.model) required.add(prop.model);
            });
        }
        for (const name of required) {
            if (!KayKitLoader.hasModel || !KayKitLoader.hasModel(name)) {
                return false;
            }
        }
        return true;
    }

    function buildFloor(entry, span) {
        const instance = makeModelInstance(entry);
        if (!instance) return null;
        // Skaliere Boden auf volle span-Größe
        scaleUniformToSpan(instance, span);
        // Mache Boden EXTREM flach (nur 5% Höhe) wie eine dünne Platte
        instance.scale.y *= 0.05;
        // Berechne BoundingBox um Boden korrekt zu positionieren
        const box = new THREE.Box3().setFromObject(instance);
        const floorHeight = box.max.y - box.min.y;
        // Positioniere so dass OBERSEITE bei Y=0 ist (Unterseite darunter)
        instance.position.y = -box.min.y - floorHeight;
        applyEntryTransform(instance, entry);
        return instance;
    }

    function buildWalls(entry, span, wallHeight) {
        const base = makeModelInstance(entry);
        if (!base) return null;

        // Skaliere Wand-Modell auf die volle span-Breite
        scaleAxisToSpan(base, 'x', span);

        const group = new THREE.Group();
        // Wände am RAND des Bodens positionieren (span / 2)
        const half = span / 2;

        const north = cloneGroup(base);
        north.position.set(0, 0, -half);
        group.add(north);

        const south = cloneGroup(base);
        south.rotation.y = Math.PI;
        south.position.set(0, 0, half);
        group.add(south);

        const east = cloneGroup(base);
        east.rotation.y = -Math.PI / 2;
        east.position.set(half, 0, 0);
        group.add(east);

        const west = cloneGroup(base);
        west.rotation.y = Math.PI / 2;
        west.position.set(-half, 0, 0);
        group.add(west);

        group.traverse(node => {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });

        // Skaliere Wand-Höhe auf gewünschte wallHeight
        const currentHeight = getBoundingSize(group).y;
        const scaleFactor = wallHeight / Math.max(currentHeight, 0.0001);
        group.scale.y *= scaleFactor;

        // WICHTIG: Wände mit UNTERSEITE auf Y=0 (Boden-Oberseite)
        const box = new THREE.Box3().setFromObject(group);
        group.position.y = -box.min.y;

        applyEntryTransform(group, entry);
        return group;
    }

    function buildProp(entry) {
        const instance = makeModelInstance(entry);
        if (!instance) return null;
        adjustToGround(instance);
        applyEntryTransform(instance, entry);
        return instance;
    }

    function makeModelInstance(entry) {
        if (!entry || !entry.model || !window.KayKitLoader) return null;
        if (!KayKitLoader.hasModel || !KayKitLoader.hasModel(entry.model)) return null;
        const source = KayKitLoader.getModel(entry.model);
        if (!source) return null;
        const wrapper = new THREE.Group();
        const clone = cloneObject(source);
        wrapper.add(clone);
        applyTint(wrapper, entry.tint);
        wrapper.traverse(node => {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        return wrapper;
    }

    function cloneObject(object) {
        if (THREE.SkeletonUtils && typeof THREE.SkeletonUtils.clone === 'function') {
            return THREE.SkeletonUtils.clone(object);
        }
        return object.clone(true);
    }

    function cloneGroup(group) {
        const copy = group.clone(true);
        copy.traverse(node => {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        return copy;
    }

    function scaleUniformToSpan(group, span) {
        const size = getBoundingSize(group);
        const max = Math.max(size.x, size.z);
        if (!max || !isFinite(max)) return;
        const factor = span / max;
        group.scale.multiplyScalar(factor);
    }

    function scaleAxisToSpan(group, axis, span) {
        const size = getBoundingSize(group);
        const axisSize = axis === 'z' ? size.z : size.x;
        if (!axisSize || !isFinite(axisSize)) return;
        const factor = span / axisSize;
        if (axis === 'z') {
            group.scale.z *= factor;
        } else {
            group.scale.x *= factor;
        }
    }

    function getBoundingSize(group) {
        const box = new THREE.Box3().setFromObject(group);
        const size = new THREE.Vector3();
        box.getSize(size);
        return size;
    }

    function adjustToGround(group) {
        const box = new THREE.Box3().setFromObject(group);
        const offsetY = box.min.y;
        group.position.y -= offsetY;
    }

    function applyTint(group, tint) {
        const hex = parseColor(tint);
        if (hex === null) return;
        group.traverse(node => {
            if (node.isMesh) {
                const material = node.material;
                if (Array.isArray(material)) {
                    material.forEach(mat => mat && mat.color && mat.color.set(hex));
                } else if (material && material.color) {
                    material.color.set(hex);
                }
            }
        });
    }

    function applyEntryTransform(group, entry) {
        if (!entry) return;

        if (typeof entry.scale === 'number') {
            group.scale.multiplyScalar(entry.scale);
        } else if (Array.isArray(entry.scale)) {
            const [sx = 1, sy = 1, sz = 1] = entry.scale;
            group.scale.x *= sx;
            group.scale.y *= sy;
            group.scale.z *= sz;
        }

        if (Array.isArray(entry.rotation)) {
            const [rx = 0, ry = 0, rz = 0] = entry.rotation;
            group.rotation.set(rx, ry, rz);
        }

        if (Array.isArray(entry.position)) {
            const [px = 0, py = 0, pz = 0] = entry.position;
            // Nur X und Z setzen, Y wird durch adjustToGround() bestimmt
            group.position.x += px;
            group.position.z += pz;
            // Y-Offset wird NACH adjustToGround angewendet
            if (py !== 0) {
                group.position.y += py;
            }
        }

        // adjustToGround wurde bereits vorher aufgerufen, nicht nochmal!
        // adjustToGround(group);
    }

    function parseColor(value) {
        if (typeof value === 'number') return value;
        if (typeof value === 'string') {
            try {
                return new THREE.Color(value).getHex();
            } catch (error) {
                return null;
            }
        }
        return null;
    }

    function applyPalette(roomPalette) {
        const paletteSource = privateModeActive
            ? PRIVATE_PALETTE
            : roomPalette
            ? { ...DEFAULT_PALETTE, ...roomPalette }
            : DEFAULT_PALETTE;

        const palette = { ...DEFAULT_PALETTE };
        Object.keys(paletteSource).forEach(key => {
            const value = paletteSource[key];
            palette[key] = typeof value === 'string' ? parseColor(value) || palette[key] : value;
        });

        scene.background = new THREE.Color(palette.background);
        if (!scene.fog) {
            scene.fog = new THREE.Fog(palette.fog, 12, 160);
        } else {
            scene.fog.color.setHex(palette.fog);
        }

        ambientLight.color.setHex(palette.dir);
        ambientLight.intensity = palette.ambient;

        dirLight.color.setHex(palette.dir);
        dirLight.intensity = palette.dirIntensity;

        pointLight1.color.setHex(palette.primary);
        pointLight2.color.setHex(palette.secondary);

        if (baseFloor && usingFallbackRoom) {
            baseFloor.material.color.setHex(palette.floor);
        }
    }

    function resetCharacterPosition(spawn) {
        if (!characterGroup) return;
        const [x = 0, y = 0, z = 0] = Array.isArray(spawn) ? spawn : [0, 0, 0];
        characterGroup.position.set(x, y, z);
        clampCharacterToRoom(characterGroup.position);
    }

    function loadCharacter() {
        if (!THREE.GLTFLoader) {
            console.warn('Scene3D: GLTFLoader missing; cannot load character.');
            return;
        }
        const loader = new THREE.GLTFLoader();
        loader.load(
            '/assets/KayKit_Skeletons_1.0_FREE/characters/gltf/Skeleton_Mage.glb',
            gltf => {
                characterGroup = gltf.scene;
                characterGroup.traverse(node => {
                    if (node.isMesh) {
                        node.castShadow = true;
                        node.receiveShadow = true;
                    }
                });
                adjustToGround(characterGroup);

                // Set starting position based on world mode
                if (useWorldManager) {
                    // Open World: Start at Götterfels (Schwarze Mühle)
                    characterGroup.position.set(4800, 0, 4800);
                    console.log('🌍 Character spawned in Open World at Götterfels (4800, 4800)');
                } else {
                    // Old system: Default position
                    characterGroup.position.set(0, 0, 0);
                }

                scene.add(characterGroup);
                attachStaffToCharacter();
                characterReady = true;
                console.log('✅ Skeleton_Mage geladen');

                // Update WorldManager if active
                if (useWorldManager && worldManager) {
                    worldManager.setPlayerPosition(characterGroup.position);
                }
            },
            undefined,
            error => {
                console.warn('Scene3D: failed to load Mage model', error);
            }
        );
    }

    // loadAnimationsForCharacter ENTFERNT - wird nicht gebraucht

    function attachStaffToCharacter() {
        if (!characterGroup || !window.KayKitLoader || !KayKitLoader.getModel) {
            return;
        }
        if (characterGroup.getObjectByName('najika_staff')) {
            return;
        }
        const wandModel = KayKitLoader.getModel(
            'KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Assets/gltf/wand.gltf'
        );
        if (!wandModel) {
            return;
        }
        const wand = cloneObject(wandModel);
        wand.name = 'najika_staff';
        adjustToGround(wand);
        wand.scale.multiplyScalar(1.3);
        wand.rotation.set(0, Math.PI / 2, Math.PI / 8);
        wand.position.set(0.4, 1.1, -0.2);
        characterGroup.add(wand);
    }

    function updateCharacter(delta) {
        // 🎬 Update Animation Mixer
        if (!characterGroup) return;

        // Input relativ zum Spieler (lokal)
        let forward = 0;
        let right = 0;

        // Third & Orbit: W/S vertauscht | First: A/D vertauscht
        if (cameraMode === CAMERA_MODES.FIRST) {
            // FIRST: A/D vertauscht
            if (activeKeys.has('KeyW') || activeKeys.has('ArrowUp')) forward += 1;
            if (activeKeys.has('KeyS') || activeKeys.has('ArrowDown')) forward -= 1;
            if (activeKeys.has('KeyA') || activeKeys.has('ArrowLeft')) right += 1;  // VERTAUSCHT
            if (activeKeys.has('KeyD') || activeKeys.has('ArrowRight')) right -= 1;  // VERTAUSCHT
        } else {
            // THIRD & ORBIT: W/S vertauscht
            if (activeKeys.has('KeyW') || activeKeys.has('ArrowUp')) forward -= 1;  // VERTAUSCHT
            if (activeKeys.has('KeyS') || activeKeys.has('ArrowDown')) forward += 1;  // VERTAUSCHT
            if (activeKeys.has('KeyA') || activeKeys.has('ArrowLeft')) right -= 1;
            if (activeKeys.has('KeyD') || activeKeys.has('ArrowRight')) right += 1;
        }

        if (forward !== 0 || right !== 0) {
            // FORTNITE-Style: WASD relativ zur KAMERA (orbitYaw)
            const inputAngle = Math.atan2(right, forward);
            const worldAngle = orbitYaw + inputAngle;

            // Bewegungsvektor in Weltkoordinaten
            const moveX = Math.sin(worldAngle);
            const moveZ = Math.cos(worldAngle);

            const speed = CHARACTER_SPEED * (cameraMode === CAMERA_MODES.FIRST ? 0.9 : 1);
            characterGroup.position.x += moveX * speed * delta;
            characterGroup.position.z += moveZ * speed * delta;
            clampCharacterToRoom(characterGroup.position);

            // Charakter dreht sich in Bewegungsrichtung
            characterHeading = worldAngle;
            characterGroup.rotation.y = characterHeading;
        }

        // 🎬 Spiele passende Animation basierend auf Input
    }

    function clampCharacterToRoom(position) {
        // Disable clamping in Schwarze Mühle (multi-room building with rooms at different positions)
        if (currentInterior === 'Schwarze Mühle') {
            return; // No clamping - allow free movement between rooms
        }

        // Disable clamping in Open World (allow free movement across entire world)
        if (!currentInterior && currentRoomSpan >= 2000) {
            return; // No clamping in large open world
        }

        // Disable clamping if using WorldManager (even if currentRoomSpan not yet set)
        if (useWorldManager && !currentInterior) {
            return; // WorldManager handles bounds
        }

        const limit = Math.max(8, currentRoomSpan / 2 - CLAMP_PADDING);
        position.x = clamp(position.x, -limit, limit);
        position.z = clamp(position.z, -limit, limit);
    }

    function getCameraTarget() {
        if (characterGroup) {
            return characterGroup.position.clone().add(new THREE.Vector3(0, CHARACTER_HEIGHT * 0.85, 0));
        }
        return new THREE.Vector3(0, 0, 0);
    }

    function updateCamera(delta) {
        if (!camera) return;

        const target = getCameraTarget();
        const cosPitch = Math.cos(orbitPitch);
        const sinPitch = Math.sin(orbitPitch);
        const cosYaw = Math.cos(orbitYaw);
        const sinYaw = Math.sin(orbitYaw);

        if (cameraMode === CAMERA_MODES.ORBIT || !characterGroup) {
            // ORBIT Mode: Freie Kamera-Steuerung
            const offset = new THREE.Vector3(
                sinYaw * cosPitch,
                sinPitch,
                cosYaw * cosPitch
            ).multiplyScalar(orbitDistance);
            camera.position.copy(target).add(offset);
            camera.lookAt(target);
        } else if (cameraMode === CAMERA_MODES.THIRD) {
            // THIRD: Kamera wie Orbit, nur näher (Fortnite-Style: Maus steuert Kamera)
            const distance = 12;
            const height = 4;
            const offset = new THREE.Vector3(
                sinYaw * cosPitch * distance,
                height + sinPitch * distance * 0.5,
                cosYaw * cosPitch * distance
            );
            camera.position.copy(target).add(offset);
            camera.lookAt(target);
        } else if (cameraMode === CAMERA_MODES.FIRST) {
            // FIRST: Kamera DIREKT am Kopf (Augen), Blickrichtung = orbitYaw/Pitch
            const eyeHeight = CHARACTER_HEIGHT * 0.85;

            // Kamera DIREKT am Kopf (keine Offset-Berechnung nötig)
            camera.position.set(
                characterGroup.position.x,
                characterGroup.position.y + eyeHeight,
                characterGroup.position.z
            );

            // Blickrichtung folgt MAUS (orbitYaw und orbitPitch)
            const lookDistance = 10;
            const lookTarget = new THREE.Vector3(
                camera.position.x + sinYaw * cosPitch * lookDistance,
                camera.position.y + sinPitch * lookDistance,
                camera.position.z + cosYaw * cosPitch * lookDistance
            );
            camera.lookAt(lookTarget);
        }
    }

    function faceCharacter() {
        if (!characterGroup || !camera) return;
        const dx = camera.position.x - characterGroup.position.x;
        const dz = camera.position.z - characterGroup.position.z;
        characterHeading = Math.atan2(dx, dz);
        characterGroup.rotation.y = characterHeading;
    }

    async function toggleWebcam(videoElement) {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            if (typeof notify === 'function') notify('Webcam wird nicht unterstützt.', 'error');
            return false;
        }
        if (webcamStream) {
            webcamStream.getTracks().forEach(track => track.stop());
            webcamStream = null;
            if (webcamElement) {
                webcamElement.srcObject = null;
            }
            webcamElement = null;
            return false;
        }
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            webcamStream = stream;
            webcamElement = videoElement;
            webcamElement.srcObject = stream;
            await webcamElement.play();
            return true;
        } catch (error) {
            console.warn('Scene3D: webcam access failed', error);
            if (typeof notify === 'function') notify('Webcam konnte nicht gestartet werden.', 'error');
            return false;
        }
    }

    function updateCameraMode(mode) {
        if (!Object.values(CAMERA_MODES).includes(mode)) {
            return;
        }
        cameraMode = mode;
        // Clear pointer state when leaving Orbit mode
        if (cameraMode !== CAMERA_MODES.ORBIT) {
            activePointers.clear();
            pointerMode = null;
        }
        return cameraMode;
    }

    function setPrivateMode(active) {
        privateModeActive = !!active;
        scheduleRoomBuild();
    }

    function getCameraMode() {
        return cameraMode;
    }

    function disposeHierarchy(object) {
        if (!object) return;
        object.traverse(child => {
            if (child.geometry && child.geometry.dispose) {
                child.geometry.dispose();
            }
            if (child.material) {
                if (Array.isArray(child.material)) {
                    child.material.forEach(mat => mat && mat.dispose && mat.dispose());
                } else if (child.material.dispose) {
                    child.material.dispose();
                }
            }
        });
    }

    function clamp(value, min, max) {
        return Math.min(max, Math.max(min, value));
    }

    function bootWhenReady() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    }

    window.Scene3D = {
        init,
        changeRoom(name) {
            if (name) {
                // Exit combat when changing rooms
                if (window.DungeonCombat && typeof DungeonCombat.exitDungeon === 'function') {
                    DungeonCombat.exitDungeon();
                }

                currentRoomName = name;
                if (window.KayKitLoader && typeof KayKitLoader.loadRoomOnDemand === 'function') {
                    KayKitLoader.loadRoomOnDemand(name);
                }
                // Lade Dungeon-Assets wenn Keller betreten wird
                if (name === 'Schwarze Mühle – Keller' && window.DungeonGenerator) {
                    DungeonGenerator.preloadDungeonAssets();
                }
                scheduleRoomBuild();
            }
        },
        setCameraMode: updateCameraMode,
        getCameraMode,
        faceCharacter,
        toggleWebcam,
        setPrivateMode,
        // Export scene for Dungeon Combat
        get scene() { return scene; },
        get characterGroup() { return characterGroup; },
        // ⚔️ Export Combat System
        get combat() { return COMBAT_SYSTEM; },
        get COMBAT_SYSTEM() { return COMBAT_SYSTEM; },
        get camera() { return camera; }
    };

    bootWhenReady();
})();
