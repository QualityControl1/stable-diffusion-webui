@echo off
REM Maximum speed (requires 8GB+ VRAM)
echo Starting WebUI with GPU acceleration - Maximum speed (requires 8GB+ VRAM)...
echo.

REM Install dependencies (same as GPU config)
echo Installing core dependencies...
pip install packaging setuptools wheel --upgrade --quiet
pip install "pytorch_lightning>=2.0.0,<3.0.0" torchmetrics --upgrade --quiet
pip install omegaconf safetensors accelerate --upgrade --quiet
pip install diskcache jsonmerge inflection --upgrade --quiet
pip install "gradio==3.41.2" "pydantic>=1.10.0,<2.0.0" fastapi uvicorn --upgrade --quiet
pip install tomesd einops kornia --upgrade --quiet
pip install "numpy>=2.0.2" --upgrade --quiet
echo Core dependencies installed.
echo.

REM GPU optimization environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Configuration flags
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install --precision autocast --opt-split-attention --no-half-vae --opt-channelslast

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch installation"

echo GPU Configuration: Maximum speed (requires 8GB+ VRAM)
echo.

call webui.bat %*
