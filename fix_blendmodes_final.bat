@echo off
echo Fixing blendmodes Import Error
echo ==============================
echo.
echo This will resolve the blendmodes import error in processing.py
echo while maintaining all Python 3.13 compatibility fixes.
echo.

echo Running blendmodes fix...
python fix_blendmodes_final.py

echo.
echo blendmodes fix completed!
echo.
echo Now launch WebUI with: .\webui_gpu_rtx3080_final.bat
echo.
pause
