@echo off
echo VAE Test: CPU-Only Mode - Maximum Compatibility
echo ===============================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --use-cpu all --precision full
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-ema-560000-ema-pruned.safetensors"

echo Configuration: CPU-only processing with full precision
echo Expected: Very slow but maximum compatibility
echo Test prompt: "a simple red apple on white background"
echo.
echo WARNING: This will be VERY slow but should work if GPU has issues
echo.

call webui.bat %*
