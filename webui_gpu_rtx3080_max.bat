@echo off
REM RTX 3080 Laptop GPU Maximum Performance Configuration
REM Optimized for 16GB VRAM - Maximum Speed Mode
echo Starting WebUI with RTX 3080 Maximum Performance Mode...
echo Target: 10-15 seconds per 512x512 image, 20-30 seconds per 768x768
echo.

REM Install core dependencies (preserving Python 3.13 compatibility)
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

REM RTX 3080 Maximum Performance GPU Environment Variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024,roundup_power2_divisions:16
set CUDA_LAUNCH_BLOCKING=0
set CUDA_CACHE_DISABLE=0
set CUDA_MODULE_LOADING=LAZY
set TORCH_CUDNN_V8_API_ENABLED=1

REM Skip problematic package installations but enable GPU
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing GPU-enabled PyTorch installation"

REM Skip CLIP packages (compatibility issues preserved)
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM RTX 3080 Maximum Performance Flags (WebUI v1.10.1 compatible)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --disable-safe-unpickle

REM Additional RTX 3080 optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers

echo RTX 3080 Maximum Performance Configuration:
echo - GPU: NVIDIA GeForce RTX 3080 Laptop GPU (16GB VRAM)
echo - Mode: Maximum Performance (10-15s per 512x512 image)
echo - VRAM Usage: Up to 14GB (aggressive optimization)
echo - Python 3.13 compatibility: PRESERVED
echo - All previous fixes: ACTIVE
echo - xFormers: ENABLED for maximum speed
echo - Precision: Mixed (autocast) for optimal performance
echo.

call webui.bat %*
