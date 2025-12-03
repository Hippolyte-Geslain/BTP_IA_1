@echo off
setlocal enabledelayedexpansion

REM Script de démarrage complet et automatique - Plateforme XP

cls
echo ==================================================
echo PLATEFORME XP v2.0
echo ==================================================
echo.
echo Démarrage automatique...
echo.

REM Obtenir le répertoire courant
set PROJECT_DIR=%~dp0

REM Arrêter tout processus Node en cours
taskkill /IM node.exe /F /T 2>nul

REM Backend
echo [1/2] Démarrage du serveur Backend (Flask)...
start "Plateforme XP - Backend" cmd.exe /k "cd /d %PROJECT_DIR%backend && call START_BACKEND.bat"

REM Attendre que le backend démarre
timeout /t 5 /nobreak

REM Frontend
echo [2/2] Démarrage du serveur Frontend (React)...
start "Plateforme XP - Frontend" cmd.exe /k "cd /d %PROJECT_DIR%frontend && call START.bat"

echo.
echo ==================================================
echo Démarrage complet!
echo ==================================================
echo.
echo Serveurs disponibles:
echo - Backend:  http://localhost:5000
echo - Frontend: http://localhost:3000
echo.
echo Les deux terminaux se sont ouverts dans des fenêtres séparées.
echo Pour arrêter l'application:
echo   - Fermez les deux fenêtres de terminal
echo   - OU lancez: taskkill /IM node.exe /F
echo.

timeout /t 3

REM Ouvrir le navigateur sur le frontend
echo Ouverture du navigateur...
start http://localhost:3000

echo Terminé! Vérifiez les fenêtres de terminal pour les logs.
pause
