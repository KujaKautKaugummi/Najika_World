# ═══════════════════════════════════════════════════════════════════
# 🌟 NAJIKA PROJECT - INSTALLER PART 4: MOBILE & PWA
# ═══════════════════════════════════════════════════════════════════
# Version: 2.5
# Part: 4/5 - Mobile PWA, Touch Controls, Digivice Interface
# ═══════════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🌟 NAJIKA PROJECT - INSTALLER PART 4/5" -ForegroundColor Magenta
Write-Host "Mobile & PWA (Touch Controls, Digivice UI)" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "C:\Najika"
Set-Location $projectRoot

# ═══════════════════════════════════════════════════════════════════
# 1. INSTALL PWA DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📱 PWA Dependencies installieren" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Set-Location "frontend"
npm install workbox-webpack-plugin react-device-detect --silent
Set-Location $projectRoot

Write-Host "✅ PWA Pakete installiert" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 2. CREATE PWA MANIFEST
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📱 PWA Manifest erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$manifest = @"
{
  "short_name": "Najika",
  "name": "Najika - Your AI Companion",
  "description": "Najika: Deine persönliche KI-Begleiterin & Action-RPG",
  "icons": [
    {
      "src": "najika-icon-192.png",
      "type": "image/png",
      "sizes": "192x192",
      "purpose": "any maskable"
    },
    {
      "src": "najika-icon-512.png",
      "type": "image/png",
      "sizes": "512x512",
      "purpose": "any maskable"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#FF6B9D",
  "background_color": "#1a1a2e",
  "orientation": "portrait"
}
"@

$manifestPath = Join-Path $projectRoot "frontend\public\manifest.json"
$manifest | Out-File -FilePath $manifestPath -Encoding UTF8
Write-Host "✅ manifest.json erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 3. CREATE TOUCH CONTROLS
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎮 Touch Controls erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$touchControls = @"
// Najika Touch Controls
import React, { useRef, useState } from 'react';
import styled from 'styled-components';

const ControlsContainer = styled.div``
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2000;
``;

const VirtualJoystick = styled.div``
  position: absolute;
  bottom: 30px;
  left: 30px;
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  pointer-events: auto;
``;

const JoystickHandle = styled.div``
  position: absolute;
  width: 50px;
  height: 50px;
  background: rgba(255, 107, 157, 0.8);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translate(\$\{props => props.x}px, \$\{props => props.y}px);
  transition: transform 0.1s ease;
``;

const ActionButtons = styled.div``
  position: absolute;
  bottom: 30px;
  right: 30px;
  display: flex;
  gap: 15px;
  pointer-events: auto;
``;

const ActionButton = styled.button``
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 107, 157, 0.3);
  color: white;
  font-size: 20px;
  cursor: pointer;
  backdrop-filter: blur(5px);
  
  &:active {
    background: rgba(255, 107, 157, 0.8);
    transform: scale(0.95);
  }
``;

const WeavePad = styled.div``
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  display: grid;
  grid-template-columns: repeat(2, 50px);
  grid-template-rows: repeat(3, 50px);
  gap: 10px;
  pointer-events: auto;
``;

const ElementButton = styled.button``
  width: 50px;
  height: 50px;
  border-radius: 10px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: \$\{props => props.color};
  color: white;
  font-size: 12px;
  cursor: pointer;
  
  &:active {
    transform: scale(0.9);
  }
``;

export default function TouchControls({ onAction }) {
  const [joystickPos, setJoystickPos] = useState({ x: 0, y: 0 });
  
  const elements = [
    { name: 'Fire', color: '#FF4444' },
    { name: 'Ice', color: '#44AAFF' },
    { name: 'Light', color: '#FFFF44' },
    { name: 'Shad', color: '#444444' },
    { name: 'Nature', color: '#44FF44' },
    { name: 'Lightning', color: '#AA44FF' }
  ];
  
  return (
    <ControlsContainer>
      {/* Virtual Joystick */}
      <VirtualJoystick>
        <JoystickHandle x={joystickPos.x} y={joystickPos.y} />
      </VirtualJoystick>
      
      {/* Action Buttons */}
      <ActionButtons>
        <ActionButton onClick={() => onAction('light')}>⚔️</ActionButton>
        <ActionButton onClick={() => onAction('heavy')}>🔨</ActionButton>
        <ActionButton onClick={() => onAction('dodge')}>🏃</ActionButton>
      </ActionButtons>
      
      {/* Element Weave Pad */}
      <WeavePad>
        {elements.map((el, i) => (
          <ElementButton
            key={i}
            color={el.color}
            onClick={() => onAction('weave', el.name)}
          >
            {el.name}
          </ElementButton>
        ))}
      </WeavePad>
    </ControlsContainer>
  );
}
"@

$touchScript = Join-Path $projectRoot "frontend\src\ui\TouchControls.jsx"
$touchControls | Out-File -FilePath $touchScript -Encoding UTF8
Write-Host "✅ Touch Controls erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 4. CREATE DIGIVICE INTERFACE
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📟 Digivice Interface erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$digivice = @"
// Najika Digivice Interface (Tamagotchi-Style)
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const DigiviceContainer = styled.div``
  width: 300px;
  height: 400px;
  background: linear-gradient(145deg, #FF6B9D, #C44569);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  position: relative;
``;

const Screen = styled.div``
  width: 100%;
  height: 200px;
  background: #1a1a2e;
  border-radius: 10px;
  padding: 10px;
  color: #00ff00;
  font-family: 'Courier New', monospace;
  overflow-y: auto;
``;

const NeedsDisplay = styled.div``
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
``;

const NeedBar = styled.div``
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: white;
``;

const BarFill = styled.div``
  flex: 1;
  height: 15px;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  overflow: hidden;
  
  &::after {
    content: '';
    display: block;
    width: \$\{props => props.percent}%;
    height: 100%;
    background: \$\{props => props.color};
    transition: width 0.3s ease;
  }
``;

const ActionButtons = styled.div``
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 15px;
``;

const Button = styled.button``
  padding: 10px;
  background: rgba(255,255,255,0.2);
  border: 2px solid rgba(255,255,255,0.5);
  border-radius: 10px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  
  &:active {
    transform: scale(0.95);
    background: rgba(255,255,255,0.4);
  }
``;

export default function DigiviceInterface() {
  const [needs, setNeeds] = useState({
    hunger: 80,
    thirst: 70,
    energy: 60,
    social: 90,
    joy: 85
  });
  
  const [messages, setMessages] = useState([
    'Najika: Kuja! Du bist da! 💥',
    'System: Digivice aktiviert'
  ]);
  
  const addMessage = (msg) => {
    setMessages(prev => [...prev, msg].slice(-10));
  };
  
  const feed = () => {
    setNeeds(prev => ({ ...prev, hunger: Math.min(100, prev.hunger + 20) }));
    addMessage('Najika: Danke fürs Füttern! 😋');
  };
  
  const play = () => {
    setNeeds(prev => ({ ...prev, joy: Math.min(100, prev.joy + 15) }));
    addMessage('Najika: Juhu! Spielzeit! 🎉');
  };
  
  return (
    <DigiviceContainer>
      <Screen>
        {messages.map((msg, i) => (
          <div key={i}>&gt; {msg}</div>
        ))}
      </Screen>
      
      <NeedsDisplay>
        <NeedBar>
          🍖 <BarFill percent={needs.hunger} color="#FF6B6B" />
        </NeedBar>
        <NeedBar>
          💧 <BarFill percent={needs.thirst} color="#4ECDC4" />
        </NeedBar>
        <NeedBar>
          ⚡ <BarFill percent={needs.energy} color="#FFE66D" />
        </NeedBar>
        <NeedBar>
          👥 <BarFill percent={needs.social} color="#95E1D3" />
        </NeedBar>
        <NeedBar>
          😊 <BarFill percent={needs.joy} color="#FF6B9D" />
        </NeedBar>
      </NeedsDisplay>
      
      <ActionButtons>
        <Button onClick={feed}>🍖 Feed</Button>
        <Button onClick={play}>🎮 Play</Button>
        <Button onClick={() => addMessage('Najika: Zzz... 😴')}>
          💤 Sleep
        </Button>
        <Button onClick={() => addMessage('Najika: Kuja! 💕')}>
          💬 Talk
        </Button>
        <Button>🎯 Train</Button>
        <Button>📊 Stats</Button>
      </ActionButtons>
    </DigiviceContainer>
  );
}
"@

$digiviceScript = Join-Path $projectRoot "frontend\src\ui\DigiviceInterface.jsx"
$digivice | Out-File -FilePath $digiviceScript -Encoding UTF8
Write-Host "✅ Digivice Interface erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 5. CREATE SERVICE WORKER
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "⚙️  Service Worker erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$serviceWorker = @"
// Najika Service Worker
const CACHE_NAME = 'najika-v2.5';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
"@

$swPath = Join-Path $projectRoot "frontend\public\service-worker.js"
$serviceWorker | Out-File -FilePath $swPath -Encoding UTF8
Write-Host "✅ Service Worker erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 6. CREATE MOBILE README
# ═══════════════════════════════════════════════════════════════════

$mobileReadme = @"
# 📱 Najika Mobile / PWA

## Installation auf Smartphone

### Android:
1. Öffne Chrome Browser
2. Gehe zu http://[deine-ip]:3000
3. Tippe auf Menü (⋮)
4. Wähle "Zum Startbildschirm hinzufügen"
5. Bestätige mit "Hinzufügen"

### iOS:
1. Öffne Safari Browser
2. Gehe zu http://[deine-ip]:3000
3. Tippe auf Teilen-Button (□↑)
4. Wähle "Zum Home-Bildschirm"
5. Bestätige mit "Hinzufügen"

## Touch Controls

- **Joystick (links unten)**: Bewegung
- **Action Buttons (rechts unten)**: Angriffe
- **Element Pad (rechts mitte)**: Magie-Weaving
- **Swipe Gesten**:
  - Swipe Up: Block
  - Swipe Down: Dodge
  - Double Tap: Lock-On

## Digivice Modus

Wechsle in den Tamagotchi-Style Digivice Modus für:
- Najika füttern
- Mit ihr spielen
- Bedürfnisse überwachen
- Schnelle Interaktion

## Offline-Nutzung

Die PWA funktioniert teilweise offline:
- UI bleibt verfügbar
- Gespeicherte Daten bleiben
- Backend-Features erfordern Verbindung

## Cloudflare Tunnel (Empfohlen)

Für sicheren Zugriff von überall:

``bash
cloudflared tunnel --url http://localhost:3000
``

Nutze die generierte URL auf jedem Gerät!
"@

$mobileReadmePath = Join-Path $projectRoot "mobile\README.md"
$mobileReadme | Out-File -FilePath $mobileReadmePath -Encoding UTF8
Write-Host "✅ Mobile README erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# PART 4 SUMMARY
# ═══════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ PART 4 ABGESCHLOSSEN!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Erstellt:" -ForegroundColor Yellow
Write-Host "   ✅ PWA Manifest" -ForegroundColor Green
Write-Host "   ✅ Service Worker" -ForegroundColor Green
Write-Host "   ✅ Touch Controls" -ForegroundColor Green
Write-Host "   ✅ Virtual Joystick" -ForegroundColor Green
Write-Host "   ✅ Digivice Interface" -ForegroundColor Green
Write-Host "   ✅ Mobile README" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📱 MOBILE ZUGRIFF:" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lokales Netzwerk:" -ForegroundColor Yellow
Write-Host "   http://[deine-pc-ip]:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Mit Cloudflare Tunnel (sicher):" -ForegroundColor Yellow
Write-Host "   cloudflared tunnel --url http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📌 NÄCHSTER SCHRITT:" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Führe jetzt aus:" -ForegroundColor Yellow
Write-Host "   .\najika_installer_part5_finalize.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Das macht:" -ForegroundColor Yellow
Write-Host "   - Integration aller Systeme" -ForegroundColor Gray
Write-Host "   - Finale Konfiguration" -ForegroundColor Gray
Write-Host "   - Dokumentation" -ForegroundColor Gray
Write-Host "   - Start-Skripte" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
pause
