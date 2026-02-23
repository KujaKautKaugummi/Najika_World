// ☀️🌙 DAY/NIGHT CYCLE - Dynamic time progression and lighting
// Simulates 24-hour cycle with realistic lighting transitions

// THREE is loaded globally

class DayNightCycle {
  constructor(scene, camera, renderer) {
    this.scene = scene;
    this.camera = camera;
    this.renderer = renderer;

    // Time settings
    this.timeOfDay = 12.0;  // 0-24 hours (start at noon)
    this.timeSpeed = 1.0;   // Real-time multiplier (1.0 = real-time, 60.0 = 1 min = 1 hour)
    this.isPaused = false;

    // Lighting
    this.sunLight = null;
    this.moonLight = null;
    this.ambientLight = null;
    this.hemisphereLight = null;

    // Sun/Moon objects
    this.sun = null;
    this.moon = null;

    // Sky colors for different times
    this.skyColors = {
      night: new THREE.Color(0x000814),      // Deep blue-black
      dawn: new THREE.Color(0xff6b35),       // Orange-red
      day: new THREE.Color(0x87ceeb),        // Sky blue
      dusk: new THREE.Color(0xff8c42),       // Orange
      midnight: new THREE.Color(0x0a1128)    // Dark blue
    };

    // Callbacks
    this.onTimeChange = null;  // Callback for time changes

    console.log('☀️🌙 Day/Night Cycle initialized');
  }

  /**
   * Initialize lighting system
   */
  initialize() {
    console.log('☀️ Creating lighting system...');

    this.createSunLight();
    this.createMoonLight();
    this.createAmbientLighting();
    this.createCelestialBodies();

    // Set initial time
    this.updateLighting();

    console.log('☀️🌙 Lighting system ready');
  }

  /**
   * Create directional sun light
   */
  createSunLight() {
    this.sunLight = new THREE.DirectionalLight(0xffffee, 1.0);
    this.sunLight.position.set(0, 100, 0);
    this.sunLight.castShadow = true;

    // Shadow settings
    this.sunLight.shadow.mapSize.width = 2048;
    this.sunLight.shadow.mapSize.height = 2048;
    this.sunLight.shadow.camera.near = 1;
    this.sunLight.shadow.camera.far = 1000;
    this.sunLight.shadow.camera.left = -500;
    this.sunLight.shadow.camera.right = 500;
    this.sunLight.shadow.camera.top = 500;
    this.sunLight.shadow.camera.bottom = -500;
    this.sunLight.shadow.bias = -0.0001;

    this.scene.add(this.sunLight);
    this.scene.add(this.sunLight.target);

    console.log('  ✅ Sun light created');
  }

  /**
   * Create directional moon light
   */
  createMoonLight() {
    this.moonLight = new THREE.DirectionalLight(0xadd8e6, 0.3);  // Light blue
    this.moonLight.position.set(0, 100, 0);
    this.moonLight.castShadow = true;

    // Shadow settings (less detailed than sun)
    this.moonLight.shadow.mapSize.width = 1024;
    this.moonLight.shadow.mapSize.height = 1024;
    this.moonLight.shadow.camera.near = 1;
    this.moonLight.shadow.camera.far = 1000;
    this.moonLight.shadow.camera.left = -500;
    this.moonLight.shadow.camera.right = 500;
    this.moonLight.shadow.camera.top = 500;
    this.moonLight.shadow.camera.bottom = -500;

    this.moonLight.visible = false;  // Start hidden
    this.scene.add(this.moonLight);
    this.scene.add(this.moonLight.target);

    console.log('  ✅ Moon light created');
  }

  /**
   * Create ambient and hemisphere lighting
   */
  createAmbientLighting() {
    // Ambient light (base illumination)
    this.ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    this.scene.add(this.ambientLight);

    // Hemisphere light (sky/ground color)
    this.hemisphereLight = new THREE.HemisphereLight(
      0x87ceeb,  // Sky color
      0x8b7355,  // Ground color
      0.6
    );
    this.scene.add(this.hemisphereLight);

    console.log('  ✅ Ambient lighting created');
  }

