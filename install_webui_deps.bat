@echo off
echo Installing WebUI Dependencies for Python 3.13
echo =============================================
echo.
echo This will install pytorch_lightning and other essential
echo dependencies required for stable-diffusion-webui.
echo.

echo Installing WebUI dependencies...
python install_webui_deps.py

echo.
echo WebUI dependencies installation completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
