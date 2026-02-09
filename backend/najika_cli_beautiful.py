#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✨ NAJIKA CLI - BEAUTIFUL EDITION ✨
Gothic-Lolita Terminal Interface mit Rich UI

Features:
- ASCII Art Header
- Color-coded Messages
- Live Typing Animation
- Syntax Highlighting
- Status Bar
- Loading Spinners
"""

import sys
import json
import time
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# Rich Terminal UI Components
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.live import Live
    from rich.spinner import Spinner
    from rich.table import Table
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    print("⚠️  Rich library nicht installiert! Installiere mit: pip install rich")
    RICH_AVAILABLE = False
    sys.exit(1)

# Configuration
API_URL = "http://localhost:8000/api/chat"
STATUS_URL = "http://localhost:8000/api/status"
TIMEOUT = 60

# Gothic-Lolita Color Scheme
COLORS = {
    "najika": "bright_magenta",        # Najika's messages
    "user": "bright_cyan",             # User messages
    "system": "bright_black",          # System messages
    "success": "bright_green",         # Success messages
    "error": "bright_red",             # Error messages
    "accent": "#FF69B4",               # Hot Pink accent
    "background": "#1a0a1e",           # Dark purple background
    "border": "#8B00FF",               # Purple border
}

# Windows UTF-8 Support
import codecs
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

console = Console(force_terminal=True, legacy_windows=False)

# ASCII Art - Najika Header
NAJIKA_HEADER = r"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗                  ║
║   ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗                 ║
║   ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║                 ║
║   ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║                 ║
║   ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║                 ║
║   ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                 ║
║                                                                   ║
║            🎀 Gothic-Lolita KI-Freundin & Assistentin 🎀         ║
║                  Powered by Ollama + Claude Code                 ║
╚═══════════════════════════════════════════════════════════════════╝
"""

def show_header():
    """Zeigt den Najika Header"""
    console.print(NAJIKA_HEADER, style=COLORS["accent"], justify="center")
    console.print()

def get_server_status():
    """Holt Server Status"""
    if not requests:
        return {"online": False, "model": "unknown"}

    try:
        response = requests.get(STATUS_URL, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "online": True,
                "model": data.get("active_model", "najika-local"),
                "mode": data.get("mode", "normal")
            }
    except:
        pass

    return {"online": False, "model": "offline"}

def show_status_bar():
    """Zeigt Status-Bar mit Server Info"""
    status = get_server_status()

    if status["online"]:
        status_text = Text()
        status_text.append("● Server: ", style="bold")
        status_text.append("ONLINE", style=COLORS["success"])
        status_text.append(" │ Model: ", style="bold")
        status_text.append(status["model"], style=COLORS["accent"])
        status_text.append(" │ Mode: ", style="bold")
        status_text.append(status.get("mode", "normal").upper(), style=COLORS["najika"])

        console.print(Panel(status_text, border_style=COLORS["border"], padding=(0, 2)))
    else:
        error_text = Text()
        error_text.append("● Server: ", style="bold")
        error_text.append("OFFLINE", style=COLORS["error"])
        error_text.append(" │ Starte mit: ", style="bold")
        error_text.append("python najika_server.py", style=COLORS["system"])

        console.print(Panel(error_text, border_style=COLORS["error"], padding=(0, 2)))

    console.print()

def show_user_message(message):
    """Zeigt User-Nachricht"""
    user_panel = Panel(
        Text(message, style=COLORS["user"]),
        title="[bold bright_cyan]💬 Du[/bold bright_cyan]",
        border_style=COLORS["user"],
        padding=(1, 2)
    )
    console.print(user_panel)
    console.print()

