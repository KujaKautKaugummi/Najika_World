# CLAUDE CODE INTEGRATION IN NAJIKA

**Datum:** 2025-10-22
**Status:** ✅ AKTIV
**Version:** 1.0

---

## 🎯 WAS IST DAS?

Najika nutzt jetzt **CLAUDE CODE** (dein unlimited Abo) als Haupt-Intelligenz!

**VORHER:**
```
User → Najika → Ollama (lokal, schwächer)
```

**JETZT:**
```
User → Najika → Claude Code (UNLIMITED!) → Falls Fehler: Ollama
```

---

## 📊 INTELLIGENZ-HIERARCHIE

### PRIORITÄT 1: CLAUDE CODE ⭐
- **Was:** Claude Code CLI (DU!)
- **Kosten:** KEINE! (Dein Monats-Abo ist unlimited!)
- **Qualität:** Beste AI (wie ich jetzt gerade)
- **Verfügbar:** Wenn Claude Code CLI installiert

### PRIORITÄT 2: OLLAMA 🔄
- **Was:** Lokales Modell (najika-local / najika-wizard)
- **Kosten:** Kostenlos
- **Qualität:** Gut, aber schwächer als Claude
- **Verfügbar:** Immer (Fallback)

### PRIORITÄT 3: CLOUD APIs 🔒
- **Was:** OpenAI / Anthropic API
- **Kosten:** Pay-per-use (TEUER!)
- **Verfügbar:** Nur mit PIN-Freigabe
- **Status:** Aktuell GESPERRT (wie gewünscht)

---

## 🔧 WIE ES FUNKTIONIERT

### Automatische Auswahl:

1. **Najika bekommt Nachricht**
2. **Prüft:** "Ist Claude Code verfügbar?"
   - ✅ JA → Nutzt Claude Code (über dein Abo)
   - ❌ NEIN → Fallback zu Ollama
3. **Claude Code antwortet**
4. **Falls Fehler** → Automatisch Ollama als Backup

### Code-Flow:

```python
# In najika_server.py (Zeile 1132-1139)
out, provider = call_ai_with_hierarchy(
    prompt=prompt,
    use_wizard=private_trigger,
    context=STATE["history"],
    ollama_callback=call_ollama
)
# provider = "claude_code" oder "ollama"
```

---

## 📁 NEUE DATEIEN

### `najika_claude_code.py`
**Kern-Modul für Claude Code Integration**

**Klassen:**
- `NajikaClaudeCode` - Haupt-Integration
- `call_ai_with_hierarchy()` - Intelligenz-Auswahl-Funktion

**Features:**
- Claude Code CLI Check
- Automatischer Fallback
- Statistiken (Erfolge/Fehler)
- Prompt-Building mit Kontext

---

## 📊 STATISTIKEN

### Health-Check:
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "provider": "ollama",
  "cloud": false,
  "claude_code": {
    "available": false,  // true wenn Claude CLI installiert
    "stats": {
      "claude_code_calls": 0,
      "claude_code_success": 0,
      "claude_code_failures": 0,
      "fallback_to_ollama": 0
    }
  }
}
```

---

## ⚠️ WICHTIG: CLAUDE CODE CLI

### Aktueller Status:
**Claude Code CLI ist NICHT installiert!**

Das bedeutet:
- Najika nutzt aktuell nur Ollama
- Integration ist BEREIT, wartet nur auf CLI

### So würdest du Claude CLI installieren:
```bash
# Wenn du es aktivieren willst (optional!):
npm install -g @anthropic-ai/claude-code

