@echo off
echo.
echo ======================================================
echo   PLATEFORME XP - COMPLETE STARTUP SCRIPT
echo ======================================================
echo.

cd /d "%~dp0"

echo [1/3] Starting Backend Server...
cd backend
start "Plateforme XP Backend" cmd /k "python run.py"
cd ..

echo [2/3] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo [3/3] Opening browser...
start http://localhost:5000

echo.
echo ======================================================
echo   Backend Started Successfully!
echo ======================================================
echo.
echo Backend API: http://localhost:5000
echo Health Check: http://localhost:5000/health
echo.
echo To start the FRONTEND:
echo   1. Open a NEW terminal
echo   2. Run: cd frontend
echo   3. Run: npm install (first time only)
echo   4. Run: npm start
echo   5. Access: http://localhost:3000
echo.
echo Test Account:
echo   Email: test
echo   Password: test123
echo.
echo ======================================================
echo Press any key to exit...
pause >nul
