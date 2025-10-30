@echo off
echo ====================================
echo   REORGANISATION DES DOCS
echo ====================================
echo.
echo Ce script va reorganiser les fichiers de documentation.
echo Consultez REORGANIZATION_PLAN.md pour les details.
echo.
echo Appuyez sur une touche pour continuer ou CTRL+C pour annuler...
pause >nul

echo.
echo Creation de la structure...
mkdir docs 2>nul
mkdir docs\installation 2>nul
mkdir docs\guides 2>nul
mkdir docs\implementation 2>nul
mkdir docs\planning 2>nul
mkdir docs\reference 2>nul
mkdir docs\archive 2>nul
echo ✓ Structure creee

echo.
echo Deplacement des fichiers...

REM Installation
if exist INSTALLATION_COMPLETE.md (
    move INSTALLATION_COMPLETE.md docs\installation\ >nul
    echo ✓ Installation: 1 fichier
)

REM Guides
if exist QUICK_REFERENCE.md move QUICK_REFERENCE.md docs\guides\ >nul
if exist NAVIGATION_QUICK_REF.txt move NAVIGATION_QUICK_REF.txt docs\guides\ >nul
if exist TROUBLESHOOTING.md move TROUBLESHOOTING.md docs\guides\ >nul
echo ✓ Guides: 3 fichiers

REM Implementation
if exist TASK_IMPLEMENTATIONS.md move TASK_IMPLEMENTATIONS.md docs\implementation\ >nul
if exist TASK_SUMMARY.md move TASK_SUMMARY.md docs\implementation\ >nul
if exist WEB_VERSION_COMPLETE.md move WEB_VERSION_COMPLETE.md docs\implementation\ >nul
if exist NAVIGATION_IMPLEMENTATION.md move NAVIGATION_IMPLEMENTATION.md docs\implementation\ >nul
if exist NAVIGATION_ADDED.md move NAVIGATION_ADDED.md docs\implementation\ >nul
echo ✓ Implementation: 5 fichiers

REM Planning
if exist ROADMAP_RAPIDE.md move ROADMAP_RAPIDE.md docs\planning\ >nul
if exist EVOLUTIONS_REQUISES.md move EVOLUTIONS_REQUISES.md docs\planning\ >nul
if exist ACTIONS_IMMEDIATES.md move ACTIONS_IMMEDIATES.md docs\planning\ >nul
if exist AVANT_APRES.md move AVANT_APRES.md docs\planning\ >nul
echo ✓ Planning: 4 fichiers

REM Reference
if exist INDEX_PRINCIPAL.md move INDEX_PRINCIPAL.md docs\reference\ >nul
if exist MASTER_INDEX.md move MASTER_INDEX.md docs\reference\ >nul
if exist CHECKLIST_COMPLETUDE.txt move CHECKLIST_COMPLETUDE.txt docs\reference\ >nul
if exist LIRE_MOI_DABORD.txt move LIRE_MOI_DABORD.txt docs\reference\ >nul
if exist RESUME_FINAL.txt move RESUME_FINAL.txt docs\reference\ >nul
if exist VISUALISATION.txt move VISUALISATION.txt docs\reference\ >nul
echo ✓ Reference: 6 fichiers

echo.
echo Archivage des doublons...
if exist docs\implementation\TASK_SUMMARY.md move docs\implementation\TASK_SUMMARY.md docs\archive\ >nul
if exist docs\reference\LIRE_MOI_DABORD.txt move docs\reference\LIRE_MOI_DABORD.txt docs\archive\ >nul
if exist docs\reference\RESUME_FINAL.txt move docs\reference\RESUME_FINAL.txt docs\archive\ >nul
echo ✓ 3 doublons archives

echo.
echo Creation de l'index...
(
echo # 📚 INDEX DE LA DOCUMENTATION
echo.
echo Derniere mise a jour: %date% %time%
echo.
echo ## 📂 Structure
echo.
echo ### Installation
echo - [Installation Complete](installation/INSTALLATION_COMPLETE.md^)
echo.
echo ### Guides
echo - [Reference Rapide](guides/QUICK_REFERENCE.md^)
echo - [Navigation](guides/NAVIGATION_QUICK_REF.txt^)
echo - [Troubleshooting](guides/TROUBLESHOOTING.md^)
echo.
echo ### Implementation
echo - [Implementations des Taches](implementation/TASK_IMPLEMENTATIONS.md^)
echo - [Version Web Complete](implementation/WEB_VERSION_COMPLETE.md^)
echo - [Navigation Implementation](implementation/NAVIGATION_IMPLEMENTATION.md^)
echo - [Navigation Ajoutee](implementation/NAVIGATION_ADDED.md^)
echo.
echo ### Planning
echo - [Roadmap Rapide](planning/ROADMAP_RAPIDE.md^)
echo - [Evolutions Requises](planning/EVOLUTIONS_REQUISES.md^)
echo - [Actions Immediates](planning/ACTIONS_IMMEDIATES.md^)
echo - [Avant/Apres](planning/AVANT_APRES.md^)
echo.
echo ### Reference
echo - [Index Principal](reference/INDEX_PRINCIPAL.md^)
echo - [Master Index](reference/MASTER_INDEX.md^)
echo - [Checklist](reference/CHECKLIST_COMPLETUDE.txt^)
echo - [Visualisation](reference/VISUALISATION.txt^)
echo.
echo ### Archive
echo - [Fichiers Archives](archive/^)
) > docs\README.md
echo ✓ Index cree

echo.
echo ====================================
echo   REORGANISATION TERMINEE
echo ====================================
echo.
echo Fichiers deplaces: 19
echo Fichiers archives: 3
echo Fichiers conserves a la racine: 5
echo.
echo Consultez docs\README.md pour l'index complet
echo.
pause
