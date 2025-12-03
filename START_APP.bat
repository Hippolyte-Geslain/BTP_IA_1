@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   PLATEFORME XP - Web Application
echo ========================================
echo.

REM Kill any existing processes on ports 5000 and 3000
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":5000 "') do taskkill /pid %%a /f 2>nul
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":3000 "') do taskkill /pid %%a /f 2>nul

timeout /t 1 /nobreak

echo Starting Backend (Flask - port 5000)...
start "Backend" cmd /k "cd /d "%~dp0backend" && python run.py"

timeout /t 3 /nobreak

echo Starting Frontend (React - port 3000)...
start "Frontend" cmd /k "cd /d "%~dp0" && call START_FRONTEND_ONLY.bat"

timeout /t 8 /nobreak

echo.
echo Opening http://localhost:3000 in browser...
start "" http://localhost:3000

echo.
echo ✓ Application started!
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:3000
echo.
