/**
 * World Map 3D Renderer
 * 9600×9600 Najika World - Vollständige 3D-Visualisierung
 *
 * Features:
 * - THREE.js basierte 3D-Darstellung der gesamten Welt
 * - 8 Biome mit korrekten Farben und Höhen
 * - Götterfels als zentraler Berg
 * - Cities und Special Locations
 * - Spieler-Position mit Marker
 * - Fast Travel Points
 * - Fog of War System
 * - Zoom, Pan, Rotate Funktionalität
 */

class WorldMap3DRenderer {
    constructor(container) {
        this.container = container;

        // THREE.js Components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;

        // World Data
        this.worldSize = 9600;
        this.scale = 0.1; // 9600 -> 960 units in 3D
        this.heightScale = 0.05; // Height multiplier for terrain

        this.regionsData = null;
        this.biomesData = null;
        this.citiesData = null;

        // 3D Objects
        this.terrainMeshes = [];
        this.cityMarkers = [];
        this.travelPointMarkers = [];
        this.playerMarker = null;

        // Player Data
        this.playerPosition = { x: 4800, z: 4800 }; // Start at center
        this.playerRotation = 0;

        // Fog of War
        this.exploredRegions = new Set();
        this.fogOfWarEnabled = true;

        // Animation
        this.animationId = null;
        this.clock = new THREE.Clock();

        this.init();
    }

    async init() {
        console.log('🗺️ Initializing World Map 3D Renderer...');

        // Load world data
        await this.loadWorldData();

        // Setup THREE.js scene
        this.setupScene();
        this.setupLighting();
        this.setupCamera();
        this.setupRenderer();
        this.setupControls();

        // Build world
        this.buildWorld();

        // Start animation loop
        this.animate();

        console.log('✅ World Map 3D Renderer initialized!');
    }

    async loadWorldData() {
        try {
            // Load regions data
            const regionsResponse = await fetch('/data/regions.json');
            this.regionsData = await regionsResponse.json();

            // Load biomes data
            const biomesResponse = await fetch('/data/biomes.json');
            this.biomesData = await biomesResponse.json();

            // Load cities data
            const citiesResponse = await fetch('/data/cities.json');
            this.citiesData = await citiesResponse.json();

            console.log('✅ World data loaded successfully');
        } catch (error) {
            console.error('❌ Failed to load world data:', error);
        }
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a15);
        this.scene.fog = new THREE.Fog(0x0a0a15, 500, 2000);
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        this.scene.add(ambientLight);

        // Directional light (sun)
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(500, 800, 300);
        dirLight.castShadow = true;
        dirLight.shadow.camera.left = -1000;
        dirLight.shadow.camera.right = 1000;
        dirLight.shadow.camera.top = 1000;
        dirLight.shadow.camera.bottom = -1000;
        this.scene.add(dirLight);

