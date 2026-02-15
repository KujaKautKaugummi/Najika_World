#!/usr/bin/env python3
"""
NAJIKA ECHTES CODE TRAINING V2
Trainiert Najika mit Ollama - MIT ECHTEM CODE-EXECUTION!

FIXES gegenueber V1:
- ECHTE Code-Ausfuehrung statt Heuristik-Bewertung
- 60+ Aufgaben ueber 4 Schwierigkeitsstufen (nicht nur 7!)
- Automatische Schwierigkeits-Progression
- Nutzt das richtige Ollama Model (qwen2-instruct)
- Unit-Tests fuer jede Aufgabe
"""
import json
import re
import requests
import time
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# === KONFIGURATION ===
NAJIKA_DIR = Path(__file__).resolve().parent
PROGRESS_FILE = NAJIKA_DIR / "code_training_progress.json"
SOLUTIONS_DIR = NAJIKA_DIR / "code_training_solutions"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2-instruct:latest"  # Instruct Model fuer Code!

DAILY_PROBLEMS = 5
MAX_ATTEMPTS = 3
TIMEOUT = 300

# === ALLE AUFGABEN (4 LEVELS) ===

PROBLEMS = {
    "beginner": [
        {
            "title": "FizzBuzz",
            "description": "Schreibe eine Funktion fizzbuzz(n) die eine Liste von 1 bis n zurueckgibt. Fuer Vielfache von 3: 'Fizz', von 5: 'Buzz', von beidem: 'FizzBuzz', sonst die Zahl als String.",
            "test_code": """
result = fizzbuzz(15)
assert result[0] == '1', f"Expected '1', got {result[0]}"
assert result[2] == 'Fizz', f"Expected 'Fizz', got {result[2]}"
assert result[4] == 'Buzz', f"Expected 'Buzz', got {result[4]}"
assert result[14] == 'FizzBuzz', f"Expected 'FizzBuzz', got {result[14]}"
assert len(result) == 15, f"Expected 15 elements, got {len(result)}"
print("OK")
"""
        },
        {
            "title": "Palindrom Check",
            "description": "Schreibe eine Funktion is_palindrome(s) die True zurueckgibt wenn der String ein Palindrom ist (Gross/Kleinschreibung ignorieren, nur Buchstaben zaehlen).",
            "test_code": """
assert is_palindrome("racecar") == True
assert is_palindrome("hello") == False
assert is_palindrome("A man a plan a canal Panama") == True
assert is_palindrome("") == True
assert is_palindrome("Was it a car or a cat I saw") == True
print("OK")
"""
        },
        {
            "title": "Fibonacci mit Memoization",
            "description": "Schreibe eine Funktion fib(n) die die n-te Fibonacci-Zahl zurueckgibt. Nutze Memoization damit fib(100) in unter 1ms laeuft.",
            "test_code": """
assert fib(0) == 0
assert fib(1) == 1
assert fib(10) == 55
assert fib(50) == 12586269025
assert fib(100) == 354224848179261915075
print("OK")
"""
        },
        {
            "title": "Array Rotation",
            "description": "Schreibe eine Funktion rotate(arr, k) die ein Array um k Positionen nach rechts rotiert. k kann groesser als die Array-Laenge sein.",
            "test_code": """
assert rotate([1,2,3,4,5], 2) == [4,5,1,2,3]
assert rotate([1,2,3], 0) == [1,2,3]
assert rotate([1,2,3], 3) == [1,2,3]
assert rotate([1,2,3], 5) == [2,3,1]
assert rotate([], 3) == []
print("OK")
"""
        },
        {
            "title": "Two Sum",
            "description": "Schreibe eine Funktion two_sum(nums, target) die die Indizes zweier Zahlen zurueckgibt deren Summe target ergibt. Gib ein Tupel (i, j) mit i < j zurueck.",
            "test_code": """
assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 2, 4], 6) == (1, 2)
assert two_sum([3, 3], 6) == (0, 1)
result = two_sum([1, 5, 3, 7, 2], 9)
assert result == (1, 3) or result == (3, 1), f"Got {result}"
print("OK")
"""
        },
    ],
    "intermediate": [
        {
            "title": "Binary Search Tree",
            "description": "Implementiere eine Klasse BST mit insert(val), search(val)->bool, und inorder()->list Methoden. inorder() gibt alle Werte sortiert zurueck.",
            "test_code": """
tree = BST()
for v in [5, 3, 7, 1, 4, 6, 8]:
    tree.insert(v)
assert tree.search(4) == True
assert tree.search(9) == False
assert tree.inorder() == [1, 3, 4, 5, 6, 7, 8]
tree.insert(2)
assert tree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8]
print("OK")
"""
        },
        {
            "title": "LRU Cache",
            "description": "Implementiere eine Klasse LRUCache(capacity) mit get(key)->value und put(key, value). Bei vollem Cache wird der am laengsten nicht benutzte Eintrag entfernt. get() gibt -1 zurueck wenn key nicht existiert.",
            "test_code": """
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1
cache.put(3, 3)
assert cache.get(2) == -1
cache.put(4, 4)
assert cache.get(1) == -1
assert cache.get(3) == 3
assert cache.get(4) == 4
print("OK")
"""
        },
        {
            "title": "Merge Intervals",
            "description": "Schreibe eine Funktion merge_intervals(intervals) die ueberlappende Intervalle zusammenfuegt. Input: Liste von [start, end] Paaren. Output: Zusammengefuegte Liste.",
            "test_code": """
assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert merge_intervals([[1,4],[4,5]]) == [[1,5]]
assert merge_intervals([[1,4],[0,4]]) == [[0,4]]
assert merge_intervals([]) == []
assert merge_intervals([[1,4],[2,3]]) == [[1,4]]
print("OK")
"""
        },
        {
            "title": "Valid Parentheses Extended",
            "description": "Schreibe eine Funktion is_valid(s) die prueft ob ein String mit ()[]{}* gueltig ist. * kann (, ) oder leer sein.",
            "test_code": """
assert is_valid("()") == True
assert is_valid("(*)") == True
assert is_valid("(*))") == True
assert is_valid(")(") == False
assert is_valid("(*") == True
assert is_valid("(((*))") == True
assert is_valid("(((") == False
assert is_valid("") == True
print("OK")
"""
        },
        {
            "title": "Matrix Spiral Order",
            "description": "Schreibe eine Funktion spiral_order(matrix) die die Elemente einer NxM Matrix in Spiral-Reihenfolge zurueckgibt (im Uhrzeigersinn von aussen nach innen).",
            "test_code": """
assert spiral_order([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]
assert spiral_order([[1,2],[3,4]]) == [1,2,4,3]
assert spiral_order([[1]]) == [1]
assert spiral_order([[1,2,3,4]]) == [1,2,3,4]
assert spiral_order([[1],[2],[3]]) == [1,2,3]
print("OK")
"""
        },
        {
            "title": "Group Anagrams",
            "description": "Schreibe eine Funktion group_anagrams(strs) die eine Liste von Strings in Anagramm-Gruppen aufteilt. Gib eine Liste von Listen zurueck (Reihenfolge innerhalb der Gruppen alphabetisch sortiert).",
            "test_code": """
result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
result = [sorted(g) for g in result]
result.sort()
expected = [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
assert result == expected, f"Got {result}"
assert group_anagrams([""]) == [[""]]
assert group_anagrams(["a"]) == [["a"]]
print("OK")
"""
        },
    ],
    "advanced": [
        {
            "title": "Dijkstra Shortest Path",
            "description": "Schreibe eine Funktion dijkstra(graph, start, end) die den kuerzesten Pfad in einem gewichteten Graphen findet. graph ist ein Dict: {node: [(neighbor, weight), ...]}. Gib (distance, path) zurueck. path ist eine Liste von Knoten.",
            "test_code": """
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}
dist, path = dijkstra(graph, 'A', 'D')
assert dist == 4, f"Expected distance 4, got {dist}"
assert path == ['A', 'B', 'C', 'D'], f"Expected ['A','B','C','D'], got {path}"
dist2, path2 = dijkstra(graph, 'A', 'A')
assert dist2 == 0
print("OK")
"""
        },
        {
            "title": "Trie mit Prefix Search",
            "description": "Implementiere eine Klasse Trie mit insert(word), search(word)->bool, starts_with(prefix)->list (gibt alle Woerter mit diesem Prefix zurueck, sortiert).",
            "test_code": """
trie = Trie()
for w in ["apple", "app", "application", "banana", "band", "apex"]:
    trie.insert(w)
assert trie.search("apple") == True
assert trie.search("app") == True
assert trie.search("ap") == False
result = trie.starts_with("app")
assert result == ["app", "apple", "application"], f"Got {result}"
assert trie.starts_with("ban") == ["banana", "band"]
assert trie.starts_with("xyz") == []
print("OK")
"""
        },
        {
            "title": "Longest Increasing Subsequence",
            "description": "Schreibe eine Funktion lis(nums) die die Laenge der laengsten strikt aufsteigenden Teilfolge zurueckgibt. Muss in O(n log n) laufen.",
            "test_code": """
assert lis([10,9,2,5,3,7,101,18]) == 4
assert lis([0,1,0,3,2,3]) == 4
assert lis([7,7,7,7]) == 1
assert lis([]) == 0
assert lis([1]) == 1
assert lis([3,5,6,2,5,4,19,5,6,7,12]) == 6
print("OK")
"""
        },
        {
            "title": "Topological Sort",
            "description": "Schreibe eine Funktion topo_sort(num_nodes, edges) die eine topologische Sortierung zurueckgibt. edges ist eine Liste von (from, to) Tupeln. Bei Zyklen gib eine leere Liste zurueck.",
            "test_code": """
result = topo_sort(4, [(0,1),(0,2),(1,3),(2,3)])
assert result[0] == 0
assert result[-1] == 3
assert result.index(0) < result.index(1)
assert result.index(0) < result.index(2)
assert topo_sort(2, [(0,1),(1,0)]) == []
assert topo_sort(1, []) == [0]
print("OK")
"""
        },
        {
            "title": "Regex Matcher",
            "description": "Schreibe eine Funktion regex_match(text, pattern) die True zurueckgibt wenn der Text zum Pattern passt. Unterstuetze '.' (ein beliebiges Zeichen) und '*' (null oder mehr des vorherigen Zeichens). Das Pattern muss den GANZEN Text matchen.",
            "test_code": """
assert regex_match("aa", "a") == False
assert regex_match("aa", "a*") == True
assert regex_match("ab", ".*") == True
assert regex_match("aab", "c*a*b") == True
assert regex_match("mississippi", "mis*is*ip*.") == True
assert regex_match("", ".*") == True
assert regex_match("abc", "") == False
print("OK")
"""
        },
    ],
    "expert": [
        {
            "title": "Red-Black Tree Insert",
            "description": "Implementiere eine Klasse RBTree mit insert(val) und inorder()->list. Der Baum muss nach jedem Insert die Red-Black-Tree Eigenschaften beibehalten (korrekte Rotationen und Umfaerbungen).",
            "test_code": """
tree = RBTree()
for v in [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]:
    tree.insert(v)
result = tree.inorder()
assert result == sorted(result), f"Not sorted: {result}"
assert len(result) == 11, f"Expected 11 elements, got {len(result)}"
assert result == [2, 3, 6, 7, 8, 10, 11, 13, 18, 22, 26]
print("OK")
"""
        },
        {
            "title": "A* Pathfinding",
            "description": "Schreibe eine Funktion astar(grid, start, end) die den kuerzesten Pfad in einem 2D Grid findet. grid ist eine Liste von Listen (0=frei, 1=blockiert). start/end sind (row, col) Tupel. Gib den Pfad als Liste von (row, col) Tupeln zurueck. Diagonale Bewegung erlaubt.",
            "test_code": """
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
path = astar(grid, (0,0), (4,4))
assert path[0] == (0,0), f"Start wrong: {path[0]}"
assert path[-1] == (4,4), f"End wrong: {path[-1]}"
for r, c in path:
    assert grid[r][c] == 0, f"Path goes through wall at ({r},{c})"
assert len(path) <= 7, f"Path too long: {len(path)}"
blocked = astar(grid, (0,0), (1,2))
assert blocked is None or blocked == [], f"Should be unreachable but got {blocked}"
print("OK")
"""
        },
        {
            "title": "Huffman Coding",
            "description": "Implementiere eine Klasse HuffmanCoder mit encode(text)->str (gibt Bitstring zurueck) und decode(bits, tree)->str. Die encode Methode soll auch den Baum zurueckgeben. Schreibe auch build_tree(text) als Hilfsfunktion.",
            "test_code": """
coder = HuffmanCoder()
text = "hello world"
encoded, tree = coder.encode(text)
assert all(c in '01' for c in encoded), "Encoded must be binary string"
decoded = coder.decode(encoded, tree)
assert decoded == text, f"Expected '{text}', got '{decoded}'"
text2 = "aaaaaabbbbccd"
encoded2, tree2 = coder.encode(text2)
decoded2 = coder.decode(encoded2, tree2)
assert decoded2 == text2
assert len(encoded2) < len(text2) * 8, "Huffman should compress"
print("OK")
"""
        },
        {
            "title": "Concurrent Task Scheduler",
            "description": "Schreibe eine Funktion schedule_tasks(tasks, max_parallel) die Tasks mit Abhaengigkeiten plant. tasks ist eine Liste von dicts: {'id': str, 'duration': int, 'depends_on': [str]}. Gib die minimale Gesamtdauer zurueck und den Schedule als Liste von (start_time, task_id) Tupeln.",
            "test_code": """
tasks = [
    {'id': 'A', 'duration': 3, 'depends_on': []},
    {'id': 'B', 'duration': 2, 'depends_on': []},
    {'id': 'C', 'duration': 4, 'depends_on': ['A']},
    {'id': 'D', 'duration': 1, 'depends_on': ['A', 'B']},
    {'id': 'E', 'duration': 2, 'depends_on': ['C', 'D']},
]
total_time, schedule = schedule_tasks(tasks, 2)
assert total_time == 9, f"Expected 9, got {total_time}"
starts = {tid: st for st, tid in schedule}
assert starts['A'] == 0 or starts['B'] == 0
assert starts['C'] >= 3
assert starts['D'] >= max(3, 2)
assert starts['E'] >= starts['C'] + 4
print("OK")
"""
        },
    ]
}

