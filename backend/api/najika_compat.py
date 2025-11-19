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
        while True:
            data = {
                "status": "online",
                "personality": "megumin",
                "mood": "happy",
                "energy": 85,
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "backend": "fastapi",
        "version": "2.0.0"
    }
