// 🌧️ WEATHER SYSTEM - Dynamic weather effects for biomes
// Rain, Snow, Fog, Storms, Wind effects

// THREE is loaded globally

class WeatherSystem {
  constructor(scene, camera) {
    this.scene = scene;
    this.camera = camera;

    // Weather state
    this.currentWeather = null;
    this.weatherIntensity = 0.0;  // 0.0 - 1.0
    this.transitionSpeed = 0.01;  // Smooth weather transitions

    // Weather particle systems
    this.rainParticles = null;
    this.snowParticles = null;
    this.fogSystem = null;

    // Weather effects
    this.windDirection = new THREE.Vector3(1, 0, 0);
    this.windStrength = 0.0;

    // Configuration
    this.config = {
      rainParticleCount: 10000,
      snowParticleCount: 5000,
      particleSpread: 500,
      particleHeight: 300,
      rainSpeed: 50,
      snowSpeed: 10
    };

    console.log('🌧️ Weather System initialized');
  }

  /**
   * Initialize particle systems
   */
  initialize() {
    console.log('🌧️ Creating weather particle systems...');

    this.createRainSystem();
    this.createSnowSystem();

    console.log('🌧️ Weather systems ready');
  }

  /**
   * Create rain particle system
   */
  createRainSystem() {
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];

    const { rainParticleCount, particleSpread, particleHeight } = this.config;

    for (let i = 0; i < rainParticleCount; i++) {
      // Random position in a cylinder around camera
      const x = (Math.random() - 0.5) * particleSpread;
      const y = Math.random() * particleHeight;
      const z = (Math.random() - 0.5) * particleSpread;

      positions.push(x, y, z);

      // Velocity (downward + slight wind)
      velocities.push(
        (Math.random() - 0.5) * 2,   // x (wind)
        -this.config.rainSpeed * (0.8 + Math.random() * 0.4),  // y (falling)
        (Math.random() - 0.5) * 2    // z (wind)
      );
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.Float32BufferAttribute(velocities, 3));

    // Rain material (thin white lines)
    const material = new THREE.PointsMaterial({
      color: 0xaaaaaa,
      size: 0.5,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending
    });

    this.rainParticles = new THREE.Points(geometry, material);
    this.rainParticles.visible = false;
    this.scene.add(this.rainParticles);

