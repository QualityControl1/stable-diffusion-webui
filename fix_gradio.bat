@echo off
echo Fixing Gradio Compatibility Issues
echo ==================================
echo.
echo This will fix Gradio version compatibility issues
echo between WebUI v1.10.1 and newer Gradio versions.
echo.

echo Running Gradio compatibility fix...
python fix_gradio_compatibility.py

echo.
echo Gradio compatibility fix completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
