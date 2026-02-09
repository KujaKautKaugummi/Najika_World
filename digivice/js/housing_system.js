/**
 * HOUSING SYSTEM - Fortnite Creative Style
 *
 * Features:
 * - Freies Bauen mit Grid-Snap
 * - Möbel platzieren & rotieren
 * - Zimmer in der Schwarzen Mühle
 * - Speichern/Laden
 *
 * Erstellt: 2025-12-12
 */

const HousingSystem = (function() {
    'use strict';

    // ============================================
    // KONFIGURATION
    // ============================================

    const GRID_SIZE = 0.5; // Meter
    const ROTATE_SNAP = 45; // Grad

    // ============================================
    // MÖBEL-KATALOG
    // ============================================

    const FURNITURE_CATALOG = {
        // Grundmöbel
        'bed_simple': { name: 'Einfaches Bett', category: 'bedroom', size: [2, 1, 1], price: 100, model: 'bed_simple' },
        'bed_double': { name: 'Doppelbett', category: 'bedroom', size: [2, 2, 1], price: 250, model: 'bed_double' },
        'wardrobe': { name: 'Kleiderschrank', category: 'bedroom', size: [1, 2, 2], price: 150, model: 'wardrobe' },
        'nightstand': { name: 'Nachttisch', category: 'bedroom', size: [0.5, 0.5, 0.5], price: 30, model: 'nightstand' },

        // Wohnzimmer
        'sofa': { name: 'Sofa', category: 'living', size: [2, 1, 0.8], price: 200, model: 'sofa' },
        'armchair': { name: 'Sessel', category: 'living', size: [1, 1, 0.8], price: 80, model: 'armchair' },
        'coffee_table': { name: 'Couchtisch', category: 'living', size: [1, 0.5, 0.5], price: 60, model: 'coffee_table' },
        'bookshelf': { name: 'Bücherregal', category: 'living', size: [1, 0.3, 2], price: 120, model: 'bookshelf' },
        'fireplace': { name: 'Kamin', category: 'living', size: [1.5, 0.5, 1.5], price: 500, model: 'fireplace', animated: true },

        // Küche
        'stove': { name: 'Herd', category: 'kitchen', size: [1, 1, 1], price: 300, model: 'stove', functional: true },
        'fridge': { name: 'Kühlschrank', category: 'kitchen', size: [1, 1, 2], price: 250, model: 'fridge', functional: true },
        'sink': { name: 'Spüle', category: 'kitchen', size: [1, 0.5, 1], price: 100, model: 'sink' },
        'kitchen_table': { name: 'Esstisch', category: 'kitchen', size: [2, 1, 1], price: 150, model: 'kitchen_table' },
        'chair': { name: 'Stuhl', category: 'kitchen', size: [0.5, 0.5, 1], price: 40, model: 'chair' },

        // Badezimmer
        'bathtub': { name: 'Badewanne', category: 'bathroom', size: [2, 1, 0.6], price: 400, model: 'bathtub', functional: true },
        'toilet': { name: 'Toilette', category: 'bathroom', size: [0.5, 0.5, 0.8], price: 80, model: 'toilet', functional: true },
        'bathroom_sink': { name: 'Waschbecken', category: 'bathroom', size: [0.5, 0.4, 0.8], price: 60, model: 'bathroom_sink' },
        'mirror': { name: 'Spiegel', category: 'bathroom', size: [0.1, 1, 1], price: 50, model: 'mirror', wall: true },

        // Dekoration
        'lamp_floor': { name: 'Stehlampe', category: 'decor', size: [0.3, 0.3, 1.5], price: 70, model: 'lamp_floor', light: true },
        'lamp_table': { name: 'Tischlampe', category: 'decor', size: [0.2, 0.2, 0.4], price: 40, model: 'lamp_table', light: true },
        'plant_pot': { name: 'Topfpflanze', category: 'decor', size: [0.4, 0.4, 0.8], price: 30, model: 'plant_pot' },
        'painting': { name: 'Gemälde', category: 'decor', size: [0.1, 1, 0.8], price: 100, model: 'painting', wall: true },
        'rug': { name: 'Teppich', category: 'decor', size: [2, 2, 0.05], price: 80, model: 'rug', floor: true },

        // Spezial
        'crafting_table': { name: 'Crafting-Tisch', category: 'special', size: [2, 1, 1], price: 500, model: 'crafting_table', functional: true },
        'alchemy_station': { name: 'Alchemie-Station', category: 'special', size: [1.5, 1, 1.2], price: 800, model: 'alchemy_station', functional: true },
        'terminal': { name: 'Terminal', category: 'special', size: [1, 0.5, 1.5], price: 1000, model: 'terminal', functional: true },
        'training_dummy': { name: 'Trainings-Puppe', category: 'special', size: [0.5, 0.5, 1.8], price: 300, model: 'training_dummy', functional: true }
    };

    // ============================================
    // RÄUME DER SCHWARZEN MÜHLE
    // ============================================

    const ROOMS = {
        'wohnzimmer': { name: 'Wohnzimmer', floor: 0, size: [8, 6], position: [0, 0, 0] },
        'kueche': { name: 'Küche', floor: 0, size: [5, 5], position: [8, 0, 0] },
        'badezimmer': { name: 'Badezimmer', floor: 0, size: [4, 4], position: [8, 0, 5] },
        'schlafzimmer': { name: 'Schlafzimmer', floor: 1, size: [6, 6], position: [0, 3, 0] },
        'lager': { name: 'Lager', floor: 1, size: [4, 4], position: [6, 3, 0] },
        'training': { name: 'Trainingsraum', floor: 1, size: [6, 5], position: [0, 3, 6] },
        'terminal_raum': { name: 'Terminal', floor: 2, size: [5, 5], position: [0, 6, 0] },
        'keller_studieren': { name: 'Studierzimmer', floor: -1, size: [6, 6], position: [0, -3, 0] },
        'keller_crafting': { name: 'Crafting-Keller', floor: -1, size: [6, 4], position: [6, -3, 0] }
    };

    // ============================================
    // STATE
    // ============================================

    let state = {
        editMode: false,
        currentRoom: null,
        selectedFurniture: null,
        placementPreview: null,
        rotation: 0,
        placedFurniture: {}, // { roomId: [ {id, type, position, rotation} ] }
        ownedFurniture: [], // Gekaufte Möbel
        gold: 1000
    };

    // ============================================
    // SPEICHERN / LADEN
    // ============================================

    function loadState() {
        const saved = localStorage.getItem('housing_state');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                state.placedFurniture = data.placedFurniture || {};
                state.ownedFurniture = data.ownedFurniture || [];
                state.gold = data.gold || 1000;
            } catch(e) {
                console.error('Housing: Fehler beim Laden');
            }
        }
    }

    function saveState() {
        localStorage.setItem('housing_state', JSON.stringify({
            placedFurniture: state.placedFurniture,
            ownedFurniture: state.ownedFurniture,
            gold: state.gold
        }));
    }

    // ============================================
    // EDIT MODE
    // ============================================

    function enterEditMode(roomId) {
        if (!ROOMS[roomId]) {
            showNotification('Unbekannter Raum!');
            return;
        }

        state.editMode = true;
        state.currentRoom = roomId;
        state.selectedFurniture = null;
        state.rotation = 0;

        openEditUI();
        showNotification(`🏠 Bearbeitungsmodus: ${ROOMS[roomId].name}`);
    }

    function exitEditMode() {
        state.editMode = false;
        state.currentRoom = null;
        state.selectedFurniture = null;
        closeEditUI();
        saveState();
        showNotification('Änderungen gespeichert!');
    }

    // ============================================
    // MÖBEL MANAGEMENT
    // ============================================

    function buyFurniture(furnitureType) {
        const furniture = FURNITURE_CATALOG[furnitureType];
        if (!furniture) return false;

        if (state.gold < furniture.price) {
            showNotification('Nicht genug Gold!');
            return false;
        }

        state.gold -= furniture.price;
        state.ownedFurniture.push(furnitureType);
        saveState();
        showNotification(`${furniture.name} gekauft!`);
        return true;
    }

    function selectFurniture(furnitureType) {
        if (!state.editMode) return false;

        // Check if owned
        const ownedIndex = state.ownedFurniture.indexOf(furnitureType);
        if (ownedIndex === -1) {
            showNotification('Du besitzt dieses Möbel nicht!');
            return false;
        }

        state.selectedFurniture = furnitureType;
        updateEditUI();
        return true;
    }

    function placeFurniture(x, z) {
        if (!state.editMode || !state.selectedFurniture || !state.currentRoom) return false;

        const furniture = FURNITURE_CATALOG[state.selectedFurniture];
        const room = ROOMS[state.currentRoom];

        // Grid Snap
        const snappedX = Math.round(x / GRID_SIZE) * GRID_SIZE;
        const snappedZ = Math.round(z / GRID_SIZE) * GRID_SIZE;

        // Bounds Check
        if (snappedX < 0 || snappedX + furniture.size[0] > room.size[0] ||
            snappedZ < 0 || snappedZ + furniture.size[1] > room.size[1]) {
            showNotification('Außerhalb des Raums!');
            return false;
        }

        // Collision Check
        if (checkCollision(snappedX, snappedZ, furniture.size, state.rotation)) {
            showNotification('Kollidiert mit anderem Möbel!');
            return false;
        }

        // Place
        if (!state.placedFurniture[state.currentRoom]) {
            state.placedFurniture[state.currentRoom] = [];
        }

        const placedItem = {
            id: Date.now(),
            type: state.selectedFurniture,
            position: [snappedX, 0, snappedZ],
            rotation: state.rotation
        };

        state.placedFurniture[state.currentRoom].push(placedItem);

        // Remove from owned (consumed)
        const ownedIndex = state.ownedFurniture.indexOf(state.selectedFurniture);
        if (ownedIndex !== -1) {
            state.ownedFurniture.splice(ownedIndex, 1);
        }

        state.selectedFurniture = null;
        saveState();
        updateEditUI();
        render3DFurniture(placedItem);

        showNotification(`${furniture.name} platziert!`);
        return true;
    }

    function removeFurniture(itemId) {
        if (!state.editMode || !state.currentRoom) return false;

        const roomFurniture = state.placedFurniture[state.currentRoom];
        if (!roomFurniture) return false;

        const index = roomFurniture.findIndex(f => f.id === itemId);
        if (index === -1) return false;

        const removed = roomFurniture.splice(index, 1)[0];
        state.ownedFurniture.push(removed.type);

        saveState();
        updateEditUI();
        remove3DFurniture(itemId);

        showNotification(`${FURNITURE_CATALOG[removed.type].name} entfernt!`);
        return true;
    }

    function rotateFurniture() {
        state.rotation = (state.rotation + ROTATE_SNAP) % 360;
        updateEditUI();
    }

    function checkCollision(x, z, size, rotation) {
        const roomFurniture = state.placedFurniture[state.currentRoom] || [];

        // Simplified AABB collision
        const newBox = {
            minX: x,
            maxX: x + size[0],
            minZ: z,
            maxZ: z + size[1]
        };

        for (const item of roomFurniture) {
            const itemSize = FURNITURE_CATALOG[item.type].size;
            const itemBox = {
                minX: item.position[0],
                maxX: item.position[0] + itemSize[0],
                minZ: item.position[2],
                maxZ: item.position[2] + itemSize[1]
            };

            if (newBox.minX < itemBox.maxX && newBox.maxX > itemBox.minX &&
                newBox.minZ < itemBox.maxZ && newBox.maxZ > itemBox.minZ) {
                return true; // Collision!
            }
        }

        return false;
    }

    // ============================================
    // 3D RENDERING (Placeholder - nutzt Three.js wenn verfügbar)
    // ============================================

    function render3DFurniture(item) {
        // Placeholder - wird von 3d_scene.js implementiert
        if (window.HousingRenderer && window.HousingRenderer.addFurniture) {
            window.HousingRenderer.addFurniture(item);
        }
    }

    function remove3DFurniture(itemId) {
        if (window.HousingRenderer && window.HousingRenderer.removeFurniture) {
            window.HousingRenderer.removeFurniture(itemId);
        }
    }

    function renderRoom(roomId) {
        const furniture = state.placedFurniture[roomId] || [];
        furniture.forEach(item => render3DFurniture(item));
    }

    // ============================================
    // UI
    // ============================================

    function openEditUI() {
        let ui = document.getElementById('housing-edit-ui');
        if (!ui) {
            ui = document.createElement('div');
            ui.id = 'housing-edit-ui';
            document.body.appendChild(ui);
        }

        if (!document.getElementById('housing-styles')) {
            const style = document.createElement('style');
            style.id = 'housing-styles';
            style.textContent = getHousingStyles();
            document.head.appendChild(style);
        }

        updateEditUI();
        ui.style.display = 'block';
    }

    function closeEditUI() {
        const ui = document.getElementById('housing-edit-ui');
        if (ui) ui.style.display = 'none';
    }

    function updateEditUI() {
        const ui = document.getElementById('housing-edit-ui');
        if (!ui) return;

        const room = ROOMS[state.currentRoom];
        const roomFurniture = state.placedFurniture[state.currentRoom] || [];

        // Gruppiere Möbel nach Kategorie
        const categories = {};
        for (const [id, furniture] of Object.entries(FURNITURE_CATALOG)) {
            if (!categories[furniture.category]) {
                categories[furniture.category] = [];
            }
            categories[furniture.category].push({ id, ...furniture });
        }

        ui.innerHTML = `
            <div class="housing-container">
                <div class="housing-header">
                    <h2>🏠 ${room ? room.name : 'Housing'}</h2>
                    <span class="gold-display">💰 ${state.gold}G</span>
                    <button class="housing-close" onclick="HousingSystem.exit()">✕</button>
                </div>

                <div class="housing-content">
                    <div class="housing-sidebar">
                        <h3>Möbel-Katalog</h3>
                        <div class="furniture-categories">
                            ${Object.entries(categories).map(([cat, items]) => `
                                <div class="category">
                                    <h4>${cat.charAt(0).toUpperCase() + cat.slice(1)}</h4>
                                    <div class="category-items">
                                        ${items.map(item => `
                                            <div class="furniture-item ${state.ownedFurniture.includes(item.id) ? 'owned' : ''}"
                                                 onclick="HousingSystem.selectFromCatalog('${item.id}')">
                                                <span class="item-name">${item.name}</span>
                                                <span class="item-price">${item.price}G</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <div class="housing-main">
                        <div class="placed-furniture">
                            <h3>Platzierte Möbel (${roomFurniture.length})</h3>
                            <div class="placed-list">
                                ${roomFurniture.map(item => {
                                    const furniture = FURNITURE_CATALOG[item.type];
                                    return `
                                        <div class="placed-item">
                                            <span>${furniture.name}</span>
                                            <button onclick="HousingSystem.remove(${item.id})">🗑️</button>
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>

                        ${state.selectedFurniture ? `
                            <div class="placement-controls">
                                <h3>Platzieren: ${FURNITURE_CATALOG[state.selectedFurniture].name}</h3>
                                <p>Rotation: ${state.rotation}°</p>
                                <button onclick="HousingSystem.rotate()">🔄 Rotieren</button>
                                <p class="hint">Klicke in den Raum zum Platzieren</p>
                            </div>
                        ` : ''}

                        <div class="owned-furniture">
                            <h3>Dein Inventar (${state.ownedFurniture.length})</h3>
                            <div class="owned-list">
                                ${[...new Set(state.ownedFurniture)].map(type => {
                                    const count = state.ownedFurniture.filter(t => t === type).length;
                                    const furniture = FURNITURE_CATALOG[type];
                                    return `
                                        <div class="owned-item" onclick="HousingSystem.select('${type}')">
                                            <span>${furniture.name} x${count}</span>
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="housing-footer">
                    <button onclick="HousingSystem.exit()">💾 Speichern & Beenden</button>
                </div>
            </div>
        `;
    }

    function selectFromCatalog(furnitureType) {
        const furniture = FURNITURE_CATALOG[furnitureType];
        if (!furniture) return;

        // Bereits besessen?
        if (state.ownedFurniture.includes(furnitureType)) {
            selectFurniture(furnitureType);
        } else {
            // Kaufen
            if (confirm(`${furniture.name} für ${furniture.price}G kaufen?`)) {
                if (buyFurniture(furnitureType)) {
                    selectFurniture(furnitureType);
                }
            }
        }
    }

    function getHousingStyles() {
        return `
            #housing-edit-ui {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 10000;
                display: none;
            }
            .housing-container {
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.95);
                display: flex;
                flex-direction: column;
                color: #fff;
                font-family: monospace;
            }
            .housing-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(90deg, #1a1a2e, #16213e);
                border-bottom: 2px solid #4CAF50;
            }
            .housing-header h2 { margin: 0; color: #4CAF50; }
            .gold-display { color: #FFD700; font-size: 18px; }
            .housing-close {
                background: #ff4444;
                border: none;
                color: white;
                width: 35px; height: 35px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
            }
            .housing-content {
                display: flex;
                flex: 1;
                overflow: hidden;
            }
            .housing-sidebar {
                width: 280px;
                background: rgba(0,0,0,0.5);
                border-right: 1px solid #333;
                overflow-y: auto;
                padding: 15px;
            }
            .housing-sidebar h3 { color: #4CAF50; margin-bottom: 10px; }
            .category h4 {
                color: #888;
                font-size: 12px;
                margin: 10px 0 5px;
                text-transform: uppercase;
            }
            .furniture-item {
                display: flex;
                justify-content: space-between;
                padding: 8px 10px;
                margin: 3px 0;
                background: rgba(255,255,255,0.05);
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .furniture-item:hover { background: rgba(76,175,80,0.2); }
            .furniture-item.owned { border-left: 3px solid #4CAF50; }
            .item-price { color: #FFD700; font-size: 12px; }
            .housing-main {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
            }
            .housing-main h3 { color: #4CAF50; margin-bottom: 10px; }
            .placed-list, .owned-list {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .placed-item, .owned-item {
                padding: 10px 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 5px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .placed-item button {
                background: #ff4444;
                border: none;
                padding: 5px 8px;
                border-radius: 3px;
                cursor: pointer;
            }
            .owned-item { cursor: pointer; }
            .owned-item:hover { background: rgba(76,175,80,0.3); }
            .placement-controls {
                margin: 20px 0;
                padding: 15px;
                background: rgba(76,175,80,0.1);
                border: 1px solid #4CAF50;
                border-radius: 8px;
            }
            .placement-controls button {
                padding: 10px 20px;
                background: #4CAF50;
                border: none;
                color: white;
                border-radius: 5px;
                cursor: pointer;
                margin: 10px 5px 10px 0;
            }
            .hint { color: #888; font-size: 12px; }
            .housing-footer {
                padding: 15px 20px;
                background: rgba(0,0,0,0.5);
                border-top: 1px solid #333;
                text-align: center;
            }
            .housing-footer button {
                padding: 12px 30px;
                background: #4CAF50;
                border: none;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
        `;
    }

    // Utility
    function showNotification(msg) {
        if (typeof window.showNotification === 'function') {
            window.showNotification(msg);
        } else {
            console.log('[HOUSING]', msg);
        }
    }

    // Init
    loadState();

    return {
        enter: enterEditMode,
        exit: exitEditMode,
        buy: buyFurniture,
        select: selectFurniture,
        selectFromCatalog: selectFromCatalog,
        place: placeFurniture,
        remove: removeFurniture,
        rotate: rotateFurniture,
        renderRoom: renderRoom,
        getCatalog: () => FURNITURE_CATALOG,
        getRooms: () => ROOMS,
        getState: () => state,
        isEditing: () => state.editMode,
        loadState: loadState,
        saveState: saveState
    };
})();

window.HousingSystem = HousingSystem;

console.log('🏠 Housing System (Fortnite Creative Style) geladen');
