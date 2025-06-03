@echo off
echo VAE Test: Complete FP32 Conversion - Final Fix
echo ===============================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM GPU environment variables for stability
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Complete FP32 conversion (should fix type mismatch)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision full --no-half --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --upcast-sampling --disable-safe-unpickle
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-ema-560000-ema-pruned.safetensors"

echo Configuration: Complete FP32 with upcast sampling
echo Expected: Should fix type mismatch causing grey images
echo Test prompt: "a simple red apple on white background"
echo.
echo IMPORTANT: This forces all operations to FP32
echo If this works, the issue was mixed precision in the model
echo.

call webui.bat %*
