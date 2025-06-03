@echo off
echo Fixing SGM open_clip Import Issues
echo ==================================
echo.
echo This will resolve the open_clip import error in the
echo generative-models repository for Python 3.13 compatibility.
echo.

echo Running SGM open_clip fix...
python fix_sgm_openclip.py

echo.
echo SGM fix completed! Try launching WebUI again.
echo.
pause
