@echo off
echo Windows Build Tools Fix for Python 3.13
echo ========================================
echo.
echo This will fix the sentencepiece/open_clip build issues
echo by installing required dependencies and using pre-built packages.
echo.

echo Running build tools fix...
python fix_build_tools.py

echo.
echo Fix completed! Try running webui.bat or webui_build_friendly.bat
echo.
pause
