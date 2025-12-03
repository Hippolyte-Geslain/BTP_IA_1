@echo off
cd /d "%~dp0\frontend"

echo.
echo ========================================
echo   Cleaning and reinstalling dependencies
echo ========================================
echo.

REM Delete node_modules and package-lock.json
echo Cleaning old dependencies...
if exist "node_modules" (
    echo Removing node_modules...
    rmdir /s /q node_modules
)

if exist "package-lock.json" (
    echo Removing package-lock.json...
    del package-lock.json
)

echo.
echo Installing fresh dependencies...
echo This may take a few minutes...
echo.

REM Install with legacy peer deps flag
npm install --legacy-peer-deps

if %errorlevel% equ 0 (
    echo.
    echo ✓ Dependencies installed successfully!
    echo.
    echo You can now run: RUN_FRONTEND.bat
) else (
    echo.
    echo ✗ Installation failed
    echo Please try again or check Node.js installation
)

pause
