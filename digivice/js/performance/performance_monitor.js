/**
 * Performance Monitor
 * Track FPS, memory usage, and performance metrics
 */

class PerformanceMonitor {
    constructor() {
        this.enabled = true;
        this.visible = false;

        // FPS tracking
        this.fps = 0;
        this.frameCount = 0;
        this.lastFrameTime = performance.now();
        this.lastFPSUpdate = performance.now();
        this.frameTimes = [];
        this.maxFrameTimes = 60;

        // Memory tracking
        this.memoryInfo = null;
        this.memoryHistory = [];
        this.maxMemoryHistory = 100;

        // Performance marks
        this.marks = new Map();
        this.measures = [];

        // Thresholds
        this.thresholds = {
            minFPS: 30,
            maxMemory: 500 * 1024 * 1024, // 500 MB
            maxFrameTime: 33 // 33ms = 30 FPS
        };

        // Warnings
        this.warnings = [];
        this.maxWarnings = 50;

        // Stats container
        this.statsContainer = null;

        this.init();

        console.log('📊 Performance Monitor initialized');
    }

    /**
     * Initialize performance monitor
     */
    init() {
        // Start FPS tracking
        this.startFPSTracking();

        // Start memory tracking
        this.startMemoryTracking();

        // Create stats UI
        this.createStatsUI();
    }

    /**
     * Start FPS tracking
     */
    startFPSTracking() {
        const trackFrame = (timestamp) => {
            if (!this.enabled) {
                requestAnimationFrame(trackFrame);
                return;
            }

            // Calculate frame time
            const frameTime = timestamp - this.lastFrameTime;
            this.lastFrameTime = timestamp;

            // Store frame time
            this.frameTimes.push(frameTime);
            if (this.frameTimes.length > this.maxFrameTimes) {
                this.frameTimes.shift();
            }

            this.frameCount++;

            // Update FPS every second
            const elapsed = timestamp - this.lastFPSUpdate;
            if (elapsed >= 1000) {
                this.fps = Math.round((this.frameCount * 1000) / elapsed);
                this.frameCount = 0;
                this.lastFPSUpdate = timestamp;

                // Check FPS threshold
                if (this.fps < this.thresholds.minFPS) {
                    this.addWarning(`Low FPS: ${this.fps}`);
                }
            }

            // Check frame time
            if (frameTime > this.thresholds.maxFrameTime) {
                this.addWarning(`Long frame: ${frameTime.toFixed(2)}ms`);
            }

            requestAnimationFrame(trackFrame);
        };

        requestAnimationFrame(trackFrame);
    }

    /**
     * Start memory tracking
     */
    startMemoryTracking() {
        setInterval(() => {
            if (!this.enabled) return;

            if (performance.memory) {
                this.memoryInfo = {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize,
                    jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
                    timestamp: Date.now()
                };

                this.memoryHistory.push(this.memoryInfo);
                if (this.memoryHistory.length > this.maxMemoryHistory) {
                    this.memoryHistory.shift();
                }

                // Check memory threshold
                if (this.memoryInfo.usedJSHeapSize > this.thresholds.maxMemory) {
                    this.addWarning(
                        `High memory usage: ${(this.memoryInfo.usedJSHeapSize / (1024 * 1024)).toFixed(2)} MB`
                    );
                }
            }
        }, 1000);
    }

