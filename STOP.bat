@echo off
echo.
echo ========================================
echo   Stopping Plateforme XP...
echo ========================================
echo.

taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul

echo ✓ Backend stopped
echo ✓ Frontend stopped
echo.
echo Application stopped!
echo.
pause
