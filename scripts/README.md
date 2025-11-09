# Scripts Directory

This directory contains setup and startup scripts for PhoneticHybrid.

## Directory Structure

```
scripts/
├── setup/              # Initial setup scripts
│   ├── setup-macos.sh
│   ├── setup-linux.sh
│   └── setup-windows.bat
│
└── start/              # Development server startup scripts
    ├── start-macos.sh
    ├── start-linux.sh
    ├── start-windows.bat
    └── deprecated/     # Old startup scripts (archived)
```

## Setup Scripts

Run these scripts **once** to set up your development environment.

### macOS
```bash
./scripts/setup/setup-macos.sh
```

**What it does:**
- Checks Python 3.10+, Node.js 18+, npm
- Installs eSpeak-NG via Homebrew (if missing)
- Creates Python virtual environment
- Installs all Python dependencies
- Installs all Node.js dependencies
- Creates `.env` configuration file
- Verifies installation

### Linux
```bash
./scripts/setup/setup-linux.sh
```

**What it does:**
- Checks Python 3.10+, Node.js 18+, npm
- Installs eSpeak-NG via package manager (apt/dnf/pacman)
- Installs audio processing libraries (libsndfile, ffmpeg)
- Creates Python virtual environment
- Installs all Python dependencies
- Installs all Node.js dependencies
- Creates `.env` configuration file
- Verifies installation

### Windows
```cmd
scripts\setup\setup-windows.bat
```

**What it does:**
- Checks Python 3.10+, Node.js 18+, npm
- Checks for eSpeak-NG installation (provides download link if missing)
- Creates Python virtual environment
- Installs all Python dependencies
- Installs all Node.js dependencies
- Creates `.env` configuration file
- Verifies installation

**Note:** On Windows, you need to manually install eSpeak-NG from:
https://github.com/espeak-ng/espeak-ng/releases

## Startup Scripts

Run these scripts to start the development servers.

### macOS
```bash
./scripts/start/start-macos.sh
```

### Linux
```bash
./scripts/start/start-linux.sh
```

### Windows
```cmd
scripts\start\start-windows.bat
```

**What they do:**
- Verify that setup has been completed
- Start backend server (Python FastAPI)
- Start frontend server (React + Vite)
- Display server URLs and status

**Servers:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173 (or http://localhost:3000)
- API Docs: http://localhost:8000/docs

## First-Time Setup

1. **Run the setup script** for your OS (see above)
2. **Wait for completion** (installs may take 5-10 minutes)
3. **Run the startup script** to launch development servers
4. **Open your browser** to http://localhost:5173

**Note:** On first analysis, Whisper will download a ~150MB model (1-2 minutes).

## Troubleshooting

### Setup Issues

**Python not found:**
- Install Python 3.10+ from https://python.org
- Ensure Python is added to PATH

**Node.js not found:**
- Install Node.js 18+ from https://nodejs.org
- Ensure Node.js is added to PATH

**eSpeak-NG issues:**
- macOS: Install Homebrew, then run setup script again
- Linux: Setup script will install automatically
- Windows: Download installer from https://github.com/espeak-ng/espeak-ng/releases

### Startup Issues

**"Virtual environment not found":**
- Run the setup script first

**"Dependencies not installed":**
- Run the setup script first

**Backend fails to start:**
- Check if port 8000 is already in use
- Verify Python dependencies: `cd backend && source venv/bin/activate && pip list`

**Frontend fails to start:**
- Check if port 5173/3000 is already in use
- Verify Node dependencies: `cd frontend && npm list`

## Manual Setup

If you prefer manual setup instead of using the scripts:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install

# Start backend
cd backend
source venv/bin/activate
python main.py

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## What's Different from Old Scripts?

The old `start_dev.sh` and `start_dev.bat` files in the root directory have been:
- Moved to `scripts/start/deprecated/`
- Replaced with improved scripts in `scripts/setup/` and `scripts/start/`

**New features:**
- Separate setup and startup scripts
- OS-specific optimizations
- Better error checking and validation
- Automated dependency installation
- Colored output and progress indicators
- Comprehensive verification steps
