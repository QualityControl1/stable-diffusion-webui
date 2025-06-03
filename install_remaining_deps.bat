@echo off
echo Installing Remaining WebUI Dependencies
echo =======================================
echo.
echo This will install diskcache and other remaining
echo dependencies required for stable-diffusion-webui.
echo.

echo Installing remaining dependencies...
python install_remaining_deps.py

echo.
echo Remaining dependencies installation completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
