/**
 * Cache Manager
 * Intelligent caching system for API responses and resources
 */

class CacheManager {
    constructor() {
        this.caches = new Map();
        this.config = {
            defaultTTL: 300000, // 5 minutes
            maxSize: 100, // Max entries per cache
            persistToDisk: true
        };

        // Statistics
        this.stats = {
            hits: 0,
            misses: 0,
            sets: 0,
            evictions: 0
        };

        this.init();

        console.log('💾 Cache Manager initialized');
    }

    /**
     * Initialize cache manager
     */
    async init() {
        // Create default caches
        this.createCache('api', { ttl: 300000, maxSize: 100 });
        this.createCache('resources', { ttl: 3600000, maxSize: 200 }); // 1 hour
        this.createCache('user_data', { ttl: 600000, maxSize: 50 });
        this.createCache('static', { ttl: 86400000, maxSize: 500 }); // 24 hours

        // Load persisted caches
        if (this.config.persistToDisk) {
            await this.loadFromStorage();
        }

        // Start cleanup interval
        this.startCleanup();
    }

    /**
     * Create a new cache
     */
    createCache(name, options = {}) {
        const cache = new Cache(name, {
            ttl: options.ttl || this.config.defaultTTL,
            maxSize: options.maxSize || this.config.maxSize
        });

        this.caches.set(name, cache);

        console.log(`📦 Created cache: ${name}`);

        return cache;
    }

    /**
     * Get cache by name
     */
    getCache(name) {
        return this.caches.get(name);
    }

    /**
     * Get value from cache
     */
    get(cacheName, key) {
        const cache = this.caches.get(cacheName);

        if (!cache) {
            this.stats.misses++;
            return null;
        }

        const value = cache.get(key);

        if (value !== null) {
            this.stats.hits++;
        } else {
            this.stats.misses++;
        }

        return value;
    }

    /**
     * Set value in cache
     */
    set(cacheName, key, value, ttl = null) {
        let cache = this.caches.get(cacheName);

        if (!cache) {
            cache = this.createCache(cacheName);
        }

        cache.set(key, value, ttl);
        this.stats.sets++;

        // Persist if enabled
        if (this.config.persistToDisk) {
            this.persistCache(cacheName);
        }
    }

    /**
     * Delete value from cache
     */
    delete(cacheName, key) {
        const cache = this.caches.get(cacheName);

        if (cache) {
            cache.delete(key);
        }
    }

    /**
     * Clear cache
     */
    clear(cacheName) {
        const cache = this.caches.get(cacheName);

        if (cache) {
            cache.clear();
        }
    }

    /**
     * Clear all caches
     */
    clearAll() {
        this.caches.forEach(cache => cache.clear());
        this.stats.evictions = 0;

        console.log('🗑️ All caches cleared');
    }

    /**
     * Start cleanup interval
     */
    startCleanup() {
        setInterval(() => {
            this.caches.forEach(cache => {
                const evicted = cache.cleanup();
                this.stats.evictions += evicted;
            });
        }, 60000); // Cleanup every minute
    }

    /**
     * Persist cache to localStorage
     */
    persistCache(cacheName) {
        const cache = this.caches.get(cacheName);

        if (!cache) return;

        try {
            const data = cache.serialize();
            localStorage.setItem(`cache_${cacheName}`, JSON.stringify(data));
        } catch (error) {
            console.error(`Failed to persist cache ${cacheName}:`, error);
        }
    }

    /**
     * Load caches from localStorage
     */
    async loadFromStorage() {
        const keys = Object.keys(localStorage);

        for (const key of keys) {
            if (key.startsWith('cache_')) {
                const cacheName = key.replace('cache_', '');

                try {
                    const data = JSON.parse(localStorage.getItem(key));

                    let cache = this.caches.get(cacheName);
                    if (!cache) {
                        cache = this.createCache(cacheName);
                    }

                    cache.deserialize(data);

                    console.log(`📥 Loaded cache from storage: ${cacheName}`);

                } catch (error) {
                    console.error(`Failed to load cache ${cacheName}:`, error);
                }
            }
        }
    }

    /**
     * Get cache hit rate
     */
    getHitRate() {
        const total = this.stats.hits + this.stats.misses;
        return total > 0 ? (this.stats.hits / total) * 100 : 0;
    }

    /**
     * Get statistics
     */
    getStats() {
        const cacheStats = {};

        this.caches.forEach((cache, name) => {
            cacheStats[name] = cache.getStats();
        });

        return {
            ...this.stats,
            hitRate: this.getHitRate(),
            caches: cacheStats
        };
    }
}

/**
 * Cache implementation
 */
class Cache {
    constructor(name, options = {}) {
        this.name = name;
        this.ttl = options.ttl || 300000; // 5 minutes default
        this.maxSize = options.maxSize || 100;
        this.entries = new Map();
    }

