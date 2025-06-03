@echo off
echo PyTorch CUDA Fix for Python 3.13
echo ==================================
echo.
echo This will replace your CPU-only PyTorch with CUDA-enabled version
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

echo Running CUDA PyTorch fix...
echo.
python fix_pytorch_cuda.py

echo.
echo Fix completed! Check the output above for results.
echo If successful, use webui_env.bat to launch the WebUI.
echo.
pause
