/**
 * GAME DATA LOADER - Lädt alle JSON Game-Content-Dateien
 * =====================================================
 *
 * Lädt 40 JSON-Dateien aus /digivice/digivice/data/:
 * - NPCs (9× nach Stadt-Namen)
 * - Items (9× nach Stadt-Namen)
 * - Quests (9× nach Stadt-Namen)
 * - Enemies (9× nach Regions-Namen)
 * - Zusätzliche Dateien (regions.json, cities.json, etc.)
 */

class GameDataLoader {
    constructor() {
        // Game Content Storage
        this.npcs = {};
        this.items = {};
        this.quests = {};
        this.enemies = {};

        // Meta Data
        this.regions = [];
        this.cities = [];
        this.biomes = [];

        // Loading Status
        this.loaded = false;
        this.loadProgress = 0;
    }

    /**
     * Lädt ALLE Game-Content JSON-Dateien
     * PERFORMANCE FIX: Parallel loading statt sequential
     */
    async loadAll() {
        console.log('🎮 Starte Laden von Game Content (PARALLEL)...');
        const startTime = performance.now();

        try {
            // 1. Meta-Dateien laden (klein, schnell)
            await this.loadMetaData();

            // 2. ALLE anderen Kategorien PARALLEL laden!
            await Promise.all([
                this.loadNPCs(),
                this.loadItems(),
                this.loadQuests(),
                this.loadEnemies()
            ]);

            this.loaded = true;
            this.logStats();

            const loadTime = (performance.now() - startTime).toFixed(0);
            console.log(`✅ Game Content vollständig geladen in ${loadTime}ms!`);
            return true;

        } catch (error) {
            console.error('❌ Fehler beim Laden von Game Content:', error);
            return false;
        }
    }

    /**
     * Lädt Meta-Dateien (regions.json, cities.json, biomes.json)
     */
    async loadMetaData() {
        try {
            // Regions - Try multiple paths
            let regionsRes = await fetch('data/regions.json').catch(() => null);
            if (!regionsRes || !regionsRes.ok) {
                regionsRes = await fetch('/digivice/data/regions.json');
            }
            this.regions = await regionsRes.json();

            // Cities
            let citiesRes = await fetch('data/cities.json').catch(() => null);
            if (!citiesRes || !citiesRes.ok) {
                citiesRes = await fetch('/digivice/data/cities.json');
            }
            this.cities = await citiesRes.json();

            // Biomes
            let biomesRes = await fetch('data/biomes.json').catch(() => null);
            if (!biomesRes || !biomesRes.ok) {
                biomesRes = await fetch('/digivice/data/biomes.json');
            }
            this.biomes = await biomesRes.json();

            console.log('✅ Meta-Daten geladen:', {
                regions: this.regions.length,
                cities: this.cities.length,
                biomes: this.biomes.length
            });

        } catch (error) {
            console.warn('⚠️ Meta-Daten teilweise nicht verfügbar:', error);
        }
    }

    /**
     * Lädt alle NPC-Dateien (Stadt-Namen) - PARALLEL
     */
    async loadNPCs() {
        const stadtNamen = [
            'dampfhain',
            'funkensiedlung',
            'goetterfels',
            'gruenschlamm',
            'handelsfestung',
            'reichderdrei',
            'runenheim',
            'salzigebucht',
            'tiefenhoehlen'
        ];

        // PERFORMANCE FIX: Load all cities in parallel
        await Promise.all(stadtNamen.map(async stadt => {
            try {
                let response = await fetch(`data/npcs_${stadt}.json`).catch(() => null);
                if (!response || !response.ok) {
                    response = await fetch(`/digivice/data/npcs_${stadt}.json`);
                }
                this.npcs[stadt] = await response.json();
            } catch (error) {
                this.npcs[stadt] = [];
            }
        }));

        console.log(`✅ NPCs geladen: ${Object.values(this.npcs).flat().length} total`);
    }

