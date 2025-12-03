@echo off
setlocal enabledelayedexpansion

title Plateforme XP - Frontend

REM Aller au répertoire frontend
cd /d "%~dp0"

echo ==================================================
echo PLATEFORME XP - Frontend
echo ==================================================
echo.

REM Vérifier si Node est installé
node --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Node.js n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Node.js depuis nodejs.org
    pause
    exit /b 1
)

REM Vérifier et installer les dépendances si nécessaire
if not exist node_modules (
    echo Installation des dépendances npm...
    call npm install --legacy-peer-deps
    echo.
)

echo Démarrage du serveur React en cours...
echo L'application s'ouvrira automatiquement sur http://localhost:3000
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur.
echo.

REM Utiliser set pour les variables d'environnement sur Windows
set SKIP_PREFLIGHT_CHECK=true
call npm start

pause
