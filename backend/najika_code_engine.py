# =============================================================================
# NAJIKA CODE ENGINE - Multi-Model System für Code-Generierung
# =============================================================================
# OPTION 2: StarCoder2 für Code
# OPTION 3: Claude API Fallback für komplexe Tasks
#
# Optimiert für:
# - RTX 3060 Ti (8GB) - aktuell
# - Jetson AGX Orin 64GB - später (kann größere Modelle!)
# =============================================================================

import os
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Generator
from enum import Enum

# Versuche anthropic SDK zu importieren (für Claude API)
try:
    import anthropic
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("[CODE ENGINE] anthropic SDK nicht installiert - pip install anthropic")


class TaskComplexity(Enum):
    """Komplexitätsstufen für intelligentes Routing"""
    SIMPLE = "simple"      # Einfache Syntax, Einzeiler
    MEDIUM = "medium"      # Funktionen, kleine Klassen
    COMPLEX = "complex"    # Algorithmen, Architektur
    EXPERT = "expert"      # Multi-File, System Design


class CodeModel(Enum):
    """Verfügbare Code-Modelle"""
    STARCODER2_3B = "starcoder2:3b"       # Lokal, schnell, klein
    STARCODER2_7B = "starcoder2:7b"       # Lokal, besser
    STARCODER2_15B = "starcoder2:15b"     # Lokal, beste Qualität (Jetson Orin!)
    CODELLAMA_7B = "codellama:7b"         # Alternative
    CODELLAMA_13B = "codellama:13b"       # Größer
    QWEN_CODER_7B = "qwen2.5-coder:7b"    # Qwen Code-Variante
    CLAUDE_CLI = "claude-cli"             # Claude Code CLI (über Abo - KOSTENLOS!)
    CLAUDE_SONNET = "claude-sonnet-4-5"   # Cloud API (beste Qualität!)
    CLAUDE_HAIKU = "claude-haiku"         # Cloud API (schnell, günstig)


