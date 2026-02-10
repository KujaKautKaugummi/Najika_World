/**
 * Full World Map UI
 * Vollbildkarte mit 3D-Visualisierung
 *
 * Features:
 * - Taste 'M' öffnet/schließt die Karte
 * - 3D-Visualisierung mit THREE.js
 * - Zoom In/Out mit Mausrad
 * - Pan mit Maus-Drag
 * - Klick auf Locations für Details
 * - Fast Travel zu freigeschalteten Punkten
 * - Region Information Panel
 * - Filter für Biome/Cities/POIs
 * - Search Funktion
 */

class WorldMapFullUI {
    constructor() {
        // UI State
        this.isOpen = false;
        this.selectedRegion = null;
        this.selectedCity = null;

        // 3D Renderer
        this.renderer3D = null;

        // Data
        this.regionsData = null;
        this.biomesData = null;
        this.citiesData = null;
        this.travelPoints = [];
        this.playerPosition = { x: 4800, z: 4800 };

        // DOM Elements
        this.modal = null;
        this.container3D = null;
        this.sidePanel = null;

        // Filters
        this.filters = {
            showCities: true,
            showTravelPoints: true,
            showPOI: true,
            biomeFilter: 'all'
        };

        this.init();
    }

    async init() {
        console.log('🗺️ Initializing Full World Map UI...');

        // Load data
        await this.loadWorldData();

        // Create UI
        this.createUI();

        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();

        console.log('✅ Full World Map UI initialized!');
    }

    async loadWorldData() {
        try {
            // Load regions
            const regionsResponse = await fetch('/data/regions.json');
            this.regionsData = await regionsResponse.json();

            // Load biomes
            const biomesResponse = await fetch('/data/biomes.json');
            this.biomesData = await biomesResponse.json();

            // Load cities
            const citiesResponse = await fetch('/data/cities.json');
            this.citiesData = await citiesResponse.json();

            console.log('✅ World Map data loaded');
        } catch (error) {
            console.error('❌ Failed to load world map data:', error);
        }
    }

    createUI() {
        // Create modal overlay
        this.modal = document.createElement('div');
        this.modal.id = 'world-map-full-modal';
        this.modal.style.cssText = `
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            overflow: hidden;
        `;

        // Create main container
        const mainContainer = document.createElement('div');
        mainContainer.style.cssText = `
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
        `;

        // Create header
        const header = this.createHeader();
        mainContainer.appendChild(header);

        // Create content area (3D view + side panel)
        const contentArea = document.createElement('div');
        contentArea.style.cssText = `
            flex: 1;
            display: flex;
            overflow: hidden;
        `;

        // Create 3D container
        this.container3D = document.createElement('div');
        this.container3D.id = 'world-map-3d-container';
        this.container3D.style.cssText = `
            flex: 1;
            position: relative;
            background: #0a0a15;
        `;
        contentArea.appendChild(this.container3D);

        // Create side panel
        this.sidePanel = this.createSidePanel();
        contentArea.appendChild(this.sidePanel);

        mainContainer.appendChild(contentArea);

        // Create footer
        const footer = this.createFooter();
        mainContainer.appendChild(footer);

        this.modal.appendChild(mainContainer);
        document.body.appendChild(this.modal);
    }

