#!/usr/bin/env python3
"""
NAJIKA: Wende User-Entscheidungen aus BAUSTEIN_SYSTEM.json an
- Liest User-Entscheidungen
- Erstellt FINALE_KONFIGURATION.json
- Listet alle Änderungen auf
"""
import json
from pathlib import Path
from datetime import datetime

BAUSTEIN_FILE = Path('C:/NajikaCore/BAUSTEIN_SYSTEM.json')
OUTPUT_FILE = Path('C:/NajikaCore/FINALE_KONFIGURATION.json')
CHANGELOG_FILE = Path('C:/NajikaCore/ÄNDERUNGEN_LOG.md')

print('='*80)
print('NAJIKA: Wende Baustein-Entscheidungen an')
print('='*80)

# Lade Bausteine
with open(BAUSTEIN_FILE, 'r', encoding='utf-8') as f:
    bausteine = json.load(f)

# Sammle Entscheidungen
änderungen = {
    'HINZUFÜGEN': [],
    'ERSETZEN': [],
    'ANPASSEN': [],
    'MÜLL': [],
    'SPÄTER': [],
    'GRUNDSTEIN_ÄNDERUNGEN': []
}

# Analysiere neue Bausteine
print('\n[1/3] Analysiere neue Bausteine...')
for name, baustein in bausteine['NEUE_BAUSTEINE'].items():
    if name == 'beschreibung':
        continue

    status = baustein.get('user_entscheidung', baustein.get('status', 'OFFEN'))

    if status in änderungen:
        änderungen[status].append({
            'name': name,
            'quelle': baustein.get('quelle', 'unbekannt'),
            'beschreibung': baustein.get('beschreibung', ''),
            'priorität': baustein.get('priorität', 0),
            'ersetzt_was': baustein.get('ersetzt_was'),
            'notizen': baustein.get('notizen', '')
        })

# Analysiere Grundstein-Änderungen
print('[2/3] Analysiere Grundstein-Änderungen...')
for name, änderung in bausteine['ÄNDERBARE_GRUNDSTEIN_TEILE'].items():
    if name == 'beschreibung':
        continue

    if änderung.get('user_entscheidung'):
        änderungen['GRUNDSTEIN_ÄNDERUNGEN'].append({
            'name': name,
            'komponente': änderung.get('komponente'),
            'aktuell': änderung.get('aktuell'),
            'neu': änderung.get('user_entscheidung'),
            'typ': änderung.get('änderungs_typ'),
            'notizen': änderung.get('notizen', '')
        })

# Erstelle Finale Konfiguration
print('[3/3] Erstelle finale Konfiguration...\n')

finale_config = {
    'meta': {
        'version': '1.0',
        'datum': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'beschreibung': 'Finale Najika-Konfiguration nach User-Entscheidungen'
    },
    'grundstein': bausteine['GRUNDSTEIN'],
    'hinzugefügt': [b for b in änderungen['HINZUFÜGEN']],
    'ersetzt': [b for b in änderungen['ERSETZEN']],
    'angepasst': [b for b in änderungen['ANPASSEN']],
    'verworfen': [b for b in änderungen['MÜLL']],
    'später': [b for b in änderungen['SPÄTER']],
    'grundstein_änderungen': änderungen['GRUNDSTEIN_ÄNDERUNGEN'],
    'statistik': {
        'bausteine_hinzugefügt': len(änderungen['HINZUFÜGEN']),
        'bausteine_ersetzt': len(änderungen['ERSETZEN']),
        'bausteine_angepasst': len(änderungen['ANPASSEN']),
        'bausteine_verworfen': len(änderungen['MÜLL']),
        'bausteine_später': len(änderungen['SPÄTER']),
        'grundstein_änderungen': len(änderungen['GRUNDSTEIN_ÄNDERUNGEN'])
    }
}

# Speichere finale Konfiguration
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(finale_config, f, indent=2, ensure_ascii=False)

# Erstelle Changelog
changelog = f"""# NAJIKA ÄNDERUNGEN LOG
**Datum**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## ✅ HINZUGEFÜGT ({len(änderungen['HINZUFÜGEN'])} Bausteine)

"""

