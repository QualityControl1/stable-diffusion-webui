@echo off
echo Simple RTX 3080 GPU Fix
echo =======================
echo.
echo This will fix the blendmodes version error and
echo complete your GPU acceleration setup.
echo.

echo Running simple GPU fix...
python fix_gpu_simple.py

echo.
echo Simple fix completed!
echo.
echo Launch WebUI with: .\webui_gpu_working.bat
echo.
pause
