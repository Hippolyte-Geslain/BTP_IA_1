@echo off
echo ================================================
echo    NETTOYAGE COMPLET DU CACHE PYTHON
echo ================================================
echo.
cd /d "%~dp0"

echo [1/4] Arret de tous les processus Python...
taskkill /F /IM python.exe /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/4] Suppression du dossier __pycache__...
if exist "__pycache__" rmdir /S /Q "__pycache__"

echo [3/4] Suppression des fichiers .pyc...
del /S /Q "*.pyc" >nul 2>&1

echo [4/4] Suppression des fichiers .pyo...
del /S /Q "*.pyo" >nul 2>&1

echo.
echo ================================================
echo    CACHE NETTOYE !
echo ================================================
echo.
echo Appuyez sur une touche pour lancer l'application...
pause >nul

python app_gui.py
