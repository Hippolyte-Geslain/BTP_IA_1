@echo off
cd /d "%~dp0\frontend"

echo.
echo ========================================
echo   Starting Frontend (React)
echo ========================================
echo.
echo Server will start on http://localhost:3000
echo Press CTRL+C to stop
echo.

set SKIP_PREFLIGHT_CHECK=true
npm start

pause
