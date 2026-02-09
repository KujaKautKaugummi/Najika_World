/**
 * NAJIKA WORLD - CREATURE TAMING SYSTEM
 * ======================================
 * NUR für Kategorie 2 "Vieh" (Minecraft-artige Tiere ohne Verstand)
 *
 * KEIN POKEMON! Kein Pokeball! Kein Fangen!
 * Zähmen = Füttern + Geduld + Zeit
 *
 * Ablauf:
 *   1. Vieh in der Welt finden
 *   2. Richtiges Futter geben (tameFood aus MonsterRegistry)
 *   3. Warten, nicht erschrecken, Geduld zeigen
 *   4. Nach mehreren Fütterungen: Vieh folgt dir
 *   5. Zur Farm bringen → produziert Ressourcen
 *
 * Gezähmtes Vieh ≠ Begleiter!
 *   Begleiter = Slime (alle Spieler) oder Najika (Kuja)
 *   Gezähmtes Vieh = Farmtier, bleibt auf der Farm
 */

(function() {
    'use strict';

    // ==========================================
    // TAMING KONFIGURATION
    // ==========================================

    const TAMING_CONFIG = {
        // Wie viele Fütterungen bis gezähmt
        baseFeedingsRequired: 5,
        // Bonus-Fütterungen für höhere Tier
        feedingsPerTier: 2,
        // Mindest-Wartezeit zwischen Fütterungen (Sekunden Spielzeit)
        feedCooldown: 30,
        // Wie weit darf man sich entfernen bevor Fortschritt verloren geht
        maxDistanceBeforeFlee: 50,
        // Chance dass Vieh flüchtet wenn man zu nah rennt
        fleeChanceOnRun: 0.3,
        // Vertrauens-Verlust wenn man in der Nähe kämpft
        trustLossOnCombat: 0.5,
        // Max Vieh auf der Farm
        maxFarmAnimals: 12,
        // Produktion-Intervall Multiplikator (1.0 = wie in Registry)
        productionMultiplier: 1.0,
    };

    // Farm-Gebäude Typen die Vieh beherbergen
    const FARM_BUILDINGS = {
        stall:    { name: 'Stall',       capacity: 4, types: ['reittier', 'lasttier'] },
        weide:    { name: 'Weide',       capacity: 6, types: ['all'] },
        huehner:  { name: 'Hühnerstall', capacity: 8, types: ['small'] },
        teich:    { name: 'Teich',       capacity: 3, types: ['wasser'] },
    };

    // ==========================================
    // TAMING STATE
    // ==========================================

    // Aktive Zähm-Versuche: { monsterId_instanceId: TamingProgress }
    const activeTaming = {};

    // Gezähmte Tiere auf der Farm: [ FarmAnimal ]
    let farmAnimals = [];

    // ==========================================
    // TAMING PROGRESS
    // ==========================================

    class TamingProgress {
        constructor(monsterId, instanceId, monsterData) {
            this.monsterId = monsterId;
            this.instanceId = instanceId;
            this.monsterData = monsterData;
            this.feedingsGiven = 0;
            this.feedingsRequired = TAMING_CONFIG.baseFeedingsRequired +
                (monsterData.tier || 0) * TAMING_CONFIG.feedingsPerTier;
            this.trust = 0;           // 0-100
            this.lastFeedTime = 0;
            this.startTime = Date.now();
            this.fled = false;
            this.tamed = false;
        }

        get progress() {
            return Math.min(100, Math.floor((this.feedingsGiven / this.feedingsRequired) * 100));
        }

        get key() {
            return `${this.monsterId}_${this.instanceId}`;
        }
    }

    // ==========================================
    // FARM ANIMAL
    // ==========================================

    class FarmAnimal {
        constructor(monsterId, monsterData, nickname) {
            this.id = `farm_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
            this.monsterId = monsterId;
            this.monsterData = monsterData;
            this.nickname = nickname || monsterData.name;
            this.tamedAt = Date.now();
            this.lastProductionTime = Date.now();
            this.happiness = 80;     // 0-100, beeinflusst Produktion
            this.health = 100;       // 0-100
            this.fedToday = false;
            this.building = null;    // Zugewiesenes Gebäude
        }

        get product() {
            return this.monsterData.product || null;
        }

        get productInterval() {
            const interval = this.monsterData.productInterval || 'daily';
            const ms = {
                'daily':   86400000,   // 24h
                '3days':   259200000,  // 72h
                '7days':   604800000,  // 168h
                'passive': 43200000,   // 12h (passive = öfter, weniger)
            };
            return ms[interval] || ms['daily'];
        }
    }

    // ==========================================
    // CORE TAMING FUNCTIONS
    // ==========================================

    /**
     * Beginnt einen Zähm-Versuch mit einem Vieh
     * @param {string} monsterId - ID aus MonsterRegistry
     * @param {string} instanceId - Einzigartige Instanz-ID des Vieh in der Welt
     * @returns {object} Status
     */
    function startTaming(monsterId, instanceId) {
        const registry = window.MonsterRegistry;
        if (!registry) return { success: false, error: 'MonsterRegistry nicht geladen' };

        const monster = registry.getMonster(monsterId);
        if (!monster) return { success: false, error: `Unbekanntes Monster: ${monsterId}` };

        if (monster.category !== 'vieh') {
            return {
                success: false,
                error: `${monster.name} ist kein Vieh! Lebende Kreaturen werden ANGEWORBEN, nicht gezähmt.`,
                hint: 'Nutze creature_recruit.js für Lebende Kreaturen'
            };
        }

        const key = `${monsterId}_${instanceId}`;

        // Bereits in Zähmung?
        if (activeTaming[key] && !activeTaming[key].fled && !activeTaming[key].tamed) {
            return {
                success: true,
                status: 'already_taming',
                progress: activeTaming[key].progress,
                message: `Du zähmst bereits ${monster.name}. Füttere weiter!`
            };
        }

        // Farm voll?
        if (farmAnimals.length >= TAMING_CONFIG.maxFarmAnimals) {
            return {
                success: false,
                error: `Farm ist voll! Max ${TAMING_CONFIG.maxFarmAnimals} Tiere.`,
                hint: 'Baue mehr Gebäude oder lasse ein Tier frei.'
            };
        }

        const tp = new TamingProgress(monsterId, instanceId, monster);
        activeTaming[key] = tp;

        console.log(`🐄 Zähm-Versuch gestartet: ${monster.name} (${tp.feedingsRequired} Fütterungen nötig)`);

        return {
            success: true,
            status: 'started',
            feedingsRequired: tp.feedingsRequired,
            tameFood: monster.tameFood,
            message: `Du näherst dich ${monster.name} vorsichtig. Es braucht ${monster.tameFood} zum Füttern.`
        };
    }

    /**
     * Vieh füttern (Haupt-Zähm-Aktion)
     * @param {string} monsterId
     * @param {string} instanceId
     * @param {string} foodItem - Item das du gibst
     * @returns {object} Ergebnis
     */
    function feedCreature(monsterId, instanceId, foodItem) {
        const key = `${monsterId}_${instanceId}`;
        const tp = activeTaming[key];

        if (!tp) return { success: false, error: 'Kein aktiver Zähm-Versuch. Starte mit startTaming().' };
        if (tp.fled) return { success: false, error: `${tp.monsterData.name} ist geflohen! Suche ein neues.` };
        if (tp.tamed) return { success: false, error: `${tp.monsterData.name} ist bereits gezähmt!` };

        // Richtiges Futter?
        if (foodItem !== tp.monsterData.tameFood) {
            // Falsches Futter = leichter Vertrauensverlust
            tp.trust = Math.max(0, tp.trust - 5);
            return {
                success: false,
                wrongFood: true,
                needed: tp.monsterData.tameFood,
                given: foodItem,
                message: `${tp.monsterData.name} schnüffelt an ${foodItem}... und wendet sich ab. Es will ${tp.monsterData.tameFood}!`
            };
        }

        // Cooldown prüfen
        const now = Date.now();
        const cooldownMs = TAMING_CONFIG.feedCooldown * 1000;
        if (tp.lastFeedTime && (now - tp.lastFeedTime) < cooldownMs) {
            const remaining = Math.ceil((cooldownMs - (now - tp.lastFeedTime)) / 1000);
            return {
                success: false,
                cooldown: true,
                remainingSeconds: remaining,
                message: `${tp.monsterData.name} kaut noch. Warte ${remaining}s.`
            };
        }

        // Fütterung erfolgreich!
        tp.feedingsGiven++;
        tp.lastFeedTime = now;
        tp.trust = Math.min(100, tp.trust + Math.floor(100 / tp.feedingsRequired));

        console.log(`🥕 ${tp.monsterData.name} gefüttert (${tp.feedingsGiven}/${tp.feedingsRequired})`);

        // Gezähmt?
        if (tp.feedingsGiven >= tp.feedingsRequired) {
            return _completeTaming(tp);
        }

        // Fortschritt
        const remaining = tp.feedingsRequired - tp.feedingsGiven;
        const messages = [
            `${tp.monsterData.name} frisst gierig. Noch ${remaining} Fütterungen.`,
            `${tp.monsterData.name} schaut dich neugierig an. Noch ${remaining}x füttern.`,
            `${tp.monsterData.name} kommt etwas näher. Nur noch ${remaining}x!`,
            `${tp.monsterData.name} lässt sich fast berühren... ${remaining}x noch.`,
        ];
        const msgIndex = Math.min(messages.length - 1, Math.floor(tp.progress / 30));

        return {
            success: true,
            status: 'feeding',
            progress: tp.progress,
            feedingsGiven: tp.feedingsGiven,
            feedingsRequired: tp.feedingsRequired,
            trust: tp.trust,
            message: messages[msgIndex],
            consumed: foodItem
        };
    }

    /**
     * Zähmung abschließen → Tier auf die Farm
     */
    function _completeTaming(tp) {
        tp.tamed = true;
        const animal = new FarmAnimal(tp.monsterId, tp.monsterData);
        farmAnimals.push(animal);

        // Aus Inventar entfernen passiert im Aufrufer
        _save();

        console.log(`🎉 ${tp.monsterData.name} gezähmt! Farm: ${farmAnimals.length}/${TAMING_CONFIG.maxFarmAnimals}`);

        if (typeof notify === 'function') {
            notify(`🐄 ${tp.monsterData.name} ist nun dein Farmtier!`, 'success');
        }

        return {
            success: true,
            status: 'tamed',
            farmAnimal: animal,
            farmCount: farmAnimals.length,
            maxFarm: TAMING_CONFIG.maxFarmAnimals,
            message: `${tp.monsterData.name} folgt dir jetzt! Bringe es zur Farm.`,
            product: tp.monsterData.product,
            productInterval: tp.monsterData.productInterval
        };
    }

    /**
     * Spieler rennt nah am Vieh vorbei → Flucht-Check
     */
    function checkFlee(monsterId, instanceId, playerRunning) {
        const key = `${monsterId}_${instanceId}`;
        const tp = activeTaming[key];
        if (!tp || tp.fled || tp.tamed) return { fled: false };

        if (playerRunning && Math.random() < TAMING_CONFIG.fleeChanceOnRun * (1 - tp.trust / 100)) {
            tp.fled = true;
            return {
                fled: true,
                message: `${tp.monsterData.name} erschreckt sich und flüchtet!`
            };
        }

        return { fled: false };
    }

    /**
     * Kampf in der Nähe → Vertrauensverlust
     */
    function onNearbyCombat(monsterId, instanceId) {
        const key = `${monsterId}_${instanceId}`;
        const tp = activeTaming[key];
        if (!tp || tp.fled || tp.tamed) return;

        tp.trust = Math.max(0, tp.trust - TAMING_CONFIG.trustLossOnCombat * 20);
        if (tp.trust <= 0) {
            tp.fled = true;
            console.log(`⚠️ ${tp.monsterData.name} flüchtet wegen Kampf in der Nähe!`);
        }
    }

    // ==========================================
    // FARM MANAGEMENT
    // ==========================================

    /**
     * Farm-Produktion einsammeln
     * @returns {Array} Gesammelte Produkte
     */
    function collectProduction() {
        const now = Date.now();
        const collected = [];

        farmAnimals.forEach(animal => {
            if (!animal.product) return;
            if (animal.health <= 0) return;

            const interval = animal.productInterval * TAMING_CONFIG.productionMultiplier;
            const happinessBonus = animal.happiness >= 80 ? 0.8 : 1.0; // Glückliche Tiere = schneller
            const adjustedInterval = interval * happinessBonus;

            if ((now - animal.lastProductionTime) >= adjustedInterval) {
                const product = animal.product;
                animal.lastProductionTime = now;

                collected.push({
                    animalId: animal.id,
                    animalName: animal.nickname,
                    monsterId: animal.monsterId,
                    product: product.item,
                    quantity: product.quantity || 1,
                    icon: animal.monsterData.icon || '🐄'
                });

                console.log(`📦 ${animal.nickname} produziert: ${product.quantity || 1}x ${product.item}`);
            }
        });

        if (collected.length > 0) _save();

        return collected;
    }

    /**
     * Farmtier füttern (tägliche Pflege)
     */
    function feedFarmAnimal(animalId, food) {
        const animal = farmAnimals.find(a => a.id === animalId);
        if (!animal) return { success: false, error: 'Tier nicht gefunden' };

        if (animal.fedToday) {
            return { success: false, message: `${animal.nickname} wurde heute schon gefüttert.` };
        }

        animal.fedToday = true;
        animal.happiness = Math.min(100, animal.happiness + 10);
        animal.health = Math.min(100, animal.health + 5);
        _save();

        return {
            success: true,
            message: `${animal.nickname} frisst zufrieden.`,
            happiness: animal.happiness,
            health: animal.health
        };
    }

    /**
     * Täglicher Reset (Hunger, Happiness-Verlust)
     */
    function dailyUpdate() {
        farmAnimals.forEach(animal => {
            if (!animal.fedToday) {
                animal.happiness = Math.max(0, animal.happiness - 15);
                animal.health = Math.max(0, animal.health - 5);
            }
            animal.fedToday = false;
        });

        // Tote Tiere entfernen
        const dead = farmAnimals.filter(a => a.health <= 0);
        if (dead.length > 0) {
            dead.forEach(a => {
                console.log(`💀 ${a.nickname} ist gestorben (Vernachlässigung)`);
                if (typeof notify === 'function') {
                    notify(`💀 ${a.nickname} ist gestorben!`, 'error');
                }
            });
            farmAnimals = farmAnimals.filter(a => a.health > 0);
        }

        _save();
        return { alive: farmAnimals.length, dead: dead.length };
    }

    /**
     * Tier umbenennen
     */
    function renameAnimal(animalId, newName) {
        const animal = farmAnimals.find(a => a.id === animalId);
        if (!animal) return { success: false, error: 'Tier nicht gefunden' };
        const oldName = animal.nickname;
        animal.nickname = newName;
        _save();
        return { success: true, message: `${oldName} heißt jetzt ${newName}!` };
    }

    /**
     * Tier freilassen
     */
    function releaseAnimal(animalId) {
        const index = farmAnimals.findIndex(a => a.id === animalId);
        if (index === -1) return { success: false, error: 'Tier nicht gefunden' };
        const animal = farmAnimals[index];
        farmAnimals.splice(index, 1);
        _save();
        return {
            success: true,
            message: `${animal.nickname} läuft zurück in die Wildnis.`,
            farmCount: farmAnimals.length
        };
    }

    /**
     * Farm-Status abfragen
     */
    function getFarmStatus() {
        return {
            animals: farmAnimals.map(a => ({
                id: a.id,
                monsterId: a.monsterId,
                name: a.nickname,
                icon: a.monsterData.icon || '🐄',
                happiness: a.happiness,
                health: a.health,
                fedToday: a.fedToday,
                product: a.product,
                building: a.building,
                biome: a.monsterData.biome
            })),
            count: farmAnimals.length,
            max: TAMING_CONFIG.maxFarmAnimals,
            buildings: FARM_BUILDINGS
        };
    }

    /**
     * Aktive Zähm-Versuche anzeigen
     */
    function getActiveTaming() {
        return Object.values(activeTaming)
            .filter(tp => !tp.fled && !tp.tamed)
            .map(tp => ({
                monsterId: tp.monsterId,
                name: tp.monsterData.name,
                icon: tp.monsterData.icon,
                progress: tp.progress,
                feedingsGiven: tp.feedingsGiven,
                feedingsRequired: tp.feedingsRequired,
                trust: tp.trust,
                tameFood: tp.monsterData.tameFood
            }));
    }

    // ==========================================
    // REITTIER SYSTEM
    // ==========================================

    /**
     * Farmtier als Reittier verwenden (wenn es ein Reittier ist)
     */
    function mountAnimal(animalId) {
        const animal = farmAnimals.find(a => a.id === animalId);
        if (!animal) return { success: false, error: 'Tier nicht gefunden' };

        const product = animal.monsterData.product;
        if (!product || product.item !== 'Reittier') {
            return { success: false, error: `${animal.nickname} ist kein Reittier!` };
        }

        if (animal.happiness < 30) {
            return { success: false, error: `${animal.nickname} ist zu unglücklich zum Reiten. Füttere es zuerst!` };
        }

        return {
            success: true,
            mount: {
                id: animal.id,
                name: animal.nickname,
                monsterId: animal.monsterId,
                icon: animal.monsterData.icon,
                speedBonus: animal.monsterData.speed || 1.5,
            },
            message: `Du reitest auf ${animal.nickname}!`
        };
    }

    // ==========================================
    // PERSISTENCE
    // ==========================================

    function _save() {
        try {
            const data = {
                farmAnimals: farmAnimals.map(a => ({
                    id: a.id,
                    monsterId: a.monsterId,
                    nickname: a.nickname,
                    tamedAt: a.tamedAt,
                    lastProductionTime: a.lastProductionTime,
                    happiness: a.happiness,
                    health: a.health,
                    fedToday: a.fedToday,
                    building: a.building,
                })),
                activeTaming: Object.fromEntries(
                    Object.entries(activeTaming).map(([k, tp]) => [k, {
                        monsterId: tp.monsterId,
                        instanceId: tp.instanceId,
                        feedingsGiven: tp.feedingsGiven,
                        trust: tp.trust,
                        lastFeedTime: tp.lastFeedTime,
                        fled: tp.fled,
                        tamed: tp.tamed,
                    }])
                )
            };
            localStorage.setItem('najika_taming', JSON.stringify(data));
        } catch (e) {
            console.error('Taming Save Error:', e);
        }
    }

    function _load() {
        try {
            const raw = localStorage.getItem('najika_taming');
            if (!raw) return;
            const data = JSON.parse(raw);
            const registry = window.MonsterRegistry;
            if (!registry) return;

            // Farm-Tiere laden
            if (data.farmAnimals) {
                farmAnimals = data.farmAnimals.map(saved => {
                    const monsterData = registry.getMonster(saved.monsterId);
                    if (!monsterData) return null;
                    const animal = new FarmAnimal(saved.monsterId, monsterData, saved.nickname);
                    animal.id = saved.id;
                    animal.tamedAt = saved.tamedAt;
                    animal.lastProductionTime = saved.lastProductionTime;
                    animal.happiness = saved.happiness;
                    animal.health = saved.health;
                    animal.fedToday = saved.fedToday;
                    animal.building = saved.building;
                    return animal;
                }).filter(Boolean);
            }

            console.log(`🐄 Taming geladen: ${farmAnimals.length} Farmtiere`);
        } catch (e) {
            console.error('Taming Load Error:', e);
        }
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        _load();
        console.log(`🐄 Creature Taming System bereit (${farmAnimals.length} Farmtiere)`);
    }

    // Auto-Init wenn DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.CreatureTaming = {
        // Zähmen
        startTaming,
        feedCreature,
        checkFlee,
        onNearbyCombat,
        getActiveTaming,
        // Farm
        collectProduction,
        feedFarmAnimal,
        dailyUpdate,
        renameAnimal,
        releaseAnimal,
        getFarmStatus,
        // Reittier
        mountAnimal,
        // Config
        TAMING_CONFIG,
        FARM_BUILDINGS,
    };

})();
