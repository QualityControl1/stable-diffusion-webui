@echo off
echo PyTorch Python 3.13 Compatibility Fix
echo =====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

echo Running PyTorch compatibility fix...
python fix_pytorch_python313.py

echo.
echo Fix completed! Check the output above for results.
echo.
pause