  /**
   * Create visual sun and moon
   */
  createCelestialBodies() {
    // Sun
    const sunGeometry = new THREE.SphereGeometry(50, 32, 32);
    const sunMaterial = new THREE.MeshBasicMaterial({
      color: 0xffff00,
      emissive: 0xffff00,
      emissiveIntensity: 1.0
    });
    this.sun = new THREE.Mesh(sunGeometry, sunMaterial);
    this.scene.add(this.sun);

    // Moon
    const moonGeometry = new THREE.SphereGeometry(30, 32, 32);
    const moonMaterial = new THREE.MeshBasicMaterial({
      color: 0xcccccc,
      emissive: 0xaaaaaa,
      emissiveIntensity: 0.3
    });
    this.moon = new THREE.Mesh(moonGeometry, moonMaterial);
    this.moon.visible = false;
    this.scene.add(this.moon);

    console.log('  ✅ Sun and moon created');
  }

  /**
   * Update cycle (call every frame)
   * @param {number} deltaTime - Time since last frame (seconds)
   */
  update(deltaTime) {
    if (this.isPaused) return;

    // Advance time
    const hoursPerSecond = this.timeSpeed / 3600;
    this.timeOfDay += hoursPerSecond * deltaTime;

    // Wrap around 24 hours
    if (this.timeOfDay >= 24) {
      this.timeOfDay -= 24;
      console.log('🌅 New day started');
    }

    // Update lighting and sky
    this.updateLighting();

    // Trigger callback
    if (this.onTimeChange) {
      this.onTimeChange(this.timeOfDay);
    }
  }

  /**
   * Update lighting based on time of day
   */
  updateLighting() {
    const hour = this.timeOfDay;

    // Calculate sun/moon positions (circular path)
    const angle = (hour / 24) * Math.PI * 2 - Math.PI / 2;  // Start at sunrise
    const radius = 800;
    const sunX = Math.cos(angle) * radius;
    const sunY = Math.sin(angle) * radius;

    // Sun position and visibility
    this.sunLight.position.set(sunX, Math.max(sunY, 10), 0);
    this.sun.position.copy(this.sunLight.position);

    // Moon is opposite to sun
    this.moonLight.position.set(-sunX, Math.max(-sunY, 10), 0);
    this.moon.position.copy(this.moonLight.position);

    // Determine time period
    let period = this.getTimePeriod(hour);

    // Update lighting intensities
    this.updateLightIntensities(hour, period);

    // Update sky color
    this.updateSkyColor(hour, period);

    // Update ambient lighting
    this.updateAmbientLighting(hour, period);

    // Show/hide sun and moon
    this.sun.visible = (hour >= 6 && hour <= 18);
    this.moon.visible = (hour < 6 || hour > 18);
    this.sunLight.visible = this.sun.visible;
    this.moonLight.visible = this.moon.visible;
  }

  /**
   * Get current time period
   * @param {number} hour - Current hour (0-24)
   * @returns {string} - "night", "dawn", "day", "dusk"
   */
  getTimePeriod(hour) {
    if (hour >= 6 && hour < 7) return 'dawn';
    if (hour >= 7 && hour < 18) return 'day';
    if (hour >= 18 && hour < 19) return 'dusk';
    return 'night';
  }

  /**
   * Update light intensities based on time
   */
  updateLightIntensities(hour, period) {
    switch (period) {
      case 'dawn':
        // Sunrise: sun intensity grows
        const dawnProgress = (hour - 6) / 1;  // 0-1 over 1 hour
        this.sunLight.intensity = 0.3 + dawnProgress * 0.7;
        this.moonLight.intensity = 0.3 - dawnProgress * 0.3;
        break;

      case 'day':
        // Full daylight
        this.sunLight.intensity = 1.0;
        this.moonLight.intensity = 0.0;
        break;

      case 'dusk':
        // Sunset: sun intensity decreases
        const duskProgress = (hour - 18) / 1;  // 0-1 over 1 hour
        this.sunLight.intensity = 1.0 - duskProgress * 0.7;
        this.moonLight.intensity = duskProgress * 0.3;
        break;

      case 'night':
        // Nighttime: moon only
        this.sunLight.intensity = 0.0;
        this.moonLight.intensity = 0.3;
        break;
    }
  }

  /**
   * Update sky background color
   */
  updateSkyColor(hour, period) {
    let skyColor;

    switch (period) {
      case 'dawn':
        // Blend from night to day through dawn
        const dawnProgress = (hour - 6) / 1;
        skyColor = this.skyColors.night.clone().lerp(this.skyColors.dawn, dawnProgress);
        break;

      case 'day':
        // Bright blue sky
        skyColor = this.skyColors.day;
        break;

      case 'dusk':
        // Blend from day to night through dusk
        const duskProgress = (hour - 18) / 1;
        skyColor = this.skyColors.day.clone().lerp(this.skyColors.dusk, duskProgress);
        break;

      case 'night':
        // Dark night sky
        skyColor = this.skyColors.night;
        break;
    }

    this.scene.background = skyColor;

    // Update fog color to match sky
    if (this.scene.fog) {
      this.scene.fog.color = skyColor;
    }
  }

