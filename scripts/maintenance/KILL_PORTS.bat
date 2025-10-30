@echo off
echo ====================================
echo   NETTOYAGE DES PORTS
echo ====================================
echo.

echo Recherche des processus sur les ports 5000 et 3000...
echo.

REM Kill port 5000 (Backend)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do (
    echo Arret du processus %%a sur le port 5000...
    taskkill /F /PID %%a 2>nul
)

REM Kill port 3000 (Frontend)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    echo Arret du processus %%a sur le port 3000...
    taskkill /F /PID %%a 2>nul
)

echo.
echo ====================================
echo   PORTS NETTOYES
echo ====================================
echo.
pause
