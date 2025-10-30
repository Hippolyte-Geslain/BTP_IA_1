@echo off
title Plateforme XP - Lancement
color 0A
echo.
echo ========================================
echo   PLATEFORME XP - APPLICATION COMPLETE
echo ========================================
echo.
echo Installation des dependances...
pip install customtkinter --quiet
echo.
echo Lancement de l'application...
python app_moderne.py
pause
