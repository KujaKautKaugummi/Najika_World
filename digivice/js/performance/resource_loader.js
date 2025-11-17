/**
 * Resource Loader
 * Lazy loading and resource management for optimal performance
 */

export class ResourceLoader {
    constructor() {
        this.loadedModules = new Map();
        this.loadingPromises = new Map();
        this.resourceCache = new Map();
        this.preloadQueue = [];
        this.isPreloading = false;

        // Configuration
        this.config = {
            maxConcurrentLoads: 6,
            cacheEnabled: true,
            preloadEnabled: true,
            retryAttempts: 3,
            retryDelay: 1000
        };

        // Statistics
        this.stats = {
            totalLoads: 0,
            cacheHits: 0,
            loadErrors: 0,
            totalLoadTime: 0
        };

        console.log('📦 Resource Loader initialized');
    }

    /**
     * Lazy load a module
     */
    async loadModule(moduleName, modulePath) {
        const startTime = performance.now();

        // Check if already loaded
        if (this.loadedModules.has(moduleName)) {
            this.stats.cacheHits++;
            return this.loadedModules.get(moduleName);
        }

        // Check if currently loading
        if (this.loadingPromises.has(moduleName)) {
            return this.loadingPromises.get(moduleName);
        }

        // Create loading promise
        const loadPromise = this._loadModuleWithRetry(moduleName, modulePath);

        this.loadingPromises.set(moduleName, loadPromise);

        try {
            const module = await loadPromise;

            this.loadedModules.set(moduleName, module);
            this.stats.totalLoads++;
            this.stats.totalLoadTime += performance.now() - startTime;

            console.log(`✅ Module loaded: ${moduleName} (${(performance.now() - startTime).toFixed(2)}ms)`);

            return module;

        } catch (error) {
            this.stats.loadErrors++;
            console.error(`❌ Failed to load module: ${moduleName}`, error);
            throw error;

        } finally {
            this.loadingPromises.delete(moduleName);
        }
    }

    /**
     * Load module with retry logic
     */
    async _loadModuleWithRetry(moduleName, modulePath, attempt = 1) {
        try {
            const module = await import(modulePath);
            return module;

        } catch (error) {
            if (attempt < this.config.retryAttempts) {
                console.warn(`Retry ${attempt}/${this.config.retryAttempts} for ${moduleName}`);

                await new Promise(resolve =>
                    setTimeout(resolve, this.config.retryDelay * attempt)
                );

                return this._loadModuleWithRetry(moduleName, modulePath, attempt + 1);
            }

            throw error;
        }
    }

    /**
     * Preload modules in the background
     */
    async preloadModules(modules) {
        if (!this.config.preloadEnabled) {
            return;
        }

        this.preloadQueue.push(...modules);

        if (!this.isPreloading) {
            this.processPreloadQueue();
        }
    }

    /**
     * Process preload queue
     */
    async processPreloadQueue() {
        if (this.preloadQueue.length === 0) {
            this.isPreloading = false;
            return;
        }

        this.isPreloading = true;

        // Load modules in batches
        while (this.preloadQueue.length > 0) {
            const batch = this.preloadQueue.splice(0, this.config.maxConcurrentLoads);

            await Promise.allSettled(
                batch.map(({ name, path }) => this.loadModule(name, path))
            );

            // Yield to main thread
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        this.isPreloading = false;
    }

    /**
     * Load and cache resource (image, audio, etc.)
     */
    async loadResource(url, type = 'auto') {
        // Check cache
        if (this.config.cacheEnabled && this.resourceCache.has(url)) {
            this.stats.cacheHits++;
            return this.resourceCache.get(url);
        }

        // Determine type if auto
        if (type === 'auto') {
            type = this._detectResourceType(url);
        }

        // Load resource
        let resource;

        switch (type) {
            case 'image':
                resource = await this.loadImage(url);
                break;
            case 'audio':
                resource = await this.loadAudio(url);
                break;
            case 'json':
                resource = await this.loadJSON(url);
                break;
            case 'text':
                resource = await this.loadText(url);
                break;
            default:
                throw new Error(`Unknown resource type: ${type}`);
        }

        // Cache resource
        if (this.config.cacheEnabled) {
            this.resourceCache.set(url, resource);
        }

        this.stats.totalLoads++;

        return resource;
    }

    /**
     * Load image
     */
    async loadImage(url) {
        return new Promise((resolve, reject) => {
            const img = new Image();

            img.onload = () => resolve(img);
            img.onerror = () => reject(new Error(`Failed to load image: ${url}`));

            img.src = url;
        });
    }

    /**
     * Load audio
     */
    async loadAudio(url) {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Failed to load audio: ${url}`);
        }

        return await response.arrayBuffer();
    }

    /**
     * Load JSON
     */
    async loadJSON(url) {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Failed to load JSON: ${url}`);
        }