    /**
     * Lädt alle Items-Dateien (Stadt-Namen) - PARALLEL
     */
    async loadItems() {
        const stadtNamen = [
            'dampfhain',
            'funkensiedlung',
            'goetterfels',
            'gruenschlamm',
            'handelsfestung',
            'reichderdrei',
            'runenheim',
            'salzigebucht',
            'tiefenhoehlen'
        ];

        // PERFORMANCE FIX: Load all cities in parallel
        await Promise.all(stadtNamen.map(async stadt => {
            try {
                let response = await fetch(`data/items_${stadt}.json`).catch(() => null);
                if (!response || !response.ok) {
                    response = await fetch(`/digivice/data/items_${stadt}.json`);
                }
                this.items[stadt] = await response.json();
            } catch (error) {
                this.items[stadt] = [];
            }
        }));

        console.log(`✅ Items geladen: ${Object.values(this.items).flat().length} total`);
    }

    /**
     * Lädt alle Quest-Dateien (Stadt-Namen) - PARALLEL
     */
    async loadQuests() {
        const stadtNamen = [
            'dampfhain',
            'funkensiedlung',
            'goetterfels',
            'gruenschlamm',
            'handelsfestung',
            'reichderdrei',
            'runenheim',
            'salzigebucht',
            'tiefenhoehlen'
        ];

        // PERFORMANCE FIX: Load all cities in parallel
        await Promise.all(stadtNamen.map(async stadt => {
            try {
                let response = await fetch(`data/quests_${stadt}.json`).catch(() => null);
                if (!response || !response.ok) {
                    response = await fetch(`/digivice/data/quests_${stadt}.json`);
                }
                this.quests[stadt] = await response.json();
            } catch (error) {
                this.quests[stadt] = [];
            }
        }));

        console.log(`✅ Quests geladen: ${Object.values(this.quests).flat().length} total`);
    }

    /**
     * Lädt alle Enemy-Dateien (Regions-Namen) - PARALLEL
     */
    async loadEnemies() {
        const regionsNamen = [
            'blitzebene',
            'goetterfels',
            'gruenschlamm',
            'heisse_duenen',
            'magmastroeme',
            'reichderdrei',
            'salzwind_kueste',
            'samtmoos_tiefwald',
            'tiefenhoehlen'
        ];

        // PERFORMANCE FIX: Load all regions in parallel
        await Promise.all(regionsNamen.map(async region => {
            try {
                let response = await fetch(`data/enemies_${region}.json`).catch(() => null);
                if (!response || !response.ok) {
                    response = await fetch(`/digivice/data/enemies_${region}.json`);
                }
                this.enemies[region] = await response.json();
            } catch (error) {
                this.enemies[region] = [];
            }
        }));

        console.log(`✅ Enemies geladen: ${Object.values(this.enemies).flat().length} total`);
    }

    /**
     * Gibt Statistiken aus
     */
    logStats() {
        const stats = {
            npcs: Object.values(this.npcs).flat().length,
            items: Object.values(this.items).flat().length,
            quests: Object.values(this.quests).flat().length,
            enemies: Object.values(this.enemies).flat().length
        };

        console.log('📊 Game Content Statistik:');
        console.log(`   NPCs: ${stats.npcs}`);
        console.log(`   Items: ${stats.items}`);
        console.log(`   Quests: ${stats.quests}`);
        console.log(`   Enemies: ${stats.enemies}`);
        console.log(`   TOTAL: ${stats.npcs + stats.items + stats.quests + stats.enemies} Einträge`);
    }

    /**
     * Holt NPCs für eine Stadt
     */
    getNPCsForCity(cityName) {
        return this.npcs[cityName] || [];
    }

    /**
     * Holt Items für eine Stadt
     */
    getItemsForCity(cityName) {
        return this.items[cityName] || [];
    }

    /**
     * Holt Quests für eine Stadt
     */
    getQuestsForCity(cityName) {
        return this.quests[cityName] || [];
    }

    /**
     * Holt Enemies für eine Region
     */
    getEnemiesForRegion(regionName) {
        return this.enemies[regionName] || [];
    }
}

// Globale Instanz
window.gameDataLoader = new GameDataLoader();