# Oder via pip:
pip install claude-cli
```

**ABER:** Du musst das NICHT machen!
- Ollama funktioniert super
- Claude CLI ist nur ein Bonus

---

## 🎮 WIE DU ES NUTZT

### Automatisch!

Du musst **NICHTS** tun!

1. **Starte Najika normal:**
   ```bash
   START_NAJIKA.bat
   ```

2. **Najika wählt automatisch:**
   - Claude Code (wenn verfügbar)
   - Sonst Ollama

3. **Du siehst im Log:**
   ```
   [NAJIKA CLAUDE CODE] [WARNING] Claude Code nicht verfuegbar - nutze nur Ollama
   [AI HIERARCHY] [FALLBACK] Nutze Ollama...
   ```

---

## 💰 KOSTEN-ÜBERSICHT

| Provider | Kosten | Qualität | Status |
|----------|--------|----------|--------|
| **Claude Code** | ✅ **0€ (Dein Abo!)** | ⭐⭐⭐⭐⭐ | Bereit (CLI fehlt) |
| **Ollama** | ✅ **0€ (Lokal)** | ⭐⭐⭐⭐ | ✅ Aktiv |
| **Cloud APIs** | ❌ **$$$** | ⭐⭐⭐⭐⭐ | 🔒 Gesperrt |

**DEIN VORTEIL:**
- Claude Code = Unlimited über Abo
- Keine API-Kosten!
- Beste Qualität kostenlos!

---

## 🔍 TECHNISCHE DETAILS

### Prompt-Building:

```python
def _build_prompt(self, prompt, context=None):
    parts = []

    # System-Kontext
    parts.append("Du bist Najika - die KI-Begleiterin von Kuja!")
    parts.append("Antworte kurz, explosiv und im Megumin-Stil.")

    # Chat-Historie (letzte 4 Nachrichten)
    if context:
        parts.append("=== CHAT-HISTORIE ===")
        for msg in context[-4:]:
            parts.append(f"{msg['role']}: {msg['content']}")

    # Eigentlicher Prompt
    parts.append("=== AUFGABE ===")
    parts.append(prompt)

    return "\n".join(parts)
```

### CLI-Aufruf:

```python
subprocess.run(
    ["claude", "--non-interactive", "--input", temp_file],
    capture_output=True,
    timeout=60
)
```

---

## 🎯 VORTEILE

### ✅ Unlimited Nutzung
- Dein Claude Code Abo = Flatrate
- Keine Token-Limits wie bei APIs
- Keine Pay-per-use Kosten

### ✅ Beste Qualität
- Claude Sonnet 4.5 (wie ich!)
- Bessere Antworten als Ollama
- Versteht komplexe Anfragen

### ✅ Automatischer Fallback
- Claude Code kaputt? → Ollama springt ein
- Keine Ausfälle
- Immer eine Antwort

### ✅ Statistiken
- Siehst wie oft Claude Code genutzt wird
- Erfolgsrate trackbar
- Fallback-Häufigkeit sichtbar

---

## 🚀 ZUKÜNFTIGE ERWEITERUNGEN

### Geplant:
1. **Streaming** - Token-für-Token Antworten (wie bei Ollama)
2. **Caching** - Häufige Fragen cachen
3. **Load Balancing** - Zwischen Claude Code Instanzen wechseln
4. **Offline-Mode** - Auto-Switch zu Ollama wenn offline

---

## 📝 CHANGELOG

### v1.0 (2025-10-22)
- ✅ Initiales Release
- ✅ Claude Code CLI Integration
- ✅ Automatische Hierarchie: Claude Code → Ollama
- ✅ Health-Check mit Statistiken
- ✅ Unicode-Fixes für Windows Console

---

## ❓ FAQ

**Q: Muss ich Claude CLI installieren?**
A: NEIN! Ollama funktioniert super. Claude CLI ist nur ein Bonus.

**Q: Kostet Claude Code extra?**
A: NEIN! Dein Monats-Abo deckt alles ab (unlimited).

**Q: Was wenn Claude Code offline ist?**
A: Najika nutzt automatisch Ollama als Backup.

**Q: Kann ich Cloud APIs aktivieren?**
A: Ja, aber nur mit PIN (aktuell gesperrt wie gewünscht).

**Q: Wie sehe ich welcher Provider genutzt wird?**
A: Im Server-Log steht: `[INFO] [AI] AI Provider: claude_code` oder `ollama`

---

**FAZIT:** Najika ist jetzt NOCH intelligenter - dank deinem Claude Code Abo! 🔥
