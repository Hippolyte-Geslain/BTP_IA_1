@echo off
echo.
echo ======================================================
echo   PLATEFORME XP - QUICK START SCRIPT
echo ======================================================
echo.

cd /d "%~dp0"

echo Starting Backend Server...
cd backend
start "Plateforme XP Backend" cmd /k "python run.py"
cd ..

echo.
echo Backend started on http://localhost:5000
echo.
echo To start the frontend:
echo   1. Open a new terminal
echo   2. Navigate to: %CD%\frontend
echo   3. Run: npm install (first time only)
echo   4. Run: npm start
echo.
echo ======================================================
echo   Backend is running!
echo   Press any key to open backend in browser...
echo ======================================================
pause >nul

start http://localhost:5000
