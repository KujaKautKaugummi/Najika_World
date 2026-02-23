"""
Najika Chat API Router - Multi-Turn mit NajikaMind AGI-Orchester
Handles all chat interactions with Ollama via /api/chat (Multi-Turn!)

Integration:
- NajikaMind: 9-Schritt AGI-Pipeline (ToM → Memory → Feel → Facetten → Think → Speak → Express → Learn)
- PersonalityEngine: Mood, Persönlichkeits-Gewichtung, Sucht-Mechaniken, Psycho-Techniken
- Conversation History: In-Memory Store mit Session-IDs
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import asyncio
import time
import uuid
import sys
import os

from backend.utils import handle_errors

from backend.services.ollama_service import (
    call_ollama,
    call_ollama_chat,
    call_ollama_chat_sync,
    call_ollama_chat_stream,
    call_ollama_stream,
    check_ollama_health
)

# ===== NajikaMind AGI-Orchester (graceful fallback) =====
# NajikaMind ist in backend/ (nicht backend/api/), braucht sys.path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

MIND_AVAILABLE = False
PERSONALITY_AVAILABLE = False

try:
    from najika_mind import process_with_mind, MindResponse, get_mind
    MIND_AVAILABLE = True
    print("[CHAT] NajikaMind AGI-Orchester verfügbar")
except ImportError as e:
    print(f"[CHAT] NajikaMind nicht verfügbar: {e}")

try:
    from najika_personality_engine import (
        build_prompt as build_personality_prompt,
        process_response as process_personality_response,
        update_state as update_personality_state,
        get_state as get_personality_state
    )
    PERSONALITY_AVAILABLE = True
    print("[CHAT] PersonalityEngine verfügbar (Mood, Sucht, Psycho-Techniken)")
except ImportError as e:
    print(f"[CHAT] PersonalityEngine nicht verfügbar: {e}")

# ===== ChromaDB Memory Persistence =====
MEMORY_AVAILABLE = False
_memory_instance = None
try:
    from najika_memory import NajikaMemory
    _memory_instance = NajikaMemory()
    MEMORY_AVAILABLE = True
    print(f"[CHAT] ChromaDB Memory verfügbar ({_memory_instance.conversations.count()} Conversations)")
except Exception as e:
    print(f"[CHAT] ChromaDB Memory nicht verfügbar: {e}")

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# ===== IN-MEMORY CONVERSATION STORE =====
_conversations: Dict[str, dict] = {}
MAX_HISTORY_MESSAGES = 20     # Max Messages pro Session speichern
CONTEXT_WINDOW_MESSAGES = 10  # Letzte N Messages an Ollama senden

# Shared State für NajikaMind (simuliert najika_server.py STATE)
_mind_state: Dict[str, Any] = {
    "history": [],
    "bond_strength": 50,
    "behavior_mode": "standard",
    "personality_weights": {
        "megumin": 35, "harley": 25, "shiro": 20, "melissa": 20
    }
}


def _get_or_create_session(session_id: str = None) -> tuple:
    """Get existing session or create new one."""
    if not session_id or session_id not in _conversations:
        session_id = session_id or str(uuid.uuid4())[:8]
        _conversations[session_id] = {
            "messages": [],
            "created_at": time.time(),
            "last_active": time.time(),
            "mode": "public"
        }
    session = _conversations[session_id]
    session["last_active"] = time.time()
    return session_id, session


def _cleanup_old_sessions():
    """Entferne Sessions die älter als 24h sind"""
    now = time.time()
    expired = [sid for sid, s in _conversations.items() if now - s["last_active"] > 86400]
    for sid in expired:
        del _conversations[sid]


def _build_ollama_messages(session: dict, limit: int = CONTEXT_WINDOW_MESSAGES) -> list:
    """Baut Messages-Array für Ollama /api/chat aus Session-History"""
    messages = []
    for msg in session["messages"][-limit:]:
        content = msg["content"]
        if not content.strip():
            continue
        messages.append({
            "role": msg["role"],
            "content": content[:2000]  # Truncate lange Messages
        })
    return messages


def _detect_mood_from_text(text: str) -> str:
    """Fallback Mood-Detection aus Response-Text"""
    lower = text.lower()
    if "traurig" in lower or "😢" in text or "😔" in text:
        return "sad"
    elif "wütend" in lower or "😠" in text:
        return "angry"
    elif "müde" in lower or "😴" in text or "*gähn*" in lower:
        return "tired"
    elif "explosion" in lower or "EXPLOSION" in text:
        return "explosive"
    elif "glücklich" in lower or "💕" in text or "✨" in text:
        return "happy"
    elif "needy" in lower or "vermiss" in lower or "🥺" in text:
        return "needy"
    elif "dominant" in lower or "befehl" in lower:
        return "dominant"
    return "excited"


def _build_hooks_from_mood(mood: str) -> list:
    """Generiert Animation-Hooks basierend auf Mood"""
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


# ===== NAJIKAMIND BRIDGE (sync→async) =====

def _process_with_mind_sync(message: str, history: list, is_private: bool) -> dict:
    """
    Synchroner Wrapper für NajikaMind-Pipeline.
    Wird via asyncio.to_thread() aufgerufen.
    """
    # Prompt-Builder: KEIN History-Text hier!
    # History wird bereits über den 'context' Parameter als separate Messages gesendet.
    # Hier nur den User-Message als Kontext, damit NajikaMind darauf aufbauen kann.
    def _prompt_builder(hist, msg):
        return f"Kuja sagt: {msg}"

    # AI-Caller: nutzt call_ollama_chat_sync mit Messages-Array
    # WICHTIG: 'prompt' enthält den angereicherten NajikaMind-Kontext
    # (Personality, Memory, Whispers, RAG, Stil-Hinweise) und MUSS an Ollama!
    def _ai_caller(prompt, use_wizard, context, user_message):
        chat_messages = []

        # KEIN Kontext-Injection ins LLM!
        # Das 7B-Modell kann keine komplexen Kontext-Prompts verarbeiten ohne
        # Character-Breaks (echot Metadaten, generiert analytische Texte).
        # Die Modelfile hat bereits die komplette Najika-Persona als SYSTEM-Prompt.
        # NajikaMind's Wert = Routing + Mood + Post-Processing + Memory, NICHT Prompting.

        # History einfügen
        if context:
            for h in context[-8:]:
                content = h.get("content", "")
                if content.strip():
                    chat_messages.append({
                        "role": "user" if h.get("role") == "user" else "assistant",
                        "content": content[:2000]
                    })

        # Aktuelle User-Nachricht (sauber)
        if user_message:
            chat_messages.append({"role": "user", "content": user_message})

        result = call_ollama_chat_sync(chat_messages, use_wizard=use_wizard)
        return (result or "*blinzelt verwirrt* Ehm... Blackout!", "ollama")

    try:
        mind_response = process_with_mind(
            message=message,
            history=history,
            state=_mind_state,
            prompt_builder=_prompt_builder,
            ai_caller=_ai_caller,
            private_mode=is_private
        )

        return {
            "text": mind_response.text,
            "mood": mind_response.mood,
            "hooks": mind_response.hooks,
            "personality": mind_response.personality_dominant,
            "intent": mind_response.intent,
            "inner_thought": mind_response.inner_thought,
            "success": True
        }
    except Exception as e:
        print(f"[CHAT] NajikaMind ERROR: {e}")
        return {"success": False, "error": str(e)}


# ===== ENDPOINTS =====

class ChatMessage(BaseModel):
    message: str
    mode: str = "public"
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    mode: str
    mood: str = "excited"
    model_used: str = "ollama"
    hooks: List[Dict[str, Any]] = []
    session_id: str = ""


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse)
@handle_errors()
async def chat(message: ChatMessage):
    """
    Multi-Turn Chat mit NajikaMind AGI-Orchester

    - **message**: Kujas Nachricht
    - **mode**: "public" (SFW) oder "private"/"kaetzchen" (NSFW)
    - **session_id**: Optional - für Gesprächs-Kontinuität

    Pipeline: NajikaMind (9 Schritte) → PersonalityEngine → Sucht-Mechaniken → Response
    """
    # Cleanup alte Sessions gelegentlich
    if len(_conversations) > 100:
        _cleanup_old_sessions()

    is_private = message.mode.lower() in ["private", "kaetzchen", "nsfw"]

    # Session holen/erstellen
    session_id, session = _get_or_create_session(message.session_id)
    session["mode"] = message.mode

    # User-Message in History speichern
    session["messages"].append({
        "role": "user",
        "content": message.message,
        "timestamp": time.time()
    })
    # Max-History einhalten
    if len(session["messages"]) > MAX_HISTORY_MESSAGES:
        session["messages"] = session["messages"][-MAX_HISTORY_MESSAGES:]

    # Auch in _mind_state History syncen
    _mind_state["history"] = [
        {"role": m["role"], "content": m["content"]}
        for m in session["messages"]
    ]

    response_text = None
    mood = "excited"
    hooks = []
    model_used = "najika-nsfw" if is_private else "najika-local"

    # ===== PFAD 1: NajikaMind AGI-Pipeline =====
    if MIND_AVAILABLE:
        history_for_mind = [
            {"role": m["role"], "content": m["content"]}
            for m in session["messages"][:-1]  # Ohne die aktuelle User-Message
        ]

        mind_result = await asyncio.to_thread(
            _process_with_mind_sync,
            message.message,
            history_for_mind,
            is_private
        )

        if mind_result.get("success"):
            response_text = mind_result["text"]
            mood = mind_result.get("mood", "excited")
            hooks = mind_result.get("hooks", [])
            model_used = f"mind+{mind_result.get('personality', 'megumin')}"
            print(f"[CHAT] Mind: mood={mood}, personality={mind_result.get('personality')}, "
                  f"intent={mind_result.get('intent')}")
        else:
            print(f"[CHAT] Mind failed: {mind_result.get('error')}, Fallback...")

    # ===== PFAD 2: PersonalityEngine Fallback =====
    if response_text is None and PERSONALITY_AVAILABLE:
        try:
            update_personality_state("interaction")
            if is_private:
                update_personality_state("kaetzchen_on")
            else:
                update_personality_state("kaetzchen_off")

            # Ollama /api/chat mit Messages-Array
            ollama_messages = _build_ollama_messages(session)
            response_text = await call_ollama_chat(ollama_messages, use_wizard=is_private)

            if response_text:
                # Post-Processing mit Sucht/Psycho-Techniken
                response_text = process_personality_response(message.message, response_text)
                p_state = get_personality_state()
                mood = p_state.get("mood", "excited")
                model_used = "personality+ollama"
                print(f"[CHAT] Personality Fallback: mood={mood}")
        except Exception as e:
            print(f"[CHAT] Personality Fallback ERROR: {e}")
            response_text = None

    # ===== PFAD 3: Bare Ollama Fallback =====
    if response_text is None:
        ollama_messages = _build_ollama_messages(session)
        response_text = await call_ollama_chat(ollama_messages, use_wizard=is_private)

        if response_text:
            mood = _detect_mood_from_text(response_text)
            model_used = "ollama-direct"
        else:
            response_text = "Kuja! Ollama ist nicht gestartet... *traurig schau* Bitte starte 'ollama serve' für mich! 💔"
            mood = "sad"

    # Hooks generieren falls nicht von Mind gesetzt
    if not hooks:
        hooks = _build_hooks_from_mood(mood)

    # Najika-Response in Session-History speichern
    session["messages"].append({
        "role": "assistant",
        "content": response_text,
        "timestamp": time.time(),
        "mood": mood
    })

    # ChromaDB Memory Persistence - Konversation dauerhaft speichern
    if MEMORY_AVAILABLE and _memory_instance:
        try:
            room = "Schlafzimmer" if is_private else "Wohnzimmer"
            _memory_instance.add_conversation(
                user_message=message.message,
                najika_response=response_text,
                room=room,
                private_mode=is_private
            )
        except Exception as e:
            print(f"[CHAT] ChromaDB Save Fehler: {e}")

    return ChatResponse(
        response=response_text,
        mode=message.mode,
        mood=mood,
        model_used=model_used,
        hooks=hooks,
        session_id=session_id
    )


@router.post("/stream")
async def chat_stream(message: ChatMessage):
    """
    Streaming Multi-Turn Chat mit Ollama /api/chat

    Returns Server-Sent Events (SSE) mit Token-by-Token Response
    """
    is_private = message.mode.lower() in ["private", "kaetzchen", "nsfw"]

    # Session für History
    session_id, session = _get_or_create_session(message.session_id)
    session["messages"].append({
        "role": "user",
        "content": message.message,
        "timestamp": time.time()
    })

    # Messages-Array für Ollama
    ollama_messages = _build_ollama_messages(session)

    accumulated = []

    async def generate():
        async for token in call_ollama_chat_stream(ollama_messages, use_wizard=is_private):
            accumulated.append(token)
            yield f"data: {json.dumps({'token': token})}\n\n"

        # Response in History speichern
        full_response = "".join(accumulated)
        session["messages"].append({
            "role": "assistant",
            "content": full_response,
            "timestamp": time.time()
        })

        yield f"data: {json.dumps({'session_id': session_id})}\n\n"
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
@handle_errors()
async def chat_health():
    """Check if Ollama is running and Najika models are available"""
    health = await check_ollama_health()
    health["mind_available"] = MIND_AVAILABLE
    health["personality_available"] = PERSONALITY_AVAILABLE
    return health


@router.get("/models")
@handle_errors()
async def get_models():
    """Get information about Najika's Ollama models"""
    return {
        "backend": "ollama",
        "models": {
            "sfw": "najika-natural:latest",
            "nsfw": "najika-nsfw-natural:latest"
        },
        "mind_available": MIND_AVAILABLE,
        "personality_available": PERSONALITY_AVAILABLE,
        "info": "Personality baked into Modelfile + NajikaMind AGI-Orchester + Sucht-Mechaniken"
    }


@router.get("/history")
@handle_errors()
async def chat_history(session_id: str = None, limit: int = 50):
    """
    Get chat history for a session
    """
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
            "mood": msg.get("mood", "")
        })

    return {
        "history": history,
        "count": len(history),
        "session_id": session_id
    }


@router.get("/sessions")
@handle_errors()
async def list_sessions():
    """List active chat sessions"""
    sessions = []
    for sid, s in _conversations.items():
        msg_count = len(s["messages"])
        if msg_count > 0:
            last_msg = s["messages"][-1]["content"][:50]
        else:
            last_msg = ""
        sessions.append({
            "session_id": sid,
            "messages": msg_count,
            "mode": s.get("mode", "public"),
            "last_active": s.get("last_active", 0),
            "preview": last_msg
        })
    return {"sessions": sessions, "count": len(sessions)}