    console.log('  ✅ Rain system created');
  }

  /**
   * Create snow particle system
   */
  createSnowSystem() {
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];

    const { snowParticleCount, particleSpread, particleHeight } = this.config;

    for (let i = 0; i < snowParticleCount; i++) {
      // Random position
      const x = (Math.random() - 0.5) * particleSpread;
      const y = Math.random() * particleHeight;
      const z = (Math.random() - 0.5) * particleSpread;

      positions.push(x, y, z);

      // Velocity (slower falling, more wind drift)
      velocities.push(
        (Math.random() - 0.5) * 5,   // x (wind drift)
        -this.config.snowSpeed * (0.5 + Math.random() * 0.5),  // y (floating down)
        (Math.random() - 0.5) * 5    // z (wind drift)
      );
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.Float32BufferAttribute(velocities, 3));

    // Snow material (white fluffy particles)
    const material = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 2.0,
      transparent: true,
      opacity: 0.8,
      map: this.createSnowflakeTexture(),
      blending: THREE.AdditiveBlending
    });

    this.snowParticles = new THREE.Points(geometry, material);
    this.snowParticles.visible = false;
    this.scene.add(this.snowParticles);

    console.log('  ✅ Snow system created');
  }

  /**
   * Create snowflake texture
   */
  createSnowflakeTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 32;
    canvas.height = 32;
    const ctx = canvas.getContext('2d');

    // Draw snowflake
    const centerX = 16;
    const centerY = 16;
    const radius = 12;

    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fill();

    // Add gradient for soft edges
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
    gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.5)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 32, 32);

    const texture = new THREE.CanvasTexture(canvas);
    return texture;
  }

  /**
   * Set weather type
   * @param {string} weatherType - "clear", "rain", "snow", "storm", "fog"
   * @param {number} intensity - 0.0 - 1.0
   */
  setWeather(weatherType, intensity = 0.5) {
    console.log(`🌧️ Setting weather: ${weatherType} (intensity: ${intensity})`);

    this.currentWeather = weatherType;
    this.targetIntensity = Math.min(1.0, Math.max(0.0, intensity));

    // Immediate visibility changes
    this.updateWeatherVisibility();
  }

  /**
   * Update weather visibility based on current weather
   */
  updateWeatherVisibility() {
    // Hide all weather effects first
    if (this.rainParticles) this.rainParticles.visible = false;
    if (this.snowParticles) this.snowParticles.visible = false;

    // Show active weather
    switch (this.currentWeather) {
      case 'rain':
      case 'storm':
        if (this.rainParticles) this.rainParticles.visible = true;
        break;

      case 'snow':
        if (this.snowParticles) this.snowParticles.visible = true;
        break;

      case 'fog':
        // Fog is handled by scene.fog in biome system
        break;

      case 'clear':
      default:
        // No particles
        break;
    }
  }

  /**
   * Update weather system (call every frame)
   * @param {number} deltaTime - Time since last frame (seconds)
   */
  update(deltaTime) {
    if (!this.currentWeather || this.currentWeather === 'clear') return;

    // Smooth intensity transition
    if (this.weatherIntensity < this.targetIntensity) {
      this.weatherIntensity = Math.min(
        this.targetIntensity,
        this.weatherIntensity + this.transitionSpeed
      );
    } else if (this.weatherIntensity > this.targetIntensity) {
      this.weatherIntensity = Math.max(
        this.targetIntensity,
        this.weatherIntensity - this.transitionSpeed
      );
    }

    // Update rain
    if (this.currentWeather === 'rain' || this.currentWeather === 'storm') {
      this.updateRainParticles(deltaTime);
    }

    // Update snow
    if (this.currentWeather === 'snow') {
      this.updateSnowParticles(deltaTime);
    }

    // Follow camera
    this.followCamera();
  }

  /**
   * Update rain particles
   */
  updateRainParticles(deltaTime) {
    if (!this.rainParticles || !this.rainParticles.visible) return;

    const positions = this.rainParticles.geometry.attributes.position.array;
    const velocities = this.rainParticles.geometry.attributes.velocity.array;

    for (let i = 0; i < positions.length; i += 3) {
      // Update position based on velocity
      positions[i] += velocities[i] * deltaTime * this.weatherIntensity;       // x
      positions[i + 1] += velocities[i + 1] * deltaTime * this.weatherIntensity; // y
      positions[i + 2] += velocities[i + 2] * deltaTime * this.weatherIntensity; // z

      // Reset if particle falls below ground
      if (positions[i + 1] < 0) {
        positions[i + 1] = this.config.particleHeight;
      }

      // Keep within bounds (wrap around)
      const bound = this.config.particleSpread / 2;
      if (Math.abs(positions[i]) > bound) {
        positions[i] = (Math.random() - 0.5) * this.config.particleSpread;
      }
      if (Math.abs(positions[i + 2]) > bound) {
        positions[i + 2] = (Math.random() - 0.5) * this.config.particleSpread;
      }
    }

    this.rainParticles.geometry.attributes.position.needsUpdate = true;

    // Storm effect: more intense
    if (this.currentWeather === 'storm') {
      this.rainParticles.material.opacity = 0.8 * this.weatherIntensity;
    } else {
      this.rainParticles.material.opacity = 0.6 * this.weatherIntensity;
    }
  }

  /**
   * Update snow particles
   */
  updateSnowParticles(deltaTime) {
    if (!this.snowParticles || !this.snowParticles.visible) return;

    const positions = this.snowParticles.geometry.attributes.position.array;
    const velocities = this.snowParticles.geometry.attributes.velocity.array;

    for (let i = 0; i < positions.length; i += 3) {
      // Update position
      positions[i] += velocities[i] * deltaTime * this.weatherIntensity;       // x (drift)
      positions[i + 1] += velocities[i + 1] * deltaTime * this.weatherIntensity; // y (fall)
      positions[i + 2] += velocities[i + 2] * deltaTime * this.weatherIntensity; // z (drift)

      // Add swirling motion
      const time = Date.now() * 0.001;
      positions[i] += Math.sin(time + i) * 0.05;
      positions[i + 2] += Math.cos(time + i) * 0.05;

      // Reset if particle falls below ground
      if (positions[i + 1] < 0) {
        positions[i + 1] = this.config.particleHeight;
      }

      // Keep within bounds
      const bound = this.config.particleSpread / 2;
      if (Math.abs(positions[i]) > bound) {
        positions[i] = (Math.random() - 0.5) * this.config.particleSpread;
      }
      if (Math.abs(positions[i + 2]) > bound) {
        positions[i + 2] = (Math.random() - 0.5) * this.config.particleSpread;
      }
    }

    this.snowParticles.geometry.attributes.position.needsUpdate = true;

    // Fade based on intensity
    this.snowParticles.material.opacity = 0.8 * this.weatherIntensity;
  }

  /**
   * Follow camera position (weather system moves with player)
   */
  followCamera() {
    const cameraPos = this.camera.position;

    if (this.rainParticles) {
      this.rainParticles.position.set(cameraPos.x, 0, cameraPos.z);
    }

    if (this.snowParticles) {
      this.snowParticles.position.set(cameraPos.x, 0, cameraPos.z);
    }
  }

  /**
   * Set wind direction and strength
   * @param {THREE.Vector3} direction - Wind direction vector
   * @param {number} strength - 0.0 - 1.0
   */
  setWind(direction, strength) {
    this.windDirection = direction.normalize();
    this.windStrength = strength;

    // Update particle velocities
    if (this.rainParticles) {
      const velocities = this.rainParticles.geometry.attributes.velocity.array;
      for (let i = 0; i < velocities.length; i += 3) {
        velocities[i] = this.windDirection.x * this.windStrength * 10;
        velocities[i + 2] = this.windDirection.z * this.windStrength * 10;
      }
      this.rainParticles.geometry.attributes.velocity.needsUpdate = true;
    }

    if (this.snowParticles) {
      const velocities = this.snowParticles.geometry.attributes.velocity.array;
      for (let i = 0; i < velocities.length; i += 3) {
        velocities[i] = this.windDirection.x * this.windStrength * 5;
        velocities[i + 2] = this.windDirection.z * this.windStrength * 5;
      }
      this.snowParticles.geometry.attributes.velocity.needsUpdate = true;
    }
  }

  /**
   * Apply biome-specific weather
   * @param {Object} biome - Biome configuration
   */
  applyBiomeWeather(biome) {
    if (!biome.weather || biome.weather.length === 0) {
      this.setWeather('clear', 0);
      return;
    }

    // Select random weather from biome's weather types
    const weatherType = biome.weather[Math.floor(Math.random() * biome.weather.length)];

    // Intensity based on biome
    let intensity = 0.5;

    switch (weatherType) {
      case 'rain':
        intensity = 0.6;
        break;
      case 'storm':
        intensity = 0.9;
        break;
      case 'snow':
        intensity = 0.7;
        break;
      case 'fog':
        intensity = 0.8;
        break;
    }

    this.setWeather(weatherType, intensity);

    console.log(`🌧️ Applied ${biome.name} weather: ${weatherType}`);
  }

  /**
   * Clear all weather effects
   */
  clearWeather() {
    this.setWeather('clear', 0);
    console.log('🌧️ Weather cleared');
  }

  /**
   * Cleanup
   */
  dispose() {
    if (this.rainParticles) {
      this.scene.remove(this.rainParticles);
      this.rainParticles.geometry.dispose();
      this.rainParticles.material.dispose();
    }

    if (this.snowParticles) {
      this.scene.remove(this.snowParticles);
      this.snowParticles.geometry.dispose();
      this.snowParticles.material.dispose();
    }

    console.log('🌧️ Weather system disposed');
  }

  /**
   * Get current weather info
   */
  getWeatherInfo() {
    return {
      currentWeather: this.currentWeather,
      intensity: this.weatherIntensity,
      windDirection: this.windDirection,
      windStrength: this.windStrength
    };
  }
}

// Window export for script-tag usage (ES6 export removed)

// Window export for script-tag usage
if (typeof window !== 'undefined') {
  window.WeatherSystem = WeatherSystem;
}
