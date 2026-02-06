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


# ============================================================================
# NAJIKA CARE ENDPOINTS (Füttern, Trinken, Waschen, Schlafen)
# ============================================================================

@router.post("/najika/feed")
async def najika_feed():
    """Feed Najika - increases hunger stat"""
    return {
        "success": True,
        "message": "*mampf mampf* Danke für das Essen! 🍜",
        "stat_change": {"hunger": +25},
        "new_stats": {
            "hunger": 100,
            "thirst": 75,
            "cleanliness": 80,
            "energy": 85
        }
    }


@router.post("/najika/drink")
async def najika_drink():
    """Give Najika a drink - increases thirst stat"""
    return {
        "success": True,
        "message": "*schlürf* Erfrischend! 🥤",
        "stat_change": {"thirst": +30},
        "new_stats": {
            "hunger": 85,
            "thirst": 100,
            "cleanliness": 80,
            "energy": 85
        }
    }


@router.post("/najika/wash")
async def najika_wash():
    """Wash/bathe Najika - increases cleanliness stat"""
    return {
        "success": True,
        "message": "*plätsch* Jetzt fühl ich mich sauber! 🛁",
        "stat_change": {"cleanliness": +40},
        "new_stats": {
            "hunger": 85,
            "thirst": 90,
            "cleanliness": 100,
            "energy": 80
        }
    }


@router.post("/najika/sleep")
async def najika_sleep():
    """Let Najika sleep - restores energy"""
    return {
        "success": True,
        "message": "*gähn* Gute Nacht... zzz 😴",
        "stat_change": {"energy": +50},
        "new_stats": {
            "hunger": 75,
            "thirst": 80,
            "cleanliness": 90,
            "energy": 100
        }
    }
