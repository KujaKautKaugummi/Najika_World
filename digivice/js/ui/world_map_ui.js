/**
 * World Map UI System
 * 9600×9600 Persistent World Map with 8 Biome Regions
 * Shows regions, fast travel points, player position
 */

class WorldMapUI {
    constructor() {
        this.apiBase = 'http://localhost:8001/api/world-map';
        this.playerId = (typeof getPlayerId === 'function') ? getPlayerId() : 1;

        // Map state
        this.worldData = null;
        this.regions = [];
        this.travelPoints = [];
        this.playerPosition = null;

        // Canvas settings
        this.scale = 0.05; // 9600 → 480px (fits in UI)
        this.offsetX = 0;
        this.offsetY = 0;
        this.isDragging = false;
        this.lastMouseX = 0;
        this.lastMouseY = 0;

        // Selected region
        this.selectedRegion = null;
        this.hoveredTravelPoint = null;

        this.init();
    }

    async init() {
        console.log('🗺️ Initializing World Map UI...');
        await this.loadWorldData();
        await this.loadPlayerPosition();
        await this.loadTravelPoints();
    }

    async loadWorldData() {
        try {
            const response = await fetch(`${this.apiBase}/map`);
            const data = await response.json();
            this.worldData = data;
            this.regions = data.regions || [];
            console.log(`✅ Loaded ${this.regions.length} regions`);
        } catch (error) {
            console.error('❌ Failed to load world map:', error);
        }
    }

    async loadPlayerPosition() {
        try {
            const response = await fetch(`${this.apiBase}/position/${this.playerId}`);
            this.playerPosition = await response.json();
            console.log('✅ Loaded player position:', this.playerPosition);
        } catch (error) {
            console.error('❌ Failed to load player position:', error);
        }
    }

    async loadTravelPoints() {
        try {
            const response = await fetch(`${this.apiBase}/travel-points?player_id=${this.playerId}`);
            const data = await response.json();
            this.travelPoints = data.travel_points || [];
            console.log(`✅ Loaded ${this.travelPoints.length} travel points`);
        } catch (error) {
            console.error('❌ Failed to load travel points:', error);
        }
    }

    show() {
        if (this.modal) {
            this.modal.style.display = 'block';
            this.render();
            return;
        }

        this.createUI();
        this.render();
    }

    hide() {
        if (this.modal) {
            this.modal.style.display = 'none';
        }
    }

