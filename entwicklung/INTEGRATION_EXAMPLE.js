// 🌍 INTEGRATION EXAMPLE - Vollständiges Beispiel für Najika World Integration
// Zeigt wie WorldManager in bestehenden Code integriert wird

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import WorldManager from '/entwicklung/world/world_manager.js';

// ============================================
// 1. SCENE SETUP
// ============================================

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  10000  // Far plane erhöht für große Welt
);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2 - 0.1;  // Nicht unter Terrain
controls.maxDistance = 500;
controls.minDistance = 10;

// Clock für deltaTime
const clock = new THREE.Clock();

// ============================================
// 2. WORLD MANAGER INITIALISIERUNG
// ============================================

let worldManager;
let initialized = false;

async function initWorld() {
  console.log('🌍 Initializing Najika World...');

  // WorldManager erstellen
  worldManager = new WorldManager(scene, camera);

  // Initialisieren (async!)
  const success = await worldManager.initialize({
    dataPath: '/entwicklung/data/',
    enableLOD: true,
    enableStreaming: true,
    enableVegetationBatching: true
  });

  if (success) {
    console.log('✅ World initialized successfully!');
    initialized = true;

    // Starte am Götterfels (Zentrum)
    worldManager.teleportTo(new THREE.Vector3(4800, 50, 4800));

    // Zeige Stats
    worldManager.logStats();
    worldManager.listCities();

    // Start animation
    animate();
  } else {
    console.error('❌ Failed to initialize world');
  }
}

// ============================================
// 3. ANIMATION LOOP
// ============================================

function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();

  // Update World-System
  if (initialized) {
    worldManager.update(deltaTime);
    worldManager.setPlayerPosition(camera.position);
  }

  // Update Controls
  controls.update();

  // Render
  renderer.render(scene, camera);
}

// ============================================
// 4. KEYBOARD CONTROLS (DEV MODE)
// ============================================

window.addEventListener('keydown', (e) => {
  if (!initialized) return;

  // Stats & Debug
  if (e.key === 'F1') {
    worldManager.logStats();
  }

  if (e.key === 'F2') {
    worldManager.listCities();
  }

  if (e.key === 'F3') {
    worldManager.listRegions();
  }

  if (e.key === 'F4') {
    worldManager.debugLOD(true);
  }

  if (e.key === 'F5') {
    worldManager.debugRegions();
  }

  // Schnell-Teleport zu Städten (Numpad 1-5)
  if (e.key === '1') {
    console.log('🏘️ Teleporting to Handelsfestung...');
    worldManager.teleportToCity('Handelsfestung');
  }

  if (e.key === '2') {
    console.log('🏘️ Teleporting to Dampf-Hain...');
    worldManager.teleportToCity('Dampf-Hain');
  }

  if (e.key === '3') {
    console.log('🏘️ Teleporting to Salzige Bucht...');
    worldManager.teleportToCity('Salzige Bucht');
  }

  if (e.key === '4') {
    console.log('🏘️ Teleporting to Runenheim...');
    worldManager.teleportToCity('Runenheim');
  }

  if (e.key === '5') {
    console.log('🏘️ Teleporting to Funken-Siedlung...');
    worldManager.teleportToCity('Funken-Siedlung');
  }

  // Teleport zu Regionen (Q, W, E, R, T, Z, U, I)
  if (e.key === 'q') {
    worldManager.teleportToRegion('samtmoos_tiefwald');
  }

  if (e.key === 'w') {
    worldManager.teleportToRegion('reich_der_drei');
  }

  if (e.key === 'e') {
    worldManager.teleportToRegion('salzwind_kueste');
  }

  if (e.key === 'r') {
    worldManager.teleportToRegion('blitzebene');
  }

  if (e.key === 't') {
    worldManager.teleportToRegion('gruenschlamm_sumpf');
  }

  if (e.key === 'z') {
    worldManager.teleportToRegion('magmastroeme');
  }

  if (e.key === 'u') {
    worldManager.teleportToRegion('heisse_duenen');
  }

  if (e.key === 'i') {
    worldManager.teleportToRegion('tiefenhoehlen');
  }

  // Götterfels (Zentrum)
  if (e.key === '0') {
    console.log('⛰️ Teleporting to Götterfels...');
    worldManager.teleportTo(new THREE.Vector3(4800, 50, 4800));
  }

  // Performance-Optionen (P, O, L)
  if (e.key === 'p') {
    // Toggle Streaming
    const streaming = !worldManager.enableStreaming;
    worldManager.setStreaming(streaming);
    console.log(`🌍 Streaming: ${streaming ? 'ON' : 'OFF'}`);
  }

  if (e.key === 'o') {
    // Toggle LOD
    const lod = !worldManager.enableLOD;
    worldManager.setLOD(lod);
    console.log(`🎯 LOD: ${lod ? 'ON' : 'OFF'}`);
  }

  if (e.key === 'l') {
    // LOD Debug Toggle
    static let lodDebug = false;
    lodDebug = !lodDebug;
    worldManager.debugLOD(lodDebug);
    console.log(`🎯 LOD Debug: ${lodDebug ? 'ON' : 'OFF'}`);
  }

  // Streaming Radius ändern (+ und -)
  if (e.key === '+') {
    const currentStats = worldManager.getStats();
    const newRadius = currentStats.streaming.loadRadiusRegions + 1;
    worldManager.setStreamingRadius(newRadius);
    console.log(`🌍 Streaming Radius: ${newRadius}`);
  }

  if (e.key === '-') {
    const currentStats = worldManager.getStats();
    const newRadius = Math.max(1, currentStats.streaming.loadRadiusRegions - 1);
    worldManager.setStreamingRadius(newRadius);
    console.log(`🌍 Streaming Radius: ${newRadius}`);
  }
});

