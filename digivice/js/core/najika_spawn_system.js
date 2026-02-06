/**
 * NAJIKA SPAWN SYSTEM
 * ===================
 * Verwaltet Najikas Spawn-Position in verschiedenen Kontexten.
 *
 * REGELN:
 * - DIGIVICE: Najika ist IMMER in der Schwarzen Mühle
 * - GAME WORLD: Najika spawnt an letzter Position > letzte Stadt > Schwarze Mühle
 *
 * Copyright: Najika World
 * Author: Claude Code (Sonnet)
 * Date: 2026-02-06
 */

const NajikaSpawnSystem = {
    // ===== KONSTANTEN =====

    // Schwarze Mühle - Mitte der Welt auf dem Götterfels
    SCHWARZE_MUEHLE: {
        x: 4800,
        y: 150,  // Auf dem Berg
        z: 4800,
        name: 'Schwarze Mühle',
        isSafeZone: true
    },

    // Welt-Grenzen (9600 x 9600)
    WORLD_BOUNDS: {
        minX: 0, maxX: 9600,
        minZ: 0, maxZ: 9600
    },

    // Stadt-Spawn-Punkte
    CITY_SPAWNS: {
        // Heiße Dünen - Süd-Ost
        'handelsfeste': { x: 7200, y: 10, z: 7200, region: 'heisse_duenen' },

        // Reich der Drei - Nord-West (Eis)
        'frostheim': { x: 1200, y: 50, z: 1200, region: 'reich_der_drei' },

        // Blitzebene - Ost
        'sturmwacht': { x: 7800, y: 20, z: 4800, region: 'blitzebene' },

        // Grünschlamm-Sumpf - Süd-West
        'sumpfheim': { x: 2400, y: 5, z: 6000, region: 'gruenschlamm_sumpf' },

        // Samtmoos-Tiefwald - Nord
        'waldheim': { x: 4800, y: 30, z: 1200, region: 'samtmoos_tiefwald' },

        // Magmaströme - Süd
        'magmafort': { x: 4800, y: 25, z: 8400, region: 'magmastroeme' },

        // Tiefenhöhlen - Unter Samtmoos
        'tiefenstadt': { x: 4800, y: -50, z: 2400, region: 'tiefenhoehlen' },

        // Salzwind-Küste - West
        'hafenstadt': { x: 600, y: 5, z: 4800, region: 'salzwind_kueste' }
    },

    // ===== SPAWN-DATEN =====

    spawnData: {
        lastPosition: null,
        lastCity: null,
        lastRegion: null,
        lastTimestamp: null,
        currentContext: 'digivice',  // 'digivice' oder 'game_world'
        sessionId: null
    },

    // ===== INITIALISIERUNG =====

    /**
     * Initialisiert das Spawn-System
     */
    init() {
        this.loadSpawnData();
        this.spawnData.sessionId = this.generateSessionId();
        console.log('[NajikaSpawn] Initialisiert:', this.spawnData);
        return this;
    },

    /**
     * Generiert eine Session-ID
     */
    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },

    // ===== SPAWN-LOGIK =====

    /**
     * Bestimmt Najikas Spawn-Position
     * @param {string} context - 'digivice' oder 'game_world'
     * @returns {Object} Spawn-Info mit position, location, reason
     */
    getSpawnPosition(context = 'game_world') {
        this.spawnData.currentContext = context;

        // DIGIVICE: Immer Schwarze Mühle
        if (context === 'digivice') {
            return {
                position: { ...this.SCHWARZE_MUEHLE },
                location: 'schwarze_muehle',
                locationName: 'Schwarze Mühle',
                reason: 'Digivice Home - Najikas Zuhause',
                isSafeZone: true,
                najikaMessage: "Willkommen in meinem Zuhause, Mr. K! Die Schwarze Mühle ist unser sicherer Hafen!"
            };
        }

        // GAME WORLD: Prioritäts-Reihenfolge

        // 1. Letzte Position (wenn gültig und nicht zu alt)
        if (this.spawnData.lastPosition && this.isValidPosition(this.spawnData.lastPosition)) {
            const age = Date.now() - (this.spawnData.lastTimestamp || 0);
            const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 Tage

            if (age < maxAge) {
                return {
                    position: { ...this.spawnData.lastPosition },
                    location: 'last_position',
                    locationName: this.spawnData.lastRegion || 'Unbekannt',
                    reason: 'Letzte bekannte Position',
                    isSafeZone: false,
                    najikaMessage: "Mr. K! Hier waren wir zuletzt! Ich erinnere mich genau!"
                };
            }
        }

        // 2. Letzte Stadt
        if (this.spawnData.lastCity && this.CITY_SPAWNS[this.spawnData.lastCity]) {
            const cityData = this.CITY_SPAWNS[this.spawnData.lastCity];
            return {
                position: { x: cityData.x, y: cityData.y, z: cityData.z },
                location: this.spawnData.lastCity,
                locationName: this.formatCityName(this.spawnData.lastCity),
                reason: 'Letzte besuchte Stadt',
                isSafeZone: true,  // Städte sind Safe Zones
                najikaMessage: `Mr. K! Wir sind wieder in ${this.formatCityName(this.spawnData.lastCity)}! Diese Stadt mag ich!`
            };
        }

        // 3. Fallback: Schwarze Mühle
        return {
            position: { ...this.SCHWARZE_MUEHLE },
            location: 'schwarze_muehle',
            locationName: 'Schwarze Mühle',
            reason: 'Safe Zone Fallback - Kein vorheriger Spawn-Punkt',
            isSafeZone: true,
            najikaMessage: "Mr. K! Wir starten in der Schwarzen Mühle! Unser sicherer Hafen!"
        };
    },

    /**
     * Formatiert Stadt-Namen für Anzeige
     */
    formatCityName(cityKey) {
        const names = {
            'handelsfeste': 'Handelsfeste',
            'frostheim': 'Frostheim',
            'sturmwacht': 'Sturmwacht',
            'sumpfheim': 'Sumpfheim',
            'waldheim': 'Waldheim',
            'magmafort': 'Magmafort',
            'tiefenstadt': 'Tiefenstadt',
            'hafenstadt': 'Hafenstadt'
        };
        return names[cityKey] || cityKey;
    },

    // ===== POSITION SPEICHERN =====

    /**
     * Speichert Najikas aktuelle Position
     * @param {Object} position - {x, y, z}
     * @param {string} cityName - Name der Stadt (optional)
     * @param {string} regionName - Name der Region (optional)
     */
    savePosition(position, cityName = null, regionName = null) {
        if (!this.isValidPosition(position)) {
            console.warn('[NajikaSpawn] Ungültige Position, nicht gespeichert:', position);
            return false;
        }

        this.spawnData.lastPosition = { ...position };
        this.spawnData.lastTimestamp = Date.now();

        if (cityName) {
            this.spawnData.lastCity = cityName.toLowerCase();
        }

        if (regionName) {
            this.spawnData.lastRegion = regionName;
        }

        this.persistSpawnData();
        console.log('[NajikaSpawn] Position gespeichert:', this.spawnData);
        return true;
    },

    /**
     * Markiert Eintritt in eine Stadt
     * @param {string} cityName - Name der Stadt
     */
    enterCity(cityName) {
        const cityKey = cityName.toLowerCase();
        if (this.CITY_SPAWNS[cityKey]) {
            const cityData = this.CITY_SPAWNS[cityKey];
            this.savePosition(
                { x: cityData.x, y: cityData.y, z: cityData.z },
                cityKey,
                cityData.region
            );
            return true;
        }
        return false;
    },

    // ===== VALIDIERUNG =====

    /**
     * Prüft ob Position gültig ist
     */
    isValidPosition(pos) {
        if (!pos || typeof pos.x !== 'number' || typeof pos.z !== 'number') {
            return false;
        }

        // Innerhalb der Welt-Grenzen?
        return pos.x >= this.WORLD_BOUNDS.minX &&
               pos.x <= this.WORLD_BOUNDS.maxX &&
               pos.z >= this.WORLD_BOUNDS.minZ &&
               pos.z <= this.WORLD_BOUNDS.maxZ;
    },

    /**
     * Prüft ob Position in einer Safe Zone ist
     */
    isInSafeZone(pos) {
        // Schwarze Mühle (Radius 200)
        const distToMuehle = Math.sqrt(
            Math.pow(pos.x - this.SCHWARZE_MUEHLE.x, 2) +
            Math.pow(pos.z - this.SCHWARZE_MUEHLE.z, 2)
        );
        if (distToMuehle < 200) return true;

        // Städte (Radius 100)
        for (const [cityName, cityData] of Object.entries(this.CITY_SPAWNS)) {
            const dist = Math.sqrt(
                Math.pow(pos.x - cityData.x, 2) +
                Math.pow(pos.z - cityData.z, 2)
            );
            if (dist < 100) return true;
        }

        return false;
    },

    // ===== PERSISTENZ =====

    /**
     * Lädt Spawn-Daten aus localStorage
     */
    loadSpawnData() {
        try {
            const saved = localStorage.getItem('najika_spawn_data');
            if (saved) {
                const parsed = JSON.parse(saved);
                this.spawnData = { ...this.spawnData, ...parsed };
            }
        } catch (e) {
            console.error('[NajikaSpawn] Fehler beim Laden:', e);
        }
    },

    /**
     * Speichert Spawn-Daten in localStorage
     */
    persistSpawnData() {
        try {
            localStorage.setItem('najika_spawn_data', JSON.stringify(this.spawnData));
        } catch (e) {
            console.error('[NajikaSpawn] Fehler beim Speichern:', e);
        }
    },

    /**
     * Setzt alle Spawn-Daten zurück
     */
    reset() {
        this.spawnData = {
            lastPosition: null,
            lastCity: null,
            lastRegion: null,
            lastTimestamp: null,
            currentContext: 'digivice',
            sessionId: this.generateSessionId()
        };
        localStorage.removeItem('najika_spawn_data');
        console.log('[NajikaSpawn] Zurückgesetzt');
    },

    // ===== HELPER =====

    /**
     * Holt alle verfügbaren Städte
     */
    getAllCities() {
        return Object.entries(this.CITY_SPAWNS).map(([key, data]) => ({
            id: key,
            name: this.formatCityName(key),
            position: { x: data.x, y: data.y, z: data.z },
            region: data.region
        }));
    },

    /**
     * Teleportiert Najika zur Schwarzen Mühle
     */
    teleportToHome() {
        this.savePosition(this.SCHWARZE_MUEHLE, null, 'Götterfels');
        return this.getSpawnPosition('game_world');
    },

    /**
     * Gibt aktuellen Status zurück
     */
    getStatus() {
        return {
            ...this.spawnData,
            schwarzeMuehle: this.SCHWARZE_MUEHLE,
            availableCities: this.getAllCities()
        };
    }
};

// Auto-Init wenn geladen
if (typeof window !== 'undefined') {
    window.NajikaSpawnSystem = NajikaSpawnSystem.init();
}

// Export für Module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NajikaSpawnSystem;
}