        return await response.json();
    }

    /**
     * Load text
     */
    async loadText(url) {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Failed to load text: ${url}`);
        }

        return await response.text();
    }

    /**
     * Detect resource type from URL
     */
    _detectResourceType(url) {
        const ext = url.split('.').pop().toLowerCase();

        const typeMap = {
            'png': 'image',
            'jpg': 'image',
            'jpeg': 'image',
            'gif': 'image',
            'webp': 'image',
            'svg': 'image',
            'mp3': 'audio',
            'wav': 'audio',
            'ogg': 'audio',
            'json': 'json',
            'txt': 'text',
            'md': 'text'
        };

        return typeMap[ext] || 'text';
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.resourceCache.clear();
        console.log('🗑️ Resource cache cleared');
    }

    /**
     * Get cache size estimate
     */
    getCacheSize() {
        let totalSize = 0;

        this.resourceCache.forEach((value, key) => {
            if (value instanceof ArrayBuffer) {
                totalSize += value.byteLength;
            } else if (value instanceof Image) {
                // Estimate image size
                totalSize += value.width * value.height * 4; // RGBA
            } else if (typeof value === 'string') {
                totalSize += value.length * 2; // UTF-16
            }
        });

        return totalSize;
    }

    /**
     * Get statistics
     */
    getStats() {
        return {
            ...this.stats,
            loadedModules: this.loadedModules.size,
            cachedResources: this.resourceCache.size,
            cacheSize: this.getCacheSize(),
            avgLoadTime: this.stats.totalLoads > 0
                ? this.stats.totalLoadTime / this.stats.totalLoads
                : 0,
            cacheHitRate: this.stats.totalLoads > 0
                ? (this.stats.cacheHits / this.stats.totalLoads) * 100
                : 0
        };
    }
}

/**
 * Code Splitting Helper
 */
export class CodeSplitter {
    constructor(resourceLoader) {
        this.resourceLoader = resourceLoader;
        this.chunks = new Map();

        console.log('✂️ Code Splitter initialized');
    }

    /**
     * Define code chunk
     */
    defineChunk(chunkName, modulePaths) {
        this.chunks.set(chunkName, {
            name: chunkName,
            modules: modulePaths,
            loaded: false
        });
    }

    /**
     * Load code chunk
     */
    async loadChunk(chunkName) {
        const chunk = this.chunks.get(chunkName);

        if (!chunk) {
            throw new Error(`Chunk not defined: ${chunkName}`);
        }

        if (chunk.loaded) {
            return;
        }

        console.log(`📦 Loading chunk: ${chunkName}`);

        const startTime = performance.now();

        // Load all modules in chunk
        const promises = chunk.modules.map(({ name, path }) =>
            this.resourceLoader.loadModule(name, path)
        );

        await Promise.all(promises);

        chunk.loaded = true;

        console.log(`✅ Chunk loaded: ${chunkName} (${(performance.now() - startTime).toFixed(2)}ms)`);
    }

    /**
     * Define standard chunks
     */
    defineStandardChunks() {
        // Core chunk (always loaded)
        this.defineChunk('core', [
            { name: 'config', path: './config.js' },
            { name: 'api', path: './api_client.js' },
            { name: 'auth', path: './auth.js' }
        ]);

        // Digimon chunk
        this.defineChunk('digimon', [
            { name: 'digimon_viewer', path: './digimon_viewer.js' },
            { name: 'digimon_stats', path: './digimon_stats.js' },
            { name: 'evolution_system', path: './evolution_system.js' }
        ]);

        // Battle chunk
        this.defineChunk('battle', [
            { name: 'battle_system', path: './battle_system.js' },
            { name: 'battle_ui', path: './battle_ui.js' }
        ]);

        // Arena chunk
        this.defineChunk('arena', [
            { name: 'nemesis_arena_ui', path: './nemesis_arena_ui.js' },
            { name: 'finisher_category_selector', path: './finisher_category_selector.js' }
        ]);

        // Particles chunk
        this.defineChunk('particles', [
            { name: 'combat_particles', path: './particles/combat_particles.js' },
            { name: 'magic_particles', path: './particles/magic_particles.js' },
            { name: 'environment_particles', path: './particles/environment_particles.js' },
            { name: 'evolution_effects', path: './particles/evolution_effects.js' }
        ]);

        // Audio chunk
        this.defineChunk('audio', [
            { name: 'spatial_audio', path: './audio/spatial_audio_engine.js' },
            { name: 'music_system', path: './audio/music_system.js' },
            { name: 'combat_sfx', path: './audio/combat_sfx_system.js' }
        ]);

        // Admin chunk
        this.defineChunk('admin', [
            { name: 'admin_dashboard', path: './admin_dashboard.js' }
        ]);
    }
}

// Global resource loader instance
export const resourceLoader = new ResourceLoader();
export const codeSplitter = new CodeSplitter(resourceLoader);

// Define standard chunks
codeSplitter.defineStandardChunks();

// Make globally available
window.resourceLoader = resourceLoader;
window.codeSplitter = codeSplitter;
