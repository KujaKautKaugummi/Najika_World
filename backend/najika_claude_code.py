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

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class NajikaClaudeCode:
    """Integration zwischen Najika und Claude Code"""

    def __init__(self):
        self.enabled = True
        self.fallback_to_ollama = True
        self.max_retries = 2
        self.stats = {
            "claude_code_calls": 0,
            "claude_code_success": 0,
            "claude_code_failures": 0,
            "fallback_to_ollama": 0
        }

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
            # Versuche claude --version zu rufen
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            print(f"[NAJIKA CLAUDE CODE] Claude CLI check failed: {e}")
            return False

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

            # Erstelle temporäre Datei für den Prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                temp_file = f.name
                f.write(full_prompt)

            try:
                # Rufe Claude Code CLI auf
                result = subprocess.run(
                    ["claude", "--non-interactive", "--input", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=60,  # 60 Sekunden Timeout
                    encoding='utf-8'
                )

                if result.returncode == 0 and result.stdout:
                    self.stats["claude_code_success"] += 1
                    return result.stdout.strip()
                else:
                    print(f"[NAJIKA CLAUDE CODE] [WARNING] Fehler: {result.stderr}")
                    self.stats["claude_code_failures"] += 1
                    return None

            finally:
                # Lösche temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass

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


def call_ai_with_hierarchy(prompt, use_wizard=False, context=None, ollama_callback=None):
    """
    INTELLIGENZ-HIERARCHIE

    1. Versuche Claude Code (unlimited!)
    2. Falls nicht verfügbar/Fehler → Ollama
    3. Cloud APIs nur mit PIN (separates System)

    Args:
        prompt: Die Frage/Aufgabe
        use_wizard: NSFW Mode für Ollama
        context: Chat-Historie
        ollama_callback: Funktion die Ollama aufruft

    Returns:
        tuple: (response, provider) - z.B. ("EXPLOSION!!!", "claude_code")
    """

    # Globale Claude Code Instanz (wird beim Import erstellt)
    global CLAUDE_CODE_INSTANCE

    # 1. PRIORITAET: CLAUDE CODE
    if CLAUDE_CODE_INSTANCE and CLAUDE_CODE_INSTANCE.available:
        print("[AI HIERARCHY] [TRY] Versuche Claude Code...")
        response = CLAUDE_CODE_INSTANCE.ask_claude_code(prompt, context)

        if response:
            print("[AI HIERARCHY] [OK] Claude Code erfolgreich!")
            return (response, "claude_code")
        else:
            print("[AI HIERARCHY] [WARNING] Claude Code fehlgeschlagen - fallback zu Ollama")
            CLAUDE_CODE_INSTANCE.stats["fallback_to_ollama"] += 1

    # 2. PRIORITAET: OLLAMA (FALLBACK)
    if ollama_callback:
        print("[AI HIERARCHY] [FALLBACK] Nutze Ollama...")
        response = ollama_callback(prompt, use_wizard)
        return (response, "ollama")

    # Sollte nicht passieren
    return ("ERROR: Keine AI verfügbar!", "none")


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