class NajikaCodeEngine:
    """
    Multi-Model Code Engine mit intelligentem Routing

    Routing-Logik:
    - SIMPLE/MEDIUM → StarCoder2 (lokal, schnell)
    - COMPLEX → StarCoder2 15B oder Claude Haiku
    - EXPERT → Claude Sonnet (beste Qualität)
    """

    def __init__(self):
        # Hardware Detection
        self.is_jetson = self._detect_jetson()
        self.available_vram = self._detect_vram()

        # Model Configuration
        self.primary_model = self._select_primary_model()
        self.fallback_model = CodeModel.CLAUDE_CLI  # Nutze Claude CLI über Abo!

        # Claude CLI Integration (über Abo - KOSTENLOS!)
        self.claude_cli_available = self._check_claude_cli()
        self.claude_cli_path = self._find_claude_cli()

        # API Keys (nur als Backup wenn CLI nicht verfügbar)
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.claude_client = None
        if CLAUDE_SDK_AVAILABLE and self.anthropic_key:
            self.claude_client = anthropic.Anthropic(api_key=self.anthropic_key)

        # Statistics
        self.stats = {
            "local_calls": 0,
            "cloud_calls": 0,
            "local_tokens": 0,
            "cloud_tokens": 0,
            "errors": 0,
            "cache_hits": 0
        }

        # Simple Response Cache (für wiederholte Anfragen)
        self.cache = {}
        self.cache_ttl = 3600  # 1 Stunde

        print(f"[CODE ENGINE] Initialisiert")
        print(f"  - Hardware: {'Jetson Orin' if self.is_jetson else 'PC/GPU'}")
        print(f"  - VRAM: {self.available_vram}GB")
        print(f"  - Primary Model: {self.primary_model.value}")
        print(f"  - Claude CLI: {'Verfügbar (über Abo!)' if self.claude_cli_available else 'Nicht verfügbar'}")
        print(f"  - Claude API: {'Verfügbar' if self.claude_client else 'Nicht konfiguriert'}")

    def _detect_jetson(self) -> bool:
        """Erkennt ob wir auf Jetson laufen"""
        try:
            with open("/etc/nv_tegra_release", "r") as f:
                return True
        except:
            return os.path.exists("/usr/local/cuda/targets/aarch64-linux")

    def _detect_vram(self) -> int:
        """Erkennt verfügbaren VRAM"""
        try:
            import torch
            if torch.cuda.is_available():
                props = torch.cuda.get_device_properties(0)
                return props.total_memory // (1024**3)  # GB
        except:
            pass

        # Jetson Orin hat shared memory
        if self.is_jetson:
            # Versuche aus /proc/meminfo zu lesen
            try:
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            mem_kb = int(line.split()[1])
                            return mem_kb // (1024**2)  # GB
            except:
                return 64  # Annahme: Orin 64GB

        return 8  # Fallback: 8GB (RTX 3060 Ti)

    def _select_primary_model(self) -> CodeModel:
        """Wählt das beste lokale Modell basierend auf Hardware"""
        if self.available_vram >= 48:
            # Jetson Orin 64GB oder high-end GPU
            return CodeModel.STARCODER2_15B
        elif self.available_vram >= 16:
            return CodeModel.STARCODER2_7B
        else:
            # RTX 3060 Ti (8GB)
            return CodeModel.STARCODER2_3B

    def _check_claude_cli(self) -> bool:
        """Prüft ob Claude CLI verfügbar ist"""
        import subprocess
        import sys
        try:
            cli_path = self._find_claude_cli()
            if not cli_path:
                return False
            result = subprocess.run(
                [cli_path, "--version"] if sys.platform != 'win32' else f'"{cli_path}" --version',
                capture_output=True,
                text=True,
                timeout=5,
                shell=True
            )
            return result.returncode == 0
        except:
            return False

    def _find_claude_cli(self) -> Optional[str]:
        """Findet Claude CLI Executable"""
        import sys
        from pathlib import Path

        if sys.platform == 'win32':
            # Windows: Suche claude.cmd im npm Pfad
            npm_path = Path.home() / 'AppData' / 'Roaming' / 'npm' / 'claude.cmd'
            if npm_path.exists():
                return str(npm_path)
            # Alternativ: claude.exe
            exe_path = Path.home() / 'AppData' / 'Roaming' / 'npm' / 'claude.exe'
            if exe_path.exists():
                return str(exe_path)
        else:
            # Unix: claude im PATH
            return "claude"
        return None

    def _estimate_complexity(self, prompt: str) -> TaskComplexity:
        """Schätzt die Komplexität einer Code-Anfrage"""
        prompt_lower = prompt.lower()

        # EXPERT Keywords
        expert_keywords = [
            "architecture", "system design", "multi-file", "refactor entire",
            "design pattern", "microservice", "database schema", "api design",
            "security audit", "performance optimization", "full implementation"
        ]
        if any(kw in prompt_lower for kw in expert_keywords):
            return TaskComplexity.EXPERT

        # COMPLEX Keywords
        complex_keywords = [
            "algorithm", "class", "implement", "create a", "build a",
            "recursive", "async", "threading", "decorator", "generator",
            "data structure", "binary", "tree", "graph", "sort"
        ]
        if any(kw in prompt_lower for kw in complex_keywords):
            return TaskComplexity.COMPLEX

        # MEDIUM Keywords
        medium_keywords = [
            "function", "method", "loop", "if", "for", "while",
            "list comprehension", "dictionary", "json", "file", "read", "write"
        ]
        if any(kw in prompt_lower for kw in medium_keywords):
            return TaskComplexity.MEDIUM

        # Default: SIMPLE
        return TaskComplexity.SIMPLE

    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generiert Cache-Key"""
        import hashlib
        return hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()

    def _check_cache(self, prompt: str, model: str) -> Optional[str]:
        """Prüft Cache auf vorherige Antwort"""
        key = self._get_cache_key(prompt, model)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["time"] < self.cache_ttl:
                self.stats["cache_hits"] += 1
                return entry["response"]
        return None

    def _save_cache(self, prompt: str, model: str, response: str):
        """Speichert Antwort im Cache"""
        key = self._get_cache_key(prompt, model)
        self.cache[key] = {"response": response, "time": time.time()}

        # Cache-Größe begrenzen (max 1000 Einträge)
        if len(self.cache) > 1000:
            oldest = min(self.cache.items(), key=lambda x: x[1]["time"])
            del self.cache[oldest[0]]

    def call_ollama_code(self, prompt: str, model: CodeModel = None) -> str:
        """Ruft lokales Code-Modell via Ollama auf"""
        if model is None:
            model = self.primary_model

        # Cache Check
        cached = self._check_cache(prompt, model.value)
        if cached:
            return cached

        # Code-spezifischer System-Prompt
        system_prompt = """Du bist ein Code-Assistent. Antworte NUR mit Code.
