@echo off
echo Installing Core Dependencies for Python 3.13
echo ============================================
echo.
echo This will install the missing 'packaging' module and other
echo essential dependencies required for WebUI initialization.
echo.

echo Installing core dependencies...
python install_core_deps.py

echo.
echo Core dependencies installation completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
