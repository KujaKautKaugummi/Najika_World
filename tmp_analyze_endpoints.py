import re
import os

# Backend routes from the user
backend_routes = """
/api/battle/cheer, /api/battle/companion-action, /api/battle/companion-auto-turn, /api/battle/end/{player_id}, /api/battle/enemies, /api/battle/explain-decision, /api/battle/finisher, /api/battle/finisher/categories, /api/battle/modes, /api/battle/player-action, /api/battle/set-companion-form, /api/battle/set-companion-mode, /api/battle/skills, /api/battle/start, /api/battle/status/{player_id}
/api/building/*, /api/cards/*, /api/chat, /api/chat/, /api/chat/health, /api/chat/history, /api/chat/models, /api/chat/stream
/api/cloud/status
/api/combat-magic/combo, /api/combat-magic/grab, /api/combat-magic/grab/execute, /api/combat-magic/tids
/api/decks/*, /api/dice/*, /api/dice-duel/*
/api/farming/*, /api/housing/*
/api/instrument/*
/api/lebensraum/*
/api/living/activity/check, /api/living/activity/start, /api/living/proactive, /api/living/state
/api/magic/*
/api/matches/*, /api/memory/*
/api/meta/*
/api/music/*
/api/najika/drink, /api/najika/equipment, /api/najika/feed, /api/najika/sleep, /api/najika/status, /api/najika/wash
/api/oregon/*
/api/pvp/*
/api/rankings/*
/api/region-boss/*
/api/room/actions
/api/slime-ai/*, /api/slime-arena/*, /api/slime/*
/api/special/*
/api/spells/name/*
/api/status, /api/status/stream
/api/temperature/status
/api/v1/admin/*, /api/v1/auth/*, /api/v1/game/arena/*, /api/v1/game/character/*, /api/v1/game/combat/*, /api/v1/game/food/*, /api/v1/game/inventory/*, /api/v1/game/load, /api/v1/game/quests/*, /api/v1/game/save, /api/v1/game/skills/*
/api/v1/training/*, /api/v1/voice/*
/api/voice-ue5/*
/api/world/*, /api/world-map/*
/multiplayer/*
/najika/actions, /najika/auto-decide-action, /najika/complete-action, /najika/cook, /najika/craft, /najika/current-activity, /najika/dashboard, /najika/explore, /najika/farm, /najika/health, /najika/locations, /najika/recipes, /najika/status, /najika/suggest-action, /najika/teleport
"""

# Parse backend routes
backend_set = set()
for route in backend_routes.split(','):
    route = route.strip()
    if route:
        backend_set.add(route)

# Function to normalize endpoints
def normalize_endpoint(url):
    # Remove http://localhost:8000 prefix
    url = url.replace('http://localhost:8000', '')
    # Remove query parameters for comparison
    url = re.sub(r'\?.*$', '', url)
    # Normalize template params
    url = re.sub(r'\$\{[^}]+\}', '{param}', url)
    return url

# Function to check if endpoint matches backend route
def matches_backend(endpoint, backend_routes):
    endpoint = normalize_endpoint(endpoint)

    # Exact match
    if endpoint in backend_routes:
        return True, endpoint

    # Check wildcard routes
    for route in backend_routes:
        if route.endswith('/*'):
            prefix = route[:-2]
            if endpoint.startswith(prefix):
                return True, route
        # Check param routes
        route_pattern = re.sub(r'\{[^}]+\}', '[^/]+', route)
        if re.match(f'^{route_pattern}$', endpoint):
            return True, route

    return False, None

