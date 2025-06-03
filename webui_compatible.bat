@echo off
REM Compatible WebUI Configuration for Python 3.13
echo Starting WebUI with Python 3.13 compatibility...
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

REM Skip problematic package installations and GPU checks
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install --skip-torch-cuda-test

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch installation"

REM Skip CLIP packages (compatibility issues)
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM Disable xformers if problematic
set XFORMERS_PACKAGE=none

REM Set CPU optimization environment variables for better image generation
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
set OMP_NUM_THREADS=4
set MKL_NUM_THREADS=4
set PYTORCH_NO_CUDA_MEMORY_CACHING=1
set CUDA_VISIBLE_DEVICES=

REM Additional stability flags for CPU-only operation
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half --precision full --use-cpu all --no-half-vae --opt-sub-quad-attention

echo Configuration:
echo - Python 3.13 compatibility mode
echo - Skipping CLIP installation (compatibility issues)
echo - Using existing PyTorch installation
echo - Skipping GPU/CUDA tests (CPU-only mode)
echo - CPU-only processing enabled with optimizations
echo - Image generation stability flags enabled
echo - Memory optimization enabled
echo.

call webui.bat %*
