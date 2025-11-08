#!/bin/bash
# ===================================================================
# NAJIKA WORLD - Asset Copy Script (Linux/Docker)
# ===================================================================
# Kopiert heruntergeladene 3D-Assets von /mnt/c/Najika_World/assets/
# nach digivice/static/assets/ für Web-Deployment
#
# Gesamt: ~435 GLB-Dateien werden kopiert
# Zeitaufwand: ~2-3 Minuten
# ===================================================================

echo ""
echo "========================================"
echo "NAJIKA WORLD - Asset Copy Script"
echo "========================================"
echo ""
echo "Kopiere 3D-Assets ins Web-Deployment..."
echo ""

# Farben für Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Basis-Pfade
SOURCE_BASE="/mnt/c/Najika_World/assets"
DEST_BASE="digivice/static/assets"

# Prüfe ob Quell-Ordner existiert
if [ ! -d "$SOURCE_BASE" ]; then
    echo -e "${RED}FEHLER: $SOURCE_BASE nicht gefunden!${NC}"
    echo "Bitte stelle sicher dass die Assets dort liegen."
    echo "Falls du Windows benutzt, sollten die Assets unter C:\\Najika_World\\assets\\ liegen"
    exit 1
fi

# Erstelle Ziel-Ordner falls nicht vorhanden
echo "[1/8] Erstelle Ziel-Ordnerstruktur..."
mkdir -p "$DEST_BASE/jellysquish/oasis"
mkdir -p "$DEST_BASE/kaykit/dungeon"
mkdir -p "$DEST_BASE/kaykit/medieval"
mkdir -p "$DEST_BASE/kaykit/nature"
mkdir -p "$DEST_BASE/kaykit/restaurant"
mkdir -p "$DEST_BASE/kaykit/furniture"
mkdir -p "$DEST_BASE/kaykit/adventurers"
mkdir -p "$DEST_BASE/kaykit/skeletons"
mkdir -p "$DEST_BASE/kaykit/halloween"
mkdir -p "$DEST_BASE/kaykit/spooktober"
mkdir -p "$DEST_BASE/kaykit/prototype"
mkdir -p "$DEST_BASE/kaykit/resources"
mkdir -p "$DEST_BASE/kaykit/minigames"
echo -e "${GREEN}OK - Ordnerstruktur erstellt${NC}"
echo ""

# ===================================================================
# 1. JELLYSQUISH OASIS PACK (Desert)
# ===================================================================
echo "[2/8] Kopiere JellySquish Oasis Pack (Desert)..."
SOURCE_DIR="$SOURCE_BASE/JellySquish Oasis Pack - Base Version/JellySquish Oasis Pack - Base Version/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/jellysquish/oasis/" 2>/dev/null
    if [ $? -eq 0 ]; then
        COUNT=$(ls "$DEST_BASE/jellysquish/oasis/"*.glb 2>/dev/null | wc -l)
        echo -e "${GREEN}OK - Oasis Pack kopiert ($COUNT Dateien: Palm Trees, Cactus, Desert Houses)${NC}"
    else
        echo -e "${YELLOW}WARNUNG: Keine GLB-Dateien gefunden${NC}"
    fi
else
    echo -e "${YELLOW}WARNUNG: Oasis Pack nicht gefunden - überspringe${NC}"
fi
echo ""

# ===================================================================
# 2. KAYKIT DUNGEON REMASTERED (Caves)
# ===================================================================
echo "[3/8] Kopiere KayKit Dungeon Pack (Caves)..."
SOURCE_DIR="$SOURCE_BASE/KayKit_DungeonRemastered_1.1_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/dungeon/" 2>/dev/null
    if [ $? -eq 0 ]; then
        COUNT=$(ls "$DEST_BASE/kaykit/dungeon/"*.glb 2>/dev/null | wc -l)
        echo -e "${GREEN}OK - Dungeon Pack kopiert ($COUNT Dateien: 200+ Cave Assets)${NC}"
    else
        echo -e "${YELLOW}WARNUNG: Keine GLB-Dateien gefunden${NC}"
    fi
else
    echo -e "${YELLOW}WARNUNG: Dungeon Pack nicht gefunden - überspringe${NC}"
fi
echo ""

# ===================================================================
# 3. KAYKIT MEDIEVAL HEXAGON (Cities)
# ===================================================================
echo "[4/8] Kopiere KayKit Medieval Pack (Cities)..."
SOURCE_DIR="$SOURCE_BASE/KayKit_Medieval_Hexagon_Pack_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/medieval/" 2>/dev/null
    if [ $? -eq 0 ]; then
        COUNT=$(ls "$DEST_BASE/kaykit/medieval/"*.glb 2>/dev/null | wc -l)
        echo -e "${GREEN}OK - Medieval Pack kopiert ($COUNT Dateien: Houses, Towers, Markets)${NC}"
    else
        echo -e "${YELLOW}WARNUNG: Keine GLB-Dateien gefunden${NC}"
    fi
else
    echo -e "${YELLOW}WARNUNG: Medieval Pack nicht gefunden - überspringe${NC}"
fi
echo ""