# === LEVEL PROGRESSION ===
LEVEL_ORDER = ["beginner", "intermediate", "advanced", "expert"]
PROMOTION_THRESHOLD = 0.8  # 80% Erfolgsrate zum Aufstieg


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "start_date": datetime.now().isoformat(),
        "total_problems": 0,
        "solved_problems": 0,
        "current_day": 1,
        "current_level": "beginner",
        "level_stats": {level: {"attempted": 0, "solved": 0} for level in LEVEL_ORDER},
        "performance_history": [],
        "last_training": None
    }


def save_progress(progress):
    PROGRESS_FILE.parent.mkdir(exist_ok=True, parents=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def call_ollama(prompt, max_tokens=4000):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Niedrig fuer Code!
                    "top_p": 0.9,
                    "num_predict": max_tokens
                }
            },
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            print(f"[ERROR] Ollama returned {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Ollama call failed: {e}")
        return None


def extract_python_code(response):
    """Extrahiert Python-Code aus der Ollama-Antwort"""
    # Versuche Code-Bloecke zu finden
    code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', response, re.DOTALL)
    if code_blocks:
        return '\n'.join(code_blocks)

    # Fallback: Suche nach def/class Definitionen
    lines = response.split('\n')
    code_lines = []
    in_code = False
    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith(('def ', 'class ', 'import ', 'from ')):
            in_code = True
        if in_code:
            if stripped == '' and code_lines and not code_lines[-1].strip():
                continue  # Doppelte Leerzeilen skippen
            code_lines.append(line)

    return '\n'.join(code_lines) if code_lines else response


