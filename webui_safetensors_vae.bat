@echo off
echo SAFETENSORS VAE FIX for PyTorch 2.6 Compatibility
echo =================================================
echo.
echo This script uses safetensors VAE format which is compatible
echo with PyTorch 2.6's new weights_only=True default.
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Use safetensors VAE (compatible with PyTorch 2.6)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-ema-560000-ema-pruned.safetensors"

echo Configuration: Safetensors VAE + Autocast Precision
echo Expected: Should fix PyTorch 2.6 compatibility issues
echo.
echo Test with simple prompt: "a red apple"
echo.

call webui.bat %*
