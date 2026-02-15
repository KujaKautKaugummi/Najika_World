"""
Integration Check - Verify all files are properly integrated
============================================================

Checks:
1. All Python API files exist
2. All routers are registered in main_fastapi.py
3. All JavaScript UI files exist
4. All scripts are loaded in index.html
5. Documentation exists
"""

import os
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check_file_exists(path: str, description: str) -> bool:
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = f"{GREEN}[OK]" if exists else f"{RED}[FAIL]"
    print(f"{status} {description}: {path}{RESET}")
    return exists

def check_file_contains(path: str, search_text: str, description: str) -> bool:
    """Check if a file contains specific text"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            contains = search_text in content
            status = f"{GREEN}[OK]" if contains else f"{RED}[FAIL]"
            print(f"{status} {description}: '{search_text}'{RESET}")
            return contains
    except Exception as e:
        print(f"{RED}[FAIL] {description}: Error reading file - {e}{RESET}")
        return False

def main():
    print(f"\n{BLUE}{'='*60}")
    print("INTEGRATION CHECK - Magic/Skill System V3")
    print(f"{'='*60}{RESET}\n")

    all_checks_passed = True

    # ========== BACKEND API FILES ==========
    print(f"{BLUE}[BACKEND API FILES]{RESET}")
    print("-" * 60)

    backend_files = [
        ("backend/api/spell_names.py", "Spell Names API"),
        ("backend/api/special_stats.py", "S.P.E.C.I.A.L. Stats API"),
        ("backend/api/slime_2layer_ai.py", "Slime-KI 2-Layer API"),
        ("backend/api/magic_schools.py", "Magic Schools API (updated)")
    ]

    for path, desc in backend_files:
        if not check_file_exists(path, desc):
            all_checks_passed = False

    # ========== ROUTER REGISTRATION ==========
    print(f"\n{BLUE}[ROUTER REGISTRATION IN main_fastapi.py]{RESET}")
    print("-" * 60)

    main_fastapi_path = "backend/main_fastapi.py"
    router_imports = [
        ("spell_names", "Spell Names import"),
        ("special_stats", "S.P.E.C.I.A.L. Stats import"),
        ("slime_2layer_ai", "Slime-KI 2-Layer import")
    ]

    for import_name, desc in router_imports:
        if not check_file_contains(main_fastapi_path, import_name, desc):
            all_checks_passed = False

    router_includes = [
        ("spell_names.router", "Spell Names router"),
        ("special_stats.router", "S.P.E.C.I.A.L. Stats router"),
        ("slime_2layer_ai.router", "Slime-KI 2-Layer router")
    ]

    for router, desc in router_includes:
        if not check_file_contains(main_fastapi_path, router, desc):
            all_checks_passed = False

    # ========== FRONTEND UI FILES ==========
    print(f"\n{BLUE} FRONTEND UI FILES{RESET}")
    print("-" * 60)

    frontend_files = [
        ("digivice/js/ui/gildenhaus_ui.js", "Gildenhaus UI"),
        ("digivice/js/unified_combat_system.js", "Unified Combat System (updated)"),
        ("digivice/js/teleporter_system.js", "Teleporter System")
    ]

    for path, desc in frontend_files:
        if not check_file_exists(path, desc):
            all_checks_passed = False

    # ========== SCRIPT LOADING ==========
    print(f"\n{BLUE} SCRIPT LOADING IN index.html{RESET}")
    print("-" * 60)

    index_html_path = "digivice/index.html"
    scripts = [
        ("gildenhaus_ui.js", "Gildenhaus UI script"),
        ("teleporter_system.js", "Teleporter System script"),
        ("unified_combat_system.js", "Unified Combat System script")
    ]

    for script, desc in scripts:
        if not check_file_contains(index_html_path, script, desc):
            all_checks_passed = False

    # ========== DOCUMENTATION ==========
    print(f"\n{BLUE} DOCUMENTATION{RESET}")
    print("-" * 60)

    docs = [
        ("THREEJS_TO_UE5_MAPPING.md", "Three.js  UE5 Mapping Guide"),
        ("ZAUBER_UND_SKILL_SYSTEM_V3_FINAL.md", "Magic/Skill System V3 Spec")
    ]

    for path, desc in docs:
        if not check_file_exists(path, desc):
            all_checks_passed = False

    # ========== ADDITIONAL FILES ==========
    print(f"\n{BLUE} TEST FILES{RESET}")
    print("-" * 60)

    test_files = [
        ("TEST_MAGIC_SYSTEM_V3.py", "Comprehensive Test Suite"),
        ("CHECK_INTEGRATION.py", "This Integration Check")
    ]

    for path, desc in test_files:
        if not check_file_exists(path, desc):
            all_checks_passed = False

    # ========== SUMMARY ==========
    print(f"\n{BLUE}{'='*60}")
    print(" INTEGRATION CHECK SUMMARY")
    print(f"{'='*60}{RESET}")

    if all_checks_passed:
        print(f"\n{GREEN} ALL CHECKS PASSED!{RESET}")
        print(f"{GREEN} System ist vollstndig integriert und bereit!{RESET}")
        print(f"\n{YELLOW} Nchste Schritte:{RESET}")
        print("1. Starte Backend: python backend/main_fastapi.py")
        print("2. ffne Frontend: http://localhost:8000/digivice/")
        print("3. Teste APIs: python TEST_MAGIC_SYSTEM_V3.py")
        return True
    else:
        print(f"\n{RED} SOME CHECKS FAILED!{RESET}")
        print(f"{YELLOW}  Bitte berprfe die fehlenden Dateien/Eintrge oben.{RESET}")
        return False


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}  Check abgebrochen!{RESET}")
        exit(1)
