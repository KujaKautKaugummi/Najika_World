/**
 * World Mode Manager
 * Switches between Digivice Mode (rooms) and Open World Mode (9 regions)
 */

class WorldModeManager {
    constructor() {
        this.currentMode = 'digivice'; // 'digivice' or 'openworld'
        this.openWorldLoaded = false;
        this.openWorldSystems = null;
    }

    // ═══════════════════════════════════════════════════════════════
    // MODE SWITCHING
    // ═══════════════════════════════════════════════════════════════

    async switchMode(mode) {
        if (mode === this.currentMode) {
            console.log(`Already in ${mode} mode`);
            return;
        }

        console.log(`🔄 Switching to ${mode} mode...`);

        if (mode === 'openworld') {
            await this.loadOpenWorld();
        } else {
            await this.unloadOpenWorld();
        }

        this.currentMode = mode;
        this.updateUI();
    }

    // ═══════════════════════════════════════════════════════════════
    // OPEN WORLD LOADING
    // ═══════════════════════════════════════════════════════════════

    async loadOpenWorld() {
        if (this.openWorldLoaded) {
            this.showOpenWorld();
            return;
        }

        console.log('📦 Loading Open World Systems...');

        // Hide Digivice elements
        this.hideDigiviceElements();

        // Load Open World scripts (if not already loaded)
        await this.loadOpenWorldScripts();

        // Initialize Open World systems
        await this.initializeOpenWorldSystems();

        this.openWorldLoaded = true;
        this.showOpenWorld();

        console.log('✅ Open World loaded!');
    }

    async unloadOpenWorld() {
        console.log('🔄 Switching back to Digivice Mode...');

        // Hide Open World elements
        this.hideOpenWorld();

        // Show Digivice elements
        this.showDigiviceElements();

        console.log('✅ Digivice Mode restored!');
    }

    // ═══════════════════════════════════════════════════════════════
    // SCRIPT LOADING
    // ═══════════════════════════════════════════════════════════════

    async loadOpenWorldScripts() {
        const scripts = [
            '/digivice/static/js/api_client.js',
            '/digivice/static/js/interior_generator.js',
            '/digivice/static/js/realtime_combat.js',
            '/digivice/static/js/food_system.js',
            '/digivice/static/js/inventory_system.js',
            '/digivice/static/js/npc_system.js',
            '/digivice/static/js/quest_system.js',
            '/digivice/static/js/special_features.js',
            '/digivice/static/js/skill_system.js',
            '/digivice/static/js/crafting_system.js',
            '/digivice/static/js/special_locations.js',
            '/digivice/static/js/performance_monitor.js',
            '/digivice/static/js/save_system.js',
            '/digivice/static/js/sound_system.js',
            '/digivice/static/js/tutorial_system.js'
        ];

        for (const src of scripts) {
            // Check if script already loaded
            if (document.querySelector(`script[src="${src}"]`)) {
                continue;
            }

            await this.loadScript(src);
        }
    }

    loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src + `?v=${Date.now()}`; // Cache busting
            script.onload = () => {
                console.log(`✅ Loaded: ${src}`);
                resolve();
            };
            script.onerror = () => {
                console.warn(`⚠️ Failed to load: ${src}`);
                resolve(); // Don't reject, continue loading
            };
            document.body.appendChild(script);
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // SYSTEM INITIALIZATION
    // ═══════════════════════════════════════════════════════════════

    async initializeOpenWorldSystems() {
        // Wait for all scripts to load
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Clear existing scene (if any)
        if (window.Scene3D && window.Scene3D.scene) {
            while (window.Scene3D.scene.children.length > 0) {
                window.Scene3D.scene.remove(window.Scene3D.scene.children[0]);
            }
        }

        // Initialize 9-region world
        this.createOpenWorldScene();

        // Initialize all systems
        this.openWorldSystems = {
            interiorGenerator: new InteriorGenerator(window.Scene3D.scene, THREE),
            realtimeCombat: new RealtimeCombat(window.Scene3D.scene, THREE),
            foodSystem: new FoodSystem(),
            inventorySystem: new InventorySystem(),
            npcSystem: new NPCSystem(window.Scene3D.scene, THREE),
            questManager: new QuestManager(),
            specialFeatures: new SpecialFeatures(window.Scene3D.scene, THREE),
            skillSystem: new SkillSystem(),
            craftingSystem: new CraftingSystem(),
            specialLocations: new SpecialLocations(window.Scene3D.scene, THREE),
            performanceMonitor: new PerformanceMonitor(),
            saveSystem: new SaveSystem(),
            soundSystem: new SoundSystem(),
            tutorialSystem: new TutorialSystem()
        };

        // Connect systems
        this.openWorldSystems.inventorySystem.foodSystem = this.openWorldSystems.foodSystem;
        this.openWorldSystems.inventorySystem.combatSystem = this.openWorldSystems.realtimeCombat;
        this.openWorldSystems.realtimeCombat.foodSystem = this.openWorldSystems.foodSystem;

        // Expose globally
        window.openWorldSystems = this.openWorldSystems;

        console.log('✨ Open World Systems initialized!');
    }

