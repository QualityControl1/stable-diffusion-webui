@echo off
echo Fixing Grey Image Generation Issues
echo ===================================
echo.
echo This will:
echo 1. Check your current VAE configuration
echo 2. Download a compatible VAE if needed
echo 3. Configure WebUI to use the VAE
echo 4. Create a fixed launch script
echo.

echo Running grey image fix...
python fix_grey_images.py

echo.
echo Grey image fix completed!
echo.
echo Next steps:
echo 1. Launch WebUI with: .\webui_vae_fixed.bat
echo 2. Generate a test image: "a red apple"
echo 3. Images should now show actual content
echo.
pause
