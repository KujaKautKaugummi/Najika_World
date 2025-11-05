# NAJIKA DEPLOYMENT NOTES

## Browser Integration für finale App

**WICHTIG:** Die finale Najika-App muss folgende Browser mitbringen:

### 1. Tor Browser (Portable)
- **Zweck:** Darknet-Zugriff, .onion Sites, anonyme Suchen
- **Version:** Latest stable (aktuell 13.5.7)
- **Integration:** `najika_tor.py` erkennt automatisch Darknet-Anfragen
- **Pfad in App:** `C:\NajikaCore\browsers\tor-browser\`
- **Download:** https://www.torproject.org/download/

### 2. Firefox (Portable)
- **Zweck:** Normale Web-Browsing innerhalb der App
- **Version:** Latest ESR oder Regular
- **Integration:** Für Web Search Visualisierung, normale Browsing
- **Pfad in App:** `C:\NajikaCore\browsers\firefox\`
- **Download:** https://www.mozilla.org/firefox/

## Packaging Strategy

### Verzeichnisstruktur finale App:
```
NajikaCore/
├── najika_server.py
├── najika_*.py (alle Module)
├── digivice/ (Frontend)
├── assets/ (KayKit, Textures, etc.)
├── models/ (Ollama GGUF files)
├── browsers/
│   ├── tor-browser/ (komplette Tor Installation)
│   └── firefox/ (komplette Firefox Installation)
├── memory_db/ (ChromaDB persistence)
├── saves/
└── logs/

```

### Auto-Detection Anpassungen:

**najika_tor.py** muss angepasst werden:
```python
def _find_tor_browser(self):
    # Priorisiere gebundelte Version
    bundled_path = os.path.join(os.path.dirname(__file__), "browsers", "tor-browser", "Browser", "firefox.exe")
    if os.path.exists(bundled_path):
        return bundled_path

    # Fallback: System-Installation
    # ... existing code ...
```

### Installer Anforderungen:

1. **Gesamtgröße:** ~500MB
   - Tor Browser: ~95MB
   - Firefox Portable: ~80MB
   - Ollama Models: ~250MB (najika-local + najika-wizard)
   - Rest: ~75MB

2. **Dependencies bereits gebündelt:**
   - Python embedded (falls exe-Packaging)
   - Alle pip packages
   - ChromaDB
   - Beide Browser

3. **Erste Start-Erkennung:**
   - Prüfe ob Ollama läuft
   - Falls nicht: Starte lokale Ollama-Instanz oder zeige Setup-Anleitung
   - Kopiere Models nach `~/.ollama/models/` falls nicht vorhanden

## Sicherheitshinweise

- ExpressVPN bereits installiert beim User
- Tor Browser: Empfehle Bridges für China/Iran/etc.
- Firefox: Privacy-Settings voreingestellt (Tracking Protection Strict)

## Testing Checklist vor Release

- [ ] Tor Browser: .onion Links funktionieren
- [ ] Firefox: Normale URLs funktionieren
- [ ] Beide Browser: Integration mit Najika Security Module
- [ ] Auto-Detection: Beide Browser werden gefunden
- [ ] Portable Mode: App läuft von USB-Stick
- [ ] ExpressVPN Detection: Warnung wenn VPN aus

## Notizen

- User wünscht BEIDE Browser in der App gebündelt
- Tor für Darknet, Firefox für normale Suchen
- Maximale Unabhängigkeit von System-Installationen
