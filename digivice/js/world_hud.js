/**
 * World HUD System - Najika World
 * In-game HUD overlay showing region info, coordinates, time, weather
 *
 * Features:
 * - Region name & biome display
 * - Player coordinates
 * - Time of day & weather
 * - Compass direction
 * - Minimalistic design
 *
 * Integration with world_info_ui.js
 */

(function() {
    'use strict';

class WorldHUD {
    constructor() {
        this.hudElement = null;
        this.isVisible = true;
        this.currentRegion = 'Unknown';
        this.currentBiome = 'unknown';
        this.playerPosition = { x: 0, y: 0, z: 0 };
        this.heading = 0; // 0-360 degrees (0 = North)
        this.timeOfDay = '12:00';
        this.weather = 'Clear';

        this.createHUD();
        console.log('🌍 World HUD initialized');
    }

    /**
     * Create HUD DOM element
     */
    createHUD() {
        this.hudElement = document.createElement('div');
        this.hudElement.id = 'world-hud';
        this.hudElement.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(102, 126, 234, 0.5);
            border-radius: 15px;
            padding: 15px 20px;
            color: white;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            z-index: 1000;
            min-width: 280px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            user-select: none;
            pointer-events: none;
        `;

        this.hudElement.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <!-- Region & Biome -->
                <div style="border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 8px;">
                    <div style="font-weight: bold; font-size: 16px; color: #667eea;" id="hud-region">
                        🗺️ Unknown Region
                    </div>
                    <div style="font-size: 11px; color: #888; margin-top: 3px;" id="hud-biome">
                        Biome: Unknown
                    </div>
                </div>

                <!-- Position & Heading -->
                <div style="display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center;">
                    <div>
                        <div style="color: #aaa; font-size: 11px;">Position</div>
                        <div id="hud-position" style="font-family: 'Courier New', monospace;">
                            X: 0 | Y: 0 | Z: 0
                        </div>
                    </div>
                    <div id="hud-compass" style="
                        width: 50px;
                        height: 50px;
                        background: rgba(255,255,255,0.1);
                        border-radius: 50%;
                        border: 2px solid rgba(255,255,255,0.3);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        position: relative;
                    ">
                        <span style="position: absolute; top: 2px; font-size: 10px; color: #ff6b6b;">N</span>
                        <span id="hud-compass-arrow" style="
                            transform: rotate(0deg);
                            transition: transform 0.3s;
                        ">↑</span>
                    </div>
                </div>

                <!-- Time & Weather -->
                <div style="display: flex; justify-content: space-between; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.2);">
                    <div>
                        <span style="color: #aaa;">⏰</span>
                        <span id="hud-time">12:00</span>
                    </div>
                    <div>
                        <span id="hud-weather-icon">☀️</span>
                        <span id="hud-weather">Clear</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.hudElement);
    }

    /**
     * Update region info
     * @param {string} regionName - Region name
     * @param {string} biomeName - Biome name
     */
    updateRegion(regionName, biomeName) {
        this.currentRegion = regionName;
        this.currentBiome = biomeName;

        const regionEl = document.getElementById('hud-region');
        const biomeEl = document.getElementById('hud-biome');

        if (regionEl) {
            regionEl.textContent = `🗺️ ${regionName}`;
        }

        if (biomeEl) {
            biomeEl.textContent = `Biome: ${biomeName}`;
        }
    }

    /**
     * Update player position
     * @param {Object} position - {x, y, z}
     */
    updatePosition(position) {
        this.playerPosition = position;

        const posEl = document.getElementById('hud-position');
        if (posEl) {
            posEl.textContent = `X: ${Math.round(position.x)} | Y: ${Math.round(position.y)} | Z: ${Math.round(position.z)}`;
        }
    }

    /**
     * Update compass heading
     * @param {number} degrees - Heading in degrees (0-360, 0 = North)
     */
    updateHeading(degrees) {
        this.heading = degrees;

        const arrow = document.getElementById('hud-compass-arrow');
        if (arrow) {
            arrow.style.transform = `rotate(${degrees}deg)`;
        }
    }

    /**
     * Update time of day
     * @param {string} time - Time string (HH:MM)
     */
    updateTime(time) {
        this.timeOfDay = time;

        const timeEl = document.getElementById('hud-time');
        if (timeEl) {
            timeEl.textContent = time;
        }
    }

    /**
     * Update weather
     * @param {string} weather - Weather type (Clear, Rain, Snow, etc.)
     */
    updateWeather(weather) {
        this.weather = weather;

        const weatherEl = document.getElementById('hud-weather');
        const weatherIcon = document.getElementById('hud-weather-icon');

        if (weatherEl) {
            weatherEl.textContent = weather;
        }

        if (weatherIcon) {
            const icons = {
                'Clear': '☀️',
                'Cloudy': '☁️',
                'Rain': '🌧️',
                'Snow': '❄️',
                'Storm': '⛈️',
                'Fog': '🌫️'
            };
            weatherIcon.textContent = icons[weather] || '☀️';
        }
    }

    /**
     * Show/hide HUD
     * @param {boolean} visible
     */
    setVisible(visible) {
        this.isVisible = visible;

        if (this.hudElement) {
            this.hudElement.style.display = visible ? 'block' : 'none';
        }
    }

    /**
     * Toggle HUD visibility
     */
    toggle() {
        this.setVisible(!this.isVisible);
    }

    /**
     * Update HUD with all data at once
     * @param {Object} data - HUD data object
     */
    updateAll(data) {
        if (data.region) this.updateRegion(data.region, data.biome || 'unknown');
        if (data.position) this.updatePosition(data.position);
        if (data.heading !== undefined) this.updateHeading(data.heading);
        if (data.time) this.updateTime(data.time);
        if (data.weather) this.updateWeather(data.weather);
    }

    /**
     * Auto-detect region based on coordinates
     * @param {Object} position - {x, z}
     * @returns {Object} {region, biome}
     */
    detectRegion(position) {
        // 9600×9600 world divided into 9 regions (3×3 grid)
        // Each region is 3200×3200

        const regions = [
            // Row 1 (Top)
            { x: [0, 3200], z: [0, 3200], name: 'Crimson Desert', biome: 'desert' },
            { x: [3200, 6400], z: [0, 3200], name: 'Amber Forests', biome: 'forest' },
            { x: [6400, 9600], z: [0, 3200], name: 'Emerald Grasslands', biome: 'grassland' },

            // Row 2 (Middle)
            { x: [0, 3200], z: [3200, 6400], name: 'Ivory Tundra', biome: 'tundra' },
            { x: [3200, 6400], z: [3200, 6400], name: 'Götterfels', biome: 'alpine' },
            { x: [6400, 9600], z: [3200, 6400], name: 'Violet Swamps', biome: 'swamp' },

            // Row 3 (Bottom)
            { x: [0, 3200], z: [6400, 9600], name: 'Obsidian Peaks', biome: 'volcanic' },
            { x: [3200, 6400], z: [6400, 9600], name: 'Golden Highlands', biome: 'highland' },
            { x: [6400, 9600], z: [6400, 9600], name: 'Azure Coastline', biome: 'coastal' }
        ];

        for (const region of regions) {
            if (position.x >= region.x[0] && position.x < region.x[1] &&
                position.z >= region.z[0] && position.z < region.z[1]) {
                return { region: region.name, biome: region.biome };
            }
        }

        return { region: 'Unknown', biome: 'unknown' };
    }

    /**
     * Calculate heading from character rotation
     * @param {number} rotation - Rotation in radians
     * @returns {number} Degrees (0-360)
     */
    calculateHeading(rotation) {
        // Convert radians to degrees
        let degrees = (rotation * 180 / Math.PI) % 360;

        // Normalize to 0-360
        if (degrees < 0) degrees += 360;

        return degrees;
    }

    /**
     * Dispose HUD
     */
    dispose() {
        if (this.hudElement && this.hudElement.parentNode) {
            this.hudElement.parentNode.removeChild(this.hudElement);
        }
        console.log('🌍 World HUD disposed');
    }
}

// Export to global scope
window.WorldHUD = WorldHUD;

console.log('🌍 WorldHUD loaded successfully');

})();
