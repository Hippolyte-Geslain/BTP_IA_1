@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   Complete Frontend Reset
echo ========================================
echo.

cd frontend

echo Removing old files...
if exist "node_modules" rmdir /s /q node_modules
if exist "package-lock.json" del package-lock.json

echo.
echo Clearing npm cache...
call npm cache clean --force

echo.
echo Installing dependencies (this may take 10-15 minutes)...
call npm install

echo.
if %errorlevel% equ 0 (
    echo ✓ Installation successful!
) else (
    echo ✗ Installation failed - retrying with different flags
    call npm install --legacy-peer-deps --no-audit --no-fund
)

cd ..

echo.
echo ========================================
echo You can now run: RUN_FRONTEND.bat
echo ========================================
echo.
pause
