@echo off
REM GPU-Optimized WebUI Configuration for Python 3.13
echo Starting WebUI with Python 3.13 compatibility and GPU acceleration...
echo.

REM Install core dependencies that might be missing from venv
echo Installing core dependencies and WebUI requirements...
pip install packaging setuptools wheel --upgrade --quiet
pip install "pytorch_lightning>=2.0.0,<3.0.0" torchmetrics --upgrade --quiet
pip install omegaconf safetensors accelerate --upgrade --quiet
pip install diskcache jsonmerge inflection --upgrade --quiet
pip install "gradio==3.41.2" "pydantic>=1.10.0,<2.0.0" fastapi uvicorn --upgrade --quiet
pip install tomesd einops kornia --upgrade --quiet
pip install "numpy>=2.0.2" --upgrade --quiet
echo Attempting pillow_avif installation (may fail on Python 3.13)...
pip install pillow_avif --quiet || echo "pillow_avif installation failed - AVIF support disabled"
echo Attempting open_clip installation (may fail on Python 3.13)...
pip install open-clip-torch --no-deps --quiet || echo "open_clip installation failed - using fallback"
echo Core dependencies and WebUI requirements installed.
echo.

REM GPU optimization environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0
set CUDA_CACHE_DISABLE=0
set CUDA_MODULE_LOADING=LAZY

REM Skip problematic package installations but allow GPU
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch installation"

REM Skip CLIP packages (compatibility issues)
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM GPU-optimized flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --opt-split-attention --opt-sub-quad-attention --opt-chunk-size 512

REM Memory optimization for GPU
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram --opt-channelslast

echo Configuration:
echo - Python 3.13 compatibility mode
echo - GPU acceleration enabled
echo - Memory optimization enabled
echo - Performance flags enabled
echo - CUDA optimizations active
echo.

call webui.bat %*
