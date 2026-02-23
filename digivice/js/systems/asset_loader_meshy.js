/**
 * MESHY ASSET LOADER SYSTEM
 *
 * Handles loading and managing 3D assets generated from Meshy AI
 * Supports: GLB, GLTF formats with animations
 *
 * Features:
 * - Async loading with progress tracking
 * - Animation controller
 * - LOD (Level of Detail) management
 * - Asset caching
 * - Texture optimization
 */

// THREE is loaded globally
const GLTFLoader = THREE.GLTFLoader || (window.THREE && window.THREE.GLTFLoader);
const DRACOLoader = THREE.DRACOLoader || (window.THREE && window.THREE.DRACOLoader);

class MeshyAssetLoader {
    constructor(scene) {
        this.scene = scene;
        this.loadedAssets = new Map(); // Asset cache
        this.animationMixers = new Map(); // Animation mixers per asset
        this.loadingQueue = [];
        this.isLoading = false;

        // Initialize loaders
        this.gltfLoader = new GLTFLoader();
        this.dracoLoader = new DRACOLoader();
        this.dracoLoader.setDecoderPath('/static/libs/draco/');
        this.gltfLoader.setDRACOLoader(this.dracoLoader);

        // Asset base path
        this.assetBasePath = '/static/assets/meshy/';

        // LOD settings
        this.lodSettings = {
            high: { distance: 50, quality: 1.0 },
            medium: { distance: 100, quality: 0.6 },
            low: { distance: 200, quality: 0.3 }
        };

        console.log('[MeshyAssetLoader] Initialized');
    }

    /**
     * Load a single Meshy asset
     * @param {string} assetId - Asset identifier (e.g., 'slime_basic_ice_blue')
     * @param {object} options - Loading options
     * @returns {Promise<THREE.Group>} Loaded 3D object
     */
    async loadAsset(assetId, options = {}) {
        const {
            scale = 1.0,
            position = { x: 0, y: 0, z: 0 },
            rotation = { x: 0, y: 0, z: 0 },
            enableLOD = true,
            enableShadows = true,
            playAnimation = null, // Animation name to auto-play
            animationLoop = true
        } = options;

        // Check cache
        if (this.loadedAssets.has(assetId)) {
            console.log(`[MeshyAssetLoader] Using cached asset: ${assetId}`);
            return this.createInstance(assetId, options);
        }

        // Construct file path
        const filePath = `${this.assetBasePath}${assetId}.glb`;

        console.log(`[MeshyAssetLoader] Loading asset: ${assetId} from ${filePath}`);

        try {
            const gltf = await this.loadGLTF(filePath);

            // Cache the loaded asset
            this.loadedAssets.set(assetId, {
                scene: gltf.scene,
                animations: gltf.animations,
                cameras: gltf.cameras,
                metadata: gltf.userData
            });

            console.log(`[MeshyAssetLoader] Successfully loaded: ${assetId}`);
            console.log(`  - Animations: ${gltf.animations.length}`);
            console.log(`  - Meshes: ${this.countMeshes(gltf.scene)}`);

            // Create and configure instance
            return this.createInstance(assetId, options);

        } catch (error) {
            console.error(`[MeshyAssetLoader] Failed to load ${assetId}:`, error);
            return this.createFallbackModel(assetId);
        }
    }

    /**
     * Load GLTF file
     */
    loadGLTF(path) {
        return new Promise((resolve, reject) => {
            this.gltfLoader.load(
                path,
                (gltf) => resolve(gltf),
                (progress) => {
                    const percent = (progress.loaded / progress.total) * 100;
                    console.log(`[MeshyAssetLoader] Loading: ${percent.toFixed(1)}%`);
                },
                (error) => reject(error)
            );
        });
    }

