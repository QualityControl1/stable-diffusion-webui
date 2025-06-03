@echo off
echo QUICK FIX for VAE Noise/Static Issue
echo =====================================
echo.
echo This script uses the anime-optimized VAE which often fixes
echo noise issues with NSFW and custom models.
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Use anime VAE with autocast precision (most compatible)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/kl-f8-anime2.ckpt"

echo Configuration: Anime VAE + Autocast Precision
echo Expected: Should fix colorful noise/static
echo.
echo Test with simple prompt: "a red apple"
echo.

call webui.bat %*
