/**
 * Mobile Performance Manager
 * Optimizes performance for mobile devices through dynamic quality adjustment
 */

class MobilePerformanceManager {
    constructor(renderer, scene, camera) {
        this.renderer = renderer;
        this.scene = scene;
        this.camera = camera;

        // Performance metrics
        this.fps = 60;
        this.fpsHistory = [];
        this.maxFpsHistory = 60;
        this.lastFrameTime = performance.now();
        this.frameCount = 0;

        // Quality settings
        this.quality = {
            current: 'auto',
            levels: ['low', 'medium', 'high', 'ultra']
        };

        // Performance targets
        this.targets = {
            minFPS: 30,
            targetFPS: 60,
            lowFPSThreshold: 25,
            criticalFPSThreshold: 15
        };

        // Auto-adjustment
        this.autoAdjust = true;
        this.adjustmentCooldown = 5000; // 5 seconds between adjustments
        this.lastAdjustment = 0;

        // Current settings
        this.settings = {
            pixelRatio: 1,
            shadowQuality: 'medium',
            particleLimit: 500,
            drawDistance: 100,
            lodBias: 1.0,
            antialiasing: true,
            postProcessing: true
        };

        // Device capabilities
        this.deviceInfo = this.detectDeviceCapabilities();

        // Initialize
        this.init();
    }

    /**
     * Detect device capabilities
     */
    detectDeviceCapabilities() {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');

        const info = {
            isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
            isTablet: /(tablet|ipad|playbook|silk)|(android(?!.*mobile))/i.test(navigator.userAgent),
            gpuTier: 'unknown',
            maxTextureSize: gl ? gl.getParameter(gl.MAX_TEXTURE_SIZE) : 2048,
            maxRenderbufferSize: gl ? gl.getParameter(gl.MAX_RENDERBUFFER_SIZE) : 2048,
            devicePixelRatio: window.devicePixelRatio || 1,
            screenWidth: window.screen.width,
            screenHeight: window.screen.height,
            cores: navigator.hardwareConcurrency || 2,
            memory: navigator.deviceMemory || 2
        };

        // Estimate GPU tier
        if (gl) {
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            if (debugInfo) {
                const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                info.gpuRenderer = renderer;

                // Simple tier detection
                if (renderer.includes('Mali') || renderer.includes('Adreno 3') || renderer.includes('PowerVR')) {
                    info.gpuTier = 'low';
                } else if (renderer.includes('Adreno 5') || renderer.includes('Mali-G')) {
                    info.gpuTier = 'medium';
                } else if (renderer.includes('Adreno 6') || renderer.includes('Apple GPU')) {
                    info.gpuTier = 'high';
                } else {
                    info.gpuTier = 'medium'; // Default
                }
            }
        }

        console.log('📱 Device Info:', info);
        return info;
    }

    /**
     * Initialize performance manager
     */
    init() {
        console.log('⚡ Initializing Mobile Performance Manager...');

        // Set initial quality based on device
        this.setInitialQuality();

        // Apply settings
        this.applySettings();

        // Start monitoring
        this.startMonitoring();

        console.log('✅ Performance Manager initialized');
        console.log(`   Quality: ${this.quality.current}`);
        console.log(`   Pixel Ratio: ${this.settings.pixelRatio}`);
        console.log(`   Target FPS: ${this.targets.targetFPS}`);
    }

    /**
     * Set initial quality based on device capabilities
     */
    setInitialQuality() {
        const { gpuTier, memory, isMobile, isTablet } = this.deviceInfo;

        if (gpuTier === 'low' || memory <= 2) {
            this.setQuality('low');
        } else if (gpuTier === 'medium' || memory <= 4 || isMobile) {
            this.setQuality('medium');
        } else if (gpuTier === 'high' || memory >= 6 || isTablet) {
            this.setQuality('high');
        } else {
            this.setQuality('medium'); // Safe default
        }
    }

    /**
     * Set quality level
     */
    setQuality(level) {
        if (!this.quality.levels.includes(level)) {
            console.warn(`Invalid quality level: ${level}`);
            return;
        }

        this.quality.current = level;

        // Update settings based on quality
        switch (level) {
            case 'low':
                this.settings.pixelRatio = 0.75;
                this.settings.shadowQuality = 'off';
                this.settings.particleLimit = 200;
                this.settings.drawDistance = 60;
                this.settings.lodBias = 1.5;
                this.settings.antialiasing = false;
                this.settings.postProcessing = false;
                break;

            case 'medium':
                this.settings.pixelRatio = 1.0;
                this.settings.shadowQuality = 'low';
                this.settings.particleLimit = 500;
                this.settings.drawDistance = 80;
                this.settings.lodBias = 1.0;
                this.settings.antialiasing = false;
                this.settings.postProcessing = false;
                break;

            case 'high':
                this.settings.pixelRatio = 1.5;
                this.settings.shadowQuality = 'medium';
                this.settings.particleLimit = 1000;
                this.settings.drawDistance = 100;
                this.settings.lodBias = 0.8;
                this.settings.antialiasing = true;
                this.settings.postProcessing = true;
                break;

            case 'ultra':
                this.settings.pixelRatio = 2.0;
                this.settings.shadowQuality = 'high';
                this.settings.particleLimit = 2000;
                this.settings.drawDistance = 120;
                this.settings.lodBias = 0.5;
                this.settings.antialiasing = true;
                this.settings.postProcessing = true;
                break;
        }

        console.log(`⚙️ Quality set to: ${level}`);
        this.applySettings();
    }

