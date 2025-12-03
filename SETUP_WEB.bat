@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   SETUP - Plateforme XP Web
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo ✓ Python found
echo ✓ Node.js found
echo.

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Install frontend dependencies
echo.
echo Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo   Setup completed!
echo ========================================
echo.
echo You can now run: START.bat
echo.
pause
