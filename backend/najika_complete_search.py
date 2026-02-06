#!/usr/bin/env python3
"""
NAJIKA: Durchsuche ZIP-Ordner nach ALLEN Ideen/Ansätzen
"""
from pathlib import Path
import json

ZIP_DIR = Path('C:/Users/0KKK0/Desktop/zip')
OUTPUT = Path('C:/Najika_World/ZIP_ORDNER_KOMPLETT_INVENTAR.json')

print('NAJIKA: Durchsuche ZIP-Ordner komplett...\n')

# Kategorien für Suche
KATEGORIEN = {
    'CODEX': ['codex'],
    'SKILL_SYSTEME': ['skill', 'skyrim', 'use-based', 'transformation', 'weaving'],
    'COMBAT': ['combat', 'kampf', 'soulframe', 'dark souls', 'digimon world'],
    'SPELL_MAGIC': ['spell', 'magic', 'magie', 'explosion', 'megumin'],
    'SPIEL_IDEEN': ['spiel', 'game', 'concept', 'konzept', 'idee'],
    '8_GEBIETE': ['8 gebiete', 'crimson desert', 'celestial', 'oregon'],
    'SLIME_BEGLEITER': ['slime', 'companion', 'begleiter', 'pet'],
    'FORTNITE_UEFN': ['fortnite', 'uefn', 'portal', 'universum'],
    'CRAFTING_HOUSING': ['crafting', 'housing', 'alchemie', 'alchemy'],
    'PERSOENLICHKEIT': ['megumin', 'harley', 'shiro', 'melissa', 'najika'],
    'ROADMAP': ['roadmap', 'plan', 'übersicht', 'zusammenfassung'],
    'INSTALLER': ['install', 'setup', 'complete', 'rebuild'],
}

# Sammle alle Dateien
inventar = {}

for kategorie, keywords in KATEGORIEN.items():
    inventar[kategorie] = {
        'dateien': [],
        'groesse_gesamt': 0,
        'anzahl': 0
    }

# Durchsuche alle Dateien
print('Durchsuche Dateien...')
alle_dateien = list(ZIP_DIR.glob('*'))
print(f'Gefunden: {len(alle_dateien)} Dateien\n')

for datei in alle_dateien:
    if not datei.is_file():
        continue

    datei_name_lower = datei.name.lower()
    datei_groesse = datei.stat().st_size

    # Prüfe gegen alle Kategorien
    for kategorie, keywords in KATEGORIEN.items():
        for keyword in keywords:
            if keyword in datei_name_lower:
                inventar[kategorie]['dateien'].append({
                    'name': datei.name,
                    'groesse': datei_groesse,
                    'pfad': str(datei),
                    'keyword_match': keyword
                })
                inventar[kategorie]['groesse_gesamt'] += datei_groesse
                inventar[kategorie]['anzahl'] += 1
                break  # Nur einmal pro Kategorie zählen

# Ausgabe
print('='*80)
print('ERGEBNISSE:')
print('='*80)

for kategorie, data in inventar.items():
    if data['anzahl'] > 0:
        print(f'\n{kategorie}: {data["anzahl"]} Dateien ({data["groesse_gesamt"]:,} bytes)')
        for datei in data['dateien'][:5]:  # Zeige max 5
            print(f'  - {datei["name"]} ({datei["groesse"]:,} bytes) [keyword: {datei["keyword_match"]}]')
        if data['anzahl'] > 5:
            print(f'  ... und {data["anzahl"] - 5} weitere')

# Speichere als JSON
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(inventar, f, indent=2, ensure_ascii=False)

print(f'\n\nInventar gespeichert: {OUTPUT}')
print(f'Gesamtzahl Kategorien mit Treffern: {sum(1 for v in inventar.values() if v["anzahl"] > 0)}')
