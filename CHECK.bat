@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   Checking Plateforme XP Setup
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python is installed
    for /f "tokens=*" %%a in ('python --version 2^>^&1') do echo   Version: %%a
) else (
    echo ✗ Python not found
    echo   Please install Python from https://www.python.org
    goto error
)

echo.

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Node.js is installed
    for /f "tokens=*" %%a in ('node --version 2^>^&1') do echo   Version: %%a
) else (
    echo ✗ Node.js not found
    echo   Please install Node.js from https://nodejs.org
    goto error
)

echo.

REM Check backend dependencies
echo Checking backend dependencies...
if exist "backend\requirements.txt" (
    echo ✓ Backend requirements.txt found
) else (
    echo ✗ Backend requirements.txt not found
    goto error
)

echo.

REM Check frontend dependencies
echo Checking frontend setup...
if exist "frontend\package.json" (
    echo ✓ Frontend package.json found
) else (
    echo ✗ Frontend package.json not found
    goto error
)

if exist "frontend\node_modules" (
    echo ✓ Frontend dependencies installed
) else (
    echo ✗ Frontend dependencies not installed
    echo   Run SETUP_WEB.bat first
    goto error
)

echo.
echo ========================================
echo   All checks passed!
echo ========================================
echo.
echo You can now run: START.bat
echo.
pause
goto end

:error
echo.
echo ========================================
echo   Setup issues found
echo ========================================
echo.
pause

:end
