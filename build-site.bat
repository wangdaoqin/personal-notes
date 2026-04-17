@echo off
cls

REM Build Notes Website
echo Building website...
echo.

REM Change to project directory
cd /d "E:\personal-notes"
echo Current directory: %cd%
echo.

REM Check if scripts directory exists
if exist "scripts" (
    echo scripts directory exists
) else (
    echo ERROR: scripts directory not found
    pause
    exit /b 1
)

REM Check if build.py exists
if exist "scripts\build.py" (
    echo build.py file exists
) else (
    echo ERROR: build.py file not found
    pause
    exit /b 1
)

REM Check Python availability
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not available
    pause
    exit /b 1
)

echo.
echo Running build script...
echo Command: python scripts\build.py
echo.

REM Run build script
python scripts\build.py

REM Check build result
if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    echo Please check the error messages above
) else (
    echo.
    echo BUILD SUCCESSFUL!
    echo Website updated in docs directory
)

echo.
echo Press any key to close...
pause >nul