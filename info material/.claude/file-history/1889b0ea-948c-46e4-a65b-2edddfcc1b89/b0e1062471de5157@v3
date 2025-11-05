#!/usr/bin/env python3
"""
NAJIKA CLI - Terminal Interface mit File-Access
Nutze Najika im Terminal wie Claude Code!

Usage:
    python najika_cli.py "Hallo Najika!"
    python najika_cli.py "Lies Datei 'test.txt'"
    python najika_cli.py "Schreib Code für ein Hello World"
"""

import sys
import json
import os
from pathlib import Path

try:
    import requests
except ImportError:
    import urllib.request
    import urllib.parse
    requests = None

# Import Najika Tools
try:
    from najika_tools import NajikaTools, parse_tool_request
except ImportError:
    NajikaTools = None
    parse_tool_request = None

# Configuration
API_URL = "http://localhost:8000/api/chat"
TIMEOUT = 60  # seconds

def clean_unicode(text):
    """Remove emoji and special Unicode characters for Windows CMD"""
    import re
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\u2728"                 # sparkles
        u"\u2764"                 # heart
        u"\U0001F48E"             # gem
        u"\U0001F525"             # fire
        u"\U0001F4A5"             # boom
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def chat_with_najika(message, context=""):
    """Send message to Najika and get response"""

    full_message = message
    if context:
        full_message = f"[CONTEXT]\n{context}\n\n[USER REQUEST]\n{message}"

    payload = {"message": full_message}

    if requests:
        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            najika_response = data.get("response", "FEHLER: Keine Response erhalten")
            return clean_unicode(najika_response)
        except requests.exceptions.ConnectionError:
            return "FEHLER: Najika-Server läuft nicht! Starte ihn mit: python najika_server.py"
        except requests.exceptions.Timeout:
            return "FEHLER: Timeout - Najika braucht zu lange zum Antworten"
        except Exception as e:
            return f"FEHLER: {str(e)}"
    else:
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                result = json.loads(response.read().decode('utf-8'))
                return clean_unicode(result.get("response", "FEHLER: Keine Response erhalten"))
        except urllib.error.URLError:
            return "FEHLER: Najika-Server läuft nicht! Starte ihn mit: python najika_server.py"
        except Exception as e:
            return f"FEHLER: {str(e)}"

def execute_tool_request(user_message):
    """
    Führt Tool-Request direkt aus oder fragt Najika
    Returns: (executed, result)
    """
    if not NajikaTools or not parse_tool_request:
        return (False, None)

    tool_name, args = parse_tool_request(user_message)

    if not tool_name:
        return (False, None)

    # Tool ausführen
    tools = NajikaTools()

    try:
        if tool_name == "read_file":
            result = tools.read_file(args)
        elif tool_name == "write_file":
            path, content = args
            result = tools.write_file(path, content)
        elif tool_name == "list_files":
            result = tools.list_files(args)
        elif tool_name == "execute_command":
            result = tools.execute_command(args)
        else:
            return (False, None)

        return (True, result)
    except Exception as e:
        return (True, f"TOOL FEHLER: {str(e)}")

def main():
    """Main CLI entry point"""

    # Set UTF-8 encoding for Windows CMD
    import sys
    import codecs
    if sys.platform == 'win32':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

    # Check if message provided
    if len(sys.argv) < 2:
        print("NAJIKA CLI - Option A (Full Features)")
        print("=" * 60)
        print("\nUsage: python najika_cli.py \"Deine Nachricht\"")
        print("\nBeispiele:")
        print("  python najika_cli.py \"Hallo Najika!\"")
        print("  python najika_cli.py \"Was machst du gerade?\"")
        print("  python najika_cli.py \"EXPLOSION!!!\"")
        print("\nMit File-Access:")
        print("  python najika_cli.py \"Liste Dateien\"")
        print("  python najika_cli.py \"Lies Datei 'test.txt'\"")
        print("  python najika_cli.py \"Schreib einen Hello World Code\"")
        print("\nCurrent Directory:", Path.cwd())
        return

    # Get user message
    user_message = " ".join(sys.argv[1:])

    # Print user message
    print(f"\n[Du]: {user_message}")
    print("-" * 60)

    # Try direct tool execution
    executed, tool_result = execute_tool_request(user_message)

    if executed:
        # Tool wurde ausgeführt - sende Ergebnis an Najika für Antwort
        context = f"TOOL RESULT:\n{tool_result}"
        najika_response = chat_with_najika(user_message, context)
    else:
        # Normale Chat-Anfrage
        najika_response = chat_with_najika(user_message)

    # Print Najika's response
    print(f"[Najika]: {najika_response}")

    # Print tool result if available
    if executed and tool_result:
        print("\n" + "="  * 60)
        print("[TOOL OUTPUT]")
        print(tool_result)

    print("-" * 60)
    print()

if __name__ == "__main__":
    main()
