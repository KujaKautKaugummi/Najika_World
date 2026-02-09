"""
Ollama Service for Najika
Backend: 100% Ollama (LM Studio removed)
Models: dolphin-qwen2 (Chat) + qwen2-instruct (Tasks)
"""

import httpx
import json
from typing import Optional, AsyncGenerator

# ===== OLLAMA CONFIGURATION =====
OLLAMA_URL = "http://localhost:11434"

# Najika Models - alle basieren auf Qwen2 Familie
# Persona ist im Modelfile eingebaut = kein extra Context overhead!
OLLAMA_MODELS = {
    "chat": "najika-local",      # SFW Chat (dolphin-qwen2 + Najika Persona)
    "nsfw": "najika-nsfw",       # NSFW/Kätzchen-Modus (dolphin-qwen2 + NSFW Persona)
    "instruct": "qwen2-instruct" # Tasks, Code, Mathe (Qwen2.5 Instruct Uncensored)
}


def is_task_request(text: str) -> bool:
    """Erkennt ob eine Nachricht ein Task-Request ist (braucht Instruct-Model)"""
    task_keywords = [
        "zaehle", "zähle", "berechne", "rechne", "liste", "erklaere", "erklär",
        "code", "programmiere", "schreibe code", "funktion", "python", "javascript",
        "analysiere", "zusammenfassung", "fasse zusammen", "uebersetze", "übersetze",
        "konvertiere", "formatiere", "sortiere", "finde", "suche nach", "wie viel",
        "was ist", "definiere", "beschreibe technisch"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in task_keywords)


def select_model(prompt: str, use_wizard: bool = False) -> str:
    """Waehlt das richtige Ollama Model basierend auf dem Prompt"""
    # NSFW/Kaetzchen-Modus -> najika-nsfw
    if use_wizard:
        return OLLAMA_MODELS["nsfw"]

    # Task-Request -> qwen2.5 basis
    if is_task_request(prompt):
        return OLLAMA_MODELS["instruct"]

    # Normal Chat -> najika-local
    return OLLAMA_MODELS["chat"]


async def call_ollama(prompt: str, use_wizard: bool = False) -> Optional[str]:
    """
    Ruft Ollama API auf

    Args:
        prompt: Die Nachricht des Users
        use_wizard: True für NSFW/Kaetzchen-Modus

    Returns:
        Najika's Antwort oder None bei Fehler
    """
    model = select_model(prompt, use_wizard)
    timeout = 120  # Ollama kann langsamer sein als LM Studio

    # NSFW/Kaetzchen-Modus: Optimierte Parameter
    if use_wizard:
        temperature = 0.85
        num_predict = 300
    else:
        temperature = 0.70
        num_predict = 150  # KURZ!

    # Najika-Modelle haben Persona eingebaut, instruct braucht sie
    use_system = model == OLLAMA_MODELS["instruct"]

    # Ollama /api/generate Format
    payload = {
        "model": model,
        "prompt": prompt[:4000],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "repeat_penalty": 1.1,
            "top_p": 0.9,
            "num_ctx": 8192
        }
    }

    # System-Prompt nur fuer instruct-model (Najika-Modelle haben es eingebaut)
    if use_system:
        payload["system"] = "Du bist Najika, eine hilfreiche KI-Assistentin. Antworte auf Deutsch, kurz und präzise."

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()

            content = data.get("response", "")
            print(f"[OLLAMA] Model: {model} - OK")
            return content

    except Exception as e:
        print(f"[OLLAMA] ERROR: {e}")
        return None


async def call_ollama_stream(prompt: str, use_wizard: bool = False) -> AsyncGenerator[str, None]:
    """
    Streamt Ollama Response Token für Token

    Args:
        prompt: Die Nachricht des Users
        use_wizard: True für NSFW/Kaetzchen-Modus

    Yields:
        Tokens der Antwort
    """
    model = select_model(prompt, use_wizard)

    # NSFW/Kaetzchen-Modus: Optimierte Parameter
    if use_wizard:
        temperature = 0.85
        num_predict = 300
    else:
        temperature = 0.70
        num_predict = 150

    use_system = model == OLLAMA_MODELS["instruct"]

    payload = {
        "model": model,
        "prompt": prompt[:4000],
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "repeat_penalty": 1.1,
            "top_p": 0.9,
            "num_ctx": 8192
        }
    }

    if use_system:
        payload["system"] = "Du bist Najika, eine hilfreiche KI-Assistentin. Antworte auf Deutsch, kurz und präzise."

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("response", "")
                            if content:
                                yield content
                            if chunk.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue

    except Exception as e:
        yield f"[ERROR: {e}]"


async def check_ollama_health() -> dict:
    """Prüft ob Ollama erreichbar ist und welche Modelle geladen sind"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                available_models = [m["name"] for m in data.get("models", [])]

                # Check ob unsere Modelle da sind
                najika_local_ok = any("najika-local" in m for m in available_models)
                najika_nsfw_ok = any("najika-nsfw" in m for m in available_models)

                return {
                    "status": "online",
                    "url": OLLAMA_URL,
                    "models": OLLAMA_MODELS,
                    "available": available_models,
                    "najika_local": najika_local_ok,
                    "najika_nsfw": najika_nsfw_ok
                }
    except:
        pass

    return {
        "status": "offline",
        "url": OLLAMA_URL,
        "error": "Ollama nicht erreichbar - bitte 'ollama serve' starten"
    }


async def ensure_model_loaded(model_name: str) -> bool:
    """Stellt sicher dass ein Model geladen ist (Ollama lädt on-demand)"""
    try:
        async with httpx.AsyncClient() as client:
            # Ollama lädt Models automatisch beim ersten Request
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": model_name,
                    "prompt": "test",
                    "stream": False,
                    "options": {"num_predict": 1}
                },
                timeout=60.0
            )
            return response.status_code == 200
    except:
        return False
