#!/usr/bin/env python3
"""
NAJIKA: Erstelle lesbare Übersicht aus technischem Status
NUR basierend auf faktischen Daten - keine Spekulationen
"""
import json
from pathlib import Path
from datetime import datetime

NAJIKA_DIR = Path('C:/Najika_World')
OUTPUT_FILE = Path('C:/Users/0KKK0/Desktop/NAJIKA_LESBARE_UEBERSICHT.txt')

def analyze_server():
    """Analysiert Server-Capabilities"""
    server_file = NAJIKA_DIR / 'najika_server.py'

    if not server_file.exists():
        return {}

    content = server_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    info = {
        'imports': [],
        'rooms': [],
        'endpoints': [],
        'state_variables': [],
        'features': []
    }

    # Imports
    for line in lines:
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            info['imports'].append(line.strip())

    # ROOMS Array
    for i, line in enumerate(lines):
        if 'ROOMS = [' in line or 'ROOMS=[' in line:
            # Sammle bis ]
            rooms_str = line
            j = i
            while ']' not in rooms_str:
                j += 1
                if j < len(lines):
                    rooms_str += lines[j]
            try:
                start = rooms_str.find('[')
                end = rooms_str.find(']') + 1
                info['rooms'] = eval(rooms_str[start:end])
            except:
                pass
            break

    # Endpoints (do_GET, do_POST)
    current_method = None
    for line in lines:
        if 'def do_GET' in line:
            current_method = 'GET'
        elif 'def do_POST' in line:
            current_method = 'POST'

        if current_method and ('path ==' in line or 'path.startswith' in line):
            # Extrahiere Endpoint
            if '"' in line or "'" in line:
                parts = line.split('"') if '"' in line else line.split("'")
                if len(parts) >= 2:
                    endpoint = parts[1]
                    info['endpoints'].append(f"{current_method} {endpoint}")

    # STATE Dictionary
    in_state = False
    for i, line in enumerate(lines):
        if 'STATE = {' in line:
            in_state = True
            continue
        if in_state:
            if line.strip().startswith('}'):
                break
            if '":' in line or '"' in line:
                # Extrahiere Key
                if '"' in line:
                    key = line.split('"')[1]
                    info['state_variables'].append(key)

    # Features (durch Kommentare/Importe erkennen)
    if 'najika_living_system' in content:
        info['features'].append('Living System')
    if 'najika_memory' in content:
        info['features'].append('Memory System (ChromaDB)')
    if 'najika_search' in content:
        info['features'].append('Web Search')
    if 'najika_tor' in content:
        info['features'].append('Tor Browser Integration')
    if 'najika_security' in content:
        info['features'].append('Security Module')
    if 'najika_battle' in content:
        info['features'].append('Battle System')
    if 'private_mode' in content:
        info['features'].append('Private Mode')
    if 'ollama' in content.lower():
        info['features'].append('Ollama AI Integration')

    return info

def analyze_frontend():
    """Analysiert Frontend-Capabilities"""
    html_file = NAJIKA_DIR / 'digivice' / 'index.html'

    if not html_file.exists():
        return {}

    content = html_file.read_text(encoding='utf-8')

    info = {
        'scripts': [],
        'features': []
    }

    # Script-Includes
    for line in content.split('\n'):
        if '<script' in line and 'src=' in line:
            if '.js' in line:
                # Extrahiere Dateiname
                parts = line.split('src=')
                if len(parts) >= 2:
                    script_path = parts[1].split('"')[1] if '"' in parts[1] else parts[1].split("'")[1]
                    script_name = script_path.split('/')[-1]
                    info['scripts'].append(script_name)

    # Features durch Script-Namen
    script_features = {
        '3d_scene.js': '3D-Szene (Three.js)',
        'kaykit_loader.js': 'KayKit Asset-Loader',
        'minigames.js': 'Minispiele',
        'battle_core.js': 'Kampfsystem (Client)',
        'private_mode.js': 'Private Mode Indicator',
        'touch_controls.js': 'Touch-Steuerung',
        'chat_ui.js': 'Chat-Interface',
        'room_connector.js': 'Raum-Verbindung'
    }

    for script in info['scripts']:
        if script in script_features:
            info['features'].append(script_features[script])

    return info

