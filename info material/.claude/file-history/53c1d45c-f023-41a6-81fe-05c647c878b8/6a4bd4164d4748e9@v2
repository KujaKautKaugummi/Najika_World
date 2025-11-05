#!/usr/bin/env python3
"""
ECHTE TRAINING DATEN HERUNTERLADEN
Keine leeren Versprechen - ECHTE Daten von GitHub & anderen Quellen!
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime

BACKEND_DIR = Path(__file__).parent
TRAINING_DIR = BACKEND_DIR / "training_data_real"
TRAINING_DIR.mkdir(exist_ok=True)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def run_git_clone(url, target_dir):
    """Clone Git Repository"""
    try:
        log(f"Lade {url}...")
        result = subprocess.run(
            ["git", "clone", "--depth=1", url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            log(f"   [OK] Erfolgreich: {target_dir.name}")
            return True
        else:
            log(f"   [ERR] Fehler: {result.stderr}")
            return False
    except Exception as e:
        log(f"   [ERR] Exception: {e}")
        return False

def download_leetcode_problems():
    """LeetCode Probleme von GitHub"""
    log("\n[1/10] LeetCode Problems...")

    repos = [
        ("https://github.com/neetcode-gh/leetcode", "leetcode_problems"),
        ("https://github.com/doocs/leetcode", "leetcode_solutions")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "code" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: LeetCode: {success}/{len(repos)} Repositories")
    return success

def download_design_patterns():
    """Design Patterns Examples"""
    log("\n[2/10] Design Patterns...")

    repos = [
        ("https://github.com/kamranahmedse/design-patterns-for-humans", "design_patterns"),
        ("https://github.com/iluwatar/java-design-patterns", "java_patterns"),
        ("https://github.com/faif/python-patterns", "python_patterns")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "patterns" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: Patterns: {success}/{len(repos)} Repositories")
    return success

def download_system_design():
    """System Design Resources"""
    log("\n[3/10] System Design...")

    repos = [
        ("https://github.com/donnemartin/system-design-primer", "system_design_primer"),
        ("https://github.com/checkcheckzz/system-design-interview", "system_design_interview"),
        ("https://github.com/binhnguyennus/awesome-scalability", "scalability")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "system_design" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: System Design: {success}/{len(repos)} Repositories")
    return success

def download_security():
    """Security & OWASP"""
    log("\n[4/10] Security Training...")

    repos = [
        ("https://github.com/OWASP/CheatSheetSeries", "owasp_cheatsheets"),
        ("https://github.com/swisskyrepo/PayloadsAllTheThings", "security_payloads"),
        ("https://github.com/qazbnm456/awesome-web-security", "web_security")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "security" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: Security: {success}/{len(repos)} Repositories")
    return success

def download_web_development():
    """Web Dev Examples"""
    log("\n[5/10] Web Development...")

    repos = [
        ("https://github.com/dypsilon/frontend-dev-bookmarks", "frontend_bookmarks"),
        ("https://github.com/thedaviddias/Front-End-Checklist", "frontend_checklist"),
        ("https://github.com/kamranahmedse/developer-roadmap", "dev_roadmap")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "web_dev" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: Web Dev: {success}/{len(repos)} Repositories")
    return success

def download_python_projects():
    """Real Python Projects"""
    log("\n[6/10] Python Projects...")

    repos = [
        ("https://github.com/TheAlgorithms/Python", "algorithms_python"),
        ("https://github.com/trekhleb/learn-python", "learn_python"),
        ("https://github.com/vinta/awesome-python", "awesome_python")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "python" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: Python: {success}/{len(repos)} Repositories")
    return success

def download_databases():
    """Database Patterns"""
    log("\n[7/10] Databases...")

    repos = [
        ("https://github.com/pingcap/awesome-database-learning", "database_learning"),
        ("https://github.com/numetriclabz/awesome-db", "awesome_db")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "databases" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: Databases: {success}/{len(repos)} Repositories")
    return success

def download_devops():
    """DevOps Resources"""
    log("\n[8/10] DevOps...")

    repos = [
        ("https://github.com/bregman-arie/devops-exercises", "devops_exercises"),
        ("https://github.com/veggiemonk/awesome-docker", "docker_resources")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "devops" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: DevOps: {success}/{len(repos)} Repositories")
    return success

def download_best_practices():
    """Best Practices & Clean Code"""
    log("\n[9/10] Best Practices...")

    repos = [
        ("https://github.com/ryanmcdermott/clean-code-javascript", "clean_code_js"),
        ("https://github.com/zedr/clean-code-python", "clean_code_python"),
        ("https://github.com/mtdvio/every-programmer-should-know", "programmer_knowledge")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "best_practices" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: Best Practices: {success}/{len(repos)} Repositories")
    return success

def download_ml_ai():
    """ML/AI Resources"""
    log("\n[10/10] ML/AI...")

    repos = [
        ("https://github.com/microsoft/ML-For-Beginners", "ml_beginners"),
        ("https://github.com/josephmisiti/awesome-machine-learning", "awesome_ml")
    ]

    success = 0
    for url, name in repos:
        target = TRAINING_DIR / "ml_ai" / name
        if run_git_clone(url, target):
            success += 1

    log(f"   STATS: ML/AI: {success}/{len(repos)} Repositories")
    return success

def create_index():
    """Erstelle Index aller heruntergeladenen Daten"""
    log("\n[FINAL] Erstelle Daten-Index...")

    index = {
        "created": datetime.now().isoformat(),
        "total_repositories": 0,
        "categories": {},
        "size_gb": 0
    }

    for category_dir in TRAINING_DIR.iterdir():
        if category_dir.is_dir():
            repos = list(category_dir.iterdir())
            index["categories"][category_dir.name] = {
                "count": len(repos),
                "repositories": [r.name for r in repos]
            }
            index["total_repositories"] += len(repos)

    # Berechne Größe
    try:
        result = subprocess.run(
            ["du", "-sh", str(TRAINING_DIR)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            size_str = result.stdout.split()[0]
            index["size_gb"] = size_str
    except:
        pass

    index_file = TRAINING_DIR / "training_data_index.json"
    index_file.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')

    log(f"\n[OK] Index erstellt: {index_file}")
    log(f"STATS: Gesamt: {index['total_repositories']} Repositories")
    log(f"SIZE: Größe: {index.get('size_gb', 'unbekannt')}")

    return index

def main():
    log("="*80)
    log("NAJIKA ECHTE TRAINING DATEN DOWNLOAD")
    log("="*80)
    log(f"Ziel: {TRAINING_DIR}")
    log("Quelle: GitHub (Open Source)")
    log("")

    # Check Git
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except:
        log("[ERR] FEHLER: Git nicht installiert!")
        log("   Installiere Git: https://git-scm.com/download/win")
        return

    total_success = 0
    total_repos = 0

    downloads = [
        download_leetcode_problems,
        download_design_patterns,
        download_system_design,
        download_security,
        download_web_development,
        download_python_projects,
        download_databases,
        download_devops,
        download_best_practices,
        download_ml_ai
    ]

    for download_func in downloads:
        success = download_func()
        total_success += success
        total_repos += 3  # Durchschnittlich 3 Repos pro Kategorie

    index = create_index()

    log("\n" + "="*80)
    log("DOWNLOAD ABGESCHLOSSEN!")
    log("="*80)
    log(f"Erfolg: {total_success} Repositories")
    log(f"Fehler: {total_repos - total_success}")
    log(f"Erfolgsrate: {(total_success/total_repos*100):.1f}%")
    log(f"\nDaten bereit für Training! [DONE]")
    log(f"Nächster Schritt: SETUP_INTENSIVE_TRAINING.bat\n")

if __name__ == "__main__":
    main()