    /**
     * Create stats UI
     */
    createStatsUI() {
        this.statsContainer = document.createElement('div');
        this.statsContainer.id = 'performance-stats';
        this.statsContainer.className = 'performance-stats';
        this.statsContainer.style.display = 'none';

        this.statsContainer.innerHTML = `
            <div class="perf-stats-header">
                <span>Performance Stats</span>
                <button class="perf-close-btn">×</button>
            </div>
            <div class="perf-stats-body">
                <div class="perf-stat">
                    <span class="perf-stat-label">FPS:</span>
                    <span class="perf-stat-value" id="perf-fps">0</span>
                </div>
                <div class="perf-stat">
                    <span class="perf-stat-label">Frame Time:</span>
                    <span class="perf-stat-value" id="perf-frame-time">0ms</span>
                </div>
                <div class="perf-stat">
                    <span class="perf-stat-label">Memory:</span>
                    <span class="perf-stat-value" id="perf-memory">0 MB</span>
                </div>
                <div class="perf-stat">
                    <span class="perf-stat-label">DOM Nodes:</span>
                    <span class="perf-stat-value" id="perf-dom-nodes">0</span>
                </div>
                <div class="perf-warnings" id="perf-warnings">
                    <!-- Warnings will be inserted here -->
                </div>
            </div>
        `;

        document.body.appendChild(this.statsContainer);

        // Close button
        this.statsContainer.querySelector('.perf-close-btn').addEventListener('click', () => {
            this.hide();
        });

        // Update stats UI
        this.startStatsUI();
    }

    /**
     * Start stats UI updates
     */
    startStatsUI() {
        setInterval(() => {
            if (!this.visible) return;

            // Update FPS
            document.getElementById('perf-fps').textContent = this.fps;

            // Update frame time
            const avgFrameTime = this.getAverageFrameTime();
            document.getElementById('perf-frame-time').textContent = `${avgFrameTime.toFixed(2)}ms`;

            // Update memory
            if (this.memoryInfo) {
                const memoryMB = (this.memoryInfo.usedJSHeapSize / (1024 * 1024)).toFixed(2);
                document.getElementById('perf-memory').textContent = `${memoryMB} MB`;
            }

            // Update DOM nodes
            const domNodes = document.getElementsByTagName('*').length;
            document.getElementById('perf-dom-nodes').textContent = domNodes;

            // Update warnings
            this.updateWarningsUI();

        }, 100);
    }

    /**
     * Update warnings UI
     */
    updateWarningsUI() {
        const warningsContainer = document.getElementById('perf-warnings');
        if (!warningsContainer) return;

        const recentWarnings = this.warnings.slice(-10);

        warningsContainer.innerHTML = recentWarnings.map(warning => `
            <div class="perf-warning">
                <span class="perf-warning-time">${new Date(warning.timestamp).toLocaleTimeString()}</span>
                <span class="perf-warning-msg">${warning.message}</span>
            </div>
        `).join('');
    }

    /**
     * Show stats UI
     */
    show() {
        this.visible = true;
        this.statsContainer.style.display = 'block';
    }

    /**
     * Hide stats UI
     */
    hide() {
        this.visible = false;
        this.statsContainer.style.display = 'none';
    }

    /**
     * Toggle stats UI
     */
    toggle() {
        if (this.visible) {
            this.hide();
        } else {
            this.show();
        }
    }

    /**
     * Add warning
     */
    addWarning(message) {
        this.warnings.push({
            message: message,
            timestamp: Date.now()
        });

        if (this.warnings.length > this.maxWarnings) {
            this.warnings.shift();
        }

        console.warn(`⚠️ Performance: ${message}`);
    }

    /**
     * Mark performance point
     */
    mark(name) {
        performance.mark(name);
        this.marks.set(name, performance.now());
    }

    /**
     * Measure performance between two marks
     */
    measure(name, startMark, endMark) {
        try {
            performance.measure(name, startMark, endMark);

            const measure = performance.getEntriesByName(name)[0];

            this.measures.push({
                name: name,
                duration: measure.duration,
                timestamp: Date.now()
            });

            console.log(`📊 ${name}: ${measure.duration.toFixed(2)}ms`);

            return measure.duration;

        } catch (error) {
            console.error('Failed to measure performance:', error);
            return null;
        }
    }

    /**
     * Get average frame time
     */
    getAverageFrameTime() {
        if (this.frameTimes.length === 0) return 0;

        const sum = this.frameTimes.reduce((a, b) => a + b, 0);
        return sum / this.frameTimes.length;
    }