# Collect all API calls from frontend
api_calls = []
js_dir = r'c:\Najika_World\digivice\js'
for root, dirs, files in os.walk(js_dir):
    for file in files:
        if file.endswith('.js'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        patterns = [
                            r'fetch\s*\(\s*[`\'"]([^`\'"]+)[`\'"]',
                            r'fetch\s*\(\s*`([^`]+)`',
                            r'\.get\s*\(\s*[`\'"]([^`\'"]+)[`\'"]',
                            r'\.get\s*\(\s*`([^`]+)`',
                            r'\.post\s*\(\s*[`\'"]([^`\'"]+)[`\'"]',
                            r'\.post\s*\(\s*`([^`]+)`',
                            r'api\s*\(\s*[`\'"]([^`\'"]+)[`\'"]',
                        ]

                        for pattern in patterns:
                            matches = re.finditer(pattern, line)
                            for match in matches:
                                url = match.group(1)
                                if '/api/' in url or '/najika/' in url or '/multiplayer/' in url:
                                    url_clean = re.sub(r'\$\{[^}]+\}', '{param}', url)
                                    api_calls.append({
                                        'file': filepath.replace(js_dir, '').replace('\\', '/').lstrip('/'),
                                        'line': line_num,
                                        'url': url_clean,
                                        'original': line.strip()
                                    })
            except:
                pass

# Categorize endpoints
missing = []
prefix_mismatch = []
path_mismatch = []
matched = []

for call in api_calls:
    url = normalize_endpoint(call['url'])

    # Skip if it starts with {param} (variable base URL)
    if url.startswith('{param}'):
        url = url.replace('{param}', '')

    matches, matched_route = matches_backend(url, backend_set)

    if matches:
        matched.append(call)
    else:
        # Check for prefix mismatches
        if '/api/arena/' in url and any('/api/v1/game/arena/' in r for r in backend_set):
            prefix_mismatch.append({**call, 'suggestion': url.replace('/api/arena/', '/api/v1/game/arena/')})
        elif '/api/game/' in url and any('/api/v1/game/' in r for r in backend_set):
            prefix_mismatch.append({**call, 'suggestion': url.replace('/api/game/', '/api/v1/game/')})
        elif '/api/battle/action' in url and '/api/battle/player-action' in backend_set:
            path_mismatch.append({**call, 'suggestion': '/api/battle/player-action'})
        elif '/api/battle/status' == url and '/api/battle/status/{player_id}' in backend_set:
            path_mismatch.append({**call, 'note': 'Missing player_id parameter'})
        elif '/api/battle/reset' in url:
            missing.append({**call, 'note': 'No /api/battle/reset endpoint in backend'})
        else:
            missing.append(call)

print("=" * 80)
print("API ENDPOINT MISMATCH REPORT")
print("=" * 80)

print(f"\n1. MISSING ENDPOINTS ({len(missing)} found)")
print("-" * 80)
seen_missing = {}
for call in missing:
    url = normalize_endpoint(call['url'])
    if url not in seen_missing:
        seen_missing[url] = call
        print(f"\nEndpoint: {url}")
        print(f"  File: {call['file']}:{call['line']}")
        if 'note' in call:
            print(f"  Note: {call['note']}")

print(f"\n\n2. PREFIX MISMATCHES ({len(prefix_mismatch)} found)")
print("-" * 80)
seen_prefix = {}
for call in prefix_mismatch:
    url = normalize_endpoint(call['url'])
    if url not in seen_prefix:
        seen_prefix[url] = call
        print(f"\nFrontend calls: {url}")
        print(f"  Should be: {call['suggestion']}")
        print(f"  File: {call['file']}:{call['line']}")

print(f"\n\n3. PATH MISMATCHES ({len(path_mismatch)} found)")
print("-" * 80)
seen_path = {}
for call in path_mismatch:
    url = normalize_endpoint(call['url'])
    if url not in seen_path:
        seen_path[url] = call
        print(f"\nFrontend calls: {url}")
        if 'suggestion' in call:
            print(f"  Backend has: {call['suggestion']}")
        if 'note' in call:
            print(f"  Note: {call['note']}")
        print(f"  File: {call['file']}:{call['line']}")

print(f"\n\n4. SUMMARY")
print("-" * 80)
print(f"Total API calls found: {len(api_calls)}")
print(f"Matched endpoints: {len(matched)}")
print(f"Missing endpoints: {len(seen_missing)}")
print(f"Prefix mismatches: {len(seen_prefix)}")
print(f"Path mismatches: {len(seen_path)}")
print(f"Total issues: {len(seen_missing) + len(seen_prefix) + len(seen_path)}")
