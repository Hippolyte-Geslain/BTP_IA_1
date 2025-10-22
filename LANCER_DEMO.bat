@echo off
echo ========================================
echo   PLATEFORME XP - DEMO AUTOMATIQUE
echo ========================================
echo.
echo Installation des dependances...
python -m pip install --quiet qrcode Pillow
echo.
echo Lancement de la demo...
echo.
python demo.py
echo.
echo ========================================
echo   DEMO TERMINEE !
echo ========================================
pause
