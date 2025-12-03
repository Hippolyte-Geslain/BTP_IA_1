@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ========================================
echo   PLATEFORME XP - Interface Web
echo ========================================
echo.

REM Kill any existing Python or Node processes on ports 5000 and 3000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000 "') do taskkill /pid %%a /f 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000 "') do taskkill /pid %%a /f 2>nul

timeout /t 1 /nobreak

echo Starting Backend (Flask) on port 5000...
start "Backend Flask" cmd /k "cd /d "%~dp0backend" && python run.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo Starting Frontend (React) on port 3000...
start "Frontend React" cmd /k "cd /d "%~dp0frontend" && npm start"

echo Waiting for frontend to start...
timeout /t 10 /nobreak

echo.
echo ========================================
echo   Opening browser...
echo ========================================
echo.

timeout /t 2 /nobreak
start "" http://localhost:3000

echo.
echo ✓ Application web lancée!
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul

