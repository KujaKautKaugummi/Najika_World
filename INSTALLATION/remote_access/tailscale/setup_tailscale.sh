#!/bin/bash
###############################################################################
# Najika Tailscale Setup (Alternative to Cloudflare)
# Mesh VPN for secure remote access
###############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Najika Tailscale Setup${NC}"
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
# Step 1: Install Tailscale
###############################################################################

echo -e "${YELLOW}Step 1: Installing Tailscale...${NC}"

if [ "$OS" == "linux" ]; then
    # Install Tailscale on Linux
    if ! command -v tailscale &> /dev/null; then
        echo -e "${BLUE}Installing Tailscale...${NC}"
        curl -fsSL https://tailscale.com/install.sh | sh
        echo -e "${GREEN}✓ Tailscale installed${NC}"
    else
        echo -e "${GREEN}✓ Tailscale already installed${NC}"
    fi
elif [ "$OS" == "windows" ]; then
    echo -e "${YELLOW}For Windows:${NC}"
    echo -e "${BLUE}1. Download Tailscale from: https://tailscale.com/download/windows${NC}"
    echo -e "${BLUE}2. Install and run Tailscale${NC}"
    echo -e "${BLUE}3. Come back here when done${NC}"
    echo ""
    read -p "Press Enter when Tailscale is installed..."
fi

echo ""

###############################################################################
# Step 2: Start Tailscale
###############################################################################

echo -e "${YELLOW}Step 2: Starting Tailscale...${NC}"

if [ "$OS" == "linux" ]; then
    sudo systemctl start tailscaled
    sudo systemctl enable tailscaled
    echo -e "${GREEN}✓ Tailscale service started${NC}"
fi

echo ""

###############################################################################
# Step 3: Connect to Tailscale
###############################################################################

echo -e "${YELLOW}Step 3: Connecting to Tailscale network...${NC}"
echo -e "${BLUE}This will open a browser window for authentication${NC}"
echo ""

if [ "$OS" == "linux" ]; then
    sudo tailscale up --accept-routes --accept-dns=false
elif [ "$OS" == "windows" ]; then
    echo -e "${BLUE}Use the Tailscale system tray icon to login${NC}"
    read -p "Press Enter when connected..."
fi

echo -e "${GREEN}✓ Connected to Tailscale${NC}"
echo ""

###############################################################################
# Step 4: Get Tailscale IP
###############################################################################

echo -e "${YELLOW}Step 4: Getting Tailscale IP address...${NC}"

if [ "$OS" == "linux" ]; then
    TAILSCALE_IP=$(tailscale ip -4)
else
    echo -e "${BLUE}Run in PowerShell: ${YELLOW}tailscale ip -4${NC}"
    read -p "Enter your Tailscale IP: " TAILSCALE_IP
fi

if [ -z "$TAILSCALE_IP" ]; then
    echo -e "${RED}Could not determine Tailscale IP${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Tailscale IP: $TAILSCALE_IP${NC}"
echo ""

###############################################################################
# Step 5: Enable MagicDNS (Optional)
###############################################################################

echo -e "${YELLOW}Step 5: Enable MagicDNS (optional)...${NC}"
echo -e "${BLUE}MagicDNS allows you to use device names instead of IPs${NC}"
echo ""

read -p "Enable MagicDNS? (y/n): " ENABLE_MAGICDNS

if [ "$ENABLE_MAGICDNS" == "y" ]; then
    echo -e "${BLUE}To enable MagicDNS:${NC}"
    echo -e "1. Go to: ${YELLOW}https://login.tailscale.com/admin/dns${NC}"
    echo -e "2. Enable MagicDNS"
    echo -e "3. Your device will be accessible at: ${YELLOW}$(hostname).your-tailnet.ts.net${NC}"
    echo ""
    read -p "Press Enter when MagicDNS is enabled..."
fi

echo ""

###############################################################################
# Step 6: Configure Firewall
###############################################################################

echo -e "${YELLOW}Step 6: Configuring firewall...${NC}"

if [ "$OS" == "linux" ]; then
    # Allow Tailscale ports
    if command -v ufw &> /dev/null; then
        echo -e "${BLUE}Configuring UFW...${NC}"
        sudo ufw allow 41641/udp comment 'Tailscale'
        sudo ufw allow from 100.64.0.0/10 to any port 5000 comment 'Najika Mobile'
        sudo ufw allow from 100.64.0.0/10 to any port 5001 comment 'Najika Messenger'
        echo -e "${GREEN}✓ UFW configured${NC}"
    elif command -v firewall-cmd &> /dev/null; then
        echo -e "${BLUE}Configuring firewalld...${NC}"
        sudo firewall-cmd --permanent --add-port=41641/udp
        sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="100.64.0.0/10" port protocol="tcp" port="5000" accept'
        sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="100.64.0.0/10" port protocol="tcp" port="5001" accept'
        sudo firewall-cmd --reload
        echo -e "${GREEN}✓ firewalld configured${NC}"
    fi
elif [ "$OS" == "windows" ]; then
    echo -e "${BLUE}Windows Firewall:${NC}"
    echo -e "Tailscale automatically configures Windows Firewall"
    echo -e "${GREEN}✓ No manual configuration needed${NC}"
fi

echo ""

###############################################################################
# Step 7: Install Tailscale on Mobile Device
###############################################################################

