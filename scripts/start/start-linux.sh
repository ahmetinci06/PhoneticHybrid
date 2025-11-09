#!/bin/bash

# ============================================
# PhoneticHybrid Start Script - Linux
# ============================================

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  PhoneticHybrid Development Server     ║"
echo "╔════════════════════════════════════════╗"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo -e "${RED}Error: Backend virtual environment not found!${NC}"
    echo "Please run the setup script first:"
    echo "  ./scripts/setup/setup-linux.sh"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}Error: Frontend dependencies not installed!${NC}"
    echo "Please run the setup script first:"
    echo "  ./scripts/setup/setup-linux.sh"
    exit 1
fi

# Start backend in background
echo -e "${YELLOW}Starting Backend Server...${NC}"
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}Error: Backend failed to start!${NC}"
    exit 1
fi

# Start frontend
echo -e "${YELLOW}Starting Frontend Server...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  Servers Running ✨                    ║"
echo "╔════════════════════════════════════════╗"
echo ""
echo -e "${GREEN}Backend:${NC}  http://localhost:8000"
echo -e "${GREEN}Frontend:${NC} http://localhost:5173 (or http://localhost:3000)"
echo -e "${GREEN}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Note:${NC} First analysis will take 1-2 minutes (Whisper model download)"
echo ""
echo -e "${RED}Press Ctrl+C to stop all servers${NC}"
echo ""

# Trap Ctrl+C to kill both processes
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped.'; exit" INT TERM

# Wait for processes
wait
