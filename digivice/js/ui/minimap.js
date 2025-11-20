/**
 * Minimap System
 * Kleine Karte in der Ecke des Bildschirms
 *
 * Features:
 * - Zeigt aktuelle Region und Umgebung
 * - Spieler-Marker mit Blickrichtung
 * - Nearby Points of Interest
 * - Nearby Enemies (als rote Punkte)
 * - Interactive: Klick zum Öffnen der großen Karte
 * - Zoombare Mini-Ansicht
 */

class Minimap {
    constructor(options = {}) {
        // Configuration
        this.size = options.size || 200; // Size in pixels
        this.position = options.position || 'top-right'; // top-left, top-right, bottom-left, bottom-right
        this.zoom = options.zoom || 20; // How many world units per pixel
        this.showPOI = options.showPOI !== false; // Show Points of Interest
        this.showEnemies = options.showEnemies !== false; // Show nearby enemies
        this.interactive = options.interactive !== false; // Allow clicking to open full map

        // World data
        this.worldSize = 9600;
        this.regionsData = null;
        this.biomesData = null;

        // Player data
        this.playerPosition = { x: 4800, z: 4800 };
        this.playerRotation = 0; // In radians

        // POI data
        this.pointsOfInterest = [];
        this.nearbyEnemies = [];

        // Canvas elements
        this.container = null;
        this.canvas = null;
        this.ctx = null;

        // State
        this.visible = true;
        this.opacity = 1.0;

        // Animation
        this.animationId = null;
        this.lastUpdate = 0;
        this.updateInterval = 100; // Update every 100ms

        this.init();
    }

    async init() {
        console.log('🗺️ Initializing Minimap...');

        // Load world data
        await this.loadWorldData();

        // Create UI elements
        this.createMinimapUI();

        // Start rendering
        this.startRendering();

        console.log('✅ Minimap initialized!');
    }

    async loadWorldData() {
        try {
            // Load regions data
            const regionsResponse = await fetch('/data/regions.json');
            this.regionsData = await regionsResponse.json();

            // Load biomes data
            const biomesResponse = await fetch('/data/biomes.json');
            this.biomesData = await biomesResponse.json();

            console.log('✅ Minimap world data loaded');
        } catch (error) {
            console.error('❌ Failed to load minimap world data:', error);
        }
    }

