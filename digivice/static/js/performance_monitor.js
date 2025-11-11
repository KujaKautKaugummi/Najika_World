/**
 * NAJIKA WORLD - PERFORMANCE MONITOR
 * ====================================
 *
 * Performance-Optimierung + Monitoring:
 * - FPS-Counter
 * - Performance-Stats
 * - Memory-Tracking
 */

class PerformanceMonitor {
    constructor() {
        this.fps = 0;
        this.frameCount = 0;
        this.lastTime = performance.now();
        this.updateInterval = 1000; // Update every second

        // Performance stats
        this.stats = {
            fps: 0,
            ms: 0, // Frame time in ms
            memory: 0, // MB (if available)
            drawCalls: 0,
            triangles: 0,
            objects: 0
        };

        // Create UI
        this.createUI();

        console.log('📊 Performance Monitor initialisiert');
    }

    createUI() {
        const container = document.createElement('div');
        container.id = 'performance-monitor';
        container.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.85);
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #4CAF50;
            color: white;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            z-index: 9999;
            min-width: 200px;
            display: none;
        `;

        container.innerHTML = `
            <div style="font-weight: bold; color: #4CAF50; margin-bottom: 8px;">📊 PERFORMANCE</div>
            <div id="perf-fps" style="margin: 3px 0;">FPS: <span style="color: #00ff00;">--</span></div>
            <div id="perf-ms" style="margin: 3px 0;">MS: <span style="color: #ffaa00;">--</span></div>
            <div id="perf-memory" style="margin: 3px 0;">Memory: <span style="color: #00aaff;">--</span></div>
            <div id="perf-objects" style="margin: 3px 0;">Objects: <span style="color: #ff00ff;">--</span></div>
            <div style="margin-top: 8px; font-size: 10px; color: #aaa;">
                Drücke F3 zum Toggle
            </div>
        `;

        document.body.appendChild(container);
        this.container = container;

        // F3 to toggle
        window.addEventListener('keydown', (e) => {
            if (e.key === 'F3') {
                e.preventDefault();
                this.toggle();
            }
        });
    }

    toggle() {
        const visible = this.container.style.display !== 'none';
        this.container.style.display = visible ? 'none' : 'block';
    }

    update(renderer) {
        this.frameCount++;
        const currentTime = performance.now();
        const elapsed = currentTime - this.lastTime;

        // Update stats every second
        if (elapsed >= this.updateInterval) {
            // Calculate FPS
            this.stats.fps = Math.round((this.frameCount * 1000) / elapsed);

            // Calculate frame time
            this.stats.ms = Math.round(elapsed / this.frameCount * 100) / 100;

            // Memory (if available)
            if (performance.memory) {
                this.stats.memory = Math.round(performance.memory.usedJSHeapSize / 1048576); // MB
            }

            // Renderer info
            if (renderer) {
                const info = renderer.info;
                this.stats.drawCalls = info.render.calls;
                this.stats.triangles = info.render.triangles;
                this.stats.objects = info.memory.geometries + info.memory.textures;
            }

            // Update UI
            this.updateUI();

            // Reset counters
            this.frameCount = 0;
            this.lastTime = currentTime;
        }
    }

    updateUI() {
        // FPS color (green > 50, yellow > 30, red < 30)
        let fpsColor = '#ff0000';
        if (this.stats.fps > 50) fpsColor = '#00ff00';
        else if (this.stats.fps > 30) fpsColor = '#ffaa00';

        document.getElementById('perf-fps').innerHTML = `FPS: <span style="color: ${fpsColor};">${this.stats.fps}</span>`;
        document.getElementById('perf-ms').innerHTML = `MS: <span style="color: #ffaa00;">${this.stats.ms}</span>`;
        document.getElementById('perf-memory').innerHTML = `Memory: <span style="color: #00aaff;">${this.stats.memory} MB</span>`;
        document.getElementById('perf-objects').innerHTML = `Objects: <span style="color: #ff00ff;">${this.stats.objects}</span>`;
    }

    getStats() {
        return this.stats;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceMonitor;
}