    createUI() {
        // Create modal
        this.modal = document.createElement('div');
        this.modal.id = 'world-map-modal';
        this.modal.style.cssText = `
            display: block;
            position: fixed;
            z-index: 10000;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 90vw;
            max-width: 1200px;
            height: 85vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 3px solid #0f3460;
            border-radius: 15px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.8);
            overflow: hidden;
        `;

        this.modal.innerHTML = `
            <div style="
                display: flex;
                flex-direction: column;
                height: 100%;
                color: #e8e8e8;
            ">
                <!-- Header -->
                <div style="
                    background: linear-gradient(90deg, #0f3460 0%, #16213e 100%);
                    padding: 15px 25px;
                    border-bottom: 2px solid #e94560;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <h2 style="
                        margin: 0;
                        font-size: 28px;
                        color: #e94560;
                        text-shadow: 0 0 10px rgba(233,69,96,0.5);
                    ">🗺️ World Map - Najika's World</h2>
                    <button onclick="window.worldMapUI.hide()" style="
                        background: #e94560;
                        border: none;
                        color: white;
                        font-size: 24px;
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        cursor: pointer;
                        transition: all 0.3s;
                    ">×</button>
                </div>

                <!-- Content -->
                <div style="
                    display: flex;
                    flex: 1;
                    overflow: hidden;
                ">
                    <!-- Map Canvas -->
                    <div id="map-canvas-container" style="
                        flex: 1;
                        background: #0a0a15;
                        border-right: 2px solid #0f3460;
                        position: relative;
                        overflow: hidden;
                    ">
                        <canvas id="world-map-canvas" style="
                            cursor: grab;
                            display: block;
                        "></canvas>

                        <!-- Map Controls -->
                        <div style="
                            position: absolute;
                            top: 15px;
                            right: 15px;
                            background: rgba(15,52,96,0.9);
                            padding: 10px;
                            border-radius: 8px;
                            border: 1px solid #e94560;
                        ">
                            <button onclick="window.worldMapUI.zoomIn()" style="
                                background: #0f3460;
                                border: 1px solid #e94560;
                                color: white;
                                padding: 5px 12px;
                                margin: 3px;
                                border-radius: 5px;
                                cursor: pointer;
                            ">🔍 +</button>
                            <button onclick="window.worldMapUI.zoomOut()" style="
                                background: #0f3460;
                                border: 1px solid #e94560;
                                color: white;
                                padding: 5px 12px;
                                margin: 3px;
                                border-radius: 5px;
                                cursor: pointer;
                            ">🔍 -</button>
                            <button onclick="window.worldMapUI.resetView()" style="
                                background: #0f3460;
                                border: 1px solid #e94560;
                                color: white;
                                padding: 5px 12px;
                                margin: 3px;
                                border-radius: 5px;
                                cursor: pointer;
                            ">🎯 Reset</button>
                        </div>

                        <!-- Player Info -->
                        <div id="player-info-display" style="
                            position: absolute;
                            bottom: 15px;
                            left: 15px;
                            background: rgba(15,52,96,0.9);
                            padding: 12px 18px;
                            border-radius: 8px;
                            border: 1px solid #e94560;
                            color: white;
                        ">
                            <div style="font-weight: bold; margin-bottom: 5px;">📍 Your Position</div>
                            <div id="player-coords">Loading...</div>
                        </div>
                    </div>

                    <!-- Side Panel -->
                    <div style="
                        width: 350px;
                        background: #16213e;
                        padding: 20px;
                        overflow-y: auto;
                    ">
                        <h3 style="
                            color: #e94560;
                            margin-top: 0;
                            border-bottom: 2px solid #0f3460;
                            padding-bottom: 10px;
                        ">Region Information</h3>

                        <div id="region-info-panel">
                            <p style="color: #aaa;">Click on a region to see details</p>
                        </div>

                        <h3 style="
                            color: #e94560;
                            margin-top: 30px;
                            border-bottom: 2px solid #0f3460;
                            padding-bottom: 10px;
                        ">Fast Travel Points</h3>

                        <div id="travel-points-list">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                </div>

                <!-- Footer Stats -->
                <div style="
                    background: linear-gradient(90deg, #0f3460 0%, #16213e 100%);
                    padding: 12px 25px;
                    border-top: 2px solid #e94560;
                    display: flex;
                    justify-content: space-between;
                    font-size: 14px;
                ">
                    <span>🌍 World Size: 9600×9600</span>
                    <span>🗻 Center: Götterfels Mountain</span>
                    <span>🏞️ Regions: ${this.regions.length}</span>
                    <span>🚩 Travel Points: ${this.travelPoints.length}</span>
                </div>
            </div>
        `;

        document.body.appendChild(this.modal);

        // Setup canvas
        this.canvas = document.getElementById('world-map-canvas');
        this.ctx = this.canvas.getContext('2d');

        // Set canvas size
        const container = document.getElementById('map-canvas-container');
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;

        // Add event listeners
        this.setupEventListeners();

        // Populate travel points list
        this.updateTravelPointsList();
    }

    setupEventListeners() {
        // Mouse dragging
        this.canvas.addEventListener('mousedown', (e) => {
            this.isDragging = true;
            this.lastMouseX = e.clientX;
            this.lastMouseY = e.clientY;
            this.canvas.style.cursor = 'grabbing';
        });

        this.canvas.addEventListener('mousemove', (e) => {
            if (this.isDragging) {
                const dx = e.clientX - this.lastMouseX;
                const dy = e.clientY - this.lastMouseY;
                this.offsetX += dx;
                this.offsetY += dy;
                this.lastMouseX = e.clientX;
                this.lastMouseY = e.clientY;
                this.render();
            } else {
                // Check hover on travel points
                this.checkTravelPointHover(e);
            }
        });

        this.canvas.addEventListener('mouseup', () => {
            this.isDragging = false;
            this.canvas.style.cursor = 'grab';
        });

        this.canvas.addEventListener('mouseleave', () => {
            this.isDragging = false;
            this.canvas.style.cursor = 'grab';
        });

        // Click for region selection
        this.canvas.addEventListener('click', (e) => {
            this.handleMapClick(e);
        });

        // Resize handler
        window.addEventListener('resize', () => {
            if (this.canvas && this.modal.style.display === 'block') {
                const container = document.getElementById('map-canvas-container');
                this.canvas.width = container.clientWidth;
                this.canvas.height = container.clientHeight;
                this.render();
            }
        });
    }

