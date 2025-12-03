@echo off
setlocal enabledelayedexpansion

echo ==================================================
echo NETTOYAGE ET DEMARRAGE - PLATEFORME XP
echo ==================================================

REM Arrêter tout processus Node en cours
taskkill /IM node.exe /F /T 2>nul

REM Attendre un peu
timeout /t 2 /nobreak

REM Aller au répertoire frontend
cd /d "%~dp0"
echo Répertoire courant: %cd%

REM Nettoyage
echo.
echo Nettoyage du cache npm...
call npm cache clean --force

REM Supprimer node_modules et package-lock
echo Suppression de node_modules...
if exist node_modules (
    rmdir /s /q node_modules
    echo node_modules supprimé
)

if exist package-lock.json (
    del package-lock.json
    echo package-lock.json supprimé
)

REM Réinstaller les dépendances
echo.
echo Installation des dépendances npm...
call npm install

REM Démarrer l'application
echo.
echo ==================================================
echo Démarrage de l'application React...
echo ==================================================
echo Accédez à http://localhost:3000
echo.

call npm start
pause
