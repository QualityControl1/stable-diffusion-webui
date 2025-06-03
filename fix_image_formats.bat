@echo off
echo Fixing Image Format Dependencies
echo ================================
echo.
echo This will fix pillow_avif and other image format
echo import issues for Python 3.13 compatibility.
echo.

echo Running image format fix...
python fix_image_formats.py

echo.
echo Image format fix completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