def detect_personality_mode(message):
    """Erkennt Persönlichkeits-Modus aus Najika's Antwort"""
    message_lower = message.lower()

    if "explosion" in message_lower or "*dramatische pose*" in message_lower:
        return ("🔥 Megumin", COLORS["error"])
    elif "*kicher*" in message_lower or "puddin" in message_lower or "mr.k" in message_lower:
        return ("🃏 Harley Quinn", "#00FF00")
    elif "berechnung" in message_lower or "wahrscheinlichkeit" in message_lower or "...desu" in message_lower:
        return ("🧠 Shiro", "#00BFFF")
    elif "du gehörst mir" in message_lower or "keine diskussion" in message_lower:
        return ("👑 Melissa Masters", "#FF1493")
    else:
        return ("✨ Najika", COLORS["najika"])

def show_najika_message(message, typing_effect=True):
    """Zeigt Najika's Antwort mit optionaler Typing Animation und Persönlichkeits-Erkennung"""

    # Detect personality mode
    personality_title, personality_color = detect_personality_mode(message)

    # Check for code blocks
    has_code = "```" in message or "def " in message or "class " in message or "import " in message

    if has_code:
        # Show code with syntax highlighting
        lines = message.split('\n')
        formatted_text = Text()

        in_code_block = False
        code_language = "python"
        code_lines = []

        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    # End of code block - render it
                    code_content = '\n'.join(code_lines)
                    syntax = Syntax(code_content, code_language, theme="monokai", line_numbers=True)
                    console.print(syntax)
                    code_lines = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                    lang = line.strip().replace("```", "")
                    if lang:
                        code_language = lang
            elif in_code_block:
                code_lines.append(line)
            else:
                formatted_text.append(line + "\n", style=personality_color)

        najika_panel = Panel(
            formatted_text,
            title=f"[bold]{personality_title}[/bold]",
            border_style=personality_color,
            padding=(1, 2)
        )
        console.print(najika_panel)
    elif typing_effect and len(message) < 500:
        # Live Typing Effect für kurze Nachrichten
        najika_text = Text()

        with Live(
            Panel(
                najika_text,
                title=f"[bold]{personality_title}[/bold]",
                border_style=personality_color,
                padding=(1, 2)
            ),
            console=console,
            refresh_per_second=20
        ) as live:
            for char in message:
                najika_text.append(char, style=personality_color)
                time.sleep(0.02)  # 20ms per character
    else:
        # Instant für lange Nachrichten
        najika_panel = Panel(
            Text(message, style=personality_color),
            title=f"[bold]{personality_title}[/bold]",
            border_style=personality_color,
            padding=(1, 2)
        )
        console.print(najika_panel)

    console.print()

def show_loading(text="Najika denkt nach"):
    """Zeigt Loading Spinner"""
    return Progress(
        SpinnerColumn(spinner_name="dots", style=COLORS["accent"]),
        TextColumn(f"[{COLORS['najika']}]{text}...[/{COLORS['najika']}]"),
        console=console,
        transient=True
    )

