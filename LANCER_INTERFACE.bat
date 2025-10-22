@echo off
echo ========================================
echo   PLATEFORME XP - INTERFACE GRAPHIQUE
echo ========================================
echo.
echo Installation des dependances...
python -m pip install --quiet qrcode Pillow
echo.
echo Lancement de l'interface...
echo.
python app_gui.py
echo.
pause
