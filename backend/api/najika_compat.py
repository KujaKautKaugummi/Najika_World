"""
Najika Compatibility API
Endpoints for compatibility with old najika_server.py
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Najika Compatibility"])


@router.get("/status")
async def status():
    """Legacy status endpoint"""
    return {
        "status": "online",
        "personality": "megumin",
        "mood": "happy",
        "energy": 85,
        "timestamp": datetime.now().isoformat(),
        "backend": "fastapi",
        "version": "2.0.0"
    }


@router.get("/najika/status")
async def najika_status():
    """Legacy Najika status endpoint"""
    return {
        "status": "online",
        "personality": "megumin",
        "mood": "happy",
        "energy": 85,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/status/stream")
async def status_stream():
    """Legacy status stream endpoint (SSE)"""
    async def event_generator():
        try:
            while True:
                data = {
                    "status": "online",
                    "personality": "megumin",
                    "mood": "happy",
                    "energy": 85,
                    "private_mode": False,  # Add private_mode field expected by frontend
                    "timestamp": datetime.now().isoformat()
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            # Client disconnected - this is normal, don't log error
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "backend": "fastapi",
        "version": "2.0.0"
    }


@router.get("/chat/history")
async def chat_history(user_id: int = 1):
    """Legacy chat history endpoint"""
    return {
        "history": [],
        "count": 0
    }


@router.get("/cloud/status")
async def cloud_status():
    """Legacy cloud provider status"""
    return {
        "cloud_enabled": False,
        "provider": "local",
        "status": "offline"
    }


@router.post("/najika/equipment")
async def najika_equipment():
    """Legacy equipment endpoint"""
    return {
        "weapon": "staff",
        "armor": "mage_robe",
        "accessory": "explosion_ring",
        "stats": {
            "attack": 50,
            "defense": 30,
            "magic": 100
        }
    }


@router.post("/room/actions")
async def room_actions(room: str = "Wohnzimmer"):
    """Legacy room actions endpoint"""
    # Return default actions for rooms
    actions_map = {
        "Wohnzimmer": ["Chat", "Minigame", "Stats"],
        "Schlafzimmer": ["Sleep", "Save", "Stats"],
        "Küche": ["Cook", "Eat", "Stats"],
        "Garten": ["Garden", "Plant", "Stats"],
        "Musikraum": ["Play", "Listen", "Stats"],
        "Trainingszimmer": ["Train", "Battle", "Stats"],
        "Kampfarena": ["Fight", "Tournament", "Stats"],
    }

    return {
        "room": room,
        "actions": actions_map.get(room, ["Chat", "Stats"])
    }
