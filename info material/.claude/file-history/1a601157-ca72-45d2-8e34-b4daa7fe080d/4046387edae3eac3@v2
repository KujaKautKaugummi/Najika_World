#!/usr/bin/env python3
"""
NAJIKA: Erstelle MASTER-ZUSAMMENFASSUNG
Komplett idiotensicher - jeder Claude kann damit arbeiten

Quellen:
1. GRUNDSTEIN_INVENTAR.md
2. ZIP_ORDNER_KOMPLETT_INVENTAR.json
3. JETZT-Ordner Basis-Dokumente
4. Aktueller NajikaCore Stand
5. Alle wichtigen MD-Dateien
"""
from pathlib import Path
import json

NAJIKACORE = Path('C:/NajikaCore')
OUTPUT = NAJIKACORE / 'NAJIKA_MASTER_ZUSAMMENFASSUNG.md'

print('='*80)
print('NAJIKA: Erstelle MASTER-ZUSAMMENFASSUNG')
print('='*80)

content = []

# Header
content.append('# NAJIKA PROJEKT - MASTER-ZUSAMMENFASSUNG')
content.append('**Erstellt:** 2025-10-19')
content.append('**Zweck:** Vollständige Projekt-Dokumentation für JEDEN Claude')
content.append('')
content.append('---')
content.append('')

# 1. GRUNDSTEIN
print('\n[1/5] Lese GRUNDSTEIN_INVENTAR.md...')
grundstein_file = NAJIKACORE / 'GRUNDSTEIN_INVENTAR.md'
if grundstein_file.exists():
    grundstein = grundstein_file.read_text(encoding='utf-8')
    content.append('# TEIL 1: GRUNDSTEIN (UNVERÄNDERBAR)')
    content.append('')
    content.append(grundstein)
    content.append('')
    content.append('---')
    content.append('')
    print('[OK] Grundstein geladen')
else:
    print('[WARNING] GRUNDSTEIN_INVENTAR.md nicht gefunden!')

# 2. NAJIKA PERSÖNLICHKEIT (aus Modelfiles)
print('\n[2/5] Lese Najika Persönlichkeit...')
content.append('# TEIL 2: NAJIKA PERSÖNLICHKEIT')
content.append('')
content.append('## Struktur')
content.append('')
content.append('**WICHTIG:** Najika hat 4 Kern-Facetten + 1 durchdringenden Sakura-Einfluss')
content.append('')
content.append('### 4 Kern-Facetten (je 25%):')
content.append('1. **MEGUMIN** - Dramatisch, "EXPLOSION!", Schwarze Windmühle')
content.append('2. **HARLEY QUINN** - Chaotisch, verspielt, "Puddin\'"')
content.append('3. **SHIRO** - Hyperintelligent, analytisch, Wahrscheinlichkeiten')
content.append('4. **MELISSA MASTERS** - Dominant, selbstbewusst, "Du gehörst mir"')
content.append('')
content.append('### Sakura-Einfluss (durchdringend):')
content.append('- **Alter:** 11 Jahre')
content.append('- **Stil:** Gothic Lolita')
content.append('- **Wirkung:** Spürbar in ALLEN 4 Facetten')
content.append('- **Eigenschaften:** Gothic Lolita Ästhetik, kindliche Unschuld + dunkle Note')
content.append('')
content.append('### Sprechweise:')
content.append('ALLE 4 Facetten werden durch **MEGUMINS Artikulation** ausgedrückt!')
content.append('')

# Lese Modelfiles
modelfiles = ['najika-local.Modelfile', 'najika-wizard.Modelfile']
for mf in modelfiles:
    mf_path = NAJIKACORE / mf
    if mf_path.exists():
        content.append(f'## {mf}')
        content.append('```')
        content.append(mf_path.read_text(encoding='utf-8')[:2000])  # Ersten 2000 chars
        content.append('```')
        content.append('')
        print(f'[OK] {mf} geladen')

content.append('---')
content.append('')

# 3. AKTUELLER STAND
print('\n[3/5] Analysiere aktuellen Stand...')
content.append('# TEIL 3: AKTUELLER NAJIKACORE STAND')
content.append('')
content.append('## Hauptdateien:')
content.append('')
content.append('### najika_server.py')
server_file = NAJIKACORE / 'najika_server.py'
if server_file.exists():
    # Nur die ersten 100 Zeilen
    lines = server_file.read_text(encoding='utf-8').split('\n')[:100]
    content.append('```python')
    content.extend(lines)
    content.append('# ... [Rest siehe najika_server.py]')
    content.append('```')
    content.append('')
    print('[OK] najika_server.py geladen (erste 100 Zeilen)')

