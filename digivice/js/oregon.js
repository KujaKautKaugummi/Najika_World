const Oregon=(function(){
  async function next(){ const r=await fetch("/api/event/next",{method:"POST"}); return r.json() }
  return {next}
})(); window.Oregon=Oregon;
