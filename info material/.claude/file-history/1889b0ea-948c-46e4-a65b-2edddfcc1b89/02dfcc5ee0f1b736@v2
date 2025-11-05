#!/usr/bin/env python3
"""
NAJIKA TOOLS - File Access & Code Execution
Najika kann jetzt auf Files zugreifen und Code schreiben!
"""

import os
import subprocess
from pathlib import Path

class NajikaTools:
    """Tools die Najika zur Verfügung stehen"""

    @staticmethod
    def read_file(file_path):
        """Liest eine Datei"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"FEHLER: Datei nicht gefunden: {file_path}"

            content = path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Limit zu 100 Zeilen
            if len(lines) > 100:
                preview = '\n'.join(lines[:100])
                return f"{preview}\n\n... (gekürzt, {len(lines)} Zeilen total)"

            return content
        except Exception as e:
            return f"FEHLER beim Lesen: {str(e)}"

    @staticmethod
    def write_file(file_path, content):
        """Schreibt eine Datei"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return f"ERFOLG: Datei geschrieben: {file_path}"
        except Exception as e:
            return f"FEHLER beim Schreiben: {str(e)}"

    @staticmethod
    def list_files(directory="."):
        """Listet Dateien in einem Verzeichnis"""
        try:
            path = Path(directory)
            if not path.exists():
                return f"FEHLER: Verzeichnis nicht gefunden: {directory}"

            files = []
            for item in sorted(path.iterdir()):
                if item.is_file():
                    size = item.stat().st_size
                    files.append(f"  {item.name} ({size} bytes)")
                elif item.is_dir():
                    files.append(f"  {item.name}/")

            if not files:
                return f"Verzeichnis ist leer: {directory}"

            return f"Dateien in {directory}:\n" + "\n".join(files)
        except Exception as e:
            return f"FEHLER beim Listen: {str(e)}"

    @staticmethod
    def execute_command(command):
        """Führt einen Shell-Befehl aus"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )

            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += "\nERROR:\n" + result.stderr

            if not output.strip():
                output = f"Befehl ausgeführt (kein Output)"

            return output
        except subprocess.TimeoutExpired:
            return "FEHLER: Befehl timeout (>30s)"
        except Exception as e:
            return f"FEHLER bei Ausführung: {str(e)}"

    @staticmethod
    def get_current_directory():
        """Gibt aktuelles Verzeichnis zurück"""
        return str(Path.cwd())


def parse_tool_request(message):
    """
    Erkennt Tool-Requests im User-Input
    Returns: (tool_name, args) oder (None, None)
    """
    message_lower = message.lower()

    # File Read
    if any(x in message_lower for x in ["lies datei", "lese datei", "zeig datei", "read file", "show file"]):
        # Extrahiere Pfad aus Nachricht
        import re
        match = re.search(r'["\']([^"\']+)["\']', message)
        if match:
            return ("read_file", match.group(1))

    # File Write
    if any(x in message_lower for x in ["schreib datei", "schreibe datei", "write file", "erstell datei"]):
        # Format: "schreib datei 'path' mit inhalt 'content'"
        import re
        match = re.search(r'["\']([^"\']+)["\'].*["\']([^"\']+)["\']', message)
        if match:
            return ("write_file", (match.group(1), match.group(2)))

    # List Files
    if any(x in message_lower for x in ["liste dateien", "zeig dateien", "list files", "show files", "ls"]):
        import re
        match = re.search(r'in ["\']?([^"\']+)["\']?', message)
        if match:
            return ("list_files", match.group(1))
        return ("list_files", ".")

    # Execute Command
    if any(x in message_lower for x in ["führe aus", "execute", "run command"]):
        import re
        match = re.search(r'["\']([^"\']+)["\']', message)
        if match:
            return ("execute_command", match.group(1))

    return (None, None)


if __name__ == "__main__":
    print("Najika Tools geladen!")
    print("Verfügbare Tools:")
    print("- read_file(path)")
    print("- write_file(path, content)")
    print("- list_files(directory)")
    print("- execute_command(cmd)")
    print("- get_current_directory()")
