// Najika HUD Component
import React from 'react';
import styled from 'styled-components';

const HudContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1000;
`;

const HealthBar = styled.div`
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 300px;
  height: 30px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 15px;
  overflow: hidden;
  pointer-events: auto;
`;

const HealthFill = styled.div`
  height: 100%;
  background: linear-gradient(90deg, #e74c3c, #c0392b);
  width: \$\{props => props.percent}%;
  transition: width 0.3s ease;
`;

const NeedsPanel = styled.div`
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  padding: 15px;
  border-radius: 10px;
  color: white;
`;

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
