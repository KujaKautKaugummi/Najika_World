/**
 * GAME DATA LOADER - Lädt alle JSON Game-Content-Dateien
 * =====================================================
 *
 * Lädt 40 JSON-Dateien aus /data/:
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
     */
    async loadAll() {
        console.log('🎮 Starte Laden von Game Content...');

        try {
            // 1. Meta-Dateien laden
            await this.loadMetaData();

            // 2. NPCs laden (Stadt-Namen)
            await this.loadNPCs();

            // 3. Items laden (Stadt-Namen)
            await this.loadItems();

            // 4. Quests laden (Stadt-Namen)
            await this.loadQuests();

            // 5. Enemies laden (Regions-Namen)
            await this.loadEnemies();

            this.loaded = true;
            this.logStats();

            console.log('✅ Game Content vollständig geladen!');
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
            // Regions
            const regionsRes = await fetch('data/regions.json');
            if (!regionsRes.ok) throw new Error(`Regions fetch failed: ${regionsRes.status}`);
            this.regions = await regionsRes.json();

            // Cities
            const citiesRes = await fetch('data/cities.json');
            if (!citiesRes.ok) throw new Error(`Cities fetch failed: ${citiesRes.status}`);
            this.cities = await citiesRes.json();

            // Biomes
            const biomesRes = await fetch('data/biomes.json');
            if (!biomesRes.ok) throw new Error(`Biomes fetch failed: ${biomesRes.status}`);
            this.biomes = await biomesRes.json();

            console.log('✅ Meta-Daten geladen:', {
                regions: this.regions?.length || 0,
                cities: this.cities?.length || 0,
                biomes: this.biomes?.length || 0
            });

        } catch (error) {
            console.warn('⚠️ Meta-Daten teilweise nicht verfügbar:', error);
            // Fallback empty arrays to prevent null reference
            this.regions = this.regions || [];
            this.cities = this.cities || [];
            this.biomes = this.biomes || [];
        }
    }

    /**
     * Lädt alle NPC-Dateien (Stadt-Namen)
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

        for (const stadt of stadtNamen) {
            try {
                const response = await fetch(`data/npcs_${stadt}.json`);
                this.npcs[stadt] = await response.json();
            } catch (error) {
                console.warn(`⚠️ NPCs für ${stadt} nicht gefunden`);
                this.npcs[stadt] = [];
            }
        }

        console.log(`✅ NPCs geladen: ${Object.values(this.npcs).flat().length} total`);
    }

    /**
     * Lädt alle Items-Dateien (Stadt-Namen)
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

        for (const stadt of stadtNamen) {
            try {
                const response = await fetch(`data/items_${stadt}.json`);
                this.items[stadt] = await response.json();
            } catch (error) {
                console.warn(`⚠️ Items für ${stadt} nicht gefunden`);
                this.items[stadt] = [];
            }
        }

        console.log(`✅ Items geladen: ${Object.values(this.items).flat().length} total`);
    }

    /**
     * Lädt alle Quest-Dateien (Stadt-Namen)
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

        for (const stadt of stadtNamen) {
            try {
                const response = await fetch(`data/quests_${stadt}.json`);
                this.quests[stadt] = await response.json();
            } catch (error) {
                console.warn(`⚠️ Quests für ${stadt} nicht gefunden`);
                this.quests[stadt] = [];
            }
        }

        console.log(`✅ Quests geladen: ${Object.values(this.quests).flat().length} total`);
    }

    /**
     * Lädt alle Enemy-Dateien (Regions-Namen)
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

        for (const region of regionsNamen) {
            try {
                const response = await fetch(`data/enemies_${region}.json`);
                this.enemies[region] = await response.json();
            } catch (error) {
                console.warn(`⚠️ Enemies für ${region} nicht gefunden`);
                this.enemies[region] = [];
            }
        }

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