    /**
     * Create an instance of a cached asset
     */
    createInstance(assetId, options) {
        const cached = this.loadedAssets.get(assetId);
        if (!cached) {
            console.error(`[MeshyAssetLoader] Asset not in cache: ${assetId}`);
            return this.createFallbackModel(assetId);
        }

        // Clone the scene
        const instance = cached.scene.clone();

        // Apply transformations
        instance.scale.setScalar(options.scale || 1.0);
        instance.position.set(
            options.position?.x || 0,
            options.position?.y || 0,
            options.position?.z || 0
        );
        instance.rotation.set(
            options.rotation?.x || 0,
            options.rotation?.y || 0,
            options.rotation?.z || 0
        );

        // Configure shadows
        if (options.enableShadows !== false) {
            instance.traverse((child) => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                }
            });
        }

        // Setup animations
        if (cached.animations.length > 0) {
            const mixer = new THREE.AnimationMixer(instance);
            const instanceId = this.generateInstanceId();

            this.animationMixers.set(instanceId, {
                mixer,
                actions: new Map(),
                currentAction: null
            });

            // Create animation actions
            cached.animations.forEach((clip) => {
                const action = mixer.clipAction(clip);
                this.animationMixers.get(instanceId).actions.set(clip.name, action);
            });

            // Auto-play animation if specified
            if (options.playAnimation) {
                this.playAnimation(instanceId, options.playAnimation, options.animationLoop);
            }

            instance.userData.animationInstanceId = instanceId;
        }

        // Setup LOD if enabled
        if (options.enableLOD) {
            this.setupLOD(instance);
        }

        return instance;
    }

    /**
     * Setup Level of Detail (LOD) for an object
     */
    setupLOD(object) {
        const lod = new THREE.LOD();

        // High detail (original)
        const highDetail = object.clone();
        lod.addLevel(highDetail, this.lodSettings.high.distance);

        // Medium detail (simplified)
        const mediumDetail = this.simplifyModel(object.clone(), this.lodSettings.medium.quality);
        lod.addLevel(mediumDetail, this.lodSettings.medium.distance);

        // Low detail (very simplified)
        const lowDetail = this.simplifyModel(object.clone(), this.lodSettings.low.quality);
        lod.addLevel(lowDetail, this.lodSettings.low.distance);

        return lod;
    }

    /**
     * Simplify model geometry (basic implementation)
     */
    simplifyModel(object, quality) {
        object.traverse((child) => {
            if (child.isMesh && child.geometry) {
                // Simple decimation: reduce vertex count
                // TODO: Implement proper mesh simplification algorithm
                child.material.wireframe = false;
            }
        });
        return object;
    }

    /**
     * Play animation on an instance
     */
    playAnimation(instanceId, animationName, loop = true) {
        const animData = this.animationMixers.get(instanceId);
        if (!animData) {
            console.warn(`[MeshyAssetLoader] No animation data for instance: ${instanceId}`);
            return false;
        }

        const action = animData.actions.get(animationName);
        if (!action) {
            console.warn(`[MeshyAssetLoader] Animation not found: ${animationName}`);
            console.log(`Available animations:`, Array.from(animData.actions.keys()));
            return false;
        }

        // Stop current animation
        if (animData.currentAction) {
            animData.currentAction.fadeOut(0.5);
        }

        // Play new animation
        action.reset();
        action.setLoop(loop ? THREE.LoopRepeat : THREE.LoopOnce, loop ? Infinity : 1);
        action.fadeIn(0.5);
        action.play();

        animData.currentAction = action;

        console.log(`[MeshyAssetLoader] Playing animation: ${animationName} (loop: ${loop})`);
        return true;
    }

    /**
     * Stop animation
     */
    stopAnimation(instanceId) {
        const animData = this.animationMixers.get(instanceId);
        if (animData && animData.currentAction) {
            animData.currentAction.stop();
            animData.currentAction = null;
        }
    }

    /**
     * Update all animation mixers (call in render loop)
     */
    update(deltaTime) {
        this.animationMixers.forEach((animData) => {
            animData.mixer.update(deltaTime);
        });
    }

    /**
     * Load multiple assets in batch
     */
    async loadBatch(assetIds, options = {}) {
        console.log(`[MeshyAssetLoader] Loading batch of ${assetIds.length} assets...`);

        const promises = assetIds.map((id) => this.loadAsset(id, options));

        try {
            const results = await Promise.all(promises);
            console.log(`[MeshyAssetLoader] Batch loaded successfully`);
            return results;
        } catch (error) {
            console.error(`[MeshyAssetLoader] Batch load failed:`, error);
            return [];
        }
    }

    /**
     * Preload assets (load into cache without adding to scene)
     */
    async preloadAssets(assetIds) {
        console.log(`[MeshyAssetLoader] Preloading ${assetIds.length} assets...`);

        for (const id of assetIds) {
            if (!this.loadedAssets.has(id)) {
                await this.loadAsset(id, { addToScene: false });
            }
        }

        console.log(`[MeshyAssetLoader] Preload complete`);
    }

    /**
     * Get list of available animations for an asset
     */
    getAvailableAnimations(assetId) {
        const cached = this.loadedAssets.get(assetId);
        if (!cached) return [];

        return cached.animations.map((clip) => clip.name);
    }

    /**
     * Remove asset from scene and cleanup
     */
    removeAsset(object) {
        // Stop animations
        const instanceId = object.userData?.animationInstanceId;
        if (instanceId) {
            this.stopAnimation(instanceId);
            this.animationMixers.delete(instanceId);
        }

        // Remove from scene
        if (object.parent) {
            object.parent.remove(object);
        }

        // Dispose geometries and materials
        object.traverse((child) => {
            if (child.isMesh) {
                child.geometry?.dispose();

                if (Array.isArray(child.material)) {
                    child.material.forEach((mat) => mat.dispose());
                } else {
                    child.material?.dispose();
                }
            }
        });

        console.log(`[MeshyAssetLoader] Asset removed and cleaned up`);
    }

    /**
     * Clear cache
     */
    clearCache() {
        console.log(`[MeshyAssetLoader] Clearing cache (${this.loadedAssets.size} assets)...`);

        this.loadedAssets.forEach((asset, id) => {
            asset.scene.traverse((child) => {
                if (child.isMesh) {
                    child.geometry?.dispose();
                    if (Array.isArray(child.material)) {
                        child.material.forEach((mat) => mat.dispose());
                    } else {
                        child.material?.dispose();
                    }
                }
            });
        });

        this.loadedAssets.clear();
        this.animationMixers.clear();

        console.log(`[MeshyAssetLoader] Cache cleared`);
    }

    /**
     * Create fallback model (colored cube) when asset fails to load
     */
    createFallbackModel(assetId) {
        console.warn(`[MeshyAssetLoader] Creating fallback model for: ${assetId}`);

        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshStandardMaterial({
            color: 0xff00ff,
            wireframe: true
        });
        const mesh = new THREE.Mesh(geometry, material);

        const group = new THREE.Group();
        group.add(mesh);
        group.userData.isFallback = true;

        return group;
    }

    /**
     * Utility: Count meshes in a scene
     */
    countMeshes(object) {
        let count = 0;
        object.traverse((child) => {
            if (child.isMesh) count++;
        });
        return count;
    }

    /**
     * Generate unique instance ID
     */
    generateInstanceId() {
        return `instance_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Get memory usage statistics
     */
    getStats() {
        return {
            cachedAssets: this.loadedAssets.size,
            activeMixers: this.animationMixers.size,
            memoryEstimate: this.estimateMemoryUsage()
        };
    }

    /**
     * Estimate memory usage (rough calculation)
     */
    estimateMemoryUsage() {
        let totalBytes = 0;

        this.loadedAssets.forEach((asset) => {
            asset.scene.traverse((child) => {
                if (child.isMesh && child.geometry) {
                    const positions = child.geometry.attributes.position;
                    if (positions) {
                        totalBytes += positions.array.byteLength;
                    }
                }
            });
        });

        return {
            bytes: totalBytes,
            mb: (totalBytes / 1024 / 1024).toFixed(2)
        };
    }
}

/**
 * ASSET MANAGER
 * High-level API for managing all Meshy assets in the game
 */
class MeshyAssetManager {
    constructor(scene, camera) {
        this.scene = scene;
        this.camera = camera;
        this.loader = new MeshyAssetLoader(scene);

        // Asset registry
        this.spawnedAssets = new Map(); // Track all spawned assets
        this.assetGroups = new Map(); // Organize assets by category

        console.log('[MeshyAssetManager] Initialized');
    }

    /**
     * Spawn asset into the game world
     */
    async spawnAsset(assetId, options = {}) {
        const {
            category = 'misc',
            name = assetId,
            ...loadOptions
        } = options;

        const object = await this.loader.loadAsset(assetId, loadOptions);

        // Add to scene
        this.scene.add(object);

        // Track asset
        const spawnId = this.loader.generateInstanceId();
        this.spawnedAssets.set(spawnId, {
            object,
            assetId,
            category,
            name,
            spawnedAt: Date.now()
        });

        // Add to category group
        if (!this.assetGroups.has(category)) {
            this.assetGroups.set(category, []);
        }
        this.assetGroups.get(category).push(spawnId);

        console.log(`[MeshyAssetManager] Spawned: ${name} (${assetId}) [${spawnId}]`);

        return {
            spawnId,
            object
        };
    }

    /**
     * Spawn multiple assets
     */
    async spawnBatch(assetList) {
        const promises = assetList.map((item) => this.spawnAsset(item.assetId, item.options));
        return await Promise.all(promises);
    }

    /**
     * Remove spawned asset
     */
    removeSpawnedAsset(spawnId) {
        const asset = this.spawnedAssets.get(spawnId);
        if (!asset) {
            console.warn(`[MeshyAssetManager] Asset not found: ${spawnId}`);
            return false;
        }

        // Remove from scene
        this.loader.removeAsset(asset.object);

        // Remove from tracking
        this.spawnedAssets.delete(spawnId);

        // Remove from category group
        const categoryAssets = this.assetGroups.get(asset.category);
        if (categoryAssets) {
            const index = categoryAssets.indexOf(spawnId);
            if (index > -1) {
                categoryAssets.splice(index, 1);
            }
        }

        console.log(`[MeshyAssetManager] Removed: ${asset.name} [${spawnId}]`);
        return true;
    }

    /**
     * Get all assets in a category
     */
    getAssetsByCategory(category) {
        const spawnIds = this.assetGroups.get(category) || [];
        return spawnIds.map((id) => this.spawnedAssets.get(id)).filter(Boolean);
    }

    /**
     * Play animation on spawned asset
     */
    playAnimation(spawnId, animationName, loop = true) {
        const asset = this.spawnedAssets.get(spawnId);
        if (!asset) {
            console.warn(`[MeshyAssetManager] Asset not found: ${spawnId}`);
            return false;
        }

        const instanceId = asset.object.userData.animationInstanceId;
        if (!instanceId) {
            console.warn(`[MeshyAssetManager] No animations on asset: ${spawnId}`);
            return false;
        }

        return this.loader.playAnimation(instanceId, animationName, loop);
    }

    /**
     * Update loop (call in render loop)
     */
    update(deltaTime) {
        this.loader.update(deltaTime);
    }

    /**
     * Cleanup all spawned assets
     */
    cleanup() {
        console.log(`[MeshyAssetManager] Cleaning up ${this.spawnedAssets.size} assets...`);

        this.spawnedAssets.forEach((asset, spawnId) => {
            this.removeSpawnedAsset(spawnId);
        });

        this.loader.clearCache();

        console.log(`[MeshyAssetManager] Cleanup complete`);
    }

    /**
     * Get statistics
     */
    getStats() {
        return {
            spawnedAssets: this.spawnedAssets.size,
            categories: this.assetGroups.size,
            loader: this.loader.getStats()
        };
    }
}

// Global export (nicht als ES6 Modul geladen)
window.MeshyAssetLoader = MeshyAssetLoader;
window.MeshyAssetManager = MeshyAssetManager;
