// Najika Touch Controls
import React, { useRef, useState } from 'react';
import styled from 'styled-components';

const ControlsContainer = styled.div`
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2000;
`;

const VirtualJoystick = styled.div`
  position: absolute;
  bottom: 30px;
  left: 30px;
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  pointer-events: auto;
`;

const JoystickHandle = styled.div`
  position: absolute;
  width: 50px;
  height: 50px;
  background: rgba(255, 107, 157, 0.8);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translate(\$\{props => props.x}px, \$\{props => props.y}px);
  transition: transform 0.1s ease;
`;

const ActionButtons = styled.div`
  position: absolute;
  bottom: 30px;
  right: 30px;
  display: flex;
  gap: 15px;
  pointer-events: auto;
`;

const ActionButton = styled.button`
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
`;

const WeavePad = styled.div`
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  display: grid;
  grid-template-columns: repeat(2, 50px);
  grid-template-rows: repeat(3, 50px);
  gap: 10px;
  pointer-events: auto;
`;

const ElementButton = styled.button`
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
`;

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
