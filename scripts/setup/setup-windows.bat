@echo off
setlocal enabledelayedexpansion

REM ============================================
REM PhoneticHybrid Setup Script - Windows
REM ============================================

echo.
echo ========================================
echo   PhoneticHybrid Setup - Windows
echo ========================================
echo.

REM Check Python
echo [1/6] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.10+ is required but not installed.
    echo Install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js 18+ is required but not installed.
    echo Install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo [OK] Node.js %NODE_VERSION% found

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is required but not installed.
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('npm --version') do set NPM_VERSION=%%i
echo [OK] npm %NPM_VERSION% found

REM Check eSpeak-NG
echo.
echo [2/6] Checking eSpeak-NG (phoneme generation)...

set "ESPEAK_PATH=C:\Program Files\eSpeak NG\espeak-ng.exe"
if exist "%ESPEAK_PATH%" (
    echo [OK] eSpeak-NG already installed
) else (
    echo [WARNING] eSpeak-NG not found at: %ESPEAK_PATH%
    echo.
    echo eSpeak-NG is required for phoneme generation.
    echo.
    echo Please install eSpeak-NG:
    echo   1. Download from: https://github.com/espeak-ng/espeak-ng/releases
    echo   2. Download the Windows installer (.msi file)
    echo   3. Run the installer (use default installation path)
    echo   4. Run this setup script again
    echo.
    pause
    exit /b 1
)

REM Backend setup
echo.
echo [3/6] Setting up Backend (Python)...

cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo Installing Python dependencies (this may take a few minutes)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] Backend dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    copy .env.example .env >nul
    echo [OK] Created .env file from template
    echo [NOTE] Using Whisper (no API keys needed)
) else (
    echo [OK] .env file already exists
)

cd ..

REM Frontend setup
echo.
echo [4/6] Setting up Frontend (React)...

cd frontend

echo Installing Node.js dependencies (this may take a few minutes)...
call npm install

if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    echo Try running: npm install
    pause
    exit /b 1
)

echo [OK] Frontend dependencies installed

cd ..

REM Create data directory
echo.
echo [5/6] Setting up data directories...

if not exist "data" mkdir data
echo [OK] Data directory created

REM Test installations
echo.
echo [6/6] Verifying installation...

REM Test eSpeak-NG
"%ESPEAK_PATH%" --version >nul 2>&1
if errorlevel 1 (
    echo [X] eSpeak-NG verification failed
) else (
    echo [OK] eSpeak-NG working
)

REM Test Python packages
cd backend
call venv\Scripts\activate.bat
python -c "import whisper, phonemizer, librosa, fastapi" 2>nul
if errorlevel 1 (
    echo [X] Some Python packages may have issues
) else (
    echo [OK] Python packages working
)
cd ..

echo.
echo ========================================
echo   Setup Complete! ✨
echo ========================================
echo.
echo Next steps:
echo   1. Start the development servers:
echo      scripts\start\start-windows.bat
echo.
echo   2. Or start manually:
echo      Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo      Frontend: cd frontend ^&^& npm run dev
echo.
echo Note: On first run, Whisper will download a ~150MB model (1-2 minutes)
echo.
pause