    /**
     * Get min/max frame times
     */
    getFrameTimeRange() {
        if (this.frameTimes.length === 0) {
            return { min: 0, max: 0 };
        }

        return {
            min: Math.min(...this.frameTimes),
            max: Math.max(...this.frameTimes)
        };
    }

    /**
     * Get current stats
     */
    getStats() {
        const frameTimeRange = this.getFrameTimeRange();

        return {
            fps: this.fps,
            avgFrameTime: this.getAverageFrameTime(),
            minFrameTime: frameTimeRange.min,
            maxFrameTime: frameTimeRange.max,
            memory: this.memoryInfo,
            domNodes: document.getElementsByTagName('*').length,
            warnings: this.warnings.length,
            measures: this.measures.length
        };
    }

    /**
     * Get detailed report
     */
    getReport() {
        const stats = this.getStats();

        return {
            ...stats,
            memoryHistory: this.memoryHistory,
            recentWarnings: this.warnings.slice(-20),
            recentMeasures: this.measures.slice(-20),
            thresholds: this.thresholds
        };
    }

    /**
     * Export stats to JSON
     */
    exportStats() {
        const report = this.getReport();
        const json = JSON.stringify(report, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `performance-stats-${Date.now()}.json`;
        a.click();

        URL.revokeObjectURL(url);
    }

    /**
     * Clear all data
     */
    clear() {
        this.frameTimes = [];
        this.memoryHistory = [];
        this.warnings = [];
        this.measures = [];
        this.marks.clear();

        performance.clearMarks();
        performance.clearMeasures();

        console.log('🗑️ Performance data cleared');
    }

    /**
     * Enable/disable monitoring
     */
    setEnabled(enabled) {
        this.enabled = enabled;
        console.log(`📊 Performance monitoring ${enabled ? 'enabled' : 'disabled'}`);
    }
}

/**
 * Object Pool for performance
 */
class ObjectPool {
    constructor(factory, initialSize = 10, maxSize = 100) {
        this.factory = factory;
        this.maxSize = maxSize;
        this.pool = [];
        this.activeObjects = new Set();

        // Pre-populate pool
        for (let i = 0; i < initialSize; i++) {
            this.pool.push(this.factory());
        }

        console.log(`🎱 Object Pool initialized (size: ${initialSize})`);
    }

    /**
     * Acquire object from pool
     */
    acquire() {
        let obj;

        if (this.pool.length > 0) {
            obj = this.pool.pop();
        } else if (this.activeObjects.size < this.maxSize) {
            obj = this.factory();
        } else {
            console.warn('Object pool exhausted');
            return null;
        }

        this.activeObjects.add(obj);
        return obj;
    }

    /**
     * Release object back to pool
     */
    release(obj) {
        if (!this.activeObjects.has(obj)) {
            console.warn('Releasing object not from pool');
            return;
        }

        this.activeObjects.delete(obj);

        if (this.pool.length < this.maxSize) {
            // Reset object if it has a reset method
            if (typeof obj.reset === 'function') {
                obj.reset();
            }

            this.pool.push(obj);
        }
    }

    /**
     * Get pool stats
     */
    getStats() {
        return {
            poolSize: this.pool.length,
            activeObjects: this.activeObjects.size,
            maxSize: this.maxSize,
            utilization: (this.activeObjects.size / this.maxSize) * 100
        };
    }

    /**
     * Clear pool
     */
    clear() {
        this.pool = [];
        this.activeObjects.clear();
    }
}

// Global performance monitor
const performanceMonitor = new PerformanceMonitor();

// Make globally available
window.performanceMonitor = performanceMonitor;
window.ObjectPool = ObjectPool;

// Keyboard shortcut to toggle stats (Ctrl+Shift+P)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        performanceMonitor.toggle();
    }
});
