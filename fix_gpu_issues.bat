@echo off
echo Fixing RTX 3080 GPU Acceleration Issues
echo =======================================
echo.
echo This will resolve:
echo - NumPy version conflicts
echo - Invalid command-line arguments  
echo - Missing xFormers installation
echo - GPU acceleration problems
echo.

echo Running comprehensive GPU fixes...
python fix_gpu_issues.py

echo.
echo GPU issues fix completed!
echo.
echo Try launching with:
echo - webui_gpu_rtx3080_fixed.bat (recommended)
echo - webui_gpu_rtx3080_balanced.bat (updated)
echo.
pause
