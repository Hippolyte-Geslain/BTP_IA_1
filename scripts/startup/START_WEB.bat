@echo off
echo.
echo ========================================================
echo   STARTING PLATEFORME XP - WEB VERSION
echo ========================================================
echo.

REM Kill any existing processes on ports 5000 and 3000
echo [1/3] Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 2 >nul
echo    Done!
echo.

REM Start Backend
echo [2/3] Starting Backend Server (port 5000)...
cd backend
start "Backend - Plateforme XP" cmd /k "python run.py"
cd ..
timeout /t 5 >nul
echo    Backend started!
echo.

REM Start Frontend
echo [3/3] Starting Frontend Server (port 3000)...
cd frontend
start "Frontend - Plateforme XP" cmd /k "npm start"
cd ..
echo    Frontend starting...
echo.

echo ========================================================
echo   SERVERS STARTED!
echo ========================================================
echo.
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:3000
echo.
echo   Login: test / test123
echo.
echo   Press any key to open browser...
echo ========================================================
pause >nul

start http://localhost:3000

echo.
echo Browser opened! Enjoy your web app!
echo.
echo To stop servers: Close the Backend and Frontend windows
echo.
