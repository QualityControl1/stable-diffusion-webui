@echo off
echo VAE Test: Alternative VAE (MSE instead of EMA)
echo =============================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision full --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-mse-840000-ema-pruned.safetensors"

echo Configuration: MSE-trained VAE with full precision
echo Expected: Different VAE training may fix compatibility
echo Test prompt: "a simple red apple on white background"
echo.

call webui.bat %*
