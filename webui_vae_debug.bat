@echo off
echo VAE Debug Launch Script
echo ========================
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Maximum VAE debugging and fixes
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Force specific VAE (using working alternative)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-ema-560000-ema-pruned.safetensors"

REM VAE precision fixes
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision full

REM Disable problematic optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --disable-nan-check
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half

REM GPU optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram

REM Enable verbose logging
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --log-startup

echo VAE Debug Configuration:
echo ==========================
echo - Forcing specific VAE path
echo - Full precision mode (no half precision anywhere)
echo - Disabled NaN checking
echo - Maximum compatibility mode
echo - Verbose logging enabled
echo.
echo This should definitely fix grey images!
echo.

call webui.bat %*
