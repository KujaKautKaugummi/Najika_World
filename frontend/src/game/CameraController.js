// Najika Camera Controller - 3 Modes
// Orbit Cam (Cheer Mode) / Third Person (Action) / First Person (Action)

export class CameraController {
  constructor(camera, target) {
    this.camera = camera;
    this.target = target; // Najika's position

    // Camera modes
    this.modes = {
      ORBIT: 'orbit',
      THIRD_PERSON: 'third_person',
      FIRST_PERSON: 'first_person'
    };

    this.currentMode = this.modes.ORBIT; // Start with Orbit

    // Orbit Cam settings
    this.orbit = {
      distance: 8,
      minDistance: 5,
      maxDistance: 15,
      height: 3,
      angle: 0,
      rotationSpeed: 2,
      autoRotate: false,
      autoRotateSpeed: 0.5
    };

    // Third Person settings (over-shoulder)
    this.thirdPerson = {
      offsetX: 1.2, // Right side
      offsetY: 2.0, // Height
      offsetZ: 3.5, // Behind
      lookAheadDistance: 2.0, // Look ahead of player
      smoothness: 0.15 // Camera lag/smoothness
    };

    // First Person settings
    this.firstPerson = {
      eyeHeight: 1.7, // Eye level
      bobAmount: 0.05, // Head bob intensity
      bobSpeed: 8,
      bobPhase: 0
    };

    // Mouse look
    this.mouseLook = {
      sensitivity: 0.002,
      yaw: 0, // Horizontal rotation
      pitch: 0, // Vertical rotation
      minPitch: -Math.PI / 2 + 0.1,
      maxPitch: Math.PI / 2 - 0.1
    };

    // Smooth camera movement
    this.currentPosition = { x: 0, y: 0, z: 0 };
    this.currentLookAt = { x: 0, y: 0, z: 0 };
  }

  // Switch camera mode
  setMode(mode) {
    if (Object.values(this.modes).includes(mode)) {
      this.currentMode = mode;
      this.resetCameraForMode();
      return { success: true, mode: this.currentMode };
    }
    return { success: false, reason: 'invalid_mode' };
  }

  // Reset camera position when switching modes
  resetCameraForMode() {
    switch (this.currentMode) {
      case this.modes.ORBIT:
        // Position camera for orbit
        this.camera.position.set(
          this.target.x,
          this.target.y + this.orbit.height,
          this.target.z + this.orbit.distance
        );
        break;

      case this.modes.THIRD_PERSON:
        // Position camera behind and to the side
        this.camera.position.set(
          this.target.x + this.thirdPerson.offsetX,
          this.target.y + this.thirdPerson.offsetY,
          this.target.z + this.thirdPerson.offsetZ
        );
        break;

      case this.modes.FIRST_PERSON:
        // Position camera at eye level
        this.camera.position.set(
          this.target.x,
          this.target.y + this.firstPerson.eyeHeight,
          this.target.z
        );
        break;
    }

    this.currentPosition = { ...this.camera.position };
    this.currentLookAt = { ...this.target };
  }

  // Update camera (called every frame)
  update(deltaTime, input = {}) {
    switch (this.currentMode) {
      case this.modes.ORBIT:
        this.updateOrbit(deltaTime, input);
        break;
      case this.modes.THIRD_PERSON:
        this.updateThirdPerson(deltaTime, input);
        break;
      case this.modes.FIRST_PERSON:
        this.updateFirstPerson(deltaTime, input);
        break;
    }
  }

  // Update Orbit Cam (Digimon World style)
  updateOrbit(deltaTime, input) {
    // Mouse drag to rotate
    if (input.mouseDown && input.mouseDeltaX) {
      this.orbit.angle -= input.mouseDeltaX * this.orbit.rotationSpeed * deltaTime;
    }

    // Auto-rotate if enabled
    if (this.orbit.autoRotate) {
      this.orbit.angle += this.orbit.autoRotateSpeed * deltaTime;
    }

    // Mouse wheel to zoom
    if (input.wheelDelta) {
      this.orbit.distance = Math.max(
        this.orbit.minDistance,
        Math.min(this.orbit.maxDistance, this.orbit.distance - input.wheelDelta * 0.1)
      );
    }

    // Calculate camera position in orbit
    const targetPosition = {
      x: this.target.x + Math.sin(this.orbit.angle) * this.orbit.distance,
      y: this.target.y + this.orbit.height,
      z: this.target.z + Math.cos(this.orbit.angle) * this.orbit.distance
    };

    // Smooth interpolation
    this.currentPosition.x += (targetPosition.x - this.currentPosition.x) * 0.1;
    this.currentPosition.y += (targetPosition.y - this.currentPosition.y) * 0.1;
    this.currentPosition.z += (targetPosition.z - this.currentPosition.z) * 0.1;

    // Apply to camera
    this.camera.position.set(
      this.currentPosition.x,
      this.currentPosition.y,
      this.currentPosition.z
    );

    // Always look at Najika
    this.camera.lookAt(this.target.x, this.target.y + 1, this.target.z);
  }