// ============================================
// 5. UI INFO (OPTIONAL)
// ============================================

// Erstelle UI-Overlay für Info
const infoDiv = document.createElement('div');
infoDiv.style.position = 'absolute';
infoDiv.style.top = '10px';
infoDiv.style.left = '10px';
infoDiv.style.color = 'white';
infoDiv.style.fontFamily = 'monospace';
infoDiv.style.fontSize = '14px';
infoDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
infoDiv.style.padding = '10px';
infoDiv.style.borderRadius = '5px';
infoDiv.style.pointerEvents = 'none';
document.body.appendChild(infoDiv);

function updateUI() {
  if (!initialized) {
    infoDiv.innerHTML = '⏳ Loading...';
    return;
  }

  const stats = worldManager.getStats();
  const currentRegion = worldManager.getCurrentRegion();

  infoDiv.innerHTML = `
    <strong>🌍 NAJIKA WORLD</strong><br>
    📍 Region: ${currentRegion ? currentRegion.name : 'Unknown'}<br>
    🗺️ Loaded Regions: ${stats.streaming.loadedRegions} / ${stats.streaming.totalRegions}<br>
    🌿 Vegetation: ${stats.vegetation.totalVegetation}<br>
    🏘️ Cities: ${stats.cities.citiesLoaded}<br>
    🎯 LOD: H:${stats.lod.highDetail} M:${stats.lod.mediumDetail} L:${stats.lod.lowDetail} C:${stats.lod.culled}<br>
    <br>
    <strong>Controls:</strong><br>
    1-5: Teleport zu Städten<br>
    Q,W,E,R,T,Z,U,I: Teleport zu Regionen<br>
    0: Götterfels (Zentrum)<br>
    F1: Stats | F2: Städte | F3: Regionen<br>
    P: Toggle Streaming | O: Toggle LOD
  `;
}

setInterval(updateUI, 500);  // Update UI every 500ms

// ============================================
// 6. WINDOW RESIZE
// ============================================

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// ============================================
// 7. START APPLICATION
// ============================================

initWorld();

// ============================================
// 8. INTEGRATION MIT BESTEHENDEN SYSTEMEN
// ============================================

// Beispiel: Garden System Integration
function placeGarden() {
  const gardenX = 4900;
  const gardenZ = 4900;
  const gardenY = worldManager.getHeightAt(gardenX, gardenZ);

  const gardenPosition = new THREE.Vector3(gardenX, gardenY, gardenZ);

  console.log(`🌱 Garden placed at (${gardenX}, ${gardenY.toFixed(2)}, ${gardenZ})`);

  // Dein Garden-System Code hier...
  // createGarden(gardenPosition);
}

// Beispiel: Fishing System Integration
function canFishHere(position) {
  const currentRegion = worldManager.getCurrentRegion();

  if (!currentRegion) return false;

  // Prüfe ob Region Wasser hat
  if (currentRegion.waterPresence || currentRegion.hasOcean) {
    console.log('🎣 Fishing available!');
    return true;
  } else {
    console.log('❌ No water here!');
    return false;
  }
}

// Beispiel: Crafting System Integration
function getCraftingBonus() {
  const currentRegion = worldManager.getCurrentRegion();

  if (currentRegion && currentRegion.city) {
    // Spezielle Boni in bestimmten Städten
    switch (currentRegion.city.name) {
      case 'Funken-Siedlung':
        return { type: 'forging', bonus: 2.0 };  // Meister-Schmiede
      case 'Handelsfestung':
        return { type: 'trading', bonus: 1.5 };  // Handels-Bonus
      default:
        return { type: 'none', bonus: 1.0 };
    }
  }

  return { type: 'none', bonus: 1.0 };
}

// Beispiel: Harvesting System Integration
function harvestVegetation(position, radius = 2) {
  const removed = worldManager.removeVegetationAt(position, radius);

  if (removed > 0) {
    console.log(`✅ Harvested ${removed} vegetation items`);

    // Belohnung geben
    // givePlayerReward('wood', removed);

    return true;
  } else {
    console.log('❌ No vegetation to harvest');
    return false;
  }
}

// Beispiel: Replanting System
function replantTree(position) {
  const currentRegion = worldManager.getCurrentRegion();

  if (currentRegion) {
    // Pflanze Baum basierend auf Biome
    let treeType = 'tree';

    switch (currentRegion.biome) {
      case 'forest':
        treeType = 'tree';
        break;
      case 'coast':
        treeType = 'palm_tree';
        break;
      case 'ice':
        treeType = 'frozen_tree';
        break;
      case 'desert':
        treeType = 'cactus';
        break;
      default:
        treeType = 'tree';
    }

    const vegetation = worldManager.spawnVegetationAt(treeType, position);

    if (vegetation) {
      console.log(`🌱 Planted ${treeType}`);
      return true;
    }
  }

  return false;
}

// ============================================
// EXPORT FÜR GLOBALE NUTZUNG
// ============================================

window.worldManager = worldManager;  // Globaler Zugriff für Dev-Console
window.placeGarden = placeGarden;
window.canFishHere = canFishHere;
window.harvestVegetation = harvestVegetation;
window.replantTree = replantTree;
