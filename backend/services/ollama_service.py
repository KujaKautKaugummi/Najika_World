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

# Najika Models - Q4_K_M quantisiert (passen in 8GB VRAM!)
# F16-Modelle (najika-trained, najika-nsfw-trained) sind 16GB = zu groß!
# Persona ist im Modelfile eingebaut = kein extra Context overhead!
OLLAMA_MODELS = {
    "chat": "najika-natural:latest",          # SFW Chat - bereinigtes Modelfile (natuerlicher!)
    "nsfw": "najika-nsfw-natural:latest",     # NSFW/Kätzchen-Modus - bereinigtes Modelfile!
    "instruct": "qwen2:7b"                   # Tasks, Code, Mathe
}


def is_task_request(text: str) -> bool:
    """Erkennt ob eine Nachricht ein Task-Request ist (braucht Instruct-Model)

    WICHTIG: Nur echte technische Tasks! Normale Fragen wie "Was ist dein Lieblingszauber?"
    sind KEINE Tasks und sollen von Najika beantwortet werden!
    """
    task_keywords = [
        "zaehle", "zähle", "berechne", "rechne",
        "programmiere", "schreibe code", "funktion", "python", "javascript",
        "fasse zusammen", "uebersetze", "übersetze",
        "konvertiere", "formatiere", "sortiere",
        "beschreibe technisch"
    ]
    text_lower = text.lower()
    # Nur matchen wenn der Task-Keyword am Anfang steht (als Befehl)
    # oder wenn die Nachricht sehr kurz und technisch ist
    for kw in task_keywords:
        if text_lower.startswith(kw) or f" {kw} " in f" {text_lower} ":
            # Ausschluss: Fragen die mit "dein/deine/dir" persönlich sind
            if any(p in text_lower for p in ["dein", "deine", "dir", "du", "najika"]):
                return False
            return True
    return False


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
        num_predict = 600
    else:
        temperature = 0.70
        num_predict = 400

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
            "repeat_penalty": 1.35,
            "repeat_last_n": 256,
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
        num_predict = 600
    else:
        temperature = 0.70
        num_predict = 400

    use_system = model == OLLAMA_MODELS["instruct"]

    payload = {
        "model": model,
        "prompt": prompt[:4000],
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "repeat_penalty": 1.35,
            "repeat_last_n": 256,
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


# ===== MULTI-TURN CHAT FUNCTIONS (Ollama /api/chat) =====
# KRITISCH: /api/chat nutzt die MESSAGE-Examples aus der Modelfile!
# /api/generate ignoriert sie → darum klang Najika vorher so schlecht!

async def call_ollama_chat(messages: list, use_wizard: bool = False) -> Optional[str]:
    """
    Multi-Turn Chat via Ollama /api/chat

    Args:
        messages: Chat-Verlauf als [{"role": "user"|"assistant", "content": "..."}]
        use_wizard: True für NSFW/Kätzchen-Modus

    Returns:
        Najika's Antwort oder None bei Fehler
    """
    # Model aus letzter User-Nachricht bestimmen
    last_user_msg = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user_msg = m["content"]
            break

    model = select_model(last_user_msg, use_wizard)
    timeout = 120

    if use_wizard:
        temperature = 0.85
        num_predict = 600
    else:
        temperature = 0.70
        num_predict = 400

    # KEIN system-Message für Najika-Modelle! Persona ist in Modelfile eingebaut.
    # Ein system hier würde die Modelfile-SYSTEM-Message ÜBERSCHREIBEN!
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "repeat_penalty": 1.35,
            "repeat_last_n": 256,
            "top_p": 0.9,
            "num_ctx": 8192
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("message", {}).get("content", "")
            print(f"[OLLAMA CHAT] Model: {model} - OK ({len(content)} chars)")
            return content

    except Exception as e:
        print(f"[OLLAMA CHAT] ERROR: {e}, Fallback auf /api/generate...")
        # Fallback: /api/generate mit letzter Nachricht
        try:
            fallback_prompt = last_user_msg[:4000] if last_user_msg else "Hallo!"
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": model,
                        "prompt": fallback_prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": num_predict,
                            "repeat_penalty": 1.35,
                            "repeat_last_n": 256,
                            "top_p": 0.9,
                            "num_ctx": 8192
                        }
                    },
                    timeout=timeout
                )
                response.raise_for_status()
                data = response.json()
                content = data.get("response", "")
                print(f"[OLLAMA GENERATE FALLBACK] Model: {model} - OK")
                return content
        except Exception as e2:
            print(f"[OLLAMA] Fallback auch fehlgeschlagen: {e2}")
            return None


def call_ollama_chat_sync(messages: list, use_wizard: bool = False) -> Optional[str]:
    """
    Synchrone Version von call_ollama_chat für NajikaMind-Callbacks.
    NajikaMind.process() ist synchron, braucht daher synchronen AI-Caller.
    """
    last_user_msg = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user_msg = m["content"]
            break

    model = select_model(last_user_msg, use_wizard)
    timeout = 120

    if use_wizard:
        temperature = 0.85
        num_predict = 600
    else:
        temperature = 0.70
        num_predict = 400

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "repeat_penalty": 1.35,
            "repeat_last_n": 256,
            "top_p": 0.9,
            "num_ctx": 8192
        }
    }

    try:
        with httpx.Client() as client:
            response = client.post(
                f"{OLLAMA_URL}/api/chat",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("message", {}).get("content", "")
            print(f"[OLLAMA CHAT SYNC] Model: {model} - OK ({len(content)} chars)")
            return content

    except Exception as e:
        print(f"[OLLAMA CHAT SYNC] ERROR: {e}, Fallback...")
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": model,
                        "prompt": last_user_msg[:4000] if last_user_msg else "Hallo!",
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": num_predict,
                        }
                    },
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json().get("response", "")
        except Exception as e2:
            print(f"[OLLAMA SYNC] Fallback fehlgeschlagen: {e2}")
            return None


async def call_ollama_chat_stream(messages: list, use_wizard: bool = False) -> AsyncGenerator[str, None]:
    """
    Streaming Multi-Turn Chat via Ollama /api/chat

    Args:
        messages: Chat-Verlauf als Messages-Array
        use_wizard: True für NSFW/Kätzchen-Modus

    Yields:
        Tokens der Antwort
    """
    last_user_msg = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user_msg = m["content"]
            break

    model = select_model(last_user_msg, use_wizard)

    if use_wizard:
        temperature = 0.85
        num_predict = 600
    else:
        temperature = 0.70
        num_predict = 400

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "repeat_penalty": 1.35,
            "repeat_last_n": 256,
            "top_p": 0.9,
            "num_ctx": 8192
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/chat",
                json=payload,
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
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

                # Check ob unsere trainierten Q4 Modelle da sind
                najika_local_ok = any("najika-natural" in m for m in available_models)
                najika_nsfw_ok = any("najika-nsfw-natural" in m for m in available_models)

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