    checkTravelPointHover(e) {
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        let hovering = false;
        for (const point of this.travelPoints) {
            const x = (point.position.x * this.scale) + this.offsetX + (this.canvas.width / 2);
            const y = (point.position.y * this.scale) + this.offsetY + (this.canvas.height / 2);

            const dist = Math.sqrt((mouseX - x) ** 2 + (mouseY - y) ** 2);
            if (dist < 15) {
                this.hoveredTravelPoint = point;
                this.canvas.style.cursor = 'pointer';
                hovering = true;
                break;
            }
        }

        if (!hovering && !this.isDragging) {
            this.hoveredTravelPoint = null;
            this.canvas.style.cursor = 'grab';
        }

        this.render();
    }

    handleMapClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Check travel point click
        for (const point of this.travelPoints) {
            const x = (point.position.x * this.scale) + this.offsetX + (this.canvas.width / 2);
            const y = (point.position.y * this.scale) + this.offsetY + (this.canvas.height / 2);

            const dist = Math.sqrt((mouseX - x) ** 2 + (mouseY - y) ** 2);
            if (dist < 15) {
                this.fastTravel(point);
                return;
            }
        }

        // Check region click
        for (const region of this.regions) {
            const x = (region.position.x * this.scale) + this.offsetX + (this.canvas.width / 2);
            const y = (region.position.y * this.scale) + this.offsetY + (this.canvas.height / 2);
            const w = region.position.width * this.scale;
            const h = region.position.height * this.scale;

            if (mouseX >= x && mouseX <= x + w && mouseY >= y && mouseY <= y + h) {
                this.selectRegion(region);
                return;
            }
        }
    }

    selectRegion(region) {
        this.selectedRegion = region;
        this.updateRegionInfo(region);
        this.render();
    }

    updateRegionInfo(region) {
        const panel = document.getElementById('region-info-panel');
        if (!panel) return;

        panel.innerHTML = `
            <div style="
                background: rgba(15,52,96,0.5);
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #e94560;
            ">
                <h4 style="margin-top: 0; color: #e94560;">${region.name}</h4>
                <p><strong>Biome:</strong> ${this.formatBiome(region.biome)}</p>
                <p><strong>Slime Color:</strong> ${region.slime_color}</p>
                <p><strong>Climate:</strong> ${region.climate}</p>

                <p style="margin-top: 15px;"><strong>Features:</strong></p>
                <ul style="margin: 5px 0; padding-left: 20px;">
                    ${region.features.map(f => `<li>${f}</li>`).join('')}
                </ul>

                <p style="margin-top: 15px;"><strong>Dangers:</strong></p>
                <ul style="margin: 5px 0; padding-left: 20px; color: #ff6b6b;">
                    ${region.dangers.map(d => `<li>${d}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    formatBiome(biome) {
        const biomeMap = {
            'desert': '🏜️ Desert',
            'forest': '🌲 Forest',
            'tundra': '❄️ Tundra',
            'volcanic': '🌋 Volcanic',
            'sky_islands': '☁️ Sky Islands',
            'plains': '⚡ Thunder Plains',
            'swamp': '🌑 Swamp',
            'coastal': '🌊 Coastal'
        };
        return biomeMap[biome] || biome;
    }

    updateTravelPointsList() {
        const list = document.getElementById('travel-points-list');
        if (!list) return;

        list.innerHTML = this.travelPoints.map(point => `
            <div style="
                background: ${point.is_locked ? 'rgba(100,50,50,0.3)' : 'rgba(15,52,96,0.5)'};
                padding: 10px;
                margin: 8px 0;
                border-radius: 6px;
                border: 1px solid ${point.is_locked ? '#ff6b6b' : '#0f3460'};
                ${point.is_locked ? 'opacity: 0.6;' : 'cursor: pointer;'}
            " ${point.is_locked ? '' : `onclick="window.worldMapUI.fastTravelById(${point.id})"`}>
                <div style="font-weight: bold;">
                    ${point.icon} ${point.name}
                </div>
                <div style="font-size: 12px; color: #aaa; margin-top: 3px;">
                    ${point.type} ${point.is_locked ? '🔒 Locked' : '✅ Unlocked'}
                </div>
                ${point.is_locked ? `
                    <div style="font-size: 11px; color: #ff6b6b; margin-top: 3px;">
                        ${point.unlock_requirement}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    async fastTravelById(pointId) {
        const point = this.travelPoints.find(p => p.id === pointId);
        if (point) {
            await this.fastTravel(point);
        }
    }

    async fastTravel(point) {
        if (point.is_locked) {
            if (typeof notify === 'function') notify(`🔒 Gesperrt! Voraussetzung: ${point.unlock_requirement}`, 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/travel`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    travel_point_id: point.id
                })
            });

            const result = await response.json();

            if (result.success) {
                if (typeof notify === 'function') notify(`✅ Reise nach ${result.travel_point.name} (${result.region.name})`, 'success');
                await this.loadPlayerPosition();
                this.render();
                this.updatePlayerInfoDisplay();
            } else {
                if (typeof notify === 'function') notify('❌ Schnellreise fehlgeschlagen!', 'error');
            }
        } catch (error) {
            console.error('❌ Fast travel error:', error);
            if (typeof notify === 'function') notify('❌ Schnellreise fehlgeschlagen!', 'error');
        }
    }

    updatePlayerInfoDisplay() {
        const display = document.getElementById('player-coords');
        if (!display || !this.playerPosition) return;

        display.innerHTML = `
            <div>X: ${Math.round(this.playerPosition.world_x)}</div>
            <div>Y: ${Math.round(this.playerPosition.world_y)}</div>
            <div>Z: ${Math.round(this.playerPosition.world_z)}</div>
            ${this.playerPosition.region_name ? `<div>Region: ${this.playerPosition.region_name}</div>` : ''}
        `;
    }

    zoomIn() {
        this.scale *= 1.2;
        this.render();
    }

    zoomOut() {
        this.scale /= 1.2;
        this.render();
    }

    resetView() {
        this.scale = 0.05;
        this.offsetX = 0;
        this.offsetY = 0;
        this.render();
    }

    render() {
        if (!this.ctx || !this.canvas) return;

        const ctx = this.ctx;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;

        // Clear canvas
        ctx.fillStyle = '#0a0a15';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw grid
        this.drawGrid(ctx, centerX, centerY);

        // Draw center mountain (Götterfels)
        this.drawCenterMountain(ctx, centerX, centerY);

        // Draw regions
        for (const region of this.regions) {
            this.drawRegion(ctx, region, centerX, centerY);
        }

        // Draw travel points
        for (const point of this.travelPoints) {
            this.drawTravelPoint(ctx, point, centerX, centerY);
        }

        // Draw player position
        if (this.playerPosition) {
            this.drawPlayerPosition(ctx, centerX, centerY);
        }

        // Update player info
        this.updatePlayerInfoDisplay();
    }

    drawGrid(ctx, centerX, centerY) {
        ctx.strokeStyle = 'rgba(255,255,255,0.05)';
        ctx.lineWidth = 1;

        const gridSize = 1000; // Draw grid every 1000 units
        for (let i = 0; i <= 9600; i += gridSize) {
            // Vertical lines
            const x = (i * this.scale) + this.offsetX + centerX;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, this.canvas.height);
            ctx.stroke();

            // Horizontal lines
            const y = (i * this.scale) + this.offsetY + centerY;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(this.canvas.width, y);
            ctx.stroke();
        }
    }

    drawCenterMountain(ctx, centerX, centerY) {
        const x = (3300 * this.scale) + this.offsetX + centerX;
        const y = (3300 * this.scale) + this.offsetY + centerY;
        const w = 3000 * this.scale;
        const h = 3000 * this.scale;

        // Mountain background
        ctx.fillStyle = 'rgba(100,50,30,0.6)';
        ctx.fillRect(x, y, w, h);

        // Mountain border
        ctx.strokeStyle = '#d4a574';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, w, h);

        // Label
        if (this.scale > 0.03) {
            ctx.fillStyle = '#fff';
            ctx.font = `${Math.max(12, 14 * this.scale * 20)}px Arial`;
            ctx.textAlign = 'center';
            ctx.fillText('🗻 Götterfels', x + w/2, y + h/2);
            ctx.fillText('(Schwarze Mühle)', x + w/2, y + h/2 + 20);
        }
    }

    drawRegion(ctx, region, centerX, centerY) {
        const x = (region.position.x * this.scale) + this.offsetX + centerX;
        const y = (region.position.y * this.scale) + this.offsetY + centerY;
        const w = region.position.width * this.scale;
        const h = region.position.height * this.scale;

        // Region color based on biome
        const biomeColors = {
            'desert': 'rgba(255,200,100,0.3)',
            'forest': 'rgba(50,150,50,0.3)',
            'tundra': 'rgba(150,200,255,0.3)',
            'volcanic': 'rgba(255,50,50,0.3)',
            'sky_islands': 'rgba(200,220,255,0.3)',
            'plains': 'rgba(255,255,100,0.3)',
            'swamp': 'rgba(100,50,150,0.3)',
            'coastal': 'rgba(100,150,255,0.3)'
        };

        // Fill region
        ctx.fillStyle = biomeColors[region.biome] || 'rgba(100,100,100,0.3)';
        ctx.fillRect(x, y, w, h);

        // Border
        const isSelected = this.selectedRegion && this.selectedRegion.id === region.id;
        ctx.strokeStyle = isSelected ? '#e94560' : 'rgba(255,255,255,0.3)';
        ctx.lineWidth = isSelected ? 3 : 1;
        ctx.strokeRect(x, y, w, h);

        // Label
        if (this.scale > 0.02) {
            ctx.fillStyle = '#fff';
            ctx.font = `${Math.max(10, 12 * this.scale * 20)}px Arial`;
            ctx.textAlign = 'center';
            ctx.fillText(region.name, x + w/2, y + h/2);
        }
    }

    drawTravelPoint(ctx, point, centerX, centerY) {
        const x = (point.position.x * this.scale) + this.offsetX + centerX;
        const y = (point.position.y * this.scale) + this.offsetY + centerY;

        const isHovered = this.hoveredTravelPoint && this.hoveredTravelPoint.id === point.id;

        // Draw icon
        if (point.is_locked) {
            // Locked point
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(x, y, isHovered ? 10 : 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#000';
            ctx.font = `${isHovered ? 14 : 12}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('🔒', x, y);
        } else {
            // Unlocked point
            ctx.fillStyle = '#4CAF50';
            ctx.beginPath();
            ctx.arc(x, y, isHovered ? 12 : 10, 0, Math.PI * 2);
            ctx.fill();

            // Pulsing effect for unlocked
            if (isHovered) {
                ctx.strokeStyle = 'rgba(76,175,80,0.5)';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(x, y, 16, 0, Math.PI * 2);
                ctx.stroke();
            }
        }

        // Label
        if (this.scale > 0.03 || isHovered) {
            ctx.fillStyle = '#fff';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';
            ctx.fillText(point.name, x, y + 15);
        }

        // Tooltip on hover
        if (isHovered) {
            this.drawTooltip(ctx, point, x, y - 25);
        }
    }

    drawTooltip(ctx, point, x, y) {
        const text = `${point.icon} ${point.name}\n${point.type}`;
        const lines = text.split('\n');

        const padding = 8;
        const lineHeight = 14;
        const maxWidth = Math.max(...lines.map(l => ctx.measureText(l).width));
        const boxWidth = maxWidth + padding * 2;
        const boxHeight = lines.length * lineHeight + padding * 2;

        // Background
        ctx.fillStyle = 'rgba(15,52,96,0.95)';
        ctx.fillRect(x - boxWidth/2, y - boxHeight, boxWidth, boxHeight);

        // Border
        ctx.strokeStyle = '#e94560';
        ctx.lineWidth = 1;
        ctx.strokeRect(x - boxWidth/2, y - boxHeight, boxWidth, boxHeight);

        // Text
        ctx.fillStyle = '#fff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        lines.forEach((line, i) => {
            ctx.fillText(line, x, y - boxHeight + padding + lineHeight/2 + i * lineHeight);
        });
    }

    drawPlayerPosition(ctx, centerX, centerY) {
        const x = (this.playerPosition.world_x * this.scale) + this.offsetX + centerX;
        const y = (this.playerPosition.world_y * this.scale) + this.offsetY + centerY;

        // Pulsing circle
        const pulseSize = 20 + Math.sin(Date.now() / 300) * 5;

        // Outer glow
        ctx.fillStyle = 'rgba(233,69,96,0.3)';
        ctx.beginPath();
        ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
        ctx.fill();

        // Player marker
        ctx.fillStyle = '#e94560';
        ctx.beginPath();
        ctx.arc(x, y, 12, 0, Math.PI * 2);
        ctx.fill();

        // Inner dot
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fill();

        // Label
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText('YOU', x, y + 18);
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    window.worldMapUI = new WorldMapUI();
    console.log('✅ World Map UI ready!');
});