    createOpenWorldScene() {
        // Create 9 regions (3x3 grid, each 133.32 x 133.32)
        const regionSize = 133.32;
        const regions = [
            { name: 'Handelsfestung', type: 'city', x: 0, z: 0 },
            { name: 'Dampf-Hain', type: 'city', x: regionSize, z: 0 },
            { name: 'Salzige Bucht', type: 'city', x: -regionSize, z: 0 },
            { name: 'Ewiger Winterforst', type: 'city', x: 0, z: regionSize },
            { name: 'Goldene Wüste', type: 'city', x: regionSize, z: regionSize },
            { name: 'Plains', type: 'plains', x: -regionSize, z: regionSize },
            { name: 'Forest', type: 'forest', x: 0, z: -regionSize },
            { name: 'Swamp', type: 'swamp', x: regionSize, z: -regionSize },
            { name: 'Mountains', type: 'mountains', x: -regionSize, z: -regionSize }
        ];

        regions.forEach(region => {
            this.createRegion(region);
        });

        // Add lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        window.Scene3D.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 100, 50);
        window.Scene3D.scene.add(directionalLight);
    }

    createRegion(region) {
        // Create ground
        const groundGeometry = new THREE.PlaneGeometry(133.32, 133.32);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: this.getRegionColor(region.type),
            roughness: 0.8,
            metalness: 0.2
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.set(region.x, 0, region.z);
        window.Scene3D.scene.add(ground);

        // Add city marker if it's a city
        if (region.type === 'city') {
            const markerGeometry = new THREE.BoxGeometry(10, 20, 10);
            const markerMaterial = new THREE.MeshStandardMaterial({ color: 0xff6b6b });
            const marker = new THREE.Mesh(markerGeometry, markerMaterial);
            marker.position.set(region.x, 10, region.z);
            marker.userData = { type: 'city_entrance', cityName: region.name };
            window.Scene3D.scene.add(marker);
        }
    }

    getRegionColor(type) {
        const colors = {
            'city': 0x8B7355,
            'plains': 0x90EE90,
            'forest': 0x228B22,
            'swamp': 0x556B2F,
            'mountains': 0x696969
        };
        return colors[type] || 0x888888;
    }

    // ═══════════════════════════════════════════════════════════════
    // UI MANAGEMENT
    // ═══════════════════════════════════════════════════════════════

    hideDigiviceElements() {
        // Hide Digivice-specific panels
        const elementsToHide = [
            '#najikaPanel',
            '#equipmentPanel',
            '#praiseBtn',
            '#scoldBtn',
            '#faceNajikaBtn'
        ];

        elementsToHide.forEach(selector => {
            const el = document.querySelector(selector);
            if (el) el.style.display = 'none';
        });
    }

    showDigiviceElements() {
        const elementsToShow = [
            '#najikaPanel',
            '#equipmentPanel',
            '#praiseBtn',
            '#scoldBtn',
            '#faceNajikaBtn'
        ];

        elementsToShow.forEach(selector => {
            const el = document.querySelector(selector);
            if (el) el.style.display = '';
        });
    }

    hideOpenWorld() {
        // Hide Open World UI
        const hudElements = document.querySelectorAll('.openworld-hud');
        hudElements.forEach(el => el.style.display = 'none');
    }

    showOpenWorld() {
        // Show Open World UI
        this.createOpenWorldHUD();

        const hudElements = document.querySelectorAll('.openworld-hud');
        hudElements.forEach(el => el.style.display = 'block');
    }