def analyze_room_config():
    """Analysiert Raum-Konfiguration"""
    config_file = NAJIKA_DIR / 'assets' / 'room_config_detailed.json'

    if not config_file.exists():
        return {}

    data = json.load(open(config_file, encoding='utf-8'))

    # rooms ist ein Array
    rooms_list = data.get('rooms', [])

    rooms = []
    for room_data in rooms_list:
        rooms.append({
            'name': room_data.get('name', 'N/A'),
            'floor_model': room_data.get('floor', {}).get('model', 'N/A'),
            'wall_model': room_data.get('walls', {}).get('model', 'N/A'),
            'props_count': len(room_data.get('props', [])),
            'has_palette': 'palette' in room_data,
            'spawn_point': room_data.get('spawnPoint', 'N/A')
        })

    return rooms

def analyze_python_modules():
    """Analysiert vorhandene Python-Module"""
    modules = []

    # Wichtige Module
    important = [
        'najika_server.py',
        'najika_living_system.py',
        'najika_memory.py',
        'najika_battle.py',
        'najika_search.py',
        'najika_tor.py',
        'najika_security.py',
        'najika_enhanced_personality.py'
    ]

    for module in important:
        module_file = NAJIKA_DIR / module
        if module_file.exists():
            content = module_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Finde Docstring
            docstring = None
            if '"""' in content:
                try:
                    start = content.find('"""') + 3
                    end = content.find('"""', start)
                    docstring = content[start:end].strip().split('\n')[0]
                except:
                    pass

            modules.append({
                'name': module,
                'exists': True,
                'lines': len(lines),
                'docstring': docstring,
                'size_kb': module_file.stat().st_size / 1024
            })
        else:
            modules.append({
                'name': module,
                'exists': False
            })

    return modules

def analyze_training_system():
    """Analysiert Training-System"""
    training_dir = NAJIKA_DIR / 'training'

    if not training_dir.exists():
        return None

    info = {
        'exists': True,
        'resources': [],
        'scheduler_exists': False
    }

    # Ressourcen
    resources = [
        'CODE_KATAS_DAILY.md',
        'COMMON_PITFALLS.md',
        'PERFORMANCE_PATTERNS.md',
        'ARCHITECTURE_PATTERNS.md'
    ]

    for res in resources:
        res_file = training_dir / res
        if res_file.exists():
            info['resources'].append({
                'name': res,
                'size_kb': res_file.stat().st_size / 1024
            })

    # Scheduler
    scheduler = NAJIKA_DIR / 'najika_training_scheduler.py'
    info['scheduler_exists'] = scheduler.exists()

    return info

def analyze_env_config():
    """Analysiert .env Konfiguration"""
    env_file = NAJIKA_DIR / '.env'

    if not env_file.exists():
        return None

    content = env_file.read_text(encoding='utf-8')
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]

    config = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            # Für bestimmte Keys geben wir Info (nicht Secret!)
            if key.strip() in ['HOST', 'PORT', 'AI_PROVIDER', 'CLOUD_ENABLED', 'NSFW_LOCAL']:
                config[key.strip()] = value.strip()
            else:
                config[key.strip()] = '[CONFIGURED]'

    return config

