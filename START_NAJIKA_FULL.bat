@echo off
title Najika World - Complete Game + Backend
color 0B

echo ========================================
echo   NAJIKA WORLD - FULL VERSION
echo ========================================
echo.
echo   Starting Backend + Frontend...
echo.
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:5173
echo   Game: najika_world_UNIFIED.html
echo ========================================
echo.

REM Starte Backend (Najika Server) in neuem Fenster
echo [1/2] Starte Najika Backend (Port 8000)...
start "Najika Backend (Port 8000)" cmd /k "cd /d %~dp0backend && python najika_server.py"

REM Warte 3 Sekunden damit Backend Zeit hat zu starten
timeout /t 3 /nobreak >nul

REM Starte Frontend (HTTP Server + Browser)
echo [2/2] Starte Game Server (Port 5173)...
cd /d %~dp0digivice

REM Öffne Browser
start http://localhost:5173/najika_world_UNIFIED.html

REM Starte HTTP Server (blockiert, daher am Ende)
echo.
echo ========================================
echo   NAJIKA WORLD LÄUFT!
echo ========================================
echo.
echo   Backend:  http://localhost:8000 (Fenster 1)
echo   Frontend: http://localhost:5173 (Fenster 2)
echo.
echo   Status: Backend Online (grüner Punkt)
echo   Features: Chat, Teleport, Stats Sync, Voice
echo.
echo   Alle Dependencies vorhanden:
echo   - Ollama: najika-local, najika-wizard
echo   - ChromaDB: Memories + Training Data
echo   - Coqui TTS: Megumin Voice Clone
echo   - PyTorch: CUDA 12.1 (GPU)
echo.
echo   Press CTRL+C to stop Frontend
echo   Schließe "Backend" Fenster für Server
echo ========================================
echo.

python -m http.server 5173
