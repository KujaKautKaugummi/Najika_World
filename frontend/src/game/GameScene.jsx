// Najika Game Scene - Three.js Setup with Combat System
import React, { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Sky, Environment, KeyboardControls } from '@react-three/drei';
import * as THREE from 'three';

// Import combat systems
import { CombatSystem } from './CombatSystem';
import { CheerSystem } from './CheerSystem';
import { CameraController } from './CameraController';
import { CommandSystem } from './CommandSystem';
import { battleAPI } from './BattleAPI';
import { FinisherQTE } from './FinisherQTE';

// Najika Character Model (Placeholder - will be replaced with proper model)
function NajikaModel({ position, rotation, combatSystem, cheerSystem, cameraMode }) {
  const meshRef = useRef();
  const [najikaState, setNajikaState] = useState('idle');

  useFrame((state, delta) => {
    if (!meshRef.current) return;

    // Update Najika's animation based on state
    if (cameraMode === 'orbit') {
      // Autonomous movement in cheer mode
      // Simulate combat states for cheer timing
      const now = Date.now();
      const cycle = (now % 3000) / 3000; // 3s cycle

      if (cycle < 0.2) {
        setNajikaState('attacking');
        cheerSystem.updateNajikaState('attacking');
      } else if (cycle < 0.4) {
        setNajikaState('recovering');
        cheerSystem.updateNajikaState('recovering');
      } else if (cycle < 0.6) {
        setNajikaState('dodging');
        cheerSystem.updateNajikaState('dodging');
      } else {
        setNajikaState('idle');
        cheerSystem.updateNajikaState('idle');
      }

      // Rotate slowly
      meshRef.current.rotation.y += delta * 0.5;
    } else {
      // Player controlled in action mode
      meshRef.current.position.copy(position);
      meshRef.current.rotation.y = rotation;
    }

    // Update combat system
    combatSystem.update(delta);
    cheerSystem.update(delta);
  });

  return (
    <mesh ref={meshRef} position={[position.x, position.y + 0.75, position.z]} castShadow>
      <capsuleGeometry args={[0.5, 1.5, 4, 8]} />
      <meshStandardMaterial color="#FF6B9D" />

      {/* Visual indicator for Najika's state */}
      {najikaState === 'attacking' && (
        <mesh position={[0, 2, 0]}>
          <sphereGeometry args={[0.2, 8, 8]} />
          <meshBasicMaterial color="#FF0000" />
        </mesh>
      )}

      {najikaState === 'dodging' && (
        <mesh position={[0, 2, 0]}>
          <sphereGeometry args={[0.2, 8, 8]} />
          <meshBasicMaterial color="#00FF00" />
        </mesh>
      )}
    </mesh>
  );
}

