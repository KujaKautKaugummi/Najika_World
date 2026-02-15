// 🌾 NAJIKA FARMING SYSTEM - 3D VISUALISIERUNG (Stardew Valley + Harvest Moon + Minecraft)
(function() {
    const FARMING_CONFIG = {
        // API Endpoint
        apiBaseUrl: 'http://localhost:8001/api/farming',

        // Farm Area in World (Near Schwarze Mühle)
        farmAreaCenter: [550, 0, 600],
        farmAreaRadius: 100,

        // Plot Layout (4 plots per player in 2x2 grid)
        plotLayout: {
            0: { offset: [-15, 0, -15], color: 0x654321 },
            1: { offset: [15, 0, -15], color: 0x654321 },
            2: { offset: [-15, 0, 15], color: 0x654321 },
            3: { offset: [15, 0, 15], color: 0x654321 }
        },

        // Crop Visualization by Growth Stage (0-4)
        cropStages: {
            0: { // Just planted
                height: 0.1,
                color: 0x3d2817,
                scale: 0.2
            },
            1: { // Seedling
                height: 0.5,
                color: 0x90ee90,
                scale: 0.4
            },
            2: { // Growing
                height: 1.0,
                color: 0x32cd32,
                scale: 0.6
            },
            3: { // Maturing
                height: 1.5,
                color: 0x228b22,
                scale: 0.8
            },
            4: { // Fully grown (ready to harvest)
                height: 2.0,
                color: 0xffd700,
                scale: 1.0,
                glow: true
            }
        },

        // Crop-specific visuals
        cropTypes: {
            wheat: { color: 0xf4a460, icon: '🌾', harvestColor: 0xdaa520 },
            corn: { color: 0xffd700, icon: '🌽', harvestColor: 0xffff00 },
            tomato: { color: 0xff6347, icon: '🍅', harvestColor: 0xff4500 },
            potato: { color: 0xd2b48c, icon: '🥔', harvestColor: 0xcd853f },
            carrot: { color: 0xff8c00, icon: '🥕', harvestColor: 0xff7f00 },
            lettuce: { color: 0x90ee90, icon: '🥬', harvestColor: 0x7cfc00 },
            pumpkin: { color: 0xff7f00, icon: '🎃', harvestColor: 0xff6600 },
            strawberry: { color: 0xff69b4, icon: '🍓', harvestColor: 0xff1493 }
        },

        // Tool visualizations
        tools: {
            hoe: { color: 0x8b4513, icon: '⛏️' },
            wateringCan: { color: 0x4169e1, icon: '🚿' },
            scythe: { color: 0xc0c0c0, icon: '🪓' }
        },

        // Interaction
        plotSize: 8,
        interactionRadius: 5
    };

    // State
    let farmPlots = [];
    let plotMeshes = [];
    let cropMeshes = {};  // { plotId: { soil, crop, particles } }
    let currentPlayerId = 1;
    let selectedPlot = null;
    let farmingUI = null;
    let scene = null;
    let particleSystem = null;

    // === PUBLIC API ===

    function init(threeScene, playerId = ((typeof getPlayerId === 'function') ? getPlayerId() : 1)) {
        scene = threeScene;
        currentPlayerId = playerId;
        console.log('🌾 Farming System 3D initialized');

        createFarmingUI();
        loadPlayerFarmPlots(currentPlayerId);
        initParticleSystem();

        return true;
    }

    function setScene(threeScene) {
        scene = threeScene;
    }

    function setPlayerId(playerId) {
        currentPlayerId = playerId;
        loadPlayerFarmPlots(playerId);
    }

    // === API CALLS ===

    async function loadPlayerFarmPlots(playerId) {
        try {
            const response = await fetch(`${FARMING_CONFIG.apiBaseUrl}/plots/${playerId}`);
            if (!response.ok) {
                console.warn(`⚠️ Could not load farm plots for player ${playerId}`);
                return null;
            }

            const plots = await response.json();
            farmPlots = plots;

            console.log(`🌾 Loaded ${plots.length} farm plots for player ${playerId}`);

            // Visualize plots in 3D
            if (scene) {
                visualizeFarmPlots(plots);
            }

            return plots;
        } catch (error) {
            console.error('❌ Error loading farm plots:', error);
            return null;
        }
    }

    async function plantCrop(playerId, plotIndex, cropType) {
        try {
            const response = await fetch(`${FARMING_CONFIG.apiBaseUrl}/plant`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: playerId,
                    plot_index: plotIndex,
                    crop_type: cropType
                })
            });

            if (!response.ok) {
                const error = await response.json();
                console.warn('⚠️ Could not plant crop:', error.detail);
                if (typeof notify === 'function') {
                    notify(`⚠️ ${error.detail}`, 'warning');
                }
                return false;
            }

            const result = await response.json();
            console.log('🌱 Crop planted:', result);

            // Reload plots to update visualization
            await loadPlayerFarmPlots(playerId);

            // Show planting animation
            showPlantingAnimation(plotIndex);

            if (typeof notify === 'function') {
                notify(`🌱 ${result.message}`, 'success');
            }

            return true;
        } catch (error) {
            console.error('❌ Error planting crop:', error);
            return false;
        }
    }

    async function waterCrop(plotId) {
        try {
            const response = await fetch(`${FARMING_CONFIG.apiBaseUrl}/water/${plotId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                const error = await response.json();
                console.warn('⚠️ Could not water crop:', error.detail);
                if (typeof notify === 'function') {
                    notify(`⚠️ ${error.detail}`, 'warning');
                }
                return false;
            }

            const result = await response.json();
            console.log('💧 Crop watered:', result);

            // Reload plots to update visualization
            await loadPlayerFarmPlots(currentPlayerId);

            // Show watering animation
            showWateringAnimation(plotId);

            if (typeof notify === 'function') {
                notify(`💧 ${result.message}`, 'success');
            }

            return true;
        } catch (error) {
            console.error('❌ Error watering crop:', error);
            return false;
        }
    }

    async function harvestCrop(playerId, plotId) {
        try {
            const response = await fetch(`${FARMING_CONFIG.apiBaseUrl}/harvest`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: playerId,
                    plot_id: plotId
                })
            });

            if (!response.ok) {
                const error = await response.json();
                console.warn('⚠️ Could not harvest crop:', error.detail);
                if (typeof notify === 'function') {
                    notify(`⚠️ ${error.detail}`, 'warning');
                }
                return false;
            }

            const result = await response.json();
            console.log('✅ Crop harvested:', result);

            // Show harvest animation before reloading
            showHarvestAnimation(plotId);

            // Reload plots to update visualization
            setTimeout(() => {
                loadPlayerFarmPlots(playerId);
            }, 500);

            if (typeof notify === 'function') {
                notify(`✅ ${result.message} (+${result.gold_earned}G)`, 'success');
            }

            return true;
        } catch (error) {
            console.error('❌ Error harvesting crop:', error);
            return false;
        }
    }

    async function loadCropCatalog() {
        try {
            const response = await fetch(`${FARMING_CONFIG.apiBaseUrl}/crops/catalog`);
            if (!response.ok) {
                console.warn('⚠️ Could not load crop catalog');
                return null;
            }

            const data = await response.json();
            return data.crops;
        } catch (error) {
            console.error('❌ Error loading crop catalog:', error);
            return null;
        }
    }

    // === 3D VISUALIZATION ===

    function visualizeFarmPlots(plots) {
        if (!scene) {
            console.warn('⚠️ Scene not initialized');
            return;
        }

        // Clear existing visualizations
        clearFarmVisualization();

        plots.forEach((plot, index) => {
            const layout = FARMING_CONFIG.plotLayout[plot.plot_index];
            if (!layout) return;

            // Calculate plot position
            const plotPos = [
                FARMING_CONFIG.farmAreaCenter[0] + layout.offset[0],
                FARMING_CONFIG.farmAreaCenter[1],
                FARMING_CONFIG.farmAreaCenter[2] + layout.offset[2]
            ];

            // Create soil plot
            const soilMesh = createSoilPlot(plotPos, plot);
            scene.add(soilMesh);
            plotMeshes.push(soilMesh);

            // Create crop if planted
            if (plot.crop_type) {
                const cropMesh = createCropMesh(plot, plotPos);
                if (cropMesh) {
                    scene.add(cropMesh);

                    cropMeshes[plot.id] = {
                        soil: soilMesh,
                        crop: cropMesh,
                        particles: null
                    };

                    // Add glow effect if ready to harvest
                    if (plot.ready_to_harvest) {
                        addGlowEffect(cropMesh);
                    }
                }
            } else {
                cropMeshes[plot.id] = {
                    soil: soilMesh,
                    crop: null,
                    particles: null
                };
            }
        });

        console.log(`🌾 Visualized ${plots.length} farm plots`);
    }

    function createSoilPlot(position, plotData) {
        const geometry = new THREE.BoxGeometry(
            FARMING_CONFIG.plotSize,
            0.2,
            FARMING_CONFIG.plotSize
        );

        // Darker soil if crop planted, lighter if empty
        const soilColor = plotData.crop_type ? 0x3d2817 : 0x654321;

        const material = new THREE.MeshStandardMaterial({
            color: soilColor,
            roughness: 0.9
        });

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(position[0], position[1] + 0.1, position[2]);
        mesh.receiveShadow = true;

        mesh.userData.isFarmPlot = true;
        mesh.userData.plotId = plotData.id;
        mesh.userData.plotIndex = plotData.plot_index;

        // Add border
        const borderGeometry = new THREE.EdgesGeometry(geometry);
        const borderMaterial = new THREE.LineBasicMaterial({ color: 0x8b4513, linewidth: 2 });
        const border = new THREE.LineSegments(borderGeometry, borderMaterial);
        mesh.add(border);

        return mesh;
    }

    function createCropMesh(plotData, position) {
        const growthStage = Math.min(plotData.growth_stage, 4);
        const stageConfig = FARMING_CONFIG.cropStages[growthStage];
        const cropConfig = FARMING_CONFIG.cropTypes[plotData.crop_type];

        if (!cropConfig) {
            console.warn(`⚠️ Unknown crop type: ${plotData.crop_type}`);
            return null;
        }

        // Create crop group
        const cropGroup = new THREE.Group();

        // Different shapes based on crop type
        let cropGeometry;
        if (plotData.crop_type === 'pumpkin' && growthStage >= 3) {
            // Pumpkin uses sphere
            cropGeometry = new THREE.SphereGeometry(
                stageConfig.height / 2 * stageConfig.scale,
                16,
                12
            );
        } else if (plotData.crop_type === 'wheat' || plotData.crop_type === 'corn') {
            // Wheat/Corn uses tall cylinder
            cropGeometry = new THREE.CylinderGeometry(
                0.1 * stageConfig.scale,
                0.2 * stageConfig.scale,
                stageConfig.height,
                8
            );
        } else {
            // Default: cone shape for plants
            cropGeometry = new THREE.ConeGeometry(
                0.5 * stageConfig.scale,
                stageConfig.height,
                8
            );
        }

        // Use crop-specific color if fully grown, otherwise stage color
        const cropColor = (growthStage >= 4 && cropConfig.harvestColor)
            ? cropConfig.harvestColor
            : (growthStage >= 2 ? cropConfig.color : stageConfig.color);

        const cropMaterial = new THREE.MeshStandardMaterial({
            color: cropColor,
            roughness: 0.6
        });

        const cropMesh = new THREE.Mesh(cropGeometry, cropMaterial);
        cropMesh.position.y = stageConfig.height / 2;
        cropMesh.castShadow = true;
        cropGroup.add(cropMesh);

        // Add leaves for certain crops
        if (growthStage >= 2 && ['tomato', 'lettuce', 'strawberry'].includes(plotData.crop_type)) {
            const leafGeometry = new THREE.SphereGeometry(0.3 * stageConfig.scale, 8, 6);
            const leafMaterial = new THREE.MeshStandardMaterial({
                color: 0x228b22,
                roughness: 0.7
            });

            for (let i = 0; i < 3; i++) {
                const leaf = new THREE.Mesh(leafGeometry, leafMaterial);
                const angle = (Math.PI * 2 / 3) * i;
                leaf.position.x = Math.cos(angle) * 0.4 * stageConfig.scale;
                leaf.position.z = Math.sin(angle) * 0.4 * stageConfig.scale;
                leaf.position.y = stageConfig.height * 0.7;
                leaf.castShadow = true;
                cropGroup.add(leaf);
            }
        }

        // Position group
        cropGroup.position.set(position[0], position[1] + 0.2, position[2]);

        cropGroup.userData.isCrop = true;
        cropGroup.userData.plotId = plotData.id;
        cropGroup.userData.cropType = plotData.crop_type;
        cropGroup.userData.growthStage = growthStage;
        cropGroup.userData.readyToHarvest = plotData.ready_to_harvest;

        return cropGroup;
    }

    function addGlowEffect(mesh) {
        // Add point light for glow
        const glowLight = new THREE.PointLight(0xffd700, 1.5, 5);
        glowLight.position.copy(mesh.position);
        glowLight.position.y += 1;
        scene.add(glowLight);

        // Store reference
        if (cropMeshes[mesh.userData.plotId]) {
            cropMeshes[mesh.userData.plotId].glowLight = glowLight;
        }

        // Animate glow (pulsing)
        const startIntensity = glowLight.intensity;
        let time = 0;
        const glowInterval = setInterval(() => {
            time += 0.05;
            glowLight.intensity = startIntensity + Math.sin(time) * 0.5;

            // Check if mesh still exists
            if (!scene.children.includes(mesh)) {
                clearInterval(glowInterval);
                scene.remove(glowLight);
            }
        }, 50);
    }

    function clearFarmVisualization() {
        // Remove plot meshes
        plotMeshes.forEach(mesh => {
            scene.remove(mesh);
        });
        plotMeshes = [];

        // Remove crop meshes and lights
        Object.values(cropMeshes).forEach(cropData => {
            if (cropData.crop) scene.remove(cropData.crop);
            if (cropData.glowLight) scene.remove(cropData.glowLight);
            if (cropData.particles) scene.remove(cropData.particles);
        });
        cropMeshes = {};
    }

    // === PARTICLE SYSTEM ===

    function initParticleSystem() {
        // Simple particle system for visual effects
        console.log('✨ Particle system initialized');
    }

    function showPlantingAnimation(plotIndex) {
        // Create particle burst (soil particles)
        const plot = farmPlots.find(p => p.plot_index === plotIndex);
        if (!plot) return;

        const layout = FARMING_CONFIG.plotLayout[plotIndex];
        if (!layout) return;

        const position = new THREE.Vector3(
            FARMING_CONFIG.farmAreaCenter[0] + layout.offset[0],
            FARMING_CONFIG.farmAreaCenter[1] + 0.5,
            FARMING_CONFIG.farmAreaCenter[2] + layout.offset[2]
        );

        createParticleBurst(position, 0x8b4513, 15);
    }

    function showWateringAnimation(plotId) {
        // Create water droplet particles
        const cropData = cropMeshes[plotId];
        if (!cropData || !cropData.soil) return;

        const position = cropData.soil.position.clone();
        position.y += 1;

        createParticleBurst(position, 0x4169e1, 20);
    }

    function showHarvestAnimation(plotId) {
        // Create sparkle particles
        const cropData = cropMeshes[plotId];
        if (!cropData || !cropData.crop) return;

        const position = cropData.crop.position.clone();
        position.y += 1;

        createParticleBurst(position, 0xffd700, 30);

        // Remove crop mesh immediately
        if (cropData.crop) {
            scene.remove(cropData.crop);
            cropData.crop = null;
        }
        if (cropData.glowLight) {
            scene.remove(cropData.glowLight);
            cropData.glowLight = null;
        }
    }

    function createParticleBurst(position, color, count) {
        if (!scene) return;

        const particles = [];
        const particleGeometry = new THREE.SphereGeometry(0.1, 4, 4);
        const particleMaterial = new THREE.MeshBasicMaterial({ color });

        for (let i = 0; i < count; i++) {
            const particle = new THREE.Mesh(particleGeometry, particleMaterial);
            particle.position.copy(position);

            // Random velocity
            const velocity = new THREE.Vector3(
                (Math.random() - 0.5) * 5,
                Math.random() * 5,
                (Math.random() - 0.5) * 5
            );

            particle.userData.velocity = velocity;
            particle.userData.life = 1.0;

            scene.add(particle);
            particles.push(particle);
        }

        // Animate particles
        const animateParticles = () => {
            let allDead = true;

            particles.forEach(particle => {
                if (particle.userData.life > 0) {
                    allDead = false;

                    // Update position
                    particle.position.add(
                        particle.userData.velocity.clone().multiplyScalar(0.016)
                    );

                    // Apply gravity
                    particle.userData.velocity.y -= 9.8 * 0.016;

                    // Fade out
                    particle.userData.life -= 0.016;
                    particle.material.opacity = particle.userData.life;
                    particle.material.transparent = true;
                }
            });

            if (!allDead) {
                requestAnimationFrame(animateParticles);
            } else {
                // Clean up
                particles.forEach(particle => {
                    scene.remove(particle);
                });
            }
        };

        animateParticles();
    }

    // === INTERACTION ===

    function checkNearPlot(playerPosition) {
        if (!farmPlots || farmPlots.length === 0) return null;

        let nearestPlot = null;
        let minDist = Infinity;

        farmPlots.forEach(plot => {
            const layout = FARMING_CONFIG.plotLayout[plot.plot_index];
            if (!layout) return;

            const plotPos = [
                FARMING_CONFIG.farmAreaCenter[0] + layout.offset[0],
                FARMING_CONFIG.farmAreaCenter[1],
                FARMING_CONFIG.farmAreaCenter[2] + layout.offset[2]
            ];

            const dist = Math.sqrt(
                Math.pow(playerPosition.x - plotPos[0], 2) +
                Math.pow(playerPosition.z - plotPos[2], 2)
            );

            if (dist < FARMING_CONFIG.interactionRadius && dist < minDist) {
                minDist = dist;
                nearestPlot = plot;
            }
        });

        if (nearestPlot) {
            selectedPlot = nearestPlot;
            showFarmingUI();
            updateFarmingUI();
        } else {
            selectedPlot = null;
            hideFarmingUI();
        }

        return nearestPlot;
    }

    // === UPDATE LOOP ===

    function updateFarming(delta, playerPosition) {
        if (!farmPlots || farmPlots.length === 0) return;

        // Check proximity to plots
        checkNearPlot(playerPosition);

        // Update crop growth visuals (could add subtle animations here)
    }

    // === UI ===

    function createFarmingUI() {
        farmingUI = document.createElement('div');
        farmingUI.id = 'farming-ui';
        farmingUI.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.85);
            border: 3px solid #228b22;
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-family: monospace;
            font-size: 13px;
            display: none;
            z-index: 1000;
            max-width: 350px;
        `;

        farmingUI.innerHTML = `
            <h3 style="margin: 0 0 15px 0; font-size: 18px; text-align: center;">
                🌾 Farm Plot
            </h3>
            <div id="plot-info" style="margin-bottom: 15px;">
                <div><strong>Plot:</strong> <span id="plot-number">-</span></div>
                <div><strong>Crop:</strong> <span id="plot-crop">Empty</span></div>
                <div><strong>Growth:</strong> <span id="plot-growth">-</span></div>
                <div><strong>Status:</strong> <span id="plot-status">-</span></div>
            </div>
            <div id="plot-actions" style="margin-top: 15px;">
                <button id="plant-btn" style="
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
                    margin-bottom: 8px;
                ">🌱 Plant Crop</button>
                <button id="water-btn" style="
                    width: 100%;
                    padding: 10px;
                    background: #4169e1;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 13px;
                    cursor: pointer;
                    font-weight: bold;
                    margin-bottom: 8px;
                ">💧 Water Crop</button>
                <button id="harvest-btn" style="
                    width: 100%;
                    padding: 10px;
                    background: #ffd700;
                    color: black;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 13px;
                    cursor: pointer;
                    font-weight: bold;
                ">✂️ Harvest</button>
            </div>
            <div style="margin-top: 15px; font-size: 11px; color: #aaa; text-align: center;">
                E: Quick Action | F: Farm Menu
            </div>
        `;

        document.body.appendChild(farmingUI);

        // Button handlers
        const plantBtn = farmingUI.querySelector('#plant-btn');
        if (plantBtn) {
            plantBtn.addEventListener('click', () => {
                showCropSelectionDialog();
            });
        }

        const waterBtn = farmingUI.querySelector('#water-btn');
        if (waterBtn) {
            waterBtn.addEventListener('click', () => {
                if (selectedPlot) {
                    waterCrop(selectedPlot.id);
                }
            });
        }

        const harvestBtn = farmingUI.querySelector('#harvest-btn');
        if (harvestBtn) {
            harvestBtn.addEventListener('click', () => {
                if (selectedPlot) {
                    harvestCrop(currentPlayerId, selectedPlot.id);
                }
            });
        }
    }

    function showFarmingUI() {
        if (!farmingUI) return;
        farmingUI.style.display = 'block';
        updateFarmingUI();
    }

    function hideFarmingUI() {
        if (!farmingUI) return;
        farmingUI.style.display = 'none';
    }

    function updateFarmingUI() {
        if (!farmingUI || !selectedPlot) return;

        // Update plot info
        const plotNumberEl = farmingUI.querySelector('#plot-number');
        const plotCropEl = farmingUI.querySelector('#plot-crop');
        const plotGrowthEl = farmingUI.querySelector('#plot-growth');
        const plotStatusEl = farmingUI.querySelector('#plot-status');

        if (plotNumberEl) plotNumberEl.textContent = selectedPlot.plot_index + 1;

        if (plotCropEl) {
            const cropConfig = FARMING_CONFIG.cropTypes[selectedPlot.crop_type];
            const cropName = selectedPlot.crop_type
                ? `${cropConfig ? cropConfig.icon : '🌱'} ${selectedPlot.crop_type}`
                : 'Empty';
            plotCropEl.textContent = cropName;
        }

        if (plotGrowthEl) {
            if (selectedPlot.crop_type) {
                plotGrowthEl.innerHTML = `Stage ${selectedPlot.growth_stage}/4`;
            } else {
                plotGrowthEl.textContent = '-';
            }
        }

        if (plotStatusEl) {
            if (selectedPlot.ready_to_harvest) {
                plotStatusEl.innerHTML = '<span style="color: #ffd700;">✨ Ready to Harvest!</span>';
            } else if (selectedPlot.crop_type) {
                plotStatusEl.innerHTML = selectedPlot.watered_at
                    ? '<span style="color: #4169e1;">💧 Watered</span>'
                    : '<span style="color: #ff6347;">🚫 Needs Water</span>';
            } else {
                plotStatusEl.textContent = 'Empty';
            }
        }

        // Update button states
        const plantBtn = farmingUI.querySelector('#plant-btn');
        const waterBtn = farmingUI.querySelector('#water-btn');
        const harvestBtn = farmingUI.querySelector('#harvest-btn');

        if (plantBtn) {
            plantBtn.disabled = !!selectedPlot.crop_type;
            plantBtn.style.opacity = plantBtn.disabled ? '0.5' : '1';
            plantBtn.style.cursor = plantBtn.disabled ? 'not-allowed' : 'pointer';
        }

        if (waterBtn) {
            waterBtn.disabled = !selectedPlot.crop_type || selectedPlot.ready_to_harvest;
            waterBtn.style.opacity = waterBtn.disabled ? '0.5' : '1';
            waterBtn.style.cursor = waterBtn.disabled ? 'not-allowed' : 'pointer';
        }

        if (harvestBtn) {
            harvestBtn.disabled = !selectedPlot.ready_to_harvest;
            harvestBtn.style.opacity = harvestBtn.disabled ? '0.5' : '1';
            harvestBtn.style.cursor = harvestBtn.disabled ? 'not-allowed' : 'pointer';
        }
    }

    async function showCropSelectionDialog() {
        const catalog = await loadCropCatalog();
        if (!catalog) {
            if (typeof notify === 'function') {
                notify('⚠️ Could not load crop catalog', 'warning');
            }
            return;
        }

        // Create selection dialog
        const dialog = document.createElement('div');
        dialog.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.95);
            border: 3px solid #228b22;
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
            <h2 style="margin: 0 0 20px 0; text-align: center;">🌱 Select Crop</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px;">
        `;

        catalog.forEach(crop => {
            const cropConfig = FARMING_CONFIG.cropTypes[crop.type];
            const icon = cropConfig ? cropConfig.icon : '🌱';
            html += `
                <div onclick="window.FarmingSystem.selectCropForPlanting('${crop.type}')" style="
                    background: rgba(255,255,255,0.1);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    border: 2px solid #228b22;
                    cursor: pointer;
                    transition: all 0.2s;
                " onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                    <div style="font-size: 40px; margin-bottom: 8px;">${icon}</div>
                    <div style="font-weight: bold; margin-bottom: 5px;">${crop.name}</div>
                    <div style="font-size: 11px; color: #aaa; margin-bottom: 5px;">
                        Growth: ${crop.growth_time_hours}h
                    </div>
                    <div style="color: #ffd700; font-weight: bold;">
                        Sells for ${crop.sell_price}G
                    </div>
                </div>
            `;
        });

        html += `
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <button id="cancel-crop-selection" style="
                    padding: 12px 30px;
                    background: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 14px;
                    cursor: pointer;
                    font-weight: bold;
                ">Cancel</button>
            </div>
        `;

        dialog.innerHTML = html;
        document.body.appendChild(dialog);

        const cancelBtn = dialog.querySelector('#cancel-crop-selection');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                document.body.removeChild(dialog);
            });
        }

        // Store dialog reference for removal
        window._cropSelectionDialog = dialog;
    }

    function selectCropForPlanting(cropType) {
        if (selectedPlot) {
            plantCrop(currentPlayerId, selectedPlot.plot_index, cropType);
        }

        // Close dialog
        if (window._cropSelectionDialog) {
            document.body.removeChild(window._cropSelectionDialog);
            window._cropSelectionDialog = null;
        }
    }

    // === KEYBOARD HANDLER ===

    function setupKeyboardHandler() {
        document.addEventListener('keydown', (e) => {
            // E: Quick action (plant/water/harvest)
            if (e.code === 'KeyE' && selectedPlot && !window.combatActive) {
                // Check if no other system is active
                const buildingPrompt = document.getElementById('building-prompt-ui');
                if (buildingPrompt && buildingPrompt.style.display === 'block') {
                    return; // Building has priority
                }
                const housingUI = document.getElementById('housing-ui');
                if (housingUI && housingUI.style.display === 'block') {
                    return; // Housing has priority
                }

                // Quick action based on plot state
                if (!selectedPlot.crop_type) {
                    // Empty plot - show crop selection
                    showCropSelectionDialog();
                } else if (selectedPlot.ready_to_harvest) {
                    // Ready - harvest
                    harvestCrop(currentPlayerId, selectedPlot.id);
                } else {
                    // Growing - water
                    waterCrop(selectedPlot.id);
                }
            }

            // F: Farming-Menü für ausgewähltes Feld
            if (e.code === 'KeyF' && selectedPlot) {
                const plot = selectedPlot;
                const crops = ['wheat', 'potato', 'carrot', 'herb_green', 'herb_blue', 'herb_red'];
                const cropNames = { wheat: 'Weizen', potato: 'Kartoffel', carrot: 'Karotte', herb_green: 'Heilkraut', herb_blue: 'Manakraut', herb_red: 'Feuerkraut' };
                if (!plot.crop) {
                    // Pflanzen-Auswahl zeigen
                    const menu = crops.map((c, i) => `${i + 1}. ${cropNames[c] || c}`).join('\n');
                    if (typeof notify === 'function') notify(`🌾 Drücke 1-${crops.length} zum Pflanzen:\n${menu}`, 'info');
                    const cropHandler = (ev) => {
                        const idx = parseInt(ev.key) - 1;
                        if (idx >= 0 && idx < crops.length) {
                            plantCrop(currentPlayerId, plot.id, crops[idx]);
                            document.removeEventListener('keydown', cropHandler);
                        }
                        if (ev.key === 'Escape') document.removeEventListener('keydown', cropHandler);
                    };
                    document.addEventListener('keydown', cropHandler);
                } else if (plot.crop.ready) {
                    harvestCrop(currentPlayerId, plot.id);
                } else {
                    waterCrop(plot.id);
                }
            }
        });
    }

    // === EXPORT ===

    window.FarmingSystem = {
        init,
        setScene,
        setPlayerId,
        loadPlayerFarmPlots,
        checkNearPlot,
        updateFarming,
        plantCrop,
        waterCrop,
        harvestCrop,
        showFarmingUI,
        hideFarmingUI,
        updateFarmingUI,
        selectCropForPlanting,
        get selectedPlot() { return selectedPlot; },
        get farmPlots() { return farmPlots; }
    };

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setupKeyboardHandler();
        });
    } else {
        setupKeyboardHandler();
    }

    console.log('🌾 Farming System 3D loaded!');
})();
