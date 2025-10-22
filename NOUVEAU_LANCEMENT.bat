@echo off
echo ================================================
echo    PLATEFORME XP - Nouveau Lancement
echo ================================================
echo.
echo Arret des anciennes instances...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo.
echo Lancement de l'application...
echo.
cd /d "%~dp0"
python app_gui.py
pause
