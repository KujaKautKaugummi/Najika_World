// Mobile Touch Controls - Virtual Joystick + Buttons
import React, { useRef, useEffect, useState } from 'react';
import styled from 'styled-components';

const ControlsContainer = styled.div`
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 250px;
  pointer-events: none;
  z-index: 150;
`;

const Joystick = styled.div`
  position: absolute;
  bottom: 30px;
  left: 30px;
  width: 150px;
  height: 150px;
  background: rgba(255, 255, 255, 0.1);
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  pointer-events: auto;
  touch-action: none;
`;

const JoystickKnob = styled.div`
  position: absolute;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #FF6B9D, #FF1744);
  border: 3px solid white;
  border-radius: 50%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.1s;
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);
`;

const ActionButtons = styled.div`
  position: absolute;
  bottom: 30px;
  right: 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  pointer-events: auto;
`;

const ActionButton = styled.button`
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid white;
  background: ${props => props.primary ?
    'linear-gradient(135deg, #FF6B9D, #FF1744)' :
    'linear-gradient(135deg, #666, #333)'
  };
  color: white;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  pointer-events: auto;
  touch-action: none;
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);

  &:active {
    transform: scale(0.95);
    box-shadow: 0 2px 4px rgba(0,0,0,0.4);
  }
`;

export default function MobileControls({ onMove, onAction, onInteract }) {
  const joystickRef = useRef(null);
  const knobRef = useRef(null);
  const [joystickActive, setJoystickActive] = useState(false);
  const [knobPosition, setKnobPosition] = useState({ x: 0, y: 0 });

  const joystickStartPos = useRef({ x: 0, y: 0 });
  const activeTouch = useRef(null);

  useEffect(() => {
    const joystick = joystickRef.current;
    if (!joystick) return;

    const handleTouchStart = (e) => {
      e.preventDefault();
      const touch = e.touches[0];
      activeTouch.current = touch.identifier;

      const rect = joystick.getBoundingClientRect();
      joystickStartPos.current = {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2
      };

      setJoystickActive(true);
    };

    const handleTouchMove = (e) => {
      e.preventDefault();
      if (!joystickActive) return;

      const touch = Array.from(e.touches).find(t => t.identifier === activeTouch.current);
      if (!touch) return;

      const dx = touch.clientX - joystickStartPos.current.x;
      const dy = touch.clientY - joystickStartPos.current.y;

      const distance = Math.sqrt(dx * dx + dy * dy);
      const maxDistance = 45; // Max knob displacement

      let finalDx = dx;
      let finalDy = dy;

      if (distance > maxDistance) {
        finalDx = (dx / distance) * maxDistance;
        finalDy = (dy / distance) * maxDistance;
      }

      setKnobPosition({ x: finalDx, y: finalDy });

      // Calculate normalized direction (-1 to 1)
      const normalizedX = finalDx / maxDistance;
      const normalizedY = finalDy / maxDistance;

      onMove({ x: normalizedX, y: normalizedY });
    };

    const handleTouchEnd = (e) => {
      e.preventDefault();
      setJoystickActive(false);
      setKnobPosition({ x: 0, y: 0 });
      activeTouch.current = null;
      onMove({ x: 0, y: 0 });
    };

    joystick.addEventListener('touchstart', handleTouchStart);
    joystick.addEventListener('touchmove', handleTouchMove);
    joystick.addEventListener('touchend', handleTouchEnd);
    joystick.addEventListener('touchcancel', handleTouchEnd);

    return () => {
      joystick.removeEventListener('touchstart', handleTouchStart);
      joystick.removeEventListener('touchmove', handleTouchMove);
      joystick.removeEventListener('touchend', handleTouchEnd);
      joystick.removeEventListener('touchcancel', handleTouchEnd);
    };
  }, [joystickActive, onMove]);

  return (
    <ControlsContainer>
      {/* Virtual Joystick */}
      <Joystick ref={joystickRef}>
        <JoystickKnob
          ref={knobRef}
          style={{
            transform: `translate(calc(-50% + ${knobPosition.x}px), calc(-50% + ${knobPosition.y}px))`
          }}
        />
      </Joystick>

      {/* Action Buttons */}
      <ActionButtons>
        <ActionButton
          primary
          onTouchStart={() => onAction('attack')}
          onTouchEnd={() => {}}
        >
          ⚔️
        </ActionButton>
        <ActionButton
          onTouchStart={() => onInteract()}
          onTouchEnd={() => {}}
        >
          E
        </ActionButton>
      </ActionButtons>
    </ControlsContainer>
  );
}
