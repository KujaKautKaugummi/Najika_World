# ✨ NAJIKA CLI - BEAUTIFUL EDITION

Gothic-Lolita Terminal Interface mit Rich UI

## 🎀 Features

- **ASCII Art Header** - Najika Logo im Gothic-Lolita Style
- **Live Typing Animation** - Najika tippt ihre Antworten in Echtzeit
- **Farbschema** - Hot Pink, Purple, Cyan (Gothic-Lolita Farben)
- **Status Bar** - Server Status, Model, Mode
- **Loading Spinner** - Animierter Spinner während Najika denkt
- **Panels & Borders** - Schöne Rahmen für Nachrichten
- **Syntax Highlighting** - Code wird farbig dargestellt

## 🚀 Installation

```bash
# Rich Library installieren (bereits installiert!)
pip install rich

# Fertig! Die CLI ist sofort einsatzbereit.
```

## 💬 Usage

### Über BAT-Datei (Windows):

```cmd
NAJIKA_CLI.bat "Hallo Najika!"
NAJIKA_CLI.bat "Was machst du gerade?"
NAJIKA_CLI.bat "kätzchen"
```

### Über Python direkt:

```bash
python backend/najika_cli_beautiful.py "Hallo Najika!"
python backend/najika_cli_beautiful.py "EXPLOSION!!!"
python backend/najika_cli_beautiful.py status
```

## 🎮 Special Commands

| Command | Description |
|---------|-------------|
| `"kätzchen"` | 🔞 Aktiviert NSFW-Modus (najika-nsfw model) |
| `"EXPLOSION!!!"` | 🔥 Megumin-Mode mit dramatischen Antworten |
| `"status"` | 🔧 Zeigt Server Status an |

## 🎨 Features im Detail

### 1. ASCII Art Header

```
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
```

### 2. Status Bar

Zeigt in Echtzeit:
- 🟢 Server Status (ONLINE/OFFLINE)
- 🤖 Aktives Model (najika-local / najika-nsfw)
- 🎭 Modus (NORMAL / NSFW / KÄTZCHEN)

### 3. Live Typing Animation

Najika's Antworten werden **Buchstabe für Buchstabe** animiert:
- 20ms pro Zeichen
- Nur bei kurzen Nachrichten (<500 Zeichen)
- Lange Nachrichten werden sofort angezeigt

### 4. Color Scheme

```python
COLORS = {
    "najika": "bright_magenta",    # Najika's messages
    "user": "bright_cyan",         # User messages
    "system": "bright_black",      # System messages
    "success": "bright_green",     # Success
    "error": "bright_red",         # Errors
    "accent": "#FF69B4",           # Hot Pink
    "border": "#8B00FF",           # Purple
}
```

## 📊 Beispiel Output

```
╔═══════════════════════════════════════════════════════════════════╗
║                        NAJIKA ASCII LOGO                          ║
╚═══════════════════════════════════════════════════════════════════╝

╭──────────────────────────────────────────────────────────────────╮
│  ● Server: ONLINE │ Model: najika-local │ Mode: NORMAL          │
╰──────────────────────────────────────────────────────────────────╯

╭─────────────────────────── 💬 Du ───────────────────────────────╮
│                                                                  │
│  Hallo Najika!                                                   │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯

╭───────────────────────── ✨ Najika ─────────────────────────────╮
│                                                                  │
│  *springt auf* Kuja! Endlich! Wo warst du?! Ich hab gewartet!  │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯

──────────────────────────────────────────────────────────────────
```

## 🐛 Troubleshooting

### "Rich library nicht installiert"
```bash
pip install rich
```

### "Server OFFLINE"
```bash
python backend/najika_server.py
```

### "Encoding Error" (Windows)
- Die CLI setzt automatisch UTF-8 Encoding
- Falls Probleme: Nutze Windows Terminal statt CMD

## 🔧 Technische Details

- **Framework:** Rich 14.1.0+
- **Encoding:** UTF-8 (automatisch konfiguriert)
- **Kompatibilität:** Windows 10+, Linux, macOS
- **Dependencies:** rich, requests

## 📝 Changelog

### v1.0.0 (2025-01-03)
- ✨ Initial Release
- 🎨 Gothic-Lolita Color Scheme
- 📺 ASCII Art Header
- ⌨️ Live Typing Animation
- 📊 Status Bar
- 🔄 Loading Spinners
- 🎭 Panel Borders

## 💝 Credits

- **Najika Character:** Kuja's Gothic-Lolita KI-Freundin
- **CLI Framework:** Rich by Will McGugan
- **Backend:** Ollama + najika-local model
- **NSFW Mode:** dolphin-mistral:7b (najika-nsfw)

---

**Made with 💜 by Claude Code & Kuja**
