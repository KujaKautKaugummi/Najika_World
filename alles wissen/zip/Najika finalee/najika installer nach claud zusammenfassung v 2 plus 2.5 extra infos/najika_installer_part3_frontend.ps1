# ═══════════════════════════════════════════════════════════════════
# 🌟 NAJIKA PROJECT - INSTALLER PART 3: FRONTEND
# ═══════════════════════════════════════════════════════════════════
# Version: 2.5
# Part: 3/5 - React Frontend, Three.js 3D Engine, Game UI
# ═══════════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🌟 NAJIKA PROJECT - INSTALLER PART 3/5" -ForegroundColor Magenta
Write-Host "Frontend (React, Three.js, Game Systems)" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "C:\Najika"
Set-Location $projectRoot

# ═══════════════════════════════════════════════════════════════════
# 1. CREATE REACT APP
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "⚛️  React Frontend erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (-not (Test-Path "frontend\package.json")) {
    Write-Host "📦 Erstelle React App..." -ForegroundColor Yellow
    npx create-react-app frontend
    Write-Host "✅ React App erstellt" -ForegroundColor Green
} else {
    Write-Host "✅ React App bereits vorhanden" -ForegroundColor Green
}

Set-Location "frontend"

# ═══════════════════════════════════════════════════════════════════
# 2. INSTALL FRONTEND DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📦 Frontend Dependencies installieren" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$frontendPackages = @(
    "three@0.160.0",
    "@react-three/fiber",
    "@react-three/drei",
    "axios",
    "socket.io-client",
    "framer-motion",
    "styled-components",
    "zustand",
    "react-router-dom"
)

Write-Host "📦 Installiere Pakete..." -ForegroundColor Yellow
npm install $frontendPackages --silent
Write-Host "✅ Dependencies installiert" -ForegroundColor Green

Set-Location $projectRoot
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 3. CREATE GAME SCENE (Three.js)
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎮 3D Game Scene erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$gameScene = @"
// Najika Game Scene - Three.js Setup
import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sky, Environment } from '@react-three/drei';
import * as THREE from 'three';

// Najika Character Model (Placeholder)
function NajikaModel() {
  const meshRef = useRef();
  
  useFrame((state, delta) => {
    meshRef.current.rotation.y += delta * 0.5;
  });

  return (
    <mesh ref={meshRef} position={[0, 1, 0]}>
      <capsuleGeometry args={[0.5, 1.5, 4, 8]} />
      <meshStandardMaterial color="#FF6B9D" />
    </mesh>
  );
}

// Main Game Scene
export default function GameScene() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Canvas
        camera={{ position: [0, 2, 5], fov: 60 }}
        shadows
      >
        <Sky sunPosition={[100, 20, 100]} />
        <ambientLight intensity={0.3} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1}
          castShadow
        />
        
        {/* Najika Character */}
        <NajikaModel />
        
        {/* Ground */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
          <planeGeometry args={[50, 50]} />
          <meshStandardMaterial color="#4CAF50" />
        </mesh>
        
        {/* Camera Controls */}
        <OrbitControls
          target={[0, 1, 0]}
          maxPolarAngle={Math.PI / 2}
          minDistance={2}
          maxDistance={10}
        />
        
        <Environment preset="sunset" />
      </Canvas>
    </div>
  );
}
"@

$sceneScript = Join-Path $projectRoot "frontend\src\game\GameScene.jsx"
$gameScene | Out-File -FilePath $sceneScript -Encoding UTF8
Write-Host "✅ Game Scene erstellt" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════════
# 4. CREATE COMBAT SYSTEM
# ═══════════════════════════════════════════════════════════════════

$combatSystem = @"
// Najika Combat System
export class CombatSystem {
  constructor() {
    this.player = {
      hp: 100,
      maxHp: 100,
      mana: 50,
      maxMana: 50,
      stamina: 100
    };
    
    this.combos = [];
    this.elements = ['fire', 'ice', 'lightning', 'shadow', 'light', 'nature'];
  }
  
  lightAttack() {
    this.combos.push('light');
    return { damage: 10, stamina: -5 };
  }
  
  heavyAttack() {
    this.combos.push('heavy');
    return { damage: 25, stamina: -15 };
  }
  
  parry() {
    return { success: Math.random() > 0.5, stamina: -10 };
  }
  
  dodge() {
    return { success: true, stamina: -20 };
  }
  
  weaveElements(element1, element2) {
    const combinations = {
      'fire_ice': 'steam',
      'fire_lightning': 'plasma',
      'ice_lightning': 'freeze',
      'shadow_light': 'chaos',
      'fire_nature': 'wildfire',
      'ice_nature': 'blizzard'
    };
    
    const key = [element1, element2].sort().join('_');
    return combinations[key] || 'basic';
  }
}
"@

