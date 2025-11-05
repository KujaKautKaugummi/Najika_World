"""
Najika Backend API
Version: 2.5
FastAPI-based backend for Najika AI + Game
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

app = FastAPI(title="Najika API", version="2.5")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════

class ChatMessage(BaseModel):
    message: str
    mode: str = "public"  # public or private

class GameAction(BaseModel):
    action_type: str
    data: dict

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "2.5",
        "najika": "Ready to serve Kuja! 💥"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_backend": "ollama" if os.getenv("USE_OLLAMA") == "true" else "llama.cpp",
        "chromadb": "connected"
    }

@app.post("/chat")
async def chat(message: ChatMessage):
    """
    Main chat endpoint for Najika
    """
    # TODO: Implement AI response logic
    return {
        "response": "Kuja! Ich bin noch nicht vollständig implementiert, aber ich bin hier! 💥",
        "mode": message.mode,
        "emotion": "excited"
    }

@app.post("/game/action")
async def game_action(action: GameAction):
    """
    Handle game actions (combat, crafting, etc.)
    """
    # TODO: Implement game logic
    return {
        "success": True,
        "result": "Action processed"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket for real-time communication
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Najika: {data}")
    except:
        pass

# ═══════════════════════════════════════════════════════════════
# RUN SERVER
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", 5000))
    
    print("🌟 Najika Backend starting...")
    print(f"🔗 Listening on {host}:{port}")
    
    uvicorn.run(app, host=host, port=port)