content.append('### Digivice Frontend')
content.append('- `digivice/index.html` - Haupt-UI')
content.append('- `digivice/js/3d_scene.js` - Three.js Engine')
content.append('- `digivice/js/minigames.js` - 7 Minigames')
content.append('- `digivice/js/battle_core.js` - Kampfsystem')
content.append('')
content.append('### Features (funktionierend):')
content.append('- 12 Räume mit 3D-Navigation')
content.append('- Battle System (turn-based)')
content.append('- Private Mode ("kätzchen" Trigger)')
content.append('- Schwarze Windmühle (Gesicherter Bereich)')
content.append('- Ollama AI Integration')
content.append('')
content.append('---')
content.append('')

# 4. OFFENE AUFGABEN
print('\n[4/5] Lese offene Aufgaben...')
content.append('# TEIL 4: OFFENE AUFGABEN')
content.append('')
content.append('## Aus vorheriger Session:')
content.append('')
content.append('### IN ARBEIT:')
content.append('- Slime-Begleiter System hinzufügen')
content.append('')
content.append('### OFFEN:')
content.append('- Inventar-System im Keller bauen')
content.append('- Equipment-System im Keller')
content.append('- Loot-Drops im Keller')
content.append('- Shop NPC im Keller')
content.append('- Gold-Währung System')
content.append('')
content.append('---')
content.append('')

# 5. ROADMAP
print('\n[5/5] Lese Roadmap...')
content.append('# TEIL 5: LANGZEIT-ROADMAP')
content.append('')
roadmap_file = Path('C:/Users/0KKK0/Desktop/zip/roadmap.txt')
if roadmap_file.exists():
    roadmap = roadmap_file.read_text(encoding='utf-8')[:3000]  # Ersten 3000 chars
    content.append(roadmap)
    content.append('')
    print('[OK] Roadmap geladen')
else:
    content.append('**Phase 1:** Kern-Konsolidierung (Najika finalisieren)')
    content.append('**Phase 2:** Digivice App-Entwicklung (PWA)')
    content.append('**Phase 3:** UEFN-Portierung (Fortnite)')
    content.append('**Phase 4:** Öffentlicher Release')
    content.append('**Phase 5:** Langzeit-Vision (Lebenslange Begleitung)')
    content.append('')

content.append('---')
content.append('')

# ANWEISUNGEN FÜR CLAUDE
content.append('# ANWEISUNGEN FÜR CLAUDE')
content.append('')
content.append('## PFLICHT beim Start:')
content.append('1. `python najika_smart_update_v2.py` ausführen')
content.append('2. `CLAUDE_SMART_UPDATE.md` KOMPLETT lesen')
content.append('3. Alle erwähnten Files lesen')
content.append('4. User KURZ fragen was als nächstes (max 2 Sätze!)')
content.append('')
content.append('## REGELN:')
content.append('- NIEMALS den Grundstein ohne Nachfrage ändern')
content.append('- Read IMMER komplett vor Edit')
content.append('- Grep für Suchen, nicht File-Reading')
content.append('- Kurze Antworten - User kennt Kontext!')
content.append('- Token-Effizienz: Najika nutzen für große Aufgaben')
content.append('')
content.append('## WICHTIGE FILES:')
content.append('- `CLAUDE.md` - Projekt-Übersicht')
content.append('- `GRUNDSTEIN_INVENTAR.md` - Basis-System')
content.append('- `CLAUDE_SMART_UPDATE.md` - Session-Update')
content.append('- `najika_server.py` - Backend')
content.append('- `digivice/index.html` - Frontend')
content.append('')
content.append('---')
content.append('')
content.append('**ENDE MASTER-ZUSAMMENFASSUNG**')

# Speichern
OUTPUT.write_text('\n'.join(content), encoding='utf-8')

print('\n' + '='*80)
print('FERTIG!')
print('='*80)
print(f'\nGespeichert: {OUTPUT}')
print(f'Größe: {OUTPUT.stat().st_size:,} bytes')
print('\n✅ Jeder Claude kann jetzt damit arbeiten!')
print('='*80)