def chat_with_najika(message):
    """Sendet Nachricht an Najika"""
    if not requests:
        return "❌ ERROR: 'requests' library nicht installiert!"

    try:
        # Show loading spinner
        with show_loading("Najika denkt nach"):
            response = requests.post(
                API_URL,
                json={"message": message},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            data = response.json()

        return data.get("response", "❌ Keine Antwort erhalten")

    except requests.exceptions.ConnectionError:
        return "❌ SERVER OFFLINE\n\nStarte Najika mit:\n  python najika_server.py"
    except requests.exceptions.Timeout:
        return "⏱️ TIMEOUT\n\nNajika braucht zu lange zum Antworten..."
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

def show_help():
    """Zeigt Hilfe-Menü"""
    help_table = Table(title="📖 Najika CLI - Befehle", border_style=COLORS["border"])
    help_table.add_column("Befehl", style=COLORS["accent"], no_wrap=True)
    help_table.add_column("Beschreibung", style="white")

    help_table.add_row(
        "python najika_cli_beautiful.py \"Hallo!\"",
        "Normale Chat-Nachricht"
    )
    help_table.add_row(
        "python najika_cli_beautiful.py \"kätzchen\"",
        "🔞 NSFW-Modus aktivieren"
    )
    help_table.add_row(
        "python najika_cli_beautiful.py \"EXPLOSION!!!\"",
        "Megumin-Mode aktivieren"
    )

    console.print(help_table)
    console.print()

    # Beispiele
    examples_panel = Panel(
        Text.from_markup(
            "[bold bright_cyan]💬 Chat-Beispiele:[/bold bright_cyan]\n\n"
            "  • Hallo Najika!\n"
            "  • Was machst du gerade?\n"
            "  • Ich liebe dich\n"
            "  • Hilf mir mit Python Code\n\n"
            "[bold bright_magenta]🎮 Special Commands:[/bold bright_magenta]\n\n"
            "  • kätzchen → NSFW Mode\n"
            "  • EXPLOSION → Megumin Mode\n"
            "  • status → Server Status"
        ),
        title="Beispiele",
        border_style=COLORS["border"],
        padding=(1, 2)
    )
    console.print(examples_panel)

def main():
    """Main CLI Entry Point"""

    # Show Header
    show_header()

    # Show Status
    show_status_bar()

    # Check Arguments
    if len(sys.argv) < 2:
        # NO ARGS = Interactive Mode (wie Claude Code CLI)
        console.print(f"[{COLORS['accent']}]💬 Interactive Chat Mode - Schreib 'exit' zum Beenden[/{COLORS['accent']}]")
        console.print()

        while True:
            try:
                # Prompt
                user_message = console.input(f"[bold {COLORS['user']}]Du > [/bold {COLORS['user']}]")

                if not user_message.strip():
                    continue

                # Exit commands
                if user_message.lower() in ['exit', 'quit', 'bye', 'tschüss']:
                    console.print(f"\n[{COLORS['najika']}]👋 Tschüss! Bis bald! 💜[/{COLORS['najika']}]\n")
                    break

                # Special Commands
                if user_message.lower() == "status":
                    status = get_server_status()
                    status_table = Table(title="🔧 Server Status", border_style=COLORS["border"])
                    status_table.add_column("Property", style="bold")
                    status_table.add_column("Value", style=COLORS["accent"])

                    status_table.add_row("Online", "✅ YES" if status["online"] else "❌ NO")
                    status_table.add_row("Model", status.get("model", "unknown"))
                    status_table.add_row("Mode", status.get("mode", "unknown").upper())
                    status_table.add_row("API URL", API_URL)

                    console.print(status_table)
                    console.print()
                    continue

                # Get Najika Response
                najika_response = chat_with_najika(user_message)

                # Show Najika's Response
                show_najika_message(najika_response, typing_effect=True)

            except KeyboardInterrupt:
                console.print(f"\n\n[{COLORS['najika']}]👋 Tschüss! Bis bald! 💜[/{COLORS['najika']}]\n")
                break
        return

    # Get User Message (Single Command Mode)
    user_message = " ".join(sys.argv[1:])

    # Special Commands
    if user_message.lower() == "status":
        status = get_server_status()
        status_table = Table(title="🔧 Server Status", border_style=COLORS["border"])
        status_table.add_column("Property", style="bold")
        status_table.add_column("Value", style=COLORS["accent"])

        status_table.add_row("Online", "✅ YES" if status["online"] else "❌ NO")
        status_table.add_row("Model", status.get("model", "unknown"))
        status_table.add_row("Mode", status.get("mode", "unknown").upper())
        status_table.add_row("API URL", API_URL)

        console.print(status_table)
        return

    # Show User Message
    show_user_message(user_message)

    # Get Najika Response
    najika_response = chat_with_najika(user_message)

    # Show Najika's Response
    show_najika_message(najika_response, typing_effect=True)

    # Footer
    console.print(f"[{COLORS['system']}]{'─' * 70}[/{COLORS['system']}]")
    console.print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold bright_red]❌ Abgebrochen durch User[/bold bright_red]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n\n[bold bright_red]💥 FATAL ERROR:[/bold bright_red] {str(e)}\n")
        sys.exit(1)