    createHeader() {
        const header = document.createElement('div');
        header.style.cssText = `
            background: linear-gradient(90deg, #0f3460 0%, #16213e 100%);
            padding: 15px 25px;
            border-bottom: 2px solid #e94560;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #e8e8e8;
        `;

        // Title
        const title = document.createElement('h2');
        title.textContent = '🗺️ World Map - Najika\'s World (9600×9600)';
        title.style.cssText = `
            margin: 0;
            font-size: 24px;
            color: #e94560;
            text-shadow: 0 0 10px rgba(233,69,96,0.5);
        `;
        header.appendChild(title);

        // Controls
        const controls = document.createElement('div');
        controls.style.cssText = `
            display: flex;
            gap: 10px;
            align-items: center;
        `;

        // Search input
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search location...';
        searchInput.style.cssText = `
            background: rgba(15, 52, 96, 0.5);
            border: 1px solid #0f3460;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 14px;
            width: 200px;
        `;
        searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        controls.appendChild(searchInput);

        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✕';
        closeBtn.style.cssText = `
            background: #e94560;
            border: none;
            color: white;
            font-size: 24px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s;
        `;
        closeBtn.addEventListener('click', () => this.close());
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.background = '#ff5570';
            closeBtn.style.transform = 'scale(1.1)';
        });
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.background = '#e94560';
            closeBtn.style.transform = 'scale(1)';
        });
        controls.appendChild(closeBtn);

        header.appendChild(controls);

        return header;
    }

    createSidePanel() {
        const panel = document.createElement('div');
        panel.style.cssText = `
            width: 350px;
            background: #16213e;
            padding: 20px;
            overflow-y: auto;
            border-left: 2px solid #0f3460;
        `;

        // Filters section
        const filtersSection = this.createFiltersSection();
        panel.appendChild(filtersSection);

        // Region info section
        const regionInfo = document.createElement('div');
        regionInfo.id = 'region-info-panel';
        regionInfo.innerHTML = `
            <h3 style="
                color: #e94560;
                margin-top: 20px;
                border-bottom: 2px solid #0f3460;
                padding-bottom: 10px;
            ">Region Information</h3>
            <p style="color: #aaa; font-size: 14px;">Click on a region to see details</p>
        `;
        panel.appendChild(regionInfo);

        // Travel points section
        const travelSection = this.createTravelPointsSection();
        panel.appendChild(travelSection);

        // Legend section
        const legend = this.createLegend();
        panel.appendChild(legend);

        return panel;
    }

    createFiltersSection() {
        const section = document.createElement('div');
        section.innerHTML = `
            <h3 style="
                color: #e94560;
                margin-top: 0;
                border-bottom: 2px solid #0f3460;
                padding-bottom: 10px;
            ">Filters</h3>
        `;

        // Create checkboxes for filters
        const filters = [
            { id: 'showCities', label: 'Cities', icon: '🏛️' },
            { id: 'showTravelPoints', label: 'Travel Points', icon: '🚩' },
            { id: 'showPOI', label: 'Points of Interest', icon: '⭐' }
        ];

        filters.forEach(filter => {
            const checkbox = this.createCheckbox(filter.id, filter.label, filter.icon);
            section.appendChild(checkbox);
        });

        // Biome filter dropdown
        const biomeFilter = document.createElement('div');
        biomeFilter.style.cssText = 'margin-top: 15px;';
        biomeFilter.innerHTML = `
            <label style="color: #e8e8e8; font-size: 14px; display: block; margin-bottom: 5px;">
                🏞️ Biome Filter:
            </label>
            <select id="biome-filter" style="
                background: rgba(15, 52, 96, 0.5);
                border: 1px solid #0f3460;
                color: white;
                padding: 8px;
                border-radius: 5px;
                width: 100%;
                font-size: 14px;
            ">
                <option value="all">All Biomes</option>
                <option value="forest">🌲 Forest</option>
                <option value="desert">🏜️ Desert</option>
                <option value="ice">❄️ Ice</option>
                <option value="volcano">🌋 Volcano</option>
                <option value="coast">🌊 Coast</option>
                <option value="highland">⚡ Highland</option>
                <option value="swamp">🌑 Swamp</option>
                <option value="mountain">🗻 Mountain</option>
            </select>
        `;
        section.appendChild(biomeFilter);

        // Add event listeners
        const select = biomeFilter.querySelector('#biome-filter');
        select.addEventListener('change', (e) => {
            this.filters.biomeFilter = e.target.value;
            this.applyFilters();
        });

        return section;
    }

    createCheckbox(id, label, icon) {
        const container = document.createElement('div');
        container.style.cssText = `
            margin: 10px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        `;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = id;
        checkbox.checked = this.filters[id];
        checkbox.style.cssText = `
            width: 18px;
            height: 18px;
            cursor: pointer;
        `;
        checkbox.addEventListener('change', (e) => {
            this.filters[id] = e.target.checked;
            this.applyFilters();
        });

        const labelEl = document.createElement('label');
        labelEl.htmlFor = id;
        labelEl.textContent = `${icon} ${label}`;
        labelEl.style.cssText = `
            color: #e8e8e8;
            font-size: 14px;
            cursor: pointer;
            user-select: none;
        `;

        container.appendChild(checkbox);
        container.appendChild(labelEl);

        return container;
    }

    createTravelPointsSection() {
        const section = document.createElement('div');
        section.id = 'travel-points-section';
        section.innerHTML = `
            <h3 style="
                color: #e94560;
                margin-top: 30px;
                border-bottom: 2px solid #0f3460;
                padding-bottom: 10px;
            ">Fast Travel Points</h3>
            <div id="travel-points-list" style="margin-top: 10px;">
                <!-- Populated dynamically -->
            </div>
        `;

        return section;
    }

    createLegend() {
        const legend = document.createElement('div');
        legend.innerHTML = `
            <h3 style="
                color: #e94560;
                margin-top: 30px;
                border-bottom: 2px solid #0f3460;
                padding-bottom: 10px;
            ">Legend</h3>
            <div style="margin-top: 10px; font-size: 12px; color: #e8e8e8;">
                <div style="margin: 5px 0;">🔴 Your Position</div>
                <div style="margin: 5px 0;">🟢 Unlocked Travel Point</div>
                <div style="margin: 5px 0;">🔒 Locked Travel Point</div>
                <div style="margin: 5px 0;">🏛️ City</div>
                <div style="margin: 5px 0;">🗻 Götterfels (Center)</div>
                <div style="margin: 5px 0;">⭐ Special Location</div>
            </div>
        `;

        return legend;
    }

    createFooter() {
        const footer = document.createElement('div');
        footer.style.cssText = `
            background: linear-gradient(90deg, #0f3460 0%, #16213e 100%);
            padding: 12px 25px;
            border-top: 2px solid #e94560;
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            color: #e8e8e8;
        `;

        footer.innerHTML = `
            <span id="player-position-footer">📍 Position: X: ${Math.round(this.playerPosition.x)}, Z: ${Math.round(this.playerPosition.z)}</span>
            <span>🌍 World Size: 9600×9600</span>
            <span>🏞️ Regions: ${this.regionsData ? Object.keys(this.regionsData.regions).length : 0}</span>
            <span>🏛️ Cities: ${this.citiesData ? this.citiesData.cities.length : 0}</span>
            <span>Press <strong>M</strong> to close</span>
        `;

        return footer;
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // 'M' key to toggle map
            if (e.key === 'm' || e.key === 'M') {
                if (!this.isOpen) {
                    this.open();
                } else {
                    this.close();
                }
            }

            // ESC to close
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    open() {
        if (this.isOpen) return;

        this.isOpen = true;
        this.modal.style.display = 'block';

        // Initialize 3D renderer if not already done
        if (!this.renderer3D) {
            this.renderer3D = new WorldMap3DRenderer(this.container3D);
            this.renderer3D.setPlayerPosition(this.playerPosition.x, this.playerPosition.z, 0);
        }

        // Update travel points list
        this.updateTravelPointsList();

        console.log('🗺️ World Map opened');
    }

    close() {
        if (!this.isOpen) return;

        this.isOpen = false;
        this.modal.style.display = 'none';

        console.log('🗺️ World Map closed');
    }

    updatePlayerPosition(x, z, rotation = 0) {
        this.playerPosition = { x, z };

        if (this.renderer3D) {
            this.renderer3D.setPlayerPosition(x, z, rotation);
        }

        // Update footer
        const footerPos = document.getElementById('player-position-footer');
        if (footerPos) {
            footerPos.textContent = `📍 Position: X: ${Math.round(x)}, Z: ${Math.round(z)}`;
        }
    }

    updateTravelPointsList() {
        const list = document.getElementById('travel-points-list');
        if (!list) return;

        // TODO: Load travel points from API
        // For now, use cities as travel points
        if (this.citiesData && this.citiesData.cities) {
            list.innerHTML = this.citiesData.cities.map(city => {
                const distance = Math.sqrt(
                    Math.pow(city.position.x - this.playerPosition.x, 2) +
                    Math.pow(city.position.z - this.playerPosition.z, 2)
                );

                return `
                    <div style="
                        background: rgba(15, 52, 96, 0.5);
                        padding: 10px;
                        margin: 8px 0;
                        border-radius: 6px;
                        border: 1px solid #0f3460;
                        cursor: pointer;
                    " onclick="window.worldMapFullUI.focusOnCity('${city.id}')">
                        <div style="font-weight: bold; color: #e8e8e8;">
                            🏛️ ${city.name}
                        </div>
                        <div style="font-size: 12px; color: #aaa; margin-top: 3px;">
                            ${city.region} • ${city.size}
                        </div>
                        <div style="font-size: 11px; color: #667eea; margin-top: 3px;">
                            Distance: ${Math.round(distance)} units
                        </div>
                    </div>
                `;
            }).join('');
        }
    }

    focusOnCity(cityId) {
        const city = this.citiesData.cities.find(c => c.id === cityId);
        if (!city) return;

        // Focus 3D camera on city
        if (this.renderer3D) {
            this.renderer3D.camera.position.set(
                city.position.x * this.renderer3D.scale,
                300,
                city.position.z * this.renderer3D.scale + 200
            );
            this.renderer3D.camera.lookAt(
                city.position.x * this.renderer3D.scale,
                0,
                city.position.z * this.renderer3D.scale
            );
        }

        // Update info panel
        this.showCityInfo(city);
    }

    showCityInfo(city) {
        const panel = document.getElementById('region-info-panel');
        if (!panel) return;

        const features = city.features ? Object.keys(city.features).map(f =>
            `<li>${f.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</li>`
        ).join('') : '';

        panel.innerHTML = `
            <h3 style="color: #e94560; margin-top: 20px; border-bottom: 2px solid #0f3460; padding-bottom: 10px;">
                🏛️ ${city.name}
            </h3>
            <div style="background: rgba(15,52,96,0.5); padding: 15px; border-radius: 8px; border: 1px solid #e94560; color: #e8e8e8;">
                <p><strong>Region:</strong> ${city.region}</p>
                <p><strong>Size:</strong> ${city.size}</p>
                <p><strong>Population:</strong> ${city.population || 'Unknown'}</p>
                ${city.isCapital ? '<p><strong>⭐ CAPITAL CITY</strong></p>' : ''}

                ${features ? `
                    <p style="margin-top: 15px;"><strong>Features:</strong></p>
                    <ul style="margin: 5px 0; padding-left: 20px;">${features}</ul>
                ` : ''}

                ${city.foodSpeciality ? `
                    <p style="margin-top: 15px;"><strong>🍖 Specialty:</strong> ${city.foodSpeciality.name}</p>
                ` : ''}

                <button onclick="window.worldMapFullUI.fastTravelToCity('${city.id}')" style="
                    background: #e94560;
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    margin-top: 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 14px;
                    font-weight: bold;
                ">🚩 Fast Travel Here</button>
            </div>
        `;
    }

    async fastTravelToCity(cityId) {
        const city = this.citiesData.cities.find(c => c.id === cityId);
        if (!city) return;

        // TODO: Implement actual fast travel API call
        console.log('🚩 Fast traveling to:', city.name);
        if (typeof notify === 'function') notify(`🚩 Schnellreise nach ${city.name}!`, 'success');

        // Update player position
        this.updatePlayerPosition(city.position.x, city.position.z);
    }

    handleSearch(query) {
        if (!query || query.length < 2) return;

        query = query.toLowerCase();

        // Search in cities
        const matchingCities = this.citiesData.cities.filter(city =>
            city.name.toLowerCase().includes(query)
        );

        // Search in regions
        const matchingRegions = Object.values(this.regionsData.regions).filter(region =>
            region.name.toLowerCase().includes(query)
        );

        // Update search results
        console.log('🔍 Search results:', { matchingCities, matchingRegions });

        // Focus on first result
        if (matchingCities.length > 0) {
            this.focusOnCity(matchingCities[0].id);
        } else if (matchingRegions.length > 0) {
            this.focusOnRegion(matchingRegions[0].id);
        }
    }

    focusOnRegion(regionId) {
        if (this.renderer3D) {
            this.renderer3D.focusOnRegion(regionId);
        }
    }

    applyFilters() {
        // TODO: Implement filter logic for 3D renderer
        console.log('Applying filters:', this.filters);

        // This would hide/show different markers in the 3D scene
        // For now, just log the filters
    }

    dispose() {
        if (this.renderer3D) {
            this.renderer3D.dispose();
        }

        if (this.modal && this.modal.parentNode) {
            this.modal.parentNode.removeChild(this.modal);
        }
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    window.worldMapFullUI = new WorldMapFullUI();
    console.log('✅ World Map Full UI ready! Press M to open.');
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorldMapFullUI;
} else {
    window.WorldMapFullUI = WorldMapFullUI;
}
