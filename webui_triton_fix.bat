@echo off
REM PyTorch Triton-Compatible Configuration for Python 3.13
REM This configuration attempts to work around triton namespace conflicts

echo Starting Stable Diffusion WebUI with Triton workarounds...
echo Python 3.13 detected - using compatibility mode
echo.

REM Set PyTorch installation command
set TORCH_COMMAND=pip install torch==2.7.0 torchvision==0.22.0 --extra-index-url https://download.pytorch.org/whl/cu121

REM Set command line arguments to avoid triton conflicts
set COMMANDLINE_ARGS=--skip-python-version-check --disable-safe-unpickle --no-half-vae

REM Disable xformers to avoid additional triton conflicts
set XFORMERS_PACKAGE=none

REM Set CUDA memory management
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

REM Disable triton compilation cache
set TRITON_CACHE_DIR=

echo Configuration:
echo - PyTorch: 2.7.0 with CUDA 12.1
echo - Triton: Disabled/Workarounds enabled
echo - XFormers: Disabled
echo - Memory management: Optimized
echo.

call webui.bat %*