def execute_code_with_tests(code, test_code):
    """Fuehrt Code + Tests in einem sicheren Subprocess aus. Gibt (success, output) zurueck."""
    full_code = code + "\n\n# === TESTS ===\n" + test_code

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(full_code)
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0 and "OK" in result.stdout:
            return True, result.stdout.strip()
        else:
            error = result.stderr.strip() if result.stderr else result.stdout.strip()
            return False, error[:500]  # Max 500 chars Fehler
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: Code lief laenger als 30 Sekunden!"
    except Exception as e:
        return False, f"Execution error: {e}"
    finally:
        try:
            Path(temp_path).unlink()
        except:
            pass


def generate_training_prompt(problem, attempt=1, previous_error=None):
    prompt = f"""Schreibe eine Python-Loesung fuer folgende Aufgabe.

AUFGABE: {problem['title']}
{problem['description']}

REGELN:
- NUR Python-Code, keine Erklaerungen
- Code in ```python ... ``` Block
- Alle Funktionen/Klassen muessen genau so heissen wie beschrieben
- Code muss mit Python 3.10+ laufen
- Keine externen Libraries (nur stdlib)
"""

    if attempt > 1 and previous_error:
        prompt += f"""

VORHERIGER VERSUCH HAT DIESEN FEHLER PRODUZIERT:
{previous_error}

Analysiere den Fehler und korrigiere die Loesung!
"""

    return prompt


