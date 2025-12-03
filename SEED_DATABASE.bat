@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================
echo Initialisation de la base de donnees
echo ================================================
echo.

cd /d "%~dp0\backend"

if exist "plateforme_xp.db" (
    echo Base de donnees detectee.
    echo.
)

echo En cours d'initialisation...
python seed_db.py

if errorlevel 1 (
    echo.
    echo Erreur lors de l'initialisation.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Base de donnees initialisee avec succes!
echo ================================================
echo.
pause