    createMinimapUI() {
        // Create container
        this.container = document.createElement('div');
        this.container.id = 'minimap-container';
        this.container.style.cssText = `
            position: fixed;
            width: ${this.size}px;
            height: ${this.size}px;
            z-index: 9999;
            border: 3px solid #0f3460;
            border-radius: 10px;
            background: rgba(10, 10, 21, 0.9);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
            overflow: hidden;
            ${this.getPositionCSS()}
        `;

        if (this.interactive) {
            this.container.style.cursor = 'pointer';
            this.container.addEventListener('click', () => this.openFullMap());
        }

        // Create canvas
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.size;
        this.canvas.height = this.size;
        this.canvas.style.cssText = `
            display: block;
            width: 100%;
            height: 100%;
        `;

        this.ctx = this.canvas.getContext('2d');
        this.container.appendChild(this.canvas);

        // Add toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = '−';
        toggleBtn.style.cssText = `
            position: absolute;
            top: 5px;
            right: 5px;
            width: 20px;
            height: 20px;
            background: rgba(233, 69, 96, 0.8);
            border: none;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 3px;
            cursor: pointer;
            padding: 0;
            line-height: 18px;
            z-index: 10;
        `;
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
            toggleBtn.textContent = this.visible ? '−' : '+';
        });
        this.container.appendChild(toggleBtn);

        // Add zoom controls
        const zoomContainer = document.createElement('div');
        zoomContainer.style.cssText = `
            position: absolute;
            bottom: 5px;
            right: 5px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        `;

        const createZoomBtn = (text, action) => {
            const btn = document.createElement('button');
            btn.textContent = text;
            btn.style.cssText = `
                width: 20px;
                height: 20px;
                background: rgba(15, 52, 96, 0.8);
                border: 1px solid #0f3460;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border-radius: 3px;
                cursor: pointer;
                padding: 0;
                line-height: 18px;
            `;
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                action();
            });
            return btn;
        };

        zoomContainer.appendChild(createZoomBtn('+', () => this.zoomIn()));
        zoomContainer.appendChild(createZoomBtn('−', () => this.zoomOut()));
        this.container.appendChild(zoomContainer);

        // Add label
        const label = document.createElement('div');
        label.textContent = 'Map';
        label.style.cssText = `
            position: absolute;
            top: 5px;
            left: 5px;
            color: #e94560;
            font-size: 10px;
            font-weight: bold;
            text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
            pointer-events: none;
        `;
        this.container.appendChild(label);

        document.body.appendChild(this.container);
    }

    getPositionCSS() {
        const margin = '20px';
        switch (this.position) {
            case 'top-left':
                return `top: ${margin}; left: ${margin};`;
            case 'top-right':
                return `top: ${margin}; right: ${margin};`;
            case 'bottom-left':
                return `bottom: ${margin}; left: ${margin};`;
            case 'bottom-right':
                return `bottom: ${margin}; right: ${margin};`;
            default:
                return `top: ${margin}; right: ${margin};`;
        }
    }

    startRendering() {
        const render = (timestamp) => {
            // Throttle updates
            if (timestamp - this.lastUpdate >= this.updateInterval) {
                this.render();
                this.lastUpdate = timestamp;
            }

            this.animationId = requestAnimationFrame(render);
        };

        this.animationId = requestAnimationFrame(render);
    }

    render() {
        if (!this.visible || !this.ctx) return;

        const ctx = this.ctx;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;

        // Clear canvas
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw background
        ctx.fillStyle = 'rgba(10, 10, 21, 0.95)';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw surrounding regions/biomes
        this.drawBiomes(ctx, centerX, centerY);

        // Draw grid
        this.drawGrid(ctx, centerX, centerY);

        // Draw Points of Interest
        if (this.showPOI) {
            this.drawPOI(ctx, centerX, centerY);
        }

        // Draw nearby enemies
        if (this.showEnemies) {
            this.drawEnemies(ctx, centerX, centerY);
        }

        // Draw player marker
        this.drawPlayer(ctx, centerX, centerY);

        // Draw compass
        this.drawCompass(ctx);

        // Draw border
        ctx.strokeStyle = '#0f3460';
        ctx.lineWidth = 2;
        ctx.strokeRect(1, 1, this.canvas.width - 2, this.canvas.height - 2);
    }

    drawBiomes(ctx, centerX, centerY) {
        if (!this.regionsData || !this.biomesData) return;

        Object.values(this.regionsData.regions).forEach(region => {
            const bounds = region.bounds;

            // Convert world coordinates to minimap coordinates
            const minX = this.worldToMinimap(bounds.minX, centerX);
            const maxX = this.worldToMinimap(bounds.maxX, centerX);
            const minZ = this.worldToMinimap(bounds.minZ, centerY);
            const maxZ = this.worldToMinimap(bounds.maxZ, centerY);

            // Check if region is visible on minimap
            if (maxX < 0 || minX > this.canvas.width || maxZ < 0 || minZ > this.canvas.height) {
                return; // Skip regions outside minimap view
            }

            // Get biome color
            const biome = this.biomesData.biomes[region.biome];
            if (!biome) return;

            const color = biome.colors.ground;

            // Draw region
            ctx.fillStyle = this.hexToRgba(color, 0.5);
            ctx.fillRect(minX, minZ, maxX - minX, maxZ - minZ);

            // Draw border
            ctx.strokeStyle = this.hexToRgba(color, 0.8);
            ctx.lineWidth = 1;
            ctx.strokeRect(minX, minZ, maxX - minX, maxZ - minZ);
        });
    }

    drawGrid(ctx, centerX, centerY) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;

        const gridSize = 500; // Grid every 500 world units

        // Calculate visible range
        const halfView = (this.canvas.width / 2) * this.zoom;
        const startX = Math.floor((this.playerPosition.x - halfView) / gridSize) * gridSize;
        const endX = Math.ceil((this.playerPosition.x + halfView) / gridSize) * gridSize;
        const startZ = Math.floor((this.playerPosition.z - halfView) / gridSize) * gridSize;
        const endZ = Math.ceil((this.playerPosition.z + halfView) / gridSize) * gridSize;

        // Draw vertical lines
        for (let x = startX; x <= endX; x += gridSize) {
            const screenX = this.worldToMinimap(x, centerX);
            ctx.beginPath();
            ctx.moveTo(screenX, 0);
            ctx.lineTo(screenX, this.canvas.height);
            ctx.stroke();
        }

        // Draw horizontal lines
        for (let z = startZ; z <= endZ; z += gridSize) {
            const screenZ = this.worldToMinimap(z, centerY);
            ctx.beginPath();
            ctx.moveTo(0, screenZ);
            ctx.lineTo(this.canvas.width, screenZ);
            ctx.stroke();
        }
    }

    drawPOI(ctx, centerX, centerY) {
        this.pointsOfInterest.forEach(poi => {
            const x = this.worldToMinimap(poi.x, centerX);
            const z = this.worldToMinimap(poi.z, centerY);

            // Only draw if visible
            if (x < 0 || x > this.canvas.width || z < 0 || z > this.canvas.height) {
                return;
            }

            // Draw POI marker
            ctx.fillStyle = poi.color || '#00ff00';
            ctx.beginPath();
            ctx.arc(x, z, 4, 0, Math.PI * 2);
            ctx.fill();

            // Draw border
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1;
            ctx.stroke();

            // Draw icon if available
            if (poi.icon) {
                ctx.fillStyle = '#ffffff';
                ctx.font = '10px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(poi.icon, x, z);
            }
        });
    }

    drawEnemies(ctx, centerX, centerY) {
        this.nearbyEnemies.forEach(enemy => {
            const x = this.worldToMinimap(enemy.x, centerX);
            const z = this.worldToMinimap(enemy.z, centerY);

            // Only draw if visible
            if (x < 0 || x > this.canvas.width || z < 0 || z > this.canvas.height) {
                return;
            }

            // Draw enemy marker (pulsing red dot)
            const pulse = Math.sin(Date.now() * 0.005) * 0.5 + 0.5;
            const size = 3 + pulse * 2;

            ctx.fillStyle = `rgba(255, 0, 0, ${0.6 + pulse * 0.4})`;
            ctx.beginPath();
            ctx.arc(x, z, size, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    drawPlayer(ctx, centerX, centerY) {
        // Draw player direction indicator
        const arrowLength = 15;
        const arrowWidth = 10;

        // Calculate arrow points
        const tipX = centerX + Math.sin(this.playerRotation) * arrowLength;
        const tipY = centerY - Math.cos(this.playerRotation) * arrowLength;

        const baseAngle1 = this.playerRotation + Math.PI * 0.75;
        const baseAngle2 = this.playerRotation - Math.PI * 0.75;

        const base1X = centerX + Math.sin(baseAngle1) * arrowWidth;
        const base1Y = centerY - Math.cos(baseAngle1) * arrowWidth;
        const base2X = centerX + Math.sin(baseAngle2) * arrowWidth;
        const base2Y = centerY - Math.cos(baseAngle2) * arrowWidth;

        // Draw arrow (player direction)
        ctx.fillStyle = '#e94560';
        ctx.beginPath();
        ctx.moveTo(tipX, tipY);
        ctx.lineTo(base1X, base1Y);
        ctx.lineTo(base2X, base2Y);
        ctx.closePath();
        ctx.fill();

        // Draw player circle
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
        ctx.fill();

        // Draw pulsing glow
        const pulse = Math.sin(Date.now() * 0.003) * 0.5 + 0.5;
        ctx.strokeStyle = `rgba(233, 69, 96, ${pulse})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(centerX, centerY, 8 + pulse * 3, 0, Math.PI * 2);
        ctx.stroke();
    }

    drawCompass(ctx) {
        const compassSize = 20;
        const compassX = this.canvas.width - compassSize - 10;
        const compassY = compassSize + 10;

        // Draw compass circle
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(compassX, compassY, compassSize / 2, 0, Math.PI * 2);
        ctx.stroke();

        // Draw North indicator
        ctx.fillStyle = '#ff0000';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('N', compassX, compassY - compassSize / 2 - 8);

        // Draw cardinal directions
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.font = '10px Arial';
        ctx.fillText('S', compassX, compassY + compassSize / 2 + 8);
        ctx.fillText('E', compassX + compassSize / 2 + 8, compassY);
        ctx.fillText('W', compassX - compassSize / 2 - 8, compassY);
    }

    worldToMinimap(worldCoord, center) {
        // Convert world coordinate to minimap pixel coordinate
        const relativePos = worldCoord - (center === this.canvas.width / 2 ? this.playerPosition.x : this.playerPosition.z);
        return center + (relativePos / this.zoom);
    }

    hexToRgba(hex, alpha = 1) {
        // Remove # if present
        hex = hex.replace('#', '');

        // Parse RGB values
        const r = parseInt(hex.substring(0, 2), 16);
        const g = parseInt(hex.substring(2, 4), 16);
        const b = parseInt(hex.substring(4, 6), 16);

        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    // Public API
    updatePlayerPosition(x, z, rotation) {
        this.playerPosition = { x, z };
        this.playerRotation = rotation;
    }

    addPOI(poi) {
        // poi = { x, z, icon, color, name }
        this.pointsOfInterest.push(poi);
    }

    removePOI(index) {
        this.pointsOfInterest.splice(index, 1);
    }

    clearPOI() {
        this.pointsOfInterest = [];
    }

    updateNearbyEnemies(enemies) {
        // enemies = [{ x, z }, ...]
        this.nearbyEnemies = enemies;
    }

    zoomIn() {
        this.zoom = Math.max(5, this.zoom * 0.8);
    }

    zoomOut() {
        this.zoom = Math.min(100, this.zoom * 1.25);
    }

    toggle() {
        this.visible = !this.visible;
        this.container.style.display = this.visible ? 'block' : 'none';
    }

    show() {
        this.visible = true;
        this.container.style.display = 'block';
    }

    hide() {
        this.visible = false;
        this.container.style.display = 'none';
    }

    setOpacity(opacity) {
        this.opacity = Math.max(0, Math.min(1, opacity));
        this.container.style.opacity = this.opacity;
    }

    openFullMap() {
        // Trigger event to open full map UI
        if (window.worldMapUI) {
            window.worldMapUI.show();
        } else {
            console.warn('World Map UI not available');
        }
    }

    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }

        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Minimap;
} else {
    window.Minimap = Minimap;
}
