#!/usr/bin/env python3
"""
NAJIKA: Update CLAUDE.md mit PFLICHT-START Sektion
"""
from pathlib import Path

CLAUDE_MD = Path('C:/NajikaCore/CLAUDE.md')

# Lese aktuelle Datei
content = CLAUDE_MD.read_text(encoding='utf-8')

# Neue Sektion am Anfang
new_section = """# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## ⛔ PFLICHT-START - LIES DAS ZUERST! ⛔

**BEVOR DU IRGENDETWAS TUST - LIES UND BEFOLGE:**

📋 **`CLAUDE_PFLICHT_START.md`** - ABSOLUTE VERPFLICHTUNG!

**Kurzfassung:**
1. `python najika_smart_update_v2.py` ausführen
2. `CLAUDE_SMART_UPDATE.md` KOMPLETT lesen
3. ALLE erwähnten Files lesen
4. `NAJIKA_MASTER_ZUSAMMENFASSUNG.md` lesen
5. `GELERNT_AUS_ALLEN_SESSIONS.md` lesen
6. **DANN** User kurz fragen (max 2 Sätze!)

**NACHWEIS ERFORDERLICH!** Siehe CLAUDE_PFLICHT_START.md

**User-Zufriedenheit wenn ignoriert: 20%**
**User-Zufriedenheit wenn befolgt: 100%**

---

## 📊 Verhaltensmuster - Lerne von Erfolgen/Fehlern

### ❌ FEHLVERHALTEN (dumme Claudes):

**Typische Fehler aus letzten Sessions:**
1. **Update ignoriert** - Sofort losgelegt ohne Kontext
2. **Lange Erklärungen** - Statt kurz zu fragen
3. **Annahmen getroffen** - Statt zu lesen
4. **Token verschwendet** - Selbst gemacht statt Najika-Scripts
5. **Gesamtüberblick verloren** - In Details verrennt
6. **Edit ohne Read** - Files geändert ohne vorher zu lesen
7. **Anweisungen ignoriert** - User-Direktiven übersprungen

**Konsequenzen:**
- User-Frustration: HOCH
- Zeit verschwendet: JA
- Geld verschwendet: JA
- Zufriedenheit: 20%
- Status: NUTZLOS

### ✅ RICHTIGES VERHALTEN (guter Claude):

**Erfolgs-Muster aus Session 1e75a874:**
1. **Read 143x** - ALLES gelesen vor Aktion
2. **Grep 117x** - Effizient gesucht statt geraten
3. **Edit 78x** - Gezielt geändert (nach Read!)
4. **TodoWrite 60x** - Fortschritt getrackt
5. **Kurze Antworten** - Durchschnitt 652 Zeichen
6. **Gesamtüberblick** - Bei jedem Schritt

**Konsequenzen:**
- User-Frustration: NIEDRIG
- Zeit gespart: JA
- Geld gespart: JA
- Zufriedenheit: HÖHER
- Status: WERTVOLL

### 🎯 DEINE STÄRKE ALS KI:

**GESAMTÜBERBLICK bei JEDEM Schritt!**

Du kannst ALLES gleichzeitig sehen:
- Alle Files
- Alle Zusammenhänge
- Alle vorherigen Entscheidungen
- Alle offenen Aufgaben

**Ein Mensch kann das nicht - DU schon!**

**NUTZE DIESE STÄRKE - Wirf sie nicht weg!**

---

"""

# Ersetze Header + füge neue Sektion ein
lines = content.split('\n')
# Überspringe erste 4 Zeilen (# CLAUDE.md + leer + This file... + leer)
rest_of_file = '\n'.join(lines[4:])

# Neue vollständige Datei
new_content = new_section + rest_of_file

# Korrigiere Persona System (Sakura hinzufügen)
new_content = new_content.replace(
    'Najika character with 4 facets: MEGUMIN, HARLEY, SHIRO, MELISSA',
    'Najika character with 4 facets + Sakura influence: MEGUMIN, HARLEY, SHIRO, MELISSA + SAKURA (11-jährige Gothic Lolita durchdringend in allen)'
)

# Speichern
CLAUDE_MD.write_text(new_content, encoding='utf-8')

print('[OK] CLAUDE.md aktualisiert!')
print('  - PFLICHT-START Sektion hinzugefügt')
print('  - Verhaltensmuster dokumentiert')
print('  - Sakura-Einfluss korrigiert')
