#!/bin/bash
###############################################################################
# Najika Cloudflare Tunnel Setup
# Enables remote access while ExpressVPN is active
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Najika Cloudflare Tunnel Setup${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

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
# Step 1: Install cloudflared
###############################################################################

echo -e "${YELLOW}Step 1: Installing cloudflared...${NC}"

if [ "$OS" == "linux" ]; then
    # Download cloudflared for Linux
    if [ ! -f "/usr/local/bin/cloudflared" ]; then
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
        sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
        sudo chmod +x /usr/local/bin/cloudflared
        echo -e "${GREEN}✓ cloudflared installed${NC}"
    else
        echo -e "${GREEN}✓ cloudflared already installed${NC}"
    fi
elif [ "$OS" == "windows" ]; then
    # Download cloudflared for Windows
    if [ ! -f "cloudflared.exe" ]; then
        echo -e "${YELLOW}Downloading cloudflared for Windows...${NC}"
        curl -L -o cloudflared.exe https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
        echo -e "${GREEN}✓ cloudflared downloaded${NC}"
    else
        echo -e "${GREEN}✓ cloudflared already exists${NC}"
    fi
fi

echo ""

###############################################################################
# Step 2: Login to Cloudflare
###############################################################################

echo -e "${YELLOW}Step 2: Login to Cloudflare...${NC}"
echo -e "${BLUE}This will open a browser window for authentication${NC}"
echo -e "${BLUE}Please login with your Cloudflare account${NC}"
echo ""

if [ "$OS" == "linux" ]; then
    cloudflared tunnel login
elif [ "$OS" == "windows" ]; then
    ./cloudflared.exe tunnel login
fi

echo -e "${GREEN}✓ Cloudflare login successful${NC}"
echo ""

###############################################################################
# Step 3: Create Tunnel
###############################################################################

echo -e "${YELLOW}Step 3: Creating Cloudflare Tunnel...${NC}"
TUNNEL_NAME="najika-tunnel"

if [ "$OS" == "linux" ]; then
    cloudflared tunnel create $TUNNEL_NAME
    TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')
elif [ "$OS" == "windows" ]; then
    ./cloudflared.exe tunnel create $TUNNEL_NAME
    TUNNEL_ID=$(./cloudflared.exe tunnel list | grep $TUNNEL_NAME | awk '{print $1}')
fi

echo -e "${GREEN}✓ Tunnel created${NC}"
echo -e "${BLUE}Tunnel ID: $TUNNEL_ID${NC}"
echo ""

###############################################################################
# Step 4: Create Configuration File
###############################################################################

echo -e "${YELLOW}Step 4: Creating configuration file...${NC}"

# Ask user for domain
echo -e "${BLUE}Enter your domain (e.g., najika.yourdomain.com):${NC}"
read -p "Domain: " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Domain cannot be empty${NC}"
    exit 1
fi

# Configuration directory
if [ "$OS" == "linux" ]; then
    CONFIG_DIR="$HOME/.cloudflared"
else
    CONFIG_DIR="$HOME/.cloudflared"
fi

mkdir -p "$CONFIG_DIR"

# Create config file
cat > "$CONFIG_DIR/config.yml" <<EOF
# Najika Cloudflare Tunnel Configuration
tunnel: $TUNNEL_ID
credentials-file: $CONFIG_DIR/$TUNNEL_ID.json

# Ingress rules
ingress:
  # Mobile Server
  - hostname: $DOMAIN
    service: http://localhost:5000
    originRequest:
      noTLSVerify: true

  # Messenger Server
  - hostname: messenger.$DOMAIN
    service: http://localhost:5001
    originRequest:
      noTLSVerify: true

  # WebSocket support
  - hostname: ws.$DOMAIN
    service: http://localhost:5000
    originRequest:
      noTLSVerify: true

  # Catch-all (404)
  - service: http_status:404

# Logging
logDirectory: $CONFIG_DIR/logs
loglevel: info
EOF

echo -e "${GREEN}✓ Configuration file created at $CONFIG_DIR/config.yml${NC}"
echo ""

###############################################################################
# Step 5: Configure DNS
###############################################################################

echo -e "${YELLOW}Step 5: Configuring DNS...${NC}"

if [ "$OS" == "linux" ]; then
    cloudflared tunnel route dns $TUNNEL_NAME $DOMAIN
    cloudflared tunnel route dns $TUNNEL_NAME messenger.$DOMAIN
    cloudflared tunnel route dns $TUNNEL_NAME ws.$DOMAIN
elif [ "$OS" == "windows" ]; then
    ./cloudflared.exe tunnel route dns $TUNNEL_NAME $DOMAIN
    ./cloudflared.exe tunnel route dns $TUNNEL_NAME messenger.$DOMAIN
    ./cloudflared.exe tunnel route dns $TUNNEL_NAME ws.$DOMAIN
fi

echo -e "${GREEN}✓ DNS configured${NC}"
echo ""

###############################################################################
# Step 6: Create Systemd Service (Linux only)
###############################################################################

if [ "$OS" == "linux" ]; then
    echo -e "${YELLOW}Step 6: Creating systemd service...${NC}"

    sudo tee /etc/systemd/system/cloudflared-najika.service > /dev/null <<EOF
[Unit]
Description=Najika Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/local/bin/cloudflared tunnel --config $CONFIG_DIR/config.yml run
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable cloudflared-najika.service
    sudo systemctl start cloudflared-najika.service

    echo -e "${GREEN}✓ Systemd service created and started${NC}"
    echo ""

    # Check status
    echo -e "${YELLOW}Service Status:${NC}"
    sudo systemctl status cloudflared-najika.service --no-pager
    echo ""
fi

###############################################################################
# Step 7: Create Windows Service / Startup Script
###############################################################################

if [ "$OS" == "windows" ]; then
    echo -e "${YELLOW}Step 6: Creating startup script...${NC}"

    # Create startup batch file
    cat > "start_cloudflared.bat" <<EOF
@echo off
cloudflared.exe tunnel --config %USERPROFILE%\\.cloudflared\\config.yml run
EOF

    echo -e "${GREEN}✓ Startup script created: start_cloudflared.bat${NC}"
    echo -e "${BLUE}To run at startup, add this to Windows Task Scheduler${NC}"
    echo ""
fi

###############################################################################
# Summary
###############################################################################

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Cloudflare Tunnel Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Configuration Summary:${NC}"
echo -e "  • Tunnel Name: ${YELLOW}$TUNNEL_NAME${NC}"
echo -e "  • Tunnel ID: ${YELLOW}$TUNNEL_ID${NC}"
echo -e "  • Main Domain: ${YELLOW}https://$DOMAIN${NC}"
echo -e "  • Messenger Domain: ${YELLOW}https://messenger.$DOMAIN${NC}"
echo -e "  • WebSocket Domain: ${YELLOW}wss://ws.$DOMAIN${NC}"
echo ""
echo -e "${BLUE}Local Services:${NC}"
echo -e "  • Mobile Server: ${YELLOW}http://localhost:5000${NC}"
echo -e "  • Messenger Server: ${YELLOW}http://localhost:5001${NC}"
echo ""

if [ "$OS" == "linux" ]; then
    echo -e "${BLUE}Service Management:${NC}"
    echo -e "  • Start: ${YELLOW}sudo systemctl start cloudflared-najika${NC}"
    echo -e "  • Stop: ${YELLOW}sudo systemctl stop cloudflared-najika${NC}"
    echo -e "  • Status: ${YELLOW}sudo systemctl status cloudflared-najika${NC}"
    echo -e "  • Logs: ${YELLOW}sudo journalctl -u cloudflared-najika -f${NC}"
elif [ "$OS" == "windows" ]; then
    echo -e "${BLUE}To Start Tunnel:${NC}"
    echo -e "  • Run: ${YELLOW}start_cloudflared.bat${NC}"
fi

echo ""
echo -e "${GREEN}✓ Your Najika server is now accessible remotely!${NC}"
echo -e "${GREEN}✓ Works with ExpressVPN active!${NC}"
echo ""

###############################################################################
# Testing
###############################################################################

echo -e "${YELLOW}Testing connection...${NC}"
echo ""

# Wait a moment for tunnel to establish
sleep 3

echo -e "${BLUE}Attempting to reach: https://$DOMAIN/api/mobile/health${NC}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN/api/mobile/health || echo "000")

if [ "$RESPONSE" == "200" ]; then
    echo -e "${GREEN}✓ Connection successful!${NC}"
    echo -e "${GREEN}✓ Server is reachable at: https://$DOMAIN${NC}"
else
    echo -e "${YELLOW}⚠ Server not responding yet (HTTP $RESPONSE)${NC}"
    echo -e "${YELLOW}This is normal if servers aren't started yet${NC}"
    echo -e "${BLUE}Start the servers and test again:${NC}"
    echo -e "  python3 najika_server_mobile.py"
    echo -e "  python3 najika_messenger_server.py"
fi

echo ""
echo -e "${BLUE}Setup complete! 🚀${NC}"