    createOpenWorldHUD() {
        // Check if HUD already exists
        if (document.getElementById('openWorldHUD')) {
            return;
        }

        // Create Open World HUD
        const hudHTML = `
            <div id="openWorldHUD" class="openworld-hud" style="position: fixed; top: 80px; right: 20px; z-index: 1000; background: rgba(20, 20, 30, 0.95); padding: 15px; border-radius: 10px; border: 2px solid #667eea; min-width: 250px; font-size: 0.9rem; color: #eaeaea;">
                <h3 style="margin: 0 0 10px 0; color: #667eea;">🗺️ Open World</h3>

                <!-- Player Stats -->
                <div style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>❤️ HP:</span>
                        <span id="owHP">100</span>/<span id="owMaxHP">100</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>⚡ MP:</span>
                        <span id="owMP">100</span>/<span id="owMaxMP">100</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>💪 Stamina:</span>
                        <span id="owStamina">100</span>/<span id="owMaxStamina">100</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>💰 Gold:</span>
                        <span id="owGold">100</span>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div style="margin-top: 10px; display: flex; gap: 5px; flex-wrap: wrap;">
                    <button id="owInventoryBtn" style="flex: 1; padding: 5px; font-size: 0.8rem; background: #667eea; border: none; border-radius: 5px; color: white; cursor: pointer;">🎒 Inventar (I)</button>
                    <button id="owQuestsBtn" style="flex: 1; padding: 5px; font-size: 0.8rem; background: #667eea; border: none; border-radius: 5px; color: white; cursor: pointer;">📜 Quests (J)</button>
                </div>
                <div style="margin-top: 5px; display: flex; gap: 5px; flex-wrap: wrap;">
                    <button id="owSkillsBtn" style="flex: 1; padding: 5px; font-size: 0.8rem; background: #667eea; border: none; border-radius: 5px; color: white; cursor: pointer;">✨ Skills (K)</button>
                    <button id="owMapBtn" style="flex: 1; padding: 5px; font-size: 0.8rem; background: #667eea; border: none; border-radius: 5px; color: white; cursor: pointer;">🗺️ Karte (M)</button>
                </div>

                <!-- Active Quests -->
                <div style="margin-top: 15px;">
                    <h4 style="margin: 0 0 5px 0; font-size: 0.85rem; color: #a3b3ff;">📜 Active Quests</h4>
                    <div id="owActiveQuests" style="font-size: 0.75rem; color: #ccc;">
                        Keine aktiven Quests
                    </div>
                </div>

                <!-- Performance -->
                <div style="margin-top: 15px; font-size: 0.75rem; color: #888;">
                    <div>FPS: <span id="owFPS">60</span></div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', hudHTML);

        // Add event listeners
        this.attachOpenWorldEventListeners();
    }

    attachOpenWorldEventListeners() {
        // Inventory
        document.getElementById('owInventoryBtn')?.addEventListener('click', () => {
            if (window.openWorldSystems?.inventorySystem) {
                window.openWorldSystems.inventorySystem.toggleUI();
            }
        });

        // Quests
        document.getElementById('owQuestsBtn')?.addEventListener('click', () => {
            if (window.openWorldSystems?.questManager) {
                window.openWorldSystems.questManager.toggleUI();
            }
        });

        // Skills
        document.getElementById('owSkillsBtn')?.addEventListener('click', () => {
            if (window.openWorldSystems?.skillSystem) {
                window.openWorldSystems.skillSystem.toggleUI();
            }
        });

        // Map
        document.getElementById('owMapBtn')?.addEventListener('click', () => {
            if (window.openWorldSystems?.specialLocations) {
                window.openWorldSystems.specialLocations.showMapUI();
            } else {
                console.log('🗺️ Map: Zeige 9-Regionen Übersicht');
                alert('🗺️ Open World Map:\n\n- Handelsfestung (0, 0)\n- Salzige Bucht (-133, 0)\n- Dampf-Hain (133, 0)\n- Ewiger Winterforst (0, 133)\n- Goldene Wüste (133, 133)\n- Plains (-133, 133)\n- Forest (0, -133)\n- Swamp (133, -133)\n- Mountains (-133, -133)');
            }
        });
    }

    updateUI() {
        // Update world mode indicator
        const worldLabel = document.querySelector('[style*="Najika Open World"]');
        if (worldLabel) {
            worldLabel.textContent = this.currentMode === 'openworld'
                ? 'Open World RPG'
                : 'Najika Open World';
        }

        // Update button state
        const toggleBtn = document.getElementById('worldModeToggle');
        if (toggleBtn) {
            toggleBtn.textContent = this.currentMode === 'openworld'
                ? '🏠 Digivice'
                : '🗺️ Open World';
            toggleBtn.style.background = this.currentMode === 'openworld'
                ? 'linear-gradient(135deg, #e74c3c, #c0392b)'
                : 'linear-gradient(135deg, #667eea, #764ba2)';
        }
    }
}

// Initialize World Mode Manager
window.worldModeManager = new WorldModeManager();

console.log('✨ World Mode Manager initialized');