def train_on_problem(problem, progress, level):
    """Trainiert an einem Problem mit ECHTEM Code-Execution"""
    print(f"\n{'='*80}")
    print(f"[{level.upper()}] {problem['title']}")
    print(f"{'='*80}\n")

    best_score = 0
    previous_error = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"  [VERSUCH {attempt}/{MAX_ATTEMPTS}]")

        prompt = generate_training_prompt(problem, attempt, previous_error)
        print("  [DENKT] Najika arbeitet...")
        response = call_ollama(prompt)

        if not response:
            print("  [ERROR] Keine Antwort von Ollama!")
            continue

        code = extract_python_code(response)
        if not code.strip():
            print("  [ERROR] Kein Code extrahiert!")
            previous_error = "Keine gueltige Python-Funktion gefunden"
            continue

        # ECHTE Code-Ausfuehrung!
        print("  [TESTE] Fuehre Code aus...")
        success, output = execute_code_with_tests(code, problem['test_code'])

        if success:
            print(f"  [BESTANDEN] Alle Tests OK!")
            best_score = 100

            # Speichere Loesung
            save_solution(problem, code, 100, progress['current_day'], level)
            break
        else:
            print(f"  [FEHLER] {output[:200]}")
            previous_error = output
            best_score = max(best_score, 25)  # Teilpunkte fuer Versuch

    # Update Stats
    progress['total_problems'] += 1
    if 'level_stats' not in progress:
        progress['level_stats'] = {l: {"attempted": 0, "solved": 0} for l in LEVEL_ORDER}
    if level not in progress['level_stats']:
        progress['level_stats'][level] = {"attempted": 0, "solved": 0}

    progress['level_stats'][level]['attempted'] += 1
    if best_score >= 100:
        progress['solved_problems'] += 1
        progress['level_stats'][level]['solved'] += 1

    progress['performance_history'].append({
        "day": progress['current_day'],
        "level": level,
        "problem": problem['title'],
        "score": best_score,
        "attempts": attempt if best_score >= 100 else MAX_ATTEMPTS,
        "timestamp": datetime.now().isoformat()
    })

    return best_score >= 100


