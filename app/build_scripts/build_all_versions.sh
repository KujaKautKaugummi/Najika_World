#!/bin/bash

# ============================================================
# Najika Digivice - Build All Versions Script
# ============================================================
# This script builds all 3 versions of the Digivice app:
# 1. Master Edition (Najika)
# 2. Trusted Edition (Friends)
# 3. Public Edition
#
# Usage: ./build_all_versions.sh
# ============================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/../flutter_app/najika_digivice"
OUTPUT_DIR="$SCRIPT_DIR/builds"
BUILD_CONFIG="$PROJECT_DIR/lib/config/build_config.dart"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# ============================================================
# Helper Functions
# ============================================================

print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# ============================================================
# Build Configuration Switcher
# ============================================================

set_build_edition() {
    local edition=$1
    print_info "Setting build edition to: $edition"

    # Backup original
    cp "$BUILD_CONFIG" "$BUILD_CONFIG.bak"

    # Replace edition in build_config.dart
    case $edition in
        "master")
            sed -i 's/static const DigiviceEdition edition = DigiviceEdition\.[a-z]*;/static const DigiviceEdition edition = DigiviceEdition.master;/g' "$BUILD_CONFIG"
            ;;
        "trusted")
            sed -i 's/static const DigiviceEdition edition = DigiviceEdition\.[a-z]*;/static const DigiviceEdition edition = DigiviceEdition.trusted;/g' "$BUILD_CONFIG"
            ;;
        "public")
            sed -i 's/static const DigiviceEdition edition = DigiviceEdition\.[a-z]*;/static const DigiviceEdition edition = DigiviceEdition.public;/g' "$BUILD_CONFIG"
            ;;
        *)
            print_error "Unknown edition: $edition"
            exit 1
            ;;
    esac

    print_success "Build edition set to: $edition"
}

restore_build_config() {
    if [ -f "$BUILD_CONFIG.bak" ]; then
        mv "$BUILD_CONFIG.bak" "$BUILD_CONFIG"
        print_info "Restored original build_config.dart"
    fi
}

# ============================================================
# Build Function
# ============================================================

build_version() {
    local edition=$1
    local output_name=$2

    print_header "Building $edition Edition"

    # Set build edition
    set_build_edition "$edition"

    # Navigate to project
    cd "$PROJECT_DIR"

    # Clean previous builds
    print_info "Cleaning previous builds..."
    flutter clean

    # Get dependencies
    print_info "Getting dependencies..."
    flutter pub get

    # Build APK
    print_info "Building APK..."
    flutter build apk --release

    # Copy APK to output directory
    local apk_path="build/app/outputs/flutter-apk/app-release.apk"
    if [ -f "$apk_path" ]; then
        cp "$apk_path" "$OUTPUT_DIR/$output_name"
        print_success "APK built successfully: $output_name"

        # Get APK size
        local size=$(du -h "$OUTPUT_DIR/$output_name" | cut -f1)
        print_info "APK size: $size"
    else
        print_error "APK not found at: $apk_path"
        return 1
    fi

    # Restore build config
    restore_build_config

    echo ""
}

# ============================================================
# Main Build Process
# ============================================================

print_header "Najika Digivice - Build All Versions"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    print_error "Flutter is not installed or not in PATH"
    exit 1
fi

print_info "Flutter version:"
flutter --version

echo ""

# Ask user which versions to build
echo -e "${YELLOW}Which versions do you want to build?${NC}"
echo "1) All versions"
echo "2) Master only"
echo "3) Trusted only"
echo "4) Public only"
echo "5) Master + Trusted"
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        # Build all versions
        build_version "master" "najika_digivice_master.apk"
        build_version "trusted" "najika_digivice_trusted.apk"
        build_version "public" "najika_digivice_public.apk"
        ;;
    2)
        build_version "master" "najika_digivice_master.apk"
        ;;
    3)
        build_version "trusted" "najika_digivice_trusted.apk"
        ;;
    4)
        build_version "public" "najika_digivice_public.apk"
        ;;
    5)
        build_version "master" "najika_digivice_master.apk"
        build_version "trusted" "najika_digivice_trusted.apk"
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# ============================================================
# Summary
# ============================================================

print_header "Build Summary"

echo -e "${GREEN}Built APKs:${NC}"
ls -lh "$OUTPUT_DIR"/*.apk 2>/dev/null || echo "No APKs found"

echo ""
print_success "All builds completed!"
print_info "APKs saved to: $OUTPUT_DIR"

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Master Edition → Install on your phone"
echo "2. Trusted Edition → Send to friends"
echo "3. Public Edition → Test before App Store submission"

echo ""
echo -e "${BLUE}Installation:${NC}"
echo "adb install $OUTPUT_DIR/najika_digivice_master.apk"

# ============================================================
# Cleanup
# ============================================================

# Ensure build config is restored
restore_build_config

print_success "Done!"
