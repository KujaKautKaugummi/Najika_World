@echo off
REM ===================================================================
REM NAJIKA WORLD - Asset Copy Script V2 (KORRIGIERT)
REM ===================================================================
REM Kopiert mit KORRIGIERTEN Pfaden (doppelte Ordner beachtet)
REM ===================================================================

echo.
echo ========================================
echo NAJIKA WORLD - Asset Copy Script V2
echo ========================================
echo.
echo Kopiere 3D-Assets (KORRIGIERTE PFADE)...
echo.

REM Prüfe ob Quell-Ordner existiert
if not exist "C:\Najika_World\assets\" (
    echo FEHLER: C:\Najika_World\assets\ nicht gefunden!
    pause
    exit /b 1
)

echo [1/7] Oasis Pack (bereits kopiert - ueberspringe)...
echo   25 Dateien bereits vorhanden
echo.

REM ===================================================================
REM 2. KAYKIT DUNGEON REMASTERED (Caves) - KORRIGIERTER PFAD
REM ===================================================================
echo [2/7] Kopiere KayKit Dungeon Pack (Caves)...
if exist "C:\Najika_World\assets\KayKit_DungeonRemastered_1.1_FREE\KayKit_DungeonRemastered_1.1_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_DungeonRemastered_1.1_FREE\KayKit_DungeonRemastered_1.1_FREE\Models\*.glb" "digivice\static\assets\kaykit\dungeon\"
    echo OK - Dungeon Pack kopiert
) else (
    echo WARNUNG: Dungeon Pack nicht gefunden
)
echo.

REM ===================================================================
REM 3. KAYKIT MEDIEVAL - KORRIGIERTER PFAD
REM ===================================================================
echo [3/7] Kopiere KayKit Medieval Pack (Cities)...
if exist "C:\Najika_World\assets\KayKit_Medieval_Hexagon_Pack_1.0_FREE\KayKit_Medieval_Hexagon_Pack_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Medieval_Hexagon_Pack_1.0_FREE\KayKit_Medieval_Hexagon_Pack_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\medieval\"
    echo OK - Medieval Pack kopiert
) else (
    echo WARNUNG: Medieval Pack nicht gefunden
)
echo.

REM ===================================================================
REM 4. KAYKIT NATURE - KORRIGIERTER PFAD
REM ===================================================================
echo [4/7] Kopiere KayKit Nature Pack (Forest)...
if exist "C:\Najika_World\assets\KayKit_Forest_Nature_Pack_1.0_FREE\KayKit_Forest_Nature_Pack_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Forest_Nature_Pack_1.0_FREE\KayKit_Forest_Nature_Pack_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\nature\"
    echo OK - Nature Pack kopiert
) else (
    echo WARNUNG: Nature Pack nicht gefunden
)
echo.

REM ===================================================================
REM 5. KAYKIT RESTAURANT - KORRIGIERTER PFAD
REM ===================================================================
echo [5/7] Kopiere KayKit Restaurant Pack (Dampf-Hain)...
if exist "C:\Najika_World\assets\KayKit_Restaurant_Bits_1.0_FREE\KayKit_Restaurant_Bits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Restaurant_Bits_1.0_FREE\KayKit_Restaurant_Bits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\restaurant\"
    echo OK - Restaurant Pack kopiert
) else (
    echo WARNUNG: Restaurant Pack nicht gefunden
)
echo.

REM ===================================================================
REM 6. KAYKIT FURNITURE - KORRIGIERTER PFAD
REM ===================================================================
echo [6/7] Kopiere KayKit Furniture Pack (Housing)...
if exist "C:\Najika_World\assets\KayKit_Furniture_Bits_1.0_FREE\KayKit_Furniture_Bits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Furniture_Bits_1.0_FREE\KayKit_Furniture_Bits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\furniture\"
    echo OK - Furniture Pack kopiert
) else (
    echo WARNUNG: Furniture Pack nicht gefunden
)
echo.

REM ===================================================================
REM 7. BONUS PACKS - KORRIGIERTE PFADE
REM ===================================================================
echo [7/7] Kopiere Bonus Packs...

REM Adventurers
if exist "C:\Najika_World\assets\KayKit_Adventurers_1.0_FREE\KayKit_Adventurers_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Adventurers_1.0_FREE\KayKit_Adventurers_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\adventurers\"
    echo   - Adventurers Pack kopiert
)

REM Skeletons (hat anderen Ordnernamen!)
if exist "C:\Najika_World\assets\KayKit Character Pack - Skeletons 1.0\KayKit Character Pack - Skeletons 1.0\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit Character Pack - Skeletons 1.0\KayKit Character Pack - Skeletons 1.0\Models\*.glb" "digivice\static\assets\kaykit\skeletons\"
    echo   - Skeletons Pack kopiert
)

REM Halloween
if exist "C:\Najika_World\assets\KayKit_HalloweenBits_1.0_FREE\KayKit_HalloweenBits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_HalloweenBits_1.0_FREE\KayKit_HalloweenBits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\halloween\"
    echo   - Halloween Pack kopiert
)

REM Spooktober
if exist "C:\Najika_World\assets\KayKit Spooktober Seasonal Pack 1.1\KayKit Spooktober Seasonal Pack 1.1\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit Spooktober Seasonal Pack 1.1\KayKit Spooktober Seasonal Pack 1.1\Models\*.glb" "digivice\static\assets\kaykit\spooktober\"
    echo   - Spooktober Pack kopiert
)

REM Prototype
if exist "C:\Najika_World\assets\KayKit_Prototype_Bits_1.0_FREE\KayKit_Prototype_Bits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Prototype_Bits_1.0_FREE\KayKit_Prototype_Bits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\prototype\"
    echo   - Prototype Pack kopiert
)

REM Resources
if exist "C:\Najika_World\assets\KayKit_ResourceBits_1.0_FREE\KayKit_ResourceBits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_ResourceBits_1.0_FREE\KayKit_ResourceBits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\resources\"
    echo   - Resource Pack kopiert
)

REM Mini-Games
if exist "C:\Najika_World\assets\KayKit Mini-Game Variety Pack 1.2\KayKit Mini-Game Variety Pack 1.2\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit Mini-Game Variety Pack 1.2\KayKit Mini-Game Variety Pack 1.2\Models\*.glb" "digivice\static\assets\kaykit\minigames\"
    echo   - Mini-Game Pack kopiert
)

echo OK - Bonus Packs fertig
echo.

REM ===================================================================
REM STATISTIK
REM ===================================================================
echo.
echo ========================================
echo KOPIER-VORGANG ABGESCHLOSSEN!
echo ========================================
echo.
echo Alle GLB-Dateien wurden kopiert nach:
echo   digivice\static\assets\
echo.
echo Naechste Schritte:
echo   1. Pruefe Assets in digivice\static\assets\
echo   2. Starte World-System Integration
echo.
pause
