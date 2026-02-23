"""
Temperature System API
Handles environment and body temperature for Najika World
Used by index.html temperature integration
"""

from fastapi import APIRouter
from backend.utils import handle_errors

router = APIRouter(prefix="/api/temperature", tags=["Temperature"])


@router.get("/status")
@handle_errors()
async def get_temperature_status():
    """Get current temperature status"""
    return {
        "body_temp": 37.0,
        "environment_temp": 22.0,
        "region": "Samtmoos-Tiefwald",
        "weather": "clear",
        "effects": []
    }