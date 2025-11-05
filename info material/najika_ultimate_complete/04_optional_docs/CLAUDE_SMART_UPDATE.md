# NAJIKA SMART UPDATE V2
**08:43:19**

## VORHERIGE SESSION KONTEXT

---

## ANWEISUNGEN FÜR CLAUDE:

**PFLICHT:**
1. Lies Files aus 'FILES DIE ERWÄHNT WURDEN' KOMPLETT (Read ohne offset)!
2. Prüfe 'ERKANNTE OFFENE AUFGABEN' - was ist noch zu tun?
3. Frage User kurz was als nächstes (max 2 Sätze!)

**TOKEN-EFFIZIENZ:**
- Read IMMER komplett vor Edit
- Grep für Suchen, nicht File-Reading
- User-Textstück? → `grep -F 'TEXT' SESSION.jsonl`
- Kurze Antworten - User kennt Kontext!
