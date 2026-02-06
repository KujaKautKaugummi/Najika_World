#!/usr/bin/env python3
"""
NAJIKA: Technisches Inventar von NajikaCore
NUR CODE/FILES/CONFIG - KEINE Chat-History, KEINE Meinungen
Reiner IST-Zustand der Installation
"""
import json
from pathlib import Path
from datetime import datetime

NAJIKA_DIR = Path('C:/Najika_World')
OUTPUT_FILE = Path('C:/Users/0KKK0/Desktop/NAJIKACORE_TECHNISCHER_STATUS.txt')

# Wichtige Config/Code Files
IMPORTANT_FILES = [
    '.env',
    'najika_server.py',
    'START_NAJIKA.bat',
    'digivice/index.html',
    'assets/room_config_detailed.json'
]

def scan_directory_structure():
    """Scannt Verzeichnisstruktur"""
    structure = {}

    for item in NAJIKA_DIR.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(NAJIKA_DIR)
            parent = str(rel_path.parent)

            if parent not in structure:
                structure[parent] = []

            structure[parent].append({
                'name': item.name,
                'size': item.stat().st_size,
                'ext': item.suffix,
                'modified': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            })

    return structure

def analyze_python_files():
    """Analysiert alle Python-Dateien"""
    py_files = []

    for py_file in NAJIKA_DIR.glob('*.py'):
        try:
            content = py_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Funktionen/Klassen zählen
            functions = len([l for l in lines if l.strip().startswith('def ')])
            classes = len([l for l in lines if l.strip().startswith('class ')])
            imports = len([l for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')])

            py_files.append({
                'name': py_file.name,
                'size': py_file.stat().st_size,
                'lines': len(lines),
                'functions': functions,
                'classes': classes,
                'imports': imports
            })
        except:
            pass

    return sorted(py_files, key=lambda x: x['size'], reverse=True)

def analyze_json_files():
    """Analysiert JSON Config-Dateien"""
    json_files = []

    for json_file in NAJIKA_DIR.rglob('*.json'):
        try:
            content = json_file.read_text(encoding='utf-8')
            data = json.loads(content)

            json_files.append({
                'path': str(json_file.relative_to(NAJIKA_DIR)),
                'size': json_file.stat().st_size,
                'keys': list(data.keys()) if isinstance(data, dict) else None,
                'items': len(data) if isinstance(data, (list, dict)) else None
            })
        except:
            pass

    return json_files

def analyze_room_config():
    """Analysiert room_config_detailed.json"""
    config_file = NAJIKA_DIR / 'assets' / 'room_config_detailed.json'

    if not config_file.exists():
        return None

    try:
        data = json.load(open(config_file, encoding='utf-8'))

        rooms = []
        for room_name, room_data in data.items():
            rooms.append({
                'name': room_name,
                'floor': room_data.get('floor', {}).get('model', 'N/A'),
                'wall': room_data.get('walls', {}).get('model', 'N/A'),
                'props': len(room_data.get('props', [])),
                'palette': room_data.get('palette', {})
            })

        return rooms
    except:
        return None

def analyze_server_py():
    """Analysiert najika_server.py"""
    server_file = NAJIKA_DIR / 'najika_server.py'

    if not server_file.exists():
        return None

    try:
        content = server_file.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Extrahiere Imports
        imports = [l.strip() for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')]

        # Extrahiere ROOMS
        rooms = None
        for line in lines:
            if 'ROOMS = [' in line or 'ROOMS=[' in line:
                # Versuche zu parsen
                try:
                    start = content.find('ROOMS')
                    bracket_start = content.find('[', start)
                    bracket_end = content.find(']', bracket_start)
                    rooms_str = content[bracket_start:bracket_end+1]
                    rooms = eval(rooms_str)
                except:
                    pass
                break

        # Extrahiere API Endpoints (einfache Suche)
        endpoints = []
        for line in lines:
            if 'def do_GET' in line or 'def do_POST' in line:
                endpoints.append(line.strip())
            if 'path ==' in line or 'path.startswith' in line:
                endpoints.append(line.strip())

        return {
            'lines': len(lines),
            'imports': imports[:10],  # Erste 10
            'rooms': rooms,
            'endpoints_hints': endpoints[:20]  # Erste 20
        }
    except:
        return None

def analyze_index_html():
    """Analysiert digivice/index.html"""
    html_file = NAJIKA_DIR / 'digivice' / 'index.html'

    if not html_file.exists():
        return None

    try:
        content = html_file.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Finde Script-Includes
        scripts = []
        for line in lines:
            if '<script' in line and 'src=' in line:
                scripts.append(line.strip())

        return {
            'lines': len(lines),
            'size': html_file.stat().st_size,
            'scripts': scripts
        }
    except:
        return None

def analyze_env():
    """Analysiert .env (OHNE Secrets!)"""
    env_file = NAJIKA_DIR / '.env'

    if not env_file.exists():
        return None

    try:
        content = env_file.read_text(encoding='utf-8')
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]

        # Nur Keys, KEINE Values
        keys = []
        for line in lines:
            if '=' in line:
                key = line.split('=')[0].strip()
                keys.append(key)

        return {
            'keys_found': keys,
            'total_lines': len(lines)
        }
    except:
        return None

def main():
    print('='*80)
    print('NAJIKA: Technisches Inventar - NUR IST-Zustand')
    print('='*80)
    print('')

    lines = []
    lines.append('='*80)
    lines.append('NAJIKACORE - TECHNISCHER STATUS (REIN FAKTISCH)')
    lines.append('='*80)
    lines.append('')
    lines.append(f'Erstellt: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append(f'Basis-Verzeichnis: {NAJIKA_DIR}')
    lines.append('')
    lines.append('='*80)
    lines.append('HINWEIS: Nur technische Fakten - keine Interpretationen!')
    lines.append('='*80)
    lines.append('')

    # 1. Verzeichnisstruktur
    print('[1/8] Scanne Verzeichnisstruktur...')
    structure = scan_directory_structure()

    lines.append('='*80)
    lines.append('1. VERZEICHNISSTRUKTUR')
    lines.append('='*80)
    lines.append('')

    for folder in sorted(structure.keys()):
        files = structure[folder]
        lines.append(f'\n[{folder}] - {len(files)} Dateien')
        lines.append('-'*80)

        # Nach Größe sortiert
        for f in sorted(files, key=lambda x: x['size'], reverse=True)[:10]:
            size_kb = f['size'] / 1024
            lines.append(f"  {f['name']:<40} {size_kb:>10.1f} KB  {f['ext']:<8} {f['modified']}")

    lines.append('')

    # 2. Python-Dateien
    print('[2/8] Analysiere Python-Dateien...')
    py_files = analyze_python_files()

    lines.append('='*80)
    lines.append('2. PYTHON-DATEIEN (HAUPTVERZEICHNIS)')
    lines.append('='*80)
    lines.append('')
    lines.append(f'Gesamt: {len(py_files)} Dateien')
    lines.append('')
    lines.append(f"{'Name':<40} {'Zeilen':>8} {'Func':>6} {'Class':>6} {'KB':>8}")
    lines.append('-'*80)

    for py in py_files:
        lines.append(f"{py['name']:<40} {py['lines']:>8} {py['functions']:>6} {py['classes']:>6} {py['size']/1024:>8.1f}")

    lines.append('')

    # 3. JSON Config-Dateien
    print('[3/8] Analysiere JSON-Dateien...')
    json_files = analyze_json_files()

    lines.append('='*80)
    lines.append('3. JSON KONFIGURATIONSDATEIEN')
    lines.append('='*80)
    lines.append('')
    lines.append(f'Gesamt: {len(json_files)} Dateien')
    lines.append('')

    for jf in json_files:
        lines.append(f"\nDatei: {jf['path']}")
        lines.append(f"  Größe: {jf['size']/1024:.1f} KB")
        if jf['keys']:
            lines.append(f"  Keys: {', '.join(jf['keys'][:10])}")
        if jf['items']:
            lines.append(f"  Items: {jf['items']}")

    lines.append('')

    # 4. Room Config
    print('[4/8] Analysiere Room Config...')
    rooms = analyze_room_config()

    if rooms:
        lines.append('='*80)
        lines.append('4. RAUM-KONFIGURATION (room_config_detailed.json)')
        lines.append('='*80)
        lines.append('')
        lines.append(f'Gesamt: {len(rooms)} Räume')
        lines.append('')
        lines.append(f"{'Raum':<30} {'Floor':<25} {'Wall':<25} {'Props':>6}")
        lines.append('-'*80)

        for room in rooms:
            lines.append(f"{room['name']:<30} {room['floor']:<25} {room['wall']:<25} {room['props']:>6}")

    lines.append('')

    # 5. Server.py
    print('[5/8] Analysiere najika_server.py...')
    server = analyze_server_py()

    if server:
        lines.append('='*80)
        lines.append('5. NAJIKA_SERVER.PY')
        lines.append('='*80)
        lines.append('')
        lines.append(f"Zeilen: {server['lines']}")
        lines.append('')
        lines.append('Imports (erste 10):')
        for imp in server['imports']:
            lines.append(f"  {imp}")
        lines.append('')

        if server['rooms']:
            lines.append(f"ROOMS Array ({len(server['rooms'])} Räume):")
            for room in server['rooms']:
                lines.append(f"  - {room}")

    lines.append('')

    # 6. Index.html
    print('[6/8] Analysiere index.html...')
    html = analyze_index_html()

    if html:
        lines.append('='*80)
        lines.append('6. DIGIVICE/INDEX.HTML')
        lines.append('='*80)
        lines.append('')
        lines.append(f"Zeilen: {html['lines']}")
        lines.append(f"Größe: {html['size']/1024:.1f} KB")
        lines.append('')
        lines.append('Eingebundene Scripts:')
        for script in html['scripts']:
            lines.append(f"  {script}")

    lines.append('')

    # 7. .env
    print('[7/8] Analysiere .env...')
    env = analyze_env()

    if env:
        lines.append('='*80)
        lines.append('7. ENVIRONMENT-KONFIGURATION (.env)')
        lines.append('='*80)
        lines.append('')
        lines.append(f"Konfigurationszeilen: {env['total_lines']}")
        lines.append('')
        lines.append('Definierte Keys (OHNE Werte):')
        for key in env['keys_found']:
            lines.append(f"  {key}")

    lines.append('')

    # 8. Statistik
    print('[8/8] Erstelle Statistik...')

    lines.append('='*80)
    lines.append('8. GESAMT-STATISTIK')
    lines.append('='*80)
    lines.append('')

    total_files = sum(len(files) for files in structure.values())
    total_size = sum(f['size'] for files in structure.values() for f in files)

    lines.append(f"Gesamt Dateien: {total_files}")
    lines.append(f"Gesamt Größe: {total_size/1024/1024:.1f} MB")
    lines.append(f"Python-Dateien (Hauptverzeichnis): {len(py_files)}")
    lines.append(f"JSON-Dateien: {len(json_files)}")
    if rooms:
        lines.append(f"Konfigurierte Räume: {len(rooms)}")

    lines.append('')
    lines.append('='*80)
    lines.append('ENDE TECHNISCHES INVENTAR')
    lines.append('='*80)

    # Speichern
    OUTPUT_FILE.write_text('\n'.join(lines), encoding='utf-8')

    print('')
    print('='*80)
    print('FERTIG')
    print('='*80)
    print(f'\n[OK] Technischer Status: {OUTPUT_FILE}')
    print(f'[OK] Zeilen: {len(lines)}')
    print(f'[OK] Dateien analysiert: {total_files}')
    print('')

if __name__ == '__main__':
    main()
