#!/bin/bash
###############################################################################
# Build All APK Flavors
# Builds: Private, Friends, Public
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Building ALL Najika APK Flavors${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

START_TIME=$(date +%s)

# Build Private
echo -e "${YELLOW}[1/3] Building PRIVATE flavor...${NC}"
./build_private.sh

echo ""

# Build Friends
echo -e "${YELLOW}[2/3] Building FRIENDS flavor...${NC}"
./build_friends.sh

echo ""

# Build Public
echo -e "${YELLOW}[3/3] Building PUBLIC flavor...${NC}"
./build_public.sh

echo ""

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ ALL APKs Built Successfully!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Build time: ${NC}${DURATION}s"
echo ""
echo -e "${BLUE}Output directory:${NC}"
echo "$(pwd)/../output/"
echo ""
ls -lh ../output/*.apk
echo ""

echo -e "${GREEN}✓ Build complete! 🚀${NC}"
