// Najika World App - Main Game Controller
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import OpenWorldScene from './OpenWorldScene';
import InteriorScene from './InteriorScene';
import GameScene from './GameScene_Battle'; // Battle System (complete from NajikaFinal)

// Import building -> room mapping
const worldConfig = require('../assets/open_world_config.json');
const roomConfig = require('../assets/room_config_detailed.json');

export default function NajikaWorldApp() {
  const [gameMode, setGameMode] = useState('world'); // 'world', 'interior', 'battle'
  const [currentLocation, setCurrentLocation] = useState(null);
  const [currentRoom, setCurrentRoom] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking...');

  useEffect(() => {
    // Check backend connection
    axios.get('http://localhost:8000/health')
      .then(response => {
        setBackendStatus('Connected ✅');
        console.log('Backend:', response.data);
      })
      .catch(error => {
        setBackendStatus('Disconnected ❌');
        console.error('Backend error:', error);
      });
  }, []);

  const handleEnterBuilding = (building) => {
    console.log('Entering building:', building);
    setCurrentLocation(building);

    // Map building to room
    if (building.id === 'schwarze_muehle') {
      // Show room selector or enter first room
      setCurrentRoom('Wohnzimmer');
      setGameMode('interior');
    } else if (building.id === 'kampfarena') {
      // Enter battle mode
      setGameMode('battle');
    } else if (building.id === 'garten') {
      setCurrentRoom('Garten');
      setGameMode('interior');
    } else if (building.id.startsWith('dungeon_')) {
      // Enter dungeon (battle mode with specific difficulty)
      setGameMode('battle');
    }
  };

  const handleExitToWorld = () => {
    setGameMode('world');
    setCurrentLocation(null);
    setCurrentRoom(null);
  };

  const handleRoomChange = (roomName) => {
    setCurrentRoom(roomName);
  };

  // Render appropriate scene based on game mode
  if (gameMode === 'world') {
    return (
      <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
        {/* Backend Status Badge */}
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          zIndex: 200,
          background: 'rgba(0,0,0,0.8)',
          padding: '15px 20px',
          borderRadius: '10px',
          color: 'white',
          fontFamily: 'monospace',
          fontSize: '12px',
          border: '2px solid #FF6B9D'
        }}>
          <div style={{ color: '#FF6B9D', fontWeight: 'bold', marginBottom: '5px' }}>
            🌟 NAJIKA WORLD V1.0
          </div>
          <div>Backend: {backendStatus}</div>
          <div>Mode: Open World 🗺️</div>
        </div>

        <OpenWorldScene onEnterBuilding={handleEnterBuilding} />
      </div>
    );
  }

  if (gameMode === 'interior') {
    return (
      <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
        {/* Backend Status */}
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          zIndex: 200,
          background: 'rgba(0,0,0,0.8)',
          padding: '15px 20px',
          borderRadius: '10px',
          color: 'white',
          fontFamily: 'monospace',
          fontSize: '12px',
          border: '2px solid #FF6B9D'
        }}>
          <div style={{ color: '#FF6B9D', fontWeight: 'bold', marginBottom: '5px' }}>
            🌟 NAJIKA WORLD V1.0
          </div>
          <div>Backend: {backendStatus}</div>
          <div>Mode: Interior 🏠</div>
          <div>Location: {currentLocation?.name || 'Unknown'}</div>
        </div>

        {/* Room Selector (if in Schwarze Mühle) */}
        {currentLocation?.id === 'schwarze_muehle' && (
          <div style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            zIndex: 200,
            background: 'rgba(0,0,0,0.8)',
            padding: '15px',
            borderRadius: '10px',
            color: 'white',
            fontFamily: 'monospace',
            fontSize: '12px',
            maxWidth: '200px'
          }}>
            <div style={{ fontWeight: 'bold', marginBottom: '10px', color: '#FF6B9D' }}>
              🏰 Schwarze Mühle
            </div>
            <div style={{ fontSize: '11px', color: '#aaa', marginBottom: '10px' }}>
              Stockwerke:
            </div>
            {roomConfig.rooms
              .filter(room => [
                'Wohnzimmer', 'Küche', 'Badezimmer',
                'Schlafzimmer', 'Musikraum', 'Medizin',
                'Terminal', 'Studieren & Crafting', 'Trainingszimmer'
              ].includes(room.name))
              .map(room => (
                <button
                  key={room.name}
                  onClick={() => handleRoomChange(room.name)}
                  style={{
                    display: 'block',
                    width: '100%',
                    marginBottom: '5px',
                    padding: '8px',
                    background: currentRoom === room.name ? '#FF6B9D' : '#444',
                    border: 'none',
                    color: 'white',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    fontSize: '11px'
                  }}
                >
                  {room.name}
                </button>
              ))
            }
          </div>
        )}

        <InteriorScene roomName={currentRoom} onExit={handleExitToWorld} />
      </div>
    );
  }

  if (gameMode === 'battle') {
    return (
      <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
        {/* Backend Status */}
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          zIndex: 200,
          background: 'rgba(0,0,0,0.8)',
          padding: '15px 20px',
          borderRadius: '10px',
          color: 'white',
          fontFamily: 'monospace',
          fontSize: '12px',
          border: '2px solid #FF6B9D'
        }}>
          <div style={{ color: '#FF6B9D', fontWeight: 'bold', marginBottom: '5px' }}>
            🌟 NAJIKA WORLD V1.0
          </div>
          <div>Backend: {backendStatus}</div>
          <div>Mode: Battle ⚔️</div>
          <div>Location: {currentLocation?.name || 'Unknown'}</div>
        </div>

        {/* Exit Battle button */}
        <div style={{
          position: 'absolute',
          bottom: '30px',
          right: '30px',
          zIndex: 200
        }}>
          <button
            onClick={handleExitToWorld}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              fontWeight: 'bold',
              background: 'linear-gradient(135deg, #666, #333)',
              color: 'white',
              border: '2px solid white',
              borderRadius: '8px',
              cursor: 'pointer',
              boxShadow: '0 4px 8px rgba(0,0,0,0.5)'
            }}
          >
            ← Exit to World
          </button>
        </div>

        <GameScene />
      </div>
    );
  }

  return null;
}