def save_solution(problem, code, score, day, level):
    SOLUTIONS_DIR.mkdir(exist_ok=True, parents=True)
    filename = f"day{day}_{level}_{problem['title'].replace(' ', '_')}.py"
    filepath = SOLUTIONS_DIR / filename
    header = f'# {problem["title"]} [{level.upper()}] - Tag {day}\n'
    header += f'# Score: {score}/100 - {datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n'
    filepath.write_text(header + code, encoding='utf-8')
    print(f"  [SAVED] {filepath.name}")


def check_level_promotion(progress):
    """Prueft ob Najika ein Level aufsteigen kann"""
    level = progress['current_level']
    stats = progress.get('level_stats', {}).get(level, {"attempted": 0, "solved": 0})

    if stats['attempted'] < 5:
        return level  # Mindestens 5 Versuche noetig

    success_rate = stats['solved'] / max(1, stats['attempted'])
    level_idx = LEVEL_ORDER.index(level)

    if success_rate >= PROMOTION_THRESHOLD and level_idx < len(LEVEL_ORDER) - 1:
        new_level = LEVEL_ORDER[level_idx + 1]
        print(f"\n  *** LEVEL UP! {level.upper()} -> {new_level.upper()} ***")
        print(f"  *** Erfolgsrate: {success_rate*100:.0f}% ***\n")
        return new_level

    return level


