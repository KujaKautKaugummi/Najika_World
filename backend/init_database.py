#!/usr/bin/env python3
"""
NAJIKA WORLD - DATABASE INITIALIZATION
======================================
Initialisiert die SQLite Datenbank mit allen Tabellen.

Fuehre aus mit:
    python init_database.py

Erstellt:
    - najika_world.db (SQLite Datenbank)
    - Alle Tabellen fuer Card Game, Dice Monsters, etc.
"""

import sys
import os

# Setze Pfade korrekt
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, BACKEND_DIR)

# Setze Umgebungsvariable fuer Debug-Modus
os.environ['DEBUG'] = 'true'

def main():
    print("=" * 70)
    print("  NAJIKA WORLD - DATABASE INITIALIZATION")
    print("=" * 70)
    print()

    # Import Database Module
    print("[1/3] Lade Database Module...")
    try:
        from backend.database import init_db, engine, Base
        from backend.config import settings
        print(f"  [OK] Database URL: {settings.DATABASE_URL}")
    except ImportError as e:
        print(f"  [ERROR] Import fehlgeschlagen: {e}")
        sys.exit(1)

    # Erstelle Datenbank
    print()
    print("[2/3] Erstelle Datenbank und Tabellen...")
    try:
        init_db()
        print("  [OK] Alle Tabellen erstellt!")
    except Exception as e:
        print(f"  [ERROR] Datenbank-Erstellung fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Zeige erstellte Tabellen
    print()
    print("[3/3] Erstellte Tabellen:")
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        for i, table in enumerate(tables, 1):
            print(f"  {i:2}. {table}")
        print()
        print(f"  TOTAL: {len(tables)} Tabellen erstellt!")
    except Exception as e:
        print(f"  [WARNING] Konnte Tabellen nicht auflisten: {e}")

    print()
    print("=" * 70)
    print("  DATABASE INITIALIZATION COMPLETE!")
    print("=" * 70)
    print()
    print("  Naechste Schritte:")
    print("  1. Starte die Server: python start_all_servers.py")
    print("  2. Oder starte nur FastAPI: uvicorn main_fastapi:app --port 8001")
    print("  3. Oeffne http://127.0.0.1:8001/docs fuer API Dokumentation")
    print()

if __name__ == "__main__":
    main()