  /**
   * Update ambient lighting
   */
  updateAmbientLighting(hour, period) {
    switch (period) {
      case 'dawn':
        const dawnProgress = (hour - 6) / 1;
        this.ambientLight.intensity = 0.2 + dawnProgress * 0.3;
        this.hemisphereLight.intensity = 0.3 + dawnProgress * 0.3;
        break;

      case 'day':
        this.ambientLight.intensity = 0.5;
        this.hemisphereLight.intensity = 0.6;
        break;

      case 'dusk':
        const duskProgress = (hour - 18) / 1;
        this.ambientLight.intensity = 0.5 - duskProgress * 0.3;
        this.hemisphereLight.intensity = 0.6 - duskProgress * 0.3;
        break;

      case 'night':
        this.ambientLight.intensity = 0.2;
        this.hemisphereLight.intensity = 0.3;
        break;
    }
  }

  /**
   * Set time of day
   * @param {number} hour - Hour (0-24)
   */
  setTime(hour) {
    this.timeOfDay = Math.max(0, Math.min(24, hour));
    this.updateLighting();
    console.log(`🕐 Time set to ${this.getFormattedTime()}`);
  }

  /**
   * Set time speed multiplier
   * @param {number} speed - Speed multiplier (1.0 = real-time, 60.0 = 1 min = 1 hour)
   */
  setTimeSpeed(speed) {
    this.timeSpeed = Math.max(0, speed);
    console.log(`⏱️ Time speed set to ${speed}x`);
  }

  /**
   * Pause/resume time progression
   */
  pause() {
    this.isPaused = true;
    console.log('⏸️ Time paused');
  }

  resume() {
    this.isPaused = false;
    console.log('▶️ Time resumed');
  }

  togglePause() {
    this.isPaused = !this.isPaused;
    console.log(this.isPaused ? '⏸️ Time paused' : '▶️ Time resumed');
  }

  /**
   * Get formatted time string
   * @returns {string} - "HH:MM"
   */
  getFormattedTime() {
    const hour = Math.floor(this.timeOfDay);
    const minute = Math.floor((this.timeOfDay - hour) * 60);
    return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
  }

  /**
   * Get time info
   */
  getTimeInfo() {
    return {
      timeOfDay: this.timeOfDay,
      formattedTime: this.getFormattedTime(),
      period: this.getTimePeriod(this.timeOfDay),
      timeSpeed: this.timeSpeed,
      isPaused: this.isPaused,
      isDaytime: this.timeOfDay >= 6 && this.timeOfDay < 18,
      isNighttime: this.timeOfDay < 6 || this.timeOfDay >= 18
    };
  }

  /**
   * Skip to specific time period
   * @param {string} period - "dawn", "noon", "dusk", "midnight"
   */
  skipTo(period) {
    switch (period) {
      case 'dawn':
        this.setTime(6);
        break;
      case 'noon':
      case 'day':
        this.setTime(12);
        break;
      case 'dusk':
        this.setTime(18);
        break;
      case 'midnight':
      case 'night':
        this.setTime(0);
        break;
      default:
        console.warn(`Unknown period: ${period}`);
    }
  }

  /**
   * Enable/disable shadows globally
   * @param {boolean} enabled
   */
  setShadowsEnabled(enabled) {
    this.sunLight.castShadow = enabled;
    this.moonLight.castShadow = enabled;
    this.renderer.shadowMap.enabled = enabled;
    console.log(`🌓 Shadows ${enabled ? 'enabled' : 'disabled'}`);
  }

  /**
   * Cleanup
   */
  dispose() {
    this.scene.remove(this.sunLight);
    this.scene.remove(this.moonLight);
    this.scene.remove(this.ambientLight);
    this.scene.remove(this.hemisphereLight);
    this.scene.remove(this.sun);
    this.scene.remove(this.moon);

    console.log('☀️🌙 Day/Night cycle disposed');
  }
}

// Window export for script-tag usage (ES6 export removed)

// Window export for script-tag usage
if (typeof window !== 'undefined') {
  window.DayNightCycle = DayNightCycle;
}