    /**
     * Apply current settings
     */
    applySettings() {
        // Pixel ratio (resolution)
        this.renderer.setPixelRatio(this.settings.pixelRatio * window.devicePixelRatio);

        // Shadows
        if (this.settings.shadowQuality === 'off') {
            this.renderer.shadowMap.enabled = false;
        } else {
            this.renderer.shadowMap.enabled = true;

            switch (this.settings.shadowQuality) {
                case 'low':
                    this.renderer.shadowMap.type = THREE.BasicShadowMap;
                    break;
                case 'medium':
                    this.renderer.shadowMap.type = THREE.PCFShadowMap;
                    break;
                case 'high':
                    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                    break;
            }
        }

        // Camera far plane (draw distance)
        if (this.camera) {
            this.camera.far = this.settings.drawDistance;
            this.camera.updateProjectionMatrix();
        }

        // Antialiasing
        this.renderer.antialias = this.settings.antialiasing;

        console.log('✅ Settings applied');
    }

    /**
     * Start performance monitoring
     */
    startMonitoring() {
        // Update FPS counter every second
        setInterval(() => {
            this.updateFPSCounter();
        }, 1000);

        // Check for auto-adjustment every 5 seconds
        if (this.autoAdjust) {
            setInterval(() => {
                this.checkAutoAdjustment();
            }, this.adjustmentCooldown);
        }
    }

    /**
     * Update (call every frame)
     */
    update(deltaTime) {
        // Calculate FPS
        this.frameCount++;
        const currentTime = performance.now();
        const elapsed = currentTime - this.lastFrameTime;

        if (elapsed >= 1000) {
            this.fps = Math.round((this.frameCount * 1000) / elapsed);
            this.fpsHistory.push(this.fps);

            // Keep history limited
            if (this.fpsHistory.length > this.maxFpsHistory) {
                this.fpsHistory.shift();
            }

            this.frameCount = 0;
            this.lastFrameTime = currentTime;
        }
    }

    /**
     * Update FPS counter display
     */
    updateFPSCounter() {
        let fpsElement = document.getElementById('fps-counter');

        if (!fpsElement) {
            fpsElement = document.createElement('div');
            fpsElement.id = 'fps-counter';
            document.body.appendChild(fpsElement);
        }

        fpsElement.textContent = `FPS: ${this.fps}`;

        // Color code based on performance
        fpsElement.className = '';
        if (this.fps < this.targets.criticalFPSThreshold) {
            fpsElement.className = 'critical';
        } else if (this.fps < this.targets.lowFPSThreshold) {
            fpsElement.className = 'warning';
        }
    }

    /**
     * Check if quality should be auto-adjusted
     */
    checkAutoAdjustment() {
        if (!this.autoAdjust) return;

        const now = Date.now();
        if (now - this.lastAdjustment < this.adjustmentCooldown) {
            return; // Cooldown active
        }

        // Calculate average FPS from recent history
        if (this.fpsHistory.length < 5) return; // Not enough data

        const recentFPS = this.fpsHistory.slice(-10);
        const avgFPS = recentFPS.reduce((a, b) => a + b, 0) / recentFPS.length;

        const currentIndex = this.quality.levels.indexOf(this.quality.current);

        // Downgrade if performance is poor
        if (avgFPS < this.targets.lowFPSThreshold && currentIndex > 0) {
            const newQuality = this.quality.levels[currentIndex - 1];
            console.log(`⬇️ Auto-lowering quality: ${this.quality.current} -> ${newQuality} (avg FPS: ${avgFPS.toFixed(1)})`);
            this.setQuality(newQuality);
            this.lastAdjustment = now;
        }
        // Upgrade if performance is good
        else if (avgFPS > this.targets.targetFPS && currentIndex < this.quality.levels.length - 1) {
            const newQuality = this.quality.levels[currentIndex + 1];
            console.log(`⬆️ Auto-raising quality: ${this.quality.current} -> ${newQuality} (avg FPS: ${avgFPS.toFixed(1)})`);
            this.setQuality(newQuality);
            this.lastAdjustment = now;
        }
    }

    /**
     * Get current performance metrics
     */
    getMetrics() {
        return {
            fps: this.fps,
            avgFPS: this.fpsHistory.length > 0
                ? this.fpsHistory.reduce((a, b) => a + b, 0) / this.fpsHistory.length
                : 0,
            quality: this.quality.current,
            settings: this.settings,
            deviceInfo: this.deviceInfo
        };
    }

    /**
     * Enable/disable auto quality adjustment
     */
    setAutoAdjust(enabled) {
        this.autoAdjust = enabled;
        console.log(`Auto quality adjustment: ${enabled ? 'enabled' : 'disabled'}`);
    }

    /**
     * Pause performance monitoring (e.g., when game is paused)
     */
    pause() {
        this.lastFrameTime = performance.now();
        this.frameCount = 0;
    }

    /**
     * Resume performance monitoring
     */
    resume() {
        this.lastFrameTime = performance.now();
        this.frameCount = 0;
    }

    /**
     * Reduce particle count if needed
     */
    limitParticles(particles) {
        if (particles.length > this.settings.particleLimit) {
            return particles.slice(0, this.settings.particleLimit);
        }
        return particles;
    }

    /**
     * Get LOD bias for distance-based quality
     */
    getLODBias() {
        return this.settings.lodBias;
    }

    /**
     * Check if feature should be enabled based on quality
     */
    shouldEnableFeature(feature) {
        const qualityIndex = this.quality.levels.indexOf(this.quality.current);

        const featureRequirements = {
            postProcessing: 2, // high or ultra
            shadows: 1, // medium or higher
            antialiasing: 2, // high or ultra
            particles: 0, // all levels (but limited count)
            reflections: 3 // ultra only
        };

        const requiredLevel = featureRequirements[feature];
        return requiredLevel !== undefined && qualityIndex >= requiredLevel;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobilePerformanceManager;
}
