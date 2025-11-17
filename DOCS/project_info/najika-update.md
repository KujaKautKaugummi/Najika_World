# Najika Update Command V3

Smart Update System mit VERIFICATION-CODES - Bombensicher!

## PFLICHT-ABLAUF:

1. `python C:/NajikaCore/najika_smart_update_v3.py`
2. Warte bis fertig
3. **LIES KOMPLETT:** `C:/NajikaCore/CLAUDE_SMART_UPDATE.md` (Read OHNE offset!)

Das Update enthaelt:
- Letzte 5 User-Messages VOLLSTAENDIG (max 800 chars)
- Erkannte offene Aufgaben (kategorisiert)
- Files die erwaehnt wurden (Read-Liste!)
- Task-Tracking ueber Sessions
- **VERIFICATION CODES die du finden musst!**

4. **PFLICHT:** Lies `NAJIKA_MASTER_ZUSAMMENFASSUNG.md` KOMPLETT - finde CODE!
5. **PFLICHT:** Lies `GELERNT_AUS_ALLEN_SESSIONS.md` KOMPLETT - finde CODE!
6. Lies alle Files aus "FILES DIE ERWAEHNT WURDEN" KOMPLETT!
7. **BERICHTE ALLE VERIFICATION CODES** die du gefunden hast!
8. Pruefe offene Aufgaben
9. Frage User KURZ (max 2 Saetze!) was als naechstes

**TOKEN-EFFIZIENZ (KRITISCH!):**

- Read IMMER komplett vor Edit (keine Ausnahmen!)
- Grep fuer Suchen, nicht File-Reading
- User-Textstueck? → `grep -F "TEXT" SESSION.jsonl`
- Halte Antworten kurz - User kennt Kontext!
- Keine Trial-and-Error Edits - erst lesen!

**WENN FEHLER PASSIEREN:**

- File modified? → Read nochmal!
- Nicht raten - User fragen!
- Keine Token-Verschwendung!

**VERIFICATION SYSTEM:**

- Codes werden automatisch in Files injiziert
- Du MUSST sie finden und berichten
- KEINE Codes = Du hast NICHT gelesen!
- User merkt SOFORT wenn du schummels!