echo -e "${YELLOW}Step 7: Install Tailscale on mobile device...${NC}"
echo ""
echo -e "${BLUE}To connect from your mobile device:${NC}"
echo -e "1. Install Tailscale app:"
echo -e "   • Android: ${YELLOW}https://play.google.com/store/apps/details?id=com.tailscale.ipn${NC}"
echo -e "   • iOS: ${YELLOW}https://apps.apple.com/app/tailscale/id1470499037${NC}"
echo ""
echo -e "2. Login with the same account"
echo -e "3. Your server will be accessible at: ${YELLOW}$TAILSCALE_IP${NC}"
echo ""
read -p "Press Enter when Tailscale is installed on mobile..."
echo ""

###############################################################################
# Step 8: Create Connection Test Script
###############################################################################

echo -e "${YELLOW}Step 8: Creating connection test script...${NC}"

cat > "test_tailscale_connection.sh" <<'EOF'
#!/bin/bash
# Test Tailscale connection

TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "100.x.x.x")

echo "Testing Najika servers via Tailscale..."
echo ""

echo "1. Mobile Server (http://$TAILSCALE_IP:5000):"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$TAILSCALE_IP:5000/api/mobile/health 2>/dev/null || echo "000")
if [ "$RESPONSE" == "200" ]; then
    echo "   ✓ Mobile Server: OK"
else
    echo "   ✗ Mobile Server: Not responding (HTTP $RESPONSE)"
fi

echo "2. Messenger Server (http://$TAILSCALE_IP:5001):"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$TAILSCALE_IP:5001/api/messenger/health 2>/dev/null || echo "000")
if [ "$RESPONSE" == "200" ]; then
    echo "   ✓ Messenger Server: OK"
else
    echo "   ✗ Messenger Server: Not responding (HTTP $RESPONSE)"
fi

echo ""
echo "Your Tailscale IP: $TAILSCALE_IP"
EOF

chmod +x test_tailscale_connection.sh

echo -e "${GREEN}✓ Test script created: test_tailscale_connection.sh${NC}"
echo ""

###############################################################################
# Summary
###############################################################################

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Tailscale Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Configuration Summary:${NC}"
echo -e "  • Tailscale IP: ${YELLOW}$TAILSCALE_IP${NC}"
echo -e "  • Mobile Server: ${YELLOW}http://$TAILSCALE_IP:5000${NC}"
echo -e "  • Messenger Server: ${YELLOW}http://$TAILSCALE_IP:5001${NC}"
echo ""
echo -e "${BLUE}Mobile App Configuration:${NC}"
echo -e "  In your Flutter app, set server URL to:"
echo -e "  ${YELLOW}http://$TAILSCALE_IP:5000${NC}"
echo ""
echo -e "${BLUE}Advantages:${NC}"
echo -e "  ✓ Works with ExpressVPN active"
echo -e "  ✓ Encrypted mesh VPN"
echo -e "  ✓ No port forwarding needed"
echo -e "  ✓ Automatic NAT traversal"
echo -e "  ✓ MagicDNS for easy addressing"
echo ""

if [ "$OS" == "linux" ]; then
    echo -e "${BLUE}Tailscale Management:${NC}"
    echo -e "  • Status: ${YELLOW}tailscale status${NC}"
    echo -e "  • IP Address: ${YELLOW}tailscale ip -4${NC}"
    echo -e "  • Logout: ${YELLOW}sudo tailscale logout${NC}"
    echo -e "  • Service: ${YELLOW}sudo systemctl status tailscaled${NC}"
    echo ""
fi

echo -e "${BLUE}Testing:${NC}"
echo -e "  Run: ${YELLOW}./test_tailscale_connection.sh${NC}"
echo ""

###############################################################################
# Testing
###############################################################################

echo -e "${YELLOW}Testing connection...${NC}"
echo ""

sleep 2

echo -e "${BLUE}Mobile Server:${NC}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$TAILSCALE_IP:5000/api/mobile/health 2>/dev/null || echo "000")
if [ "$RESPONSE" == "200" ]; then
    echo -e "${GREEN}✓ Mobile Server: Accessible${NC}"
else
    echo -e "${YELLOW}⚠ Mobile Server: Not responding (HTTP $RESPONSE)${NC}"
    echo -e "${YELLOW}  Make sure server is running: python3 najika_server_mobile.py${NC}"
fi

echo ""
echo -e "${BLUE}Messenger Server:${NC}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$TAILSCALE_IP:5001/api/messenger/health 2>/dev/null || echo "000")
if [ "$RESPONSE" == "200" ]; then
    echo -e "${GREEN}✓ Messenger Server: Accessible${NC}"
else
    echo -e "${YELLOW}⚠ Messenger Server: Not responding (HTTP $RESPONSE)${NC}"
    echo -e "${YELLOW}  Make sure server is running: python3 najika_messenger_server.py${NC}"
fi

echo ""
echo -e "${GREEN}✓ Tailscale setup complete! 🚀${NC}"
echo -e "${BLUE}Your servers are now accessible via Tailscale mesh VPN${NC}"
echo ""

###############################################################################
# Additional Info
###############################################################################

echo -e "${BLUE}Next Steps:${NC}"
echo -e "1. Start your Najika servers:"
echo -e "   ${YELLOW}python3 najika_server_mobile.py${NC}"
echo -e "   ${YELLOW}python3 najika_messenger_server.py${NC}"
echo ""
echo -e "2. Install Tailscale on your Xiaomi 11T Pro"
echo ""
echo -e "3. In the Najika app, use this server URL:"
echo -e "   ${YELLOW}http://$TAILSCALE_IP:5000${NC}"
echo ""
echo -e "4. Enjoy secure, encrypted remote access!"
echo ""
