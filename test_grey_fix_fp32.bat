@echo off
echo VAE Test: Full Precision (FP32) - Grey Image Fix
echo =============================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Full precision arguments (should fix grey images)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision full --no-half --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-ema-560000-ema-pruned.safetensors"

echo Configuration: Full FP32 precision with safetensors VAE
echo Expected: Should fix grey images by using full precision
echo Test prompt: "a simple red apple on white background"
echo.
echo IMPORTANT: This will be slower but should produce proper images
echo If this works, grey images were caused by precision issues
echo.

call webui.bat %*
