@echo off
echo Fixing UI Compatibility Issues
echo ==============================
echo.
echo This will fix Pydantic v2, Gradio version, and NumPy
echo compatibility issues preventing WebUI interface creation.
echo.

echo Running UI compatibility fix...
python fix_ui_compatibility.py

echo.
echo UI compatibility fix completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
