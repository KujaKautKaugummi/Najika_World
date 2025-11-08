#!/bin/bash
# ===================================================================
# NAJIKA WORLD V2 - TEST SERVER (Port 8001)
# ===================================================================
# Startet separaten Server nur für World Manager V2 Test
# Läuft parallel zum Hauptserver (Port 8000)
# ===================================================================

echo ""
echo "========================================"
echo " NAJIKA WORLD V2 - TEST SERVER"
echo "========================================"
echo ""
echo "Startet Test-Server auf Port 8001..."
echo ""
echo "WICHTIG:"
echo " - Hauptserver (Port 8000) bleibt unberührt"
echo " - V2 Test läuft parallel auf Port 8001"
echo " - Browser: http://localhost:8001/najika_world_v2.html"
echo ""
echo "========================================"
echo ""

cd digivice

echo "Server startet..."
python3 -m http.server 8001