        // Hemisphere light for better color gradients
        const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x2d5016, 0.3);
        this.scene.add(hemiLight);
    }

    setupCamera() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 1, 3000);

        // Position camera for top-down view with slight angle
        this.camera.position.set(480, 600, 480); // Center of map
        this.camera.lookAt(480, 0, 480);
    }

    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        this.container.appendChild(this.renderer.domElement);

        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }

    setupControls() {
        // Simple orbit controls (we'll use OrbitControls if available)
        if (typeof THREE.OrbitControls !== 'undefined') {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
            this.controls.screenSpacePanning = false;
            this.controls.minDistance = 100;
            this.controls.maxDistance = 1500;
            this.controls.maxPolarAngle = Math.PI / 2.2; // Prevent going below ground
        }
    }

    buildWorld() {
        if (!this.regionsData || !this.biomesData) {
            console.error('❌ World data not loaded yet');
            return;
        }

        // Build terrain for each region
        Object.values(this.regionsData.regions).forEach(region => {
            this.buildRegionTerrain(region);
        });

        // Build Götterfels (central mountain)
        this.buildGoetterfels();

        // Add cities
        if (this.citiesData && this.citiesData.cities) {
            this.citiesData.cities.forEach(city => {
                this.addCityMarker(city);
            });
        }

        // Add player marker
        this.addPlayerMarker();

        // Add grid helper
        const gridHelper = new THREE.GridHelper(960, 48, 0x444444, 0x222222);
        gridHelper.position.set(480, 0, 480);
        this.scene.add(gridHelper);
    }

    buildRegionTerrain(region) {
        const biome = this.biomesData.biomes[region.biome];
        if (!biome) return;

        const bounds = region.bounds;
        const width = (bounds.maxX - bounds.minX) * this.scale;
        const depth = (bounds.maxZ - bounds.minZ) * this.scale;
        const centerX = (bounds.minX + (bounds.maxX - bounds.minX) / 2) * this.scale;
        const centerZ = (bounds.minZ + (bounds.maxZ - bounds.minZ) / 2) * this.scale;

        // Get terrain height
        const heightVariation = biome.terrain.heightVariation || 25;
        const avgHeight = heightVariation * this.heightScale;

        // Create plane geometry with segments for terrain variation
        const segments = 32;
        const geometry = new THREE.PlaneGeometry(width, depth, segments, segments);

        // Rotate to horizontal
        geometry.rotateX(-Math.PI / 2);

        // Add height variation using noise
        const positions = geometry.attributes.position;
        const noiseScale = biome.terrain.noiseScale || 0.02;

        for (let i = 0; i < positions.count; i++) {
            const x = positions.getX(i);
            const z = positions.getZ(i);

            // Simple noise function (in production, use proper noise library)
            const noise = this.simpleNoise(x * noiseScale, z * noiseScale);
            const height = noise * heightVariation * this.heightScale;

            positions.setY(i, height);
        }

        geometry.computeVertexNormals();

        // Create material based on biome color
        const groundColor = new THREE.Color(biome.colors.ground);
        const material = new THREE.MeshStandardMaterial({
            color: groundColor,
            roughness: 0.8,
            metalness: 0.2,
            flatShading: false
        });

        // Add fog of war effect if region not explored
        if (this.fogOfWarEnabled && !this.exploredRegions.has(region.id)) {
            material.transparent = true;
            material.opacity = 0.3;
            material.color.multiplyScalar(0.3); // Darken unexplored regions
        }

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(centerX, avgHeight / 2, centerZ);
        mesh.receiveShadow = true;
        mesh.userData = { region: region };

        this.scene.add(mesh);
        this.terrainMeshes.push(mesh);

        // Add special biome features
        this.addBiomeFeatures(region, biome, centerX, avgHeight, centerZ);
    }

    addBiomeFeatures(region, biome, centerX, baseHeight, centerZ) {
        // Add water for coastal/swamp biomes
        if (biome.waterPresence) {
            const bounds = region.bounds;
            const width = (bounds.maxX - bounds.minX) * this.scale;
            const depth = (bounds.maxZ - bounds.minZ) * this.scale;

            const waterGeometry = new THREE.PlaneGeometry(width * 0.6, depth * 0.6);
            waterGeometry.rotateX(-Math.PI / 2);

            const waterColor = biome.colors.water ?
                new THREE.Color(biome.colors.water) :
                new THREE.Color(0x1e90ff);

            const waterMaterial = new THREE.MeshStandardMaterial({
                color: waterColor,
                transparent: true,
                opacity: 0.6,
                roughness: 0.1,
                metalness: 0.8
            });

            const waterMesh = new THREE.Mesh(waterGeometry, waterMaterial);
            waterMesh.position.set(centerX, 0.5, centerZ);
            this.scene.add(waterMesh);
        }

        // Add lava for volcano biome
        if (biome.lavaFlows) {
            const bounds = region.bounds;
            const width = (bounds.maxX - bounds.minX) * this.scale;
            const depth = (bounds.maxZ - bounds.minZ) * this.scale;

            const lavaGeometry = new THREE.PlaneGeometry(width * 0.3, depth * 0.3);
            lavaGeometry.rotateX(-Math.PI / 2);

            const lavaColor = new THREE.Color(biome.colors.lava);
            const lavaMaterial = new THREE.MeshStandardMaterial({
                color: lavaColor,
                emissive: lavaColor,
                emissiveIntensity: 0.8,
                roughness: 0.5
            });

            const lavaMesh = new THREE.Mesh(lavaGeometry, lavaMaterial);
            lavaMesh.position.set(centerX, 1, centerZ);
            this.scene.add(lavaMesh);

            // Add glow effect
            const lavaLight = new THREE.PointLight(lavaColor, 1, 100);
            lavaLight.position.set(centerX, 5, centerZ);
            this.scene.add(lavaLight);
        }
    }

    buildGoetterfels() {
        const goetterfelsData = this.regionsData.regions.goetterfels;
        if (!goetterfelsData) return;

        const bounds = goetterfelsData.bounds;
        const width = (bounds.maxX - bounds.minX) * this.scale;
        const depth = (bounds.maxZ - bounds.minZ) * this.scale;
        const height = goetterfelsData.height * this.heightScale;

        const centerX = 480; // Center of world
        const centerZ = 480;

        // Create mountain geometry (cone-like shape)
        const segments = 64;
        const geometry = new THREE.ConeGeometry(width / 2, height, segments);

        // Add texture variation to make it look more natural
        const positions = geometry.attributes.position;
        for (let i = 0; i < positions.count; i++) {
            const x = positions.getX(i);
            const y = positions.getY(i);
            const z = positions.getZ(i);

            // Add some roughness
            const noise = this.simpleNoise(x * 0.1, z * 0.1) * 2;
            positions.setX(i, x + noise);
            positions.setZ(i, z + noise);
        }

        geometry.computeVertexNormals();

        // Mountain material (grey/brown rock)
        const material = new THREE.MeshStandardMaterial({
            color: 0x808080,
            roughness: 0.9,
            metalness: 0.1
        });

        const mountainMesh = new THREE.Mesh(geometry, material);
        mountainMesh.position.set(centerX, height / 2, centerZ);
        mountainMesh.castShadow = true;
        mountainMesh.receiveShadow = true;
        mountainMesh.userData = { type: 'goetterfels' };

        this.scene.add(mountainMesh);

        // Add peak marker (Schwarze Mühle)
        const peakGeometry = new THREE.SphereGeometry(3, 16, 16);
        const peakMaterial = new THREE.MeshStandardMaterial({
            color: 0xffff00,
            emissive: 0xffff00,
            emissiveIntensity: 0.5
        });
        const peakMarker = new THREE.Mesh(peakGeometry, peakMaterial);
        peakMarker.position.set(centerX, height + 5, centerZ - 20);
        this.scene.add(peakMarker);

        // Add label (will be rendered as sprite)
        this.addTextLabel('Götterfels\nSchwarze Mühle', centerX, height + 15, centerZ, 0xffffff);
    }

    addCityMarker(city) {
        const x = city.position.x * this.scale;
        const z = city.position.z * this.scale;

        // City marker size based on city size
        const sizeMap = { small: 5, medium: 8, large: 12 };
        const markerSize = sizeMap[city.size] || 5;

        // Create city marker (cylinder)
        const geometry = new THREE.CylinderGeometry(markerSize, markerSize, 15, 16);

        // Color based on capital status
        const color = city.isCapital ? 0xffd700 : 0x00ff00;
        const material = new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.3,
            transparent: true,
            opacity: 0.8
        });

        const marker = new THREE.Mesh(geometry, material);
        marker.position.set(x, 10, z);
        marker.userData = { type: 'city', city: city };

        this.scene.add(marker);
        this.cityMarkers.push(marker);

        // Add icon on top
        const iconGeometry = new THREE.SphereGeometry(markerSize * 0.6, 16, 16);
        const iconMaterial = new THREE.MeshStandardMaterial({
            color: 0xffffff,
            emissive: 0xffffff,
            emissiveIntensity: 0.5
        });
        const icon = new THREE.Mesh(iconGeometry, iconMaterial);
        icon.position.set(x, 18, z);
        this.scene.add(icon);

        // Add label
        this.addTextLabel(city.name, x, 25, z, color);
    }

    addPlayerMarker() {
        // Create player marker (glowing pyramid)
        const geometry = new THREE.ConeGeometry(5, 15, 4);
        const material = new THREE.MeshStandardMaterial({
            color: 0xe94560,
            emissive: 0xe94560,
            emissiveIntensity: 0.8,
            transparent: true,
            opacity: 0.9
        });

        this.playerMarker = new THREE.Mesh(geometry, material);
        this.playerMarker.userData = { type: 'player' };

        // Add pulsing glow
        const glowGeometry = new THREE.SphereGeometry(8, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: 0xe94560,
            transparent: true,
            opacity: 0.3
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        this.playerMarker.add(glow);

        this.scene.add(this.playerMarker);
        this.updatePlayerMarker();
    }

    updatePlayerMarker() {
        if (!this.playerMarker) return;

        const x = this.playerPosition.x * this.scale;
        const z = this.playerPosition.z * this.scale;

        // Get terrain height at player position
        const height = this.getTerrainHeightAt(this.playerPosition.x, this.playerPosition.z);

        this.playerMarker.position.set(x, height + 20, z);
        this.playerMarker.rotation.y = this.playerRotation;
    }

    getTerrainHeightAt(worldX, worldZ) {
        // Simple height lookup - in production, raycast against terrain
        // For now, return base height based on region
        const region = this.getRegionAt(worldX, worldZ);
        if (!region) return 5;

        const biome = this.biomesData.biomes[region.biome];
        if (!biome) return 5;

        const heightVariation = biome.terrain.heightVariation || 25;
        return heightVariation * this.heightScale / 2;
    }

    getRegionAt(worldX, worldZ) {
        if (!this.regionsData) return null;

        for (const region of Object.values(this.regionsData.regions)) {
            const bounds = region.bounds;
            if (worldX >= bounds.minX && worldX <= bounds.maxX &&
                worldZ >= bounds.minZ && worldZ <= bounds.maxZ) {
                return region;
            }
        }
        return null;
    }

    addTextLabel(text, x, y, z, color = 0xffffff) {
        // Create canvas for text
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 128;

        // Draw text
        context.fillStyle = '#000000';
        context.fillRect(0, 0, canvas.width, canvas.height);

        context.font = 'bold 24px Arial';
        context.fillStyle = '#' + color.toString(16).padStart(6, '0');
        context.textAlign = 'center';
        context.textBaseline = 'middle';

        const lines = text.split('\n');
        lines.forEach((line, i) => {
            context.fillText(line, canvas.width / 2, (canvas.height / 2) + (i * 30) - ((lines.length - 1) * 15));
        });

        // Create sprite
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({
            map: texture,
            transparent: true
        });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.position.set(x, y, z);
        sprite.scale.set(40, 20, 1);

        this.scene.add(sprite);
    }

    // Simple noise function (for terrain variation)
    simpleNoise(x, y) {
        // Very basic noise - in production use simplex/perlin noise
        const n = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
        return (n - Math.floor(n)) * 2 - 1;
    }

    // Public API for updating player position
    setPlayerPosition(x, z, rotation = 0) {
        this.playerPosition = { x, z };
        this.playerRotation = rotation;
        this.updatePlayerMarker();

        // Mark region as explored
        const region = this.getRegionAt(x, z);
        if (region) {
            this.addExploredRegion(region.id);
        }
    }

    addExploredRegion(regionId) {
        if (this.exploredRegions.has(regionId)) return;

        this.exploredRegions.add(regionId);

        // Update terrain mesh opacity
        this.terrainMeshes.forEach(mesh => {
            if (mesh.userData.region && mesh.userData.region.id === regionId) {
                mesh.material.transparent = false;
                mesh.material.opacity = 1.0;
                mesh.material.color.multiplyScalar(1 / 0.3); // Restore original color
                mesh.material.needsUpdate = true;
            }
        });
    }

    focusOnPlayer() {
        if (!this.playerMarker || !this.camera) return;

        const targetPos = this.playerMarker.position.clone();
        targetPos.y += 300; // Offset above player
        targetPos.z += 200; // Offset behind player

        this.camera.position.lerp(targetPos, 0.1);
        this.camera.lookAt(this.playerMarker.position);
    }

    focusOnRegion(regionId) {
        const region = this.regionsData.regions[regionId];
        if (!region) return;

        const bounds = region.bounds;
        const centerX = (bounds.minX + (bounds.maxX - bounds.minX) / 2) * this.scale;
        const centerZ = (bounds.minZ + (bounds.maxZ - bounds.minZ) / 2) * this.scale;

        this.camera.position.set(centerX, 400, centerZ + 300);
        this.camera.lookAt(centerX, 0, centerZ);
    }

    handleResize() {
        if (!this.camera || !this.renderer) return;

        const width = this.container.clientWidth;
        const height = this.container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();

        this.renderer.setSize(width, height);
    }

    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());

        const delta = this.clock.getDelta();

        // Update controls
        if (this.controls) {
            this.controls.update();
        }

        // Animate player marker (pulsing glow)
        if (this.playerMarker && this.playerMarker.children[0]) {
            const glow = this.playerMarker.children[0];
            const pulse = Math.sin(Date.now() * 0.003) * 0.5 + 0.5;
            glow.material.opacity = 0.2 + pulse * 0.2;
        }

        // Animate city markers (rotation)
        this.cityMarkers.forEach(marker => {
            marker.rotation.y += delta * 0.5;
        });

        // Render scene
        this.renderer.render(this.scene, this.camera);
    }

    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }

        // Clean up THREE.js resources
        this.terrainMeshes.forEach(mesh => {
            mesh.geometry.dispose();
            mesh.material.dispose();
        });

        this.cityMarkers.forEach(marker => {
            marker.geometry.dispose();
            marker.material.dispose();
        });

        if (this.playerMarker) {
            this.playerMarker.geometry.dispose();
            this.playerMarker.material.dispose();
        }

        if (this.renderer) {
            this.renderer.dispose();
        }

        if (this.container && this.renderer) {
            this.container.removeChild(this.renderer.domElement);
        }
    }

    // Public API
    toggleFogOfWar(enabled) {
        this.fogOfWarEnabled = enabled;
        this.buildWorld(); // Rebuild to apply changes
    }

    getExploredRegions() {
        return Array.from(this.exploredRegions);
    }

    clearExploredRegions() {
        this.exploredRegions.clear();
        this.buildWorld(); // Rebuild to apply changes
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WorldMap3DRenderer;
} else {
    window.WorldMap3DRenderer = WorldMap3DRenderer;
}
