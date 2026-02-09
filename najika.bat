@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM  NAJIKA CODE - Lokale CLI wie Claude Code
REM
REM  Starte aus beliebigem Ordner:
REM    najika              -> Interaktiver Modus
REM    najika "Frage"      -> Einzel-Anfrage
REM    najika --scan       -> Projekt scannen
REM    najika --search X   -> Suche nach X
REM    najika --todos      -> Alle TODOs finden
REM    najika --treasures  -> Verlorene Schätze finden
REM ═══════════════════════════════════════════════════════════════════════════

REM Setze UTF-8 für Umlaute
chcp 65001 >nul 2>&1

REM Pfad zum Najika-Backend
set NAJIKA_DIR=%~dp0backend

REM Python mit najika_code.py starten
python "%NAJIKA_DIR%\najika_code.py" %*
