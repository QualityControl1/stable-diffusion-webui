@echo off
echo Installing Final WebUI Dependencies
echo ===================================
echo.
echo This will install tomesd and other remaining core
echo dependencies required for stable-diffusion-webui.
echo.

echo Installing final WebUI dependencies...
python install_final_webui_deps.py

echo.
echo Final dependencies installation completed!
echo WebUI should now be ready to launch with: .\webui_compatible.bat
echo.
pause
