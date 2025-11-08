#!/bin/bash
###############################################################################
# Build Script: Najika Friends APK
# Flavor: FRIENDS (NSFW disabled)
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Building Najika FRIENDS APK${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Navigate to Flutter project
cd "$(dirname "$0")/../flutter_app/najika_digivice"

echo -e "${BLUE}Cleaning previous builds...${NC}"
flutter clean

echo -e "${BLUE}Getting dependencies...${NC}"
flutter pub get

echo -e "${BLUE}Building FRIENDS flavor...${NC}"
flutter build apk \
  --release \
  --obfuscate \
  --split-debug-info=build/debug-info \
  --target-platform android-arm64 \
  --dart-define=FLAVOR=friends \
  --dart-define=APP_NAME="Najika (Friends)" \
  --dart-define=NSFW_ENABLED=false

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ FRIENDS APK Built Successfully!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}APK Location:${NC}"
echo "$(pwd)/build/app/outputs/flutter-apk/app-release.apk"
echo ""

# Copy to output directory
OUTPUT_DIR="../../output"
mkdir -p "$OUTPUT_DIR"
cp build/app/outputs/flutter-apk/app-release.apk "$OUTPUT_DIR/najika-friends.apk"

echo -e "${GREEN}✓ Copied to: $OUTPUT_DIR/najika-friends.apk${NC}"
echo ""

# Show APK info
APK_SIZE=$(du -h "$OUTPUT_DIR/najika-friends.apk" | cut -f1)
echo -e "${BLUE}APK Size: ${NC}$APK_SIZE"
echo ""

echo -e "${BLUE}Next steps:${NC}"
echo "1. Install on device: adb install $OUTPUT_DIR/najika-friends.apk"
echo "2. Or transfer to device and install manually"
echo ""
