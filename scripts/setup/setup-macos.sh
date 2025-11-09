#!/bin/bash

# ============================================
# PhoneticHybrid Setup Script - macOS
# ============================================

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  PhoneticHybrid Setup - macOS          ║"
echo "╔════════════════════════════════════════╗"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}Error: This script is for macOS only!${NC}"
    exit 1
fi

# Check prerequisites
echo -e "${YELLOW}[1/6]${NC} Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3.10+ is required but not installed.${NC}"
    echo "Install Python from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION} found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js 18+ is required but not installed.${NC}"
    echo "Install Node.js from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓${NC} Node.js ${NODE_VERSION} found"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is required but not installed.${NC}"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo -e "${GREEN}✓${NC} npm ${NPM_VERSION} found"

# Check/Install eSpeak-NG
echo ""
echo -e "${YELLOW}[2/6]${NC} Checking eSpeak-NG (phoneme generation)..."

if ! command -v espeak-ng &> /dev/null; then
    echo -e "${YELLOW}eSpeak-NG not found. Installing via Homebrew...${NC}"

    if ! command -v brew &> /dev/null; then
        echo -e "${RED}Error: Homebrew is required to install eSpeak-NG.${NC}"
        echo "Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi

    brew install espeak-ng
    echo -e "${GREEN}✓${NC} eSpeak-NG installed successfully"
else
    echo -e "${GREEN}✓${NC} eSpeak-NG already installed"
fi

# Backend setup
echo ""
echo -e "${YELLOW}[3/6]${NC} Setting up Backend (Python)..."

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo -e "${GREEN}✓${NC} Backend dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env file from template"
    echo -e "${YELLOW}Note: Using Whisper (no API keys needed)${NC}"
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

cd ..

# Frontend setup
echo ""
echo -e "${YELLOW}[4/6]${NC} Setting up Frontend (React)..."

cd frontend

echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✓${NC} Frontend dependencies installed"

cd ..

# Create data directory
echo ""
echo -e "${YELLOW}[5/6]${NC} Setting up data directories..."

mkdir -p data
echo -e "${GREEN}✓${NC} Data directory created"

# Test installations
echo ""
echo -e "${YELLOW}[6/6]${NC} Verifying installation..."

# Test eSpeak-NG
if espeak-ng --version > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} eSpeak-NG working"
else
    echo -e "${RED}✗${NC} eSpeak-NG verification failed"
fi

# Test Python packages
source backend/venv/bin/activate
if python3 -c "import whisper, phonemizer, librosa, fastapi" 2> /dev/null; then
    echo -e "${GREEN}✓${NC} Python packages working"
else
    echo -e "${RED}✗${NC} Some Python packages may have issues"
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  Setup Complete! ✨                    ║"
echo "╔════════════════════════════════════════╗"
echo ""
echo "Next steps:"
echo "  1. Start the development servers:"
echo "     ./scripts/start/start-macos.sh"
echo ""
echo "  2. Or start manually:"
echo "     Backend:  cd backend && source venv/bin/activate && python main.py"
echo "     Frontend: cd frontend && npm run dev"
echo ""
echo "Note: On first run, Whisper will download a ~150MB model (1-2 minutes)"
echo ""
