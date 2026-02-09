#!/bin/bash
###############################################################################
# Najika Mobile & Messenger - MASTER INSTALLER
#
# This script installs and configures:
# 1. Backend servers (Mobile + Messenger)
# 2. Remote access (Cloudflare Tunnel OR Tailscale)
# 3. Flutter mobile app (builds APKs)
#
# Author: Claude Code
# Date: 2025-11-07
# Version: 1.0
###############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
clear
echo -e "${MAGENTA}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗               ║
║   ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗              ║
║   ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║              ║
║   ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║              ║
║   ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║              ║
║   ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝              ║
║                                                               ║
║             MOBILE APP & MESSENGER INSTALLER                  ║
║                 Post-Quantum Secured                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}⚠️  Do NOT run this script as root!${NC}"
    echo -e "${YELLOW}Run as normal user. Sudo will be requested when needed.${NC}"
    exit 1
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    echo -e "${RED}Unsupported OS: $OSTYPE${NC}"
    exit 1
fi

echo -e "${GREEN}Detected OS: $OS${NC}"
echo ""

###############################################################################
# STEP 1: Check Prerequisites
###############################################################################

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}STEP 1: Checking Prerequisites${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

MISSING_DEPS=""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ Python 3: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    MISSING_DEPS="$MISSING_DEPS python3"
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 installed${NC}"
else
    echo -e "${RED}✗ pip3 not found${NC}"
    MISSING_DEPS="$MISSING_DEPS python3-pip"
fi

# Check Flutter
if command -v flutter &> /dev/null; then
    FLUTTER_VERSION=$(flutter --version | head -1 | awk '{print $2}')
    echo -e "${GREEN}✓ Flutter: $FLUTTER_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Flutter not found${NC}"
    echo -e "${BLUE}Install Flutter from: https://flutter.dev/docs/get-started/install${NC}"
    MISSING_DEPS="$MISSING_DEPS flutter"
fi

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓ Git installed${NC}"
else
    echo -e "${RED}✗ Git not found${NC}"
    MISSING_DEPS="$MISSING_DEPS git"
fi

echo ""

if [ -n "$MISSING_DEPS" ]; then
    echo -e "${RED}Missing dependencies:${NC} $MISSING_DEPS"
    echo ""
    echo -e "${YELLOW}Install missing dependencies and run this script again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met!${NC}"
echo ""

###############################################################################
# STEP 2: User Configuration
###############################################################################

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}STEP 2: Configuration${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}Select remote access method:${NC}"
echo "1. Cloudflare Tunnel (Recommended - works with ExpressVPN)"
echo "2. Tailscale (Alternative - mesh VPN)"
echo "3. Local only (no remote access)"
echo ""
read -p "Choice [1/2/3]: " REMOTE_ACCESS_CHOICE

case $REMOTE_ACCESS_CHOICE in
    1)
        REMOTE_ACCESS="cloudflare"
        echo -e "${GREEN}✓ Cloudflare Tunnel selected${NC}"
        ;;
    2)
        REMOTE_ACCESS="tailscale"
        echo -e "${GREEN}✓ Tailscale selected${NC}"
        ;;
    3)
        REMOTE_ACCESS="none"
        echo -e "${GREEN}✓ Local only${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice. Defaulting to Cloudflare.${NC}"
        REMOTE_ACCESS="cloudflare"
        ;;
esac

echo ""

# Ask which APK flavors to build
echo -e "${BLUE}Select APK flavors to build:${NC}"
echo "1. Private only (NSFW enabled)"
echo "2. Friends only (NSFW off)"
echo "3. Public only (Clean)"
echo "4. All flavors"
echo ""
read -p "Choice [1/2/3/4]: " APK_CHOICE

case $APK_CHOICE in
    1) BUILD_APKS="private" ;;
    2) BUILD_APKS="friends" ;;
    3) BUILD_APKS="public" ;;
    4) BUILD_APKS="all" ;;
    *)
        echo -e "${RED}Invalid choice. Defaulting to all.${NC}"
        BUILD_APKS="all"
        ;;
esac

echo -e "${GREEN}✓ Will build: $BUILD_APKS${NC}"
echo ""

###############################################################################
# STEP 3: Install Backend Dependencies
###############################################################################

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}STEP 3: Installing Backend Dependencies${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}Installing Python packages...${NC}"
pip3 install -r backend/requirements_mobile.txt

echo -e "${GREEN}✓ Backend dependencies installed${NC}"
echo ""

