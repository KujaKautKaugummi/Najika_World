"""
Najika Chat API Router
Handles all chat interactions with Ollama (najika-local, najika-nsfw)
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from backend.services.ollama_service import (
    call_ollama,
    call_ollama_stream,
    check_ollama_health
)

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    message: str
    mode: str = "public"  # public or private (kaetzchen-modus)


class ChatResponse(BaseModel):
    response: str
    mode: str
    emotion: str = "excited"
    model_used: str = "ollama"


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Main chat endpoint for Najika

    - **message**: The user's message to Najika
    - **mode**: "public" for normal chat, "private" for Kaetzchen-Modus (NSFW)

    Returns Najika's response with her full personality

    Models used:
    - public: najika-local (based on qwen2.5:7b)
    - private/nsfw: najika-nsfw (based on dolphin-mistral:7b)
    """
    # Determine if NSFW/private mode
    is_private = message.mode.lower() in ["private", "kaetzchen", "nsfw"]

    # Call Ollama with Najika's personality (baked into model!)
    response_text = await call_ollama(message.message, use_wizard=is_private)

    if not response_text:
        response_text = "Kuja! Ollama ist nicht gestartet... *traurig schau* Bitte starte 'ollama serve' für mich! 💔"

    # Determine emotion from response
    emotion = "excited"
    if "traurig" in response_text.lower() or "😢" in response_text or "😔" in response_text:
        emotion = "sad"
    elif "wütend" in response_text.lower() or "😠" in response_text:
        emotion = "angry"
    elif "müde" in response_text.lower() or "😴" in response_text or "*gähn*" in response_text.lower():
        emotion = "tired"
    elif "glücklich" in response_text.lower() or "💕" in response_text or "✨" in response_text:
        emotion = "happy"
    elif "explosion" in response_text.lower() or "EXPLOSION" in response_text:
        emotion = "explosive"

    return ChatResponse(
        response=response_text,
        mode=message.mode,
        emotion=emotion,
        model_used="najika-nsfw" if is_private else "najika-local"
    )


@router.post("/stream")
async def chat_stream(message: ChatMessage):
    """
    Streaming chat endpoint for Najika

    Returns Server-Sent Events (SSE) with token-by-token response
    """
    is_private = message.mode.lower() in ["private", "kaetzchen", "nsfw"]

    async def generate():
        async for token in call_ollama_stream(message.message, use_wizard=is_private):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/health")
async def chat_health():
    """
    Check if Ollama is running and Najika models are available
    """
    return await check_ollama_health()


@router.get("/models")
async def get_models():
    """
    Get information about Najika's Ollama models
    """
    return {
        "backend": "ollama",
        "models": {
            "sfw": "najika-local (qwen2.5:7b base)",
            "nsfw": "najika-nsfw (dolphin-mistral:7b base)"
        },
        "info": "Personality is baked into the models via Modelfile!"
    }


@router.get("/history")
async def chat_history(user_id: int = 1, limit: int = 50):
    """
    Get chat history (placeholder - implement with database later)
    """
    # TODO: Implement with database
    return {
        "history": [],
        "count": 0,
        "user_id": user_id
    }