for b in sorted(änderungen['HINZUFÜGEN'], key=lambda x: x['priorität']):
    changelog += f"""### {b['name']}
- **Quelle**: `{b['quelle']}`
- **Beschreibung**: {b['beschreibung']}
- **Priorität**: {b['priorität']}
- **Notizen**: {b['notizen']}

"""

changelog += f"""
---

## 🔄 ERSETZT ({len(änderungen['ERSETZEN'])} Bausteine)

"""

for b in änderungen['ERSETZEN']:
    changelog += f"""### {b['name']}
- **Quelle**: `{b['quelle']}`
- **Beschreibung**: {b['beschreibung']}
- **Ersetzt**: `{b['ersetzt_was']}`
- **Notizen**: {b['notizen']}

"""

changelog += f"""
---

## 🛠️ ANGEPASST ({len(änderungen['ANPASSEN'])} Bausteine)

"""

for b in änderungen['ANPASSEN']:
    changelog += f"""### {b['name']}
- **Quelle**: `{b['quelle']}`
- **Beschreibung**: {b['beschreibung']}
- **Passt an**: `{b['ersetzt_was']}`
- **Notizen**: {b['notizen']}

"""

changelog += f"""
---

## 🔧 GRUNDSTEIN-ÄNDERUNGEN ({len(änderungen['GRUNDSTEIN_ÄNDERUNGEN'])} Änderungen)

"""

for ä in änderungen['GRUNDSTEIN_ÄNDERUNGEN']:
    changelog += f"""### {ä['name']}
- **Komponente**: `{ä['komponente']}`
- **Aktuell**: {ä['aktuell']}
- **Neu**: {ä['neu']}
- **Typ**: {ä['typ']}
- **Notizen**: {ä['notizen']}

"""

changelog += f"""
---

## ⏳ SPÄTER ({len(änderungen['SPÄTER'])} Bausteine)

"""

for b in änderungen['SPÄTER']:
    changelog += f"""### {b['name']}
- **Quelle**: `{b['quelle']}`
- **Beschreibung**: {b['beschreibung']}
- **Notizen**: {b['notizen']}

"""

changelog += f"""
---

## ❌ VERWORFEN ({len(änderungen['MÜLL'])} Bausteine)

"""

for b in änderungen['MÜLL']:
    changelog += f"""### {b['name']}
- **Quelle**: `{b['quelle']}`
- **Beschreibung**: {b['beschreibung']}
- **Notizen**: {b['notizen']}

"""

# Speichere Changelog
with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
    f.write(changelog)

# Ausgabe
print('='*80)
print('ERGEBNISSE:')
print('='*80)
print(f'\n✅ HINZUFÜGEN:    {len(änderungen["HINZUFÜGEN"])} Bausteine')
for b in änderungen['HINZUFÜGEN']:
    print(f'   - {b["name"]} (Priorität {b["priorität"]})')

print(f'\n🔄 ERSETZEN:      {len(änderungen["ERSETZEN"])} Bausteine')
for b in änderungen['ERSETZEN']:
    print(f'   - {b["name"]} → ersetzt {b["ersetzt_was"]}')

print(f'\n🛠️ ANPASSEN:      {len(änderungen["ANPASSEN"])} Bausteine')
for b in änderungen['ANPASSEN']:
    print(f'   - {b["name"]} → passt {b["ersetzt_was"]} an')

print(f'\n🔧 GRUNDSTEIN:    {len(änderungen["GRUNDSTEIN_ÄNDERUNGEN"])} Änderungen')
for ä in änderungen['GRUNDSTEIN_ÄNDERUNGEN']:
    print(f'   - {ä["name"]} ({ä["typ"]})')

print(f'\n⏳ SPÄTER:        {len(änderungen["SPÄTER"])} Bausteine')
for b in änderungen['SPÄTER']:
    print(f'   - {b["name"]}')

print(f'\n❌ VERWORFEN:     {len(änderungen["MÜLL"])} Bausteine')
for b in änderungen['MÜLL']:
    print(f'   - {b["name"]}')

print('\n' + '='*80)
print('DATEIEN ERSTELLT:')
print('='*80)
print(f'  1. {OUTPUT_FILE}')
print(f'  2. {CHANGELOG_FILE}')
print('\n✅ FERTIG! Claude kann jetzt die Änderungen implementieren.')
print('='*80)
