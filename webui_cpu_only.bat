@echo off
REM CPU-only configuration for Python 3.13 - Guaranteed compatibility
REM This will work without GPU but will be slower

echo Starting Stable Diffusion WebUI in CPU-only mode...
echo This mode is slower but avoids all CUDA/Triton conflicts
echo.

REM Set CPU-only PyTorch installation
set TORCH_COMMAND=pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cpu

REM Set CPU-only command line arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-torch-cuda-test --precision full --no-half --use-cpu all

REM Disable GPU-related packages
set XFORMERS_PACKAGE=none

echo Configuration:
echo - PyTorch: 2.7.0 CPU-only
echo - GPU: Disabled
echo - Precision: Full (CPU optimized)
echo - XFormers: Disabled
echo.
echo Note: Image generation will be slower but stable
echo.

call webui.bat %*
