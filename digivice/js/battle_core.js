const BattleCore=(function(){
  const enemiesDB={rat:{hp:15,atk:3},skeleton:{hp:30,atk:6},slime:{hp:20,atk:4}};
  let state=null;
  function start(){ state={hp:100,wave:1,enemies:spawn(1)}; return state }
  function spawn(w){ const pool=["rat","skeleton","slime"]; const arr=[]; for(let i=0;i<w+2;i++){ const t=pool[i%3]; arr.push({type:t,hp:enemiesDB[t].hp}) } return arr }
  function attack(){
    if(!state) return {done:false}; if(state.enemies.length){ state.enemies[0].hp-=10; if(state.enemies[0].hp<=0){ state.enemies.shift() } }
    if(!state.enemies.length){ state.wave++; state.enemies=spawn(state.wave) }
    state.hp=Math.max(0,state.hp-Math.max(0,state.enemies.length-1));
    return {hp:state.hp,wave:state.wave,enemies:state.enemies.length,done:state.hp==0}
  }
  return {start,attack}
})(); window.BattleCore=BattleCore;