    /**
     * Get value from cache
     */
    get(key) {
        const entry = this.entries.get(key);

        if (!entry) {
            return null;
        }

        // Check if expired
        if (Date.now() > entry.expiresAt) {
            this.entries.delete(key);
            return null;
        }

        // Update access time
        entry.lastAccess = Date.now();
        entry.hits++;

        return entry.value;
    }

    /**
     * Set value in cache
     */
    set(key, value, ttl = null) {
        // Check size limit
        if (this.entries.size >= this.maxSize && !this.entries.has(key)) {
            this.evictLRU();
        }

        const expiresAt = Date.now() + (ttl || this.ttl);

        this.entries.set(key, {
            value: value,
            expiresAt: expiresAt,
            createdAt: Date.now(),
            lastAccess: Date.now(),
            hits: 0
        });
    }

    /**
     * Delete value from cache
     */
    delete(key) {
        this.entries.delete(key);
    }

    /**
     * Clear cache
     */
    clear() {
        this.entries.clear();
    }

    /**
     * Cleanup expired entries
     */
    cleanup() {
        const now = Date.now();
        let evicted = 0;

        this.entries.forEach((entry, key) => {
            if (now > entry.expiresAt) {
                this.entries.delete(key);
                evicted++;
            }
        });

        return evicted;
    }

    /**
     * Evict least recently used entry
     */
    evictLRU() {
        let lruKey = null;
        let lruTime = Infinity;

        this.entries.forEach((entry, key) => {
            if (entry.lastAccess < lruTime) {
                lruTime = entry.lastAccess;
                lruKey = key;
            }
        });

        if (lruKey) {
            this.entries.delete(lruKey);
        }
    }

    /**
     * Serialize cache
     */
    serialize() {
        const entries = [];

        this.entries.forEach((entry, key) => {
            entries.push({
                key: key,
                ...entry
            });
        });

        return {
            name: this.name,
            ttl: this.ttl,
            maxSize: this.maxSize,
            entries: entries
        };
    }

    /**
     * Deserialize cache
     */
    deserialize(data) {
        this.ttl = data.ttl;
        this.maxSize = data.maxSize;

        data.entries.forEach(entry => {
            // Only restore if not expired
            if (Date.now() < entry.expiresAt) {
                this.entries.set(entry.key, {
                    value: entry.value,
                    expiresAt: entry.expiresAt,
                    createdAt: entry.createdAt,
                    lastAccess: entry.lastAccess,
                    hits: entry.hits
                });
            }
        });
    }

    /**
     * Get statistics
     */
    getStats() {
        let totalHits = 0;
        let oldestEntry = Date.now();
        let newestEntry = 0;

        this.entries.forEach(entry => {
            totalHits += entry.hits;
            if (entry.createdAt < oldestEntry) oldestEntry = entry.createdAt;
            if (entry.createdAt > newestEntry) newestEntry = entry.createdAt;
        });

        return {
            size: this.entries.size,
            maxSize: this.maxSize,
            utilization: (this.entries.size / this.maxSize) * 100,
            totalHits: totalHits,
            avgHits: this.entries.size > 0 ? totalHits / this.entries.size : 0,
            oldestEntry: oldestEntry,
            newestEntry: newestEntry
        };
    }
}

/**
 * API Response Cache Wrapper
 */
class APICacheWrapper {
    constructor(cacheManager) {
        this.cacheManager = cacheManager;
    }

    /**
     * Cached fetch
     */
    async fetch(url, options = {}) {
        const cacheKey = this.getCacheKey(url, options);
        const cacheName = 'api';

        // Try to get from cache
        const cached = this.cacheManager.get(cacheName, cacheKey);

        if (cached && !options.noCache) {
            console.log(`💾 Cache hit: ${url}`);
            return cached;
        }

        // Fetch from network
        console.log(`🌐 Cache miss: ${url}`);

        const response = await fetch(url, options);
        const data = await response.json();

        // Cache response
        if (response.ok && !options.noCache) {
            this.cacheManager.set(cacheName, cacheKey, data, options.cacheTTL);
        }

        return data;
    }

    /**
     * Get cache key
     */
    getCacheKey(url, options) {
        const method = options.method || 'GET';
        const body = options.body ? JSON.stringify(options.body) : '';

        return `${method}:${url}:${body}`;
    }

    /**
     * Invalidate cache
     */
    invalidate(url) {
        const cacheKey = this.getCacheKey(url, {});
        this.cacheManager.delete('api', cacheKey);
    }
}

// Global cache manager
const cacheManager = new CacheManager();
const apiCache = new APICacheWrapper(cacheManager);

// Make globally available
window.cacheManager = cacheManager;
window.apiCache = apiCache;
