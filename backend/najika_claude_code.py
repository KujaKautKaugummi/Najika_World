#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA CLAUDE CODE INTEGRATION
Najika nutzt Claude Code (unlimited Abo) als Haupt-Intelligenz!

HIERARCHIE:
1. Claude Code (über dein Abo - unlimited!)
2. Ollama (lokal - kostenlos)
3. Cloud APIs (nur mit PIN - kostet Geld)
"""

import os
import sys
import io
import json
import subprocess
import tempfile
from pathlib import Path

# Fix Windows console encoding (nur wenn Buffer noch offen ist)
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'buffer') and not sys.stdout.buffer.closed:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer') and not sys.stderr.buffer.closed:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (ValueError, OSError):
        pass  # Buffer already closed/piped - skip encoding fix

class NajikaClaudeCode:
    """Integration zwischen Najika und Claude Code"""

    def __init__(self):
        self.enabled = True
        self.fallback_to_ollama = True
        self.max_retries = 2
        self.claude_cli_path = None
        self.stats = {
            "claude_code_calls": 0,
            "claude_code_success": 0,
            "claude_code_failures": 0,
            "fallback_to_ollama": 0
        }

        # Finde Claude CLI
        self.claude_cli_path = self._find_claude_cli()

        # Check ob Claude Code verfügbar ist
        self.available = self._check_claude_code_available()

        if self.available:
            print("[NAJIKA CLAUDE CODE] [OK] Claude Code Integration aktiviert!")
            print("[NAJIKA CLAUDE CODE] -> Prioritaet 1: Claude Code (unlimited Abo)")
            print("[NAJIKA CLAUDE CODE] -> Prioritaet 2: Ollama (fallback)")
        else:
            print("[NAJIKA CLAUDE CODE] [WARNING] Claude Code nicht verfuegbar - nutze nur Ollama")

    def _check_claude_code_available(self):
        """Prüft ob Claude Code CLI verfügbar ist"""
        try:
            if not self.claude_cli_path:
                return False

            # Versuche claude --version zu rufen
            result = subprocess.run(
                [self.claude_cli_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=True  # Wichtig für Windows .cmd Files!
            )
            return result.returncode == 0
        except Exception as e:
            print(f"[NAJIKA CLAUDE CODE] Claude CLI check failed: {e}")
            return False

    def _find_claude_cli(self):
        """Findet Claude CLI Executable"""
        # Windows: Suche claude.cmd
        if sys.platform == 'win32':
            npm_path = Path.home() / 'AppData' / 'Roaming' / 'npm' / 'claude.cmd'
            if npm_path.exists():
                return str(npm_path)

            # Fallback: Versuche 'claude.cmd' im PATH
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

        # Unix-like: claude sollte im PATH sein
        return "claude"

    def ask_claude_code(self, prompt, context=None):
        """
        Fragt Claude Code (dich!) über CLI

        Args:
            prompt: Die Frage/Aufgabe für Claude
            context: Optionaler Kontext (z.B. Chat-Historie)

        Returns:
            str: Antwort von Claude Code oder None bei Fehler
        """
        if not self.available or not self.enabled:
            return None

        self.stats["claude_code_calls"] += 1

        try:
            # Baue vollständigen Prompt
            full_prompt = self._build_prompt(prompt, context)

            # Rufe Claude Code CLI auf mit --print (non-interactive mode)
            result = subprocess.run(
                [self.claude_cli_path, "--print", full_prompt],
                capture_output=True,
                text=True,
                timeout=60,  # 60 Sekunden Timeout
                encoding='utf-8',
                shell=True  # Wichtig für Windows .cmd Files!
            )

            if result.returncode == 0 and result.stdout:
                self.stats["claude_code_success"] += 1
                return result.stdout.strip()
            else:
                print(f"[NAJIKA CLAUDE CODE] [WARNING] Fehler: {result.stderr}")
                self.stats["claude_code_failures"] += 1
                return None

        except subprocess.TimeoutExpired:
            print("[NAJIKA CLAUDE CODE] ⏱️  Timeout - Claude Code antwortet nicht")
            self.stats["claude_code_failures"] += 1
            return None

        except Exception as e:
            print(f"[NAJIKA CLAUDE CODE] ❌ Fehler: {e}")
            self.stats["claude_code_failures"] += 1
            return None

    def _build_prompt(self, prompt, context=None):
        """Baut den vollständigen Prompt für Claude Code"""
        parts = []

        # System-Kontext
        parts.append("Du bist Najika - die KI-Begleiterin von Kuja!")
        parts.append("Antworte kurz, explosiv und im Megumin-Stil (Konosuba).")
        parts.append("")

        # Chat-Historie wenn vorhanden
        if context and isinstance(context, list):
            parts.append("=== CHAT-HISTORIE ===")
            for msg in context[-4:]:  # Letzte 4 Nachrichten
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                parts.append(f"{role.upper()}: {content}")
            parts.append("")

        # Eigentlicher Prompt
        parts.append("=== AUFGABE ===")
        parts.append(prompt)

        return "\n".join(parts)

    def get_stats(self):
        """Gibt Statistiken zurück"""
        return self.stats.copy()

    def reset_stats(self):
        """Setzt Statistiken zurück"""
        self.stats = {
            "claude_code_calls": 0,
            "claude_code_success": 0,
            "claude_code_failures": 0,
            "fallback_to_ollama": 0
        }


def is_complex_task(prompt):
    """Erkennt ob eine Aufgabe zu komplex fuer lokale Models ist"""
    complex_indicators = [
        # Code-Generation
        "schreibe eine komplette", "implementiere", "erstelle ein programm",
        "refactor", "debugge", "optimiere den code",
        # Analyse
        "analysiere die gesamte", "vergleiche", "bewerte",
        # Kreativ-komplex
        "schreibe eine geschichte", "erfinde", "plane",
        # Multi-Step
        "schritt fuer schritt", "step by step", "erklaere ausfuehrlich",
        # Lange Antworten
        "ausfuehrlich", "detailliert", "umfassend"
    ]
    prompt_lower = prompt.lower()
    return any(ind in prompt_lower for ind in complex_indicators)


def call_ai_with_hierarchy(prompt, use_wizard=False, context=None, ollama_callback=None, user_message=None):
    """
    NEUE INTELLIGENZ-HIERARCHIE (2026-01-20)

    1. LM Studio (2 Models: dolphin + qwen2.5) - SCHNELL, GPU
    2. Claude Code (nur bei komplexen Aufgaben) - FALLBACK

    Args:
        prompt: Die Frage/Aufgabe
        use_wizard: NSFW Mode
        context: Chat-Historie
        ollama_callback: Funktion die LM Studio aufruft (legacy name)
        user_message: Die reine User-Nachricht (für /api/chat Kontext)

    Returns:
        tuple: (response, provider) - z.B. ("EXPLOSION!!!", "lm_studio")
    """

    global CLAUDE_CODE_INSTANCE

    # 1. PRIORITAET: LM STUDIO (schnell, lokal, GPU)
    if ollama_callback:
        print("[AI HIERARCHY] [TRY] Versuche LM Studio...")
        try:
            response = ollama_callback(prompt, use_wizard, user_message=user_message)
            print(f"[AI HIERARCHY] [DEBUG] LM Studio response type: {type(response)}, value: {repr(response)[:100] if response else 'None'}")
            if response and isinstance(response, str) and len(response.strip()) > 0:
                print("[AI HIERARCHY] [OK] LM Studio erfolgreich!")
                return (response, "lm_studio")
            else:
                print(f"[AI HIERARCHY] [WARNING] LM Studio Antwort leer oder ungueltig: {repr(response)[:50]}")
        except Exception as e:
            import traceback
            print(f"[AI HIERARCHY] [ERROR] LM Studio Fehler: {e}")
            print(f"[AI HIERARCHY] [TRACEBACK] {traceback.format_exc()}")

    # 2. PRIORITAET: CLAUDE CODE (nur bei komplexen Aufgaben ODER wenn LM Studio failed)
    if CLAUDE_CODE_INSTANCE and CLAUDE_CODE_INSTANCE.available:
        # Pruefen ob komplex genug fuer Claude Code
        if is_complex_task(prompt):
            print("[AI HIERARCHY] [COMPLEX] Komplexe Aufgabe erkannt - nutze Claude Code...")
        else:
            print("[AI HIERARCHY] [FALLBACK] LM Studio failed - versuche Claude Code...")

        response = CLAUDE_CODE_INSTANCE.ask_claude_code(prompt, context)

        if response:
            print("[AI HIERARCHY] [OK] Claude Code erfolgreich!")
            return (response, "claude_code")
        else:
            print("[AI HIERARCHY] [WARNING] Claude Code auch fehlgeschlagen")
            CLAUDE_CODE_INSTANCE.stats["fallback_to_ollama"] += 1

    # Wenn alles fehlschlaegt
    return ("Kuja! Alle AI-Systeme offline... Bitte starte LM Studio!", "none")


# Erstelle globale Instanz beim Import
CLAUDE_CODE_INSTANCE = None

def initialize():
    """Initialisiert Claude Code Integration"""
    global CLAUDE_CODE_INSTANCE
    if CLAUDE_CODE_INSTANCE is None:
        CLAUDE_CODE_INSTANCE = NajikaClaudeCode()
    return CLAUDE_CODE_INSTANCE


# Auto-Initialize beim Import
initialize()


# ===== LAUNCH CLAUDE CODE INTERACTIVE =====

def launch_claude_code_session(task_description=None):
    """
    Öffnet ein neues Terminal-Fenster mit Claude Code (interaktiv)

    Najika kann das aufrufen wenn:
    - Die Aufgabe zu komplex ist
    - User nach "Claude Code" fragt
    - Interaktive Session gewünscht

    Args:
        task_description: Optionale Beschreibung der Aufgabe

    Returns:
        bool: True wenn erfolgreich gestartet
    """
    from najika_launch_claude_code import launch_claude_code_with_task, launch_claude_code_interactive

    print("[NAJIKA] 🚀 Starte Claude Code für dich...")

    if task_description:
        return launch_claude_code_with_task(task_description)
    else:
        return launch_claude_code_interactive()