// Combat UI Overlay
function CombatUI({ combatSystem, cheerSystem, commandSystem, cameraMode, onCheer, onCameraSwitch, onCommand, onPraise, onScold, onOverrideToggle, onStartBattle }) {
  const [stats, setStats] = useState(combatSystem.getStats());
  const [cheerData, setCheerData] = useState(cheerSystem.getUIData());
  const [commandStats, setCommandStats] = useState(commandSystem.getStats());
  const [availableCommands, setAvailableCommands] = useState(commandSystem.getAvailableCommands());

  useEffect(() => {
    const interval = setInterval(() => {
      setStats(combatSystem.getStats());
      setCheerData(cheerSystem.getUIData());
      setCommandStats(commandSystem.getStats());
      setAvailableCommands(commandSystem.getAvailableCommands());
    }, 100);

    return () => clearInterval(interval);
  }, [combatSystem, cheerSystem, commandSystem]);

  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      color: 'white',
      fontFamily: 'Arial',
      padding: '20px'
    }}>
      {/* Battle Status & Start Button */}
      <div style={{ marginBottom: '15px', display: 'flex', gap: '10px', alignItems: 'center' }}>
        <button
          onClick={onStartBattle}
          style={{
            padding: '10px 20px',
            fontSize: '14px',
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #FF6B9D, #FF1744)',
            color: 'white',
            border: '3px solid white',
            borderRadius: '8px',
            cursor: 'pointer',
            pointerEvents: 'auto',
            boxShadow: '0 4px 8px rgba(0,0,0,0.5)',
            transition: 'all 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
          ⚔️ START BATTLE
        </button>
      </div>

      {/* HP Bar */}
      <div style={{ marginBottom: '10px' }}>
        <div style={{ fontSize: '14px', marginBottom: '5px' }}>HP: {stats.hp}/{stats.maxHp}</div>
        <div style={{
          width: '300px',
          height: '20px',
          background: '#333',
          border: '2px solid white',
          borderRadius: '10px',
          overflow: 'hidden'
        }}>
          <div style={{
            width: `${(stats.hp / stats.maxHp) * 100}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #FF6B9D, #FF1744)',
            transition: 'width 0.3s'
          }} />
        </div>
      </div>

      {/* Stamina Bar */}
      <div style={{ marginBottom: '10px' }}>
        <div style={{ fontSize: '14px', marginBottom: '5px' }}>Stamina: {Math.floor(stats.stamina)}/100</div>
        <div style={{
          width: '300px',
          height: '15px',
          background: '#333',
          border: '2px solid white',
          borderRadius: '10px',
          overflow: 'hidden'
        }}>
          <div style={{
            width: `${stats.stamina}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #76FF03, #CDDC39)',
            transition: 'width 0.1s'
          }} />
        </div>
      </div>

      {/* Evolution Stage & Stats - Top Left */}
      {cameraMode === 'orbit' && (
        <div style={{
          position: 'absolute',
          top: '80px',
          left: '20px',
          padding: '10px',
          background: commandStats.overrideMode ? 'rgba(255, 69, 0, 0.9)' : 'rgba(76, 175, 80, 0.9)',
          borderRadius: '8px',
          border: '2px solid white',
          fontSize: '11px'
        }}>
          <div style={{ fontWeight: 'bold' }}>
            {commandStats.overrideMode ? '⚠️ DIRECT MODE' : `STUFE: ${commandStats.evolutionStage.toUpperCase()}`}
          </div>
          <div style={{ fontSize: '9px', marginTop: '3px' }}>
            XP: {commandStats.battleXP} / {commandStats.nextStageXP || '∞'}
          </div>
        </div>
      )}

      {/* Relationship Stats - Top Right */}
      {cameraMode === 'orbit' && (
        <div style={{
          position: 'absolute',
          top: '80px',
          right: '20px',
          padding: '8px',
          background: 'rgba(0,0,0,0.8)',
          borderRadius: '8px',
          border: '2px solid white',
          fontSize: '10px'
        }}>
          <div style={{ fontWeight: 'bold', marginBottom: '3px' }}>BEZIEHUNG:</div>
          <div>😊 {commandStats.happiness}%</div>
          <div>💪 {commandStats.discipline}%</div>
          <div>❤️ {commandStats.trust}%</div>
          <div>⭐ {commandStats.synergy}%</div>
        </div>
      )}

      {/* Command Buttons - Bottom Center (Digimon World 1 Style) */}
      {cameraMode === 'orbit' && (
        <div style={{
          position: 'absolute',
          bottom: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '15px',
          alignItems: 'flex-end'
        }}>
          {/* Main Commands - Circular Buttons */}
          {availableCommands.commands.map((cmd) => (
            <div key={cmd.key} style={{ textAlign: 'center' }}>
              {/* Speech Bubble Tooltip */}
              <div style={{
                background: 'rgba(0, 0, 0, 0.85)',
                color: 'white',
                padding: '5px 10px',
                borderRadius: '12px',
                border: '2px solid white',
                fontSize: '10px',
                marginBottom: '5px',
                whiteSpace: 'nowrap',
                pointerEvents: 'none'
              }}>
                {cmd.label}
              </div>

              {/* Circular Button */}
              <button
                onClick={() => onCommand(cmd.key)}
                disabled={!commandStats.canCommand}
                style={{
                  width: '70px',
                  height: '70px',
                  borderRadius: '50%',
                  fontSize: '28px',
                  background: commandStats.canCommand
                    ? 'radial-gradient(circle, #4CAF50, #2E7D32)'
                    : 'radial-gradient(circle, #666, #333)',
                  color: 'white',
                  border: '3px solid white',
                  cursor: commandStats.canCommand ? 'pointer' : 'not-allowed',
                  pointerEvents: 'auto',
                  boxShadow: commandStats.canCommand
                    ? '0 4px 8px rgba(0,0,0,0.5)'
                    : '0 2px 4px rgba(0,0,0,0.3)',
                  transition: 'all 0.2s',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                onMouseEnter={(e) => {
                  if (commandStats.canCommand) {
                    e.currentTarget.style.transform = 'scale(1.1)';
                  }
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'scale(1)';
                }}
              >
                {cmd.icon}
              </button>

              {/* Key Hint */}
              <div style={{
                fontSize: '10px',
                marginTop: '3px',
                color: 'white',
                textShadow: '1px 1px 2px black',
                fontWeight: 'bold'
              }}>
                [{cmd.key}]
              </div>
            </div>
          ))}

          {/* Separator */}
          <div style={{ width: '2px', height: '60px', background: 'white', margin: '0 10px' }} />

          {/* Praise Button */}
          <div style={{ textAlign: 'center' }}>
            <div style={{
              background: 'rgba(0, 0, 0, 0.85)',
              color: 'white',
              padding: '5px 10px',
              borderRadius: '12px',
              border: '2px solid white',
              fontSize: '10px',
              marginBottom: '5px',
              whiteSpace: 'nowrap',
              pointerEvents: 'none'
            }}>
              PRAISE
            </div>
            <button
              onClick={onPraise}
              style={{
                width: '70px',
                height: '70px',
                borderRadius: '50%',
                fontSize: '28px',
                background: 'radial-gradient(circle, #FFC107, #F57F17)',
                color: 'white',
                border: '3px solid white',
                cursor: 'pointer',
                pointerEvents: 'auto',
                boxShadow: '0 4px 8px rgba(0,0,0,0.5)',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              👏
            </button>
            <div style={{
              fontSize: '10px',
              marginTop: '3px',
              color: 'white',
              textShadow: '1px 1px 2px black',
              fontWeight: 'bold'
            }}>
              [SPACE]
            </div>
          </div>

          {/* Scold Button */}
          <div style={{ textAlign: 'center' }}>
            <div style={{
              background: 'rgba(0, 0, 0, 0.85)',
              color: 'white',
              padding: '5px 10px',
              borderRadius: '12px',
              border: '2px solid white',
              fontSize: '10px',
              marginBottom: '5px',
              whiteSpace: 'nowrap',
              pointerEvents: 'none'
            }}>
              SCOLD
            </div>
            <button
              onClick={onScold}
              style={{
                width: '70px',
                height: '70px',
                borderRadius: '50%',
                fontSize: '28px',
                background: 'radial-gradient(circle, #F44336, #C62828)',
                color: 'white',
                border: '3px solid white',
                cursor: 'pointer',
                pointerEvents: 'auto',
                boxShadow: '0 4px 8px rgba(0,0,0,0.5)',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              😠
            </button>
            <div style={{
              fontSize: '10px',
              marginTop: '3px',
              color: 'white',
              textShadow: '1px 1px 2px black',
              fontWeight: 'bold'
            }}>
              [CTRL]
            </div>
          </div>

          {/* Separator */}
          <div style={{ width: '2px', height: '60px', background: 'white', margin: '0 10px' }} />

          {/* Override Toggle */}
          <div style={{ textAlign: 'center' }}>
            <div style={{
              background: 'rgba(0, 0, 0, 0.85)',
              color: 'white',
              padding: '5px 10px',
              borderRadius: '12px',
              border: '2px solid white',
              fontSize: '10px',
              marginBottom: '5px',
              whiteSpace: 'nowrap',
              pointerEvents: 'none'
            }}>
              {commandStats.overrideMode ? 'AUTO' : 'DIRECT'}
            </div>
            <button
              onClick={onOverrideToggle}
              style={{
                width: '70px',
                height: '70px',
                borderRadius: '50%',
                fontSize: '28px',
                background: commandStats.overrideMode
                  ? 'radial-gradient(circle, #4CAF50, #2E7D32)'
                  : 'radial-gradient(circle, #FF5722, #D84315)',
                color: 'white',
                border: '3px solid white',
                cursor: 'pointer',
                pointerEvents: 'auto',
                boxShadow: '0 4px 8px rgba(0,0,0,0.5)',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              {commandStats.overrideMode ? '✅' : '⚠️'}
            </button>
            <div style={{
              fontSize: '10px',
              marginTop: '3px',
              color: 'white',
              textShadow: '1px 1px 2px black',
              fontWeight: 'bold'
            }}>
              [TAB]
            </div>
          </div>
        </div>
      )}

      {/* Cheer Meter (Orbit Cam only) */}
      {cameraMode === 'orbit' && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '16px', marginBottom: '5px', fontWeight: 'bold' }}>
            {cheerData.meterDisplay.status}
          </div>
          <div style={{ fontSize: '24px', marginBottom: '10px' }}>
            {cheerData.meterDisplay.display}
          </div>
          <div style={{
            width: '300px',
            height: '25px',
            background: '#333',
            border: '3px solid #FFD700',
            borderRadius: '15px',
            overflow: 'hidden',
            boxShadow: cheerData.specialReady ? '0 0 20px #FFD700' : 'none'
          }}>
            <div style={{
              width: `${cheerData.cheerMeter}%`,
              height: '100%',
              background: cheerData.specialReady
                ? 'linear-gradient(90deg, #FF9800, #F44336)'
                : 'linear-gradient(90deg, #FFEB3B, #FFC107)',
              transition: 'width 0.3s'
            }} />
          </div>

          {/* Cheer Button */}
          <button
            onClick={onCheer}
            disabled={!cheerData.canCheer}
            style={{
              marginTop: '10px',
              padding: '15px 30px',
              fontSize: '18px',
              fontWeight: 'bold',
              background: cheerData.canCheer ? '#4CAF50' : '#666',
              color: 'white',
              border: '3px solid white',
              borderRadius: '10px',
              cursor: cheerData.canCheer ? 'pointer' : 'not-allowed',
              pointerEvents: 'auto',
              boxShadow: cheerData.canCheer ? '0 4px 10px rgba(0,0,0,0.3)' : 'none',
              transition: 'all 0.2s'
            }}
          >
            👏 ANFEUERN (SPACE)
          </button>

          {cheerData.specialReady && (
            <div style={{
              marginTop: '15px',
              padding: '15px',
              background: 'rgba(255, 69, 0, 0.9)',
              border: '3px solid #FFD700',
              borderRadius: '10px',
              fontSize: '18px',
              fontWeight: 'bold',
              textAlign: 'center',
              animation: 'pulse 1s infinite'
            }}>
              🔥 SPECIAL FINISHER BEREIT! 🔥<br/>
              <small>Drücke F für EXPLOSION!</small>
            </div>
          )}
        </div>
      )}

      {/* Camera Mode Indicator */}
      <div style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        background: 'rgba(0,0,0,0.7)',
        padding: '15px',
        borderRadius: '10px',
        border: '2px solid white'
      }}>
        <div style={{ fontSize: '14px', marginBottom: '5px' }}>Kamera-Modus:</div>
        <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
          {cameraMode === 'orbit' && '🎥 ORBIT (Anfeuern)'}
          {cameraMode === 'third_person' && '👤 THIRD PERSON (Action)'}
          {cameraMode === 'first_person' && '👁️ FIRST PERSON (Action)'}
        </div>
        <button
          onClick={onCameraSwitch}
          style={{
            marginTop: '10px',
            padding: '8px 15px',
            fontSize: '12px',
            background: '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            pointerEvents: 'auto'
          }}
        >
          WECHSELN (C)
        </button>
      </div>

      {/* Controls Help */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        background: 'rgba(0,0,0,0.7)',
        padding: '15px',
        borderRadius: '10px',
        border: '2px solid white',
        fontSize: '12px',
        maxWidth: '250px'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>STEUERUNG:</div>
        {cameraMode === 'orbit' ? (
          <>
            <div>SPACE - Anfeuern</div>
            <div>F - Special Finisher</div>
            <div>Maus - Kamera drehen</div>
            <div>Scroll - Zoom</div>
          </>
        ) : (
          <>
            <div>WASD - Bewegung</div>
            <div>LMB - Light Attack</div>
            <div>RMB - Heavy Attack</div>
            <div>SPACE - Dodge</div>
            <div>Q - Parry</div>
            <div>SHIFT - Block</div>
            <div>1-6 - Elemente</div>
          </>
        )}
        <div style={{ marginTop: '10px', borderTop: '1px solid white', paddingTop: '10px' }}>
          C - Kamera wechseln
        </div>
      </div>
    </div>
  );
}

// Main Game Scene Component
function Scene({ combatSystem, cheerSystem, cameraController, cameraMode, setCameraMode }) {
  const { camera } = useThree();
  const [najikaPosition, setNajikaPosition] = useState(new THREE.Vector3(0, 0.75, 0));
  const [najikaRotation, setNajikaRotation] = useState(0);

  // Keyboard input
  const keys = useRef({});

  useEffect(() => {
    const handleKeyDown = (e) => { keys.current[e.key.toLowerCase()] = true; };
    const handleKeyUp = (e) => { keys.current[e.key.toLowerCase()] = false; };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  useFrame((state, delta) => {
    // Update camera
    const input = {
      mouseDeltaX: 0,
      mouseDeltaY: 0,
      wheelDelta: 0,
      mouseDown: false,
      isMoving: false
    };

    // Movement in action modes
    if (cameraMode !== 'orbit') {
      const moveSpeed = 5 * delta;
      const forward = cameraController.getForwardVector();
      const right = cameraController.getRightVector();

      let moved = false;

      if (keys.current['w']) {
        najikaPosition.x += forward.x * moveSpeed;
        najikaPosition.z += forward.z * moveSpeed;
        moved = true;
      }
      if (keys.current['s']) {
        najikaPosition.x -= forward.x * moveSpeed;
        najikaPosition.z -= forward.z * moveSpeed;
        moved = true;
      }
      if (keys.current['a']) {
        najikaPosition.x -= right.x * moveSpeed;
        najikaPosition.z -= right.z * moveSpeed;
        moved = true;
      }
      if (keys.current['d']) {
        najikaPosition.x += right.x * moveSpeed;
        najikaPosition.z += right.z * moveSpeed;
        moved = true;
      }

      input.isMoving = moved;
      setNajikaPosition(najikaPosition);
    }

    // Update camera controller
    cameraController.target = najikaPosition;
    cameraController.update(delta, input);
  });

  return (
    <>
      <Sky sunPosition={[100, 20, 100]} />
      <ambientLight intensity={0.3} />
      <directionalLight
        position={[10, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />

      {/* Najika Character */}
      <NajikaModel
        position={najikaPosition}
        rotation={najikaRotation}
        combatSystem={combatSystem}
        cheerSystem={cheerSystem}
        cameraMode={cameraMode}
      />

      {/* Ground */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[100, 100]} />
        <meshStandardMaterial color="#4CAF50" />
      </mesh>

      {/* Environment */}
      <Environment preset="sunset" />
    </>
  );
}

// Main Game Scene Export
export default function GameScene() {
  const [combatSystem] = useState(() => new CombatSystem());
  const [cheerSystem] = useState(() => new CheerSystem());
  const [commandSystem] = useState(() => new CommandSystem());
  const [finisherQTE] = useState(() => new FinisherQTE());
  const [cameraController, setCameraController] = useState(null);
  const [cameraMode, setCameraMode] = useState('orbit');
  const [cheerMessage, setCheerMessage] = useState('');
  const [commandMessage, setCommandMessage] = useState('');
  const [finisherActive, setFinisherActive] = useState(false);

  // Initialize camera controller
  useEffect(() => {
    // Will be initialized in Canvas
  }, []);

  useEffect(() => {
    if (cameraController) {
      // Set target height to Najika's center
      cameraController.target.y = 1.5;
    }
  }, [cameraController]);

  // Handle cheer input
  const handleCheer = () => {
    const result = cheerSystem.onCheerInput();
    setCheerMessage(result.message || '');

    setTimeout(() => setCheerMessage(''), 2000);
  };

  // Handle command
  const handleCommand = async (key) => {
    // Get current Najika state from battle system
    const battleStatus = await battleAPI.getBattleStatus();
    const najikaState = battleAPI.getNajikaState(battleStatus);

    // Execute command in CommandSystem (local)
    const result = commandSystem.executeCommand(key, najikaState);

    if (result.success) {
      // Send command to backend battle system
      try {
        const battleResult = await battleAPI.executeCommand(key, result);

        // Calculate and add Battle XP
        const battleXP = battleAPI.calculateBattleXP(battleResult);
        if (battleXP > 0) {
          const evolutionResult = commandSystem.addBattleXP(battleXP, battleResult.result === 'victory');
          if (evolutionResult.evolved) {
            setCommandMessage(evolutionResult.message);
            setTimeout(() => setCommandMessage(''), 4000);
            return;
          }
        }

        // Show timing or battle message
        const message = result.timing?.message || battleResult.message || 'Command ausgeführt!';
        setCommandMessage(message);
      } catch (error) {
        console.error('Battle API Error:', error);
        setCommandMessage(result.timing?.message || 'Command ausgeführt (Offline)');
      }
    } else {
      setCommandMessage(result.message);
    }

    setTimeout(() => setCommandMessage(''), 2000);
  };

  // Handle praise
  const handlePraise = () => {
    const result = commandSystem.praise('normal');
    setCommandMessage(result.message);
    setTimeout(() => setCommandMessage(''), 2000);
  };

  // Handle scold
  const handleScold = () => {
    const result = commandSystem.scold('normal');
    setCommandMessage(result.message);
    setTimeout(() => setCommandMessage(''), 2000);
  };

  // Handle override toggle
  const handleOverrideToggle = () => {
    const result = commandSystem.toggleOverride();
    setCommandMessage(result.message);
    setTimeout(() => setCommandMessage(''), 3000);
  };

  // Handle camera switch
  const handleCameraSwitch = () => {
    const modes = ['orbit', 'third_person', 'first_person'];
    const currentIndex = modes.indexOf(cameraMode);
    const nextMode = modes[(currentIndex + 1) % modes.length];
    setCameraMode(nextMode);

    if (cameraController) {
      cameraController.setMode(nextMode);
    }
  };

  // Handle battle start
  const handleStartBattle = async () => {
    try {
      const battleStatus = await battleAPI.startBattle();
      if (battleStatus.active) {
        setCommandMessage('⚔️ Kampf gestartet! ' + (battleStatus.message || ''));
        console.log('Battle started:', battleStatus);
      } else if (battleStatus.fallback) {
        setCommandMessage('⚠️ Offline-Modus: Backend nicht erreichbar');
      } else {
        setCommandMessage('❌ Kampf konnte nicht gestartet werden');
      }
    } catch (error) {
      console.error('Start Battle Error:', error);
      setCommandMessage('❌ Fehler beim Kampfstart');
    }
    setTimeout(() => setCommandMessage(''), 3000);
  };

  // Handle finisher
  const handleFinisher = () => {
    if (finisherQTE.isActive()) {
      // QTE bereits aktiv = Mash Input
      const result = finisherQTE.onMash();
      if (result.success) {
        console.log(`Mash! Meter: ${result.meter}%`);
      }
    } else {
      // Starte Finisher QTE
      const result = finisherQTE.start();
      setFinisherActive(true);
      setCommandMessage(result.message);

      // Update-Loop für QTE
      const qteInterval = setInterval(() => {
        const updateResult = finisherQTE.update(0.016); // ~60fps

        if (!updateResult || !updateResult.active) {
          // QTE beendet
          clearInterval(qteInterval);
          setFinisherActive(false);

          if (updateResult && updateResult.completed) {
            setCommandMessage(updateResult.message);
            setTimeout(() => setCommandMessage(''), 3000);

            // TODO: Send finisher damage to backend
            console.log(`Finisher Completed: ${updateResult.multiplier.toFixed(2)}x damage`);
          }
        }
      }, 16);
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (cameraMode === 'orbit') {
        // Finisher QTE active? SPACE = Mash!
        if (finisherQTE.isActive() && e.key === ' ') {
          e.preventDefault();
          handleFinisher(); // Mash!
          return;
        }

        // Commands 1-4
        if (['1', '2', '3', '4'].includes(e.key)) {
          e.preventDefault();
          handleCommand(e.key);
        }
        // Space for cheer (if not in finisher QTE)
        else if (e.key === ' ') {
          e.preventDefault();
          handleCheer();
        }
        // F for finisher
        else if (e.key.toLowerCase() === 'f') {
          e.preventDefault();
          handleFinisher(); // Start QTE
        }
      }

      // Camera switch (always available)
      if (e.key.toLowerCase() === 'c') {
        handleCameraSwitch();
      }
    };

    const handleKeyDown = (e) => {
      // TAB for override toggle (orbit cam only)
      if (e.key === 'Tab' && cameraMode === 'orbit') {
        e.preventDefault();
        handleOverrideToggle();
      }
      // Ctrl for scold
      else if (e.key === 'Control' && cameraMode === 'orbit') {
        e.preventDefault();
        handleScold();
      }
    };

    window.addEventListener('keypress', handleKeyPress);
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keypress', handleKeyPress);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [cameraMode, cheerSystem, commandSystem, cameraController]);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Canvas
        camera={{ position: [0, 3, 8], fov: 60 }}
        shadows
        onCreated={({ camera }) => {
          const controller = new CameraController(camera, { x: 0, y: 1.5, z: 0 });
          setCameraController(controller);
        }}
      >
        {cameraController && (
          <Scene
            combatSystem={combatSystem}
            cheerSystem={cheerSystem}
            cameraController={cameraController}
            cameraMode={cameraMode}
            setCameraMode={setCameraMode}
          />
        )}
      </Canvas>

      {/* Combat UI Overlay */}
      {cameraController && (
        <CombatUI
          combatSystem={combatSystem}
          cheerSystem={cheerSystem}
          commandSystem={commandSystem}
          cameraMode={cameraMode}
          onCheer={handleCheer}
          onCameraSwitch={handleCameraSwitch}
          onCommand={handleCommand}
          onPraise={handlePraise}
          onScold={handleScold}
          onOverrideToggle={handleOverrideToggle}
          onStartBattle={handleStartBattle}
        />
      )}

      {/* Cheer Message Popup */}
      {cheerMessage && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          background: 'rgba(0,0,0,0.9)',
          color: 'white',
          padding: '30px 50px',
          borderRadius: '20px',
          border: '4px solid #FFD700',
          fontSize: '24px',
          fontWeight: 'bold',
          textAlign: 'center',
          zIndex: 1000,
          animation: 'fadeInOut 2s'
        }}>
          {cheerMessage}
        </div>
      )}

      {/* Command Message Popup */}
      {commandMessage && !finisherActive && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          background: 'rgba(0,0,0,0.9)',
          color: 'white',
          padding: '30px 50px',
          borderRadius: '20px',
          border: '4px solid #4CAF50',
          fontSize: '20px',
          fontWeight: 'bold',
          textAlign: 'center',
          zIndex: 1000,
          animation: 'fadeInOut 2s'
        }}>
          {commandMessage}
        </div>
      )}

      {/* Finisher QTE Overlay */}
      {finisherActive && (() => {
        const qteData = finisherQTE.getUIData();
        return (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            background: 'rgba(0, 0, 0, 0.8)',
            zIndex: 2000,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center'
          }}>
            {/* FINISH!!! Text */}
            <div style={{
              fontSize: '80px',
              fontWeight: 'bold',
              color: '#FFD700',
              textShadow: '0 0 20px #FF6B00, 0 0 40px #FF1744',
              marginBottom: '40px',
              animation: 'pulse 0.5s infinite'
            }}>
              🔥 FINISH!!! 🔥
            </div>

            {/* Instruction */}
            <div style={{
              fontSize: '24px',
              color: 'white',
              marginBottom: '30px',
              textShadow: '2px 2px 4px black'
            }}>
              {qteData.instruction}
            </div>

            {/* Meter Container */}
            <div style={{
              width: '600px',
              marginBottom: '20px'
            }}>
              {/* Meter Background */}
              <div style={{
                width: '100%',
                height: '50px',
                background: '#333',
                border: '4px solid white',
                borderRadius: '25px',
                overflow: 'hidden',
                position: 'relative'
              }}>
                {/* Meter Fill */}
                <div style={{
                  width: `${qteData.meter}%`,
                  height: '100%',
                  background: qteData.meter >= 90
                    ? 'linear-gradient(90deg, #FFD700, #FFA500)'
                    : qteData.meter >= 50
                    ? 'linear-gradient(90deg, #4CAF50, #8BC34A)'
                    : 'linear-gradient(90deg, #FF6B9D, #FF1744)',
                  transition: 'width 0.1s',
                  boxShadow: '0 0 20px rgba(255, 215, 0, 0.8)'
                }} />

                {/* Meter Text */}
                <div style={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  fontSize: '24px',
                  fontWeight: 'bold',
                  color: 'white',
                  textShadow: '2px 2px 4px black'
                }}>
                  {qteData.meter}%
                </div>
              </div>

              {/* Stats */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginTop: '15px',
                fontSize: '18px',
                color: 'white',
                textShadow: '1px 1px 2px black'
              }}>
                <div>⏱️ Zeit: {qteData.timeLeft}s</div>
                <div>💥 Mashes: {qteData.mashCount}</div>
              </div>
            </div>

            {/* Rank Indicator */}
            {qteData.meter >= 90 && (
              <div style={{
                fontSize: '40px',
                fontWeight: 'bold',
                color: '#FFD700',
                textShadow: '0 0 10px #FFA500',
                animation: 'pulse 0.3s infinite'
              }}>
                ✨ RANK S! ✨
              </div>
            )}
            {qteData.meter >= 70 && qteData.meter < 90 && (
              <div style={{
                fontSize: '40px',
                fontWeight: 'bold',
                color: '#4CAF50',
                textShadow: '0 0 10px #8BC34A'
              }}>
                🔥 RANK A!
              </div>
            )}
          </div>
        );
      })()}

      <style>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        @keyframes fadeInOut {
          0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
          20% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
          80% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
          100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
        }
      `}</style>
    </div>
  );
}
