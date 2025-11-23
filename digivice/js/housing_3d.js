// 🏠 NAJIKA HOUSING SYSTEM - 3D VISUALISIERUNG (Sims + Skyrim + Animal Crossing)
(function() {
    const HOUSING_CONFIG = {
        // API Endpoint
        apiBaseUrl: '/api/housing',

        // House Positions in World (Schwarze Mühle Housing District)
        housePositions: {
            player1: [-200, 0, 400],
            player2: [-150, 0, 400],
            player3: [-100, 0, 400],
            player4: [-200, 0, 450],
            player5: [-150, 0, 450],
            player6: [-100, 0, 450]
        },

        // House Level Sizes (1-10)
        houseSizes: {
            1: { width: 8, depth: 8, height: 4, color: 0x8b7355 },    // Small cottage
            2: { width: 10, depth: 10, height: 4.5, color: 0x9b8365 },
            3: { width: 12, depth: 12, height: 5, color: 0xab9375 },
            4: { width: 14, depth: 12, height: 5.5, color: 0xbb9385 },
            5: { width: 16, depth: 14, height: 6, color: 0xcb9395 },   // Medium house
            6: { width: 18, depth: 16, height: 6.5, color: 0xdba3a5 },
            7: { width: 20, depth: 18, height: 7, color: 0xebb3b5 },
            8: { width: 22, depth: 20, height: 7.5, color: 0xfbc3c5 },
            9: { width: 24, depth: 22, height: 8, color: 0xffd3d5 },
            10: { width: 28, depth: 26, height: 9, color: 0xffe3e5 }   // Mansion
        },

        // Furniture Types mit 3D-Visualisierung
        furnitureTypes: {
            bed: {
                width: 2, depth: 3, height: 0.8,
                color: 0x8b4513,
                icon: '🛏️',
                category: 'bedroom'
            },
            table: {
                width: 2, depth: 2, height: 1.2,
                color: 0xa0522d,
                icon: '🪑',
                category: 'dining'
            },
            chair: {
                width: 0.8, depth: 0.8, height: 1.5,
                color: 0xcd853f,
                icon: '🪑',
                category: 'dining'
            },
            sofa: {
                width: 3, depth: 1.5, height: 1.2,
                color: 0x4a4a4a,
                icon: '🛋️',
                category: 'living'
            },
            bookshelf: {
                width: 2, depth: 0.6, height: 2.5,
                color: 0x654321,
                icon: '📚',
                category: 'study'
            },
            desk: {
                width: 2, depth: 1, height: 1.2,
                color: 0x8b7355,
                icon: '🪑',
                category: 'study'
            },
            wardrobe: {
                width: 2, depth: 1, height: 2.8,
                color: 0x5d4e37,
                icon: '👔',
                category: 'bedroom'
            },
            lamp: {
                width: 0.3, depth: 0.3, height: 1.5,
                color: 0xffd700,
                icon: '💡',
                category: 'lighting',
                emitsLight: true
            },
            rug: {
                width: 3, depth: 2, height: 0.05,
                color: 0xdc143c,
                icon: '🎨',
                category: 'decoration'
            },
            plant: {
                width: 0.6, depth: 0.6, height: 1.2,
                color: 0x228b22,
                icon: '🪴',
                category: 'decoration'
            },
            painting: {
                width: 1.5, depth: 0.1, height: 2,
                color: 0x8b008b,
                icon: '🖼️',
                category: 'decoration'
            },
            tv: {
                width: 2, depth: 0.3, height: 1.5,
                color: 0x000000,
                icon: '📺',
                category: 'entertainment'
            },
            fireplace: {
                width: 2, depth: 1, height: 2,
                color: 0x8b0000,
                icon: '🔥',
                category: 'living',
                emitsLight: true
            },
            kitchen_counter: {
                width: 3, depth: 1, height: 1.5,
                color: 0xc0c0c0,
                icon: '🍳',
                category: 'kitchen'
            },
            refrigerator: {
                width: 1.2, depth: 1, height: 2.5,
                color: 0xe0e0e0,
                icon: '🧊',
                category: 'kitchen'
            }
        },

        // Proximity detection
        interactionRadius: 15,
        insideHouseRadius: 8
    };

    // State
    let playerHouses = {};  // { playerId: houseData }
    let houseMeshes = {};   // { playerId: { building, furniture: [], lights: [] } }
    let currentPlayerHouse = null;
    let selectedHouse = null;
    let isInsideHouse = false;
    let currentPlayerId = 1;  // Default player ID
    let housingUI = null;
    let scene = null;  // Will be set from 3d_scene.js
    let furnitureEditMode = false;
    let selectedFurniture = null;

    // === PUBLIC API ===

    function init(threeScene, playerId = 1) {
        scene = threeScene;
        currentPlayerId = playerId;
        console.log('🏠 Housing System 3D initialized');

        createHousingUI();
        loadPlayerHouse(currentPlayerId);

        return true;
    }

    function setScene(threeScene) {
        scene = threeScene;
    }

    function setPlayerId(playerId) {
        currentPlayerId = playerId;
        loadPlayerHouse(playerId);
    }

    // === API CALLS ===

    async function loadPlayerHouse(playerId) {
        try {
            const response = await fetch(`${HOUSING_CONFIG.apiBaseUrl}/house/${playerId}`);
            if (!response.ok) {
                console.warn(`⚠️ Could not load house for player ${playerId}`);
                return null;
            }

            const houseData = await response.json();
            playerHouses[playerId] = houseData;
            currentPlayerHouse = houseData;

            console.log(`🏠 Loaded house for player ${playerId}:`, houseData);

            // Visualize house in 3D
            if (scene) {
                visualizeHouse(playerId, houseData);
            }

            return houseData;
        } catch (error) {
            console.error('❌ Error loading player house:', error);
            return null;
        }
    }

    async function placeFurniture(playerId, furnitureData) {
        try {
            const response = await fetch(`${HOUSING_CONFIG.apiBaseUrl}/furniture/place`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: playerId,
                    furniture: furnitureData
                })
            });

            if (!response.ok) {
                const error = await response.json();
                console.warn('⚠️ Could not place furniture:', error.detail);
                if (typeof notify === 'function') {
                    notify(`⚠️ ${error.detail}`, 'warning');
                }
                return false;
            }

            const result = await response.json();
            console.log('✅ Furniture placed:', result);

            // Reload house to update visualization
            await loadPlayerHouse(playerId);

            if (typeof notify === 'function') {
                notify(`✅ ${result.message}`, 'success');
            }

            return true;
        } catch (error) {
            console.error('❌ Error placing furniture:', error);
            return false;
        }
    }

    async function removeFurniture(playerId, furnitureIndex) {
        try {
            const response = await fetch(`${HOUSING_CONFIG.apiBaseUrl}/furniture/remove`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: playerId,
                    furniture_index: furnitureIndex
                })
            });

            if (!response.ok) {
                const error = await response.json();
                console.warn('⚠️ Could not remove furniture:', error.detail);
                return false;
            }

            const result = await response.json();
            console.log('✅ Furniture removed:', result);

            // Reload house to update visualization
            await loadPlayerHouse(playerId);

            if (typeof notify === 'function') {
                notify(`✅ ${result.message}`, 'success');
            }

            return true;
        } catch (error) {
            console.error('❌ Error removing furniture:', error);
            return false;
        }
    }

    async function upgradeHouse(playerId) {
        try {
            const response = await fetch(`${HOUSING_CONFIG.apiBaseUrl}/upgrade`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player_id: playerId })
            });

            if (!response.ok) {
                const error = await response.json();
                console.warn('⚠️ Could not upgrade house:', error.detail);
                if (typeof notify === 'function') {
                    notify(`⚠️ ${error.detail}`, 'warning');
                }
                return false;
            }

            const result = await response.json();
            console.log('🎉 House upgraded:', result);

            // Reload house to update visualization
            await loadPlayerHouse(playerId);

            if (typeof notify === 'function') {
                notify(`🎉 ${result.message}`, 'success');
            }

            return true;
        } catch (error) {
            console.error('❌ Error upgrading house:', error);
            return false;
        }
    }

    async function loadFurnitureCatalog() {
        try {
            const response = await fetch(`${HOUSING_CONFIG.apiBaseUrl}/furniture/catalog`);
            if (!response.ok) {
                console.warn('⚠️ Could not load furniture catalog');
                return null;
            }

            const data = await response.json();
            return data.catalog;
        } catch (error) {
            console.error('❌ Error loading furniture catalog:', error);
            return null;
        }
    }

    // === 3D VISUALIZATION ===

    function visualizeHouse(playerId, houseData) {
        if (!scene) {
            console.warn('⚠️ Scene not initialized');
            return;
        }

        // Remove old house visualization if exists
        if (houseMeshes[playerId]) {
            clearHouseVisualization(playerId);
        }

        // Get house position
        const position = HOUSING_CONFIG.housePositions[`player${playerId}`] || [-200, 0, 400];
        const houseSize = HOUSING_CONFIG.houseSizes[houseData.level] || HOUSING_CONFIG.houseSizes[1];

        // Create house building
        const building = createHouseBuilding(houseSize, position);
        scene.add(building);

        // Create furniture
        const furnitureMeshes = [];
        if (houseData.furniture && houseData.furniture.length > 0) {
            houseData.furniture.forEach((furnitureData, index) => {
                const mesh = createFurnitureMesh(furnitureData, position, houseSize);
                if (mesh) {
                    mesh.userData.furnitureIndex = index;
                    mesh.userData.playerId = playerId;
                    scene.add(mesh);
                    furnitureMeshes.push(mesh);
                }
            });
        }

        // Create lights for furniture with emitsLight
        const lights = [];
        furnitureMeshes.forEach(mesh => {
            if (mesh.userData.emitsLight) {
                const light = new THREE.PointLight(0xffaa00, 0.8, 10);
                light.position.copy(mesh.position);
                light.position.y += 1;
                scene.add(light);
                lights.push(light);
            }
        });

        // Store references
        houseMeshes[playerId] = {
            building,
            furniture: furnitureMeshes,
            lights
        };

        console.log(`🏠 Visualized house for player ${playerId}: Level ${houseData.level}, ${furnitureMeshes.length} furniture items`);
    }

    function createHouseBuilding(houseSize, position) {
        const group = new THREE.Group();

        // Foundation
        const foundation = new THREE.Mesh(
            new THREE.BoxGeometry(houseSize.width + 1, 0.5, houseSize.depth + 1),
            new THREE.MeshStandardMaterial({
                color: 0x4a4a4a,
                roughness: 0.8
            })
        );
        foundation.position.set(position[0], position[1] - 0.25, position[2]);
        foundation.castShadow = true;
        foundation.receiveShadow = true;
        group.add(foundation);

        // Walls
        const wallMaterial = new THREE.MeshStandardMaterial({
            color: houseSize.color,
            roughness: 0.7
        });

        // Front wall (with door)
        const frontWall = new THREE.Group();
        const frontLeft = new THREE.Mesh(
            new THREE.BoxGeometry(houseSize.width * 0.3, houseSize.height, 0.3),
            wallMaterial
        );
        frontLeft.position.set(-houseSize.width * 0.35, houseSize.height / 2, -houseSize.depth / 2);
        frontLeft.castShadow = true;
        frontWall.add(frontLeft);

        const frontRight = new THREE.Mesh(
            new THREE.BoxGeometry(houseSize.width * 0.3, houseSize.height, 0.3),
            wallMaterial
        );
        frontRight.position.set(houseSize.width * 0.35, houseSize.height / 2, -houseSize.depth / 2);
        frontRight.castShadow = true;
        frontWall.add(frontRight);

        const frontTop = new THREE.Mesh(
            new THREE.BoxGeometry(houseSize.width * 0.4, houseSize.height * 0.3, 0.3),
            wallMaterial
        );
        frontTop.position.set(0, houseSize.height * 0.85, -houseSize.depth / 2);
        frontTop.castShadow = true;
        frontWall.add(frontTop);

        // Door
        const door = new THREE.Mesh(
            new THREE.BoxGeometry(2, 3, 0.2),
            new THREE.MeshStandardMaterial({ color: 0x654321 })
        );
        door.position.set(0, 1.5, -houseSize.depth / 2 - 0.05);
        door.castShadow = true;
        frontWall.add(door);

        frontWall.position.set(position[0], position[1], position[2]);
        group.add(frontWall);

        // Back wall
        const backWall = new THREE.Mesh(
            new THREE.BoxGeometry(houseSize.width, houseSize.height, 0.3),
            wallMaterial
        );
        backWall.position.set(position[0], position[1] + houseSize.height / 2, position[2] + houseSize.depth / 2);
        backWall.castShadow = true;
        group.add(backWall);

        // Left wall
        const leftWall = new THREE.Mesh(
            new THREE.BoxGeometry(0.3, houseSize.height, houseSize.depth),
            wallMaterial
        );
        leftWall.position.set(position[0] - houseSize.width / 2, position[1] + houseSize.height / 2, position[2]);
        leftWall.castShadow = true;
        group.add(leftWall);

        // Right wall
        const rightWall = new THREE.Mesh(
            new THREE.BoxGeometry(0.3, houseSize.height, houseSize.depth),
            wallMaterial
        );
        rightWall.position.set(position[0] + houseSize.width / 2, position[1] + houseSize.height / 2, position[2]);
        rightWall.castShadow = true;
        group.add(rightWall);

        // Roof
        const roofGeometry = new THREE.ConeGeometry(
            Math.sqrt(houseSize.width * houseSize.width + houseSize.depth * houseSize.depth) / 1.5,
            houseSize.height * 0.4,
            4
        );
        const roof = new THREE.Mesh(
            roofGeometry,
            new THREE.MeshStandardMaterial({
                color: 0x8b0000,
                roughness: 0.6
            })
        );
        roof.rotation.y = Math.PI / 4;
        roof.position.set(position[0], position[1] + houseSize.height + houseSize.height * 0.2, position[2]);
        roof.castShadow = true;
        group.add(roof);

        // Floor inside
        const floor = new THREE.Mesh(
            new THREE.PlaneGeometry(houseSize.width - 0.5, houseSize.depth - 0.5),
            new THREE.MeshStandardMaterial({
                color: 0x8b7355,
                roughness: 0.9
            })
        );
        floor.rotation.x = -Math.PI / 2;
        floor.position.set(position[0], position[1] + 0.01, position[2]);
        floor.receiveShadow = true;
        group.add(floor);

        group.userData.isHouse = true;
        group.userData.playerId = position;

        return group;
    }

    function createFurnitureMesh(furnitureData, housePosition, houseSize) {
        const furnitureType = HOUSING_CONFIG.furnitureTypes[furnitureData.type];
        if (!furnitureType) {
            console.warn(`⚠️ Unknown furniture type: ${furnitureData.type}`);
            return null;
        }

        // Create mesh based on furniture type
        const geometry = new THREE.BoxGeometry(
            furnitureType.width * (furnitureData.scale || 1),
            furnitureType.height * (furnitureData.scale || 1),
            furnitureType.depth * (furnitureData.scale || 1)
        );

        const material = new THREE.MeshStandardMaterial({
            color: furnitureType.color,
            roughness: 0.6
        });

        const mesh = new THREE.Mesh(geometry, material);

        // Position relative to house
        const relPos = furnitureData.position;
        mesh.position.set(
            housePosition[0] + relPos.x - houseSize.width / 2 + furnitureType.width / 2,
            housePosition[1] + furnitureType.height / 2,
            housePosition[2] + relPos.z - houseSize.depth / 2 + furnitureType.depth / 2
        );

        // Rotation
        mesh.rotation.y = furnitureData.rotation || 0;

        // Shadows
        mesh.castShadow = true;
        mesh.receiveShadow = true;

        // User data
        mesh.userData.furnitureType = furnitureData.type;
        mesh.userData.isFurniture = true;
        mesh.userData.emitsLight = furnitureType.emitsLight || false;

        return mesh;
    }

    function clearHouseVisualization(playerId) {
        if (!houseMeshes[playerId]) return;

        const houseData = houseMeshes[playerId];

        // Remove building
        if (houseData.building) {
            scene.remove(houseData.building);
        }

        // Remove furniture
        houseData.furniture.forEach(mesh => {
            scene.remove(mesh);
        });

        // Remove lights
        houseData.lights.forEach(light => {
            scene.remove(light);
        });

        delete houseMeshes[playerId];
    }

    // === INTERACTION ===

    function checkNearHouse(playerPosition) {
        if (!currentPlayerHouse) return null;

        const housePos = HOUSING_CONFIG.housePositions[`player${currentPlayerId}`] || [-200, 0, 400];
        const dist = Math.sqrt(
            Math.pow(playerPosition.x - housePos[0], 2) +
            Math.pow(playerPosition.z - housePos[2], 2)
        );

        if (dist < HOUSING_CONFIG.interactionRadius) {
            selectedHouse = currentPlayerHouse;

            // Check if inside house
            const houseSize = HOUSING_CONFIG.houseSizes[currentPlayerHouse.level] || HOUSING_CONFIG.houseSizes[1];
            if (dist < HOUSING_CONFIG.insideHouseRadius) {
                isInsideHouse = true;
            } else {
                isInsideHouse = false;
            }

            return currentPlayerHouse;
        }

        selectedHouse = null;
        isInsideHouse = false;
        return null;
    }

    function enterHouse() {
        if (!selectedHouse) {
            if (typeof notify === 'function') {
                notify('⚠️ Kein Haus in der Nähe', 'warning');
            }
            return false;
        }

        isInsideHouse = true;
        showHousingUI();
        updateHousingUI();

        console.log('🏠 Entered house');

        if (typeof notify === 'function') {
            notify(`🏠 Willkommen in deinem Haus (Level ${selectedHouse.level})`, 'info');
        }

        return true;
    }

    function exitHouse() {
        isInsideHouse = false;
        hideHousingUI();
        console.log('🏠 Exited house');
        return true;
    }

    // === UPDATE LOOP ===

    function updateHousing(delta, playerPosition) {
        if (!currentPlayerHouse) return;

        // Check proximity
        const nearHouse = checkNearHouse(playerPosition);

        if (nearHouse && !isInsideHouse) {
            // Show prompt to enter
            // (Handled by main system)
        }

        // Update UI if inside
        if (isInsideHouse) {
            updateHousingUI();
        }
    }

    // === UI ===

    function createHousingUI() {
        housingUI = document.createElement('div');
        housingUI.id = 'housing-ui';
        housingUI.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.85);
            border: 3px solid #8b7355;
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-family: monospace;
            font-size: 13px;
            display: none;
            z-index: 1000;
            max-width: 350px;
        `;

        housingUI.innerHTML = `
            <h3 style="margin: 0 0 15px 0; font-size: 18px; text-align: center;">
                🏠 Mein Haus
            </h3>
            <div id="house-info" style="margin-bottom: 15px;">
                <div><strong>Level:</strong> <span id="house-level">1</span>/10</div>
                <div><strong>Möbel:</strong> <span id="house-furniture-count">0</span>/<span id="house-max-furniture">20</span></div>
                <div style="margin-top: 8px;">
                    <button id="upgrade-house-btn" style="
                        width: 100%;
                        padding: 10px;
                        background: #50c878;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-family: monospace;
                        font-size: 13px;
                        cursor: pointer;
                        font-weight: bold;
                    ">🔨 Haus Upgraden</button>
                </div>
            </div>
            <div id="furniture-list" style="margin-bottom: 15px; max-height: 300px; overflow-y: auto;">
                <strong>Möbel:</strong>
                <div id="furniture-items" style="margin-top: 8px; font-size: 12px;">
                    Keine Möbel platziert
                </div>
            </div>
            <div style="margin-top: 15px;">
                <button id="place-furniture-btn" style="
                    width: 100%;
                    padding: 10px;
                    background: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 13px;
                    cursor: pointer;
                    font-weight: bold;
                    margin-bottom: 8px;
                ">➕ Möbel Platzieren</button>
                <button id="furniture-catalog-btn" style="
                    width: 100%;
                    padding: 10px;
                    background: #9b59b6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 13px;
                    cursor: pointer;
                    font-weight: bold;
                ">📖 Möbel Katalog</button>
            </div>
            <div style="margin-top: 15px; font-size: 11px; color: #aaa; text-align: center;">
                H: Schließen
            </div>
        `;

        document.body.appendChild(housingUI);

        // Button handlers
        const upgradeBtn = housingUI.querySelector('#upgrade-house-btn');
        if (upgradeBtn) {
            upgradeBtn.addEventListener('click', () => {
                upgradeHouse(currentPlayerId);
            });
        }

        const placeFurnitureBtn = housingUI.querySelector('#place-furniture-btn');
        if (placeFurnitureBtn) {
            placeFurnitureBtn.addEventListener('click', () => {
                showFurniturePlacementDialog();
            });
        }

        const catalogBtn = housingUI.querySelector('#furniture-catalog-btn');
        if (catalogBtn) {
            catalogBtn.addEventListener('click', async () => {
                const catalog = await loadFurnitureCatalog();
                if (catalog) {
                    showFurnitureCatalog(catalog);
                }
            });
        }
    }

    function showHousingUI() {
        if (!housingUI) return;
        housingUI.style.display = 'block';
        updateHousingUI();
    }

    function hideHousingUI() {
        if (!housingUI) return;
        housingUI.style.display = 'none';
    }

    function updateHousingUI() {
        if (!housingUI || !currentPlayerHouse) return;

        // Update house info
        const levelEl = housingUI.querySelector('#house-level');
        const furnitureCountEl = housingUI.querySelector('#house-furniture-count');
        const maxFurnitureEl = housingUI.querySelector('#house-max-furniture');

        if (levelEl) levelEl.textContent = currentPlayerHouse.level;
        if (furnitureCountEl) furnitureCountEl.textContent = (currentPlayerHouse.furniture || []).length;
        if (maxFurnitureEl) maxFurnitureEl.textContent = currentPlayerHouse.max_furniture;

        // Update furniture list
        const furnitureItemsEl = housingUI.querySelector('#furniture-items');
        if (furnitureItemsEl) {
            if (!currentPlayerHouse.furniture || currentPlayerHouse.furniture.length === 0) {
                furnitureItemsEl.innerHTML = 'Keine Möbel platziert';
            } else {
                let html = '';
                currentPlayerHouse.furniture.forEach((furniture, index) => {
                    const furnitureType = HOUSING_CONFIG.furnitureTypes[furniture.type];
                    const icon = furnitureType ? furnitureType.icon : '📦';
                    html += `
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            padding: 8px;
                            background: rgba(255,255,255,0.05);
                            border-radius: 6px;
                            margin-bottom: 6px;
                        ">
                            <span>${icon} ${furniture.type}</span>
                            <button onclick="window.HousingSystem.removeFurnitureByIndex(${index})" style="
                                padding: 4px 10px;
                                background: #e74c3c;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                font-size: 11px;
                                cursor: pointer;
                            ">🗑️</button>
                        </div>
                    `;
                });
                furnitureItemsEl.innerHTML = html;
            }
        }

        // Disable upgrade button if max level
        const upgradeBtn = housingUI.querySelector('#upgrade-house-btn');
        if (upgradeBtn) {
            if (currentPlayerHouse.level >= 10) {
                upgradeBtn.disabled = true;
                upgradeBtn.style.background = '#666';
                upgradeBtn.style.cursor = 'not-allowed';
                upgradeBtn.textContent = '✅ Max Level';
            } else {
                upgradeBtn.disabled = false;
                upgradeBtn.style.background = '#50c878';
                upgradeBtn.style.cursor = 'pointer';
                upgradeBtn.textContent = '🔨 Haus Upgraden';
            }
        }
    }

    function showFurniturePlacementDialog() {
        // Simple placement - random position for now
        const furnitureTypes = Object.keys(HOUSING_CONFIG.furnitureTypes);
        const randomType = furnitureTypes[Math.floor(Math.random() * furnitureTypes.length)];

        const furnitureData = {
            type: randomType,
            position: {
                x: Math.random() * 6 - 3,
                y: 0,
                z: Math.random() * 6 - 3
            },
            rotation: Math.random() * Math.PI * 2,
            scale: 1.0
        };

        placeFurniture(currentPlayerId, furnitureData);
    }

    function showFurnitureCatalog(catalog) {
        // Create catalog UI
        const catalogUI = document.createElement('div');
        catalogUI.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.95);
            border: 3px solid #8b7355;
            border-radius: 15px;
            padding: 25px;
            color: white;
            font-family: monospace;
            font-size: 13px;
            z-index: 2000;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
        `;

        let html = `
            <h2 style="margin: 0 0 20px 0; text-align: center;">📖 Möbel Katalog</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px;">
        `;

        catalog.forEach(item => {
            const furnitureType = HOUSING_CONFIG.furnitureTypes[item.type];
            const icon = furnitureType ? furnitureType.icon : '📦';
            html += `
                <div style="
                    background: rgba(255,255,255,0.1);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    border: 2px solid #8b7355;
                ">
                    <div style="font-size: 32px; margin-bottom: 8px;">${icon}</div>
                    <div style="font-weight: bold; margin-bottom: 5px;">${item.name}</div>
                    <div style="font-size: 11px; color: #aaa; margin-bottom: 8px;">${item.category}</div>
                    <div style="color: #ffd700; font-weight: bold;">${item.cost}G</div>
                </div>
            `;
        });

        html += `
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <button id="close-catalog-btn" style="
                    padding: 12px 30px;
                    background: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 14px;
                    cursor: pointer;
                    font-weight: bold;
                ">Schließen</button>
            </div>
        `;

        catalogUI.innerHTML = html;
        document.body.appendChild(catalogUI);

        const closeBtn = catalogUI.querySelector('#close-catalog-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                document.body.removeChild(catalogUI);
            });
        }
    }

    function removeFurnitureByIndex(index) {
        removeFurniture(currentPlayerId, index);
    }

    // === KEYBOARD HANDLER ===

    function setupKeyboardHandler() {
        document.addEventListener('keydown', (e) => {
            // H: Toggle Housing UI (only when near/inside house)
            if (e.code === 'KeyH' && (selectedHouse || isInsideHouse)) {
                if (housingUI && housingUI.style.display === 'block') {
                    hideHousingUI();
                } else {
                    showHousingUI();
                }
            }

            // E: Enter house (only when near and not inside)
            if (e.code === 'KeyE' && selectedHouse && !isInsideHouse) {
                // Check if no other system is active
                const buildingPrompt = document.getElementById('building-prompt-ui');
                if (buildingPrompt && buildingPrompt.style.display === 'block') {
                    return; // Building has priority
                }
                const gardenUI = document.getElementById('garden-ui');
                if (gardenUI && gardenUI.style.display === 'block') {
                    return; // Garden has priority
                }

                enterHouse();
            }
        });
    }

    // === 3D PLACEMENT INTEGRATION ===

    /**
     * Start 3D placement mode (called from housing UI)
     * @param {string} furnitureType - Furniture type key
     */
    function startPlacingFurniture(furnitureType) {
        if (!window.housing3DPlacement) {
            console.warn('⚠️ Housing3DPlacement not available');
            return;
        }

        const furnitureConfig = HOUSING_CONFIG.furnitureTypes[furnitureType];
        if (!furnitureConfig) {
            console.error(`❌ Unknown furniture type: ${furnitureType}`);
            return;
        }

        // Prepare furniture data for placement
        const furniture = {
            type: furnitureType,
            name: furnitureConfig.icon + ' ' + furnitureType,
            size: {
                x: furnitureConfig.width,
                y: furnitureConfig.height,
                z: furnitureConfig.depth
            },
            color: furnitureConfig.color
        };

        // Get house position
        const housePos = getHousePosition();
        const houseSize = getHouseSize();

        window.housing3DPlacement.startPlacement(furniture, housePos, houseSize);

        if (typeof notify === 'function') {
            notify(`🏠 Platziere ${furnitureType} (R = Drehen, Esc = Abbrechen)`, 'info');
        }
    }

    /**
     * Get current house position in world
     * @returns {THREE.Vector3}
     */
    function getHousePosition() {
        const THREE = window.THREE;
        const pos = HOUSING_CONFIG.housePositions[`player${currentPlayerId}`] || [0, 0, 0];
        return new THREE.Vector3(pos[0], pos[1], pos[2]);
    }

    /**
     * Get current house size
     * @returns {Object} {width, depth}
     */
    function getHouseSize() {
        const level = currentPlayerHouse?.level || 1;
        const size = HOUSING_CONFIG.houseSizes[level];
        return { width: size.width, depth: size.depth };
    }

    /**
     * Callback when furniture is placed (called from Housing3DPlacement)
     * @param {Object} placementData - {furniture, position, rotation}
     */
    async function onFurniturePlaced(placementData) {
        const furnitureData = {
            type: placementData.furniture.type,
            pos_x: placementData.position.x,
            pos_y: placementData.position.y,
            pos_z: placementData.position.z,
            rotation: placementData.rotation
        };

        const success = await placeFurniture(currentPlayerId, furnitureData);

        if (success && typeof notify === 'function') {
            notify('✅ Möbel platziert!', 'success');
        }
    }

    // === EXPORT ===

    window.HousingSystem = {
        init,
        setScene,
        setPlayerId,
        loadPlayerHouse,
        checkNearHouse,
        enterHouse,
        exitHouse,
        updateHousing,
        placeFurniture,
        removeFurniture,
        removeFurnitureByIndex,
        upgradeHouse,
        showHousingUI,
        hideHousingUI,
        updateHousingUI,
        startPlacingFurniture,
        onFurniturePlaced,
        get isInsideHouse() { return isInsideHouse; },
        get selectedHouse() { return selectedHouse; },
        get currentPlayerHouse() { return currentPlayerHouse; }
    };

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setupKeyboardHandler();
        });
    } else {
        setupKeyboardHandler();
    }

    console.log('🏠 Housing System 3D loaded!');
})();
