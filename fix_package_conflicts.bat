@echo off
echo Fixing Package Installation Conflicts
echo =====================================
echo.
echo This will resolve:
echo - NumPy 2.2.6 downgrade to 1.26.4 (gradio compatible)
echo - blendmodes installation failures
echo - xFormers installation for PyTorch 2.7.0+cu118
echo - Package dependency conflicts
echo.

echo Running package conflicts fix...
python fix_package_conflicts.py

echo.
echo Package conflicts fix completed!
echo.
echo Launch WebUI with: .\webui_gpu_optimized.bat
echo.
pause
