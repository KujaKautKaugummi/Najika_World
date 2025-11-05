// Najika Digivice Interface (Tamagotchi-Style)
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const DigiviceContainer = styled.div`
  width: 300px;
  height: 400px;
  background: linear-gradient(145deg, #FF6B9D, #C44569);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  position: relative;
`;

const Screen = styled.div`
  width: 100%;
  height: 200px;
  background: #1a1a2e;
  border-radius: 10px;
  padding: 10px;
  color: #00ff00;
  font-family: 'Courier New', monospace;
  overflow-y: auto;
`;

const NeedsDisplay = styled.div`
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const NeedBar = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: white;
`;

const BarFill = styled.div`
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
`;

const ActionButtons = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 15px;
`;

const Button = styled.button`
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
`;

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
