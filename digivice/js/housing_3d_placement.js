/**
 * Housing 3D Placement System - Najika World
 * Hybrid placement system combining 2D planning with 3D preview
 *
 * Features:
 * - Ghost preview of furniture in 3D scene
 * - Snap-to-grid placement
 * - Rotation controls (R key)
 * - Collision detection
 * - Integration with housing_ui.js
 *
 * NOTE: Uses THREE from global scope
 */

(function() {
    'use strict';

    if (typeof THREE === 'undefined') {
        console.error('❌ THREE.js is required for Housing3DPlacement');
        return;
    }

class Housing3DPlacement {
    constructor(scene, camera) {
        this.scene = scene;
        this.camera = camera;

        // Placement state
        this.isPlacing = false;
        this.ghostObject = null;
        this.currentFurniture = null;
        this.placementPosition = new THREE.Vector3();
        this.placementRotation = 0; // Rotation in radians
        this.gridSize = 1; // 1 meter grid
        this.housePosition = new THREE.Vector3(0, 0, 0);
        this.houseSize = { width: 10, depth: 10 }; // Default house dimensions

        // Raycaster for mouse picking
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);

        // Event listeners
        this.onMouseMoveBound = this.onMouseMove.bind(this);
        this.onMouseClickBound = this.onMouseClick.bind(this);
        this.onKeyPressBound = this.onKeyPress.bind(this);

        console.log('🏠 Housing 3D Placement initialized');
    }

    /**
     * Start placing furniture
     * @param {Object} furniture - Furniture data {id, name, size, model}
     * @param {Vector3} housePosition - House position in world
     * @param {Object} houseSize - {width, depth}
     */
    startPlacement(furniture, housePosition, houseSize) {
        if (this.isPlacing) {
            this.cancelPlacement();
        }

        this.currentFurniture = furniture;
        this.housePosition.copy(housePosition);
        this.houseSize = houseSize;
        this.placementRotation = 0;

        // Create ghost preview
        this.createGhostPreview(furniture);

        // Enable mouse tracking
        this.isPlacing = true;
        window.addEventListener('mousemove', this.onMouseMoveBound);
        window.addEventListener('click', this.onMouseClickBound);
        window.addEventListener('keydown', this.onKeyPressBound);

        console.log(`🏠 Placing furniture: ${furniture.name}`);
    }

    /**
     * Create ghost preview mesh
     * @param {Object} furniture - Furniture data
     */
    createGhostPreview(furniture) {
        // Create simple box geometry for preview
        const size = furniture.size || { x: 1, y: 1, z: 1 };

        const geometry = new THREE.BoxGeometry(size.x, size.y, size.z);
        const material = new THREE.MeshStandardMaterial({
            color: 0x00ff00,
            transparent: true,
            opacity: 0.5,
            emissive: 0x00ff00,
            emissiveIntensity: 0.3
        });

        this.ghostObject = new THREE.Mesh(geometry, material);
        this.ghostObject.position.y = size.y / 2; // Lift to sit on ground

        // Add wireframe outline
        const wireframe = new THREE.WireframeGeometry(geometry);
        const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 });
        const outline = new THREE.LineSegments(wireframe, lineMaterial);
        this.ghostObject.add(outline);

        this.scene.add(this.ghostObject);
    }

    /**
     * Update ghost preview position
     * @param {number} mouseX - Mouse X (-1 to 1)
     * @param {number} mouseY - Mouse Y (-1 to 1)
     */
    updateGhostPosition(mouseX, mouseY) {
        if (!this.ghostObject || !this.camera) return;

        // Raycast from camera to ground plane
        this.raycaster.setFromCamera(new THREE.Vector2(mouseX, mouseY), this.camera);

        const intersection = new THREE.Vector3();
        this.raycaster.ray.intersectPlane(this.groundPlane, intersection);

        if (intersection) {
            // Snap to grid
            intersection.x = Math.round(intersection.x / this.gridSize) * this.gridSize;
            intersection.z = Math.round(intersection.z / this.gridSize) * this.gridSize;

            // Constrain to house bounds
            const halfWidth = this.houseSize.width / 2;
            const halfDepth = this.houseSize.depth / 2;

            intersection.x = THREE.MathUtils.clamp(
                intersection.x,
                this.housePosition.x - halfWidth + this.gridSize,
                this.housePosition.x + halfWidth - this.gridSize
            );

            intersection.z = THREE.MathUtils.clamp(
                intersection.z,
                this.housePosition.z - halfDepth + this.gridSize,
                this.housePosition.z + halfDepth - this.gridSize
            );

            this.placementPosition.copy(intersection);
            this.ghostObject.position.x = intersection.x;
            this.ghostObject.position.z = intersection.z;

            // Apply rotation
            this.ghostObject.rotation.y = this.placementRotation;

            // Check collision
            const isValid = this.checkPlacementValid();
            this.ghostObject.material.color.setHex(isValid ? 0x00ff00 : 0xff0000);
        }
    }

    /**
     * Check if current placement is valid (no collisions)
     * @returns {boolean}
     */
    checkPlacementValid() {
        if (!this.ghostObject) return false;

        // TODO: Implement proper collision detection with existing furniture
        // For now, always return true (simplified)

        // Check if inside house bounds
        const halfWidth = this.houseSize.width / 2;
        const halfDepth = this.houseSize.depth / 2;

        const isInside =
            this.placementPosition.x >= this.housePosition.x - halfWidth &&
            this.placementPosition.x <= this.housePosition.x + halfWidth &&
            this.placementPosition.z >= this.housePosition.z - halfDepth &&
            this.placementPosition.z <= this.housePosition.z + halfDepth;

        return isInside;
    }

    /**
     * Rotate ghost preview
     * @param {number} direction - 1 for clockwise, -1 for counter-clockwise
     */
    rotate(direction = 1) {
        if (!this.isPlacing || !this.ghostObject) return;

        // Rotate by 90 degrees
        this.placementRotation += (Math.PI / 2) * direction;
        this.placementRotation = this.placementRotation % (Math.PI * 2);

        this.ghostObject.rotation.y = this.placementRotation;

        console.log(`🔄 Rotated to ${Math.round((this.placementRotation * 180) / Math.PI)}°`);
    }

    /**
     * Confirm placement
     * @returns {Object|null} Placement data or null if invalid
     */
    confirmPlacement() {
        if (!this.isPlacing || !this.checkPlacementValid()) {
            console.warn('⚠️ Invalid placement');
            return null;
        }

        const placementData = {
            furniture: this.currentFurniture,
            position: {
                x: this.placementPosition.x,
                y: this.placementPosition.y,
                z: this.placementPosition.z
            },
            rotation: this.placementRotation
        };

        console.log('✅ Furniture placed:', placementData);

        // Cancel placement mode
        this.cancelPlacement();

        return placementData;
    }

    /**
     * Cancel placement
     */
    cancelPlacement() {
        if (!this.isPlacing) return;

        this.isPlacing = false;

        // Remove ghost preview
        if (this.ghostObject) {
            if (this.ghostObject.geometry) this.ghostObject.geometry.dispose();
            if (this.ghostObject.material) this.ghostObject.material.dispose();

            // Dispose outline
            this.ghostObject.traverse(child => {
                if (child.geometry) child.geometry.dispose();
                if (child.material) child.material.dispose();
            });

            this.scene.remove(this.ghostObject);
            this.ghostObject = null;
        }

        // Remove event listeners
        window.removeEventListener('mousemove', this.onMouseMoveBound);
        window.removeEventListener('click', this.onMouseClickBound);
        window.removeEventListener('keydown', this.onKeyPressBound);

        this.currentFurniture = null;

        console.log('🏠 Placement cancelled');
    }

    /**
     * Mouse move handler
     * @param {MouseEvent} event
     */
    onMouseMove(event) {
        if (!this.isPlacing) return;

        // Calculate normalized device coordinates
        this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

        this.updateGhostPosition(this.mouse.x, this.mouse.y);
    }

    /**
     * Mouse click handler
     * @param {MouseEvent} event
     */
    onMouseClick(event) {
        if (!this.isPlacing) return;

        const placementData = this.confirmPlacement();

        if (placementData) {
            // Notify housing system
            if (window.HousingSystem && window.HousingSystem.onFurniturePlaced) {
                window.HousingSystem.onFurniturePlaced(placementData);
            }

            // Trigger custom event
            window.dispatchEvent(new CustomEvent('furniturePlaced', {
                detail: placementData
            }));
        }
    }

    /**
     * Keyboard handler
     * @param {KeyboardEvent} event
     */
    onKeyPress(event) {
        if (!this.isPlacing) return;

        switch (event.code) {
            case 'KeyR':
                this.rotate(event.shiftKey ? -1 : 1);
                break;
            case 'Escape':
                this.cancelPlacement();
                break;
        }
    }

    /**
     * Set house dimensions for placement bounds
     * @param {Vector3} position - House position
     * @param {Object} size - {width, depth}
     */
    setHouseBounds(position, size) {
        this.housePosition.copy(position);
        this.houseSize = size;
    }

    /**
     * Check if currently placing
     * @returns {boolean}
     */
    isCurrentlyPlacing() {
        return this.isPlacing;
    }

    /**
     * Dispose system
     */
    dispose() {
        this.cancelPlacement();
        console.log('🏠 Housing 3D Placement disposed');
    }
}

// Export to global scope
window.Housing3DPlacement = Housing3DPlacement;

console.log('🏠 Housing3DPlacement loaded successfully');

})();
