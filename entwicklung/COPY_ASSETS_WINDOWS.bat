@echo off
REM ===================================================================
REM NAJIKA WORLD - Asset Copy Script (Windows)
REM ===================================================================
REM Kopiert heruntergeladene 3D-Assets von C:\Najika_World\assets\
REM nach digivice\static\assets\ für Web-Deployment
REM
REM Gesamt: ~435 GLB-Dateien werden kopiert
REM Zeitaufwand: ~2-3 Minuten
REM ===================================================================

echo.
echo ========================================
echo NAJIKA WORLD - Asset Copy Script
echo ========================================
echo.
echo Kopiere 3D-Assets ins Web-Deployment...
echo.

REM Prüfe ob Quell-Ordner existiert
if not exist "C:\Najika_World\assets\" (
    echo FEHLER: C:\Najika_World\assets\ nicht gefunden!
    echo Bitte stelle sicher dass die Assets dort liegen.
    pause
    exit /b 1
)

REM Erstelle Ziel-Ordner falls nicht vorhanden
echo [1/8] Erstelle Ziel-Ordnerstruktur...
mkdir "digivice\static\assets\jellysquish\oasis" 2>nul
mkdir "digivice\static\assets\kaykit\dungeon" 2>nul
mkdir "digivice\static\assets\kaykit\medieval" 2>nul
mkdir "digivice\static\assets\kaykit\nature" 2>nul
mkdir "digivice\static\assets\kaykit\restaurant" 2>nul
mkdir "digivice\static\assets\kaykit\furniture" 2>nul
mkdir "digivice\static\assets\kaykit\adventurers" 2>nul
mkdir "digivice\static\assets\kaykit\skeletons" 2>nul
mkdir "digivice\static\assets\kaykit\halloween" 2>nul
mkdir "digivice\static\assets\kaykit\spooktober" 2>nul
mkdir "digivice\static\assets\kaykit\prototype" 2>nul
mkdir "digivice\static\assets\kaykit\resources" 2>nul
mkdir "digivice\static\assets\kaykit\minigames" 2>nul
echo OK - Ordnerstruktur erstellt
echo.

REM ===================================================================
REM 1. JELLYSQUISH OASIS PACK (Desert)
REM ===================================================================
echo [2/8] Kopiere JellySquish Oasis Pack (Desert)...
if exist "C:\Najika_World\assets\JellySquish Oasis Pack - Base Version\JellySquish Oasis Pack - Base Version\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\JellySquish Oasis Pack - Base Version\JellySquish Oasis Pack - Base Version\Models\*.glb" "digivice\static\assets\jellysquish\oasis\"
    echo OK - Oasis Pack kopiert (Palm Trees, Cactus, Desert Houses)
) else (
    echo WARNUNG: Oasis Pack nicht gefunden - ueberspringe
)
echo.

REM ===================================================================
REM 2. KAYKIT DUNGEON REMASTERED (Caves)
REM ===================================================================
echo [3/8] Kopiere KayKit Dungeon Pack (Caves)...
if exist "C:\Najika_World\assets\KayKit_DungeonRemastered_1.1_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_DungeonRemastered_1.1_FREE\Models\*.glb" "digivice\static\assets\kaykit\dungeon\"
    echo OK - Dungeon Pack kopiert (200+ Cave Assets)
) else (
    echo WARNUNG: Dungeon Pack nicht gefunden - ueberspringe
)
echo.

REM ===================================================================
REM 3. KAYKIT MEDIEVAL HEXAGON (Cities)
REM ===================================================================
echo [4/8] Kopiere KayKit Medieval Pack (Cities)...
if exist "C:\Najika_World\assets\KayKit_Medieval_Hexagon_Pack_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Medieval_Hexagon_Pack_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\medieval\"
    echo OK - Medieval Pack kopiert (Houses, Towers, Markets)
) else (
    echo WARNUNG: Medieval Pack nicht gefunden - ueberspringe
)
echo.