- Keine Erklärungen außer in Kommentaren
- Sauberer, lesbarer Code
- Best Practices befolgen
- Fehlerbehandlung wo nötig"""

        full_prompt = f"{system_prompt}\n\n{prompt}"

        payload = json.dumps({
            "model": model.value,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_ctx": 8192,  # Größerer Context für Code
                "temperature": 0.3,  # Niedriger für präziseren Code
                "top_p": 0.95,
                "repeat_penalty": 1.1
            }
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                response = result.get("response", "")

                self.stats["local_calls"] += 1
                self.stats["local_tokens"] += len(response.split())

                self._save_cache(prompt, model.value, response)
                return response

        except Exception as e:
            self.stats["errors"] += 1
            return f"[OLLAMA ERROR: {e}]"

    def call_claude_cli(self, prompt: str) -> str:
        """Ruft Claude CLI (über Abo) für Code-Generierung auf"""
        import subprocess

        if not self.claude_cli_available:
            return "[CLAUDE CLI ERROR: Nicht verfügbar]"

        # Cache Check
        cached = self._check_cache(prompt, "claude-cli")
        if cached:
            return cached

        try:
            # Verwende --print für non-interaktive Ausgabe
            code_prompt = f"""Generiere NUR Code als Antwort (keine Erklärungen außer Kommentare):

{prompt}