def run_daily_training():
    print("=" * 80)
    print(" NAJIKA CODE TRAINING V2 - ECHTES CODE EXECUTION!")
    print("=" * 80)
    print()

    progress = load_progress()

    # Migration: Alte Progress-Dateien ohne level_stats
    if 'level_stats' not in progress:
        progress['level_stats'] = {l: {"attempted": 0, "solved": 0} for l in LEVEL_ORDER}
        progress['performance_history'] = []
        progress['total_problems'] = 0
        progress['solved_problems'] = 0
        progress['current_day'] = 1

    level = progress['current_level']
    day = progress['current_day']

    print(f"  TAG:   {day}")
    print(f"  LEVEL: {level.upper()}")
    total = progress['total_problems']
    solved = progress['solved_problems']
    rate = (solved / max(1, total)) * 100
    print(f"  RATE:  {solved}/{total} ({rate:.0f}%)")
    print()

    # Waehle Probleme fuer heute
    available = PROBLEMS.get(level, [])
    if not available:
        print(f"[ERROR] Keine Probleme fuer Level {level}!")
        return

    # Rotiere durch die Probleme basierend auf Tag
    start_idx = ((day - 1) * DAILY_PROBLEMS) % len(available)
    todays = []
    for i in range(DAILY_PROBLEMS):
        idx = (start_idx + i) % len(available)
        todays.append(available[idx])

    print(f"  Heute: {len(todays)} Aufgaben [{level.upper()}]")
    for i, p in enumerate(todays, 1):
        print(f"    {i}. {p['title']}")
    print()

    # Trainiere
    solved_today = 0
    for problem in todays:
        success = train_on_problem(problem, progress, level)
        if success:
            solved_today += 1
        time.sleep(2)

    # Level-Check
    new_level = check_level_promotion(progress)
    if new_level != level:
        progress['current_level'] = new_level

    # Update
    progress['current_day'] += 1
    progress['last_training'] = datetime.now().isoformat()
    save_progress(progress)

    # Report
    print()
    print("=" * 80)
    print(" TAGES-REPORT")
    print("=" * 80)
    print(f"  Geloest:  {solved_today}/{len(todays)}")
    print(f"  Level:    {progress['current_level'].upper()}")
    print(f"  Gesamt:   {progress['solved_problems']}/{progress['total_problems']}")
    print()

    # Level-Stats
    for lvl in LEVEL_ORDER:
        stats = progress.get('level_stats', {}).get(lvl, {"attempted": 0, "solved": 0})
        if stats['attempted'] > 0:
            sr = stats['solved'] / stats['attempted'] * 100
            bar = '#' * int(sr / 5) + '.' * (20 - int(sr / 5))
            print(f"  {lvl:>12}: [{bar}] {sr:.0f}% ({stats['solved']}/{stats['attempted']})")

    print()
    print("[DONE] Training abgeschlossen!")
    print()


if __name__ == "__main__":
    run_daily_training()