# ===================================================================
# 4. KAYKIT FOREST NATURE (Forest)
# ===================================================================
echo "[5/8] Kopiere KayKit Nature Pack (Forest)..."
SOURCE_DIR="$SOURCE_BASE/KayKit_Forest_Nature_Pack_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/nature/" 2>/dev/null
    if [ $? -eq 0 ]; then
        COUNT=$(ls "$DEST_BASE/kaykit/nature/"*.glb 2>/dev/null | wc -l)
        echo -e "${GREEN}OK - Nature Pack kopiert ($COUNT Dateien: Trees, Rocks, Vegetation)${NC}"
    else
        echo -e "${YELLOW}WARNUNG: Keine GLB-Dateien gefunden${NC}"
    fi
else
    echo -e "${YELLOW}WARNUNG: Nature Pack nicht gefunden - überspringe${NC}"
fi
echo ""

# ===================================================================
# 5. KAYKIT RESTAURANT BITS (Dampf-Hain)
# ===================================================================
echo "[6/8] Kopiere KayKit Restaurant Pack (Dampf-Hain)..."
SOURCE_DIR="$SOURCE_BASE/KayKit_Restaurant_Bits_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/restaurant/" 2>/dev/null
    if [ $? -eq 0 ]; then
        COUNT=$(ls "$DEST_BASE/kaykit/restaurant/"*.glb 2>/dev/null | wc -l)
        echo -e "${GREEN}OK - Restaurant Pack kopiert ($COUNT Dateien: Tables, Food, Kitchen)${NC}"
    else
        echo -e "${YELLOW}WARNUNG: Keine GLB-Dateien gefunden${NC}"
    fi
else
    echo -e "${YELLOW}WARNUNG: Restaurant Pack nicht gefunden - überspringe${NC}"
fi
echo ""

# ===================================================================
# 6. KAYKIT FURNITURE BITS (Housing System)
# ===================================================================
echo "[7/8] Kopiere KayKit Furniture Pack (Housing)..."
SOURCE_DIR="$SOURCE_BASE/KayKit_Furniture_Bits_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/furniture/" 2>/dev/null
    if [ $? -eq 0 ]; then
        COUNT=$(ls "$DEST_BASE/kaykit/furniture/"*.glb 2>/dev/null | wc -l)
        echo -e "${GREEN}OK - Furniture Pack kopiert ($COUNT Dateien: Beds, Chairs, Tables)${NC}"
    else
        echo -e "${YELLOW}WARNUNG: Keine GLB-Dateien gefunden${NC}"
    fi
else
    echo -e "${YELLOW}WARNUNG: Furniture Pack nicht gefunden - überspringe${NC}"
fi
echo ""

# ===================================================================
# 7. BONUS PACKS (Optional)
# ===================================================================
echo "[8/8] Kopiere Bonus Packs (Optional)..."

# Adventurers
SOURCE_DIR="$SOURCE_BASE/KayKit_Adventurers_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/adventurers/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Adventurers Pack kopiert (Characters)${NC}"
fi

# Skeletons
SOURCE_DIR="$SOURCE_BASE/KayKit_Skeletons_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/skeletons/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Skeletons Pack kopiert (Enemies)${NC}"
fi

# Halloween
SOURCE_DIR="$SOURCE_BASE/KayKit_HalloweenBits_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/halloween/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Halloween Pack kopiert (Spooky Props for Swamp)${NC}"
fi

# Spooktober
SOURCE_DIR="$SOURCE_BASE/KayKit_Spooktober_Seasonal_Pack_1.1/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/spooktober/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Spooktober Pack kopiert (Dead Trees for Swamp)${NC}"
fi

# Prototype Bits
SOURCE_DIR="$SOURCE_BASE/KayKit_Prototype_Bits_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/prototype/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Prototype Pack kopiert (Totems, Props)${NC}"
fi

# Resource Bits
SOURCE_DIR="$SOURCE_BASE/KayKit_ResourceBits_1.0_FREE/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/resources/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Resource Pack kopiert (Crafting Items)${NC}"
fi

# Mini-Game Pack
SOURCE_DIR="$SOURCE_BASE/KayKit Mini-Game Variety Pack 1.2/Models"
if [ -d "$SOURCE_DIR" ]; then
    cp "$SOURCE_DIR"/*.glb "$DEST_BASE/kaykit/minigames/" 2>/dev/null
    [ $? -eq 0 ] && echo -e "  ${GREEN}- Mini-Game Pack kopiert (Mini-Game Props)${NC}"
fi

echo -e "${GREEN}OK - Bonus Packs kopiert${NC}"
echo ""

# ===================================================================
# STATISTIK
# ===================================================================
TOTAL_FILES=$(find "$DEST_BASE" -name "*.glb" 2>/dev/null | wc -l)

echo ""
echo "========================================"
echo "KOPIER-VORGANG ABGESCHLOSSEN!"
echo "========================================"
echo ""
echo -e "${GREEN}Gesamt kopierte GLB-Dateien: $TOTAL_FILES${NC}"
echo ""
echo "Assets wurden kopiert nach:"
echo "  $DEST_BASE/"
echo ""
echo "Nächste Schritte:"
echo "  1. Prüfe die kopierten Assets"
echo "  2. Starte die Integration ins World-System"
echo "  3. Teste die 3D-Model-Anzeige"
echo ""
