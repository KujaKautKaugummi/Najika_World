const Oregon=(function(){
  const API = window.API_BASE_URL || 'http://localhost:8000';
  async function next(){ const r=await fetch(`${API}/api/event/next`,{method:"POST"}); return r.json() }
  return {next}
})(); window.Oregon=Oregon;
