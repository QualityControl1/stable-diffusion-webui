@echo off
REM RTX 3080 GPU Launch Script (Working Version)
echo Starting WebUI with RTX 3080 GPU acceleration...
echo.

REM Install dependencies if needed
echo Checking dependencies...
python -c "import numpy; import torch; print('Dependencies OK')" || (
    echo Installing missing dependencies...
    pip install "numpy>=1.21.0,<2.0.0" "blendmodes==2022" --quiet
)

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM WebUI configuration
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set TORCH_COMMAND=echo "Using existing PyTorch installation"
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM RTX 3080 optimization flags (WebUI v1.10.1 compatible)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae

REM Enable xFormers if available
python -c "import xformers" >nul 2>&1 && (
    set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers
    echo xFormers enabled for maximum performance
) || (
    echo xFormers not available - using standard attention
)

echo RTX 3080 Configuration:
echo - Target: 15-25 seconds per 512x512 image
echo - VRAM: Medium usage (8-12GB)
echo - Compatibility: Python 3.13 preserved
echo.

call webui.bat %*
