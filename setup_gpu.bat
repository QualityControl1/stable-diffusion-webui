@echo off
echo Setting Up GPU Acceleration
echo ===========================
echo.
echo This will configure GPU acceleration for your WebUI
echo while preserving all Python 3.13 compatibility fixes.
echo.

echo Running GPU acceleration setup...
python setup_gpu_acceleration.py

echo.
echo GPU setup completed!
echo Check the output above for next steps and configuration files.
echo.
pause
