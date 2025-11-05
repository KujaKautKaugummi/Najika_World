// Najika Interior Scene - Room Viewer with room_config_detailed.json
import React, { useRef, useEffect, useState, Suspense } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

// Import room config
const roomConfigData = require('../assets/room_config_detailed.json');

// Floor Component
function RoomFloor({ roomData }) {
  if (!roomData || !roomData.floor) return null;

  return (
    <mesh
      rotation={[-Math.PI / 2, 0, 0]}
      position={[0, 0, 0]}
      receiveShadow
    >
      <planeGeometry args={[roomData.floor.span || 48, roomData.floor.span || 48]} />
      <meshStandardMaterial
        color={roomData.floor.tint || "#7a5c3d"}
        roughness={roomData.floor.roughness || 0.75}
        metalness={roomData.floor.metalness || 0.02}
      />
    </mesh>
  );
}

// Walls Component
function RoomWalls({ roomData }) {
  if (!roomData || !roomData.walls) return null;

  const span = roomData.floor?.span || 48;
  const height = roomData.wallHeight || 6;
  const wallColor = roomData.walls.tint || "#4c2f35";

  return (
    <group>
      {/* North Wall */}
      <mesh position={[0, height / 2, -span / 2]} receiveShadow castShadow>
        <boxGeometry args={[span, height, 2]} />
        <meshStandardMaterial color={wallColor} />
      </mesh>

      {/* South Wall */}
      <mesh position={[0, height / 2, span / 2]} receiveShadow castShadow>
        <boxGeometry args={[span, height, 2]} />
        <meshStandardMaterial color={wallColor} />
      </mesh>

      {/* East Wall */}
      <mesh position={[span / 2, height / 2, 0]} receiveShadow castShadow>
        <boxGeometry args={[2, height, span]} />
        <meshStandardMaterial color={wallColor} />
      </mesh>

      {/* West Wall */}
      <mesh position={[-span / 2, height / 2, 0]} receiveShadow castShadow>
        <boxGeometry args={[2, height, span]} />
        <meshStandardMaterial color={wallColor} />
      </mesh>
    </group>
  );
}

// Props Component - Furniture and decorations
function RoomProps({ roomData }) {
  if (!roomData || !roomData.props || roomData.props.length === 0) return null;

  return (
    <group>
      {roomData.props.map((prop, index) => (
        <mesh
          key={index}
          position={prop.position || [0, 0, 0]}
          rotation={prop.rotation || [0, 0, 0]}
          scale={prop.scale || 1}
          castShadow
          receiveShadow
        >
          {/* Placeholder cube - will load actual model */}
          <boxGeometry args={[2, 2, 2]} />
          <meshStandardMaterial color="#8b4513" />
        </mesh>
      ))}
    </group>
  );
}

// Character in room
function RoomCharacter({ onExit }) {
  const characterRef = useRef();
  const [position, setPosition] = useState(new THREE.Vector3(0, 0, 15));
  const [rotation, setRotation] = useState(0);

  const keys = useRef({
    forward: false,
    backward: false,
    left: false,
    right: false
  });

  useEffect(() => {
    const handleKeyDown = (e) => {
      switch(e.code) {
        case 'KeyW': keys.current.forward = true; break;
        case 'KeyS': keys.current.backward = true; break;
        case 'KeyA': keys.current.left = true; break;
        case 'KeyD': keys.current.right = true; break;
        case 'KeyE':
          // Check if near door (position z > 20)
          if (position.z > 20) {
            onExit();
          }
          break;
      }
    };

    const handleKeyUp = (e) => {
      switch(e.code) {
        case 'KeyW': keys.current.forward = false; break;
        case 'KeyS': keys.current.backward = false; break;
        case 'KeyA': keys.current.left = false; break;
        case 'KeyD': keys.current.right = false; break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [position, onExit]);

  useFrame((state, delta) => {
    if (!characterRef.current) return;

    const speed = 5 * delta;
    const moveX = (keys.current.right ? 1 : 0) - (keys.current.left ? 1 : 0);
    const moveZ = (keys.current.backward ? 1 : 0) - (keys.current.forward ? 1 : 0);

    if (moveX !== 0 || moveZ !== 0) {
      const newPos = position.clone();
      newPos.x += moveX * speed;
      newPos.z += moveZ * speed;

      // Boundary check (room size)
      newPos.x = Math.max(-20, Math.min(20, newPos.x));
      newPos.z = Math.max(-20, Math.min(25, newPos.z));

      setPosition(newPos);

      const angle = Math.atan2(moveX, moveZ);
      setRotation(angle);
    }

    characterRef.current.position.copy(position);
    characterRef.current.rotation.y = rotation;
  });

  return (
    <mesh ref={characterRef} position={position} castShadow>
      <capsuleGeometry args={[0.5, 1.5, 4, 8]} />
      <meshStandardMaterial color="#ff6b9d" />
    </mesh>
  );
}

// Main Interior Scene
export default function InteriorScene({ roomName, onExit }) {
  const [roomData, setRoomData] = useState(null);

  useEffect(() => {
    // Find room in config
    const room = roomConfigData.rooms.find(r => r.name === roomName);
    if (room) {
      setRoomData(room);
    }
  }, [roomName]);

  if (!roomData) {
    return (
      <div style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#000',
        color: '#fff',
        fontSize: '24px'
      }}>
        Loading {roomName}...
      </div>
    );
  }

  const palette = roomData.palette || {};

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      {/* Room Info */}
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        background: 'rgba(0,0,0,0.7)',
        color: palette.primary || '#ff9b71',
        padding: '15px',
        borderRadius: '10px',
        fontFamily: 'monospace',
        fontSize: '14px',
        zIndex: 100
      }}>
        <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '10px' }}>
          🏠 {roomData.name}
        </div>
        <div>WASD - Move</div>
        <div>E - Exit (near door)</div>
      </div>

      {/* Exit button */}
      <div style={{
        position: 'absolute',
        bottom: '30px',
        right: '30px',
        zIndex: 100
      }}>
        <button
          onClick={onExit}
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

      {/* 3D Canvas */}
      <Canvas
        shadows
        camera={{ position: [0, 8, 25], fov: 60 }}
        style={{ background: palette.background || '#231419' }}
      >
        <Suspense fallback={null}>
          {/* Lighting */}
          <ambientLight intensity={palette.ambient || 0.45} />
          <directionalLight
            position={[10, 15, 10]}
            intensity={0.8}
            castShadow
            shadow-mapSize={[1024, 1024]}
          />
          <pointLight
            position={[0, 5, 0]}
            intensity={0.5}
            color={palette.primary || "#ff9b71"}
          />

          {/* Fog */}
          <fog attach="fog" args={[palette.fog || '#1a1013', 30, 80]} />

          {/* Floor */}
          <RoomFloor roomData={roomData} />

          {/* Walls */}
          <RoomWalls roomData={roomData} />

          {/* Props/Furniture */}
          <RoomProps roomData={roomData} />

          {/* Character */}
          <RoomCharacter onExit={onExit} />

          {/* Door indicator */}
          <mesh position={[0, 1.5, 23]} castShadow>
            <boxGeometry args={[4, 3, 0.5]} />
            <meshStandardMaterial color="#4a2511" emissive="#ff6b9d" emissiveIntensity={0.2} />
          </mesh>
        </Suspense>
      </Canvas>
    </div>
  );
}
