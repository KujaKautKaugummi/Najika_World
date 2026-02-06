# Vegetation System InstancedMesh Refactor Plan

## Problem Statement

**Current Issue:**
- VegetationSystem uses `.clone()` for each vegetation instance ([vegetation_system.js:280](C:\Najika_World\digivice\js\world\vegetation_system.js#L280))
- Results in 200,000+ individual draw calls per frame
- FPS drops to 15 in vegetation-heavy areas (should be 60+)

**Root Cause:**
- Each vegetation is a separate THREE.Mesh → separate draw call
- No batching/instancing applied during population
- `lod_manager.js` has `batchVegetation()` but it's NEVER called

**Impact:**
- Unplayable performance (15 FPS vs 60+ FPS target)
- Critical blocker for large worlds

---

## Solution Strategy

**Core Approach: THREE.InstancedMesh**
- Group vegetation by type during `populateRegion()`
- Create ONE InstancedMesh per vegetation type per region
- Expected: 200,000+ draw calls → ~30 draw calls (99.98% reduction)
- Target FPS: 60+ (300% improvement)

**Key Technical Decisions:**
1. **Pre-batch during population** - Don't create individual meshes first
2. **Maintain API compatibility** - External code sees no changes
3. **Feature flag migration** - Keep legacy code during transition
4. **Spatial index for queries** - Separate data structure for `getVegetationNear()`
5. **Visibility flags for removal** - Can't remove from InstancedMesh, hide instead

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)

**Add new data structures to `vegetation_system.js`:**

```javascript
// Per-region instanced mesh management
class RegionInstancedVegetation {
  constructor(regionId) {
    this.instancedMeshes = new Map(); // type → InstancedMeshData
    this.spatialGrid = new SpatialGrid(50); // Fast proximity queries
    this.instanceMetadata = new Map(); // instanceId → metadata
    this.nextInstanceId = 0;
  }
}

// Per-type instanced mesh data
class InstancedMeshData {
  constructor(geometry, material, maxInstances) {
    this.mesh = new THREE.InstancedMesh(geometry, material, maxInstances);
    this.count = 0;
    this.visibilityArray = new Float32Array(maxInstances); // For hiding
    this.freeSlots = []; // Reuse removed slots
  }
}

// Spatial index for fast queries
class SpatialGrid {
  constructor(cellSize = 50) {
    this.grid = new Map(); // cellKey → Set<instanceId>
  }
  queryRadius(position, radius) { /* ... */ }
}
```

**Update VegetationSystem:**
- Add `this.instancedRegions = new Map()` for instanced regions
- Add `this.useInstancing = true` feature flag
- Rename existing methods to `*Legacy` suffix

### Phase 2: Instanced Population (Week 1)

**Refactor `populateRegion()` to batch by type:**

```javascript
populateRegionInstanced(regionId, regionData, biomeData) {
  // 1. Generate ALL vegetation positions first
  const vegetationByType = new Map(); // type → [{position, rotation, scale}]

  for (let i = 0; i < vegetationCount; i++) {
    // Generate position/rotation/scale
    const type = selectRandomType();
    vegetationByType.get(type).push({position, rotation, scale});
  }

  // 2. Create ONE InstancedMesh per type
  for (const [type, instances] of vegetationByType.entries()) {
    this.createInstancedVegetationGroup(regionId, type, instances);
  }
}
```

**Key changes:**
- NO `.clone()` calls
- Group by type BEFORE creating meshes
- Use `THREE.Matrix4` for transforms
- Pre-allocate buffer with 30% overhead for dynamic spawning

### Phase 3: Dynamic Operations (Week 2)

**Handle removal with visibility flags:**
```javascript
removeVegetationAt(position, radius) {
  // Find nearby instances via spatial grid
  const candidateIds = spatialGrid.queryRadius(position, radius);

  // Hide instances (don't actually remove)
  for (const instanceId of candidateIds) {
    instancedMeshData.visibilityArray[index] = 0.0; // GPU will cull
  }

  instancedMeshData.mesh.geometry.attributes.instanceVisibility.needsUpdate = true;
}
```

**Handle spawning with free slots:**
```javascript
spawnVegetationAt(type, position) {
  // Reuse freed slot or allocate new
  const index = instancedMeshData.freeSlots.pop() || instancedMeshData.count++;

  // Set matrix transform
  matrix.compose(position, rotation, scale);
  instancedMeshData.mesh.setMatrixAt(index, matrix);
  instancedMeshData.mesh.instanceMatrix.needsUpdate = true;
}
```

### Phase 4: Spatial Queries (Week 2)

**Maintain separate spatial index:**
```javascript
getVegetationNearInstanced(position, radius) {
  // 1. Broad-phase: Spatial grid query
  const candidateIds = spatialGrid.queryRadius(position, radius);

  // 2. Narrow-phase: Distance check against metadata
  const nearby = [];
  for (const instanceId of candidateIds) {
    const metadata = instanceMetadata.get(instanceId);
    if (metadata.position.distanceTo(position) <= radius) {
      nearby.push(metadata);
    }
  }
  return nearby;
}
```

### Phase 5: API Compatibility (Week 2)

**Feature flag delegation pattern:**
```javascript
populateRegion(regionId, regionData, biomeData) {
  if (this.useInstancing) {
    return this.populateRegionInstanced(regionId, regionData, biomeData);
  } else {
    return this.populateRegionLegacy(regionId, regionData, biomeData);
  }
}
```

**External code unchanged:**
- `RegionStreaming` calls same APIs
- `WorldManager` proxies same methods
- No changes needed outside `vegetation_system.js`

---

## Critical Files

**Primary Modification:**
- `C:\Najika_World\digivice\js\world\vegetation_system.js` (442 lines)
  - Add new data structures (RegionInstancedVegetation, InstancedMeshData, SpatialGrid)
  - Refactor `populateRegion()` to batch by type
  - Implement instanced versions of all methods
  - Add feature flag delegation

**Integration Points (verify compatibility):**
- `C:\Najika_World\digivice\js\world\region_streaming_v2.js:198`
  - Calls `vegetationSystem.populateRegion()` - must continue working
- `C:\Najika_World\digivice\js\world\world_manager.js:298-319`
  - Proxies `getVegetationNear()`, `removeVegetationAt()`, `spawnVegetationAt()`
  - Must maintain same signatures

**Reference (optional reuse):**
- `C:\Najika_World\digivice\js\world\lod_manager.js:340-407`
  - Has `createInstancedMesh()` and `batchVegetation()` methods
  - Currently unused, can adapt patterns

---

## Migration Strategy

**Week 1: Development**
- Implement all instanced methods with `*Instanced` suffix
- Rename existing methods to `*Legacy` suffix
- Add feature flag with default `useInstancing = false`

**Week 2: Testing**
- Enable flag: `vegetationSystem.useInstancing = true`
- Test all APIs: populate, remove, spawn, query
- Performance benchmarking
- Fix any issues

**Week 3: Rollout**
- Change default to `useInstancing = true`
- Monitor for regressions
- A/B test in production

**Week 4+: Cleanup**
- Remove feature flag
- Remove legacy methods
- Update documentation

---

## Testing & Verification

### Unit Tests
```javascript
// Test spatial grid queries
test('SpatialGrid.queryRadius returns nearby instances', () => {
  const grid = new SpatialGrid(50);
  grid.insert('id1', new THREE.Vector3(100, 0, 100));
  grid.insert('id2', new THREE.Vector3(110, 0, 110));

  const results = grid.queryRadius(new THREE.Vector3(100, 0, 100), 20);
  expect(results).toContain('id1');
  expect(results).toContain('id2');
});

// Test instance allocation
test('InstancedMeshData reuses freed slots', () => {
  const data = new InstancedMeshData(geo, mat, 100);
  const idx1 = data.allocateInstance('id1');
  data.freeInstance('id1');
  const idx2 = data.allocateInstance('id2');
  expect(idx2).toBe(idx1); // Reused
});
```

### Integration Tests
```javascript
// Test region streaming
test('Region load/unload cycles work with instancing', async () => {
  vegetationSystem.useInstancing = true;
  regionStreaming.loadRegion('forest_region');

  expect(vegetationSystem.instancedRegions.has('forest_region')).toBe(true);

  regionStreaming.unloadRegion('forest_region');
  expect(vegetationSystem.instancedRegions.has('forest_region')).toBe(false);
});

// Test API compatibility
test('getVegetationNear returns same results', () => {
  const pos = new THREE.Vector3(100, 0, 100);

  vegetationSystem.useInstancing = false;
  vegetationSystem.populateRegion('test', regionData, biomeData);
  const legacyResults = vegetationSystem.getVegetationNear(pos, 50);

  vegetationSystem.removeRegionVegetation('test');

  vegetationSystem.useInstancing = true;
  vegetationSystem.populateRegion('test', regionData, biomeData);
  const instancedResults = vegetationSystem.getVegetationNear(pos, 50);

  expect(instancedResults.length).toBe(legacyResults.length);
});
```

### Performance Tests
```javascript
// Benchmark draw calls
test('Draw calls reduced by 99%+', () => {
  vegetationSystem.useInstancing = true;
  vegetationSystem.populateRegion('test', regionData, biomeData);

  const drawCalls = countDrawCalls(scene);
  expect(drawCalls).toBeLessThan(50); // Should be ~30
});

// Benchmark FPS
test('FPS improves by 300%+', () => {
  vegetationSystem.useInstancing = true;
  vegetationSystem.populateRegion('test', regionData, biomeData);

  const fps = measureAverageFPS(1000); // 1 second
  expect(fps).toBeGreaterThan(50); // Target 60 FPS
});
```

### Manual Verification
1. **Load world** - Verify vegetation appears correctly
2. **Walk around** - Check streaming loads/unloads regions
3. **Harvest vegetation** - Test `removeVegetationAt()` hides instances
4. **Replant vegetation** - Test `spawnVegetationAt()` shows instances
5. **Check console** - No errors, draw call count logged
6. **Performance profiling** - Chrome DevTools FPS counter

---

## Expected Outcomes

**Performance Improvements:**
- **Draw Calls:** 200,000+ → ~30 (99.98% reduction)
- **FPS:** 15 → 60+ (300% improvement)
- **Memory:** +10-15% for spatial index (acceptable)
- **Loading:** Similar or faster (batched operations)

**Compatibility:**
- ✅ All public APIs unchanged
- ✅ RegionStreaming works transparently
- ✅ WorldManager works transparently
- ✅ Existing game code unchanged

**Risk Mitigation:**
- Feature flag allows instant rollback
- Legacy implementation preserved during transition
- Comprehensive test coverage
- Gradual rollout strategy

---

## Success Criteria

- [ ] FPS in vegetation-heavy areas: 60+ (currently 15)
- [ ] Draw calls per frame: <50 (currently 200,000+)
- [ ] All unit tests pass (100% coverage for new code)
- [ ] All integration tests pass (region streaming, world manager)
- [ ] Manual testing: vegetation appears, harvesting works, replanting works
- [ ] Performance profiling: No memory leaks, stable FPS over time
- [ ] No breaking changes to external code

---

## Next Steps

1. **Start with Phase 1** - Implement data structures (SpatialGrid, InstancedMeshData, RegionInstancedVegetation)
2. **Implement Phase 2** - Refactor populateRegion() to batch by type
3. **Test incrementally** - Verify each phase before moving to next
4. **Enable feature flag** - Test with real world data
5. **Performance benchmark** - Measure actual FPS improvement
6. **Gradual rollout** - Monitor for issues
