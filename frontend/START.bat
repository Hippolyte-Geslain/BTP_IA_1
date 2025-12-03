@echo off
setlocal enabledelayedexpansion

title Plateforme XP - Frontend

REM Aller au répertoire frontend
cd /d "%~dp0"

echo ==================================================
echo PLATEFORME XP - Frontend
echo ==================================================
echo.
echo Démarrage du serveur React en cours...
echo L'application s'ouvrira automatiquement sur http://localhost:3000
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur.
echo.

REM Utiliser set pour les variables d'environnement sur Windows
set SKIP_PREFLIGHT_CHECK=true
call npm start

pause