  // Update Third Person (over-shoulder)
  updateThirdPerson(deltaTime, input) {
    // Mouse look
    if (input.mouseDeltaX || input.mouseDeltaY) {
      this.mouseLook.yaw -= input.mouseDeltaX * this.mouseLook.sensitivity;
      this.mouseLook.pitch -= input.mouseDeltaY * this.mouseLook.sensitivity;

      // Clamp pitch
      this.mouseLook.pitch = Math.max(
        this.mouseLook.minPitch,
        Math.min(this.mouseLook.maxPitch, this.mouseLook.pitch)
      );
    }

    // Calculate camera position (behind and to the side)
    const yawSin = Math.sin(this.mouseLook.yaw);
    const yawCos = Math.cos(this.mouseLook.yaw);

    const targetPosition = {
      x: this.target.x - yawSin * this.thirdPerson.offsetZ + yawCos * this.thirdPerson.offsetX,
      y: this.target.y + this.thirdPerson.offsetY,
      z: this.target.z - yawCos * this.thirdPerson.offsetZ - yawSin * this.thirdPerson.offsetX
    };

    // Smooth camera lag
    const smoothness = this.thirdPerson.smoothness;
    this.currentPosition.x += (targetPosition.x - this.currentPosition.x) * smoothness;
    this.currentPosition.y += (targetPosition.y - this.currentPosition.y) * smoothness;
    this.currentPosition.z += (targetPosition.z - this.currentPosition.z) * smoothness;

    // Apply to camera
    this.camera.position.set(
      this.currentPosition.x,
      this.currentPosition.y,
      this.currentPosition.z
    );

    // Look ahead of player
    const lookAtPosition = {
      x: this.target.x + yawSin * this.thirdPerson.lookAheadDistance,
      y: this.target.y + 1,
      z: this.target.z + yawCos * this.thirdPerson.lookAheadDistance
    };

    // Smooth look-at
    this.currentLookAt.x += (lookAtPosition.x - this.currentLookAt.x) * smoothness;
    this.currentLookAt.y += (lookAtPosition.y - this.currentLookAt.y) * smoothness;
    this.currentLookAt.z += (lookAtPosition.z - this.currentLookAt.z) * smoothness;

    this.camera.lookAt(
      this.currentLookAt.x,
      this.currentLookAt.y,
      this.currentLookAt.z
    );
  }

  // Update First Person (ego perspective)
  updateFirstPerson(deltaTime, input) {
    // Mouse look
    if (input.mouseDeltaX || input.mouseDeltaY) {
      this.mouseLook.yaw -= input.mouseDeltaX * this.mouseLook.sensitivity;
      this.mouseLook.pitch -= input.mouseDeltaY * this.mouseLook.sensitivity;

      // Clamp pitch
      this.mouseLook.pitch = Math.max(
        this.mouseLook.minPitch,
        Math.min(this.mouseLook.maxPitch, this.mouseLook.pitch)
      );
    }

    // Head bob (when moving)
    let bobOffset = 0;
    if (input.isMoving) {
      this.firstPerson.bobPhase += deltaTime * this.firstPerson.bobSpeed;
      bobOffset = Math.sin(this.firstPerson.bobPhase) * this.firstPerson.bobAmount;
    } else {
      this.firstPerson.bobPhase = 0;
    }

    // Camera at eye level + bob
    this.camera.position.set(
      this.target.x,
      this.target.y + this.firstPerson.eyeHeight + bobOffset,
      this.target.z
    );

    // Calculate look direction
    const yawSin = Math.sin(this.mouseLook.yaw);
    const yawCos = Math.cos(this.mouseLook.yaw);
    const pitchCos = Math.cos(this.mouseLook.pitch);
    const pitchSin = Math.sin(this.mouseLook.pitch);

    const lookAtPosition = {
      x: this.camera.position.x + yawSin * pitchCos,
      y: this.camera.position.y + pitchSin,
      z: this.camera.position.z + yawCos * pitchCos
    };

    this.camera.lookAt(
      lookAtPosition.x,
      lookAtPosition.y,
      lookAtPosition.z
    );
  }

  // Get camera forward vector (for movement)
  getForwardVector() {
    const forward = {
      x: Math.sin(this.mouseLook.yaw),
      y: 0,
      z: Math.cos(this.mouseLook.yaw)
    };
    return forward;
  }

  // Get camera right vector (for strafing)
  getRightVector() {
    const right = {
      x: Math.cos(this.mouseLook.yaw),
      y: 0,
      z: -Math.sin(this.mouseLook.yaw)
    };
    return right;
  }

  // Toggle auto-rotate (orbit cam only)
  toggleAutoRotate() {
    if (this.currentMode === this.modes.ORBIT) {
      this.orbit.autoRotate = !this.orbit.autoRotate;
      return { success: true, autoRotate: this.orbit.autoRotate };
    }
    return { success: false, reason: 'not_in_orbit_mode' };
  }

  // Get current mode info
  getModeInfo() {
    return {
      mode: this.currentMode,
      isOrbit: this.currentMode === this.modes.ORBIT,
      isThirdPerson: this.currentMode === this.modes.THIRD_PERSON,
      isFirstPerson: this.currentMode === this.modes.FIRST_PERSON,
      settings: this.getCurrentSettings()
    };
  }

  // Get current mode settings
  getCurrentSettings() {
    switch (this.currentMode) {
      case this.modes.ORBIT:
        return { ...this.orbit };
      case this.modes.THIRD_PERSON:
        return { ...this.thirdPerson };
      case this.modes.FIRST_PERSON:
        return { ...this.firstPerson };
      default:
        return {};
    }
  }
}
