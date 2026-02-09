#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA AI HIERARCHIE - Multi-Model System

HIERARCHIE (KORREKT!):
1. Qwen 2.5 (7B) - Normale Chats, schnell
2. StarCoder2 (3B) - Code-Aufgaben
3. Claude Code - Komplexe Aufgaben (wenn nötig)

KÄTZCHEN-MODUS:
→ DIREKT zu Ollama najika-wizard (NSFW ohne Filter!)
"""

import os
import sys
import io
import json
import subprocess
import tempfile
import re
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================
# OLLAMA MODEL CONFIGURATION
# ============================================

OLLAMA_MODELS = {
    "chat": "qwen2.5:7b",           # Normale Chats
    "code": "starcoder2:3b",         # Code-Aufgaben
    "wizard": "najika-wizard",       # NSFW (Kätzchen-Modus)
    "fallback": "najika-local"       # Fallback
}

# ============================================
# CODE DETECTION
# ============================================

CODE_KEYWORDS = [
    # Programmier-Begriffe
    "code", "programmier", "funktion", "function", "class", "klasse",
    "variable", "array", "loop", "schleife", "if", "else", "switch",
    "return", "import", "export", "module", "api", "endpoint",
    "bug", "fix", "fehler", "error", "debug", "test",
    # Sprachen
    "python", "javascript", "js", "typescript", "ts", "java", "c++",
    "html", "css", "sql", "bash", "shell", "powershell",
    # Frameworks
    "react", "vue", "angular", "node", "express", "django", "flask",
    "three.js", "threejs", "webgl", "canvas",
    # Aktionen
    "schreib", "erstell", "implementier", "refactor", "optimier",
    "write", "create", "implement", "build", "make",
    # Datei-Endungen
    ".py", ".js", ".ts", ".html", ".css", ".json", ".md"
]

COMPLEX_KEYWORDS = [
    # Komplexe Aufgaben die Claude Code brauchen
    "architektur", "design", "struktur", "konzept", "plan",
    "erkläre ausführlich", "analysiere", "vergleiche",
    "pro und contra", "vor und nachteile",
    "refactor komplett", "umstrukturier",
    "claude code", "claude", "hilfe bei"
]

def detect_task_type(prompt):
    """
    Erkennt den Aufgabentyp aus dem Prompt

    Returns:
        str: "chat", "code", oder "complex"
    """
    prompt_lower = prompt.lower()

    # Check für komplexe Aufgaben (Claude Code)
    for keyword in COMPLEX_KEYWORDS:
        if keyword in prompt_lower:
            return "complex"

    # Check für Code-Aufgaben (StarCoder2)
    code_score = 0
    for keyword in CODE_KEYWORDS:
        if keyword in prompt_lower:
            code_score += 1

    # Wenn Code-Blöcke im Prompt
    if "```" in prompt or "def " in prompt or "function " in prompt:
        code_score += 3

    if code_score >= 2:
        return "code"

    # Default: Chat (Qwen)
    return "chat"


# ============================================
# CLAUDE CODE INTEGRATION (für komplexe Aufgaben)
# ============================================

class NajikaClaudeCode:
    """Integration zwischen Najika und Claude Code"""

    def __init__(self):
        self.enabled = True
        self.max_retries = 2
        self.claude_cli_path = None
        self.stats = {
            "claude_code_calls": 0,
            "claude_code_success": 0,
            "claude_code_failures": 0,
            "qwen_calls": 0,
            "starcoder_calls": 0,
            "wizard_calls": 0
        }

        # Finde Claude CLI
        self.claude_cli_path = self._find_claude_cli()
        self.available = self._check_claude_code_available()

        print("[NAJIKA AI] ========================================")
        print("[NAJIKA AI] HIERARCHIE AKTIV:")
        print("[NAJIKA AI]   1. Qwen 2.5 (7B) - Chats")
        print("[NAJIKA AI]   2. StarCoder2 (3B) - Code")
        print("[NAJIKA AI]   3. Claude Code - Komplex")
        print("[NAJIKA AI]   * najika-wizard - Kätzchen-Modus")
        if self.available:
            print("[NAJIKA AI] [OK] Claude Code verfügbar!")
        else:
            print("[NAJIKA AI] [INFO] Claude Code nicht verfügbar")
        print("[NAJIKA AI] ========================================")

    def _check_claude_code_available(self):
        """Prüft ob Claude Code CLI verfügbar ist"""
        try:
            if not self.claude_cli_path:
                return False

            result = subprocess.run(
                [self.claude_cli_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=True
            )
            return result.returncode == 0
        except Exception as e:
            return False

    def _find_claude_cli(self):
        """Findet Claude CLI Executable"""
        if sys.platform == 'win32':
            npm_path = Path.home() / 'AppData' / 'Roaming' / 'npm' / 'claude.cmd'
            if npm_path.exists():
                return str(npm_path)

            try:
                result = subprocess.run(
                    ["where", "claude.cmd"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                if result.returncode == 0 and result.stdout:
                    return result.stdout.strip().split('\n')[0]
            except:
                pass

        return "claude"

    def ask_claude_code(self, prompt, context=None):
        """Fragt Claude Code für komplexe Aufgaben"""
        if not self.available or not self.enabled:
            return None

        self.stats["claude_code_calls"] += 1

        try:
            full_prompt = self._build_prompt(prompt, context)

            result = subprocess.run(
                [self.claude_cli_path, "--print", full_prompt],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                shell=True
            )

            if result.returncode == 0 and result.stdout:
                self.stats["claude_code_success"] += 1
                return result.stdout.strip()
            else:
                self.stats["claude_code_failures"] += 1
                return None

        except subprocess.TimeoutExpired:
            self.stats["claude_code_failures"] += 1
            return None
        except Exception as e:
            self.stats["claude_code_failures"] += 1
            return None

    def _build_prompt(self, prompt, context=None):
        """Baut den Prompt für Claude Code"""
        parts = []
        parts.append("Du bist Najika - die KI-Begleiterin von Kuja!")
        parts.append("Antworte kurz, explosiv und im Megumin-Stil (Konosuba).")
        parts.append("")

        if context and isinstance(context, list):
            parts.append("=== CHAT-HISTORIE ===")
            for msg in context[-4:]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                parts.append(f"{role.upper()}: {content}")
            parts.append("")

        parts.append("=== AUFGABE ===")
        parts.append(prompt)

        return "\n".join(parts)

    def get_stats(self):
        return self.stats.copy()


# ============================================
# HAUPT-HIERARCHIE FUNKTION
# ============================================

def call_ai_with_hierarchy(prompt, use_wizard=False, context=None, ollama_callback=None):
    """
    INTELLIGENZ-HIERARCHIE (KORREKT!)

    KÄTZCHEN-MODUS (use_wizard=True):
        → DIREKT zu Ollama najika-wizard (NSFW!)

    NORMAL-MODUS (use_wizard=False):
        1. Erkennung: Chat, Code, oder Komplex?
        2. Chat → Qwen 2.5 (7B)
        3. Code → StarCoder2 (3B)
        4. Komplex → Claude Code (falls verfügbar)

    Args:
        prompt: Die Frage/Aufgabe
        use_wizard: NSFW Mode - BYPASSED alles!
        context: Chat-Historie
        ollama_callback: Funktion die Ollama aufruft (model, prompt, use_wizard)

    Returns:
        tuple: (response, provider)
    """
    global CLAUDE_CODE_INSTANCE

    # ===== KÄTZCHEN-MODUS: DIREKT ZU WIZARD =====
    if use_wizard:
        if ollama_callback:
            print("[AI] [KÄTZCHEN] → najika-wizard (NSFW)")
            CLAUDE_CODE_INSTANCE.stats["wizard_calls"] += 1
            response = ollama_callback(prompt, True, None)  # use_wizard=True
            return (response, "ollama_wizard")
        else:
            return ("ERROR: Ollama nicht verfügbar!", "none")

    # ===== NORMAL-MODUS: Aufgabentyp erkennen =====
    task_type = detect_task_type(prompt)
    print(f"[AI] Erkannter Typ: {task_type.upper()}")

    # ===== 1. CHAT → QWEN =====
    if task_type == "chat":
        if ollama_callback:
            print(f"[AI] [CHAT] → {OLLAMA_MODELS['chat']}")
            CLAUDE_CODE_INSTANCE.stats["qwen_calls"] += 1
            response = ollama_callback(prompt, False, OLLAMA_MODELS['chat'])
            return (response, "qwen")

    # ===== 2. CODE → STARCODER2 =====
    if task_type == "code":
        if ollama_callback:
            print(f"[AI] [CODE] → {OLLAMA_MODELS['code']}")
            CLAUDE_CODE_INSTANCE.stats["starcoder_calls"] += 1
            response = ollama_callback(prompt, False, OLLAMA_MODELS['code'])
            return (response, "starcoder2")

    # ===== 3. KOMPLEX → CLAUDE CODE =====
    if task_type == "complex":
        if CLAUDE_CODE_INSTANCE and CLAUDE_CODE_INSTANCE.available:
            print("[AI] [KOMPLEX] → Claude Code")
            response = CLAUDE_CODE_INSTANCE.ask_claude_code(prompt, context)
            if response:
                return (response, "claude_code")
            print("[AI] [WARNING] Claude Code fehlgeschlagen - Fallback zu Qwen")

    # ===== FALLBACK: QWEN =====
    if ollama_callback:
        print(f"[AI] [FALLBACK] → {OLLAMA_MODELS['chat']}")
        response = ollama_callback(prompt, False, OLLAMA_MODELS['chat'])
        return (response, "qwen_fallback")

    return ("ERROR: Keine AI verfügbar!", "none")


# ============================================
# GLOBALE INSTANZ
# ============================================

CLAUDE_CODE_INSTANCE = None

def initialize():
    """Initialisiert AI System"""
    global CLAUDE_CODE_INSTANCE
    if CLAUDE_CODE_INSTANCE is None:
        CLAUDE_CODE_INSTANCE = NajikaClaudeCode()
    return CLAUDE_CODE_INSTANCE

# Auto-Initialize beim Import
initialize()


# ============================================
# LAUNCH CLAUDE CODE INTERACTIVE
# ============================================

def launch_claude_code_session(task_description=None):
    """Öffnet Claude Code interaktiv"""
    try:
        from najika_launch_claude_code import launch_claude_code_with_task, launch_claude_code_interactive

        print("[NAJIKA] Starte Claude Code...")

        if task_description:
            return launch_claude_code_with_task(task_description)
        else:
            return launch_claude_code_interactive()
    except ImportError:
        print("[NAJIKA] Claude Code Launcher nicht verfügbar")
        return False