$combatScript = Join-Path $projectRoot "frontend\src\game\CombatSystem.js"
$combatSystem | Out-File -FilePath $combatScript -Encoding UTF8
Write-Host "✅ Combat System erstellt" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════════
# 5. CREATE UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════

$hudComponent = @"
// Najika HUD Component
import React from 'react';
import styled from 'styled-components';

const HudContainer = styled.div``
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1000;
``;

const HealthBar = styled.div``
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 300px;
  height: 30px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 15px;
  overflow: hidden;
  pointer-events: auto;
``;

const HealthFill = styled.div``
  height: 100%;
  background: linear-gradient(90deg, #e74c3c, #c0392b);
  width: \$\{props => props.percent}%;
  transition: width 0.3s ease;
``;

const NeedsPanel = styled.div``
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  padding: 15px;
  border-radius: 10px;
  color: white;
``;

export default function HUD({ player, needs }) {
  return (
    <HudContainer>
      <HealthBar>
        <HealthFill percent={(player.hp / player.maxHp) * 100} />
      </HealthBar>
      
      <NeedsPanel>
        <div>Hunger: {needs.hunger}%</div>
        <div>Thirst: {needs.thirst}%</div>
        <div>Energy: {needs.energy}%</div>
        <div>Social: {needs.social}%</div>
        <div>Joy: {needs.joy}%</div>
      </NeedsPanel>
    </HudContainer>
  );
}
"@

$hudScript = Join-Path $projectRoot "frontend\src\ui\HUD.jsx"
$hudComponent | Out-File -FilePath $hudScript -Encoding UTF8
Write-Host "✅ HUD Component erstellt" -ForegroundColor Green

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 6. CREATE MAIN APP
# ═══════════════════════════════════════════════════════════════════

$appComponent = @"
import React, { useState } from 'react';
import GameScene from './game/GameScene';
import HUD from './ui/HUD';
import './App.css';

function App() {
  const [player, setPlayer] = useState({
    hp: 100,
    maxHp: 100,
    mana: 50,
    maxMana: 50
  });
  
  const [needs, setNeeds] = useState({
    hunger: 80,
    thirst: 70,
    energy: 60,
    social: 90,
    joy: 85
  });

  return (
    <div className="App">
      <GameScene />
      <HUD player={player} needs={needs} />
      
      <div style={{
        position: 'fixed',
        bottom: 20,
        right: 20,
        background: 'rgba(0,0,0,0.8)',
        color: 'white',
        padding: '15px',
        borderRadius: '10px',
        zIndex: 1001
      }}>
        <h3>🌟 Najika v2.5</h3>
        <p>Frontend läuft!</p>
        <button onClick={() => alert('EXPLOSION! 💥')}>
          Test Najika
        </button>
      </div>
    </div>
  );
}

export default App;
"@

$appScript = Join-Path $projectRoot "frontend\src\App.js"
$appComponent | Out-File -FilePath $appScript -Encoding UTF8
Write-Host "✅ Main App erstellt" -ForegroundColor Green

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 7. CREATE START SCRIPT
# ═══════════════════════════════════════════════════════════════════

$startFrontend = @"
@echo off
echo ════════════════════════════════════════════
echo 🌟 Starting Najika Frontend...
echo ════════════════════════════════════════════
echo.
echo Opening: http://localhost:3000
echo.

cd /d "%~dp0\frontend"
start http://localhost:3000
npm start

pause
"@

$startFrontendPath = Join-Path $projectRoot "start_frontend.bat"
$startFrontend | Out-File -FilePath $startFrontendPath -Encoding ASCII
Write-Host "✅ start_frontend.bat erstellt" -ForegroundColor Green

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# PART 3 SUMMARY
# ═══════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ PART 3 ABGESCHLOSSEN!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Installiert:" -ForegroundColor Yellow
Write-Host "   ✅ React Frontend" -ForegroundColor Green
Write-Host "   ✅ Three.js 3D Engine" -ForegroundColor Green
Write-Host "   ✅ Game Components" -ForegroundColor Green
Write-Host "   ✅ UI System (HUD, Needs)" -ForegroundColor Green
Write-Host ""

Write-Host "📁 Erstellt:" -ForegroundColor Yellow
Write-Host "   ✅ GameScene (3D)" -ForegroundColor Green
Write-Host "   ✅ CombatSystem" -ForegroundColor Green
Write-Host "   ✅ HUD Component" -ForegroundColor Green
Write-Host "   ✅ Main App" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📌 FRONTEND TESTEN:" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starte Frontend:" -ForegroundColor Yellow
Write-Host "   .\start_frontend.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "Öffnet automatisch: http://localhost:3000" -ForegroundColor Gray
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📌 NÄCHSTER SCHRITT:" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Führe jetzt aus:" -ForegroundColor Yellow
Write-Host "   .\najika_installer_part4_mobile.ps1" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
pause
