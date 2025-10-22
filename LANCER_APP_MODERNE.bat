@echo off
title Plateforme XP - Application Moderne
color 0B
echo.
echo ========================================
echo   INSTALLATION ET LANCEMENT
echo ========================================
echo.
echo Installation de CustomTkinter...
python -m pip install customtkinter pillow --quiet
echo.
echo Lancement de l'application moderne...
echo.
python app_moderne.py
pause
