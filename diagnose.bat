@echo off
echo Environment Diagnostic for stable-diffusion-webui
echo =================================================
echo.
echo This will diagnose your Python environment and create
echo a compatible WebUI configuration.
echo.

python diagnose_environment.py

echo.
echo Diagnostic completed! Check the output above for next steps.
echo If webui_compatible.bat was created, use it to launch WebUI.
echo.
pause
