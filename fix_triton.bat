@echo off
echo PyTorch Triton Conflict Fix
echo ===========================
echo.
echo This will fix the TORCH_LIBRARY triton namespace conflict
echo by installing a compatible PyTorch version.
echo.

REM Stop the current cu118 installation if running
echo Stopping any running pip processes...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 >nul

echo Running Triton conflict fix...
echo.
python fix_triton_conflict.py

echo.
echo Fix completed! 
echo If successful, use webui_triton_fix.bat to launch WebUI.
echo.
pause
