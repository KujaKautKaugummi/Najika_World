/**
 * Housing & Farming UI
 * Furniture placement, farming, fishing system
 */

class HousingUI {
    constructor() {
        this.apiBase = {
            housing: 'http://localhost:8001/api/housing',
            farming: 'http://localhost:8001/api/farming'
        };
        this.playerId = (typeof getPlayerId === 'function') ? getPlayerId() : 1;
        this.currentHouse = null;
        this.furnitureCatalog = [];
        this.farmPlots = [];
        this.createUI();
    }

    createUI() {
        this.modal = document.createElement('div');
        this.modal.id = 'housing-modal';
        this.modal.className = 'game-modal hidden';
        this.modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>🏠 Housing & Farming</h2>
                    <button class="close-btn" onclick="window.housingUI.hide()">✕</button>
                </div>

                <div class="modal-body">
                    <div class="tabs">
                        <button class="tab-btn active" onclick="window.housingUI.showTab('house')">🏠 House</button>
                        <button class="tab-btn" onclick="window.housingUI.showTab('farming')">🌾 Farming</button>
                        <button class="tab-btn" onclick="window.housingUI.showTab('fishing')">🎣 Fishing</button>
                    </div>

                    <!-- House Tab -->
                    <div id="house-tab" class="tab-content active">
                        <div class="house-info">
                            <h3>Your House</h3>
                            <div id="house-stats">
                                <p>Level: <span id="house-level">1</span></p>
                                <p>Furniture: <span id="furniture-count">0</span> / <span id="max-furniture">20</span></p>
                            </div>
                            <button class="action-btn" onclick="window.housingUI.upgradeHouse()">⬆️ Upgrade House</button>
                        </div>

                        <div class="furniture-section">
                            <h4>Furniture Catalog</h4>
                            <div id="furniture-catalog" class="furniture-grid"></div>
                        </div>

                        <div class="placed-furniture">
                            <h4>Placed Furniture</h4>
                            <div id="placed-furniture-list"></div>
                        </div>
                    </div>

                    <!-- Farming Tab -->
                    <div id="farming-tab" class="tab-content">
                        <div class="farm-info">
                            <h3>Your Farm</h3>
                            <p>Manage your crops and harvest them when ready!</p>
                        </div>

                        <div class="crop-catalog">
                            <h4>Available Crops</h4>
                            <div id="crop-catalog" class="crop-grid"></div>
                        </div>

                        <div class="farm-plots-section">
                            <h4>Farm Plots</h4>
                            <div id="farm-plots-grid" class="plots-grid"></div>
                        </div>
                    </div>

                    <!-- Fishing Tab -->
                    <div id="fishing-tab" class="tab-content">
                        <div class="fishing-info">
                            <h3>Fishing Spots</h3>
                            <p>Cast your line and catch some fish!</p>
                        </div>

                        <div id="fishing-spots-list"></div>

                        <div class="fishing-action">
                            <button class="action-btn big" onclick="window.housingUI.castFishingRod()">🎣 Cast Fishing Rod</button>
                        </div>

                        <div id="fishing-results"></div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.modal);
    }

    async show() {
        this.modal.classList.remove('hidden');
        await this.loadHouseData();
        await this.loadFarmData();
    }

    hide() {
        this.modal.classList.add('hidden');
    }

    showTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('#housing-modal .tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('#housing-modal .tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(`${tabName}-tab`).classList.add('active');
        event.target.classList.add('active');

        // Load data based on tab
        if (tabName === 'house') {
            this.loadHouseData();
        } else if (tabName === 'farming') {
            this.loadFarmData();
        } else if (tabName === 'fishing') {
            this.loadFishingSpots();
        }
    }

    // ========================================================================
    // HOUSE FUNCTIONS
    // ========================================================================

    async loadHouseData() {
        try {
            // Get house
            const houseRes = await fetch(`${this.apiBase.housing}/house/${this.playerId}`);
            this.currentHouse = await houseRes.json();

            // Update UI
            document.getElementById('house-level').textContent = this.currentHouse.level;
            document.getElementById('furniture-count').textContent = this.currentHouse.furniture.length;
            document.getElementById('max-furniture').textContent = this.currentHouse.max_furniture;

            // Load furniture catalog
            const catalogRes = await fetch(`${this.apiBase.housing}/furniture/catalog`);
            const catalogData = await catalogRes.json();
            this.furnitureCatalog = catalogData.catalog;

            this.renderFurnitureCatalog();
            this.renderPlacedFurniture();

        } catch (error) {
            console.error('Error loading house data:', error);
        }
    }

    renderFurnitureCatalog() {
        const catalog = document.getElementById('furniture-catalog');
        catalog.innerHTML = '';

        this.furnitureCatalog.forEach(item => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'furniture-item';
            itemDiv.innerHTML = `
                <div class="furniture-icon">${this.getFurnitureIcon(item.type)}</div>
                <h5>${item.name}</h5>
                <p class="category">${item.category}</p>
                <p class="cost">💰 ${item.cost} gold</p>
                <button class="action-btn small" onclick="window.housingUI.placeFurniture('${item.type}')">
                    Place
                </button>
            `;
            catalog.appendChild(itemDiv);
        });
    }

    renderPlacedFurniture() {
        const list = document.getElementById('placed-furniture-list');
        list.innerHTML = '';

        if (this.currentHouse.furniture.length === 0) {
            list.innerHTML = '<p class="empty-state">No furniture placed yet</p>';
            return;
        }

        this.currentHouse.furniture.forEach((furniture, index) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'placed-furniture-item';
            itemDiv.innerHTML = `
                <span>${this.getFurnitureIcon(furniture.type)} ${furniture.type}</span>
                <button class="action-btn danger small" onclick="window.housingUI.removeFurniture(${index})">
                    Remove
                </button>
            `;
            list.appendChild(itemDiv);
        });
    }

    getFurnitureIcon(type) {
        const icons = {
            'bed': '🛏️',
            'table': '🪑',
            'chair': '💺',
            'sofa': '🛋️',
            'bookshelf': '📚',
            'desk': '🖥️',
            'wardrobe': '👔',
            'lamp': '💡',
            'rug': '🧶',
            'plant': '🪴',
            'painting': '🖼️',
            'tv': '📺',
            'fireplace': '🔥',
            'kitchen_counter': '🍳',
            'refrigerator': '🧊'
        };
        return icons[type] || '📦';
    }

    async placeFurniture(furnitureType) {
        if (this.currentHouse.furniture.length >= this.currentHouse.max_furniture) {
            if (typeof notify === 'function') notify('🏠 House is full! Upgrade to place more furniture.', 'warning'); else console.warn('House full');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase.housing}/furniture/place`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    player_id: this.playerId,
                    furniture: {
                        type: furnitureType,
                        position: {x: Math.random() * 10, y: 0, z: Math.random() * 10},
                        rotation: Math.random() * 360,
                        scale: 1.0
                    }
                })
            });

            const data = await response.json();
            if (data.success) {
                if (typeof notify === 'function') notify(`✅ ${furnitureType} placed!`, 'success');
                await this.loadHouseData();
            }
        } catch (error) {
            console.error('Error placing furniture:', error);
            if (typeof notify === 'function') notify('Failed to place furniture', 'error');
        }
    }

    async removeFurniture(index) {
        try {
            const response = await fetch(`${this.apiBase.housing}/furniture/remove`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    player_id: this.playerId,
                    furniture_index: index
                })
            });

            const data = await response.json();
            if (data.success) {
                if (typeof notify === 'function') notify('✅ Furniture removed!', 'success');
                await this.loadHouseData();
            }
        } catch (error) {
            console.error('Error removing furniture:', error);
        }
    }

    async upgradeHouse() {
        if (this.currentHouse.level >= 10) {
            if (typeof notify === 'function') notify('🏠 House is already at max level!', 'info');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase.housing}/upgrade`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({player_id: this.playerId})
            });

            const data = await response.json();
            if (data.success) {
                if (typeof notify === 'function') notify(`✅ House upgraded to level ${data.level}! Max furniture: ${data.max_furniture}`, 'success');
                await this.loadHouseData();
            }
        } catch (error) {
            console.error('Error upgrading house:', error);
        }
    }

    // ========================================================================
    // FARMING FUNCTIONS
    // ========================================================================

    async loadFarmData() {
        try {
            // Get farm plots
            const plotsRes = await fetch(`${this.apiBase.farming}/plots/${this.playerId}`);
            this.farmPlots = await plotsRes.json();

            // Get crop catalog
            const catalogRes = await fetch(`${this.apiBase.farming}/crops/catalog`);
            const catalogData = await catalogRes.json();
            this.cropCatalog = catalogData.crops;

            this.renderCropCatalog();
            this.renderFarmPlots();

        } catch (error) {
            console.error('Error loading farm data:', error);
        }
    }

    renderCropCatalog() {
        const catalog = document.getElementById('crop-catalog');
        catalog.innerHTML = '';

        this.cropCatalog.forEach(crop => {
            const cropDiv = document.createElement('div');
            cropDiv.className = 'crop-item';
            cropDiv.innerHTML = `
                <div class="crop-icon">${this.getCropIcon(crop.type)}</div>
                <h5>${crop.name}</h5>
                <p>⏱️ ${crop.growth_time_hours}h</p>
                <p>💰 ${crop.sell_price} gold</p>
            `;
            catalog.appendChild(cropDiv);
        });
    }

    renderFarmPlots() {
        const grid = document.getElementById('farm-plots-grid');
        grid.innerHTML = '';

        this.farmPlots.forEach(plot => {
            const plotDiv = document.createElement('div');
            plotDiv.className = `farm-plot ${plot.crop_type ? 'planted' : 'empty'}`;

            if (plot.crop_type) {
                plotDiv.innerHTML = `
                    <div class="plot-header">
                        <span>Plot ${plot.plot_index + 1}</span>
                        <span class="growth-stage">Stage ${plot.growth_stage}/4</span>
                    </div>
                    <div class="crop-display">
                        ${this.getCropIcon(plot.crop_type)}
                        <p>${plot.crop_type}</p>
                    </div>
                    ${plot.ready_to_harvest ?
                        `<button class="action-btn success" onclick="window.housingUI.harvestCrop(${plot.id})">✂️ Harvest</button>` :
                        `<button class="action-btn" onclick="window.housingUI.waterCrop(${plot.id})">💧 Water</button>`
                    }
                `;
            } else {
                plotDiv.innerHTML = `
                    <div class="plot-header">
                        <span>Plot ${plot.plot_index + 1}</span>
                        <span class="empty-label">Empty</span>
                    </div>
                    <div class="empty-plot">
                        🌱
                    </div>
                    <select id="crop-select-${plot.plot_index}" class="crop-select">
                        <option value="">Select crop...</option>
                        ${this.cropCatalog.map(c => `<option value="${c.type}">${c.name}</option>`).join('')}
                    </select>
                    <button class="action-btn" onclick="window.housingUI.plantCrop(${plot.plot_index})">🌱 Plant</button>
                `;
            }
            grid.appendChild(plotDiv);
        });
    }

    getCropIcon(cropType) {
        const icons = {
            'wheat': '🌾',
            'corn': '🌽',
            'tomato': '🍅',
            'potato': '🥔',
            'carrot': '🥕',
            'lettuce': '🥬',
            'pumpkin': '🎃',
            'strawberry': '🍓'
        };
        return icons[cropType] || '🌱';
    }

    async plantCrop(plotIndex) {
        const select = document.getElementById(`crop-select-${plotIndex}`);
        const cropType = select.value;

        if (!cropType) {
            if (typeof notify === 'function') notify('🌱 Please select a crop!', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase.farming}/plant`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    player_id: this.playerId,
                    plot_index: plotIndex,
                    crop_type: cropType
                })
            });

            const data = await response.json();
            if (data.success) {
                if (typeof notify === 'function') notify(`✅ Planted ${cropType}!`, 'success');
                await this.loadFarmData();
            }
        } catch (error) {
            console.error('Error planting crop:', error);
        }
    }

    async waterCrop(plotId) {
        try {
            const response = await fetch(`${this.apiBase.farming}/water/${plotId}`, {
                method: 'POST'
            });

            const data = await response.json();
            if (data.success) {
                if (data.ready_to_harvest) {
                    if (typeof notify === 'function') notify('✅ Crop is ready to harvest!', 'success');
                } else {
                    if (typeof notify === 'function') notify(`💧 Watered! Growth stage: ${data.growth_stage}/4`, 'info');
                }
                await this.loadFarmData();
            }
        } catch (error) {
            console.error('Error watering crop:', error);
        }
    }

    async harvestCrop(plotId) {
        try {
            const response = await fetch(`${this.apiBase.farming}/harvest`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    player_id: this.playerId,
                    plot_id: plotId
                })
            });

            const data = await response.json();
            if (data.success) {
                if (typeof notify === 'function') notify(`✅ Harvested ${data.quantity}x ${data.crop}! Earned ${data.gold_earned} gold!`, 'success');
                await this.loadFarmData();
            }
        } catch (error) {
            console.error('Error harvesting crop:', error);
        }
    }

    // ========================================================================
    // FISHING FUNCTIONS
    // ========================================================================

    async loadFishingSpots() {
        try {
            const response = await fetch(`${this.apiBase.farming}/fishing/spots`);
            const data = await response.json();

            const list = document.getElementById('fishing-spots-list');
            list.innerHTML = '';

            data.fishing_spots.forEach(spot => {
                const spotDiv = document.createElement('div');
                spotDiv.className = 'fishing-spot';
                spotDiv.innerHTML = `
                    <h4>🎣 ${spot.location_name}</h4>
                    <p>Fish: ${spot.fish_pool.join(', ')}</p>
                    <p>Rare chance: ${(spot.rare_fish_chance * 100).toFixed(1)}%</p>
                    <button class="action-btn" onclick="window.housingUI.castAtSpot(${spot.id})">Cast Here</button>
                `;
                list.appendChild(spotDiv);
            });

            this.fishingSpots = data.fishing_spots;

        } catch (error) {
            console.error('Error loading fishing spots:', error);
        }
    }

    async castAtSpot(spotId) {
        const results = document.getElementById('fishing-results');
        results.innerHTML = '<p class="loading">🎣 Casting...</p>';

        try {
            const response = await fetch(`${this.apiBase.farming}/fishing/cast`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    player_id: this.playerId,
                    fishing_spot_id: spotId
                })
            });

            const data = await response.json();

            if (data.success) {
                const rarityClass = data.is_rare ? 'rare' : data.quality.toLowerCase();
                results.innerHTML = `
                    <div class="fishing-result ${rarityClass}">
                        <h3>🎣 ${data.message}</h3>
                        <div class="fish-details">
                            <p class="fish-name">${data.fish}</p>
                            <p>Size: ${data.size}</p>
                            <p>Quality: ${data.quality}</p>
                            ${data.is_rare ? '<p class="rare-badge">✨ RARE ✨</p>' : ''}
                            <p class="gold-value">💰 ${data.gold_value} gold</p>
                        </div>
                    </div>
                `;
            }

        } catch (error) {
            console.error('Error casting rod:', error);
            results.innerHTML = '<p class="error">Failed to cast fishing rod</p>';
        }
    }

    async castFishingRod() {
        if (!this.fishingSpots || this.fishingSpots.length === 0) {
            await this.loadFishingSpots();
        }

        if (this.fishingSpots.length > 0) {
            // Cast at random spot
            const randomSpot = this.fishingSpots[Math.floor(Math.random() * this.fishingSpots.length)];
            await this.castAtSpot(randomSpot.id);
        }
    }
}

// Initialize on window load
window.addEventListener('load', () => {
    window.housingUI = new HousingUI();
    console.log('✅ Housing UI initialized!');
});
