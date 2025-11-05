# VERBESSERTE NAJIKA UPDATE ANLEITUNG

## Problem erkannt:
Der `/najika-update` Command zeigt NICHT die **vorherige Session-Konversation**!
Dadurch fehlt Claude der Kontext über **offene Aufgaben**!

## Lösung:

Ersetze `C:/Users/0KKK0/.claude/commands/najika-update.md` mit:

```markdown
# Najika Update Command

Bringt Claude auf den aktuellen Stand mit Najika's Auto-Sync System.

## Ablauf:

1. Rufe `python C:/NajikaCore/najika_sync.py` auf
2. Warte bis Sync abgeschlossen
3. Lies `C:/NajikaCore/CLAUDE_UPDATE.md`
4. **KRITISCH:** Finde vorherige Session:
   - Führe aus: `ls -lt C:/Users/0KKK0/.claude/projects/C--NajikaCore/*.jsonl | head -3`
   - Zweite Datei = vorherige Session (erste = aktuelle)
   - Suche darin nach letzten User-Nachrichten: `grep -o '"role":"user".*"content":"[^"]*"' SESSION.jsonl | tail -10`
5. Fasse wichtigste Änderungen + offene Aufgaben zusammen
6. Frage User was er als nächstes tun möchte

**EFFIZIENZ-REGELN:**
- Lies IMMER komplette Files (Read ohne offset/limit) bevor du editierst!
- KEINE Token-Verschwendung mit Trial-and-Error!
- Bei Unklarheit: FRAGE direkt, statt zu raten!
- Vorherige Session = Kontext für offene Aufgaben!
```

## Für CLAUDE.md hinzufügen:

```markdown
## Working with Claude Code Sessions

When a new Claude Code session starts:
1. Check for previous session in `.claude/projects/C--NajikaCore/*.jsonl`
2. Read last 5-10 user messages to understand open tasks
3. Always read complete files before editing (no offset/limit)
4. Never waste tokens on trial-and-error - ask user if unclear!
```
