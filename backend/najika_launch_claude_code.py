#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA LAUNCH CLAUDE CODE - EIGENSTÄNDIG!
Najika kann selbst ein neues Claude Code Terminal öffnen!
"""

import subprocess
import sys
import os
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def launch_claude_code_interactive(initial_message=None):
    """
    Öffnet ein neues Terminal-Fenster mit Claude Code (interaktiv)

    Args:
        initial_message: Optionale erste Nachricht an Claude

    Returns:
        bool: True wenn erfolgreich gestartet
    """

    try:
        # Finde Claude CLI
        claude_cli = _find_claude_cli()
        if not claude_cli:
            print("[NAJIKA LAUNCH] ❌ Claude CLI nicht gefunden!")
            return False

        # Windows: Öffne neues PowerShell-Fenster mit Claude
        if sys.platform == 'win32':
            # Baue PowerShell Command
            if initial_message:
                # Mit initialer Nachricht
                ps_command = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {{ Write-Host \'NAJIKA hat Claude Code für dich gestartet!\' -ForegroundColor Green; Write-Host \'\'; claude \'{initial_message}\' }}"'
            else:
                # Ohne initiale Nachricht
                ps_command = 'Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { Write-Host \'NAJIKA hat Claude Code für dich gestartet!\' -ForegroundColor Green; Write-Host \'\'; claude }"'

            # Starte PowerShell
            subprocess.Popen(
                ['powershell', '-Command', ps_command],
                creationflags=subprocess.CREATE_NO_WINDOW  # Kein zusätzliches Fenster
            )

            print("[NAJIKA LAUNCH] ✅ Claude Code gestartet (neues PowerShell-Fenster)!")
            return True

        # Unix-like: Öffne neues Terminal mit Claude
        else:
            # Versuche verschiedene Terminals
            terminals = [
                ['gnome-terminal', '--', 'claude'],
                ['xterm', '-e', 'claude'],
                ['konsole', '-e', 'claude'],
                ['x-terminal-emulator', '-e', 'claude']
            ]

            for terminal_cmd in terminals:
                try:
                    subprocess.Popen(terminal_cmd)
                    print(f"[NAJIKA LAUNCH] ✅ Claude Code gestartet ({terminal_cmd[0]})!")
                    return True
                except FileNotFoundError:
                    continue

            print("[NAJIKA LAUNCH] ❌ Kein Terminal gefunden!")
            return False

    except Exception as e:
        print(f"[NAJIKA LAUNCH] ❌ Fehler: {e}")
        return False


def launch_claude_code_with_task(task_description):
    """
    Öffnet Claude Code mit einer konkreten Aufgabe

    Args:
        task_description: Beschreibung der Aufgabe für Claude

    Returns:
        bool: True wenn erfolgreich
    """
    prompt = f"Najika hat mich geschickt! Aufgabe: {task_description}"
    return launch_claude_code_interactive(prompt)


def _find_claude_cli():
    """Findet Claude CLI Executable"""
    # Windows: Suche claude.cmd
    if sys.platform == 'win32':
        npm_path = Path.home() / 'AppData' / 'Roaming' / 'npm' / 'claude.cmd'
        if npm_path.exists():
            return str(npm_path)

        # Fallback: Versuche 'where claude.cmd'
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


def test_launch():
    """Test-Funktion"""
    print("="*80)
    print("TEST: Najika startet Claude Code")
    print("="*80)
    print()

    print("Starte Claude Code in neuem Fenster...")
    success = launch_claude_code_interactive("Hallo! Najika hat dich gestartet! Kannst du mir helfen?")

    if success:
        print()
        print("✅ Erfolgreich! Ein neues PowerShell-Fenster sollte sich geöffnet haben.")
        print("   Schau nach einem neuen Fenster mit Claude Code!")
    else:
        print()
        print("❌ Fehlgeschlagen! Claude Code konnte nicht gestartet werden.")

    print()
    print("="*80)


if __name__ == '__main__':
    test_launch()
