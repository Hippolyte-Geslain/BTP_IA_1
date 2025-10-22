@echo off
echo ========================================
echo   PLATEFORME XP - APPLICATION
echo ========================================
echo.
echo Installation des dependances...
python -m pip install --quiet qrcode Pillow
echo.
echo Lancement de l'application...
echo.
python test.py
echo.
pause
