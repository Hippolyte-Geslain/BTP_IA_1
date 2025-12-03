@echo off
setlocal enabledelayedexpansion

title Plateforme XP - Backend Python

REM Aller au répertoire backend
cd /d "%~dp0"

echo ==================================================
echo PLATEFORME XP - Backend Python
echo ==================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis python.org
    pause
    exit /b 1
)

echo Python détecté:
python --version
echo.

REM Créer un environnement virtuel s'il n'existe pas
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dépendances Python...
pip install -r requirements.txt

REM Démarrer le serveur Flask
echo.
echo ==================================================
echo Démarrage du serveur Flask sur http://localhost:5000
echo ==================================================
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur.
echo.

python app.py

pause