def main():
    print('='*80)
    print('NAJIKA: Erstelle lesbare Übersicht')
    print('='*80)
    print('')

    lines = []
    lines.append('='*80)
    lines.append('NAJIKA - LESBARE PROJEKT-ÜBERSICHT')
    lines.append('='*80)
    lines.append('')
    lines.append(f'Erstellt: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append('')
    lines.append('Diese Übersicht zeigt was Najika JETZT kann - basierend auf')
    lines.append('vorhandenem Code, Konfiguration und Ressourcen.')
    lines.append('')
    lines.append('='*80)
    lines.append('')

    # 1. SERVER-FUNKTIONEN
    print('[1/7] Analysiere Server...')
    server = analyze_server()

    lines.append('## 1. SERVER (najika_server.py)')
    lines.append('='*80)
    lines.append('')

    if server.get('rooms'):
        lines.append(f'**RÄUME ({len(server["rooms"])}):**')
        for i, room in enumerate(server['rooms'], 1):
            lines.append(f'  {i:2d}. {room}')
        lines.append('')

    if server.get('features'):
        lines.append('**INTEGRIERTE SYSTEME:**')
        for feature in server['features']:
            lines.append(f'  - {feature}')
        lines.append('')

    if server.get('endpoints'):
        lines.append(f'**API-ENDPUNKTE ({len(server["endpoints"])}):**')
        # Deduplizieren
        unique_endpoints = list(set(server['endpoints']))
        for endpoint in sorted(unique_endpoints)[:20]:  # Erste 20
            lines.append(f'  - {endpoint}')
        if len(unique_endpoints) > 20:
            lines.append(f'  ... und {len(unique_endpoints)-20} weitere')
        lines.append('')

    if server.get('state_variables'):
        lines.append('**STATE-VARIABLEN:**')
        for var in server['state_variables'][:15]:  # Erste 15
            lines.append(f'  - {var}')
        lines.append('')

    # 2. FRONTEND
    print('[2/7] Analysiere Frontend...')
    frontend = analyze_frontend()

    lines.append('## 2. FRONTEND (digivice/index.html)')
    lines.append('='*80)
    lines.append('')

    if frontend.get('scripts'):
        lines.append(f'**GELADENE SCRIPTS ({len(frontend["scripts"])}):**')
        for script in frontend['scripts']:
            lines.append(f'  - {script}')
        lines.append('')

    if frontend.get('features'):
        lines.append('**FRONTEND-FEATURES:**')
        for feature in frontend['features']:
            lines.append(f'  - {feature}')
        lines.append('')

    # 3. RÄUME
    print('[3/7] Analysiere Räume...')
    rooms = analyze_room_config()

    if rooms:
        lines.append('## 3. RAUM-KONFIGURATION')
        lines.append('='*80)
        lines.append('')
        lines.append(f'**KONFIGURIERTE RÄUME ({len(rooms)}):**')
        lines.append('')

        for room in rooms:
            lines.append(f"### {room['name']}")
            lines.append(f"  - Floor: {room['floor_model']}")
            lines.append(f"  - Walls: {room['wall_model']}")
            lines.append(f"  - Props: {room['props_count']}")
            lines.append(f"  - Palette: {'Ja' if room['has_palette'] else 'Nein'}")
            lines.append('')

    # 4. PYTHON-MODULE
    print('[4/7] Analysiere Python-Module...')
    modules = analyze_python_modules()

    lines.append('## 4. PYTHON-MODULE')
    lines.append('='*80)
    lines.append('')

    existing = [m for m in modules if m['exists']]
    missing = [m for m in modules if not m['exists']]

    lines.append(f'**VORHANDENE MODULE ({len(existing)}):**')
    lines.append('')
    for mod in existing:
        lines.append(f"**{mod['name']}** ({mod['lines']} Zeilen, {mod['size_kb']:.1f} KB)")
        if mod['docstring']:
            lines.append(f"  → {mod['docstring']}")
        lines.append('')

    if missing:
        lines.append('**FEHLENDE MODULE:**')
        for mod in missing:
            lines.append(f"  - {mod['name']}")
        lines.append('')

    # 5. TRAINING
    print('[5/7] Analysiere Training-System...')
    training = analyze_training_system()

    if training:
        lines.append('## 5. TRAINING-SYSTEM')
        lines.append('='*80)
        lines.append('')
        lines.append(f"**Status:** {'Eingerichtet' if training['scheduler_exists'] else 'Teilweise'}")
        lines.append('')

        if training['resources']:
            lines.append(f"**RESSOURCEN ({len(training['resources'])}):**")
            for res in training['resources']:
                lines.append(f"  - {res['name']} ({res['size_kb']:.1f} KB)")
            lines.append('')

        if training['scheduler_exists']:
            lines.append('**Scheduler:** najika_training_scheduler.py vorhanden')
            lines.append('**Geplant:** Montag-Freitag, 09:00-14:00 Uhr')
            lines.append('')

    # 6. KONFIGURATION
    print('[6/7] Analysiere Konfiguration...')
    env_config = analyze_env_config()

    if env_config:
        lines.append('## 6. KONFIGURATION (.env)')
        lines.append('='*80)
        lines.append('')

        for key, value in sorted(env_config.items()):
            lines.append(f'  {key:<25} = {value}')
        lines.append('')

    # 7. ZUSAMMENFASSUNG
    print('[7/7] Erstelle Zusammenfassung...')

    lines.append('## 7. ZUSAMMENFASSUNG - WAS KANN NAJIKA?')
    lines.append('='*80)
    lines.append('')

    lines.append('### SERVER-SEITE:')
    lines.append('  - Python HTTP Server läuft auf Port 8000 (konfigurierbar)')
    lines.append('  - AI-Integration über Ollama (lokal)')
    if 'CLOUD_ENABLED' in (env_config or {}):
        if env_config['CLOUD_ENABLED'].lower() == 'true':
            lines.append('  - Cloud AI Provider aktiviert')
    lines.append(f"  - {len(server.get('rooms', []))} navigierbare Räume")
    lines.append(f"  - {len(server.get('features', []))} integrierte Systeme")
    lines.append('')

    lines.append('### FRONTEND-SEITE:')
    lines.append('  - 3D-Umgebung mit Three.js')
    lines.append('  - KayKit Asset-basierte Grafik')
    lines.append('  - Interaktive Minispiele')
    lines.append('  - Chat-Interface mit AI')
    lines.append('  - Touch-Steuerung für Mobile')
    lines.append('')

    lines.append('### BESONDERE FEATURES:')
    if 'Living System' in server.get('features', []):
        lines.append('  - Living System (autonome Aktivitäten)')
    if 'Memory System (ChromaDB)' in server.get('features', []):
        lines.append('  - Persistentes Gedächtnis (ChromaDB)')
    if 'Battle System' in server.get('features', []):
        lines.append('  - Turn-based Kampfsystem')
    if 'Private Mode' in server.get('features', []):
        lines.append('  - Private Mode (trigger: "kätzchen")')
    if 'Web Search' in server.get('features', []):
        lines.append('  - Web-Suche Integration')
    if 'Security Module' in server.get('features', []):
        lines.append('  - Security Module (Alcatraz)')
    lines.append('')

    lines.append('### VORBEREITET/IN ARBEIT:')
    if training:
        lines.append('  - Training-System (Mo-Fr 09:00-14:00)')
    lines.append('  - Raum-Navigation mit 12 Räumen')
    lines.append('  - Asset-Loading System')
    lines.append('')

    lines.append('='*80)
    lines.append('ENDE ÜBERSICHT')
    lines.append('='*80)

    # Speichern
    OUTPUT_FILE.write_text('\n'.join(lines), encoding='utf-8')

    print('')
    print('='*80)
    print('FERTIG')
    print('='*80)
    print(f'\n[OK] Lesbare Übersicht: {OUTPUT_FILE}')
    print(f'[OK] Zeilen: {len(lines)}')
    print('')
    print('Zusammenfassung:')
    print(f'  - Räume: {len(server.get("rooms", []))}')
    print(f'  - Features: {len(server.get("features", []))}')
    print(f'  - Module: {len(existing)}/{len(modules)}')
    print(f'  - Frontend Scripts: {len(frontend.get("scripts", []))}')
    print('')

if __name__ == '__main__':
    main()
