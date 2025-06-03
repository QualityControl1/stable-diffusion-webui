@echo off
echo Starting WebUI with VAE fixes for grey image issue...
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM VAE-specific fixes for grey images
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram

REM CRITICAL: Force VAE to not use half precision (fixes grey images)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae

REM Additional stability flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-sub-quad-attention

echo VAE Configuration for Grey Image Fix:
echo =====================================
echo - VAE file: vae-ft-mse-840000-ema-pruned.safetensors
echo - Forcing full precision VAE (--no-half-vae) - CRITICAL FIX
echo - GPU acceleration enabled (RTX 3080)
echo - Memory optimization enabled
echo - This should completely fix grey image generation
echo.
echo Expected result: Actual images instead of grey squares
echo.

call webui.bat %*
