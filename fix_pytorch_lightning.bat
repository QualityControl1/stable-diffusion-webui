@echo off
echo Fixing PyTorch Lightning Import Issues
echo ======================================
echo.
echo This will fix pytorch_lightning.utilities.distributed
echo import errors across all repository files.
echo.

echo Running PyTorch Lightning import fix...
python fix_pytorch_lightning_imports.py

echo.
echo PyTorch Lightning fix completed!
echo Try launching WebUI again with: .\webui_compatible.bat
echo.
pause
