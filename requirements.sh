#!/bin/bash

# ─────────────────────────────────────────────
#  ReconFlow - Requirements Installer
# ─────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ____                      _____ _"
echo " |  _ \ ___  ___ ___  _ __ |  ___| | _____      __"
echo " | |_) / _ \/ __/ _ \| '_ \| |_  | |/ _ \ \ /\ / /"
echo " |  _ <  __/ (_| (_) | | | |  _| | | (_) \ V  V /"
echo " |_| \_\___|\___\___/|_| |_|_|   |_|\___/ \_/\_/"
echo -e "${NC}"
echo -e "${YELLOW}[*] Installing required tools...${NC}\n"

MISSING=0

install_go_tool() {
    local name=$1
    local pkg=$2
    if ! command -v "$name" &>/dev/null; then
        echo -e "${YELLOW}[*] Installing $name...${NC}"
        go install "$pkg" 2>/dev/null
        if command -v "$name" &>/dev/null; then
            echo -e "${GREEN}[+] $name installed successfully${NC}"
        else
            echo -e "${RED}[-] Failed to install $name. Install manually: go install $pkg${NC}"
            MISSING=$((MISSING+1))
        fi
    else
        echo -e "${GREEN}[+] $name already installed${NC}"
    fi
}

install_apt_tool() {
    local name=$1
    local pkg=$2
    if ! command -v "$name" &>/dev/null; then
        echo -e "${YELLOW}[*] Installing $name...${NC}"
        sudo apt-get install -y "$pkg" &>/dev/null
        if command -v "$name" &>/dev/null; then
            echo -e "${GREEN}[+] $name installed successfully${NC}"
        else
            echo -e "${RED}[-] Failed to install $name${NC}"
            MISSING=$((MISSING+1))
        fi
    else
        echo -e "${GREEN}[+] $name already installed${NC}"
    fi
}

# Check Go
if ! command -v go &>/dev/null; then
    echo -e "${RED}[!] Go is not installed. Please install Go first: https://golang.org/dl/${NC}"
    exit 1
fi

# Check Python3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[!] Python3 is not installed. Please install Python3 first.${NC}"
    exit 1
fi

echo -e "\n${CYAN}[*] Installing Go-based tools...${NC}"
install_go_tool "subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
install_go_tool "httpx" "github.com/projectdiscovery/httpx/cmd/httpx@latest"
install_go_tool "dnsx" "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
install_go_tool "gau" "github.com/lc/gau/v2/cmd/gau@latest"
install_go_tool "ffuf" "github.com/ffuf/ffuf/v2@latest"

echo -e "\n${CYAN}[*] Installing system tools...${NC}"
install_apt_tool "nmap" "nmap"
install_apt_tool "whois" "whois"
install_apt_tool "whatweb" "whatweb"

echo ""
if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}[+] All tools installed successfully. You are ready to run ReconFlow.${NC}"
else
    echo -e "${RED}[!] $MISSING tool(s) failed to install. Please install them manually before running ReconFlow.${NC}"
fi