###############################################################################
# STEP 4: Setup Remote Access
###############################################################################

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}STEP 4: Setting up Remote Access${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

if [ "$REMOTE_ACCESS" == "cloudflare" ]; then
    echo -e "${BLUE}Setting up Cloudflare Tunnel...${NC}"
    cd remote_access/cloudflare
    ./setup_cloudflare_tunnel.sh
    cd ../..
    echo -e "${GREEN}✓ Cloudflare Tunnel configured${NC}"

elif [ "$REMOTE_ACCESS" == "tailscale" ]; then
    echo -e "${BLUE}Setting up Tailscale...${NC}"
    cd remote_access/tailscale
    ./setup_tailscale.sh
    cd ../..
    echo -e "${GREEN}✓ Tailscale configured${NC}"

else
    echo -e "${YELLOW}⚠ Skipping remote access setup${NC}"
fi

echo ""

###############################################################################
# STEP 5: Build Mobile App
###############################################################################

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}STEP 5: Building Mobile App${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

cd build_scripts

if [ "$BUILD_APKS" == "all" ]; then
    echo -e "${BLUE}Building all APK flavors...${NC}"
    ./build_all.sh
elif [ "$BUILD_APKS" == "private" ]; then
    ./build_private.sh
elif [ "$BUILD_APKS" == "friends" ]; then
    ./build_friends.sh
elif [ "$BUILD_APKS" == "public" ]; then
    ./build_public.sh
fi

cd ..

echo -e "${GREEN}✓ APKs built successfully${NC}"
echo ""

###############################################################################
# STEP 6: Create Systemd Services (Linux only)
###############################################################################

if [ "$OS" == "linux" ]; then
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}STEP 6: Creating Systemd Services${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""

    echo -e "${BLUE}Creating Mobile Server service...${NC}"
    sudo tee /etc/systemd/system/najika-mobile.service > /dev/null <<EOF
[Unit]
Description=Najika Mobile Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)/backend
ExecStart=/usr/bin/python3 najika_server_mobile.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    echo -e "${BLUE}Creating Messenger Server service...${NC}"
    sudo tee /etc/systemd/system/najika-messenger.service > /dev/null <<EOF
[Unit]
Description=Najika Messenger Server (Zero-Knowledge)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)/backend
ExecStart=/usr/bin/python3 najika_messenger_server.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd
    sudo systemctl daemon-reload

    # Enable services
    sudo systemctl enable najika-mobile.service
    sudo systemctl enable najika-messenger.service

    echo -e "${GREEN}✓ Systemd services created${NC}"
    echo ""
fi

###############################################################################
# STEP 7: Final Summary
###############################################################################

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════${NC}"
echo -e "${MAGENTA}  ✓ INSTALLATION COMPLETE!${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}📋 Installation Summary:${NC}"
echo ""

echo -e "${BLUE}Backend Servers:${NC}"
echo -e "  • Mobile Server: ${GREEN}Installed${NC}"
echo -e "  • Messenger Server: ${GREEN}Installed${NC}"
echo ""

echo -e "${BLUE}Remote Access:${NC}"
if [ "$REMOTE_ACCESS" == "cloudflare" ]; then
    echo -e "  • Cloudflare Tunnel: ${GREEN}Configured${NC}"
elif [ "$REMOTE_ACCESS" == "tailscale" ]; then
    echo -e "  • Tailscale: ${GREEN}Configured${NC}"
else
    echo -e "  • ${YELLOW}Local only${NC}"
fi
echo ""

echo -e "${BLUE}Mobile App:${NC}"
echo -e "  • APKs built: ${GREEN}$BUILD_APKS${NC}"
echo -e "  • Location: ${YELLOW}$(pwd)/output/${NC}"
echo ""

if [ "$OS" == "linux" ]; then
    echo -e "${CYAN}🚀 Starting Services:${NC}"
    echo ""
    sudo systemctl start najika-mobile.service
    sudo systemctl start najika-messenger.service

    sleep 2

    echo -e "${BLUE}Service Status:${NC}"
    sudo systemctl status najika-mobile.service --no-pager | head -3
    sudo systemctl status najika-messenger.service --no-pager | head -3
    echo ""
fi

echo -e "${CYAN}📱 Next Steps:${NC}"
echo ""
echo -e "1. ${BLUE}Install APK on your Xiaomi 11T Pro:${NC}"
if [ "$BUILD_APKS" == "all" ]; then
    echo "   • Private: output/najika-private.apk"
    echo "   • Friends: output/najika-friends.apk"
    echo "   • Public: output/najika-public.apk"
else
    echo "   • output/najika-$BUILD_APKS.apk"
fi
echo ""

echo -e "2. ${BLUE}Transfer APK to device:${NC}"
echo "   • Via USB: adb install output/najika-*.apk"
echo "   • Or copy manually and install"
echo ""

echo -e "3. ${BLUE}Server URLs (configure in app):${NC}"
if [ "$REMOTE_ACCESS" == "cloudflare" ]; then
    echo "   • Remote: https://najika.yourdomain.com"
elif [ "$REMOTE_ACCESS" == "tailscale" ]; then
    TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "100.x.x.x")
    echo "   • Tailscale: http://$TAILSCALE_IP:5000"
fi
echo "   • Local: http://192.168.1.100:5000"
echo ""

if [ "$OS" == "linux" ]; then
    echo -e "${CYAN}🔧 Service Management:${NC}"
    echo ""
    echo "Start servers:"
    echo "  sudo systemctl start najika-mobile"
    echo "  sudo systemctl start najika-messenger"
    echo ""
    echo "Stop servers:"
    echo "  sudo systemctl stop najika-mobile"
    echo "  sudo systemctl stop najika-messenger"
    echo ""
    echo "View logs:"
    echo "  sudo journalctl -u najika-mobile -f"
    echo "  sudo journalctl -u najika-messenger -f"
    echo ""
fi

echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Ready to use! 🚀${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}📚 Documentation: INSTALLATION/docs/README.md${NC}"
echo ""