Antworte NUR mit dem Code, ohne Markdown-Blöcke."""

            result = subprocess.run(
                f'"{self.claude_cli_path}" --print "{code_prompt}"',
                capture_output=True,
                text=True,
                timeout=120,
                shell=True,
                encoding='utf-8'
            )

            if result.returncode == 0 and result.stdout:
                response = result.stdout.strip()
                self.stats["cloud_calls"] += 1  # Zählt als "cloud" weil externes Tool
                self._save_cache(prompt, "claude-cli", response)
                return response
            else:
                self.stats["errors"] += 1
                return f"[CLAUDE CLI ERROR: {result.stderr}]"

        except subprocess.TimeoutExpired:
            self.stats["errors"] += 1
            return "[CLAUDE CLI ERROR: Timeout]"
        except Exception as e:
            self.stats["errors"] += 1
            return f"[CLAUDE CLI ERROR: {e}]"

    def call_claude_code(self, prompt: str, model: CodeModel = CodeModel.CLAUDE_SONNET) -> str:
        """Ruft Claude API für Code-Generierung auf"""
        if not self.claude_client:
            return "[CLAUDE ERROR: API nicht konfiguriert - setze ANTHROPIC_API_KEY]"

        # Cache Check
        cached = self._check_cache(prompt, model.value)
        if cached:
            return cached

        # Model ID mapping
        model_ids = {
            CodeModel.CLAUDE_SONNET: "claude-sonnet-4-5-20250514",
            CodeModel.CLAUDE_HAIKU: "claude-3-haiku-20240307"
        }
        model_id = model_ids.get(model, "claude-sonnet-4-5-20250514")

        try:
            message = self.claude_client.messages.create(
                model=model_id,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Du bist ein Expert-Code-Assistent.

Aufgabe: {prompt}

Antworte mit sauberem, produktionsreifem Code.
Füge hilfreiche Kommentare hinzu.
Befolge Best Practices."""
                    }
                ]
            )

            response = message.content[0].text

            self.stats["cloud_calls"] += 1
            self.stats["cloud_tokens"] += message.usage.output_tokens

            self._save_cache(prompt, model.value, response)
            return response

        except Exception as e:
            self.stats["errors"] += 1
            return f"[CLAUDE ERROR: {e}]"

    def generate_code(self, prompt: str, force_cloud: bool = False) -> Dict[str, Any]:
        """
        Haupt-Methode für Code-Generierung mit intelligentem Routing

        Args:
            prompt: Die Code-Anfrage
            force_cloud: Erzwingt Claude API (für wichtige Tasks)

        Returns:
            Dict mit response, model_used, complexity, cached
        """
        # Komplexität schätzen
        complexity = self._estimate_complexity(prompt)

        # Routing-Entscheidung
        # PRIORITÄT: Claude CLI (über Abo) > StarCoder2 (lokal) > Claude API (backup)

        if force_cloud or complexity == TaskComplexity.EXPERT:
            # Nutze Claude CLI für komplexe Tasks (über Abo - KOSTENLOS!)
            if self.claude_cli_available:
                response = self.call_claude_cli(prompt)
                model_used = "claude-cli"
            elif self.claude_client:
                response = self.call_claude_code(prompt, CodeModel.CLAUDE_SONNET)
                model_used = "claude-sonnet"
            else:
                # Fallback zu bestem lokalen Modell
                response = self.call_ollama_code(prompt, self.primary_model)
                model_used = self.primary_model.value

        elif complexity == TaskComplexity.COMPLEX:
            # Versuche lokales Modell (StarCoder2)
            response = self.call_ollama_code(prompt, self.primary_model)
            model_used = self.primary_model.value

            # Wenn Antwort zu kurz oder fehlerhaft, nutze Claude CLI
            if len(response) < 50 or "ERROR" in response:
                if self.claude_cli_available:
                    response = self.call_claude_cli(prompt)
                    model_used = "claude-cli"
                elif self.claude_client:
                    response = self.call_claude_code(prompt, CodeModel.CLAUDE_HAIKU)
                    model_used = "claude-haiku"

        else:
            # SIMPLE/MEDIUM: Lokales Modell (StarCoder2)
            response = self.call_ollama_code(prompt, self.primary_model)
            model_used = self.primary_model.value

        return {
            "response": response,
            "model_used": model_used,
            "complexity": complexity.value,
            "cached": self._get_cache_key(prompt, model_used) in self.cache
        }

    def generate_code_stream(self, prompt: str) -> Generator[str, None, None]:
        """Streaming Code-Generierung (nur lokal)"""
        payload = json.dumps({
            "model": self.primary_model.value,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_ctx": 8192,
                "temperature": 0.3,
                "top_p": 0.95
            }
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                for line in resp:
                    if line:
                        try:
                            chunk = json.loads(line.decode("utf-8"))
                            if "response" in chunk:
                                yield chunk["response"]
                            if chunk.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            yield f"[STREAM ERROR: {e}]"

    def validate_python(self, code: str) -> Dict[str, Any]:
        """Validiert Python-Code syntaktisch"""
        try:
            compile(code, "<string>", "exec")
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax Error: {e.msg} (Line {e.lineno})"}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def get_stats(self) -> Dict[str, Any]:
        """Gibt Statistiken zurück"""
        return {
            **self.stats,
            "primary_model": self.primary_model.value,
            "is_jetson": self.is_jetson,
            "vram_gb": self.available_vram,
            "claude_cli_available": self.claude_cli_available,
            "claude_api_available": self.claude_client is not None,
            "cache_size": len(self.cache)
        }

    def setup_ollama_models(self) -> Dict[str, bool]:
        """Installiert benötigte Ollama-Modelle"""
        import subprocess

        models_to_install = []

        # Basierend auf Hardware
        if self.available_vram >= 48:
            models_to_install = ["starcoder2:15b", "starcoder2:7b"]
        elif self.available_vram >= 16:
            models_to_install = ["starcoder2:7b", "starcoder2:3b"]
        else:
            models_to_install = ["starcoder2:3b"]

        results = {}
        for model in models_to_install:
            try:
                print(f"[CODE ENGINE] Installiere {model}...")
                subprocess.run(["ollama", "pull", model], check=True, timeout=600)
                results[model] = True
                print(f"[CODE ENGINE] {model} installiert!")
            except Exception as e:
                results[model] = False
                print(f"[CODE ENGINE] Fehler bei {model}: {e}")

        return results


# =============================================================================
# NAJIKA INTEGRATION
# =============================================================================

class NajikaCodeAssistant:
    """
    Wrapper für Najika-Integration
    Kombiniert Code Engine mit Personality
    """

    def __init__(self, code_engine: NajikaCodeEngine):
        self.engine = code_engine
        self.personality_prefix = {
            "intro": [
                "*tippt aufgeregt auf die Tastatur* Code incoming!",
                "*leuchtet vor Begeisterung* Lass mich das programmieren!",
                "*Shiro-Modus aktiviert* Analysiere... Code wird generiert.",
                "EXPLOSION... äh, ich meine CODE! *kicher*"
            ],
            "success": [
                "*stolz präsentiert* Ta-da! Fertiger Code!",
                "*zufrieden nickend* Das sollte funktionieren, Mr.K!",
                "Perfekt! *macht V-Zeichen*",
                "*Shiro analytisch* Effizienz: 94.7%. Code complete."
            ],
            "error": [
                "*kratzt sich am Kopf* Hmm, das war knifflig...",
                "*schmollt* Der Code wollte nicht so wie ich...",
                "*seufzt* Auch Explosions-Magierin braucht manchmal Hilfe!"
            ]
        }

    def assist(self, prompt: str, force_cloud: bool = False) -> Dict[str, Any]:
        """
        Generiert Code mit Najika-Personality
        """
        import random

        # Intro
        intro = random.choice(self.personality_prefix["intro"])

        # Code generieren
        result = self.engine.generate_code(prompt, force_cloud)

        # Validation (nur für Python)
        if "python" in prompt.lower() or "def " in result["response"]:
            validation = self.engine.validate_python(result["response"])
        else:
            validation = {"valid": True, "error": None}

        # Outro basierend auf Erfolg
        if validation["valid"] and "ERROR" not in result["response"]:
            outro = random.choice(self.personality_prefix["success"])
        else:
            outro = random.choice(self.personality_prefix["error"])

        return {
            "intro": intro,
            "code": result["response"],
            "outro": outro,
            "model": result["model_used"],
            "complexity": result["complexity"],
            "validation": validation,
            "cached": result["cached"]
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Globale Instanz
CODE_ENGINE = None
CODE_ASSISTANT = None

def init_code_engine():
    """Initialisiert die Code Engine (einmal beim Server-Start aufrufen)"""
    global CODE_ENGINE, CODE_ASSISTANT

    CODE_ENGINE = NajikaCodeEngine()
    CODE_ASSISTANT = NajikaCodeAssistant(CODE_ENGINE)

    return CODE_ENGINE

def get_code_engine() -> NajikaCodeEngine:
    """Gibt die Code Engine Instanz zurück"""
    global CODE_ENGINE
    if CODE_ENGINE is None:
        init_code_engine()
    return CODE_ENGINE

def get_code_assistant() -> NajikaCodeAssistant:
    """Gibt den Code Assistant zurück"""
    global CODE_ASSISTANT
    if CODE_ASSISTANT is None:
        init_code_engine()
    return CODE_ASSISTANT


# =============================================================================
# CLI TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA CODE ENGINE - TEST")
    print("=" * 60)

    engine = init_code_engine()

    print("\n--- Stats ---")
    print(json.dumps(engine.get_stats(), indent=2))

    print("\n--- Test: Simple Code ---")
    result = engine.generate_code("Write a Python function to calculate factorial")
    print(f"Model: {result['model_used']}")
    print(f"Complexity: {result['complexity']}")
    print(f"Code:\n{result['response'][:500]}...")

    print("\n--- Test: With Personality ---")
    assistant = get_code_assistant()
    result = assistant.assist("Create a Python class for a Stack data structure")
    print(f"Intro: {result['intro']}")
    print(f"Code:\n{result['code'][:500]}...")
    print(f"Outro: {result['outro']}")
    print(f"Valid: {result['validation']['valid']}")
