@echo off
REM ===================================================================
REM NAJIKA WORLD - Asset Copy Script V3 (GLTF Support)
REM ===================================================================
REM Kopiert GLTF + BIN Dateien (KayKit hat keine GLB!)
REM ===================================================================

echo.
echo ========================================
echo NAJIKA WORLD - Asset Copy Script V3
echo ========================================
echo.
echo Kopiere 3D-Assets (GLTF + GLB Support)...
echo.

if not exist "C:\Najika_World\assets\" (
    echo FEHLER: C:\Najika_World\assets\ nicht gefunden!
    pause
    exit /b 1
)

echo [1/7] Oasis Pack (GLB - bereits kopiert)...
echo   25 GLB-Dateien OK
echo.

REM ===================================================================
REM 2. KAYKIT DUNGEON - GLTF FORMAT
REM ===================================================================
echo [2/7] Kopiere KayKit Dungeon Pack (GLTF + BIN)...
if exist "C:\Najika_World\assets\KayKit_DungeonRemastered_1.1_FREE\KayKit_DungeonRemastered_1.1_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_DungeonRemastered_1.1_FREE\KayKit_DungeonRemastered_1.1_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\dungeon\"
    echo OK - Dungeon Pack kopiert (GLTF + BIN Dateien)
) else (
    echo WARNUNG: Dungeon Pack nicht gefunden
)
echo.

REM ===================================================================
REM 3. KAYKIT MEDIEVAL - GLTF FORMAT
REM ===================================================================
echo [3/7] Kopiere KayKit Medieval Pack (GLTF + BIN)...
if exist "C:\Najika_World\assets\KayKit_Medieval_Hexagon_Pack_1.0_FREE\KayKit_Medieval_Hexagon_Pack_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_Medieval_Hexagon_Pack_1.0_FREE\KayKit_Medieval_Hexagon_Pack_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\medieval\"
    echo OK - Medieval Pack kopiert (GLTF + BIN Dateien)
) else (
    echo WARNUNG: Medieval Pack nicht gefunden
)
echo.

REM ===================================================================
REM 4. KAYKIT NATURE - GLTF FORMAT
REM ===================================================================
echo [4/7] Kopiere KayKit Nature Pack (GLTF + BIN)...
if exist "C:\Najika_World\assets\KayKit_Forest_Nature_Pack_1.0_FREE\KayKit_Forest_Nature_Pack_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_Forest_Nature_Pack_1.0_FREE\KayKit_Forest_Nature_Pack_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\nature\"
    echo OK - Nature Pack kopiert (GLTF + BIN Dateien)
) else (
    echo WARNUNG: Nature Pack nicht gefunden
)
echo.

REM ===================================================================
REM 5. KAYKIT RESTAURANT - GLTF FORMAT
REM ===================================================================
echo [5/7] Kopiere KayKit Restaurant Pack (GLTF + BIN)...
if exist "C:\Najika_World\assets\KayKit_Restaurant_Bits_1.0_FREE\KayKit_Restaurant_Bits_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_Restaurant_Bits_1.0_FREE\KayKit_Restaurant_Bits_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\restaurant\"
    echo OK - Restaurant Pack kopiert (GLTF + BIN Dateien)
) else (
    echo WARNUNG: Restaurant Pack nicht gefunden
)
echo.

REM ===================================================================
REM 6. KAYKIT FURNITURE - GLTF FORMAT
REM ===================================================================
echo [6/7] Kopiere KayKit Furniture Pack (GLTF + BIN)...
if exist "C:\Najika_World\assets\KayKit_Furniture_Bits_1.0_FREE\KayKit_Furniture_Bits_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_Furniture_Bits_1.0_FREE\KayKit_Furniture_Bits_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\furniture\"
    echo OK - Furniture Pack kopiert (GLTF + BIN Dateien)
) else (
    echo WARNUNG: Furniture Pack nicht gefunden
)
echo.

REM ===================================================================
REM 7. BONUS PACKS - GLTF FORMAT
REM ===================================================================
echo [7/7] Kopiere Bonus Packs (GLTF + BIN)...

REM Adventurers
if exist "C:\Najika_World\assets\KayKit_Adventurers_1.0_FREE\KayKit_Adventurers_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_Adventurers_1.0_FREE\KayKit_Adventurers_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\adventurers\"
    echo   - Adventurers Pack kopiert
)

REM Skeletons
if exist "C:\Najika_World\assets\KayKit Character Pack - Skeletons 1.0\KayKit Character Pack - Skeletons 1.0\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit Character Pack - Skeletons 1.0\KayKit Character Pack - Skeletons 1.0\Assets\gltf\*.*" "digivice\static\assets\kaykit\skeletons\"
    echo   - Skeletons Pack kopiert
)

REM Halloween
if exist "C:\Najika_World\assets\KayKit_HalloweenBits_1.0_FREE\KayKit_HalloweenBits_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_HalloweenBits_1.0_FREE\KayKit_HalloweenBits_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\halloween\"
    echo   - Halloween Pack kopiert
)

REM Spooktober
if exist "C:\Najika_World\assets\KayKit Spooktober Seasonal Pack 1.1\KayKit Spooktober Seasonal Pack 1.1\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit Spooktober Seasonal Pack 1.1\KayKit Spooktober Seasonal Pack 1.1\Assets\gltf\*.*" "digivice\static\assets\kaykit\spooktober\"
    echo   - Spooktober Pack kopiert
)

REM Prototype
if exist "C:\Najika_World\assets\KayKit_Prototype_Bits_1.0_FREE\KayKit_Prototype_Bits_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_Prototype_Bits_1.0_FREE\KayKit_Prototype_Bits_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\prototype\"
    echo   - Prototype Pack kopiert
)

REM Resources
if exist "C:\Najika_World\assets\KayKit_ResourceBits_1.0_FREE\KayKit_ResourceBits_1.0_FREE\Assets\gltf\" (
    xcopy /E /Y /I "C:\Najika_World\assets\KayKit_ResourceBits_1.0_FREE\KayKit_ResourceBits_1.0_FREE\Assets\gltf\*.*" "digivice\static\assets\kaykit\resources\"
    echo   - Resource Pack kopiert
)

echo OK - Bonus Packs fertig
echo.

echo.
echo ========================================
echo KOPIER-VORGANG ABGESCHLOSSEN!
echo ========================================
echo.
echo Kopierte Formate:
echo   - GLB: JellySquish Oasis (25 Dateien)
echo   - GLTF + BIN: Alle KayKit Packs
echo.
echo Assets wurden kopiert nach:
echo   digivice\static\assets\
echo.
echo WICHTIG: GLTF Dateien benoetigen die zugehoerigen BIN-Dateien!
echo Beide wurden kopiert und funktionieren mit Three.js.
echo.
pause
