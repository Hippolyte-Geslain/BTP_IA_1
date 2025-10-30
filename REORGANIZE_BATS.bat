@echo off
echo ====================================
echo   REORGANISATION DES SCRIPTS BAT
echo ====================================
echo.
echo Ce script va reorganiser les fichiers .bat.
echo Les scripts seront classes par fonction.
echo.
echo Appuyez sur une touche pour continuer ou CTRL+C pour annuler...
pause >nul

echo.
echo Creation de la structure...
mkdir scripts 2>nul
mkdir scripts\startup 2>nul
mkdir scripts\maintenance 2>nul
mkdir scripts\utilities 2>nul
mkdir scripts\archive 2>nul
echo ✓ Structure creee

echo.
echo Deplacement des fichiers...

REM Startup scripts
if exist START_ALL.bat (
    move START_ALL.bat scripts\startup\ >nul
    echo ✓ Startup: START_ALL.bat
)
if exist START_BACKEND.bat (
    move START_BACKEND.bat scripts\startup\ >nul
    echo ✓ Startup: START_BACKEND.bat
)
if exist START_WEB.bat (
    move START_WEB.bat scripts\startup\ >nul
    echo ✓ Startup: START_WEB.bat
)

REM Maintenance scripts
if exist NETTOYER_ET_RELANCER.bat (
    move NETTOYER_ET_RELANCER.bat scripts\maintenance\ >nul
    echo ✓ Maintenance: NETTOYER_ET_RELANCER.bat
)
if exist KILL_PORTS.bat (
    move KILL_PORTS.bat scripts\maintenance\ >nul
    echo ✓ Maintenance: KILL_PORTS.bat
)

REM Utilities scripts
if exist REORGANIZE_DOCS.bat (
    move REORGANIZE_DOCS.bat scripts\utilities\ >nul
    echo ✓ Utilities: REORGANIZE_DOCS.bat
)

echo.
echo Creation de l'index...
(
echo # 🔧 INDEX DES SCRIPTS BAT
echo.
echo Derniere mise a jour: %date% %time%
echo.
echo ## 📂 Structure
echo.
echo ### Startup Scripts (scripts\startup\^)
echo Scripts de demarrage des services
echo.
echo - **START_ALL.bat** - Demarre tous les services (backend + frontend^)
echo - **START_BACKEND.bat** - Demarre uniquement le backend
echo - **START_WEB.bat** - Demarre uniquement le frontend web
echo.
echo ### Maintenance Scripts (scripts\maintenance\^)
echo Scripts de maintenance et nettoyage
echo.
echo - **NETTOYER_ET_RELANCER.bat** - Nettoie et relance les services
echo - **KILL_PORTS.bat** - Tue les processus sur les ports utilises
echo.
echo ### Utilities Scripts (scripts\utilities\^)
echo Scripts utilitaires divers
echo.
echo - **REORGANIZE_DOCS.bat** - Reorganise les fichiers de documentation
echo.
echo ### Archive (scripts\archive\^)
echo Scripts obsoletes ou remplaces
echo.
echo ## 🚀 Utilisation Rapide
echo.
echo ### Demarrage Normal
echo ```batch
echo scripts\startup\START_ALL.bat
echo ```
echo.
echo ### Demarrage Selectif
echo ```batch
echo REM Backend seulement
echo scripts\startup\START_BACKEND.bat
echo.
echo REM Frontend seulement
echo scripts\startup\START_WEB.bat
echo ```
echo.
echo ### Maintenance
echo ```batch
echo REM Nettoyage complet et redemarrage
echo scripts\maintenance\NETTOYER_ET_RELANCER.bat
echo.
echo REM Liberer les ports
echo scripts\maintenance\KILL_PORTS.bat
echo ```
echo.
echo ### Utilitaires
echo ```batch
echo REM Reorganiser la documentation
echo scripts\utilities\REORGANIZE_DOCS.bat
echo ```
echo.
echo ## ⚠️ Notes
echo.
echo - Tous les scripts doivent etre executes depuis la racine du projet
echo - Les scripts de startup ouvrent de nouvelles fenetres de terminal
echo - Les scripts de maintenance peuvent necessiter des privileges administrateur
echo.
) > scripts\README.md
echo ✓ Index cree

echo.
echo Creation d'un lanceur rapide...
(
echo @echo off
echo REM Lanceur rapide - Execute depuis la racine du projet
echo cd /d "%%~dp0.."
echo call scripts\startup\START_ALL.bat
) > scripts\QUICK_START.bat
echo ✓ Lanceur rapide cree

echo.
echo ====================================
echo   REORGANISATION TERMINEE
echo ====================================
echo.
echo Scripts deplaces:
echo   - Startup: 3
echo   - Maintenance: 2
echo   - Utilities: 1
echo   - Total: 6
echo.
echo Fichiers crees:
echo   - scripts\README.md (documentation^)
echo   - scripts\QUICK_START.bat (lanceur^)
echo.
echo ⚠️  Note: Ce script (REORGANIZE_BATS.bat^) reste a la racine
echo.
echo Consultez scripts\README.md pour l'index complet
echo.
pause
