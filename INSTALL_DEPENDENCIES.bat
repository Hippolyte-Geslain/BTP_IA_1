@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================
echo Installation des dependances Python
echo ================================================
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Erreur lors de l'installation.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Dependances installes avec succes!
echo ================================================
echo.
pause
