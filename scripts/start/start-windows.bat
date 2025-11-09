@echo off
setlocal

REM ============================================
REM PhoneticHybrid Start Script - Windows
REM ============================================

echo.
echo ========================================
echo   PhoneticHybrid Development Server
echo ========================================
echo.

REM Check if backend venv exists
if not exist "backend\venv\" (
    echo [ERROR] Backend virtual environment not found!
    echo Please run the setup script first:
    echo   scripts\setup\setup-windows.bat
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules\" (
    echo [ERROR] Frontend dependencies not installed!
    echo Please run the setup script first:
    echo   scripts\setup\setup-windows.bat
    pause
    exit /b 1
)

REM Start backend in a new window
echo Starting Backend Server...
start "PhoneticHybrid Backend" cmd /k "cd backend && venv\Scripts\activate && python main.py"

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in a new window
echo Starting Frontend Server...
start "PhoneticHybrid Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Servers Starting... ✨
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173 (or http://localhost:3000)
echo API Docs: http://localhost:8000/docs
echo.
echo Note: First analysis will take 1-2 minutes (Whisper model download)
echo.
echo Two command windows have been opened:
echo   - Backend Server (Python)
echo   - Frontend Server (React)
echo.
echo Close those windows to stop the servers.
echo.
echo Press any key to exit this window...
pause > nul
