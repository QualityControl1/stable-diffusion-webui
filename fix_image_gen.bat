@echo off
echo Fixing Image Generation Issues
echo ==============================
echo.
echo This will diagnose and fix grey/blank image generation
echo issues in CPU-only mode with Python 3.13.
echo.

echo Running image generation fix...
python fix_image_generation.py

echo.
echo Image generation fix completed!
echo Restart WebUI with: .\webui_compatible.bat
echo.
pause