REM ===================================================================
REM 4. KAYKIT FOREST NATURE (Forest)
REM ===================================================================
echo [5/8] Kopiere KayKit Nature Pack (Forest)...
if exist "C:\Najika_World\assets\KayKit_Forest_Nature_Pack_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Forest_Nature_Pack_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\nature\"
    echo OK - Nature Pack kopiert (Trees, Rocks, Vegetation)
) else (
    echo WARNUNG: Nature Pack nicht gefunden - ueberspringe
)
echo.

REM ===================================================================
REM 5. KAYKIT RESTAURANT BITS (Dampf-Hain)
REM ===================================================================
echo [6/8] Kopiere KayKit Restaurant Pack (Dampf-Hain)...
if exist "C:\Najika_World\assets\KayKit_Restaurant_Bits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Restaurant_Bits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\restaurant\"
    echo OK - Restaurant Pack kopiert (Tables, Food, Kitchen)
) else (
    echo WARNUNG: Restaurant Pack nicht gefunden - ueberspringe
)
echo.

REM ===================================================================
REM 6. KAYKIT FURNITURE BITS (Housing System)
REM ===================================================================
echo [7/8] Kopiere KayKit Furniture Pack (Housing)...
if exist "C:\Najika_World\assets\KayKit_Furniture_Bits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Furniture_Bits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\furniture\"
    echo OK - Furniture Pack kopiert (Beds, Chairs, Tables)
) else (
    echo WARNUNG: Furniture Pack nicht gefunden - ueberspringe
)
echo.

REM ===================================================================
REM 7. BONUS PACKS (Optional)
REM ===================================================================
echo [8/8] Kopiere Bonus Packs (Optional)...

REM Adventurers
if exist "C:\Najika_World\assets\KayKit_Adventurers_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Adventurers_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\adventurers\"
    echo   - Adventurers Pack kopiert (Characters)
)

REM Skeletons
if exist "C:\Najika_World\assets\KayKit_Skeletons_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Skeletons_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\skeletons\"
    echo   - Skeletons Pack kopiert (Enemies)
)

REM Halloween
if exist "C:\Najika_World\assets\KayKit_HalloweenBits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_HalloweenBits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\halloween\"
    echo   - Halloween Pack kopiert (Spooky Props for Swamp)
)

REM Spooktober
if exist "C:\Najika_World\assets\KayKit_Spooktober_Seasonal_Pack_1.1\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Spooktober_Seasonal_Pack_1.1\Models\*.glb" "digivice\static\assets\kaykit\spooktober\"
    echo   - Spooktober Pack kopiert (Dead Trees for Swamp)
)

REM Prototype Bits
if exist "C:\Najika_World\assets\KayKit_Prototype_Bits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_Prototype_Bits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\prototype\"
    echo   - Prototype Pack kopiert (Totems, Props)
)

REM Resource Bits
if exist "C:\Najika_World\assets\KayKit_ResourceBits_1.0_FREE\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit_ResourceBits_1.0_FREE\Models\*.glb" "digivice\static\assets\kaykit\resources\"
    echo   - Resource Pack kopiert (Crafting Items)
)

REM Mini-Game Pack
if exist "C:\Najika_World\assets\KayKit Mini-Game Variety Pack 1.2\Models\" (
    xcopy /Y /Q "C:\Najika_World\assets\KayKit Mini-Game Variety Pack 1.2\Models\*.glb" "digivice\static\assets\kaykit\minigames\"
    echo   - Mini-Game Pack kopiert (Mini-Game Props)
)

echo OK - Bonus Packs kopiert
echo.

REM ===================================================================
REM FERTIG
REM ===================================================================
echo.
echo ========================================
echo KOPIER-VORGANG ABGESCHLOSSEN!
echo ========================================
echo.
echo Assets wurden kopiert nach:
echo   digivice\static\assets\
echo.
echo Naechste Schritte:
echo   1. Pruefe die kopierten Assets
echo   2. Starte die Integration ins World-System
echo   3. Teste die 3D-Model-Anzeige
echo.
pause
