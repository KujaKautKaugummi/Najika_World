"""
Chat Router V2 - Nutzt Shared State
Migriert aus najika_server.py Chat-Logik + existierendem chat.py.

Verbesserungen gegenueber chat.py:
- Nutzt backend.shared_state (zentral, nicht eigener _mind_state)
- Bond-Strength/Interaction-Tracking ueber shared_state
- Memory-Instanz aus shared_state (lifespan-initialisiert)
- Alles andere (NajikaMind, Sessions, Streaming) bleibt gleich
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.utils import handle_errors
import json
import asyncio
import time
import uuid
import sys
import os
import logging

logger = logging.getLogger("najika.api.chat_v2")

# Backend-Dir fuer najika_* Imports
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from backend.shared_state import STATE, add_interaction
from backend.services.ollama_service import (
    call_ollama_chat,
    call_ollama_chat_sync,
    call_ollama_chat_stream,
    check_ollama_health,
)

# ===== NajikaMind (graceful) =====
MIND_AVAILABLE = False
PERSONALITY_AVAILABLE = False
MEMORY_AVAILABLE = False

try:
    from najika_mind import process_with_mind, MindResponse, get_mind
    MIND_AVAILABLE = True
    logger.info("NajikaMind AGI-Orchester verfuegbar")
except ImportError as e:
    logger.warning(f"NajikaMind nicht verfuegbar: {e}")

try:
    from najika_personality_engine import (
        build_prompt as build_personality_prompt,
        process_response as process_personality_response,
        update_state as update_personality_state,
        get_state as get_personality_state,
    )
    PERSONALITY_AVAILABLE = True
    logger.info("PersonalityEngine verfuegbar")
except ImportError as e:
    logger.warning(f"PersonalityEngine nicht verfuegbar: {e}")

try:
    from najika_memory import NajikaMemory
    _memory_instance = NajikaMemory()
    MEMORY_AVAILABLE = True
    logger.info(f"ChromaDB Memory verfuegbar ({_memory_instance.conversations.count()} Conversations)")
except Exception as e:
    _memory_instance = None
    logger.warning(f"ChromaDB Memory nicht verfuegbar: {e}")


router = APIRouter(prefix="/api/v2/chat", tags=["Chat V2"])

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

_conversations: Dict[str, dict] = {}
MAX_HISTORY_MESSAGES = 20
CONTEXT_WINDOW_MESSAGES = 10


def _get_or_create_session(session_id: str = None) -> tuple:
    if not session_id or session_id not in _conversations:
        session_id = session_id or str(uuid.uuid4())[:8]
        _conversations[session_id] = {
            "messages": [],
            "created_at": time.time(),
            "last_active": time.time(),
            "mode": "public",
        }
    session = _conversations[session_id]
    session["last_active"] = time.time()
    return session_id, session


def _cleanup_old_sessions():
    now = time.time()
    expired = [sid for sid, s in _conversations.items() if now - s["last_active"] > 86400]
    for sid in expired:
        del _conversations[sid]


def _build_ollama_messages(session: dict, limit: int = CONTEXT_WINDOW_MESSAGES) -> list:
    messages = []
    for msg in session["messages"][-limit:]:
        content = msg["content"]
        if not content.strip():
            continue
        messages.append({
            "role": msg["role"],
            "content": content[:2000],
        })
    return messages


def _detect_mood_from_text(text: str) -> str:
    lower = text.lower()
    if "traurig" in lower or "\U0001F622" in text or "\U0001F614" in text:
        return "sad"
    elif "wuetend" in lower or "\U0001F620" in text:
        return "angry"
    elif "muede" in lower or "\U0001F634" in text or "*gaehn*" in lower:
        return "tired"
    elif "explosion" in lower or "EXPLOSION" in text:
        return "explosive"
    elif "gluecklich" in lower or "\U0001F495" in text or "\u2728" in text:
        return "happy"
    elif "needy" in lower or "vermiss" in lower or "\U0001F97A" in text:
        return "needy"
    return "excited"


def _build_hooks_from_mood(mood: str) -> list:
    mood_animations = {
        "happy": "cheer", "excited": "cheer", "sad": "wave",
        "angry": "idle", "explosive": "cheer", "sleepy": "idle",
        "needy": "wave", "dominant": "idle", "playful": "dance",
        "possessive": "idle", "sweet": "cheer", "horny": "dance",
        "pouty": "wave", "jealous": "idle", "loving": "cheer",
    }
    anim = mood_animations.get(mood)
    if anim:
        return [{"type": "ANIMATION", "content": anim}]
    return []


# ============================================================================
# NAJIKAMIND BRIDGE
# ============================================================================

def _process_with_mind_sync(message: str, history: list, is_private: bool) -> dict:
    """Synchroner Wrapper fuer NajikaMind-Pipeline"""
    def _prompt_builder(hist, msg):
        return f"Kuja sagt: {msg}"

    def _ai_caller(prompt, use_wizard, context, user_message):
        chat_messages = []
        if context:
            for h in context[-8:]:
                content = h.get("content", "")
                if content.strip():
                    chat_messages.append({
                        "role": "user" if h.get("role") == "user" else "assistant",
                        "content": content[:2000],
                    })
        if user_message:
            chat_messages.append({"role": "user", "content": user_message})

        result = call_ollama_chat_sync(chat_messages, use_wizard=use_wizard)
        return (result or "*blinzelt verwirrt* Ehm... Blackout!", "ollama")

    # Shared State nutzen statt lokaler Kopie
    mind_state = {
        "history": STATE["history"],
        "bond_strength": STATE["bond_strength"],
        "behavior_mode": STATE["behavior_mode"],
        "personality_weights": STATE["personality_weights"],
    }

    try:
        mind_response = process_with_mind(
            message=message,
            history=history,
            state=mind_state,
            prompt_builder=_prompt_builder,
            ai_caller=_ai_caller,
            private_mode=is_private,
        )
        return {
            "text": mind_response.text,
            "mood": mind_response.mood,
            "hooks": mind_response.hooks,
            "personality": mind_response.personality_dominant,
            "intent": mind_response.intent,
            "inner_thought": mind_response.inner_thought,
            "success": True,
        }
    except Exception as e:
        logger.error(f"NajikaMind ERROR: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ChatMessage(BaseModel):
    message: str
    mode: str = "public"
    session_id: Optional[str] = None
    use_rag: bool = True
    use_mind: bool = True
    temperature: Optional[float] = None


class ChatResponse(BaseModel):
    response: str
    mode: str
    mood: str = "excited"
    model_used: str = "ollama"
    hooks: List[Dict[str, Any]] = []
    session_id: str = ""
    rag_used: bool = False
    mind_used: bool = False
    timestamp: float = 0


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
@handle_errors()
async def chat_v2(message: ChatMessage):
    """
    Chat V2 - Nutzt Shared State + NajikaMind AGI-Orchester.

    Verbesserungen:
    - Bond-Strength Tracking ueber shared_state
    - Interaction-Counter
    - Shared Memory-Instanz
    - RAG/Mind Toggle per Request
    """
    if len(_conversations) > 100:
        _cleanup_old_sessions()

    is_private = message.mode.lower() in ["private", "kaetzchen", "nsfw"]

    session_id, session = _get_or_create_session(message.session_id)
    session["mode"] = message.mode

    # User-Message speichern
    session["messages"].append({
        "role": "user",
        "content": message.message,
        "timestamp": time.time(),
    })
    if len(session["messages"]) > MAX_HISTORY_MESSAGES:
        session["messages"] = session["messages"][-MAX_HISTORY_MESSAGES:]

    # Shared State History syncen
    STATE["history"] = [
        {"role": m["role"], "content": m["content"]}
        for m in session["messages"]
    ]

    # Kaetzchen-Trigger
    if "kaetzchen" in message.message.lower() or "kätzchen" in message.message.lower():
        STATE["private_mode"] = True

    # Interaction tracking (shared_state!)
    add_interaction()

    response_text = None
    mood = "excited"
    hooks = []
    model_used = "najika-nsfw" if is_private else "najika-local"
    mind_used = False
    rag_used = False

    # ===== PFAD 1: NajikaMind =====
    if MIND_AVAILABLE and message.use_mind:
        history_for_mind = [
            {"role": m["role"], "content": m["content"]}
            for m in session["messages"][:-1]
        ]
        mind_result = await asyncio.to_thread(
            _process_with_mind_sync,
            message.message,
            history_for_mind,
            is_private,
        )
        if mind_result.get("success"):
            response_text = mind_result["text"]
            mood = mind_result.get("mood", "excited")
            hooks = mind_result.get("hooks", [])
            model_used = f"mind+{mind_result.get('personality', 'megumin')}"
            mind_used = True
            logger.info(f"Mind: mood={mood}, personality={mind_result.get('personality')}")
        else:
            logger.warning(f"Mind failed: {mind_result.get('error')}, Fallback...")

    # ===== PFAD 2: PersonalityEngine =====
    if response_text is None and PERSONALITY_AVAILABLE:
        try:
            update_personality_state("interaction")
            if is_private:
                update_personality_state("kaetzchen_on")
            else:
                update_personality_state("kaetzchen_off")

            ollama_messages = _build_ollama_messages(session)
            response_text = await call_ollama_chat(ollama_messages, use_wizard=is_private)

            if response_text:
                response_text = process_personality_response(message.message, response_text)
                p_state = get_personality_state()
                mood = p_state.get("mood", "excited")
                model_used = "personality+ollama"
        except Exception as e:
            logger.error(f"Personality Fallback ERROR: {e}")
            response_text = None

    # ===== PFAD 3: Bare Ollama =====
    if response_text is None:
        ollama_messages = _build_ollama_messages(session)
        response_text = await call_ollama_chat(ollama_messages, use_wizard=is_private)
        if response_text:
            mood = _detect_mood_from_text(response_text)
            model_used = "ollama-direct"
        else:
            response_text = "Kuja! Ollama ist nicht gestartet... *traurig schau* Bitte starte 'ollama serve'!"
            mood = "sad"

    if not hooks:
        hooks = _build_hooks_from_mood(mood)

    # Response in Session
    session["messages"].append({
        "role": "assistant",
        "content": response_text,
        "timestamp": time.time(),
        "mood": mood,
    })

    # ChromaDB Memory Persistence
    if MEMORY_AVAILABLE and _memory_instance:
        try:
            room = "Schlafzimmer" if is_private else "Wohnzimmer"
            _memory_instance.add_conversation(
                user_message=message.message,
                najika_response=response_text,
                room=room,
                private_mode=is_private,
            )
        except Exception as e:
            logger.error(f"ChromaDB Save Fehler: {e}")

    # Shared State Memory (enhanced, aus lifespan)
    from backend.shared_state import NAJIKA_MEMORY
    if NAJIKA_MEMORY:
        try:
            NAJIKA_MEMORY.add_message("user", message.message)
            NAJIKA_MEMORY.add_message("assistant", response_text)
            rag_used = True
        except Exception as e:
            logger.error(f"Enhanced Memory Save Fehler: {e}")

    return ChatResponse(
        response=response_text,
        mode=message.mode,
        mood=mood,
        model_used=model_used,
        hooks=hooks,
        session_id=session_id,
        rag_used=rag_used,
        mind_used=mind_used,
        timestamp=time.time(),
    )


@router.post("/stream")
async def chat_stream_v2(message: ChatMessage):
    """Streaming Chat V2 - Token-by-Token SSE"""
    is_private = message.mode.lower() in ["private", "kaetzchen", "nsfw"]
    session_id, session = _get_or_create_session(message.session_id)
    session["messages"].append({
        "role": "user",
        "content": message.message,
        "timestamp": time.time(),
    })

    ollama_messages = _build_ollama_messages(session)
    accumulated = []

    async def generate():
        async for token in call_ollama_chat_stream(ollama_messages, use_wizard=is_private):
            accumulated.append(token)
            yield f"data: {json.dumps({'token': token})}\n\n"

        full_response = "".join(accumulated)
        session["messages"].append({
            "role": "assistant",
            "content": full_response,
            "timestamp": time.time(),
        })
        add_interaction()
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/health")
async def chat_health_v2():
    """Health-Check mit System-Status"""
    health = await check_ollama_health()
    health["mind_available"] = MIND_AVAILABLE
    health["personality_available"] = PERSONALITY_AVAILABLE
    health["memory_available"] = MEMORY_AVAILABLE
    health["version"] = "v2"
    return health


@router.get("/history")
async def chat_history_v2(session_id: str = None, limit: int = 50):
    """Chat History fuer eine Session"""
    if not session_id or session_id not in _conversations:
        return {"history": [], "count": 0, "session_id": session_id or ""}

    session = _conversations[session_id]
    messages = session["messages"][-limit:]

    history = []
    for msg in messages:
        history.append({
            "sender": "Mr.K" if msg["role"] == "user" else "Najika",
            "message": msg["content"],
            "timestamp": msg.get("timestamp", 0),
            "mood": msg.get("mood", ""),
        })

    return {"history": history, "count": len(history), "session_id": session_id}


@router.delete("/history")
async def clear_history_v2(session_id: str = None):
    """Chat History loeschen"""
    if session_id and session_id in _conversations:
        _conversations[session_id]["messages"] = []
        return {"success": True, "session_id": session_id}

    # Alle Sessions loeschen
    _conversations.clear()
    STATE["history"] = []
    return {"success": True, "message": "Alle Sessions geloescht"}


@router.post("/reset")
async def reset_conversation_v2():
    """Gespraech zuruecksetzen (inkl. Private Mode)"""
    _conversations.clear()
    STATE["history"] = []
    STATE["private_mode"] = False
    STATE["behavior_mode"] = "standard"
    return {"success": True}


@router.get("/sessions")
async def list_sessions_v2():
    """Aktive Sessions auflisten"""
    sessions = []
    for sid, s in _conversations.items():
        msg_count = len(s["messages"])
        last_msg = s["messages"][-1]["content"][:50] if msg_count > 0 else ""
        sessions.append({
            "session_id": sid,
            "messages": msg_count,
            "mode": s.get("mode", "public"),
            "last_active": s.get("last_active", 0),
            "preview": last_msg,
        })
    return {"sessions": sessions, "count": len(sessions)}
